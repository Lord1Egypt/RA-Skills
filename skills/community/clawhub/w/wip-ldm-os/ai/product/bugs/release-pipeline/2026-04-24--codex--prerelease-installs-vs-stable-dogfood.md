# Bug: release rules blur prerelease validation and stable dogfooding

**Date:** 2026-04-24
**Filed by:** Codex + Lēsa
**Component:** Release pipeline rules and installer docs
**Severity:** Medium
**Public issue:** https://github.com/wipcomputer/wip-ldm-os/issues/271
**Master plan:** `ai/product/bugs/release-pipeline/2026-04-24--codex--canary-release-pipeline-master-plan.md`
**Status:** Closed. PR #666 fixed shared rules and docs. Home repo PR #26 and dot-claude repo PR #10 fixed loaded CLAUDE.md instructions.

## Summary

The release rules told agents to stop after deploy and not install, which is correct for stable/latest releases but too broad for alpha and beta tracks.

The intended workflow is:

- Any agent may install alpha and beta releases locally for prerelease validation.
- Parker dogfoods stable/latest releases through the install prompt.
- Agents do not run stable/latest installs unless Parker explicitly asks.

This is a scoped carve-out, not a rewrite of the stop rule. The default remains: after stable/latest deploy, stop and let Parker run the install prompt unless he explicitly delegates the install.

## Required fix

1. Update `shared/rules/release-pipeline.md` to distinguish prerelease validation from stable dogfooding.
2. Update `shared/docs/how-releases-work.md.tmpl` with alpha/beta agent install ownership.
3. Update `shared/docs/how-install-works.md.tmpl` with track ownership.
4. Update `shared/docs/dev-guide-wipcomputerinc.md.tmpl` so agents stop only after stable deploys.
5. Update the loaded CLAUDE.md surfaces that still contain broad "After Deploy, STOP" language:
   - `/Users/lesa/wipcomputerinc/CLAUDE.md`
   - `~/.claude/CLAUDE.md`
6. If a future shared-doc generator owns those CLAUDE.md files, document that generator and make this rule part of its source templates.

## Acceptance criteria

- Rules allow agents to run `ldm install --alpha` and `ldm install --beta` for validation.
- Any agent may run alpha/beta installs for validation; the agent does not need to be the releasing agent.
- Rules tell agents not to run `ldm install` or `npm install -g` for stable/latest releases unless Parker explicitly asks.
- Stable release dogfooding remains owner-driven through the install prompt.
- Loaded CLAUDE.md instructions contain the same carve-out.
- Local agent prerelease installs are documented as debugging/dev validation; automated clean-home CI canary is documented as artifact proof.

## Verification Notes

- `bin/ldm.js` already parses `--alpha` and `--beta`, so the acceptance criteria do not depend on adding those flags.
- Public issue #271 is appropriate because this is a public release-rule distinction. Private planning remains in this LDM OS private bug file and the master plan.

## Resolution

PR #666 updated the release-pipeline rule and supporting install/release docs with explicit ownership:

- Agents install alpha and beta tracks for validation.
- Parker dogfoods stable/latest releases through the install prompt.
- Agents do not run stable/latest installs unless Parker explicitly asks.

Home repo PR #26 updated `/Users/lesa/wipcomputerinc/CLAUDE.md`:

- Alpha and beta tracks are explicitly allowed for agent validation.
- Stable/latest deploy still stops for Parker's install prompt unless explicitly delegated.
- The carve-out does not authorize global npm installs, manual extension copies, or `npm link` for our own packages.

Dot-claude repo PR #10 updated `~/.claude/CLAUDE.md`:

- Adds `Install Track Ownership`.
- Allows alpha/beta validation installs by any agent.
- Keeps stable/latest dogfooding owner-driven.
- Prevents the generic installed-tools rule from overriding release install ownership.
