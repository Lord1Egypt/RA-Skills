---
name: twittershots
description: |
  Generate high-quality screenshots of Twitter/X posts using the TwitterShots API.
  Use when the user wants to: capture a tweet as an image, screenshot a tweet,
  generate tweet image, convert tweet to PNG/SVG/HTML, create tweet screenshot
  for social media (Instagram, TikTok), or mentions "TwitterShots", "tweet screenshot",
  "capture tweet", "tweet image". Triggers on tweet URLs (twitter.com/*/status/* or x.com/*/status/*)
  or tweet IDs. Default to format=png and theme=light without asking follow-up questions;
  if the user explicitly provides format and/or theme, use the user-provided values.
homepage: https://github.com/twittershots/skills
source: https://github.com/twittershots/skills
credentials:
  - name: TWITTERSHOTS_API_KEY
    description: API key from https://twittershots.com/settings/keys
    required: true
dependencies:
  python:
    - requests
---

# TwitterShots Skill

Generate high-quality screenshots of Twitter/X posts via REST API.

## Prerequisites

- API key from [TwitterShots Account Settings](https://twittershots.com/settings/keys)
- Store the key securely (environment variable `TWITTERSHOTS_API_KEY` recommended)

## Extract Tweet ID

Parse tweet ID from various URL formats:

```
https://twitter.com/username/status/1617979122625712128
https://x.com/username/status/1617979122625712128
https://twitter.com/username/status/1617979122625712128?s=20
```

Extract pattern: `/status/(\d+)` → Tweet ID is the numeric part after `/status/`

## API Request

**Endpoint:** `GET https://api.twittershots.com/api/v1/screenshot/:statusId`

**Required Header:**
```
X-API-KEY: YOUR_API_KEY
Accept: image/svg+xml, image/png, text/html
```

## Common Parameters

| Parameter | Default | Options | Description |
|-----------|---------|---------|-------------|
| format | png | svg, png, html | Output format (Note: API default is svg, skill defaults to png) |
| theme | light | light, dark | Color theme |
| aspectRatio | auto | auto, 1:1, 4:5, 5:4, 16:9, 9:16 | Screenshot ratio |
| returnType | buffer | buffer, url | Return image directly or URL |
| showStats | true | true, false | Show reply/retweet/like counts |
| showViews | true | true, false | Show view count |
| showTimestamp | true | true, false | Show timestamp |
| showMedia | true | true, false | Show images/videos |
| showFullText | true | true, false | Show full tweet or collapsed with "Show more" |
| mediaLayout | grid | grid, vertical | Media display layout |
| timeZoneOffset | UTC+0 | UTC±N, UTC±N:M | Fixed UTC offset for timestamp formatting |
| logo | x | x, bluebird, none | Logo style |
| width | 410 | 300-1000 | Content width in pixels |
| height | auto | auto, numeric | Content height in pixels |
| containerBackground | theme default | hex, rgba, linear-gradient | Background color |
| backgroundImage | none | HTTPS URL | Background image URL |
| borderRadius | 16 | numeric | Border radius in pixels |
| containerPadding | 16 | numeric | Padding in pixels |

## Usage Examples

### Basic Screenshot (SVG)

```bash
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?format=svg&theme=light" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Accept: image/svg+xml" \
  -o tweet.svg
```

### Dark Theme PNG

```bash
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?format=png&theme=dark" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Accept: image/png" \
  -o tweet.png
```

### Instagram Ready (4:5 ratio)

```bash
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?format=png&aspectRatio=4:5&theme=light" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Accept: image/png" \
  -o tweet-instagram.png
```

### Get URL Instead of Buffer

```bash
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?returnType=url&format=svg" \
  -H "X-API-KEY: YOUR_API_KEY"
```

Response:
```json
{
  "url": "https://i.twittershots.com/twitter-screenshots/2025/12/15/tweet-1617979122625712128-xxx.svg",
  "format": "svg",
  "tweetId": "1617979122625712128"
}
```

### Minimal Style (No Stats)

```bash
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?format=png&showStats=false&showViews=false&showTimestamp=false" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Accept: image/png" \
  -o tweet-minimal.png
```

### Custom Background

```bash
# Gradient background
curl -X GET "https://api.twittershots.com/api/v1/screenshot/1617979122625712128?format=png&containerBackground=linear-gradient(90deg,%23003f5b,%232b4b7d,%235f5195)" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Accept: image/png" \
  -o tweet-gradient.png
```

## Python Example

```python
import requests
import os

def screenshot_tweet(
    tweet_id: str,
    format: str = "png",
    theme: str = "light",
    aspect_ratio: str = "auto",
    show_full_text: bool = True,
    media_layout: str = "grid",
    time_zone_offset: str = "UTC+0",
    height: str = "auto",
    background_image: str = None,
    **kwargs
) -> bytes:
    """Generate a screenshot of a tweet."""
    api_key = os.environ.get("TWITTERSHOTS_API_KEY")
    if not api_key:
        raise ValueError("TWITTERSHOTS_API_KEY environment variable not set")
    
    params = {
        "format": format,
        "theme": theme,
        "aspectRatio": aspect_ratio,
        "showFullText": str(show_full_text).lower(),
        "mediaLayout": media_layout,
        "timeZoneOffset": time_zone_offset,
        "height": height,
        **kwargs
    }
    
    if background_image:
        params["backgroundImage"] = background_image
    
    response = requests.get(
        f"https://api.twittershots.com/api/v1/screenshot/{tweet_id}",
        headers={
            "X-API-KEY": api_key,
            "Accept": f"image/{format}" if format != "html" else "text/html"
        },
        params=params
    )
    response.raise_for_status()
    return response.content

# Extract tweet ID from URL
def extract_tweet_id(url: str) -> str:
    import re
    match = re.search(r'/status/(\d+)', url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract tweet ID from: {url}")

# Usage
tweet_url = "https://twitter.com/elonmusk/status/1617979122625712128"
tweet_id = extract_tweet_id(tweet_url)
image_data = screenshot_tweet(tweet_id, format="png", theme="dark")

with open("tweet.png", "wb") as f:
    f.write(image_data)
```

## Response Headers

Monitor quota via response headers:
- `X-Quota-Remaining`: Remaining requests
- `X-Quota-Limit`: Total quota for period

## Error Handling

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Invalid parameters |
| 401 | Missing API key |
| 403 | Invalid API key |
| 404 | Tweet not found |
| 429 | Rate limit exceeded |
| 5xx | Server error |

## Workflow

1. **Parse input**: Extract tweet ID from URL or use directly if numeric
2. **Apply defaults**: Use `format=png` and `theme=light` unless the user explicitly sets either value
3. **Build request**: Construct URL with desired parameters
4. **Execute**: Make GET request with API key header
5. **Handle response**: Save buffer to file or use returned URL
6. **Report**: Show quota remaining from response headers
