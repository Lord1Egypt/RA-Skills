---
name: trade-plan-assistant
description: 负责交易计划的结构化创建、有效期管理、状态更新与历史相似场景参考查询。适用于盘前计划录入、计划提醒、执行/放弃标记，但不替代用户做计划内容上的决策。
---

# Trade Plan Assistant

## Read First

- `../finance-journal-orchestrator/references/data-contracts.md`
- `../TRADE_MEMORY_ARCHITECTURE.md`

## What To Produce

- a structured plan object with instrument, direction, thesis, logic tags, risk boundary, and validity window
- an explicit list of missing fields when the user input is incomplete
- optional historical references framed as precedent, not advice
- status updates that keep original plan intent and later execution state separate

## Working Rules

1. ask for or infer the minimum fields needed to make a plan reviewable
2. keep `thesis`, trigger conditions, invalidation, and sizing logic distinct
3. historical references can summarize prior patterns, but must not become buy/sell instructions
4. if the user abandons a plan, preserve the abandonment reason for later behavior review
