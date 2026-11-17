# Quantinuum docs corpus (multi-site crawler + API-drift audit)

Nine Quantinuum Sphinx sites are crawled into the repo so code is written
against the *current* docs instead of recollection: Nexus, Guppy, Selene, tket
(user guide **and** API docs), lambeq, Quantum Origin, InQuanto, and the Systems
hardware user guide.

```bash
python -m quantum.docs_crawler.fetch                 # all sites, resumable
python -m quantum.docs_crawler.fetch --site guppy selene --force
python -m quantum.docs_crawler.extract --site guppy  # <slug>/snippets.jsonl + api_surface.json
python -m quantum.docs_crawler.audit                 # <slug>/audit_report.md + AUDIT.md roll-up
```

Sites live in `quantum/docs_crawler/sites.py`: base URL, whether raw sources
exist, the import roots to mine, and which of *our* modules get audited against
them. Corpus at `corpus/<slug>/<docname>.md`, index at `corpus/index-<slug>.json`
(Nexus keeps the legacy `corpus/index.json`).

## Two acquisition paths — most sites have no `_sources`

Every site publishes `searchindex.js` (there is no `sitemap.xml` anywhere; it
404s). Only three serve the raw markdown/notebook twin under
`/_sources/<filename>.txt`:

| Site | Pages | Snippets | Raw sources |
| --- | ---: | ---: | --- |
| nexus | 89 | 272 | yes |
| guppy | 257 | 377 | **no — HTML** |
| selene | 106 | 39 | **no — HTML** |
| tket-user-guide | 28 | 750 | yes |
| tket-api | 31 | 44 | yes |
| lambeq | 82 | 529 | yes (16 notebooks) |
| origin | 52 | 5 | **no — HTML** |
| inquanto | 126 | 1174 | **no — HTML** |
| systems | 59 | 609 | **no — HTML** |

830 pages, 3 799 snippets, zero fetch failures, ~6 min at the 0.4 s delay.

For the HTML sites the fallback takes the article container
(`div.bd-article-container` / `article.bd-article` / `[role=main]`), decomposes
nav/sidebar/footer/headerlink, and re-fences each `div.highlight pre` with the
language read off the parent `highlight-<lang>` class before flattening to text.
Do this *before* stripping tags — a plain tag-strip loses every code block, which
is the only part of a docs page worth auditing.

`tket` has **no single Sphinx root**: `tket/user-guide/` and `tket/api-docs/` are
separate builds with separate search indexes, registered as two sites. A crawl of
`https://docs.quantinuum.com/tket/searchindex.js` 404s.

## What the multi-site audit found

- **guppy** — zero drift; everything we call is documented. Unadopted and
  interesting: `guppy.load_pytket` (10x — pytket circuit straight into a kernel),
  `guppy.nat_var`/`type_var`/`type_alias` (generic-width kernels, which would
  collapse our per-n kernel factories), `guppy.struct`, `guppy.comptime`,
  `guppy.overload`.
- **selene** — the docs' own snippets are thin (39 across 106 pages; most pages
  are autodoc stubs). Drift: `selene_sim.build` used in `emulate.py` never
  appears in a snippet. Their example imports point at
  `selene_sim.result_handling.parse_shot`, `selene_sim.event_hooks`, and
  `hugr.qsystem.result` — the structured-result path we hand-roll.
- **tket-user-guide** — richest snippet density in the whole corpus (750 from 28
  pages). Unadopted: `Backend.get_operator_expectation_value`,
  `get_pauli_expectation_value`, `pytket.utils.expectation_from_counts/shots`,
  `partition.measurement_reduction`, `compare_unitaries/statevectors` — i.e. the
  expectation-value and verification machinery we reimplement by hand.
- **systems** — the hardware guide is a *combined* Guppy+pytket+qnexus corpus
  (`guppylang.std.qsystem` appears 12x); it is the canonical source for access,
  queueing and HQC costing, and it documents `QuantinuumConfig`,
  `projects.get_or_create`, `jobs.wait_for`, `jobs.results`.
- **inquanto** — 1 174 snippets, dominated by `inquanto.ansatzes`,
  `protocols`, `states`, `express`, `extensions.pyscf`. `express` is the
  ready-made molecular-system shortcut for anything H2/ethylene-shaped.
- **lambeq** — 529 snippets, `lambeq.backend.{grammar,quantum,tensor}` plus
  torch; entirely disjoint from our current stack (no modules audited yet).
- **origin** — only 5 snippets across 52 pages: Quantum Origin docs are CLI and
  concept prose, not a Python API surface. Do not expect an importable library.

## The Nexus lane

## Refresh the corpus

