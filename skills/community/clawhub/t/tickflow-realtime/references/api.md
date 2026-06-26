# TickFlow API Notes

本文件只保留实现这个 skill 需要的最小事实，来源是：

- 官网文档页
- `https://api.tickflow.org/openapi.json`

## 认证

- 所有接口通过请求头 `x-api-key` 认证
- 本 skill 统一从环境变量 `TICKFLOW_API_KEY` 读取 API Key

## 实时行情

### GET `/v1/quotes`

- 参数：
  - `symbols`: 逗号分隔字符串
  - `universes`: 逗号分隔字符串
- 适合少量查询

### POST `/v1/quotes`

- Body schema: `QuotesRequest`
- 字段：
  - `symbols: string[] | null`
  - `universes: string[] | null`
- 适合大量标的，避免 URL 过长

### `QuotesResponse`

- 顶层：`data: Quote[]`

### `Quote`

- 必填核心字段：
  - `symbol`
  - `region`
  - `last_price`
  - `prev_close`
  - `open`
  - `high`
  - `low`
  - `volume`
  - `amount`
  - `timestamp`
- 可选字段：
  - `session`
  - `ext`

### 区域与交易时段

- `region`: `CN | US | HK`
- `session`:
  - `pre_market`
  - `regular`
  - `after_hours`
  - `closed`
  - `halted`
  - `lunch_break`

### `ext`

`ext` 是按市场区分的联合类型：

- `cn_equity`
  - `name`
  - `change_amount`
  - `change_pct`
  - `amplitude`
  - `turnover_rate`
- `us_equity`
  - `name`
  - `pre_market_price`
  - `pre_market_change_pct`
  - `after_hours_price`
  - `after_hours_change_pct`
- `hk_equity`
  - `name`

### 百分比字段

TickFlow 的百分比说明是：

- `0.01 -> 1%`

因此展示时应乘以 `100` 再加 `%`。

## K 线

### GET `/v1/klines`

- 单标的
- 参数：
  - `symbol` 必填
  - `period` 可选
  - `count` 可选
  - `start_time` 可选，毫秒时间戳
  - `end_time` 可选，毫秒时间戳
  - `adjust` 可选

### GET `/v1/klines/batch`

- 多标的
- 参数：
  - `symbols` 必填，逗号分隔字符串
  - 其余参数与单标的一致

### `Period`

- `1m`
- `5m`
- `10m`
- `15m`
- `30m`
- `60m`
- `1d`
- `1w`
- `1M`
- `1Q`
- `1Y`

对于这个 skill，默认优先 `1d`。

### `AdjustType`

- `forward`
- `backward`
- `forward_additive`
- `backward_additive`
- `none`

### `KlinesResponse`

- 顶层：`data: CompactKlineData`

### `KlinesBatchResponse`

- 顶层：`data: { [symbol: string]: CompactKlineData }`

### `CompactKlineData`

K 线不是逐根对象数组，而是列式结构：

- `timestamp: int64[]`
- `open: number[]`
- `high: number[]`
- `low: number[]`
- `close: number[]`
- `volume: int64[]`
- `amount: number[]`
- 可选：
  - `prev_close`
  - `open_interest`
  - `settlement_price`

做摘要或表格前，先按索引解压成逐根 K 线对象。

## 错误

错误响应 schema: `ApiError`

- `code`
- `message`
- `details` 可选

## 相关标的池接口

- `GET /v1/universes`
- `POST /v1/universes/batch`
- `GET /v1/universes/{id}`

当用户给的是 `universes` 时，实时行情可以直接透传给 `/v1/quotes`；如果后续要做校验或增强展示，可以再接入这些接口。
