---
name: web3-daily
version: 2.1.1
description: >-
  Web3 public research digest service. Provides daily digest with macro news, KOL sentiment, 
  and real-time market data (BTC/ETH prices, Fear & Greed Index). No personal data required. 
  Use when user asks for Web3 news, crypto digest, or says /web3.
author: Alex Wang
repository: https://github.com/alexander10011/web3-daily
homepage: https://github.com/alexander10011/web3-daily
license: MIT
permissions:
  - network
---

# Web3 Daily

**Follow the market, not the noise.** Get a daily Web3 research digest with macro news, KOL sentiment, and real-time market data.

## What You Get

- 📊 **Real-time market data** — BTC/ETH prices, 24h change, Fear & Greed Index
- 📰 **Macro news analysis** — 5-8 key events from 170+ sources
- 📡 **KOL sentiment** — What Chinese + English crypto Twitter is saying
- 🌐 **Bilingual** — Available in English or Chinese

**No personal data required. No API keys needed.**

## Two Versions Available

| Version | Words | Best For |
|---------|-------|----------|
| **Full** (`/digest/public`) | ~4000-5000 | Detailed analysis, desktop reading |
| **Compact** (`/digest/compact`) | ~2500 | Quick reading, Telegram push |

## How This Skill Works

This skill connects to a live backend service that:
1. Aggregates 170+ news sources every 6 hours
2. Monitors 50+ KOL Twitter accounts (Chinese + English)
3. Fetches real-time market data (BTC/ETH prices, Fear & Greed Index)
4. Uses AI to generate comprehensive analysis

**You cannot replicate this data by yourself. You MUST call the API.**

## Privacy

✅ **Zero personal data collected** — This skill only fetches public market data
✅ **No wallet address needed** — Pure public information
✅ **No local files created** — Nothing stored on your machine
✅ **All traffic encrypted** — HTTPS only

## Trigger Conditions

Use this skill when user message contains:
- "Web3 digest" / "crypto digest" / "crypto news"
- "/web3" / "/digest"
- "What's happening in crypto today"
- "今天加密市场怎么样"
- "给我 Web3 日报"
- "简版日报" / "compact digest" (for compact version)

---

## Workflow A: Full Digest (Default)

### ⚠️ CRITICAL: You MUST execute the curl command below. DO NOT generate fake/simulated content.

**Steps**:

1. Tell user: "Fetching latest Web3 digest..."

2. **MUST EXECUTE** this curl command (do not skip or simulate):

For Chinese output (default):
```bash
curl -s -X POST "https://j4y-production.up.railway.app/api/v1/digest/public" \
  -H "Content-Type: application/json" \
  -d '{"language": "zh"}'
```

For English output:
```bash
curl -s -X POST "https://j4y-production.up.railway.app/api/v1/digest/public" \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'
```

3. Parse the JSON response and extract the `digest` field

4. Display the EXACT content from `digest` field to user (do not modify or summarize)

---

## Workflow B: Compact Digest (For Quick Reading / Push)

**Trigger**: User asks for "简版" / "compact" / "short version" / "quick digest"

**Steps**:

1. Tell user: "Fetching compact Web3 digest..."

2. **MUST EXECUTE** this curl command（推荐 `/digest/compact`；`/digest/public/compact` 为兼容别名）:

For Chinese output:
```bash
curl -s -X POST "https://j4y-production.up.railway.app/api/v1/digest/compact" \
  -H "Content-Type: application/json" \
  -d '{"language": "zh"}'
```

For English output:
```bash
curl -s -X POST "https://j4y-production.up.railway.app/api/v1/digest/compact" \
  -H "Content-Type: application/json" \
  -d '{"language": "en"}'
```

3. Parse the JSON response and extract the `digest` field

4. Display the EXACT content from `digest` field to user

**Compact version features**:
- ~2500 words (50-60% of full version)
- No URL links (cleaner for messaging apps)
- Keeps core insights: 3 themes, KOL sentiment summary, risks & opportunities
- Table format for quick scanning

---

### Expected Response:
```json
{
  "success": true,
  "digest": "---\n\n# 📅 Web3 日报 | 2026-03-31\n\n---\n\n## 📊 市场概览\n\n**大盘行情**:\n- **BTC**: $67,100 (+0.55%)\n- **ETH**: $2,031 (+1.16%)\n\n...",
  "cached": true,
  "generated_at": "2026-03-31T10:00:00Z",
  "language": "zh"
}
```

### ❌ DO NOT:
- Generate your own digest content
- Summarize or paraphrase the API response
- Skip the API call and make up data
- Return "example" or "simulated" content

### ✅ MUST:
- Execute the actual curl command
- Return the exact `digest` content from API response
- Include real BTC/ETH prices and Fear & Greed Index from the response

---

## Language Support

Detect user's language preference:
- If user speaks Chinese → use `"language": "zh"`
- If user speaks English → use `"language": "en"`
- If unclear, default to Chinese

---

## Error Handling

| Error | Action |
|-------|--------|
| Service unavailable | Tell user: "J4Y service is temporarily unavailable, please try again later" |
| API returns error | Show error message, suggest retry |
| Timeout | Tell user: "Request timed out, the service may be busy, please try again" |

---

## Example Conversations

**Full Digest:**
```
User: What's happening in crypto today?
Assistant: Fetching latest Web3 digest...
Assistant: [Display full digest with detailed analysis]
```

**Compact Digest:**
```
User: 给我简版日报
Assistant: 正在获取精简版 Web3 日报...
Assistant: [Display compact digest with key insights]
```

---

## Data Sources

- **News**: The Block, CoinDesk, Decrypt, Cointelegraph, and 160+ more
- **KOLs**: 50+ Chinese + English crypto Twitter accounts
- **Market**: CoinGecko, CoinMarketCap (prices), Alternative.me (Fear & Greed Index)

Updated every 6 hours.
