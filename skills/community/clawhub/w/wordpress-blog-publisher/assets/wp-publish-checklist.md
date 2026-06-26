# WordPress Publishing Quality Checklist

---

## Pre-Publish Setup

### Auth & Connection
- [ ] Site URL confirmed (no trailing slash)
- [ ] Application Password generated (not login password) and tested with GET /wp-json/wp/v2/users/me
- [ ] User has `publish_posts` capability confirmed
- [ ] User has `upload_files` capability confirmed (for media)

### Content Preparation
- [ ] YAML front-matter extracted (title, slug, categories, tags, featured image)
- [ ] Markdown converted to clean HTML
- [ ] H1 title removed from body
- [ ] All images uploaded to WP media library
- [ ] All inline image src attributes updated to WP source_url
- [ ] Code blocks formatted correctly (pre/code tags)
- [ ] Tables formatted as HTML tables
- [ ] No raw markdown syntax in final HTML

### Metadata
- [ ] Category IDs resolved (not names)
- [ ] Tag IDs resolved (not names)
- [ ] Featured media ID obtained
- [ ] Slug is URL-safe (lowercase, hyphens, max 60 chars)
- [ ] Publication date set (date_gmt in UTC)

---

## Dry-Run Validation (First Post in Batch)

- [ ] Post created as `draft` or `future` (not published yet)
- [ ] Draft URL reviewed in browser
- [ ] Title renders correctly
- [ ] Featured image displays
- [ ] All inline images display
- [ ] Formatting looks correct (headings, lists, code blocks, tables)
- [ ] Slug is correct
- [ ] Categories and tags are correct
- [ ] No HTML artifacts visible

---

## Batch Publishing

- [ ] Confirmed dry-run looks correct before proceeding
- [ ] Delay between requests set (1–2 seconds to avoid rate limiting)
- [ ] Error logging enabled (failed posts logged with reason)
- [ ] Progress tracking visible (e.g., [X/N] published)

---

## Post-Publish

- [ ] Each published post's permalink captured
- [ ] Permalink written back to upstream system (Airtable/Sheets/Bitable/log file)
- [ ] Post status in upstream system updated to "Published"
- [ ] Final summary reviewed: N published, N failed

---

## Common Error Resolutions

| Error | Likely Cause | Fix |
|-------|-------------|-----|
| 401 Unauthorized | Wrong auth type | Use Application Password, not login password |
| 403 Forbidden | Insufficient capability | Add `publish_posts` to user role |
| 400 Bad Request on date | Wrong date format | Use ISO 8601: `2025-06-15T09:00:00` |
| 400 Bad Request on categories | Category ID doesn't exist | Look up ID via /categories API |
| Post shows raw markdown | Content not converted | Convert markdown to HTML before posting |
| Images broken | External URLs not uploaded | Upload all images to WP media library |
| Slug conflict | Slug already in use | Append `-2` or modify slug |
| 500 Server Error | WP internal issue | Check WP debug log at wp-content/debug.log |
