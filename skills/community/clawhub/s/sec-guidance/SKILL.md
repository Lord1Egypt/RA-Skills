---
name: sec-guidance
description: Extract management guidance from SEC filings (10-K/10-Q, and 20-F/40-F/6-K for foreign private issuers) with verifiable inline citations and an honest recall check — and detect guidance REVISIONS (--diff) by comparing consecutive earnings 8-Ks and emitting graded events (raised/lowered/narrowed/dropped, with magnitude, horizon, and verbatim quotes). Self-contained (EDGAR + pure-Python BM25 + Claude/OpenAI or local claude CLI). Optional heavy mode delegates to a local RAG pipeline.
version: 0.5.1
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalEnv: ["ANTHROPIC_API_KEY", "OPENAI_API_KEY", "SEC_PIPELINE_DIR", "SEC_GUIDANCE_UA", "SEC_GUIDANCE_MODEL"]
    homepage: https://github.com/TINGHAO0724/sec-guidance-skill
---

# SEC Guidance Extractor

Ask what management said about the future — revenue, margins, outlook — and get
an answer **grounded in the actual SEC filing, with inline `[n]` citations you
can click back to the source.** Every run ends with a **recall check** that
tells you, honestly, which guidance-dense passages the retriever did *not*
surface — so you know what you're not seeing, instead of trusting a black box.

What makes the retrieval trustworthy:

- **Section-aware** — the filing is split into its real SEC sections (MD&A,
  Results of Operations, Outlook, Forward-Looking Statements, Risk Factors) and
  forward-looking prose is boosted, so a revenue *history* table no longer
  outranks the revenue *outlook* paragraph.
- **Verifiable, not generative** — answers cite numbered passages; the model is
  told to say "not in the filing" rather than speculate, and never to give
  trading advice.

Handles domestic filers (10-Q/10-K) and foreign private issuers (20-F/40-F/6-K)
via `--form auto`.

## Try it in 5 seconds — no key, no install

```bash
python sec_guidance_light.py --demo AAPL
```

Runs the full pipeline on a bundled cached Apple 10-Q — **no network, no API
key, no third-party packages** (BM25 is pure Python). This is the fastest way
to see real output before committing to setup.

## Revision detection (`--diff`) — the signal, not the level

A guidance *level* is a data point. The tradeable object is the **revision**:
management raising, cutting, narrowing, or quietly dropping a metric versus
what they themselves said last quarter. `--diff` compares the two most recent
guidance-bearing filings and emits graded revision events:

```bash
python extract_guidance.py --ticker SGI --diff
```

```
🔴 GUIDANCE REVISION — SGI: FY2026 adjusted EPS guide narrowed from the top,
   cutting ceiling $3.15→$2.95; implied YoY growth decelerates from ~11% to ~7%.
   8-K 2026-11-09 vs 8-K 2026-08-06

🔴 FY2026 adjusted EPS: $2.85 to $3.15 → $2.85 to $2.95  [LOWERED -3.3%]
   (current_fy, unclear)
     Floor held, ceiling cut $0.20
     prior: "...range of $2.85 to $3.15, ... approximate 11% increase from 2025..."
     new:   "...range of $2.85 to $2.95, ... approximate 7% increase from 2025..."
```

Where it looks: quarterly guidance updates live in **8-K Item 2.02 earnings
releases** (the EX-99 exhibits), not the 10-Q — so `--diff` targets the two
most recent Item 2.02 8-Ks (exhibit text fetched via the filing index's Type
column) and falls back to 10-Q/10-K MD&A for companies that don't file them.
Snapshots are cached per accession under `~/.cache/sec-guidance/snapshots/`,
so repeat diffs are one cheap comparison call.

Each change is classified as RAISED / LOWERED / NARROWED / WIDENED /
REAFFIRMED / INITIATED / WITHDRAWN / DROPPED (a metric management guided on
last time and no longer guides on), with midpoint magnitude, horizon
(current quarter / current FY / long-dated), attribution when the filing
states a reason, and a significance grade.

