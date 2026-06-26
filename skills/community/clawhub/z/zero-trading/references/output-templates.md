# output templates reference

callback_data mappings, card endpoints, and message format specifications.

## callback_data mappings

| callback_data | action |
|---|---|
| `deploy_momentum_paper` | `zero_start_session("momentum", paper=True)` |
| `deploy_momentum_live` | `zero_start_session("momentum", paper=False)` — confirm first |
| `deploy_defense_paper` | `zero_start_session("defense", paper=True)` |
| `deploy_defense_live` | `zero_start_session("defense", paper=False)` — confirm first |
| `deploy_degen_paper` | `zero_start_session("degen", paper=True)` |
| `deploy_degen_live` | `zero_start_session("degen", paper=False)` — confirm first |
| `deploy_scout_paper` | `zero_start_session("scout", paper=True)` |
| `deploy_funding_paper` | `zero_start_session("funding", paper=True)` |
| `deploy_fade_paper` | `zero_start_session("fade", paper=True)` |
| `deploy_sniper_paper` | `zero_start_session("sniper", paper=True)` |
| `deploy_apex_paper` | `zero_start_session("apex", paper=True)` |
| `deploy_auto` | `zero_start_session(auto_select.strategy, paper=True)` |
| `preview_momentum` | `zero_preview_strategy("momentum")` |
| `preview_[strategy]` | `zero_preview_strategy("[strategy]")` |
| `list_strategies` | `zero_list_strategies` |
| `session_status` | `zero_session_status` + status buttons |
| `end_session` | confirm, then `zero_end_session` |
| `queue_session` | ask which strategy, then `zero_queue_session` |
| `new_session` | go to strategy selection flow |
| `show_heat` | render heat card, send to operator |
| `show_brief` | render brief card, send to operator |
| `show_approaching` | render approaching card, send to operator |
| `show_result` | render result card, send to operator |
| `show_history` | `zero_session_history` |
| `show_regime` | render regime card, send to operator |
| `show_score` | render score card, send to operator |
| `show_milestones` | render milestone card, send to operator |
| `show_streak` | render streak card, send to operator |
| `show_profile` | render profile card, send to operator |
| `show_leaderboard` | render leaderboard card, send to operator |
| `show_rivalry` | render rivalry card, send to operator |
| `show_equity` | `zero_get_equity_curve` |
| `show_diagnostics` | `zero_get_diagnostics` |
| `show_circuit_breaker` | `zero_get_circuit_breaker` |
| `set_mode_comfort` | `zero_set_mode("comfort")` |
| `set_mode_sport` | `zero_set_mode("sport")` |
| `set_mode_track` | `zero_set_mode("track")` |
| `eval_[COIN]` | `zero_evaluate("[COIN]")` + eval card |
| `eval_detail_[COIN]` | `zero_evaluate("[COIN]")` full text breakdown |
| `radar_[COIN]` | render radar chart for [COIN] |
| `cancel_deploy` | "no problem. say 'deploy' when ready." |
| `show_immune` | `zero_get_immune_status` |
| `show_immune_log` | `zero_get_immune_log` |
| `show_evolution` | `zero_get_evolution_status` |

for dynamic callbacks like `eval_SOL`, `eval_BTC`: parse the coin name after `eval_`.

## card endpoints

