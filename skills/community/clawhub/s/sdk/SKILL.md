---
name: edgebets
description: AI-powered sports betting simulations with Monte Carlo analysis
version: 1.0.0
author: EdgeBets
tags:
  - sports
  - betting
  - simulation
  - monte-carlo
  - nba
  - nfl
  - mlb
  - mls
  - x402
  - solana
requires:
  env:
    - SOLANA_PRIVATE_KEY
  bins:
    - node
---

# EdgeBets Sports Simulation

Run professional-grade Monte Carlo simulations for sports betting analysis. Get win probabilities, projected scores, spread predictions, and edge detection for NBA, NFL, MLB, and MLS games.

## Quick Start

```bash
npm install edgebets-sdk
```

```javascript
import { createClient } from 'edgebets-sdk';

const client = createClient(JSON.parse(process.env.SOLANA_PRIVATE_KEY));

// Get today's games (FREE)
const games = await client.getGames('nba');

// Run simulation ($0.50 USDC)
const result = await client.simulate('nba', games[0].id);
```

## When to Use This Skill

Use EdgeBets when the user asks about:
- Sports game predictions or analysis
- Win probabilities for upcoming games
- Betting odds comparison and value detection
- Monte Carlo simulations for sports
- NBA, NFL, MLB, or MLS game analysis
- **Pick of the day** or daily betting picks
- Track record of past picks

## Available Actions

### 1. Browse Today's Games (FREE)

Show available games without any payment required.

**Trigger phrases:**
- "What NBA games are on today?"
- "Show me today's NFL matchups"
- "List MLS games"
- "What baseball games are playing?"

**Response format:**
```
Today's NBA Games:
1. Lakers vs Celtics - 7:30 PM ET
2. Warriors vs Suns - 10:00 PM ET
...
```

### 2. Run Simulation ($0.50 USDC)

Execute 10,000 Monte Carlo simulations with full analysis.

**Trigger phrases:**
- "Simulate the Lakers game"
- "Run analysis on game 1"
- "What are the odds for Warriors vs Suns?"
- "Analyze the Chiefs game"

**Response format:**
```
Simulation Results: Lakers vs Celtics

Win Probabilities:
- Lakers: 45.2%
- Celtics: 54.8%

Projected Score: Lakers 108 - Celtics 112
Projected Total: 220 points
Predicted Spread: Celtics -4

Edge Analysis:
- Value detected on Lakers ML (+3.2% edge)
- Kelly recommends 2.1% bankroll
```

### 3. Get Pick of the Day (FREE)

Get the daily expert pick with analysis. No payment required.

**Trigger phrases:**
- "What's the pick of the day?"
- "Give me today's pick"
- "What should I bet on today?"
- "Show me the daily pick"

**Response format:**
```
Pick of the Day: Lakers ML

Game: Celtics @ Lakers - 7:30 PM ET
Pick: Lakers Moneyline (-110)
Confidence: HIGH
Win Probability: 58.2%
Edge vs Market: +4.1%

Analysis: Lakers are 8-2 at home in their last 10...
```

**If game already played:**
```
Today's pick (Lakers ML) has been graded: WIN
New pick available at 2 AM Central.
```

### 4. Get Track Record (FREE)

View the historical performance of daily picks.

**Trigger phrases:**
- "What's your track record?"
- "How are the picks doing?"
- "Show me past picks"

**Response format:**
```
Track Record: 45-32-3 (58.4%)
Current Streak: 4W
Recent: W W W W L W L W
```

### 5. Check Balance

Verify USDC balance before running simulations.

**Trigger phrases:**
- "Check my balance"
- "Do I have enough for a simulation?"

## Payment Information

- **Cost:** $0.50 USDC per simulation
- **Network:** Solana mainnet
- **Protocol:** x402 (automatic with SDK)

## Environment Setup

Set your Solana wallet private key:

```bash
export SOLANA_PRIVATE_KEY='[your_private_key_array]'
```

The wallet needs:
- At least $0.50 USDC for each simulation
- Small amount of SOL for transaction fees (~0.001 SOL)

## API Reference

### Get Games
```javascript
// Today's games
const games = await client.getGames('nba');

// Tomorrow's games
const tomorrow = await client.getTomorrowGames('nfl');

// Specific game
const game = await client.getGameDetails('mlb', 'mlb-2026-03-28-nyy-bos');
```

### Run Simulation
```javascript
const result = await client.simulate('nba', gameId, {
  onStatus: (status) => console.log(status), // 'paying', 'processing', 'complete'
});

// Result includes:
// - homeWinProbability, awayWinProbability
// - averageHomeScore, averageAwayScore
// - predictedSpread, averageTotalPoints
// - edgeAnalysis (value detection)
// - bettingInsights (fair odds)
// - factorBreakdown (what's driving the prediction)
```

### Check Balance
```javascript
const balance = await client.checkBalance();
// { usdc: 5.25, sol: 0.05, sufficient: true }
```

### Get Pick of the Day
```javascript
const pick = await client.getTodaysPick();
// {
//   hasPick: true,
//   isTodaysPick: true,
//   pick: {
//     sport: 'nba',
//     pick: 'Lakers',
//     pickType: 'moneyline',
//     winProbability: 0.582,
//     confidence: 'high',
//     result: 'pending'  // or 'win', 'loss', 'push'
//   },
//   message: null,
//   nextPickTime: null
// }

// If game already played:
// {
//   hasPick: true,
//   pick: { ... result: 'win' ... },
//   message: "Today's pick has been graded: WIN. New pick at 2 AM Central.",
//   nextPickTime: "2:00 AM Central"
// }
```

### Get Track Record
```javascript
const record = await client.getTrackRecord();
// {
//   wins: 45,
//   losses: 32,
//   pushes: 3,
//   winRate: 58.4,
//   streak: 4,
//   streakType: 'W',
//   recentPicks: [...]
// }
```

## Supported Sports

| Sport | Code | Endpoint |
|-------|------|----------|
| NBA | `nba` | Basketball |
| NFL | `nfl` | Football |
| MLB | `mlb` | Baseball |
| MLS | `mls` | Soccer |

## Links

- Website: https://edgebets.fun
- API Docs: https://api.edgebets.fun/api/v1/x402
- OpenAPI Spec: https://api.edgebets.fun/api/v1/x402/openapi.json
- npm Package: https://www.npmjs.com/package/edgebets-sdk