Output is **events, not advice**: direction, magnitude, horizon, attribution,
significance, and verbatim quotes from both filings so every claim is
verifiable. `--diff --json` emits the same as structured JSON (plus both
snapshots) for piping into your own process.

### Watch mode (where the timeliness comes from)

An ad-hoc diff is a post-mortem; a scheduled one is a signal. Cron recipe for
your own watchlist — quiet unless something actually changed:

```bash
#!/bin/sh
# guidance-watch.sh — run daily after market open
for T in SGI CEG WING; do
  OUT=$(python extract_guidance.py --ticker "$T" --diff --json 2>/dev/null)
  echo "$OUT" | python -c "
import json,sys
d=json.load(sys.stdin)
ev=[e for e in d['events'] if e['direction'] not in ('REAFFIRMED',)]
if ev and d['overall']!='LOW':
    print(f\"{d['ticker']}: {d['summary']}\")" \
  # pipe non-empty output to mail / Slack / your notifier
done
```

Snapshot caching makes this cheap: a day with no new filing re-diffs two
cached snapshots; the LLM extraction only runs when a new accession appears.

## Quickstart (light mode — live EDGAR)

```bash
pip install -r requirements.txt          # requests + beautifulsoup4 (+ anthropic for answers)
export ANTHROPIC_API_KEY=sk-ant-...       # or OPENAI_API_KEY; optional, see below
python extract_guidance.py --ticker AAPL
```

No Docker, no Elasticsearch, no Ollama.

**No API key?** It still runs: prints the top-ranked, section-labeled passages
with quotes and the recall check, and tells you which key unlocks synthesized
answers.

## When to invoke

- User asks what management said about future revenue, earnings, margins, or outlook
- User asks for guidance from an SEC filing (10-K, 10-Q, 20-F, 6-K)
- User asks "what is [company]'s guidance for next quarter?"
- User wants forward-looking statements or risk factors from SEC filings
- User asks whether a company raised/cut/changed its guidance, or what changed
  vs last quarter → use `--diff`

## When NOT to invoke (boundaries)

- **Stock prices or valuation** — this reads filings, not market data. Use a
  market-data skill for quotes, charts, or ratios.
- **Companies that don't file with the SEC** — private companies and non-US
  companies without a US listing have no EDGAR filings. The skill fails with
  a clear error, but don't invoke it for these.
- **Earnings-call transcripts or news** — only EDGAR filing text is fetched.
  What the CEO said on the call is out of scope.
- **Buy/sell recommendations** — the skill extracts and cites what management
  said; it is prompted to never produce trading advice.

Division of labor: this skill answers *"what did management commit to in the
filing"*. Pair it with market-data skills for prices and transcript tools for
call commentary.

## Options

```bash
# Offline demo: bundled filing, no network / key / deps
python extract_guidance.py --demo AAPL

# Auto form selection (default): 10-Q → 10-K → 20-F → 40-F → 6-K
python extract_guidance.py --ticker BABA          # foreign issuer → picks 20-F/6-K

# Specific form
python extract_guidance.py --ticker AAPL --form 10-K --top-k 8

# Single custom question
python extract_guidance.py --ticker MSFT --query "What did management say about Azure growth?"

# Structured output (JSON on stdout, progress on stderr)
python extract_guidance.py --ticker NVDA --json

# Force a mode (default: auto)
python extract_guidance.py --mode light --ticker NVDA
python extract_guidance.py --mode heavy --ticker NVDA
```

## Env vars

| Var | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | no* | Claude API key (preferred) |
| `OPENAI_API_KEY` | no* | OpenAI API key (fallback) |
| *(none, `claude` CLI on PATH)* | no* | Claude Code subscription fallback — used automatically when no API key is set |
| `SEC_GUIDANCE_UA` | no | User-Agent for EDGAR requests. SEC rate-limits generic UAs — set to `"yourname you@example.com"` if you make many requests. |
| `SEC_GUIDANCE_MODEL` | no | Override default LLM model. Anthropic default: `claude-sonnet-4-6`. OpenAI default: `gpt-4o-mini`. |
| `SEC_PIPELINE_DIR` | no | Enables heavy mode — see below. |

