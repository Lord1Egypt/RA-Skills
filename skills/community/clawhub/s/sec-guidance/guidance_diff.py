"""
Guidance revision detection (`--diff`): the alpha-shaped upgrade.

A guidance *level* is a data point; the tradeable object is the *revision* —
management raising, cutting, narrowing, or quietly dropping a metric versus
what they themselves said last quarter. This module turns two consecutive
filings into one structured revision event:

  1. Snapshot: extract quantified forward guidance from each filing into a
     fixed schema (metric / period / value / basis / quote), cached per
     accession under ~/.cache/sec-guidance/snapshots/.
  2. Diff: compare the two snapshots and emit graded revision events.

Where guidance actually lives: for most US filers the quarterly guidance
update is in the 8-K Item 2.02 earnings release (exhibit EX-99.*), not the
10-Q — so `--diff` defaults to the two most recent Item 2.02 8-Ks (exhibit
text included) and falls back to 10-Q/10-K when a company doesn't file them.

This emits graded *events*, never trading advice.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from sec_guidance_light import (
    CACHE_DIR, _BM25, _chunk_sections, _fetch_and_extract_text, _lookup_cik,
    _rank, _recent_filings, _ask_llm_raw, _pick_llm, _tokenize,
)

SNAP_DIR = CACHE_DIR / "snapshots"
SNAP_TOP_K = 14  # chunks fed to the snapshot extractor

# The diff defaults to earnings 8-Ks; a company that puts outlook in the
# 10-Q MD&A instead is caught by the fallback chain.
DIFF_FORM_CHAIN = ["8-K", "10-Q", "10-K"]

SNAPSHOT_QUERY = (
    "management guidance outlook expects full year fiscal revenue earnings "
    "EPS margin growth capital expenditures raised lowered reaffirmed"
)

SNAPSHOT_PROMPT = """You are extracting management's forward-looking guidance \
from numbered SEC-filing passages. Extract ONLY quantified, forward-looking \
statements made by management about future periods (revenue, EPS, margins, \
unit growth, capex, segment KPIs, free cash flow). Historical results are NOT \
guidance. Do not infer numbers that are not stated.

Reply with ONLY JSON:
{"guidance": [{"metric": "<short name, e.g. 'FY2026 revenue'>",
  "period": "<fiscal period it covers, e.g. 'FY2026' or 'Q4 FY2026'>",
  "value": "<the guided value or range, verbatim units, e.g. '$5.2B-$5.4B'>",
  "basis": "<GAAP | adjusted/non-GAAP | unclear>",
  "quote": "<=200 chars verbatim from the passage>",
  "passage": <passage number n>}],
 "qualitative_outlook": "<=200 chars: directional but unquantified outlook, or ''>",
 "no_guidance": <true if no quantified forward guidance appears>}"""

DIFF_RUBRIC = """Grading instructions:
- Compute magnitude as the midpoint move in percent where both sides are
  quantified ranges or points; otherwise 'n/a'.
- DROPPED means a metric management guided on last time that no longer
  appears in the new snapshot; record it rather than omitting the metric.
- Set attribution (timing | structural | unclear) only from reasons stated
  in the filing text; do not infer one.
- Assign significance (HIGH/MEDIUM/LOW) using your own judgment of how
  material the change is to the company's stated outlook."""

DIFF_PROMPT_TEMPLATE = """You compare two consecutive guidance snapshots from \
the same company's SEC filings and emit structured revision events.

PRIOR snapshot (filed {prior_date}, {prior_form}):
{prior_json}

NEW snapshot (filed {new_date}, {new_form}):
{new_json}

Match metrics across the two snapshots (names may differ slightly — 'FY26
revenue' and 'fiscal 2026 net sales' are the same metric; adjusted vs GAAP are
NOT the same). {rubric}

Reply with ONLY JSON:
{{"events": [{{"metric": "...", "period": "...",
   "prior": "<prior value or null>", "new": "<new value or null>",
   "direction": "RAISED|LOWERED|NARROWED|WIDENED|REAFFIRMED|INITIATED|WITHDRAWN|DROPPED",
   "magnitude": "<midpoint move as % or 'n/a'>",
   "horizon": "current_quarter|current_fy|long_dated",
   "attribution": "structural|timing|unclear",
   "significance": "HIGH|MEDIUM|LOW",
   "why": "<=120 chars, the rubric reason>",
   "prior_quote": "<verbatim or ''>", "new_quote": "<verbatim or ''>"}}],
 "overall": "HIGH|MEDIUM|LOW",
 "summary": "<=200 chars, lead with the single most significant change>"}}"""

_SIG_DOT = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}


