# 公开 Error Reference

[English](../en/errors.md) | [简体中文](errors.md)

Guide ID：`error-reference`。

HTTP Groups：`400`、`401`、`404`、`409`、`500`、`501`、`502`、`503`。

失败 response 使用 `error` object，其中 `code` 机器可读，`message` 面向用户；HTTP status 表示大类。程序应按 `code` 分支，不能依赖 message 文案。记录顶层 `request_id` 供 support 与对账，但不能附加敏感 raw request 或 response。

## 400 Bad Request

| Code | 含义 |
| --- | --- |
| `invalid_request` | Body 无法解析，或缺少 required field。 |
| `invalid_provider` | URL 中的 provider 缺失或不支持。 |
| `unsupported_action` | 无法识别 account action。 |
| `invalid_conversation_type` | `type` 必须是 `user`、`group` 或 `channel`。 |
| `unsupported_conversation_type` | Provider 不支持该 conversation type 的 operation。 |
| `unsupported_message_type` | 所选 provider 不支持 `message.type`。 |
| `unsupported_provider_auth_mode` | 所选 provider 不支持 `auth_mode`。 |
| `auth_mode_phone_required` | 所选 auth mode 要求创建 account 时提供 `provider_data.phone`。 |
| `invalid_reply_token` | `reply_to.reply_token` 被修改、使用其他 key 加密或无法读取；必须原样回传 inbound token。 |
| `create_api_key_failed` | API Key 创建请求被拒绝。 |
| `update_api_key_failed` | API Key 更新请求被拒绝。 |
| `rotate_api_key_failed` | API Key 轮换请求被拒绝。 |
| `create_webhook_endpoint_failed` | Webhook endpoint 创建请求被拒绝。 |
| `update_webhook_endpoint_failed` | Webhook endpoint 更新请求被拒绝。 |
| `deactivate_webhook_endpoint_failed` | Webhook endpoint 停用请求被拒绝。 |
| `delete_webhook_endpoint_failed` | Webhook endpoint 删除请求被拒绝。 |
| `update_workspace_failed` | Workspace 更新请求被拒绝。 |

修正非敏感 input 后重新 preview。不能要求用户把 credential 粘贴到 chat。

## 401 Unauthorized

| Code | 含义 |
| --- | --- |
| `missing_api_key` | 缺少 `X-Api-Key`。 |
| `invalid_api_key` | API Key 无法识别或已禁用。 |

内置 runner 只从 `UNIFYPORT_API_KEY` 获取 key。排查这两个 code 时不能打印它。

## 404 Not Found

| Code | 含义 |
| --- | --- |
| `not_found` | Route 不存在。 |
| `conversation_not_found` | Provider 找不到 conversation。 |
| `contact_not_found` | 该 account 下找不到 contact。 |
| `group_not_found` | 该 account 下找不到 group。 |

不能因为 `not_found` 而猜测其他 route 或 undocumented route。

## 409 Conflict

| Code | 含义 |
| --- | --- |
| `account_allocation_busy` | Allocation lock 正被占用；短暂延迟后 retry。 |
| `no_allocatable_server` | 请求 region 中没有可分配的 provider server。 |
| `workspace_account_quota_exceeded` | Workspace account quota 已用尽。 |
| `duplicate_provider_account` | Workspace 中另一个 account 已使用同一 provider identity。 |
| `account_already_authorized` | Account 已 authorized，因此拒绝该 auth action。 |
| `account_binding_not_found` | Account 未绑定 active provider server。 |

只有 `account_allocation_busy` 明确建议短暂 retry。任何状态变更 retry 前先重新查询状态。

## 500 Internal Server Error

