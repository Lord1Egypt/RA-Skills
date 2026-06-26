#!/usr/bin/env python3
"""
Fetch structured financial data from SEC XBRL companyfacts.

Scope:
- Resolve company -> CIK
- Fetch structured financials from data.sec.gov
- Do NOT handle IR PDF downloading (use ir-pdf-downloader for documents)
"""

import argparse
import json
import re
import ssl
import sys
import textwrap
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path
from typing import Optional

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
XBRL_BASE = "https://data.sec.gov/api/xbrl"
EDGAR_BASE = "https://www.sec.gov/cgi-bin/browse-edgar"
ISSUERS_FILE = Path(__file__).resolve().parent.parent / "references" / "issuers.json"

REVENUE_CONCEPTS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "SalesRevenueNet",
    "SalesRevenueGoodsNet",
    "SalesRevenueServicesNet",
    "Revenues",
]
NET_INCOME_CONCEPTS = [
    "NetIncomeLossAvailableToCommonStockholdersBasic",
    "NetIncomeLoss",
    "ProfitLoss",
]
EPS_CONCEPTS = [
    "EarningsPerShareBasicAndDiluted",
    "BasicAndDilutedEarningsPerShare",
    "BasicEarningsPerShare",
    "DilutedEarningsPerShare",
]


def load_issuers() -> list[dict]:
    if not ISSUERS_FILE.exists():
        return []
    return json.loads(ISSUERS_FILE.read_text())


ISSUERS = load_issuers()
ALIAS_MAP = {}
for issuer in ISSUERS:
    for alias in issuer.get("aliases", []):
        ALIAS_MAP[alias.lower()] = issuer
    if issuer.get("name"):
        ALIAS_MAP[issuer["name"].lower()] = issuer
    if issuer.get("ticker"):
        ALIAS_MAP[issuer["ticker"].lower()] = issuer


def _secure_ctx() -> ssl.SSLContext:
    return ssl.create_default_context()


def _fallback_insecure_ctx() -> ssl.SSLContext:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _get_json(url: str, timeout: int = 20, retries: int = 2) -> dict:
    parsed = urllib.parse.urlparse(url)
    last_error = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "application/json",
                "Host": parsed.netloc,
            },
        )
        for ctx_factory in (_secure_ctx, _fallback_insecure_ctx):
            try:
                with urllib.request.urlopen(req, timeout=timeout, context=ctx_factory()) as resp:
                    return json.loads(resp.read())
            except ssl.SSLError as e:
                last_error = e
                continue
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries:
                    time.sleep(3 * (attempt + 1))
                    last_error = e
                    break
                if e.code == 404:
                    raise ValueError(f"CIK or resource not found: {url}") from e
                raise ValueError(f"HTTP {e.code} fetching {url}: {e.reason}") from e
            except urllib.error.URLError as e:
                last_error = e
                continue
        if attempt < retries:
            time.sleep(1.5 ** attempt)
    raise ConnectionError(f"Network/SSL error fetching {url}: {last_error}")


def _get_text(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    last_error = None
    for ctx_factory in (_secure_ctx, _fallback_insecure_ctx):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=ctx_factory()) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            last_error = e
    raise ConnectionError(f"Failed to fetch {url}: {last_error}")


def cik_from_name(company_name: str) -> Optional[dict]:
    key = company_name.strip().lower()
    if key in ALIAS_MAP and ALIAS_MAP[key].get("cik"):
        issuer = ALIAS_MAP[key]
        return {
            "name": issuer["name"],
            "cik": issuer["cik"],
            "ticker": issuer.get("ticker"),
            "exchange": issuer.get("exchange"),
        }

    encoded = urllib.parse.quote(company_name)
    url = f"{EDGAR_BASE}?action=getcompany&company={encoded}&owner=include&count=10"
    html = _get_text(url, timeout=15)
    ciks = list(dict.fromkeys(re.findall(r"CIK=(\d+)", html)))
    if not ciks:
        raise ValueError(f"No SEC results found for company: {company_name}")
    cik = ciks[0].zfill(10)
    name_match = re.search(r"companyName>([^<]+)<", html)
    name = name_match.group(1).strip() if name_match else company_name
    return {"name": name, "cik": cik}


def fetch_company_facts(cik: str) -> dict:
    return _get_json(f"{XBRL_BASE}/companyfacts/CIK{cik.zfill(10)}.json")


