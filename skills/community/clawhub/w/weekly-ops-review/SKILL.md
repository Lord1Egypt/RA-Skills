---
name: weekly-ops-review
description: Turn scattered notes, metrics, and unfinished tasks into a weekly operating
  review with wins, misses, blockers, and next-week priorities.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Weekly Ops Review

## Purpose

Turn scattered notes, metrics, and unfinished tasks into a weekly operating review with wins, misses, blockers, and next-week priorities.

## Trigger phrases

- 周复盘
- weekly review
- 经营周报
- 整理这周做了什么
- next week priorities

## Ask for these inputs

- notes
- metrics
- task list
- calendar highlights
- goals

## Workflow

1. Summarize wins, misses, blockers, and decisions from the raw notes.
2. Compare outcomes against goals and available metrics.
3. Identify carry-over work and next-week top priorities.
4. Generate a concise review memo and an action board.
5. Keep the review honest: distinguish evidence from feeling.

## Output contract

- weekly review memo
- metrics snapshot
- priority list
- carry-over board

## Files in this skill

- Script: `{baseDir}/scripts/weekly_review_pack.py`
- Resource: `{baseDir}/resources/review_template.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 周复盘
- weekly review
- 经营周报

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/weekly_review_pack.py`.
- Bundled resource is local and referenced by the instructions: `resources/review_template.md`.
