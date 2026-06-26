# wechat-publisher

An [OpenClaw](https://openclaw.ai) Skill that lets AI agents publish Markdown articles to WeChat Official Account (微信公众号) draft box via the official API.

## What it does

Give the agent a Markdown file + image files → it handles everything:

1. Uploads images to WeChat CDN
2. Converts Markdown to WeChat-compatible HTML (inline CSS, mobile-friendly)
3. Uploads the article as a draft to your 公众号 草稿箱

**The agent does not generate images** — bring your own (AI-generated or otherwise).

## Setup

### 1. Install as OpenClaw Skill

```bash
# Clone into your OpenClaw workspace skills folder
git clone https://github.com/yuejiangli/wechat-publisher ~/.openclaw/workspace/skills/wechat-publisher
```

Or install via [ClaWHub](https://clawhub.com) (coming soon).

### 2. Configure credentials

```bash
cp config.example.json config.json
# Edit config.json with your AppID and AppSecret
```

Get your credentials from [WeChat MP Backend](https://mp.weixin.qq.com) → 开发 → 基本配置.

Or use environment variables:
```bash
export WX_APPID="wx1234567890abcdef"
export WX_APPSECRET="your_appsecret_here"
```

### 3. Requirements

- Python 3.6+
- No external dependencies (stdlib only)
- Optional: `pip3 install markdown` for richer Markdown support

## Usage

Once installed as an OpenClaw Skill, just tell your agent:

> "把这篇文章发到公众号草稿箱，封面用 cover.jpg"

The agent will handle the full workflow automatically.

### Manual / scripted usage

```bash
# Get access token
python3 scripts/get_token.py

# Upload cover image → get thumb_media_id
THUMB_ID=$(python3 scripts/upload_thumb.py cover.jpg)

# Upload body image → get WeChat CDN URL
WX_URL=$(python3 scripts/upload_img.py images/figure1.png)

# Convert Markdown to HTML (with image map)
echo '{"figure1.png": "'$WX_URL'"}' > /tmp/image_map.json
python3 scripts/md_to_html.py article.md --image-map /tmp/image_map.json > /tmp/article.html

# Upload draft
python3 scripts/upload_draft.py \
  --title "文章标题" \
  --html /tmp/article.html \
  --thumb-media-id "$THUMB_ID" \
  --author "作者名" \
  --digest "文章摘要"
```

## Scripts

| Script | Description |
|--------|-------------|
| `get_token.py` | Get/cache WeChat access token (auto-refreshes) |
| `upload_thumb.py` | Upload cover image → returns `thumb_media_id` |
| `upload_img.py` | Upload body image → returns WeChat CDN URL |
| `md_to_html.py` | Convert Markdown to WeChat-compatible HTML |
| `upload_draft.py` | Upload article as draft → returns `media_id` |

## WeChat Account Requirements

- Subscription account (订阅号) or Service account (服务号)
- API access enabled (开发者模式)
- Draft box feature enabled (草稿箱)

## License

MIT
