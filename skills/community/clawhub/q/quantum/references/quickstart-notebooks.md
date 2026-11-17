# Quickstart notebooks (Guppy / Selene / tket / lambeq)

Four `.ipynb` quickstarts are **generated**, never hand-edited: they are assembled
from the crawled Quantinuum docs corpus (`references/quantinuum-docs-corpus.md`)
by `quantum/docs_crawler/notebooks.py` and written to `notebooks/quickstart-<key>.ipynb`.
Edit the spec or the corpus, then regenerate — a hand edit is silently reverted by
the byte-match test.

## Spec shape

```python
NotebookSpec(
    key="guppy", site="guppy", title=..., blurb=...,
    install='pip install "guppylang>=1.0"',
    env_check="import guppylang\n...",     # the ONE executable cell
    env_modules=("guppylang",),            # metadata only, never emitted
    pages=(...docnames in order...),       # only these are mined
    bridge_title=..., bridge_code=...,     # how this library plugs into our sweeps
    pitfalls=(...),                        # rendered as the closing numbered list
    max_cells=..., per_page_cap=4, extra_pages=(),
)
```

`env_modules` must list **every** third-party top-level module the `env_check`
cell imports. It is not decoration: the test suite parametrises the skip gate and
the drift gate over it, so an import that is not declared escapes both guards.
A test re-derives the declared set from the cell source and fails on divergence.

## CLI

```bash
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks --list
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks              # all four
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks --only guppy
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks --only guppy,tket
PYTHONPATH=.pydeps python3 -m quantum.docs_crawler.notebooks --only selene --out /tmp/nb
```

- `--only` is repeatable *and* comma-separated; an unknown key exits non-zero
  printing the valid keys (silently generating nothing is the worse failure).
- The **default** output dir owns the committed `notebook_manifest.json`. A
  non-default `--out` writes its own manifest beside its notebooks and leaves the
  committed one untouched — otherwise a scratch run poisons the shared manifest
  with rows pointing at files that are not in `notebooks/`.
- A bad snippet pick is pinned out by hand via the manifest's `exclude` list, not
  by editing the notebook.

## Gate ladder (`tests/test_notebooks.py`)

Ordered by what each one actually catches:

| Gate | Catches |
| --- | --- |
| manifest picks resolve against the corpus | a re-crawl dropping a page we mined |
| valid `nbformat` v4 | structural breakage in the writer |
| every code cell `compile()`s | a snippet that is prose or truncated |
| every sourced cell attributed | an unattributed upstream block |
| no credentials / no billable calls | a quickstart that would spend HQCs |
| **byte-exact regeneration** | indentation, key order, trailing-newline drift |
| declared `env_modules` == imported | a new import escaping both env gates |
| env-check cell **runs** when deps present | a genuinely broken cell |
| env-check cell **skips** when deps absent | the skip path (see the pitfall below) |

The skip gate runs the real env-check test in a **child pytest** with a
`meta_path` finder that raises `ModuleNotFoundError` for the target module and
its submodules (and purges it from `sys.modules` first). A plugin collects
per-test outcomes into a JSON report; the parent asserts zero failures, exactly
one skip, and a reason naming both the module and its install command. The
blocker lives in the child only — installed in the parent it leaks into every
later test in the file. A child that fails to start is a **skip carrying its
stdout**, never a silent pass.

## `/skills` cards

`scripts/build-skill-bundles.mjs` parses each generated notebook to build its
card, so the card content is a function of the generator's markdown shape:

- `topics` / `sourcePages` — distinct titles from the `**[Title](url)**`
  attribution lines.
- `pitfalls` — the closing numbered list under `## Pitfalls`, verbatim.
- `install` — the opening bash block.

All parsers are defensive (unexpected shape yields an empty value rather than a
build failure), which means a shape change **empties the cards silently**.
`tests/test_skill_bundles_manifest.py` is the gate: every notebook entry must
have non-empty `topics` and `pitfalls`, `sourcePages` matching `topics.length`,
and clean single-line strings.
