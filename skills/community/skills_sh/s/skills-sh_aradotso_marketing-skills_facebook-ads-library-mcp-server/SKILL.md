---
name: facebook-ads-library-mcp-server
description: MCP server for querying and analyzing Facebook Ads Library data with batch processing and AI-powered video/image analysis
triggers:
  - "search Facebook ads for a brand"
  - "analyze competitor advertising strategies"
  - "get ads running by multiple companies"
  - "compare ad campaigns across brands"
  - "analyze video ads creative strategy"
  - "check what ads a company is running"
  - "batch analyze Facebook ad videos"
  - "find advertising themes for brands"
---

# Facebook Ads Library MCP Server

> Skill by [ara.so](https://ara.so) — Marketing Skills collection

This MCP (Model Context Protocol) server enables AI agents to query Facebook's public Ads Library API, retrieve advertising data for brands, and perform AI-powered analysis of ad creative including images and videos. It supports batch processing for efficient multi-brand queries and includes intelligent caching and credit management.

## What It Does

- **Brand Search**: Convert brand names to Meta platform IDs
- **Ad Retrieval**: Fetch currently running ads for one or multiple brands
- **Image Analysis**: Analyze ad images for visual elements, text, colors, and composition
- **Video Analysis**: Deep analysis of video ads using Gemini AI (pacing, storytelling, messaging)
- **Batch Processing**: Query multiple brands or platform IDs simultaneously with ~88% token savings
- **Smart Caching**: Reduces API calls and improves performance
- **Credit Management**: Automatic detection of API credit exhaustion

## Installation

### Quick Install

```bash
git clone https://github.com/proxy-intell/facebook-ads-library-mcp.git
cd facebook-ads-library-mcp

# Run installer
./install.sh  # macOS/Linux
# OR
install.bat   # Windows
```

### Manual Setup

```bash
# Clone repository
git clone https://github.com/proxy-intell/facebook-ads-library-mcp.git
cd facebook-ads-library-mcp

# Create virtual environment
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Configure environment
cp .env.template .env
# Edit .env and add:
# SCRAPECREATORS_API_KEY=your_key_here
# GEMINI_API_KEY=your_gemini_key_here (optional, for video analysis)
```

### MCP Configuration

**Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fb_ad_library": {
      "command": "/full/path/to/facebook-ads-library-mcp/venv/bin/python",
      "args": [
        "/full/path/to/facebook-ads-library-mcp/mcp_server.py"
      ]
    }
  }
}
```

**Cursor** (`~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "fb_ad_library": {
      "command": "/full/path/to/facebook-ads-library-mcp/venv/bin/python",
      "args": [
        "/full/path/to/facebook-ads-library-mcp/mcp_server.py"
      ]
    }
  }
}
```

Replace `/full/path/to/` with your actual project path.

## API Keys Required

1. **ScrapeCreators API** (required): Sign up at [scrapecreators.com](https://scrapecreators.com/?via=tntm)
2. **Google Gemini API** (optional, for video analysis): Get key at [Google AI Studio](https://aistudio.google.com/app/apikey)

Store keys in `.env` file:

```bash
SCRAPECREATORS_API_KEY=your_scrapecreators_key
GEMINI_API_KEY=your_gemini_key
```

## Available MCP Tools

### 1. get_meta_platform_id

Converts brand name(s) to Meta platform ID(s).

**Input**: Single brand name (string) or multiple brands (array)

```python
# Single brand
{
  "brand_name": "Nike"
}

# Multiple brands (batch)
{
  "brand_name": ["Nike", "Adidas", "Under Armour"]
}
```

**Output**:
```json
{
  "Nike": "123456789",
  "Adidas": "987654321",
  "Under Armour": "456789123"
}
```

### 2. get_meta_ads

Retrieves currently running ads for platform ID(s).

**Input**: Single platform ID (string) or multiple IDs (array)

```python
# Single platform
{
  "platform_id": "123456789"
}

