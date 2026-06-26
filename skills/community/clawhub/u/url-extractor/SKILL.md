---
name: url-extractor
description: Extract and validate URLs from text, presenting results in a clear format with brief descriptions and image previews. 
---

# URL Extractor

Quickly extract all URLs from text, validate them, and present results in a structured format.

## Use Cases

Use when users need to "extract links", "extract URLs", "find web addresses", or "extract links from text".

## Workflow

### 1. Text Analysis & Extraction

Quickly identify and extract all possible URLs from user-provided text:
- Full URLs (starting with `https://` or `http://`)
- Domain-style links (e.g., `example.com/path`)
- Ensure extracted URLs are correctly formatted and not truncated

### 2. Validation

Validate extracted URLs:
- Use the `web_fetch` tool to access each URL and confirm accessibility
- Extract page titles as URL descriptions
- If a URL returns an image (`Content-Type: image/*`), mark it as previewable
- Mark inaccessible URLs as `❌ Unreachable`

### 3. Present Results

Output in a structured format:

```
## Extraction Results

N URLs extracted (M accessible, K unreachable)

| # | URL | Status | Title/Description |
|---|-----|--------|-------------------|
| 1 | https://example.com | ✅ | Example Domain |
| 2 | https://example.com/img.png | ✅ 🖼️ | Image Preview |
| 3 | https://broken.link | ❌ | Unreachable |

### Image Previews
[For image URLs, use the image tool to show previews]
```

## Notes

- Only handle tasks related to URL extraction and validation
- Do not provide detailed analysis of URL content unless explicitly requested
- Extracted URLs must be valid and relevant to the user's query
- For large numbers of URLs (>20), prioritize validating the first 20; list the rest as pending