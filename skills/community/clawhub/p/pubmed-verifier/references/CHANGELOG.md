> **何时读我**：想知道某版本改了什么、或对照旧版行为时。
> **最短路径**：SKILL.md 只保留最近三版摘要；完整 20 版历史在本文件逐字保留。
> **回 INDEX**：[INDEX.md](INDEX.md)

# pubmed-verifier — full release history

**Navigate by era** (v5.x and v4.x entries are self-contained; each
section reads standalone):

- **v5.x — capability era**: v5.4 grouped flags & cheat sheet · v5.3
  retraction reasons / doctor / JSONL / expandable HTML · v5.2 input
  guard & citation counts · v5.1 retraction detail & explicit precedence · v4.9 PowerPoint & ladder monotonicity ·
  v5.0 paste-and-verify & --quick
- **v4.x — document-reality era**: v4.8 Word/HTML input & second opinion · v3.8 verdict-ladder corrections ·
  v4.7 medical-document fixes · v4.6 finding ledger · v4.4 evidence
  pack · v4.3 GB/T author-date · v4.1 OpenAlex & CJK · v4.0 plain-text
  parsing & formatted lists
- **v2.x–v3.x — hardening era**: network hardening, retraction
  detection, DOI-native, arXiv, BibTeX/RIS, audit working-paper

Complete version history. The SKILL.md "Recent releases" section keeps
the recent highlights; everything older lives here verbatim.

## v7.0.0 — a healthier self-check, a one-liner claim, one CI command

Feedback-driven release (an independent test line exercised v6.9.0 for
real: all five verdict states, honest degradation and the 363-test
matrix held; no P0/P1 defects found). Three refinements landed:

- **Retraction-source health probe** — `--self-check` now runs six
  promises: five offline ones plus a live probe that picks a retracted
  record from PubMed's retracted pool and requires Europe PMC to agree.
  Upstream policies change (the Crossref Labs RW-annotations deprecation
  is the precedent); reachable-but-disagreeing sources FAIL loudly
  instead of drifting silently. Unreachable registries SKIP honestly —
  the offline promises still carry exit 0.
- **`--title` one-liner claim** — "is PMID X the paper titled T?" needs
  no claims file anymore: `--pmids X --title "T"` (optionally
  `--journal` / `--year`). A wrong title grades mismatch (the claim is
  user-typed, not heuristic parsing); a matching bare title grades
  correct via the existence+title route; adding `--year`/`--journal`
  keeps the conservative partial cap until authors are claimed.
- **One CI command** — `python3 tests/run_tests.py` runs the offline
  matrix with a milestone line (`--verbose` prints every test); the file
  ships in the package and guides package copies to `--self-check`.
  `MAILTO` joins `PUBMED_VERIFIER_MAILTO` as the polite-pool env
  fallback.

## v6.9.0 — two more verified-list styles: Harvard and Chicago

`--format-references` rendered five citation styles; two author–date
styles join: `--citation-style harvard` (`Surname, F.M. and Surname, F.M.
(Year) 'Title', Journal, Vol(Issue), pp. Pages.`) and
`--citation-style chicago` (`Surname, First, and First Surname. "Title."
Journal Vol, no. Issue (Year): Pages.`).

Both follow the verify-then-format loop: entries stand on
registry-verified records, author-date lists are sorted by first author
and printed unnumbered (as GB/T author-date already was), and
registry-truncated author lists close with et-al — never invented names.

## v6.8.0 — one home per fact, reader-facing docs lean

The Top-10 NOT-to-do table lived twice: a table in Quick FAQ plus the
numbered entries in Anti-patterns said the same things. The table is now
the speed index at the top of the Anti-patterns section and Quick FAQ
routes there — one fact, one home (EN+ZH, test-locked in both
directions).

The README restated large parts of the main doc. Its feature list is
grouped into four sections (verification core / outputs & audits /
resilience & honesty / shape & docs) with a leaner quick start, so the
repo landing page stays self-sufficient while the details live once, in
the main doc they belong to.

## v6.7.0 — the Files table reads the package, not the repo

The v6.6.0 evaluation held at 4.887 (all fifteen dimensions ≥ 4.8;
progressive recovered to 5.0). Both remaining seats named one concrete
defect: the main doc's Files table listed sample names that do not match
what the shipped package actually contains.

- **The Files table is now generated against the package**: every
  backticked path must exist, every package-carriable example/reference
  file must appear (by its full name — short forms like `.json` or
  `+_ZH` hid real files from the reader), and the native-extension
  `.bib`/`.ris` samples are explicitly marked "GitHub repo and zip
  only". Two test locks enforce both directions against the actual
  scripts/ and package whitelist.
- **The Use-cases section is gone** — four of its five bullets were
  already covered by the "When to use this skill" list one screen above
  (the progressive judges have flagged main-doc duplication for three
  releases running); pharmacovigilance verification moves there.
- SKILL_ZH Files table synced to the same shape.

## v6.6.0 — one count, one home per fact

The v6.5.0 evaluation reached 4.893 (ten dimensions at 5.0). Two of the
three remaining notes were the same defect in different seats: one page
still said "five pv_* modules" while `scripts/` holds six, and the main
document duplicated mechanics/performance details that live in the
reference pages.

- **The module count is now one fact, locked to the directory** —
  SKILL_ZH and python_api corrected to "entry file + six pv_* modules"
  (the accuracy judge quoted the stale "five" verbatim); a lock fails the
  suite if any channel-facing doc says five while `scripts/` holds six.
- **The main doc keeps summaries, references keep details** — the
  six-step mechanics block became a three-line summary pointing at
  usage_guide (the Jaccard/SequenceMatcher thresholds live there), and
  the stale measured-numbers Performance block now points at the
  operations batching math. The main doc drops under 500 lines, guarded
  by a lock.
- Honesty note kept: usage_guide's Worked-scenarios duplication and the
  single-file claim were fixed in v6.5.0 — this release closes the last
  two stale-prose seats the evaluations named.

## v6.5.0 — the documentation debt cleared where the judges read it

The v6.4.0 evaluation recovered to 4.873 (stability and errorHandling
back to 5.0 — the module split did exactly what it was built for). The
remaining notes all pointed at stale prose, so this release is a
documentation-debt payoff:

