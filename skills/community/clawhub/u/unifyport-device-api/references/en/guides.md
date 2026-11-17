# Public guide snapshot

[English](guides.md) | [简体中文](../zh-CN/guides.md)

This file summarizes the nine public conceptual and authorization guides. It deliberately contains no captured payload, customer identifier, phone number, session, or credential. Operation request fields and execution policy remain authoritative in `../operations.json`.

Guide IDs: `introduction`, `quickstart`, `account-lifecycle`, `provider-auth-telegram`, `provider-auth-line`, `provider-auth-zalo`, `provider-auth-twitter`, `provider-auth-whatsapp`, `provider-auth-facebook`.

## Introduction

UnifyPort exposes one REST API and one normalized webhook event stream for Telegram, WhatsApp, LINE, X (Twitter), Zalo, and TikTok. Public operation and capability details currently cover only the providers shown by the relevant guide; do not infer TikTok behaviour where no matrix or authorization guide exists.

- `Workspace`: isolation boundary. `X-Api-Key` resolves exactly one workspace, so request bodies do not need another workspace id.
- `Account`: one provider login, treated as one virtual device. Create it, complete a supported authorization flow, then send and receive through it.
- `Runtime`: live connection behind an account. Successful authorization starts it automatically; `runtime_status` exposes the connection state.
- `Webhook`: primary record of observed message traffic. Message history is not persisted and missed events cannot be replayed, so register a receiver first and save only required data on arrival.

All live requests use `https://api.unifyport.ai` and `X-Api-Key`. Every success or error response has top-level `request_id` and the `X-Request-Id` response header. A caller-supplied `X-Request-Id` is echoed as `client_request_id` for reconciliation.

## Quickstart

The public WhatsApp quickstart has this order:

1. Verify access with `get-workspace`.
2. Register a webhook with `create-webhook` before authentication; `subscribed_events: ["*"]` deliberately selects the full standard catalog.
3. Call `provider-regions` for `whatsapp` and choose a region with `allocatable: true`; otherwise account creation can return `409 no_allocatable_server`.
4. Use `create-account` with `provider: whatsapp`, the chosen region, `auth_mode: code`, and `provider_data.phone: <E164_DIGITS>`.
5. Call `start-code-auth` with an empty body. The public API returns a transient `auth_payload.verify_code` for entry on the phone, valid for roughly three minutes. This safe runner redacts it; a product that must display it needs its own controlled UI or secure destination outside Agent chat. Wait for `account.auth.succeeded`, then `account.started`; runtime start is automatic.
6. Use the message-specific catalog entry `send-text-message` with `<ACCOUNT_ID>` and a provider-formatted recipient placeholder.
7. Receive `message.received`, verify the delivery signature, and store only the fields the application needs.

Steps 2, 4, 5, and 6 are state-changing or credential-sensitive and must follow runner preview, confirmation, opt-in, and stdin rules.

## Account lifecycle

An account has three independent state dimensions:

| Dimension | Owner and source |
| --- | --- |
| `status` | Caller-owned business on/off switch, set at creation or by update. |
| authentication `status` | Platform-owned, read through `GET /v1/accounts/{account_id}/auth`. The REST account object itself has no `auth_status` field. |
| `runtime_status` | Platform-owned live connection state on the account object. Webhook payloads expose both `auth_status` and `runtime_status`. |

Authentication states:

| State | Meaning |
| --- | --- |
| `pending_auth` | Initial state or no active flow. |
| `awaiting_qr_scan` | QR flow active; `auth_payload` carries rendering material. |
| `awaiting_code` | Verification-code flow active. |
| `awaiting_password` | Provider requires a two-factor password. |
| `authorized` | Authentication complete; runtime starts automatically. |
| `failed` | Flow failed; `last_error` may carry the reason. |

`/auth/qr/start` enters QR waiting, `/auth/start` enters code waiting, password challenges enter `awaiting_password`, and successful user action enters `authorized`. `/auth/cancel` abandons a waiting flow. Provider failure emits `account.auth.failed`; invalidated sessions emit `account.auth.required` and require a fresh flow. While already authorized, starting or importing authentication returns `409 account_already_authorized`; cancel first only when reauthentication is truly intended.

Runtime states are `unknown`, `starting`, `running`, `reconnecting`, `disconnected`, `stopping`, `stopped`, and `error`. Authorization normally drives `starting` to `running`; explicit start, stop, reconnect, and refresh actions handle recovery or operator control. Mirror changes from `account.status.updated` rather than aggressive polling.

