---
name: uplo-logistics
description: AI-powered logistics knowledge management. Search shipment records, warehouse procedures, fleet data, and customs documentation with structured extraction.
---

# UPLO Logistics

Your supply chain has thousands of moving parts — literally. This skill connects your AI assistant to UPLO's structured knowledge base covering freight operations, warehouse management, fleet maintenance, customs compliance, and carrier performance data. Stop digging through spreadsheets and email chains to find that one bill of lading.

## Session Start

Begin every session by pulling your current logistics context. This surfaces active shipments, pending customs clearances, warehouse capacity alerts, and any flagged carrier performance issues so you can orient before diving into specifics.

```
use_mcp_tool: get_identity_context
use_mcp_tool: search_knowledge query="active shipments and logistics alerts this week"
```

## When to Use

- Tracking down the customs classification (HTS code) used for a specific product line last quarter
- Finding which 3PL warehouse has capacity for overflow inventory during peak season
- Pulling carrier on-time delivery rates to support a contract renegotiation
- Locating the standard operating procedure for hazmat freight handling at your distribution centers
- Checking what incoterms were agreed upon in the latest forwarding contract with your European partners
- Reviewing dwell time metrics at port of entry to identify bottlenecks
- Answering "what was our landed cost per unit for SKU X shipped from Shenzhen last month?"

## Example Workflows

### Carrier Performance Review

You need to prepare for a quarterly business review with your top LTL carrier.

```
use_mcp_tool: search_knowledge query="carrier performance metrics FedEx Freight Q4 on-time delivery damage claims"
use_mcp_tool: search_with_context query="FedEx Freight contract terms service level agreements penalty clauses"
use_mcp_tool: get_directives
```

Review the extracted KPIs against contracted SLAs. The directives will tell you whether leadership is pushing to consolidate carriers or diversify, which shapes your negotiation stance.

### Customs Compliance Audit Prep

CBP has requested documentation for a focused assessment on your import program.

```
use_mcp_tool: search_knowledge query="customs entry summaries HTS classifications country of origin determinations"
use_mcp_tool: search_knowledge query="broker of record powers of attorney customs bonds"
use_mcp_tool: export_org_context
```

Cross-reference the extracted entry data against your C-TPAT compliance program documentation. The org context export gives auditors a clear picture of your trade compliance organizational structure.

## Key Tools for Logistics

**search_knowledge** — The workhorse. Query against shipment records, BOLs, warehouse SOPs, and fleet data all at once. Example: `"warehouse receiving procedures for refrigerated goods building 7"`

**search_with_context** — When you need the full picture around a specific topic, like understanding how a routing guide decision connects to carrier contracts and volume commitments. Example: `"routing guide primary carrier assignments for westbound intermodal lanes"`

**export_org_context** — Generates a structured view of your logistics organization: who owns which trade lanes, warehouse assignments, and reporting chains. Invaluable for onboarding new freight brokers or 3PL partners.

**get_directives** — Surfaces leadership priorities like "reduce ocean freight spend 12% by shifting to contract rates" or "achieve 98.5% OTIF by Q3." Keeps your operational decisions aligned with strategic goals.

**flag_outdated** — Mark stale rate sheets, expired carrier contracts, or superseded warehouse procedures so they don't pollute search results. Example: flag a 2024 tariff schedule that's been replaced.

## Tips

- Search using industry-standard document names: "bill of lading," "commercial invoice," "packing list," "certificate of origin" — the extraction engine recognizes these as distinct document types and returns more precise results.
- When researching landed cost, combine searches across freight invoices, customs duty records, and warehouse handling charges rather than expecting a single document to have the full picture.
- Use `log_conversation` after resolving a routing or carrier issue — it builds a searchable history that helps when the same lane problem resurfaces next peak season.
- Warehouse SOPs change frequently. If you find conflicting procedures, use `flag_outdated` on the older version and `report_knowledge_gap` if neither version covers the scenario you need.