- **Worked scenarios, once** — usage_guide.md had carried the
  three-scenario walkthrough verbatim twice (three evaluations flagged
  it). One section remains, promoted to a top-level heading.
- **The stale single-file claim retired** — the tuning playbook still
  said "the verifier is a single stdlib-only file … (that portability is
  why the code is not split into modules)", directly contradicting
  v6.4.0. It now describes the real deployment shape (entry file + six
  siblings, copy the directory, --self-check verifies the copy) in a
  dedicated "Deployment shape" section.
- **Module counts made exact** — README and SKILL say "one entry file
  plus six stdlib-only sibling modules" (the scripts directory holds
  exactly seven Python files; a lock enforces the count and the wording).

## v6.4.0 — the module split: under the static-reader ceiling

The v6.3.0 evaluation did not crater because of a code change. The
judge's static reader stops at ~120 KB, and `verify_pmids.py` had grown
to 290 KB — the report read a file truncated mid-string and scored the
invisible half as corruption (stability 3.0, errorHandling 3.5, func
3.5). The same ceiling applies to any agent host reading the skill, so
this was a real distribution defect, not an evaluation artifact.

- **Layered modules, zero dependencies intact** — the file split into
  stdlib-only siblings: `pv_meta` (shared constants and helpers),
  `pv_netio` (transport, circuit breaker, registry fetchers),
  `pv_textio` (document extractors, citation-context parser, BibTeX/
  RIS/plain-text parsers, format sniffer), `pv_claims` (loaders,
  linters, skeletons), `pv_exports` (every report and bibliography
  generator) and `pv_cli` (argparse + the orchestration pass). The main
  file drops to 86 KB — about 72% of the ceiling, with headroom to keep
  growing.
- **API surface unchanged** — every public name is re-exported by the
  main module: `import verify_pmids as vp` keeps working exactly as
  documented in `references/python_api.md`, `vp.main()` included.
  Deployment is still "copy the scripts directory, no pip/venv".
- **Locks see the whole codebase** — every source-scanning test lock
  now reads all six files (`_all_src()`), and a static undefined-name
  scanner guards the split (it caught an OpenAlex-only constant the
  test suite never exercised).
- Known trade-off, stated honestly: `usage_guide.md` still carries a
  duplicated Worked-scenarios block (flagged by the previous two
  evaluations); the split was the structural priority.

## v6.3.0 — the bibliography samples finally travel

The v6.2.0 evaluation kept docking four dimensions for one packaging
fact the notes had only disclosed: the .bib/.ris sample files the docs
reference do not ride in the SkillHub package (its upload list skips
those extensions). Disclosure became a fix.

- **Content, not extension** — `--bibliography`, `--lint-claims` and
  `--claims-template` now sniff the bibliography format from the file's
  own markers (a BibTeX entry opens with `@type{`; an RIS record with
  `TY  - `), so renamed and extension-less files run as-is. Explicit
  `.bib`/`.ris` extensions keep priority; nothing about existing
  behavior changed for correctly-named files.
- **The samples travel** — `refs.sample.bib.txt` and
  `refs.sample.ris.txt` ship in the package next to the originals, and
  every command in the docs now works on every distribution channel:
  `--bibliography examples/refs.sample.bib.txt` runs out of the box.
- Two locks updated to lock the fix (parity requires the .txt copies;
  the file tables state the sniffer), and a new lock fails the suite if
  a documented sample ever lacks its package-carriable copy again.

## v6.2.0 — --self-check & the end of rotting numbers

The v6.1.0 evaluation held at 4.853 (docQuality back to 5.0 — the
consistency gate worked) while two dimensions asked for the same thing
from different seats: a shipped copy that can prove itself, and numbers
in the docs that do not rot.

- **`--self-check`** — the shipped single file can now verify itself:
  five core promises (the five-state ladder, claimed-field evidence,
  plain-text parsing, CSL export, version carriers) run offline with one
  OK/FAIL line each. Exit 0 = this copy is intact; a damaged or modified
  copy says so and asks for a re-download. CI and reviewers no longer
  need the repo to verify a download.
- **Numbers that rot, retired** — the operations manual's hard-coded
  "≈5,500 lines" (actual: past 5,800) loses the count; the data-source
  naming is unified everywhere to "four data sources + the arXiv
  preprint API" (the old mixed four/five sourcing is retired), with a
  lock that fails any return of "five data sources"/"five registries".
- **Distribution scope on the .bib/.ris samples** — the SKILL file
  tables (both languages) now state what examples/README.txt already
  said: those two samples ship with the GitHub repo and the zip, and the
  SkillHub package list skips the extensions.

## v6.1.0 — the doc-vs-artifact consistency gate

The v6.0.0 evaluation scored the tool 4.860 (a new high) but four
dimensions pointed at one and the same debt: README lists lagging the
parser, a license split across files, sample files whose notes did not
match the package, and one sample row demoing with placeholder metadata.
This release pays that debt down and bolts a gate in its place.

- **Samples demo the real world** — the DOI-only row in
  `examples/claims.sample.json` now carries the verbatim Crossref/PubMed
  record (all three sample rows grade correct end to end); the lock that
  replaced it drives `verify_doi_entry` on that very row, so a sample
  that stops matching the registries fails the suite instead of the
  demo.
- **README currency** — the File-types row lists all ten extensions the
  parser actually reads (`.docx`/`.pptx`/`.html`/`.nxml`/`.jats`/`.xml`
  had shipped without a README mention), and the Exit-codes row states
  the v5.8.0 flag-validation semantics; a lock compares the row against
  the parser's extension set.
- **One license, four files** — README, both SKILL frontmatters and
  `skillhub-meta.json` all say MIT-0 (the meta said plain MIT); a
  four-way lock keeps them aligned.
- **`examples/README.txt` completeness** — every sample file is
  documented (the refs-list sample had shipped undocumented), and the
  `.bib`/`.ris` samples note their distribution scope (GitHub/zip ship
  them; the SkillHub package list skips those extensions).

## v6.0.0 — JATS/NLM input, honest fallbacks, a leaner front door

The first 6.x major: input coverage reaches the PMC/NLM article format
that journal and repository pipelines actually produce, and the two
remaining silent behaviors (a damaged structured file degrading to a
byte scan; circuit-breaker jargon) are made visible.

