---
name: pnpm
description: Node.js package manager with strict dependency resolution. Use when running pnpm specific commands, configuring workspaces, or managing dependencies with catalogs, patches, or overrides.
metadata:
  author: Anthony Fu
  version: "2026.2.1"
  source: Generated from https://github.com/pnpm/pnpm, scripts located at https://github.com/antfu/skills
---

pnpm is a fast, disk space efficient package manager. It uses a content-addressable store to deduplicate packages across all projects on a machine, saving significant disk space. pnpm enforces strict dependency resolution by default, preventing phantom dependencies. Configuration should preferably be placed in `pnpm-workspace.yaml` for pnpm-specific settings.

**Important:** When working with pnpm projects, agents should check for `pnpm-workspace.yaml` and `.npmrc` files to understand workspace structure and configuration. Always use `--frozen-lockfile` in CI environments.

> The skill is based on pnpm 10.x, generated at 2026-02-01.

## Core

| Topic | Description | Reference |
|-------|-------------|-----------|
| Installation | Standalone script, Corepack, npm, system package managers | [core-installation](references/core-installation.md) |
| CLI Commands | Install, add, remove, update, run, exec, dlx, and workspace commands | [core-cli](references/core-cli.md) |
| Configuration | pnpm-workspace.yaml, .npmrc settings, and package.json fields | [core-config](references/core-config.md) |
| Workspaces | Monorepo support with filtering, workspace protocol, and shared lockfile | [core-workspaces](references/core-workspaces.md) |
| Store | Content-addressable storage, hard links, and disk efficiency | [core-store](references/core-store.md) |
| Package Sources | npm, JSR, workspace, Git, tarball—trusted and exotic sources | [core-package-sources](references/core-package-sources.md) |
| Errors | Common error codes and resolutions | [core-errors](references/core-errors.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Filtering | Rich selector syntax for --filter (deps, dependents, changed, globs) | [features-filtering](references/features-filtering.md) |
| Catalogs | Centralized dependency version management for workspaces | [features-catalogs](references/features-catalogs.md) |
| Overrides | Force specific versions of dependencies including transitive | [features-overrides](references/features-overrides.md) |
| Patches | Modify third-party packages with custom fixes | [features-patches](references/features-patches.md) |
| Aliases | Install packages under custom names using npm: protocol | [features-aliases](references/features-aliases.md) |
| Hooks | Customize resolution with .pnpmfile.cjs hooks | [features-hooks](references/features-hooks.md) |
| Peer Dependencies | Auto-install, strict mode, and dependency rules | [features-peer-deps](references/features-peer-deps.md) |
| Config Dependencies | Share hooks, catalogs, patches across projects | [features-config-dependencies](references/features-config-dependencies.md) |
| Git Branch Lockfiles | Branch-specific lockfiles to avoid merge conflicts | [features-git-branch-lockfiles](references/features-git-branch-lockfiles.md) |
| Changesets | Monorepo versioning and publishing | [features-changesets](references/features-changesets.md) |
| Supply Chain Security | allowBuilds, blockExoticSubdeps, trustPolicy | [features-supply-chain-security](references/features-supply-chain-security.md) |
| Finders | Search dependency graph by package properties (v10.16+) | [features-finders](references/features-finders.md) |
| Completion | Shell tab completion (Bash, Zsh, Fish) | [features-completion](references/features-completion.md) |
| Scripts | Lifecycle scripts and pnpm:devPreinstall | [features-scripts](references/features-scripts.md) |
| Cache | Metadata cache commands (list, view, delete) | [features-cache](references/features-cache.md) |
| Node.js Env | Manage Node.js versions (pnpm env use/add/remove) | [features-env](references/features-env.md) |
| Publish & Deploy | publish, pack, deploy, fetch for Docker and registry | [features-publish-deploy](references/features-publish-deploy.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| CI/CD Setup | GitHub Actions, GitLab CI, Docker, and caching strategies | [best-practices-ci](references/best-practices-ci.md) |
| Docker | BuildKit cache, pnpm fetch, pnpm deploy for monorepos | [best-practices-docker](references/best-practices-docker.md) |
| Production | Lockfile deployment, offline install | [best-practices-production](references/best-practices-production.md) |
| Only Allow pnpm | Enforce pnpm with preinstall (only-allow) | [best-practices-only-allow-pnpm](references/best-practices-only-allow-pnpm.md) |
| TypeScript | preserveSymlinks, packageExtensions, @pnpm/plugin-types-fixer | [best-practices-typescript](references/best-practices-typescript.md) |
| Podman | Btrfs reflinks, store and node_modules volume mounts | [best-practices-podman](references/best-practices-podman.md) |
| Git | Lockfile commit and merge conflict resolution | [best-practices-git](references/best-practices-git.md) |
| Migration | Migrating from npm/Yarn, handling phantom deps, monorepo migration | [best-practices-migration](references/best-practices-migration.md) |
| Performance | Install optimizations, store caching, workspace parallelization | [best-practices-performance](references/best-practices-performance.md) |

## Advanced

| Topic | Description | Reference |
|-------|-------------|-----------|
| Limitations | npm lockfile ignored, binstubs are shell scripts | [advanced-limitations](references/advanced-limitations.md) |
