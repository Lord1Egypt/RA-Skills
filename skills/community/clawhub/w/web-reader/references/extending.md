# Adding a New Platform

How to extend web-fetcher with support for a new website.

## Step 1: Add Route Entry

Edit `lib/router.py` and add an entry to `ROUTE_TABLE`:

```python
ROUTE_TABLE = {
    # ... existing entries ...
    "example.com": {
        "type": "article",      # "article" or "video"
        "method": "scrapling",  # "scrapling", "camoufox", "ytdlp", or "feishu"
        "selector": ".content", # CSS selector for main content (None for full page)
        "post": "default_images"  # Image post-processing hook name
    },
}
```

### Route Fields

| Field | Values | Description |
|-------|--------|-------------|
| `type` | `article`, `video` | Determines which handler to use |
| `method` | `scrapling`, `camoufox`, `ytdlp`, `feishu` | Fetch strategy |
| `selector` | CSS selector or `None` | Content extraction selector |
| `post` | `default_images`, `wx_images`, `toutiao_images` | Image processing hook |

## Step 2: Add Image Post-Processing Hook (if needed)

If the platform has non-standard image loading (lazy load, base64 placeholders, etc.), add a hook in `lib/article.py`:

```python
def _mysite_image_hook(md_text, html_text, img_dir):
    """MySite-specific: extract real image URLs from data attributes."""
    # 1. Find real image URLs in html_text
    urls = re.findall(r'data-original="(https://[^"]+)"', html_text)
    # 2. Download each image
    os.makedirs(img_dir, exist_ok=True)
    for i, url in enumerate(urls):
        local_name = f"img_{i:02d}.jpg"
        local_path = os.path.join(img_dir, local_name)
        _download_image(url, local_path, referer="https://example.com/")
        md_text = md_text.replace(url, os.path.join("images", os.path.basename(img_dir), local_name))
    return md_text
```

Then register it in `fetch_article()`:

```python
if post_hook == "mysite_images":
    md_text = _mysite_image_hook(md_text, html_text, img_dir)
```

## Step 3: Add Dedicated Handler (if needed)

For platforms that need entirely custom logic (like Feishu's virtual scroll), create a new module `lib/mysite.py`:

```python
def fetch_mysite(url, output_dir, no_images=False):
    """Fetch content from MySite. Returns output path."""
    # Custom logic here
    pass
```

Then add routing in `fetcher.py`:

```python
elif r["method"] == "mysite":
    result = fetch_mysite(url, args.output, no_images=args.no_images)
```

## Testing

Always test with a real URL after adding a platform:

```bash
python3 fetcher.py "https://example.com/article/123" -o /tmp/test
```

Check:
1. Markdown output has meaningful content (not empty/garbled)
2. Images are downloaded locally (if applicable)
3. Image URLs in markdown point to local paths