- **JATS/NLM XML input (`.nxml`/`.jats`/`.xml`)** — the article format
  used by PubMed Central and journal export pipelines is extracted
  in-memory (paragraphs, titles, table cells, refs; `xlink:href` targets
  kept, 64 MB cap). Only a real NLM document is extracted: any other
  `.xml` falls through to the plain-text read, now with a visible
  `[NOTE]` (below). Directory scans include the new extensions.
- **No more silent fallbacks** — when a structured file (`.docx`,
  `.pptx`, `.html`, JATS `.xml`) produces no text and the tool degrades
  to a plain-text read, a `[NOTE]` line says so; results from such a
  file may be incomplete and the run says so up front instead of
  looking like a clean empty scan.
- **Circuit-breaker messages lead with the outcome** — the Chinese
  breaker notices now open with what happened and what it means for the
  run (source skipped, affected citations stay unknown, never false
  not-found) before the tuning hints.
- **A leaner front door** — Quick start keeps the ten commands that
  cover most runs with an explicit pointer to the flag cheat sheet; the removed commands all live in the scenario
  tables and [references/flags.md](references/flags.md).

## v5.9.0 — a troubleshooting index, a Chinese API page, mixed-intent rules

Shaped by the v5.8.0 audit follow-ups: documentation follow-ups asked
for the scattered error advice to meet in one place, domestic follow-ups
asked for a Chinese Python-API page, trigger follow-ups asked who wins
when two tasks are named in one request.

- **`references/troubleshooting.md` (+`_ZH`)** — one error, one row: the
  literal `[ERROR]`/`[WARN]` text → the cause → the one-command fix,
  covering exit codes, the flag-validation errors, breaker skips,
  skip-line parser messages, the wrong-looking-verdict cases, mixed
  intent, and restricted-network quick fixes. Routed from INDEX and both
  documentation maps.
- **`python_api.md` goes Chinese-first** — a 30-second quick-start block,
  a per-section Chinese summary line, and a translated notes section, so
  a code-integrating reader works from Chinese without cross-referencing.
- **Mixed-intent arbitration in the trigger section** — when a request
  names verification AND another task ("润色并核对文献"), the citation
  list belongs to this skill first; writing/polishing alone with no list
  never triggers it.
- **CJK boundary made concrete** — an ID-less Chinese line of ~12+
  characters routes to OpenAlex title search, and the verdict needs the
  registered title verbatim in the entry (a given year must match;
  journal is not required); short fragments and prose paragraphs stay
  unknown (`--claims-file` is the language-independent route).

## v5.8.0 — loud flags, visible breakers, runnable samples

Shaped by the v5.7.0 audit follow-ups: error-handling follow-ups asked
for clearer feedback at the edges (flag validation, breaker state),
documentation follow-ups asked for more runnable samples and a leaner
main document.

- **Immediate flag validation** — out-of-range values now fail before
  any work starts with `[ERROR]` + exit 2 (`--timeout 0`,
  `--cache-days -1`, `--threshold 1.5`, `--workers 0`, `--retries -1`),
  and soft over-ranges clamp with a `[WARN]` (`--workers 99` -> 8,
  `--retries 10` -> 3) instead of silently skewing the run.
- **Circuit-breaker visibility** — when the breaker skipped calls during
  a run, the run ends with one `[WARN]` line naming the hosts, the skip
  counts and the recovery path (the counts also land in
  `stats.breaker_skipped`), instead of leaving a pile of unknowns with
  no explanation.
- **Sample pack grows** — new `claims.sample.json` (the three claims
  row types in JSON) and `refs.sample.txt` (the three plain-text
  routing shapes in one list: inline PMID, inline DOI, title-only);
  both lint/parse clean, with commands in `examples/README.txt`. The
  `.bib`/`.ris` samples stay for GitHub/zip users.
- **Leaner main doc** — Recent releases keeps the last three rows
  (history lives in CHANGELOG), the Python section and the parsing note
  condensed; nothing load-bearing was removed.

## v5.7.0 — in-batch retry sweeps & reachable-means-reachable

Shaped by the v5.6.0 audit follow-ups: reliability follow-ups asked for
an in-batch retry mechanism, documentation follow-ups asked for the FAQ
to stop hiding behind the anti-pattern tables.

- **`--retries N` (default 1)** — after each batch fetch stage (PMID
  metadata, DOI resolution, linked-PMID metadata), the calls the network
  lost re-run once after a 2 s cool-off; recovered citations get real
  verdicts in the same run instead of forcing a full re-run, and the
  recovery count lands in `retried_recovered` (stderr `[NOTE]` lines,
  JSON/HTML stats). A sweep never worsens a run: a still-open circuit
  breaker aborts it and first-pass answers stand; `--retries 0` restores
  the old single-pass behavior.
- **`--check-net` semantics fix**: any HTTP response — including a 429 —
  now counts as reachable (the host answered); only transport-level
  failures (DNS, refused connection, timeout) report unreachable. A rate
  limit is no longer misread as an outage, which matters in restricted
  networks where 429s are common.
- **Quick FAQ** — the main doc separates plain questions (with short
  two-line answers: unknown vs invalid, partial caps, retry behavior,
  claims-file timing, Zotero import, restricted networks) from the
  anti-pattern tables, so neither has to stand in for the other.

## v5.6.0 — CSL JSON export & dual-route network pre-flight

Two additions aimed at where the tool meets real workflows: the library
manager on one side, the restricted network on the other.

- **`--export-csl FILE`** — the verified bibliography as CSL JSON, the
  open citation-format standard: Zotero ingests it via File > Import,
  and Mendeley and Pandoc read the same file. Correct entries
  land as article items with the registry's own author/journal/year/
  DOI fields; partial entries carry a verify-manually note; retracted,
  mismatched and unknown entries are excluded (same inclusion rules as
  the BibTeX and RIS exports). The evidence pack includes it as
  `verified-refs.csl` (now eight files).
- **`--check-net` probes every source twice** — once ignoring proxy
  settings, once through your `HTTPS_PROXY`. A source that is blocked on the
  direct route but reachable through the configured proxy now reports
  as usable instead of unreachable, and every line names the
  verification paths that source serves plus the in-tool fallback
  (e.g. NCBI → `--meta-source europepmc`). Clearer answers for
  restricted-network environments, with no new flags to learn.