```bash
python -m quantum.docs_crawler.fetch      # resumable; --force to refetch, --section trainings, --limit N
python -m quantum.docs_crawler.extract    # snippets.jsonl + api_surface.json
python -m quantum.docs_crawler.audit      # audit_report.md
```

Layout (`quantum/docs_crawler/`):

| Path | Contents |
| --- | --- |
| `corpus/nexus/<docname>.md` | 89 pages of raw Sphinx source; `.ipynb` sources flattened to markdown + fenced python |
| `corpus/index.json` | per page: title, source URL, raw URL, sha256, bytes, fetched_at |
| `snippets.jsonl` | 278 code blocks tagged with their docname |
| `api_surface.json` | imports + `qnexus.*` call counts as the docs actually use them |
| `audit_report.md` | drift risk vs our code, documented-but-unused capabilities |

## Why it crawls cleanly

- Sphinx/Furo site: every page has a raw twin at `/_sources/<filename>.txt`. No
  HTML parsing, no JS rendering.
- `searchindex.js` enumerates all 89 docnames + source filenames — there is **no
  `sitemap.xml`** (404). Parse it as `Search.setIndex( <json> )`.
- 16 of the sources are `.ipynb` JSON. Flatten them at fetch time; otherwise a
  naive fence regex finds zero code in the most useful training pages
  (33 snippets vs 278 after flattening).

## What the first audit found

Undocumented-but-used: `qnexus.HeliosConfig`, `auth.login`,
`auth.login_with_token`, `auth.is_logged_in`, `devices.get_all`,
`jobs.HybridStrategy`, `jobs.cost`, `jobs.get`, `users.get_self`. These are the
exact calls our cost guard and resume path depend on, and none of them appear in
a single doc snippet — they are the drift surface.

They are now fenced behind **`quantum/qnexus_compat.py`**, the single import
point for the client:

```python
from quantum import qnexus_compat as compat

compat.PINNED_QNEXUS            # "0.48.2" — lockstep with quantum/requirements.txt
qnx = compat.import_qnexus()    # lazy; warns (does not fail) on a version mismatch
compat.assert_no_drift(qnx)     # fatal BEFORE submission if any symbol moved
compat.drift_report(qnx)        # {symbol: present}, never raises — safe in a preflight

compat.jobs_cost(qnx)(job)      # named accessor per drift symbol; a missing one
                                # raises QnexusDriftError naming it + both versions
```

Rules that keep it maintainable: only the drift surface goes through the layer
(documented calls stay on plain `qnx.`), the offline fake in
`tests/fake_qnexus.py` carries a `__version__` matching the pin so every
accessor is exercised with zero submissions, and a new undocumented call means
a new entry in `DRIFT_SYMBOLS` plus a case in `tests/test_qnexus_compat.py`.

### Keeping the list honest: `drift_watch`

A hand-maintained drift list rots in both directions, so the reconciliation is
automated — `quantum/docs_crawler/drift_watch.py` diffs three derived sets
(crawled `api_surface.json`, our real call sites, `DRIFT_SYMBOLS`) and grades
every symbol:

| Verdict | Meaning | Action |
|---|---|---|
| `stable` | declared, still undocumented, still used | none |
| `newly-documented` | the docs now cover it | may leave the compat layer |
| `undeclared` | used + undocumented + unguarded | **add it before the next paid run** |
| `obsolete` | declared, nothing calls it | remove entry + accessor |

```bash
python -m quantum.docs_crawler.drift_watch          # writes drift_state.json
python -m quantum.docs_crawler.drift_watch --check  # exit 1 when out of sync
```

`audit.py` renders the same state into `nexus/audit_report.md` and `AUDIT.md`,
so the ordinary `fetch → extract → audit` cycle refreshes it, and
`tests/test_drift_watch.py` fails the day the declaration goes stale.

Two things the diff must get right or it lies:

- **Count compat-mediated use.** Once a symbol is routed through the layer, no
  file writes `qnx.jobs.cost(` any more; a scan for direct calls alone grades
  the entire guarded surface `obsolete` and invites deleting exactly the code
  that protects the cost path. `ACCESSORS` maps symbol → accessor name so the
  indirection still counts as use.
- **Tokenize before scanning.** A plain regex over source counts
  `qnexus.auth.login()` written inside a docstring and invents an `undeclared`
  symbol nobody calls. Strip comments and string literals first.


### Catching upstream change: `api_diff` (all nine sites)

`drift_watch` only guards the Nexus drift list. The wider risk is a Guppy,
Selene, tket or InQuanto symbol moving under us and surfacing as a mid-sweep
crash on a billed run. `quantum/docs_crawler/api_diff.py` snapshots each site's
**imports + calls + page set** and compares the new crawl against a committed
`<slug>/api_baseline.json`:

