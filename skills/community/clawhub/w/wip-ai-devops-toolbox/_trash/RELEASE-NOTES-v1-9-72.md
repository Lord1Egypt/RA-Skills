# AI DevOps Toolbox v1.9.72

## Promote v1.9.71-alpha series to stable

Closes #256.

Consolidates 21 alpha prereleases (`v1.9.71-alpha.1` through `v1.9.71-alpha.21`) into a stable v1.9.72 release. No code changes beyond the version bump in the toolbox root `package.json`; the sub-tool code has been stable and dogfooded across the alpha iterations.

## Why

The root `package.json` had been sitting at `1.9.71-alpha.21` without a stable promotion. That blocked `deploy-public.sh` from syncing the private repo to the public mirror ... the script gates public release on stable root versions.

Symptom during 2026-04-21: wip-branch-guard sub-tool shipped stable (v1.9.82 → v1.9.83 → v1.9.84) to npm successfully, but the public `wipcomputer/wip-ai-devops-toolbox` GitHub releases page did not show any of them because `deploy-public.sh` refused to run with an alpha root.

## What's in the diff

- `package.json`
  - Version bump `1.9.71-alpha.21` → `1.9.72`

Everything else flows from `wip-release`:

- CHANGELOG.md updated
- Git tag `v1.9.72`
- GitHub release on private repo
- npm publish to `@latest`
- `deploy-public.sh` runs, syncs private code (minus `ai/`) to `wipcomputer/wip-ai-devops-toolbox`
- Public GitHub release created

## Sub-tool versions at this release

| Sub-tool | npm version |
|---|---|
| `@wipcomputer/wip-branch-guard` | 1.9.84 |
| Other sub-tools | See their individual `package.json` |

The sub-tool releases have their own cadence; this release is purely the toolbox root bump.

## Co-authors

Parker Todd Brooks, Lēsa (oc-lesa-mini, Opus 4.7), Claude Code (cc-mini, Opus 4.7).
