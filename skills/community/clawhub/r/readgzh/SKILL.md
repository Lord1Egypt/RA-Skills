# ReadGZH -- 微信公众号文章 AI 阅读器 / WeChat Official Account Article AI Reader

<!-- Chinese Section -->

## ReadGZH -- 微信公众号文章 AI 阅读器

ReadGZH 是一款专为 AI 智能体设计的微信公众号内容解析工具。它通过服务端 API 将复杂的公众号 HTML 转换为纯净、结构化的 Markdown 内容，大幅节省 Token 消耗。

## 核心功能

- **99.89% 解析成功率**：自研 7 阶段提取管线，精准提取公众号文章内容
- **50-87% Token 节省**：自动剥离冗余标签及广告干扰，输出极简 Markdown
- **CDN 图片代理**：将图片路由至持久化 CDN，解决微信图片 2 小时过期的硬伤
- **全球共享缓存**：转换过的文章永久入库，后续任何用户或 Agent 读取均完全免费
- **零安装依赖**：纯云端 API 模式，无需本地微信客户端或浏览器环境
- **原生支持 MCP**：内置 Model Context Protocol，支持 AI Agent 协议化直接调用

## 如何使用

直接对你的 AI 助手下令：

> "帮我读一下这篇微信公众号文章：[链接]"

## 可用工具

| 工具 | 说明 |
|------|------|
| readgzh.read | 通过 URL 读取微信文章全文 |
| readgzh.get | 通过 slug 获取已缓存文章（支持分页和摘要） |
| readgzh.search | 按关键词搜索已缓存文章 |
| readgzh.list | 列出最近缓存的文章 |

## API 端点说明

### GET /rd — 读取文章

| 参数 | 说明 |
|------|------|
| url | 微信文章链接（mp.weixin.qq.com） |
| s | 文章 slug（用于读取已缓存文章） |
| part | 分块编号（长文章自动拆分约 40KB/块，从 1 开始） |
| format | 设为 `text` 返回纯 Markdown（推荐 AI 使用） |
| mode | 设为 `summary` 返回 AI 结构化摘要（Pro 专属） |

### HEAD /rd — 健康检查

检查 API 服务是否在线：

```
HEAD https://api.readgzh.site/rd
```

返回 `200 OK` 即表示服务正常。

## API 接入方式

### MCP 协议（推荐）

在 OpenClaw 配置中添加：

```json
{
  "mcpServers": {
    "readgzh": {
      "url": "https://api.readgzh.site/mcp-server"
    }
  }
}
```

### REST API

```bash
# 方式一：GET 直接抓取（推荐 AI 使用）
curl "https://api.readgzh.site/rd?url=https://mp.weixin.qq.com/s/xxxxx" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# 方式二：POST 抓取并缓存
curl -X POST "https://api.readgzh.site/rd" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/xxxxx"}'

# 读取已缓存文章（Markdown 格式）
curl "https://api.readgzh.site/rd?s=article-slug&format=text" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# 长文分页读取（第 2 部分）
curl "https://api.readgzh.site/rd?s=article-slug&part=2" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# AI 智能摘要（Pro 专属）
curl "https://api.readgzh.site/rd?s=article-slug&mode=summary" \
  -H "Authorization: Bearer <YOUR_API_KEY>"
```

## Credits 说明

| 类型 | 消耗 |
|------|------|
| 简单文章（< 5 图）| 1 credit |
| 复杂文章（≥ 5 图）| 2 credits |
| 缓存文章读取 | 免费 |
| 免费额度 | 每日 30 credits（需在控制台点击「领取今日积分」） |
| Pro 订阅 | 每月最高 2,000 credits（自动发放） |

## 错误码

| 状态码 | 含义 |
|--------|------|
| 401 | 未提供 API Key 或 Key 无效 |
| 402 | API Key 积分已用完，响应包含 pricing_url 引导充值 |
| 403 | 功能需要 Pro 套餐（如 `?mode=summary`） |
| 429 | 超出频率限制（匿名用户每日 10 次） |

## 使用须知

- 支持微信公众号普通图文文章和图片消息（小绿书）两种格式
- 仅支持微信公众号链接（mp.weixin.qq.com）
- 文章内容会自动缓存，重复请求不会重新抓取
- 图片消息会提取所有图片和文字描述
- 请遵守相关法律法规，仅用于个人学习和研究

## 隐私说明