| Verdict | Meaning | Action |
|---|---|---|
| `added` | new documented surface | opportunity — read it before the next gate |
| `removed` | gone upstream, we never used it | none |
| `moved` | a removal pairs 1:1 with an addition | follow the rename |
| `breaking` | gone upstream **and** our code imports/calls it | **fix before the next paid run** |

```bash
python -m quantum.docs_crawler.api_diff --check              # exit 1 on breaking
python -m quantum.docs_crawler.api_diff --check --introspect # also probe installed pkgs
python -m quantum.docs_crawler.api_diff --site guppy --accept  # adopt, then commit
```

Four things this had to get right:

- **Key on imports as well as calls.** The lib-rooted call surface in the docs
  is far thinner than the import surface (Guppy: 13 calls vs 45 imports; Selene
  3 vs 12), and this repo touches Guppy almost entirely through
  `from guppylang.std.quantum import h`. Calls alone would grade a real removal
  as unused.
- **Grade by *our* dependency, not by doc-hit count.** `removed` vs `breaking`
  is decided by `our_usage()`, which unions the call-chain scan with an import
  scan across `sites.py`'s `our_files`/`our_globs`. A gap in those globs
  silently downgrades a breaking change — widen them when a new module starts
  importing a library.
- **Baselines move only on a human `--accept`.** A snapshot-only audit can
  never say "this changed"; the committed baseline is what makes the diff a
  gate instead of a description.
- **Unknown ≠ broken.** A missing baseline, an uncrawled site, or a package
  absent from `.pydeps` after a sandbox reset all render as "run `--accept`" or
  stay silent — never as `breaking`.

`--introspect` resolves used symbols against the *installed* packages with
`importlib`, which catches removals the docs haven't caught up with yet.
`audit.py` renders the rows into every per-site report and a
"Breaking API changes since the accepted baseline" section of `AUDIT.md`;
`tests/test_api_diff.py` (39 offline tests) covers the graders, the
accept round-trip, and the CLI exit codes.

### Running the docs: `snippet_run` (Gate 0.9.2)

`api_diff` proves a symbol still *exists*; `snippet_run` proves the documented
example still *runs*. It groups a page's snippets in document order and
executes them as one real `.py` file in a locked-down subprocess:

```bash
python -m quantum.docs_crawler.snippet_run --jobs 8          # execute + write results
python -m quantum.docs_crawler.snippet_run --check --no-run  # CI gate, exit 1 on regression
python -m quantum.docs_crawler.snippet_run --site selene --accept
```

Design decisions that had to be made this way:

- **A real file on disk, never `exec(code_string)`.** Guppy compiles a kernel by
  reading its own source back with `inspect.getsource`, so every `@guppy`
  example raised `OSError: source code not available` under a string-exec
  harness — 34 fake failures in Guppy alone. The page is written to
  `snippet_page.py` with a `_snip_mark(i)` line between blocks; the marks give
  per-block attribution without indenting the doc code (indenting also breaks
  what Guppy reads back).
- **Page-level namespace.** Selene's `build(hugr)` block depends on the
  `hugr = main.compile()` block above it. Isolated blocks would fail as
  fragments. A failure stops the page and the rest grade `skipped`.
- **Loopback stays open.** Selene drives its own emulator over a local socket;
  a blanket socket ban failed every emulation example for a sandbox reason.
  The injected `sitecustomize` blocks non-local `connect`/`getaddrinfo` only.
- **Prefilter before executing, not after.** Anything mentioning `qnexus`,
  `start_execute_job`, `QuantinuumBackend`, or an API key is `blocked`
  unexecuted — a docs pass must never touch the account. A committed test
  re-derives this from the corpus for every executed block.
- **Verdicts separate their causes.** `fail` is reserved for a real breakage;
  `NameError`/`ModuleNotFoundError`/`FileNotFoundError` grade `blocked`
  (fragment or optional dep), memory-cap kills grade `blocked`, and a missing
  library grades `skipped`. Only `pass -> fail` is a regression;
  `pass -> skipped` is our environment, not their API.
- **Reasons must be stable.** The temp page path is normalised to `<page>`, or
  every run diffs against its own baseline. Guppy prints its real diagnostic to
  *stdout* and ends stderr with the useless "Guppy compilation failed due to 1
  previous error", so the harness prefers the `Error:` line.

Current state (guppylang 1.0.1, selene-sim 0.3.0, pytket 2.18.1):

| Site | pass | fail |
|---|---:|---:|
| guppy | 143 | 19 |
| tket-user-guide | 166 | 0 |
| tket-api | 26 | 0 |
| systems | 55 | 11 |
| selene | 1 | 7 |
| nexus | 10 | 0 |

