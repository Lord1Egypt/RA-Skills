---
name: zero-session-management
description: "deploy, monitor, end, and queue trading sessions. manage the session lifecycle."
---

# session management

## before deploying: always check first

call `zero_session_status` BEFORE starting anything.
- if a session is active: "you have [strategy] running. want to check status or end it first?"
- if no session: proceed to deploy.

ONE session at a time. attempting to start a second will be rejected.

## deploying a session

1. call `zero_preview_strategy("momentum")` — show risk math to operator
2. confirm with buttons:

```
message: "momentum. 5 positions max. 3% stops. 48 hours. paper mode."
buttons:
  row 1: [▶ Deploy Paper | deploy_momentum_paper] [💰 Deploy Live | deploy_momentum_live]
  row 2: [📊 Preview Risk | preview_momentum] [✗ Cancel | cancel_deploy]
```

3. on `deploy_*_paper`: call `zero_start_session("momentum", paper=True)`
4. on `deploy_*_live`: call `zero_start_session("momentum", paper=False)` — warn first: "live mode. real money. confirm?"
5. if success: "session deployed. momentum surf. paper mode. ends in 48h."
6. if plan error: "that strategy needs a higher plan. try momentum (free)."
7. if already active: "a session is already running. end it first or queue this one."
8. if any other error: report the exact error to operator. don't guess.

never deploy without operator confirmation via button or explicit text.
always show risk parameters BEFORE deploying.
always start in paper mode unless operator explicitly says "live" or "real money."

## monitoring active session

call `zero_session_status` periodically (every 15-30 min during active hours).

note: `eval_count` and `reject_count` in session status may show 0 if the supervisor is running evaluations independently. this is normal — the engine evaluates via its own cycle, not through the API session object. check `zero_get_pulse` for actual evaluation activity, or count positions/trades as proof the engine is working.

when reporting status, include buttons:

```
message: "[session status summary]"
buttons:
  row 1: [🔥 Heat Map | show_heat] [📡 Approaching | show_approaching]
  row 2: [⏹ End Session | end_session] [📋 Queue Next | queue_session]
```

report changes:
- new position opened: "entered SOL short at $85.07. 5/9 consensus. trending." + eval card image
- position closed: "SOL closed +$2.40 (+2.8%). trailing stop locked profits."
- position stopped: "stop worked. SOL -$1.60 (-1.3%)."

note: say "stop worked" not "sorry about the loss." stops are protection, not failure.

don't report if nothing changed. silence means the engine is watching.

## checking approaching

call `zero_get_approaching` to narrate what's forming.
"BTC at 4/9. book depth is the bottleneck. watching."

if approaching returns empty: "nothing forming. engine is selective."
this keeps the operator engaged between trades.

## ending a session

call `zero_end_session` when:
- operator asks to stop
- market conditions changed dramatically
- daily loss limit approaching

if no session is active: "no session running. nothing to end."

send the result card image with caption that includes session comparison data:
"momentum session #8. +$3.40 (avg: +$2.10). your best yet."
"[strategy] complete. [trades] trades. [P&L]. [rejection_rate]% rejected."

session_result is enhanced with comparison data from PatternEngine.compare_session().

delete the "deploy?" confirmation message if it still exists (cleanup stale buttons).

then ask what's next using a poll:
```
poll:
  question: "what next?"
  options:
    - "momentum (trend following)"
    - "defense (capital protection)"
    - "degen (high conviction)"
    - "let the engine decide"
  anonymous: false
```

## auto-pilot (let the engine decide)

when operator picks "let the engine decide" in post-session poll:

1. call `zero_auto_select`
2. show the decision with explanation:
   "engine recommends [strategy]. [reason]. confidence: [confidence]%."
3. show autopilot card image
4. deploy with buttons:

```
message: "engine recommends [strategy]. [reason]."
buttons:
  row 1: [▶ Deploy | deploy_auto] [✗ Override | list_strategies]
```

on `deploy_auto`: call `zero_start_session(decision.strategy, paper=True)`
on `list_strategies`: show full strategy list for manual selection.

if `auto_rotate` is enabled on the session config, skip the poll and auto-deploy:
- call `zero_auto_select`
- auto-deploy the recommended strategy (paper mode)
- push result to operator: "auto-rotating to [strategy]. [reason]."

also show buttons for report actions:
```
buttons:
  row 1: [📊 Full Report | show_result] [📈 Equity Curve | show_equity]
  row 2: [📜 History | show_history]
```

include near misses: "degen would have caught AVAX +6.8%."

if narrative sounds generic ("0 evaluations. Pure observation."), rewrite it: "ran for [actual duration]. market was quiet — nothing met the threshold. the engine was selective, not idle." don't relay raw generic narratives.

## queuing sessions

call `zero_queue_session("defense")` to queue the next session.
"defense queued. starts when current session completes."

useful for overnight: "deploy momentum now. queue defense for overnight."

## session history

call `zero_session_history` to review past performance.
"your last 5 sessions: 3 profitable, 2 flat. best: degen +12.4%."
if history is empty: "no sessions yet. deploy your first one."

## auto-recovery

if the circuit breaker triggers during a session:
- engine auto-deploys defense strategy with 24h cooldown
- existing positions remain protected (stops still active)
- operator is notified: "circuit breaker triggered. auto-deploying defense to protect capital."
- after 24h cooldown, operator can deploy a new strategy manually

## evolved strategy variants

some strategies have evolved versions with improved parameters discovered through backtesting. when deploying, check `zero_get_evolution_status` — if an evolved variant exists for the selected strategy, inform the operator:
"evolved momentum variant available. sharpe improved. approve to promote?"

evolved variants must be explicitly approved before they replace the base strategy.

## key rules

- ONE session at a time. always check status first.
- paper mode is the default. live mode requires explicit approval.
- session has a timer. momentum = 48h. degen = 24h. defense = 168h.
- session can be ended early at any time.
- queued sessions auto-start when current session completes.
