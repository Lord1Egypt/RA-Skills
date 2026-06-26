---
name: scheduler-notification-runbook
description: Reliable runbook for scheduled reminders and notification workflows with OpenClaw cron. Use when creating or reviewing reminder skills, scheduling one-shot or recurring reminders, choosing between systemEvent and agentTurn payloads, selecting the correct sessionTarget, writing reminder text that will still read clearly when delivered later, validating whether a job actually fired, or troubleshooting why a scheduled notification did not deliver as expected. Especially useful for ClawHub-published skills that need production-safe reminder behavior instead of ad hoc cron setup.
---

# Scheduler Notification Runbook

## Overview

Use this skill to create reliable reminder and scheduled notification workflows with OpenClaw cron.
Focus on production-safe decisions: choose the correct payload type, choose the correct session target, write reminder text that still makes sense when delivered later, and verify that the job actually fired and delivered.

## Core workflow

### 1. Classify the scheduling need

Decide which of these cases applies before creating any job:

- **One-shot reminder**: "Remind me in 20 minutes" or "Remind me tomorrow at 9 AM"
- **Recurring reminder**: "Remind me every weekday at 6 PM"
- **Background agent task**: a scheduled isolated agent run that produces a summary or follow-up
- **Current-session follow-up**: a scheduled agent run that must keep using the current session thread

If the request is only a reminder and does not need reasoning at fire time, prefer a `systemEvent` reminder.
If the request needs the agent to think, check state, summarize, or perform a task when the time arrives, prefer an `agentTurn` job.

### 2. Choose the payload type

Use this decision rule:

#### Use `payload.kind = "systemEvent"` when:

- The future action is a plain reminder
- The message can be fully written now
- No tool use or reasoning is needed when it fires
- The user mainly wants a notification, not a follow-up workflow

This is the default reminder pattern for simple reminders.

#### Use `payload.kind = "agentTurn"` when:

- The scheduled task must inspect context or perform work later
- The task needs tool use, web access, summarization, or decision-making at fire time
- The task should produce a delivery summary after it completes
- The task must be bound to the current session or a named persistent session

Do not use `agentTurn` just to send a basic reminder that could be expressed in plain text.

### 3. Choose the session target

Match `sessionTarget` to the payload and the desired behavior.

#### Use `sessionTarget = "main"`

Only with `payload.kind = "systemEvent"`.
Use this for normal reminder injection into the main session.

Recommended when:

- The user asked for a straightforward reminder
- The reminder should appear like a natural follow-up in the main conversation

#### Use `sessionTarget = "isolated"`

Only with `payload.kind = "agentTurn"`.
Use this for scheduled work that should run independently and optionally announce a summary.

Recommended when:

- The task should not rely on the current thread
- The task may be long-running or more operational
- You want isolated execution with clear delivery behavior

#### Use `sessionTarget = "current"`

Only with `payload.kind = "agentTurn"`.
Use this when the future agent run must stay attached to the current session context.

Recommended when:

- The user explicitly wants the follow-up in the same thread
- The current session context matters later

#### Use `sessionTarget = "session:<name>"`

Only with `payload.kind = "agentTurn"`.
Use this for durable named workflows that should accumulate their own thread history.

Recommended when:

- You are building a recurring operational workflow
- The job should write into a stable named session rather than a transient isolated run

## Writing reminder text

Reminder text quality matters because the user will read it later, not now.
Write the text as if it has already arrived in the future.

### Rules for good reminder text

- Explicitly say it is a reminder when the time gap is meaningful
- Include the original task or intent
- Include enough context so the user does not have to remember why it was scheduled
- Keep it short and readable
- Avoid raw implementation details such as cron expressions, session targets, job IDs, or internal payload terms

### Good patterns

#### Short-delay reminder

Use for reminders in minutes or within the same day:

- `Reminder: check the build in 20 minutes.`
- `Reminder: join the design review now.`
- `Reminder: send the follow-up message to Alex this afternoon.`

#### Next-day or dated reminder

Use for tomorrow or specific dates/times:

- `Reminder: review the OrAHub CLI Quick Start draft this morning.`
- `Reminder: your 3 PM call with the partner team is coming up.`
- `Reminder: submit the legal review notes for the scheduler skill today.`

