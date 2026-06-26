# X Alpha Scout

Turn your AI agent into an alpha-hunting machine. This skill enables agents to scan X/Twitter for crypto calls, NFT mints, and deliver daily intelligence reports.

## What It Does

- **Comprehensive Daily Alpha Reports** — Auto-generated at 00:00 UTC with market updates, news, CT sentiment, NFT ecosystem coverage (ETH/BTC/SOL), alpha from reputable figures, and warnings
- **On-Demand Analysis** — Ask about any token/NFT and get CT sentiment breakdown

## Perfect For

- Agents that need daily market intelligence
- Traders who want CT sentiment on specific plays
- Anyone wanting structured alpha without the noise

## Installation

1. **Install bird** — X/Twitter CLI tool (by founder of OpenClaw)
   ```bash
   # Via Homebrew (macOS/Linux)
   brew install steipete/tap/bird
   
   # Or download from releases (if brew doesn't work)
   # https://github.com/steipete/bird/releases
   ```
   
2. **Get X credentials:**
   - Auth token (`X_AUTH_TOKEN`)
   - CT0 cookie (`X_CT0`)
   
3. **Verify access:**
   ```bash
   bird whoami --auth-token "$X_AUTH_TOKEN" --ct0 "$X_CT0"
   ```

## Usage

**Daily Report:**
> "Run my daily alpha"

**On-Demand Analysis:**
> "What do you think of $PEPEAI?"
> "Analyze Pudgy Penguins"

## Example Daily Report

```markdown
# 🦅 Alpha Report — Feb 10, 2026

### 1. Good Morning
Rise and grind — market's showing some life.

### 2. Crypto Market Update
- BTC: ~$69,400 (+3% 24h)
- ETH: ~$2,318 (-3% 24h)
- SOL: ~$86 (stable)
- Fear & Greed Index: 9 (Extreme Fear)

### 3. News of the Day
- [Pudgy Penguins teases Visa credit card](https://x.com/coingecko/status/...)
- [Tether announces LayerZero investment](https://x.com/PeteyK/status/...)

### 4. Crypto Twitter (CT)
- Main narrative: AI agents running — $BANKR launchpad live
- @pudgypenguins dominating with Visa teaser

### 5. NFTs Market Update

**ETH Eco:** Pudgy Penguins holding at ~4.5 ETH floor. D3lMundos pumped 138% with whale buying.

**Bitcoin Eco:** Taproot Wizards quiet — no major moves.

**Sol Eco:** Backpack TGE coming — 25% supply to community. Mad Lads floor ~$850.

**Notable Mints:**
- Minting Today: [@owlbiteth](https://x.com/owlbiteth) [@popisinger](https://x.com/popisinger)
- Upcoming Mints: [@RokuTrade](https://x.com/RokuTrade) [@BlobaETH](https://x.com/BlobaETH)

### 6. Alpha from Reputable Figures:
- Top calls: @shivst3r all-in on Pudgy expansion — $100K daily revenue
- High-conviction: @aixbt_agent lists bankr, megaeth as best setups
- WL opportunities: @The_sugargirl mentioned RokuTrade utility NFT
- Emerging narratives: AI agents launching tokens autonomously
- Notable warnings: @somanyfigs notes Pudgy floor -82% from ATH

### 7. Extra / Warnings
- Extreme fear index = potential local bottom
- NerdsOnEth reveal issues — floor down 50%

---
*Report time: 00:00 UTC | NFA/DYOR*
```

## On-Demand Analysis Format

When you ask about a specific asset, you get:

```
📊 CT Sentiments:
[4-5 line summary of what CT is saying]

📈 Overall: [Bullish/Bearish/Neutral]

🐋 Takes of High-Rep Accounts:
[@username: "their take" — Bullish/Bearish]
[Or: No noticeable activity — Bearish]

⚠️ Red Flags:
[Any issues found]

📊 Score: XX/100

✅ Verdict: [High/Medium/Low confidence — Sentiment]

⚡ NFA / DYOR
```

## How It Works

**Stack:**
- `bird` — X/Twitter CLI by founder of OpenClaw (install separately, no API costs)
- `x-alpha-scout` skill — The playbook for what to scan and how to format
- Your agent's reasoning — Parses and structures the alpha

Bird is NOT pre-installed with OpenClaw. Install it via brew or download from releases. Your agent brings its own X credentials, you bring the intelligence.

No Twitter API costs. No rate limits. Just raw alpha.

## License

MIT — Use it, fork it, build on it.

---

Built for the agent economy. 🦅
