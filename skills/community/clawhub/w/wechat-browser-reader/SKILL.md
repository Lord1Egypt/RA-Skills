---
name: wechat-browser-reader
description: "Read WeChat Official Account articles (mp.weixin.qq.com) via Chrome DevTools browser automation. Use when user provides a WeChat article URL and other extractors fail due to captcha, JS encryption, or anti-scraping. Requires Chrome remote debugging (port 9222) to be running. Handles captcha verification, JS content decryption, and content extraction."
---

# WeChat Browser Reader

Read WeChat articles via Chrome DevTools when HTTP-based extractors fail.

## Prerequisites

- Chrome with remote debugging enabled: `google-chrome --no-first-run --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug-profile`
- OpenClaw browser tools available (navigate_page, evaluate_script, etc.)

## Workflow

### 1. Navigate

```
navigate_page(url=<article_url>)
```

### 2. Handle Captcha (if present)

If the page shows "环境异常" / "去验证":

```
take_snapshot()  # find the "去验证" element
click(uid=<verify_button_uid>)
```

If the page shows "轻触查看原文" (non-WeChat container):

```
evaluate_script(() => document.querySelector('.wx_expand_article_button_wrap')?.click())
```

### 3. Wait for Content

WeChat articles use JS encryption. Content may take 3-5 seconds to decrypt after page load.

```
wait_for(text=["activity-name", "js_content"], timeout=15000)
```

### 4. Extract Content

```javascript
evaluate_script(() => {
  const title = document.getElementById('activity-name')?.innerText || '';
  const author = document.getElementById('js_name')?.innerText || '';
  const content = document.getElementById('js_content')?.innerText || '';
  return { title, author, contentLength: content.length, content };
})
```

If `activity-name` is empty but `js_content` exists, content is loaded — just extract it.

If both are empty after 10+ seconds, try:

```javascript
evaluate_script(() => new Promise(resolve => {
  setTimeout(() => {
    const el = document.getElementById('js_content');
    resolve({ exists: !!el, htmlLen: el?.innerHTML?.length || 0, text: el?.innerText || '' });
  }, 5000);
}))
```

### 5. Return to User

Summarize or present the article content. Key fields:
- **title**: article title
- **author**: account name
- **content**: full article text

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| "环境异常" | Captcha triggered | Click "去验证", wait for redirect |
| "轻触查看原文" | Non-WeChat browser | Click the button or use JS click |
| Empty content after load | JS decryption not complete | Wait 3-5 seconds, retry extraction |
| Chrome not connected | Remote debugging not running | Start Chrome with `--remote-debugging-port=9222` |
| Page stuck on loading | Network or rendering issue | Reload page, check network conditions |

## Tips

- Always use `evaluate_script` with `setTimeout` (3-5s) for reliable content extraction — WeChat's JS decryption is async
- If captcha keeps appearing, the IP may be rate-limited — wait a few minutes
- The approach works because a real Chrome browser executes WeChat's decryption scripts, unlike HTTP-only fetchers
