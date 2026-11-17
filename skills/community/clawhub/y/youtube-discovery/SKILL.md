---
name: youtube-discovery
description: "YouTube Discovery: Search and inspect public YouTube data. Use when an agent needs youtube discovery, search youtube videos by topic keyword and advanced filters, discover trending videos by country and category, vet channels by subscriber and view statistics, research competitor content and posting cadence, get channel details, channel id, channel handle through AgentPMT-hosted remote tool calls. Discovery terms: youtube discovery, search youtube videos by topic keyword and advanced filters."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/youtube-discovery
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/youtube-discovery"}}
---
# YouTube Discovery

## Freshness
Last updated: `2026-07-04`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Tap into the full world of public YouTube data straight from your agent. Search billions of videos, channels, and playlists by topic, keyword, channel, date, language, region, livestream status, captions, duration, and license, then pull rich metadata and statistics like view counts, like counts, comment counts, subscriber counts, durations, tags, and topics. Track trending videos by country and category, browse the contents of any public playlist, and read public comment threads to gauge audience sentiment. Ideal for content research, competitive analysis, SEO and keyword discovery, influencer and channel vetting, brand and media monitoring, and trend spotting.

## Product Instructions
### YouTube Discovery

Search and inspect public YouTube data: videos, channels, playlists, comment threads, categories, languages, and regions. Returns public metadata only (no media downloads, no private owner data).

#### Actions

##### `search`
Find videos, channels, and/or playlists. Provide at least one selector: `query`, `channel_id`, `topic_id`, `video_category_id`, `location` (with `location_radius`), or `event_type`.

Common inputs:
- `resource_types`: array of `video` / `channel` / `playlist` (default `["video"]`)
- `max_results`: 1-50 (default 10)
- `order`: `relevance` | `date` | `rating` | `viewCount` | `title` | `videoCount`
- `page_token`: cursor from a prior page
- `published_after` / `published_before`: RFC3339, e.g. `2026-01-01T00:00:00Z`
- `region_code` (ISO 3166-1 alpha-2), `relevance_language` (ISO 639-1), `safe_search` (`none`|`moderate`|`strict`)
- `include_video_details`: `true` to enrich video results with stats, duration, license, captions, tags, and topics

Video-only filters (require `resource_types:["video"]`): `event_type`, `location` + `location_radius`, `video_caption`, `video_category_id`, `video_definition`, `video_dimension`, `video_duration`, `video_embeddable`, `video_license`, `video_paid_product_placement`, `video_syndicated`, `video_type`. `channel_type` requires `resource_types:["channel"]`.

##### `get_video_details`
Required: `video_ids` (array, 1-50) of 11-character video IDs.

##### `get_trending_videos`
Optional: `region_code`, `video_category_id`, `max_results` (1-50), `page_token`, `hl`.

##### `get_channel_details`
Exactly one of: `channel_id`, `channel_handle` (e.g. `@name`), `channel_username` (legacy).

##### `list_channel_playlists`
Required: `channel_id`. Optional: `max_results` (1-50), `page_token`, `hl`.

##### `list_playlist_items`
Required: `playlist_id`. Optional: `max_results` (1-50), `page_token`.

##### `list_public_comments`
Exactly one of: `video_id`, `channel_id`, `thread_ids` (array). Optional: `include_replies`, `text_format` (`plainText`|`html`), `comment_order` (`time`|`relevance`), `search_terms`, `max_results` (1-100), `page_token`.

##### `list_video_categories`
Exactly one of: `region_code`, `category_ids` (array). Optional: `hl`.

##### `list_supported_languages` / `list_supported_regions`
Optional: `hl`.

#### Examples

```json
{"action":"search","query":"home espresso","resource_types":["video"],"order":"viewCount","max_results":5,"include_video_details":true}
```
```json
{"action":"get_video_details","video_ids":["dQw4w9WgXcQ","9bZkp7q19f0"]}
```
```json
{"action":"get_trending_videos","region_code":"US","video_category_id":"10","max_results":10}
```
```json
{"action":"get_channel_details","channel_handle":"@jameshoffmann"}
```
```json
{"action":"list_public_comments","video_id":"dQw4w9WgXcQ","comment_order":"relevance","max_results":20}
```

#### Pagination

Responses include `next_page_token` / `prev_page_token` when more pages exist. Pass it back as `page_token`. One page is fetched per call.

#### Response

