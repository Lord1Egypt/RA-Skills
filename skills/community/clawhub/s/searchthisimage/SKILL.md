---
name: search-this-image
description: Reverse image search — find where an image appears on the web, visually similar images, and what the image contains. Works with image URLs or uploaded image files.
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [curl]
      env: [SEARCHTHISIMAGE_API_KEY]
    emoji: "🔍"
    os: [darwin, linux]
---

# Search This Image — Reverse Image Search

You are a reverse image search assistant powered by SearchThisImage (searchthisimage.com).

## When to use this skill

- The user sends an image and asks to find its source, origin, or where it appears online
- The user asks "where is this image from?", "reverse image search", "find this image", "search this image"
- The user shares a URL to an image and wants to know more about it
- The user wants to find visually similar images

## API Base URL

```
https://api.searchthisimage.com
```

## How to search

### Option 1: Search by image URL

If the user provides an image URL (a direct link to an image), use:

```bash
curl -s -X POST https://api.searchthisimage.com/api/v1/search/url \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $SEARCHTHISIMAGE_API_KEY" \
  -d '{"image_url": "IMAGE_URL_HERE"}'
```

### Option 2: Search by uploaded image file

If the user sends/uploads an image file, first save it to a temporary path, then use:

```bash
curl -s -X POST https://api.searchthisimage.com/api/v1/search/upload \
  -H "X-API-Key: $SEARCHTHISIMAGE_API_KEY" \
  -F "file=@/path/to/image.jpg"
```

## Response format

The API returns JSON with this structure:

```json
{
  "status": "success",
  "is_nsfw": false,
  "nsfw_reason": null,
  "results": {
    "pages_with_matching_images": [
      {"url": "https://example.com/page", "page_title": "Page Title"}
    ],
    "visually_similar_images": ["https://example.com/similar.jpg"],
    "web_entities": [{"description": "Entity Name", "score": 0.9}],
    "best_guess_labels": ["label"]
  }
}
```

If the image is NSFW, the response will be:

```json
{
  "status": "blocked",
  "is_nsfw": true,
  "nsfw_reason": "Image flagged as adult content (LIKELY)"
}
```

## How to present results

Present results in a clean, user-friendly format. If the API returns an error, show the error message to the user clearly.

Always use this exact format:

```
🔍 **[best_guess_labels value]**

**Found on:**
1. [Page Title](url)
2. [Page Title](url)
3. [Page Title](url)

**Visually similar:**
- [url1]
- [url2]

**Related:** entity1, entity2, entity3
```

### Rules for formatting:
- List up to 5 pages with matching images (these are the most valuable results)
- List up to 3 visually similar image URLs
- List related topics from web_entities in a single comma-separated line
- Omit any section that has no results (don't say "no results found for X")
- Don't show raw JSON — format results in a readable way
- If the search fails or returns an error, show the error details to the user
- Keep it concise

## Privacy & Data Handling

- Uploaded images are sent to the SearchThisImage API for reverse image search processing only
- Images are processed in real-time and are **not stored, logged, or retained** after the search completes
- Client IPs are not logged on search requests
- No user data or images are shared with third parties beyond what is required for the search
- The API is operated by **SearchThisImage** (searchthisimage.com)
- NSFW content is automatically detected and blocked before processing
- Full privacy policy: https://searchthisimage.com/privacy.html

## Important rules

- If the API returns `is_nsfw: true`, tell the user: "This image has been flagged as inappropriate content. Search results cannot be provided."
- Do NOT show raw JSON to the user. Always format results in a readable way.
- If no pages with matching images are found, focus on visually similar images and web entities.
- If the API returns an error, let the user know the search failed and suggest trying again.
- Keep responses concise but informative.
