---
name: space-earth-science-explorer
description: "Space & Earth Science Explorer: Search and retrieve space imagery, scientific datasets, earthquake events, and earth observation data. Use when an agent needs space & earth science explorer, space earth science explorer, search space and astronomy imagery, discover scientific research datasets, track real time earthquake activity, explore climate and weather observation data, query space science data, query through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/space-earth-science-explorer
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/space-earth-science-explorer"}}
---
# Space & Earth Science Explorer

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Explore the cosmos and our planet from your workflow. Search stunning space imagery, discover scientific datasets, track earthquake activity in real time, and tap into decades of earth observation and climate research. Whether you're building a research project, creating content, or just curious about what's happening in space and on Earth — this puts a universe of scientific data at your fingertips.

## Product Instructions
### Space & Earth Science Explorer

#### Overview
Search space imagery, scientific datasets, earthquake activity, and earth observation records from NASA, NOAA, and USGS. Supports natural-language queries, source filtering, time period ranges, and returns clean, structured results for research, content creation, or analysis. All data comes from public federal APIs requiring no user credentials.

#### Actions

##### query_space_science_data
Search across multiple federal science data sources using a natural-language query.

**Required Parameters:**
- `action` (string): Must be `"query_space_science_data"`
- `query` (string): Natural-language search query describing the data you want

**Optional Parameters:**
- `source` (string): Filter results to a specific agency. One of `"nasa"`, `"noaa"`, `"usgs"`, or `"all"`. Default: `"all"`
- `time_period` (string): Time filter. Accepts `"latest"`, a single year like `"2024"`, or a range like `"2015:2024"`. When omitted or set to `"latest"`, no year filtering is applied (USGS earthquakes default to the last 30 days)
- `limit` (integer): Maximum number of records to return. Range: 1-100. Default: 20

**Source Behavior:**
- `"nasa"` -- Searches the NASA Image Library for imagery and data.gov for NASA datasets
- `"noaa"` -- Searches data.gov for NOAA datasets (climate, ocean, weather)
- `"usgs"` -- Searches USGS earthquake events and data.gov for DOI/USGS datasets
- `"all"` -- Queries all three sources. The limit is split evenly across sources

**Earthquake Magnitude Filtering:**
Include magnitude hints in your query text using patterns like `"magnitude >= 4"`, `"mag:5"`, or `"mag>=6.0"` and the tool will automatically apply a minimum magnitude filter to USGS earthquake results.

**Example -- Search NASA for Mars rover images:**
```json
{
  "action": "query_space_science_data",
  "query": "mars rover images",
  "source": "nasa",
  "limit": 5
}
```

**Example -- Search NOAA for sea level data over a year range:**
```json
{
  "action": "query_space_science_data",
  "query": "sea level rise",
  "source": "noaa",
  "time_period": "2020:2025"
}
```

**Example -- Search USGS for earthquakes with magnitude filter:**
```json
{
  "action": "query_space_science_data",
  "query": "magnitude >= 4 earthquakes",
  "source": "usgs",
  "limit": 10
}
```

**Example -- Search all sources for solar flare activity in a specific year:**
```json
{
  "action": "query_space_science_data",
  "query": "solar flare activity",
  "time_period": "2024"
}
```

**Example -- Broad search across all sources with default settings:**
```json
{
  "action": "query_space_science_data",
  "query": "ocean temperature anomalies"
}
```

#### Response Format

Each result in the `results` array contains:
- `source` -- Origin of the data (e.g., `"nasa_images"`, `"data_gov"`, `"usgs_earthquakes"`)
- `kind` -- Type of result: `"image"`, `"dataset"`, or `"event"`
- `agency` -- Originating agency name (e.g., `"NASA"`, `"USGS"`)
- `title` -- Title of the image, dataset, or event
- `description` -- Trimmed description (max 320 characters)

Additional fields vary by source:
- **NASA Images**: `date_created`, `nasa_id`, `preview_url`, `asset_manifest_url`
- **Data.gov Datasets**: `landing_page_url`, `resource_url`, `resource_format`, `metadata_modified`, `tags`
- **USGS Earthquakes**: `url`, `time`, `magnitude`, `place`, `tsunami`

The response also includes an `errors` array listing any upstream source failures, allowing partial results when some sources are unavailable.

#### Suggested Workflows

1. **Research Briefing**: Query with `source: "all"` to gather imagery, datasets, and events on a topic, then compile into a summary
2. **Earthquake Monitoring**: Use `source: "usgs"` with magnitude filters in the query to monitor seismic activity for a region
3. **Climate Data Discovery**: Use `source: "noaa"` with time ranges to find datasets on ocean, weather, or atmospheric conditions
4. **Space Image Collection**: Use `source: "nasa"` to find space and astronomy imagery for presentations or content

#### Notes
- When `source` is `"all"`, the `limit` is divided evenly across sources (e.g., limit of 20 with 3 sources gives roughly 7 results per source)
- Unrecognized `time_period` values are silently ignored (no filtering applied)
- If all upstream sources fail and no results are returned, the tool raises an error with details about the failures
- The tool uses publicly available federal APIs and does not require any API keys or credentials

## When To Use
- Use this skill for `Space & Earth Science Explorer` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: space & earth science explorer, space earth science explorer, search space and astronomy imagery, discover scientific research datasets, track real time earthquake activity, explore climate and weather observation data, query space science data, query.
- Supported action names: `query_space_science_data`.

## Use Cases
- Search space and astronomy imagery
- Discover scientific research datasets
- Track real-time earthquake activity
- Explore climate and weather observation data
- Find earth observation satellite imagery
- Research space mission archives
- Analyze geophysical and environmental trends

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `query_space_science_data` (action slug: `query-space-science-data`): Search across NASA, NOAA, and USGS public data sources using a natural-language query. Returns space imagery, scientific datasets, earthquake events, and earth observation records. Price: `5` credits. Parameters: `limit`, `query`, `source`, `time_period`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "space-earth-science-explorer"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "space-earth-science-explorer"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "space-earth-science-explorer"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "space-earth-science-explorer"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "space-earth-science-explorer"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "space-earth-science-explorer"
  }
}
```

## Call This Tool
Product slug: `space-earth-science-explorer`

Marketplace page: https://www.agentpmt.com/marketplace/space-earth-science-explorer

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
    "name": "Space--Earth-Science-Explorer",
    "arguments": {
      "action": "query_space_science_data",
      "limit": 20,
      "query": "example search query",
      "source": "all",
      "time_period": "example time period"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "space-earth-science-explorer",
  "parameters": {
    "action": "query_space_science_data",
    "limit": 20,
    "query": "example search query",
    "source": "all",
    "time_period": "example time period"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `query_space_science_data` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/space-earth-science-explorer
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
