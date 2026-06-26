---
name: roblox-cli
description: Manage Roblox game passes and developer products via Open Cloud API.
metadata: {"clawdbot":{"requires":{"env":["ROBLOX_API_KEY"]},"primaryEnv":"ROBLOX_API_KEY","emoji":"🎮","homepage":"https://create.roblox.com/docs/cloud","source":"https://github.com/ingalls-ltd/RobloxCliSkillOpenClaw"}}
---

# Roblox CLI

Manage Roblox game passes and developer products via the Open Cloud API.

## Features

- List games owned by your API key
- Manage game passes (list, get, create, update)
- Manage developer products (list, get, create, update)
- JSON output for easy parsing
- Automatic pagination
- Rate limit handling with exponential backoff

## Setup

1. Create a Roblox API key in [Creator Hub](https://create.roblox.com/dashboard/credentials)
   - If you land on the OAuth 2.0 Apps page, click "All Tools" then "API Keys"
2. Add the required access permissions:
   - `game-pass:read` and `game-pass:write` for game passes
   - `developer-product:read` and `developer-product:write` for products
3. Optionally restrict access to specific experiences
4. Set the `ROBLOX_API_KEY` environment variable

## Usage

The skill is invoked via:
```bash
npx -y bun ${SKILL_DIR}/scripts/cli.ts [command] [subcommand] [args] [options]
```

### Commands

**Games**
```bash
# List all games owned by API key holder
npx -y bun ${SKILL_DIR}/scripts/cli.ts games list
```

**Game Passes**
```bash
# List all game passes for a universe
npx -y bun ${SKILL_DIR}/scripts/cli.ts passes list <universeId>

# Get specific game pass details
npx -y bun ${SKILL_DIR}/scripts/cli.ts passes get <universeId> <passId>

# Create new game pass
npx -y bun ${SKILL_DIR}/scripts/cli.ts passes create <universeId> --name "VIP Pass" --price 100 --for-sale true

# Update game pass
npx -y bun ${SKILL_DIR}/scripts/cli.ts passes update <universeId> <passId> --price 50
```

**Developer Products**
```bash
# List all developer products for a universe
npx -y bun ${SKILL_DIR}/scripts/cli.ts products list <universeId>

# Get specific product details
npx -y bun ${SKILL_DIR}/scripts/cli.ts products get <universeId> <productId>

# Create new product
npx -y bun ${SKILL_DIR}/scripts/cli.ts products create <universeId> --name "Gold Coins" --price 25 --for-sale true

# Update product
npx -y bun ${SKILL_DIR}/scripts/cli.ts products update <universeId> <productId> --price 30
```

## Options

**Create/Update Flags:**
- `--name <name>` - Name of the pass/product (required for create)
- `--description <desc>` - Description text (optional)
- `--price <robux>` - Price in Robux (required for create)
- `--for-sale <true|false>` - Whether item is for sale (default: true)

## Output Format

All commands return JSON:

**Success:**
```json
{
  "success": true,
  "data": [...]
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

**Error Codes:**
- `MISSING_API_KEY` - ROBLOX_API_KEY environment variable not set
- `INVALID_API_KEY` - API key could not be parsed
- `INVALID_ARGS` - Missing required arguments or invalid flag values
- `NOT_FOUND` - Requested resource not found
- `API_ERROR` - Roblox API returned an error
- `RATE_LIMITED` - Max retries exceeded on 429 responses
- `NETWORK_ERROR` - Network request failed

## Environment Variables

- `ROBLOX_API_KEY` (required) - Your Roblox Open Cloud API key from Creator Hub

## API Permissions

Your API key must have the following permissions:

| Feature | Required Permission |
|---------|---------------------|
| Game Passes - Read | `game-pass:read` |
| Game Passes - Write | `game-pass:write` |
| Developer Products - Read | `developer-product:read` |
| Developer Products - Write | `developer-product:write` |

## Notes

- Game passes automatically get a placeholder icon (150x150 green PNG)
- All list commands fetch all pages automatically
- Rate limiting is handled with exponential backoff (max 3 retries)
- Delete operations are not supported (Roblox API limitation)
- To disable an item, use `--for-sale false` in update command

## Testing

Run unit tests:
```bash
bun test skills/roblox-cli/scripts/__tests__
```

## References

- [Roblox Open Cloud API Documentation](https://create.roblox.com/docs/cloud)
- [Game Passes API](https://create.roblox.com/docs/cloud/reference/features/game-passes)
- [Developer Products API](https://create.roblox.com/docs/cloud/reference/features/developer-products)
- [API Keys Guide](https://create.roblox.com/docs/cloud/auth/api-keys)
