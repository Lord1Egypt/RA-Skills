---
name: vig-calculator
description: "Calculate vig (juice/overround/hold) for any sportsbook market. Convert odds to no-vig fair lines. Rank books by efficiency. Use when asked about vig, juice, hold percentage, overround, or sportsbook sharpness."
metadata:
  openclaw:
    emoji: "🧮"
    requires:
      bins: ["python3"]
---

# Vig Calculator

Calculate the vig (juice/overround) for any sportsbook market and rank books by efficiency.

## When to Use

Use this skill when the user asks about:
- Vig, juice, or overround on a market
- Hold percentage for a sportsbook
- Removing vig to find fair/true odds
- Ranking sportsbooks by efficiency or sharpness
- Which book has the lowest juice
- The AgentBets Vig Index

## Operations

### 1. Calculate Vig for a Two-Way Market

Given American odds for both sides:

```python
python3 -c "
import sys
odds = [int(x) for x in sys.argv[1:]]
probs = []
for o in odds:
    if o < 0:
        probs.append(abs(o) / (abs(o) + 100))
    else:
        probs.append(100 / (o + 100))
total = sum(probs)
vig = (total - 1) * 100
hold = (1 - 1/total) * 100
print(f'Implied probs: {[round(p*100,2) for p in probs]}%')
print(f'Sum: {round(total*100,2)}%')
print(f'Vig (overround): {round(vig,2)}%')
print(f'Hold: {round(hold,2)}%')
fair = [round(p/total*100,2) for p in probs]
print(f'No-vig fair probs: {fair}%')
" ODDS_SIDE_A ODDS_SIDE_B

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-vig-calculator-skill/](https://agentbets.ai/guides/openclaw-vig-calculator-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
