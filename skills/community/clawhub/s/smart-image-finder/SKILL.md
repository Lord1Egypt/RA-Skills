---
name: smart-image-finder
description: |
  Smart image search and download tool for AI agents. Three methods: news website extraction, Brave image search, AI generation.
  Use cases: article illustrations, news thumbnails, dashboard images, social media posts.
  Triggers: find image, search photo, download picture, news image, AI generate image, article illustration
version: 1.0.4
author: Justin
---

# Smart Image Finder

A complete solution for AI agents to find high-quality images for articles, dashboards, and content creation.

**No browser required** — all methods work via command line in the background.

## Core Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| **News Site Extraction** | Specific news events | Authentic, high-res, authoritative | Need to know source |
| **Brave Image Search** | General keywords | Fast, free, good relevance | Variable quality |
| **AI Generation** | Concept art, custom visuals | Fully customizable | Requires good prompts |

---

## Method 1: News Website High-Res Extraction (No Browser)

### Workflow: curl + grep (Recommended)

Extract image URLs directly from HTML without opening a browser:

```bash
# Step 1: Fetch page HTML and extract image URLs
curl -sL "https://www.reuters.com/world/article-slug/" | \
  grep -oE 'https://www\.reuters\.com/resizer/v2/[^"]+\.jpg[^"]*' | head -3

# Step 2: Download with HD parameters
curl -sL -o photo.jpg "https://www.reuters.com/resizer/v2/xxx.jpg?width=3000&quality=100"

# Step 3: Verify it's actually an image
file photo.jpg  # Should show: JPEG image data
```

### Source-Specific Extraction Patterns

```bash
# Reuters
curl -sL "$URL" | grep -oE 'https://www\.reuters\.com/resizer/v2/[^"]+\.jpg[^"]*' | head -3

# TechCrunch
curl -sL "$URL" | grep -oE 'https://techcrunch\.com/wp-content/uploads/[^"]+\.(jpg|png)' | head -3

# Bloomberg
curl -sL "$URL" | grep -oE 'https://assets\.bwbx\.io/images/[^"]+\.(jpg|webp)' | head -3

# BBC
curl -sL "$URL" | grep -oE 'https://ichef\.bbci\.co\.uk/news/[0-9]+/[^"]+\.jpg' | head -3

# France24
curl -sL "$URL" | grep -oE 'https://s\.france24\.com/media/display/[^"]+\.jpg' | head -3

# Spaceflight Now (WordPress)
curl -sL "$URL" | grep -oE 'https://spaceflightnow\.com/wp-content/uploads/[^"]+\.jpg' | head -3

# ThePaper (澎湃)
curl -sL "$URL" | grep -oE 'https://imagepphcloud\.thepaper\.cn/pph/image/[^"]+\.jpg' | head -3
```

### Verified Sources (Direct Download Works)

#### Tech/AI Category
| Source | CDN Pattern | HD Parameters | Notes |
|--------|-------------|---------------|-------|
| **TechCrunch** | `techcrunch.com/wp-content/uploads/` | `?w=2048` | Most stable ✅ |
| **Bloomberg** | `assets.bwbx.io/images/` | Direct HD | WebP format |

#### Politics/International Category
| Source | CDN Pattern | HD Parameters | Notes |
|--------|-------------|---------------|-------|
| **Reuters** | `reuters.com/resizer/v2/` | `?width=3000&quality=100` | Most stable ✅ |
| **BBC** | `ichef.bbci.co.uk/news/1024/` | `/1024/` max | Limited to 1024px |
| **NBC News** | `media-cldnry.s-nbcnews.com/image/` | Direct download | Medium size |
| **France24** | `s.france24.com/media/display/` | `w:1920` | Adjustable ✅ |

#### Space/Science Category
| Source | CDN Pattern | HD Parameters | Notes |
|--------|-------------|---------------|-------|
| **Spaceflight Now** | `spaceflightnow.com/wp-content/uploads/` | Remove size suffix | WordPress standard |

#### Chinese Sources
| Source | CDN Pattern | Notes |
|--------|-------------|-------|
| **ThePaper (澎湃)** | `imagepphcloud.thepaper.cn/pph/image/` | Direct download ✅ |

### Sources Requiring Manual Save

| Source | Issue | Workaround |
|--------|-------|------------|
| Guardian | URL signature validation | Right-click save |
| The Verge | Complex CDN format | Use Brave search instead |
| Wired | Page protection | Manual save |
| CNN | URL extraction difficult | Use Brave search instead |
| AP News | Parameter adjustment fails | Save original manually |

### HD Parameter Quick Reference

```bash
# Reuters
?width=3000&quality=100

# TechCrunch
?w=2048

# BBC (replace number in URL)
/1024/  # Max available

# France24
w:1920

# NBC News (URL parameter)
t_fit-1500w
```

---

## Method 2: Brave Image Search (No Browser)

Best for: Quick general-purpose images, automated workflows.

### Basic Usage

```bash
# Set API Key (first time)
export BRAVE_API_KEY="your_api_key"

# Search images
curl -s "https://api.search.brave.com/res/v1/images/search?q=keyword&count=10" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq '.results[] | {title, url: .properties.url, width: .properties.width}'

# Get first image URL directly
curl -s "https://api.search.brave.com/res/v1/images/search?q=SpaceX%20Starship&count=1" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url'
```

