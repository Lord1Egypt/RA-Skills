---
name: tradingview
description: TradingView platform skill for SurfAgent, covering chart workflows, proof rules, blockers, and when to use the TradingView adapter over generic browser control.
version: 1.0.0
metadata:
  openclaw:
    homepage: https://surfagent.app
    emoji: "📈"
---

# TradingView

> TradingView-specific operating skill. Use this with `browser-operations`, `surfagent-perception`, and `surfagent-mcp-selection`.

This skill teaches agents how to work TradingView without treating a live chart like a generic webpage, guessing at chart state, or claiming technical-analysis results without proof.

## 1. Use this skill for

- chart state inspection
- symbol, timeframe, and chart-type changes
- quote and OHLCV reads
- indicator and study-value inspection
- screenshots and export flows
- alert setup support
- drawing workflows
- Pine editor workflows
- watchlist reads and updates
- deciding when to use the TradingView adapter instead of generic browser control

## 2. Tool preference

Use this order:
1. TradingView adapter state/data tools
2. TradingView adapter action tools
3. SurfAgent perception for visual confirmation
4. targeted browser evaluation only when needed
5. raw generic browser actions as fallback

Verdict: if the task is about chart state, market data, indicators, Pine, alerts, or drawings, the TradingView adapter should usually win.

## 3. TradingView truths that matter

TradingView is not a normal DOM-first app.

It has:
- chart widget state hidden behind app internals
- dynamic panes, dialogs, and side panels
- editor surfaces that are not plain textareas
- actions where a visible chart is not proof the requested state applied
- premium-gated features that can look like broken automation

Important: clicking around the UI is usually the dumbest path. If the adapter can read or set chart state directly, use it.

## 4. Core TradingView loop

Default loop:
1. confirm TradingView is open and chart-ready
2. read current chart state
3. apply one chart change or extract one data view
4. verify the changed state or rendered chart
5. continue only if the chart settled into the expected mode

## 5. Verified chart workflow

Known-good pattern:
- run `tv_health_check`
- inspect `tv_chart_state`
- set symbol, timeframe, or chart type with adapter verbs
- re-read `tv_chart_state`
- if the task is visual, capture `tv_screenshot` or use perception
- if the task is analytical, pull `tv_quote`, `tv_ohlcv`, `tv_indicators`, or `tv_study_values`

Do not claim a chart change succeeded from navigation alone.

## 6. Proof rules

For TradingView, success requires evidence from the right layer.

1. **state proof**
   - `tv_health_check` says TradingView is open and chart-ready
   - `tv_chart_state` shows the expected symbol, interval, or chart type

2. **data proof**
   - quote, OHLCV, indicator, study, alert, drawing, or watchlist output matches the requested target

3. **visual proof** when the task is visual
   - `tv_screenshot`, `tv_export_image`, or perception confirms the rendered chart or dialog

Good proof examples:
- timeframe change verified by `tv_chart_state`
- support line creation verified by `tv_drawings_list` plus screenshot
- Pine compile verified by compile result and error-free editor state
- alert setup verified by visible alert dialog or `tv_alert_list`

Bad proof:
- page loaded
- click succeeded
- a toolbar button existed
- no exception was thrown

## 7. When to use the TradingView adapter

Prefer the TradingView adapter for:
- opening TradingView
- health/readiness checks
- chart state reads
- symbol, timeframe, and chart-type changes
- price and OHLCV extraction
- indicator and study-value reads
- chart screenshots and export attempts
- alert listing and alert-dialog opening
- drawing creation/listing/clearing
- Pine editor open, source set, compile, and error inspection
- watchlist reads and watchlist add flows

