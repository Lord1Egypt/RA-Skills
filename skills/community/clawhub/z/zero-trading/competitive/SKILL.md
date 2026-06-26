---
name: zero-competitive
version: "2.0"
description: "arena leaderboard, rivalry system, seasonal play, and chain progress."
triggers:
  - "leaderboard"
  - "arena"
  - "ranking"
  - "rival"
  - "who's ahead"
  - "my rank"
  - operator asks about competition or ranking
---

# competitive features

## constraints

- NEVER fabricate leaderboard data. always call the tool.
- ALWAYS show rank change after sessions in sport/track mode.
- chains and seasons are Phase 4 — acknowledge they're coming, use live tools instead.

## steps

### 1. arena leaderboard

1. call `zero_get_arena`
2. report: top 10 agents with rank/class/score/WR/streak, operator's rank and percentile, network stats
3. after session ends (sport/track mode): "moved up [N] spots. now #[rank] of [total] agents."
4. show buttons: `[📊 Leaderboard | show_leaderboard]`

### 2. rivalry

1. call `zero_get_rivalry`
2. report side-by-side: score, WR, sessions, streak, strategy
3. "beat them by [X] points to move up."
4. green/red indicators for where operator is ahead/behind
5. if rank #1: rivalry returns null — no one above you
6. show buttons: `[📊 Rivalry Card | show_rivalry]`

### 3. chains

1. call `zero_get_chain` (scale tier)
2. chain rewards: 3 profitable sessions = bronze, 5 = silver, 10 = gold
3. breaking a chain = badge, not punishment

### 4. seasonal play (Phase 4)

1. seasons last 90 days. rankings reset.
2. top 10 at end of season earn permanent badges.
3. not yet active — acknowledge and move on.

## error handling

| error | response |
|---|---|
| arena returns error | "can't reach leaderboard. try again in a minute." |
| rivalry returns null | "you're #1. no rival above you." |
| chain tool unavailable | "chain tracking requires scale plan." |
| Phase 4 tool returns placeholder | "coming soon. use live tools for now." |

## output format

- **arena**: leaderboard card + caption with rank/percentile + buttons
- **rivalry**: rivalry card + caption with comparison + "beat by X points"
- **chains**: text with chain length + badge tier
