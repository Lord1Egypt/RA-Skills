---
name: zero-pattern-recognition
description: "use discovered patterns from operator history to improve future sessions."
---

# pattern recognition

## status: active

pattern engine analyzes operator session history for personalized insights. requires 5+ completed sessions for insight generation, 3+ for strategy profiles.

## after every session ends

call `PatternEngine.compare_session()` to generate a `SessionComparison`. include in the session result narration:

"momentum session #8. +$3.40 (avg: +$2.10). your best yet."

the comparison includes:
- session number for this strategy
- P&L vs average
- win rate vs average
- rank (top 20%, average, bottom 20%)
- is_best / is_worst flags
- personalized narrative

## insights (5+ sessions)

call `zero_get_insights` to discover operator patterns:

### regime affinity
"you're a trending market trader. WR: 74% in trending, 48% in mixed."
- groups sessions by regime at time of session
- triggers when WR spread across regimes is 15%+

### strategy edge
"momentum is your edge. 72% WR vs 58% average."
- groups by strategy, compares WR
- triggers when one strategy WR is 10%+ above average

### time patterns
"your evening sessions outperform morning by 40%."
- groups by start hour bucket (morning/afternoon/evening/night)
- triggers when $1+ spread in avg PnL

### hold duration
"your 24h sessions outperform 48h. consider degen."
- compares short (<36h) vs long (>=36h) sessions
- triggers when $1+ spread in avg PnL

### loss recovery
"you recover well. sessions after a loss: +$2.40 avg."
- or: "after losses, your next session drops. consider defense."
- tracks performance after losing sessions

## building profile message

when < 5 sessions: "building your profile. [N] more sessions until insights."

## every 5th session

include an insight in the session complete message:
"insight: you're a fear trader. WR is 74% when F&G < 30."

## how to present patterns

don't dump statistics. tell a story:
"i've noticed something across your last 15 sessions.
you're a fear trader. your best results come when everyone else is scared."

## feedback loop weights

layer weights adjust based on your trading history — high-accuracy layers get more influence. the engine tracks which layers correctly predicted winners vs losers across your sessions and rebalances their conviction weight automatically. this means the 9-layer evaluation becomes personalized over time — layers that work for your style carry more weight.

## evolving recommendations

as patterns emerge, adjust strategy selection:
- operator consistently profitable with degen -> recommend more degen
- operator loses on fade -> stop recommending fade
- patterns are personal. the engine is the same. the operator's edge is their own.
