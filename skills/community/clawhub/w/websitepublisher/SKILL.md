---
name: websitepublisher
description: >
  Build and publish complete websites via WebsitePublisher.ai. Create pages,
  upload assets, manage dynamic data (products, team members, blog posts),
  configure contact forms, and publish to a live URL — all through conversation.
  No WordPress. No hosting setup. No CMS configuration.
homepage: https://www.websitepublisher.ai
license: MIT
metadata:
  clawdbot:
    emoji: "🌐"
    requires:
      env:
        - WEBSITEPUBLISHER_TOKEN
        - WEBSITEPUBLISHER_PROJECT
    primaryEnv: WEBSITEPUBLISHER_TOKEN
  openclaw:
    emoji: "🌐"
    requires:
      env:
        - WEBSITEPUBLISHER_TOKEN
        - WEBSITEPUBLISHER_PROJECT
---

# WebsitePublisher.ai

Build and publish real websites through conversation. You describe it — the AI builds and deploys it.

**The user's credentials are set as environment variables:**
- `WEBSITEPUBLISHER_TOKEN` — API token (starts with `wpa_`)
- `WEBSITEPUBLISHER_PROJECT` — Project ID (numeric, e.g. `12345`)

**If either variable is missing**, stop and instruct the user:
1. Sign up at https://www.websitepublisher.ai/dashboard
2. Copy their API token and Project ID from the dashboard
3. Add to their OpenClaw config:
   ```json
   {
     "env": {
       "WEBSITEPUBLISHER_TOKEN": "wpa_xxxx...",
       "WEBSITEPUBLISHER_PROJECT": "12345"
     }
   }
   ```

---

## Authentication

Every API call requires these headers:
```
Authorization: Bearer $WEBSITEPUBLISHER_TOKEN
Content-Type: application/json
Accept: application/json
```

**Base URL:** `https://api.websitepublisher.ai`

---

## Workflow — Build a Complete Website

When asked to build a website, follow this exact sequence:

### Step 1 — Check existing content
```bash
curl -s \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Accept: application/json" \
  "https://api.websitepublisher.ai/papi/project/$WEBSITEPUBLISHER_PROJECT/status"
```

This returns the project URL, existing pages, and current status. Always do this first.

### Step 2 — Create pages (use bulk for multiple pages)

**Single page:**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "slug": "index.html",
    "content": "<!DOCTYPE html><html lang=\"en\">...</html>",
    "title": "Homepage",
    "seotitle": "Company Name — Tagline",
    "seodescription": "One sentence describing the page for search engines."
  }' \
  "https://api.websitepublisher.ai/papi/project/$WEBSITEPUBLISHER_PROJECT/pages"
```

**Multiple pages at once (preferred — saves API calls):**
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "pages": [
      {"slug": "index.html", "content": "...", "title": "Home"},
      {"slug": "about.html", "content": "...", "title": "About"},
      {"slug": "contact.html", "content": "...", "title": "Contact"}
    ]
  }' \
  "https://api.websitepublisher.ai/papi/project/$WEBSITEPUBLISHER_PROJECT/pages/bulk"
```

### Step 3 — Upload assets (images, CSS, JS)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "slug": "images/logo.png",
    "content": "BASE64_ENCODED_DATA",
    "alt": "Company Logo"
  }' \
  "https://api.websitepublisher.ai/papi/project/$WEBSITEPUBLISHER_PROJECT/assets"
```

**Asset URL pattern:** `https://cdn.websitepublisher.ai/[path]/[slug]`  
Reference assets in HTML using this CDN URL.

### Step 4 — Confirm live URL

The project URL is returned by the status endpoint. Share it with the user.

---

## PAPI — Pages & Assets (Full Reference)

### Pages

| Action | Method | Endpoint |
|--------|--------|----------|
| List pages | GET | `/papi/project/{id}/pages` |
| Get page | GET | `/papi/project/{id}/pages/{slug}` |
| Create page | POST | `/papi/project/{id}/pages` |
| Bulk create | POST | `/papi/project/{id}/pages/bulk` |
| Update page | PUT | `/papi/project/{id}/pages/{slug}` |
| Patch page | PATCH | `/papi/project/{id}/pages/{slug}` |
| Delete page | DELETE | `/papi/project/{id}/pages/{slug}` |
| List versions | GET | `/papi/project/{id}/pages/{slug}/versions` |
| Rollback | POST | `/papi/project/{id}/pages/{slug}/rollback` |

**Page fields:**
```json
{
  "slug": "about.html",
  "content": "full HTML string",
  "title": "label shown in dashboard",
  "seotitle": "browser tab + search title",
  "seodescription": "meta description for search",
  "seokeywords": "comma,separated,keywords",
  "canonical": "https://example.com/about"
}
```

**Patch a page** (partial update — send only changed HTML fragment):
```bash
curl -s -X PATCH \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "patches": [
      {
        "search": "<h1>Old Title</h1>",
        "replace": "<h1>New Title</h1>"
      }
    ]
  }' \
  "https://api.websitepublisher.ai/papi/project/$WEBSITEPUBLISHER_PROJECT/pages/index.html"
```

### Assets

| Action | Method | Endpoint |
|--------|--------|----------|
| List assets | GET | `/papi/project/{id}/assets` |
| Get asset | GET | `/papi/project/{id}/assets/{slug}` |
| Upload asset | POST | `/papi/project/{id}/assets` |
| Bulk upload | POST | `/papi/project/{id}/assets/bulk` |
| Delete asset | DELETE | `/papi/project/{id}/assets/{slug}` |

