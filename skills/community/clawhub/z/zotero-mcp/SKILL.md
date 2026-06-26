---
name: zotero-mcp
description: |
  Search and access Zotero reference library via MCP (Model Context Protocol) server.
  Use when working with Zotero literature databases, searching papers, getting item details,
  managing collections, or extracting PDF content and annotations. Requires Zotero running
  with API enabled (Edit, Preferences, Advanced, Network: Allow other applications to access Zotero).
---

# Zotero MCP Skill

This skill provides tools to interact with your Zotero library via the MCP (Model Context Protocol) server.

## Prerequisites

1. **Zotero must be running** with API enabled:
   - Open Zotero → Edit → Preferences → Advanced → Network
   - Check "Allow other applications to access Zotero"

2. **Install zotero-mcp package**:
   ```bash
   npm install -g zotero-mcp
   ```

3. **The MCP server connects to Zotero API at** `http://127.0.0.1:23119`

## Available Tools

### Search Library
```bash
# Search papers by keyword
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"q":"deep learning"}}' | node $(which zotero-mcp-server)
```

### Get Item Details
```bash
# Get full details of an item by key
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_item_by_key","arguments":{"key":"ITEM_KEY"}}' | node $(which zotero-mcp-server)
```

### List Collections
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_collections","arguments":{}}}' | node $(which zotero-mcp-server)
```

### Get Collection Items
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_collection_items","arguments":{"collectionKey":"COLLECTION_KEY"}}}' | node $(which zotero-mcp-server)
```

### Extract PDF Content
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"get_pdf_content","arguments":{"itemKey":"ITEM_KEY"}}}' | node $(which zotero-mcp-server)
```

### Search Annotations
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_annotations","arguments":{"q":"keyword"}}}' | node $(which zotero-mcp-server)
```

## Direct API Access

You can also access Zotero API directly without MCP:

```bash
# Get user ID
curl http://127.0.0.1:23119/api/users/0/items

# Get all collections
curl http://127.0.0.1:23119/api/users/7120115/collections

# Search items
curl "http://127.0.0.1:23119/api/users/7120115/items?q=keyword"
```

## Troubleshooting

- **Port 23119 not responding**: Check Zotero preferences → Advanced → Network
- **No items found**: Try different search keywords or check collection key
- **MCP errors**: Restart Zotero and try again
