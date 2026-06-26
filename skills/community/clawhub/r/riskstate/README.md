<p align="center">
  <img src="https://riskstate.ai/logo-r-grey.svg" width="48" alt="RiskState" />
</p>

<h1 align="center">RiskState</h1>

<p align="center">
  <strong>Pre-trade risk API for crypto — BTC/USD and ETH/USD exposure governance</strong><br />
  <sub>For trading agents, open-source systems, and capital desks. Spot and perpetual futures (perps). DeFi borrowing aware.</sub>
</p>

<p align="center">
  <a href="https://api.riskstate.ai/v1/risk-state"><img src="https://img.shields.io/badge/API-v1.4.0-blue?style=flat-square" alt="API Version" /></a>
  <a href="https://riskstate.ai"><img src="https://img.shields.io/badge/status-beta-green?style=flat-square" alt="Status" /></a>
  <a href="#supported-assets"><img src="https://img.shields.io/badge/assets-BTC%2FUSD%20%7C%20ETH%2FUSD-orange?style=flat-square" alt="Assets" /></a>
  <a href="#markets"><img src="https://img.shields.io/badge/markets-spot%20%7C%20perps%20%7C%20DeFi-purple?style=flat-square" alt="Markets" /></a>
  <a href="#pricing"><img src="https://img.shields.io/badge/pricing-free%20beta-brightgreen?style=flat-square" alt="Pricing" /></a>
</p>

<p align="center">
  <a href="https://riskstate.ai">Website</a> · <a href="docs/api-v1.md">API Reference</a> · <a href="SKILL.md">SKILL.md</a> · <a href="https://x.com/riskstate_ai">X/Twitter</a>
</p>

---

## What is RiskState?

A deterministic engine that converts live market state into **dynamic risk permissions** — exposure limits, leverage caps, and allowed actions — before capital is deployed.

One API call returns position limits, allowed actions, and policy constraints computed from **30+ real-time signals** across macro, on-chain, derivatives, and DeFi health. The assessment is **USD-denominated**: all scoring is based on BTC/USD and ETH/USD price action, derivatives, and macro conditions.

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC"}'
```

```json
{
  "exposure_policy": {
    "max_size_fraction": 0.42,
    "leverage_allowed": true,
    "allowed_actions": ["DCA", "LONG_SHORT_CONFIRMED"],
    "blocked_actions": ["ALL_IN", "LEVERAGE_GT_2X"]
  },
  "policy_level": 4,
  "risk_flags": {
    "structural_blockers": [],
    "context_risks": ["HIGH_COUPLING"]
  },
  "binding_constraint": {
    "source": "MACRO",
    "reason_codes": ["MACRO_NEUTRAL", "COUPLING_NORMAL"]
  }
}
```

Read `max_size_fraction`, check `structural_blockers`, and act. No parsing. No interpretation.

## Why?

Whether you run an AI trading agent, a systematic trading system, or a manual desk — crypto markets have regime shifts that require adaptive risk governance. Static rules fail. RiskState provides a **pre-trade risk check** that adapts every 60 seconds.

| Without governance | With RiskState |
|---|---|
| Position size based on signal confidence alone | Capped at `max_size_fraction` (max notional exposure) |
| No awareness of macro regime | `RISK-OFF` → `blocked_actions: ["AGGRESSIVE_LONG"]` |
| DeFi health factor ignored | Wallet health feeds directly into position limit |
| Leverage unbounded | Policy-level constraints enforced |
| No circuit breaker | `structural_blockers` non-empty → halt |

## Quick Start

### 1. Get an API key

Sign up at [riskstate.ai](https://riskstate.ai) — email only, free during beta.

### 2. Query the API

```bash
curl -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC"}'
```

### 3. Enforce before execution

**In an AI trading agent (Python):**

```python
import requests

policy = requests.post(
    "https://api.riskstate.ai/v1/risk-state",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"asset": "BTC"}
).json()

# Hard stop: structural blockers
if policy["risk_flags"]["structural_blockers"]:
    return  # Do not trade

# Size cap — max notional exposure as fraction of portfolio
max_size = policy["exposure_policy"]["max_size_fraction"]
position_size = min(desired_size, portfolio_value * max_size)

# Action filter
if "LEVERAGE" in policy["exposure_policy"]["blocked_actions"]:
    leverage = 1.0
```

**In a trading system (pre-trade check):**

```python
# Before placing a spot or perps order
policy = fetch_riskstate("ETH")

if policy["risk_flags"]["structural_blockers"]:
    log("BLOCKED: structural risk — skipping order")
    return

max_notional = portfolio_value * policy["exposure_policy"]["max_size_fraction"]
# Spot: max_notional is the $ amount to deploy
# Perps: max_notional is the notional exposure cap
#   e.g., at 10x leverage → margin = max_notional / 10
```

**Manual pre-trade check (curl):**

```bash
# Quick check before placing an order on Binance/Hyperliquid/Aave
curl -s -X POST https://api.riskstate.ai/v1/risk-state \
  -H "Authorization: Bearer $RISKSTATE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"asset": "BTC"}' | jq '{
    policy_level, 
    max_size: .exposure_policy.max_size_fraction,
    blocked: .exposure_policy.blocked_actions,
    blockers: .risk_flags.structural_blockers
  }'
