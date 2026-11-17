# Safe workflows

[English](workflows.md) | [简体中文](../zh-CN/workflows.md)

## Answer a documentation question

1. Stay in `docs-only`; do not read `UNIFYPORT_API_KEY`.
2. Identify the relevant guide, catalog `id`, `operationId`, or event type.
3. Read its catalog metadata and the linked public documentation in the user's language.
4. Explain the request fields and provider caveats without inventing defaults.
5. Use placeholders such as `<ACCOUNT_ID>` and `<YOUR_API_KEY>`; never substitute live values from previous output.

## Inspect current data

1. Confirm the user wants a live call rather than an example.
2. Select exactly one allowlisted read operation.
3. Collect only required path/query inputs and choose the smallest useful page. Because identifiers are sensitive, provide the complete `{params,query,body}` object through `--input-stdin` when the runner requires it.
4. Preview the fixed origin, method, redacted path values, and operation ID.
5. Execute through the bundled runner and summarize the redacted result.

Read results can contain personal data. Do not paste an entire contact, conversation, membership, or message dataset unless the user has a concrete need and the output can be handled safely.

## Send or change a message

1. Check the public provider capability guide for the requested message type or action.
2. Confirm the exact account, recipient or conversation, content/action, and user intent.
3. Select the message-specific catalog entry even when it shares `POST /v1/messages` with other actions.
4. Provide sensitive identifiers and content with a complete `--input-stdin` object, generate a redacted preview, and request the exact confirmation required by the runner.
5. Execute once. The preview token expires after five minutes and is never reused after an execution attempt, even if still valid. Do not retry automatically after an ambiguous timeout; use `request_id` and provider state to reconcile first, then create a new preview if another attempt is explicitly required.

## Manage accounts and runtime

Treat account creation, updates, deletion, authorization, start/stop/reconnect, and group membership changes as state-changing actions. Deletion, leaving a group, revocation, and similar irreversible or externally visible actions require explicit destructive intent.

Authentication codes, two-factor passwords, QR payloads, and imported sessions are sensitive. Keep them out of prompts and ordinary output; provide the complete request through `--input-stdin` and only from a controlled input channel.

## Register a webhook endpoint

1. Use a user-owned HTTPS destination; do not invent or probe a callback URL.
2. Select only required standard event subscriptions, or use the documented wildcard deliberately.
3. Treat `signing_secret` and endpoint URL as sensitive input; send the complete request through `--input-stdin` and never show the secret afterward.
4. Implement signature verification over the exact raw request body before parsing JSON.
5. Acknowledge delivery promptly, make handlers idempotent, and keep only necessary data.

Consult the public webhook delivery guide for the current header, signature, retry, and ordering contract.

## Create or rotate an API key

These are `credential` operations. Confirm the intended key scope/status and secure destination before execution. The public API may return plaintext only once, but this safe runner redacts it; a product that must capture it needs a caller-controlled secure destination outside Agent chat. Never write it to Agent history, console logs, or repository files. Rotation also changes the validity of the previous credential; do not execute it as routine troubleshooting.

## Handle an API error

1. Capture the HTTP status, public error code, and `request_id`.
2. Redact request/response fields before explaining the failure.
3. Check the public error reference and provider capability guide.
4. Ask for missing non-secret inputs; never ask the user to paste an API key or session.
5. Retry reads only when appropriate. Never blindly retry a write, destructive action, or credential operation.


## Published contract update 2026-11-03

Page list-accounts with query.limit/cursor, preserve data.next_cursor and bound page counts. Caller-owned optional headers.Idempotency-Key identifies the same logical purchase and is included in HMAC confirmation. Use --input-stdin for the complete input; authentication header overrides are rejected. A 202 deletion is acceptance only: bound get-account-operation queries; legacy 204 has no operation ID. REVIEW needs reconciliation; SUCCEEDED does not prove refunds or authorization.

create-auth-session, submit-passkey-response (webauthn_response is a complete serialized JSON string) and confirm-passkey require credential opt-in. Documented proxy objects remain subject to public egress validation. PATCH auth_mode alone; distinguish omission, explicit empty clears and invalid null values.

add-contact and get-contact-membership follow WhatsApp LID rules; false is a valid result. History before must refer to one real content message; preserve sent_at and reject synthetic call_record IDs. 202 is not guaranteed callbacks or completion. Post/comment IDs remain nonblank strings. get-post/list-post-comments are POST reads without write confirmation; reply-post-comment requires HMAC and comment_id refers only to a confirmed top-level comment.

create-call requires explicit write intent; hangup-call also needs destructive opt-in and HMAC. Server private beta/is_beta eligibility still applies; never dial automatically. Join URLs, authorization URLs, WebAuthn, provider profiles and reply tokens are redacted from model output; use a controlled UI outside chat when display is necessary. get-active-call is read-only; null means no active call. Hangup may return ended or failed, both terminal.

## Protocol import, labels and read receipts

Use import-auth-session for the nested whatsapp-protocol object; required keys, stdin, redaction and credential/HMAC rules are mandatory. Legacy X session_url/pin/proxy_config remain available. Use query.label_id as an exact string for list-conversations; omission on WhatsApp means starred conversations. For WhatsApp message receipts pair up_to_message_id with up_to_message_sender_id, taking group sender from data.sender.id. Telegram uses a single inbound ID and does not support a non-empty sender. The runner cannot infer the channel. See [migration](migration.md) for empty-value and provider limits.

## Account-scoped Webhook configuration

list/get/deactivate/delete accept query.account_id; create/update accept body.account_id. Omission on list selects workspace endpoints; a filter selects only independent account endpoints. Creation may bind an account, while update only validates the original binding. PATCH is replacement: supply all settings and the saved signing secret to retain them. Do not automatically retry account_webhook_already_exists. Inactive or unmatched subscriptions do not fall back to workspace configuration. See [migration](migration.md).
