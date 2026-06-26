# Taxonomy, Pagination, and Search

## Taxonomy Handling

Common taxonomy endpoints:
- `/wp-json/wp/v2/categories`
- `/wp-json/wp/v2/tags`

Assign taxonomy IDs on posts/pages:

```json
{
  "categories": [12, 19],
  "tags": [33, 47]
}
```

Rules:
- Resolve slug -> ID before write.
- Create missing taxonomy term only when explicitly requested.
- Avoid duplicate term creation caused by case/slug mismatch.

## Pagination

Use `page` + `per_page` and inspect headers:
- `X-WP-Total`
- `X-WP-TotalPages`

Pattern:
```bash
curl -i -sS -u "$WP_USER:$WP_APP_PASSWORD" \
  "$WP_SITE/wp-json/wp/v2/posts?per_page=50&page=1"
```

Stop paging when page > `X-WP-TotalPages`.

## Search and Filtering

Useful params:
- `search`
- `slug`
- `status`
- `categories`
- `tags`
- `orderby`
- `order`

For conflict-safe updates:
1. Search by slug/title.
2. If one clear match -> update.
3. If multiple matches -> pause and ask for disambiguation.
