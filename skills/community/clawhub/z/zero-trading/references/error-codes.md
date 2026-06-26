# error handling reference

complete error handling matrix for all zero tools and common failure scenarios.

## tool errors

| tool | error | operator message | fallback |
|---|---|---|---|
| `zero_get_engine_health` | connection error | "engine offline. check MCP config: url should be `https://api.getzero.dev/mcp`" | stop onboarding, retry in 60s |
| `zero_evaluate` | returns error or price=0 | "can't reach market data for [coin]. try again in a minute." | skip this coin |
| `zero_get_heat` | returns count: 0 | (no message — this is cold start) | evaluate BTC, ETH, SOL, AVAX, DOGE individually |
| `zero_get_heat` | returns error | "can't reach heat map. try again in a minute." | evaluate individual coins |
| `zero_get_approaching` | returns empty | "nothing forming. engine is selective." | (this is normal, not an error) |
| `zero_get_approaching` | returns error | "can't reach approaching data. try again in a minute." | check heat map instead |
| `zero_get_pulse` | returns empty | "quiet period. no entries or exits since last check." | (this is normal) |
| `zero_get_pulse` | returns error | "can't reach event feed. checking session status instead." | call `zero_session_status` |
| `zero_get_brief` | returns error | "couldn't fetch overnight summary. checking session status." | call `zero_session_status` |
| `zero_get_regime` | returns error | "can't reach regime data. try again in a minute." | skip regime context |
| `zero_start_session` | plan error | "[strategy] needs [plan] plan. try momentum (free) or upgrade at getzero.dev/pricing." | suggest free strategy |
| `zero_start_session` | active session | "session already running. end it first or queue this one." | show session status |
| `zero_start_session` | other error | "[exact error from tool]." | retry once, then report |
| `zero_end_session` | no active session | "no session running. nothing to end." | (this is normal) |
| `zero_session_status` | no active session | (proceed to deploy flow) | (this is expected) |
| `zero_session_status` | returns error | "can't reach session data. try again in a minute." | retry once |
| `zero_preview_strategy` | returns error | "can't load risk preview. engine may be unreachable." | don't guess parameters |
| `zero_auto_select` | returns error | "engine can't recommend right now. let's pick manually." | fall back to manual strategy selection |
| `zero_queue_session` | returns error | "couldn't queue session. try again." | retry once |
| `zero_session_history` | returns count: 0 | "no sessions yet. deploy your first one." | recommend momentum |
| `zero_get_circuit_breaker` | returns error | "can't check circuit breaker status." | proceed with caution |
| `zero_get_rejections` | plan error | "rejection details need pro plan." | suggest upgrade |
| `zero_get_near_misses` | plan error | "near miss details need pro plan." | suggest upgrade |
| `zero_get_execution_quality` | plan error | "execution quality needs pro plan." | suggest upgrade |
| `zero_get_equity_curve` | plan error | "equity curve needs pro plan." | suggest upgrade |
| `zero_backtest_strategy` | plan error | "backtesting needs scale plan." | suggest upgrade |
| `zero_reconcile` | plan error | "reconciliation needs scale plan." | suggest upgrade |
| `zero_get_immune_status` | heartbeat.json missing | "immune system not reporting. check zeroos is running." | check engine_health instead |
| `zero_get_immune_status` | dead_man_active: true | "controller down >5min. dead man's switch active — positions tightened to 1%." | urgent: restart controller |
| `zero_get_immune_log` | returns empty | "no immune events yet. normal if no stop repairs needed." | (not an error) |
| `zero_get_immune_log` | plan error | "immune log needs pro plan." | suggest upgrade |
| `zero_get_evolution_status` | no evolved_configs/ dir | "no evolution cycles run yet." | (normal for new setups) |
| `zero_get_evolution_status` | plan error | "evolution status needs scale plan." | suggest upgrade |
| `zero_evaluate` (layer 8) | Ollama timeout/unreachable | "LLM layer skipped — using mechanical consensus only." | auto-pass (non-blocking) |
| `zero_evaluate` (layer 8) | unparseable LLM response | "LLM layer skipped — response unclear." | auto-pass (non-blocking) |
| `zero_evaluate` (layer 9) | timeframe_signals.json missing | (silent — agent hasn't run) | auto-pass (non-blocking) |
| `zero_evaluate` (layer 9) | coin not in timeframe data | (silent — not tracked by cross-timeframe agent) | auto-pass (non-blocking) |
| `auto_recovery` | cooldown active (24h) | "auto-recovery already triggered today. manual intervention needed." | wait 24h or restart manually |
| `auto_recovery` | defense deploy fails | "auto-recovery failed to deploy defense. check engine status." | manual deploy needed |
| `feedback_loop` | no trade history | "not enough trade data for weight adjustment." | default weights (all 1.0) |
| `feedback_loop` | events.jsonl corrupt | "execution feedback unavailable." | default weights |
| `strategy_generator` | Ollama unavailable | "strategy generation requires local LLM. check Ollama is running." | N/A |
| `strategy_generator` | generated config fails validation | "generated strategy violates hard constraints. regenerating." | retry |
| `coevolution` | no strategy configs found | "no strategies to test." | N/A |

## rate limiting

| header | meaning |
|---|---|
| `X-RateLimit-Limit` | max requests per hour for this plan |
| `X-RateLimit-Remaining` | requests remaining in current window |
| `X-RateLimit-Reset` | unix timestamp when window resets |

| plan | limit |
|---|---|
| free | 30/hour |
| pro | 120/hour |
| scale | 1200/hour |
| api | 6000/hour |

when rate limited (HTTP 429): "rate limit reached. [remaining] seconds until reset. upgrade at getzero.dev/pricing."

## authentication errors

| error | operator message |
|---|---|
| missing token (401) | "authentication required. run setup to configure your token." |
| invalid token (401) | "token not recognized. check your MCP configuration." |
| forbidden — plan too low (403) | "[tool] requires [plan] plan. upgrade at getzero.dev/pricing." |

## data quality issues

| issue | how to detect | response |
|---|---|---|
| stale prices | price_stale_ms > 120000 | "market data is stale. waiting for fresh prices." |
| stale sources | source_stale_ms > 30000 | (flag internally, don't alarm operator) |
| null/zero values in eval | layer values are null or 0 | "some evaluation data is missing. result may be partial." |
| collective layer = None | collective value is None | this is normal (v1). don't mention unless asked. |
| eval_count = 0 in session | session shows 0 evaluations | engine evaluates independently. check `zero_get_pulse` for activity. |

## golden rules

1. **never fabricate data.** if a tool fails, say so.
2. **never guess parameters.** if preview_strategy fails, don't quote risk numbers from memory.
3. **be specific.** "can't reach heat map" not "something went wrong."
4. **offer fallbacks.** heat empty → evaluate individual coins. brief fails → check session status.
5. **distinguish errors from normal states.** empty approaching = selective engine, not an error.
