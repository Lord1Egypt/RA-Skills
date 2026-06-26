# Release Notes: wip-ldm-os v0.4.39

Fixes #191, #193, #197

## Shared Rules + Prompts Deployment

`ldm install` now deploys shared rules and prompts to both harnesses:

- `~/.ldm/shared/rules/` ... 5 rule files (git conventions, release pipeline, security, workspace boundaries, writing style)
- `~/.ldm/shared/prompts/` ... 6 prompt files (daily/weekly/monthly/quarterly agent summaries, org combine, dev summary)
- `~/.claude/rules/` ... rules deployed to Claude Code
- `~/.openclaw/workspace/DEV-RULES.md` ... rules deployed to OpenClaw (combined into one file)

Both agents get the same dev conventions. Lesa was missing these entirely.

## Total Recall Docs + Scripts

- `docs/total-recall/README.md` + `TECHNICAL.md` ... Total Recall as an LDM OS component (like Bridge)
- `docs/recall/TECHNICAL.md` ... updated with Total Recall cross-reference
- `scripts/ldm-summary.sh` ... per-agent crystal search, reads prompts from files, Opus for org combine
- `scripts/backfill-summaries.sh` ... loops dailies, weeklies, monthlies, quarterly

## Agent Memory Dir Scaffolding

`ldm init` now scaffolds per-agent memory dirs and workspace output dirs:
- `~/.ldm/agents/{agentId}/memory/daily/journals/sessions/transcripts/`
- `~/wipcomputerinc/team/{agent}/journals/` and `automated/memory/summaries/{cadence}/`
- `~/wipcomputerinc/operations/updates/{team,dev}/{cadence}/`

## Crystal --until Flag (MC side)

Memory Crystal now supports date range queries: `crystal search --since 2026-02-10 --until 2026-02-11`. Required for backfill.
