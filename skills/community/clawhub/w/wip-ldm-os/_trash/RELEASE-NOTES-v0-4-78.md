# wip-ldm-os v0.4.78

## Dev-guide: Branch Guard runtime enforcement section

Docs-only release. The shared `dev-guide-wipcomputerinc.md.tmpl` gains a new "Branch Guard: Runtime Enforcement" section covering:

- Layer 1 (write gate) with shared-state allowlist
- Layer 2 (destructive-command block)
- Layer 3 (session-level gates: onboarding, blocked-file tracking, external-PR create)
- Override env vars table
- Expected first-write ritual
- Bypass audit trail

Agents (cc-mini, Lēsa) read the deployed copy at `~/.ldm/library/documentation/dev-guide-wipcomputerinc.md` during boot. Without this release the new rules from today's `wip-branch-guard 1.9.77–1.9.80` aren't documented where agents look.

Complements `tools/wip-branch-guard/SKILL.md` (shipped in wip-branch-guard; that's the in-session reference when the hook fires).

## Files

- `shared/docs/dev-guide-wipcomputerinc.md.tmpl`: +57 insertions (one new section between "Branch Protection Audit" and "Worktree Workflow").

## Rollout

After merge: `wip-release patch` bumps to 0.4.78 and publishes `@wipcomputer/wip-ldm-os`. `ldm install` redeploys the shared templates, picking up the new section.

## Related

- PR #628 (dev-guide section add)
- `wip-ai-devops-toolbox-private` PR #362 (SKILL.md for wip-branch-guard ... deploys via the guard extension itself, already live)
- `wip-branch-guard v1.9.80` (the enforcement the docs describe)
