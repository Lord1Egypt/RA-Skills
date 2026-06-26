---
name: wechat-reader
description: Read WeChat public account (微信公众号) articles. Activate when the user shares a mp.weixin.qq.com link, asks to read/summarize a WeChat article, or mentions 公众号/微信文章. These pages are JS-rendered and blocked by web_fetch — this skill uses browser automation to extract full article text.
---

# WeChat Article Reader

## Why This Skill Exists

WeChat public account articles (`mp.weixin.qq.com/s/...`) are fully JS-rendered and have anti-scraping measures. `web_fetch` only returns the title. Browser automation is required to get the full content.

## How to Read an Article

1. Detect `mp.weixin.qq.com` URLs in user messages
2. Open with browser tool:

```
browser(action="open", url="<article_url>", profile="openclaw")
```

3. Wait for render, then snapshot:

```
browser(action="snapshot", targetId=<id>, maxChars=15000)
```

4. Close the tab:

```
browser(action="close", targetId=<id>)
```

5. Present the content to the user (summarize or translate as requested)

## Tips

- Articles may contain images — snapshot captures alt text and captions
- Very long articles: increase `maxChars` to 30000 or use multiple snapshots with scrolling
- If the page shows "此内容因违规无法查看" (content removed), inform the user
- Some articles require WeChat login — if snapshot shows a login wall, inform the user
- For multiple articles, process sequentially to avoid resource waste