def _parse_json_reply(raw: str) -> dict:
    """Tolerate code fences and leading prose around the JSON object."""
    m = re.search(r"\{.*\}", raw, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON object in LLM reply: {raw[:200]}")
    return json.loads(m.group(0))


def _filings_with_guidance(recent: dict, cik: str, form: str, n: int) -> list[dict]:
    """The n most recent filings of `form`. For 8-K, only Item 2.02 earnings
    releases count — routine 8-Ks (votes, officer changes) carry no guidance."""
    out = []
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])
    items_l = recent.get("items", [""] * len(forms))
    form_norm = form.replace("-", "").upper()
    for f, d, acc, doc, items in zip(forms, dates, accs, docs, items_l):
        if f.replace("-", "").upper() != form_norm:
            continue
        if form_norm == "8K" and "2.02" not in (items or ""):
            continue
        acc_nodash = acc.replace("-", "")
        out.append({
            "form": form, "accession": acc, "filing_date": d, "items": items,
            "primary_doc_url": (f"https://www.sec.gov/Archives/edgar/data/"
                                f"{int(cik)}/{acc_nodash}/{doc}"),
            "acc_nodash": acc_nodash,
        })
        if len(out) >= n:
            break
    return out


def _exhibit_urls(cik: str, filing: dict) -> list[str]:
    """EX-99.* press-release documents of an 8-K — that's where guidance lives.

    Exhibit *filenames* are arbitrary (`a11092026sgipressrelease-f.htm`), so
    filename matching is unreliable; the authoritative mapping is the Type
    column of the filing's -index.html table. Falls back to [] (primary doc
    only) if the fetch/parse fails."""
    from sec_guidance_light import _get
    base = (f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/"
            f"{filing['acc_nodash']}")
    try:
        from bs4 import BeautifulSoup
        r = _get(f"{base}/{filing['accession']}-index.html")
        soup = BeautifulSoup(r.text, "html.parser")
    except SystemExit:
        raise
    except Exception:
        return []
    urls = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if not any(re.match(r"EX-99", c.get_text(strip=True)) for c in cells):
            continue
        a = row.find("a", href=True)
        if not a:
            continue
        href = a["href"]
        # Inline-XBRL viewer links wrap the real document path
        href = re.sub(r"^/ix\?doc=", "", href)
        if not href.lower().endswith((".htm", ".html")):
            continue
        urls.append(href if href.startswith("http") else f"https://www.sec.gov{href}")
    return urls


def _filing_text(ticker: str, cik: str, filing: dict) -> str:
    """Primary doc text; for 8-Ks, append EX-99 exhibit text (the earnings
    release body — the 8-K wrapper itself is usually two paragraphs)."""
    key = f"{ticker.upper()}_{filing['form'].replace('-', '')}_{filing['accession']}"
    text = _fetch_and_extract_text(filing["primary_doc_url"], key)
    if filing["form"].replace("-", "").upper() == "8K":
        for i, url in enumerate(_exhibit_urls(cik, filing)):
            text += "\n\n" + _fetch_and_extract_text(url, f"{key}_ex{i}")
    return text


def _snapshot(ticker: str, filing: dict, text: str, provider: str, model: str,
              say) -> dict:
    """Extract (or load cached) structured guidance snapshot for one filing."""
    SNAP_DIR.mkdir(parents=True, exist_ok=True)
    snap_path = SNAP_DIR / (f"{ticker.upper()}_{filing['form'].replace('-', '')}"
                            f"_{filing['accession'].replace('-', '')}.json")
    if snap_path.exists():
        say(f"  snapshot (cached): {filing['form']} {filing['filing_date']}")
        return json.loads(snap_path.read_text())
    chunks = _chunk_sections(text)
    bm25 = _BM25([_tokenize(c) for c, _ in chunks])
    passages = _rank(SNAPSHOT_QUERY, chunks, bm25, SNAP_TOP_K)
    context = "\n\n".join(
        f"[{i + 1}]\n{t}" for i, (_idx, _s, t, _lbl) in enumerate(passages))
    raw = _ask_llm_raw(SNAPSHOT_PROMPT, f"PASSAGES:\n{context}", provider, model)
    snap = _parse_json_reply(raw)
    snap["_meta"] = {"ticker": ticker.upper(), "form": filing["form"],
                     "filing_date": filing["filing_date"],
                     "accession": filing["accession"],
                     "filing_url": filing["primary_doc_url"]}
    snap_path.write_text(json.dumps(snap, indent=2))
    say(f"  snapshot (extracted): {filing['form']} {filing['filing_date']} — "
        f"{len(snap.get('guidance', []))} guided metrics")
    return snap


