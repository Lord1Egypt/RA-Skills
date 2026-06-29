---
name: real-estate-sales-leasing-and-valuations
description: "Real Estate Sales Leasing and Valuations: Look up US property records, get value and rent estimates with comparable properties, search sale and rental listings with agent info, and retrieve aggregated market statistics by zip code. Use when an agent needs real estate sales leasing and valuations, property value estimates, rent estimates with comparables, property record lookups, sale listing search, market statistics, zip code, data type through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations"}}
---
# Real Estate Sales Leasing and Valuations

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Get instant residential property valuations, rent estimates, and market insights for any US address. Search active sale and rental listings, pull detailed property records with tax history and owner information, and analyze market trends by zip code — all in one place. Whether you're evaluating an investment, pricing a rental, or researching a neighborhood, get the real estate data you need without bouncing between multiple sources.

## Product Instructions
### Real Estate Data

Look up property records, get value and rent estimates with comparables, search sale and rental listings, and retrieve market statistics for any US zip code.

#### Actions

##### `value_estimate`
Get an estimated property value with comparable sales.

Required: `address` (string, full address) OR `latitude`+`longitude`
Optional: `property_type`, `bedrooms`, `bathrooms`, `square_footage`, `max_radius`, `days_old`, `comp_count` (5-25)

Returns: price estimate, price range (low/high), subject property details, array of comparable properties with correlation scores.

Example: `{"action":"value_estimate","address":"5500 Grand Lake Dr, San Antonio, TX, 78244"}`

##### `rent_estimate`
Get an estimated monthly rent with comparable rentals.

Required: `address` OR `latitude`+`longitude`
Optional: `property_type`, `bedrooms`, `bathrooms`, `square_footage`, `max_radius`, `days_old`, `comp_count` (5-25)

Returns: rent estimate, rent range (low/high), subject property details, array of comparable rentals with correlation scores.

Example: `{"action":"rent_estimate","address":"5500 Grand Lake Dr, San Antonio, TX, 78244"}`

##### `property_search`
Search property records by location and criteria.

Required: at least one location param (`address`, `city`+`state`, `zip_code`, or `latitude`+`longitude`)
Optional: `radius`, `property_type`, `bedrooms`, `bathrooms`, `square_footage`, `lot_size`, `year_built`, `sale_date_range`, `limit` (1-500), `offset`

Returns: array of property records with tax assessments, features, owner info, sale history.

Example: `{"action":"property_search","zip_code":"78244","property_type":"Single Family","limit":10}`

##### `property_details`
Get a single property record by ID.

Required: `record_id` (string, e.g. "5500-Grand-Lake-Dr,-San-Antonio,-TX-78244")

Example: `{"action":"property_details","record_id":"5500-Grand-Lake-Dr,-San-Antonio,-TX-78244"}`

##### `sale_listings`
Search active or inactive sale listings.

Required: at least one location param
Optional: `radius`, `property_type`, `bedrooms`, `bathrooms`, `square_footage`, `lot_size`, `year_built`, `status` (Active/Inactive), `price`, `days_old`, `limit`, `offset`

Returns: array of listings with price, agent/office info, MLS data, listing history.

Example: `{"action":"sale_listings","city":"Austin","state":"TX","status":"Active","limit":10}`

##### `sale_listing_details`
Get a single sale listing by ID.

Required: `record_id`

##### `rental_listings`
Search active or inactive rental listings.

Required: at least one location param
Optional: same filters as sale_listings

Returns: array of rental listings with rent price, agent/office info, MLS data.

Example: `{"action":"rental_listings","zip_code":"78705","bedrooms":"2","limit":10}`

##### `rental_listing_details`
Get a single rental listing by ID.

Required: `record_id`

##### `market_statistics`
Get aggregated market data for a zip code.

Required: `zip_code`
Optional: `data_type` (All/Sale/Rental, default All), `history_range` (months, default 12)

Returns: sale data (avg/median/min/max price, price per sqft, listings count) and rental data (avg/median/min/max rent, rent per sqft) with historical trends.

