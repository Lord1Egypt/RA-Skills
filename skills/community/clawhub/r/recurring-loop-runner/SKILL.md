---
name: "recurring_loop_runner"
description: "Use when the user wants a prompt or command to run on a recurring interval, such as checking deploys, polling status, or repeating a slash-command."
---


# Recurring Loop Runner

Use this skill when a task should repeat on a time interval.

## Workflow
1. Parse the interval from the user request.
2. Normalize human phrasing into a valid cadence.
3. Create the recurring schedule.
4. Confirm the cadence, identifier, and expiry behavior.
5. Execute the task once immediately so the user gets instant feedback.

## Guardrails
- Do not trigger for one-off requests.
- If the cadence is ambiguous or uneven, round and explain the rounding.
- Make cancellation or update instructions easy to find.

## Example Requests
- Check the deploy every 15 minutes.
- Run this slash-command hourly and execute it once now.

## Inputs
- Requested cadence
- Prompt or command to repeat

## Outputs
- Scheduled recurring task
- Immediate first execution
- Cancellation details

## Success Criteria
- The interval is parsed correctly.
- The task is both scheduled and run once immediately.
- The user knows how to stop it later.

## Non-Goals
- One-off commands with no repeating behavior

## Source Provenance
Derived from `src/skills/bundled/loop.ts`.
