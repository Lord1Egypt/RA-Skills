---
name: read-tweet
description: 阅读Twitter/X推文内容。当用户分享Twitter/X链接，或说"读一下这条推文"、"read tweet"、"看看这条X"时使用。
allowed-tools: Bash, Read
---

# 阅读 Twitter/X 推文

X/Twitter 页面依赖 JavaScript 渲染，WebFetch 直接抓取会失败。使用 fxtwitter API 代理获取推文结构化数据。

## 流程

### Step 1: 解析 URL，提取用户名和推文 ID

从用户提供的 URL 中提取：
- **用户名**: URL 路径第一段（如 `HiTw93`）
- **推文 ID**: URL 路径末尾的数字（如 `2032091246588518683`）

支持的 URL 格式：
- `https://x.com/{username}/status/{tweet_id}`
- `https://twitter.com/{username}/status/{tweet_id}`

### Step 2: 通过 fxtwitter API 获取内容

将原始 URL 的域名替换为 `api.fxtwitter.com`：

```
原始: https://x.com/HiTw93/status/2032091246588518683
代理: https://api.fxtwitter.com/HiTw93/status/2032091246588518683
```

使用 Bash 通过 curl 访问代理 URL：

```bash
curl -s "https://api.fxtwitter.com/{username}/status/{tweet_id}"
```

返回的是 JSON 数据，从中提取推文完整内容。

### Step 3: 结构化输出

将获取到的信息整理为以下格式：

```
## 推文内容

**作者**: {display_name} (@{username})
**发布时间**: {created_at}
**互动**: {likes} 赞 | {retweets} 转发 | {views} 浏览

{推文正文}

{如有图片/视频/链接，列出描述}
```

## 备选方案

如果 fxtwitter 不可用，依次尝试：
1. `https://api.vxtwitter.com/{username}/status/{tweet_id}`
2. 使用 WebSearch 搜索推文 ID 或正文关键词

## 注意事项

- fxtwitter 返回的是 JSON 格式数据，curl 直接获取
- 长推文（Thread）可能只返回第一条，需提示用户
- 如推文包含外链文章，可进一步用 curl 抓取外链内容
