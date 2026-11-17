---
name: work-productivity-self-improving-workflow-helper
description: >-
  Create self-improving agent or team workflows that capture failures, extract lessons, update instructions, and verify improvements without uncontrolled drift. Use when a user asks for self-improving agent, feedback loop, runbook, prompt update, quality review, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Self-Improving Workflow Helper

## Purpose

Use this skill when a workflow should learn from failed runs, review comments, user corrections, or quality audits and turn them into bounded updates to prompts, skills, tests, or runbooks.

Audience: agent maintainers, prompt engineers, support operations teams, and skill authors who want repeatable improvement loops.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Identify the improvement source: failed task, user correction, review finding, quality score, incident, duplicate work, or missed requirement.
2. Separate raw observation from diagnosis, proposed rule change, implementation patch, and verification evidence.
3. Choose the smallest durable update: checklist item, trigger wording, prompt constraint, test fixture, documentation note, or automation guardrail.
4. Prevent drift by requiring each update to cite the failure it addresses and the behavior it should change.
5. Run a replay or focused validation that proves the new instruction catches the old failure without breaking common successful paths.
6. Record the memory entry, version note, or changelog so future maintainers can audit why the workflow changed.

## Expected Outputs

- A failure-to-improvement analysis with root cause and durable fix.
- A proposed prompt, skill, checklist, test, or runbook update.
- A replay or validation plan for proving the improvement works.
- A compact changelog entry for future audits.

## Validation

- The improvement is tied to a specific observed failure or correction.
- The update is narrow, testable, and does not create broad behavioral drift.
- Verification includes a replay, focused test, or concrete acceptance criteria.
- The reason for the change is recorded for future maintainers.

## Triggers

Keywords: `self-improving agent`, `feedback loop`, `runbook`, `prompt update`, `quality review`, `workflow improvement`

Example trigger sentences:

- `Use $work-productivity-self-improving-workflow-helper to turn this failed run into a durable skill update.`
- `Create a feedback loop for recurring review comments.`
- `Design a safe self-improvement process for our agent workflow.`
