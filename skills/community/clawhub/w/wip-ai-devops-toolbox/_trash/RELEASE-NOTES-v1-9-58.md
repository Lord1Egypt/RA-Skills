# Release Notes: wip-ai-devops-toolbox v1.9.58

**Fix deploy-public.sh losing release notes when invoked with relative path.**

## The story

When deploy-public.sh was called with `.` as the private repo path (e.g. `bash scripts/deploy-public.sh . wipcomputer/repo`), the script later cd'd into a temp directory. After that, `cd "."` no longer pointed to the private repo, so `gh release view` failed silently and release notes fell back to the empty "Release vX.Y.Z" default. This has been broken since at least v1.9.51.

Fix: resolve PRIVATE_REPO to an absolute path at startup before any cd happens.

## Issues closed

- #228 (continued from v1.9.57)

## How to verify

```bash
# From a repo directory, run with "." and check public release has real notes:
cd /path/to/private-repo
bash scripts/deploy-public.sh . wipcomputer/public-repo --dry-run
```
