> **何时读我**：遇到 FAQ 之外的报错、网络/代理问题、批量提速与 CI 集成、或想深调缓存与阈值时。
> **最短路径**：先看 SKILL.md 的「Know before you run」四条限制与 Quick start——90% 的问题在那里已有单参数解法。
> **回 INDEX**：[references/INDEX.md](INDEX.md)

# Usage guide — FAQ（完整版）· 场景演练 · 最佳实践

## FAQ — full list

**❓ unknown vs ❌ invalid?**
`unknown` (exit 2) = "could not verify, sources unreachable" — retry later;
`invalid` (exit 1) = "verified not-found". Network failures are never
reported as not-found and never cached.

**What does RETRACTED mean in a report?**
The registry itself lists the paper's publication type as "Retracted
Publication" (checked for every citation since v2.7.0 — no DOI or flags
needed), and/or Crossref records a retraction (or, since v5.1.0, a removal — the paper withdrawn from the record entirely; the markdown flag then reads `[RETRACTED:removal (date)]`, and JSON carries `retraction_type`). The verdict is capped at
partial and a human review note is attached — citing it would propagate
withdrawn science. A retraction *notice* is never flagged; papers under
*Expression of Concern* (an editorial note, not a retraction) are not
flagged either. Retraction status reflects the registry at cache time — for
a final pre-submission check, run with `--no-cache`.

**Where does `retraction_reason` come from?**
v5.3.0 fetches the retraction NOTICE itself (the DOI in `updated-by`) and distills its abstract — or, when there is no abstract, its title only if the title names the offence. Many notices are literally "Retraction Note: <original title>"; there the honest output is the notice citation (`retraction_notice_title` + `retraction_reason_doi`), never the original title pretending to be a reason. `--doctor` checks the rest of your environment.

**Mismatch reported but the title looks similar?**
Check `details` for which field diverged; thresholds are strict on purpose.
Feed the full citation via `--claims-file` for a precise verdict.

**Can I audit my .bib or .ris file directly?**
Yes — `--bibliography refs.bib` (BibTeX) and `--bibliography refs.ris`
(RIS/Zotero/EndNote/Mendeley) route each entry by PMID > DOI > arXiv
and cross-check the claimed metadata. `--lint-claims` validates either
format offline first. The round trip works both ways: `--export-bibtex`
and `--export-ris` output can be fed back after edits.

**Can I get the verified entries into Zotero?**
`--export-csl library.json` writes the verified bibliography as CSL
JSON — Zotero ingests it via File > Import (Mendeley and
Pandoc read the same format). Correct entries land as article items;
partial entries carry a "verify manually" note; retracted, mismatched
and unknown entries are excluded. The evidence pack
(`--report-bundle`) includes the same file as `verified-refs.csl`.

