---
name: pubmed-verifier
license: MIT-0
version: 7.0.0
description: >-
  Reference checker for AI-fabricated citations: batch-verify PMIDs against
  PubMed and catch the hallucination existence checks miss — a REAL PMID
  pointing to a DIFFERENT paper. Five-state citation verification (correct /
  mismatch / partial / invalid / unknown), citation-context parsing, Crossref
  DOI cross-check, retraction detection (capped at partial), correct-PMID
  suggestion, arXiv ID verification, plain-text reference list parsing,
  formatted reference lists (GB/T 7714 / Vancouver / APA / AMA / Harvard /
  Chicago), OpenAlex DOI
  fallback for non-Crossref registries, Chinese-reference title search,
  CSV/JSON claims, HTML/JSON/text reports. Four data sources: NCBI, Europe PMC
  fallback, Crossref, OpenAlex. Network failures are honestly reported as
  unverified, never as "not found". Zero dependencies, runs fully local.
  Triggers: verify PMIDs, check citations, citation audit, reference check,
  citation check, batch verify references, AI hallucination detection, verify DOI,
  DOI check, citation formatting, reference formatter, GB/T 7714.
---

# PubMed Citation Verifier v7.0.0

Batch verification of PMID citations via the PubMed E-utilities API. Not just
"does this PMID exist" — **does this PMID point to the paper you claim?**
Zero dependencies, pure standard library, fully local.

## When to use this skill

Invoke it whenever citation truth matters:

- "Verify / check these PMIDs / this reference list" (before submission or release)
- Auditing citations in AI-generated text (fabricated or mismatched references)
- Spot-checking a systematic review's bibliography
- "Does PMID 12345678 really say X?" — point-of-doubt verification
- Batch QA of a knowledge base's PMID/DOI citations
- Pharmacovigilance literature verification
- Automatic invocation: trigger this skill whenever the user asks to
  "verify/check/audit" citations, PMIDs, DOIs, arXiv preprints or
  references — no flags needed for a first pass; add `--claims-file`
  when they supply the expected titles.

**Trigger priority & tool choice** — explicit "verify / check / audit
citations, references, PMIDs, DOIs" requests invoke this skill first.
cite-holmes is for deep research with machine-verified citations; when a
request mixes research and verification, run the research first, then
this tool for the final reference audit.

## Trigger words

Use this skill when the user's request matches any of: **verify PMIDs**,
**check citations**, **validate references**, **citation audit**,
**reference check**, **batch verify references**, **AI hallucination
detection**, **verify DOI**, **DOI check**, **citation formatting**,
**reference formatter**, **GB/T 7714**, 中文文献验证 / 参考文献核查 /
文献排版. A pasted reference list, a `.bib`/`.ris` file, a Word `.docx`
document, a PowerPoint `.pptx` deck, an exported `.html` page, or a
claims CSV are all direct inputs.

Three quick mappings: "帮我验证这几个 PMID 31018962、22213727" →
`--pmids`; "is this PMID the paper titled T?" one-liner →
`--pmids X --title "T"` (v7.0.0, no claims file); "检查我论文参考文献" + a pasted list → `--parse-text` (or pipe
it to `--stdin` — **a pasted list IS the input, no explicit "verify"
word needed**); "这篇撤稿了该引什么" → `--suggest` on a retracted entry.

