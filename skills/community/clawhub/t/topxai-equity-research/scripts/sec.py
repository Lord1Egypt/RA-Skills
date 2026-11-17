#!/usr/bin/env python3
"""SEC EDGAR data for research agents: raw responses go to a disk cache, only compact JSON is printed.

    python3 scripts/sec.py facts TICKER [--quarters 8]
        Last N quarters of revenue, gross profit, operating income, net income, operating cash flow and capex,
        plus the latest cash, debt, remaining performance obligations (RPO) and shares outstanding.
        Every value carries its period end, form, filing date and XBRL tag.
    python3 scripts/sec.py filings TICKER [--days 120] [--forms 8-K,10-Q,10-K,DEF 14A,4]
        Recent filings with 8-K item numbers and a link to the primary document.
    python3 scripts/sec.py feed [--hours 24] [--tickers A,B]
        New filings for several companies; without --tickers it reads the coverage list in research/watch.json.

Why: a full companyfacts JSON is several megabytes. Reading it into an agent's context wastes most of a research
budget. This tool keeps the raw JSON in a cache directory and prints only the cells you need (a 2.7 MB response
becomes roughly 3 KB).

Environment (required by the SEC fair-access policy, https://www.sec.gov/os/accessing-edgar-data):
    SEC_USER_AGENT="Your Name your.email@example.com"
Optional:
    SEC_CACHE_DIR   cache root (default: research/desk/cache/sec, one sub-folder per day)
Network: only https://www.sec.gov and https://data.sec.gov. At most 5 requests per second.

Method notes for `facts` (why the numbers can be trusted):
- Periods are derived from each fact's start/end dates, not from SEC "frame" labels (20-F filers often lack frames).
  75-100 days = a quarter, 350-380 days = a year; six- and nine-month year-to-date values are used only to derive quarters.
- A concept often changes tags over time (Revenues -> RevenueFromContractWithCustomer...). Tags are merged by period:
  the higher-priority tag wins a period, others only fill gaps. A restated period keeps the latest filing of the same tag.
- Missing quarters are derived: Q2 = 6M - Q1, Q3 = 9M - 6M, Q4 = FY - 9M (cash-flow statements are year-to-date), or
  FY minus the other three quarters of the same fiscal year. Derived quarters are flagged `derivedQ`.
- A derived value that is negative for a naturally non-negative item (revenue, gross profit, capex) is rejected and noted.
- `stale` marks a latest value whose period ends 400+ days before the company's newest figure: the company moved to a
  different tag, so do not use it as the current number.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

TAGS = {
    "revenue": ["us-gaap:Revenues", "us-gaap:RevenueFromContractWithCustomerExcludingAssessedTax", "us-gaap:SalesRevenueNet",
                "us-gaap:RevenueFromContractWithCustomerIncludingAssessedTax", "ifrs-full:Revenue",
                "ifrs-full:RevenueFromContractsWithCustomers"],
    "grossProfit": ["us-gaap:GrossProfit", "ifrs-full:GrossProfit"],
    "opIncome": ["us-gaap:OperatingIncomeLoss", "ifrs-full:ProfitLossFromOperatingActivities"],
    "netIncome": ["us-gaap:NetIncomeLoss", "us-gaap:ProfitLoss", "ifrs-full:ProfitLossAttributableToOwnersOfParent",
                  "ifrs-full:ProfitLoss"],
    "ocf": ["us-gaap:NetCashProvidedByUsedInOperatingActivities",
            "us-gaap:NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
            "ifrs-full:CashFlowsFromUsedInOperatingActivities"],
    "capex": ["us-gaap:PaymentsToAcquirePropertyPlantAndEquipment", "us-gaap:PaymentsToAcquireProductiveAssets",
              "ifrs-full:PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities"],
    "cash": ["us-gaap:CashAndCashEquivalentsAtCarryingValue",
             "us-gaap:CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents", "ifrs-full:CashAndCashEquivalents"],
    "debt": ["us-gaap:LongTermDebt", "us-gaap:LongTermDebtAndCapitalLeaseObligations", "us-gaap:DebtInstrumentCarryingAmount",
             "us-gaap:LongTermDebtNoncurrent", "ifrs-full:Borrowings", "ifrs-full:LongtermBorrowings"],
    "rpo": ["us-gaap:RevenueRemainingPerformanceObligation"],
    "shares": ["dei:EntityCommonStockSharesOutstanding"],
}
FLOW = ["revenue", "grossProfit", "opIncome", "netIncome", "ocf", "capex"]
INSTANT = ["cash", "debt", "rpo", "shares"]
NONNEG = {"revenue", "grossProfit", "capex"}
DISCOVER = {"revenue": (r"^(Revenue|Revenues|SalesRevenue)",
                        r"Cost|Deferred|Remaining|Unbilled|Interest|Percentage|Other|Tax|Related|Segment|Net$|Recognized|Excluding|Including|PerShare")}
_last = [0.0]


# ── HTTP with cache ──────────────────────────────────────────────────────

def user_agent() -> str:
    ua = os.environ.get("SEC_USER_AGENT", "").strip()
    if not re.search(r"\S+@\S+\.\S+", ua):
        raise SystemExit('Set SEC_USER_AGENT to your name and email, e.g. SEC_USER_AGENT="Jane Doe jane@example.com" '
                         "(required by the SEC fair-access policy).")
    return ua


def cache_dir() -> Path:
    root = Path(os.environ.get("SEC_CACHE_DIR", "research/desk/cache/sec"))
    return root / dt.date.today().isoformat()


def get(url: str, name: str) -> dict:
    """Fetch once per day per URL; the raw JSON is written to the cache and never printed."""
    f = cache_dir() / name
    if f.exists():
        return json.loads(f.read_text())
    wait = 0.2 - (time.monotonic() - _last[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": user_agent(), "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise SystemExit(f"SEC returned HTTP {e.code} for {url}")
    _last[0] = time.monotonic()
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(data))
    return data


def cik_of(ticker: str) -> int:
    d = get("https://www.sec.gov/files/company_tickers.json", "company_tickers.json")
    for v in d.values():
        if v["ticker"].upper() == ticker.upper():
            return int(v["cik_str"])
    raise SystemExit(f"{ticker} is not in the SEC ticker list (some foreign issuers are missing; look up the CIK on EDGAR).")


# ── Period helpers ───────────────────────────────────────────────────────

def qframe(end: str) -> str:
    """Calendar quarter closest to a period end (shift back 45 days); handles 52/53-week and off-calendar years."""
    d = dt.date.fromisoformat(end) - dt.timedelta(days=45)
    return f"CY{d.year}Q{(d.month - 1) // 3 + 1}"


def yframe(end: str) -> str:
    d = dt.date.fromisoformat(end) - dt.timedelta(days=182)
    return str(d.year)


def qkey(frm: str) -> int:
    return int(frm[2:6]) * 4 + int(frm[7])


def qname(v: int) -> str:
    return f"CY{(v - 1) // 4}Q{(v - 1) % 4 + 1}"


def _unit_end(arr) -> str:
    return max((f.get("end") or "" for f in arr), default="")


# ── XBRL extraction ──────────────────────────────────────────────────────

def collect(facts: dict, keys: list, discover=None) -> list:
    """Candidate tags in priority order, one unit each (the unit with the latest period end, then the longest history)."""
    def best_unit(units):
        return max(units.items(), key=lambda kv: (_unit_end(kv[1]), len({f.get("end") for f in kv[1]}), kv[0] == "USD"),
                   default=None)
    out = []
    for k in keys:
        tax, tag = k.split(":")
        node = facts.get(tax, {}).get(tag)
        if node:
            b = best_unit(node.get("units", {}))
            if b and b[1]:
                out.append((k, b[0], b[1]))
    if discover and (not out or max(_unit_end(c[2]) for c in out) < (dt.date.today() - dt.timedelta(days=500)).isoformat()):
        pat, neg = discover
        for tax in ("us-gaap", "ifrs-full"):
            for tag, node in facts.get(tax, {}).items():
                k = f"{tax}:{tag}"
                if not re.search(pat, tag) or re.search(neg, tag) or any(c[0] == k for c in out):
                    continue
                b = best_unit(node.get("units", {}))
                if b and b[1] and sum(1 for f in b[1] if f.get("start")) >= 4:
                    out.append((k, b[0], b[1]))
        out.sort(key=lambda c: _unit_end(c[2]), reverse=True)
    return out


def pick_flow(facts: dict, m: str, notes: list):
    cands = collect(facts, TAGS[m], DISCOVER.get(m))
    if not cands:
        return None, {}, {}, set()
    unit = cands[0][1]
    q, a, h6, n9 = {}, {}, {}, {}
    for k, u, fr in cands:
        if u != unit:
            continue
        for f in fr:
            st, en = f.get("start"), f.get("end")
            if not st or not en or f.get("val") is None:
                continue
            days = (dt.date.fromisoformat(en) - dt.date.fromisoformat(st)).days
            rec = (f["val"], en, f.get("form") or "", f.get("filed") or "", k)
            if 75 <= days <= 100:
                frm, tgt = qframe(en), q
            elif 170 <= days <= 200:
                frm, tgt = qframe(en), h6
            elif 260 <= days <= 290:
                frm, tgt = qframe(en), n9
            elif 350 <= days <= 380:
                frm, tgt = yframe(en), a
            else:
                continue
            cur = tgt.get(frm)
            if cur is None or (cur[4] == k and rec[3] > cur[3]):
                tgt[frm] = rec
    derived = set()

    def derive(frm, total, prev_map, prev_frm):
        if frm in q or prev_frm not in prev_map:
            return
        val, end, form, filed, k = total
        dv = val - prev_map[prev_frm][0]
        if m in NONNEG and dv < 0:
            notes.append({"metric": m, "quarter": frm, "rejected": "negative derived value"})
            return
        q[frm] = (dv, end, form, filed, k)
        derived.add(frm)

    for frm, r in list(h6.items()):
        derive(frm, r, q, qname(qkey(frm) - 1))
    for frm, r in list(n9.items()):
        derive(frm, r, h6, qname(qkey(frm) - 1))
    for _, r in list(a.items()):
        derive(qframe(r[1]), r, n9, qname(qkey(qframe(r[1])) - 1))
    # FY minus the other three quarters of the same fiscal year (the window looks back 330 days from FY end).
    for y, (val, end, form, filed, k) in list(a.items()):
        E = dt.date.fromisoformat(end)
        inwin = [(frm, r) for frm, r in q.items() if E - dt.timedelta(days=330) < dt.date.fromisoformat(r[1]) <= E]
        if len(inwin) != 3:
            continue
        ks = sorted(qkey(frm) for frm, _ in inwin)
        if ks[2] - ks[0] == 2:
            last_end = max(dt.date.fromisoformat(r[1]) for _, r in inwin)
            missing = ks[2] + 1 if (E - last_end).days > 45 else ks[0] - 1
        elif ks[2] - ks[0] == 3:
            missing = next(x for x in range(ks[0], ks[2] + 1) if x not in ks)
        else:
            continue
        frm = qname(missing)
        if frm in q:
            continue
        known = sum(r[0] for _, r in inwin)
        if m in NONNEG and val < known:
            notes.append({"metric": m, "fiscal_year": y, "rejected": "annual value below the sum of its quarters"})
            del a[y]
            continue
        dv = val - known
        if m in NONNEG and dv < 0:
            notes.append({"metric": m, "quarter": frm, "rejected": "negative derived value"})
            continue
        q[frm] = (dv, end, form, filed, k)
        derived.add(frm)
    return unit, q, a, derived


def pick_instant(facts: dict, m: str):
    """Point-in-time items: tags have different definitions, so never merge across tags; take the tag with the latest end."""
    best = None
    for k, u, fr in collect(facts, TAGS[m]):
        ins = {}
        for f in fr:
            if f.get("start") or not f.get("end") or f.get("val") is None:
                continue
            rec = (f["val"], f["end"], f.get("form") or "", f.get("filed") or "", k, u)
            frm = qframe(f["end"])
            if frm not in ins or rec[3] > ins[frm][3]:
                ins[frm] = rec
        if ins:
            rec = max(ins.values(), key=lambda r: r[1])
            if best is None or rec[1] > best[1]:
                best = rec
    return best


# ── Commands ─────────────────────────────────────────────────────────────

def out(obj) -> None:
    print(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def cmd_facts(a) -> None:
    cik = cik_of(a.ticker)
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik:010d}.json"
    raw = get(url, f"companyfacts-{cik}.json")
    facts = raw.get("facts", {})
    notes: list = []
    series, latest, annual, currency = {}, {}, {}, None
    for m in FLOW:
        unit, q, yr, derived = pick_flow(facts, m, notes)
        currency = currency or unit
        series[m] = {frm: r[0] for frm, r in q.items()}
        annual[m] = {y: r[0] for y, r in sorted(yr.items())[-3:]}
        if q:
            frm, r = max(q.items(), key=lambda kv: kv[1][1])
            latest[m] = {"val": r[0], "end": r[1], "form": r[2], "filed": r[3], "tag": r[4], "quarter": frm}
            if frm in derived:
                latest[m]["derivedQ"] = True
        else:
            latest[m] = None
    for m in INSTANT:
        r = pick_instant(facts, m)
        latest[m] = None if r is None else {"val": r[0], "end": r[1], "form": r[2], "filed": r[3], "tag": r[4], "unit": r[5]}
    newest = max((v["end"] for v in latest.values() if v), default="")
    for v in latest.values():
        if v and newest and (dt.date.fromisoformat(newest) - dt.date.fromisoformat(v["end"])).days > 400:
            v["stale"] = True
    frames = sorted({f for s in series.values() for f in s}, key=qkey)[-a.quarters:]
    out({"ticker": a.ticker.upper(), "cik": cik, "entity": raw.get("entityName"), "currency": currency,
         "evidence": "A", "source": url,
         "quarters": [{"q": f, **{m: series[m].get(f) for m in FLOW}} for f in frames],
         "latest": latest, "annual": annual, "notes": notes[-10:]})


def recent(cik: int, since: dt.datetime, forms) -> list:
    d = get(f"https://data.sec.gov/submissions/CIK{cik:010d}.json", f"submissions-{cik}.json")
    r = d["filings"]["recent"]
    rows = []
    for i, acc in enumerate(r["accessionNumber"]):
        t = dt.datetime.fromisoformat(r["acceptanceDateTime"][i].replace("Z", "+00:00"))
        if t < since:
            break
        if forms and r["form"][i] not in forms:
            continue
        rows.append({"form": r["form"][i], "filed": r["filingDate"][i], "accepted": r["acceptanceDateTime"][i],
                     "items": r["items"][i] or None, "accession": acc,
                     "url": f"https://www.sec.gov/Archives/edgar/data/{cik}/{acc.replace('-', '')}/{r['primaryDocument'][i]}"})
    return rows


def cmd_filings(a) -> None:
    cik = cik_of(a.ticker)
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=a.days)
    forms = {f.strip() for f in a.forms.split(",")} if a.forms else None
    out({"ticker": a.ticker.upper(), "cik": cik, "since": since.date().isoformat(), "evidence": "A",
         "filings": recent(cik, since, forms)})


def cmd_feed(a) -> None:
    if a.tickers:
        tickers = [t.strip().upper() for t in a.tickers.split(",") if t.strip()]
    else:
        watch = Path(os.environ.get("RESEARCH_WATCH", "research/watch.json"))
        if not watch.exists():
            raise SystemExit(f"{watch} not found; use --tickers A,B or create it from assets/templates/watch-entry.json")
        tickers = [s["ticker"] for s in json.loads(watch.read_text())["series"].values()]
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=a.hours)
    for t in tickers:
        rows = recent(cik_of(t), since, None)
        if rows:
            out({"ticker": t, "filings": rows})
    print(f"# feed: {len(tickers)} companies since {since:%Y-%m-%d %H:%M} UTC", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("facts"); f.add_argument("ticker"); f.add_argument("--quarters", type=int, default=8)
    g = sub.add_parser("filings"); g.add_argument("ticker"); g.add_argument("--days", type=int, default=120)
    g.add_argument("--forms")
    h = sub.add_parser("feed"); h.add_argument("--hours", type=int, default=24); h.add_argument("--tickers")
    a = ap.parse_args()
    {"facts": cmd_facts, "filings": cmd_filings, "feed": cmd_feed}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
