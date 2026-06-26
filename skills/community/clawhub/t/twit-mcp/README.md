# twit-mcp

An MCP server that gives AI agents real-time access to X/Twitter data through [twit.sh](https://twit.sh) — powered by [x402](https://x402.org) micropayments. No API keys, no sign-up. Agents pay per request in USDC on Base.

## Tools

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

| Tool | Description |
|------|-------------|
| `connect_twitter` | Connect your Twitter/X account (opens browser) |
| `twitter_account_status` | Check if a Twitter account is connected |
| `disconnect_twitter` | Disconnect and clear stored credentials |

## Requirements

- Node.js 20+
- A wallet with a small amount of USDC on Base Mainnet
- The wallet's private key (used locally to sign payments — never sent anywhere)

> **Use a dedicated wallet with minimal funds. Do not use your main wallet.**

## Setup

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "twit": {
      "command": "npx",
      "args": ["-y", "twit-mcp"],
      "env": {
        "WALLET_PRIVATE_KEY": "0xYourPrivateKeyHere"
      }
    }
  }
}
```

### Claude Code

```bash
claude mcp add twit -e WALLET_PRIVATE_KEY=0xYourPrivateKeyHere -- npx -y twit-mcp
```

### OpenClaw

In OpenClaw chat:

```
/install twit-mcp
```

Then set `WALLET_PRIVATE_KEY` in OpenClaw's environment settings.

### Cursor

Add to your Cursor MCP settings:

```json
{
  "mcpServers": {
    "twit": {
      "command": "npx",
      "args": ["-y", "twit-mcp"],
      "env": {
        "WALLET_PRIVATE_KEY": "0xYourPrivateKeyHere"
      }
    }
  }
}
```

## Posting Tweets

To post or delete tweets, you need to connect your Twitter/X account first:

1. Ask your agent: **"connect my Twitter"** or **"connect my X"**
2. A Chrome window will open at x.com — log in if prompted
3. The agent confirms connection and saves credentials locally
4. Ask the agent to post or delete tweets — no restart needed

Credentials are stored in `~/.twit-mcp-credentials.json` (macOS/Linux) or `C:\Users\<you>\.twit-mcp-credentials.json` (Windows).

## How It Works

1. Your agent calls a tool (e.g. `get_user_tweets`)
2. The MCP server requests the data from `x402.twit.sh`
3. The API responds with `402 Payment Required` and a USDC amount
4. The MCP server signs the payment locally using your private key
5. The API verifies the payment on Base and returns the data
6. Your agent gets the result — all in one round-trip

Your private key never leaves your machine. It is only used locally to sign EIP-712 typed data for x402 payments.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WALLET_PRIVATE_KEY` | Yes | Private key of the wallet that will pay for requests (hex, `0x`-prefixed) |
| `API_BASE` | No | Override the API base URL (default: `https://x402.twit.sh`) |

## Links

- [twit.sh](https://twit.sh) — API reference and pricing
- [x402.org](https://x402.org) — x402 protocol documentation
- [Base](https://base.org) — L2 network used for payments