*With no key set, a local `claude` CLI is used if present; otherwise output
degrades to ranked passages with quotes (no synthesized answers). `--diff`
requires one of the three — snapshot extraction and grading are judgment
steps, not retrieval.

## Standard queries (default, when `--query` not given)

1. Future revenue and earnings outlook
2. Forward-looking performance expectations
3. Expected gross margins and profitability
4. New product launches, services, or expansion plans
5. Macroeconomic risks and uncertainties

## Output & citations

For each query: an LLM answer with inline `[1]`, `[2]` citations, plus a
source list showing chunk index, BM25 score, **and a direct quote from each
cited chunk** so every claim can be checked against the filing URL printed
at the top. `--json` emits the same content as structured JSON (answers,
sources with quotes, filing metadata, recall stats).

**Recall check:** after retrieval, the skill reports how many
"guidance-dense" chunks (≥3 forward-looking keywords) the retrieved set
covered, and warns when coverage is low — BM25 can miss relevant sections,
and this makes that visible instead of silent. Raise `--top-k` or ask a
narrower `--query` when warned.

EDGAR requests retry 3× with backoff on 429/5xx. Filings are cached under
`~/.cache/sec-guidance/` so repeat runs on the same ticker are fast.

## Heavy mode (optional — for bulk / repeat users)

If you already run a local SEC RAG pipeline (Elasticsearch + sentence-transformers +
cross-encoder rerank + Ollama), you can wire this skill to it:

```bash
export SEC_PIPELINE_DIR=/path/to/your/pipeline
python extract_guidance.py --ticker AAPL  # auto-detects heavy mode
```

The skill auto-detects heavy mode when `SEC_PIPELINE_DIR` is set, the
pipeline is importable, and Elasticsearch is reachable. Otherwise it silently
falls back to light mode. Heavy mode gives higher-quality retrieval on
large indexed corpora (cross-encoder rerank, hybrid dense+sparse search) —
worth the setup only if you're querying hundreds of tickers per day.
`--json` and `--form auto` are light-mode features; heavy mode maps `auto`
to 10-Q.

**Ticker scoping.** A shared index may hold many companies' filings, so heavy
mode answers only from documents the index labels with the requested ticker:
it resolves that ticker's `source_file` set up front and post-filters every
retrieval hit against it. If the index has no documents labeled with the
ticker (not ingested, or your pipeline doesn't populate a `ticker` field),
heavy mode exits with an error instead of answering from other companies'
documents — use light mode in that case.

Heavy-mode pipeline expected layout:
- `pipeline/index.py` exports `get_es()`, `INDEX` (docs carry `ticker` and
  `source_file` keyword fields)
- `pipeline/embed.py` exports `Embedder`
- `pipeline/retrieve.py` exports `hybrid_search(query, embedder, es, top_k)`
- `pipeline/rerank.py` exports `Reranker` (optional)
- `pipeline/answer.py` exports `generate_answer(query, results)`

See the reference implementation at the homepage repo. The heavy pipeline
is a slimmed-down open version of the system behind
[deltavigil.com](https://deltavigil.com) — daily SEC-guidance monitoring
across 1000+ US tickers (currently invite-only).

## Limitations of light mode

- One filing at a time (the most recent matching form). Heavy mode indexes
  the full history.
- BM25 only, no semantic embeddings or reranking. Roughly ~20% quality gap
  on the same single-filing query, larger gap on ambiguous questions. The
  recall check surfaces (but cannot fix) retrieval misses.
- 6-K filings are thin wrappers around press releases; guidance content
  varies much more than in 10-Q/10-K and answers may be sparse.
- Full filing text is sent through chunking (~1500 char chunks); very large
  10-Ks (>500 chunks) may be slow to rank. Not slow enough to matter for
  interactive use.
