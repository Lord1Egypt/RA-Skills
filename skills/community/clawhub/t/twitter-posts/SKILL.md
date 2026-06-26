---
name: twitter-posts
description: Draft, publish, and manage posts on X (Twitter), inspect timelines, manage profiles, and automate social media workflows via the X API. Use this skill when users want to post tweets, review timelines, search posts, or manage X/Twitter workflows.
---

# X (Twitter)

![X (Twitter)](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/twitter-dark.svg)

Manage X (Twitter) — draft and publish posts, inspect timelines, search content, manage profiles, and automate social media workflows via the X API.

This skill uses [ClawLink](https://claw-link.dev) for hosted connection flows and credentials so you do not need to configure X API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect X (Twitter) |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect X |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    X API         │
│   (User Chat)   │     │   (OAuth)    │     │                  │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                       │                       │
         │  1. Install Plugin    │                       │
         │  2. Pair Device       │                       │
         │  3. Connect X         │                       │
         │                       │  4. Secure Token       │
         │                       │  5. Proxy Requests    │
         │                       │                       │
         ▼                       ▼                       ▼
   ┌──────────┐           ┌──────────┐           ┌──────────┐
   │  SKILL   │           │ Dashboard│           │    X     │
   │  File    │           │ Auth     │           │ Account  │
   └──────────┘           └──────────┘           └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for X (Twitter) again."

## Quick Start

```bash
# Get user profile
clawlink_call_tool --tool "twitter_get_user" --params '{"username": "username"}'

# Post a tweet
clawlink_call_tool --tool "twitter_create_tweet" --params '{"text": "Hello from OpenClaw!"}'

# search tweets
clawlink_call_tool --tool "twitter_search_tweets" --params '{"query": "openclaw"}'
```

## Authentication

All X tool calls are authenticated automatically by ClawLink using the user's connected X account OAuth token.

**No API token is required in chat.** ClawLink stores the OAuth token securely and injects it into every X API request on the user's behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=twitter and connect X.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `twitter` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration twitter
```

**Response:** Returns the live tool catalog for X.

### Reconnect

If X tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=twitter
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration twitter`

## Security & Permissions

- Access is scoped to the X account connected during OAuth setup and the permissions granted.
- **All write operations (post tweet, delete, retweet, like, follow) require explicit user confirmation.**
- Posts are public-facing by default — always confirm the content before posting.
- Account deletion or suspension-related operations are high-impact and must be confirmed.
- Rate limits apply to many endpoints — honor backoff guidance.

## Tool Reference

### Tweets (Posts)

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_list_tweets` | List tweets from a user's timeline | Read |
| `twitter_get_tweet` | Get a specific tweet's details | Read |
| `twitter_create_tweet` | Post a new tweet | Write |
| `twitter_delete_tweet` | Delete a tweet | Write |
| `twitter_update_tweet` | Update a tweet's text | Write |
| `twitter_retweet` | Retweet an existing tweet | Write |
| `twitter_unretweet` | Remove a retweet | Write |
| `twitter_like_tweet` | Like a tweet | Write |
| `twitter_unlike_tweet` | Remove a like from a tweet | Write |

### Timelines

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_get_home_timeline` | Get tweets from the home timeline | Read |
| `twitter_get_user_timeline` | Get tweets from a specific user's timeline | Read |
| `twitter_get_mentions_timeline` | Get tweets mentioning the authenticated user | Read |

### Search

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_search_tweets` | Search for tweets matching a query | Read |
| `twitter_search_users` | Search for users matching a query | Read |

### Users & Profiles

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_get_user` | Get a user's profile information | Read |
| `twitter_list_followers` | List followers of a user | Read |
| `twitter_list_following` | List accounts a user follows | Read |
| `twitter_follow_user` | Follow a user | Write |
| `twitter_unfollow_user` | Unfollow a user | Write |
| `twitter_block_user` | Block a user | Write |
| `twitter_unblock_user` | Unblock a user | Write |
| `twitter_mute_user` | Mute a user | Write |
| `twitter_unmute_user` | Unmute a user | Write |

### Bookmarks

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_list_bookmarks` | List the authenticated user's bookmarks | Read |
| `twitter_add_bookmark` | Add a tweet to bookmarks | Write |
| `twitter_remove_bookmark` | Remove a tweet from bookmarks | Write |

### Lists

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_list_list_memberships` | List lists a user is a member of | Read |
| `twitter_list_list_subscribers` | List subscribers to a list | Read |
| `twitter_list_list_tweets` | Get tweets from a specific list | Read |

### Direct Messages

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_list_direct_messages` | List direct messages | Read |
| `twitter_send_direct_message` | Send a direct message | Write |

### Media

| Tool | Description | Mode |
|------|-------------|------|
| `twitter_upload_media` | Upload an image or video to attach to a tweet | Write |
| `twitter_create_tweet_with_media` | Post a tweet with attached media | Write |

## Code Examples

### Post a tweet

```bash
clawlink_call_tool --tool "twitter_create_tweet" \
  --params '{
    "text": "Excited to announce our new integration! Check it out at https://example.com"
  }'
