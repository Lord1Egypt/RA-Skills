#!/usr/bin/env python3
"""Fetch World Bank indicator data (free API, no key). Python 3.8+, stdlib only.

Usage:
  wb_data.py INDICATOR COUNTRIES [--date RANGE | --mrv N | --mrnev N] [--source ID] [--json]
  wb_data.py --search "keyword" [--all-sources]
  wb_data.py --aliases

INDICATOR is a World Bank code (NY.GDP.MKTP.CD) or a built-in alias (gdp).
COUNTRIES is a comma- or semicolon-separated list of ISO-2/ISO-3 codes,
aggregate codes (WLD, EUU, HIC...), or "all".

Examples:
  wb_data.py gdp US,JP,CN
  wb_data.py SP.POP.TOTL BR --date 2000:2024
  wb_data.py inflation all --mrv 1
  wb_data.py --search "renewable energy"

Exit codes: 0 success, 1 not found / no data, 2 API or network error.
"""

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.worldbank.org/v2"

ALIASES = {
    "gdp": "NY.GDP.MKTP.CD",
    "gdp-growth": "NY.GDP.MKTP.KD.ZG",
    "gdp-per-capita": "NY.GDP.PCAP.CD",
    "gdp-ppp": "NY.GDP.MKTP.PP.CD",
    "gni-per-capita": "NY.GNP.PCAP.CD",
    "population": "SP.POP.TOTL",
    "population-growth": "SP.POP.GROW",
    "inflation": "FP.CPI.TOTL.ZG",
    "unemployment": "SL.UEM.TOTL.ZS",
    "life-expectancy": "SP.DYN.LE00.IN",
    "fertility": "SP.DYN.TFRT.IN",
    "co2": "EN.GHG.CO2.PC.CE.AR5",
    "poverty": "SI.POV.DDAY",
    "gini": "SI.POV.GINI",
    "internet": "IT.NET.USER.ZS",
    "exports": "NE.EXP.GNFS.ZS",
    "imports": "NE.IMP.GNFS.ZS",
    "fdi": "BX.KLT.DINV.WD.GD.ZS",
    "exchange-rate": "PA.NUS.FCRF",
    "urban": "SP.URB.TOTL.IN.ZS",
    "literacy": "SE.ADT.LITR.ZS",
    "gov-debt": "GC.DOD.TOTL.GD.ZS",
    "remittances": "BX.TRF.PWKR.DT.GD.ZS",
    "military": "MS.MIL.XPND.GD.ZS",
    "electricity-access": "EG.ELC.ACCS.ZS",
    "health-expenditure": "SH.XPD.CHEX.GD.ZS",
    "current-account": "BN.CAB.XOKA.GD.ZS",
}


def fetch(path, **params):
    """GET a v2 path, return parsed [meta, rows]. Retries transient failures."""
    params.setdefault("format", "json")
    params.setdefault("per_page", 20000)
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    last_err = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "wb_data.py"})
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read().decode("utf-8-sig")
            # The API occasionally emits transient HTML error pages.
            if raw.lstrip().startswith("<"):
                raise ValueError("transient HTML error page from API")
            body = json.loads(raw)
            if isinstance(body, list) and body and isinstance(body[0], dict) \
                    and "message" in body[0]:
                msg = body[0]["message"][0]
                print(f"API error {msg.get('id')}: {msg.get('value')}", file=sys.stderr)
                if msg.get("id") == "175":
                    print("Hint: this indicator's data was archived; search for a "
                          "successor code (wb_data.py --search ...).", file=sys.stderr)
                sys.exit(1)
            return body
        except SystemExit:
            raise
        except Exception as err:  # noqa: BLE001 - retry any transport hiccup
            last_err = err
            time.sleep(1.5 * (attempt + 1))
    print(f"Request failed after retries: {last_err}\nURL: {url}", file=sys.stderr)
    sys.exit(2)


