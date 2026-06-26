# SolanaProx MCP Server

> Pay for AI inference with Solana. No API keys. Your wallet is your identity.

[![npm version](https://badge.fury.io/js/solanaprox-mcp.svg)](https://www.npmjs.com/package/solanaprox-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Connect Claude Desktop, Cursor, or any MCP-compatible AI tool to SolanaProx — pay per request using USDC or SOL directly from your Phantom wallet.

---

## What is SolanaProx?

SolanaProx is an AI API gateway where your **Phantom wallet is your account**. Deposit USDC or SOL, make AI requests, pay per use. No signups. No subscriptions. No API key management.

SolanaProx implements the **Coinbase x402 payment protocol** — unauthenticated requests receive HTTP 402 with a spec-compliant `X-PAYMENT-REQUIRED` header, making it compatible with x402-aware agents and listed on [402index.io](https://402index.io).

```
Your Phantom Wallet → SolanaProx → Claude / GPT-4
       ↑                                    ↓
   USDC balance                        AI response
```

---

## Quick Start

### 1. Install the MCP server

```bash
npx solanaprox-mcp
```

### 2. Add to Claude Desktop

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "solanaprox": {
      "command": "npx",
      "args": ["solanaprox-mcp"],
      "env": {
        "SOLANA_WALLET": "YOUR_PHANTOM_WALLET_ADDRESS"
      }
    }
  }
}
```

### 3. Add to Cursor

Edit `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "solanaprox": {
      "command": "npx",
      "args": ["solanaprox-mcp"],
      "env": {
        "SOLANA_WALLET": "YOUR_PHANTOM_WALLET_ADDRESS"
      }
    }
  }
}
```

### 4. Deposit USDC

Visit [solanaprox.com](https://solanaprox.com), connect your Phantom wallet, and deposit USDC or SOL.

That's it. Claude can now make AI requests that pay automatically from your balance.

---

## Tools

### `ask_ai`
Send a prompt to Claude or GPT-4. Cost deducted automatically from wallet balance.

```
Input:
  prompt      (required) — your question or task
  model       (optional) — claude-sonnet-4-20250514 (default) | gpt-4-turbo
  max_tokens  (optional) — 1-4096, default 1024
  system      (optional) — system prompt for context
```

### `check_balance`
Check your current USDC/SOL balance on SolanaProx.

```
Input:
  wallet  (optional) — defaults to configured SOLANA_WALLET
```

### `estimate_cost`
Estimate request cost before making it.

```
Input:
  prompt      (required)
  model       (optional)
  max_tokens  (optional)
```

### `list_models`
List all available models and pricing.

---

## Pricing

| Model | Input | Output |
|-------|-------|--------|
| Claude Sonnet 4 | $3.60/1M tokens | $18.00/1M tokens |
| GPT-4 Turbo | $12.00/1M tokens | $36.00/1M tokens |

Cached responses receive a **50% discount**.

Typical request costs:
- Short question/answer: ~$0.001–0.003
- Code review (500 lines): ~$0.01–0.03  
- Long document analysis: ~$0.05–0.15

---

## Use Cases

### Personal AI assistant with micropayments
Pay only for what you use. No $20/month subscription burning while you sleep.

### Autonomous AI agents
AI agents that pay for their own inference — no hardcoded API keys, no human in the loop.

```js
// Agent pays autonomously on every request
const res = await fetch("https://solanaprox.com/v1/messages", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-Wallet-Address": process.env.SOLANA_WALLET,
  },
  body: JSON.stringify({
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  }),
});
```

### Solana app integration
Let your app's users pay for AI features directly from their Phantom wallet. No backend payment processing required.

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SOLANA_WALLET` | ✅ | Your Phantom wallet address |
| `SOLANAPROX_URL` | ❌ | Override API URL (default: https://solanaprox.com) |

---

## Standalone Agent Example

```bash
git clone https://github.com/solanaprox/mcp-server
cd mcp-server
npm install

# Run the research agent
SOLANA_WALLET=your_wallet node agent-example.js research "Solana DeFi trends 2026"

# Check balance
SOLANA_WALLET=your_wallet node agent-example.js balance

# Quick demo
SOLANA_WALLET=your_wallet node agent-example.js
```

---

## Integration Examples

### LangChain (Python)
Coming soon — or use the REST API directly.

### Direct REST API

```bash
# Check balance
curl https://solanaprox.com/api/balance/YOUR_WALLET

# Make AI request
curl -X POST https://solanaprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Wallet-Address: YOUR_WALLET" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

---

## Security

- Your wallet address is used as an identifier — it's public by design on Solana
- Private keys never leave your wallet
- SolanaProx only reads incoming transactions to your deposit address
- Rate limiting and spend limits protect against runaway costs
- All transactions verifiable on [Solscan](https://solscan.io)

---

## Links

- 🌐 [solanaprox.com](https://solanaprox.com)
- 📖 [API Docs](https://solanaprox.com/docs)
- 🐦 [Twitter/X](https://twitter.com/solanaprox)
- ⚡ [LightningProx](https://lightningprox.com) — same product, Bitcoin Lightning payments

---

## Built by LPX Digital Group LLC

Part of the LPX ecosystem:
- [LightningProx](https://lightningprox.com) — AI APIs via Bitcoin Lightning
- [SolanaProx](https://solanaprox.com) — AI APIs via Solana/USDC
- [LPXPoly](https://lpxpoly.com) — AI-powered Polymarket analysis
- [IsItARug](https://isitarug.com) — Solana token safety scanner

---

MIT License
