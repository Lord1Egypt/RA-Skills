# Webflow CMS

## Collection Architecture

**Plan before creating:**
- What content types exist?
- How do they relate? (blog → authors, products → categories)
- What fields are needed for filtering/sorting?

**Reference fields:**
- Single reference: Post → Author
- Multi-reference: Post → Tags (limited to 5 per item)

## Field Types

| Field | Use Case | Gotcha |
|-------|----------|--------|
| Plain text | Short strings | 256 char limit |
| Rich text | Blog content | Limited formatting options |
| Image | Featured images | No built-in lazy loading |
| Multi-image | Galleries | Can't reorder after upload |
| Reference | Relationships | 5 multi-reference limit |
| Option | Status/category | Can't add options dynamically |
| Switch | Boolean flags | Defaults to OFF |
| Color | Theme colors | No opacity control |

## CMS Limits

| Plan | CMS Items | Collections |
|------|-----------|-------------|
| CMS Hosting | 2,000 | 20 |
| Business | 10,000 | 40 |

**Workaround for large datasets:** Paginate API calls, use external database for overflow.

## Headless API

**Endpoint:** `https://api.webflow.com/v2/collections/{collection_id}/items`

**Authentication:** Bearer token from Site Settings → Integrations

**Rate limits:** 60 requests/minute (v2 API)

**TypeScript types from schema:**
```typescript
// Generate from collection fields
interface BlogPost {
  name: string;
  slug: string;
  "post-body": string;
  "featured-image": { url: string; alt: string };
  author: { _id: string }; // reference
  _draft: boolean;
  _archived: boolean;
}
```

## Pagination

```javascript
// Fetch all items with pagination
async function getAllItems(collectionId) {
  const items = [];
  let offset = 0;
  const limit = 100;
  
  while (true) {
    const res = await fetch(
      `${API}/collections/${collectionId}/items?offset=${offset}&limit=${limit}`,
      { headers: { Authorization: `Bearer ${TOKEN}` } }
    );
    const data = await res.json();
    items.push(...data.items);
    if (data.items.length < limit) break;
    offset += limit;
  }
  return items;
}
```

## Content Migration

**Import format:** CSV with exact column headers matching field names

**Image handling:** Use URLs in CSV, Webflow fetches them

**Common issues:**
- Rich text needs HTML formatting in CSV
- Reference fields need item IDs, not names
- Switch fields: "true"/"false" strings
