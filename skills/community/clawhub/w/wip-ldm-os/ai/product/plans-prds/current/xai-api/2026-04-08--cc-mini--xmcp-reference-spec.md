# Plan: Expand wip-x-xai-grok with xmcp Reference

**Date:** 2026-04-08
**Author:** cc-mini (with Parker)
**Status:** plan
**Repo:** `wip-x-xai-grok-private`
**Reference:** https://github.com/xdevplatform/xmcp (X's official MCP server, 648 stars)

## Context

X published an official MCP server (`xmcp`) with 150+ tools covering the full X API v2 surface. It's Python, uses OAuth browser flow, and doesn't include Grok. We use it as a reference, not a dependency.

Our `wip-x-xai-grok-private` currently has 16 tools. The xmcp reference shows us what's available and how the endpoints work. We bring in the tools we need, in our stack (Node/JS), with our auth (1Password helper).

## What xmcp Has That We Don't

### High Priority (bring in next)

| xmcp Tool | What it does | Why we need it |
|---|---|---|
| `getPostsById` | Get tweet by ID with full fields | We have `fetch_post` but limited fields |
| `getUsersByUsername` | Lookup user by @handle | Needed for "who is @handle" queries |
| `searchPostsAll` | Full archive search (Academic) | Our `raw_x_search` only does recent |
| `getPostsAnalytics` | Engagement metrics | "How did this post perform?" |
| `createPosts` with media | Post with images/video attached | Our `post_tweet` + `upload_media` are separate |
| `repostPost` | Retweet | Basic social action |
| `likePost` / `unlikePost` | Like/unlike | Basic social action |

### Medium Priority (bring in later)

| xmcp Tool | What it does |
|---|---|
| `createDirectMessagesConversation` | Start a DM |
| `createDirectMessagesByConversationId` | Send DM in existing thread |
| `getDirectMessagesEvents` | Read DMs |
| `getUsersFollowers` / `getUsersFollowing` | Social graph |
| `createLists` / `addListsMember` | List management |
| `getMediaAnalytics` | Media performance |
| `getTrends` | Trending topics |

### Low Priority (future)

| xmcp Tool | What it does |
|---|---|
| `followList` / `unfollowList` | List follows |
| `muteUser` / `blockUser` | Moderation |
| Community notes tools | Community notes |
| Compliance tools | Enterprise |

## What We Have That xmcp Doesn't

| Our tool | What it does |
|---|---|
| `search_web` | Grok web search |
| `search_x` | Grok AI-synthesized X search (semantic, keyword, user, thread modes) |
| `generate_image` | Grok Imagine |
| `edit_image` | Grok image editing |
| `generate_video` | Grok video gen |
| `poll_video` | Video status polling |
| 1Password auth | Headless secret access via JS SDK |

## Implementation Plan

### Phase 1: Expand X Platform Tools (high priority)

Add to `core/x-platform.mjs`:

```javascript
// New exports
export async function get_post_analytics(postId) { ... }
export async function get_user_by_username(username) { ... }
export async function search_posts_all(query, opts) { ... }  // full archive
export async function repost(postId) { ... }
export async function like_post(postId) { ... }
export async function unlike_post(postId) { ... }
export async function create_post_with_media(text, mediaIds) { ... }
```

Register in `mcp-server.mjs` as new MCP tools.

### Phase 2: Expand Read Tools (medium priority)

```javascript
export async function get_followers(userId, opts) { ... }
export async function get_following(userId, opts) { ... }
export async function send_dm(conversationId, text) { ... }
export async function get_dms(conversationId) { ... }
export async function get_trends(woeid) { ... }
```

### Phase 3: List Management + Moderation (low priority)

Only build when needed.

## Architecture Notes

- All new tools follow the same pattern as existing ones in `core/x-platform.mjs`
- Auth via `@wipcomputer/wip-1password/helper` (opRead)
- X API v2 base URL: `https://api.x.com/2/`
- Use `@xdevplatform/xdk` where it has typed helpers
- Fall back to raw fetch for endpoints xdk doesn't cover
- xmcp fetches the OpenAPI spec at startup (`api.twitter.com/2/openapi.json`). We could do the same for auto-discovery, but manual is cleaner for our tool count.

## xmcp Reference Files

Clone for reference (do NOT run or depend on):
```bash
gh repo clone xdevplatform/xmcp ~/wipcomputerinc/repos/third-party-repos/xmcp
```

Key files to study:
- `server.py` ... tool generation from OpenAPI spec
- `tools/` ... individual tool implementations
- `auth/` ... OAuth flow (we don't use this, we use 1Password)

## Testing Plan

1. Generate new xAI key at console.x.ai, store in 1Password
2. Test `search_x` and `search_web` via the MCP server
3. Test `fetch_post` with a real tweet URL
4. Test `post_tweet` (post to @wipcomputer test account)
5. Add high priority tools, test each
6. Verify 1Password helper resolves both keys correctly

## Cross-references

- `repos/ldm-os/apis/wip-x-xai-grok-private/` ... our combined repo
- `ai/product/plans-prds/1password/2026-04-08--cc-mini--1password-as-single-source.md` ... 1Password helper plan
- `repos/ldm-os/apis/wip-x-xai-grok-private/ai/product/plans-prds/current/2026-03-24--cc-mini--combine-x-xai-repos.md` ... original combine plan
