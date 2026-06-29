# skill-build-wizard

> End-to-end guided workflow for building production-quality agent skills.
> 4 stages (pre-flight → spec confirmation → coding acceptance → release prep),
> sequenced so nothing important gets skipped.

Part of the [`build-better-skills`](https://github.com/Songhonglei/build-better-skills) suite — see [Stages](https://github.com/Songhonglei/build-better-skills#stages) for the full lifecycle map.

## What it does

Unlike `skill-creator` (a technical reference written **for AI**), this wizard
is written **for the user**. It walks you through the 4 stages of building a
skill and pauses for confirmation at each handoff:

| Stage | What you do |
|---|---|
| **1. Pre-flight** | Verify workspace git, long-task tolerance, session continuity (skippable) |
| **2. Spec clarification** | Three musts: use `skill-creator` / design before code / no local deps |
| **3. Coding acceptance** | Four checks: design alignment / edge cases / 2× code review / 2× smoke test |
| **4. Release prep** | Five requirements: regression → glic-check → release-audit → cross-env → release-plus |

Stages 2-4 each have a detailed checklist in `references/` that gets loaded
on demand.

## Quick start

```bash
# Install
clawhub install skill-build-wizard

# Or clone directly
git clone https://github.com/Songhonglei/build-better-skills.git
# (this skill lives under skills/skill-build-wizard/)
```

Then ask your agent: *"Use skill-build-wizard to help me build a skill."*

## Install in your AI agent

| Agent | Install |
|---|---|
| Any clawhub user | `clawhub install skill-build-wizard` |
| OpenClaw | `clawhub install skill-build-wizard` |
| Claude Code | Copy to `~/.claude/skills/` |
| Cursor | Copy to `.cursor/skills/` |

## Companion skills

This wizard delegates to other skills at specific stages. They're all in the
same suite:

- [`skill-creator`](https://github.com/anthropics/skills) — scaffolds the skill (Stage 2)
- [`skill-regression`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-regression) — Stage 4 Step 1
- [`glic-check`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/glic-check) — Stage 4 Step 2
- [`skill-release-audit`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-audit) — Stage 4 Step 3
- [`skill-release-plus`](https://github.com/Songhonglei/build-better-skills/tree/main/skills/skill-release-plus) — Stage 4 Step 5

## License

MIT — see [LICENSE](./LICENSE)

## Author

Evan Song · [github.com/Songhonglei](https://github.com/Songhonglei)

## Changelog

### v1.0.0 (2026-06-22)

- Initial open-source release
- Forked from internal `skill-creator-plus`, removed internal-only dependencies
- Stage 1 simplified: 1 automated check (git) + 2 platform-agnostic recommendations
- Stage 4 reordered: regression → **glic-check** (replaces internal `skill-healthcheck`) → release-audit → cross-env → release-plus