- 文章内容会被全局缓存，其他用户也可能访问
- 请勿提交包含隐私或敏感信息的公众号链接
- 建议使用自己的 API Key，而非共享凭据

## 开发者信息

- **API 文档**：https://readgzh.site/docs
- **免费 API Key**：https://readgzh.site/dashboard
- **技术支持**：https://readgzh.site
- **开发维护**：Sweesama（@sweesama）

---

<!-- English Section -->

## ReadGZH -- WeChat Official Account Article AI Reader

ReadGZH is a WeChat article parsing tool designed for AI agents. It converts complex WeChat HTML into clean, structured Markdown, reducing Token consumption by 50-87%.

## Core Features

- **99.89% Success Rate**: 7-stage extraction pipeline for accurate article parsing
- **50-87% Token Savings**: Automatic removal of redundant tags and ad interference
- **CDN Image Proxy**: Permanent image access, no 2-hour WeChat image expiry
- **Global Shared Cache**: Converted articles are permanently cached and freely accessible
- **Zero Installation**: Cloud API mode, no local WeChat client required
- **MCP Native Support**: Built-in Model Context Protocol for AI Agent integration

## How to Use

Just tell your AI assistant:

> "Read this WeChat article: [link]"

## Available Tools

| Tool | Description |
|------|-------------|
| readgzh.read | Read a WeChat article by URL |
| readgzh.get | Get a cached article by slug (supports pagination and summary) |
| readgzh.search | Search cached articles by keyword |
| readgzh.list | List recently cached articles |

## API Endpoints

### GET /rd — Read Article

| Parameter | Description |
|-----------|-------------|
| url | WeChat article URL (mp.weixin.qq.com) |
| s | Article slug (for cached articles) |
| part | Chunk number (long articles auto-split ~40KB/chunk, starting from 1) |
| format | Set to `text` for plain Markdown (recommended for AI) |
| mode | Set to `summary` for AI-generated structured summary (Pro only) |

### HEAD /rd — Health Check

Check if the API service is online:

```
HEAD https://api.readgzh.site/rd
```

Returns `200 OK` when service is operational.

## Integration Methods

### MCP Protocol (Recommended)

Add to OpenClaw config:

```json
{
  "mcpServers": {
    "readgzh": {
      "url": "https://api.readgzh.site/mcp-server"
    }
  }
}
```

### REST API

```bash
# Method 1: GET direct fetch (recommended for AI)
curl "https://api.readgzh.site/rd?url=https://mp.weixin.qq.com/s/xxxxx" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# Method 2: POST scrape and cache
curl -X POST "https://api.readgzh.site/rd" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://mp.weixin.qq.com/s/xxxxx"}'

# Read cached article (Markdown format)
curl "https://api.readgzh.site/rd?s=article-slug&format=text" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# Paginated reading (part 2 of long article)
curl "https://api.readgzh.site/rd?s=article-slug&part=2" \
  -H "Authorization: Bearer <YOUR_API_KEY>"

# AI summary (Pro only)
curl "https://api.readgzh.site/rd?s=article-slug&mode=summary" \
  -H "Authorization: Bearer <YOUR_API_KEY>"
```

## Credits

| Type | Cost |
|------|------|
| Simple article (< 5 images) | 1 credit |
| Complex article (>= 5 images) | 2 credits |
| Cached article read | Free |
| Free tier | 30 credits/day (must click "Claim Today's Credits" in dashboard) |
| Pro subscription | Up to 2,000 credits/month (auto-issued) |

## Error Codes

| Status | Meaning |
|--------|---------|
| 401 | Missing or invalid API Key |
| 402 | API Key credits exhausted (response includes pricing_url) |
| 403 | Pro feature required (e.g., `?mode=summary`) |
| 429 | Rate limit exceeded (10/day for unauthenticated) |

## Usage Notes

- Supports both standard article and image-post (Little Green Book) formats
- Only WeChat Official Account links (mp.weixin.qq.com) are supported
- Articles are auto-cached; repeat requests do not re-scrape
- Image posts extract all images and text descriptions
- Please comply with applicable laws and regulations, for personal learning and research only

## Privacy Note

- Articles are cached globally and may be visible to other users
- Do not submit private or sensitive article links
- Use your own API key rather than shared credentials

## Developer Info

- **API Docs**: https://readgzh.site/docs
- **Free API Key**: https://readgzh.site/dashboard
- **Support**: https://readgzh.site
- **Maintainer**: Sweesama (@sweesama)