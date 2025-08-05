import csv, datetime, requests, pathlib
from bs4 import BeautifulSoup

BASE = "https://craft.co"
TARGETS = {}

reader = csv.reader(open("targets.csv"))
next(reader, None)                              # skip header
for name, path in reader:
    if name:
        TARGETS[name] = path.strip()

today = datetime.date.today().isoformat()
rows  = []

for name, path in TARGETS.items():
    if not path.startswith("/"):
        path = "/" + path                       # auto-fix missing slash

    html = requests.get(BASE + path, timeout=15).text
    soup = BeautifulSoup(html, "lxml")

    hq      = soup.select_one('a[data-attr="hq"]')
    hq      = hq.text.strip() if hq else "N/A"

    founded = soup.select_one('span[data-attr="founded"]')
    founded = founded.text.strip() if founded else "N/A"

    cyber   = soup.select_one('span[data-attr="cybersecurity-rating"]')
    cyber   = cyber.text.strip() if cyber else "N/A"

    rows.append([today, name, founded, hq, cyber])

file = pathlib.Path("genai_kpi.csv")
write_header = not file.exists()

with file.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow(["date", "company", "founded", "hq", "cyber"])
    w.writerows(rows)

print(f"{len(rows)} rows appended on {today}.")
