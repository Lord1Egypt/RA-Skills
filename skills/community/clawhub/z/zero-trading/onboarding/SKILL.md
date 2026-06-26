---
name: zero-onboarding
description: "onboard a new operator to zero. first session, first evaluation, first trade."
---

# onboarding flow

when operator says "set me up on zero" or similar:

## step 1: connect (3 seconds)

call `zero_get_engine_health`.
- returns "operational": proceed immediately. don't narrate the check.
- returns error: "engine offline. check MCP config: url should be https://api.getzero.dev/mcp"

## step 2: show the market (10 seconds)

send heat card image with caption:
"50 coins. [X] trending short. [Y] trending long. fear & greed: [Z]."

```
buttons:
  row 1: [▶ Deploy Now | deploy_momentum_paper] [📊 See Strategies | list_strategies]
```

this is the "wow" moment. the operator sees the engine is ALREADY watching 50 markets. no setup needed.

## step 3: check for active session

call `zero_session_status` FIRST.
- if a session is already active: "you have [strategy] running."
  show session status + buttons: [📊 Status | session_status] [⏹ End | end_session]
- if no session: proceed to deploy.

## step 4: deploy (5 seconds)

before deploying, confirm with buttons:

```
message: "momentum. paper mode. 48 hours. 5 positions max. 3% stops."
buttons:
  row 1: [▶ Deploy Paper | deploy_momentum_paper] [📊 Preview Risk | preview_momentum]
  row 2: [📋 Other Strategies | list_strategies] [✗ Cancel | cancel_deploy]
```

on `deploy_momentum_paper`: call `zero_start_session("momentum", paper=True)`.
on `preview_momentum`: call `zero_preview_strategy("momentum")` and show risk math.
on `list_strategies`: call `zero_list_strategies` and show all options with backtest results if available.
on `cancel_deploy`: "no problem. say 'deploy' when you're ready."

- if deploy succeeds:
  1. delete the "deploy?" confirmation message (stale buttons)
  2. "session live. momentum. paper mode. 50 markets. every 60 seconds."
- if plan error: "that strategy needs a higher plan. try momentum (free)."
- if already active: go back to step 3.

## step 5: show the engine thinking (10 seconds)

pick the highest conviction coin from heat map.
send eval card image with caption:
"[COIN]: [X]/9 [DIRECTION]. [passing layers] pass. [failing layers] block."

then send radar card image with caption:
"9-layer breakdown. filled = passing."

then explain briefly:
"9 layers. every coin. every minute.
5 must pass for momentum. most coins get 2-3.
layer 8 (LLM) is conditional — only fires when mechanical layers pass. not every eval includes it.
when one breaks through — that's the trade."

## step 6: set expectations (5 seconds)

send funnel card image with caption:
"97% rejected. 3% became trades. patience is the product."

```
buttons:
  row 1: [📡 Approaching | show_approaching] [🔥 Heat Map | show_heat]
```

if approaching has coins: show them. "these are forming right now."
if empty: "nothing forming. engine is selective. that's the point."

## step 7: hand off (3 seconds)

send mode card image with caption:
"3 drive modes. you're on comfort. upgrades available."

```
message: "you're set up. here's what happens next:
• i push you a card when a position enters or exits
• morning brief every day at 08:00
• approaching alerts when coins near threshold
• silence means i'm watching. no news is good news.
• your agent has a public profile: getzero.dev/agent/{id}
• share it to show your track record

drive modes:
• comfort (default) — set it and forget it
• sport — full narration, see the engine thinking
• track — you approve every trade manually"
buttons:
  row 1: [📊 Status | session_status] [🔥 Heat Map | show_heat] [📡 Approaching | show_approaching]
  row 2: [🏎 Sport Mode | set_mode_sport] [🏁 Track Mode | set_mode_track] [👤 Profile | show_profile]
```

total onboarding: 7 steps. 5 images. 36 seconds of operator time.
they're deployed and understand the philosophy.

## key principles

- show, don't tell. images first, text second.
- every step has buttons. the operator taps, not types.
- the heat card is the hook. "50 coins being watched" is the selling moment.
- the funnel is the philosophy. "97% rejected" explains why this isn't another trading bot.
- hand off with a promise: "i'll push you cards." then actually do it (card_push.py handles this).
