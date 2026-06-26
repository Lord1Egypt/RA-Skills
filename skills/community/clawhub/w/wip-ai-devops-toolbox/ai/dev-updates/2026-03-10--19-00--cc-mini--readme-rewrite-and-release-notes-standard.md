# Dev Update: README Rewrite + Release Notes Standard

**Date:** 2026-03-10 19:00 PST
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private
**PRs:** #46, #47, #48, #49, #50
**Branch:** cc-mini/readme-polish-and-mcp-examples
**Plan:** ai/plan/archive/2026-03-10--cc-mini--readme-polish-and-mcp-examples.md (7 phases, all complete)

## What happened

Second session of the day. Took external feedback from Grok and GPT, turned it into a 7-phase plan, built all of it, then went beyond the plan to add a release notes standard to the tooling. Parker reviewed everything on the branch in real time.

### README rewrite (human-first)

Parker's direction: the README is for humans, not developers. No install commands, no MCP tool mappings, no Quick Start sections. Those are developer-brain content.

- Removed Quick Start section (moved to TECHNICAL.md)
- Removed "Talk to Your Tools" MCP examples section (moved to SKILL.md)
- Added Karpathy quote with both paragraphs. "Andrej Karpathy put it clearly:" intro, Source link outside blockquote, italic response line
- Added Interface Coverage matrix (all 10 tools x 6 interfaces)
- Added "Can I use this?" plain-English license examples
- Added "More Info" section linking to TECHNICAL.md, Universal Interface Spec, Dev Guide
- Release Pipeline feature description updated to include release notes review

### Dual MIT+AGPLv3 licensing (enforcement)

Previous session created the license format. This session enforced it.

- PR #46: license section format standardized (code block, AGPLv3, "Commercial licenses available")
- PR #47: all 10 sub-tool LICENSE files updated to dual format
- PR #48: wip-license-guard built to enforce it going forward
- wip-license-guard checks README structure too: catches developer-brain content that belongs in TECHNICAL.md

### SKILL.md v1.5.1

- Interface Coverage matrix added (same as README)
- "Talk to Your Tools" MCP examples added
- Version bumped from v1.4.0 to v1.5.1
- Tool names fixed, descriptions updated
- SKILL.md staleness warning added to wip-release

### Release notes standard (new)

Parker called the v1.5.2 release notes "bullshit" because they were just commit lists. Built three things:

1. **Quality warnings in wip-release.** Warns when --notes is missing, too short (<50 chars), or looks like a changelog entry.
2. **Versioned release notes file.** `RELEASE-NOTES-v1-6-0.md` lives on the branch. You review it in the PR. wip-release auto-detects the file based on the target version. One file, renamed each release.
3. **Narrative structure.** Commits fold into a collapsible `<details>` section. The narrative is the headline.

Release notes for this release written in the memory-crystal + OpenClaw style: per-PR narrative sections with problem/solution/files changed/commits.

### Feedback processing

External feedback documented and analyzed:
- `ai/notes/2026-03-10--grok-feedback--readme-and-licensing.md`
- `ai/notes/2026-03-10--gpt-feedback--product-and-adoption.md`
- `ai/notes/2026-03-10--cc-mini--readme-standard-and-universal-installer-vision.md`

Actionable items turned into the 7-phase plan. Deferred items documented: evidence screenshots, recommended adoption order, CI badges, COMMERCIAL-LICENSE.md.

## Files changed

- `README.md` ... full rewrite (multiple commits)
- `TECHNICAL.md` ... Quick Start moved here, release notes convention documented
- `SKILL.md` ... v1.5.1 with matrix and MCP examples
- `tools/wip-release/core.mjs` ... narrative release notes, quality warnings, collapsible commits
- `tools/wip-release/cli.js` ... --notes-file flag, versioned file auto-detection, updated help
- `tools/wip-license-guard/cli.mjs` ... README structure standard checks added
- `RELEASE-NOTES-v1-6-0.md` (NEW) ... full narrative release notes for v1.6.0
- `ai/notes/` ... Grok feedback, GPT feedback files
- `ai/plan/current/` ... 7-phase plan (all DONE, ready to archive)

## Status

- PR #50 is open with all changes, ready for final review
- PRs #46-49 already merged to main
- Plan complete. All 7 phases done plus release notes standard (bonus)
- Ready to merge, deploy to public, and release v1.6.0

## Open items

- Merge PR #50
- Deploy to public repo via deploy-public.sh
- Release v1.6.0 with `wip-release minor --notes-file=RELEASE-NOTES-v1-6-0.md`
- Rename merged branches with --merged-YYYY-MM-DD
- Update .github org profile README with new repo name (carried from previous session)
- Rewrite v1.5.0/1/2 release notes with narrative (deferred)
