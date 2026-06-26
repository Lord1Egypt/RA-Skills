---
name: Sara
description: Quiet logic guard for risky multi-skill workflows. Checks order before delete, send, booking, publishing, or other high-impact actions.
version: 0.1.0
---

# Sara

You have access to **Sara**, a quiet logic guard for multi-skill workflows.

Sara helps reduce risky ordering mistakes when a plan includes multiple skills or tool actions.

Use Sara especially when a plan includes:

- destructive actions like delete, remove, clear, wipe, drop, truncate
- external actions like send, publish, post, deploy, submit
- booking or scheduling actions
- repo-destructive actions
- privacy, permission, or sensitive data access actions

## What Sara checks

Sara v0.1 enforces a small set of hard safety rules:

1. **backup before delete**
2. **check before operate**
3. **permission before read**
4. **preview before publish**

Examples:
- backup -> delete
- check_calendar -> book_flight
- review_draft -> send_email
- request_access -> read_private_data
- draft -> publish_post

## When to use Sara

Run Sara before executing a risky multi-step plan when:

- 2 or more skills/tools are involved, and
- at least one step is high-risk, irreversible, externally visible, or destructive

For simple low-risk single-step actions, Sara is usually unnecessary.

## Required behavior

Before executing a risky multi-step plan:

1. Write down the proposed tool or skill order as a simple list.
2. Run `scripts/run_audit.py` with that plan.
3. Read the result carefully.
4. If `is_safe` is `false`, do **not** continue with the original order.
5. Show the user the risk and propose the `suggested_order`.
6. If the action is destructive or irreversible, ask for confirmation before continuing.

Skipping Sara for risky multi-step plans increases the chance of contradictory actions, failed retries, or destructive ordering mistakes.

## Example audit input

```json
{"tools":["backup","delete"]}
```

## Example audit output

```json
{
  "is_safe": false,
  "risk_level": "critical",
  "warnings": [
    "Run 'backup' before 'delete'. Backups should happen before destructive actions."
  ],
  "suggested_order": ["backup", "delete"]
}
```

## How to respond
- If Sara says the plan is safe: continue.
- If Sara says the plan is unsafe: pause, explain the risk, and suggest the safer order.
- If the plan touches deletion, publishing, payment, scheduling, permissions, or sensitive data, prefer confirmation before continuing.

## Response style

When Sara detects a risky order, explain it clearly and briefly.

Good example:

- “Sara noticed a risky sequence. Suggested order: backup -> delete. Would you like me to continue in that order?”

Do not mention internal implementation details unless the user asks.

## Important

Sara is a **guard**, not a replacement for user intent.

Use Sara to:
- reduce risky ordering mistakes
- reduce repeated retries
- reduce contradictory multi-skill plans
- make high-risk workflows safer and more consistent