def run_diff(ticker: str, form: str, as_json: bool = False) -> None:
    say = (lambda *a, **k: print(*a, file=sys.stderr, **k)) if as_json else print
    say(f"\n{'=' * 64}")
    say(f"  SEC GUIDANCE REVISION (--diff) | {ticker.upper()}")
    say(f"{'=' * 64}\n")

    provider, model = _pick_llm()
    if not provider:
        print("ERROR: --diff needs an LLM (ANTHROPIC_API_KEY / OPENAI_API_KEY, "
              "or a `claude` CLI on PATH) — snapshot extraction and revision "
              "grading are judgment steps, not retrieval.")
        sys.exit(1)
    say(f"LLM: {provider}/{model}")

    cik = _lookup_cik(ticker)
    if not cik:
        print(f"ERROR: no CIK found for ticker {ticker}.")
        sys.exit(1)

    recent = _recent_filings(cik)
    filings: list[dict] = []
    for f in (DIFF_FORM_CHAIN if form == "auto" else [form]):
        filings = _filings_with_guidance(recent, cik, f, n=2)
        if len(filings) >= 2:
            break
    if len(filings) < 2:
        print(f"ERROR: need two comparable filings for {ticker.upper()}, found "
              f"{len(filings)} (tried "
              f"{' / '.join(DIFF_FORM_CHAIN if form == 'auto' else [form])}; "
              f"for 8-K only Item 2.02 earnings releases count).")
        sys.exit(1)
    new_f, prior_f = filings[0], filings[1]
    say(f"Comparing {new_f['form']} {new_f['filing_date']} vs "
        f"{prior_f['form']} {prior_f['filing_date']}\n")

    snaps = []
    for fil in (prior_f, new_f):
        text = _filing_text(ticker, cik, fil)
        snaps.append(_snapshot(ticker, fil, text, provider, model, say))
    prior_snap, new_snap = snaps

    if prior_snap.get("no_guidance") and new_snap.get("no_guidance"):
        say("")
        print(f"No quantified guidance in either filing — {ticker.upper()} "
              f"likely guides on earnings calls only (out of scope). "
              f"Try --diff --form 10-Q for MD&A outlook language.")
        return

    def _public(s: dict) -> str:
        return json.dumps({k: v for k, v in s.items() if k != "_meta"},
                          ensure_ascii=False)

    prompt = DIFF_PROMPT_TEMPLATE.format(
        prior_date=prior_f["filing_date"], prior_form=prior_f["form"],
        prior_json=_public(prior_snap),
        new_date=new_f["filing_date"], new_form=new_f["form"],
        new_json=_public(new_snap), rubric=DIFF_RUBRIC)
    diff = _parse_json_reply(_ask_llm_raw(
        "You are a guidance-revision analyst. Reply with ONLY JSON.",
        prompt, provider, model))

    events = diff.get("events", [])
    overall = diff.get("overall", "LOW")
    say("")
    out_lines = [f"{_SIG_DOT.get(overall, '⚪')} GUIDANCE REVISION — "
                 f"{ticker.upper()}: {diff.get('summary', '')}",
                 f"   {new_f['form']} {new_f['filing_date']} vs "
                 f"{prior_f['form']} {prior_f['filing_date']}", ""]
    for ev in events:
        dot = _SIG_DOT.get(ev.get("significance", "LOW"), "⚪")
        line = (f"{dot} {ev.get('metric', '?')}: {ev.get('prior') or '—'} → "
                f"{ev.get('new') or '—'}  [{ev.get('direction', '?')}"
                f" {ev.get('magnitude', '')}] "
                f"({ev.get('horizon', '?')}, {ev.get('attribution', '?')})")
        out_lines.append(line)
        if ev.get("why"):
            out_lines.append(f"     {ev['why']}")
        for side, q in (("prior", ev.get("prior_quote")), ("new", ev.get("new_quote"))):
            if q:
                out_lines.append(f"     {side}: \"{q[:160]}\"")
    out_lines += ["", f"Verify: new {new_f['primary_doc_url']}",
                  f"        prior {prior_f['primary_doc_url']}",
                  "Events, not advice — a graded revision is an input to your "
                  "process, not a recommendation."]
    for ln in out_lines:
        say(ln)

    if as_json:
        print(json.dumps({
            "ticker": ticker.upper(),
            "new_filing": {k: new_f[k] for k in ("form", "filing_date", "accession", "primary_doc_url")},
            "prior_filing": {k: prior_f[k] for k in ("form", "filing_date", "accession", "primary_doc_url")},
            "llm": f"{provider}/{model}",
            "overall": overall,
            "summary": diff.get("summary", ""),
            "events": events,
            "prior_snapshot": {k: v for k, v in prior_snap.items() if k != "_meta"},
            "new_snapshot": {k: v for k, v in new_snap.items() if k != "_meta"},
        }, indent=2))
