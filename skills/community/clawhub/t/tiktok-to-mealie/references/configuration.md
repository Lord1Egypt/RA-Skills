# Configuration

This skill requires a Mealie base URL and API token.

## Recommended setup

Use one of these patterns:

### Option 1: Environment variables
- `MEALIE_BASE_URL`
- `MEALIE_API_TOKEN`

Example:
```bash
export MEALIE_BASE_URL="https://mealie.example.com"
export MEALIE_API_TOKEN="your_token_here"
```

### Option 2: Local secret files
Store secrets in a local private path such as:
- `~/.openclaw/secrets/mealie_base_url`
- `~/.openclaw/secrets/mealie_token`

Example:
```bash
mkdir -p ~/.openclaw/secrets
printf '%s\n' 'https://mealie.example.com' > ~/.openclaw/secrets/mealie_base_url
printf '%s\n' 'your_token_here' > ~/.openclaw/secrets/mealie_token
chmod 600 ~/.openclaw/secrets/mealie_*
```

## Resolution order
When implementing this skill, prefer:
1. environment variables
2. local secret files
3. explicit user-provided config

## What must be configured
- Mealie base URL
- Mealie API token

## What should not be hardcoded
- private hostnames
- local IPs
- user-specific file paths
- personal domain names
- API tokens