def cmd_search(keyword, all_sources):
    """Client-side keyword match over indicator names (the API has no text search)."""
    kw = keyword.lower()
    hits = []
    if all_sources:
        page, pages = 1, 1
        while page <= pages:
            meta, rows = fetch("/indicator", per_page=2000, page=page)
            pages = int(meta["pages"])
            hits += [r for r in rows if kw in r["name"].lower() or kw in r["id"].lower()]
            page += 1
    else:
        _, rows = fetch("/source/2/indicators", per_page=2000)  # WDI only: one request
        hits = [r for r in rows or [] if kw in r["name"].lower() or kw in r["id"].lower()]
    if not hits:
        scope = "all sources" if all_sources else "World Development Indicators"
        print(f"No indicator matching {keyword!r} in {scope}."
              + ("" if all_sources else " Try --all-sources."))
        sys.exit(1)
    for r in hits[:40]:
        src = r.get("source") or {}
        print(f"{r['id']:<28} {r['name']}  (source {src.get('id', '?')})")
    if len(hits) > 40:
        print(f"... and {len(hits) - 40} more matches")


def cmd_data(args):
    indicator = ALIASES.get(args.indicator.lower(), args.indicator)
    countries = args.countries.replace(",", ";")
    params = {}
    if args.date:
        params["date"] = args.date
    elif args.mrnev:
        params["mrnev"] = args.mrnev
    else:
        params["mrv"] = args.mrv
    if args.source:
        params["source"] = args.source
    body = fetch(f"/country/{countries}/indicator/{indicator}", **params)
    meta, rows = body[0], (body[1] if len(body) > 1 else None)
    if not rows:
        print("No data returned (country may not report this series, or the "
              "period is empty). Try --mrnev 1 for the latest available value.",
              file=sys.stderr)
        sys.exit(1)
    if args.json:
        json.dump(rows, sys.stdout, indent=2, ensure_ascii=False)
        print()
        return
    name = rows[0]["indicator"]["value"]
    print(f"{name} [{rows[0]['indicator']['id']}]  (source updated {meta.get('lastupdated', '?')})")
    current = None
    for r in rows:
        if r["country"]["value"] != current:
            current = r["country"]["value"]
            print(f"\n{current} ({r['countryiso3code'] or r['country']['id']})")
        val = r["value"]
        if val is None:
            shown = "—"
        elif isinstance(val, float) and abs(val) >= 1e6:
            shown = f"{val:,.0f}"
        elif isinstance(val, float):
            shown = f"{val:,.4g}"
        else:
            shown = f"{val:,}"
        print(f"  {r['date']:>8}  {shown}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("indicator", nargs="?", help="indicator code or alias")
    ap.add_argument("countries", nargs="?", help="country codes (comma/semicolon separated) or 'all'")
    ap.add_argument("--date", help="year or range: 2024, 2000:2024, 2025M01:2025M06")
    ap.add_argument("--mrv", type=int, default=5, help="most recent N periods (default 5)")
    ap.add_argument("--mrnev", type=int, help="most recent N non-empty values")
    ap.add_argument("--source", help="source id (needed outside WDI, e.g. 3 for governance)")
    ap.add_argument("--json", action="store_true", help="print raw JSON data rows")
    ap.add_argument("--search", metavar="KEYWORD", help="find indicator codes by keyword")
    ap.add_argument("--all-sources", action="store_true",
                    help="with --search: scan the full ~29,500-indicator catalog")
    ap.add_argument("--aliases", action="store_true", help="list built-in aliases")
    args = ap.parse_args()

    if args.aliases:
        for alias, code in sorted(ALIASES.items()):
            print(f"{alias:<20} {code}")
        return
    if args.search:
        cmd_search(args.search, args.all_sources)
        return
    if not args.indicator or not args.countries:
        ap.error("INDICATOR and COUNTRIES are required (or use --search / --aliases)")
    cmd_data(args)


if __name__ == "__main__":
    main()
