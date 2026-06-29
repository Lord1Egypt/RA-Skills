---
name: real-estate-aerial-video-generator
description: "Real Estate Aerial Video Generator: Create cinematic aerial videos from street addresses, check whether a video is ready yet, and return downloadable MP4 links for completed footage. Use when an agent needs real estate aerial video generator, real estate listing videos, vacation rental marketing, neighborhood preview videos, destination marketing, fetch existing aerial video, address, video id through AgentPMT-hosted remote tool calls. Discovery terms: real estate aerial video generator."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator"}}
---
# Real Estate Aerial Video Generator

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Turn a street address into a cinematic aerial property video you can share with buyers, clients, or stakeholders. This tool is useful for real estate listings, neighborhood previews, destination marketing, property presentations, and location-based sales materials. Completed videos are returned as downloadable MP4 links that can be handed directly to the user.

## Product Instructions
### Real Estate Aerial Video Generator

Create cinematic aerial property videos from a street address and return a downloadable MP4 when the footage is ready.

#### Actions

##### generate_aerial_video

Request an aerial video for a location.

Required fields:
- `address` (string): Full street address.

Optional fields:
- None.

Example:
```json
{
  "action": "generate_aerial_video",
  "address": "230 Wellington St, Traverse City, MI 49686"
}
```

Typical statuses:
- `completed`: Video is ready now. Return the `signed_url` to the user.
- `queued`: A new request was submitted. Save the returned `video_id` for later checks.
- `processing`: A prior request is still being prepared.
- `unavailable`: No aerial coverage is available for that location.

##### fetch_existing_aerial_video

Retrieve a completed video or check the status of an earlier request.

Required fields:
- At least one of `address` or `video_id`.

Optional fields:
- `address` (string): Street address used for the request.
- `video_id` (string): Video identifier from a prior response.

Example using an address:
```json
{
  "action": "fetch_existing_aerial_video",
  "address": "230 Wellington St, Traverse City, MI 49686"
}
```

Example using a video ID:
```json
{
  "action": "fetch_existing_aerial_video",
  "video_id": "ZsqpL5f2WAQxXrtbqWq8AP"
}
```

Typical statuses:
- `completed`: Response includes `signed_url`, `file_id`, `size_bytes`, and metadata such as `videoId`, `captureDate`, and `duration`.
- `processing`: Video is still being prepared.
- `not_found`: No prior video exists for that address or ID.
- `failed`: The prior request did not complete successfully.

#### Recommended Flow

1. Call `generate_aerial_video` when the user asks for a new video.
2. If the response is `completed`, present the `signed_url` directly.
3. If the response is `queued`, keep the returned `video_id`.
4. Use `fetch_existing_aerial_video` later with the `video_id` or original address.

#### Example Chat Conversation

User: "Can you make an aerial video for 230 Wellington St, Traverse City, MI 49686?"

Assistant: "I’ll check whether one is already available for that address and return the download link if it is ready."

Assistant tool call:
```json
{
  "action": "fetch_existing_aerial_video",
  "address": "230 Wellington St, Traverse City, MI 49686"
}
```

Assistant if completed:
"The aerial video is ready. Here is the download link: <signed_url>"

Assistant if processing:
"The video is not ready yet. I can check again later using the saved video ID."

#### Notes

- Completed download links expire after 7 days.
- New requests can take 24 to 48 hours before they are ready.
- Some addresses do not have aerial coverage.

## When To Use
- Use this skill for `Real Estate Aerial Video Generator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: real estate aerial video generator, real estate listing videos, vacation rental marketing, neighborhood preview videos, destination marketing, fetch existing aerial video, address, video id.
- Supported action names: `fetch_existing_aerial_video`, `generate_aerial_video`.

## Use Cases
- Real estate listing videos
- Vacation rental marketing
- Neighborhood preview videos
- Destination marketing
- Property presentation media
- Venue showcase videos
- Sales outreach assets
- Location-based client presentations

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `2`.
x402 availability: not enabled for this product.

- `fetch_existing_aerial_video` (action slug: `fetch-existing-aerial-video`): Retrieve a completed aerial video or check the status of a previous request. Provide either the original address or a prior video_id. Price: `0` credits. Parameters: `address`, `video_id`.
- `generate_aerial_video` (action slug: `generate-aerial-video`): Request an aerial video for a street address. If a video already exists for that address, return it immediately. Otherwise queue the request and return the current status. Price: `25` credits. Parameters: `address`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "real-estate-aerial-video-generator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "real-estate-aerial-video-generator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "real-estate-aerial-video-generator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "real-estate-aerial-video-generator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "real-estate-aerial-video-generator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "real-estate-aerial-video-generator"
  }
}
```

## Call This Tool
Product slug: `real-estate-aerial-video-generator`

Marketplace page: https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator

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
    "name": "Real-Estate-Aerial-Video-Generator",
    "arguments": {
      "action": "fetch_existing_aerial_video",
      "address": "example address",
      "video_id": "example video id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "real-estate-aerial-video-generator",
  "parameters": {
    "action": "fetch_existing_aerial_video",
    "address": "example address",
    "video_id": "example video id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `fetch_existing_aerial_video` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
