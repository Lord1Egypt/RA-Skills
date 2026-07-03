---
name: wp-publisher
description: "Publish WordPress posts via REST API from any OpenClaw channel (WeChat/QQ/DingTalk/etc). AI writes in Markdown, auto-converts to HTML, posts to your blog, and returns the link."
---

# WP Publisher — Remote WordPress Blog Publishing

Publish posts to your WordPress blog from any OpenClaw channel. Send "发布博客" in WeChat and AI handles the rest.

## Prerequisites

1. WordPress site with REST API enabled (native since WP 4.7)
2. Create an Application Password: WP Admin → Users → Profile → Application Passwords
3. Configure these env vars or replace in commands:
   - `WP_API_BASE`: `https://your-blog.com/wp-json/wp/v2`
   - `WP_USER`: Your WordPress username
   - `WP_APP_PASSWORD`: Generated application password

## Available Categories (customize per site)

Get your own categories:
```bash
curl -sk -u "USER:PASS" "$WP_API_BASE/categories?per_page=50" | python3 -c "
import sys,json
for c in json.load(sys.stdin):
    print(f'{c[\"id\"]}: {c[\"name\"]}')
"
```

## API Operations

### Create Post (Publish)

```bash
curl -sk -u "USER:PASS" \
  -X POST "$WP_API_BASE/posts" \
  -H 'Content-Type: application/json' \
  -d '{
    "title": "Post Title",
    "content": "<p>HTML content here</p>",
    "status": "publish",
    "categories": [CAT_ID],
    "slug": "post-slug"
  }' | python3 -c "import sys,json;d=json.load(sys.stdin);print(f'Published: {d[\"link\"]}')"
```

Params:
- `status`: `publish` | `draft` | `future` (with `date` field)
- `categories`: array of category IDs
- `slug`: URL slug (optional, auto-generated from title)
- `tags`: array of tag IDs (optional)

### List Posts

```bash
curl -sk -u "USER:PASS" "$WP_API_BASE/posts?per_page=5&search=keyword"
```

### Update Post

```bash
curl -sk -u "USER:PASS" \
  -X PUT "$WP_API_BASE/posts/POST_ID" \
  -H 'Content-Type: application/json' \
  -d '{"title":"New Title","content":"<p>Updated</p>"}'
```

### Delete Post

```bash
curl -sk -u "USER:PASS" -X DELETE "$WP_API_BASE/posts/POST_ID?force=true"
```

## Workflow

When user asks to publish a blog post:

1. **Confirm topic + category** — Ask if not specified
2. **Generate content** — Write article in Markdown, then convert to HTML
3. **Call API** — POST to WordPress REST API with Basic Auth
4. **Reply with link** — Give user the published article URL

## Markdown → HTML Conversion

Run this Python snippet before posting:

```python
import re

def md2html(md):
    md = re.sub(r'```([\s\S]*?)```', r'<pre><code>\1</code></pre>', md)
    md = re.sub(r'`([^`]+)`', r'<code>\1</code>', md)
    md = re.sub(r'^### (.+)$', r'<h4>\1</h4>', md, flags=re.M)
    md = re.sub(r'^## (.+)$', r'<h3>\1</h3>', md, flags=re.M)
    md = re.sub(r'^# (.+)$', r'<h2>\1</h2>', md, flags=re.M)
    md = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', md)
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.+?)\*', r'<em>\1</em>', md)
    md = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', md)
    md = re.sub(r'^- (.+)$', r'<li>\1</li>', md, flags=re.M)
    md = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', md)
    md = re.sub(r'^(?!<[a-z/]|$)(.+)$', r'<p>\1</p>', md, flags=re.M)
    return md.strip()
```

## Notes

- Content must be HTML, not raw Markdown
- Special chars in title auto-handled by WordPress
- Article link format: `https://your-blog.com/archives/{ID}` (varies by permalink setting)
- For scheduled posts: `"status":"future","date":"2026-06-10T09:00:00"`
