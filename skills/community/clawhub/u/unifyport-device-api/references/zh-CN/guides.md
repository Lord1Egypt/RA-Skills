# 公开 Guide 快照

[English](../en/guides.md) | [简体中文](guides.md)

本文件汇总 9 个公开概念与授权 guide，不包含抓取的 payload、客户 identifier、手机号、session 或 credential。Operation request field 与执行策略仍以 `../operations.json` 为准。

Guide ID：`introduction`、`quickstart`、`account-lifecycle`、`provider-auth-telegram`、`provider-auth-line`、`provider-auth-zalo`、`provider-auth-twitter`、`provider-auth-whatsapp`、`provider-auth-facebook`。

## Introduction

UnifyPort 为 Telegram、WhatsApp、LINE、X (Twitter)、Zalo 与 TikTok 提供一个 REST API 和一个 normalized webhook event stream。当前公开 operation 与 capability 细节只覆盖对应 guide 中明确出现的 provider；没有 matrix 或 authorization guide 时，不能推断 TikTok behaviour。

- `Workspace`：隔离边界。`X-Api-Key` 只解析到一个 workspace，request body 不需要额外 workspace id。
- `Account`：一个 provider login，可视为一台虚拟设备。先创建、完成支持的 authorization flow，再通过它收发消息。
- `Runtime`：account 背后的 live connection。授权成功后自动启动；`runtime_status` 暴露连接状态。
- `Webhook`：已观察消息流量的主要记录。消息历史不持久化，漏掉的 event 不能重放，因此应先注册 receiver，并在到达时只保存需要的数据。

所有 live request 使用 `https://api.unifyport.ai` 与 `X-Api-Key`。每个成功或错误 response 都包含顶层 `request_id` 和 `X-Request-Id` response header。Caller 自带的 `X-Request-Id` 会回显为 `client_request_id`，用于对账。

## Quickstart

公开 WhatsApp quickstart 的顺序是：

1. 使用 `get-workspace` 验证访问权限。
2. Authentication 前用 `create-webhook` 注册 webhook；`subscribed_events: ["*"]` 表示有意识地订阅全部标准 catalog。
3. 针对 `whatsapp` 调用 `provider-regions`，选择 `allocatable: true` 的 region；否则创建 account 可能返回 `409 no_allocatable_server`。
4. 使用 `create-account`，设置 `provider: whatsapp`、已选择的 region、`auth_mode: code` 与 `provider_data.phone: <E164_DIGITS>`。
5. 用空 body 调用 `start-code-auth`。公开 API 会返回 transient `auth_payload.verify_code`，供用户在约三分钟内输入手机。本 safe runner 会脱敏该值；确需展示时，产品必须使用 Agent chat 之外的受控 UI 或 secure destination。等待 `account.auth.succeeded`，随后等待 `account.started`；runtime 会自动启动。
6. 使用 message-specific catalog entry `send-text-message`，传入 `<ACCOUNT_ID>` 与 provider 格式的 recipient placeholder。
7. 接收 `message.received`、验证 delivery signature，并只保存 application 需要的 field。

第 2、4、5、6 步会改变状态或涉及 credential，必须遵守 runner 的 preview、confirmation、opt-in 与 stdin 规则。

## Account Lifecycle

Account 有三个互相独立的状态维度：

| 维度 | Owner 与来源 |
| --- | --- |
| `status` | Caller 管理的业务开关，在 create 或 update 时设置。 |
| authentication `status` | 平台管理，通过 `GET /v1/accounts/{account_id}/auth` 读取。REST account object 本身没有 `auth_status` field。 |
| `runtime_status` | 平台管理的 live connection state，位于 account object 上。Webhook payload 同时暴露 `auth_status` 与 `runtime_status`。 |

Authentication state：

| State | 含义 |
| --- | --- |
| `pending_auth` | 初始状态，或没有 active flow。 |
| `awaiting_qr_scan` | QR flow 进行中；`auth_payload` 携带渲染材料。 |
| `awaiting_code` | Verification-code flow 进行中。 |
| `awaiting_password` | Provider 要求 two-factor password。 |
| `authorized` | Authentication 完成；runtime 自动启动。 |
| `failed` | Flow 失败；`last_error` 可能携带原因。 |

`/auth/qr/start` 进入 QR 等待，`/auth/start` 进入 code 等待，password challenge 进入 `awaiting_password`，用户操作成功后进入 `authorized`。`/auth/cancel` 放弃等待中的 flow。Provider failure 触发 `account.auth.failed`；session 失效触发 `account.auth.required`，需要 fresh flow。已经 authorized 时重新 start 或 import authentication 会返回 `409 account_already_authorized`；只有确实需要重新认证时才先 cancel。

Runtime state 包括 `unknown`、`starting`、`running`、`reconnecting`、`disconnected`、`stopping`、`stopped` 与 `error`。Authorization 通常驱动 `starting` 到 `running`；显式 start、stop、reconnect 与 refresh 用于恢复或 operator control。应通过 `account.status.updated` 同步变化，避免频繁 polling。

