# Release Notes: wip-ai-devops-toolbox v1.9.54

Force redeploy: guard files were stale after v1.9.53.

## The story

v1.9.53 published the .worktrees guard fix to npm but ldm install saw the version as current and skipped redeploying the files. The deployed guard.mjs was still the old version. This release forces a version bump so the installer re-deploys.

This is a bug in the installer: it checks version numbers but not file contents. Filed for future fix.

## Issues closed

- #240 (partial: .worktrees convention)
