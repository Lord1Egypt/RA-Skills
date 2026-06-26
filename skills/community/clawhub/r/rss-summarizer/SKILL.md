---
name: rss-summarizer
description: 智能 RSS 订阅与摘要。用于订阅、抓取、过滤和摘要 RSS/Atom 订阅源。当用户需要跟踪新闻、博客更新并提供摘要时使用。
---

# RSS Summarizer Skill

本技能提供 RSS 订阅源管理、抓取和摘要功能。

## 何时使用

- 用户希望订阅某个 RSS/Atom feed
- 需要定期获取最新内容并摘要
- 需要根据关键词过滤内容
- 需要将更新推送到聊天或保存为文档

## 可用脚本

- `scripts/add.js` - 添加订阅源
- `scripts/list.js` - 列出所有订阅源
- `scripts/remove.js` - 删除订阅源
- `scripts/fetch.js` - 抓取最新内容并摘要
- `scripts/configure.js` - 配置参数（摘要模式、语言、最大条目、过滤器）

## 使用方法

AI 在响应用户请求时，应调用相应的脚本，传入 JSON 参数（通过 stdin），并返回 JSON 结果。

脚本通用输入/输出格式：

**输入 (stdin)**:
```json
{
  "context": { "send": function } // 可选，用于通知用户
  ... 具体参数（见各脚本）
}
```

**输出 (stdout)**:
```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

### 示例

用户说：“订阅 Hacker News 的 RSS”
AI 调用 `scripts/add.js`:
```json
{ "url": "https://news.ycombinator.com/rss", "name": "Hacker News" }
```

AI 收到响应后向用户确认。

## 数据存储

脚本使用 `data/subscriptions.json` 和 `data/config.json` 存储数据。首次运行会自动创建。

## 备注

- 抓取时若网络错误会返回 `error` 字段。
- 摘要功能依赖外部 AI 服务（通过 oracle CLI），如需高级摘要可扩展。
- 支持多语言输出，默认中文。