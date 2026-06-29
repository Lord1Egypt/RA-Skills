---
name: youtube-comment-manager
description: "YouTube Comment Manager: List YouTube comment threads on any video or across a. Use when an agent needs youtube comment manager, triage the held for review and likely spam queues and ban repeat offenders, reply to high signal questions on a launch or tutorial video, bulk moderate comments awaiting review across an entire channel, search a channel's comments for brand mentions or specific keywords, create top level comment, channel id, video id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/youtube-comment-manager
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/youtube-comment-manager"}}
---
# YouTube Comment Manager

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Take control of every conversation happening on your YouTube channel. Triage the spam queue, ban repeat offenders, hold borderline comments for review, and reply to genuine fans without ever opening YouTube Studio. Pull comment threads by video, channel, or moderation status; search across all your comments for keywords; edit or delete your own posts; and moderate flagged comments in bulk. Whether you're a solo creator drowning in crypto bots after a viral upload, a community manager running comment moderation across a brand's channel, or an agent automating audience engagement at scale, this tool turns hours of comment triage into minutes of confident action — keeping your discussion section clean, your viewers engaged, and your channel's reputation protected.

## Product Instructions
### YouTube Comment Manager

Read, write, update, delete, and moderate YouTube comments and replies on the connected channel using the viewer's Google OAuth token.

#### Required Connection

All actions except `get_instructions` require a connected Google account with YouTube scopes (`youtube.force-ssl`). The OAuth token is injected automatically by AgentPMT — do not pass `google_oauth` in your tool call.

#### Actions

##### `list_comment_threads`
List top-level comment threads. Provide **exactly one** of `video_id`, `channel_id`, or `thread_ids`.

Required (one of):
- `video_id` (string) — fetch threads on a single video
- `channel_id` (string) — fetch all threads across the channel's videos
- `thread_ids` (array of strings) — fetch specific threads by ID

Optional:
- `include_replies` (bool, default false) — embed reply comments in each thread
- `text_format` (`plainText` | `html`, default `plainText`)
- `moderation_status` (`heldForReview` | `likelySpam` | `published`, default `published`) — filter threads by moderation state on a video or channel you own/moderate. Use with `video_id` or `channel_id` (not with `thread_ids`); the held-for-review and likely-spam queues are only visible to the channel owner.
- `order` (`time` | `relevance`, default `time`)
- `search_terms` (string) — server-side text filter
- `max_results` (1-100, default 25)
- `page_token` (string) — from a prior response's `nextPageToken`

```json
{"action":"list_comment_threads","video_id":"dQw4w9WgXcQ","include_replies":true,"order":"relevance","max_results":50}
```

```json
{"action":"list_comment_threads","channel_id":"UCxxxxxxxxxxxxxxxxxxxxxx","moderation_status":"heldForReview","max_results":100}
```

##### `get_comment_threads`
Fetch specific threads by ID. Use this after `list_comment_threads` to get richer payloads or refresh state.

Required:
- `thread_ids` (array of strings)

Optional:
- `include_replies` (bool)
- `text_format` (`plainText` | `html`)

```json
{"action":"get_comment_threads","thread_ids":["UgxAbc123","UgxDef456"],"include_replies":true}
```

##### `create_top_level_comment`
Post a new top-level comment on a video as the connected account.

Required:
- `channel_id` (string) — the **viewer's** channel posting the comment, not the video owner's
- `video_id` (string)
- `text` (string, max 10000 chars)

```json
{"action":"create_top_level_comment","channel_id":"UCviewerChannel","video_id":"dQw4w9WgXcQ","text":"Great breakdown — the part on cohort retention was especially useful."}
```

##### `list_replies`
List reply comments under a top-level comment.

Required:
- `parent_comment_id` (string) — the top-level comment ID

Optional:
- `text_format` (`plainText` | `html`)
- `max_results` (1-100, default 25)
- `page_token` (string)

```json
{"action":"list_replies","parent_comment_id":"UgxParent123","max_results":50}
```

##### `reply_to_comment`
Reply to an existing top-level comment.

Required:
- `parent_comment_id` (string)
- `text` (string, max 10000 chars)

```json
{"action":"reply_to_comment","parent_comment_id":"UgxParent123","text":"Thanks for the question! The repo link is in the description, and I walk through the setup in the pinned comment."}
```

##### `get_comments`
Fetch comments by ID. Useful for resolving the `text` of a reply or the snippet of a parent.

Required:
- `comment_ids` (array of strings)

Optional:
- `text_format` (`plainText` | `html`)

```json
{"action":"get_comments","comment_ids":["UgxComment1","UgxComment2"]}
```

##### `update_comment`
Edit text on a comment owned by the connected account. You cannot edit other authors' comments.

Required:
- `comment_id` (string)
- `text` (string, max 10000 chars)

```json
{"action":"update_comment","comment_id":"UgxOwnedComment","text":"Edit: fixed the timestamp I referenced — the asyncio section starts at 12:04, not 10:40."}
```

##### `delete_comment`
Permanently delete a comment owned by the connected account.

Required:
- `comment_id` (string)

```json
{"action":"delete_comment","comment_id":"UgxOwnedComment"}
```

##### `moderate_comments`
Set moderation status for one or more comments on videos the connected account owns. Channel owners only.

Required:
- `comment_ids` (array of strings)
- `moderation_status` (`heldForReview` | `published` | `rejected`)

Optional:
- `ban_author` (bool, default false) — only valid with `moderation_status: "rejected"`. Bans the author from commenting on the channel going forward.

```json
{"action":"moderate_comments","comment_ids":["UgxSpam1","UgxSpam2"],"moderation_status":"rejected","ban_author":true}
```

