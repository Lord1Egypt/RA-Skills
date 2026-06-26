# Web Fetcher

Smart web content fetcher for Claude Code. Automatically detects the platform from a URL and uses the best strategy to fetch articles or download videos.

## Supported Platforms

| Platform | Type | Method |
|----------|------|--------|
| WeChat (mp.weixin.qq.com) | Article | scrapling + image extraction |
| Feishu (*.feishu.cn) | Article | Virtual scroll collection |
| Zhihu (zhuanlan/www) | Article | scrapling |
| Toutiao | Article | scrapling + image extraction |
| Xiaohongshu | Article | camoufox (anti-bot) |
| Weibo | Article | camoufox (anti-bot) |
| Bilibili / b23.tv | Video | yt-dlp |
| YouTube / youtu.be | Video | yt-dlp |
| Douyin | Video | yt-dlp |
| Any other URL | Article | scrapling (generic) |

## Install

### As Claude Code Skill

```bash
git clone https://github.com/inspirai-store/web-fetcher ~/.claude/skills/web-fetcher
```

### Manual

```bash
git clone https://github.com/inspirai-store/web-fetcher
cd web-fetcher
```

## Quick Start

```bash
# Fetch a WeChat article
python3 fetcher.py "https://mp.weixin.qq.com/s/xxx" -o ~/docs/

# Download a Bilibili video
python3 fetcher.py "https://b23.tv/xxx" -o ~/videos/

# Fetch a Feishu document
python3 fetcher.py "https://xxx.feishu.cn/wiki/xxx" -o ~/docs/

# Batch fetch from file
python3 fetcher.py --urls-file urls.txt -o ~/docs/

# Extract audio only
python3 fetcher.py "https://b23.tv/xxx" -o ~/audio/ --audio-only
```

## CLI Reference

```
python3 fetcher.py [URL] [OPTIONS]

Arguments:
  url                    URL to fetch

Options:
  -o, --output DIR       Output directory (default: current)
  -q, --quality N        Video quality: 1080, 720, 480 (default: 1080)
  --method METHOD        Force method: scrapling, camoufox, ytdlp, feishu
  --selector CSS         Force CSS selector for content extraction
  --urls-file FILE       File with URLs (one per line, # for comments)
  --audio-only           Extract audio only (video downloads)
  --no-images            Skip image download (articles)
  --cookies-browser NAME Browser for cookies (e.g., chrome, firefox)
```

## How It Works

```
URL → router.py (domain matching) → handler
                                      ├── article.py (scrapling GET → browser → camoufox)
                                      ├── feishu.py  (virtual scroll + authenticated image fetch)
                                      └── video.py   (yt-dlp wrapper)
```

Articles are converted to Markdown with images downloaded locally. Videos are downloaded as MP4 (or MP3 with `--audio-only`).

## Dependencies

Install only what you need:

```bash
pip install scrapling       # Article fetching
pip install yt-dlp          # Video downloads
pip install html2text       # HTML→Markdown (needed for camoufox/feishu)
pip install camoufox        # Anti-bot sites (Xiaohongshu, Weibo)
python3 -m camoufox fetch   # Download camoufox browser
```

## Adding New Platforms

1. Add entry to `ROUTE_TABLE` in `lib/router.py`
2. If needed, add image post-processing hook in `lib/article.py`
3. If needed, create dedicated handler in `lib/`

See [references/extending.md](references/extending.md) for details.

## License

MIT
