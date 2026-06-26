---
name: indexion-wiki
description: Project wiki lifecycle — create pages, track source changes with ingest, update stale pages, lint structural integrity, detect code-to-doc drift with reconcile, and manage search indexes. A runbook for navigating and maintaining the wiki as an agent.
---

# indexion wiki

indexion's wiki system maintains a knowledge base at `.indexion/wiki/` as a collection of
Markdown files governed by a `wiki.json` manifest.

## A wiki page is not just a `.md` file

A wiki page consists of **four synchronized artifacts**:

| Artifact | File | Updated by |
|----------|------|------------|
| Page content | `<id>.md` | `wiki pages add`, `wiki pages update` |
| Manifest entry | `wiki.json` | `wiki pages add`, `wiki pages update` |
| Search index | `vectors.db`, `search-sections.json`, `tfidf-vocabulary.json` | `wiki pages update`, `wiki index build --full` |
| Audit log | `log.json` | Every wiki-modifying command |

**`wiki pages update` updates all four at once.** Editing the `.md` file directly updates
only the first. The other three become stale — search returns old results, the manifest
carries wrong provenance, and the log has no record of the change.

If you edit a `.md` directly (e.g. via `Edit` tool), you **must** immediately follow up:

```bash
indexion wiki pages update \
  --id=<page-id> \
  --content=.indexion/wiki/<page-id>.md \
  --sources="<comma-separated sources from wiki.json>" \
  --provenance=synthesized \
  --actor="agent:claude" \
  --wiki-dir=.indexion/wiki
```

Every wiki page also carries two provenance fields in the manifest:
- `provenance`: `"extracted"` | `"synthesized"` | `"manual"`
- `last_actor`: `"indexion"` | `"agent:<name>"` | `"user"`

## Command Structure

```
indexion wiki
  ├── pages
  │   ├── plan    -- propose page structure (init-like)
  │   ├── add     -- create a new page (writes .md + manifest + index + log)
  │   ├── update  -- update an existing page (writes .md + manifest + index + log)
  │   └── ingest  -- detect stale pages by hashing sources
  ├── index
  │   └── build   -- rebuild index.md (and optionally vectors.db)
  ├── lint        -- structural integrity checks (no LLM needed)
  ├── export      -- export to GitHub/GitLab wiki format
  ├── import      -- import from GitHub/GitLab wiki format
  └── log         -- operation audit trail
```

## Navigating the Wiki (as an agent)

Before reading individual pages, start with the index:

```bash
# Generate or regenerate index.md — the entry point for navigation
indexion wiki index build --wiki-dir=.indexion/wiki

# Then read it
cat .indexion/wiki/index.md
```

`index.md` lists pages by category and identifies **hub pages** (most-linked pages).
Hub pages are the best starting points for understanding an unfamiliar codebase.

## Writing a New Page

```bash
# 1. Write content to a temp file
cat > /tmp/my-page.md << 'EOF'
# My Page Title
...content...
EOF

# 2. Register it — this writes .md, updates wiki.json, updates search index, appends log
indexion wiki pages add \
  --id=my-page \
  --title="My Page Title" \
  --content=/tmp/my-page.md \
  --sources="src/my-module/" \
  --provenance=synthesized \
  --actor="agent:claude" \
  --wiki-dir=.indexion/wiki
```

The `--sources` field links the page to source files for change tracking.
Always specify it — pages without sources are invisible to `wiki pages ingest`.

## Updating an Existing Page

```bash
# 1. Write new content to a temp file
cat > /tmp/updated.md << 'EOF'
# Updated Page
...new content...
EOF

# 2. Update — this overwrites .md, updates wiki.json metadata,
#    incrementally updates the search index, and appends to log.json
indexion wiki pages update \
  --id=existing-page \
  --content=/tmp/updated.md \
  --sources="src/my-module/,src/other/" \
  --provenance=synthesized \
  --actor="agent:claude" \
  --wiki-dir=.indexion/wiki
```

Expected output: `Updated page 'existing-page' (search index updated)`

## Detecting What Needs Updating

```bash
# Find pages whose source files have changed since the last run
indexion wiki pages ingest --wiki-dir=.indexion/wiki

# Preview without recording the new hash state
indexion wiki pages ingest --dry-run --wiki-dir=.indexion/wiki
```

`ingest` hashes every source file listed in `wiki.json` and compares against
`.indexion/wiki/ingest-manifest.json`. It outputs an update task list but does
**not** rewrite pages — that is the agent's responsibility.

Workflow:
1. Run `wiki pages ingest` to get the task list.
2. For each task, read the changed source files.
3. Update the wiki page with `wiki pages update`.
4. Re-run `ingest` — it should report 0 pages needing attention.

## Verifying Structural Integrity

```bash
# Run all 6 structural checks
indexion wiki lint --wiki-dir=.indexion/wiki
```

| Check | What it finds |
|-------|--------------|
| Broken links | `wiki://page-id` references to pages that don't exist |
| Orphan pages | Pages unreachable from nav tree and not linked by any other page |
| Missing cross-references | Pages sharing source files that don't link to each other |
| Stale sources | `sources` paths that no longer exist on disk |
| Empty pages | Pages with near-zero content |
| Manifest-file mismatch | `wiki.json` entries with no `.md` file (or vice versa) |

After writing new pages, always run `wiki lint` and fix any issues before finishing.

