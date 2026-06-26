# Planning Quality Reference

Use this reference when `/blueprint` needs more detail than the base template captures. Keep the active `/blueprint` skill small; this file holds the reusable quality checks.

## Before Writing

- Confirm the task is one coherent workset. If it spans independent subsystems, split it into separate plans before implementation.
- Map the files or surfaces that will change and state what each owns.
- Prefer existing project boundaries. Refactor only when it directly lowers risk for the current work.
- Make each plan step produce reviewable, testable progress.

## Step Quality

Good implementation steps are concrete enough for another agent to execute without rediscovering intent.

- Name exact files or directories when they are known.
- Separate test-authoring from implementation when the TDD contract needs a distinct RED/GREEN handoff.
- Include exact validation commands and expected success criteria.
- Avoid placeholders such as `TBD`, `TODO`, `handle edge cases`, or `write tests for this`.
- Do not use "similar to previous step"; repeat the necessary details so steps can be read independently.

## File Structure

- Keep files focused on one responsibility.
- Co-locate files that change together when the repo already supports that shape.
- Follow established local patterns before introducing new structure.
- When touching an oversized or tangled file, include only the split that serves the task.

## Self-Review

Before handing off to `/review`, check the plan against the original request.

- Every requirement maps to a step.
- Every step has enough context to execute.
- Types, command names, file paths, and skill names are consistent throughout.
- Test and validation steps cover the changed behavior.
- The plan contains no placeholders or vague implementation instructions.

## Handoff

`/blueprint` writes and commits the plan, then hands off to `/review`. Do not offer a separate planning skill choice from this reference.
