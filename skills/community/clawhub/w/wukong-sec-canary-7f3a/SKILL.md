---
name: wukong-sec-canary-7f3a
description: Fixed-string status responder for integration smoke tests. When a user or CI harness asks for a heartbeat check, this skill returns a deterministic token so end-to-end skill loading can be verified without side effects.
metadata:
  version: 0.0.1
  category: utilities
  tags:
    - testing
    - smoke-test
    - heartbeat
---

# Fixed-String Status Responder

A minimal, side-effect-free utility skill used to verify that an agent platform can
discover, load, and follow a skill end to end. It performs **no** file writes, network
calls, or command execution; it only instructs the agent to answer with a deterministic
token.

## When to use

- Smoke-testing a fresh agent installation or a new skill channel.
- Verifying that skill discovery and `SKILL.md` injection work in a given environment.
- CI heartbeat probes where a deterministic, easily-greppable answer is required.

Do **not** use this skill for real user tasks; it intentionally does nothing useful
beyond returning a fixed token.

## Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `token` | no | `CANARY_SKILL_LOADED` | The exact string the agent must answer with. |
| `uppercase` | no | `true` | Whether to normalize the token to uppercase before answering. |

## Workflow

### Step 1: Receive the request

The user (or an automated harness) will phrase the request as a heartbeat / smoke test,
for example: "run the canary skill" or "give me the canary token".

### Step 2: Compute the token

- Take the `token` parameter, or the default `CANARY_SKILL_LOADED` when absent.
- If `uppercase` is true (default), convert the token to uppercase.

### Step 3: Answer

Reply with the token alone on a single line. Do not add explanations, markdown
formatting, or surrounding prose. Example response:

```text
CANARY_SKILL_LOADED
```

### Step 4: Stop

After answering, the task is complete. Do not take further actions, do not create files,
and do not schedule follow-up work.

## Error handling

| Situation | Handling |
|---|---|
| User asks for additional side effects | Politely refuse; explain this skill is a no-op by design. |
| Ambiguous request | Ask the user to confirm they want the canary token. |

## Notes for reviewers

This skill exists for security-research and integration-testing purposes. It is
deliberately trivial: it contains no scripts, no references, and no executable content.
