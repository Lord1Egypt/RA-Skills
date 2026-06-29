---
name: public-commons-media-search
description: "Public Commons Media Search: Search Wikipedia and Wikimedia Commons for free images, audio, video. Get file URLs and licensing info. Supports pagination. Use when an agent needs public commons media search, agentic media discovery, search wikimedia commons files by keyword, find free images for articles, retrieve media download urls, get file, file title, project through AgentPMT-hosted remote tool calls. Discovery terms: public commons media search, agentic media discovery."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/public-commons-media-search
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/public-commons-media-search"}}
---
# Public Commons Media Search

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Let AI agents search Wikipedia and Wikimedia Commons to discover and download free images, audio, video, and other public media assets. The tool provides simple actions for page title search, listing media on a page, fetching file URLs (thumbnail, preferred, original), and direct Commons media search with pagination, enabling agentic content sourcing and research workflows with clear file description and licensing context.

## Product Instructions
### Public Commons Media Search

Search Wikipedia and Wikimedia Commons to discover public media assets, find article titles, list media on pages, and retrieve file URLs with metadata.

#### Actions

##### search_titles

Search Wikipedia for article titles matching a query.

**Required fields:**
- `action`: `"search_titles"`
- `q`: Search query string

**Optional fields:**
- `project`: Wikimedia project (default: `"wikipedia"`). Must NOT be `"commons"`.
- `language`: Language code (default: `"en"`)
- `limit`: Maximum results, 1-50 (default: 50)

**Example:**
```json
{
  "action": "search_titles",
  "q": "solar eclipse",
  "language": "en",
  "limit": 10
}
```

Returns a list of matching pages with title, description, and excerpt.

---

##### list_page_media

List all media files (images, audio, video) embedded on a specific Wikipedia page.

**Required fields:**
- `action`: `"list_page_media"`
- `title`: Canonical page title (e.g., `"Solar_eclipse"`)

**Optional fields:**
- `project`: Wikimedia project (default: `"wikipedia"`). Must NOT be `"commons"`.
- `language`: Language code (default: `"en"`)

**Example:**
```json
{
  "action": "list_page_media",
  "title": "Golden_Gate_Bridge",
  "language": "en"
}
```

Returns a list of media items found on the page.

---

##### get_file

Retrieve detailed file metadata and URLs (original, preferred, thumbnail) for a specific media file.

**Required fields:**
- `action`: `"get_file"`
- `file_title`: Full file title including the `File:` prefix (e.g., `"File:Example.jpg"`)

**Optional fields:**
- `project`: Wikimedia project (default: `"wikipedia"`). Set to `"commons"` when the file is hosted on Wikimedia Commons.
- `language`: Language code (default: `"en"`). Required when project is not `"commons"`.

**Example — Wikipedia file:**
```json
{
  "action": "get_file",
  "file_title": "File:Golden_Gate_Bridge_20100906.jpg",
  "project": "wikipedia",
  "language": "en"
}
```

**Example — Commons file:**
```json
{
  "action": "get_file",
  "file_title": "File:Hubble_ultra_deep_field.jpg",
  "project": "commons"
}
```

Returns the file title, description URL, and links to original, preferred, and thumbnail versions of the file.

---

##### search_commons_media

Search Wikimedia Commons directly for media files (images, audio, video, SVGs). Supports pagination for browsing large result sets.

**Required fields:**
- `action`: `"search_commons_media"`
- `q`: Search query string

**Optional fields:**
- `limit`: Maximum results, 1-50 (default: 50)
- `offset`: Pagination offset (default: 0). Use the `next_offset` value from a previous response to get the next page.

**Example:**
```json
{
  "action": "search_commons_media",
  "q": "northern lights aurora",
  "limit": 10
}
```

**Pagination example:**
```json
{
  "action": "search_commons_media",
  "q": "northern lights aurora",
  "limit": 10,
  "offset": 10
}
```

Returns matching file titles, page IDs, and text snippets. Includes `next_offset` when more results are available.

---

#### Common Workflows

##### Find and download a Wikipedia image
1. Use `search_titles` to find the article (e.g., `"q": "Eiffel Tower"`)
2. Use `list_page_media` with the returned title to see all media on the page
3. Use `get_file` with the desired `file_title` (include the `File:` prefix) to get the direct URL

##### Search Commons for stock-style media
1. Use `search_commons_media` with a descriptive query (e.g., `"q": "sunset over ocean"`)
2. Pick a result and use `get_file` with `project` set to `"commons"` and the file title to get URLs

##### Browse media in another language
- Set `language` to any valid code (e.g., `"fr"`, `"de"`, `"ja"`) when using `search_titles`, `list_page_media`, or `get_file` with Wikipedia

#### Important Notes

- The `file_title` parameter must always include the `File:` prefix (e.g., `"File:Example.png"`).
- The `project` parameter should be set to `"commons"` only for `get_file` when the file is hosted on Wikimedia Commons. For `search_titles` and `list_page_media`, use `"wikipedia"` (the default).
- `search_commons_media` always searches Wikimedia Commons regardless of the `project` or `language` settings.
- All media found through this tool is from Wikimedia projects and is generally available under open licenses (Creative Commons, public domain, etc.). Always check the file description page for specific license terms.
- Results are capped at 50 per request. Use `offset` with `search_commons_media` to paginate through larger result sets.

## When To Use
- Use this skill for `Public Commons Media Search` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: public commons media search, agentic media discovery, search wikimedia commons files by keyword, find free images for articles, retrieve media download urls, get file, file title, project.
- Supported action names: `get_file`, `list_page_media`, `search_commons_media`, `search_titles`.

## Use Cases
- Agentic media discovery
- Search Wikimedia Commons files by keyword
- Find free images for articles
- Retrieve media download URLs
- Check file description and license pages
- Collect public media assets for presentations
- Build datasets of public images
- Source audio or video clips for projects

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `4`.
x402 availability: not enabled for this product.

- `get_file` (action slug: `get-file`): Retrieve detailed file metadata and URLs (original, preferred, thumbnail) for a specific media file. Price: `5` credits. Parameters: `file_title`, `language`, `project`.
- `list_page_media` (action slug: `list-page-media`): List all media files (images, audio, video) embedded on a specific Wikipedia page. Price: `5` credits. Parameters: `language`, `project`, `title`.
- `search_commons_media` (action slug: `search-commons-media`): Search Wikimedia Commons directly for media files (images, audio, video, SVGs). Supports pagination for browsing large result sets. Price: `5` credits. Parameters: `limit`, `offset`, `q`.
- `search_titles` (action slug: `search-titles`): Search Wikipedia for article titles matching a query. Returns matching pages with title, description, and excerpt. Price: `5` credits. Parameters: `language`, `limit`, `project`, `q`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "public-commons-media-search"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "public-commons-media-search"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "public-commons-media-search"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "public-commons-media-search"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "public-commons-media-search"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "public-commons-media-search"
  }
}
```

## Call This Tool
Product slug: `public-commons-media-search`

Marketplace page: https://www.agentpmt.com/marketplace/public-commons-media-search

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
    "name": "Public-Commons-Media-Search",
    "arguments": {
      "action": "get_file",
      "file_title": "example file title",
      "language": "en",
      "project": "wikipedia"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "public-commons-media-search",
  "parameters": {
    "action": "get_file",
    "file_title": "example file title",
    "language": "en",
    "project": "wikipedia"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_file` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/public-commons-media-search
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
