---
name: trend-demand-forecaster
description: Turn sales notes, trend signals, seasonal context, promo plans, and inventory constraints into a practical demand forecast brief with base, upside, and downside scenarios, leading indicators, and replenishment cues. Use when planners, ecommerce operators, founders, or consultants need forecasting support without live ERP, BI, ads, or marketplace APIs.
version: v1.0.0
tags: demand-forecasting, trend-analysis, inventory-planning, sales-prediction, business-intelligence
---

# Trend Demand Forecaster

## Overview

Use this skill to convert rough demand signals into a practical forecast narrative. It is built for teams that need a fast planning layer for the next few weeks, quarter, or seasonal window.

This MVP is heuristic. It does **not** pull live sales, ads, weather, ERP, marketplace, or competitor data. It relies on the user's provided notes, exports, and planning context.

## Trigger

Use this skill when the user wants to:
- forecast demand for the next month, quarter, or seasonal event
- estimate promo lift or post-promo normalization
- plan replenishment against demand uncertainty
- interpret whether demand is recovering, stabilizing, or softening
- turn messy trend notes into a base, upside, downside planning brief

### Example prompts
- "Forecast next month's demand using these sales and inventory notes"
- "Build a base, upside, downside demand view for our holiday campaign"
- "Should we buy deeper inventory or stay cautious?"
- "Help me interpret whether demand is rebounding or just promo noise"

## Workflow

1. Clarify the planning question, decision horizon, and risk tolerance.
2. Normalize the strongest signals, such as traffic, orders, conversion, price, inventory, and seasonality.
3. Separate baseline demand from promo distortion, stockout distortion, or one-off events.
4. Build base, upside, and downside scenarios with trigger conditions.
5. Return a markdown brief with indicators, action cues, and assumptions.

## Inputs

The user can provide any mix of:
- weekly or monthly sales summaries
- traffic, conversion, pricing, and promo notes
- stockout periods, inventory cover, or inbound timing
- launch, seasonal, holiday, or campaign context
- return rate, customer service, or marketplace feedback
- constraints such as cash, lead time, MOQ, or warehouse limits

## Outputs

Return a markdown forecast brief with:
- demand narrative and likely mode
- planning horizon and key signals
- base, upside, downside scenarios
- leading indicators to monitor
- inventory and commercial implications
- risk watchlist and next-step actions
- assumptions, confidence notes, and limits


## Usage Scenarios

1. **User input:** "We're planning Q4 inventory for our apparel brand. Sales notes say '90s revival is coming.' Turn that into numbers."
→ **Expected output:** Demand forecast brief — baselines Q4 LY actuals, quantifies trend signal with Google Trends/search-volume data proxy, applies seasonal uplift, factors planned promo calendar lift (+15%), and accounts for supply-chain lead-time constraints → 3-scenario output (base, upside +20%, downside -10%) with inventory-recommendation ranges per SKU category.
2. **User input:** "Forecast demand for our new product launch in 3 regions with only 6 months of test-market data."
→ **Expected output:** Launch-demand model — analog-based forecasting (similar-product historical curves), test-market extrapolation with regional modifiers, month-1-through-6 volume projections with confidence intervals.
3. **User input:** "Build a monthly demand forecasting workflow our small team can run in 2 hours."
→ **Expected output:** 2-hour monthly forecast SOP — data-gathering checklist (15 min), trend-signal scan (20 min), Excel/Sheets model template (45 min), assumptions-documentation step (20 min), and output format for cross-functional sharing (20 min).



### Scenario 4: 看小红书猜明年卖什么火
**User input:** "我想在拼多多开店但不知道卖什么，看到小红书上哪些品火就追，结果每次都追在山顶。怎么提前预测下一个爆品？"
**Expected output:** 趋势预判方法论——第一步：关键词监控（用5118/巨量算数/百度指数追踪核心品类搜索量变化趋势）；第二步：社交媒体信号（在小红书关注"新品首发"笔记标签、留意评论区高赞"求链接"回复）；第三步：供应链验证（在1688查相关品近3个月供应商数量变化，突然增多但买家还少的品可以入场）；第四步：搜索量vs销量对比（在淘宝/拼多多搜这个品看搜索人气和转化率，搜索量上升但销量还没爆的好机会）。关键工具：5118+巨量算数+1688+生意参谋。

## Safety

- Do not claim access to live systems or external trend feeds.
- Treat all scenarios as planning heuristics, not guaranteed forecasts.
- Do not auto-commit buys, budgets, or inventory transfers.
- Downgrade confidence when the user only provides promo-distorted or stockout-distorted history.
- Keep final purchasing and budget decisions human-approved.

## Best-fit Scenarios

- ecommerce teams planning 2 to 16 weeks ahead
- operators working from rough exports instead of a forecasting platform
- founders who need a quick demand-planning memo before placing inventory bets
- consultants preparing scenario-based planning recommendations

## Not Ideal For

- formal statistical forecasting that requires model calibration and backtesting
- highly granular store-SKU-day forecasting at enterprise scale
- workflows that require automatic PO creation or system sync
- regulated forecasts that need audited financial controls

## Acceptance Criteria

- Return markdown text.
- Include scenario, indicator, implication, and risk sections.
- Make the advisory and heuristic framing explicit.
- Keep the output practical for planning and replenishment decisions.
