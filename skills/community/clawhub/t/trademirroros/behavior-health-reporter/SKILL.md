---
name: behavior-health-reporter
description: 负责交易行为体检报告生成，聚焦计划执行率、计划外交易、持仓偏离、止损纪律、连亏后行为与大赚后频率变化等非盈亏指标。
---

# Behavior Health Reporter

## Read First

- `../finance-journal-orchestrator/references/data-contracts.md`
- `../finance-journal-orchestrator/references/operating-rhythm.md`

## What To Produce

- periodic or ad-hoc behavior health reports focused on process quality
- explicit metrics for plan adherence, off-plan trading, stop-loss discipline, and emotion-linked drift
- caveats whenever sample size, position data, or inferred fields are incomplete
- action-oriented review notes that improve discipline without becoming trading signals

## Working Rules

1. prioritize process deviations over raw PnL narration
2. highlight repeat behavior loops, especially after consecutive losses or outsized wins
3. keep limitations visible when any conclusion depends on sparse or partial data
4. frame the report as a mirror for self-correction, not a scorecard for bragging
