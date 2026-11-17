# troubleshooting.md — one error, one row

> **When to read me**: the terminal shows `[ERROR]`/`[WARN]`, every verdict
> is ❓ unknown, or a result looks wrong. Each row: the literal error text →
> the cause → the one-command fix. Deep background stays in the linked doc.
> **Back to** [INDEX.md](INDEX.md)

## First: three exit codes

| Exit | Meaning | First reaction |
|---|---|---|
| 0 | clean | — |
| 1 | problems found (invalid / mismatch / retracted / DOI-splice / arXiv claimed-DOI mismatch), or a usage error (bad claims file, missing `--source` path) | read `details` in the report, or the stderr line |
| 2 | could not verify (network unreachable) **or** an invalid flag value | `--check-net` first; then re-read the `[ERROR]` text below |

## Error quick table (literal text → fix)

| You see | Why | Fix |
|---|---|---|
| `--stdin received no input (nothing on stdin)` | the pipe was empty | paste a reference list, or use `--parse-text file` |
| `--stdin and --parse-text are mutually exclusive` | two text inputs at once | keep one |
| `both --pmids and --source given; --source is ignored` | precedence, not a bug | drop `--source` if it was not intended |
| `parsing --claims JSON: ...` / `reading claims file: ...` | malformed JSON/CSV | lint first: `--lint-claims claims.json` |
| `--threshold is a 0..1 similarity cutoff (got 1.5)` | flag validation (v5.8.0): the run refused to start | pass a 0..1 value |
| `--timeout must be a positive number of seconds` | flag validation | pass seconds, e.g. `--timeout 60` |
| `--workers 99 exceeds the polite ceiling; clamping to 8` | soft clamp — the run proceeds with 8 | nothing; lower it to silence the `[WARN]` |
| `无法连接 <host>（已连续 N 次传输失败）` / `circuit breaker skipped N call(s)` | a host failed repeatedly; later calls to it are skipped to avoid hammering | re-run later (unknowns are never cached); `--meta-source europepmc` switches the metadata source; `--check-net` shows which route works |
| `[NOTE] <file>: structured parse produced no text — reading as plain text` | a structured file (docx/pptx/html/JATS) degraded to a byte scan — results from it may be incomplete | re-export to text/HTML, or ignore if the file is genuinely plain text |
| `{source} not found` | the `--source` path does not exist | check the path |
| `text#N: no routable ID and no usable title — skipped (...)` | the line had no PMID/DOI/arXiv ID and was too short to title-search (the parentheses quote its first 48 characters) | add an ID, or feed `--claims-file` for exact metadata |

## Verdicts look wrong

- **Everything is ❓ unknown** — the network, not the citations: run
  `--check-net` (v5.6.0+: direct + proxy per source). Behind a proxy, set
  `HTTPS_PROXY`; NCBI blocked → `--meta-source europepmc`. Unknowns are
  never cached, so a clean re-run re-fetches only these; `--retries`
  already retried once for you inside the same run.
- **⚠ mismatch but the title looks the same** — look at `details` to see
  which field differed (author/journal/year are checked too). For a
  decisive verdict feed the expected metadata via `--claims-file`.
- **Capped at ⚠ partial** — a claimed field could not be checked (most
  often: no `title` in the claims), or the paper is RETRACTED (by design,
  with a human-review note).
- **Chinese references barely parse** — an ID-less Chinese line of ~12+
  characters still routes to OpenAlex title search; the verdict needs the
  registered title verbatim in the entry (a given year must match;
  journal is not required). Short fragments and prose paragraphs stay
  unknown — feed `--claims-file` (language-independent full verdicts) or
  add the ID.
- **A `.docx` produced no output** — the document carries no extractable
  text layer (scanned images): export to text/HTML first.

## Mixed intent (this skill or cite-holmes?)

| Request shape | Route |
|---|---|
| "verify these citations" / list attached | here (`--parse-text`/`--stdin`) |
| "write a literature review on X" | cite-holmes first, then audit the draft's list here |
| "check this DOI resolves" + verify intent | here (`--dois`) |
| "format my references" (already verified) | here (`--format-references`) |
| "format these citations" (never verified) | here too — `--format-references` verifies first by design |

## Restricted-network quick fixes

1. `--check-net` — see which of the four data sources + arXiv are reachable on which route.
2. Set `HTTPS_PROXY`/`HTTP_PROXY` (or unset dead ones — a stale proxy
   **masquerades as an outage**).
3. `--meta-source europepmc` when NCBI stays blocked.
4. `--timeout 60` on slow links; caching (30 days) absorbs repeat runs.

Full playbook: [operations.md](operations.md).
