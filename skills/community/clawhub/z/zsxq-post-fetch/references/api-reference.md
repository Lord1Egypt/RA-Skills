# 知识星球抓取后端参考

本文记录 `fetch_topics.js` 当前支持的两个后端：

- 默认：官方 `zsxq-cli`
- 显式 fallback：legacy HTTP `https://api.zsxq.com/v2`

## 后端选择

默认使用 CLI：

```bash
node fetch_topics.js groups
```

只有显式设置以下任一项时才使用 HTTP fallback：

```bash
export ZSXQ_BACKEND=http
```

```json
{
  "backend": "http"
}
```

`ZSXQ_BACKEND` 优先级高于 `config.json.backend`。

## 官方 zsxq-cli 后端

### 认证

使用官方 OAuth 登录：

```bash
zsxq-cli auth login
```

检查状态：

```bash
zsxq-cli auth status
```

认证 token 由官方 CLI 存入系统 Keychain。`fetch_topics.js` 不读取、不导出、不打印该 token。

### 已加入星球

```bash
zsxq-cli group +list --json --limit 200 --scope all
```

脚本归一化为：

```json
{
  "groups": [
    {
      "group_id": "12345678901234",
      "name": "星球名称",
      "description": "...",
      "member_count": 1234,
      "topics_count": 5678,
      "owner": { "user_id": "123", "name": "星主" }
    }
  ]
}
```

### 帖子列表

```bash
zsxq-cli group +topics --group-id 123456 --limit 30 --json
```

翻页时追加：

```bash
--end-time "2026-06-13T10:30:00.000+0800"
```

脚本会将 CLI JSON 归一化为现有模型：

```json
{
  "topic_id": "789",
  "type": "talk",
  "title": "",
  "text": "帖子内容...",
  "create_time": "2026-03-01T10:30:00.000+0800",
  "owner": { "user_id": "111", "name": "作者" },
  "likes_count": 10,
  "comments_count": 5,
  "reading_count": 200,
  "readers_count": 180,
  "digested": true,
  "image_count": 2,
  "file_count": 1,
  "images": [],
  "files": []
}
```

### 精华帖

官方 CLI 当前通过普通帖子列表返回数据。脚本仅在 CLI JSON 包含以下字段之一时支持本地精华过滤：

- `digested`
- `is_digested`
- `digest`
- `isDigest`

如果列表输出不包含精华标记，返回：

```json
{
  "error": "digests_unavailable_from_cli",
  "hint": "官方 zsxq-cli 输出未包含精华标记；请使用 topics all，或显式设置 ZSXQ_BACKEND=http 使用 legacy HTTP fallback"
}
```

脚本不会自动回退到 HTTP fallback。

### 单帖详情

```bash
zsxq-cli topic +detail --topic-id 82811454228448260 --json
```

用户命令仍保留旧参数形式：

```bash
node fetch_topics.js topic <group_id> <topic_id_or_url>
```

CLI 后端只使用解析出的 `topic_id`，`group_id` 用于兼容输出、附件路径和 Markdown 路径。

### 关键词搜索

```bash
zsxq-cli api call search_topics --params '{"group_id":"123456","query":"SpaceX IPO"}' --format json
```

脚本会对搜索结果执行 `topic +detail` 补全正文、图片和文件字段，然后复用现有 Markdown 与附件下载逻辑。

当前本地 `zsxq-cli api call --help` 文档化的 `search_topics` 参数只有 `group_id` 和 `query`。`count` 是脚本对官方搜索单次返回结果的客户端截断；不要向 `search_topics` 传未文档化的 `limit`、`page`、`cursor` 或 `end_time`。

用户命令：

```bash
node fetch_topics.js search <group_id> <keyword> [count] [--markdown] [--download-attachments]
```

显式 HTTP fallback 不使用新的私有搜索接口，只分页读取已有帖子列表并在本地过滤关键词。

### CLI 错误

| 错误 | 含义 | 建议动作 |
| --- | --- | --- |
| `zsxq_cli_missing` | 未找到 `zsxq-cli` | `npm install -g zsxq-cli` |
| `zsxq_cli_not_authenticated` | 官方 CLI 未登录或登录失效 | `zsxq-cli auth login` |
| `zsxq_cli_non_json` | CLI 未返回 JSON | 检查命令是否支持 `--json` 并确认登录 |
| `zsxq_cli_failed` | CLI 非零退出 | 运行 `zsxq-cli auth status` 或直接执行对应 CLI 命令排查 |

## legacy HTTP fallback

### 认证

HTTP fallback 使用 Cookie 认证：

```http
Cookie: zsxq_access_token=<token>
```

该 token 只能通过环境变量提供：

```bash
export ZSXQ_TOKEN="your_zsxq_access_token"
```

脚本不会从仓库文件、`token.json` 或硬编码默认值读取 token。

### 基础信息

- API 基础 URL：`https://api.zsxq.com/v2`
- 必须携带：`Cookie`、`Origin`、`Referer`、`X-Timestamp`
- 仅当用户显式选择 HTTP fallback 时使用

### 获取已加入星球

```http
GET /groups
```

### 获取帖子列表

```http
GET /groups/{group_id}/topics?scope={scope}&count={count}
```

参数：

- `scope`：`all` 或 `digests`
- `count`：每页数量，最大 30
- `end_time`：翻页参数，上一页最后一条的 `create_time`

### 文件下载 URL

当附件只有 `file_id` 且没有 URL 时，legacy HTTP fallback 会查询：

```http
GET /files/{file_id}/download_url
```

CLI 后端只有在文件对象本身带 `url` 或 `download_url` 时才能直接下载；否则可能需要 legacy token 才能补签名 URL。

### HTTP 错误码

| HTTP 状态码 | 含义 |
| --- | --- |
| 200 | 成功，但仍需检查 `succeeded` |
| 401 | Token 无效或过期 |
| 403 | 无权限或未加入星球 |
| 429 | 请求过于频繁 |

API 返回 `succeeded: false` 时，错误信息通常在 `resp_data.error` 或顶层字段中。

### 限速与重试

| 操作 | 策略 |
| --- | --- |
| 帖子列表翻页 | 间隔约 1s |
| 文件下载 | 间隔约 500ms |
| HTTP 429 或网络错误 | 约 2s/4s/8s 指数退避，并加入 ±25% 随机抖动 |

## 1059 说明

`code: 1059` 表示知识星球已检测并阻止非官方客户端访问。默认 CLI 后端通过官方认证路径访问，不实现伪造官方客户端、伪造 TLS/header 指纹或绕过风控逻辑。

如果 HTTP fallback 遇到 1059，应切回默认 CLI：

```bash
unset ZSXQ_BACKEND
zsxq-cli auth login
node fetch_topics.js groups
```
