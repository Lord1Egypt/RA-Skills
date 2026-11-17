# Changelog

## 0.5.1 — 2026-11-09

- Simplified the `--diff` grading prompt and trimmed docs.

## 0.5.0 — 2026-11-09

- **Guidance revision detection (`--diff`)**: compares the two most recent
  guidance-bearing filings and emits graded revision events (RAISED / LOWERED
  / NARROWED / WIDENED / REAFFIRMED / INITIATED / WITHDRAWN / DROPPED) with
  direction, midpoint magnitude, horizon, attribution (structural vs timing),
  significance, and verbatim quotes from both filings. `--diff --json` emits
  structured events plus both snapshots.
- **8-K Item 2.02 support (diff path)**: quarterly guidance updates live in
  earnings-release exhibits, not the 10-Q — the diff targets the two most
  recent Item 2.02 8-Ks, resolving EX-99.* exhibits via the filing index's
  Type column (exhibit filenames are arbitrary), with 10-Q/10-K fallback.
  Guidance snapshots are cached per accession under
  `~/.cache/sec-guidance/snapshots/`.
- **`claude` CLI fallback provider**: with no `ANTHROPIC_API_KEY` /
  `OPENAI_API_KEY` set, a local `claude` CLI (Claude Code subscription) is
  used automatically for answers, snapshots, and diffs.
- Watch-mode cron recipe in SKILL.md: scheduled diffs over a personal
  watchlist, quiet unless guidance actually moved.

## 0.4.2 — 2026-10-20

- **Heavy mode is now ticker-scoped**: answers are drawn only from documents
  the index labels with the requested ticker. Previously, on a multi-company
  index, retrieval ran unfiltered and could present another company's filings
  under the requested ticker's banner. Heavy mode now resolves the ticker's
  `source_file` set up front, post-filters every retrieval hit against it, and
  refuses to answer (with a clear error and a light-mode suggestion) when the
  index has no documents labeled with that ticker.
- Re-bundle `skill-card.md` (missing from the 0.4.1 artifact).

## 0.4.1 — 2026-10-20

- **`--demo` is now strictly offline**: it forces retrieval-only and never
  calls an LLM even when `ANTHROPIC_API_KEY`/`OPENAI_API_KEY` is set in the
  environment — so the "no network, no API key" promise holds and no question
  or passage is ever sent to a paid/external service from the demo path.

## 0.4.0 — 2026-10-20

Retrieval-quality round: fix the misses that let a revenue *history* table
outrank the revenue *outlook*, and make first-run frictionless.

- **Section-aware chunking**: the filing is split on real SEC section headers
  (MD&A, Results of Operations, Outlook, Forward-Looking Statements, Risk
  Factors); chunks never straddle a section and carry their section label.
- **Section-aware ranking**: forward-looking sections (MD&A/Outlook/FLS) are
  boosted and numeric tables are down-weighted, plus query-side guidance-synonym
  expansion so BM25 fires on "we anticipate…" prose, not just the word "outlook".
  On the bundled AAPL 10-Q this takes the recall check from **0/3 → 3/3**
  guidance-dense chunks covered, and removes the revenue-table-ranked-#1 bug.
- **Pure-Python BM25**: dropped the `rank_bm25` dependency — one less thing to
  pip-install on a fresh machine.
- **`--demo TICKER`**: runs the whole pipeline on a bundled cached filing with
  **no network, no API key, and no third-party packages** — see real output in
  seconds before any setup.
- **Section labels surfaced** in sources, JSON, and the LLM context.
- SKILL.md opener now leads with the differentiators (verifiable citations +
  honest recall) instead of caveats.

## 0.3.0 — 2026-08-14

Mentor-review round: foreign issuers, verifiable citations, recall check, UX.

- **Foreign private issuers**: `--form auto` (new default) walks
  10-Q → 10-K → 20-F → 40-F → 6-K, so BABA/TSM-style filers work without
  the user knowing which form they file. Explicit `--form 20-F` etc. also
  accepted.
- **Verifiable citations**: every source line now prints a direct quote
  from the cited chunk alongside chunk index + BM25 score, so answers can
  be checked against the filing URL.
- **Recall check**: after retrieval, reports coverage of "guidance-dense"
  chunks (≥3 forward-looking keywords, adaptive down to ≥2 for terse
  filings like AAPL 10-Qs) by the retrieved set and warns loudly when
  low — BM25 misses become visible instead of silent.
- **No-key degradation**: with neither `ANTHROPIC_API_KEY` nor
  `OPENAI_API_KEY` set, the skill prints ranked passages with quotes
  instead of exiting — usable for retrieval without any LLM.
- **Retry/backoff**: EDGAR requests retry 3× on 429/5xx with a hint to set
  `SEC_GUIDANCE_UA` when throttled.
- **`--json`**: structured output (answers, sources with quotes, filing
  metadata, recall stats) on stdout; progress on stderr.
- **Boundaries documented**: SKILL.md gains a "When NOT to invoke" section
  (no market data, no non-SEC companies, no transcripts, no trading
  advice) and division-of-labor notes vs other financial skills.
- Submissions index fetched once per run (was once per form probe).

## 0.2.0 — 2026-08-03

Self-contained light mode + auto-detect dispatcher.

- New `sec_guidance_light.py`: fetches the latest 10-K/10-Q directly from
  SEC EDGAR, extracts text (BeautifulSoup), chunks in memory, ranks with
  BM25, calls Claude or OpenAI with inline citations. No Elasticsearch,
  no Ollama, no external RAG pipeline required.
- `extract_guidance.py` now dispatches by runtime detection:
  `--mode auto` (default) runs heavy if `SEC_PIPELINE_DIR` is set AND the
  pipeline is importable AND Elasticsearch is reachable; otherwise light.
  `--mode {light,heavy}` forces one.
- `SEC_PIPELINE_DIR` demoted from required to optional; light mode needs
  only `ANTHROPIC_API_KEY` (or `OPENAI_API_KEY`).
- `requirements.txt` added: `requests`, `beautifulsoup4`, `rank-bm25`,
  `anthropic`.
- Filings cached under `~/.cache/sec-guidance/` for repeat runs.

## 0.1.0 — 2026-07-26

Initial ClawHub release.

- `extract_guidance.py`: runs 5 standard guidance queries (or a single
  custom `--query`) against a local SEC filing RAG pipeline
  (Elasticsearch + sentence-transformers + cross-encoder rerank + Ollama),
  printing cited answers with source file / page / filing date.
- Pipeline location is taken strictly from the `SEC_PIPELINE_DIR`
  environment variable (no hardcoded paths); the script exits with a
  clear error when unset, when the pipeline can't be imported, or when
  the index is empty.
- SKILL.md documents setup (env var, Elasticsearch, ingestion), trigger
  scenarios, and all commands.
