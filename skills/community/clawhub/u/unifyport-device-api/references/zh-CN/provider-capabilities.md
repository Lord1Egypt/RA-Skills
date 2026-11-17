# 渠道能力快照

[English](../en/provider-capabilities.md) | [简体中文](provider-capabilities.md)

2026-11-03 从已部署公开矩阵复核；F=完整、P=部分、-=不支持。各渠道独立判断，部分支持不能当作完整支持。

Guide IDs: `provider-message-support`, `provider-actions-support`, `provider-webhook-events`. Matrix IDs: `message-sending`, `actions`, `webhook-events`.

## message-sending

Guide ID: `provider-message-support`. Matrix ID: `message-sending`. [Public guide](https://www.unifyport.ai/zh-CN/docs/provider-guide/provider-message-support/)

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

Guide ID: `provider-actions-support`. Matrix ID: `actions`. [Public guide](https://www.unifyport.ai/zh-CN/docs/provider-guide/provider-actions-support/)

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

Guide ID: `provider-webhook-events`. Matrix ID: `webhook-events`. [Public guide](https://www.unifyport.ai/zh-CN/docs/provider-guide/provider-webhook-events/)

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

## Facebook 边界

仅 session 导入、资料/runtime、E2EE user 会话、单条文本/单个媒体；audio 为部分支持。仅 running 时发送；authorized 不证明已运行。不支持 QR/code、群/频道、引用、mentions、caption、消息操作、联系人、帖子评论与通话。不要从矩阵中的 conversations 读取能力推导详情或写入能力。

四类既有回调为 message.received、account.auth.succeeded、account.status.updated、account.auth.failed。received 可入站或出站；没有 read/delivery receipts。普通 runtime error 不等于撤销授权。上线验收需检查当前部署和真实账号，离线测试不能证明送达。

使用公开 guide 的详细条件；TikTok 与 WhatsApp Protocol 的矩阵结果不代表所有接口、授权方式或环境均可用。Webhooks 先验签、持久化和去重，历史请求为 best effort，不保证补齐漏失事件。
