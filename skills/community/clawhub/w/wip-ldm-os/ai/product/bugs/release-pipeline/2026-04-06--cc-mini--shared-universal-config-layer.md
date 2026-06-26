# Shared must be the universal config + rules layer

**Date:** 2026-04-06
**Filed by:** cc-mini (with Parker)
**Priority:** high
**Repo:** wip-ldm-os-private (installer + shared/)
**Status:** design captured, implementation not started

## Superseded / Consolidated By

This plan is consolidated into `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`, especially Phase 9: Shared Rules, Docs, and Universal Config.

Keep this file for historical context and design detail. Use the 2026-04-24 canary release pipeline master plan as the current implementation map.

## Problem

Rules and config are scattered across three harness-specific locations:

```
~/.claude/CLAUDE.md          CC-only (global instructions)
~/.claude/rules/*.md         CC-only (per-topic rules)
~/wipcomputerinc/CLAUDE.md   CC-only (workspace instructions)
~/.openclaw/workspace/TOOLS.md   Lēsa-only (her rules)
~/.ldm/config.json           LDM OS (system config, not rules)
~/.ldm/shared/docs/          LDM OS (deployed docs, but not rules)
```

When a new harness plugs in (Hermes, Codex, a future agent), it has no idea where to read the rules. Each harness has its own location. There's no universal "here's how we work" that every agent reads from the same place.

## What shared SHOULD be

`~/.ldm/shared/` is the universal location. One set of rules, config, and conventions. Every agent reads from here regardless of harness.

Source of truth: `shared/` in the wip-ldm-os-private repo.
Deploy path: `ldm install` copies to `~/.ldm/shared/`.
Harness adapters: thin wiring that points each harness at `~/.ldm/shared/`.

```
~/.ldm/shared/
  rules/                    universal rules (how we work, writing style, git conventions)
  docs/                     universal docs (system directories, release pipeline, etc.)
  config.json               system config (already exists at ~/.ldm/config.json)
```

When Hermes plugs in, it reads `~/.ldm/shared/rules/` and knows:
- How we work (worktrees, PRs, branches, releases)
- Who the agents are
- What the writing style is
- How to talk to other agents (Bridge)
- Where memory lives (Crystal)

## What ldm install needs to do

Currently `ldm install` deploys:
- `shared/docs/*.tmpl` to `~/wipcomputerinc/library/documentation/` (Parker's docs) AND `~/.ldm/shared/docs/` (was `settings/docs/`)
- `shared/rules/` to `~/.claude/rules/` (CC-specific)
- `shared/boot/` to `~/.ldm/shared/boot/` (hooks)
- `shared/templates/` to `~/.ldm/templates/`

What it SHOULD do:
- Deploy `shared/rules/` to `~/.ldm/shared/rules/` (universal) as the canonical location
- CC adapter: symlink or copy `~/.ldm/shared/rules/` to `~/.claude/rules/` (so CC reads them)
- Lēsa adapter: reference `~/.ldm/shared/rules/` from `workspace/TOOLS.md` (or symlink)
- Hermes/Codex/future: read directly from `~/.ldm/shared/rules/`

One source. Deployed once. Each harness reads from the same universal location via its own adapter.

## What goes in shared/rules/

Universal rules that apply to ALL agents, not just CC:

- **how-we-work.md:** worktrees for work, main for viewing, alpha for dogfooding, release for public. The full workflow.
- **git-conventions.md:** never commit to main, never squash, co-authors on every commit, branch prefixes
- **writing-style.md:** no em dashes, PST timezone, full paths in docs
- **release-pipeline.md:** merge, deploy, install. Three steps, never combined.
- **security.md:** secret management, audit before installing, shared file protection
- **workspace-boundaries.md:** each agent owns its own folder, repos are shared

These already exist as CC-specific rules at `shared/rules/` in the repo. They're deployed to `~/.claude/rules/` by `ldm install`. Making them universal means deploying to `~/.ldm/shared/rules/` AND keeping the CC adapter that copies to `~/.claude/rules/`.

## The "how we work" rules (new, not yet written)

Parker described the full workflow mental model that needs to be captured:

```
worktrees (where CC works)
    ↓ PR + merge
main private (what Parker sees, saved upstream on GitHub)
    ↓ wip-release alpha
alpha (dogfood, ldm install --alpha)
    ↓ wip-release patch/minor
public main (deploy-public.sh)
    ↓ ldm install
release (what users get)
```

Key rules:
- Worktrees are where agents work. Main is read-only for agents.
- Parker looks at main. Not worktrees.
- After merging a PR, ALWAYS pull main so Parker can see it.
- Alpha is for dogfooding. Install with `ldm install --alpha`.
- Public is for users. Deploy with `deploy-public.sh` after stable release.
- If alpha works but public breaks, investigate before releasing.
- Every merge to private main is saved upstream on GitHub.
- If the computer goes away, GitHub has a copy. Start back up from there.

## Concern: alpha to public gap

Parker raised a concern: "We have so many alphas. Once we go from main to public, I hope it doesn't break everything."

The risk: alpha.24 has been dogfooded and works. But the last public release is 1.9.70 (toolbox) / 0.4.72 (LDM OS). That's 24 alpha versions of accumulated changes. A stable release that pulls all 24 in at once could break things a clean alpha-by-alpha progression wouldn't catch.

Mitigation options:
1. **Release a stable now** to close the gap while it's still manageable
2. **Test the public install path** from a clean machine before releasing
3. **Ship stable more often** so the alpha-to-stable gap stays small

## Harness pluggability

The reason this matters beyond CC and Lēsa:

- **Hermes** (Nous Research, MCP-native, MIT): to be installed and tested. Needs to read the same rules.
- **Codex** (OpenAI): if added, needs the same conventions.
- **Future harnesses:** anyone building on LDM OS reads `~/.ldm/shared/` and gets the full picture.

Shared is the operating system's config layer. Like `/etc/` on Unix. Every program reads it. Each program has its own config too, but the system-wide rules live in one place.

## Implementation scope

1. Add `how-we-work.md` to `shared/rules/` in the repo (the workflow mental model)
2. Update `ldm install` to deploy `shared/rules/` to `~/.ldm/shared/rules/` (universal) in addition to `~/.claude/rules/` (CC adapter)
3. Update Lēsa's workspace to reference `~/.ldm/shared/rules/` (or symlink)
4. Document the pattern for future harnesses: "read rules from ~/.ldm/shared/rules/"

## Cross-references

- `ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md` (device pairing stores token at `~/.ldm/auth/`, same universal layer)
- `ai/product/bugs/release-pipeline/2026-04-05--cc-mini--release-pipeline-master-plan.md` (installer fixes)
- `ai/product/bugs/installer/2026-04-03--cc-mini--installer-recreates-renamed-folders.md` (deploy paths already being cleaned up)
- `library/documentation/system-directories.md` (Parker's doc on what lives where)
