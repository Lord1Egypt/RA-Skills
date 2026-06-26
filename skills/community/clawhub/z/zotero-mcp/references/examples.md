# Zotero MCP Examples

## Common Use Cases

### 1. Find Papers on a Topic
```bash
SEARCH_QUERY="gravitational waves"
curl -s "http://127.0.0.1:23119/api/users/7120115/items?q=$SEARCH_QUERY&limit=10" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data:
    d = item.get('data', {})
    if d.get('itemType') == 'attachment': continue
    print(f\"- {d.get('title', 'Untitled')[:60]}... ({d.get('date', '')[:4]})\"
"
```

### 2. List All Collections
```bash
curl -s http://127.0.0.1:23119/api/users/7120115/collections | python3 -c "
import sys, json
data = json.load(sys.stdin)
for c in data:
    print(f\"{c['data']['name']}: {c['key']}\"
"
```

### 3. Get Items from a Collection
```bash
COLLECTION_KEY="U4PZ3XNP"  # Pending collection
curl -s "http://127.0.0.1:23119/api/users/7120115/collections/$COLLECTION_KEY/items" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'Found {len(data)} items'
"
```

### 4. Get PDF Text
```bash
ITEM_KEY="VEFDJC2X"
curl -s "http://127.0.0.1:23119/api/items/$ITEM_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
d = data.get('data', {})
print(f\"Title: {d.get('title')}
Authors: {[c.get('lastName') for c in d.get('creators', [])]}
Year: {d.get('date', 'N/A')}\"
"
```

### 5. Search Annotations in PDFs
```bash
curl -s "http://127.0.0.1:23119/api/annotations/search?q=important&limit=5"
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `/api/users/{userId}/items` | List all items |
| `/api/users/{userId}/collections` | List collections |
| `/api/collections/{collectionKey}/items` | Items in collection |
| `/api/items/{itemKey}` | Single item |
| `/api/items/{itemKey}/pdf-content` | PDF text |
| `/api/annotations/search` | Search annotations |
