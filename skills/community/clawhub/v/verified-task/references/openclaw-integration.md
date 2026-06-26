# OpenClaw Integration Notes

Verified Task works best as a callable guardrail inside broader workflows.

## Recommended pattern

1. Define the task spec before generation
2. Generate the output
3. Call Verified Task on the result
4. Read the verdict
5. Proceed only if PASS
6. Allow override only when a human operator explicitly approves it

## Good places to insert the check

- before sending payments
- before sending emails or messages
- before publishing posts
- before continuing an autonomous workflow step
- before acting on a summary or recommendation

## Verification guidance

Keep the verification rule grounded in the actual task requirements.
Do not use vague approval language like "looks good".
Use specific acceptance criteria that can be checked.

## Optional external verification

If you use a separate verification service for structured verdict metadata, keep it optional and avoid sending secrets or sensitive content.
Local verification remains the primary gate.
