---
name: wordpress-ultimate
version: 1.0.0
description: "Three env vars. One script. Your agent manages your entire WordPress site — draft-only safety included."
metadata:
  openclaw:
    emoji: "📝"
    notes:
      security: "Authenticates via WP Application Passwords over HTTPS. Credentials read from .env at runtime, never hardcoded. All new content defaults to draft status. DELETE operations are blocked — trash via status change only."
    requires:
      bins: ["curl", "jq", "bash"]
      env: ["WP_URL", "WP_USER", "WP_APP_PASSWORD"]
repository: https://github.com/globalcaos/tinkerclaw
homepage: https://github.com/globalcaos/tinkerclaw
---

# WordPress Ultimate

Manage WordPress sites through the REST API with draft-only safety.

## Setup

Requires three environment variables (stored in `.env`, never committed):
```
WP_URL=https://example.com
WP_USER=user@example.com
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

## Core Script

All operations go through `scripts/wp.sh`. It wraps curl with auth and JSON handling.

```bash
# Usage: scripts/wp.sh <method> <endpoint> [json_body]
# Examples:
scripts/wp.sh GET "posts?per_page=5&status=draft,publish"
scripts/wp.sh POST "posts" '{"title":"My Post","content":"<p>Hello</p>","status":"draft"}'
scripts/wp.sh PUT "posts/42" '{"title":"Updated Title"}'
```

## Safety Rules

1. **DRAFT-ONLY by default** — `scripts/wp.sh POST posts` forces `status: draft` unless the JSON body explicitly contains `"status":"publish"` AND the caller confirms intent.
2. **Never delete** — use `scripts/wp.sh PUT posts/ID '{"status":"trash"}'` instead of DELETE.
3. **Credentials** — read from `.env` at runtime, never hardcoded in commands.

## Common Workflows

### Create a Blog Post (Draft)
```bash
scripts/wp.sh POST posts '{
  "title": "My Article Title",
  "content": "<p>Article body in HTML.</p>",
  "status": "draft",
  "categories": [3],
  "tags": [5, 8]
}'
```

### Create a Page (Draft)
```bash
scripts/wp.sh POST pages '{
  "title": "About",
  "content": "<p>About page content.</p>",
  "status": "draft"
}'
```

### List Posts
```bash
scripts/wp.sh GET "posts?per_page=20&status=draft,publish&orderby=date&order=desc"
```

### Create a Category
```bash
scripts/wp.sh POST categories '{"name": "AI & Agents", "slug": "ai-agents", "description": "Posts about AI agent development"}'
```

### Create a Tag
```bash
scripts/wp.sh POST tags '{"name": "OpenClaw", "slug": "openclaw"}'
```

### Upload Media
Use `scripts/wp-upload.sh` for media uploads:
```bash
scripts/wp-upload.sh /path/to/image.png "Alt text description"
```
Returns the media ID for use in posts (featured_media field).

### Install a Plugin
```bash
scripts/wp.sh POST plugins '{"slug": "plugin-slug", "status": "active"}'
```

### List Plugins
```bash
scripts/wp.sh GET plugins
```

### Update Yoast SEO Metadata
When Yoast is installed, posts accept `yoast_head_json` fields. Set SEO via post meta:
```bash
scripts/wp.sh PUT "posts/42" '{
  "meta": {
    "_yoast_wpseo_title": "SEO Title Here",
    "_yoast_wpseo_metadesc": "Meta description for search engines."
  }
}'
```

### Manage Categories and Tags
```bash
# List categories
scripts/wp.sh GET categories
# List tags  
scripts/wp.sh GET tags
# Assign post to categories (by ID)
scripts/wp.sh PUT "posts/42" '{"categories": [3, 7]}'
```

## Content Formatting

WordPress REST API accepts HTML in `content` field. For rich posts:
- Use `<h2>`, `<h3>` for headings (not H1 — the title IS H1)
- Use `<p>` for paragraphs
- Use `<!-- wp:heading -->` blocks for Gutenberg compatibility
- Images: upload first via `wp-upload.sh`, then reference with `<img>` or `<!-- wp:image -->`

## Gutenberg Block Format

For full Gutenberg compatibility, wrap content in block comments:
```html
<!-- wp:paragraph -->
<p>Text here.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":2} -->
<h2>Section Title</h2>
<!-- /wp:heading -->

<!-- wp:image {"id":123} -->
<figure class="wp-block-image"><img src="URL" alt="desc"/></figure>
<!-- /wp:image -->
```

## Error Handling

- **401**: Check WP_USER and WP_APP_PASSWORD
- **403**: Application password may lack required capabilities
- **404**: Check WP_URL and endpoint path
- **rest_cannot_create**: May need to enable REST API or check user role

## Reference

For full WP REST API endpoint details, see `references/wp-api-reference.md`.
For SEO optimization patterns, see `references/seo-patterns.md`.

## Pairs Well With

- [coding-agent](https://clawhub.com/globalcaos/coding-agent) — generate content with sub-agents, publish it with wordpress-ultimate
- [outlook-hack](https://clawhub.com/globalcaos/outlook-hack) — same browser-relay philosophy applied to Microsoft; this one covers your blog

👉 **https://github.com/globalcaos/tinkerclaw**

_Clone it. Fork it. Break it. Make it yours._

---

## Credits

Created by **Oscar Serra** with the help of **Claude** (Anthropic).

*Built after the third time of hand-copying blog posts from a terminal. Never again.*
