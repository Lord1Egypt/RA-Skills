# TradeAlpha 实时新闻接口参考

适合投喂 AI：可将本页链接或正文直接提供给 AI，用于快速生成接入代码、请求示例与参数处理逻辑。

## 接口说明

1. 提供国内外新闻实时数据，来源包括但不限于：路透社（含终端）（华区与国际 Top）、彭博社（交易时间终端）（华区与国际 Top）、川普 Truth 平台发言、研报快讯、以及国内主流消息源等。
2. 受采集与传输链路影响，所有消息通常存在约 `0-5` 分钟的延迟；该延迟为客观限制，无法通过技术手段完全消除，接入方请按此预期设计展示或产品说明。
3. 支持按新闻源、重要程度、新闻分类等条件筛选，并可结合请求中的时间范围等参数。

## 请求

### HTTP 方法

```text
POST /api/v1/news/realtime_news
```

### 请求体参数

- `token`：`string`，必填。API 访问令牌，从开放平台申请获得。
- `start_time`：`string`，可选。可只传日期 `YYYY-MM-DD`；若需指定到时刻，须为 `YYYY-MM-DD HH:mm:ss`。
- `end_time`：`string`，可选。可只传日期 `YYYY-MM-DD`；若需指定到时刻，须为 `YYYY-MM-DD HH:mm:ss`。
- `source`：`string`，可选。可选值：
  - `domestic`：国内，库内为 `ths` / `sina`
  - `truth`：川普 Truth
  - `bloomberg`：彭博
  - `rtrs`：路透社
  - `research_report`：研报快讯
- `category`：`string`，可选。传中文全称：
  - `政治军事`
  - `社会`
  - `娱乐体育`
  - `公司`
  - `超大型公司`
  - `政策`
  - `市场与货币`
- `level`：`string`，可选。重要程度：`很重要`、`重要`、`一般`
- `page`：`integer`，可选。页码，默认 `1`
- `page_size`：`integer`，可选。每页条数，默认 `20`，最大 `100`

## 注意事项

- `start_time` 与 `end_time` 均为可选参数，若不传则默认时间范围为近 24 小时。
- 时间下界：新闻时间不能早于 `2025-04-01`（北京时间）。
- 若显式传入的 `start_time` 或 `end_time` 落在该时间之前，将返回 `code: 1002`。
- 未传 `start_time` 时，按默认规则算出的开始时间若早于该下界，将自动从 `2025-04-01`（北京时间）起算。
- 单次请求 `page_size` 上限为 `100`，如需获取更多数据请配合 `page` 参数分页拉取。
- 接口请求频率限制为每分钟不超过 `50` 次；超出限制将返回 `code: 1003`。

## 响应

### 响应字段

- `code`：状态码，`0` 表示成功
- `message`：状态描述
- `data.total`：符合条件的新闻总条数
- `data.page`：当前页码
- `data.page_size`：每页条数
- `data.list`：新闻列表
- `data.list[].id`：新闻唯一 ID
- `data.list[].datetime`：新闻发生时间，格式 `YYYY-MM-DD HH:mm:ss`
- `data.list[].content`：新闻正文内容
- `data.list[].source`：单条新闻的展示用来源
- `data.list[].category`：新闻分类
- `data.list[].level`：重要程度

成功响应中，`data.list[]` 不包含 `import_content` 字段。

## 错误码

- `0`：成功
- `1001`：token 无效或已过期
- `1002`：请求参数错误
- `1003`：超出请求频率限制
- `1004`：账户余额不足或无权限访问该接口
- `5000`：服务器内部错误

## 页面链接

- [TradeAlpha Open Platform](https://quantaccess.lxaa.top/)