- **Boundaries surfaced**: the two limits readers had to dig into
  reference pages for (scanned-PDF input has no extractable text; very
  large batches need slicing) now sit in the main doc's "Know before
  you run" table.

## v2.2.0 — network hardening

| Feature | Flag | Effect |
|---------|------|--------|
| NCBI API key | `--ncbi-api-key` / env `NCBI_API_KEY` | Rate ceiling 3→10 req/s, batch interval 0.4s→0.12s (~3x faster) |
| Europe PMC fallback | `--meta-source auto\|ncbi\|europepmc` | NCBI batch failure automatically retries via Europe PMC (free, no key); per-entry origin in JSON (`meta_source`) |
| Crossref polite pool | `--mailto` / env `PUBMED_VERIFIER_MAILTO` | `?mailto=` on Crossref + tool/email params on NCBI — more generous limits |
| Retry-After backoff | automatic | 429 responses honored (clamped 1–5 s) instead of failing |
| UA rotation | automatic | 403/406 retried with a browser User-Agent |
| Host circuit breaker | automatic | After 2 call-level transport failures a host is skipped with an actionable message; success resets; HTTP errors never trip it |
| Honest unknown | automatic | Network failures report as ❓ unknown + exit code 2, never as "PMID not found", and are never cached |

**Exit codes:** `0` clean · `1` problems found (invalid / mismatch / retracted /
DOI-splice, incl. arXiv claimed-DOI pairing mismatches) · `2` could not verify
(data sources unreachable) — automation can tell "all good" from "no answer".

## v2.3.0 — retraction detection

With `--verify-doi`, each cited DOI is also checked against Crossref's
withdrawal records (`updated-by`). A paper Crossref lists as RETRACTED is:

- flagged in JSON (`retracted: true` + `retraction_note`) and in reports,
- **capped at 🔶 partial** even when every metadata field matches — citing a
  retracted paper is never "correct"; the report says *human review required*.

Corrections and other update types do not trigger the cap. Crossref outages
never flag anything (a missing check is not a retraction).

## v2.4.0 — DOI↔PMID cross-check & journal abbreviations

- **DOI splice detection**: add a `doi` field to your claims (JSON or CSV).
  The claimed DOI is compared with the DOI registered for that PMID — a
  mismatch is a splice/fabrication signal (a real DOI attached to the wrong
  paper): flagged in JSON (`doi_splice_suspect`), verdict capped at 🔶
  partial, counted in exit 1. Uses the PubMed record only — no extra API call.
- **Journal abbreviation equivalence**: journal matching now understands
  NLM-style abbreviations in both directions — "N Engl J Med" matches "New
  England Journal of Medicine", "Pediatr Rheumatol" matches "Pediatric
  Rheumatology" (in-order word prefixes, function words skipped). No more
  false "journal differs" for abbreviated citations.

Known limits: highly ambiguous abbreviations can over-match at the
journal-only level ("J Immunol" ~ "Journal of Immunology Research") — the
title remains the decisive field. A DOI-splice flag can also appear on an
otherwise-unverifiable citation (the DOI mismatch is an independent fact).

## v2.5.0 — author-name verification

- **Initials never match**: single-letter tokens ("A.", "L.") on either side
  are excluded from surname matching — an initial is not evidence, and
  substring-matching one produced false author hits.
- **Cross-language honesty**: CJK author names claimed against Latin
  registry records (or the reverse) are skipped, not counted as a mismatch —
  the report marks them `author_check: skipped` and the verdict falls back
  to what was actually comparable (title/journal/year), or to ❓ unknown
  when nothing else is checkable.

## Security & behavior declaration

- Single-run CLI: scan, verify, write the report, exit. No daemons, no
  background jobs, nothing downloaded or installed at runtime (pure standard
  library, zero dependencies).
- Network access is limited to these official academic registries, always
  over HTTPS: `eutils.ncbi.nlm.nih.gov`, `www.ebi.ac.uk` (Europe PMC),
  `api.crossref.org`, `api.openalex.org`, `export.arxiv.org` — no other
  hosts are contacted; no telemetry, no
  analytics, no data collection — the only outbound payloads are the PMIDs,
  DOIs and titles you asked to verify.
- Your files and reports stay on your machine. Writes are limited to the
  report paths you pass and the SQLite cache under
  `~/.cache/pubmed-verifier/` (`--no-cache` to disable).
- Optional environment variables `NCBI_API_KEY` / `PUBMED_VERIFIER_MAILTO`
  authenticate or attribute your own API requests and are never sent
  anywhere else.
- No OS integration: no subprocesses, no system services, no privilege
  changes, no scheduled tasks.

## v2.6.0 — audit working-paper & report v2

- **`--export-audit audit.json`** — a self-contained JSON working-paper for
  transparent review: tool identity and version, the exact (API-key-redacted)
  invocation, per-citation evidence chains (claimed vs registered fields,
  title match scores from both algorithms, author match with cross-language
  skip records, DOI cross-check, retraction signals) and the
  verdict-ladder trace for every citation. A reviewer can replay the entire
  verification from this file alone.
- **HTML report v2** — verdict filter tabs, severity-sorted rows (retracted
  and DOI-splice first, highlighted), a field-level evidence column
  (title/author/journal/year ✓✗—) and a reproducibility footer (redacted
  command line + version + data sources).
- **Reliability** — negative cache entries now expire after 3 days (a
  legitimately new, ahead-of-print PMID is no longer reported "not found"
  for a month), and the circuit breaker self-heals: after a 30 s cooldown it
  admits one probe call and resets on success.

## v2.7.0 — retraction for every PMID, BibTeX export, readiness verdict

- **Retraction detection, source-independent** — the registry's own
  publication type ("Retracted Publication"; present in both NCBI esummary
  and Europe PMC) now flags retracted papers for EVERY citation: no DOI
  required, no `--verify-doi` required, and the flag survives the cache
  (schema v3). Crossref `updated-by` remains the detail source (the
  retraction-notice DOI) when `--verify-doi` is on. A retraction *notice*
  itself is never flagged.
- **`--export-bibtex refs.bib`** — export the verified bibliography: correct
  entries as `@article`, partial entries commented out with their divergence
  note, mismatched/invalid/unknown/retracted entries excluded and counted.
- **Submission-readiness verdict** — every report now leads with one line:
  `SUBMISSION READY` or `NOT SUBMISSION-READY — <per-problem counts>`.
