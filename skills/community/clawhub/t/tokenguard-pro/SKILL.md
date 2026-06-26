---
name: tokenguard-pro
description: "Token cost optimizer for OpenClaw agents. Scan usage patterns, identify waste (excessive context, repeated queries, inefficient tool use), and get actionable recommendations to cut AI costs by 50-95%. Use when: monthly API spend exceeds $100, reviewing agent efficiency, or optimizing high-volume workflows. NOT a replacement for budget controls."
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "price": 49,
        "requires": { "bins": ["bash", "jq"] },
        "author": "App Incubator",
        "category": "productivity",
      },
  }
---

# TokenGuard Pro 🛡️

**Cut your AI token costs by 50-95% without sacrificing output quality.**

TokenGuard Pro analyzes your OpenClaw usage patterns to identify waste, suggest optimizations, and project your savings. Built for users spending $100–$3,600/month on AI APIs.

## What It Does

- **Scans** your session logs for token consumption patterns
- **Identifies** waste: oversized contexts, repeated queries, model mismatches, inefficient tool chains
- **Recommends** specific optimizations with estimated savings
- **Generates** a detailed cost-reduction report

## Installation

```bash
npx clawhub install tokenguard-pro
```

## Quick Start

```bash
# Run full analysis on recent usage
tokenguard-analyze

# Analyze last 7 days
tokenguard-analyze --days 7

# Focus on specific waste type
tokenguard-analyze --focus caching

# Export report as JSON
tokenguard-analyze --format json --output report.json
```

## When to Use

✅ **Use this skill when:**

- Monthly API costs exceed $100
- You suspect context bloat in long conversations
- Same queries repeat across sessions
- You're using expensive models for simple tasks
- Agents chain too many tool calls unnecessarily

❌ **Don't use this skill when:**

- Costs are already minimal (<$50/month) — overhead not worth it
- You need real-time budget enforcement — use API provider controls
- Looking for fine-grained per-request pricing — check provider dashboards

## Common Optimizations Found

| Waste Type | Typical Savings | Fix Complexity |
|------------|-----------------|----------------|
| Oversized context | 40-60% | Easy |
| Wrong model choice | 20-40% | Easy |
| Repeated queries | 15-30% | Medium |
| Inefficient tool chains | 10-25% | Medium |
| Missing response caching | 25-50% | Medium |

## Example Report Output

```
╔══════════════════════════════════════════════════════════╗
║              TOKENGARD PRO ANALYSIS REPORT               ║
╠══════════════════════════════════════════════════════════╣
║  Period Analyzed: 14 days                                ║
║  Estimated Monthly Spend: $1,240                         ║
╠══════════════════════════════════════════════════════════╣
║  TOP ISSUES FOUND:                                       ║
║  1. GPT-4 used for 78% of simple classification tasks    ║
║     → Switch to GPT-3.5: SAVE ~$420/mo                   ║
║  2. Average context size 8.2K tokens (recommend: 2K)     ║
║     → Prune old messages: SAVE ~$310/mo                  ║
║  3. 23 repeated API calls without caching                ║
║     → Add response caching: SAVE ~$180/mo                ║
╠══════════════════════════════════════════════════════════╣
║  PROJECTED SAVINGS: $910/month (73% reduction)           ║
╚══════════════════════════════════════════════════════════╝
```

## Limitations

- Analyzes historical patterns, not real-time spend
- Estimates based on standard pricing; actual rates may vary
- Cannot modify your code — provides recommendations only
- Requires access to OpenClaw logs for analysis

## Pricing

**$49 one-time purchase** — pays for itself if it saves you just one month of excess spend.

## Support

Questions? File an issue at github.com/appincubator/tokenguard-pro
