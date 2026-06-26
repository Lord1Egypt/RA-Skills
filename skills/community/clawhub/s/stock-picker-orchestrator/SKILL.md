---
name: stock-picker-orchestrator
description: Acts as a meta-orchestrator that routes stock-analysis requests across data, macro/news, backtesting, earnings quality, valuation, portfolio analytics, and risk skills under explicit budget controls.
compatibility: Requires dependent skills (`vnstock-free-expert`, macro/news monitors, `strategy-backtester`, `earnings-quality-reviewer`, `equity-valuation-framework`, `portfolio-analytics`, and `portfolio-risk-manager`) to be available in the same workspace.
metadata: {"openclaw":{"emoji":"🧩"}}
---

# Stock Picker Orchestrator

Use this skill to coordinate the full analysis system from user intent to final recommendation framing.

## Purpose
- Convert user request into the right analysis pipeline.
- Control budget: vnstock API calls, breadth of news scraping, depth of valuation work.
- Produce transparent outputs: what was fetched, assumptions, confidence, gaps.
- Scope boundary: this skill coordinates other skills and does not replace their domain-specific logic.

## Skill graph (preferred dependencies)
1. `vnstock-free-expert` for structured market/fundamental data.
2. `nso-macro-monitor` for Vietnam macro snapshot.
3. `us-macro-news-monitor` for global macro spillover signals.
4. `vn-market-news-monitor` for domestic market narrative.
5. `strategy-backtester` for historical ranking/strategy validation.
6. `earnings-quality-reviewer` for earnings quality before valuation conviction.
7. `equity-valuation-framework` for decision-grade valuation and report standard.
8. `portfolio-analytics` for portfolio risk metrics before sizing/rebalance.
9. `portfolio-risk-manager` for IPS mini + position sizing + risk triggers (no-margin).
10. `trade-decision-policy` for `BUY`, `ADD`, `HOLD`, `TRIM`, `EXIT`, target weights, and action drafts.
11. `institutional-governance` for D1 approvals, compliance checks, audit logs, and approved target portfolio state.

## Trigger conditions
- "Find best stock(s)"
- "Screen this sector"
- "Analyze ticker X deeply"
- "How do macro/news affect these stocks"
- "Value this stock like a professional"

## First step: intent classification
Classify user request into one of these modes:
- `Single-Ticker Deep Dive`
- `Multi-Ticker/Universe Screening`
- `Macro/News-Led Investigation`
- `Portfolio Refresh`

If ambiguous, choose the most conservative high-signal mode and note assumption.

## Execution workflow (ordered)
1. Parse user intent and select one routing mode.
2. Set budget preset (`Light`, `Standard`, `Deep`) and hard request limits.
3. Execute required upstream skills for the chosen route.
4. Validate intermediate outputs for freshness, completeness, and conflicts.
5. Run valuation layer only at the required depth.
6. Aggregate confidence across modules using the shared rubric.
7. Return output using the mandatory output contract.

## Budget policy (required)
Define and enforce budget at start:
- `API budget`: max vnstock calls
- `News budget`: max headlines/articles per source
- `Valuation depth`: quick multiples vs full DCF

Default safe presets:
- `Light`: 20-40 vnstock calls, headlines-only news, quick valuation
- `Standard`: 40-120 calls, mixed headlines + selected deep reads, scenario valuation
- `Deep`: 120-240 vnstock calls, full context package, full valuation + sensitivity

Prefer free-tier-safe pacing when using vnstock.

## Free-tier budget mapping (required)
Use these hard limits for vnstock runs:
- Guest/no API key: max `20 requests/min` (recommended pacing >= `3.2s/request`).
- Community API key: max `60 requests/min` (recommended pacing >= `1.1s/request`; keep `3.2s/request` if unstable).

Policy actions:
1. Estimate call count before execution and choose the smallest viable preset.
2. If estimated calls exceed current budget, reduce scope (smaller universe or fewer modules).
3. Reuse cached artifacts before making new requests.
4. Stop scope expansion when remaining call budget < 10% and report partial results.

## Routing logic

### A) Single ticker request
Priority: depth over breadth.
Pipeline:
1. `vnstock-free-expert` fetch financials + price behavior.
2. Optional macro/news context if user asks or risk is macro-sensitive.
3. Run `earnings-quality-reviewer` before valuation when financial statements are available.
4. `equity-valuation-framework` full thesis + valuation + risks.

### B) Multi-ticker/sector screening
Priority: breadth first, then depth on finalists.
Pipeline:
1. `vnstock-free-expert` broad screener/ranking.
2. Run `strategy-backtester` before treating the ranking as high-conviction when historical signal/price data is available.
3. Select top candidates by objective criteria and backtest confidence.
4. Run `earnings-quality-reviewer` on finalists when statement data is available.
5. Run quick valuation layer on shortlist.
6. Deep valuation only for top 1-3 names.

