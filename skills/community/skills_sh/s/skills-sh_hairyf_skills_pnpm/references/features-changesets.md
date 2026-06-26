---
name: pnpm-changesets
description: Monorepo versioning and publishing with Changesets
---

# pnpm + Changesets

Changesets manages versions and changelogs in pnpm workspaces.

## Setup

```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
```

## Workflow

### Add Changeset

```bash
pnpm changeset
```

Creates markdown files in `.changeset/`. Commit them.

### Release

```bash
pnpm changeset version   # Bump versions, update changelogs
pnpm install             # Update lockfile
# Commit changes
pnpm publish -r          # Publish bumped packages
```

## GitHub Actions

```yaml
name: Changesets

on:
  push:
    branches: [main]

jobs:
  version:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install
      - uses: changesets/action@v1
        with:
          commit: "chore: update versions"
          publish: pnpm ci:publish
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

Add to `package.json`:

```json
{
  "scripts": {
    "ci:publish": "pnpm publish -r"
  }
}
```

For scoped public packages, use `--access=public` in publish.

<!--
Source references:
- https://pnpm.io/using-changesets
-->
