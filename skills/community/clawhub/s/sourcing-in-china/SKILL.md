---
name: sourcing-in-china
description: Search products, suppliers, and get detailed product info from Made-in-China.com via MCP server. Use when sourcing products from China, finding manufacturers, comparing suppliers, checking MOQ/pricing, or any global procurement task involving Chinese suppliers. Triggers on keywords like "source", "find supplier", "manufacturer", "MOQ", "made in china", "China sourcing", "procurement".
metadata:
  openclaw:
    externalServices:
      - url: "https://mcp.chexb.com/sse"
        protocol: "MCP (SSE) over HTTPS"
        description: "Made-in-China.com product/supplier search proxy. Search queries and product URLs are sent to this server, which scrapes public Made-in-China.com pages and returns structured data. No authentication required. No user data is stored."
        dataFlow: "outbound: search keywords, product URLs | inbound: product listings, supplier info, pricing"
---

# Sourcing in China

Search products, find suppliers, and get product details from Made-in-China.com via a public MCP server.

**MCP Endpoint:** `https://mcp.chexb.com/sse`

No external CLI dependencies — calls are made via standard HTTP (MCP over SSE).

## Available Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `search_products` | Search products by keyword | `keyword` (required), `page` (default 1, 30/page) |
| `search_suppliers` | Search manufacturers/suppliers | `keyword` (required), `page` (default 1, 10/page) |
| `get_product_detail` | Full product page details | `url` (required, product page URL from search results) |

## How to Call

### MCP over SSE (standard HTTP)

```bash
# 1. Connect to SSE endpoint, get session
SESSION=$(curl -sN https://mcp.chexb.com/sse | grep "^data:" | head -1 | sed 's/data: //')

# 2. Initialize MCP session
curl -s -X POST "https://mcp.chexb.com${SESSION}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'

# 3. Call a tool
curl -s -X POST "https://mcp.chexb.com${SESSION}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_products","arguments":{"keyword":"LED light","page":1}}}'
```

### With mcporter (optional convenience)

If `mcporter` is installed, calls are simpler:

```bash
mcporter call https://mcp.chexb.com/sse.search_products keyword="LED light"
mcporter call https://mcp.chexb.com/sse.search_suppliers keyword="LED light"
mcporter call https://mcp.chexb.com/sse.get_product_detail url="https://..."
```

## Sourcing Workflow

### 1. Product Discovery

Start with `search_products` to find products matching requirements. Each result includes:
- Product name, price, MOQ
- Key specifications (properties)
- Supplier name and link
- Product image

Iterate pages for broader results. Refine keywords for precision (e.g., "12V LED strip waterproof" vs "LED").

### 2. Supplier Evaluation

Use `search_suppliers` to find manufacturers. Results include:
- Company name and business type (Manufacturer / Trading Company)
- Main products and location
- Certification badges (ISO, audited, etc.)

**Prefer manufacturers over trading companies** for better pricing. Check badges for quality signals.

### 3. Product Deep Dive

Use `get_product_detail` on promising products. Returns:
- Full specifications and description
- All product images
- Sample pricing (if available)
- Product categories and video URL
- Supplier/brand info

### 4. Comparison & Recommendation

When comparing options, organize by:
- **Price range** (unit price + MOQ)
- **Supplier credibility** (badges, business type)
- **Specifications match** (vs buyer requirements)
- **Sample availability** (sample price if listed)

## Best Practices

- Use English keywords for best results on Made-in-China.com
- Search both products AND suppliers for the same keyword to get different perspectives
- Always check MOQ — it varies dramatically between suppliers
- "Manufacturer" business type typically means better unit pricing
- Cross-reference supplier badges: Audited Supplier > general listings
- For detailed specs, always follow up with `get_product_detail`

## Output Format

Present results in clean, scannable format:
- Use tables for product/supplier comparisons
- Highlight price, MOQ, and key specs prominently
- Include direct links to products and supplier pages
- Flag notable badges or certifications

## Data & Privacy

This skill sends data to an external MCP server:

- **Endpoint:** `https://mcp.chexb.com/sse`
- **What is sent:** Search keywords, page numbers, product URLs
- **What is returned:** Public product listings, supplier info, pricing, images from Made-in-China.com
- **Storage:** No queries or results are stored on the server
- **Authentication:** None required — the server is a stateless proxy that scrapes public pages

⚠️ Do not include sensitive or proprietary information in search queries. All queries are transmitted over HTTPS.

For more on sourcing strategy, see [references/sourcing-guide.md](references/sourcing-guide.md).
