---
name: web3-investor
version: 3.8.0
description: AI-native DeFi investment intelligence. Discover, analyze, and compare yield opportunities across 2,500+ protocols with intent-aware search, LLM-powered deep analysis, 7-dimension risk scoring, DeFi security scanning, smart money sentiment, and multi-round conversational refinement. All intelligence runs server-side — zero API keys on the client.
author: Antalpha AI Team
homepage: https://www.antalpha.com/
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    mcp:
      antalpha-skills:
        url: https://mcp-skills.ai.antalpha.com/mcp
        tools:
          - antalpha-register
          - investor_discover
          - investor_analyze
          - investor_compare
    security_notes:
      - All queries are sent to the Antalpha MCP server (mcp-skills.ai.antalpha.com)
      - Zero API keys required on the client side
      - All trading is zero-custody — private keys never leave the user's wallet
      - User investment intent is processed server-side for analysis
---

# Web3 Investor

> **Your AI-powered DeFi research analyst.** Not a dashboard — a thinker.

Web3 Investor turns vague investment intent into structured, risk-aware recommendations. It doesn't just fetch APY data — it *understands* what you're looking for, scores every opportunity across 7 risk dimensions, cross-references smart money flows, scans for contract vulnerabilities, and explains its reasoning in plain English.

---

## The Problem It Solves

DeFi yield farming today looks like this:

1. Open DeFiLlama → see 2,500+ pools → overwhelming
2. Check audits, TVL, APY trend, IL risk — each on a different site
3. Cross-reference with Twitter sentiment and whale wallets
4. Try to figure out if the yield is sustainable or just emission bait
5. **Give up and put money in USDC savings at 4%**

Web3 Investor collapses this into **one natural-language request**:

```
"I want stablecoin yield, conservative risk, on Ethereum"
→ 5 personalized recommendations with full risk analysis in 3 seconds
```

---

## 🧠 How It Works

### The Intelligence Pipeline

```
User Intent (natural language)
  │
  ├─ 1. Intent Classification (keyword + LLM fusion)
  │    Extract: asset type, risk level, chain, time horizon,
  │            position size, liquidity needs, implicit constraints
  │
  ├─ 2. Intent Gate (NEEDS_CLARIFICATION or PASS)
  │    If ambiguous → ask user a focused question
  │    If clear → proceed with accumulated context (multi-round session)
  │
  ├─ 3. Discovery Engine (DeFiLlama + Dune Analytics + CoinGecko)
  │    Fetch 200+ candidates → filter by chain, TVL, risk threshold
  │    → deduplicate → rank by risk-adjusted score
  │
  ├─ 4. Risk Scoring (7 dimensions, 0-100)
  │    TVL, audit status, chain maturity, yield sustainability,
  │    deposit token safety, reward token safety, protocol trust
  │    → composite risk level: LOW / MEDIUM / HIGH / VERY_HIGH
  │
  ├─ 5. DeFi Security Scan
  │    AI-powered contract scanner → scam detection → critical issue flag
  │
  ├─ 6. Smart Money Sentiment (Dune Analytics)
  │    Track whale/fund flows → inflow/outflow signal
  │
  ├─ 7. Recommendation Explanation
  │    "Why this product?" — benchmarked vs bank deposits,
  │    risk classification (controllable vs uncontrollable),
  │    honest alternatives if a better option exists
  │
  └─ Output: Ranked recommendations with full context
```

---

## 🛠 Three Tools. Deep Intelligence.

### `investor_discover` — Find Opportunities

The entry point. Converts natural language into structured intent, discovers opportunities, and returns ranked recommendations.

**What makes it different from a simple DeFiLlama query:**

| Feature | DeFiLlama | investor_discover |
|---------|-----------|-------------------|
| Input | Chain + sort | Natural language ("stablecoin, conservative") |
| Intent understanding | None | Keyword + LLM fusion with 95%+ accuracy |
| Risk filtering | Manual | Automatic 7-dimension scoring + threshold |
| Multi-round | N/A | Session-based intent accumulation |
| Clarification | N/A | Asks focused questions when intent is ambiguous |
| Smart money | N/A | Integrated whale flow signals |
| DeFi security | N/A | AI contract scanner per pool |
| Explanation | N/A | "Why this?" reasoning per recommendation |

**Multi-round Session Example:**
```
Round 1:
  User: "Find me good yields"
  Agent: "What's your risk tolerance? [Conservative] [Moderate] [Aggressive]"
  → Session stores partial intent

Round 2:
  User: "Conservative, stablecoins only"
  Agent: (accumulates Round 1 + Round 2 intent)
  → Returns conservative stablecoin recommendations on Ethereum
```

**Request:**
```json
{
  "agent_id": "uuid",
  "natural_language": "stablecoin yield, conservative risk, Ethereum",
  "structured_preferences": {
    "chain": "ethereum",
    "min_apy": 5,
    "asset_type": "stablecoin"
  },
  "limit": 5
}
```

