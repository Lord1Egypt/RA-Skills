# Repo-Aware Generation

`visual-architecture` can now create a first useful architecture draft from a local repository. The extractor is deliberately conservative: it looks for repo surfaces that are easy to defend with file evidence, then emits a normal JSON spec that can be reviewed and edited.

```bash
python3 scripts/render_architecture.py extract-repo . --output examples/visual-architecture-auto.json
python3 scripts/render_architecture.py deliver examples/visual-architecture-auto.json examples/visual-architecture-auto.html --min-quality good --json
```

For pull requests, generate a changed-file review surface:

```bash
python3 scripts/render_architecture.py extract-pr --base origin/master --head HEAD --output examples/pr-delta-extracted.json
```

For hand-authored specs, apply deterministic layout before delivery:

```bash
python3 scripts/render_architecture.py layout input.json output.json --mode architecture --theme showcase
```

For release assets, bundle everything together:

```bash
python3 scripts/render_architecture.py bundle examples/visual-architecture-auto.json /tmp/visual-architecture-bundle --min-quality good
```

A generated artifact is still a draft. The receipt quality rating, warnings, and evidence list are the review surface.


## v1.6 Extraction Quality

The v1.6 extractor is language-aware rather than only filename-aware. It classifies Python runtime files, package metadata, GitHub Actions workflows, JSON schemas, checked examples, generated gallery files, and product docs. Generated source-backed artifacts carry extraction rules, source type, confidence, and file/line evidence on every node and edge. PR delta extraction groups changed files into architecture concerns so the review artifact says what surface changed, not just which files changed.


## v1.7 TypeScript Monorepo Extraction

The v1.7 extractor skips common generated and dependency directories by default, then detects workspaces from package metadata. It creates package/app nodes for client, server, and editor-extension style workspaces, scans TS/TSX imports for per-package dependency summaries, and detects backend modules, realtime gateways, database/migration layers, frontend entries, API clients, config boundaries, and feature folders. Extracted edges are filtered so generated specs cannot point at missing nodes.
