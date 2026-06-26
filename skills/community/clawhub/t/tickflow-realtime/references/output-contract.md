# Output Contract

## 实时行情

### 单标的 `summary`

输出一段简明摘要，至少包含：

- `symbol`
- `name` 或 `-`
- `region`
- `last_price`
- `change_amount`
- `change_pct`
- `volume`
- `amount`
- `session`
- `timestamp`

### 多标的 `table`

列建议：

- `symbol`
- `name`
- `region`
- `last`
- `chg`
- `chg%`
- `volume`
- `session`
- `time`

### `json`

- 原样输出接口 JSON
- `--pretty` 时使用缩进格式化

## K 线

### 单标的 `summary`

至少包含：

- `symbol`
- `period`
- `bars`
- 最新一根 K 线的 `timestamp/open/high/low/close/volume/amount`

### 单标的 `table`

按时间顺序输出最近若干根 K 线：

- `time`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `amount`

### 多标的 `summary`

每个标的只展示最新一根：

- `symbol`
- `period`
- `time`
- `open`
- `high`
- `low`
- `close`
- `volume`

### `json`

- 原样输出接口 JSON

## 空结果

- 不伪造默认值
- 输出 `No data returned.`

## 错误

- 优先输出 API 的 `code` 和 `message`
- 如果有 HTTP 状态码，一并显示
- 不输出 API Key
