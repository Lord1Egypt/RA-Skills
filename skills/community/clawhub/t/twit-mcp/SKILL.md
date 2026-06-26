---
name: twit-mcp
description: Real-time X/Twitter data and write actions via x402 micropayments. Fetch articles, tweets, users, lists, and communities — post tweets, like, retweet, bookmark, follow — pay per request in USDC on Base. No API keys required.
version: 1.4.1
homepage: https://twit.sh
metadata:
  openclaw:
    requires:
      env: [WALLET_PRIVATE_KEY]
      bins: [npx]
    primaryEnv: WALLET_PRIVATE_KEY
    emoji: 🐦
    install:
      - kind: node
        package: twit-mcp
        bins: [twit-mcp]
---

# twit-mcp

You have access to real-time X/Twitter data and write actions through this MCP server. Each tool call costs $0.0025–$0.01 USDC, paid automatically from the configured wallet on Base. No API key is required.

## Available Tools

### Articles

| Tool | Description | Price |
|------|-------------|-------|
| `get_article_by_id` | Get the full content of an X Article as Markdown by tweet ID. Not in official X API. | $0.01 USDC |

### Tweets

| Tool | Description | Price |
|------|-------------|-------|
| `get_tweet_by_id` | Get a tweet by its ID | $0.0025 USDC |
| `get_user_tweets` | Get a user's recent tweets (paginated) | $0.01 USDC |
| `get_tweet_replies` | Get replies to a tweet (paginated) | $0.01 USDC |
| `get_tweet_quote_tweets` | Get quote tweets for a tweet (paginated) | $0.01 USDC |
| `get_tweet_retweeted_by` | Get users who reposted a tweet (paginated) | $0.01 USDC |
| `search_tweets` | Full-archive tweet search with filters | $0.01 USDC |
| `get_tweets` | Bulk lookup up to 50 tweets by ID | $0.01 USDC |
| `post_tweet` | Post a new tweet as the authenticated user | $0.0025 USDC |
| `delete_tweet` | Delete a tweet owned by the authenticated user | $0.0025 USDC |
| `like_tweet` | Like a tweet as the authenticated user | $0.0075 USDC |
| `unlike_tweet` | Unlike a tweet as the authenticated user | $0.005 USDC |
| `bookmark_tweet` | Bookmark a tweet | $0.0025 USDC |
| `unbookmark_tweet` | Remove a tweet from bookmarks | $0.0025 USDC |
| `retweet` | Repost a tweet as the authenticated user | $0.0075 USDC |
| `unretweet` | Undo a repost | $0.005 USDC |

### Users

| Tool | Description | Price |
|------|-------------|-------|
| `get_user_by_username` | Get a user profile by username | $0.005 USDC |
| `get_user_by_id` | Get a user profile by numeric ID | $0.005 USDC |
| `search_users` | Search users by keyword (paginated) | $0.01 USDC |
| `get_user_followers` | Get a user's followers (paginated) | $0.01 USDC |
| `get_user_following` | Get accounts a user follows (paginated) | $0.01 USDC |
| `get_users` | Bulk lookup up to 50 users by ID | $0.01 USDC |
| `follow_user` | Follow a user as the authenticated user | $0.0075 USDC |
| `unfollow_user` | Unfollow a user as the authenticated user | $0.005 USDC |

### Lists

| Tool | Description | Price |
|------|-------------|-------|
| `get_list_by_id` | Get list details by numeric ID | $0.0025 USDC |
| `get_list_members` | Get members of a list (paginated) | $0.01 USDC |
| `get_list_followers` | Get followers of a list (paginated) | $0.01 USDC |
| `get_list_tweets` | Get latest tweets from a list (paginated) | $0.01 USDC |

### Communities

| Tool | Description | Price |
|------|-------------|-------|
| `get_community_by_id` | Get community details by ID. Not in official X API. | $0.0025 USDC |
| `get_community_posts` | Get latest posts from a community (paginated). Not in official X API. | $0.01 USDC |
| `get_community_members` | Get community members with roles (paginated). Not in official X API. | $0.01 USDC |

### Twitter Auth

Write actions (post, delete, like, bookmark, retweet, follow) require a connected Twitter/X account. Before attempting any write action, call `twitter_account_status` to check if an account is connected.

| Tool | Description |
|------|-------------|
| `connect_twitter` | Connect a Twitter/X account (opens a browser window) |
| `twitter_account_status` | Check if a Twitter account is currently connected |
| `disconnect_twitter` | Disconnect and clear stored credentials |

**Connecting an account:**

1. Call `connect_twitter` — a Chrome window will open at x.com
2. The user logs in if prompted
3. Once confirmed, credentials are saved locally to `~/.twit-mcp-credentials.json`
4. Write actions are available immediately — no restart needed

If a write action is requested and no account is connected, call `connect_twitter` first and wait for confirmation before proceeding.

## How Payments Work

Each tool call makes an HTTP request to `x402.twit.sh`. The server responds with `402 Payment Required`. The MCP server signs a USDC payment locally using the configured `WALLET_PRIVATE_KEY` and retries — all automatically, in one round-trip. The private key never leaves the machine.

## Links

- [twit.sh](https://twit.sh) — API reference and pricing
- [npm: twit-mcp](https://www.npmjs.com/package/twit-mcp)
- [x402.org](https://x402.org) — payment protocol docs
