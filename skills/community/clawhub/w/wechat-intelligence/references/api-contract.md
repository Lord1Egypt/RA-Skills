# 曼格云 API 调用规范

配置接口调用、预估费用或诊断接口响应时阅读本文件。以下价格已于 2026-08-25 对照公开产品目录核验，真实费用始终以响应中的 `consumption` 为准。

## 身份验证

- 接口根地址：`https://api.we-media.cn`
- 请求头：`X-API-Key: <MANGYUN_API_KEY>`
- JSON 请求必须携带 `Content-Type: application/json`。
- 每次调用都要发送 `Idempotency-Key`；重试同一次请求时必须保持原值。

## 发现历史文章

```text
POST /openapi/wechat-native-account-articles/accounts/articles
价格：每页 0.035 元
```

请求体只能使用一种公众号标识：

```json
{"ghid":"gh_xxxxxxxxxxxx","offset":0,"limit":20}
```

或者：

```json
{"url":"https://mp.weixin.qq.com/s/ARTICLE","offset":0,"limit":20}
```

主要响应字段包括 `data.account`、`data.items`、`data.nextOffset`、`data.hasMore`、`balance` 和 `consumption`。每篇文章可能包含 `url`、`title`、`digest`、`coverUrl`、`author`、`publishTime`、`publishTimestamp`、`biz`、`mid`、`idx`、`sn` 和 `contentType`。

固定使用 `limit=20`，减少每页条数不会降低单页价格。增量扫描从偏移量 0 开始，遇到已知文章标识时停止。只有在 `hasMore=true` 且尚未找到已知边界时才继续翻页。

## 获取纯文本正文

```text
POST /openapi/wechat-native-article-content/articles/content
价格：使用 format=text 时，每篇 0.021 元
```

```json
{"url":"https://mp.weixin.qq.com/s/ARTICLE","format":"text"}
```

主要响应字段包括 `data.article`、`data.format`、`data.content`、`balance` 和 `consumption`。

情报分析不得使用 `format=html`。它费用更高，而且增加的标签不会改善模型的事实输入。

## 错误处理

- 非 2xx 的 HTTP 响应视为调用失败。可以记录公开错误码和错误信息，但不得记录密钥或请求头。
- HTTP 请求成功但缺少预期的 `data.items` 或纯文本 `data.content` 时，该结果不可使用。将项目保留为待处理或失败状态，不得虚构数据。
- 自动重试必须复用同一个幂等键。参数校验、身份验证或余额不足错误不得盲目重试。
