---
name: x-twitter-automation
description: "X / Twitter Automation: Operate a connected X / Twitter account end-to-end from agents and workflows: compose, publish, search, engage, and DM. Use when an agent needs x / twitter automation, x twitter automation, publish posts and replies to x / twitter from agent workflows, schedule and orchestrate twitter content calendars, search recent x posts for brand monitoring, competitor tracking, create list, list name through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/x-twitter-automation
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/x-twitter-automation"}}
---
# X / Twitter Automation

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
X (Twitter) automation for AI agents and social media teams. Connect your X account once and run your entire publishing, engagement, and social listening workflow from a single MCP-ready API. Post tweets and replies, attach images, GIFs, and video, and search X for brand keywords, mentions, competitors, and trending topics — then draft and send on-brand replies in seconds. Like, repost, follow, and send DMs; build and curate X Lists; and read your mentions, home, and user timelines for reporting. Built for automated tweet scheduling, brand and competitor monitoring, social media customer support, influencer outreach, and end-to-end X / Twitter / X.com content workflows.

## Product Instructions
### X / Twitter Automation

Operate a connected X (Twitter) account end-to-end from agents and workflows: publish posts and replies, upload media, search recent posts, read timelines and DMs, engage, and manage Lists.

#### Common workflows

- On-brand reply queue: `search_posts` for your brand or topic over the last day and review the best candidates. You can only reply to a post you have already engaged with or that tags your account, so engage first (for example `set_like` or `set_repost`) or focus on posts that mention you, then `create_reply` (or `create_reply_with_link`) with on-brand drafts.
- Publish with media: `upload_media` to get `media_ids`, then `create_post` (or `create_post_with_link` when the text has a URL).
- Brand & competitor monitoring: `search_posts` on keywords plus `lookup_timeline` (`mentions`) and curated `lookup_lists`.
- Customer support over DMs: `lookup_dms` to read threads, `send_dm` to respond.

#### Posting links

Use `create_post` / `create_reply` for text without a web link. When the text contains a URL (`http://`, `https://`, `www.`, or a bare domain), use `create_post_with_link` / `create_reply_with_link`.

#### Actions

##### `search_posts`
Required: `query` (string). Optional: `start_time`, `end_time` (RFC3339 timestamps), `max_results` (1-100, default 10), `pagination_token`, `verbosity` (`minimal|standard|expanded`, default `expanded`).
Example: `{"action":"search_posts","query":"agentpmt OR \"AI agents\" -is:retweet lang:en","start_time":"2026-05-22T13:00:00Z","end_time":"2026-05-23T13:00:00Z","max_results":25}`
For List-specific recent search, use the X search operator in `query`, for example `list:2055003862814040388`, plus `start_time` and `end_time`.

##### `lookup_posts`
Required: exactly one of `post_id` (string) or `post_ids` (string[], max 100). Optional: `verbosity`.
Example: `{"action":"lookup_posts","post_ids":["123","456"],"verbosity":"standard"}`

##### `create_post`
Creates a top-level post. Required: `text` or `media_ids`. Optional: `media_ids` (string[], max 4). For text that contains a web link, use `create_post_with_link`.
Example: `{"action":"create_post","text":"Shipping from AgentPMT","media_ids":["123"]}`

##### `create_post_with_link`
Creates a top-level post whose text contains a web link. Required: `text` with a link. Optional: `media_ids` (string[], max 4).
Example: `{"action":"create_post_with_link","text":"Launch notes: https://example.com/agentpmt","media_ids":["123"]}`

##### `create_reply`
Replies to another post. You can only reply to a post the connected account has already engaged with (liked, reposted, quoted, or previously replied to) or that tags your account (mentions or quotes you); replies to any other post are rejected. Required: `reply_to_post_id` and `text` or `media_ids`. Optional: `media_ids` (string[], max 4). For replies whose text contains a web link, use `create_reply_with_link`.
Example: `{"action":"create_reply","reply_to_post_id":"123","text":"Thanks for the mention."}`

##### `create_reply_with_link`
Replies to another post with text that contains a web link. The same reply restriction applies: you can only reply to a post the connected account has already engaged with or that tags your account. Required: `reply_to_post_id` and `text` with a link. Optional: `media_ids` (string[], max 4).
Example: `{"action":"create_reply_with_link","reply_to_post_id":"123","text":"Details are here: https://example.com/agentpmt"}`

