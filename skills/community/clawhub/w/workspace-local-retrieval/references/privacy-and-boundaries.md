# Privacy and Boundaries

Use this file when designing the retrieval boundary.

## Goal

Keep retrieval useful without accidentally widening data exposure.

## Separation model

Treat these as different layers:

1. **Personal memory**
   - `MEMORY.md`
   - `memory/*.md`
   - user journals
   - private daily logs

2. **Workspace knowledge**
   - skill docs
   - agent docs
   - plans
   - schemas
   - references
   - reusable operating notes

3. **Runtime state and sensitive material**
   - credentials
   - caches
   - generated indexes
   - logs
   - tmp/out directories
   - private exports

Only the second layer should usually enter a general retrieval corpus.

## Exclude by default

Common exclusions:

```text
memory/**
my_note/**
my_profile/**
.openclaw/**
.clawhub/**
.git/**
out/**
tmp/**
node_modules/**
retrieval/indexes/**
```

Also exclude:
- secrets and credential folders
- personal archives
- binary dumps
- transcript caches
- generated HTML exports unless intentionally curated

## Corpus design heuristics

Prefer corpora that answer one of these questions cleanly:
- What should the main coordinator know?
- What should a specialist agent know?
- What should remain private to one domain?
- What should never be indexed?

Good corpus examples:
- `workspace-core`
- `workspace-product`
- `workspace-research`
- `workspace-specialist-private`

Bad corpus examples:
- `everything`
- `misc`
- `all-notes`

## Trust model

Assume that retrieval broadens access.

If an agent can retrieve a file, that file is now effectively easier to surface. Design with that assumption from the start.

## Publishing guidance

When converting a private retrieval setup into a shared skill:
- remove personal paths
- remove real usernames and identifiers
- replace domain names with neutral examples where possible
- ship templates, not private corpora snapshots
- avoid embedding any live data in sample configs
