# Platform Strategies

Detailed per-platform documentation for web-fetcher.

## WeChat (mp.weixin.qq.com)

- **Selector:** `#js_content`
- **Method:** scrapling GET (Tier 1 usually sufficient)
- **Image handling:**
  - `<img>` tags use `data-src="https://mmbiz.qpic.cn/..."` for real URLs
  - Visible `src` contains `data:image/svg+xml` placeholder (lazy loading)
  - Must download with `Referer: https://mp.weixin.qq.com/` header
  - URL parameter `wx_fmt=png|jpeg|gif` indicates format
- **Gotchas:**
  - Some articles may trigger CAPTCHA if fetched too frequently
  - Scrapling's browser impersonation helps avoid blocks

## Feishu (*.feishu.cn)

- **Selector:** `[data-content-editable-root]`
- **Method:** StealthyFetcher with virtual scroll
- **Scroll mechanism:**
  - Content container: `.bear-web-x-container`
  - Content blocks have `[data-block-id]` attributes
  - Only visible blocks are rendered (virtual scroll)
  - Must scroll 800px at a time and collect DOM after each scroll
  - Stop after 15 stable iterations (no new blocks)
- **Image handling:**
  - Images return 401 without cookies
  - Download via `page.evaluate(fetch(url, {credentials: 'include'}))` → base64
- **Artifacts:** "Unable to print" text appears in some blocks, auto-cleaned

## Toutiao (www.toutiao.com)

- **Selector:** `.article-content`
- **Method:** scrapling GET or fetch
- **Image handling:**
  - Images use `data-src` with `toutiaoimg.com` URLs
  - Visible `src` contains base64 placeholder
  - Extract real URLs from `data-src` attribute in HTML
  - Download with `Referer: https://www.toutiao.com/` header

## Zhihu

- **Zhuanlan (articles):** selector `.Post-RichText`
- **Q&A pages:** selector `.RichContent`
- **Method:** scrapling GET usually works
- **Notes:** Images are standard `<img src>`, no special handling needed

## Xiaohongshu (www.xiaohongshu.com)

- **Selector:** `.note-content`
- **Method:** camoufox (required — heavy anti-bot detection)
- **Notes:**
  - Standard scrapling will be blocked
  - Camoufox provides anti-fingerprint browsing
  - May need login for some content

## Weibo (www.weibo.com)

- **Selector:** `.WB_text`
- **Method:** camoufox (recommended for reliable access)
- **Notes:** Some content requires login

## Bilibili (bilibili.com / b23.tv)

- **Method:** yt-dlp
- **Format selection:** `bestvideo[height<=N]+bestaudio/best[height<=N]`
- **Output:** Merged to MP4 via ffmpeg
- **Short links:** b23.tv redirects are handled by yt-dlp automatically
- **Premium content:** Use `--cookies-browser chrome` to pass login cookies
- **Audio extraction:** Use `--audio-only` flag for MP3 output

## YouTube (youtube.com / youtu.be)

- **Method:** yt-dlp
- **Notes:** Standard yt-dlp usage, no special handling

## Douyin (douyin.com)

- **Method:** yt-dlp
- **Notes:** May need cookies for some content
