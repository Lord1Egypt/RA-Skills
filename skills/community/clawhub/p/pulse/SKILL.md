---
name: pulse
description: Design and configure self-contained recurring agent checks with explicit targets, authority, change-sensitive reporting and stop conditions. Use for requested monitoring, reminders or follow-ups; use the included Meta-Pulse guidance when reviewing existing watches.
---

# Pulse

A pulse is a recurring check with enough context to work without the conversation that created it. The value is the instruction, not the timer.

## Create a bounded watch

First inspect the host's actual scheduler and existing watches. Update an existing matching watch instead of creating a duplicate. Use the product's supported recurring-task mechanism; do not invent tool names or assume schedules survive disconnects, expire automatically or run without a model invocation.

Give every watch:

1. **Identity and context:** a stable tag, exact target/run identity, canonical state location, host and owner. Use private machine paths only in the user's private scheduler, never in this distributable skill.
2. **Check:** how to distinguish progressing, completed, failed, missing and unknown. A request timeout is unknown, not proof that the target disappeared. Name the source of truth and distinguish observations from inference.
3. **Authority:** read-only by default; name any specifically authorised mutations. Permission to monitor does not authorise restarts, spending, messages to third parties, publishing or deleting resources.
4. **Report:** notify on meaningful changes, completion, failure or required user action. Stay quiet when nothing actionable changed, unless the user explicitly requested every-interval updates. Record an event key or last observed state to avoid repeat notifications.
5. **Stop or review:** for finite work, stop the exact watch after verified completion or a user stop request. For ongoing monitoring, define a review date and scope. Unknown/unreachable states should trigger bounded rechecks and an escalation condition, not silent abandonment.

Choose a cadence matched to how quickly the target changes and the user's request. Prefer an event or wait mechanism for immediate response. Use an offset from busy round minutes when compatible with the scheduler and requested timing.

## Activate and verify

Write a self-contained, human-readable prompt. Check it as a fresh agent: can it locate the target and distinguish an allowed action from an escalation?

Create or update through the supported scheduler. Read back the returned identifier, cadence, enabled state, timezone and prompt. Preserve those in the configured private project record. A drafted prompt is not an active watch. Explain actual execution/lifetime limits; do not promise uptime or exact timing the host cannot provide.

If the scheduler is unavailable, provide the prepared prompt and state that nothing was scheduled. Do not create an unrelated scheduler or shell daemon as a hidden fallback.

For portfolio review, read [Meta-Pulse](references/meta-pulse.md).