def _extract_entries(facts: dict, concept_list: list[str]) -> list[dict]:
    best = {}
    for prio, concept in enumerate(concept_list):
        concept_data = facts.get(concept)
        if not concept_data:
            continue
        units = concept_data.get("units", {})
        if not units:
            continue
        currency_order = ["CNY", "USD", "HKD", next(iter(units.keys()), None)]
        currency = next((c for c in currency_order if c in units), None)
        if not currency:
            continue
        for entry in units[currency]:
            key = (entry.get("end", ""), entry.get("form", ""))
            existing = best.get(key)
            keep = (
                existing is None
                or prio < existing[0]
                or (prio == existing[0] and entry.get("filed", "") > existing[1].get("filed", ""))
            )
            if keep:
                best[key] = (prio, {
                    "start": entry.get("start", ""),
                    "end": entry.get("end", ""),
                    "val": entry.get("val"),
                    "form": entry.get("form", ""),
                    "filed": entry.get("filed", ""),
                    "currency": currency,
                    "concept": concept,
                    "period_type": _classify_period(entry.get("form", ""), entry.get("start", ""), entry.get("end", "")),
                })
    return [v[1] for v in best.values()]


def _classify_period(form: str, start: str, end: str) -> str:
    form_upper = (form or "").upper()
    if any(x in form_upper for x in ("10-K", "20-F", "40-F")):
        return "annual"
    if any(x in form_upper for x in ("10-Q", "6-K")):
        return "quarterly"
    if start and end:
        try:
            s = datetime.strptime(start, "%Y-%m-%d")
            e = datetime.strptime(end, "%Y-%m-%d")
            return "annual" if 300 < (e - s).days < 400 else "quarterly"
        except ValueError:
            pass
    return "unknown"


def _merge_by_period(rev_entries: list[dict], ni_entries: list[dict], eps_entries: list[dict]) -> list[dict]:
    def key(item):
        return (item.get("end", ""), item.get("form", ""))

    rev_map = {key(r): r for r in rev_entries}
    eps_map = {key(e): e for e in eps_entries}
    ni_map = {}
    ni_priority = [
        "NetIncomeLossAvailableToCommonStockholdersBasic",
        "NetIncomeLoss",
        "ProfitLoss",
    ]
    for item in ni_entries:
        k = key(item)
        current = ni_map.get(k)
        if current is None:
            ni_map[k] = item
            continue
        if ni_priority.index(item.get("concept", "ProfitLoss")) < ni_priority.index(current.get("concept", "ProfitLoss")):
            ni_map[k] = item

    rows = []
    for k in sorted(set(rev_map) | set(ni_map) | set(eps_map), reverse=True):
        end, form = k
        rows.append({
            "period_end": end,
            "form": form,
            "period_type": _classify_period(form, "", end),
            "revenue": rev_map.get(k, {}).get("val"),
            "net_income": ni_map.get(k, {}).get("val"),
            "eps": eps_map.get(k, {}).get("val"),
            "currency": rev_map.get(k, {}).get("currency") or ni_map.get(k, {}).get("currency") or "CNY",
        })
    return rows


def _deduplicate_periods(periods: list[dict]) -> list[dict]:
    seen = {}
    for row in periods:
        form = row.get("form", "")
        score = 4 if "20-F" in form else 3 if "10-K" in form else 2 if "6-K" in form else 1 if "10-Q" in form else 0
        key = (row.get("period_end", ""), form)
        if key not in seen or score > seen[key]["_score"]:
            row["_score"] = score
            seen[key] = row
    return [{k: v for k, v in row.items() if k != "_score"} for row in seen.values()]


def fetch_financials(cik: str, period: str = "all", limit: int = 8) -> dict:
    facts = fetch_company_facts(cik)
    us_gaap = facts.get("facts", {}).get("us-gaap", {})
    ifrs = facts.get("facts", {}).get("ifrs-full", {})

    revenue_concepts = [c for c in REVENUE_CONCEPTS if c in ifrs] + [c for c in REVENUE_CONCEPTS if c in us_gaap]
    ni_concepts = [c for c in NET_INCOME_CONCEPTS if c in ifrs] + [c for c in NET_INCOME_CONCEPTS if c in us_gaap]
    eps_concepts = [c for c in EPS_CONCEPTS if c in us_gaap]

    revenue_entries = _extract_entries(ifrs, revenue_concepts) or _extract_entries(us_gaap, revenue_concepts)
    ni_entries = _extract_entries(ifrs, ni_concepts) or _extract_entries(us_gaap, ni_concepts)
    eps_entries = _extract_entries(us_gaap, eps_concepts)

    merged = _merge_by_period(revenue_entries, ni_entries, eps_entries)
    if period != "all":
        merged = [row for row in merged if row.get("period_type") == period]
    merged = _deduplicate_periods(merged)

    return {
        "cik": cik.zfill(10),
        "company_name": facts.get("entityName", ""),
        "data_updated": facts.get("lastModified", "") or facts.get("dataLastUpdated", ""),
        "period_type": period,
        "concepts_used": {
            "revenue": revenue_concepts[0] if revenue_concepts else "N/A",
            "net_income": ni_concepts[0] if ni_concepts else "N/A",
            "eps": eps_concepts[0] if eps_concepts else "N/A",
        },
        "financials": merged[:limit],
    }


