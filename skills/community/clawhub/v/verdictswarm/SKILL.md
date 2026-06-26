---
name: verdictswarm
description: "Fight AI with AI. 6 adversarial AI agents debate crypto token risk before your agent trades. Rug-pull detection, security audits, consensus scoring via MCP."
triggers:
  - scan token
  - analyze crypto
  - is this token safe
  - token risk
  - crypto analysis
  - should I buy this token
  - check this token
  - rug pull check
requires:
  - network: "https://api.vswarm.io"
---

# VerdictSwarm — Multi-Agent Token Intelligence

**Get a second, third, fourth, fifth, and sixth opinion on any crypto token.**

Six specialized AI agents independently analyze your token from different angles, then debate their findings across multiple rounds before reaching consensus. You see the full analysis and any disagreements.

> "What do you think of this token?" → 6 agents analyze → Consensus reached → You decide

**Free tier available.** 10 quick scans per day, no API key needed.

## How It Works

Each agent specializes in a different aspect of token analysis:

| Agent | Focus Area |
|-------|-----------|
| Security Bot | Smart contract permissions, mint/freeze authority, honeypot detection |
| Tokenomics Bot | Supply mechanics, holder concentration, distribution |
| Social Bot | Community signals, social presence, engagement patterns |
| Technical Bot | On-chain metrics, liquidity analysis, trading patterns |
| Macro Bot | Market context, comparative analysis, sector trends |
| Devil's Advocate | Challenges every verdict, finds what others missed |

## MCP Tools

Install via MCP for agent integration:

```bash
pip install verdictswarm-mcp
```

| Tool | Description |
|------|-------------|
| `scan_token` | Full 6-agent consensus risk scan |
| `get_quick_score` | Fast cached score (0-100) for pre-trade screening |
| `check_rug_risk` | Rug-pull focused security check (SAFE/CAUTION/DANGER) |
| `get_token_report` | Shareable markdown report |
| `get_pricing` | View pricing and Solana payment details |
| `verify_payment` | Verify USDC payment on Solana |

## Quick Start (API)

```bash
curl -s "https://api.vswarm.io/api/scan/quick" \
  -H "Content-Type: application/json" \
  -d '{"address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", "chain": "solana"}'
```

## Scoring Guide

- 80-100: LOW risk (Grade A)
- 70-79: LOW-MEDIUM (Grade B)
- 60-69: MEDIUM (Grade C)
- 40-59: HIGH (Grade D)
- 0-39: CRITICAL (Grade F)

## Pricing

| Tier | Cost | Details |
|------|------|---------|
| **Free** | $0 | 10 quick scans/day |
| **Quick Scan** | 0.02 USDC | Cached score + metadata |
| **Rug Check** | 0.05 USDC | Security-focused verdict |
| **Full Scan** | 0.10 USDC | All 6 agents, full debate |

Pay per scan with USDC on Solana, or use a free API key from vswarm.io.

## Supported Chains

Solana, Ethereum, Base, BSC

## Agent Instructions

When the user asks to analyze or check a crypto token, use the MCP tools (preferred) or call the API directly. Present the verdict score, risk level, and consensus summary. If agents disagreed, highlight the differences. Include the report URL for the full breakdown.
