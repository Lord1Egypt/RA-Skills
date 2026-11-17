# 错误码 / 重试 / 超时

> 本文是 `invoke` 与 `content` 两个接口的**异常与重试权威说明**。Agent 遇到任何非 `delivered` 结果时，先按本文判断「这是错误、还是生成中」，再执行对应「应对动作」。

## 1. 一句话判断

- HTTP 200 且 body `status` 为 `delivered` → 拿到结果（`result_url`），展示给用户，提示「该视频由AI生成」，并尽量下载到本地。
- HTTP 200 且 body `status` 为 `generating` → **不是错误**，是生成中，按 `retry_after_seconds` 等待后用同一 `payment_id` 重试 `content`。**视频生成通常需多轮轮询，generating 持续 1-3 分钟属正常**。
- HTTP 200 且 body `status` 为 `refunded` → 终态，已自动退款，告知用户并停止（如需结果重新走 `invoke`）。
- HTTP 402 → 用户还没付钱（`content` 阶段）或需要触发支付（`invoke` 阶段），见下文区分。
- 其余 HTTP（400/404/410/500/502/504）→ 错误，按错误码表处理。

## 2. content 接口的 status 取值

`content` 是**异步状态机**，HTTP 200 不代表已出结果。必须读 body 的 `status` 字段：

| status | HTTP | body 关键字段 | 含义 | Agent 应对动作 |
|--------|------|--------------|------|----------------|
| `delivered` | 200 | `result_url` | 已生成 | 展示 `result_url` 给用户，提示「该视频由AI生成」，并尽量下载到本地 |
| `generating` | 200 | `retry_after_seconds`（=5） | 已支付、生成中，尚无结果 | 等待 `retry_after_seconds` 秒后，用**同一** `payment_id` 重新调 `content`。**不是错误，不要重新 invoke、不要重复扣费** |
| `refunded` | 200 | `refund_amount_fen` / `refunded_at` | 已自动退款的终态 | 告知用户「本次已退款」，停止；若用户仍要结果，重新走 `invoke` |
| `failed` | 502（首次）/ 200（再次回放） | `code` / `msg` / `refund_status` | 生成/提交失败，将自动退款 | 展示 `msg`，告知用户失败将退款；需结果则重新走 `invoke`，**不可复用旧 `payment_id`** |

> `failed` 的 HTTP 码说明：失败**首次**发生在本次 `content` 调用内时返回 HTTP 502（`code` 为 `MCP_SUBMIT_FAILED` 或 `TASK_FAILED`）；之后用同一 `payment_id` 再查，是终态回放，返回 HTTP 200，body 仍为 `status:"failed"`（`code` 可能为 `TASK_TIMEOUT` 等）。无论哪种，按 body `status:"failed"` 处理即可。

`content` 阶段「用户未支付」**不走上表**，而是返回错误响应：

```http
HTTP/1.1 402 Payment Required
Content-Type: application/json

{ "code": "NOT_PAID", "msg": "用户尚未完成支付", "payment_id": "WPAY_xxx", "trade_state": "..." }
```

注意：此处用 **`code` 字段**（值 `NOT_PAID`）标识，body 里**没有** `status` 字段——这与 `invoke` 阶段的 402（带 `WeixinPay-Required`）是两回事，不要混淆。应对：提示用户先完成微信支付授权，稍后用**同一** `payment_id` 重试 `content`。

## 3. 完整错误码表

所有错误响应 body 形如 `{ "code": "<CODE>", "msg": "<中文消息>", ...上下文字段 }`。Agent 必须按 `code` 判断分支，不要依赖 `msg` 文案。