## Provider Authorization

除非 catalog 明确另有分类，所有 authorization action 都属于 `credential` risk。不能把 code、password、session material、QR material、proxy credential 或 API hash 放进 chat 或 command argument。Preview 与确认执行都必须通过 `--input-stdin` 提供完整 `{params,query,body}` request。

部分旧 provider-flow 步骤仍在成功后显式调用 runtime start。当前 introduction、quickstart 与 lifecycle 契约明确授权成功会自动启动 runtime；该显式 start 只是 idempotent compatibility step，并非必需。

### Telegram

支持 `code`、`qrcode` 与 `session`。

- `code`：创建时提供 `provider_data.api_id`、`provider_data.api_hash` 与 `provider_data.phone`；发起 flow、提交收到的 code，只有状态进入 `awaiting_password` 时才提交 two-factor password。
- `qrcode`：创建时提供 `provider_data.api_id` 与 `provider_data.api_hash`；启动 QR 并 check 直到 authorized。QR token 约 30 秒过期，应重新 start 获取新 token，不能复用过期值。
- `session`：使用 `auth_mode: session` 创建，再将顶层 body field `session_url` 作为高价值 secret material 导入。
- 2FA 输入错误后需要 cancel 并重新开始 flow。Authentication transition 通过已配置的 webhook 到达。

### LINE

LINE 只支持 `qrcode`，`metadata.device_login_type` 可选。公开 guide 说明 QR URL 与只用于展示的 PIN 通过 `account.auth.required` 异步到达，不会在 QR start 中同步返回。本 runner 会脱敏这些 credential-sensitive material；确需展示时，产品必须使用 Agent chat 之外的受控 UI 或 secure destination。Guide 还描述了缓存 auth-session 的 read，但该 read 不在本 Skill 的 public operation catalog 中，因此不能自行构造。请使用 webhook 与 catalog 中的 QR-check flow。

成功后会填充 `provider_account_ref`，也可能出现标准 profile field。QR/PIN material 应视为敏感展示数据。

### Zalo

Zalo 只支持 `qrcode`，不需要预先提供 credential。QR start 返回渲染材料，QR check 完成 flow；出现 `qrcode_expired` 时必须重新 QR start。需要 webhook endpoint 来接收 authentication 与 message event。公开说明中 thread type `0` 表示 user/friend，`1` 表示 group；发送时会归一化该差异。

### Twitter / X

X 只支持 `session` import，没有公开 QR 或 code flow。使用 `auth_mode: session` 创建 account，再导入顶层 body field `session_url`。顶层 body field `pin` 可选；公开 guide 对未启用 2FA 的 export 使用 literal fallback `"0000"`；顶层 body field `proxy_config` 可用于 geographic routing。Export 与任何 proxy credential 都是高价值 secret。

Provider guide 中的 `params.session_url`、`params.pin` 与 `params.proxy_config` 表示 provider-action parameter。在公开 request 与本 runner 中，它们是顶层 body field，不是名为 `params` 的 nested object。

### WhatsApp

支持 `qrcode` 与 `code`。

- `qrcode`：创建时可选 `provider_data.device_os`、`provider_data.device_platform` 与 `provider_data.proxy_config`。QR start 进入 `awaiting_qr_scan`；实际 QR material 通过 `account.auth.required` 到达，也可通过 catalog 中的 QR-check action 检查。成功后依次触发 `account.auth.succeeded` 与 `account.started`。
- `code`：创建 account 时保存 `provider_data.phone: <E164_DIGITS>`。使用空 body 发起 code auth。公开 API 会返回 `auth_payload.verify_code`，供用户在约三分钟内输入手机，但本 safe runner 会脱敏该值；传递必须使用 Agent chat 之外由 caller 控制的 UI 或 secure destination。该 code 不回传给 API。
- 配对成功会自动启动 runtime；之后调用 runtime-start 是 no-op。

Provider-specific message、action 与 event 支持必须读取 `provider-capabilities.md`，不能根据授权成功推断。


## provider-auth-facebook

[公开授权指南](https://www.unifyport.ai/zh-CN/docs/provider-guide/provider-auth-facebook/)

1. 查询 region 并选择 allocatable=true；create-account 使用 provider=facebook、auth_mode=session。
2. 获授权的 Cookie JSON 仅存于短时受控 session_url；导入使用 credential opt-in、stdin 和 HMAC 确认。Cookie 文件结构以公开指南为准，包含 cookies 数组及 c_user、xs、datr；不要将值贴入聊天或日志。
3. 授权成功后查询 runtime；starting 等待后有界刷新、stopped 仅在明确意图后 start，running 才发送。不得自动 reconnect 或重试不确定写入。
4. 从同步的 E2EE type=user 会话获取字符串 ID；仅单条文本/单个媒体，无 caption、mentions、引用或群。audio 部分支持。先配置 active Webhook 并持久化去重，再触发业务。
