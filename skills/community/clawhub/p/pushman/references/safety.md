# Pushman safety model

Read this reference before a send, retry, CLI authorization, credential revocation, or ambiguous result.

## Send boundary

`pushman_send_notification` and `pushman push` contact the hosted Pushman service, consume one accepted-send allowance, and may create a visible iPhone notification. They are not read-only or idempotent. The operation is additive rather than destructive, but an accidental duplicate is still user-visible and quota-consuming.

Treat these requests as current authorization for one exact send:

- “Push me when this finishes.”
- “Send the notification body I just provided.”
- “Use Pushman to notify the device I named with the title and body above.”

These requests do not authorize a send:

- “Draft a notification for the deployment.”
- “What would Pushman send?”
- “Configure Pushman for this project.”
- “Check whether my devices are available.”

When authorization is absent, show the material proposed fields and wait. When it is already present, proceed once without forcing a second confirmation.

## Targeting and update semantics

- Omitted devices mean every eligible receiving device, not a preview or no-op.
- A named device is a nickname resolved by the hosted account. Inspect devices when the requested target is ambiguous; never guess from prior sessions.
- A send without a key creates a new logical notification.
- A reused key updates the matching logical notification for that sender. Do not invent or silently reuse a key.
- A keyed update still consumes one accepted-send allowance.
- Groups affect presentation; they are not authorization or account-level delivery groups.

## Failure and retry

Pushman deliberately does not retry ambiguous sends. Preserve that behavior:

- `429` means the request was rejected before acceptance; report retry guidance but do not sleep and retry unless the user asks.
- A timeout, connection interruption, or cancellation may occur after the server accepted the request. Do not retry automatically.
- “No eligible receiving device” is not fixed by repeating the same request. Inspect devices or ask the user to restore notification eligibility.
- An accepted message ID proves server acceptance, not APNs delivery or user-open state.

## Content and credential privacy

Notification bodies, titles, subtitles, URLs, images, device nicknames, and delivery history are private user data. Retrieve only what the task needs. Avoid echoing content in diagnostic summaries, examples, validation fixtures, screenshots, or issue reports.

The account CLI credential belongs in the native operating-system keyring. `PUSHMAN_TOKEN` may exist only in the process environment and is send-only. Never inspect keyring storage, print environment values, pass tokens as flags, or add them to MCP JSON. Validation examples must use placeholders and must not contain real credentials, notification content, device nicknames, or production URLs.

## Authorization and revocation

`pushman login` and `pushman pair` each create a short-lived user code. Login is approved through Google or Apple on the Pushman browser page; pairing is approved in the signed-in iPhone app. Both create the same account CLI permission set. Start either only when requested, show the verification URL and code only to the current user, and let the CLI store the resulting credential.

Browser launch failure is not a reason to restart login: the CLI continues polling and the printed URL remains usable. Do not automatically repeat an expired, denied, interrupted, or ambiguous authorization attempt. Never enter, copy, or inspect provider credentials, the hidden device code, or the issued bearer credential.

`pushman logout` revokes the current account CLI credential and removes it locally. It has no dry-run and may break MCP clients and automations that depend on that authorization. Require an explicit logout or revoke request, then confirm `pushman status` reports unauthorized.
