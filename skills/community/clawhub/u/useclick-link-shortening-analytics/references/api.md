# UseClick API Reference (Backend-Aligned)

Base URL: `https://useclick.io/api/v1`

Auth header:

```http
Authorization: Bearer uc_live_YOUR_API_KEY
```

Rate-limit headers returned by API routes:

- `X-RateLimit-Limit`
- `X-RateLimit-Remaining`
- `X-RateLimit-Reset` (unix seconds)

## Verify API Key

`GET /auth/verify`

Success response:

```json
{
  "data": {
    "authenticated": true,
    "user_id": "...",
    "organization_id": null
  }
}
```

## Links

### Create Link

`POST /links`

Minimal request body:

```json
{
  "target_url": "https://example.com",
  "slug": "optional-custom-slug"
}
```

Optional fields include:

- `title`, `description`
- `branded_domain_id` or `branded_domain`
- `group_id`
- `campaign` or `data_source`
- `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content`
- `geo_targets`
- `password`, `expires_at`, `max_clicks`, `mature_content_warning`

Success response shape:

```json
{
  "data": {
    "id": "...",
    "slug": "my-link",
    "target_url": "https://example.com",
    "short_url": "https://useclick.io/my-link"
  }
}
```

Common errors:

- `403 LINK_LIMIT_REACHED`
- `400 SLUG_ALREADY_EXISTS`
- `400 RESERVED_SLUG`
- `403 FEATURE_NOT_AVAILABLE`

### List Links

`GET /links?page=1&limit=50&sort=created_at&order=desc&campaign=...&created_after=...`

Query behavior:

- `page` default `1`
- `limit` default `50`, max `100`
- `sort` and `order` are passed through
- `campaign` filters by stored campaign/data_source
- `created_after` filters by timestamp

Success response:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 0,
    "pages": 0
  }
}
```

### Get Link

`GET /links/:slug`

Returns:

```json
{
  "data": {
    "id": "...",
    "slug": "my-link"
  }
}
```

### Update Link

`PUT /links/:slug`

Only provided fields are updated. Feature-gated fields return `403 FEATURE_NOT_AVAILABLE` on unsupported plans.

### Delete Link

`DELETE /links/:slug`

Deletes link and associated analytics data.

## Click Analytics

`GET /clicks?page=1&limit=50&sort=created_at&order=desc&created_after=...&link_slug=...`

Behavior:

- `link_slug` must belong to the authenticated account/org.
- Returns paginated click rows with joined link metadata.

Success response:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "limit": 50,
    "total": 0,
    "pages": 0
  }
}
```

## Domains

`GET /domains`

Returns the default `useclick.io` domain plus active custom domains.

Response shape:

```json
{
  "domains": [
    {
      "id": "default",
      "domain": "useclick.io",
      "is_default": true
    }
  ],
  "total": 1
}
```

## Geo-Targeting

### List Geo Targets

`GET /links/:slug/geo-targets`

### Create Geo Target

`POST /links/:slug/geo-targets`

Body:

```json
{
  "country_code": "US",
  "target_url": "https://example.com/us"
}
```

Rules:

- `country_code` must be ISO alpha-2 uppercase format.
- Duplicate country rule returns `GEO_TARGET_EXISTS`.

### Delete Geo Target

`DELETE /links/:slug/geo-targets?country_code=US`