### C) Macro/news-led request
Priority: context first, valuation second.
Pipeline:
1. `nso-macro-monitor` + `us-macro-news-monitor` + `vn-market-news-monitor`.
2. Map exposures to sectors/tickers.
3. Run quick vnstock validation on impacted names.
4. Use `earnings-quality-reviewer` for decision-critical names after quantitative validation when statement data is available.
5. If needed, run `equity-valuation-framework` for decision-critical names.

### D) Portfolio refresh
Priority: risk control + monitoring triggers + sizing discipline.
Pipeline:
1. Re-score holdings and benchmark against alternatives.
2. Macro/news stress overlay.
3. Run `portfolio-analytics` before risk sizing when holdings and price history are available.
4. Run `equity-valuation-framework` at least quick depth on key holdings/watchlist.
5. Run `portfolio-risk-manager` to produce IPS mini + position sizing policy + per-ticker triggers/invalidation.
6. Flag rebalance candidates with confidence and data gaps.

## Mandatory output contract
Always include these sections in final response:

1. `What Was Fetched`
- Data sources used, date/time, and coverage.

2. `Pipeline Chosen`
- Why this route was selected for current user intent.

3. `Assumptions`
- Explicit assumptions on macro, valuation parameters, and data quality.

4. `Results`
- Ranked outputs or thesis summary with concise evidence.

5. `Confidence and Gaps`
- Confidence level + missing data + potential impact.

6. `Risk Flags`
- Top risks and monitoring triggers.

7. `Next-Step Options`
- 2-3 practical follow-up actions (e.g., deepen 1 ticker, expand peer set, update after next macro release).

8. `Decision and Governance`
- Recommendation label: `BUY`, `ADD`, `HOLD`, `TRIM`, or `EXIT`.
- Draft target weight and maximum weight.
- Compliance status.
- Approval requirement.
- D1 write intent.
- Broker execution status: `Disabled` in the current phase.

## Shared confidence rubric (required)
Use a unified confidence output across pipeline steps:
- `High`: all critical modules complete with no material data blockers.
- `Medium`: one critical module has partial gaps but overall conclusion remains stable.
- `Low`: key module(s) missing or conflicting evidence makes conclusion fragile.

Aggregation rule:
1. Compute per-module confidence first (`vnstock`, `macro`, `news`, `backtest`, `earnings_quality`, `valuation`, `portfolio_analytics`, `risk_management`).
2. Overall confidence = minimum of critical modules used in the chosen pipeline.
3. If module outputs conflict, cap overall confidence at `Medium` unless conflict is resolved with stronger evidence.
4. If a required professional-grade module is skipped because inputs are unavailable, cap overall confidence at `Medium` and list the missing module and input.
5. Always state which module is the bottleneck for confidence.

## Governance and quality rules
- Single source of truth: if user provides ACTIVE_WATCHLIST/holdings, do not self-modify it; only propose drafts requiring user confirmation.
- Never present uncertain outputs as facts.
- Separate observed data from inference.
- Prefer reproducible logic over ad-hoc narratives.
- When data is insufficient, downgrade confidence and narrow claims.
- May issue structured `BUY`, `ADD`, `HOLD`, `TRIM`, or `EXIT` labels only through `trade-decision-policy`.
- Must not place orders, call broker APIs, execute trades, or imply that an approved target portfolio state is an executable order.
- Must route all approved target-state mutations through `institutional-governance`.
- Require downstream outputs to be English when preparing reusable reports or handoff bundles.
- Carry missing data forward across modules; do not drop gaps when aggregating results.
- If a downstream skill omits confidence or data gaps, cap overall confidence at `Medium` and state the omission.

## Conflict resolution rules
If outputs from different modules disagree:
1. Trust data quality hierarchy first (freshness/completeness/consistency).
2. Prefer broad consensus metrics over fragile point estimates.
3. Keep both interpretations and state decision boundary (what would change the conclusion).

## Fallback behavior
- If macro/news skills are unavailable: continue with vnstock + valuation only and mark missing context.
- If valuation inputs are weak: provide screening + directional view; defer full valuation.
- If API budget is near limit: stop expanding scope, summarize partial results, request user confirmation for deeper run.

## Example orchestration prompts
- "Run a single-ticker deep dive for HPG with full valuation and risk register."
- "Screen VN30 for top value-quality names, then deep value top 3."
- "Start from macro shock signals, then identify Vietnamese sector winners/losers and value 2 candidates."

## Trigger examples
- "Find the best Vietnam stocks this week with full reasoning."
- "Compare three candidate tickers and tell me which one is strongest."
- "Start from macro and news, then shortlist potential winners."
