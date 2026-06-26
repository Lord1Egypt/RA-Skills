# Discord OAuth Provider

## Overview

Discord uses OAuth 2.0 with authorization code flow. Tokens are **user tokens** (not bot tokens) — they represent a specific Discord user, not a bot application. Tokens expire after approximately 7 days with automatic refresh.

## Key Gotchas

### User Tokens, Not Bot Tokens
TapAuth provides user OAuth tokens. These let you read user info and server lists, but do NOT give bot-level access (no sending messages, managing channels, etc.). For bot functionality, use Discord's Bot API directly.

### Guilds Scope Is Read-Only
The `guilds` scope returns the user's server (guild) list only — names, icons, and IDs. It does NOT grant access to channels, messages, or members within those servers.

### Token Expiry (~7 Days)
Discord access tokens expire after approximately 7 days. TapAuth handles automatic refresh using the refresh token, so subsequent calls to `$(scripts/tapauth.sh --token discord identify)` return a fresh token without user interaction.

### No Granular Permissions
Discord OAuth scopes are coarse — you can't request "read messages in one channel." The scopes control what user data you can read, not what actions you can take in servers.

## Scopes

| Scope | Description |
|-------|-------------|
| `identify` | View username, avatar, banner, discriminator |
| `email` | View the user's email address |
| `guilds` | View the user's server (guild) list |

## Example Usage

```bash
# Get current user info
curl -s -H "Authorization: Bearer $(scripts/tapauth.sh --token discord identify)" \
  https://discord.com/api/v10/users/@me

# Get user's server list
curl -s -H "Authorization: Bearer $(scripts/tapauth.sh --token discord identify,guilds)" \
  https://discord.com/api/v10/users/@me/guilds

# Get user's email (requires email scope)
curl -s -H "Authorization: Bearer $(scripts/tapauth.sh --token discord identify,email)" \
  https://discord.com/api/v10/users/@me
```

## API Base URL

`https://discord.com/api/v10`

## Token Lifetime

~7 days with automatic refresh via TapAuth.