**Response highlights:**
```json
{
  "gate_status": "PASS",
  "recommendations": [{
    "name": "Aave V3 USDC",
    "yield": { "apy": 5.2, "apy_base": 2.8, "apy_reward": 2.4 },
    "scale": { "tvl_usd": 1500000000 },
    "risk": {
      "risk_level": "LOW",
      "risk_score": 82,
      "risk_factors": { "tvl_score": 95, "audit_score": 90, ... },
      "warnings": []
    },
    "data_quality": { "score": 95, "level": "HIGH", "cross_validated": true },
    "incentive": { "score": "medium", "reward_ratio": 0.46 },
    "smart_money": { "flow": "inflow", "sentiment_score": 0.72, "confidence": "high" },
    "explanation": {
      "summary": "Aave V3 USDC: 5.2% APY, TVL $1.5B",
      "reasons": { "for": [...], "against": [...] },
      "compared_to": { "benchmark": "US bank savings (4.0%)", "outperformance": "1.3x" },
      "risks": { "controllable": ["随时可赎回"], "uncontrollable": ["智能合约风险"] }
    }
  }],
  "search_stats": {
    "total_candidates": 247,
    "total_after_risk_filter": 89,
    "final_recommendations": 5,
    "filters_applied": ["defillama_fetch:ethereum", "intent_filter:STABLECOIN", "risk_scoring", "dust_filter:50000"]
  }
}
```

---

### `investor_analyze` — Deep Analysis

LLM-powered 5-step reasoning chain for a single product. Goes beyond numbers to provide *understanding*.

**Analysis depths:**

| Depth | What You Get | Use Case |
|-------|-------------|----------|
| `basic` | Key metrics + risk score + 1-paragraph summary | Quick check |
| `detailed` | Full risk breakdown + yield source analysis + sustainability assessment + smart money + historical APY | **Recommended for investment decisions** |
| `full` | Everything in detailed + peer comparison + protocol profile + governance analysis + LLM narrative | Due diligence |

**The LLM analysis covers:**

```
Step 1: Yield Source Analysis
  → Is this APY from trading fees (sustainable) or token emissions (unsustainable)?
  → APY breakdown: base yield vs reward yield ratio

Step 2: Sustainability Assessment
  → Historical APY trend (7d / 30d / 90d)
  → APY volatility (standard deviation)
  → Revenue coverage (can the protocol afford these rewards?)

Step 3: Risk Narrative
  → Comprehensive risk story, not just a score
  → Smart money sentiment overlay
  → DeFi security scan results (scam flags, critical issues)

Step 4: Competitive Position
  → How does this compare to peers in the same category?
  → Protocol profile: governance, longevity, audit history

Step 5: Investor Considerations
  → Actionable guidance for the specific investor profile
  → Key risks and key positives
  → "If you're conservative, consider X. If aggressive, consider Y."
```

---

### `investor_compare` — Side-by-Side Comparison

Compare 2–5 products with LLM-powered interpretation across customizable dimensions.

**Default comparison dimensions:** APY, risk score, TVL

**Extended dimensions:** fees, lock period, audit count, IL risk, governance type, smart money sentiment, incentive sustainability

**LLM comparison output:**
```json
{
  "llm_comparison": {
    "narrative": "Aave offers superior security with $1.5B TVL and 6 audits, while Compound provides higher raw yield at 6.1% but with smaller TVL...",
    "risk_comparison": "Aave's risk score (82) significantly outperforms Compound (68), primarily due to larger TVL and more comprehensive audit coverage",
    "recommendation_with_reasoning": {
      "for_conservative": "Choose Aave — battle-tested protocol, deep liquidity, multiple top-tier audits",
      "for_aggressive": "Consider Compound — 0.9% higher APY, acceptable risk for short-term positions",
      "key_tradeoff": "0.9% yield premium vs significantly lower risk score (82 vs 68)"
    }
  }
}
```

---

## 🏗️ Server-Side Architecture

```
┌─────────────────────┐
│    AI Agent          │         MCP JSON-RPC         ┌──────────────────────────────────────┐
│    (OpenClaw)        │ ─────────────────────────────► │  Antalpha MCP Server                 │
│                      │                                │  mcp-skills.ai.antalpha.com          │
│  "Find me yield"     │                                │                                      │
│  → 3 tool calls      │ ◄───────────────────────────── │  Intent Classifier (keyword + LLM)   │
│  → zero API keys     │   structured results           │  Risk Scoring (7 dimensions)         │
│  → zero custody      │                                │  DeFi Security Scanner               │
└─────────────────────┘                                │  LLM Analysis (5-step chain)         │
                                                       │  Smart Money (Dune Analytics)        │
                                                       │  Market Context (bull/bear/sideways)  │
                                                       │  Protocol Profiles (DefiLlama)       │
                                                       │  Data Validation (cross-source)      │
                                                       │  Explanation Engine (benchmarked)    │
                                                       │                                      │
                                                       │  Data Sources:                        │
                                                       │  ├─ DefiLlama (2,500+ pools)         │
                                                       │  ├─ Dune Analytics (smart money)     │
                                                       │  ├─ CoinGecko (market data)          │
                                                       │  ├─ DeFi Security (contract scan)    │
                                                       │  └─ Internal LLM (analysis)          │
                                                       └──────────────────────────────────────┘
```

