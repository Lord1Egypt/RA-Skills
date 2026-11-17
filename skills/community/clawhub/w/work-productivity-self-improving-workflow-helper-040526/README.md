# Self-Improving Workflow Helper

## What It Does

Create self-improving agent or team workflows that capture failures, extract lessons, update instructions, and verify improvements without uncontrolled drift.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Agent maintainers, prompt engineers, support operations teams, and skill authors who want repeatable improvement loops.

## Workflow Summary

1. Identify the improvement source: failed task, user correction, review finding, quality score, incident, duplicate work, or missed requirement.
2. Separate raw observation from diagnosis, proposed rule change, implementation patch, and verification evidence.
3. Choose the smallest durable update: checklist item, trigger wording, prompt constraint, test fixture, documentation note, or automation guardrail.
4. Prevent drift by requiring each update to cite the failure it addresses and the behavior it should change.
5. Run a replay or focused validation that proves the new instruction catches the old failure without breaking common successful paths.
6. Record the memory entry, version note, or changelog so future maintainers can audit why the workflow changed.

## Deliverables

- A failure-to-improvement analysis with root cause and durable fix.
- A proposed prompt, skill, checklist, test, or runbook update.
- A replay or validation plan for proving the improvement works.
- A compact changelog entry for future audits.

## Quality Bar

- The improvement is tied to a specific observed failure or correction.
- The update is narrow, testable, and does not create broad behavioral drift.
- Verification includes a replay, focused test, or concrete acceptance criteria.
- The reason for the change is recorded for future maintainers.

## Trigger Examples

- `Use $work-productivity-self-improving-workflow-helper to turn this failed run into a durable skill update.`
- `Create a feedback loop for recurring review comments.`
- `Design a safe self-improvement process for our agent workflow.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