# Multiple platforms (batch)
{
  "platform_id": ["123456789", "987654321"]
}
```

**Output**:
```json
{
  "123456789": {
    "ads": [
      {
        "id": "ad_id_123",
        "ad_creative_body": "Ad text content",
        "ad_snapshot_url": "https://...",
        "images": ["https://image1.jpg"],
        "videos": ["https://video1.mp4"]
      }
    ]
  }
}
```

### 3. analyze_ad_image

Analyzes visual elements in ad images.

**Input**:
```python
{
  "image_url": "https://example.com/ad-image.jpg"
}
```

**Output**: Detailed analysis of colors, composition, text, people, emotions, and visual elements.

### 4. analyze_ad_video

Analyzes a single video ad using Gemini AI.

**Input**:
```python
{
  "video_url": "https://example.com/ad-video.mp4"
}
```

**Output**: Comprehensive analysis including pacing, storytelling, brand messaging, visual techniques, and strategic insights.

### 5. analyze_ad_videos_batch

Analyzes multiple videos in a single API call (~88% token savings).

**Input**:
```python
{
  "video_urls": [
    "https://example.com/video1.mp4",
    "https://example.com/video2.mp4",
    "https://example.com/video3.mp4"
  ]
}
```

**Output**: Array of analyses, one per video, with comparative insights.

### 6. get_cache_stats

Returns statistics about cached media.

**Output**:
```json
{
  "total_cached_items": 42,
  "images": 30,
  "videos": 12,
  "total_size_mb": 156.7,
  "oldest_cache": "2025-01-15T10:30:00Z"
}
```

### 7. search_cached_media

Searches previously analyzed media.

**Input**:
```python
{
  "brand": "Nike",          # Optional
  "colors": ["red", "blue"], # Optional
  "has_people": true,       # Optional
  "media_type": "image"     # Optional: "image" or "video"
}
```

### 8. cleanup_media_cache

Removes old cached media files.

**Input**:
```python
{
  "days_old": 30  # Remove cache older than 30 days
}
```

## Common Usage Patterns

### Single Brand Analysis

```python
# Agent workflow:
# 1. Get platform ID
platform_id_result = get_meta_platform_id({"brand_name": "Nike"})
platform_id = platform_id_result["Nike"]

# 2. Get ads
ads_result = get_meta_ads({"platform_id": platform_id})
ads = ads_result[platform_id]["ads"]

# 3. Analyze first video ad
video_url = ads[0]["videos"][0]
video_analysis = analyze_ad_video({"video_url": video_url})
```

### Multi-Brand Competitive Analysis

```python
# Agent workflow for batch processing:
brands = ["Nike", "Adidas", "Under Armour", "Puma"]

# 1. Get all platform IDs at once (batch)
platform_ids = get_meta_platform_id({"brand_name": brands})

# 2. Get all ads at once (batch)
all_platform_ids = list(platform_ids.values())
ads_data = get_meta_ads({"platform_id": all_platform_ids})

# 3. Collect video URLs
video_urls = []
for platform_id, data in ads_data.items():
    for ad in data["ads"]:
        if ad.get("videos"):
            video_urls.extend(ad["videos"][:2])  # First 2 videos per brand

# 4. Batch analyze all videos (huge token savings)
video_analyses = analyze_ad_videos_batch({"video_urls": video_urls})
```

### Filtering and Search

```python
# Find all Nike ads with people in red/white colors
cached_results = search_cached_media({
    "brand": "Nike",
    "colors": ["red", "white"],
    "has_people": True,
    "media_type": "image"
})

# Get fresh data and analyze
for result in cached_results:
    print(f"Ad ID: {result['ad_id']}")
    print(f"Analysis: {result['analysis']}")
```

## Code Examples

### Example 1: Basic Brand Ad Check

```python
import json
from mcp import get_meta_platform_id, get_meta_ads

# Get Nike's platform ID
platform_data = get_meta_platform_id({"brand_name": "Nike"})
nike_id = platform_data["Nike"]

# Get their current ads
ads = get_meta_ads({"platform_id": nike_id})
nike_ads = ads[nike_id]["ads"]

print(f"Nike is running {len(nike_ads)} ads")
for ad in nike_ads:
    print(f"- {ad['ad_creative_body'][:100]}...")
```

### Example 2: Competitor Video Strategy Comparison

```python
from mcp import get_meta_platform_id, get_meta_ads, analyze_ad_videos_batch

# Define competitors
brands = ["Coca-Cola", "Pepsi", "Dr Pepper"]

# Get platform IDs (batch)
platform_ids = get_meta_platform_id({"brand_name": brands})

# Get all ads (batch)
all_ids = list(platform_ids.values())
all_ads = get_meta_ads({"platform_id": all_ids})

# Collect video URLs
video_map = {}  # Maps video URL to brand
for brand, pid in platform_ids.items():
    for ad in all_ads[pid]["ads"]:
        if ad.get("videos"):
            for video_url in ad["videos"][:1]:  # First video only
                video_map[video_url] = brand

# Batch analyze
video_urls = list(video_map.keys())
analyses = analyze_ad_videos_batch({"video_urls": video_urls})