- Cache schema v3 (adds a `retracted` column, auto-migrated).

## v2.8.0 — DOI-native verification & delta audits

- **`--dois "10.x/a, 10.y/b"`** — verify DOIs natively, no PMID required.
  `--source` scans now also extract DOIs from your files automatically.
  Each DOI is resolved via the Crossref works API: not-found on an explicitly
  provided DOI = fabrication signal (invalid, exit 1); on one auto-extracted
  from scanned text it stays a suspect (unknown) — scanned strings are never
  user-endorsed, and DataCite/repository DOIs do not live in Crossref, so
  always double-check at doi.org. Resolved = existence confirmed with the
  registered metadata attached for manual comparison — *existence is never
  dressed up as a match*.
- **`--diff previous-audit.json`** — delta audit against a previous working
  paper: **newly retracted** (the safety signal — a paper retracted after
  your last audit; act on it: swap or drop the citation, cite the retraction
  notice instead, and re-check any conclusion that relied on it), degraded,
  improved, new and dropped citations, with counts in every report format.
  Built for periodic knowledge-base audits: "what changed since last time?"

## v2.9.0 — DOI entries become first-class

- **DOI→PMID linking** — a resolved DOI is linked back to its PMID via the
  Europe PMC DOI field query, pulling the full PubMed record: complete
  metadata, retraction pubtype signal, and cache coverage. A DOI citation
  now gets the same five-state record as a PMID citation (existence
  confirmation only — the verdict remains unknown until claims are
  provided).
- **Parallel DOI resolution** — `--workers N` (default 4, max 8) resolves
  DOI batches on a thread pool (roughly 3x faster on large lists), with
  live progress output. For large `--dois` batches, set `--mailto` to stay
  in Crossref's polite pool.
- **`--export-csv table.csv`** — spreadsheet-friendly audit table
  (key/verdict/flags/fields/details; formula-injection hardened).

## v3.0.0 — arXiv ID verification (three citation types, one audit)

Reference lists carry preprints. v3.0.0 verifies **arXiv IDs** alongside
PMIDs and DOIs: `arXiv:2401.12345` and `arxiv.org/abs/...` patterns are
extracted from scans (or passed via `--arxivs`), checked against the
official arXiv API, and judged — nonexistent ID = fabrication signal
(invalid, exit 1); resolving ID = registered title/year attached, verdict
stays unknown. Malformed IDs (bad YYMM month) are flagged by shape.
Timely: arXiv penalizes submissions containing hallucinated or unverified
references (2026-05 policy) — audit before you submit.

## v3.3.0 — preprint ↔ published-version cross-check

arXiv entries carry the version-of-record DOI their authors registered at
publication (`arxiv:doi`). v3.3.0 puts it to work:

- **Claimed DOI vs registered DOI** — a claims row with both `arxiv_id`
  and `doi` is cross-checked: agreement is reported as evidence
  (`fields.doi ✓`); disagreement caps the verdict at `partial` — the DOI
  belongs to a different paper (same failure class as PMID DOI-splice).
- **Version of record surfaced** — verifying a bare preprint ID now shows
  the registered DOI and, when the published version is PubMed-indexed,
  its linked PMID — cite and verify the final version, not just the
  preprint.
- **Honest accounting** — the readiness line counts arXiv DOI-pairing
  mismatches as problems; DOI/arXiv phase progress (stderr) now includes
  elapsed time and an ETA for large batches.
- Context parsing no longer truncates titles at sentence-internal
  abbreviations ("U.S. population", "e.g.", "vs.", "Vol.").

Pairing example (match → correct with DOI evidence; wrong DOI → partial):

```bash
python3 scripts/verify_pmids.py --claims '[{"arxiv_id":"2005.13892",
  "title":"City size and the spreading of COVID-19 in Brazil",
  "doi":"10.1371/journal.pone.0239699"}]'
```

## v3.4.0 — DOI claims become first-class

