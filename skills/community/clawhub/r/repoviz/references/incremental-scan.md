# Incremental Scan & Cache Protocol

Read this when the same repository is being visualized repeatedly (a living
README block, a CI-updated report) or when a full scan is too expensive for a
large monorepo. Goal: **spend tokens only on what changed** while keeping every
delivered diagram consistent with the last full scan.

## Core Rule

Default repoviz runs are stateless (no local writes). Caching is an *opt-in
maintenance mode*: enable it only when the user asks for kept-up-to-date assets
("keep my README diagram current", "regenerate the report each release"). In
that mode writing the cache file is part of the deliverable, like `inject_readme.sh`.

## Artifacts

```text
.repoviz-cache.json          # next to the repo root (gitignore it)
```

```json
{
  "version": 1,
  "commit": "<full sha of last full scan>",
  "files": {
    "src/api/index.ts": { "sha": "ab12…", "module": "api", "bytes": 4211 }
  },
  "modules": {
    "api": { "nodes": ["api"], "edges": ["web→api"] }
  }
}
```

- `files` — every source file mapped to its module, with a content hash
  (`git hash-object <file>` or `sha1sum`; either is fine, pick one and keep it).
- `modules` — which IR nodes/edges each module contributed, so a change maps
  straight to the diagrams it affects.

## Workflow

```text
First run:        Full scan  → IR → diagrams → write cache + commit sha
Subsequent runs:
  1. git diff --name-only <cached commit>..HEAD   (changed files)
  2. hash unchanged candidates? No — git diff already tells you.
  3. For each changed file: re-analyze the file, remap its module.
  4. Blast radius: re-check edges TO/FROM affected modules only
     (importers of a changed module's exports; imports it added/removed).
  5. Rebuild only the diagrams whose node/edge sets changed.
  6. Update cache; if HEAD moved, record the new commit.
```

## Invalidation Rules

| Change | Effect |
|---|---|
| File content changed, module boundary same | Re-classify that module's nodes; re-verify its edges |
| New / deleted file | Add / remove nodes; recheck neighbors' edges |
| Import added / removed in any file | Re-verify the two endpoint modules; weights (Sankey) recompute |
| Manifest changed (deps, scripts) | Re-check `ext` nodes and any dependency-weighted flows |
| Merge / rebase moved HEAD many commits | If changed files > ~30% of total, do a full rescan instead |

## Token Discipline

- Never re-read unchanged files on a cache hit — trust the diff.
- Cap blast-radius re-checks at the direct neighborhood; mark second-order
  effects `inferred` instead of re-scanning them.
- A cache-miss repo (no cache file, user opted out) always behaves exactly like
  the stateless default: this protocol adds nothing to one-off scans.

## Anti-Patterns

- Don't cache silently: the user must know a file is being maintained.
- Don't reuse stale evidence: when a module is re-analyzed, its evidence entries
  are regenerated, not carried over.
- Don't cache across branches without recording the branch name — include it in
  the cache header if you support branch switching (`"branch": "main"`).