#### Context-rich reminder

Use when the reminder could be ambiguous later:

- `Reminder: follow up on the scheduler-notification-runbook skill for ClawHub publication.`
- `Reminder: check whether the recurring reminder demo was actually delivered to the main session.`
- `Reminder: revisit the OrAHub credential onboarding flow and decide whether npm or curl should be the default install path.`

### Avoid

- `ping`
- `do the thing`
- `scheduled task triggered`
- `cron fired successfully`
- Any text that only makes sense to an implementer

## Schedule selection

Pick the simplest schedule that matches the request.

### Use `schedule.kind = "at"` when:

- The reminder should happen once at a specific time
- The request is phrased as "in 20 minutes" or "tomorrow at 9"

### Use `schedule.kind = "every"` when:

- The reminder repeats on a fixed interval
- Exact calendar semantics are not required

### Use `schedule.kind = "cron"` when:

- The reminder repeats on calendar-based rules
- The user asks for things like every weekday, every Monday, or the first day of each month

Prefer the least complex schedule that accurately matches the request.

## Delivery decisions for agent jobs

Delivery matters only for `agentTurn` jobs.

### Use `delivery.mode = "announce"` when:

- The result should be posted back into chat after the isolated run finishes
- The user expects a visible summary

### Use `delivery.mode = "none"` when:

- The task is internal and does not need to notify chat directly
- Another system consumes the result

### Use `delivery.mode = "webhook"` when:

- The scheduled run must call an external HTTP endpoint
- The user explicitly wants webhook delivery

Do not try to simulate webhook behavior through ad hoc messaging if webhook delivery is the correct abstraction.

## Validation workflow

Always validate after creating or updating a scheduled reminder workflow.

### Minimum validation checklist

1. Confirm the schedule shape matches the request
2. Confirm the payload type matches the real need
3. Confirm the session target is valid for that payload
4. Confirm the reminder text reads naturally in the future
5. Confirm the job is enabled
6. Capture the returned `jobId`

### Recommended follow-up checks

- Run the job manually when safe and useful
- Inspect run history for recurring jobs
- Confirm that delivery occurred in the expected place
- If the reminder is time-sensitive, verify timezone assumptions explicitly

## Troubleshooting

Use this sequence when a scheduled reminder or notification did not behave as expected.

### Problem: the job was created but nothing happened

Check:

- Whether the job is enabled
- Whether the schedule is in the future or already missed
- Whether the timezone assumption was wrong
- Whether the scheduler is healthy
- Whether the wrong session target was used

### Problem: the job fired but the message was confusing

Check:

- Whether the reminder text included enough future context
- Whether the text referred to internal details instead of user intent
- Whether the reminder should have been written as a richer natural reminder

### Problem: an `agentTurn` job ran but did not deliver visibly

Check:

- Whether `delivery.mode` was omitted or set incorrectly
- Whether the task was isolated with announce delivery as intended
- Whether the target channel or recipient was specified when needed

### Problem: the wrong session received the follow-up

Check:

- Whether `main`, `isolated`, `current`, or `session:<name>` was selected correctly
- Whether the user wanted a reminder injection or a future agent run
- Whether a named session would be more stable than `current`

### Problem: the reminder should have been simple but was over-engineered

Check:

- Whether `agentTurn` was used when `systemEvent` was enough
- Whether unnecessary delivery settings were added
- Whether a one-shot `at` reminder would have solved the request more directly

## Production guidance for ClawHub publication

When packaging this as a reusable public skill, keep the skill focused on durable decision-making rather than local environment specifics.

### Include

- Clear payload selection rules
- Session target selection guidance
- Reminder text quality rules
- Validation and troubleshooting steps
- Examples framed around real reminder requests

### Exclude

- Local machine assumptions
- Environment-specific secrets or tokens
- Internal-only customer identifiers
- Hard-coded job IDs or one-off operational artifacts

## Reference material

Read `references/cron-patterns.md` when you need compact pattern guidance for one-shot reminders, recurring reminders, and agent-run notification workflows.

Read `references/examples.md` when you need ClawHub-friendly examples that show the difference between simple reminders, recurring reminders, isolated agent jobs, and same-thread follow-ups.
