---
name: WordPress Blog Publisher
description: Use this skill whenever the user wants to publish, update, or batch-upload blog content to a WordPress site via the REST API. Handles auth, markdown conversion, image uploads, scheduling, and writing permalink back to upstream systems.
---

# WordPress Blog Publisher

This skill turns an AI agent into a reliable publisher for WordPress sites via the REST API (`/wp-json/wp/v2/*`). Designed for batch SEO content workflows, it handles authentication, markdown-to-HTML conversion, media uploads, post scheduling, and status writeback to upstream systems like Airtable, Bitable, or Google Sheets.

## Quick Reference

| Decision | Strong Choice | Acceptable | Weak / Avoid |
|----------|---------------|------------||--------------|
| Auth method | Application Password (HTTP Basic) | JWT token | Login password (never) |
| Content format | Markdown → HTML (convert first) | Raw HTML | Raw markdown (WP won't render it) |
| Batch approach | Dry-run first post, confirm, then batch | Process all with logs | Process all without validation |
| Image handling | Upload to WP media library, rewrite src | External CDN links | Local file paths |
| Post status | `publish` or `future` (scheduled) | `draft` for review | `private` (unless intentional) |
| Error handling | Log and continue on non-critical errors | Stop on all errors | Silent fail |
| Permalink writeback | Write to upstream system after publish | Log to file | No writeback |

## Problems This Skill Solves

1. **Manual copy-paste publishing bottleneck** — writing and publishing blog posts one-by-one when a batch of 20–200 SEO articles needs to go live.
2. **Markdown format mismatch** — AI-generated content is usually markdown, but WP's classic editor expects HTML and the block editor has its own format requirements.
3. **Image scatter** — inline images in markdown that point to external URLs or local paths need to be uploaded to the WP media library and src-rewritten.
4. **No upstream status tracking** — after publishing, many workflows lose track of which posts are live vs. draft vs. scheduled.
5. **Auth confusion** — using login passwords (wrong) vs. Application Passwords (correct) is the #1 cause of 401 errors.
6. **Category/tag ID mismatch** — WP uses numeric IDs for categories and tags, not names; this skill handles the lookup.
7. **Scheduling complexity** — batch content often needs to be spread across a publication calendar rather than published all at once.

## Workflow

### Step 1 — Authenticate

**Required credentials**:
- `site_url`: e.g., `https://example.com` (no trailing slash)
- `username`: WP admin username
- `app_password`: Application Password from WP Admin → Users → Profile → Application Passwords

**Auth header**:
```
Authorization: Basic base64(username:app_password)
```

**Test connection**:
```
GET {site_url}/wp-json/wp/v2/users/me
```
If 200, auth is working. If 401, check Application Password setup. If 403, user lacks `publish_posts` capability.

### Step 2 — Prepare Content

- Strip YAML front-matter; use `title`, `slug`, `categories`, `tags` fields from it
- Convert markdown to HTML using a proper converter (not regex substitution)
- Preserve: code fences (`<pre><code>`), tables, nested lists
- Remove: `# H1` title (use as post title, not body content)

### Step 3 — Resolve Category and Tag IDs

WP requires numeric IDs, not names:
```
GET {site_url}/wp-json/wp/v2/categories?search=seo&per_page=5
```
Cache the ID map for the batch to avoid repeated lookups.

### Step 4 — Upload Media (Featured Image)

```
POST {site_url}/wp-json/wp/v2/media
Headers:
  Content-Disposition: attachment; filename="image.jpg"
  Content-Type: image/jpeg
Body: [binary image data]
```

### Step 5 — Create or Update Post

```json
POST {site_url}/wp-json/wp/v2/posts
{
  "title": "Your Post Title",
  "content": "<p>HTML content here</p>",
  "slug": "your-post-slug",
  "status": "publish",
  "categories": [12, 34],
  "tags": [56, 78],
  "featured_media": 1234,
  "date_gmt": "2025-06-15T09:00:00"
}
```

Response includes `"link"` — the live permalink. Save this.

### Step 6 — Write Status Back to Upstream System

After each successful publish, write permalink and timestamp back:
- **Airtable**: PATCH record with `permalink` and `wp_status` fields
- **Google Sheets**: Update row via Sheets API
- **Bitable**: Update record via Lark Open API
- **Local log**: Append `{slug, wp_post_id, permalink, published_at}` to CSV/JSON

### Step 7 — Batch Mode Protocol

1. Process first post fully, show draft URL
2. Wait for confirmation
3. Process remaining with 1–2 second delay between requests
4. Show running status: `[3/20] Published: /seo-guide-2025 ✓`
5. On failure: log error, continue with next post
6. Final summary: `20 published, 1 failed (see log)`

## Worked Examples

### Example 1 — Batch Publish 10 SEO Articles from Airtable

1. Fetch rows where `Status = "Ready to Publish"` from Airtable
2. For each row: convert markdown → HTML, upload featured image, resolve category ID
3. Create WP post with `status: "future"` and `date_gmt` staggered by 1 day each
4. Write permalink + WP post ID back to Airtable

### Example 2 — Update Existing Posts with New Content

1. For each slug: `GET /wp-json/wp/v2/posts?slug={slug}&status=any` to find post ID
2. Convert updated markdown to HTML
3. `POST /wp-json/wp/v2/posts/{id}` with updated content

## Common Mistakes

1. **Using login password** — results in 401; use Application Password.
2. **Posting raw markdown** — always convert to HTML first.
3. **Wrong category IDs** — always look up IDs via the API.
4. **Images > 2MB** — resize before uploading.
5. **Using `date` instead of `date_gmt`** — always use UTC.
6. **No dry-run on batches** — validate one post before running 50.
7. **Not writing permalink back** — without writeback, you lose track of published posts.
8. **Silent failures in batch** — always log errors explicitly.

## Resources

- `references/api-reference.md` — WP REST API endpoints quick reference
- `references/markdown-to-html-rules.md` — Conversion rules and edge cases
- `assets/wp-publish-checklist.md` — Pre-publish and post-publish quality checklist
