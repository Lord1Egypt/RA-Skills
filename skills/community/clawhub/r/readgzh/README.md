# ReadGZH — 微信公众号文章 AI 阅读器

ReadGZH 是一款专为 AI 智能体设计的微信公众号内容解析工具。它通过服务端代理绕过微信的反爬虫机制，将复杂的公众号 HTML 转换为纯净、结构化的 Markdown 内容，大幅节省 Token 消耗。

## 这个资产能做什么

- 穿透微信公众号反爬机制，读取任意公众号文章全文
- 将 HTML 转换为极简 Markdown，Token 消耗降低 50-87%
- 解决微信图片 2 小时过期问题（CDN 永久代理）
- 已转换文章永久缓存，重复读取完全免费
- 支持 API Key 鉴权和 MCP 协议两种接入方式

## 核心特性

- **99.89% 穿透率**：自研 7 阶段提取管线，完美绕过客户端指纹检测与反爬拦截
- **50-87% Token 节省**：自动剥离内联样式、冗余标签及广告干扰，输出极简 Markdown
- **CDN 永久代理**：将图片路由至持久化 CDN，解决微信图片 2 小时过期的硬伤
- **全球共享缓存**：转换过的文章永久入库，后续任何用户或 Agent 读取均完全免费
- **原生支持 MCP**：内置 Model Context Protocol，支持 AI Agent 协议化直接调用

## 快速开始

直接对你的 AI 助手下令：

> **"帮我读一下这篇文章：[微信公众号链接]"**

## 接入方式

### 方式一：MCP 协议（推荐）

在 OpenClaw 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "readgzh": {
      "url": "https://api.readgzh.site/mcp-server"
    }
  }
}
```

重启 OpenClaw 后自动发现工具，无需手动注入 API Key。

### 方式二：REST API + curl

```bash
curl "https://api.readgzh.site/rd?url=https://mp.weixin.qq.com/s/xxxxx" \
  -H "Authorization: Bearer <YOUR_API_KEY>"
```

### 方式三：browser 读取（无需 API Key）

OpenClaw 有 Chrome 会话时，直接用 CDP 打开微信文章 URL：

```
browser(action=open, url="https://mp.weixin.qq.com/s/xxxxx")
```

## ⚠️ 使用前必读

| 情况 | 限制 | 解决方案 |
|------|------|---------|
| 匿名用户（无 API Key） | 每天仅 10 次/IP，超出触发 429 | 注册获取 API Key |
| 带 API Key | 每日 30 credits（需在控制台领取） | `-H "Authorization: Bearer <YOUR_API_KEY>"` |
| 缓存文章 | 已转换过的文章再次读取 | 完全免费，不限次数 |

**429 错误原因**：匿名请求超出 IP 频率限制（每天10次），[注册 API Key 即可解决 →](https://readgzh.site/dashboard)

## Credits 说明

| 类型 | 消耗 |
|------|------|
| 简单文章（< 5 图）| 1 credit |
| 复杂文章（≥ 5 图）| 2 credits |
| 缓存文章读取 | 免费 |

## 开发者信息

- **API 文档**：[readgzh.site/docs](https://readgzh.site/docs)
- **API Key 领取**：[readgzh.site/dashboard](https://readgzh.site/dashboard)
- **技术支持**：[readgzh.site](https://readgzh.site)
- **开发维护**：Sweesama（[@sweesama](https://github.com/sweesama)）
