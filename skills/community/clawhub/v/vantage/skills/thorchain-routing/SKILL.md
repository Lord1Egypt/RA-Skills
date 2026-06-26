# THORChain Routing Skill
Version: 0.1.0
Author: MoreBetter Studios
Description: Cross-chain swap routing via THORChain for AI trading agents (Hyperliquid, SenpiAI ecosystem)

## Commands
- `thor-quote <fromAsset> <toAsset> <amount>` — Get swap quote from THORChain
- `thor-scan [tokens]` — Scan ecosystem for routing opportunities
- `thor-inbound` — Get THORChain inbound addresses for all supported chains

## Asset Format
BTC.BTC, ETH.ETH, THOR.RUNE, ETH.USDC-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48

## Install
```bash
cp -r skills/thorchain-routing ~/.openclaw/skills/thorchain-routing
```

## Publish to ClawHub
```bash
clawhub publish skills/thorchain-routing
```

## Integration with SenpiAI
This skill is designed for the SenpiAI Hyperliquid agent ecosystem.
When a Hyperliquid agent needs cross-chain exposure:
1. Call `thor-quote` to get optimal route
2. Use `thor-inbound` to find deposit address
3. Execute swap via THORChain memo protocol

## Roadmap
- v0.2.0: Real-time price monitoring
- v0.3.0: Chainflip + NEAR Intents multi-route comparison
- v1.0.0: Full ClawHub marketplace listing with creator fees
