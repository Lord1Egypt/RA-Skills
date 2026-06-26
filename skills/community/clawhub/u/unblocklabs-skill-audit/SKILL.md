---
name: skill-audit
description: Audit all installed skills for quality, duplicates, structural issues, and best-practice compliance. Use when asked to review, audit, lint, or check skills for problems. Triggers on "audit skills", "skill quality", "check my skills", "skill duplicates", "skill hygiene".
compatibility:
  - openclaw
---

# skill-audit

Scans all skill locations (global, workspace, project) and produces a structured audit report.

## What It Checks

### Structural Quality (per skill)
1. **Description quality** — Is the `description` field trigger-oriented (tells the model *when* to use it) vs a vague summary?
2. **Gotchas section** — Does the SKILL.md include a Gotchas/Pitfalls/Common Issues section? (Highest-signal content per Anthropic)
3. **Progressive disclosure** — Does the skill use subdirectories (scripts/, references/, assets/, examples/) or is it a flat SKILL.md?
4. **File structure** — Are there scripts, templates, or reference files the agent can discover?
5. **YAML frontmatter** — Does it have `name`, `description`, and optionally `compatibility`?
6. **Category fit** — Does it map cleanly to one of the 9 skill categories (Library/API, Verification, Data, Automation, Scaffolding, Code Quality, CI/CD, Runbooks, Infrastructure)?

### Cross-Skill Issues
7. **Duplicates** — Same skill name or overlapping functionality across global/workspace/project dirs
8. **Orphan files** — Stale `.skill` files, empty dirs, leftover copies
9. **Category gaps** — Which of the 9 categories have no skills at all?
10. **Stale skills** — Skills that reference missing tools, dead paths, or deprecated APIs

## How to Run

Tell the agent: "audit my skills" or "run skill-audit"

The agent will:
1. Run `scripts/audit.sh` to scan all skill locations and collect metadata
2. Score each skill (0-10) based on the checks above
3. Produce a summary report with:
   - Per-skill scorecard
   - Top issues to fix (sorted by impact)
   - Category coverage map
   - Duplicate/orphan findings

## Output

Results are written to `.sub-agent-results/skill-audit-report.md` and summarized in chat.

## Scoring

| Points | Criteria |
|--------|----------|
| +2 | Has YAML frontmatter with name + description |
| +2 | Description is trigger-oriented (contains "use when", "trigger", action verbs) |
| +2 | Has a Gotchas/Pitfalls/Common Issues section |
| +2 | Uses progressive disclosure (has subdirs with scripts/references/assets) |
| +1 | Has at least one script or executable file |
| +1 | SKILL.md is between 200-5000 chars (not too sparse, not bloated) |

Scores: 8-10 = Good, 5-7 = Needs work, 0-4 = Poor

## References

- [Anthropic: Lessons from Building Claude Code Skills](https://x.com/trq212/status/2033949937936085378) — Thariq's 9 categories, gotchas sections, progressive disclosure
- [Ole Lehmann: Auto-improve Skills](https://x.com/itsolelehmann/status/2033919415771713715) — Autoresearch loop (future enhance mode)
