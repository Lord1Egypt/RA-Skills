# Release Notes: wip-ai-devops-toolbox v1.9.55

Force redeploy: .worktrees guard fix.

## The story

v1.9.53 had the guard fix but deploy-public was missed. v1.9.54 force-redeployed but installer had already cached v1.9.54. This version ensures the public repo and npm are in sync so ldm install deploys the correct guard.mjs with .worktrees convention.

## Issues closed

- #240 (partial)