| Code | 含义 |
| --- | --- |
| `create_account_failed` | 创建 account 时发生 server-side error。 |
| `update_account_failed` | 更新 account 时发生 server-side error。 |
| `delete_account_failed` | 删除 account 时发生 server-side error。 |
| `get_account_failed` | 加载 account detail 时发生 server-side error。 |
| `list_accounts_failed` | 列出 account 时发生 server-side error。 |
| `get_session_failed` | 加载 authentication session 时发生 server-side error。 |
| `get_auth_state_failed` | 加载 authentication state 时发生 server-side error。 |
| `run_action_failed` | 运行 account action 时发生 server-side error。 |
| `run_runtime_action_failed` | 运行 runtime action 时发生 server-side error。 |
| `run_session_action_failed` | 运行 session action 时发生 server-side error。 |
| `run_auth_action_failed` | 运行 authentication action 时发生 server-side error。 |
| `send_message_failed` | 发送 message 时发生 server-side error。 |
| `pin_message_failed` | Pin/unpin message 时发生 server-side 或 provider error。 |
| `revoke_message_failed` | Revoke message 时发生 server-side 或 provider error。 |
| `react_message_failed` | Reaction message 时发生 server-side 或 provider error。 |
| `edit_message_failed` | 编辑 message text 时发生 server-side 或 provider error。 |
| `list_conversations_failed` | 列出 conversation 时发生 server-side error。 |
| `get_conversation_failed` | 加载 conversation 时发生 server-side error。 |
| `list_conversation_members_failed` | 列出 conversation member 时发生 server-side error。 |
| `mark_conversation_read_failed` | 标记 conversation read 时发生 server-side 或 provider error。 |
| `mark_conversation_unread_failed` | 标记 conversation unread 时发生 server-side 或 provider error。 |
| `mute_conversation_failed` | Mute conversation 时发生 server-side 或 provider error。 |
| `unmute_conversation_failed` | Unmute conversation 时发生 server-side 或 provider error。 |
| `pin_conversation_failed` | Pin conversation 时发生 server-side 或 provider error。 |
| `unpin_conversation_failed` | Unpin conversation 时发生 server-side 或 provider error。 |
| `list_conversation_labels_failed` | 列出 label 时发生 server-side 或 provider error。 |
| `upsert_label_failed` | 创建或更新 label 时发生 server-side 或 provider error。 |
| `delete_label_failed` | 删除 label 时发生 server-side 或 provider error。 |
| `set_label_members_failed` | 为 conversation 添加或移除 label 时发生 server-side/provider error。 |
| `list_contacts_failed` | 列出 contact 时发生 server-side error。 |
| `get_contact_failed` | 加载 contact 时发生 server-side error。 |
| `block_contact_failed` | Block contact 时发生 server-side 或 provider error。 |
| `unblock_contact_failed` | Unblock contact 时发生 server-side 或 provider error。 |
| `list_blocklist_failed` | 加载 blocklist 时发生 server-side 或 provider error。 |
| `set_contact_note_failed` | 设置或清除 contact note 时发生 server-side/provider error。 |
| `list_groups_failed` | 列出 group 时发生 server-side error。 |
| `get_group_failed` | 加载 group 时发生 server-side error。 |
| `create_group_failed` | 创建 group 时发生 server-side 或 provider error。 |
| `leave_group_failed` | 离开 group 时发生 server-side 或 provider error。 |
| `update_group_members_failed` | 更新 group member 时发生 server-side/provider error。 |
| `update_group_info_failed` | 更新 group name、description 或 avatar 时发生 server-side/provider error，也可能是 admin permission 拒绝。 |
| `list_group_join_requests_failed` | 列出 pending join request 时发生 server-side/provider error。 |
| `update_group_join_requests_failed` | 批准或拒绝 join request 时发生 server-side/provider error。 |
| `set_group_join_approval_mode_failed` | 修改 join-approval mode 时发生 server-side/provider error。 |
| `get_group_invite_code_failed` | 获取 invite link/code 时发生 server-side/provider error。 |
| `list_webhook_endpoints_failed` | 列出 webhook endpoint 时发生 server-side error。 |
| `get_webhook_endpoint_failed` | 加载 webhook endpoint 时发生 server-side error。 |
| `get_workspace_failed` | 加载 workspace 时发生 server-side error。 |
| `list_api_keys_failed` | 列出 API Key 时发生 server-side error。 |
| `list_provider_regions_failed` | 列出 provider region 时发生 server-side error。 |

`500` 不能证明对外可见 write 是否已经到达 provider。不能盲目 retry write、destructive action 或 credential operation；应使用 state read、webhook event 与 `request_id` 对账。

## 501 Not Implemented

| Code | 含义 |
| --- | --- |
| `unsupported_by_provider` | 所选 provider 尚未实现该 endpoint。 |

检查 `provider-capabilities.md`；不能静默切换 provider 或 operation。

## 502 Bad Gateway

| Code | 含义 |
| --- | --- |
| `provider_adapter_not_found` | Provider adapter 不可用或未注册。 |

报告 `request_id`，避免盲目 retry 状态变更。

## 503 Service Unavailable

| Code | 含义 |
| --- | --- |
| `allocation_service_unavailable` | Allocation lock service 不可用；短暂延迟后 retry。 |

使用 bounded backoff 并保留原始脱敏 intent；如果 canonical input 变化，必须生成新的 preview token。
