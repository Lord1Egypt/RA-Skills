# Highlights

Highlights are text excerpts saved from web pages, associated with individual raindrops (bookmarks).

Docs: https://developer.raindrop.io/v1/highlights

## Highlight Object

| Field | Type | Description |
|-------|------|-------------|
| `_id` | string | Unique identifier |
| `text` | string | Highlighted text content (required) |
| `title` | string | Associated bookmark title |
| `color` | string | Highlight colour (default: `yellow`) |
| `note` | string | Optional annotation |
| `created` | string | ISO 8601 timestamp |
| `tags` | array | Tag labels |
| `link` | string | Source page URL |

**Colour options**: `blue`, `brown`, `cyan`, `gray`, `green`, `indigo`, `orange`, `pink`, `purple`, `red`, `teal`, `yellow`

## Retrieve All Highlights

Paginated list of all highlights across all raindrops.

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/highlights?page=0&perpage=50" | jq '.'
```

**Query parameters:**
- `page` (number) - Page number (0-indexed)
- `perpage` (number) - Results per page (max 50, default 25)

## Retrieve Collection Highlights

Highlights from a specific collection.

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/highlights/{collectionId}" | jq '.'
```

## Retrieve Raindrop Highlights

Get highlights for a specific bookmark (returned as part of the raindrop object).

```bash
curl -s -H "Authorization: Bearer $RAINDROP_TOKEN" \
  "https://api.raindrop.io/rest/v1/raindrop/{id}" | jq '.item.highlights'
```

## Add Highlight

Add a new highlight to a raindrop by updating it with the `highlights` array.

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "highlights": [
      {
        "text": "The highlighted text",
        "color": "yellow",
        "note": "My annotation"
      }
    ]
  }' \
  "https://api.raindrop.io/rest/v1/raindrop/{id}" | jq '.'
```

**Fields:**
- `text` (string, required) - The highlighted text
- `color` (string, optional) - Colour name (default: `yellow`)
- `note` (string, optional) - User annotation

## Update Highlight

Update an existing highlight's note or colour by including its `_id`.

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "highlights": [
      {
        "_id": "HIGHLIGHT_ID",
        "note": "Updated annotation",
        "color": "blue"
      }
    ]
  }' \
  "https://api.raindrop.io/rest/v1/raindrop/{id}" | jq '.'
```

## Delete Highlight

Remove a highlight by setting its `text` to an empty string.

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "highlights": [
      {
        "_id": "HIGHLIGHT_ID",
        "text": ""
      }
    ]
  }' \
  "https://api.raindrop.io/rest/v1/raindrop/{id}" | jq '.'
```

All highlight operations return the updated raindrop object with `"result": true`.
