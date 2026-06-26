# VVVLink API Reference

Base URL: `https://publish.vvvlink.com`

## Authentication

All `/sites/*` endpoints require: `Authorization: Bearer <apiKey>`

Subdomain check endpoints are public (no auth).

---

## POST /auth/create_new_user

Create an owner and get an API key.

**Auth:** None

**Request:**
```json
{"uuid": "your-unique-id"}
```

**Response (200):**
```json
{"apiKey": "nAnOiD32ChArAcTeRs..."}
```

**Errors:** 400 if uuid missing or < 4 chars

---

## POST /sites

Create a new site. Optionally pass a desired subdomain.

**Auth:** Bearer token

**Request (optional):**
```json
{"subdomain": "my-cool-site"}
```

If subdomain is available — it will be used.
If taken, invalid, or not provided — a random name is assigned.

**Response (200):**
```json
{
  "siteId": "abc123def456",
  "subdomain": "my-cool-site"
}
```

**Errors:** 401 unauthorized, 429 site limit reached

---

## PUT /sites/:siteId/files/:path

Upload a single file. Binary body.

**Auth:** Bearer token

**Request:** Raw binary file content

**Response (200):**
```json
{"path": "index.html", "size": 1234}
```

**Errors:** 400 disallowed file type, 404 site not found, 409 site not in uploading state, 413 size limit exceeded

**Allowed extensions:** .html, .css, .js, .json, .svg, .png, .jpg, .jpeg, .gif, .webp, .avif, .ico,
.woff, .woff2, .ttf, .eot, .txt, .xml, .webmanifest, .map

---

## POST /sites/:siteId/publish

Finalize upload and make site live.

**Auth:** Bearer token

**Response (200):**
```json
{
  "url": "https://happy-fox-42.vvvlink.com",
  "version": 1
}
```

**Errors:** 400 no files uploaded, 404 site not found, 409 already published, 413 size exceeded

---

## GET /sites

List all sites owned by the authenticated user.

**Auth:** Bearer token

**Response (200):**
```json
{
  "sites": [
    {
      "siteId": "abc123",
      "subdomain": "happy-fox-42",
      "currentVersion": 1,
      "status": "live",
      "created_at": "2026-01-01T00:00:00Z",
      "totalSize": 5432
    }
  ]
}
```

---

## GET /sites/:siteId

Get details of a single site.

**Auth:** Bearer token

**Response (200):** Same shape as individual item in list

---

## GET /sites/:siteId/versions

List all versions of a site.

**Auth:** Bearer token

**Response (200):**
```json
{
  "currentVersion": 2,
  "versions": [
    {"version": 1, "files": ["index.html"], "size": 100, "created_at": "...", "published_at": "..."},
    {"version": 2, "files": ["index.html", "style.css"], "size": 500, "created_at": "...", "published_at": "..."}
  ]
}
```

---

## PUT /sites/:siteId/subdomain

Rename a site's subdomain.

**Auth:** Bearer token

**Request:**
```json
{"name": "new-subdomain"}
```

**Response (200):**
```json
{
  "subdomain": "new-subdomain",
  "url": "https://new-subdomain.vvvlink.com"
}
```

**Errors:** 400 invalid format or reserved, 404 not found, 409 taken

---

## POST /sites/:siteId/rollback

Roll back to a previous version.

**Auth:** Bearer token

**Request:**
```json
{"version": 1}
```

**Response (200):**
```json
{
  "currentVersion": 1,
  "url": "https://my-site.vvvlink.com"
}
```

---

## POST /sites/:siteId/new-version

Start uploading a new version of an existing site.

**Auth:** Bearer token

**Response (200):**
```json
{"version": 2}
```

**Errors:** 409 upload already in progress

---

## DELETE /sites/:siteId

Delete a site and all its versions.

**Auth:** Bearer token

**Response (200):**
```json
{"deleted": true}
```

---

## GET /subdomains/check/:name

Check if a subdomain is available. No auth required.

**Response (200):**
```json
{"name": "my-site", "available": true}
```
or
```json
{"name": "admin", "available": false, "reason": "reserved"}
```
or
```json
{"name": "taken-name", "available": false, "reason": "taken"}
```

---

## POST /subdomains/check-bulk

Check multiple subdomain names at once. No auth required.

**Request:**
```json
{"names": ["name1", "name2", "name3"]}
```

Max 20 names per request.

**Response (200):**
```json
{
  "results": [
    {"name": "name1", "available": true},
    {"name": "name2", "available": false, "reason": "taken"},
    {"name": "name3", "available": false, "reason": "reserved"}
  ]
}
```

---

## POST /billing/upgrade

Get a Stripe checkout URL to upgrade to Pro plan.

**Auth:** Bearer token

**Request:**
```json
{"success_url": "https://vvvlink.com"}
```

**Response (200):**
```json
{"payment_url": "https://checkout.stripe.com/..."}
```

**Errors:** 400 already on Pro, 503 billing service unavailable

---

## Limits

| Type | Sites | Size/site |
|------|-------|-----------|
| Free | 10 | 10MB |
| Pro | 100 | 10MB |

## Subdomain Rules

- Format: lowercase letters, numbers, hyphens
- Length: 2-63 characters
- Must start and end with letter or number
- Reserved names cannot be used (www, api, admin, etc.)
