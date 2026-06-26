# social-links-search

> Full OpenAPI spec: https://openwebninja.s3.us-east-1.amazonaws.com/portal/openapi/social_links_search.yaml

**Host:** `social-links-search.p.rapidapi.com`
**Notes:** Returns all social profile links in a single response. No pagination.

## Endpoints

### GET /search-social-links
Search Social Links

**Required:**
- `query` (string) — Social links search query. Example: `John Smith`

**Optional:**
- `social_networks` (string, default: facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github) Example: `facebook,tiktok,instagram,snapchat,twitter,youtube,linkedin,github,pinterest`

**Pagination:** none

---
