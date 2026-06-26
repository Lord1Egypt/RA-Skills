# Web3 Daily MCP Server

MCP (Model Context Protocol) server for Web3 Daily - providing real-time Web3 research digest through standardized AI tool interface.

## Features

This MCP server exposes 4 tools:

| Tool | Description |
|------|-------------|
| `get_public_digest` | Get today's Web3 public digest (macro news + KOL sentiment + market data) |
| `get_personalized_digest` | Get personalized digest based on wallet's on-chain behavior |
| `get_wallet_profile` | Analyze wallet's on-chain behavior and investment style |
| `get_market_overview` | Get current BTC/ETH prices and Fear & Greed Index |

## Installation

### For OpenClaw

Add to your `openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "web3-daily": {
        "enabled": true,
        "command": "npx",
        "args": ["web3-daily-mcp"]
      }
    }
  }
}
```

### For Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "web3-daily": {
      "command": "npx",
      "args": ["web3-daily-mcp"]
    }
  }
}
```

### For Cursor

Add to MCP settings:

```json
{
  "web3-daily": {
    "command": "npx",
    "args": ["web3-daily-mcp"]
  }
}
```

## Usage Examples

### Get Public Digest (Chinese)
```
User: 给我今天的 Web3 日报
Agent: [calls get_public_digest with language="zh"]
```

### Get Public Digest (English)
```
User: Give me today's Web3 digest
Agent: [calls get_public_digest with language="en"]
```

### Get Personalized Digest
```
User: My wallet is 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045, give me personalized digest
Agent: [calls get_personalized_digest with wallet_address and language]
```

### Analyze Wallet Profile
```
User: Analyze this wallet: 0x3a4e3c24720a1c11589289da99aa31de3f338bf9
Agent: [calls get_wallet_profile with wallet_address]
```

## Data Sources

The MCP server connects to the J4Y backend which aggregates:
- 170+ news sources (RSS feeds, The Block, CoinDesk, etc.)
- 50+ KOL Twitter accounts (Chinese + English)
- Real-time market data (CoinGecko, Fear & Greed Index)
- On-chain data via DeBank API

## Privacy

- **Public digest**: No personal data required
- **Personalized features**: Wallet address is sent to backend for analysis
- **Data retention**: Wallet profiles cached for 24 hours, then refreshed
- **No permanent storage**: We do not permanently store or sell wallet data

## Development

```bash
# Install dependencies
npm install

# Run in development mode
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## License

MIT
