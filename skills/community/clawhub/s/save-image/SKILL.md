---
name: save-image
description: Download images, GIFs, and media from the web correctly — with proper browser headers, Referer spoofing, and CDN-aware two-step scraping. Use when any model needs to fetch an image, GIF, meme, or media file from a URL. Prevents the common failure modes of bare curl (no headers, guessed URLs, CDN blocks). Covers the full decision tree: GIF/meme → gifgrep, video/social → yt-dlp, CDN-protected image → scrape-then-fetch, plain image → curl with headers. Trigger on any request involving "download image", "save image", "grab a meme", "fetch a GIF", "get this image", or any media download from a URL.
---

# save-image

Never guess at direct image URLs. Never use bare curl with no headers. Always pick the right tool.

## Decision Tree

```
What are you downloading?
├── GIF or meme search (no specific URL) → gifgrep
├── Video or social media (YouTube, TikTok, Twitter/X, Instagram, Reddit) → yt-dlp
├── Image URL from a CDN-protected site (Imgur, KnowYourMeme, Reddit, etc.) → two-step scrape
└── Plain image URL (direct .jpg/.png/.gif link, no CDN) → curl with headers
```

See [references/tools.md](references/tools.md) for tool-specific flags and examples.

## Rule 1: Always send browser headers

Never do bare `curl <url>`. CDNs check `Referer` and `User-Agent` and block bot-looking requests.

Minimum headers for any curl image fetch:
```bash
curl -s "<url>" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" \
  -H "Referer: <origin-of-the-page-hosting-the-image>" \
  -H "Accept: image/webp,image/apng,image/*,*/*;q=0.8" \
  -o <output-file>
```

Use `scripts/fetch-image.sh` for a ready-made wrapper.

## Rule 2: Two-step scrape for CDN images

If you don't have a direct image URL (or a guessed URL fails), scrape the page first:

```bash
# Step 1: Scrape the page for real CDN image URLs
curl -s "<page-url>" \
  -H "User-Agent: Mozilla/5.0 ..." \
  | grep -oE 'https://[a-z0-9._-]+\.(com|net|org)/[^"]+\.(jpg|jpeg|png|gif|webp)' \
  | head -10

# Step 2: Download the URL you want with Referer set to the page
curl -s "<image-url>" \
  -H "Referer: <page-url>" \
  -H "User-Agent: Mozilla/5.0 ..." \
  -o <output-file>
```

## Rule 3: Verify the download

Always confirm you got an actual image, not an HTML error page:
```bash
file <output-file>
# Should say: JPEG image data / PNG image data / GIF image data
# NOT: HTML document / ASCII text
```

## Quick Examples

**GIF search (no URL):**
```bash
gifgrep "distracted boyfriend" --download --max 1
```

**KnowYourMeme / CDN-protected image:**
```bash
# Scrape page → get URL → fetch with Referer
curl -s "https://knowyourmeme.com/memes/doge" -H "User-Agent: Mozilla/5.0..." \
  | grep -oE 'https://i\.kym-cdn\.com/[^"]+\.(jpg|png|gif)' | head -3
# Then fetch the URL with Referer: https://knowyourmeme.com/
```

**Direct image URL:**
```bash
bash scripts/fetch-image.sh "https://example.com/image.jpg" ~/Downloads/image.jpg "https://example.com"
```

**Video/social media:**
```bash
yt-dlp "<url>" -o ~/Downloads/%(title)s.%(ext)s
```