The standing finding: **every emulation page in the Selene user guide fails to
compile** because it still writes `result("x", measure(q))`, which Guppy 1.x
rejects — the same `measure().read()` migration this repo made (Gotcha #16).
Most Guppy `language_guide` failures are the docs' own deliberate
counter-examples ("this is rejected"); they are baselined, so they stay quiet
until their behaviour changes.



Documented and worth adopting:

```python
# Persist a job Ref to disk — ADOPTED in quantum/nexus_refs.py; the job-id cache
# is now the fallback, the saved Ref is the primary recovery path
qnx.filesystem.save(ref=execute_ref, path=Path.cwd() / "jobs" / job_name, mkdir=True)
ref = qnx.filesystem.load(path=Path.cwd() / "jobs" / job_name)
qnx.jobs.status(ref)

# Nested property stamping without threading kwargs through every call
with qnx.context.using_properties(name_qpu="H2-Emulator"):
    with qnx.context.using_properties(noisy=True, num_shots=512):
        qnx.start_execute_job(...)

# Partial harvest, cancel, retry, delete
qnx.jobs.results(job=ref, allow_incomplete=True)
qnx.jobs.cancel(ref)
qnx.jobs.retry_submission(ref,
    retry_status=[qnx.jobs.JobStatusEnum.CANCELLED],
    remote_retry_strategy=qnx.jobs.RemoteRetryStrategy.FULL_RESTART)
qnx.jobs.delete(ref)          # deletes results + snapshots, keeps circuits

# Preflight instead of guessing
qnx.devices.supports_shots(qnx.QuantinuumConfig(device_name="H2-1LE"))
qnx.jobs.get_all(job_status=[qnx.jobs.JobStatusEnum.SUBMITTED]).df()
```

`SelenePlusConfig` (`trainings/notebooks/basics/selene_examples.md`) is the
hosted Selene lane with error/runtime mode selection — the cloud twin of our
local `selene-sim` runs, and the cheapest way to cross-check a local sweep.

## Rules

- Re-run `fetch` + `audit` before any gate that adds a new qnexus call; treat a
  new entry in the drift list as a deliberate decision, not an accident.
- Cite corpus facts by docname + `sha256` from `corpus/index.json`; the corpus is
  a local research cache, not a re-publication of Quantinuum docs.
- Keep the crawler polite: sequential, 0.4 s delay, resumable — a re-run after a
  sandbox reset only fetches the delta.

## Quickstart notebooks generated from the corpus

`quantum/docs_crawler/notebooks.py` assembles four runnable notebooks —
`notebooks/quickstart-{guppy,selene,tket,lambeq}.ipynb` — out of the same
`<site>/snippets.jsonl` the audit reads. Generated, never hand-written: a docs
refresh re-emits them and the diff shows exactly which upstream example moved.

```bash
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks            # all four
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks --site guppy
```

Each notebook is the same five-part spine: header, environment check (Guppy: v1
API present; tket: `Circuit(1).Ry(0.5).get_unitary()` proves half-turns), sourced
examples one per cell with the page title and URL above it, a bridge cell showing
where the library plugs into this repo, and the pitfalls that apply to it.

Selection rules that matter when tuning a notebook:

- Only docnames in the spec's `pages` tuple are mined, in that order, with a
  `per_page_cap` so one 77-snippet page cannot eat the whole notebook.
- **Filter on `compile()`, not on a lang tag.** The markdown `_sources` twins hand
  back prose fenced as code on several lambeq and tket pages, and the extractor
  records no language — a block that does not parse is prose, and a notebook cell
  that does not parse is worse than a missing example.
- `FORBIDDEN_TOKENS` drops any block mentioning `qnexus` / `qnx.` /
  `start_execute_job` / `api_key`. Selene's MPS page ends in a live Nexus
  submission; a quickstart a reader runs top to bottom must never spend money.
- A bad pick is pinned out through `notebook_manifest.json`'s `exclude` map
  (`{"<key>": [["docname", index]]}`), which survives regeneration — never by
  editing the `.ipynb`.

`tests/test_notebooks.py` gates all of it: every manifest pick still resolves
against the corpus, every notebook is valid nbformat v4, every code cell compiles,
every sourced cell is attributed, no cell references credentials, and a fresh
build is byte-identical to what is on disk. The Guppy and Selene environment-check
cells are actually executed when `.pydeps` has `guppylang`, and skip cleanly when
it does not.

Full notebook lane (spec shape, CLI, gate ladder, `/skills` cards): see
`references/quickstart-notebooks.md`.
