# Public error reference

[English](errors.md) | [简体中文](../zh-CN/errors.md)

Guide ID: `error-reference`.

HTTP Groups: `400`, `401`, `404`, `409`, `500`, `501`, `502`, `503`.

Failures use an `error` object with machine-readable `code` and human-readable `message`; the broad category is the HTTP status. Branch on `code`, not message text. Capture top-level `request_id` for support and reconciliation, but do not attach a sensitive raw request or response.

## 400 Bad Request

| Code | Meaning |
| --- | --- |
| `invalid_request` | Body cannot be decoded or required fields are missing. |
| `invalid_provider` | Provider in the URL is missing or unsupported. |
| `unsupported_action` | Account action is not recognized. |
| `invalid_conversation_type` | `type` must be `user`, `group`, or `channel`. |
| `unsupported_conversation_type` | Provider does not support the operation for that conversation type. |
| `unsupported_message_type` | Selected provider does not support `message.type`. |
| `unsupported_provider_auth_mode` | Selected provider does not support `auth_mode`. |
| `auth_mode_phone_required` | Selected auth mode requires `provider_data.phone` at account creation. |
| `invalid_reply_token` | `reply_to.reply_token` was modified, encrypted under another key, or unreadable; return the inbound token unchanged. |
| `create_api_key_failed` | API-key creation request was rejected. |
| `update_api_key_failed` | API-key update request was rejected. |
| `rotate_api_key_failed` | API-key rotation request was rejected. |
| `create_webhook_endpoint_failed` | Webhook-endpoint creation was rejected. |
| `update_webhook_endpoint_failed` | Webhook-endpoint update was rejected. |
| `deactivate_webhook_endpoint_failed` | Webhook-endpoint deactivation was rejected. |
| `delete_webhook_endpoint_failed` | Webhook-endpoint deletion was rejected. |
| `update_workspace_failed` | Workspace update was rejected. |

Correct non-secret input and preview again. Never ask the user to paste a credential into chat.

## 401 Unauthorized

| Code | Meaning |
| --- | --- |
| `missing_api_key` | `X-Api-Key` is missing. |
| `invalid_api_key` | API key is unknown or disabled. |

The bundled runner obtains the key only from `UNIFYPORT_API_KEY`. Do not print it while diagnosing either code.

## 404 Not Found

| Code | Meaning |
| --- | --- |
| `not_found` | Route does not exist. |
| `conversation_not_found` | Provider could not find the conversation. |
| `contact_not_found` | Contact was not found under this account. |
| `group_not_found` | Group was not found under this account. |

Do not use `not_found` as a reason to guess alternate or undocumented routes.

## 409 Conflict

| Code | Meaning |
| --- | --- |
| `account_allocation_busy` | Allocation lock is held; retry after a short delay. |
| `no_allocatable_server` | No allocatable provider server exists in the requested region. |
| `workspace_account_quota_exceeded` | Workspace account quota is exhausted. |
| `duplicate_provider_account` | Another account in the workspace already uses the provider identity. |
| `account_already_authorized` | Account is already authorized, so the requested auth action is rejected. |
| `account_binding_not_found` | Account is not bound to an active provider server. |

Only `account_allocation_busy` explicitly recommends a short retry. Re-query state before any state-changing retry.

## 500 Internal Server Error

