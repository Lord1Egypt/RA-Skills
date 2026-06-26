# UPLO Customer 360 — Full Customer Lifecycle Intelligence

AI-powered customer lifecycle intelligence spanning sales, customer success, and retail. Unified search across pipeline data, account health, and customer analytics.

[![ClawHub](https://img.shields.io/badge/ClawHub-uplo-customer-360-blue)](https://clawhub.com/skills/uplo-customer-360)
[![MCP](https://img.shields.io/badge/MCP-21_tools-green)](https://uplo.ai)
[![Schemas](https://img.shields.io/badge/schemas-14-orange)](https://uplo.ai/schemas)

## Quick Install

```bash
clawhub install uplo-customer-360
```

Or add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "uplo-customer-360": {
      "command": "npx",
      "args": ["-y", "@agentdocs1/mcp-server", "--http"],
      "env": {
        "AGENTDOCS_URL": "https://your-instance.uplo.ai",
        "API_KEY": "your-api-key",
        "DEFAULT_PACKS": "sales_marketing,customer_success,retail"
      }
    }
  }
}
```

## What You Get

- **14 industry schemas** — pre-built extraction templates for Customer 360 documents
- **21 MCP tools** — search, GraphRAG, directives, knowledge gaps, proposals, and more
- **1,400+ format support** — PDF, DOCX, PPTX, emails, images, and 1,400 more via Docling + Tika
- **Classification tiers** — public/internal/confidential/restricted access control
- **Benchmark proven** — 96% accuracy vs 53% for raw context at scale

## MCP Tools Available

| Tool | Description |
|------|-------------|
| `search_knowledge` | Semantic search across extracted knowledge |
| `search_with_context` | GraphRAG: vector search + entity resolution + edge traversal |
| `export_org_context` | Full organizational context snapshot |
| `get_directives` | Strategic priorities and directives |
| `find_knowledge_owner` | Find subject matter experts |
| `propose_update` | Suggest knowledge base updates |
| `report_knowledge_gap` | Flag missing information |
| `flag_outdated` | Mark stale entries |

## Schema Packs

- **Sales & Marketing** — 5 schemas
- **Customer Success** — 4 schemas
- **Retail** — 5 schemas

## Related Skills

- [UPLO Customer Success — Account Health & Retention Intelligence](https://clawhub.com/skills/uplo-customer-success) — AI-powered customer success knowledge management.
- [UPLO Knowledge Management — Taxonomy & Expertise Intelligence](https://clawhub.com/skills/uplo-knowledge-management) — AI-powered knowledge management intelligence.
- [UPLO Accounting — Bookkeeping & Tax Intelligence](https://clawhub.com/skills/uplo-accounting) — AI-powered accounting knowledge management.

## About UPLO

UPLO is the organizational digital twin for AI. Ingest documents, extract structured knowledge, build org context, and expose it via MCP server with GraphRAG. [Learn more](https://uplo.ai)

---

*Built with UPLO — the knowledge layer between your organization and AI.*
