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
        visits  = soup.select_one("span[data-attr='visits']").text.strip()
        jobs    = soup.select_one("span[data-attr='jobs']").text.strip()
        twitter = soup.select_one("a[data-attr='twitter']").text.strip()
    except AttributeError:
        visits = jobs = twitter = "N/A"
    rows.append([today, name, visits, jobs, twitter])

file = pathlib.Path("genai_kpi.csv")
write_header = not file.exists()
with file.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow(["date", "company", "visits", "jobs", "twitter"])
    w.writerows(rows)

print(f"{len(rows)} rows appended on {today}.")
