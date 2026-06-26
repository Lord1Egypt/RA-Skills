# Webhooks and local listeners

This file covers both production webhook registration and local development listening.

## `webhooks create`

Use `webhooks create` to register an HTTPS endpoint and subscribe to events.

Sample:

```bash
resend --json -q webhooks create \
  --endpoint https://app.example.com/hooks/resend \
  --events email.sent email.delivered email.bounced
```

### Important rules

- endpoint must use HTTPS
- `--events` replaces “which events do I care about?”
- `all` is supported as shorthand for all current event types
- the returned `signing_secret` is shown **once** — store it immediately

## `webhooks update`

Use this to replace the endpoint URL, replace the full event list, or enable/disable delivery.

Be careful: `--events` is a **replacement**, not an additive merge.

## Production-safe webhook handling

The CLI registers webhooks, but your application still needs to verify them safely.

Always:

1. read the **raw** request body
2. verify with the signing secret
3. use `svix-id`, `svix-timestamp`, and `svix-signature`
4. dedupe on `svix-id`
5. assume at-least-once delivery
6. assume events may arrive out of order

## `webhooks listen`

This is a **local development** command, not a normal bounded request.

What it does:

1. starts a local HTTP server on `--port` (default `4318`)
2. creates a temporary webhook pointing at your public `--url`
3. prints incoming events
4. optionally forwards payloads to `--forward-to`
5. deletes the temporary webhook when you stop the process

Sample:

```bash
resend --json webhooks listen \
  --url https://example.ngrok-free.app \
  --forward-to localhost:3000/webhooks/resend
```

### Agent guidance for `webhooks listen`

- treat it as a stream
- use a timeout or explicit stop condition
- in JSON/piped mode, expect one JSON object per event
- keep stderr because interactive mode prints useful status there

### Forwarding behaviour

When `--forward-to` is used, the CLI forwards the original payload with the Svix headers preserved.
That makes it good for local app testing.

## Event modelling

Important event families include:

- email events (`email.sent`, `email.delivered`, `email.bounced`, `email.received`, etc.)
- contact events
- domain events

Remember that event delivery is per recipient: one outbound action can generate multiple event
records.
