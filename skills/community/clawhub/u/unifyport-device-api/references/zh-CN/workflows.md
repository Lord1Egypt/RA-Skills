# 安全 Workflow

[English](../en/workflows.md) | [简体中文](workflows.md)

## 回答文档问题

1. 保持 `docs-only`，不能读取 `UNIFYPORT_API_KEY`。
2. 找到相关 guide、catalog `id`、`operationId` 或 event type。
3. 阅读 catalog metadata，以及符合用户语言的公开文档链接。
4. 解释 request field 与 provider caveat，但不能虚构默认值。
5. 使用 `<ACCOUNT_ID>`、`<YOUR_API_KEY>` 等 placeholder；不能将之前 output 中的真实值代入示例。

## 查看当前数据

1. 确认用户需要 live call，而不是示例。
2. 只选择一个 allowlist read operation。
3. 只收集必需的 path/query input，并选择最小可用 page。Identifier 属于敏感数据时，按 runner 要求通过 `--input-stdin` 提供完整 `{params,query,body}` object。
4. 预览固定 origin、method、脱敏后的 path value 与 operation ID。
5. 通过内置 runner 执行，并总结脱敏结果。

Read result 可能包含 personal data。除非用户有明确需求且 output 能够被安全处理，否则不能粘贴完整 contact、conversation、membership 或 message dataset。

## 发送或修改 Message

1. 在公开 provider capability guide 中检查请求的 message type 或 action。
2. 确认精确 account、recipient 或 conversation、content/action 与用户意图。
3. 即使多个 action 共享 `POST /v1/messages`，也要选择 message-specific catalog entry。
4. 使用完整 `--input-stdin` object 提供敏感 identifier 与 content，生成脱敏 preview，并请求 runner 要求的精确 confirmation。
5. 只执行一次。Preview token 五分钟后过期；即使仍有效，execution attempt 后也不能复用。Ambiguous timeout 后不能自动 retry；应先使用 `request_id` 与 provider state 对账，明确需要再次 attempt 时重新生成 preview。

## 管理 Account 与 Runtime

Account create/update/delete、authorization、start/stop/reconnect 和 group membership change 都是状态变更 action。Delete、leave group、revoke 等不可逆或对外可见 action 需要用户明确表达 destructive intent。

Authentication code、two-factor password、QR payload 与 imported session 都是敏感数据。不能放入 prompt 或普通 output；只能从受控 input channel 通过 `--input-stdin` 提供完整 request。

## 注册 Webhook Endpoint

1. 使用用户拥有的 HTTPS destination；不能虚构或探测 callback URL。
2. 只选择必需的标准 event subscription，或有意识地使用文档定义的 wildcard。
3. 将 `signing_secret` 与 endpoint URL 视为敏感 input，通过 `--input-stdin` 发送完整 request，输入后不能展示 secret。
4. 在解析 JSON 前，基于精确 raw request body 实现 signature verification。
5. 快速 acknowledgement、保持 handler idempotent，并只保存必要数据。

当前 header、signature、retry 与 ordering contract 以公开 webhook delivery guide 为准。

## 创建或轮换 API Key

这些属于 `credential` operation。执行前确认预期的 key scope/status 与安全目的地。公开 API 可能只返回一次 plaintext，但本 safe runner 会脱敏；产品确需接收时，必须使用 Agent chat 之外由 caller 控制的 secure destination。不能将其写入 Agent history、console log 或 repository file。Rotate 还会改变旧凭据的有效性，不能作为常规 troubleshooting 操作执行。

## 处理 API Error

1. 记录 HTTP status、public error code 与 `request_id`。
2. 解释失败前先脱敏 request/response field。
3. 检查公开 error reference 与 provider capability guide。
4. 请求缺失的非敏感 input；不能要求用户粘贴 API Key 或 session。
5. 只在合适时 retry read。不能盲目 retry write、destructive action 或 credential operation。


## Published contract update 2026-11-03

账号分页使用 list-accounts 的 query.limit/cursor，保留 data.next_cursor，限制页数；创建的可选 headers.Idempotency-Key 由调用方持有，同一逻辑购买重试时原样使用，键也绑定 HMAC。完整输入通过 --input-stdin 提供；不能传认证头。202 删除仅表示受理，使用 get-account-operation 有界查询；204 没有操作 ID。REVIEW 待核对，SUCCEEDED 不证明退款到账或授权可用。

create-auth-session、submit-passkey-response（webauthn_response 为完整 JSON 字符串）、confirm-passkey 为 credential 操作。对象 proxy 为公开字段但需严格公网出口检查；auth_mode 切换只能单独 PATCH，省略/空对象/空数组清除按契约区分，不将 null 当默认值。

add-contact 与 get-contact-membership 遵循 WhatsApp LID 规则，false 为有效结果；history 的 before 必须来自同一条真实内容消息，保留 sent_at 原文，不能使用合成 call_record ID，202 不保证回调或完成。帖子 ID/评论 ID 保持非空字符串；get-post/list-post-comments 是 POST 读取，不需要写确认，reply-post-comment 需要 HMAC，comment_id 只引用已确认的一级评论。

create-call 为显式写入，hangup-call 需 destructive opt-in 和 HMAC；服务端 private beta/is_beta 资格仍然适用，不自动拨号。join_url、授权 URL、WebAuthn、provider_profile、reply_token 不能进入模型输出；本 runner 脱敏，需展示链接时使用聊天之外的受控 UI。get-active-call 为只读；null 表示无活动通话，挂断可能返回 ended 或 failed，均为终态。

## 协议导入、标签及已读回执

嵌套 whatsapp-protocol 对象使用 import-auth-session，必须遵守必填密钥、stdin、脱敏和 credential/HMAC 规则。旧 X session_url/pin/proxy_config 继续可用。list-conversations 的 query.label_id 原样保留为字符串；WhatsApp 省略它表示特别关注会话。WhatsApp 消息已读成对提供 up_to_message_id 和 up_to_message_sender_id，群消息 sender 取 data.sender.id；Telegram 使用单个已接收消息 ID，不支持非空 sender。runner 不能推断渠道。空值及渠道限制参见[迁移说明](migration.md)。

## 账号独立 Webhook 配置

list/get/deactivate/delete 接受 query.account_id，create/update 接受 body.account_id。list 省略时选 workspace 端点，筛选时只选独立账号端点。create 可绑定账号，update 只校验原绑定。PATCH 是替换操作，保留设置及 signing secret 必须重新提交。account_webhook_already_exists 不自动重试。停用或订阅不匹配不会回退 workspace，参见[迁移说明](migration.md)。