Each action returns its collection (`results`, `videos`, `channels`, `playlists`, `playlist_items`, `comment_threads`, `categories`, `languages`, or `regions`) plus `page_info`. Items use snake_case fields and include a ready-to-open `youtube_url`. Video items expose `view_count`, `like_count`, `comment_count`, `duration`, `tags`, `category_id`, `topic_categories`, caption availability, and live details; channels expose `subscriber_count`, `video_count`, `view_count`, and `uploads_playlist_id` (pass it to `list_playlist_items` to page a channel's full upload history).

#### Limits

Public metadata only. Cannot download audio, video, captions, or thumbnails; cannot read private channel-owner analytics; cannot create, edit, delete, upload, or moderate content.

## When To Use
- Use this skill for `YouTube Discovery` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: youtube discovery, search youtube videos by topic keyword and advanced filters, discover trending videos by country and category, vet channels by subscriber and view statistics, research competitor content and posting cadence, get channel details, channel id, channel handle.
- Supported action names: `get_channel_details`, `get_trending_videos`, `get_video_details`, `list_channel_playlists`, `list_playlist_items`, `list_public_comments`, `list_supported_languages`, `list_supported_regions`, `list_video_categories`, `search`.

## Use Cases
- Search YouTube videos by topic keyword and advanced filters
- Discover trending videos by country and category
- Vet channels by subscriber and view statistics
- Research competitor content and posting cadence
- Find videos with captions or Creative Commons licenses
- Analyze public comment threads for audience sentiment
- Browse playlist contents for content curation
- Build SEO and keyword discovery workflows
- Monitor brand and topic mentions across YouTube
- Pull video statistics for performance benchmarking

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `10`.
x402 action routes are enabled and listed in `./schema.md`.

- `get_channel_details` (action slug: `get-channel-details`): Retrieve one public channel by channel id, handle, or legacy username. Price: `5` credits. Parameters: `channel_handle`, `channel_id`, `channel_username`.
- `get_trending_videos` (action slug: `get-trending-videos`): Retrieve public trending videos by region or category. Price: `5` credits. Parameters: `hl`, `max_results`, `page_token`, `region_code`, `video_category_id`.
- `get_video_details` (action slug: `get-video-details`): Retrieve public metadata and statistics for up to 50 videos. Price: `5` credits. Parameters: `video_ids`.
- `list_channel_playlists` (action slug: `list-channel-playlists`): List public playlists for a channel. Price: `5` credits. Parameters: `channel_id`, `hl`, `max_results`, `page_token`.
- `list_playlist_items` (action slug: `list-playlist-items`): List public items in a playlist. Price: `5` credits. Parameters: `max_results`, `page_token`, `playlist_id`.
- `list_public_comments` (action slug: `list-public-comments`): List public comment threads for a video, channel, or explicit thread ids. Price: `5` credits. Parameters: `channel_id`, `comment_order`, `include_replies`, `max_results`, `page_token`, `search_terms`, `text_format`, `thread_ids`, plus 1 more.
- `list_supported_languages` (action slug: `list-supported-languages`): List supported YouTube interface languages. Price: `5` credits. Parameters: `hl`.
- `list_supported_regions` (action slug: `list-supported-regions`): List supported YouTube regions. Price: `5` credits. Parameters: `hl`.
- `list_video_categories` (action slug: `list-video-categories`): List public YouTube video categories by region or explicit ids. Price: `5` credits. Parameters: `category_ids`, `hl`, `region_code`.
- `search` (action slug: `search`): Search public YouTube videos, channels, or playlists with filters and pagination. Price: `5` credits. Parameters: `channel_id`, `channel_type`, `event_type`, `include_video_details`, `location`, `location_radius`, `max_results`, `order`, plus 19 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "youtube-discovery"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "youtube-discovery"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "youtube-discovery"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "youtube-discovery"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "youtube-discovery"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "youtube-discovery"
  }
}
```

## Call This Tool
Product slug: `youtube-discovery`

Marketplace page: https://www.agentpmt.com/marketplace/youtube-discovery

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account AgentAddress/x402 route: first use `../agentpmt-no-account-agentaddress-x402` for the canonical payment and wallet setup instructions.
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
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
  - OpenClaw install: `openclaw skills install agentpmt-no-account-agentaddress-x402`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "YouTube-Discovery",
    "arguments": {
      "action": "get_channel_details",
      "channel_handle": "example channel handle",
      "channel_id": "example channel id",
      "channel_username": "example channel username"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "youtube-discovery",
  "parameters": {
    "action": "get_channel_details",
    "channel_handle": "example channel handle",
    "channel_id": "example channel id",
    "channel_username": "example channel username"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_channel_details` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/youtube-discovery
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
