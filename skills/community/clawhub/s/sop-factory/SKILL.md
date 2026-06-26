---
name: sop-factory
description: Turn rough workflows into standard operating procedures with roles, inputs,
  outputs, checkpoints, and exception handling.
version: 1.1.0
metadata:
  openclaw:
    requires:
      bins:
      - python3
    emoji: 🧰
---

# SOP Factory

## Purpose

Turn rough workflows into standard operating procedures with roles, inputs, outputs, checkpoints, and exception handling.

## Trigger phrases

- 做 SOP
- turn this workflow into an SOP
- 流程文档化
- 标准作业流程
- 交接文档

## Ask for these inputs

- rough workflow
- roles
- tools used
- quality bar
- exception cases

## Workflow

1. Break the workflow into trigger, preparation, execution, QC, handoff, and exception sections.
2. Use the SOP template resource to ensure consistency.
3. Add checkpoints, examples, and escalation rules.
4. Return both a quick-start SOP and a formal version.
5. Highlight where screenshots or forms should be attached.

## Output contract

- SOP draft
- quick-start version
- roles matrix
- exceptions appendix

## Files in this skill

- Script: `{baseDir}/scripts/sop_outline_builder.py`
- Resource: `{baseDir}/resources/sop_template.md`

## Operating rules

- Be concrete and action-oriented.
- Prefer preview / draft / simulation mode before destructive changes.
- If information is missing, ask only for the minimum needed to proceed.
- Never fabricate metrics, legal certainty, receipts, credentials, or evidence.
- Keep assumptions explicit.

## Suggested prompts

- 做 SOP
- turn this workflow into an SOP
- 流程文档化

## Use of script and resources

Use the bundled script when it helps the user produce a structured file, manifest, CSV, or first-pass draft.
Use the resource file as the default schema, checklist, or preset when the user does not provide one.

## Boundaries

- This skill supports planning, structuring, and first-pass artifacts.
- It should not claim that files were modified, messages were sent, or legal/financial decisions were finalized unless the user actually performed those actions.


## Compatibility notes

- Directory-based AgentSkills/OpenClaw skill.
- Runtime dependency declared through `metadata.openclaw.requires`.
- Helper script is local and auditable: `scripts/sop_outline_builder.py`.
- Bundled resource is local and referenced by the instructions: `resources/sop_template.md`.
