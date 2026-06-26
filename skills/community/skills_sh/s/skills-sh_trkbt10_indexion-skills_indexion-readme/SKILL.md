---
name: indexion-readme
description: README construction — initialize template structure, generate per-package READMEs from doc comments, plan writing tasks, assemble root README from docs/ and package READMEs via doc.json config, and verify edits with `plan drift`.
---

# indexion readme — README Construction

Build project READMEs from templates, doc comments, hand-written prose, and
per-package READMEs. This skill covers the **construction side**: scaffolding,
generating, planning, assembling, and verifying. For evaluating existing
documentation, see `indexion-documentation`.

## Where things live

The conventions vary by project; check what actually exists before editing:

| Asset | Location patterns seen |
|-------|------------------------|
| Config | `doc.json` (repo root) **or** `.indexion/readme/doc.json` |
| Per-package template | `docs/templates/readme.md` (no SoT constant; declared via `--template`) |
| Static prose | `docs/intro.md`, `docs/installation.md`, `docs/license.md`, … |
| Per-package READMEs | `cmd/<name>/README.md`, `src/<name>/README.md` |
| Assembled root README | usually `README.md`. Some projects use a `.mbt.md` suffix so the file is also a MoonBit doctest module — when so, `README.md` is a symlink to `README.mbt.md`. |
| `.indexion.toml` | `[doc] config_path` / `per_package` auto-load doc.json |

**The first thing to check** is `git diff` / `ls -la` for: a symlink on `README.md`, a `doc.json` (at root or under `.indexion/readme/`), and `.indexion.toml`. The presence of these tells you whether the README is hand-maintained, build-assembled, or a hybrid.

## Workflow overview

```
doc init                      → .indexion/readme/template.md + doc.json (greenfield)
edit doc.json + docs/*.md     → declare sources of truth
doc readme --per-package      → cmd/<pkg>/README.md (API skeletons; non-overwriting)
hand-write each per-package README's Overview / Usage / Options / Examples
doc readme --config           → assembled root README
plan drift <prev> <new>       → verify the assembled output (or hand-edit) is purely additive
```

## Step 1: Initialize (greenfield only)

```bash
indexion doc init <project-dir>
```

Creates `.indexion/readme/template.md` + `.indexion/readme/doc.json`. Skip this step on a project that already has `doc.json` or `.indexion.toml` pointing at one.

## Step 2: Configure doc.json

```json
{
  "$schema": "./schemas/doc-config.schema.json",
  "version": "1.0",
  "spec": "moonbit",
  "output": { "format": "markdown", "filename": "README.md" },
  "packages": [
    {
      "path": "cmd/<name>",
      "title": "<command name>",
      "include_in_root": true,
      "sections": ["overview", "usage"]
    }
    // …one entry per package that should appear in the assembled root README
  ],
  "root": {
    "output": "README.md",
    "sections": [
      { "type": "static",   "file": "docs/intro.md" },
      { "type": "toc",      "title": "Commands" },
      { "type": "packages", "filter": "cmd/**" },
      { "type": "static",   "file": "docs/installation.md" },
      { "type": "static",   "file": "docs/license.md" }
    ]
  }
}
```

**Root section types:**
- `static` — include a markdown file verbatim
- `toc` — insert a table-of-contents heading
- `packages` — pull in entries from the `packages` array, filtered by glob

**Package fields:**
- `include_in_root` — whether to include in the assembled root README
- `sections` — README headings to extract; honored by per-package extraction
  flows. Note that `{ "type": "packages" }` in the root currently emits a
  **table** of package links, not the rich Overview/Usage expansion implied
  by per-package `sections`. See "Known limitation" below.

## Step 3: Generate per-package READMEs

```bash
indexion doc readme --per-package src/ cmd/
```

Generates `README.md` in each package directory that doesn't already have one. **Non-overwriting** — existing per-package READMEs are left alone.

The skeleton is API-only (extracted from `///` doc comments via KGF). Treat it as a starting point and hand-write the prose sections (Overview, Usage, Options, Examples) afterwards.

```bash
# Single package to stdout
indexion doc readme src/kgf/lexer/

# Single package to a file
indexion doc readme -o=README.md src/kgf/lexer/
```

**Note on side effects**: `doc readme --template=<t> <paths...>` (the template-based mode below) walks the given paths and **auto-creates** per-package READMEs for any package that lacks one — even without `--per-package`. If you run it on a broad path (`cmd/`, `src/`), expect new files in unrelated packages. Run with a narrow path or grep `git status` afterwards to clean up unintended creations.

## Step 4: Write static content

