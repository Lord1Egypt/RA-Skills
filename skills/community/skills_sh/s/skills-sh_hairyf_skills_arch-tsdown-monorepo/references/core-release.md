---
name: core-release
description: npm Trusted Publisher, bumpp, and release workflow
---

# Release and npm Trusted Publisher

The starter recommends **npm Trusted Publisher**: the first publish is done manually; later releases are done in CI when you push a version tag.

## One-Time Setup (Per Package)

1. **Publish once by hand** so the package exists on npm:  
   From repo root or package dir, run `pnpm publish` for each publishable package (e.g. `@pkg-placeholder/core`, `@pkg-placeholder/utils`). You may need to run from each package directory or use a filter.
2. **Connect to GitHub:** For each package, open  
   `https://www.npmjs.com/package/<your-package-name>/access`  
   and link the package to your GitHub repo (Trusted Publisher).
3. After that, **do not run `pnpm publish` locally** for normal releases; CI will publish when you push a tag.

## Release Flow

1. **Bump and tag:** Run `pnpm run release` (bumpp). Bumpp bumps version(s), updates package.json (and possibly lockfile), and creates a git tag (e.g. `v1.2.3`).
2. **Push tag:** `git push origin v1.2.3` (or push the branch with the tag).
3. **CI runs:** The **Release** workflow (`.github/workflows/release.yml`) runs on tag push `v*`, calls `sxzz/workflows` with `publish: true`, which publishes to npm using OIDC (no long-lived npm token on the runner).

## Release Workflow Snippet

```yaml
name: Release
on:
  push:
    tags:
      - 'v*'
jobs:
  release:
    uses: sxzz/workflows/.github/workflows/release.yml@v1
    with:
      publish: true
    permissions:
      contents: write
      id-token: write
```

- **contents: write** — Needed to create GitHub release / push back if the workflow does.
- **id-token: write** — Required for npm Trusted Publisher (OIDC).

## Multi-Package Releases

In a monorepo, bumpp can bump all workspace packages to the same version, or you configure it to bump only certain packages. Each publishable package that is already linked via Trusted Publisher will be published by the same workflow when its version changes and the tag is pushed.

<!--
Source references:
- https://github.com/hairyf/starter-monorepo
- https://github.com/e18e/ecosystem-issues/issues/201
- https://github.com/sxzz/workflows
-->
