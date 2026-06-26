# Social Media Metrics

## Description

Fetch follower counts and metrics from 11+ social media platforms. Supports input via profile URL or account nickname. Platforms include Instagram, YouTube, TikTok, Douyin, WeChat Video, Kuaishou, iQiyi, Xiaohongshu, Bilibili, Toutiao, and Baijiahao.

## When to Use

- When the user asks for follower counts or social media metrics
- When the user mentions "粉丝数", "粉丝量", "followers", "subscriber count"
- When the user provides a social media profile URL and wants to know the metrics
- When the user asks to compare follower counts across platforms
- NOT for posting content or managing social media accounts

## Prerequisites

- Python 3.9+
- pip packages: `requests`, `playwright`, `beautifulsoup4` (install via `pip install -r requirements.txt`)
- Playwright browsers: run `playwright install chromium` after installing the package
- **Recommended**: Google Chrome installed on the system — Douyin, Kuaishou, and Xiaohongshu use Chrome's CDP (DevTools Protocol) mode for better anti-detection. If Chrome is not installed, Playwright's bundled Chromium will be used as an automatic fallback
- Optional: `YOUTUBE_API_KEY` environment variable for YouTube Data API (falls back to browser scraping if not set)

## Supported Platforms

| Platform | Input: URL | Input: Nickname | Method |
|----------|-----------|----------------|--------|
| Bilibili (哔哩哔哩) | `space.bilibili.com/{uid}` | Yes | API |
| YouTube | `youtube.com/@{handle}` | Yes | API / Browser |
| Douyin (抖音) | `douyin.com/user/{id}` | Yes | Browser |
| Kuaishou (快手) | `kuaishou.com/profile/{id}` | Yes | Browser |
| Xiaohongshu (小红书) | `xiaohongshu.com/user/profile/{id}` | Yes | Browser (requires login) |
| TikTok | `tiktok.com/@{handle}` | Yes | Browser |
| Instagram | `instagram.com/{handle}` | Yes | Browser |
| WeChat Video (视频号) | `channels.weixin.qq.com/{id}` | No | Browser |
| Toutiao (头条号) | `toutiao.com/c/user/token/{id}` | Yes | Browser |
| Baijiahao (百家号) | `baijiahao.baidu.com/u?app_id={id}` | No | Browser |
| iQiyi (爱奇艺) | `iqiyi.com/u/{id}` | No | Browser |

## Instructions

### Step 1: Ensure dependencies are installed

Check if the required packages are available. If not, install them:

```bash
cd <skill_directory>
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Determine input type

From the user's message, determine:
- **URL input**: If the user provides a URL (e.g., `https://space.bilibili.com/946974`), use `--url`
- **Nickname input**: If the user provides a name (e.g., "MrBeast"), use `--nickname` and `--platform`

### Step 3: Run the script

**Fetch by URL:**
```bash
python <skill_directory>/scripts/main.py --url "https://space.bilibili.com/946974"
```

**Fetch by nickname (platform required):**
```bash
python <skill_directory>/scripts/main.py --nickname "MrBeast" --platform bilibili
```

Available `--platform` values: `bilibili`, `youtube`, `douyin`, `kuaishou`, `xiaohongshu`, `wechat_video`, `tiktok`, `instagram`, `toutiao`, `baijiahao`, `iqiyi`

### Step 4: Parse and present results

The script outputs JSON to stdout. Parse it and present the results in a user-friendly format.

**Success response:**
```json
{
  "platform": "bilibili",
  "username": "MrBeast",
  "uid": "946974",
  "url": "https://space.bilibili.com/946974",
  "metrics": {
    "followers": 12345678
  },
  "fetched_at": "2026-03-13T12:00:00+00:00",
  "success": true,
  "error": null
}
```

**Error response:**
```json
{
  "platform": "bilibili",
  "username": null,
  "uid": null,
  "url": null,
  "metrics": {},
  "fetched_at": "2026-03-13T12:00:00+00:00",
  "success": false,
  "error": "Description of the error"
}
```

## Platform-Specific Notes

### Xiaohongshu (小红书) — Login Required

Xiaohongshu requires an authenticated session to view search results and profile pages. The script uses a real Chrome instance (via CDP) with a persistent profile at `~/.playwright_cdp_profile`.

**First-time setup:**
1. Run any Xiaohongshu query (e.g., `python scripts/main.py --nickname "test" --platform xiaohongshu`)
2. A Chrome window will open showing a QR code login page
3. Scan the QR code with the Xiaohongshu app on your phone
4. The script will detect the login and proceed automatically (120-second timeout)

**Subsequent runs:** Cookies are persisted in the Chrome profile — no login needed until the session expires.

## Error Handling

- **Missing platform for nickname**: Ask the user which platform they want to query
- **Unsupported URL**: Tell the user which platforms are supported
- **Scraping failure**: Some platforms may block headless browsers or require login. Inform the user and suggest trying a direct URL
- **Xiaohongshu login required**: The script will prompt the user to scan a QR code in the Chrome window. If the session has expired, re-run the script and scan again
- **YouTube API key missing**: The script automatically falls back to browser scraping — no action needed
- **Timeout**: Browser-based platforms may be slow. If timeout occurs, retry once

## Examples

**User:** "帮我查一下MrBeast在B站的粉丝数"
→ Run: `python scripts/main.py --nickname "MrBeast" --platform bilibili`

**User:** "How many followers does MrBeast have on YouTube?"
→ Run: `python scripts/main.py --nickname "MrBeast" --platform youtube`

**User:** "查询 https://space.bilibili.com/946974 的粉丝数据"
→ Run: `python scripts/main.py --url "https://space.bilibili.com/946974"`

**User:** "查一下这个TikTok账号的粉丝 https://www.tiktok.com/@khaby.lame"
→ Run: `python scripts/main.py --url "https://www.tiktok.com/@khaby.lame"`

## Feedback & Issues

GitHub repository: [openclaw-social-metrics](https://github.com/guoming0000/openclaw-social-metrics)

If you encounter any problems or have feature requests, feel free to open an [Issue](https://github.com/guoming0000/openclaw-social-metrics/issues).