##### `delete_post`
Required: `post_id`.
Example: `{"action":"delete_post","post_id":"123"}`

##### `set_reply_hidden`
Required: `reply_post_id`, `hidden` (boolean).
Example: `{"action":"set_reply_hidden","reply_post_id":"123","hidden":true}`

##### `set_like`
Required: `post_id`, `liked` (boolean).
Example: `{"action":"set_like","post_id":"123","liked":true}`

##### `set_repost`
Required: `post_id`, `reposted` (boolean).
Example: `{"action":"set_repost","post_id":"123","reposted":true}`

##### `lookup_post_engagers`
Required: `post_id`, `engagement_type` (`likes|reposts|quotes`). Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_post_engagers","post_id":"123","engagement_type":"likes","max_results":25}`

##### `lookup_users`
Required: `lookup_by` (`ids|usernames|me`). For `ids`, set exactly one of `user_id` or `user_ids`. For `usernames`, set exactly one of `username` or `usernames`. Optional: `verbosity`.
Example: `{"action":"lookup_users","lookup_by":"usernames","usernames":["XDevelopers"]}`

##### `set_follow`
Required: `user_id`, `following` (boolean).
Example: `{"action":"set_follow","user_id":"123","following":true}`

##### `lookup_follows`
Required: `user_id`, `relationship` (`followers|following`). Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_follows","user_id":"123","relationship":"followers","max_results":50}`

##### `lookup_timeline`
Required: `timeline_type` (`user_posts|mentions|home`). `user_id` is required for `user_posts` and `mentions`; optional for `home`. Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_timeline","timeline_type":"home","max_results":20}`

##### `lookup_dms`
Required: `scope` (`all|conversation|participant|event_id`). Set `conversation_id`, `participant_user_id`, or `event_id` for the matching scope. Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_dms","scope":"participant","participant_user_id":"123","max_results":20}`

##### `send_dm`
Required: `target_type` (`participant|conversation|new_group`) and `text` or `media_id`. Set `participant_user_id`, `conversation_id`, or `participant_user_ids` for the matching target.
Example: `{"action":"send_dm","target_type":"participant","participant_user_id":"123","text":"Here is the post: https://x.com/i/status/456"}`

##### `upload_media`
Required: exactly one of `file_id` or `source_url`, plus `media_type` (`image|gif|video`) and `usage_context` (`post|dm`).
Example: `{"action":"upload_media","file_id":"file_abc","media_type":"image","usage_context":"post"}`

##### `create_list`
Creates a new List for the authenticated user. Required: `list_name` (1-25 characters). Optional: `list_description` (max 100 characters), `list_private` (boolean).
Example: `{"action":"create_list","list_name":"Launch Watch","list_description":"Accounts to monitor for launch week","list_private":true}`

##### `update_list`
Updates an existing List. Required: `list_id` and at least one of `list_name`, `list_description`, or `list_private`. Use `list_description:""` to clear the description and `list_private:false` to make the List public.
Example: `{"action":"update_list","list_id":"123","list_name":"Launch Signals","list_private":false}`

##### `delete_list`
Deletes a List owned by the authenticated user. Required: `list_id`.
Example: `{"action":"delete_list","list_id":"123"}`

##### `set_list_membership`
Adds or removes a user from a List owned by the authenticated user. Required: `list_id`, `user_id`, `is_member` (boolean).
Example: `{"action":"set_list_membership","list_id":"123","user_id":"456","is_member":true}`

##### `set_list_follow`
Follows or unfollows a List as the authenticated user. Required: `list_id`, `following` (boolean).
Example: `{"action":"set_list_follow","list_id":"123","following":true}`

##### `set_list_pin`
Pins or unpins a followed or owned List for the authenticated user. Required: `list_id`, `pinned` (boolean).
Example: `{"action":"set_list_pin","list_id":"123","pinned":true}`

##### `lookup_lists`
Looks up one List or Lists by relationship. Required: `list_scope` (`id|owned|memberships|followed|pinned`). For `id`, set `list_id`. For `owned`, `memberships`, or `followed`, `user_id` is optional and defaults to the authenticated user. For `pinned`, omit `user_id`. Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_lists","list_scope":"owned","max_results":25,"verbosity":"standard"}`