**My claims file seems to lose rows / verdicts look weaker than expected?**
Lint it offline first: `python3 scripts/verify_pmids.py --lint-claims
claims.csv` reports unusable rows, ID shape errors, unknown columns
(typo'd headers like "titel"), missing titles and DOI prefix problems —
no network, exit 1 on errors.

**Can I verify a DOI with claimed metadata (full verdict)?**
Yes — since v3.4.0 a claims row keyed by `doi` (with `title`, optionally
`authors`/`journal`/`year`) gets the same cross-check as PMID claims:
correct / mismatch / partial against the registered metadata. A DOI row
without claims stays `unknown` (existence only).

**Why did my arXiv citation drop from correct to partial?**
Your claims row paired an `arxiv_id` with a `doi`, and the DOI does not
match the version-of-record DOI registered on that arXiv entry — a typo,
or a DOI from a different paper. The registered DOI is in `details`;
fix the claim or drop the `doi` cell.

**Can I point `--source` at a Word document or an HTML page?**
Yes (v4.8.0). `.docx` files are unzipped in-memory and the document body
is read paragraph by paragraph (table cells included); `.html`/`.htm`
pages are tag-stripped (block elements become newlines, `script`/`style`
dropped, `href` link targets kept). A damaged .docx falls back to a raw
read rather than aborting. Scanned PDFs and images are not text — export
them first.

**Why did a scanned citation that used to grade `partial` now grade
`correct` with "existence + inline title verification"?**
v4.9.0 fixed a ladder inversion: "title matched, authors never claimed"
is stronger evidence than the bare existence checks that already graded
correct — it could not honestly rank lower. When the ONLY gap is the
missing author claim (journal and year never claimed either), scanned
citations grade correct with `route: existence_title_match`. Anything
claimed-and-differing (an author, a journal, a year) still grades
partial — that is a real doubt, and `--claims-file` with the full
metadata settles it.

**A verdict mentions "corroborated by a PubMed [Title] search" or shows a
wrong-PMID signal — what does that mean?**
That citation carried only a recoverable title (no authors), so the
v4.7.0 gate refuses to accuse on it — but v4.8.0 re-checks the claimed
title phrase via a PubMed `[Title]` field search. If the SAME PMID comes
back, the verdict upgrades to **correct** (`route: inline_title_search`
— weaker evidence than a user-supplied ID, authors were never claimed;
the details carry the "corroborated" wording). If the phrase appears
verbatim in the registered title of a DIFFERENT PubMed record, the
details name that record (evidence key `wrong_pmid_signal`) while the
verdict stays unknown: the cited PMID points to another paper. Feed
`--claims-file` with title+authors for the decisive verdict.

## Worked scenarios — reviewer evidence / thesis check / PRISMA


- **"The reviewer asked how I checked my references."** — run the audit
  with `--export-audit audit.json --verify-doi`: the JSON working-paper
  contains tool identity, version, the exact (API-key-redacted) invocation,
  and the per-citation evidence chain a reviewer or editor can replay.
  Submit it alongside the manuscript.
- **"Checking the reference list of my thesis."** — copy the list into a
  plain-text file (one reference per line, or keep the `[1]` numbering) and
  run `--parse-text refs.txt`: inline PMIDs/DOIs route exactly; English
  entries resolve via PubMed title search; Chinese entries resolve via the
  OpenAlex CJK leg. Finish with
  `--format-references refs_clean.txt --citation-style gbt` for a corrected,
  uniformly formatted list.
- **"Screening a systematic review's bibliography (PRISMA)."** — verify the
  full list once, export the audit as the baseline, then re-run
  `--diff audit.json` before each resubmission: newly retracted, degraded
  and new citations are reported as deltas, so you only re-read what
  changed.


## Matching mechanics — thresholds, splice rule, suggestions

The five-state ladder rests on a dual fuzzy match between the claimed and
the registered metadata:

- **Title**: word-level Jaccard overlap ≥ 50% OR character-sequence
  similarity ≥ 90% (SequenceMatcher) — either passes. Word overlap
  tolerates reordering and abbreviation expansion; the sequence score
  catches near-identical strings.
- **Author**: at least one claimed surname hits the registered author
  list. Single initials never count as a mismatch ("Smith J" vs
  "Smith John" is not an accusation).
- **Journal**: containment match or NLM abbreviation equivalence.
- **Year**: exact match.

**DOI↔PMID splice rule** (automatic when a claims row carries `doi`): a
claimed DOI differing from the PMID's registered DOI is a splice /
fabrication signal and caps the verdict at partial — the tool reports the
inconsistency, it does not judge who is right.

**Suggestion mechanics** (`--suggest`): for every mismatch, the claimed
metadata is searched against PubMed (always NCBI, even under
`--meta-source europepmc`) and the top-3 candidates are proposed in the
report and in `suggestions` (JSON). Suggestions are candidates to check,
not verdicts.

Context parsing is heuristic (common abbreviations protected, exotic
formatting can still mis-split); `--claims-file` feeds exact metadata and
skips the heuristics entirely.

## Deployment shape (v6.4.0+)

The verifier is one entry file (`scripts/verify_pmids.py`) plus six
stdlib-only sibling modules (`scripts/pv_meta.py` … `pv_cli.py`). Copy the
whole `scripts/` directory to any Python 3.9+ machine — no pip, no venv.
`python3 scripts/verify_pmids.py --self-check` verifies a downloaded copy
offline.

## Piping input — paste-and-verify

`pbpaste | verify_pmids.py --stdin` verifies a copied reference list
without a temp file (same parser as `--parse-text`, report source reads
"stdin"); `--quick` is the pre-submission final pass (`--no-cache` +
`--verify-doi` + `--suggest`) in one flag.

## When parsing fails — format-specific fixes

| Symptom | Why | Fix |
|---|---|---|
| A .docx/.pptx yields almost no citations | Damaged zip, an image-only export, or a scanned document — the fallback reads raw bytes and finds nothing | Re-save from Word/PowerPoint as .docx/.pptx, or export to .txt/.html; scanned PDFs/pages are NOT text — run OCR first |
| A Chinese reference without any PMID/DOI grades unknown | The Latin parser under-extracts Chinese metadata | `--parse-text` engages the OpenAlex CJK title-search leg; or supply the PMID/DOI |
| A numbered list parses as one giant entry | In numbered/heading lists, continuation lines attach to the current entry; numbering markers vary (「1、」vs "[1]" vs "1."), and fewer than two markers fall back to one-entry-per-line | Normalize to `[1]`/`1.` markers, or split entries onto their own lines; bibliography exports using `## Title` headings are detected automatically |
| Titles come back fragmented (multi-line entries) | Flattened exports join lines; continuation lines attach to the current entry | Keep each reference on one line, or use `--claims-file` for exact metadata |
| A citation grades partial and you don't know which field | Partial = some metadata claimed and NOT matching | Read the `fields` table (title/author/journal/year ✓/✗/—): any ✗ is the doubt; a "—" never caused it |
| Correct verdict but you expected stricter checking | Existence-only or title-verified paths don't check authors (none were claimed) | Feed `--claims-file` with title+authors — the decisive five-state pass |
| Everything grades unknown at once | Data sources unreachable (network/proxy) | `--check-net` first; unknown is never cached, retry when reachable |

## Best practices & tuning — full playbook

- **Speed up large batches** — request an NCBI API key (see
  https://ncbiinsights.ncbi.nlm.nih.gov/api-keys/): batches of 50 IDs run
  at 0.12 s spacing instead of 0.4 s; cached re-runs take seconds.
- **Parallel DOI verification** — `--workers` (default 4, cap 8) applies to
  Crossref resolution and Europe PMC linking; arXiv stays serial by
  official etiquette (≥3 s between calls).
- **Two-phase workflow** — sweep with metadata-only verification first
  (no `--verify-doi`, no `--suggest`), then deep-verify only the flagged
  subset; each deep flag adds one API call per citation.
- **Round-trip bibliographies** — `--export-bibtex` / `--export-ris` /
  `--export-csl` write verified entries; after edits, `--bibliography
  refs.bib` / `refs.ris` re-audits the file (the PMID re-links the full
  record); the CSL JSON imports straight into Zotero.
- **Claims over context parsing** — whenever you know the expected titles,
  feed `--claims-file`: it enables the full verdict ladder and the DOI /
  arXiv pairing checks. Validate the file offline first:
  `python3 scripts/verify_pmids.py --lint-claims claims.csv` reports ID
  shape errors, missing titles, unknown columns and duplicates without any
  network access.
- **Flaky networks** — raise `--timeout`; HTTPS_PROXY/HTTP_PROXY are
  honored natively; unreachable NCBI falls back to Europe PMC
  automatically (`meta_source` shows which answered).
- **Cache policy** — results cache 30 days, negative entries 3 days;
  `--cache-days` to tune; `--no-cache` for the final pre-submission pass.
- **Scale expectations** — metadata-only throughput is API-bound
  (~1–2 min per 1000 PMIDs with an API key); DOI resolution adds one
  Crossref call per DOI. One deliberate trade-off: zero dependencies —
  copy the whole `scripts/` directory (entry file + six sibling modules,
  since v6.4.0) to any Python 3.9+ machine and it runs, no pip, no venv.
  `--self-check` verifies the copy offline.
