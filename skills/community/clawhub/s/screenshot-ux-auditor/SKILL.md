---
name: screenshot-ux-auditor
description: Turn app screenshots into structured UX, copywriting, and conversion
  audits with issue severity and recommended fixes.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# Screenshot UX Auditor

## Purpose

Turn app screenshots into structured UX, copywriting, and conversion audits with issue severity and recommended fixes.

## Trigger phrases

- 审查这个界面
- 截图做 UX 评审
- audit this UI screenshot
- 页面哪里有问题
- 帮我做可用性检查

## Ask for these inputs

- one or more screenshots
- product goal or funnel stage
- target user
- platform web/mobile/desktop
- tone or benchmark

## Workflow

1. Identify the screen type, primary task, and likely user goal.
2. Evaluate using the bundled heuristics checklist.
3. Cluster issues into clarity, hierarchy, trust, interaction, and accessibility.
4. Assign severity and provide fix-first recommendations.
5. Generate an issue log the user can hand to design or engineering.

## Output contract

- audit summary
- issue log CSV/Markdown
- fix priority list
- before/after prompt suggestions

## Files in this skill

- Script: `{baseDir}/scripts/generate_issue_log.py`
- Resource: `{baseDir}/resources/heuristics-checklist.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 审查这个界面
- 截图做 UX 评审
- audit this UI screenshot

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/generate_issue_log.py`.
- Bundled resource is local and referenced by the instructions: `resources/heuristics-checklist.md`.
