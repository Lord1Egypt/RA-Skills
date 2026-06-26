# Webflow API v2 — quick reference (JSS)

Base: https://api.webflow.com/v2
Auth: Bearer $WEBFLOW_API_TOKEN
Headers: Content-Type: application/json; Accept-Version: 2.0.0

## Collections
- Replace with your collection IDs (from Webflow API)

## Endpoints
- List items: GET /collections/{collection_id}/items
- Create item: POST /collections/{collection_id}/items
- Update item: PATCH /collections/{collection_id}/items/{item_id}
- Publish: POST /collections/{collection_id}/items/publish {"itemIds": [..]}

## Core fields (blog)
- name
- slug
- contenu-de-l-article (HTML)
- seo---meta-description
- seo---meta-title (optional)
- image-de-couverture { fileId, url, alt }
- image---alt-text
- date-de-redaction (ISO)
- categorie (id)

## Publish sequence
1) Create or PATCH item
2) Publish with itemIds

## Gotchas
- Primary domain (www/non-www) set in Webflow UI only.
- Ensure JSON is valid (escape quotes) before POST/PATCH.
