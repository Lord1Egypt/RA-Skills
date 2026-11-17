# UnifyPort Device API 概览

[English](../en/overview.md) | [简体中文](overview.md)

## 公开边界

本 Skill 覆盖 [UnifyPort API 文档](https://www.unifyport.ai/zh-CN/docs/#introduction)中已发布的内容：workspace、account、authentication、runtime、message、conversation、contact、group、API Key、webhook endpoint、provider region、provider guide、error 与标准 webhook event。

固定 API origin 为 `https://api.unifyport.ai`。Live request 使用 `X-Api-Key` 认证，且只能从 optional `UNIFYPORT_API_KEY` environment variable 读取。

使用 `../operations.json` 解析 action，使用 `../events.json` 解析 event type。这两个 catalog 是 executable allowlist；不能根据猜测的 path 或 server response 推导未公开 operation。

## 模式

### `docs-only`

用于解释、准备 request、生成代码示例、回答 provider capability、分析 error 与设计 webhook。不读取 API Key，也不发送 network traffic。

### `read`

只有在用户明确请求当前 workspace 数据时使用。解析一个 allowlist read action，展示 target 与脱敏 parameter，再通过内置 runner 执行。实际 request 包含敏感 identifier/value 时使用 `--input-stdin`。尽量缩小 page size，并对敏感 record 做摘要。

### `write`

Allowlist 中改变状态的 action 必须先展示脱敏 preview，并取得 catalog 定义的 confirmation 后才能执行。敏感 request input 使用 `--input-stdin` 传入完整 `{params,query,body}` object；确认执行时再次提供同一个 object。任何 normalized input 变化都会使 confirmation 失效。

### `credential`

只有用户显式 opt-in 时，才能用于 allowlist 中涉及 authentication、session、password、API Key 或 signing secret 的 action。完整 request 必须使用 `--input-stdin`。不能在 chat 中索要 secret、把它作为命令参数传递或在普通 output 中复现。

Destructive action 是 `write` 的更严格子集，需要用户明确表达 destructive intent。

## 公开概念

- Workspace 是由 API Key 解析的隔离边界。
- Account 代表一个 provider login，并暴露 authentication 与 runtime state。
- Message 使用 normalized request shape，但实际能力取决于 provider。
- Webhook 传递 inbound traffic 与 lifecycle event；应验证 signature，并只保存 application 需要的数据。
- Response 包含 `request_id`；报告失败时使用该值，不要附带敏感 body。

需要详细 semantics 时，打开选定 catalog entry 中保存的英文或简体中文 URL。