Current adapter verbs include:
- `tv_health_check`
- `tv_open`
- `tv_chart_state`
- `tv_set_symbol`
- `tv_set_timeframe`
- `tv_set_chart_type`
- `tv_quote`
- `tv_ohlcv`
- `tv_indicators`
- `tv_study_values`
- `tv_screenshot`
- `tv_export_image`
- `tv_alert_list`
- `tv_alert_create`
- `tv_draw_horizontal`
- `tv_drawings_list`
- `tv_drawings_clear`
- `tv_pine_open_editor`
- `tv_pine_set_source`
- `tv_pine_compile`
- `tv_pine_get_errors`
- `tv_watchlist`
- `tv_watchlist_add`

## 8. When generic browser control is still acceptable

Use targeted browser control when:
- you need a one-off UI probe the adapter does not expose
- you must inspect a premium/paywall/modal surface visually
- you need narrow confirmation of a rendered label, menu, or pane
- the adapter returned ambiguous state and a screenshot can settle it

Even then:
- keep the scope narrow
- do not rediscover chart state from scratch if adapter state exists
- return to adapter-level proof after the UI step when possible

## 9. Chart workflows

### Symbol/timeframe/chart type
Use:
1. `tv_chart_state`
2. `tv_set_symbol` or `tv_set_timeframe` or `tv_set_chart_type`
3. `tv_chart_state` again
4. optional screenshot if the chart appearance matters

### Data extraction
Use:
1. `tv_chart_state`
2. `tv_quote` or `tv_ohlcv`
3. `tv_indicators` or `tv_study_values` if the task depends on studies

### Visual chart evidence
Use:
1. adapter state/data first
2. `tv_screenshot` for browser render proof
3. `tv_export_image` when native export quality matters and the flow is supported

## 10. Pine workflows

Use the adapter, not raw typing, for Pine work.

Default loop:
1. `tv_pine_open_editor`
2. `tv_pine_set_source`
3. `tv_pine_compile`
4. `tv_pine_get_errors`
5. screenshot or perception if the rendered study placement matters

Proof standard:
- source actually set
- compile attempted
- error state captured
- if successful, resulting indicator/study is visible in chart state or chart render

## 11. Alerts and drawings

For alerts:
- use `tv_alert_list` to inspect current state
- use `tv_alert_create` to open the flow
- verify the dialog or resulting alert state visibly
- do not pretend the alert is fully created if the UI still needs human confirmation

For drawings:
- use `tv_draw_horizontal` for support/resistance style actions
- verify with `tv_drawings_list`
- add screenshot proof when line placement matters

## 12. Common blockers

Watch for:
- TradingView tab not open
- chart widget not ready yet
- wrong symbol namespace or malformed ticker
- delayed chart settlement after symbol/timeframe changes
- paywalled indicators or alerts
- editor panel not actually open
- compile errors in Pine
- modal or side-panel state obscuring the chart
- stale or poisoned tab after retries

When blocked:
- name the blocker plainly
- say whether it is retryable, adapter-gap, account-tier-limited, or human-blocked
- do not quietly downgrade the proof bar

## 13. Token-efficiency rules for TradingView

Prefer:
- adapter state over DOM scraping
- adapter market data over screenshot-reading for numeric values
- one post-action verification read over repeated broad chart probes
- screenshots only when a visual claim must be proven

Avoid:
- giant DOM dumps for chart data
- reading candles from pixels when `tv_ohlcv` exists
- clicking through menus to discover state already exposed by the adapter
- repeated full visual passes when a state re-read would prove the change faster

## 14. Minimal TradingView checklist

Before claiming a TradingView task done, confirm:
- correct tab
- chart ready
- correct symbol/timeframe/chart type
- requested action executed
- adapter state or data confirms it
- visual proof captured if the task was visual
- blockers, limits, or human-confirm steps called out explicitly

## 15. Relationship to other docs

Use alongside:
- `browser-operations` for universal browser rules
- `surfagent-perception` for screenshots and visual state diffing
- `surfagent-mcp-selection` for layer choice discipline
- the `surfagent-tradingview` adapter docs for concrete MCP setup and verb behavior
