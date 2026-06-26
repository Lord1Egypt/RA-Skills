# WordPress REST API Quick Reference

Base URL: `{site_url}/wp-json/wp/v2/`

## Auth

```
Authorization: Basic base64("{username}:{app_password}")
```

Application Password format: `xxxx xxxx xxxx xxxx xxxx xxxx`
Test: `GET /wp-json/wp/v2/users/me`

---

## Posts

| Action | Method | Endpoint |
|--------|--------|----------|
| List posts | GET | `/posts?per_page=10&page=1` |
| Get by ID | GET | `/posts/{id}` |
| Find by slug | GET | `/posts?slug={slug}&status=any` |
| Create | POST | `/posts` |
| Update | POST | `/posts/{id}` |
| Delete (trash) | DELETE | `/posts/{id}` |

### Post Fields

| Field | Type | Notes |
|-------|------|-------|
| `title` | string | Plain string works |
| `content` | string | HTML string |
| `slug` | string | URL-safe, auto-generated from title if empty |
| `status` | string | `publish`, `draft`, `future`, `private`, `pending` |
| `date_gmt` | ISO 8601 | UTC time: `2025-06-15T09:00:00` |
| `categories` | int[] | Array of category IDs |
| `tags` | int[] | Array of tag IDs |
| `featured_media` | int | Media attachment ID |
| `meta` | object | Custom fields (requires REST API enabled for meta) |

---

## Media

| Action | Method | Endpoint |
|--------|--------|----------|
| Upload | POST | `/media` |
| Get | GET | `/media/{id}` |
| Update alt/caption | POST | `/media/{id}` |

### Upload Headers
```
Content-Type: image/jpeg
Content-Disposition: attachment; filename="image.jpg"
```

Returns: `{id, source_url, alt_text, ...}`

---

## Categories & Tags

| Action | Method | Endpoint |
|--------|--------|----------|
| List categories | GET | `/categories?per_page=100` |
| Search categories | GET | `/categories?search=keyword` |
| Create category | POST | `/categories` |
| List tags | GET | `/tags?per_page=100` |
| Search tags | GET | `/tags?search=keyword` |

---

## HTTP Status Codes

| Code | Meaning | Common Cause |
|------|---------|---------------|
| 200 | Success (GET/UPDATE) | — |
| 201 | Created (POST) | — |
| 400 | Bad Request | Invalid field value, bad JSON |
| 401 | Unauthorized | Wrong username/password |
| 403 | Forbidden | User lacks capability |
| 404 | Not Found | Wrong post ID or slug |
| 500 | Server Error | WP internal error |

---

## Pagination

- `per_page`: 1–100 (default 10)
- `page`: page number
- Response headers: `X-WP-Total`, `X-WP-TotalPages`

---

## Plugin Endpoints

ACF (Advanced Custom Fields):
```
GET /posts/{id}?_fields=id,title,acf
POST /posts/{id} {"acf": {"field_name": "value"}}
```

Yoast SEO:
```
POST /posts/{id} {"yoast_head_json": {"title": "SEO Title", "description": "Meta"}}
```
