---
name: pnpm-package-sources
description: Supported package sources—npm, JSR, workspace, Git, tarball
---

# pnpm Package Sources

pnpm supports installing from trusted and exotic sources. Exotic sources (Git, tarball URLs) pose supply-chain risks for transitive deps—use `blockExoticSubdeps: true` to restrict.

## Trusted Sources

### npm Registry

```bash
pnpm add express
pnpm add express@nightly
pnpm add express@1.0.0
pnpm add express@">=0.1.0 <0.2.0"
```

### JSR Registry (v10.9+)

```bash
pnpm add jsr:@hono/hono
pnpm add jsr:@hono/hono@4
pnpm add jsr:@hono/hono@latest
```

### Workspace

Use `workspace:` protocol for local packages. See [core-workspaces](core-workspaces.md).

### Local Filesystem

```bash
pnpm add ./package.tar.gz
pnpm add ./some-directory   # symlink, same as pnpm link
```

## Exotic Sources

### Remote Tarball

```bash
pnpm add https://github.com/user/repo/tarball/v1.0.0
```

### Git Repository

```bash
# Latest from default branch
pnpm add kevva/is-positive

# Commit hash
pnpm add kevva/is-positive#97edff6f525f192a3f83cea1944765f769ae2678

# Branch
pnpm add kevva/is-positive#master

# Tag
pnpm add zkochan/is-negative#2.0.1

# Semver range
pnpm add kevva/is-positive#semver:^2.0.0

# Subdirectory (monorepo)
pnpm add user/repo#path:/packages/app

# Full URL
pnpm add git+ssh://git@github.com:user/repo.git#2.0.1
pnpm add https://github.com/user/repo.git#2.0.1

# Provider shorthand
pnpm add github:user/repo
pnpm add bitbucket:user/repo
pnpm add gitlab:user/repo
```

## Supply Chain Safety

- `blockExoticSubdeps: true` prevents transitive deps from using Git/tarball
- See [features-supply-chain-security](features-supply-chain-security.md) for allowBuilds, trustPolicy, etc.

<!--
Source references:
- https://pnpm.io/package-sources
-->
