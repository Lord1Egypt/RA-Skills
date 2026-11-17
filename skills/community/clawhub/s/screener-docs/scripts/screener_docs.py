#!/usr/bin/env python3
"""
screener_docs.py - Download company documents listed on screener.in

For a stock name/symbol it:
  1. Resolves the company on screener.in (search API)
  2. Parses the "Documents" section of the company page
  3. Downloads, newest first:
       - Annual reports           (default max 3)
       - Concall transcripts      (default max 12)
       - Investor presentations   (default max 12)
       - Credit rating reports    (default max 3)
  4. Saves them under <out>/<SYMBOL>/<category>/ with a manifest.json

Usage:
  python3 screener_docs.py "Tata Consultancy"            # search + download
  python3 screener_docs.py TCS --out ~/stock-docs
  python3 screener_docs.py "HDFC" --list-matches          # just show matches
  python3 screener_docs.py "HDFC" --pick 2                # pick 2nd match
  python3 screener_docs.py https://www.screener.in/company/TCS/consolidated/
  python3 screener_docs.py TCS --dry-run                  # list, don't download

Dependencies: requests, beautifulsoup4
Optional env: SCREENER_SESSIONID  (sessionid cookie, only if screener asks for login)
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.stderr.write(
        "Missing dependencies. Install with:\n"
        "  python3 -m pip install requests beautifulsoup4\n"
    )
    sys.exit(2)

BASE = "https://www.screener.in"
SEARCH_API = BASE + "/api/company/search/"
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
)
MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

CATEGORIES = {
    "annual_reports": "annual_reports",
    "transcripts": "concall_transcripts",
    "presentations": "investor_presentations",
    "credit_ratings": "credit_ratings",
}


# --------------------------------------------------------------------------- #
# HTTP
# --------------------------------------------------------------------------- #
def make_session():
    s = requests.Session()
    s.headers.update({
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    })
    sid = os.environ.get("SCREENER_SESSIONID")
    if sid:
        s.cookies.set("sessionid", sid, domain="www.screener.in")
    return s


def referer_for(url):
    host = urlparse(url).netloc.lower()
    if "bseindia" in host:
        return "https://www.bseindia.com/"
    if "nseindia" in host:
        return "https://www.nseindia.com/"
    return BASE + "/"


# --------------------------------------------------------------------------- #
# Step 1: resolve company
# --------------------------------------------------------------------------- #
def search_company(session, query):
    r = session.get(SEARCH_API, params={"q": query, "v": 3, "fts": 1}, timeout=20)
    r.raise_for_status()
    results = r.json()
    # keep only company pages
    return [x for x in results if x.get("url", "").startswith("/company/")]


def resolve_company_url(session, query, pick=1):
    if query.startswith("http://") or query.startswith("https://"):
        return query, None
    matches = search_company(session, query)
    if not matches:
        raise SystemExit(f"No screener.in company found for '{query}'.")
    if pick < 1 or pick > len(matches):
        raise SystemExit(f"--pick {pick} out of range (1..{len(matches)}).")
    chosen = matches[pick - 1]
    return urljoin(BASE, chosen["url"]), matches


def symbol_from_url(url):
    m = re.search(r"/company/([^/]+)/", url)
    return m.group(1).upper() if m else "UNKNOWN"


# --------------------------------------------------------------------------- #
# Step 2: parse documents section
# --------------------------------------------------------------------------- #
def _block(soup, css_class, heading):
    """Find a documents sub-block by class, falling back to its <h3> heading."""
    blk = soup.select_one(f"#documents div.{css_class}") or soup.select_one(f"div.{css_class}")
    if blk:
        return blk
    for h in soup.find_all(["h3", "h2"]):
        if h.get_text(strip=True).lower().startswith(heading.lower()):
            return h.parent
    return None


def _clean(text):
    return re.sub(r"\s+", " ", text or "").strip()


def parse_month_year(text):
    """'Jul 2025' -> (2025, 7). Returns None if not parseable."""
    m = re.search(r"([A-Za-z]{3})[a-z]*\s+(\d{4})", text or "")
    if not m or m.group(1).lower() not in MONTHS:
        return None
    return int(m.group(2)), MONTHS[m.group(1).lower()]


def parse_day_month_year(text):
    """'3 Jun 2025' -> '2025-06-03'."""
    m = re.search(r"(\d{1,2})\s+([A-Za-z]{3})[a-z]*\s+(\d{4})", text or "")
    if not m or m.group(2).lower() not in MONTHS:
        return None
    return f"{int(m.group(3)):04d}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"


def parse_documents(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    docs = {k: [] for k in CATEGORIES}

    # ---- Annual reports ----
    blk = _block(soup, "annual-reports", "Annual reports")
    if blk:
        for a in blk.select("li a[href]"):
            label = _clean(a.get_text(" "))
            yr = re.search(r"(?:Financial Year|FY)\s*(\d{4})", label, re.I) or re.search(r"(\d{4})", label)
            year = int(yr.group(1)) if yr else None
            src = re.search(r"from\s+(\w+)", label)
            docs["annual_reports"].append({
                "label": label,
                "year": year,
                "source": src.group(1).lower() if src else None,
                "url": urljoin(page_url, a["href"]),
                "name": f"AR_FY{year}" if year else None,
            })
        # newest first
        docs["annual_reports"].sort(key=lambda d: d["year"] or 0, reverse=True)

    # ---- Credit ratings ----
    blk = _block(soup, "credit-ratings", "Credit ratings")
    if blk:
        for a in blk.select("li a[href]"):
            label = _clean(a.get_text(" "))
            date = parse_day_month_year(label)
            agency = re.search(r"from\s+([\w\-]+)", label)
            agency = agency.group(1).lower() if agency else "agency"
            docs["credit_ratings"].append({
                "label": label,
                "date": date,
                "source": agency,
                "url": urljoin(page_url, a["href"]),
                "name": f"{date or 'undated'}_{agency}",
            })
        docs["credit_ratings"].sort(key=lambda d: d["date"] or "", reverse=True)

    # ---- Concalls (transcripts + PPTs) ----
    blk = _block(soup, "concalls", "Concalls")
    if blk:
        for li in blk.select("li"):
            # date is the first non-link text in the row (e.g. "Jul 2025")
            date_el = li.find("div")
            date_txt = _clean(date_el.get_text(" ")) if date_el else _clean(li.get_text(" "))
            ym = parse_month_year(date_txt)
            tag = f"{ym[0]:04d}-{ym[1]:02d}" if ym else None
            for a in li.find_all("a", href=True):
                kind = (_clean(a.get_text(" ")) + " " + (a.get("title") or "")).lower()
                entry = {
                    "label": f"{date_txt} - {_clean(a.get_text(' '))}",
                    "date": tag,
                    "url": urljoin(page_url, a["href"]),
                }
                if "transcript" in kind:
                    entry["name"] = f"Transcript_{tag or 'undated'}"
                    docs["transcripts"].append(entry)
                elif "ppt" in kind or "presentation" in kind:
                    entry["name"] = f"PPT_{tag or 'undated'}"
                    docs["presentations"].append(entry)
                # "REC"/recordings and "Notes" are ignored
        for k in ("transcripts", "presentations"):
            docs[k].sort(key=lambda d: d["date"] or "", reverse=True)

    return docs


# --------------------------------------------------------------------------- #
# Step 3: download
# --------------------------------------------------------------------------- #
def _ext_for(resp, first_bytes, url):
    ctype = resp.headers.get("Content-Type", "").lower()
    if first_bytes.startswith(b"%PDF") or "pdf" in ctype:
        return ".pdf"
    if "html" in ctype:
        return ".html"
    path_ext = os.path.splitext(urlparse(url).path)[1].lower()
    if path_ext in (".pdf", ".ppt", ".pptx", ".doc", ".docx", ".zip", ".htm", ".html"):
        return path_ext
    if "zip" in ctype:
        return ".zip"
    return ".bin"


def _unique(path_no_ext, existing):
    name, i = path_no_ext, 2
    while name in existing:
        name = f"{path_no_ext}_{i}"
        i += 1
    existing.add(name)
    return name


def download(session, url, dest_no_ext, retries=2):
    # skip if already downloaded in a previous run
    folder = os.path.dirname(dest_no_ext)
    base = os.path.basename(dest_no_ext)
    if os.path.isdir(folder):
        for f in os.listdir(folder):
            if os.path.splitext(f)[0] == base and os.path.getsize(os.path.join(folder, f)) > 0:
                return os.path.join(folder, f), "skipped (exists)"

    last_err = None
    for attempt in range(retries + 1):
        try:
            with session.get(url, headers={"Referer": referer_for(url)},
                             timeout=60, stream=True, allow_redirects=True) as r:
                r.raise_for_status()
                it = r.iter_content(chunk_size=65536)
                first = next(it, b"")
                ext = _ext_for(r, first, r.url)
                path = dest_no_ext + ext
                os.makedirs(folder, exist_ok=True)
                with open(path, "wb") as fh:
                    fh.write(first)
                    for chunk in it:
                        fh.write(chunk)
            if os.path.getsize(path) < 1024 and ext == ".html":
                return path, "warning: tiny html (possibly blocked/redirect page)"
            return path, "ok"
        except Exception as e:  # noqa: BLE001
            last_err = e
            time.sleep(2 * (attempt + 1))
    return None, f"failed: {last_err}"


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Download screener.in company documents")
    ap.add_argument("query", help="Stock name, NSE/BSE symbol, or screener.in company URL")
    ap.add_argument("--out", default=os.path.expanduser("~/screener_docs"),
                    help="Root output folder (default: ~/screener_docs)")
    ap.add_argument("--pick", type=int, default=1, help="Which search match to use (1-based)")
    ap.add_argument("--list-matches", action="store_true", help="Only print search matches")
    ap.add_argument("--dry-run", action="store_true", help="Parse and list, don't download")
    ap.add_argument("--max-ar", type=int, default=3)
    ap.add_argument("--max-transcripts", type=int, default=12)
    ap.add_argument("--max-ppts", type=int, default=12)
    ap.add_argument("--max-ratings", type=int, default=3)
    ap.add_argument("--delay", type=float, default=1.0, help="Seconds between downloads")
    args = ap.parse_args()

    s = make_session()

    if args.list_matches:
        for i, m in enumerate(search_company(s, args.query), 1):
            print(f"{i}. {m.get('name')}  ->  {urljoin(BASE, m.get('url', ''))}")
        return

    url, matches = resolve_company_url(s, args.query, args.pick)
    if matches and len(matches) > 1:
        print("Search matches (use --pick N to choose another):")
        for i, m in enumerate(matches[:8], 1):
            mark = "*" if i == args.pick else " "
            print(f" {mark}{i}. {m.get('name')}  ({m.get('url')})")
    print(f"Company page: {url}")

    r = s.get(url, timeout=30)
    r.raise_for_status()
    docs = parse_documents(r.text, url)

    limits = {
        "annual_reports": args.max_ar,
        "transcripts": args.max_transcripts,
        "presentations": args.max_ppts,
        "credit_ratings": args.max_ratings,
    }
    for k in docs:
        docs[k] = docs[k][: max(0, limits[k])]

    symbol = symbol_from_url(url)
    root = os.path.join(os.path.expanduser(args.out), symbol)
    manifest = {
        "company_query": args.query,
        "symbol": symbol,
        "screener_url": url,
        "run_at": datetime.now().isoformat(timespec="seconds"),
        "documents": {},
    }

    for key, folder in CATEGORIES.items():
        items = docs[key]
        print(f"\n[{folder}] {len(items)} found")
        used = set()
        manifest["documents"][folder] = []
        for d in items:
            name = _unique(d.get("name") or "doc", used)
            if args.dry_run:
                print(f"  - {name}: {d['url']}")
                manifest["documents"][folder].append({**d, "file": None, "status": "dry-run"})
                continue
            path, status = download(s, d["url"], os.path.join(root, folder, name))
            print(f"  - {name}: {status}")
            manifest["documents"][folder].append({
                **d, "file": os.path.relpath(path, root) if path else None, "status": status})
            if not status.startswith("skipped"):
                time.sleep(args.delay)

    os.makedirs(root, exist_ok=True)
    with open(os.path.join(root, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)

    # summary
    print("\nSummary")
    for folder, rows in manifest["documents"].items():
        ok = sum(1 for x in rows if x["status"] in ("ok", "skipped (exists)"))
        print(f"  {folder:24s} {ok}/{len(rows)}")
    print(f"Saved to: {root}")


if __name__ == "__main__":
    main()
