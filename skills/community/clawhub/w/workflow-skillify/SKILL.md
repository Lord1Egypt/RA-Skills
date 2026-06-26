---
name: "workflow_skillify"
description: "Use when a successful session or repeatable process should be captured as a reusable skill with steps, arguments, and invocation guidance."
---


# Workflow Skillify

Use this skill at the end of a repeatable process to capture it as a standalone skill.

## Workflow
1. Summarize the session and extract user-visible goals, corrections, and constraints.
2. Identify inputs, outputs, artifacts, and success criteria.
3. Interview for missing details only where the workflow is ambiguous.
4. Write a clean `SKILL.md` with trigger conditions, steps, and optional arguments.
5. Save the skill in the appropriate repo-level or personal location.

## Guardrails
- Capture the user's corrections, not just the first draft of the process.
- Keep the resulting skill concrete and execution-oriented.
- Do not over-question simple workflows.

## Example Requests
- Turn this successful session into a reusable skill.
- Capture the process we just followed as a formal skill.

## Inputs
- Session history
- User corrections
- Desired save scope

## Outputs
- Reusable SKILL.md
- Trigger and argument guidance

## Success Criteria
- The resulting skill captures the real workflow.
- User corrections are preserved as rules.
- The saved skill is specific and reusable.

## Non-Goals
- Over-interviewing simple workflows
- Saving a vague process with no triggers or success criteria

## Source Provenance
Derived from `src/skills/bundled/skillify.ts`.
