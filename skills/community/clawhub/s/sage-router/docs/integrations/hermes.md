# Use Sage Router with Hermes

Hermes-style operator agents can use Sage Router as the stable model endpoint behind routing, fallback, and provider health checks.

## Recommended shape

- Point OpenAI-compatible Hermes calls at `http://localhost:8790/v1`.
- Keep the visible operator workflow unchanged.
- Let Sage Router choose the right route for status, review, escalation, and long-running agent work.

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=local-router
```

## Routing pattern

- Status and ACK-style work: `fast` or `local-first`.
- Review requests: `balanced`.
- Escalations or high-risk changes: `best`.

Use provider-qualified models only when the workflow needs a hard pin. Otherwise, use `auto` and let Sage Router apply policy.
