---
name: polymarket-sports-arbitrage
description: >
  Scans sports odds from traditional bookmakers (via The Odds API) to detect arbitrage
  opportunities — situations where two bookmakers offer contradictory odds on the same
  match, guaranteeing profit regardless of outcome. Computes implied probabilities,
  detects arb condition (sum < 1), calculates optimal stake split, and filters only
  opportunities above 0.5% profit. Source: The Odds API (https://the-odds-api.com),
  free tier with automatic demo fallback when no key is provided. Saves results to
  /tmp/sports_arb_results.json. No connection to Polymarket — slug reflects author
  namespace convention only.
metadata:
  author: Mibayy
  version: 1.0.1
  displayName: Sports Arbitrage Scanner
  difficulty: intermediate
  type: automaton
  source: https://the-odds-api.com
---

# Sports Arbitrage Scanner

A ClawHub automaton skill that continuously monitors sports betting odds from multiple
bookmakers, identifies arbitrage opportunities, and reports guaranteed-profit trade setups.

## How Arbitrage Works

An arbitrage opportunity exists when the sum of implied probabilities across all outcomes
of a match (using the best available odds from any bookmaker) is less than 1.0. This means
you can stake proportionally on all outcomes and lock in a profit no matter who wins.

  Implied probability of outcome = 1 / decimal_odds
  Arb exists when: sum(1/odds_i for all outcomes) < 1.0
  Profit % = (1 - sum_of_implied_probs) / sum_of_implied_probs * 100
  Stake for outcome i = (total_stake / odds_i) / sum_of_implied_probs

## Environment Variables

  ODDS_API_KEY  (optional)
    API key for The Odds API (https://the-odds-api.com).
    Free tier allows ~500 requests/month. If not set, the skill falls back to
    built-in sample/demo data so it can still demonstrate functionality.

  MIN_PROFIT_PCT  (optional, default: 0.5)
    Minimum profit percentage to report. Arbs below this threshold are silently
    filtered out. Increase to reduce noise, decrease to surface more marginal arbs.

  TOTAL_STAKE  (optional, default: 1000)
    Hypothetical total stake amount (in your currency) used to compute the
    concrete stake split per outcome. Purely illustrative — adjust to your bankroll.

  SPORTS  (optional, default: soccer_epl,basketball_nba,americanfootball_nfl)
    Comma-separated list of sport keys to scan. Valid sport keys are documented at
    https://the-odds-api.com/sports-odds-data/sports-apis.html

  RESULTS_FILE  (optional, default: /tmp/sports_arb_results.json)
    Path where the JSON results file is written after each scan run.

## Output

Each detected arbitrage opportunity is logged to stdout and appended to the JSON
results file. The JSON schema per opportunity:

  {
    "match": "Team A vs Team B",
    "sport": "soccer_epl",
    "commence_time": "2026-03-21T15:00:00Z",
    "profit_pct": 1.23,
    "total_implied_prob": 0.9879,
    "outcomes": [
      {
        "name": "Team A",
        "bookmaker": "pinnacle",
        "odds": 2.10,
        "implied_prob": 0.4762,
        "stake": 476.19,
        "potential_return": 1000.00
      },
      ...
    ],
    "total_stake": 1000,
    "guaranteed_return": 1012.30,
    "detected_at": "2026-03-21T03:00:00Z"
  }