```

### Get a user profile

```bash
clawlink_call_tool --tool "twitter_get_user" \
  --params '{
    "username": "elonmusk"
  }'
```

### Search for tweets

```bash
clawlink_call_tool --tool "twitter_search_tweets" \
  --params '{
    "query": "openclaw ai assistant",
    "max_results": 10
  }'
```

### Retweet a post

```bash
clawlink_call_tool --tool "twitter_retweet" \
  --params '{
    "tweet_id": "TWEET_ID"
  }'
```

### Follow a user

```bash
clawlink_call_tool --tool "twitter_follow_user" \
  --params '{
    "username": "example_user"
  }'
```

### Upload media and post

```bash
clawlink_call_tool --tool "twitter_create_tweet_with_media" \
  --params '{
    "text": "Check out this screenshot!",
    "media_ids": ["MEDIA_ID"]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm X is connected.
2. Call `clawlink_list_tools --integration twitter` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `twitter`.
5. If no X tools appear, direct the user to https://claw-link.dev/dashboard?add=twitter.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → search → describe                            │
│                                                             │
│  Example: Get user → List tweets → Show profile            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Preview tweet → User approves → Post tweet        │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, get, and search operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- Tweet IDs are numeric and very large — handle them as strings to avoid precision loss.
- Rate limits vary by endpoint and account type — Basic/Free accounts have stricter limits.
- Media uploads must complete before being attached to a tweet — use the returned media ID.
- Deleted tweets cannot be recovered.
- Direct messages have separate rate limits and scope restrictions.
- X API v2 is used — some v1 endpoints may not be available.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration twitter`. |
| Missing connection | X is not connected. Direct the user to https://claw-link.dev/dashboard?add=twitter. |
| `Tweet not found` | The tweet ID does not exist or has been deleted. |
| `User not found` | The username does not match any account. |
| `Unauthorized` | The OAuth token lacks permission for this operation. |
| `Duplicate` | The tweet text is identical to a recent tweet (spam protection). |
| `Rate limit exceeded` | Too many requests. Wait and retry with backoff. |
| `Media upload failed` | The file format is unsupported or exceeds size limits. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Post Fails

1. Verify the account has posting permissions — some enterprise accounts restrict API posting.
2. Check for duplicate content — X prevents posting identical tweets in quick succession.
3. Confirm media formats and sizes are within X's limits.
4. Check rate limits — free accounts have significantly reduced posting limits.

## Resources

- [X API Documentation](https://developer.x.com/en/docs)
- [X API Reference](https://developer.x.com/en/docs/api-reference)
- [X Developer Portal](https://developer.x.com/en/docs)
- ClawLink: https://claw-link.dev
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

---

**Powered by [ClawLink](https://claw-link.dev)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)