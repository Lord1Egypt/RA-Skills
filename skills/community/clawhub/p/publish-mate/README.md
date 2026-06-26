# Auto Publisher

Automatically fetch global news, generate articles with featured images, and publish to your WordPress site or custom CMS.

## Features

- **Multi-source news fetching** — RSS feeds, NewsAPI, custom REST APIs
- **Auto image sourcing** — RSS media, Unsplash, Pexels, Pixabay, or fallback
- **WordPress REST API** — Full support with auto-detection of API URL format
- **Image upload** — Uploads featured images with retry and SSL error recovery
- **Deduplication** — Tracks published articles to avoid duplicates
- **Configurable** — Language, categories, tags, post status, content templates
- **Secure** — All credentials via environment variables, never in config files

## Install

```bash
openclaw skills install auto-publisher
```

Or clone manually:

```bash
git clone https://github.com/your-username/auto-publisher.git ~/.openclaw/skills/auto-publisher
```

## Setup

### 1. Generate WordPress Application Password

1. Login to your WordPress admin (`/wp-admin/`)
2. Go to **Users > Your Profile**
3. Scroll to **Application Passwords**
4. Enter name `auto-publisher`, click **Add New**
5. Copy the generated password

### 2. Set Environment Variable

```bash
export WP_APP_PASSWORD='xxxx xxxx xxxx xxxx'
```

Or add to OpenClaw settings (`~/.openclaw/openclaw.json`):

```json
{
  "skills": {
    "entries": {
      "auto-publisher": {
        "enabled": true,
        "env": {
          "WP_APP_PASSWORD": "xxxx xxxx xxxx xxxx"
        }
      }
    }
  }
}
```

### 3. Configure

Run the setup wizard:

```bash
bash ~/.openclaw/skills/auto-publisher/setup.sh
```

Or copy and edit the config template:

```bash
cp config.example.json config.json
# Edit config.json with your settings
```

## Usage

```
/auto-publisher              # Fetch news and publish
/auto-publisher publish      # Same as above
/auto-publisher preview      # Preview without publishing
/auto-publisher setup        # Re-run setup wizard
/auto-publisher status       # Show publishing history
/auto-publisher config       # Show current configuration
```

## Configuration

See `config.example.json` for all options. Key settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `platform.url` | Your WordPress site URL | Required |
| `platform.username` | WordPress username | Required |
| `publishing.posts_per_day` | Max articles per run | 5 |
| `publishing.language` | Content language | `zh` |
| `publishing.status` | Post status | `publish` |
| `publishing.categories` | Default categories | `["News"]` |
| `images.source` | Image API provider | RSS fallback |
| `news_sources` | Array of RSS/API sources | BBC + NYT |

## News Sources

### RSS Feeds (no API key needed)

```json
{"type": "rss", "url": "https://feeds.bbci.co.uk/news/world/rss.xml", "name": "BBC", "max_items": 5}
```

### NewsAPI (requires free API key)

```json
{"type": "newsapi", "category": "general", "country": "us", "api_key_env": "NEWS_API_KEY"}
```

### Custom API

```json
{
  "type": "custom",
  "url": "https://api.example.com/news",
  "headers": {"Authorization": "$MY_TOKEN"},
  "response_path": "data.articles",
  "field_mapping": {"title": "headline", "content": "body"}
}
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `WP_APP_PASSWORD` | WordPress Application Password (required) |
| `UNSPLASH_API_KEY` | Unsplash image search |
| `PEXELS_API_KEY` | Pexels image search |
| `PIXABAY_API_KEY` | Pixabay image search |
| `NEWS_API_KEY` | NewsAPI.org access |

## Project Structure

```
auto-publisher/
├── SKILL.md                 # OpenClaw skill definition
├── README.md                # This file
├── setup.sh                 # Interactive setup wizard
├── config.example.json      # Configuration template
├── scripts/
│   ├── auto_publish.py      # Full pipeline (fetch → image → publish)
│   ├── fetch_news.py        # News fetching module
│   ├── fetch_image.py       # Image search & download module
│   └── publish.py           # WordPress publishing module
├── templates/
│   ├── default.md           # Standard article template
│   └── brief.md             # Short news brief template
├── data/                    # Runtime data (gitignored)
└── logs/                    # Logs (gitignored)
```

## License

MIT