def _fmt_money(val, symbol: str = "¥") -> str:
    if val is None:
        return f"{symbol}N/A"
    if not isinstance(val, (int, float)):
        return f"{symbol}{val}"
    abs_val = abs(val)
    if abs_val >= 1_000_000_000:
        return f"{symbol}{val / 1_000_000_000:.2f}B"
    if abs_val >= 1_000_000:
        return f"{symbol}{val / 1_000_000:.2f}M"
    return f"{symbol}{val:,.0f}"


def _fmt_eps(val) -> str:
    if val is None:
        return "N/A"
    if not isinstance(val, (int, float)):
        return str(val)
    return f"{val:.2f}"


def format_table(data: dict) -> str:
    rows = data.get("financials", [])
    if not rows:
        return f"\nNo financial data found for {data.get('company_name') or data.get('cik')}\n"
    currency = rows[0].get("currency", "CNY")
    symbol = {"CNY": "¥", "USD": "$", "HKD": "HK$"}.get(currency, currency + " ")
    lines = []
    width = 82
    lines.append(f"\n{'═' * width}")
    lines.append(f"  {data.get('company_name', 'N/A')}  |  CIK: {data.get('cik')}  |  Updated: {data.get('data_updated', 'N/A')}")
    lines.append(f"{'═' * width}")
    lines.append(f"  {'Period End':<12} {'Form':<7} {'Type':<10} {'Revenue':>18} {'Net Income':>18} {'EPS':>12}")
    lines.append(f"  {'─' * 70}")
    for row in rows:
        lines.append(
            f"  {row.get('period_end', 'N/A'):<12} {row.get('form', ''):<7} {row.get('period_type', ''):<10} "
            f"{_fmt_money(row.get('revenue'), symbol):>18} {_fmt_money(row.get('net_income'), symbol):>18} {_fmt_eps(row.get('eps')):>12}"
        )
    lines.append(f"{'═' * width}")
    concepts = data.get("concepts_used", {})
    lines.append(f"  Concepts: revenue={concepts.get('revenue')}, net_income={concepts.get('net_income')}, eps={concepts.get('eps')}")
    lines.append(f"  Currency: {currency}  |  Period filter: {data.get('period_type', 'all')}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Fetch structured financial data from SEC XBRL companyfacts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
            Examples:
              python3 sec_finance.py --search JD.com
              python3 sec_finance.py --cik 0001549802 --period quarterly
              python3 sec_finance.py --cik 0001549802 --period annual --output json
        """),
    )
    parser.add_argument("--search", type=str, help="Company name, ticker, or alias")
    parser.add_argument("--cik", type=str, help="10-digit CIK")
    parser.add_argument("--period", choices=["quarterly", "annual", "all"], default="all")
    parser.add_argument("--output", choices=["json", "table"], default="table")
    parser.add_argument("--limit", type=int, default=8)
    args = parser.parse_args()

    try:
        if args.search:
            result = cik_from_name(args.search)
            print(f"\n✅ Found: {result['name']}")
            print(f"   CIK:      {result['cik']}")
            print(f"   Ticker:   {result.get('ticker', 'N/A')}")
            print(f"   Exchange: {result.get('exchange', 'N/A')}")
            print("\n   Fetching financials...\n")
            data = fetch_financials(result["cik"], period=args.period, limit=args.limit)
        elif args.cik:
            data = fetch_financials(args.cik.strip().zfill(10), period=args.period, limit=args.limit)
        else:
            parser.print_help()
            print("\nBuilt-in issuers with validated CIKs:")
            for issuer in ISSUERS:
                if issuer.get("cik"):
                    print(f"  {issuer['name']:<22} {issuer['cik']}  {issuer.get('ticker','')}")
            return

        if args.output == "json":
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(format_table(data))
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    except ConnectionError as e:
        print(f"🌐 {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