---

## 🔐 Risk Intelligence

### 7-Dimension Risk Scoring

Each opportunity is scored 0–100 across seven independent dimensions:

| Dimension | What It Measures | Weight |
|-----------|-----------------|--------|
| **TVL Score** | Total Value Locked — protocol maturity indicator | High |
| **Audit Score** | Number and quality of security audits | High |
| **Chain Score** | Chain maturity (L1 vs L2 vs new chain) | Medium |
| **Sustainability** | Yield source analysis (fees vs emissions) | High |
| **Deposit Token** | Safety tier of the deposit asset (USDC > DAI > random) | Medium |
| **Reward Token** | Liquidity and safety of reward tokens | Low |
| **Protocol Trust** | Governance, longevity, track record | Medium |

**Risk Levels:**
- **LOW** (score ≥ 70): Battle-tested, well-audited, high TVL
- **MEDIUM** (score 50–69): Established but with some risk factors
- **HIGH** (score 30–49): Newer or with significant warnings
- **VERY_HIGH** (score < 30): Experimental or flagged

### DeFi Security Scanning

Every pool is scanned by an AI-powered contract security engine:

```json
{
  "defi_security": {
    "aiScore": 87,
    "safetyPercentage": 92,
    "isScam": false,
    "criticalIssues": 0
  }
}
```

### Smart Money Sentiment

Real-time whale and fund wallet activity aggregated from Dune Analytics:

```json
{
  "smart_money": {
    "flow": "inflow",
    "sentiment_score": 0.72,
    "confidence": "high",
    "buy_volume_usd": 15000000,
    "sell_volume_usd": 3200000,
    "net_flow_usd": 11800000,
    "signal_count": 23
  }
}
```

### Market Context Awareness

The engine is aware of the current market cycle (bull/bear/sideways), total DeFi TVL, BTC dominance, and US Treasury rates — providing context-aware recommendations that adjust for macro conditions.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- No API keys needed — all intelligence runs server-side

### Registration (one-time)

```bash
./scripts/run.sh register
# Returns agent_id — save this for all subsequent calls
```

### Usage

```bash
# Discover opportunities
./scripts/run.sh discover --chain ethereum --min-apy 5 --limit 5

# Discover with natural language
./scripts/run.sh discover --natural-language "stablecoin yield, conservative"

# Deep analysis
./scripts/run.sh analyze --product-id <id> --depth detailed

# Full due diligence
./scripts/run.sh analyze --product-id <id> --depth full

# Compare products
./scripts/run.sh compare --ids <id1> <id2> <id3>
```

---

## ⚠️ Critical Rules

### Rule 1: Discovery First
**Never give generic investment advice without real-time data.**
```
❌ "I recommend Aave for stablecoin yield"
✅ investor_discover → analyze results → data-backed recommendation
```

### Rule 2: Explain Your Reasoning
Every recommendation should include the `explanation` object — summary, reasons for/against, benchmark comparison, risk classification.

### Rule 3: Risk Is Non-Negotiable
- APY data may be delayed — always show `data_quality.score` and `last_updated`
- Never recommend VERY_HIGH risk products without explicit user acknowledgment
- Investment decisions are the user's own responsibility — always DYOR

### Rule 4: Honest About Limitations
- If no good options exist for the user's criteria, say so with `generateHonestNoResultExplanation`
- Show alternatives even if they don't perfectly match — "This is close but has X tradeoff"

---

## 🔒 Security

| Layer | Protection |
|-------|-----------|
| **Private Keys** | Zero contact — never held, transmitted, or stored |
| **Data Sources** | Triple-validated (DefiLlama + Dune + CoinGecko) with cross-source checks |
| **Contract Safety** | AI-powered DeFi security scanner on every pool |
| **Risk Scoring** | 7 independent dimensions, no single point of failure |
| **Scam Detection** | Automated flagging via DeFi Security engine (`isScam` check) |
| **Data Quality** | Freshness tracking, confidence scores, validation issue logging |

---

## 📝 Changelog

### v3.8.0 (2026-04-14)
- **Full SKILL.md rewrite** — English, feature-focused, comprehensive
- Documented complete server-side intelligence pipeline
- Added 7-dimension risk scoring documentation
- Added DeFi Security scanning documentation
- Added Smart Money sentiment documentation
- Added Market Context awareness documentation
- Added multi-round session intent accumulation flow
- Added honest "no result" explanation behavior
- Added incentive sustainability scoring documentation
- Added data quality cross-validation documentation

### v3.7.2 (2026-04-13)
- Client cleanup: removed deprecated tools (feedback/confirm-intent/get-intent)

---

## 🤝 Contributing

Test donations welcome:
- **Network**: Base Chain
- **Address**: `0x1F3A9A450428BbF161C4C33f10bd7AA1b2599a3e`

---

**Maintainer**: Web3 Investor Skill Team
**Registry**: https://clawhub.com/skills/web3-investor
**License**: MIT
