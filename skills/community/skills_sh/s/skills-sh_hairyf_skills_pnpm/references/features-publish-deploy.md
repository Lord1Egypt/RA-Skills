---
name: features-publish-deploy
description: Publishing packages, creating tarballs, deploy, and fetch for Docker
---

# Publish, Pack, Deploy & Fetch

## pnpm publish

Publish package to registry.

```bash
# Publish current package
pnpm publish

# With tag
pnpm publish --tag next

# Public scoped package
pnpm publish --access public

# Recursive (all workspace packages)
pnpm -r publish

# Dry run
pnpm publish --dry-run

# Skip git checks
pnpm publish --no-git-checks

# 2FA
pnpm publish --otp 123456

# Provenance (CI)
pnpm publish --provenance

# Filter
pnpm publish --filter "@myorg/*"
```

### publishConfig

Override fields in `package.json` before publish:

```json
{
  "publishConfig": {
    "directory": "dist",
    "registry": "https://npm.pkg.github.com",
    "access": "public"
  }
}
```

### Lifecycle scripts

- `prepublishOnly`, `prepublish`, `prepack`, `prepare`, `postpack`, `publish`, `postpublish`

### pnpm-workspace.yaml

```yaml
gitChecks: false
publishBranch: production
```

## pnpm pack

Create tarball without publishing:

```bash
pnpm pack
# Creates <name>-<version>.tgz
```

## pnpm deploy

Deploy a workspace package to a directory with isolated `node_modules`. Creates a portable bundle.

```bash
pnpm --filter <package> deploy <target-dir>

# Production (skip devDependencies)
pnpm --filter my-app --prod deploy ./dist
```

### Docker example

```dockerfile
FROM workspace as pruned
RUN pnpm --filter my-app --prod deploy pruned

FROM node:18-alpine
WORKDIR /app
COPY --from=pruned /app/pruned .
ENTRYPOINT ["node", "index.js"]
```

### Options

- `--prod`, `-P` - Skip devDependencies
- `--filter` - Select package
- `--legacy` - Use legacy deploy (no inject-workspace-packages)

## pnpm fetch

Fetch packages from lockfile into virtual store **without** reading `package.json`. Optimizes Docker layers: only lockfile changes invalidate cache.

```bash
# Fetch production deps only
pnpm fetch --prod

# Then install offline (no registry calls)
pnpm install -r --offline --prod
```

### Docker example

```dockerfile
COPY pnpm-lock.yaml pnpm-workspace.yaml ./
COPY patches patches
RUN pnpm fetch --prod

COPY . .
RUN pnpm install -r --offline --prod
```

As long as lockfile is unchanged, build cache is valid through the fetch layer.

## Key Points

- `publish` - Publish to registry; supports `--tag`, `--access`, `--filter`
- `pack` - Create tarball
- `deploy` - Bundle workspace package + deps for deployment
- `fetch` - Pre-populate store from lockfile only; use with `install --offline` in Docker

<!--
Source references:
- https://pnpm.io/cli/publish
- https://pnpm.io/cli/pack
- https://pnpm.io/cli/deploy
- https://pnpm.io/cli/fetch
-->
