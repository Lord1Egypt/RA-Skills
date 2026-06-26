---
name: world-cup-2026-odds
description: "Aggregate FIFA World Cup 2026 odds across sportsbooks and prediction markets. Track outright winner futures, group stage odds, and match lines. Compare Polymarket prices vs traditional book futures. Use when asked about World Cup odds, World Cup winner, or 2026 tournament betting."
metadata:
  openclaw:
    emoji: "🏆"
    requires:
      bins: ["curl", "jq"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# World Cup 2026 Odds Tracker

Aggregate FIFA World Cup 2026 betting odds from sportsbooks and prediction markets into one unified view.

## When to Use

Use this skill when the user asks about:
- World Cup 2026 odds, futures, or predictions
- Who will win the World Cup
- World Cup group stage or knockout match odds
- Comparing sportsbook vs prediction market prices for World Cup outcomes
- Tournament favorites, dark horses, or underdogs
- World Cup betting value or price discrepancies

## Operations

### 1. Outright Winner Futures

Fetch which teams are favored to win the 2026 World Cup across all sportsbooks:

```bash
curl -s "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup_winner/odds?apiKey=$ODDS_API_KEY&regions=us&markets=outrights&oddsFormat=american" \
  | jq '[.[] | {
    market: .away_team // "Outright Winner",
    books: [.bookmakers[] | {
      name: .title,
      selections: [.markets[0].outcomes[] | {team: .name, odds: .price}] | sort_by(.odds) | reverse
    }]
  }] | .[0].books[0].selections[:15] | map({team, odds, implied_prob: (if .odds > 0 then (100 / (.odds + 100) * 100 | round / 100) else (-.odds / (-.odds + 100) * 100 | round / 100) end)})'

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-world-cup-2026-odds-skill/](https://agentbets.ai/guides/openclaw-world-cup-2026-odds-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
