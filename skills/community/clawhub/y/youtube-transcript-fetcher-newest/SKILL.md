---
name: youtube-transcript-fetcher
description: "Youtube Transcript Fetcher: Fetch YouTube video transcripts by URL or video ID. Returns plain text or timestamped segments. Multi-language support. Use when an agent needs youtube transcript fetcher, generating searchable text from video content, creating video summaries or show notes, building accessibility tools for hearing impaired users, extracting quotes with precise timestamps for citations, fetch, video url, video id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/youtube-transcript-fetcher
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/youtube-transcript-fetcher"}}
---
# Youtube Transcript Fetcher

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
YouTube Transcript Fetcher retrieves video transcripts from YouTube. The tool accepts either a full YouTube URL or an 11-character video ID. Supported URL formats include standard watch URLs (youtube.com/watch?v=), shortened URLs (youtu.be), Shorts, embeds, and live streams. When both are provided, video_id takes precedence over video_url. Transcripts are returned as plain text by default. Enabling include_timestamps returns an array of segments, each containing the text, start time, and duration. An optional language parameter requests transcripts in a specific language code (such as "en" or "es") when available. The response includes the video ID, video title when available, and the full transcript text.

## Product Instructions
### Youtube Transcript Fetcher

#### Overview
Fetch transcripts from YouTube videos. Provide a video URL or video ID and receive the full transcript text saved as a downloadable JSON file. Supports language selection and optional timestamped segments.

#### Actions

##### fetch
Retrieve the transcript for a YouTube video. The transcript is saved to cloud storage and a signed download URL is returned.

**Required fields (one of the following):**
- `video_url` (string) — Full YouTube URL. Supported formats include `https://www.youtube.com/watch?v=VIDEO_ID`, `https://youtu.be/VIDEO_ID`, shorts, embeds, and live URLs.
- `video_id` (string) — The 11-character YouTube video ID. Takes precedence over `video_url` if both are provided.

**Optional fields:**
- `language` (string) — Language code for the transcript (e.g., `en`, `es`, `fr`). If omitted, the video's default language is used.
- `include_timestamps` (boolean, default: `false`) — When `true`, the saved transcript file includes timestamped segments with start time and duration for each line.
- `include_raw_response` (boolean, default: `false`) — When `true`, the saved transcript file includes the full raw provider response (useful for debugging; may be large).

**Example — Fetch by video URL:**
```json
{
  "action": "fetch",
  "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Example — Fetch by video ID with timestamps in Spanish:**
```json
{
  "action": "fetch",
  "video_id": "dQw4w9WgXcQ",
  "language": "es",
  "include_timestamps": true
}
```

**Example — Fetch with raw response for debugging:**
```json
{
  "action": "fetch",
  "video_id": "dQw4w9WgXcQ",
  "include_raw_response": true
}
```

**Response fields:**
- `video_id` — The resolved video ID.
- `video_title` — Title of the video (when available).
- `language` — The requested language code (or null if default).
- `transcript_file` — Object containing `file_id`, `filename`, `signed_url`, `signed_url_expires_in`, `expiration_date`, `size_bytes`, and `content_type`. Use `signed_url` to download the full transcript JSON.
- `transcript_summary` — Object with `character_count`, `word_count`, and `segment_count`.
- `timestamps_saved` — Whether timestamped segments were included in the file.

#### Common Workflows

1. **Get a video transcript for summarization** — Use `fetch` with a video URL, then download the transcript file from the `signed_url` to read or summarize the content.
2. **Multilingual transcript retrieval** — Set the `language` field to fetch transcripts in a specific language (the video must have that language available).
3. **Detailed analysis with timestamps** — Set `include_timestamps` to `true` to get per-segment timing data, useful for creating subtitles or referencing specific moments.

#### Important Notes
- You must provide either `video_url` or `video_id`. If both are given, `video_id` takes precedence.
- The transcript is returned as a stored JSON file with a signed download URL, not inline in the response. Use the `signed_url` to access the full text.
- Not all YouTube videos have transcripts available. Videos without captions or transcripts will return an error.
- The `signed_url` is temporary and will expire (see `signed_url_expires_in` and `expiration_date` in the response).
- Supported URL formats: standard watch URLs, short youtu.be links, shorts, embeds, and live URLs.

## When To Use
- Use this skill for `Youtube Transcript Fetcher` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: youtube transcript fetcher, generating searchable text from video content, creating video summaries or show notes, building accessibility tools for hearing impaired users, extracting quotes with precise timestamps for citations, fetch, video url, video id.
- Supported action names: `fetch`.

## Use Cases
- Generating searchable text from video content
- creating video summaries or show notes
- building accessibility tools for hearing-impaired users
- extracting quotes with precise timestamps for citations
- analyzing video content for keyword research
- creating training data from educational videos
- building video search indexes across content libraries
- translating video content by extracting source transcripts
- generating subtitles or closed captions in alternate formats
- content repurposing for blogs or articles
- timestamped note-taking for lectures or tutorials
- compliance review of recorded meetings or webinars
- sentiment analysis on video commentary
- creating chapter markers from transcript segments.

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `fetch` (action slug: `fetch`): Fetch the transcript for a YouTube video. Provide either video_url or video_id. The transcript is saved to cloud storage and a signed download URL is returned. Price: `25` credits. Parameters: `include_raw_response`, `include_timestamps`, `language`, `video_id`, `video_url`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "youtube-transcript-fetcher"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "youtube-transcript-fetcher"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "youtube-transcript-fetcher"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "youtube-transcript-fetcher"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "youtube-transcript-fetcher"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "youtube-transcript-fetcher"
  }
}
```

## Call This Tool
Product slug: `youtube-transcript-fetcher`

Marketplace page: https://www.agentpmt.com/marketplace/youtube-transcript-fetcher

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
    "name": "Youtube-Transcript-Fetcher",
    "arguments": {
      "action": "fetch",
      "include_raw_response": false,
      "include_timestamps": false,
      "language": "example language",
      "video_id": "example video id",
      "video_url": "https://example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "youtube-transcript-fetcher",
  "parameters": {
    "action": "fetch",
    "include_raw_response": false,
    "include_timestamps": false,
    "language": "example language",
    "video_id": "example video id",
    "video_url": "https://example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `fetch` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/youtube-transcript-fetcher
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
