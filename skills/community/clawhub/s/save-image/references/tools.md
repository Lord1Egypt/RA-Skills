# Tool Reference

## gifgrep — GIF and meme search

Use when searching by keyword (no specific URL). Handles Tenor/Giphy, proper headers, downloads cleanly.

```bash
# Search and print URLs
gifgrep "doge" --max 5 --format url

# Download first result
gifgrep "distracted boyfriend" --download --max 1

# JSON output (id, title, url, dimensions)
gifgrep search --json "this is fine" | jq '.[0]'

# Interactive TUI browser
gifgrep tui "muppets"

# Extract a still frame from a downloaded GIF
gifgrep still ./clip.gif --at 1.5s -o still.png

# Generate a sprite sheet (9 frames, 3-col grid)
gifgrep sheet ./clip.gif --frames 9 --cols 3 -o sheet.png
```

Providers: `--source auto|tenor|giphy` (GIPHY_API_KEY required for Giphy)

---

## yt-dlp — Video and social media

Use for YouTube, TikTok, Twitter/X, Instagram, Reddit, and 1000+ other sites.

```bash
# Download video (best quality)
yt-dlp "<url>" -o ~/Downloads/%(title)s.%(ext)s

# Extract audio only
yt-dlp -x --audio-format mp3 "<url>" -o ~/Downloads/%(title)s.%(ext)s

# List available formats
yt-dlp -F "<url>"

# Download specific format
yt-dlp -f 137+140 "<url>"

# Thumbnail only
yt-dlp --write-thumbnail --skip-download "<url>"
```

---

## curl with headers — Direct image URLs

Use for plain image URLs or CDN-protected images after scraping the real URL.

### Minimum viable headers
```bash
curl -s "<url>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
  -H "Referer: <page-url>" \
  -H "Accept: image/webp,image/apng,image/*,*/*;q=0.8" \
  -o <output-file> \
  -w "%{http_code} | %{size_download} bytes\n"
```

### Two-step scrape pattern
```bash
# 1. Get real CDN URLs from the page
curl -s "<page-url>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ..." \
  | grep -oE 'https://[a-z0-9._-]+\.(com|net|org)/[^"'\'']+\.(jpg|jpeg|png|gif|webp)' \
  | sort -u | head -10

# 2. Fetch the image with Referer pointing back to the page
curl -s "<cdn-image-url>" \
  -H "Referer: <page-url>" \
  -H "User-Agent: Mozilla/5.0 ..." \
  -o <output-file>
```

### Known CDN Referer requirements
| Site | CDN domain | Required Referer |
|------|-----------|-----------------|
| KnowYourMeme | i.kym-cdn.com | https://knowyourmeme.com/ |
| Imgur | i.imgur.com | https://imgur.com/ |
| Reddit media | preview.redd.it / i.redd.it | https://www.reddit.com/ |
| Giphy | media.giphy.com | https://giphy.com/ |
| Tenor | media.tenor.com | https://tenor.com/ |

---

## What won't work

- **Cloudflare-protected sites** — JS challenge required; curl can't solve it regardless of headers
- **Login-gated images** — Need session cookies; use browser automation instead
- **Signed S3/CDN URLs with expiry** — URL itself contains auth; must be scraped fresh each time
