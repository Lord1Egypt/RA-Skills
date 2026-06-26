---
name: willhaben-search
description: Willhaben marketplace search API for finding listings, browsing categories, and getting listing details on Austria's largest classifieds platform.
homepage: https://api.nochda.at
metadata: {"clawdbot":{"emoji":"🔍"}}
---

# willhaben-search

Search and browse listings on willhaben.at — Austria's largest online marketplace — using AI-powered semantic search.

## API Basics

Base URL: `https://api.nochda.at`

No authentication required. All endpoints return JSON.

```bash
curl "https://api.nochda.at/api/health"
```

Rate limits: 50 req/min global, 10 req/min for search/suggest.

## Typical Workflow

1. **Find the right category** with `GET /api/categories/suggest?q=...`
2. **Search listings** with `GET /api/search?categoryId=...&query=...`
3. **Get listing details** with `GET /api/listings/:id`

## Endpoints

### Suggest Categories (Semantic)

`GET /api/categories/suggest?q=<query>`

Find the best category for a user's intent using AI. Start here when you don't know which category to search in.

```bash
curl "https://api.nochda.at/api/categories/suggest?q=mountain%20bike"
```

**Response:**
```json
{
  "suggestions": [
    {"id": 4552, "label": "Fahrräder", "parentLabel": "Sport/Sportgeräte", "score": 1.0},
    {"id": 2145, "label": "Mountainbikes", "parentLabel": "Fahrräder", "score": 0.82}
  ]
}
```

Use the `id` of the best-matching suggestion as `categoryId` in search. Returns up to 5 suggestions ranked by relevance (score 0–1).

---

### Search Listings

`GET /api/search?categoryId=<id>&query=<query>`

Semantic search within a category. Understands natural language queries.

```bash
curl "https://api.nochda.at/api/search?categoryId=4552&query=full%20suspension%20trail%20bike&maxPrice=2000&recentDays=30"
```

**Query Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `categoryId` | Yes | Category ID (from suggest or browse) |
| `query` | Yes | Natural language search (max 500 chars) |
| `maxPrice` | No | Maximum price in EUR |
| `recentDays` | No | Only show listings from the last N days |

**Response:**
```json
{
  "results": [
    {
      "id": 12345,
      "title": "Giant Trance X 29 2024",
      "description": "Full suspension trail bike, excellent condition...",
      "price": 1800,
      "location": "Wien",
      "url": "https://willhaben.at/iad/kaufen-und-verkaufen/d/...",
      "images": ["https://cache.willhaben.at/...jpg"],
      "publishedAt": "2026-03-08T10:30:00Z",
      "similarity": 0.87
    }
  ],
  "totalCandidates": 85
}
```

Results are ranked by semantic relevance. Each result includes a direct `url` link to the original willhaben listing. Returns up to 40 results.

---

### Get Listing Details

`GET /api/listings/:id`

Full details for a specific listing including comparable pricing context.

```bash
curl "https://api.nochda.at/api/listings/12345"
```

**Response:**
```json
{
  "listing": {
    "id": 12345,
    "title": "Giant Trance X 29 2024",
    "description": "Full suspension trail bike, excellent condition...",
    "price": 1800,
    "location": "Wien",
    "url": "https://willhaben.at/iad/kaufen-und-verkaufen/d/...",
    "images": ["https://cache.willhaben.at/...jpg"],
    "publishedAt": "2026-03-08T10:30:00Z",
    "categoryLabel": "Fahrräder"
  },
  "compAnalysis": {
    "avgPrice": 2100,
    "medianPrice": 1950,
    "compCount": 30
  }
}
```

`compAnalysis` compares the listing's price against the 30 most similar listings in the same category. It can be `null` if not enough data is available.

---

### Browse Categories

**Root categories:**
```bash
curl "https://api.nochda.at/api/categories"
```

**All categories (flat list):**
```bash
curl "https://api.nochda.at/api/categories/all"
```

**Children of a category:**
```bash
curl "https://api.nochda.at/api/categories/123/children"
```

Returns `{ "parent": {...}, "children": [...] }`.

**Search categories by name:**
```bash
curl "https://api.nochda.at/api/categories/search?q=auto"
```

Categories with duplicate names include a `disambiguatedLabel` (e.g. `"PKW (Auto/Motorrad)"`).

All category objects have: `id`, `label`, `parentCategoryId`, `image`.

## Error Handling

Errors return JSON: `{"error": "Description"}`.

| Status | Meaning |
|--------|---------|
| 400 | Invalid or missing parameters |
| 404 | Resource not found |
| 429 | Rate limited — retry after `Retry-After` header value |
| 500 | Server error |

## Notes

- All prices are in EUR
- Search is AI-powered — natural language queries like "cozy armchair for reading" work well
- Categories form a hierarchy (root → children); search includes all descendant categories
- Always link users to the `url` field so they can view the full listing on willhaben