## Provider authorization

All authorization actions are `credential` risk unless the catalog says otherwise. Do not place codes, passwords, session material, QR material, proxy credentials, or API hashes in chat or command arguments. Provide the complete `{params,query,body}` request through `--input-stdin` for preview and confirmed execution.

Some older provider-flow steps explicitly call runtime start after success. The current introduction, quickstart, and lifecycle contract says authorization starts runtime automatically; that explicit start is only an idempotent compatibility step and is not required.

### Telegram

Supported modes are `code`, `qrcode`, and `session`.

- `code`: create with `provider_data.api_id`, `provider_data.api_hash`, and `provider_data.phone`; start the flow, submit the received code, and submit a two-factor password only if status becomes `awaiting_password`.
- `qrcode`: create with `provider_data.api_id` and `provider_data.api_hash`; start QR and check until authorized. QR tokens expire after about 30 seconds, so refresh with a new start rather than reusing an expired token.
- `session`: create with `auth_mode: session`, then import body field `session_url` as high-value secret material.
- A wrong 2FA attempt requires canceling and starting a fresh flow. Authentication transitions arrive on the configured webhook.

### LINE

LINE supports `qrcode` only. `metadata.device_login_type` is optional. The public guide says the QR URL and display-only PIN arrive asynchronously in `account.auth.required`; they are not returned synchronously by QR start. This runner redacts that credential-sensitive material, so a product that displays it needs a controlled UI or secure destination outside Agent chat. The guide also describes a cached auth-session read, but that read is not an executable entry in this Skill's public operation catalog: do not synthesize it. Use the webhook and cataloged QR-check flow.

On success, `provider_account_ref` is populated and standard profile fields may be present. Treat QR/PIN material as sensitive display data.

### Zalo

Zalo supports `qrcode` only and needs no credential up front. QR start returns rendering material, QR check completes the flow, and `qrcode_expired` means a fresh QR start is required. A webhook endpoint is required for authentication and message events. Public notes use thread type `0` for user/friend and `1` for group; sending normalizes this distinction.

### Twitter / X

X supports `session` import only; there is no public QR or code flow. Create the account with `auth_mode: session`, then import body field `session_url`. Body field `pin` is optional and the public guide uses the literal fallback `"0000"` for an export without 2FA; body field `proxy_config` is optional for geographic routing. Treat the export and any proxy credential as high-value secrets.

In the provider guide, `params.session_url`, `params.pin`, and `params.proxy_config` mean provider-action parameters. In the public request and this runner they are top-level body fields, not a nested object named `params`.

### WhatsApp

Supported modes are `qrcode` and `code`.

- `qrcode`: optional creation fields are `provider_data.device_os`, `provider_data.device_platform`, and `provider_data.proxy_config`. QR start enters `awaiting_qr_scan`; actual QR material arrives in `account.auth.required` and can also be checked through the cataloged QR-check action. Success emits `account.auth.succeeded` followed by `account.started`.
- `code`: save `provider_data.phone: <E164_DIGITS>` when creating the account. Start code auth with an empty body. The public API returns `auth_payload.verify_code` for entry on the phone within roughly three minutes, but this safe runner redacts it; delivery requires a caller-controlled UI or secure destination outside Agent chat. The code is not submitted back to the API.
- Successful pairing starts runtime automatically; a later runtime-start request is a no-op.

For provider-specific message, action, and event support, read `provider-capabilities.md` rather than inferring capability from successful authorization.


## provider-auth-facebook

[Public authorization guide](https://www.unifyport.ai/docs/provider-guide/provider-auth-facebook/)

1. Select an allocatable region; create-account uses provider=facebook and auth_mode=session.
2. Keep authorized Cookie JSON at a short-lived controlled session_url. Import with credential opt-in, stdin and HMAC confirmation. Follow the guide's cookies array including c_user, xs and datr; never paste values into chat or logs.
3. Check runtime after authorization. Bound refresh while starting; start stopped accounts only with explicit intent. Send only when running. Never reconnect or retry unknown writes automatically.
4. Preserve the string ID from a synchronized E2EE type=user conversation. One text or media item only; no caption, mentions, quotes or groups. Audio is partial. Configure an active Webhook and persist/deduplicate events before business traffic.
