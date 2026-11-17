---
name: sop-instantiation
description: Use when turning a broad objective into a concrete standard operating procedure with milestones, owners, artifacts, and checks.
version: 0.1.0
status: preview
language: en
type: decompression
models:
  - Claude
  - Codex
---

# SOP Instantiation Skill

## When To Use

Use this skill when the user has a goal but not an execution path. The skill turns strategic intent into a standard operating procedure that can be followed, audited, and improved.

Good fit:

- Planning a launch, hiring process, research workflow, content pipeline, or operational routine.
- Turning a broad instruction into staged work.
- Converting personal working habits into a repeatable playbook.

## Inputs

Collect:

- Goal and deadline.
- Available people, tools, and data.
- Required deliverables.
- Quality standards and failure conditions.
- Known constraints and dependencies.

## Workflow

1. Identify the objective and define what finished means.
2. Split the goal into phases.
3. For each phase, define inputs, actions, outputs, owner, and acceptance checks.
4. Add decision points where the workflow may branch.
5. Add risk controls and recovery steps.
6. Convert the procedure into a checklist or calendar-ready plan.
7. Include a review loop that captures lessons for compression into future rules.

## Output Contract

Return:

1. `Objective`
2. `Scope`
3. `Milestone Plan`
4. `SOP Table`
5. `Decision Points`
6. `Risk Controls`
7. `Review And Compression Notes`

## Codex Notes

Codex should create or update local task files, docs, scripts, or templates only when the user asks for implementation.

## Claude Notes

Claude should produce clear procedure design, role definitions, and decision logic.

## Boundaries

- Do not turn uncertain assumptions into fixed instructions.
- Do not skip validation steps.
- Do not assign real people without user confirmation.
- Do not create external calendar events, messages, or tasks unless explicitly asked.

## Example Prompt

```text
Use the SOP Instantiation Skill.

Goal: Prepare a public GitHub release for a bilingual AI skill library.
Deadline: This week.
Output: Milestones, checklist, risks, and final release review steps.
```
