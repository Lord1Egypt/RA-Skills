---
name: github-bounty-hunter
description: Find legitimate GitHub bounties by filtering out farm/scam repositories, tracking competition, and monitoring payment history. Use when you need to discover real bounty opportunities on GitHub.
metadata:
  openclaw:
    version: "1.0.0"
    author: xiaomomini
    tags: [github, bounty, automation, opportunity-discovery]
---

# GitHub Bounty Hunter

A skill for finding legitimate GitHub bounty opportunities by filtering out farm/scam repositories and tracking competition.

## What This Skill Does

1. **Scans GitHub** for bounty opportunities using multiple search strategies
2. **Filters out farms/scams** using known patterns (AgentOrchestration, RustChain, etc.)
3. **Tracks competition** by counting comments, PRs, and claims
4. **Monitors payment history** by checking for "paid" labels and tx hashes
5. **Reports viable opportunities** with clear scoring

## Usage

### Basic Scan

Ask your agent to scan for bounties:

```
Scan GitHub for legitimate bounty opportunities
```

### Filtered Scan

Specify your criteria:

```
Find JavaScript bounties under $200 with less than 5 comments
```

### Competition Check

Check a specific bounty:

```
Check competition for https://github.com/owner/repo/issues/123
```

### Payment History

Check if a project pays:

```
Check payment history for owner/repo
```

## How It Works

### Farm/Scam Detection

The skill maintains a list of known farm/scam patterns:

- **AgentOrchestration**: 2310+ issues, only bot contributor, requires star
- **RustChain**: Token has no market value, closed without merge
- **Generic farms**: High issue count, low contributor count, unclear payment

### Competition Scoring

Bounties are scored based on:

| Factor | Weight | Low Competition | High Competition |
|--------|--------|-----------------|------------------|
| Comments | 40% | <5 | >10 |
| PRs | 30% | <3 | >5 |
| Claims | 20% | <2 | >5 |
| Age | 10% | <7 days | >30 days |

### Payment Verification

Checks for:

- "paid" label on issue
- Comments with tx hash or payment confirmation
- Maintainer response confirming payment
- Historical payment patterns

## Search Strategies

### 1. Label-Based Search

```
label:bounty language:JavaScript created:>2026-05-15
label:"good first issue" language:Python created:>2026-05-15
label:sponsored language:TypeScript created:>2026-05-15
```

### 2. Platform-Specific Search

```
org:algora-io is:issue is:open
org:opire is:issue is:open
```

### 3. Keyword Search

```
"bounty" OR "reward" OR "payment" in:readme language:JavaScript
```

## Output Format

```json
{
  "opportunities": [
    {
      "url": "https://github.com/owner/repo/issues/123",
      "title": "Fix bug in component",
      "reward": "$100",
      "language": "JavaScript",
      "competition": {
        "comments": 2,
        "prs": 0,
        "score": "LOW"
      },
      "payment": {
        "verified": true,
        "method": "USD/Stripe"
      },
      "feasibility": "HIGH"
    }
  ],
  "filtered": {
    "farms": 15,
    "scams": 8,
    "high_competition": 12
  }
}
```

## Configuration

### Custom Filters

Add custom farm/scam patterns:

```
Add "suspicious-repo" to my farm list
```

### Platform Preferences

Set preferred platforms:

```
Only show bounties from Algora and Opire
```

### Reward Thresholds

Set minimum/maximum rewards:

```
Only show bounties between $50 and $500
```

## Best Practices

1. **Verify before claiming**: Always check competition and payment history
2. **Start small**: Begin with lower-value bounties to build reputation
3. **Track payments**: Monitor for "paid" labels and tx hashes
4. **Avoid farms**: If it looks too good to be true, it probably is
5. **Check activity**: Ensure the project is actively maintained

## Known Limitations

- Cannot verify off-chain payments (PayPal, bank transfer)
- Cannot access private repositories
- Cannot verify token-based payments without blockchain explorer
- Farm/scam list needs manual updates

## Support

For issues or feature requests, contact @xiaomomini on GitHub.
