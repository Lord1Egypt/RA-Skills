# Social Media Metrics — OpenClaw Skill

An OpenClaw skill for fetching follower counts across 12 social media platforms including YouTube, TikTok, Bilibili, Douyin, Kuaishou, Instagram, and more.

## Supported Platforms

| Platform | Method | Input: URL | Input: Nickname |
|----------|--------|-----------|----------------|
| Bilibili (哔哩哔哩) | API | `space.bilibili.com/{uid}` | Yes |
| YouTube | API / Browser | `youtube.com/@{handle}` | Yes |
| Douyin (抖音) | Browser | `douyin.com/user/{id}` | Yes |
| Kuaishou (快手) | Browser | `kuaishou.com/profile/{id}` | Yes |
| Xiaohongshu (小红书) | Browser (requires login) | `xiaohongshu.com/user/profile/{id}` | Yes |
| TikTok | Browser | `tiktok.com/@{handle}` | Yes |
| Instagram | Browser | `instagram.com/{handle}` | Yes |
| WeChat Video (视频号) | Browser | `channels.weixin.qq.com/{id}` | No |
| Toutiao (头条号) | Browser | `toutiao.com/c/user/token/{id}` | Yes |
| Baijiahao (百家号) | Browser | `baijiahao.baidu.com/u?app_id={id}` | No |
| Haokan (好看视频) | Browser | Yes | No |
| iQiyi (爱奇艺) | Browser | `iqiyi.com/u/{id}` | No |

## Installation

### As an OpenClaw Skill

```bash
clawhub install social-metrics
```

### Manual Setup

```bash
git clone https://github.com/guoming0000/openclaw-social-metrics.git
cd openclaw-social-metrics
pip install -r requirements.txt
playwright install chromium
```

## Usage

### Via OpenClaw

Once installed, simply ask your AI assistant:

- "帮我查一下影视飓风在B站的粉丝数"
- "How many followers does MrBeast have on YouTube?"
- "查询 https://space.bilibili.com/946974 的粉丝数据"

### Via Command Line

**Fetch by URL:**

```bash
python scripts/main.py --url "https://space.bilibili.com/946974"
```

**Fetch by nickname (requires `--platform`):**

```bash
python scripts/main.py --nickname "影视飓风" --platform bilibili
```

Available `--platform` values: `bilibili`, `youtube`, `douyin`, `kuaishou`, `xiaohongshu`, `wechat_video`, `tiktok`, `instagram`, `toutiao`, `baijiahao`, `haokan`, `iqiyi`

### Output Format

**Success:**

```json
{
  "platform": "bilibili",
  "username": "影视飓风",
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

**Error:**

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

## Configuration

| Environment Variable | Required | Description |
|---------------------|----------|-------------|
| `YOUTUBE_API_KEY` | No | YouTube Data API v3 key. Falls back to browser scraping if not set. |

## How It Works

- **API-first**: Platforms with public APIs (Bilibili, YouTube) are queried via HTTP requests for speed and reliability.
- **Browser fallback**: All other platforms use Playwright (headless Chromium) to render profile pages and extract follower counts.
- **Smart input resolution**: Accepts both profile URLs and account nicknames. URLs are parsed to detect the platform and extract user IDs automatically.

## Platform-Specific Notes

### Xiaohongshu (小红书) — Login Required

Xiaohongshu requires an authenticated session. The script uses a real Chrome instance (via CDP) with a persistent profile at `~/.playwright_cdp_profile`.

**First-time setup:**
1. Run any Xiaohongshu query (e.g., `python scripts/main.py --nickname "test" --platform xiaohongshu`)
2. A Chrome window will open showing a QR code login page
3. Scan the QR code with the Xiaohongshu app on your phone
4. The script will detect the login and proceed automatically (120-second timeout)

**Subsequent runs:** Cookies are persisted in the Chrome profile — no login needed until the session expires.

## Feedback & Issues

GitHub: [openclaw-social-metrics](https://github.com/guoming0000/openclaw-social-metrics)

If you encounter any problems or have feature requests, feel free to open an [Issue](https://github.com/guoming0000/openclaw-social-metrics/issues).

## License

MIT
