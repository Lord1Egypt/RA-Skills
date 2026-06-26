---
name: uwillberich
description: Build next-session A-share game plans from market structure, overnight macro shocks, policy timing, and watchlist leadership. Use when the user asks what A-shares may do tomorrow, which sectors may repair first, how to read the open, or wants a reusable pre-open discretionary decision workflow.
metadata: {"openclaw":{"emoji":"📈","homepage":"https://github.com/huangrichao2020/uwillberich","requires":{"bins":["python3"]}}}
---

# uwillberich

Author: 超超
Contact: `grdomai43881@gmail.com`

## Overview

Use this skill for decision-oriented A-share analysis. The goal is not to explain the market mechanically, but to convert today’s tape and overnight developments into a concrete next-session plan.

Best fit:

- next-session A-share outlook
- likely repair sectors after a selloff
- opening checklist for `09:00`, `09:25`, and `09:30-10:00`
- first-30-minute observation template for distinguishing true repair from defensive concentration
- watchlist-based decision notes
- distinguishing defensive leadership from true market repair
- persistent message iteration that maps high-attention news into watchlist overlays
- automatic event-driven stock pools that feed directly into desk reports
- main-force capital-flow confirmation for watchlists and market-wide risk tone
- industry-chain expansion that turns event themes into fresh stock pools
- sentiment scoring built from breadth, sector dispersion, and capital flow

## Core Workflow

1. Gather market structure first.
   - Confirm `EM_API_KEY` is configured before running any script.
   - Run `scripts/fetch_market_snapshot.py` for indices, breadth, and sector leaders/laggards.
   - Run `scripts/fetch_quotes.py` or `scripts/morning_brief.py` for the watchlist.
2. Confirm the overnight and policy layer.
   - Use primary sources first for `PBOC`, `Federal Reserve`, and other central-bank decisions.
   - Use high-quality news sources for geopolitics, oil, and global risk sentiment.
3. Classify the market through three layers.
   - External shock: oil, rates, U.S. equities, geopolitics
   - Domestic policy/liquidity: `LPR`, PBOC posture, macro support
   - Internal structure: breadth, leadership, relative strength, style rotation
4. Build a scenario tree.
   - Provide `Base / Bull / Bear` paths with explicit triggers and invalidations.
5. Turn the view into an execution checklist.
   - Include `09:00`, `09:20-09:25`, `09:30-10:00`, and `14:00-14:30`.

## Workflow Shortcuts

- `Step 1: overnight and policy`
  - `scripts/mx_toolkit.py preset --name preopen_policy`
  - `scripts/mx_toolkit.py preset --name preopen_global_risk`
- `Step 2: board resonance`
  - `scripts/fetch_market_snapshot.py`
  - `scripts/capital_flow.py`
  - `scripts/market_sentiment.py`
  - `scripts/mx_toolkit.py preset --name board_optical_module`
  - `scripts/mx_toolkit.py preset --name board_compute_power`
- `Step 3: single-name validation`
  - `scripts/fetch_quotes.py`
  - `scripts/mx_toolkit.py preset --name validate_inspur`
  - `scripts/mx_toolkit.py preset --name validate_luxshare`
- `Step 4: event-to-chain expansion`
  - `scripts/industry_chain.py`
  - `scripts/news_iterator.py`
- `Source benchmark`
  - `scripts/benchmark_sources.py`

## Decision Heuristics

- Prefer sectors that resisted best in a weak tape over sectors that merely fell the most.
- Treat defensive leadership as separate from broad market repair.
- On monthly `LPR` days, use the `09:00` release as a hard branch in the plan.
- A repair thesis is stronger when leadership broadens from core growth names into secondary names and brokers.
- A rebound without breadth is usually just a technical bounce.

## Scripts

Use these scripts before writing the decision note:

- `scripts/fetch_market_snapshot.py`
  - Pulls Eastmoney index and sector breadth data.
- `scripts/fetch_quotes.py`
  - Pulls Tencent quote snapshots for user-specified names.
- `scripts/morning_brief.py`
  - Builds a markdown brief from the default watchlists in `assets/default_watchlists.json`.
- `scripts/capital_flow.py`
  - Pulls the whole-market main-force snapshot plus top inflow/outflow names and intersects them with watchlists.
- `scripts/market_sentiment.py`
  - Scores the tape as `抱团行情`, `科技修复`, `修复扩散`, or `分化偏弱` using breadth, sector dispersion, and capital flow.
- `scripts/opening_window_checklist.py`
  - Builds a first-30-minute observation sheet with time gates, group scoreboards, and watchlist signal tables.
- `scripts/industry_chain.py`
  - Uses event summaries and desk groups to expand into industry-chain stock pools through live MX stock screens.
- `scripts/news_iterator.py`
  - Continuously polls public RSS feeds, classifies high-attention events, maps them into watchlist overlays, and writes dynamic event-driven stock pools.
- `scripts/runtime_config.py`
  - Loads local runtime credentials, enforces the required `EM_API_KEY`, and prints the Eastmoney application URL when it is missing.
- `scripts/mx_toolkit.py`
  - Calls the live Meixiang / Eastmoney APIs for news search, stock screening, structured data queries, and preset desk workflows.
- `scripts/benchmark_sources.py`
  - Benchmarks public and MX-enhanced sources before you decide what to trust as the primary feed.
- `scripts/install_news_iterator_launchd.py`
  - Installs the news iterator as a `launchd` job on macOS for long-running local polling.
- `scripts/smoke_test.py`
  - Verifies that the bundled scripts and public endpoints are working.

## References

Read only what you need:

- `references/methodology.md`
  - Trading philosophy, decision tree, and timing gates.
- `references/data-sources.md`
  - Source map for official and market data endpoints.
- `references/persona-prompt.md`
  - Decision-maker persona for desk-style answers.
- `references/trading-mode-prompt.md`
  - Time-boxed opening workflow for the next A-share session.
- `references/opening-window-template.md`
  - A reusable first-30-minute decision template.
- `references/cross-cycle-watchlist.md`
  - How to use the cross-cycle core stock pool without turning it into an unfocused mega-list.
- `references/event-regime-watchlists.md`
  - How to use war-shock and energy-spike watchlists as temporary overlays.
- `references/message-iterator.md`
  - How to run the persistent RSS iterator, generate event-driven stock pools, and feed them into the desk workflow.
- `assets/mx_presets.json`
  - Preset MX workflows for policy scan, global-risk scan, board resonance, and single-name validation.
- `assets/industry_chains.json`
  - Theme-to-chain map for optical module, compute power, semiconductors, robotics, oil and coal, and IDC/power-cost overlays.

## Output Standard

Default to a compact desk-style answer:

- one-paragraph decision summary
- `Base / Bull / Bear` path
- most likely repair sectors
- defensive-only sectors
- opening checklist
- `do / avoid`

## Required Credential

- `EM_API_KEY` is mandatory for this skill.
- Apply here: `https://ai.eastmoney.com/mxClaw`
- After opening the link, click download and you will see the key.
- Official site: `https://ai.eastmoney.com/nlink/`
- Store it in `~/.uwillberich/runtime.env`
