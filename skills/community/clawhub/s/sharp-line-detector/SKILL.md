---
name: sharp-line-detector
description: "Monitor line movements at sharp sportsbooks (Pinnacle, Circa, Bookmaker). Detect steam moves, reverse line movement, and significant implied probability shifts. Use when asked about line movement, sharp money, steam moves, or smart money signals."
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["curl", "jq", "python3"]
    credentials:
      - id: "odds-api-key"
        name: "The Odds API Key"
        description: "Free API key from https://the-odds-api.com/"
        env: "ODDS_API_KEY"
---

# Sharp Line Detector

Monitor line movements at sharp sportsbooks. Detect steam moves, reverse line movement, and smart money signals.

## When to Use

Use this skill when the user asks about:
- Line movement on a game or sport
- Steam moves or sharp action
- Reverse line movement (RLM) signals
- Whether smart money has moved a line
- Pinnacle, Circa, or Bookmaker line changes
- Significant odds shifts since open

## Sharp Book Keys

The skill prioritizes lines from these market-making books (in order of sharpness):

| Book | The Odds API Key | Why It Matters |
|------|-----------------|----------------|
| Pinnacle | pinnacle | Lowest vig, sharpest global market |
| Circa | circasports | Sharpest US book, accepts large limits |
| Bookmaker | bookmaker | Long-standing sharp-friendly book |
| BetOnline | betonlineag | Accepts sharp action, moves early |
| DraftKings | draftkings | High volume, useful as public benchmark |
| FanDuel | fanduel | High volume, useful as public benchmark |

If Pinnacle odds are not available in the API response, fall back to Circa, then Bookmaker.

## Configuration

Environment variables for tuning thresholds (all optional):

- SHARP_SPREAD_THRESHOLD — Minimum spread movement in points to flag (default: 1.5)
- SHARP_ML_THRESHOLD — Minimum moneyline implied probability shift to flag (default: 0.05 = 5%)
- SHARP_SNAPSHOT_DIR — Directory for snapshot files (default: /tmp/openclaw-sharp-snapshots)

## Operations

### 1. Snapshot Current Lines

Capture a timestamped snapshot of current odds from all books for a sport. Stores as JSON for later comparison.

```bash
SPORT_KEY="${SPORT_KEY:-basketball_nba}"
SNAP_DIR="${SHARP_SNAPSHOT_DIR:-/tmp/openclaw-sharp-snapshots}"
mkdir -p "$SNAP_DIR"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

curl -s "https://api.the-odds-api.com/v4/sports/$SPORT_KEY/odds?apiKey=$ODDS_API_KEY&regions=us,eu&markets=h2h,spreads&oddsFormat=american&bookmakers=pinnacle,circasports,bookmaker,betonlineag,draftkings,fanduel" \
  | jq --arg ts "$TIMESTAMP" '{
    timestamp: $ts,
    sport: "'$SPORT_KEY'",
    games: [.[] | {
      id: .id,
      game: "\(.away_team) @ \(.home_team)",
      away: .away_team,
      home: .home_team,
      start: .commence_time,
      books: [.bookmakers[] | {
        key: .key,
        name: .title,
        h2h: [(.markets[] | select(.key=="h2h")).outcomes[] | {team: .name, odds: .price}],
        spread: [(.markets[] | select(.key=="spreads")).outcomes[] | {team: .name, point: .point, odds: .price}]
      }]
    }]
  }' > "$SNAP_DIR/${SPORT_KEY}_${TIMESTAMP}.json"

echo "Snapshot saved: ${SPORT_KEY}_${TIMESTAMP}.json ($(jq '.games | length' "$SNAP_DIR/${SPORT_KEY}_${TIMESTAMP}.json") games)"

## About

Built by [AgentBets](https://agentbets.ai) — full tutorial at [agentbets.ai/guides/openclaw-sharp-line-detector-skill/](https://agentbets.ai/guides/openclaw-sharp-line-detector-skill/).

Part of the [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills) for the [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/).