##### `lookup_list_contents`
Lists members, followers, or posts for a List. Required: `list_id`, `list_view` (`members|followers|posts`). Optional: `max_results`, `pagination_token`, `verbosity`.
Example: `{"action":"lookup_list_contents","list_id":"123","list_view":"members","max_results":50}`

#### Response

All actions return `action`. List actions also return `data`, optional `includes`, optional `meta`, and `next_token`.

#### Notes

- Search covers recent posts (about the last 7 days). For quote activity on a post, use `lookup_post_engagers` with `engagement_type:"quotes"`.
- **Replies are limited to posts you are already connected to.** You can only post a reply (`create_reply` / `create_reply_with_link`) to a post when the connected account has already engaged with it (liked, reposted, quoted, or previously replied to it) or has been tagged in it (the post mentions or quotes your account). Replies to posts you have not engaged with and that do not tag you are rejected. To reply to a post surfaced by `search_posts`, engage with it first (for example `set_like` or `set_repost`) or choose a post that mentions you. If a reply is still rejected for access or policy reasons, move to another permitted post rather than retrying the same one.
- List read actions need the connected token's `list.read` scope; create, update, delete, membership, follow, and pin actions need `list.write`. If a List call returns a scope-related 403, reconnect the X account to refresh scopes.

## When To Use
- Use this skill for `X / Twitter Automation` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: x / twitter automation, x twitter automation, publish posts and replies to x / twitter from agent workflows, schedule and orchestrate twitter content calendars, search recent x posts for brand monitoring, competitor tracking, create list, list name.
- Supported action names: `create_list`, `create_post`, `create_post_with_link`, `create_reply`, `create_reply_with_link`, `delete_list`, `delete_post`, `lookup_dms`, `lookup_follows`, `lookup_list_contents`, `lookup_lists`, `lookup_post_engagers`, `lookup_posts`, `lookup_timeline`, `lookup_users`, `search_posts`, `send_dm`, `set_follow`, `set_like`, `set_list_follow`, `set_list_membership`, `set_list_pin`, `set_reply_hidden`, `set_repost`, `update_list`, `upload_media`.

## Use Cases
- Publish posts and replies to X / Twitter from agent workflows
- Schedule and orchestrate Twitter content calendars
- Search recent X posts for brand monitoring
- competitor tracking
- and trend detection
- Draft and send on-brand replies to the conversations that matter
- Upload images
- GIFs
- and video to X from File Manager files or any public URL
- Run social media customer support over X DMs
- Send launch announcements and follow-up DMs from automations
- Like
- repost
- and follow as part of engagement automations
- Hide spam or off-topic replies on your own posts
- Build and curate X Lists for launch watch

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `26`.
x402 availability: not enabled for this product.

