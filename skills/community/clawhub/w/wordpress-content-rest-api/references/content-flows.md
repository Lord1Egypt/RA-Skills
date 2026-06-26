# Safe Read/Write Flows (Posts, Pages, Media)

## A) Read Flow

Use filters to reduce payload and improve reliability.

Examples:
```bash
# Find posts by search + status
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_SITE/wp-json/wp/v2/posts?search=pricing&status=draft,publish&per_page=20&page=1"

# Fetch exact page
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_SITE/wp-json/wp/v2/pages/123"
```

## B) Create Flow (Draft First)

```bash
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "$WP_SITE/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"New Article",
    "content":"<p>Draft body</p>",
    "status":"draft"
  }'
```

## C) Update Flow (Minimal Patch)

1. Read current object.
2. Change only required fields.
3. Send update.

```bash
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "$WP_SITE/wp-json/wp/v2/pages/123" \
  -H "Content-Type: application/json" \
  -d '{
    "title":"Updated title",
    "status":"draft"
  }'
```

## D) Publish Pattern

Use only after explicit approval:

```bash
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "$WP_SITE/wp-json/wp/v2/posts/456" \
  -H "Content-Type: application/json" \
  -d '{"status":"publish"}'
```

## E) Media Upload Pattern

```bash
curl -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  -X POST "$WP_SITE/wp-json/wp/v2/media" \
  -H "Content-Disposition: attachment; filename=hero.jpg" \
  -H "Content-Type: image/jpeg" \
  --data-binary @hero.jpg
```

Then assign media ID as `featured_media` in post/page update.

## F) Delete Pattern

Avoid by default. Require explicit approval.
If needed, prefer moving content out of public state first (`draft`/`private`) before permanent delete operations.
