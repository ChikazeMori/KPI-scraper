import csv, datetime, pathlib, requests
from bs4 import BeautifulSoup

BASE = "https://craft.co"

# --- load company → slug mapping ------------------------------------------------
TARGETS = {}
with open("targets.csv", newline="", encoding="utf-8") as f:
    next(f, None)                               # skip header row if present
    for name, path in csv.reader(f):
        if name:
            TARGETS[name] = ("/" + path.strip().lstrip("/"))

# --- scrape ---------------------------------------------------------------------
today = datetime.date.today().isoformat()
rows  = []

for name, slug in TARGETS.items():
    html  = requests.get(BASE + slug, timeout=15,
                         headers={"User-Agent": "Mozilla/5.0"}).text
    soup  = BeautifulSoup(html, "lxml")

    # 1. overview → first paragraph in the Overview section
    node = soup.select_one("section#overview p")
    overview = node.text.strip().replace("\n", " ") if node else "N/A"

    # 2. sectors → all sector pills under “Sectors”, joined by “; ”
    tags = [t.text.strip() for t in soup.select('a[data-attr="sector"]')]
    sectors = "; ".join(tags) if tags else "N/A"

    rows.append([today, name, overview, sectors])

# --- write / append -------------------------------------------------------------
outfile = pathlib.Path("genai_kpi.csv")
write_header = not outfile.exists()

with outfile.open("a", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    if write_header:
        w.writerow(["date", "company", "overview", "sectors"])
    w.writerows(rows)

print(f"{len(rows)} rows appended on {today}.")
