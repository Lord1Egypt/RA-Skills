# SkillFeed

Turn failures and "I don't know what to use" moments into clear, ranked skill recommendations.

## What it does

SkillFeed watches task context (goal + error/failure signal), builds targeted ClawHub queries, ranks candidate skills, and returns an actionable recovery plan.

- Detects common failure signals (API errors, timeout, retries, missing output)
- Generates layered search queries (broad → scenario → failure-specific)
- Recommends:
  - 1 primary skill
  - 2 alternatives
  - immediate next steps
  - fallback path
- Adapts response style for Claude Code / ChatGPT / Gemini

## Typical use cases

- "Tweet publish failed, what should I use now?"
- "I need this automated but don't have time. Recommend a skill stack."
- "This workflow keeps timing out. Give me better options."

## Output shape

- Goal
- Failure signal
- Primary recommendation
- Alternatives
- Immediate actions (3–5)
- Success checks
- Fallback
- Provider runbook (Claude Code / ChatGPT / Gemini)

## Project structure

- `SKILL.md` – trigger rules + core workflow
- `references/discovery-workflow.md` – ranking and search strategy
- `references/query-templates.md` – query templates by scenario
- `references/provider-adaptation.md` – provider-specific output style

## Install

```bash
clawhub install skill-feed
```

## Notes

This project optimizes for practical recommendations (what to do next), not just listing possible skills.
