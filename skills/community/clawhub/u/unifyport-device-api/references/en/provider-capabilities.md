# Provider capability snapshot

[English](provider-capabilities.md) | [简体中文](../zh-CN/provider-capabilities.md)

Rechecked deployed public matrices on 2026-11-03. F = full, P = partial, - = unsupported. Capability and operation approval are separate boundaries.

Guide IDs: `provider-message-support`, `provider-actions-support`, `provider-webhook-events`. Matrix IDs: `message-sending`, `actions`, `webhook-events`.

## message-sending

Guide ID: `provider-message-support`. Matrix ID: `message-sending`. [Public guide](https://www.unifyport.ai/docs/provider-guide/provider-message-support/)

| Capability | Telegram | WhatsApp | X | Facebook | LINE | Zalo | TikTok | WhatsApp Protocol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| text | F | F | F | F | F | F | F | F |
| image | F | F | F | F | F | F | F | F |
| video | F | F | F | F | F | F | F | - |
| audio | F | F | P | P | F | F | - | - |
| document | F | F | F | F | F | F | - | - |
| file | F | F | F | F | F | F | - | - |
| contact | - | F | - | - | - | - | - | - |
| reply_to.reply_token | - | F | - | - | - | - | - | - |
| mentions | - | F | - | - | P | - | - | - |
| provider_data.parse_mode | F | - | - | - | - | - | - | - |

## actions

Guide ID: `provider-actions-support`. Matrix ID: `actions`. [Public guide](https://www.unifyport.ai/docs/provider-guide/provider-actions-support/)

| Capability | Telegram | WhatsApp | X | Facebook | LINE | Zalo | TikTok | WhatsApp Protocol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| messages/pin | - | F | - | - | - | - | - | - |
| messages/revoke | F | F | - | - | F | - | - | - |
| messages/reaction | F | F | - | - | - | - | - | - |
| messages/edit | - | F | - | - | - | - | - | - |
| conversations (list) | F | F | F | P | F | - | F | - |
| conversations/info | F | F | F | - | F | - | - | - |
| conversations/members | F | F | - | - | F | - | - | - |
| conversations/read | - | F | - | - | - | - | - | - |
| conversations/unread | - | F | - | - | - | - | - | - |
| conversations/mute | - | F | - | - | P | - | - | - |
| conversations/unmute | - | F | - | - | F | - | - | - |
| conversations/pin | - | F | - | - | F | - | - | - |
| conversations/unpin | - | F | - | - | F | - | - | - |
| conversations/labels (list) | - | F | - | - | - | - | - | - |
| conversations/labels (upsert) | - | F | - | - | - | - | - | - |
| conversations/labels (delete) | - | F | - | - | - | - | - | - |
| conversations/labels/members | - | F | - | - | - | - | - | - |
| contacts (list) | - | F | - | - | F | - | - | - |
| contacts/info | - | F | - | - | F | - | - | F |
| contacts/add | - | F | - | - | - | - | - | - |
| contacts/membership | - | F | - | - | - | - | - | - |
| contacts/block | - | F | - | - | - | - | - | - |
| contacts/unblock | - | F | - | - | - | - | - | - |
| contacts/blocklist | - | F | - | - | - | - | - | - |
| contacts/note | - | F | - | - | - | - | - | - |
| groups (list) | - | F | - | - | F | - | - | - |
| groups/info | - | F | - | - | F | - | - | - |
| groups/create | - | F | - | - | - | - | - | - |
| groups/leave | - | F | - | - | - | - | - | - |
| groups/members | - | F | - | - | - | - | - | - |
| groups/update-info | - | F | - | - | - | - | - | - |
| groups/join-requests (+/update) | - | F | - | - | - | - | - | - |
| groups/join-approval-mode | - | F | - | - | - | - | - | - |
| groups/invite-code | - | F | - | - | - | - | - | - |

## webhook-events

Guide ID: `provider-webhook-events`. Matrix ID: `webhook-events`. [Public guide](https://www.unifyport.ai/docs/provider-guide/provider-webhook-events/)

| Capability | Telegram | WhatsApp | X | Facebook | LINE | Zalo | TikTok | WhatsApp Protocol |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| message.received | F | F | F | P | F | F | F | P |
| message.updated | F | F | - | - | F | - | - | - |
| message.deleted | F | F | - | - | F | - | - | - |
| message.read | F | P | - | - | F | - | - | - |
| message.reaction | F | F | - | - | F | - | - | - |
| message.delivered | F | P | - | - | F | - | - | - |
| conversation.updated | F | F | - | - | - | - | - | - |
| conversation.deleted | - | F | - | - | - | - | - | - |
| conversation.cleared | - | F | - | - | - | - | - | - |
| conversation.history | - | F | - | - | - | - | - | - |
| group.updated | F | F | - | - | - | - | - | - |
| group.join_request | - | F | - | - | - | - | - | - |
| account.status.updated | F | F | F | F | F | F | F | F |
| account.started | - | F | - | - | - | - | - | F |
| account.history.synced | - | F | - | - | - | - | - | - |
| account.auth.required | F | F | - | - | F | F | F | - |
| account.auth.succeeded | F | F | F | F | F | F | F | - |
| account.auth.failed | F | F | F | F | F | - | - | F |

## Facebook boundaries

Session import, profile/runtime, E2EE user conversations, one text or one media item only; audio is partial. Send only when running; authorized is not running. No QR/code, groups/channels, quotes, mentions, caption, message actions, contacts, posts/comments or calls. Conversation listing does not imply detail or write capabilities.

Four existing callbacks apply: message.received, account.auth.succeeded, account.status.updated, account.auth.failed. Received can be inbound or outbound; there are no read/delivery receipts. Ordinary runtime error does not revoke authorization. Availability depends on deployment and account state; offline verification does not prove delivery.

Read the linked public guides for detailed conditions. TikTok and WhatsApp Protocol matrix cells do not imply every API, auth mode or deployment is supported. Verify, persist and deduplicate webhooks first; best-effort history requests do not guarantee replay of missed events.
