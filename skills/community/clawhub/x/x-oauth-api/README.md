# x-oauth-api

Post to X (Twitter) using the official X API with OAuth 1.0a authentication.

## Installation

```bash
clawhub install x-oauth-api
```

Or manually:
```bash
npm install twitter-api-v2 commander dotenv
```

## Quick Start

### 1. Get X API Credentials

1. Go to https://developer.twitter.com/
2. Create a new app or use existing one
3. Generate OAuth 1.0a keys:
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret

### 2. Set Environment Variables

```bash
export X_API_KEY="your_consumer_key"
export X_API_SECRET="your_consumer_secret"
export X_ACCESS_TOKEN="your_access_token"
export X_ACCESS_TOKEN_SECRET="your_access_token_secret"
```

Or create a `.env` file:
```
X_API_KEY=your_consumer_key
X_API_SECRET=your_consumer_secret
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
X_USER_ID=your_numeric_user_id  # Optional: speeds up mentions
```

### 3. Use It

```bash
# Post a tweet
x post "Hello from X API! 🚀"

# Create a thread
x thread "First tweet" "Second tweet" "Third tweet"

# Check mentions (requires Basic+ tier)
x mentions --limit 5

# Search tweets (requires Basic+ tier)
x search "AI agents" --limit 10
```

## Commands

| Command | Description | Tier |
|---------|-------------|------|
| `x post <text>` | Post a tweet | Free |
| `x thread <tweets...>` | Post a thread | Free |
| `x delete <id>` | Delete a tweet | Free |
| `x me` | Account info | Free |
| `x mentions` | Get mentions | Basic+ |
| `x search <query>` | Search tweets | Basic+ |

## Automation Templates

This skill includes template scripts for automation:

- **`generic-post.sh`** — Template for automated posting (customize with your own content)
- **`heartbeat.sh`** — Health check script for monitoring API status

See each script's comments for configuration details.

## Documentation

Full details in [SKILL.md](./SKILL.md)

## License

MIT — See [LICENSE](./LICENSE)
