# xiaohongshu-mcp API 参考

## 基础信息

- **URL**: `http://localhost:18060/mcp`
- **协议**: JSON-RPC 2.0 over HTTP POST
- **认证**: 通过 `Mcp-Session-Id` header（每次 initialize 从响应 header 获取）

## 请求格式

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "<tool_name>",
    "arguments": { ... }
  },
  "id": <number>
}
```

## 初始化（每次请求前必须）

```python
payload = {
    "jsonrpc": "2.0",
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "xhsmander", "version": "1.0"}
    },
    "id": 1
}
# Session ID 从响应 header "Mcp-Session-Id" 获取
```

## 工具列表

### check_login_status
检查当前登录状态。
- arguments: `{}`
- 返回: 文本 + 是否已登录

### get_login_qrcode
获取登录二维码。
- arguments: `{}`
- 返回: 文本（过期时间）+ image（base64 PNG）

### publish_content
发布图文笔记。
- arguments:
  - `title`: string (≤20字)
  - `content`: string (≤1000字)
  - `images`: string[] (容器内路径，如 `/app/images/xxx.png`)
  - `tags`: string[]
- 注意: 图片路径必须是容器内路径，不是本机路径

### search_feeds
搜索笔记。
- arguments:
  - `keyword`: string
  - `limit`: number (默认10)

### list_feeds
获取首页推荐。
- arguments: `{}` 或 `{limit: number}`

### like_feed
点赞笔记。
- arguments:
  - `feed_id`: string（从搜索/列表结果获取）
  - `xsec_token`: string（从搜索/列表结果获取）

### favorite_feed
收藏笔记。
- arguments: 同 like_feed

### get_feed_detail
获取笔记详情（含评论）。
- arguments:
  - `feed_id`: string
  - `xsec_token`: string

### user_profile
获取用户主页。
- arguments:
  - `user_id`: string
  - `xsec_token`: string

### post_comment_to_feed
发表评论。
- arguments:
  - `feed_id`: string
  - `xsec_token`: string
  - `content`: string

## 图片路径规则

Docker 部署时，图片路径需要特殊处理：

```
本机:  scripts/images/test.png
容器:  /app/images/test.png  (docker-compose 挂载)
MCP:   images 参数传 /app/images/test.png (容器内路径)
```

复制图片到挂载目录：
```bash
cp /本地路径/image.png  scripts/images/
# 调用时传 /app/images/image.png
```

## 错误处理

- `method "tools/call" is invalid during session initialization`: 需要先调用 initialize
- `MCP service not running`: 服务未启动
- 图片文件不存在: 检查容器内路径是否正确
