---
name: wewerss
description: 订阅微信公众号等信源，获取原始文章内容用于整合日报
version: 1.0.0
metadata:
  openclaw:
    homepage: https://github.com/punkpeye/wewerss
    requires:
      anyBins:
        - curl
        - jq
---

# WeWeRSS Open Channel Skill

通过 Open Channel API 订阅微信公众号等信源，获取原始文章数据。所有 AI 处理（摘要、分类、标签等）由 Agent 侧使用用户自己的 LLM token 完成。

## Environment Variables

- `WEWERSS_BASE_URL` — WeWeRSS 实例地址（必填），例如 `https://rss.example.com`

## 创建频道

```bash
curl -s -X POST "$WEWERSS_BASE_URL/api/open/channels" \
  -H "Content-Type: application/json" \
  -d '{"name":"我的日报频道"}' | jq .
```

返回频道 UUID，后续操作均需要此 ID。

## 添加信源

提交任意 URL（公众号文章链接、RSS 地址、网站首页），系统自动发现 RSS feed：

```bash
CHANNEL_ID="your-channel-uuid"

# 添加 RSS feed
curl -s -X POST "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/sources" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/feed.xml"}' | jq .

# 添加网站（自动发现 RSS）
curl -s -X POST "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/sources" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' | jq .
```

## 查看信源列表

```bash
curl -s "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/sources" | jq .
```

## 删除信源

```bash
SOURCE_ID="source-uuid-from-list"
curl -s -X DELETE "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/sources/$SOURCE_ID"
```

## 获取文章

获取最近 N 天的原始文章内容（默认 1 天）：

```bash
# 最近 1 天
curl -s "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/articles?days=1" | jq .

# 最近 7 天，第 2 页
curl -s "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/articles?days=7&page=2&page_size=50" | jq .
```

返回字段仅包含原始数据：
- `title` - 文章标题
- `author` - 作者/公众号名
- `link` - 原文链接
- `published_at` - 发布时间
- `description` - RSS 自带摘要
- `text_plain` - 纯文本全文（可能为 null）
- `source_name` - 来源订阅名称

**不返回任何 AI 生成字段**（摘要、标签、分类、质量分等），Agent 需自行处理。

## 获取 Atom Feed

```bash
curl -s "$WEWERSS_BASE_URL/api/open/channels/$CHANNEL_ID/feed"
```

标准 Atom XML，可用于 RSS 阅读器或其他消费端。

## 速率限制

- 创建频道：10 次/小时（按 IP）
- 添加信源：30 次/小时（按频道）
- 文章/Feed 读取：120 次/小时（按频道）

## 典型使用流程

1. 创建频道 → 获得 UUID
2. 添加目标信源（公众号 RSS、行业博客等）
3. 每日定时获取文章 `articles?days=1`
4. Agent 用自己的 LLM 对文章进行摘要、分类、整合
5. 生成并推送日报
