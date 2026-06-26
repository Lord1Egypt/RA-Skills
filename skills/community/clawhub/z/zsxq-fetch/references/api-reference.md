# 知识星球 API 参考

## 认证

使用 Cookie 认证，携带 `zsxq_access_token`：

```
Cookie: zsxq_access_token=<token>
```

Token 获取方式：浏览器打开 wx.zsxq.com → 登录 → F12 → Application → Cookies → 复制 `zsxq_access_token` 的值。

## 基础信息

- API 基础 URL: `https://api.zsxq.com/v2`
- 必须携带 Headers:
  - `Cookie: zsxq_access_token=<token>`
  - `Origin: https://wx.zsxq.com`
  - `Referer: https://wx.zsxq.com/`
  - `X-Timestamp: <unix_timestamp>`

## 接口列表

### 1. 获取已加入星球

```
GET /groups
```

响应:
```json
{
  "succeeded": true,
  "resp_data": {
    "groups": [
      {
        "group_id": 12345678901234,
        "name": "星球名称",
        "description": "...",
        "member_count": 1234,
        "topics_count": 5678,
        "owner": { "user_id": 123, "name": "星主" }
      }
    ]
  }
}
```

### 2. 获取帖子列表

```
GET /groups/{group_id}/topics?scope={scope}&count={count}
```

参数:
- `scope`: `all`（全部）| `digests`（精华）
- `count`: 每页数量，最大 30
- `end_time`: 翻页参数，上一页最后一条的 create_time（URL 编码）

响应:
```json
{
  "succeeded": true,
  "resp_data": {
    "topics": [
      {
        "topic_id": 123456,
        "type": "talk",
        "title": "",
        "create_time": "2026-02-20T10:30:00.000+0800",
        "digested": true,
        "likes_count": 10,
        "comments_count": 5,
        "reading_count": 200,
        "readers_count": 473,
        "talk": {
          "owner": { "user_id": 789, "name": "作者" },
          "text": "帖子内容...",
          "images": [
            { "image_id": 789, "type": "jpg" }
          ]
        }
      }
    ]
  }
}
```

帖子类型 (`type`):
- `talk`: 普通发帖（最常见）
- `q&a`: 提问/回答，内容在 `question` 和 `answer` 字段
- `task`: 作业
- `solution`: 解题

### 3. 获取单条帖子详情

```
GET /topics/{topic_id}
```

响应:
```json
{
  "succeeded": true,
  "resp_data": {
    "topic": {
      "topic_id": 123456,
      "type": "talk",
      "title": "",
      "create_time": "2026-02-20T10:30:00.000+0800",
      "digested": true,
      "likes_count": 10,
      "comments_count": 5,
      "reading_count": 200,
      "readers_count": 473,
      "talk": {
        "owner": { "user_id": 789, "name": "作者" },
        "text": "帖子完整内容...",
        "images": [
          { "image_id": 789, "type": "jpg" }
        ]
      }
    }
  }
}
```

帖子链接: `https://wx.zsxq.com/topic/{topic_id}`

## 错误码

| HTTP 状态码 | 含义 |
|------------|------|
| 200 | 成功（但需检查 `succeeded` 字段） |
| 401 | Token 无效或过期 |
| 403 | 无权限（未加入该星球） |
| 429 | 请求过于频繁 |

API 返回 `succeeded: false` 时，错误信息在 `resp_data.error` 或顶层。

## 限速建议

| 操作 | 建议间隔 |
|------|---------|
| 帖子列表翻页 | 1s |
| 多星球切换 | 1.5s |
| 429 重试 | 指数退避 2s/4s/8s |
