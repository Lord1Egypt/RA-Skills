"""
Light-mode SEC guidance extractor: self-contained, no ES / Ollama / RAG infra.

Fetches the most recent filing for a ticker directly from EDGAR (10-Q/10-K for
domestic filers, 20-F/40-F/6-K for foreign private issuers — `--form auto`
walks that chain), splits the filing into its real SEC sections (MD&A, Results
of Operations, Outlook, Forward-Looking Statements, Risk Factors), ranks
passages with a section-aware BM25, and asks Claude (or OpenAI) to answer with
inline citations.

Retrieval is lexical and dependency-light: a pure-Python BM25 (no rank_bm25),
query-side guidance-synonym expansion, a section boost for forward-looking
prose, and a down-weight for numeric tables — so a revenue *history* table no
longer outranks the revenue *outlook* paragraph. The built-in recall check
reports which guidance-dense chunks BM25 still missed.

Trades ~20% answer quality vs the heavy pipeline for zero-infra setup — good
enough for a single-ticker one-off lookup. For 100+ tickers/day, use the heavy
pipeline (mode=heavy, requires SEC_PIPELINE_DIR).

With no LLM API key set, degrades to retrieval-only output (ranked passages
with quotes) instead of failing. `--demo AAPL` runs the whole pipeline on a
bundled cached filing — no network, no API key, no third-party deps.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

UA = os.environ.get(
    "SEC_GUIDANCE_UA",
    "sec-guidance-skill contact@example.com",
)
HEADERS = {"User-Agent": UA}
CACHE_DIR = Path.home() / ".cache" / "sec-guidance"
DEMO_DIR = Path(__file__).resolve().parent / "demo"
CHUNK_CHARS = 1500
CHUNK_OVERLAP = 200
DEFAULT_TOP_K = 8

# `--form auto` tries these in order; foreign private issuers file 20-F/40-F
# (annual) and 6-K (interim) instead of 10-K/10-Q.
FORM_CHAIN = ["10-Q", "10-K", "20-F", "40-F", "6-K"]
FORM_CHOICES = ["auto"] + FORM_CHAIN

# Chunks with >=threshold hits are counted as "guidance-dense" for the recall
# check (threshold adapts to terse filers — see _recall_note).
GUIDANCE_KEYWORD_RE = re.compile(
    r"\b(guidance|outlook|expect(?:s|ed|ing)?|anticipat\w*|forecast\w*|"
    r"target(?:s|ed|ing)?|project(?:s|ed|ing)?|fiscal (?:year )?20\d\d)\b",
    re.IGNORECASE,
)

# Appended to every guidance query so BM25 also fires on forward-looking prose
# that phrases the same idea differently ("we anticipate" vs "outlook"). These
# are the signal we always want; the query's distinctive terms still dominate.
GUIDANCE_SYNONYMS = [
    "guidance", "outlook", "expect", "expects", "expected", "anticipate",
    "anticipated", "forecast", "project", "projected", "future", "forward",
    "estimate", "estimated", "intend", "plan", "believe",
]

GUIDANCE_QUERIES = [
    "What is management's guidance and outlook for future revenue and earnings?",
    "What forward-looking statements did management make about future performance expectations?",
    "What did management say about expected gross margins and profitability going forward?",
    "What new product launches, services, or business expansions did management project or plan?",
    "What macroeconomic conditions, risks, or uncertainties did management highlight for upcoming quarters?",
]

# --- Section detection ---------------------------------------------------
# Each pattern maps a filing section to a retrieval weight. Forward-looking
# prose (MD&A / Outlook / FLS) is boosted; numeric/boilerplate sections are
# left neutral or trimmed. A line is treated as a header only when it is short
# (<120 chars) so in-prose mentions ("...forward-looking statements, see...")
# don't split a paragraph.
SECTION_PATTERNS = [
    ("OUTLOOK", 1.8, re.compile(r"\b(business\s+outlook|^\s*outlook\b|guidance\s+summary)\b", re.I)),
    ("MDA", 1.6, re.compile(r"\b(management.?s discussion and analysis|results of operations|liquidity and capital resources)\b", re.I)),
    ("FORWARD", 1.5, re.compile(r"\bforward.?looking statements?\b", re.I)),
    ("RISK", 1.15, re.compile(r"\brisk factors\b", re.I)),
    ("QUANT", 1.1, re.compile(r"\bquantitative and qualitative disclosures\b", re.I)),
    ("FIN", 0.9, re.compile(r"\b(financial statements|notes to (?:the )?condensed|condensed consolidated)\b", re.I)),
]
SECTION_WEIGHT = {lbl: w for lbl, w, _ in SECTION_PATTERNS}
SECTION_WEIGHT["OTHER"] = 1.0
HEADER_MAX_LEN = 120


def _cache_path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe = re.sub(r"[^a-zA-Z0-9._-]", "_", key)
    return CACHE_DIR / safe


def _get(url: str, timeout: int = 30):
    """GET with retry/backoff — EDGAR throttles (429) and hiccups under load."""
    try:
        import requests
    except ImportError:
        print("ERROR: `requests` is required for live fetch. "
              "Install: pip install -r requirements.txt  (or try --demo AAPL)")
        sys.exit(1)
    last = ""
    for pause in (0, 2, 5):
        if pause:
            time.sleep(pause)
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout)
            if r.status_code in (429, 500, 502, 503, 504):
                last = f"HTTP {r.status_code}"
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            last = str(e)
    print(f"ERROR: EDGAR request failed after 3 attempts ({last}): {url}")
    if "429" in last:
        print("Hint: set SEC_GUIDANCE_UA=\"yourname you@example.com\" — SEC "
              "rate-limits generic User-Agents aggressively.")
    sys.exit(1)


def _lookup_cik(ticker: str) -> str | None:
    """Resolve ticker → 10-digit CIK from SEC's bulk file, cached."""
    cache = _cache_path("company_tickers.json")
    if not cache.exists() or (time.time() - cache.stat().st_mtime) > 86400:
        r = _get("https://www.sec.gov/files/company_tickers.json")
        cache.write_bytes(r.content)
    data = json.loads(cache.read_text())
    for rec in data.values():
        if rec.get("ticker", "").upper() == ticker.upper():
            return f"{int(rec['cik_str']):010d}"
    return None


