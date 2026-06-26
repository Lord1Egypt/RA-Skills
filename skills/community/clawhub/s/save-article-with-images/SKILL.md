---
name: save-article-with-images
version: 1.0.1
author: barryqin9999
description: >
  Save web articles locally with images. Automatically downloads images, generates Markdown, and converts to PDF.
  Supports WeChat Official Account articles via subagent isolation.
  Triggers: save article, save this article, download article, clip article, wechat article.
---

# Save Article with Images

Save web articles to local storage, supporting articles with images. Automatically downloads images, generates Markdown, and converts to PDF.

## Triggers

- "save article"
- "save this article"
- "download article"
- "clip article"

---

## Quick Execution

### Articles Without Images

```
1. Fetch article content (Jina Reader or browser)
2. Save to saved-articles/{title}-{date}.md
3. Send file to Feishu
```

### Articles With Images

```
1. Create directory reports/{article-name}/
2. Create images/ subdirectory
3. Download all images to images/
4. Generate Markdown (relative path references)
5. Convert to PDF
6. Send PDF to Feishu
```

---

## Complete Workflow

### Step 1: Check if Article Has Images

**Methods**:
- Jina Reader returns content with `![Image](URL)` format
- Or original webpage has `<img>` tags

**Decision**:
- Images < 3 → Save Markdown directly, don't download images separately
- Images ≥ 3 → Process with image workflow

---

### Step 2: Create Directory Structure

```bash
mkdir -p ~/.openclaw/workspace/reports/{article-name}/images/
```

**Directory Structure**:
```
reports/{article-name}/
├── {article-name}.md      # Markdown file
├── {article-name}.html    # HTML intermediate (optional)
├── {article-name}.pdf     # Final output (optional)
└── images/                # Image directory
    ├── image1.jpg
    ├── image2.png
    └── ...
```

---

### Step 3: Fetch Article Content

#### Method A: Jina Reader (Recommended)

```bash
curl -s "https://r.jina.ai/URL"
```

**Pros**: Auto-converts to Markdown, extracts image links
**Cons**: Some sites blocked

#### Method B: Browser Fetch

```bash
# Open webpage
browser action=open url=URL

# Get content
browser action=act kind=evaluate fn='() => document.body.innerText'

# Get images
browser action=act kind=evaluate fn='() => {
  const imgs = document.querySelectorAll("img");
  return JSON.stringify(Array.from(imgs).map(img => ({
    src: img.src,
    alt: img.alt
  })));
}'
```

---

### Step 4: Download Images

**Single Image**:

```bash
curl -o "images/image1.jpg" "https://example.com/image.jpg"
```

**Batch Download (Python)**:

```python
import requests
from pathlib import Path

def download_images(image_urls, output_dir):
    """Download image list"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, url in enumerate(image_urls, 1):
        try:
            # Get extension
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
                ext = 'jpg'
            
            # Download
            resp = requests.get(url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            
            if resp.status_code == 200:
                filename = f"image{i}.{ext}"
                (output_dir / filename).write_bytes(resp.content)
                print(f"✅ {filename}")
            else:
                print(f"❌ HTTP {resp.status_code}: {url}")
        except Exception as e:
            print(f"❌ {e}: {url}")

# Usage
# download_images(['url1', 'url2'], 'images/')
```

**Image Naming**:
- Sequential: `image1.jpg`, `image2.png`, ...
- By content: `cover.jpg`, `screenshot.png`, ...

---

### Step 5: Generate Markdown

**Template**:

```markdown
# {Article Title}

> Source: {URL}
> Author: {author}
> Published: {date}

---

![Cover](images/image1.jpg)

{Content}

---

## Images

![Figure 1: {description}](images/image2.jpg)
![Figure 2: {description}](images/image3.png)

---

*Saved: {timestamp}*
```

**Image Reference Format**:
```markdown
![Description](images/filename.ext)
```

---

### Step 6: Convert to PDF (Optional)

**Using Preset Styles**:

```bash
# CSS file
CSS_FILE=~/.openclaw/workspace/templates/mobile-friendly.css

# Convert to HTML
pandoc {article-name}.md -o {article-name}.html --standalone --css=$CSS_FILE

# Generate PDF
weasyprint {article-name}.html {article-name}.pdf
```

**PDF Configuration**:
- Body: 16pt, line-height 1.8
- Page: 6×9 inches, margins 1.5cm
- Font: Noto Sans CJK SC

### ⚠️ Image Overflow Solution (Important)

**Problem**: Images too large (e.g., 1200px wide), exceed PDF page width (~432pt/6 inches)

**Solution**: Create CSS file to limit image max-width

**Required CSS**:
```css
/* Prevent image overflow */
img {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1em auto;
}

/* Images in images/ directory - 90% width */
img[src^="images/"] {
  max-width: 90%;
  margin: 0.5em auto;
}

/* Body styles */
body {
  max-width: 100%;
  padding: 1cm;
}
```

**Correct PDF Generation Flow**:
```bash
# 1. Create CSS file (in article directory)
cat > style.css << 'EOF'
img { max-width: 100%; height: auto; }
img[src^="images/"] { max-width: 90%; }
EOF

# 2. Generate HTML with CSS
pandoc {article-name}.md -o {article-name}.html --standalone --css=style.css

# 3. Generate PDF
weasyprint {article-name}.html {article-name}.pdf
```

**Key Points**:
- ✅ Must add `max-width: 100%` or `max-width: 90%`
- ✅ Use relative paths `images/xxx.jpg`
- ❌ Don't render images at original size (will overflow)

---

### Step 7: Send to Feishu

**Send Markdown**:
```
message action=send channel=feishu target="user:ou_xxx" filePath="path/to/file.md"
```

**Send PDF**:
```
message action=send channel=feishu target="user:ou_xxx" filePath="path/to/file.pdf"
```

---

## Platform-Specific Handling

| Source | Fetch Method | Image Handling |
|--------|--------------|----------------|
| **Twitter/X** | Jina Reader | Download pbs.twimg.com images |
| **WeChat Official Account** | browser + Camoufox | Download mmbiz.qpic.cn images |
| **General Webpages** | Jina Reader | Download all img tags |
| **Login Required Sites** | browser | User manual screenshot |

---

## Twitter/X Articles

**Image URL Format**:
```
https://pbs.twimg.com/media/XXXXX?format=jpg&name=small
```

**Download Command**:
```bash
# Get best quality
curl -o "images/image1.jpg" "https://pbs.twimg.com/media/XXXXX?format=jpg&name=large"
```

---

## WeChat Official Account Articles

**Problem**: WeChat has anti-hotlinking, direct download fails

**Solutions**:
1. Use browser to open article
2. Save screenshot
3. Or use Camoufox tool

```bash
# Use tool from agent-reach
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "https://mp.weixin.qq.com/s/ARTICLE_ID"
```

---

## Checklist

After saving, verify:

```
□ Markdown file generated
□ All images downloaded successfully
□ Image relative paths correct
□ Images display correctly (local preview)
□ PDF generated successfully (optional)
□ File sent to Feishu
```

---

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Image download failed | Anti-hotlinking/Network | Use browser or lower quality |
| PDF generation failed | Missing fonts/dependencies | Check weasyprint installation |
| Markdown images not showing | Path error | Check relative paths |
| Jina Reader blocked | Site restriction | Use browser fetch |

---

## File Locations

| Type | Directory |
|------|-----------|
| Simple articles | `saved-articles/{title}-{date}.md` |
| Articles with images | `reports/{article-name}/` |
| Temporary files | `/tmp/article-{id}/` |

---

*Skill Version: 1.0.0*
*Created: 2026-03-17*