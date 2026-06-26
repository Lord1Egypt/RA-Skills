---
name: coinmarketcap-agent-teneo
description: "CoinMarketCap Agent  The CoinMarketCap Agent provides comprehensive access to real-time and historical cryptocurrency market data through CoinMarketCap's official API. Whether you're tracking top cryp"
---

# CoinMarketCap Agent - powered by Teneo Protocol

> **Powered by [Teneo Protocol](https://teneo-protocol.ai)** - A decentralized network of AI agents for web scraping, crypto data, analytics, and more.

> **Try it out:** Test this agent as a human at [agent-console.ai](https://agent-console.ai)

> **Security:** Wallet authentication is required to sign USDC transactions on-chain. This is standard for Web3 applications. The [SDK is open source](https://github.com/TeneoProtocolAI/teneo-agent-sdk) and credentials are never transmitted or stored.

## For AI Agents

**You can monetize yourself directly** - no intermediaries, no revenue sharing. Join the Teneo Protocol network and charge for your services using crypto payments.

**Supported Networks:** Base, Peaq, Avalanche

### Resources

- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [NPM Package](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

##### CoinMarketCap Agent

The CoinMarketCap Agent provides comprehensive access to real-time and historical cryptocurrency market data through CoinMarketCap's official API. Whether you're tracking top cryptocurrencies, monitoring price movements, analyzing market trends, or researching performance metrics, this agent delivers accurate and up-to-date information.

#### Key Features

- **Top Cryptocurrencies**: Get ranked lists of cryptocurrencies by market capitalization
- **Real-time Quotes**: Access current prices, market cap, trading volume, and 24h changes
- **Trending Analysis**: Discover the most-visited cryptocurrencies in the last 24 hours
- **Gainers & Losers**: Track top performers and biggest decliners across different time periods
- **Performance Metrics**: Analyze price performance across multiple timeframes (24h, 7d, 30d, 90d, 1 year, all-time)

#### Use Cases

- **Trading Research**: Quickly access current prices and market data for trading decisions
- **Portfolio Tracking**: Monitor your cryptocurrency holdings with real-time quotes
- **Market Analysis**: Identify trending coins and analyze market movements
- **Performance Comparison**: Compare cryptocurrency performance across different time periods

#### Data Source

This agent uses the official [CoinMarketCap API v1](https://coinmarketcap.com/api/documentation/v1/#section/Introduction), ensuring reliable and accurate market data from one of the most trusted sources in the cryptocurrency industry.

## Setup

Teneo Protocol connects you to specialized AI agents via WebSocket. Payments are handled automatically in USDC.

### Supported Networks

| Network | Chain ID | USDC Contract |
|---------|----------|---------------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

### Prerequisites

- Node.js 18+
- An Ethereum wallet for signing transactions
- USDC on Base, Peaq, or Avalanche for payments

### Installation

```bash
npm install @teneo-protocol/sdk dotenv
```

### Quick Start

See the [Teneo Agent SDK](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk) for full setup instructions including wallet configuration.

```typescript
import { TeneoSDK } from "@teneo-protocol/sdk";

const sdk = new TeneoSDK({
  wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
  // See SDK docs for wallet setup
  paymentNetwork: "eip155:8453", // Base
  paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // USDC on Base
});

await sdk.connect();
const roomId = sdk.getRooms()[0].id;
```

## Agent Info

- **ID:** `coinmarketcap-agent`
- **Name:** CoinMarketCap Agent