| endpoint | use case | key fields |
|---|---|---|
| `/v6/cards/eval?coin=SOL` | single coin evaluation | consensus, direction, conviction, 7 layers |
| `/v6/cards/heat` | top coins by conviction | sorted list, direction, conviction |
| `/v6/cards/brief` | morning briefing | fear & greed, positions, approaching count |
| `/v6/cards/approaching` | coins near threshold | bottleneck, velocity, time to threshold |
| `/v6/cards/result?session_id=X` | session summary | P&L, trades, rejection rate, comparison |
| `/v6/cards/equity?session_id=X` | equity curve | session equity over time |
| `/v6/cards/radar?coin=SOL` | 7-layer radar chart | spider polygon, per-layer pass/fail |
| `/v6/cards/gauge?value=50` | fear & greed gauge | gauge visualization |
| `/v6/cards/funnel?session_id=X` | rejection funnel | evaluated → passed → entered pipeline |
| `/v6/cards/regime` | market regime | direction, trending count, fear & greed |
| `/v6/cards/autopilot` | auto-select recommendation | strategy, confidence, regime context |
| `/v6/cards/mode?mode=comfort` | drive mode comparison | 3 modes side by side |
| `/v6/cards/insights` | pattern insights | discovered patterns, regime affinity |
| `/v6/cards/score` | operator score | 5 dimension bars + class |
| `/v6/cards/milestones` | milestone grid | earned/unearned milestones |
| `/v6/cards/streak` | streak card | current, best, badge tier |
| `/v6/cards/profile` | agent profile | public URL, stats, class |
| `/v6/cards/leaderboard` | arena rankings | top 10 + operator rank |
| `/v6/cards/rivalry` | head-to-head | side-by-side comparison |
| `/v6/cards/backtest/summary?days=90` | all-strategy backtest | per-strategy P&L, WR, Sharpe |
| `/v6/cards/backtest/equity?strategy=momentum&days=30` | strategy backtest equity | equity curve over time |
| `/v6/cards/backtest/compare?a=momentum&b=degen&days=30` | backtest comparison | side-by-side strategy metrics |

all endpoints accept `operator_id` query parameter (default: "op_default").

## message formats

### entry notification
```
caption: "entered [COIN] [direction] at $[price]. [X]/7. [regime]. stop at $[stop]."
card: eval card
buttons: [📊 Session Status | session_status] [🔥 Heat Map | show_heat]
```

### exit notification (win)
```
text: "[COIN] closed +$[pnl] (+[%]). trailing stop locked profits at $[price]."
buttons: [📊 Session Status | session_status] [📈 Equity | show_equity]
```

### exit notification (loss)
```
text: "[COIN] stopped. -$[pnl] (-[%]). stop worked. protection held."
buttons: [📊 Session Status | session_status] [📈 Equity | show_equity]
```

### session complete
```
caption: "[strategy] session #[N]. [P&L]. [trades] trades. [rejection_rate]% rejected."
card: result card
buttons:
  row 1: [📊 Full Report | show_result] [📈 Equity Curve | show_equity]
  row 2: [🔄 New Session | new_session] [📜 History | show_history]
```

### approaching alert
```
caption: "[COIN] forming. [X]/7. [bottleneck] is the bottleneck. watching."
card: approaching card
buttons: [📊 Eval [COIN] | eval_COIN] [🔥 Heat Map | show_heat]
```

### morning brief
```
caption: "overnight: [N] positions. fear & greed: [X] ([classification]). [N] approaching."
card: brief card
buttons:
  row 1: [🔥 Heat Map | show_heat] [📡 Approaching | show_approaching]
  row 2: [📊 Session Status | session_status] [📋 Full Brief | show_brief]
```

### deploy confirmation
```
text: "[strategy]. [positions] positions max. [stops]% stops. [hours] hours. paper mode."
buttons:
  row 1: [▶ Deploy Paper | deploy_STRATEGY_paper] [💰 Deploy Live | deploy_STRATEGY_live]
  row 2: [📊 Preview Risk | preview_STRATEGY] [✗ Cancel | cancel_deploy]
```

### regime update
```
caption: "[direction] market. [count] trending. fear & greed: [X]. [funding_bias]."
card: regime card
buttons: [🔥 Heat Map | show_heat] [📡 Approaching | show_approaching]
```

## reaction protocol

| event | immediate reaction | completion reaction |
|---|---|---|
| operator command (deploy, evaluate, end) | react with working indicator | react with success/failure |
| longer operation (evaluation, heat scan) | react with analyzing indicator | react with success + send card |

## threading rules

| event | reply to |
|---|---|
| approaching alert for coin on heat map | heat card message |
| entry alert | approaching alert for that coin |
| exit alert | entry alert for that coin |
| first alert (no prior context) | send top-level (no reply) |