| Code | Meaning |
| --- | --- |
| `create_account_failed` | Server-side error creating the account. |
| `update_account_failed` | Server-side error updating the account. |
| `delete_account_failed` | Server-side error deleting the account. |
| `get_account_failed` | Server-side error loading account details. |
| `list_accounts_failed` | Server-side error listing accounts. |
| `get_session_failed` | Server-side error loading the authentication session. |
| `get_auth_state_failed` | Server-side error loading authentication state. |
| `run_action_failed` | Server-side error running an account action. |
| `run_runtime_action_failed` | Server-side error running a runtime action. |
| `run_session_action_failed` | Server-side error running a session action. |
| `run_auth_action_failed` | Server-side error running an authentication action. |
| `send_message_failed` | Server-side error sending the message. |
| `pin_message_failed` | Server-side or provider error pinning/unpinning a message. |
| `revoke_message_failed` | Server-side or provider error revoking a message. |
| `react_message_failed` | Server-side or provider error reacting to a message. |
| `edit_message_failed` | Server-side or provider error editing message text. |
| `list_conversations_failed` | Server-side error listing conversations. |
| `get_conversation_failed` | Server-side error loading a conversation. |
| `list_conversation_members_failed` | Server-side error listing conversation members. |
| `mark_conversation_read_failed` | Server-side or provider error marking a conversation read. |
| `mark_conversation_unread_failed` | Server-side or provider error marking a conversation unread. |
| `mute_conversation_failed` | Server-side or provider error muting a conversation. |
| `unmute_conversation_failed` | Server-side or provider error unmuting a conversation. |
| `pin_conversation_failed` | Server-side or provider error pinning a conversation. |
| `unpin_conversation_failed` | Server-side or provider error unpinning a conversation. |
| `list_conversation_labels_failed` | Server-side or provider error listing labels. |
| `upsert_label_failed` | Server-side or provider error creating/updating a label. |
| `delete_label_failed` | Server-side or provider error deleting a label. |
| `set_label_members_failed` | Server-side or provider error tagging/untagging conversations. |
| `list_contacts_failed` | Server-side error listing contacts. |
| `get_contact_failed` | Server-side error loading a contact. |
| `block_contact_failed` | Server-side or provider error blocking a contact. |
| `unblock_contact_failed` | Server-side or provider error unblocking a contact. |
| `list_blocklist_failed` | Server-side or provider error loading the blocklist. |
| `set_contact_note_failed` | Server-side or provider error setting/clearing a contact note. |
| `list_groups_failed` | Server-side error listing groups. |
| `get_group_failed` | Server-side error loading a group. |
| `create_group_failed` | Server-side or provider error creating a group. |
| `leave_group_failed` | Server-side or provider error leaving a group. |
| `update_group_members_failed` | Server-side or provider error updating group members. |
| `update_group_info_failed` | Server-side/provider error updating group name, description, or avatar, including admin-permission rejection. |
| `list_group_join_requests_failed` | Server-side/provider error listing pending join requests. |
| `update_group_join_requests_failed` | Server-side/provider error approving/rejecting join requests. |
| `set_group_join_approval_mode_failed` | Server-side/provider error changing join-approval mode. |
| `get_group_invite_code_failed` | Server-side/provider error fetching the invite link/code. |
| `list_webhook_endpoints_failed` | Server-side error listing webhook endpoints. |
| `get_webhook_endpoint_failed` | Server-side error loading a webhook endpoint. |
| `get_workspace_failed` | Server-side error loading the workspace. |
| `list_api_keys_failed` | Server-side error listing API keys. |
| `list_provider_regions_failed` | Server-side error listing provider regions. |

A `500` does not prove whether an externally visible write reached the provider. Do not retry writes, destructive actions, or credential operations blindly; use state reads, webhook events, and `request_id` to reconcile.

## 501 Not Implemented

| Code | Meaning |
| --- | --- |
| `unsupported_by_provider` | Selected provider has not implemented the endpoint. |

Consult `provider-capabilities.md`; do not switch provider or operation silently.

## 502 Bad Gateway

| Code | Meaning |
| --- | --- |
| `provider_adapter_not_found` | Provider adapter is unavailable or not registered. |

Report `request_id` and avoid blind state-changing retries.

## 503 Service Unavailable

| Code | Meaning |
| --- | --- |
| `allocation_service_unavailable` | Allocation lock service is unavailable; retry shortly. |

Use bounded backoff and preserve the original redacted intent; a new preview token is required if canonical input changes.
