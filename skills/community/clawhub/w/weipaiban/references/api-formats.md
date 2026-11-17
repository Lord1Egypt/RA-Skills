# 作品发布 API（/api/v1/vectors/svg）

用户接口。HTML 方言见 [dialect.md](dialect.md)。

## 鉴权

| Header          | 来源                | 说明                                    |
| --------------- | ------------------- | --------------------------------------- |
| `Authorization` | `WEIPAIBAN_API_KEY` | `Bearer <sk-...>`，订阅用户或 developer |

key 以 `sk-` 开头，仅通过环境变量传递。用户登录微排版后，在 <https://weipaiban.cn/settings/api-keys> 创建或复制。`scripts/publish.py` 与取素材脚本共用 `scripts/api_base.py`：只接受 `https://weipaiban.cn`（含子域）或本机地址，并校验 TLS 证书。

## 创建

`POST ${WEIPAIBAN_API_BASE}/api/v1/vectors/svg`

```json
{
  "html": "<section data-name=\"作品\">...</section>",
  "title": "春季开学刊",
  "description": "可选说明"
}
```

| 字段          | 必需 | 说明                     |
| ------------- | ---- | ------------------------ |
| `html`        | 是   | trim 后非空，**≤ 512KB** |
| `title`       | 否   | 缺省「未命名作品」       |
| `description` | 否   | 缺省 `''`                |

元素 ≤ 300（含作品根 section）。

成功 HTTP 201：`data.id` / `data.title` / `data.createdAt` / `data.previewId`。
编辑链接：`${WEIPAIBAN_API_BASE}/vectors/{id}`。
预览链接：`${WEIPAIBAN_API_BASE}/links/{previewId}`（临时，约 6 小时）。

## 修改（整份替换）

`PUT ${WEIPAIBAN_API_BASE}/api/v1/vectors/{id}/svg`

请求体与创建相同。用新 HTML 整份替换 `groups` / `elements`。
仅所有者；已发布（`publishedAt` / `prepublishedAt` 非空）不可用。
省略 `title` / `description` 则保留原值。成功 HTTP 200，同样返回 `previewId`。

## 失败

| 状态码 | 含义                                 | 处理                                                         |
| ------ | ------------------------------------ | ------------------------------------------------------------ |
| 400    | JSON 非法 / HTML 解析失败            | 对照 dialect.md：根 section、richText 非空、禁标签、300 上限 |
| 401    | key 缺失/无效/过期                   | 请用户到 <https://weipaiban.cn/settings/api-keys> 创建或复制密钥，并更新 `WEIPAIBAN_API_KEY` |
| 402    | 作品容量已满（仅创建）               | 清理作品或升级年卡                                           |
| 403    | 未订阅且不是 developer               | 与其它 /api/v1 相同                                          |
| 404    | 不存在/非所有者/已发布（仅修改）     | 核对 workId                                                  |
| 413    | html 超 512KB 字符，或整包 JSON 过大 | 图片改用 CDN                                                 |
| 429    | 限流                                 | 稍后重试                                                     |