Create `docs/intro.md`, `docs/installation.md`, etc. — whatever your `root.sections` references. These are the hand-written prose; the assembler pulls them in verbatim.

## Step 5: Generate writing plans (optional)

```bash
indexion plan readme --template=docs/templates/readme.md --plans-dir=.indexion/plans src/
```

Emits per-section writing tasks for manual or LLM-assisted authoring.

## Step 6: Assemble the README

```bash
# Config-driven (preferred; doc.json controls layout and packages list)
indexion doc readme --config=doc.json

# Template-driven (alternative; {{include:…}} and {{packages}} placeholders)
indexion doc readme --template=docs/templates/readme.md -o=README.md cmd/
```

The config path can live at repo root or under `.indexion/readme/`. With `.indexion.toml`'s `[doc] config_path = "…"`, the `--config=` flag becomes optional.

## Step 7: Verify with `plan drift`

After regeneration **or** any hand-edit of the root README, verify the change is purely additive (no silent deletions, no reflowing of unrelated sections):

```bash
# Snapshot the previous version
git show HEAD:README.md > /tmp/README.before.md

# Compare against the new version
indexion plan drift --top=20 /tmp/README.before.md README.md
```

What to look for in the output:
- `Drift terms in /tmp/README.before.md (missing on the other side): (none)` — nothing was removed
- `Drift terms in README.md (missing on the other side): …` — exactly the new vocabulary you intended to add (command names, new flags, new concepts)
- `Cosine similarity` near 1.0 for a small additive change; substantially lower if you reshaped a section

For CI integration:

```bash
indexion plan drift --vocab-threshold=0.05 /tmp/README.before.md README.md
# exits 1 if cosine_distance > 0.05 — useful as a guard against accidental large rewrites
```

This same workflow applies to translated README pairs (`README.md` ↔ `README-ja.md`): cross-lingual drift detection works natively because vocab sub-tokenization delegates to the natural-language KGFs in `kgfs/natural/`.

## Template syntax

The template file supports `{{placeholder}}` substitution:

| Placeholder | Expansion |
|-------------|-----------|
| `{{include:path}}` | Contents of the file (relative to project root) |
| `{{packages}}` | All discovered packages (filtered by CLI `--include` / `--exclude`) |
| `{{module_doc}}` | Module-level documentation only |

## .indexion.toml integration

```toml
[doc]
config_path = "doc.json"   # auto-loads doc.json without --config
per_package = true         # makes `doc readme <path>` default to --per-package
```

Explicit `--config=…` always takes priority.

## Known limitation: `packages` root section produces a table, not rich expansion

The `doc-config.schema.json` permits `sections: ["overview", "usage", …]` on each `packageEntry`, but the current `doc readme --config` implementation does not expand those sections inline when emitting `{ "type": "packages" }` in the root. The output is a markdown table of package links with empty descriptions.

Two practical consequences:

1. If the project's checked-in root README has rich per-command Overview / Usage paragraphs, they were not produced by `doc readme --config` as it stands now. They are hand-maintained. Diff `doc readme --config -o=/tmp/regen.md` against the checked-in README to see how much of it is hand-curated; very large diffs mean the README is mostly hand-maintained.
2. For new commands, you currently need to **also** hand-edit the rich section into the assembled README, in addition to adding the package entry to `doc.json` and writing the per-package README. Use the `plan drift` verification above to confirm the hand-edit only adds, never removes.

If you fix this limitation (so `{ "type": "packages" }` honors per-entry `sections`), update this skill to remove this section.

## Common pitfalls

**"doc readme --per-package generated nothing"**
- All packages already have READMEs. The command only creates new files,
  never overwrites. Delete existing READMEs first to regenerate.

**"doc readme --template … on `cmd/` created READMEs in packages I didn't touch"**
- Template mode auto-generates missing per-package READMEs as a side effect.
  Either pass a narrow path, or revert unintended creations from `git status`.

**"Auto-generated per-package READMEs are just API listings"**
- By design. Hand-write Overview, Usage, Options, Examples. For CLI commands,
  the authoritative behavior comes from `indexion <command> --help`.

**"My hand-edit to README.md will be wiped out by `doc readme --config`"**
- It will if the assembler ever produces the rich shape (see "Known
  limitation"). Until then, the assembler produces a strict subset (the
  table) and your hand-edits to the rich sections survive. Always run the
  `plan drift` cross-check to be sure.

**"README.md edit destroyed unrelated sections"**
- Run `plan drift HEAD:README.md README.md` and look at the "missing on the
  other side" output for the previous version. If it lists anything other
  than `(none)`, you removed content.
