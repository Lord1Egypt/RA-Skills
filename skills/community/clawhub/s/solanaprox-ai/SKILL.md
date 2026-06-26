---
name: solanaprox-ai
description: Solana wallet-native AI gateway — pay per AI request with USDC on Solana. 19 models across 5 providers. No API keys, no accounts. Your wallet address is your credential.
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "🌊"
    homepage: https://solanaprox.com
    requires:
      env:
        - SOLANAPROX_WALLET_ADDRESS
---

# SolanaProx — Solana-Native AI Gateway

Pay-per-use access to 19 AI models across 5 providers via Solana USDC micropayments. No API keys. No subscriptions. No accounts. Your wallet address is your credential — deposit USDC, get inference.

## When to Use

- Accessing AI models without provider API keys
- Autonomous agent inference paid in USDC on Solana
- DeFi-native workflows where payment should flow on-chain
- Running AI pipelines from a Solana wallet balance
- Multi-agent orchestration across 14 capabilities

## Supported Models (19 total)

| Model | Provider | Type |
|-------|----------|------|
| `claude-sonnet-4-6` | Anthropic | Chat |
| `gpt-4-turbo` | OpenAI | Chat |
| `meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8` | Together.ai | Chat |
| `meta-llama/Llama-3.3-70B-Instruct-Turbo` | Together.ai | Chat |
| `meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo` | Together.ai | Chat |
| `mistralai/Mixtral-8x7B-Instruct-v0.1` | Together.ai | Chat |
| `deepseek-ai/DeepSeek-V3` | Together.ai | Chat |
| `mistral-large-latest` | Mistral | Chat |
| `mistral-medium-latest` | Mistral | Chat |
| `mistral-small-latest` | Mistral | Chat |
| `open-mistral-nemo` | Mistral | Chat |
| `codestral-latest` | Mistral | Code |
| `devstral-latest` | Mistral | Agentic Code |
| `pixtral-large-latest` | Mistral | Vision |
| `magistral-medium-latest` | Mistral | Reasoning |
| `gemini-2.5-flash` | Google | Chat |
| `gemini-2.5-pro` | Google | Chat |
| `gemini-3-flash-preview` | Google | Chat |
| `gemini-3-pro-preview` | Google | Chat |

## Payment Flow

```bash
# 1. Connect Phantom wallet at solanaprox.com
# 2. Deposit USDC to your wallet's SolanaProx balance
# 3. Use wallet address as credential

curl -X POST https://solanaprox.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-Wallet-Address: $SOLANAPROX_WALLET_ADDRESS" \
  -d '{
    "model": "claude-sonnet-4-6",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 1000
  }'
```

## Drop-in OpenAI SDK Replacement

```bash
npm install solanaprox-openai
```

```javascript
// Before: import OpenAI from 'openai'
import OpenAI from 'solanaprox-openai'
const client = new OpenAI({ apiKey: process.env.SOLANAPROX_WALLET_ADDRESS })

// Everything else stays identical:
const response = await client.chat.completions.create({
  model: 'claude-sonnet-4-6',
  messages: [{ role: 'user', content: 'Hello' }]
})
```

Two lines change. Nothing else does.

## Multi-Agent Orchestration

SolanaProx routes through the AIProx orchestrator — automatically selects the best agent for each task.

```bash
curl -X POST https://solanaprox.com/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "search for Solana DeFi news and summarize",
    "wallet_address": "$SOLANAPROX_WALLET_ADDRESS"
  }'
```

Response includes `_aiprox` metadata: which agents ran, USDC spent, receipt ID.

## Available Capabilities

`ai-inference` · `web-search` · `email` · `image-generation` · `sentiment-analysis` · `data-analysis` · `translation` · `vision` · `code-execution` · `market-data` · `token-analysis` · `scraping` · `agent-commerce` · `agent-orchestration`

## Check Available Models

```bash
curl https://solanaprox.com/api/capabilities
```

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | solanaprox.com | API calls for AI inference |
| Env Read | SOLANAPROX_WALLET_ADDRESS | Solana wallet address for USDC payments |

## Trust Statement

SolanaProx is operated by LPX Digital Group LLC. Your Solana wallet address authenticates you — no passwords, no accounts. USDC deducted from pre-deposited balance per successful request. Operated at solanaprox.com.
