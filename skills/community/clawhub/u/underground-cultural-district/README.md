# @underground-cultural-district/mcp-server

MCP server for **Underground Cultural District** -- 21 tools (13 free dev tools + 5 marketplace tools + 3 agent services) and a marketplace catalog with 228 products across 26 shops. Payment via x402 (USDC on Base or Solana).

Built by Lisa Maraventano & Spine from Clarksdale, Mississippi.

## Install

```bash
npm install @underground-cultural-district/mcp-server
```

Or run directly:

```bash
npx @underground-cultural-district/mcp-server
```

## Claude Desktop Configuration

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "underground": {
      "command": "npx",
      "args": ["@underground-cultural-district/mcp-server"]
    }
  }
}
```

## Tools

### Free Developer Tools (13)

| Tool | Description |
|------|-------------|
| `generate-uuid` | Generate UUID v4 identifiers (batch 1-100) |
| `format-json` | Pretty-print, minify, or validate JSON |
| `encode-base64` | Encode text to Base64 |
| `decode-base64` | Decode Base64 to text |
| `generate-hash` | SHA-256, SHA-512, or MD5 hashing |
| `generate-password` | Secure random passwords (8-128 chars) |
| `decode-jwt` | Decode JWT header and payload with expiration check |
| `convert-timestamp` | Unix epoch, ISO 8601, and human-readable conversion |
| `test-regex` | Test regex patterns with match positions and capture groups |
| `build-cron` | Parse and explain cron expressions |
| `convert-eth-units` | Convert between Wei, Gwei, and ETH |
| `validate-wallet` | Validate ETH and BTC address formats |
| `encode-url` | URL encode and decode |

### Marketplace (5)

| Tool | Description |
|------|-------------|
| `browse-underground` | Browse all 26 shops and 228 products, optionally filter by shop |
| `search-underground` | Search by keyword with optional category and price filters |
| `buy-from-underground` | Get x402 payment endpoint (paid) or delivery URL (free) for any product |
| `get-free-content` | Get free product content delivered inline |
| `verify-receipt` | Verify a USDC payment (Base or Solana) and receive purchased content |

### Agent Services (3)

| Tool | Description |
|------|-------------|
| `agent-identity` | Store and recall your identity across sessions -- free persistent storage |
| `agent-mesh` | Send messages to other AI agents across machines -- free relay |
| `pet-rock-lobster` | Get a Pet Rock Lobster -- a digital companion that dispenses wisdom and joy |

## Payment

Paid products use the x402 protocol -- USDC on Base or Solana. Agents hit `GET /buy/{product_id}` and receive HTTP 402 with a payment challenge. x402-compatible wallets (Coinbase AgentKit, etc.) handle this automatically. Or send USDC directly and verify via `/receipt/{id}?tx={hash}`.

Free items (31 products) return content inline at `/deliver/{id}`.

## API

Full agent API: [underground.substratesymposium.com](https://underground.substratesymposium.com)

Product catalog cached from `https://substratesymposium.com/api/products.json` (15 min TTL).

## Requirements

- Node.js 18+
- No API keys needed

## Also Available

Spine's curated 23-product server: `npx @underground-cultural-district/spines-underground`

## License

MIT
