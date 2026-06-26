# SearXNG Reference Guide

## Quick Deploy with Docker

```bash
# Create config directory
mkdir -p searxng

# Create settings.yml (REQUIRED: enable JSON format)
cat > searxng/settings.yml << 'EOF'
use_default_settings: true
server:
  secret_key: "$(openssl rand -hex 32)"
  bind_address: "0.0.0.0"
  port: 8080
  limiter: false
  image_proxy: true
search:
  safe_search: 0
  default_lang: "all"
  formats:
    - html
    - json
EOF

# Run SearXNG
docker run -d --name searxng \
  -p 8080:8080 \
  -v "$(pwd)/searxng:/etc/searxng" \
  --restart unless-stopped \
  searxng/searxng:latest
```

## Docker Compose

```yaml
version: "3.8"
services:
  searxng:
    image: searxng/searxng:latest
    container_name: searxng
    ports:
      - "8080:8080"
    volumes:
      - ./searxng:/etc/searxng:rw
    environment:
      - SEARXNG_BASE_URL=http://localhost:8080/
    restart: unless-stopped
```

## Verify JSON API

```bash
# Should return JSON results (not HTML or 403)
curl -s 'http://localhost:8080/search?q=test&format=json' | python3 -m json.tool | head -20
```

If you get 403 Forbidden, JSON format is not enabled in `settings.yml`.

## API Endpoint Reference

### `GET /search`

| Parameter | Required | Values | Description |
|---|---|---|---|
| `q` | Yes | string | Search query |
| `format` | No | `json`, `csv`, `rss` | Response format (default: `html`) |
| `categories` | No | comma-separated | `general`, `images`, `videos`, `news`, `map`, `music`, `it`, `science`, `files`, `social media` |
| `engines` | No | comma-separated | Specific engines (e.g. `google,bing`) |
| `language` | No | lang code | `en`, `zh`, `de`, `fr`, `all`, etc. |
| `pageno` | No | integer | Page number (default: 1) |
| `time_range` | No | `day`, `month`, `year` | Time filter |
| `safesearch` | No | `0`, `1`, `2` | 0=off, 1=moderate, 2=strict |

### `GET /config`

Returns instance configuration (engines, categories, supported languages).

## Response Fields

Each result in `results[]` contains:

| Field | Type | Description |
|---|---|---|
| `title` | string | Result title |
| `url` | string | Result URL |
| `content` | string | Text snippet |
| `engine` | string | Primary source engine |
| `engines` | string[] | All engines returning this result |
| `score` | float | Aggregated relevance score |
| `category` | string | Result category |
| `positions` | int[] | Rankings in source engines |
| `publishedDate` | string | ISO date (if available) |
| `thumbnail` | string | Thumbnail URL (if available) |
| `img_src` | string | Image source URL (image results) |

Top-level response also includes:

| Field | Type | Description |
|---|---|---|
| `query` | string | Original query |
| `suggestions` | string[] | Related search suggestions |
| `answers` | string[] | Direct answers |
| `corrections` | string[] | Spelling corrections |
| `infoboxes` | object[] | Knowledge panel data |
| `unresponsive_engines` | array[] | Engines that failed `[[name, reason]]` |

## Common Engine Names

General: `google`, `bing`, `duckduckgo`, `brave`, `startpage`, `qwant`, `mojeek`
News: `google news`, `bing news`, `yahoo news`, `wikinews`
IT: `github`, `stackoverflow`, `npm`, `pypi`, `crates.io`, `dockerhub`
Science: `arxiv`, `google scholar`, `semantic scholar`, `pubmed`
Images: `google images`, `bing images`, `flickr`, `unsplash`

## Troubleshooting

**403 Forbidden**: Add `json` to `search.formats` in `settings.yml`.

**429 Rate Limited**: Disable the limiter for private instances (`limiter: false`),
or whitelist your IP in `limiter.toml` under `pass_ip`.

**Empty results**: Some engines may be rate-limited. Check `unresponsive_engines`
in the response. Try specifying different engines with `--engines`.

**Slow responses**: SearXNG queries multiple engines in parallel. Reduce latency
by limiting categories or specifying fewer engines.
