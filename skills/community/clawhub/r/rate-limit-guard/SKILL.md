---
name: rate-limit-guard
description: Prevent 429 retry loops and wasted tokens. Use before expensive API calls or after hitting rate limits. Enforces preflight checks, backoff, and context shrinking.
---

# Rate Limit Guard

## Before Expensive Calls
Check: provider/model, recent failures, concurrency, context size.

## On 429
1. Set concurrency to 1.
2. Stop parallel retries.
3. Shrink context.
4. Send one minimal probe.
5. Back off (exponential).

## Rules
- Never retry a giant request unchanged.
- Never fallback-spam premium providers.
- Batch corpus work in 10–20 item chunks.

## Output
Next action: proceed / recovery mode / pause.
