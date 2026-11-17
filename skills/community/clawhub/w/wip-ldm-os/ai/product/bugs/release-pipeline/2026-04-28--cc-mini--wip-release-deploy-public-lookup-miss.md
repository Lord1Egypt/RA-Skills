# wip-release: deploy-public lookup miss leaves stable releases needing a manual second step

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Active master plan:** [2026-04-24--codex--canary-release-pipeline-master-plan.md](2026-04-24--codex--canary-release-pipeline-master-plan.md) ... start here; this ticket should land under that map.
**Historical context:** [2026-04-08--cc-mini--silent-skip-without-license-guard-config.md](2026-04-08--cc-mini--silent-skip-without-license-guard-config.md), [2026-04-17--cc-mini--release-pipeline-hardening-and-ci.md](2026-04-17--cc-mini--release-pipeline-hardening-and-ci.md) (both superseded by the canary plan above; kept for context, not for current direction).

## What

`wip-release` (stable track, `-private` repo) is supposed to run `deploy-public.sh` automatically per its own `--no-deploy-public` opt-out flag. In practice the auto-run silently skips with:

```
- deploy-public: skipped (no tools/deploy-public/deploy-public.sh)
```

The lookup is hard-coded to a path inside the *current* repo (`tools/deploy-public/deploy-public.sh`), which only exists in the `wip-ai-devops-toolbox-private` worktree. Every other `-private` repo that needs to sync (memory-crystal-private, dream-weaver-protocol-private, wip-ldm-os-private, etc.) has no such in-tree script and quietly skips public sync.

## Symptom seen today

Released `wip-ldm-os-private v0.4.84` via `wip-release patch`. wip-release reported `1 of 4 target(s) failed` and the deploy-public step printed the silent-skip line above. Public mirror `wipcomputer/wip-ldm-os` was therefore stale by ~10 versions (last public release was v0.4.74). Recovered by running `deploy-public` standalone:

```bash
deploy-public /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private wipcomputer/wip-ldm-os
```

That cleanly synced via PR `#273`, created the public release `v0.4.84`, and published `@wipcomputer/wip-ldm-os@0.4.84` to npm. So the *script* works; only wip-release's *invocation path* is broken.

## Why this matters

- Stable releases of every `-private` repo besides the toolbox itself silently lag the public mirror.
- The "1 of 4 target(s) failed" line is buried in wip-release output and easy to miss.
- The release feels successful (npm publishes, GH release created) but public consumers see stale code/docs until someone notices and runs `deploy-public` manually.
- `wip-release`'s own contract (`runs by default for -private repos`) is broken in the common case.

## Proposed fix

Three options, listed in increasing order of robustness:

**A. Fall back to the homebrew-installed `deploy-public` on PATH.** If `tools/deploy-public/deploy-public.sh` is not found, look for `deploy-public` on `$PATH` and invoke it with `<private-repo-path> <derived-public-repo>`. The public repo can be derived by stripping `-private` from the repo name (matches the deploy-public convention).

**B. Make the in-tree path optional and document an alternate hook in `package.json`.** A new `wip.deployPublic` field could declare the public counterpart and the script to run.

**C. Extract `deploy-public` from the toolbox into its own published package** (`@wipcomputer/deploy-public`) that wip-release shells out to via `npx` or a peer-installed bin. This is what the homebrew-installed version effectively does already.

**Recommendation:** A as the immediate fix (one if-else in the wip-release deploy-public dispatcher; preserves backward compat with the in-tree script). C as the longer-term design once the publish-pipeline ticket from the universal-installer master plan settles.

## Acceptance

- Stable `wip-release` of any `-private` repo (without an in-tree `tools/deploy-public/deploy-public.sh`) automatically syncs to its public counterpart, no manual second command required.
- The "1 of 4 target(s) failed" line is replaced with either a successful sync or a loud error (not a silent skip).
- A test fixture under wip-release covers the fallback path.

## Context

- Discovered while shipping `wip-ldm-os-private v0.4.84` (universal-installer doc alignment) on 2026-04-28.
- Today's manual recovery: `deploy-public /Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private wipcomputer/wip-ldm-os` → public PR `#273` → release `v0.4.84` published.
