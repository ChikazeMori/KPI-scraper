import csv, re, time, requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

SEARCH = "https://www.bing.com/search?q="      # scrape-friendly
CRAFT  = "https://craft.co"

def craft_slug(name: str) -> str | None:
    query   = f"site:craft.co {name}"
    url     = f"https://www.bing.com/search?q={quote_plus(query)}"
    html    = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).text
    soup    = BeautifulSoup(html, "html.parser")

    # NEW selector — Bing now wraps result links in <li class="b_algo"> <a …>
    for a in soup.select("li.b_algo a[href^='https://craft.co']"):
        slug = a["href"].split("https://craft.co", 1)[1]
        return slug.strip()
    return None


good, bad = [], []
for name in csv.reader(open("candidate_companies.csv")):
    slug = craft_slug(name[0])
    (good if slug else bad).append([name[0], slug or ""])

    print(f"{'yes' if slug else 'no'} {name[0]}")

    time.sleep(2)                      # polite search-engine delay

# write results
with open("targets.csv", "w", newline="") as f:
    csv.writer(f).writerows(good)
with open("missing.csv", "w", newline="") as f:
    csv.writer(f).writerows(bad)

print(f"\nSaved {len(good)} verified companies to targets.csv")
print(f"Review {len(bad)} names in missing.csv")