```

## Policy Levels

| Level | Label | Max Size | What your agent can do |
|-------|-------|----------|----------------------|
| 1 | BLOCK Survival | <15% | Reduce exposure, hedge only |
| 2 | BLOCK Defensive | <35% | Wait, hedge, small scalps |
| 3 | CAUTIOUS | <60% | DCA, R:R >2:1 only |
| 4 | GREEN Selective | <80% | Trade with confirmation |
| 5 | GREEN Expansion | ≥80% | Full operations, leverage up to 2x |

## Supported Assets

- **BTC/USD** — Full signal coverage (30+ indicators). Scoring based on BTC/USDT price, derivatives, and macro conditions.
- **ETH/USD** — Full coverage including ETH structural score, ETH/BTC ratio analysis, staking dynamics, ETH/NASDAQ correlation.

> **Note:** The assessment is USD-denominated. If you trade non-USD pairs (e.g., BTC/EUR, ETH/BTC), additional cross-rate risk is not covered.

## Markets

RiskState evaluates the same underlying market conditions regardless of where you trade. The risk assessment applies to:

| Market | How to use the output |
|--------|----------------------|
| **Spot** | `max_size_fraction` = % of portfolio to deploy. Leverage fields are not applicable. |
| **Perpetual futures (perps)** | `max_size_fraction` = max notional exposure as % of portfolio. At 10x leverage, your margin is `max_size_fraction / 10`. Derivatives signals (funding rate, basis, OI, squeeze risk) are especially relevant. |
| **DeFi borrowing** | Pass your `wallet` address for health factor and liquidation-aware risk caps. `max_leverage` reflects borrowing ratio (LTV). |

The API returns the same response for all markets — the difference is how you **interpret** the output. See [API Reference → How to Use by Context](docs/api-v1.md#how-to-use-by-context) for detailed workflows.

## Integration Paths

### REST API
Direct HTTP calls. Any language, any framework.

### SKILL.md
Drop [`SKILL.md`](SKILL.md) into your agent's repo. Compatible with Claude Code, Copilot, Cursor, and Gemini via [skills.sh](https://skills.sh).

### MCP Server

```bash
npm install @riskstate/mcp-server
```

Or run directly with `npx @riskstate/mcp-server`. Docker: `ghcr.io/likidodefi/riskstate-mcp`.

One tool: `get_risk_policy` — same parameters as the REST API. Compatible with Claude Desktop, Claude Code, Cursor, and any MCP-compatible client. See [MCP README](https://riskstate.ai/docs/mcp) for full setup.

## Listed On

- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) — Finance & Fintech category
- [LobeHub MCP](https://lobehub.com) — Auto-discovered
- [ClawHub.ai](https://clawhub.ai) — Skill marketplace
- [skills.sh](https://skills.sh) — Vercel skills registry
- [Glama.ai](https://glama.ai) — AAA score

## Binding Precedence

When consuming the response, agents **must** evaluate fields in this order:

1. `risk_flags.structural_blockers` — if non-empty, **abort** new entries
2. `exposure_policy.blocked_actions` — actions the agent must not take
3. `exposure_policy.reduce_recommended` — reduce exposure if `true`
4. `exposure_policy.max_size_fraction` — maximum position size (0.0–1.0)
5. `exposure_policy.max_leverage` — maximum leverage allowed

## Data Sources

RiskState ingests 30+ real-time signals from:

- **Price & Derivatives** — Binance, OKX, Bybit (funding, OI, basis, L/S ratio)
- **On-chain** — MVRV, NUPL, exchange netflow, supply metrics (CoinGlass)
- **Macro** — DXY, US yields, S&P 500, Gold, Fed balance sheet (FRED, Yahoo Finance)
- **DeFi** — Spark Protocol, Aave V3 health factor and liquidation thresholds
- **Sentiment** — Fear & Greed, ETF flows, institutional treasuries
- **ETH-specific** — Staking ratio, burn rate, DEX volume, fees, stablecoin TVL

## Pricing

**Free during beta.** Rate limit: 60 requests/minute.

| Tier | Calls/month | Price |
|------|------------|-------|
| Free | 100 | $0 |
| Builder | 5,000 | $49/mo |
| Growth | 25,000 | $149/mo |
| Scale | 100,000 | $399/mo |

Paid tiers coming after beta. [Sign up now](https://riskstate.ai) to lock in early access.

## Documentation

- [**API Reference**](docs/api-v1.md) — Full endpoint documentation, field types, error codes
- [**SKILL.md**](SKILL.md) — Agent discovery file with decision rules and failure modes
- [**Changelog**](CHANGELOG.md) — Version history and release notes
- [**Website**](https://riskstate.ai) — Landing page with interactive examples

## Links

- Website: [riskstate.ai](https://riskstate.ai)
- X/Twitter: [@riskstate_ai](https://x.com/riskstate_ai)
- API: `POST https://api.riskstate.ai/v1/risk-state`

---

<p align="center">
  <sub>Built by <a href="https://riskstate.ai">RiskState</a> · © 2026 Digital Venture Asset LLC</sub>
</p>
