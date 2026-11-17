# 发布说明 — 1.1.0

[English](../en/release-notes.md) | [简体中文](release-notes.md)

状态：未发布候选版本。本地验证和 ClawHub dry-run 不代表发布；最终公开证据人工签核仍待完成。

## 相比 1.0.0 的变化

- 包含此前合入的公开操作追踪、授权会话及 Passkey、联系人归属、会话历史、帖子/评论和通话动作。覆盖 82 个动作、78 条路由、24 个事件；数量不代表无限制支持所有参数。
- 补充 Facebook session 授权、authorized 与 runtime 就绪分离、E2EE user 会话、单条文本/单媒体、audio 部分支持及四类既有标准回调；不新增 FB 已读/投递事件，不推断 duration 单位。
- 补齐九个既有动作的字段：import-auth-session 的嵌套 WhatsApp Protocol 凭证、list-conversations 的 label_id、mark-conversation-read 的 up_to_message_sender_id，以及六个 Webhook 动作在各自公开位置的 account_id。
- 协议导入校验精确嵌套 schema、必填密钥、int32/uint32 和 boolean；拒绝 edge_routing、借 provider_data 传递协议凭证及非公网上游地址。必须使用完整 stdin、credential opt-in、HMAC，并对整体对象和散落密钥脱敏。
- 保留调用方 Idempotency-Key 确认、稀疏值、不透明 ID、纳秒时间字符串、旧 X session/PIN/proxy 输入及账号 PATCH 顶层空 proxy 清除语义。
- package、中英文 Skill 元数据、runner User-Agent 及 ClawHub 显式版本统一为 1.1.0。增加版本、证据和精确文件清单门禁，将 ignore 规则纳入签核，并在任何上传前匹配无 token 的官方 CLI dry-run。质量测试同时支持待签核及已签核状态；仅上传 Skill 目录。

## 限制及发布条件

update-account.provider_account_ref 的可写身份语义待澄清，继续拒绝。消息别名保留按意图拆分的 allowlist。渠道业务合法性及 Webhook 归属由服务端验证，本地不作推断。协议上游服务器覆盖遵循 runner 更严格的公网主机策略。未进行真实账号业务验收。参见[迁移说明](migration.md)。
