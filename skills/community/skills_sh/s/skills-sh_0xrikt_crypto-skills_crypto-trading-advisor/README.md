# Crypto Trading Advisor

A Claude Skill for cryptocurrency trading analysis.

## Quick Install

```bash
npx @0xrikt/crypto-trading-advisor
```

This will download the skill file and guide you through installation.

## What is this?

This is a [Claude Skill](https://claude.ai) that helps Claude provide professional crypto trading analysis when users ask questions like:

- "Is BTC a good trade right now?"
- "Can I long SOL here?"
- "What's the setup for ETH?"
- "Should I enter this trade?"

## What it provides

**1. High-value data sources** — Where to find funding rates, on-chain flows, TVL, whale movements, liquidation heatmaps, etc.

**2. Trading principles** — Analysis framework, signal priority, contrarian checkpoints, risk management, cognitive bias checks.

**3. Output principles** — Lead with conclusion, be specific with data, talk like a trader not an AI.

## Manual Installation

1. Download `SKILL.md` from this repository
2. Go to [Claude Settings → Skills](https://claude.ai/settings/skills)
3. Click "Add Skill"
4. Paste the content and save

## Example

> **User**: Can I long SOL here?
>
> **Claude**: *(fetches fear/greed index, funding rates, on-chain data, news...)*
> 
> 🎯 **Light long, don't size up**
> 
> Fear/Greed at 62 (Greed zone), funding +0.01% (neutral-bullish), 7-day exchange net outflow $89M (bullish signal). Daily just broke previous high, but volume is meh.
>
> Entry $175-178 | Stop $168 (-4%) | Target $195 (+10%) | R:R 2.5:1
>
> ⚠️ Invalidated below $168. If BTC loses $100k, reassess everything.

## License

MIT