def _recent_filings(cik: str) -> dict:
    """Fetch the submissions index once per run (recent filings block)."""
    r = _get(f"https://data.sec.gov/submissions/CIK{cik}.json")
    return r.json().get("filings", {}).get("recent", {})


def _latest_filing(recent: dict, cik: str, form: str) -> dict | None:
    """Return {accession, filing_date, primary_doc_url} for the most recent form."""
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accs = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])
    form_norm = form.replace("-", "").upper()
    for f, d, acc, doc in zip(forms, dates, accs, docs):
        if f.replace("-", "").upper() == form_norm:
            acc_nodash = acc.replace("-", "")
            url = (f"https://www.sec.gov/Archives/edgar/data/"
                   f"{int(cik)}/{acc_nodash}/{doc}")
            return {"accession": acc, "filing_date": d, "primary_doc_url": url}
    return None


def _resolve_filing(cik: str, form: str) -> tuple[str | None, dict | None]:
    """Resolve `auto` through the domestic→foreign form chain."""
    recent = _recent_filings(cik)
    for f in (FORM_CHAIN if form == "auto" else [form]):
        filing = _latest_filing(recent, cik, f)
        if filing:
            return f, filing
    return None, None


def _fetch_and_extract_text(url: str, filing_key: str) -> str:
    """Fetch primary doc, strip HTML/XBRL, return plain text. Cached per filing."""
    cache = _cache_path(f"filing__{filing_key}.txt")
    if cache.exists():
        return cache.read_text()
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("ERROR: `beautifulsoup4` is required for live fetch. "
              "Install: pip install -r requirements.txt  (or try --demo AAPL)")
        sys.exit(1)
    r = _get(url, timeout=60)
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "meta", "link"]):
        tag.decompose()
    # Inject paragraph breaks before block-level tags so text isn't a wall
    for block in soup.find_all(["p", "div", "tr", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        block.insert_before("\n\n")
    text = soup.get_text(" ")
    # Collapse whitespace but keep paragraph breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    # Strip XBRL namespace noise lines
    lines = [ln for ln in text.split("\n")
             if not re.match(r"^(xmlns|xbrli:|iso4217:|us-gaap:)", ln.strip())]
    text = "\n".join(lines)
    cache.write_text(text)
    return text


def _classify_header(line: str) -> str | None:
    """Return a section label if this line looks like a section header, else None."""
    s = line.strip()
    if not s or len(s) > HEADER_MAX_LEN:
        return None
    for lbl, _w, pat in SECTION_PATTERNS:
        if pat.search(s):
            return lbl
    return None


def _split_sections(text: str) -> list[tuple[str, str]]:
    """Split filing text into (label, body) segments by SEC section headers.

    Every line is assigned to the most recent header seen; the table-of-contents
    at the top produces tiny throwaway segments (header-to-header), while the
    real body segments carry the bulk of the text under the correct label."""
    segments: list[tuple[str, list[str]]] = [("OTHER", [])]
    for line in text.split("\n"):
        lbl = _classify_header(line)
        if lbl is not None:
            segments.append((lbl, [line]))
        else:
            segments[-1][1].append(line)
    return [(lbl, "\n".join(lines)) for lbl, lines in segments if "".join(lines).strip()]


def _chunk(text: str, size: int = CHUNK_CHARS, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    i = 0
    n = len(text)
    while i < n:
        chunks.append(text[i:i + size])
        if i + size >= n:
            break
        i += size - overlap
    return chunks


def _chunk_sections(text: str) -> list[tuple[str, str]]:
    """Section-aware chunking: a chunk never straddles two sections, and carries
    its section label. Returns list of (chunk_text, section_label)."""
    out: list[tuple[str, str]] = []
    for lbl, body in _split_sections(text):
        for c in _chunk(body):
            out.append((c, lbl))
    return out


def _tokenize(s: str) -> list[str]:
    return re.findall(r"\w+", s.lower())


class _BM25:
    """Pure-Python BM25-Okapi (no rank_bm25 dependency)."""

    def __init__(self, corpus_tokens: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.docs = corpus_tokens
        self.n = len(corpus_tokens)
        self.doc_len = [len(d) for d in corpus_tokens]
        self.avgdl = (sum(self.doc_len) / self.n) if self.n else 0.0
        self.tf = [Counter(d) for d in corpus_tokens]
        df: Counter = Counter()
        for d in corpus_tokens:
            df.update(set(d))
        # BM25 idf with +1 smoothing so it never goes negative on common terms.
        self.idf = {t: math.log(1 + (self.n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, q_tokens: list[str]):
        q = Counter(q_tokens)
        out = [0.0] * self.n
        for i in range(self.n):
            tf, dl = self.tf[i], self.doc_len[i]
            denom_base = self.k1 * (1 - self.b + self.b * dl / self.avgdl) if self.avgdl else self.k1
            s = 0.0
            for term, qc in q.items():
                f = tf.get(term, 0)
                if not f:
                    continue
                s += self.idf.get(term, 0.0) * qc * (f * (self.k1 + 1)) / (f + denom_base)
            out[i] = s
        return out


def _table_penalty(text: str) -> float:
    """0..~0.6 penalty for numeric-table-like chunks (digits/$/%/short tokens),
    so a revenue *history* table doesn't outrank a revenue *outlook* paragraph."""
    toks = _tokenize(text)
    if not toks:
        return 0.0
    numeric = sum(1 for t in toks if t.isdigit())
    frac = numeric / len(toks)
    if frac <= 0.12:
        return 0.0
    return min(0.6, (frac - 0.12) * 1.5)


def _rank(query: str, chunks: list[tuple[str, str]], bm25: "_BM25",
          k: int, expand: bool = True) -> list[tuple[int, float, str, str]]:
    """Section-aware ranking. Returns (chunk_idx, final_score, text, label)."""
    q_tok = _tokenize(query)
    if expand:
        q_tok = q_tok + GUIDANCE_SYNONYMS
    raw = bm25.scores(q_tok)
    scored = []
    for idx, (text, lbl) in enumerate(chunks):
        weight = SECTION_WEIGHT.get(lbl, 1.0)
        final = raw[idx] * weight * (1.0 - _table_penalty(text))
        scored.append((idx, final, text, lbl))
    scored.sort(key=lambda x: -x[1])
    return scored[:k]


def _snippet(text: str, chars: int = 180) -> str:
    return re.sub(r"\s+", " ", text.strip())[:chars]


def _recall_note(chunks: list[tuple[str, str]], picked: set[int]) -> tuple[str, dict]:
    """Coverage of guidance-dense chunks by the retrieved set — a cheap
    honesty check on BM25, not a guarantee of completeness."""
    hits = [len(GUIDANCE_KEYWORD_RE.findall(c)) for c, _ in chunks]
    # Adaptive threshold: terse filings (e.g. AAPL 10-Qs) never reach 3
    # keywords per chunk — fall back so the check doesn't go blind on them.
    threshold = 3 if any(h >= 3 for h in hits) else 2
    dense = [i for i, h in enumerate(hits) if h >= threshold]
    stats = {"guidance_dense_chunks": len(dense),
             "keyword_threshold": threshold,
             "covered": len(picked & set(dense)),
             "missed_chunk_indices": sorted(set(dense) - picked)[:10]}
    if not dense:
        return "Recall check: no guidance-dense chunks detected in this filing.", stats
    note = (f"Recall check: retrieved set covers {stats['covered']}/{len(dense)} "
            f"guidance-dense chunks")
    if dense and stats["covered"] / len(dense) < 0.3:
        note += ("  ⚠ LOW — raise --top-k or ask a more specific --query; "
                 f"unretrieved dense chunks start at {stats['missed_chunk_indices'][:5]}")
    return note, stats


def _pick_llm() -> tuple[str | None, str | None]:
    """Return (provider, model). Prefer Anthropic, then OpenAI, then a local
    `claude` CLI (Claude Code subscription — no API key needed).
    Returns (None, None) when none is available — caller degrades to
    retrieval-only."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic", os.environ.get("SEC_GUIDANCE_MODEL", "claude-sonnet-4-6")
    if os.environ.get("OPENAI_API_KEY"):
        return "openai", os.environ.get("SEC_GUIDANCE_MODEL", "gpt-4o-mini")
    import shutil
    if shutil.which("claude"):
        return "claude-cli", os.environ.get("SEC_GUIDANCE_MODEL", "sonnet")
    return None, None


def _ask_llm(query: str, passages: list[tuple[int, float, str, str]],
             provider: str, model: str) -> str:
    """Send prompt + numbered passages to the LLM, return answer text."""
    context = "\n\n".join(
        f"[{i + 1}] (chunk #{idx}, section={lbl}, score={score:.2f})\n{text}"
        for i, (idx, score, text, lbl) in enumerate(passages)
    )
    system = ("You are a financial analyst extracting forward-looking guidance "
              "from SEC filings. Answer the question using ONLY the numbered "
              "passages below. Cite passages inline as [1], [2], etc. If the "
              "passages don't contain the answer, say so — do not speculate. "
              "Never give buy/sell/hold recommendations.")
    user = f"QUESTION: {query}\n\nPASSAGES:\n{context}"
    return _ask_llm_raw(system, user, provider, model)


def _ask_llm_raw(system: str, user: str, provider: str, model: str) -> str:
    """Provider-dispatch for one system+user call, returns raw reply text."""
    if provider == "claude-cli":
        import subprocess
        res = subprocess.run(
            ["claude", "-p", "--model", model, "--system-prompt", system],
            input=user, capture_output=True, text=True, timeout=180)
        if res.returncode != 0:
            raise RuntimeError(f"claude CLI failed: {res.stderr.strip()[:200]}")
        return res.stdout.strip()
    if provider == "anthropic":
        try:
            import anthropic
        except ImportError:
            print("ERROR: `anthropic` SDK required. pip install anthropic")
            sys.exit(1)
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=model, max_tokens=1024, system=system,
            messages=[{"role": "user", "content": user}],
        )
        return resp.content[0].text
    if provider == "openai":
        try:
            import openai
        except ImportError:
            print("ERROR: `openai` SDK required. pip install openai")
            sys.exit(1)
        client = openai.OpenAI()
        resp = client.chat.completions.create(
            model=model, max_tokens=1024,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}],
        )
        return resp.choices[0].message.content
    raise RuntimeError(f"Unknown provider: {provider}")


def _run(ticker: str, resolved_form: str, filing: dict, text: str, top_k: int,
         custom_query: str | None, as_json: bool, say, allow_llm: bool = True) -> None:
    """Shared retrieval + answer path once filing text is in hand.

    `allow_llm=False` forces retrieval-only even when an API key is set — the
    offline `--demo` path uses this so it never makes a paid/external API call,
    matching its "no network, no key" promise."""
    chunks = _chunk_sections(text)
    sec_counts = Counter(lbl for _, lbl in chunks)
    say(f"Extracted {len(text):,} chars → {len(chunks)} chunks "
        f"({', '.join(f'{k}:{v}' for k, v in sec_counts.most_common())})\n")

    bm25 = _BM25([_tokenize(c) for c, _ in chunks])

    if not allow_llm:
        provider, model = None, None
        say("Offline demo — retrieval only; no LLM call is made even if an API "
            "key is set (no network, no external request).\n")
    else:
        provider, model = _pick_llm()
        if provider:
            say(f"LLM: {provider}/{model}\n")
        else:
            say("No LLM API key set (ANTHROPIC_API_KEY / OPENAI_API_KEY) — "
                "showing ranked passages only, no synthesized answers.\n")

    queries = [custom_query] if custom_query else GUIDANCE_QUERIES
    all_picked: set[int] = set()
    results = []
    for i, query in enumerate(queries, 1):
        say(f"[{i}/{len(queries)}] {query}")
        say("─" * 64)
        entry = {"query": query, "answer": None, "sources": [], "error": None}
        try:
            passages = _rank(query, chunks, bm25, top_k)
            if not passages or all(p[1] <= 0 for p in passages):
                say("  No candidate passages.\n")
                results.append(entry)
                continue
            all_picked.update(idx for idx, _, _, _ in passages)
            entry["sources"] = [
                {"n": j, "chunk": idx, "section": lbl, "score": round(score, 2),
                 "quote": _snippet(t)}
                for j, (idx, score, t, lbl) in enumerate(passages, 1)
            ]
            if provider:
                entry["answer"] = _ask_llm(query, passages, provider, model)
                say(entry["answer"])
            say("\nSources (verify against the filing URL above):")
            for s in entry["sources"]:
                say(f"  [{s['n']}] chunk #{s['chunk']}  [{s['section']}]  score={s['score']}")
                say(f"      \"{s['quote']}…\"")
            say("")
        except Exception as e:
            entry["error"] = str(e)
            say(f"  ERROR: {e}\n")
        results.append(entry)

    recall_line, recall_stats = _recall_note(chunks, all_picked)
    say(recall_line)
    say(f"{'='*64}\nDone.")

    if as_json:
        print(json.dumps({
            "ticker": ticker.upper(),
            "form": resolved_form,
            "filing_date": filing["filing_date"],
            "accession": filing["accession"],
            "filing_url": filing["primary_doc_url"],
            "llm": f"{provider}/{model}" if provider else None,
            "results": results,
            "recall_check": recall_stats,
        }, indent=2))


def run_demo(ticker: str, top_k: int, custom_query: str | None,
             as_json: bool = False) -> None:
    """Run the full pipeline on a bundled cached filing — no network, no key,
    no third-party deps. Proves the tool in seconds on a fresh machine."""
    say = (lambda *a, **k: print(*a, file=sys.stderr, **k)) if as_json else print
    meta_path = DEMO_DIR / f"{ticker.upper()}.json"
    if not meta_path.exists():
        avail = ", ".join(sorted(p.stem for p in DEMO_DIR.glob("*.json"))) or "(none bundled)"
        print(f"ERROR: no bundled demo for {ticker.upper()}. Available: {avail}")
        sys.exit(1)
    meta = json.loads(meta_path.read_text())
    text = (DEMO_DIR / meta["text_file"]).read_text()
    say(f"\n{'='*64}")
    say(f"  SEC GUIDANCE (demo — bundled filing, no network/key) | "
        f"{ticker.upper()} {meta['form']}")
    say(f"{'='*64}\n")
    say(f"Filing: {meta['form']} {meta['filing_date']}  accession={meta['accession']}")
    say(f"URL: {meta['primary_doc_url']}\n")
    _run(ticker, meta["form"], {
        "filing_date": meta["filing_date"],
        "accession": meta["accession"],
        "primary_doc_url": meta["primary_doc_url"],
    }, text, top_k, custom_query, as_json, say, allow_llm=False)


def run_light(ticker: str, form: str, top_k: int, custom_query: str | None,
              as_json: bool = False) -> None:
    # With --json, human-readable progress goes to stderr; stdout is pure JSON.
    say = (lambda *a, **k: print(*a, file=sys.stderr, **k)) if as_json else print

    say(f"\n{'='*64}")
    say(f"  SEC GUIDANCE (light mode) | {ticker.upper()} {form.upper()}")
    say(f"{'='*64}\n")

    cik = _lookup_cik(ticker)
    if not cik:
        print(f"ERROR: no CIK found for ticker {ticker} — the company may not "
              f"file with the SEC (private, or non-US without a US listing).")
        sys.exit(1)

    resolved_form, filing = _resolve_filing(cik, form)
    if not filing:
        tried = " / ".join(FORM_CHAIN) if form == "auto" else form
        print(f"ERROR: no {tried} filing found for {ticker} (CIK {cik}).")
        if form != "auto":
            print("Hint: try --form auto — foreign private issuers file "
                  "20-F/40-F/6-K instead of 10-K/10-Q.")
        sys.exit(1)
    if form == "auto" and resolved_form not in ("10-Q", "10-K"):
        say(f"[form auto] no 10-Q/10-K — foreign private issuer, using {resolved_form}")

    say(f"Filing: {resolved_form} {filing['filing_date']}  accession={filing['accession']}")
    say(f"URL: {filing['primary_doc_url']}\n")

    filing_key = f"{ticker.upper()}_{resolved_form.replace('-','')}_{filing['accession']}"
    text = _fetch_and_extract_text(filing['primary_doc_url'], filing_key)
    _run(ticker, resolved_form, filing, text, top_k, custom_query, as_json, say)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Light-mode SEC guidance extractor")
    p.add_argument("--ticker", default="AAPL")
    p.add_argument("--form", default="auto", choices=FORM_CHOICES,
                   help="auto tries 10-Q → 10-K → 20-F → 40-F → 6-K")
    p.add_argument("--top-k", type=int, default=DEFAULT_TOP_K)
    p.add_argument("--query", help="Single custom question (skips the 5 default queries)")
    p.add_argument("--demo", metavar="TICKER", nargs="?", const="AAPL",
                   help="Run on a bundled cached filing — no network, no API key, "
                        "no third-party deps (default AAPL)")
    p.add_argument("--json", action="store_true",
                   help="Emit structured JSON on stdout (progress goes to stderr)")
    args = p.parse_args()
    if args.demo:
        run_demo(args.demo, args.top_k, args.query, as_json=args.json)
    else:
        run_light(args.ticker, args.form, args.top_k, args.query, as_json=args.json)