Claims rows could carry a PMID or an arXiv ID — a row keyed by DOI alone
was silently ignored, and DOI entries always stayed `unknown` ("no claimed
metadata to cross-verify"). v3.4.0 closes the matrix: all three citation
types now accept claimed metadata.

- A claims row with a `doi` (no PMID, no arXiv ID) is cross-checked against
  the registered metadata — the linked PubMed record when the DOI resolves
  to one, Crossref otherwise — and gets the full verdict ladder:
  correct / mismatch / partial.
- Retraction capping applies as everywhere: a claimed-correct match on a
  retracted paper is capped at partial with the retraction note.
- Without claims, DOI entries stay unknown — existence is never dressed up
  as a match.

```bash
python3 scripts/verify_pmids.py --claims '[{"doi":"10.1371/journal.pone.0239699",
  "title":"City size and the spreading of COVID-19 in Brazil",
  "journal":"PLoS ONE","year":"2020"}]'
```

## v3.5.0 — claims lint & usage-first restructuring

- **`--lint-claims FILE`** — offline pre-flight for claims files
  (JSON/CSV, zero network): ID shape errors, missing titles (the verdict
  would cap at partial), unknown/typo'd columns, DOI prefix checks,
  unusable rows — exit 1 on errors. Fix the format before the run
  instead of guessing from weak verdicts.
- **Documentation restructured around usage**: FAQ, anti-patterns and
  declared boundaries now sit right after Quick start, led by a Top-10
  "don't do this" table; new **Best practices & tuning** section (API-key
  batching, worker tuning, two-phase deep-verification, cache policy,
  scale expectations — and why the verifier is deliberately one file).

## v3.6.0 — BibTeX bibliography audit

**`--bibliography refs.bib`** audits a .bib file directly: entries route by
PMID (the `pmid` field, or a "PMID: NNNN" in the note — including the
notes `--export-bibtex` itself writes) > DOI > arXiv (`eprint`, or an
"arXiv:XXXX.XXXXX" in the journal/note), each carrying its claimed
title/authors/journal/year for the full cross-check. Entries without any
routable ID are counted and skipped. This closes the loop with
`--export-bibtex`: a verified bibliography can be re-audited after edits.
`--lint-claims refs.bib` validates the file offline (unroutable entries,
missing titles, unclosed blocks).

## v3.7.0 — RIS bibliography support

`--bibliography` now accepts **RIS files** (`refs.ris` — Zotero/EndNote/
Mendeley exports) alongside BibTeX: records route by PMID (AN tag, or a
"PMID: NNNN" note) > DOI (DO) > arXiv (UR/eprint), each with claimed
metadata for the full cross-check. **`--export-ris`** completes the loop —
verified entries as `TY JOUR`, partials as `TY DATA` with a PARTIAL note.
`--lint-claims refs.ris` validates offline (unroutable records, missing
titles, duplicates, unterminated records).

## v3.8.0 — verdict-ladder corrections (independent external test audit)

An independent real-data audit (24 scenarios, registry-ground-truthed) found
three judgment-ladder defects; all three are fixed and locked:

- **B1 scan false positives** — when a citation is not the first sentence of
  its block, the author line was taken as the claimed title (correct
  references reported as mismatch). The parser now shifts past an
  author-shaped segment.
- **B2 author mis-attribution** — a claimed author set entirely different
  from the registry (zero surname overlap) was still reported as correct
  when title and journal matched; it now caps at partial. Partial surname
  overlap (abbreviated or reordered names) keeps correct.
- **B3 title-less claims** — author+journal+year matches without a claimed
  title now cap at partial, exactly as the FAQ/anti-patterns/boundaries
  always promised (the same author/journal/year can cover several papers).
  Cross-language author skips follow the same cap.
- Also: duplicate arXiv IDs announce their merge on stderr (run
  `--lint-claims` to catch duplicate claim rows offline); the
  cross-language skip no longer coexists with contradictory details text;
  empty `--claims` gets a one-line hint; docs state that Chinese-language
  citation contexts parse weakly — use `--claims-file`.

## v3.9.0 — Chinese references (GB/T 7714), network pre-flight, Python API

- **GB/T 7714 Chinese references parse** — `……标题[J]. 刊名, 年… PMID: xxx`
  contexts now yield the title (via the `[J]/[M]/[R]` type marker),
  authors, journal, year and any DOI that follows the PMID. The title
  comparison against a Latin registry title is skipped cross-language
  (never a mismatch source); a DOI in the reference is cross-checked
  against the registry like any claims DOI. Requires a PMID marker per
  reference.
- **`--check-net`** — probes the data sources (5 s each), shows your
  proxy state and prints practical next steps when something is
  unreachable. Run it when results come back unknown on a constrained
  network.
- **Python API reference** — `references/python_api.md` documents the
  stable importable surfaces (`fetch_summaries`, `cross_check_citation`,
  `verify_doi_entry`, `parse_citation_context`, `suggest_correct_pmid`)
  with copy-paste examples.

## v4.0.0 — plain-text reference lists & formatted reference list export

- **`--parse-text refs.txt`** — verify a reference list copied straight out
  of a manuscript draft. Numbered entries (`[1]`, `1.`) split cleanly;
  inline PMID / DOI / arXiv IDs route exactly (full five-state
  cross-check); a markerless entry with a parseable title resolves via
  PubMed title search and is marked `resolved_by: title_search` — weaker
  evidence than a supplied ID, honestly labeled, and never a mismatch
  source. A network failure stays unknown with a retry hint, never
  "not found". Entries with no routable ID and no usable title are
  skipped with a note instead of being guessed.
- **`--format-references out.txt --citation-style gbt|vancouver|apa|ama`**
  — the formatting leg of verify-then-format: verified entries rendered as
  a ready-to-paste numbered reference list (GB/T 7714-2015 numeric for
  Chinese submissions, Vancouver, APA 7th, AMA 11th). Formatting stands on
  registry-verified records only: correct entries form the list, partial
  entries go to a manual-review section (never silently dropped), and
  retracted entries are excluded with a warning. Author lists are
  formatted per style without inventing names — a registry-truncated list
  closes with the style's et-al form, and APA discloses the truncation.
- Markerless Latin references now parse through the full sentence
  segmentation (titles feed the title-search leg); CJK entries without a
  PMID/DOI marker keep the documented weak-parsing boundary — supply a
  PMID or DOI for exact routing.
- `examples/refs_list.sample.txt` ships a ready-made parse-text fixture.

## v4.1.0 — OpenAlex fallback & Chinese-reference title search

- **OpenAlex is now the fourth data source** — a DOI that Crossref reports
  404 gets a second look at OpenAlex before any verdict: DataCite, Zenodo,
  SSRN and Chinese-registry DOIs (which do not live in Crossref) become
  fully decidable — resolved, metadata attached, claims cross-checked,
  retractions flagged (`is_retracted`). Only when OpenAlex also comes up
  empty do the original 404 semantics stand (explicit DOI = invalid,
  scanned DOI = suspect). `--check-net` probes five sources now.
- **Chinese references without any ID can now be verified** — a markerless
  CJK entry in `--parse-text` searches OpenAlex by its title (the query is
  the title-shaped segment of the entry, not the whole line); a candidate
  counts only when its registered title appears **verbatim** in your entry
  text with an agreeing year, and the verdict carries
  `resolved_by: openalex_cjk_search`. No hit = honestly unknown; this leg
  never manufactures a mismatch, and a network failure stays unknown.
- Docs: the reports' actual shape is now shown in "What the output looks
  like"; three worked scenarios added to the FAQ (reviewer evidence,
  thesis citation check, PRISMA screening).

## v4.2.0 — retraction replacement suggestions & delta detail panel