```json
{"action":"moderate_comments","comment_ids":["UgxHeld1"],"moderation_status":"published"}
```

#### Common Patterns

**Triage spam queue:**
1. `list_comment_threads` with `channel_id` and `moderation_status: "likelySpam"` to surface flagged threads
2. Inspect `text` and author; for legitimate comments call `moderate_comments` with `moderation_status: "published"`; for confirmed spam call `moderate_comments` with `moderation_status: "rejected"` and optionally `ban_author: true`

**Engage on a launch video:**
1. `list_comment_threads` with `video_id`, `order: "relevance"`, `include_replies: true`
2. For each high-signal thread, call `reply_to_comment` with `parent_comment_id` and the response text

**Audit owned comments:**
1. `list_comment_threads` filtered by `search_terms` matching your past content
2. `update_comment` to correct, or `delete_comment` to remove

#### Pagination

`list_comment_threads` and `list_replies` return `nextPageToken` in the response when more results exist. Pass that value back as `page_token` to fetch the next page. Stop when `nextPageToken` is absent.

#### Response Shape

All responses wrap the YouTube Data API v3 payload:

```json
{"action":"list_comment_threads","response":{"kind":"youtube#commentThreadListResponse","items":[...],"nextPageToken":"..."}}
```

Write actions return the created/updated resource:

```json
{"action":"reply_to_comment","comment":{"id":"UgxNewReply","snippet":{"textDisplay":"...","authorDisplayName":"..."}}}
```

`delete_comment` and `moderate_comments` return `{"deleted": true}` or `{"updated": true}` because the YouTube API returns 204 No Content on success.

#### Permission Notes

- **Read** actions work on any public video.
- **Write** actions (`create_top_level_comment`, `reply_to_comment`) require the video to allow comments and the account to not be blocked.
- **Edit/Delete** actions only work on comments authored by the connected account.
- **Moderation** actions only work on videos owned by the connected channel. `moderate_comments` on a video you don't own returns 403.
- `ban_author` is irreversible from this tool — banned authors must be unbanned through YouTube Studio.

#### Scope

This tool covers comments, threads, and moderation only. Use **YouTube Channel Management** for video uploads, thumbnails, captions, playlists, channel sections, and watermarks.

## When To Use
- Use this skill for `YouTube Comment Manager` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: youtube comment manager, triage the held for review and likely spam queues and ban repeat offenders, reply to high signal questions on a launch or tutorial video, bulk moderate comments awaiting review across an entire channel, search a channel's comments for brand mentions or specific keywords, create top level comment, channel id, video id.
- Supported action names: `create_top_level_comment`, `delete_comment`, `get_comment_threads`, `get_comments`, `list_comment_threads`, `list_replies`, `moderate_comments`, `reply_to_comment`, `update_comment`.

## Use Cases
- Triage the held-for-review and likely-spam queues and ban repeat offenders
- Reply to high-signal questions on a launch or tutorial video
- Bulk-moderate comments awaiting review across an entire channel
- Search a channel's comments for brand mentions or specific keywords
- Edit or delete your own outdated comments and replies
- Surface relevance-ranked threads for community managers
- Reject crypto-spam and giveaway-scam comments and ban the accounts in one pass
- Engage authentically with fans during launches
- AMAs
- and product reveals
- Audit comment activity on a video before promoting it

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `9`.
x402 availability: not enabled for this product.

- `create_top_level_comment` (action slug: `create-top-level-comment`): Create a top-level comment on a video. Price: `5` credits. Parameters: `channel_id`, `text`, `video_id`.
- `delete_comment` (action slug: `delete-comment`): Delete a comment by ID. Price: `5` credits. Parameters: `comment_id`.
- `get_comment_threads` (action slug: `get-comment-threads`): Fetch specific YouTube comment threads by ID. Price: `5` credits. Parameters: `include_replies`, `text_format`, `thread_ids`.
- `get_comments` (action slug: `get-comments`): Fetch specific comments by ID. Price: `5` credits. Parameters: `comment_ids`, `text_format`.
- `list_comment_threads` (action slug: `list-comment-threads`): List YouTube comment threads by exactly one filter: video_id, channel_id, or thread_ids. Price: `5` credits. Parameters: `channel_id`, `include_replies`, `max_results`, `moderation_status`, `order`, `page_token`, `search_terms`, `text_format`, plus 2 more.
- `list_replies` (action slug: `list-replies`): List replies to a top-level comment. Price: `5` credits. Parameters: `max_results`, `page_token`, `parent_comment_id`, `text_format`.
- `moderate_comments` (action slug: `moderate-comments`): Set moderation status for one or more comments. Price: `5` credits. Parameters: `ban_author`, `comment_ids`, `moderation_status`.
- `reply_to_comment` (action slug: `reply-to-comment`): Reply to a top-level comment. Price: `5` credits. Parameters: `parent_comment_id`, `text`.
- `update_comment` (action slug: `update-comment`): Update an existing comment's text. Price: `5` credits. Parameters: `comment_id`, `text`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "youtube-comment-manager"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "youtube-comment-manager"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "youtube-comment-manager"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "youtube-comment-manager"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "youtube-comment-manager"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "youtube-comment-manager"
  }
}
```

## Call This Tool
Product slug: `youtube-comment-manager`

Marketplace page: https://www.agentpmt.com/marketplace/youtube-comment-manager

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
    "name": "YouTube-Comment-Manager",
    "arguments": {
      "action": "create_top_level_comment",
      "channel_id": "example channel id",
      "text": "example text",
      "video_id": "example video id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "youtube-comment-manager",
  "parameters": {
    "action": "create_top_level_comment",
    "channel_id": "example channel id",
    "text": "example text",
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
- If `create_top_level_comment` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/youtube-comment-manager
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
