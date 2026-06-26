---
name: tool-output-auditor
description: Audit tool and command results before acting on them. Use when an agent has already run a command or tool, especially in multi-step workflows where a failed, partial, or suspicious result could be accidentally ignored. Trigger for tasks involving validation, packaging, publishing, deployments, file edits, process management, API calls, or any workflow where the next action must depend on actual output rather than assumptions.
metadata:
  openclaw:
    requires:
      bins: [python3]
  homepage: https://clawhub.ai
---

# Tool Output Auditor

Always read the result before moving on. Treat tool output as evidence, not background noise.

## Core rule

After a meaningful tool or command step, explicitly decide which of these states you are in:
- **success** — output matches the intended action
- **failure** — command or tool clearly failed
- **partial** — some progress happened, but the intended outcome is not complete
- **ambiguous** — output is incomplete, contradictory, or not enough to justify the next step

If the state is not clearly `success`, do not continue as if it succeeded.

## Audit workflow

1. Identify the exact step that just ran.
2. Read the output, not just the exit status.
3. Extract the decisive signals:
   - exit code
   - explicit success/failure text
   - created/updated artifact
   - target version or ID
   - warnings that change the next action
4. Classify the result as success, failure, partial, or ambiguous.
5. Only then choose the next action.

## What counts as decisive evidence

### Good evidence
- `Successfully packaged skill to ...`
- `Published <slug>@<version>`
- `Latest: 0.1.0`
- file exists at the expected path
- expected process state is visible

### Bad evidence
- command started but did not finish
- logs were truncated before the important line
- output contains an error but the agent keeps going
- a different command succeeded, but the target command failed
- a result was assumed from memory instead of verified now

## Common anti-patterns

### Ignoring explicit errors
If output says `Validation failed`, `Path must be a folder`, `401`, or `Skill not found`, stop and address that exact error.

### Mistaking activity for success
`Preparing...`, `Fetching...`, or a running background job is not success.

### Checking the wrong thing
Do not treat a successful pre-step as proof that the real step succeeded.

### Narrating future intent as if it already happened
Do not say "published successfully" until the output proves publication.

## Recommended use

Use `scripts/audit_output.py` when you want a quick second-pass summary of a captured command result. It is especially helpful for:
- package / publish workflows
- deployment commands
- API auth failures
- background process completion
- file-generation steps

## Scripts

### `scripts/audit_output.py`
Classifies a saved output file or stdin text into `success`, `failure`, `partial`, or `ambiguous`, highlights the decisive lines, detects contexts such as publish/package/auth/process, and gives a next-step recommendation.

## References

- Read `references/checklist.md` before building automation around multi-step command workflows.
- Read `references/examples.md` for concrete examples of success, failure, partial, and ambiguous outputs.
- Read `references/real-mistakes.md` for real failure patterns this skill is meant to prevent.
