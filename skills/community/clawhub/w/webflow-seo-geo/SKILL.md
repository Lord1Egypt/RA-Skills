---
name: webflow-seo-geo
description: End-to-end workflow for SEO/GEO content updates in Webflow: prioritize via GSC, draft/refresh content, create patch JSONs, update Webflow CMS via API, set images/alt/SEO, publish, and handle technical SEO fixes (canonical domain, redirects). Use for blog/service SEO refreshes and GEO/location page optimization.
---

# Webflow SEO/GEO

## Quick start (default workflow)
1) **Prioritize**: Use GSC exports + site plan docs.
2) **Draft**: Create/refresh copy (human tone, clear intent, strong CTA). Avoid AI-isms.
3) **Patch JSON**: Write Webflow item payloads in a local `/out/` folder.
4) **Publish via API**: POST new items or PATCH existing items, then publish.
5) **Images/alt/SEO**: Set `image-de-couverture`, `image---alt-text`, meta description/title.
6) **Tech checks**: Canonical domain, redirects, sitemap status, GSC property.

## Where to look first
- **Priority plan**: your SEO plan doc
- **Daily log**: your daily SEO log
- **Existing items**: export from Webflow (`/webflow_items/`)
- **Patches**: local `/out/` folder

## Webflow API (v2) — usage pattern
Use `WEBFLOW_API_TOKEN` env var.
- **Create item**: `POST /v2/collections/{collection_id}/items`
- **Update item**: `PATCH /v2/collections/{collection_id}/items/{item_id}`
- **Publish**: `POST /v2/collections/{collection_id}/items/publish` with `itemIds`
- **List items**: `GET /v2/collections/{collection_id}/items` (paginate)

**Collection IDs**
- Replace with your collection IDs (from Webflow API)

**Important fields**
- `name`, `slug`, `contenu-de-l-article`, `seo---meta-description`
- `image-de-couverture` (object: fileId/url/alt)
- `image---alt-text`
- `date-de-redaction`, `categorie`

## Content guidelines
- **Direct, concrete, actionable**
- **One message per section**
- **Use internal links** to services and relevant blog posts
- **CTA** at top or near end
- **FAQ** with 3–5 short Q/A (adds CTR)

## GEO / Local pages
- Use clear city intent in title/meta
- Add 2–3 local cues (address/city names) + local proof
- Link to relevant service page

## Technical SEO quick wins
### Canonical domain (www vs non‑www)
- **Primary domain set in Webflow UI** (not API)
- Ensure non‑www is default → Webflow handles 301 + canonical

### Sitemap
- Must resolve on canonical domain: `https://yourdomain.tld/sitemap.xml`
- Check `robots.txt` contains the sitemap URL

## When to read references
- **Webflow API details** → `references/webflow_api.md`
- **Copy/SEO patterns** → `references/seo_copy_patterns.md`
- **Patch templates** → `references/patch_templates.md`