# Map results back to brands
brand_strategies = {}
for i, video_url in enumerate(video_urls):
    brand = video_map[video_url]
    if brand not in brand_strategies:
        brand_strategies[brand] = []
    brand_strategies[brand].append(analyses[i])

# Print comparison
for brand, strategies in brand_strategies.items():
    print(f"\n{brand} Video Strategy:")
    print(json.dumps(strategies[0], indent=2))
```

### Example 3: Image Analysis with Filtering

```python
from mcp import get_meta_ads, analyze_ad_image

# Get ads for a platform
ads = get_meta_ads({"platform_id": "123456789"})

# Analyze images
for ad in ads["123456789"]["ads"]:
    if ad.get("images"):
        image_url = ad["images"][0]
        analysis = analyze_ad_image({"image_url": image_url})
        
        # Check if red color is dominant
        colors = analysis.get("dominant_colors", [])
        if any("red" in c.lower() for c in colors):
            print(f"Red-dominant ad found: {ad['id']}")
            print(f"Colors: {colors}")
            print(f"Has people: {analysis.get('has_people', False)}")
```

## Environment Variables

All configuration is stored in `.env`:

```bash
# Required for ad retrieval
SCRAPECREATORS_API_KEY=your_api_key_here

# Optional for video analysis
GEMINI_API_KEY=your_gemini_api_key_here

# Optional cache settings (defaults shown)
CACHE_DIR=./cache
MAX_CACHE_SIZE_MB=1000
CACHE_EXPIRY_DAYS=30
```

## Troubleshooting

### API Credits Exhausted

**Error**: "ScrapeCreators API credits exhausted"

**Solution**: Top up credits at [ScrapeCreators Dashboard](https://scrapecreators.com/dashboard?via=tntm). The server will automatically resume once credits are available.

### Rate Limit Exceeded

**Error**: Rate limit messages with wait time

**Solution**: 
- Space out large batch requests
- Use batch operations to reduce total API calls
- Wait the specified time before retrying

### Video Analysis Not Working

**Problem**: Video analysis returns errors or empty results

**Check**:
1. Ensure `GEMINI_API_KEY` is set in `.env`
2. Verify Gemini API key is valid at [Google AI Studio](https://aistudio.google.com/)
3. Check video URL is accessible
4. Ensure video file size is under Gemini's limits

### MCP Server Connection Issues

**Problem**: Agent can't connect to MCP server

**Check**:
1. Verify virtual environment is activated and dependencies installed
2. Check MCP config file points to correct Python path (`venv/bin/python`)
3. Ensure `.env` file exists with API keys
4. Restart Claude Desktop or Cursor after config changes
5. Check logs in Claude Desktop: `~/Library/Logs/Claude/`

### Import Errors

**Error**: `ModuleNotFoundError` or import failures

**Solution**:
```bash
cd facebook-ads-library-mcp
./venv/bin/pip install -r requirements.txt --upgrade
```

### Cache Issues

**Problem**: Stale or incorrect cached data

**Solution**:
```python
# Clean old cache (older than 7 days)
cleanup_media_cache({"days_old": 7})

# Or manually remove cache directory
rm -rf ./cache
```

## Performance Tips

1. **Use Batch Operations**: Always prefer batch API calls when analyzing multiple brands
2. **Leverage Cache**: Check `search_cached_media` before making new API requests
3. **Video Batch Analysis**: Use `analyze_ad_videos_batch` instead of multiple single calls (88% token savings)
4. **Limit Results**: When querying ads, process only what you need (e.g., first 5 ads per brand)
5. **Monitor Credits**: Check ScrapeCreators dashboard regularly to avoid interruptions

## Integration Examples

### With LangChain

```python
from langchain.tools import Tool
from mcp import get_meta_platform_id, get_meta_ads

tools = [
    Tool(
        name="get_facebook_ads",
        func=lambda brand: get_meta_ads({
            "platform_id": get_meta_platform_id({"brand_name": brand})[brand]
        }),
        description="Get current Facebook ads for a brand"
    )
]
```

### With Custom Python Scripts

```python
#!/usr/bin/env python3
import sys
import json
from pathlib import Path

# Add MCP server to path
sys.path.insert(0, str(Path(__file__).parent / "facebook-ads-library-mcp"))

from mcp_server import get_meta_platform_id, get_meta_ads

def main():
    brand = input("Enter brand name: ")
    platform_id = get_meta_platform_id({"brand_name": brand})[brand]
    ads = get_meta_ads({"platform_id": platform_id})
    print(json.dumps(ads, indent=2))

if __name__ == "__main__":
    main()
```