**Asset fields:**
```json
{
  "slug": "images/hero.jpg",
  "content": "BASE64_STRING or https://example.com/image.jpg",
  "alt": "Description for accessibility",
  "type": "image"
}
```

> **Tip:** You can pass a public image URL as `content` — the platform fetches and stores it automatically.

---

## MAPI — Dynamic Data (Products, Blog, Team, etc.)

Use MAPI when the website needs structured, repeatable data — product listings, blog posts, team members, portfolio items, etc.

### Create an entity (data model)
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "products",
    "properties": [
      {"name": "name", "type": "string", "required": true},
      {"name": "price", "type": "number"},
      {"name": "description", "type": "text"},
      {"name": "image", "type": "image"}
    ]
  }' \
  "https://api.websitepublisher.ai/mapi/project/$WEBSITEPUBLISHER_PROJECT/entities"
```

### Create records
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Wireless Headphones",
    "price": 89.99,
    "description": "Premium noise-cancelling headphones",
    "image": "https://example.com/headphones.jpg"
  }' \
  "https://api.websitepublisher.ai/mapi/project/$WEBSITEPUBLISHER_PROJECT/products"
```

> **Note:** MAPI endpoint uses the **plural entity name** — e.g. `/products` not `/product`.

### MAPI Reference

| Action | Method | Endpoint |
|--------|--------|----------|
| List entities | GET | `/mapi/project/{id}/entities` |
| Create entity | POST | `/mapi/project/{id}/entities` |
| Get entity schema | GET | `/mapi/project/{id}/entities/{name}/properties` |
| List records | GET | `/mapi/project/{id}/{entity}` |
| Get record | GET | `/mapi/project/{id}/{entity}/{recordId}` |
| Create record | POST | `/mapi/project/{id}/{entity}` |
| Update record | PUT | `/mapi/project/{id}/{entity}/{recordId}` |
| Delete record | DELETE | `/mapi/project/{id}/{entity}/{recordId}` |

**Public read:** MAPI records are publicly readable at the same endpoint without a token — useful for frontend JavaScript fetching live data.

---

## SAPI — Contact Forms

Add a working contact form to any page in two steps.

### Step 1 — Configure the form
```bash
curl -s -X POST \
  -H "Authorization: Bearer $WEBSITEPUBLISHER_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "page_slug": "contact.html",
    "fields": [
      {"name": "name", "type": "text", "required": true, "label": "Your Name"},
      {"name": "email", "type": "email", "required": true, "label": "Email Address"},
      {"name": "message", "type": "textarea", "required": true, "label": "Message"}
    ],
    "submit_label": "Send Message",
    "success_message": "Thank you! We will get back to you shortly.",
    "notification_email": "hello@example.com"
  }' \
  "https://api.websitepublisher.ai/sapi/project/$WEBSITEPUBLISHER_PROJECT/forms"
```

> **Important:** Always send ALL fields on every configure_form call — no partial updates.

### Step 2 — Add the form HTML to the page

The API returns a `form_id`. Use this snippet in the page HTML:
```html
<form id="wp-contact-form" data-form-id="FORM_ID_HERE">
  <!-- fields rendered by JS -->
</form>
<script src="https://api.websitepublisher.ai/sapi/form.js"></script>
```

### SAPI Reference

| Action | Method | Endpoint |
|--------|--------|----------|
| Configure form | POST | `/sapi/project/{id}/forms` |
| List forms | GET | `/sapi/project/{id}/forms` |
| Remove form | DELETE | `/sapi/project/{id}/forms/{form_id}` |

---

## Rate Limits

| Plan | Limit |
|------|-------|
| Free | 30 requests/min |
| Starter | 60 requests/min |
| Pro+ | 150-300 requests/min |

**Always prefer bulk endpoints** (`/pages/bulk`, `/assets/bulk`) over individual calls to stay within rate limits. A bulk call counts as one request regardless of how many items it creates.

---

## Common Patterns

### Landing page (one page)
1. `GET /status` — check project
2. `POST /pages` — create `index.html` with full content
3. `POST /forms` — configure contact form if needed
4. Share project URL

### Multi-page website
1. `GET /status` — check project
2. `POST /pages/bulk` — create all pages in one call
3. `POST /assets/bulk` — upload all images in one call
4. `POST /forms` — configure contact form on contact page
5. Share project URL

### Website with dynamic data (e.g. product catalogue)
1. `GET /status` — check project
2. `POST /entities` — create data model (e.g. "products")
3. `POST /{entity}` — create records (one per product)
4. `POST /pages/bulk` — create pages with JS that fetches MAPI data
5. Share project URL

---

## Error Handling

All endpoints return standard HTTP status codes:

| Code | Meaning |
|------|---------|
| 200/201 | Success |
| 400 | Invalid request — check your JSON fields |
| 401 | Invalid or missing token |
| 404 | Page/asset/entity not found |
| 422 | Validation error — response body contains field errors |
| 429 | Rate limit exceeded — use bulk endpoints or wait |
| 500 | Server error — try again |

On error, the response body always contains a `message` field with a description.

---

## Support & Docs

- **Dashboard:** https://www.websitepublisher.ai/dashboard
- **Full API docs:** https://www.websitepublisher.ai/docs
- **PAPI docs:** https://www.websitepublisher.ai/docs/papi
- **MAPI docs:** https://www.websitepublisher.ai/docs/mapi
- **SAPI docs:** https://www.websitepublisher.ai/docs/sapi