- **Retraction replacement suggestions** (`--suggest`) — a retracted entry
  now comes with up to three same-topic live candidates (retracted papers
  and the entry's own PMID excluded), marked `replacement_for_retracted`
  and carrying an honest note: they are search suggestions, NOT verdicts —
  verify each before citing. Answers the reviewer question "this paper is
  retracted, what should I cite instead?" at audit time.
- **Delta audits now show their full detail** — alongside the counts
  line, the HTML report renders a per-category panel (newly retracted /
  degraded / improved / new / dropped, up to 50 rows each); the markdown
  report lists degraded/improved/new/dropped rows too. Built for PRISMA
  re-runs: you only re-read what changed.
- `--check-net` masks proxy credentials (`http://user:****@host:port`) so
  the pre-flight output is paste-safe.
- Docs: "Trigger words" and "Use from Python" sections moved up front.

## v5.5.0 — the operations playbook & a written error contract

Shaped by the v5.4.0 audit follow-ups (the same gap named from three angles (FAQ depth,
advanced-usage guidance, error handling): bulk batching, proxy setup and
the failure contract lived only in scattered sections. One page now owns
them:

- **`references/operations.md`** — the batching math (per-path API cost
  table + a worked 3,000-citation example), the three real proxy
  scenarios (corporate, dead-env masquerade, CI direct) with
  `--check-net` as the arbiter, a speed checklist in decision order, a
  minimal CI gate, and a section map of the main script.
- **The error contract, written down**: three exit codes and the stderr
  marker vocabulary (`[ERROR]` the run cannot proceed / `[WARN]`
  ambiguous invocation proceeding with stated precedence / `[NOTE]`
  informational guard) — markers normalized in the tool's own output to
  match.
- Routed from INDEX and both documentation maps.

## v5.4.0 — grouped flags, cheat sheet, citation sort

- **`--help` is grouped by task domain** (inputs / verification depth /
  output & exports / network & performance / institutional & diagnostics)
  — 38 flags in one flat list was the top usability complaint; the same
  grouping now scans top-to-bottom. Zero behavior change: only where each
  flag appears in `--help`.
- **`references/flags.md`** — the scenario→command cheat sheet: the 90%
  scenarios are each ONE command with ZERO extra flags, then the full
  flag map in the same grouping as `--help`. Routed from INDEX and both
  documentation maps.
- **`--sort cited`** — report rows ordered by citation count descending
  (Europe PMC/OpenAlex counts; entries without a count keep their
  severity position at the back). Affects the terminal/JSON/JSONL/
  markdown reports; the HTML report always keeps its severity layout.

## v5.3.0 — retraction reasons, doctor, JSONL, expandable HTML

- **Retraction reasons**: a retracted citation now distills WHY from the
  retraction notice record — the notice abstract when Crossref carries
  one, else the notice title only when it names the offence; the bare
  original title inside "Retraction Note: <original title>" never
  masquerades as a reason. Fields: `retraction_reason`,
  `retraction_notice_title`, `retraction_reason_doi` — in JSON, the
  audit chain, the HTML detail rows and the markdown report. Wired on
  both the PMID `--verify-doi` path and the DOI-native path
  (`--dois`, bibliography routing).
- **`--doctor`**: environment self-check — tool/Python versions, cache
  path and entry count (a stale-table cache reports as a finding),
  NCBI key / mailto / proxy configuration; `--doctor --check-net`
  includes the five-registry probe. Read-only, paste-safe.
- **`--jsonl PATH`**: one citation per line + a final `{"_stats": ...}`
  line — stream-friendly output for agent pipelines.
- **HTML inline evidence**: every table row gains a native
  `<details>` expansion with the full evidence trail (claimed vs
  registered, match booleans, answered-by registry, route, citation
  count, retraction reason) — zero JavaScript, and the verdict filter
  keeps the detail rows in sync.

## v5.2.0 — quantified input guard & citation counts

- **`--max-entries` guard**: the vague "large scans take hours" became a
  number — the de-duplicated workload (PMIDs + DOIs + arXiv IDs +
  title-search entries) is counted and compared against a threshold
  (default 2000); over it, a NOTE prints the actual count, the expected
  cost and a split recommendation. `--max-entries N` raises it, `0`
  silences it.
- **`cited_by_count`**: citation counts ride responses that already carry
  them (Europe PMC `citedCount`, OpenAlex `cited_by_count`) — zero extra
  requests. Surfaces in JSON/markdown ("· 128 cited" in the evidence
  cell). The NCBI path reports none, honestly.
- **Trigger section by pattern**: when-to-invoke is now described as
  patterns (MUST invoke / MUST NOT invoke alone) plus a combination-run
  table, on both language pages — an enumerated keyword list misses
  boundary phrasings.
- Boundary table row now quantifies the guard and the arXiv floor
  (1,000 arXiv IDs ≈ 50+ minutes).

## v5.1.0 — structured retraction detail & explicit precedence

- **Structured retraction detail**: every retraction now carries a
  `retraction_type` (retraction vs **removal** — the paper withdrawn
  from the record entirely, newly detected via Crossref
  `updated-by`), on top of the existing note/date/source. Wired through
  all three registries (NCBI/Europe PMC/Crossref), the JSON/audit
  evidence chain (`retraction.type`) and the markdown report flags
  (`[RETRACTED:removal (2024-03-01)]`).
- **Explicit precedence**: `--pmids` together with `--source` now
  announces on stderr that `--pmids` wins and the scan input is ignored
  — silent no-ops look like bugs from the outside.
- **Mainland-China usage guide**: one concentrated page (pre-flight,
  registry fallback, proxy semantics, package mirror, honest-failure
  contract) on both language pages — the network guidance had scattered
  across sections.
- **Boundary table** gains input-scale/concurrency and
  explicit-precedence rows; the HTML report's structure is now
  described where the text output sample lives.

## v5.0.0 — paste-and-verify, one-flag final pass, leaner main doc

Shaped by the v4.9.0 audit follow-ups (FAQ depth, trigger-boundary
clarity, flag-combination onboarding, main-doc length):

- **`--stdin` — paste-and-verify**: a copied reference list goes straight
  down the pipe (`pbpaste | verify_pmids.py --stdin`, `git show
  HEAD:refs.txt | verify_pmids.py --stdin`). Same numbered/heading parser
  as `--parse-text`; the report labels the source "stdin" — no temp file
  choreography in agent workflows.
- **`--quick` — the pre-submission final pass in one flag**: `--no-cache`
  (fresh registries) + `--verify-doi` (Crossref cross-check) +
  `--suggest` (correct-PMID hints) combined. Explicit user flags always
  win; --quick only sets what wasn't given.
- **FAQ depth**: a format-specific "when parsing fails" table in
  references/usage_guide.md (damaged office files, CJK without IDs,
  numbering variants, fragmented titles, reading the `fields` table,
  all-unknown = network).
- **Trigger boundary made explicit**: a pasted reference list IS the
  input — no explicit "verify" wording required (both language pages).
- **Main doc slimmed**: SKILL.md 579 → ~450 lines (recent-release rows
  sink into references/CHANGELOG.md, orphan historical section removed);
  SKILL_ZH.md mirrors.

## v4.9.0 — PowerPoint input & verdict-ladder monotonicity

Both grown from re-running the real rheumatology-literature audit (the
v4.7.0 acceptance sample) against v4.8.0:

- **`.pptx` decks are read directly** (`--source` and `--parse-text`):
  every slide in numeric order plus the speaker notes (DrawingML
  `a:p`/`a:t`, the same in-memory zip+XML family as .docx) —
  patient-education courseware audits without a copy-paste pass. A
  damaged file falls back to a raw read; directory scanning includes
  `.pptx`.
- **Verdict-ladder monotonicity**: the acceptance rerun surfaced
  citations grading PARTIAL on "title matches but author/journal not
  claimed" — a STRONGER evidence position than the bare existence
  checks that grade correct. On scanned sources, a partial whose only
  gap is the missing author claim (title matched; journal and year
  never claimed) now grades **correct** with `route:
  existence_title_match` and a detail line pointing at `--claims-file`
  for the full pass. An entry claiming journal/year/authors anything
  keeps its partial — those claims were checked and something differed,
  a real doubt. In the acceptance sample this resolved 4 of the 6
  manual-review items; the remaining 2 keep partial for real reasons
  (no title recoverable + author/journal differ; year claimed and
  differing).
- cross_check_citation itself is unchanged — the upgrade lives in the
  pipeline layer, so explicit `--claims-file`/CLI inputs always receive
  the full verdict.

## v4.8.0 — Word/HTML input & the title second-opinion leg

Two capabilities grown from the same medical-document reality testing:

- **`.docx` and `.html` inputs are read directly** (`--source` and
  `--parse-text`): Word paragraphs/tables are extracted in-memory from the
  document XML, exported HTML pages are tag-stripped with block elements
  as newlines. `script`/`style` content is dropped; `href`/`src`/`cite`
  link targets are KEPT (citations live in link targets on exported
  pages). A damaged .docx falls back to a raw read instead of failing the
  scan. Directory scanning now includes `.docx`.
- **The second-opinion leg for title-only claims**: the v4.7.0 mismatch
  gate correctly refuses to accuse on heuristic single-field claims — but
  "honest-but-unhelpful" left real wrong-PMID citations undiscovered. The
  gate now re-checks the claimed title phrase against PubMed's own
  `[Title]` index (quoted-phrase query): corroboration by the SAME PMID
  upgrades the verdict to correct (labeled `route: inline_title_search`,
  weaker evidence than a user-supplied ID — reachable exactly where the
  claimed title is a shortened variant that fails similarity thresholds
  but appears verbatim in the registered title); a phrase hit on a
  DIFFERENT record surfaces the `wrong_pmid_signal` evidence while the
  verdict stays unknown; no hit or a network failure stays unknown. The
  leg only confirms or reports —
  it never manufactures a mismatch, and CJK titles skip it (the OpenAlex
  CJK leg owns those).
- Docs: a documentation map on both main pages (what lives where — full
  version history, full FAQ, Python API reference, task router), the
  Trigger words section now states when `--claims-file` is required and
  where the cite-holmes boundary sits, and the boundary tables cover the
  new input formats and the second-opinion leg.

## v4.7.0 — real medical-document fixes (literature-export testing)

Found by running the verifier against a real rheumatology literature
export (385-entry file, 2026-10-14): 17 of 20 citations were false
mismatches because registry-metadata list lines ("- DOI: ...") directly
above a PMID were taken as the claimed title.

- Metadata list lines and "Year | Journal | Authors" table rows are now
  stripped before citation segmentation; when a flattened export leaves a
  single "## Title" line, that line IS the claim.
- A live PMID with no claimed metadata is an explicit **existence
  confirmation** (`existence_confirmed: true`, counted in the finding
  ledger as answered) — the old "Insufficient claimed metadata" wording
  treated the user's existence check like an error.
- `--source` merges a scanned DOI into its already-verified PMID (one
  paper, one finding; explicit `--dois`/claims are never merged).
- `--parse-text` reads "## Title" heading exports as entry boundaries.

## v4.6.0 — finding ledger & claims skeleton generator

- **Finding ledger** — text and HTML reports close with an explicit
  bookkeeping page: every planned citation is answered (correct / mismatch
  / invalid), partially answered (partial — the manual-review pool), or
  unresolved (unknown) with the reason and the next action, plus a budget
  line (citations checked / network errors).
- **`--claims-template SRC,OUT`** — reverse-generates a claims CSV
  skeleton from a plain-text reference list, .bib or .ris: every routable
  field the parsers can see (PMID, DOI, arXiv ID, title, authors, journal,
  year) is filled; fill the gaps and run `--claims-file` for the exact
  five-state path.
- Docs: capability×limit boundary table; FAQ slimmed to the top-4 with the
  full list in references/usage_guide.md; 30-second entry blocks on every
  reference file; references/INDEX.md task router; anti-pattern table
  gains the don't-repeat-burned-calls row; Skip-when negative triggers in
  the description.

## v4.5.0 — card conversion: icon + search-intent coverage

A proper skill icon (the splice-detection visual) went live with this
release, and the description now covers five more search intents verbatim
(参考文献生成 / 文献真伪 / 文献核对 / 引用核查 / 论文引用), first line
leading on citation authenticity. No code changes.

## v4.4.0 — submission evidence pack & leaner main doc

`--report-bundle DIR` — one command writes the complete evidence pack
(audit + HTML + BibTeX/RIS + CSV + GB/T list + self-describing manifest).
Full version history moved here from SKILL.md; OpenAlex 429 retries back
off at least 5s.

## v4.3.0 — GB/T author-date style & monograph journal fix

- **`--citation-style gbty`** — the second GB/T 7714-2015 form Chinese
  journals and theses actually ask for: unnumbered entries, no [J] type
  tag, sorted by first author (Latin casefold; CJK stays in Unicode order
  — true pinyin sorting needs an external library and is a documented
  manual step). Verified entries only, exactly like the numeric style.
- **Monographs no longer fake a journal** — GB/T parsing extracted the
  segment after the type tag for every entry, so `[M]` (monograph),
  `[R]` (report) and `[D]` (thesis) records picked up the PUBLISHER as
  the claimed journal and manufactured false journal mismatches. Only
  `[J]` entries yield a journal now; the others leave it empty.
- Docs: a "Know before you run" four-limit digest sits at the top of
  SKILL.md (each limit with its one-flag workaround), and the Trigger
  words section gained three request-to-action mappings.
