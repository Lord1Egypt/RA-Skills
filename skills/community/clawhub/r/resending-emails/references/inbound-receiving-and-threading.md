# Inbound receiving and threading

This file covers the receiving side of the Resend CLI.

## Recommended inbound architecture

For a production inbound mailbox:

1. enable receiving on a domain/subdomain
2. register a webhook that includes `email.received`
3. treat the webhook as a trigger only
4. use `emails receiving get` to fetch the full inbound message
5. use `emails receiving attachments` / `attachment` for files
6. only then process, store, or reply

## Receiving command group

The CLI exposes:

- `emails receiving list`
- `emails receiving get`
- `emails receiving listen`
- `emails receiving attachments`
- `emails receiving attachment`
- `emails receiving forward`

## `emails receiving list`

Use this for bounded polling or debugging:

```bash
resend --json -q emails receiving list --limit 10
```

## `emails receiving get`

Use this when you need the full content and metadata of one inbound message.

Key point: the returned data includes the raw-message download URL and full body fields. Use this
instead of assuming the webhook already contains everything you need.

## Attachments

Use:

```bash
resend --json -q emails receiving attachments <email-id>
resend --json -q emails receiving attachment <email-id> <attachment-id>
```

Attachment download URLs are signed and short-lived. Fetch them when needed instead of storing them
as if they were permanent URLs.

## `emails receiving forward`

Use this when the task is “forward an inbound email to another address” rather than “reply in the
same thread”.

## `emails receiving listen`

This is a **polling stream** for inbound mail.

Properties that matter to agents:

- minimum interval is 2 seconds
- in JSON/piped mode, output is **NDJSON**
- the command exits after 5 consecutive API failures
- it is for observation/automation loops, not a bounded one-shot call

Sample:

```bash
resend --json emails receiving listen --interval 5
```

## Reply threading

If the user wants to reply into the same thread, use `emails send`, not `emails receiving forward`.

Include appropriate threading headers derived from the inbound message, such as:

- `In-Reply-To`
- `References`

Also consider prefixing the subject with `Re:` when appropriate.