Cross-reference warnings are common when related concepts are split across pages.
Fix them by adding a `## See Also` section with `wiki://page-id` links.

## Verifying Content Accuracy (`plan reconcile`)

`wiki lint` catches **structural** problems. `plan reconcile` catches **semantic** drift —
whether the code symbols described in a wiki page still exist and whether the code has
changed since the page was last written.

**Always target the project root (`.`).** The `--doc` flag restricts which documents
participate, but the target directory determines the code symbol universe. Targeting a
subdirectory shrinks the symbol set and produces zero-fragment reports.

```bash
indexion plan reconcile \
  --doc='.indexion/wiki/*.md' \
  --doc-spec=markdown \
  --format=md \
  .
```

### Reading the report

**Summary** — key metric is `New logical reviews` (fresh drift since last run).

**Suggested Review Groups** — the actionable core:

| Category | Meaning | Action |
|----------|---------|--------|
| `stale_doc` | Code changed after the wiki page was last updated | Update the page via `wiki pages update` |
| `missing_doc` | Code symbols with no matching wiki coverage | Add coverage or create a new page via `wiki pages add` |
| `review_both` | Wiki is newer than code | Verify the wiki content is correct; this is the expected state after a maintenance cycle |

Each group lists affected symbols and the `Docs:` wiki pages involved.
Groups without a `Docs:` line mean no wiki page covers that module.

### Residual candidates that persist after maintenance

Reconcile candidates never reach zero. Three sources of persistent candidates:

1. **Modules without wiki pages** produce `missing_doc`. Create pages if coverage is needed.
2. **Qualified method names** (`Type::method` in wiki) don't match bare symbol names
   (`method` in code). Verify by grepping the wiki for the symbol name before adding entries.
3. **Same-name symbols across modules** (`get`, `tokenize`, `to_json_string`) cause
   cross-module false positives. Check which module the wiki page actually describes.

Track `New logical reviews` as the convergence metric. When it reaches zero,
all actionable drift has been addressed.

## Full Wiki Maintenance Cycle

```bash
# 1. Detect stale pages (source files changed)
indexion wiki pages ingest --wiki-dir=.indexion/wiki

# 2. Read the index to understand the wiki structure
cat .indexion/wiki/index.md

# 3. For each stale page: read changed sources, write new content to temp file,
#    then update through the command (NOT by editing .md directly)
indexion wiki pages update --id=<page-id> --content=/tmp/updated.md \
  --sources="..." --provenance=synthesized --actor="agent:<name>" \
  --wiki-dir=.indexion/wiki

# 4. Verify structural integrity
indexion wiki lint --wiki-dir=.indexion/wiki

# 5. Verify content accuracy — target project root, iterate until NLR=0
indexion plan reconcile \
  --doc='.indexion/wiki/*.md' \
  --doc-spec=markdown \
  --format=md \
  .
# → Fix stale_doc groups first. Re-run. Expect 2-3 rounds.
# → For each fix, use `wiki pages update`, not direct .md edits.

# 6. Regenerate the navigation index
indexion wiki index build --wiki-dir=.indexion/wiki

# 7. Confirm everything is current
indexion wiki pages ingest --dry-run --wiki-dir=.indexion/wiki
```

## Planning a New Wiki from Scratch

When the wiki doesn't exist yet or needs a structural overhaul:

```bash
# Analyze the project and generate a page structure proposal
indexion wiki pages plan --format=md <project-dir>

# Then execute the plan: add each proposed page
indexion wiki pages add --id=<id> --title="..." --content=/tmp/page.md \
  --sources="..." --provenance=synthesized --actor="agent:<name>"
```

**No initialization step is needed.** The first `wiki pages add` call automatically
creates `.indexion/wiki/` and an empty `wiki.json` manifest. There is no separate
`wiki init` command.

`wiki pages plan` uses the CodeGraph to propose concept-based pages, not file-based ones.
Prefer concept pages (e.g., "KGF System") over file pages (e.g., "src/kgf/lexer/lexer.mbt").

## Building the Search Index

```bash
# Build navigation index only (index.md)
indexion wiki index build --wiki-dir=.indexion/wiki

# Build navigation + vector search index (vectors.db)
indexion wiki index build --full --wiki-dir=.indexion/wiki

# Preview index.md without writing
indexion wiki index build --dry-run --wiki-dir=.indexion/wiki
```

With `--full`, `indexion search .indexion/wiki/` will use the pre-built vectors
instead of rebuilding from scratch on each query.

## Checking the Audit Trail

```bash
# Recent operations
indexion wiki log --wiki-dir=.indexion/wiki --tail=20

# Full log as JSON
indexion wiki log --wiki-dir=.indexion/wiki --json
```

Every `pages add`, `pages update`, `lint`, `pages ingest`, and `index build` call appends to
`.indexion/wiki/log.json`. Use the log to verify that previous agent runs completed
correctly, or to understand why a page was last modified.

## Key Pitfalls

**Backtick-quoted `wiki://` references are not links.** The lint checker correctly
ignores ``wiki://`` in code spans. Use bare `wiki://page-id` or Markdown links
`[Title](wiki://page-id)` to create real cross-references.

**`wiki pages ingest` manifests state at the time of the last run.** If you add new source
files to a page's `sources` list via `pages update`, the next `ingest` run will show
that page as needing attention (because the new sources have no recorded hash). This is
expected behavior — run `ingest` again after the update to record the baseline.
