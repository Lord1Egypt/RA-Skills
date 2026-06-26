---
name: web3-daily-mcp
type: mcp
description: >-
  MCP Server for Web3 Daily - Real-time Web3 research digest with macro news, 
  KOL sentiment, market data, and personalized wallet analysis. This is an MCP 
  server that provides tools for AI agents to fetch real data from the J4Y backend.
runtime: node
command: node
args: ["dist/index.js"]
---

# Web3 Daily MCP Server

> **This is an MCP Server** - It provides tools that AI agents can call to fetch real-time Web3 data.

## Available Tools

### 1. `get_public_digest`
Get today's Web3 public digest with macro news, KOL sentiment, and market data.

**Parameters:**
- `language` (optional): "zh" (Chinese, default) or "en" (English)

**Example:**
```
User: 给我今天的 Web3 日报
Agent: [calls get_public_digest(language="zh")]
```

### 2. `get_personalized_digest`
Get personalized Web3 digest based on wallet's on-chain behavior.

**Parameters:**
- `wallet_address` (required): EVM wallet address (0x + 40 hex characters)
- `language` (optional): "zh" or "en"

**Example:**
```
User: My wallet is 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
Agent: [calls get_personalized_digest(wallet_address="0x...", language="en")]
```

### 3. `get_wallet_profile`
Analyze a wallet's on-chain behavior and generate an investor profile.

**Parameters:**
- `wallet_address` (required): EVM wallet address
- `language` (optional): "zh" or "en"
- `force_update` (optional): true to bypass 24h cache

**Example:**
```
User: Analyze this wallet: 0x3a4e3c24720a1c11589289da99aa31de3f338bf9
Agent: [calls get_wallet_profile(wallet_address="0x...")]
```

### 4. `get_market_overview`
Get current BTC/ETH prices and Fear & Greed Index.

**Parameters:** None

**Example:**
```
User: What's the crypto market like today?
Agent: [calls get_market_overview()]
```

## Data Sources

This MCP server connects to the J4Y backend which aggregates:
- 170+ news sources (RSS feeds, The Block, CoinDesk, etc.)
- 50+ KOL Twitter accounts (Chinese + English)
- Real-time market data (CoinGecko, Fear & Greed Index)
- On-chain data via DeBank API

## Why MCP Server?

Unlike prompt-based skills that rely on the host LLM to execute commands, this MCP server:
- **Executes real API calls** - Tools directly call the J4Y backend
- **Returns real data** - BTC/ETH prices, Fear & Greed Index are from live sources
- **Works on any MCP-compatible platform** - OpenClaw, Claude Desktop, Cursor, etc.

## Installation

### For OpenClaw
```json
{
  "plugins": {
    "entries": {
      "web3-daily-mcp": {
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

## Privacy

- **Public digest**: No personal data required
- **Personalized features**: Wallet address is sent to backend for analysis
- **Data retention**: Wallet profiles cached for 24 hours
- **No permanent storage**: We do not permanently store or sell wallet data
