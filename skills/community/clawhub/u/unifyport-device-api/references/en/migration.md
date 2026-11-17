# Migration to 1.1.0

[English](migration.md) | [简体中文](../zh-CN/migration.md)

Status: unreleased. After publication, install the exact @unifyport/unifyport-device-api version 1.1.0 from ClawHub; confirm owner, version and files. Replace the entire old Skill directory so stale files such as skill-card.md cannot remain. Keep API keys out of files; docs-only needs no credential. Node.js >=20 is required.

## Existing integrations

Existing action IDs, API origin, confirmation domain/schema, five-minute TTL and opt-in categories remain stable. Obtain a new preview after any input or version upgrade; never automatically retry an uncertain write. Session import success or authorized is not proof of running; 202 deletion acceptance is not completion. Preserve IDs and timestamp strings without numeric/date coercion. Message aliases do not inherit each other's fields. update-account.provider_account_ref remains unavailable pending public clarification.

## Newly supported fields

- import-auth-session: send whatsapp-protocol only as a nested body object, never in provider_data. Required non-blank strings: phone, static_pub_key, static_pri_key, identity_pub_key, identity_pri_key. Preserve formatted phone and let the server normalize it. platform is int32; device is uint32; use_xxkem_handshake is boolean. Only documented optional fields are accepted. Omit deprecated hash (ignored upstream); authhexdata is a supported deprecated alias, prefer auth_hex_data. Do not send edge_routing. Public host or host:port server overrides are accepted; private/local addresses are blocked, without DNS reachability guarantees. Send the complete input using --input-stdin, then credential opt-in and the exact HMAC token. Never put session material or protocol keys into chat, argv or logs. The runner has no plaintext-secret output channel. Legacy X session_url, pin and proxy_config remain supported.
- list-conversations: query.label_id is an exact provider string, not a number; it is not trimmed. Omission on WhatsApp lists starred conversations, not all conversations. Preserve cursor and do not auto-paginate.
- mark-conversation-read: WhatsApp message receipts require non-empty up_to_message_id and up_to_message_sender_id together; group sender comes from data.sender.id. Comma-separated message IDs must share a sender. Both omitted or whitespace-empty means whole conversation for WhatsApp only. Telegram uses one inbound message ID string (ASCII digits after trimming, numeric value 1–2147483647); it rejects a non-empty sender and whole-conversation omission. The runner cannot infer the channel and keeps Telegram's single-ID form; check the documented provider contract before invoking. Non-empty sender without a non-empty message is rejected locally. Preserve original strings and reconfirm if sender changes.

## Webhook ownership and replacement

list/get/deactivate/delete use query.account_id; create/update use body.account_id. Use the exact case and one non-blank string. Query arrays, null, blank and misplaced account fields are rejected. The CLI rejects duplicate account_id keys in JSON before parsing can hide them. Without the list filter, only workspace endpoints are returned; with it, only independent account endpoints, without inherited workspace configuration.

Create binds to the account; omission creates a workspace endpoint. Update account_id only checks the original binding and cannot rebind, clear or convert ownership. Omission preserves binding. Read/deactivate/delete validate ownership on the server. PATCH replaces configuration: supply every retained setting and the saved signing secret; omission may disable signing or reset events/retries. Do not infer signing credentials from redacted output. One active independent endpoint per account; 409 account_webhook_already_exists (40008) requires reconciliation, not automatic retry. Deactivate and subscription mismatch do not restore workspace fallback; deleting the last independent endpoint restores inheritance for subsequent initial deliveries. HMAC includes the exact account scope; changes require another preview. Fixed HTTPS/public-network, redaction and destructive opt-in policies still apply.

## Validation and rollback

Run documentation and mocked read/write checks before live use; real-account acceptance is separate. To roll back, reinstall the previously reviewed immutable 1.0.0 bundle; new fields/actions will be unavailable. Rollback cannot reverse prior API side effects or migrate Webhook ownership. Report failures without credentials or customer data.
