# website-contacts-scraper

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/website_contacts_scraper.yaml

**Host:** `website-contacts-scraper.p.rapidapi.com`
**Notes:** No pagination. Accepts up to 20 domains per call via 'query' param (comma-separated).

## Endpoints

### GET /scrape-contacts
Scrape Contacts from Website

**Required:**
- `query` (string) Example: `wsgr.com`

**Optional:**
- `match_email_domain` (boolean, default: false) Example: `false`
- `external_matching` (boolean, default: false) Example: `false`

**Pagination:** none
**Response path:** `data`
**Key fields:** domain

---

### POST /website-url-by-keyword
Get Website by Keyword

**Pagination:** none

---