- `create_list` (action slug: `create-list`): Create a new X List for the authenticated user. Price: `1` credits. Parameters: `list_description`, `list_name`, `list_private`.
- `create_post` (action slug: `create-post`): Create a top-level X post without links. Use create_post_with_link for text containing web links. Quote-post creation is not supported. Price: `5` credits. Parameters: `media_ids`, `text`.
- `create_post_with_link` (action slug: `create-post-with-link`): Create a top-level X post whose text contains at least one web link. Quote-post creation is not supported. Price: `25` credits. Parameters: `media_ids`, `text`.
- `create_reply` (action slug: `create-reply`): Reply to another X post without links. X self-serve plans may restrict replies unless the original author has summoned the authenticated account. Price: `5` credits. Parameters: `media_ids`, `reply_to_post_id`, `text`.
- `create_reply_with_link` (action slug: `create-reply-with-link`): Reply to another X post with text containing at least one web link. X self-serve plans may restrict replies unless the original author has summoned the authenticated account. Price: `25` credits. Parameters: `media_ids`, `reply_to_post_id`, `text`.
- `delete_list` (action slug: `delete-list`): Delete a List owned by the authenticated user. Price: `1` credits. Parameters: `list_id`.
- `delete_post` (action slug: `delete-post`): Delete a post by ID. Price: `5` credits. Parameters: `post_id`.
- `lookup_dms` (action slug: `lookup-dms`): Read DM events by scope: all, conversation, participant, or event_id. Price: `5` credits. Parameters: `conversation_id`, `event_id`, `max_results`, `pagination_token`, `participant_user_id`, `scope`, `verbosity`.
- `lookup_follows` (action slug: `lookup-follows`): List followers or followed users for a user. Price: `5` credits. Parameters: `max_results`, `pagination_token`, `relationship`, `user_id`, `verbosity`.
- `lookup_list_contents` (action slug: `lookup-list-contents`): List members, followers, or posts for a List. Price: `1` credits. Parameters: `list_id`, `list_view`, `max_results`, `pagination_token`, `verbosity`.
- `lookup_lists` (action slug: `lookup-lists`): Look up one List or list owned, membership, followed, or pinned Lists. Price: `1` credits. Parameters: `list_id`, `list_scope`, `max_results`, `pagination_token`, `user_id`, `verbosity`.
- `lookup_post_engagers` (action slug: `lookup-post-engagers`): List users who liked or reposted a post, or list quote posts. Price: `5` credits. Parameters: `engagement_type`, `max_results`, `pagination_token`, `post_id`, `verbosity`.
- `lookup_posts` (action slug: `lookup-posts`): Get one or more X posts by ID with curated field verbosity. Price: `5` credits. Parameters: `post_id`, `post_ids`, `verbosity`.
- `lookup_timeline` (action slug: `lookup-timeline`): Read user posts, mentions, or authenticated home timeline. Price: `5` credits. Parameters: `max_results`, `pagination_token`, `timeline_type`, `user_id`, `verbosity`.
- `lookup_users` (action slug: `lookup-users`): Resolve users by ID, username, or the authenticated account. Price: `5` credits. Parameters: `lookup_by`, `user_id`, `user_ids`, `username`, `usernames`, `verbosity`.
- `search_posts` (action slug: `search-posts`): Search recent X posts from the last 7 days. Price: `5` credits. Parameters: `end_time`, `max_results`, `pagination_token`, `query`, `start_time`, `verbosity`.
- `send_dm` (action slug: `send-dm`): Send a DM to a participant, existing conversation, or new group. Price: `5` credits. Parameters: `conversation_id`, `media_id`, `participant_user_id`, `participant_user_ids`, `target_type`, `text`.
- `set_follow` (action slug: `set-follow`): Follow or unfollow a user as the authenticated user. Price: `5` credits. Parameters: `following`, `user_id`.
- `set_like` (action slug: `set-like`): Like or unlike a post as the authenticated user. Price: `5` credits. Parameters: `liked`, `post_id`.
- `set_list_follow` (action slug: `set-list-follow`): Follow or unfollow a List as the authenticated user. Price: `1` credits. Parameters: `following`, `list_id`.
- `set_list_membership` (action slug: `set-list-membership`): Add or remove a user as a member of a List owned by the authenticated user. Price: `1` credits. Parameters: `is_member`, `list_id`, `user_id`.
- `set_list_pin` (action slug: `set-list-pin`): Pin or unpin a followed or owned List for the authenticated user. Price: `1` credits. Parameters: `list_id`, `pinned`.
- `set_reply_hidden` (action slug: `set-reply-hidden`): Hide or unhide a reply on your post. Price: `5` credits. Parameters: `hidden`, `reply_post_id`.
- `set_repost` (action slug: `set-repost`): Repost or undo repost as the authenticated user. Price: `5` credits. Parameters: `post_id`, `reposted`.
- `update_list` (action slug: `update-list`): Update a List's name, description, or privacy setting. Price: `1` credits. Parameters: `list_description`, `list_id`, `list_name`, `list_private`.
- `upload_media` (action slug: `upload-media`): Upload image, GIF, or video media for posts or DMs and return a media ID. Price: `5` credits. Parameters: `file_id`, `media_type`, `source_url`, `usage_context`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "x-twitter-automation"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "x-twitter-automation"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "x-twitter-automation"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "x-twitter-automation"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "x-twitter-automation"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "x-twitter-automation"
  }
}
```

## Call This Tool
Product slug: `x-twitter-automation`

Marketplace page: https://www.agentpmt.com/marketplace/x-twitter-automation

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
    "name": "X--Twitter-Automation",
    "arguments": {
      "action": "create_list",
      "list_description": "example list description",
      "list_name": "example list name",
      "list_private": true
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "x-twitter-automation",
  "parameters": {
    "action": "create_list",
    "list_description": "example list description",
    "list_name": "example list name",
    "list_private": true
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `create_list` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/x-twitter-automation
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
