> **何时读我**：引用条数上千、网络受限、要把验证挂进 CI，或者 stderr 弹了看不懂的
> 标识时。日常单次验证用不到本页。
> **回 INDEX**：[INDEX.md](INDEX.md)

# Operations playbook — bulk runs, proxies, speed, CI, and the error contract

## 1. Bulk runs — the batching math

**Where the time goes** (one citation, no cache):

| Path | API calls | Cost |
|---|---|---|
| PMID (NCBI batch) | 1 per 50 PMIDs | ~0.4 s/batch (0.12 s with `--ncbi-api-key`) |
| DOI (`--dois`/bibliography DOI) | 2 (Crossref resolve + EPMC DOI→PMID link) | ~1–2 s, 4 workers |
| arXiv ID | 1 | **3 s floor — imposed by arXiv, not negotiable** |
| Title search (no inline ID) | 1–2 (esearch + esummary) | ~1–3 s |
| Retracted entry (`--verify-doi`) | +1 (the notice record) | ~1 s, rare |

**Worked example** — 3,000 mixed citations (2,400 PMID + 400 DOI + 200 title):

- PMID leg: 2,400 / 50 = 48 batches ≈ 20–30 s
- DOI leg: 400 × 1.5 s / 4 workers ≈ 2–3 min
- Title leg: 200 × 2 s ≈ 7 min (the long pole — inline IDs are always worth adding)
- **Total ≈ 10 min.** The same run with a `.docx` of 3,000 paragraphs adds
  seconds (in-memory extraction), not minutes.

**Splitting rule** (`--max-entries`, default 2000): the guard counts the
de-duplicated workload. When it fires, split BY SECTION (a chapter / a
hundred numbered entries), not by line ranges — entry boundaries must stay
intact for the parser. Repeat runs are cheap: verified results are cached
(30 days, `--cache-days`) and the cache survives section splits.

**Cache discipline** (the cache covers the PMID leg; DOI/arXiv rows
re-verify each run): development iterations run WITH the cache; the final
pre-submission pass is `--quick` (implies `--no-cache`). Network failures
are never cached — a cached "unknown" is impossible by construction.

## 2. Proxy configuration — the three real scenarios

| Scenario | Setup | Pitfall |
|---|---|---|
| Corporate/school proxy | `export HTTPS_PROXY=http://host:port` (HTTP_PROXY too) | Credentials in the URL are masked by `--check-net` output, but keep the env var out of CI logs |
| Dead proxy env left behind | The registries look unreachable even though the network is fine — a stale env var **masquerades as an outage** | `env \| grep -i proxy`; unset and re-run `--check-net` |
| Automation / CI direct connection | `unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy` in the job before invoking | A proxy that only handles some hosts gives partial reachability — judge by `--check-net`, not by one source |

In-batch retry (v5.7.0): each batch fetch stage (PMID metadata, DOI
resolution, linked-PMID metadata) re-runs only its network-failed calls
after a 2 s cool-off — `--retries N` (default 1, 0 = off, max 3). A sweep
never worsens a run: a still-open circuit breaker aborts it and the
first-pass answers stand; recovered counts land in `stats.retried_recovered`
and the stderr `[NOTE]` lines. Per-call transport retries (three attempts,
429 Retry-After backoff, UA rotation) are unchanged and independent.

Exit-code note (v5.8.0): exit 2 also covers invalid flag values —
`[ERROR]` + exit 2 fires before any work (`--timeout 0`, `--threshold 1.5`,
`--workers 0`, negative `--cache-days`/`--retries`/`--max-entries`); soft
over-ranges clamp with a `[WARN]` (`--workers 99` -> 8, `--retries 10` -> 3).

`--check-net` is the arbiter: four data sources + arXiv, probed twice each (direct
and via your `HTTPS_PROXY`, 5 s per route), one verdict line per source —
a source blocked on the direct route but reachable through the configured
proxy reports as usable, and every line names the verification paths that
source serves plus the in-tool fallback.
NCBI blocked but Europe PMC reachable → `--meta-source europepmc` runs the
whole verification off EPMC (no key needed). Registry retraction/abstract
extras degrade honestly (they are Crossref-side).

