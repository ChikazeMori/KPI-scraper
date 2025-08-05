import csv, datetime, requests, pathlib
from bs4 import BeautifulSoup

BASE = "https://craft.co"
TARGETS = {}
for name, path in csv.reader(open("targets.csv")):
    if name: TARGETS[name] = path.strip()

today = datetime.date.today().isoformat()
rows = []

for name, path in TARGETS.items():
    if not path.startswith("/"):
        path = "/" + path            # auto-fix missing slash
    html = requests.get(BASE + path, timeout=15).text
    soup = BeautifulSoup(html, "lxml")
    try:
        hq      = soup.select_one('a[data-attr="hq"]').text.strip()
        founded = soup.select_one('span[data-attr="founded"]').text.strip()
        cyber   = soup.select_one('span[data-attr="cybersecurity-rating"]').text.strip()
    except AttributeError:
        visits = jobs = twitter = "N/A"
    rows.append([today, name, founded, hq, cyber])

file = pathlib.Path("genai_kpi.csv")
write_header = not file.exists()
with file.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow(["date", "company", "visits", "jobs", "twitter"])
    w.writerows(rows)

print(f"{len(rows)} rows appended on {today}.")