| code | HTTP | 含义 | Agent 应对动作 |
|------|------|------|----------------|
| `INVALID_PRODUCT_ID` | 400 | `product_id` 不在白名单 | 停止。检查 SKILL 配置里的 `product_id`（见 [pricing.md](pricing.md)），修正后才能调用 |
| `MISSING_REQUIRED_FIELD` | 400 | 缺少必填字段 / `prompt` 超 500 字 | 停止。检查入参：`invoke` 需 `product_id` + `prompt`（≤500 字），`content` 需 `payment_id`；补齐后重试 |
| `MERCHANT_ORDER_FAILED` | 502 | 商户下单失败 | 提示用户稍后重试，可重新走 `invoke` |
| `PREORDER_FAILED` | 502 | X402 预下单失败 | 提示用户稍后重试，可重新走 `invoke` |
| `NOT_PAID` | 402 | 用户尚未完成支付 | 提示用户先完成微信支付授权，稍后用**同一** `payment_id` 重试 `content` |
| `PAYMENT_EXPIRED` | 410 | `payment_id` 已过期（>15 分钟）或订单已关闭，对应 `status:"expired"` | 不可复用该 `payment_id`，引导用户**重新走 `invoke`** 发起新一轮 |
| `MCP_SUBMIT_FAILED` | 502 | 生成任务提交失败，将自动退款 | 已触发退款。提示用户失败将退款；需结果则**重新走 `invoke`** |
| `TASK_FAILED` | 502 | 生成失败，将自动退款 | 已触发退款。提示用户失败将退款；需结果则**重新走 `invoke`** |
| `TASK_TIMEOUT` | 504 | 生成超时，将自动退款 | 由后台超时兜底（generating 超过 10 分钟）写入，通常以 `status:"failed"`（`code:"TASK_TIMEOUT"`）回放给 Agent。**视频生成常见**——若用户预期时间不足，可提示预计还需等待。提示用户失败将退款；需结果则**重新走 `invoke`** |
| `NOT_FOUND` | 404 | `payment_id` 不存在 | 停止。核对 `payment_id` 是否来自 `invoke` 返回；如确属本轮，重新走 `invoke` |
| `INTERNAL_ERROR` | 500 | 服务内部异常 | 稍后重试同一请求；持续失败则提示用户稍后再试 |

## 4. 重试规则

| 场景 | 是否可重试 | 怎么做 |
|------|-----------|--------|
| `content` 返回 `generating` | ✅ 必须重试 | 等待 `retry_after_seconds`（5 秒）后，用**同一** `payment_id` 再调 `content` |
| `content` 返回 `NOT_PAID`（402） | ✅ 稍后重试 | 确认用户已完成支付后，用**同一** `payment_id` 再调 `content`；幂等不会重复扣费 |
| `content` 返回 `delivered` | ✅ 可重试（幂等） | 再次请求返回**完全相同**的 `result_url`，不重复生成、不重复扣费 |
| `INTERNAL_ERROR`（500）/ `MERCHANT_ORDER_FAILED` / `PREORDER_FAILED`（502，发生在 `invoke`） | ✅ 可重试 | 稍后重新走 `invoke`（带相同入参，云端按幂等键去重，不重复下单/扣费） |
| `status:"failed"` / `TASK_FAILED` / `MCP_SUBMIT_FAILED` / `TASK_TIMEOUT` | ❌ 旧 `payment_id` 不可复用 | 已/将自动退款。需结果须**重新走 `invoke`** 拿新的 `payment_id` |
| `status:"expired"` / `PAYMENT_EXPIRED`（410） | ❌ 旧 `payment_id` 不可复用 | 引导用户**重新走 `invoke`** |
| `status:"refunded"` | ❌ 终态 | 已退款，需结果须**重新走 `invoke`** |
| `INVALID_PRODUCT_ID` / `MISSING_REQUIRED_FIELD`（400）/ `NOT_FOUND`（404） | ❌ 原样重试无意义 | 先修正入参再调用 |

**幂等保证**：同一 `payment_id` 多次调 `content` 不会重复扣费、不会重复生成；相同入参重复调 `invoke` 由云端幂等键去重，不会重复下单。

## 5. 超时建议

- `content` 单次调用最多约 8 秒返回；未出结果即返回 `generating` + `retry_after_seconds`，**不会**让 HTTP 长时间挂起。
- Agent 侧轮询 `content` 的合理上限：按 `retry_after_seconds`（5 秒）间隔轮询，总时长建议**不超过 10 分钟**。视频生成常见 `generating` 持续 1-3 分钟属正常。生成超过约 10 分钟仍未完成会自动判失败并退款，`content` 随后返回 `status:"failed"`，Agent 应停止轮询并提示用户。
- `payment_id` 整体有效期 15 分钟；超时未支付会变 `expired`。

## 6. 相关文档

| 文档 | 内容 |
|------|------|
| [`invoke-flow.md`](invoke-flow.md) | 完整调用时序、`invoke`/`content` 字段说明 |
| [`pricing.md`](pricing.md) | `product_id` 与定价 |