**When to invoke — by pattern, not just by keyword:**
- MUST invoke: any request containing citation identifiers (PMID/DOI/
  arXiv ID) together with words like check/verify/audit/validate — even
  without the word "verify" ("are these PMIDs real?", "is this DOI
  right?");
- MUST invoke: a reference list is pasted or attached, whatever the
  framing ("look at my references", "any problems here?") — the list IS
  the input (`--parse-text`/`--stdin`);
- MUST NOT invoke alone: "write me a paper/lit review" (research first —
  cite-holmes; run this skill on the DRAFT's reference list at the end);
- MUST NOT invoke for: plain formatting of UNVERIFIED citations without
  verification intent — formatting stands on verified records
  (`--format-references` verifies first by design);
- Mixed intent ("check the citations in my draft", "帮我润色并核对文献"):
  when verification is named, this skill wins for the citation list
  (run it on the draft/list first); the other task proceeds separately.
  When only writing/polishing is named with no list, do NOT invoke.

**Combination runs** (flags stack; each does one job):

| Scenario | Command shape |
|---|---|
| Pre-submission final pass | `--source DRAFT --quick --output report.html` |
| Paste-and-verify from clipboard | `pbpaste \| ... --stdin --suggest` |
| Quick one-liner check | `--pmids 12345678 --title "Expected title"` (no claims file needed) |
| Knowledge-base audit + evidence pack | `--source KB --report-bundle DIR` |
| Bibliography round-trip | `--bibliography refs.bib --export-bibtex out.bib` |
| Bibliography into Zotero | `--source KB --export-csl library.json` (Zotero: File > Import) |
| Delta audit vs last month | `--source KB --diff old-audit.json` |
| CJK-only reference list | `--parse-text refs-cn.txt` (OpenAlex CJK leg) |

**When `--claims-file` is required:** a plain scan verifies existence plus
whatever metadata the citation context carries — if a verdict will be
acted on (mismatch/partial before submission), feed the expected
title+authors via `--claims-file` for the decisive five-state verdict.
**Tool boundary:** cite-holmes covers deep research with machine-verified
citations; this skill is the verification/formatting pass — when a request
mixes both, research first, then audit the final reference list here.

## Use from Python

One stdlib module, nothing to install:

```python
import verify_pmids as vp   # sys.path pointing at scripts/
info = vp.fetch_summaries(["31018962"], batch_size=1)["31018962"]
print(vp.cross_check_citation({"claimed_title": info["title"]},
                              info)["verdict"])
```

Full function reference and runnable examples: `references/python_api.md`.

## Know before you run

Six limits cover 95% of surprises — each has a one-flag workaround:

| Limit | Workaround |
|---|---|
| Citation-context parsing is heuristic (exotic formatting can mis-split) | `--claims-file` for exact metadata |
| Chinese references without an ID: an ID-less Chinese line of ~12+ characters routes to OpenAlex title search; the verdict needs the registered title verbatim in the entry (a given year must match; journal is not required); short fragments and prose paragraphs stay unknown | `--parse-text` (OpenAlex CJK leg) or supply an ID |
| Network failures stay `unknown` — never silently "not found" | `--check-net` first, retry when reachable |
| Retraction/DOI status is as of cache time (30 days) | `--no-cache` for the final pre-submission pass |
| Office/HTML input extracts text only — scanned PDFs and images carry no extractable text | Export to text/HTML first, or feed IDs via `--claims-file` |
| Very large batches take time and may hit rate limits | See the batching math in `references/operations.md`; verify in slices |

Everything else below expands on these.

**Documentation map** — what lives where, so nothing needs hunting:

| If you want... | Go to |
|---|---|
| The full version history | `references/CHANGELOG.md` (main doc keeps the recent highlights) |
| Every FAQ, scenario walkthrough and tuning knob | `references/usage_guide.md` |
| A scenario→command cheat sheet for every flag | `references/flags.md` |
| Bulk batching, proxies, speed, CI gating and the stderr marker contract | `references/operations.md` |
| An `[ERROR]`/`[WARN]` on screen, or results that look wrong | `references/troubleshooting.md` (one error, one row) |
| The Python API reference / runnable examples | `references/python_api.md` / `references/api_examples.md` |
| Which file to open for which task | `references/INDEX.md` |

## The five-state verdict

| Verdict | Meaning |
|---------|---------|
| ✅ Correct | PMID exists AND matches the claimed paper |
| ⚠️ Mismatch | PMID exists but points to a **different** paper (the most common AI hallucination!) |
| 🔶 Partial | Some metadata matches (e.g. author+journal but title differs) |
| ❌ Invalid | PMID does not exist in PubMed |
| ❓ Unknown | Not enough claimed metadata to cross-check — or both data sources unreachable (never misreported as invalid) |

**Why existence checks are not enough:** a large share of fabricated
citations use REAL PMIDs that point to a different paper from the same
year/journal/field — in one of our own audits, 4 of 5 "valid" PMIDs were
wrong this way. A binary exists/not-exists check misses them all.

## Quick start

The ten commands below cover most runs; every flag has a one-row entry in
[references/flags.md](references/flags.md) (scenario → one command, grouped
by task) and the worked scenarios live in
[references/usage_guide.md](references/usage_guide.md).

```bash
# Pre-submission final pass in ONE command: fresh registries + Crossref
# DOI cross-check + correct-PMID suggestions, no flags to remember
python3 scripts/verify_pmids.py --source /path/to/draft --quick --output report.html

# Paste-and-verify: a copied reference list straight from the clipboard
pbpaste | python3 scripts/verify_pmids.py --stdin --suggest

# Verify specific PMIDs, or a whole project directory (Word .docx, .pptx
# decks, exported .html and JATS .nxml/.xml are read directly)
python3 scripts/verify_pmids.py --pmids 31018962,22213727
python3 scripts/verify_pmids.py --source /path/to/project --output report.html

# Precise five-state verdicts: feed the expected metadata (CSV/JSON)
python3 scripts/verify_pmids.py --claims-file claims.csv --suggest --output report.html

# Verify a pasted reference list, then format the verified entries
python3 scripts/verify_pmids.py --parse-text references.txt --no-cache
python3 scripts/verify_pmids.py --parse-text references.txt --format-references refs_gbt.txt --citation-style gbt

# Submission evidence pack: one command, every artifact
python3 scripts/verify_pmids.py --parse-text references.txt --report-bundle evidence_pack

# Health checks: environment self-check + four-data-source + arXiv network pre-flight
# (probes each source direct AND via your HTTPS_PROXY)
python3 scripts/verify_pmids.py --doctor
python3 scripts/verify_pmids.py --check-net
```

## What the output looks like

Terminal text report (verdict line, then per-citation evidence):

```
Readiness: NOT SUBMISSION-READY — 1 invalid, 1 mismatched
Results: 1/3 correct, 1 mismatch, 1 invalid, 0 partial, 0 unknown
============================================================

✅ PMID 31018962 (claims) [correct]
   Actual: Classification criteria for autoinflammatory recurrent fevers
   Claimed: Classification criteria for autoinflammatory recurrent fevers
   Evidence: title ✓ · author ✓ · journal ✓ · year ✓

⚠️ PMID 34078778 (claims) [mismatch]
   Actual: Effect of CAD/CAM materials on the marginal fit of crowds
   Claimed: JIA pathogenesis and treatment
   → Suggest: PMID 34425842 - Juvenile idiopathic arthritis: from aetio...
   Evidence: title ✗ · author ✗ · journal ✗ · year —

❌ PMID 99999999 (cli) [invalid]
   Error: PMID not found in API response
```

`--output report.html` renders a self-contained dashboard (inline CSS,
no external assets): readiness banner, a filterable verdict table
(✅/⚠️/🔶/❌/❓ tabs with per-field ✓✗— evidence columns, retraction and
DOI-splice flags highlighted on top), a delta panel when `--diff` is
given, the finding ledger, and a reproducibility footer (redacted
command + version + data sources). Open it in any browser — it is also
what `--report-bundle` packs for reviewers.

`--output report.json` carries the same verdicts plus the full evidence
chain per citation (`evidence.title_match / author_match / journal_match /
year_match`, `fields` tri-state, `meta_source` naming which registry
answered, `resolved_by` when the title-search/OpenAlex legs matched) and a
`stats` block with the submission-readiness verdict. `--format-references`
writes the ready-to-paste citation list (see the v4.0.0 entry in references/CHANGELOG.md).

## Quick FAQ

Plain questions with plain answers; the deep versions live in
[references/usage_guide.md](references/usage_guide.md). The ten mistake
patterns with their one-line fixes are the speed-index table at the top
of the Anti-patterns section below — one fact, one home.

**❓ unknown vs ❌ invalid — what's the difference?**
`unknown` (exit 2) = "the source could not be reached, nothing was judged"
— re-run when the network is up; `invalid` (exit 1) = "checked and the
record does not exist". Network failures are never reported as
not-found and never cached.

**Why is my citation capped at ⚠ partial?**
The five-state ladder caps the verdict when a claimed field could not be
checked — most often a claim without `title` (#2 above), or a
retracted paper (partial + human-review note, by design).

**A network blip made half my batch unknown — re-run everything?**
No. Unknowns are never cached, so a plain re-run re-fetches only those;
and since v5.7.0 the run itself retries: `--retries N` (default 1)
re-runs just the network-failed fetches after a 2 s cool-off and reports
what it recovered (`retried_recovered` in the stats).

**When must I use `--claims-file` instead of scanning?**
Context parsing is heuristic (v3.3.0 guards common abbreviations, exotic formatting can still mis-split).
For precise verification — or DOIs in claims (splice detection needs `doi`)
— feed structured JSON/CSV claims.

**My citation text is in Chinese — the scan parses little?**
GB/T 7714-style references (……标题[J]. 刊名, 年… PMID: xxx) parse since
v3.9.0 — title/journal comparisons against Latin registries are skipped
cross-language, so verdicts rest on year/DOI evidence. Free Chinese prose
without a PMID marker still yields little — feed `--claims-file` for full
verdicts regardless of language.

**Can I get the verified entries into Zotero?**
`--export-csl library.json` writes the verified bibliography as CSL JSON
— Zotero: File > Import (Mendeley and Pandoc read the same file).
Correct entries import as article items; partial ones carry a
verify-manually note.

**Slow or unstable network (China)?**
Standard `HTTPS_PROXY`/`HTTP_PROXY` env vars are honored natively; raise
`--timeout`; `--meta-source europepmc` routes via Europe PMC when NCBI is
unreachable (per-entry `meta_source` shows which was used); cached results
are reused for 30 days. `--check-net` probes every source on both routes
(direct + proxy) and names the fallback for each.

More FAQs, the three worked scenarios and the complete tuning playbook live in [references/usage_guide.md](references/usage_guide.md).

## Anti-patterns — things done WRONG

**Top 10 things NOT to do** — the speed index; each numbered entry below expands the why. (Usage mistakes, not questions — the question-form answers are in Quick FAQ above.)

| # | Don't | Do instead |
|---|-------|------------|
| 1 | Treat `--pmids` existence output as "verified" | Feed `--claims-file` with titles for real verification |
| 2 | Submit claims without `title` | Always include titles — the verdict caps at partial without one |
| 3 | Trust cached verdicts on publication day | Final check with `--no-cache` |
| 4 | Read "not found" as "fabricated" for auto-extracted DOIs | Check doi.org / arxiv.org by hand first |
| 5 | Treat the leading `'` in CSV cells as corruption | It is the formula-injection guard — strip after import |
| 6 | Read the READY line as a quality score | It means "no problems among the checks that ran" |
| 7 | Pass `--source` together with `--pmids` | `--source` is ignored entirely when `--pmids` is given |
| 8 | Deep-verify (`--verify-doi` / `--suggest`) a thousand-entry sweep | Sweep first, deep-verify the flagged subset |
| 9 | Expect author matching across CJK↔Latin names | They are skipped honestly (`author_check: skipped`) |
| 10 | Ship a reference list without the audit trail | `--export-audit` writes a replayable working paper |

Each entry: the mistake → why it fails → the right way.

1. **Treating `--pmids` output as "fully verified"** — existence-only.
   → Wrong: "all 5 PMIDs exist, so the citations are correct."
   → Right: existence-checked only; feed `--claims-file` with titles for
   real verification (the READY line says so explicitly).
2. **Claims without `title`** — author/journal/year alone can never reach
   `correct`; the report caps at `partial`. → Always include titles.
3. **Trusting a cached verdict right after publication day** — a brand-new
   PMID may have been cached as not-found by an earlier run, and retraction
   status is as of cache time. → Final pre-submission check: `--no-cache`.
4. **Assuming "not found" always means fabricated** — a Crossref 404 is
   re-checked at OpenAlex (DataCite/Zenodo/Chinese-registry DOIs live
   there), so "unknown in both registries" is now the bar; auto-extracted
   DOIs that 404 in both stay *suspects*. arXiv IDs removed by moderators
   also return empty. → Check doi.org / arxiv.org by hand before accusing.
5. **Copying the leading `'` from CSV cells** — that apostrophe is the
   formula-injection guard, not data corruption. → Strip it after import.
6. **Reading the READY line as a quality score** — it only means "no
   problems found among the checks that ran", not "this paper is good".

## Boundaries — declared limits

The capability×limit pairs — what each promise covers, where it stops, and
the one-flag workaround:

| Capability | What it does | Where it stops | Workaround |
|---|---|---|---|
| Context parsing | Splits reference text into claimed metadata; common abbreviations (U.S., e.g., vs.) protected | Exotic formatting can still mis-split; an ID-less CJK line verifies via OpenAlex title search only when the registered title appears verbatim in the entry — short fragments and prose paragraphs stay unknown | `--claims-file` for exact metadata; `--parse-text` adds the OpenAlex CJK leg |
| Five-state verdicts | correct / mismatch / partial / invalid / unknown with per-field evidence | Heuristic — a verdict is evidence-weighted, never absolute proof | Audit trail (`--export-audit`) keeps the chain replayable |
| Retraction detection | Registry pubtype + Crossref `updated-by`, capped at partial | Status is as of cache time (30 days) | `--no-cache` for the final pass |
| DOI verification | Crossref first, OpenAlex fallback for non-Crossref registries | DOIs absent from BOTH registries stay suspect/invalid by the 404 rule | Cross-check at doi.org before accusing |
| Title-search legs (Latin + CJK) | Markerless entries resolved by PubMed/OpenAlex title search, honestly labeled | Never a mismatch source; no hit = unknown | Supply a PMID/DOI for a decisive verdict |
| Second-opinion leg (v4.8.0) | A gated title-only claim is corroborated via PubMed title search (correct, labeled) or flagged as a wrong-PMID signal | Confirms or reports only — never manufactures a mismatch; CJK titles skip (OpenAlex CJK leg owns those) | `--claims-file` for the decisive verdict |
| Word/HTML/PowerPoint/JATS input (v4.8.0–v6.0.0) | `.docx` paragraphs/tables, `.pptx` slides+speaker notes, `.html` text and JATS/NLM `.xml` articles are extracted in-memory; `href` targets kept, script/style dropped | A damaged structured file falls back to a raw read **with a visible `[NOTE]`** (results from it may be incomplete); scanned PDFs/images are NOT text | Export to text/HTML first for PDFs |
| Verdict-ladder monotonicity (v4.9.0) | A scanned citation whose ONLY gap is the missing author claim (title matched, journal/year never claimed) grades correct with `route: existence_title_match` — stronger evidence than a bare existence check can never grade lower | Any claimed-but-differing author/journal/year keeps partial; explicit `--claims-file`/CLI inputs always get the full verdict | `--claims-file` with authors for the complete five-state pass |
| Retraction reasons (v5.3.0) | A retracted citation carries `retraction_reason` — the notice abstract when the registry has one, else the notice title — plus `retraction_reason_doi` for the source statement | Many notices are just "Retraction Note: <original title>"; the original title alone NEVER masquerades as the reason — the notice is cited instead | Read `--export-audit` for the full chain |
| Input scale & concurrency (v5.1.0/v5.2.0) | Any input size; the `--max-entries` guard (default 2000) counts the de-duplicated workload and warns with a split recommendation; DOI verification runs 4 workers; PMID batches go 50/call (0.4 s spacing, 0.12 s with an API key) | arXiv is throttled to 1 call/3 s BY THE API (1,000 arXiv IDs ≈ 50+ minutes no matter what); citation counts (`cited_by_count`) only exist on the Europe PMC/OpenAlex paths — the NCBI path reports none | `--max-entries N` raises the threshold, `0` silences it; split very large scans by section |
| Explicit precedence (v5.1.0) | `--pmids` outranks `--source` when both are given | The ignored input is announced on stderr, never silently dropped | Give only the input you mean |
| Formatted reference lists | GB/T (numeric + author-date), Vancouver, APA, AMA, Harvard, Chicago (author-date) — verified entries only | Registry-truncated author lists close with et-al, not invented names | Verify first, then format (`--format-references`) |
| Network honesty | Failures are unknown + retry hints, never "not found"; nothing cached on failure | Cannot verify anything while registries are unreachable | `--check-net` first |

## Claims reference format

`--claims-file` accepts JSON (an array of objects) or CSV. Recognized
columns: `pmid`, `title`, `authors` (semicolon/pipe-separated),
`journal`, `year`, `doi`, `arxiv_id`. A row needs one of `pmid`,
`arxiv_id` or `doi`; a missing `title` caps the verdict at partial.

```csv
pmid,title,authors,journal,year,doi,arxiv_id
31018962,Candidate criteria for diagnosis of familial...,Gattorno,Ann Rheum Dis,2019,10.1136/annrheumdis-2019-215048,
,Attention Is All You Need,Vaswani,NeurIPS,2017,,1706.03762
,City size and the spreading of COVID-19 in Brazil,Silva Junior;Other,PLOS ONE,2020,10.1371/journal.pone.0239699,
```

Validate any file offline first: `--lint-claims file.csv` reports
unusable rows, ID shape errors, unknown columns, duplicates and missing
titles (no network). Lint wins when combined with verification flags —
only the lint runs.


## Using it from mainland China — the one page

Everything network-related in one place (each item also lives where it is used):

- **Pre-flight**: `--check-net` probes all four registries + arXiv **twice
  each — direct and via your `HTTPS_PROXY`** (5 s per route) — and prints
  per-source reachability, which verification paths it serves, and the
  in-tool fallback; a source blocked on the direct route but fine through
  the proxy reports as usable.
- **Registry choice**: default `--meta-source auto` already retries a failed NCBI batch against Europe PMC (no key, generally reachable); `--meta-source europepmc` forces it.
- **Proxy**: standard `HTTPS_PROXY`/`HTTP_PROXY` env vars are honored on every request; direct-mode automation should `unset` them (a dead proxy env otherwise masks as unreachable registries).
- **Package mirror**: ModelScope carries the skill package (`modelscope.cn/skills/Docsor/pubmed-verifier`) — but verification itself still calls the academic registries at runtime; the mirror only removes the install friction.
- **Honest failure**: whatever the network does, failures grade `unknown` (exit 2), never "not found", and are never cached.

## Best practices & tuning

Full playbook: [references/usage_guide.md](references/usage_guide.md) (caching, batching, proxies, CI usage).

## Recent releases (full history in references/CHANGELOG.md)

- **v7.0.0** — `--self-check` gains a live retraction-source health probe
  (six promises; unreachable registries SKIP honestly); `--title` gives
  a one-liner claim for a single PMID (wrong title → mismatch, no
  claims file needed); `python3 tests/run_tests.py` is the one CI
  command.
- **v6.9.0** — two more verified-list styles: `--citation-style harvard` and
  `chicago` render the registry-verified bibliography as author–date
  entries (7 styles total, GB/T author-date / Harvard / Chicago sorted by
  first author).
- **v6.8.0** — the Top-10 NOT-to-do table has one home: the speed index
  atop the Anti-patterns section (Quick FAQ routes there instead of
  repeating it, EN+ZH); README features grouped, quick start leaner.
- **v6.7.0** — the Files table reads the package: every backticked path
  must exist, every package-carriable sample must appear by its full
  name (short forms like `.json` or `+_ZH` hid real files from the
  reader), native-extension `.bib`/`.ris` samples are explicitly marked
  "GitHub repo and zip only" — two test locks enforce both directions;
  the Use-cases section (a duplicate of When-to-use) is gone.
- **v6.6.0** — one count, one home per fact: module counts unified
  everywhere, locked against the directory; the main doc keeps summaries
  under a 500-line ceiling.

## Safety & behavior statement

- Single-run CLI: scan → verify → write report → exit. No daemon, no
  background task, zero runtime downloads/installs (pure standard
  library, zero dependencies).
- Network access is limited to these official academic registries, all
  HTTPS: `eutils.ncbi.nlm.nih.gov`, `www.ebi.ac.uk` (Europe PMC),
  `api.crossref.org`, `api.openalex.org`, `export.arxiv.org` — no other
  hosts; no telemetry, no stats, no data collection — outbound payloads
  are only the PMID/DOI/titles you asked to verify.
- Your files and reports stay local. Writes go only to the report paths
  you specify and the SQLite cache under `~/.cache/pubmed-verifier/`
  (disable with `--no-cache`).
- The optional `NCBI_API_KEY` / `PUBMED_VERIFIER_MAILTO` env vars
  authenticate/sign YOUR API requests only — they go nowhere else.
- No OS integration: no subprocesses, no services, no permission
  changes, no scheduled tasks.

## How it works

Extract claims from the input (context parsing, heuristic) → fetch the
registry record (batched, cached, Europe PMC fallback) → cross-check
claimed vs registered metadata (the five-state ladder) → optional
Crossref DOI verification with retraction detection (`--verify-doi`) and
correct-PMID suggestions (`--suggest`). The matching thresholds, the
DOI↔PMID splice rule and the suggestion mechanics are documented in
[references/usage_guide.md](references/usage_guide.md); the audit trail
(`--export-audit`) makes every step replayable.

| Report | Flag | Use |
|--------|------|-----|
| HTML | `--output report.html` | Human review: claimed vs actual side by side |
| JSON | `--output report.json` | Programmatic processing (includes `meta_source` per entry) |
| Text | default | Quick terminal look |

## Performance

Metadata-only verification runs in seconds for typical audits; cached
re-runs take ~5 s. Deep-verify flags add per-citation API calls — the
batching math and the speed checklist live in
[references/operations.md](references/operations.md).

## When to use which tool

- **pubmed-verifier (this skill)** — fast, batch, targeted: I have a list of
  PMIDs/DOIs and need to know if they are real and correctly cited.
- **cite-holmes** — deep research: interrogate every citation of a whole
  document across multiple databases, with graded confidence reports.

They share the same five-state philosophy and are safe to use together.

## Related tools

Each tool solves one step of reference work; use whichever fits the task.

- **cn-med-oa** — free Chinese medical literature full-text download & metadata
- **cite-holmes** — deep research with machine-verified citations
- **paper-polisher-pro** — academic polishing, terminology & journal precheck
- **academic-figures** — publication-ready scientific figures in one command
- **doc-holmes** — layout-preserving PDF translation (in testing)

Typical order: get papers (cn-med-oa), verify citations (this tool or
cite-holmes), polish (paper-polisher-pro), make figures (academic-figures),
translate PDFs (doc-holmes) — pick whichever step you need.

## Files

| File | Purpose |
|------|---------|
| `scripts/verify_pmids.py` | Entry file + orchestration (v7.0.0, stdlib-only; six `pv_*.py` sibling modules beside it) |
| `references/usage_guide.md` | full FAQ, worked scenarios, tuning playbook, matching mechanics |
| `references/troubleshooting.md` / `troubleshooting_ZH.md` | Troubleshooting index — one error, one row (literal text → cause → fix) |
| `references/flags.md` | Flag cheat sheet — scenario → one command, every flag grouped |
| `references/operations.md` | Operations playbook — batching math, proxy scenarios, speed checklist, error contract, CI gate |
| `references/INDEX.md` | Task → document routing table |
| `references/python_api.md` | Calling the verifier from Python (stable surfaces + examples) |
| `references/api_examples.md` | PubMed / Europe PMC / Crossref / arXiv API notes |
| `references/CHANGELOG.md` | Full version history |
| `examples/README.txt` | What each sample is for, with one command each |
| `examples/claims.sample.csv` / `claims.sample.json` | Reference formats for `--claims-file` (PMID / DOI-only / arXiv row types) |
| `examples/refs.sample.txt` / `refs_list.sample.txt` | Sample inputs for `--parse-text` (inline-ID routing + a title-only entry) |
| `examples/refs.sample.bib.txt` / `refs.sample.ris.txt` | Sample bibliographies for `--bibliography` (format sniffed from content) |
| `examples/refs.sample.bib` / `refs.sample.ris` | Same samples under their native extensions (GitHub repo and zip only) |
| `tests/` | Offline matrix + real-network acceptance (repo only, not in the package) |

## License

MIT-0 — free to use, modify and redistribute, no attribution required.