## 3. Speed checklist — in decision order

1. **Add inline IDs** (PMID/DOI) to references — the title-search leg is the
   long pole; exact IDs route in one call.
2. **Get an NCBI API key** (`--ncbi-api-key`): 3→10 req/s ceiling, batch
   spacing 0.4 s→0.12 s — the PMID leg shrinks ~3×.
3. **Set `--mailto`**: Crossref polite pool — friendlier DOI limits for free.
4. **Cache for iteration, `--quick` for the final pass** (see §1).
5. **Don't fight the arXiv floor**: 3 s/call is their API requirement; 1,000
   arXiv IDs ≈ 50+ minutes. Batch arXiv work overnight or trim the list.
6. **`--workers N`** only matters on DOI-heavy inputs (default 4 is tuned).

## 4. The error contract — exit codes, stderr markers, actions

**Exit codes** (the only three):

| Exit | Meaning | What to do |
|---|---|---|
| `0` | Ran clean — no invalid/mismatch/retracted/splice found | Submit / ship |
| `1` | Problems FOUND (invalid, mismatch, retracted, DOI-splice, lint errors) | Read the flagged rows — these are citation problems, not tool problems |
| `2` | Could NOT verify (registries unreachable) | Fix network (§2), re-run; nothing was cached, nothing was judged |

**stderr markers** (stdout carries results; stderr carries the tool's own
annotations):

| Marker | Meaning | Action |
|---|---|---|
| `[ERROR]` | The run cannot proceed (unreadable input, mutually exclusive flags, empty stdin) | Fix the invocation per the message |
| `[WARN]` | Ambiguous invocation — the run proceeds with a stated precedence (e.g. `--pmids` beats `--source`; the ignored input is named) | Remove the redundant flag or accept the precedence |
| `[NOTE]` | Informational guard — e.g. the `--max-entries` bulk warning with the actual count and a split hint | Split the input or raise/silence the guard |
| `parse-text:` / `bibliography:` / `Text reference list …` | Parser advisories (skipped rows, routing tallies) | Only the affected entries are skipped; the rest verified |

**Design invariant**: a network failure is `[NOTE]`-level context in the
report (`unknown`, exit 2) and NEVER a `[ERROR]` — the tool distinguishes
"your citation is wrong" (1) from "I could not look" (2) at the exit-code
level, so CI can gate on it.

## 5. CI integration — a minimal gate

```bash
python3 scripts/verify_pmids.py --lint-claims claims.csv          # 1) offline shape check
python3 scripts/verify_pmids.py --source docs/refs --quick \
        --output report.html --jsonl rows.jsonl                   # 2) verify
rc=$?                                                              # 3) gate
[ $rc -le 1 ] || { echo "verification incomplete (network) — retry"; exit 1; }
[ $rc -eq 1 ] && { echo "citation problems — see report.html"; exit 1; }
exit 0   # rc=0 falls through: the gate must PASS a clean run
```

`--lint-claims` runs offline (no network) and catches ID-shape errors,
missing titles and unknown columns before any API call. `--jsonl` feeds
per-row dashboards; the `_stats` line is the totals record.

## 6. Reading the main script (verify_pmids.py)

Approximate section map, top to bottom (extractor and bibliography
helpers interleave near Main): config & HTTP core (retry/backoff/circuit
breaker) → fetchers per registry (NCBI / Europe PMC / Crossref / OpenAlex /
arXiv) → extractors (PMID/DOI/arXiv/context parsing, docx/pptx/html) →
verdict machinery (cross-check ladder, retraction cap, gates and
second-opinion legs) → exporters (text/markdown/HTML/JSON/JSONL/CSV/BibTeX/
RIS/bundle) → `main()` (argparse groups in `--help` order, then the
pipelines: collect → verify → extras → report).
