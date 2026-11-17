> **何时读我**：被旗标数劝退时。90% 的任务只需要下表里的一行。
> **回 INDEX**：[INDEX.md](INDEX.md)

# Flag cheat sheet — by scenario, not alphabetically

## The 90% scenarios (each is ONE command)

| You want to… | Command | Flags you actually need |
|---|---|---|
| Final pre-submission pass | `verify_pmids.py --source DRAFT --quick --output report.html` | `--quick` (= --no-cache + --verify-doi + --suggest) |
| Paste-and-verify a copied list | `pbpaste \| verify_pmids.py --stdin` | none |
| Scan a project / knowledge base | `verify_pmids.py --source DIR --output report.html` | none |
| Audit a .bib / .ris library | `verify_pmids.py --bibliography refs.bib` | none |
| Verify a raw DOI list | `verify_pmids.py --dois "10.1/x,10.2/y"` | none |
| Evidence pack for reviewers | `verify_pmids.py --parse-text refs.txt --report-bundle DIR` | none |
| Format a verified reference list | `verify_pmids.py --parse-text refs.txt --format-references out.txt --citation-style gbt` | `--citation-style` if not GB/T |
| Ready-to-edit claims skeleton | `verify_pmids.py --claims-template refs.txt,claims.csv` | none |
| Stream rows into a pipeline | `verify_pmids.py --source KB --jsonl rows.jsonl` | none |
| Environment check | `verify_pmids.py --doctor` (add `--check-net`) | none |
| Delta audit vs last month | `verify_pmids.py --source KB --diff old-audit.json` | none |

**The pattern**: default flags are already right; `--quick`, `--report-bundle`
and `--format-references` are the only "composer" flags most users ever need.

## Full flag map (grouped exactly as `--help` prints them)

### inputs — what to verify
| Flag | Effect |
|---|---|
| `--source PATH` | Scan a file/directory for PMIDs + DOIs + arXiv IDs (context parsing on) |
| `--source file.nxml`/`.jats`/`.xml` | JATS/NLM article XML (PMC format) extracts in-memory; a non-JATS `.xml` reads as plain text with a `[NOTE]` |
| `--pmids 1,2,3` | Verify specific PMIDs |
| `--dois 10.1/x` | Verify DOIs via Crossref |
| `--arxivs 2401.12345` | Verify arXiv IDs (throttled 1 call/3 s by the API) |
| `--claims JSON` / `--claims-file F` | Expected title+authors → decisive five-state verdicts |
| `--title T` / `--journal J` / `--year Y` | v7.0.0 lightweight claim for ONE `--pmids` entry — no file needed; a wrong title grades mismatch, a bare title match grades correct (add authors via `--claims-file` for the full five-state verdict) |
| `--bibliography F` | Audit a BibTeX/RIS library (PMID > DOI > arXiv routing; format sniffed from content since v6.3.0 — renamed files run as-is) |
| `--parse-text F` / `--stdin` | A plain-text reference list (inline IDs route exactly) |

### verification depth
| Flag | Effect |
|---|---|
| `--quick` | Pre-submission bundle: --no-cache + --verify-doi + --suggest |
| `--verify-doi` | Crossref cross-check of the registered DOI |
| `--suggest` | Correct-PMID hints on mismatch / retraction replacements |
| `--match-keywords` / `--threshold` | Topic-relevance scoring (auxiliary only) |
| `--no-cache` / `--cache-days N` | Cache freshness (default 30 days; final pass: --no-cache) |

### output & exports
| Flag | Effect |
|---|---|
| `--output F` | .json / .html / .md report |
| `--format FMT` | Force format regardless of extension |
| `--jsonl F` | One citation per line + final `{"_stats": ...}` — agent pipelines |
| `--export-audit / -ris / -bibtex / -csv F` | Individual artifacts |
| `--export-csl F` | Verified bibliography as CSL JSON — Zotero: File > Import (Mendeley/Pandoc read the same file) |
| `--report-bundle DIR` | All artifacts at once (the evidence pack, incl. `verified-refs.csl`) |
| `--format-references F` / `--citation-style` | GB/T 7714 (numeric + author-date) / Vancouver / APA / AMA / Harvard / Chicago, verified entries only |
| `--diff BASELINE` | Delta audit vs a previous audit.json |
| `--sort cited` | Rows ordered by citation count instead of severity (terminal/JSON/JSONL/markdown; .html keeps severity) |
| `--claims-template SRC,OUT` / `--lint-claims F` | Offline claims tooling |

### network & performance
| Flag | Effect |
|---|---|
| `--meta-source auto\|ncbi\|europepmc` | Registry choice (auto = NCBI with Europe PMC retry) |
| `--timeout S` / `--workers N` | Request timeout / DOI concurrency (default 4) |
| `--retries N` | Batch-end retry sweeps for network-failed fetches (default 1; 0 = off) — recovered count lands in `retried_recovered` |
| `--max-entries N` | Large-input guard threshold (default 2000; 0 silences) |
| `--check-net` | Four-data-source + arXiv pre-flight probe |

### institutional & diagnostics
| Flag | Effect |
|---|---|
| `--ncbi-api-key` / `--mailto` | Rate ceiling 3→10 req/s / Crossref polite pool |
| `--doctor` | Environment self-check (add --check-net for registries) |
| `--self-check` | Verify this copy offline: five core promises, one OK/FAIL line each; exit 0 = intact |
| `--version` | Print the tool version and exit |
