---
name: risk-aware-retry
description: Execute tasks with reliability-first behavior under flaky conditions. Use when commands fail due to transient errors (network, timeouts, rate limits, temporary locks), when deciding whether to retry vs escalate, or when the user asks for risk-based judgment (engineer around low risk issues, notify on medium/high risk).
---

# Risk-Aware Retry

Default to completion, not first-attempt success.

## Operating rule

- Continue automatically for low-risk, reversible failures.
- Escalate before medium/high-risk actions.
- Report only: DONE with proof, or BLOCKED with exact blocker + next attempt.

## Step 1) Classify risk quickly

Classify the current issue before acting:

### Low risk (auto-engineer, no handoff)

- Transient network failures: ECONNRESET, ETIMEDOUT, DNS hiccups
- Package registry or git fetch flakiness
- Temporary 5xx responses / rate limits
- File locks that are expected to clear
- Idempotent command retries

Action:

1. Retry automatically with backoff
2. Change approach if same error repeats
3. Keep going until success or risk changes

### Medium risk (notify briefly, then proceed if user preference allows)

- Non-destructive config adjustments
- Service restarts where temporary disruption is expected
- Long-running operations with uncertain side effects
- Re-running tools that may duplicate work or messages

Action:

1. Send one-line risk note
2. State mitigation and rollback path
3. Proceed if aligned with user preference

### High risk (stop and ask)

- Destructive operations (data deletion, force resets)
- Security-sensitive changes (auth, firewall, exposure)
- Irreversible external effects (public posts, emails to third parties)
- Any action with unclear blast radius

Action:

1. Pause
2. Ask explicit confirmation
3. Provide safer alternative

## Step 2) Retry policy for low-risk failures

Use this baseline policy unless a service has stricter limits:

- Attempt budget: 8 attempts
- Backoff: 2s, 4s, 8s, 15s, 25s, 40s, 60s, 90s
- Jitter: ±20%
- Per-attempt timeout: set explicitly
- If same error repeats 3 times: switch tactic

Switch tactics examples:

- `git fetch` fails -> retry with pruned tags / re-resolve upstream
- `pnpm install` fails -> retry with longer timeout, then rerun once after lockfile check
- HTTP 429/5xx -> honor Retry-After, then exponential backoff
- Download interrupted -> resume/restart cleanly, verify checksum if available

## Step 3) Progress signaling

Do not spam.

- Silent while making normal low-risk retries
- Send update only when:
  - risk class changes,
  - operation exceeds expected duration,
  - user explicitly asks status

## Step 4) Completion contract

On success, report:

- what was done,
- evidence (version/commit/output),
- notable recoveries (e.g., retried after ECONNRESET).

On block, report:

- exact blocker,
- why it is not transient,
- next concrete action already queued or needed from user.

## Step 5) Safety guardrails

- Prefer reversible actions.
- Avoid destructive cleanup unless approved.
- Never hide risky operations behind “retry logic”.
- If uncertain on risk class, treat as medium and notify.