### Rate Limiting ⚠️

Brave API has rate limits. When making multiple searches:

```bash
# Add delay between requests (1-2 seconds recommended)
for query in "query1" "query2" "query3"; do
  curl -s "https://api.search.brave.com/res/v1/images/search?q=$query&count=1" \
    -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url'
  sleep 2  # Wait 2 seconds between requests
done
```

**Best practices:**
- Free tier: ~1 request/second max
- Add `sleep 1` or `sleep 2` between batch requests
- If you get 429 (rate limited), wait 60 seconds before retrying

### Search Tips

1. **Add year**: `SpaceX Starship 2025` is more precise than `SpaceX Starship`
2. **Add event terms**: `Keir Starmer Xi Jinping Beijing handshake` beats `UK China meeting`
3. **Site restriction**: `site:reuters.com Trump tariff` limits to specific source

### One-liner: Search and Download

```bash
# Search, get first result URL, download
IMG_URL=$(curl -s "https://api.search.brave.com/res/v1/images/search?q=SpaceX%20launch%202025&count=1" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url')
curl -sL -o spacex.jpg "$IMG_URL"
file spacex.jpg
```

### Verify Image Accessibility

```bash
# Check if URL returns 200
curl -sI "$IMAGE_URL" | head -1
# Should return: HTTP/2 200

# Check content type
curl -sI "$IMAGE_URL" | grep -i content-type
# Should return: content-type: image/jpeg or image/png
```

---

## Method 3: AI Image Generation (No Browser)

Best for: Concept images, creative illustrations, when real photos unavailable.

### Free Option: Pollinations

```bash
# Generate image (completely free, no API key needed)
curl -sL -o output.jpg "https://image.pollinations.ai/prompt/description?width=1920&height=1080&nologo=true"

# Example: Tech-style AI concept image
curl -sL -o ai-concept.jpg "https://image.pollinations.ai/prompt/futuristic%20AI%20chip%20glowing%20blue%20on%20dark%20background%20minimalist%20tech%20style?width=1920&height=1080&nologo=true"
```

### Prompt Best Practices

```
# Good prompt structure
{subject} + {style} + {color tone} + {composition} + {exclusions}

# Example
"Sam Altman speaking at conference, professional photo, warm lighting, 
 shallow depth of field, high resolution, no text no watermark"

# 16:9 cover image
"... 16:9 aspect ratio, horizontal composition, clean space on right for text overlay"

# Avoid garbled text
"... no text, no letters, no words, no watermarks"
```

### Platform Comparison

| Platform | Prompt Language | Size Params | Notes |
|----------|-----------------|-------------|-------|
| Pollinations | English | width/height | Free unlimited |
| Jimeng (即梦) | Chinese | 16:9/1:1 | Best for Chinese scenes |
| DALL-E | English | 1792x1024 | Highest quality |

---

## Complete Workflow Example (All CLI, No Browser)

### Scenario: Find image for "UK PM visits China" article

```bash
# Option A: Extract from Reuters (no browser)
# 1. Find article URL via web search or known URL
# 2. Extract image URL from HTML
IMG_URL=$(curl -sL "https://www.reuters.com/world/uk-pm-china-visit/" | \
  grep -oE 'https://www\.reuters\.com/resizer/v2/[^"]+\.jpg' | head -1)
# 3. Download with HD params
curl -sL -o starmer-xi.jpg "${IMG_URL}?width=3000&quality=100"

# Option B: Brave search (no browser)
IMG_URL=$(curl -s "https://api.search.brave.com/res/v1/images/search?q=Keir%20Starmer%20Xi%20Jinping%202025&count=1" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url')
curl -sL -o starmer-xi.jpg "$IMG_URL"

# Option C: AI generate (no browser)
curl -sL -o uk-china.jpg "https://image.pollinations.ai/prompt/British%20and%20Chinese%20flags%20diplomatic%20meeting%20minimalist?width=1920&height=1080&nologo=true"

# Verify result
file starmer-xi.jpg
ls -lh starmer-xi.jpg
```

---

## Quick Reference Card

### Choose Method by Scenario

| Need | Recommended Method | Reason |
|------|-------------------|--------|
| Specific news event | News site extraction | Authentic, authoritative |
| General concept image | Brave search | Fast, free |
| No suitable real photo | AI generation | Fully customizable |
| Article cover | AI generation | Controllable text space |
| Dashboard news | Brave search | Automation-friendly |

### Image Quality Checklist

- [ ] Resolution ≥ 1200px width
- [ ] File size > 50KB (smaller likely thumbnail)
- [ ] `file` command confirms image (not HTML)
- [ ] No watermarks
- [ ] No copyright issues (news images for commentary/citation)

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| curl returns HTML | Hotlink protection/signature | Try different source or Brave search |
| Image 403 | URL expired | Re-fetch URL |
| Blurry image | Downloaded thumbnail | Adjust HD parameters |
| Brave no results | Keywords too specific | Simplify keywords |
| grep returns empty | Page uses JavaScript rendering | Use Brave search instead |