Example: `{"action":"market_statistics","zip_code":"78244","history_range":24}`

#### Notes
- `bedrooms`, `bathrooms`, `square_footage`, `lot_size`, `year_built`, `price`, `days_old` support numeric ranges ("min-max") and multiple values ("val1,val2")
- Property types: Single Family, Condo, Townhouse, Manufactured, Multi-Family, Apartment, Land
- IDs use the format "Street-Address,-City,-ST-Zip" with hyphens replacing spaces

## When To Use
- Use this skill for `Real Estate Sales Leasing and Valuations` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: real estate sales leasing and valuations, property value estimates, rent estimates with comparables, property record lookups, sale listing search, market statistics, zip code, data type.
- Supported action names: `market_statistics`, `property_details`, `property_search`, `rent_estimate`, `rental_listing_details`, `rental_listings`, `sale_listing_details`, `sale_listings`, `value_estimate`.

## Use Cases
- Property value estimates
- Rent estimates with comparables
- Property record lookups
- Sale listing search
- Rental listing search
- Market statistics by zip code
- Investment property analysis
- Neighborhood comparison
- Property tax history lookup
- Comparable property analysis

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `9`.
x402 availability: not enabled for this product.

- `market_statistics` (action slug: `market-statistics`): Get aggregated market data for a zip code Price: `25` credits. Parameters: `data_type`, `history_range`, `zip_code`.
- `property_details` (action slug: `property-details`): Get a single property record by ID Price: `25` credits. Parameters: `record_id`.
- `property_search` (action slug: `property-search`): Search property records by location and criteria Price: `25` credits. Parameters: `address`, `bathrooms`, `bedrooms`, `city`, `latitude`, `limit`, `longitude`, `lot_size`, plus 8 more.
- `rent_estimate` (action slug: `rent-estimate`): Get a rent estimate with comparable rentals Price: `25` credits. Parameters: `address`, `bathrooms`, `bedrooms`, `comp_count`, `days_old`, `latitude`, `longitude`, `max_radius`, plus 2 more.
- `rental_listing_details` (action slug: `rental-listing-details`): Get a single rental listing by ID Price: `25` credits. Parameters: `record_id`.
- `rental_listings` (action slug: `rental-listings`): Search rental listings in an area Price: `25` credits. Parameters: `address`, `bathrooms`, `bedrooms`, `city`, `days_old`, `latitude`, `limit`, `longitude`, plus 10 more.
- `sale_listing_details` (action slug: `sale-listing-details`): Get a single sale listing by ID Price: `25` credits. Parameters: `record_id`.
- `sale_listings` (action slug: `sale-listings`): Search sale listings in an area Price: `25` credits. Parameters: `address`, `bathrooms`, `bedrooms`, `city`, `days_old`, `latitude`, `limit`, `longitude`, plus 10 more.
- `value_estimate` (action slug: `value-estimate`): Get a property value estimate with comparable sales Price: `25` credits. Parameters: `address`, `bathrooms`, `bedrooms`, `comp_count`, `days_old`, `latitude`, `longitude`, `max_radius`, plus 2 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "real-estate-sales-leasing-and-valuations"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "real-estate-sales-leasing-and-valuations"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "real-estate-sales-leasing-and-valuations"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "real-estate-sales-leasing-and-valuations"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "real-estate-sales-leasing-and-valuations"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "real-estate-sales-leasing-and-valuations"
  }
}
```

## Call This Tool
Product slug: `real-estate-sales-leasing-and-valuations`

Marketplace page: https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Real-Estate-Sales-Leasing-and-Valuations",
    "arguments": {
      "action": "market_statistics",
      "data_type": "All",
      "history_range": 1,
      "zip_code": "example zip code"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "real-estate-sales-leasing-and-valuations",
  "parameters": {
    "action": "market_statistics",
    "data_type": "All",
    "history_range": 1,
    "zip_code": "example zip code"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `market_statistics` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/real-estate-sales-leasing-and-valuations
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
