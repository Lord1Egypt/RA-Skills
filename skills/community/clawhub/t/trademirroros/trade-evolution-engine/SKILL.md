---
name: trade-evolution-engine
description: 负责交易日志、卖出后回顾、历史条件参考与交易行为自进化。适用于开仓/平仓记录、回看操作差值、生成卖飞回顾、沉淀情绪/失误/经验，并输出可复用的复盘结构。
---

# Trade Evolution Engine

## Read First

- `../finance-journal-orchestrator/references/data-contracts.md`
- `../finance-journal-orchestrator/references/operating-rhythm.md`
- `references/evolution-algorithms.md`
- `references/trajectory-self-evolution-core-algorithm.md`
- `references/trajectory-self-evolution-core-algorithm.en.md`

## What To Produce

- structured trade logs that separate entry facts, exit facts, context, and lessons
- post-trade reviews that preserve original reasons instead of rewriting history
- evolution reminders framed as reusable evidence-backed heuristics
- skill-card candidates with trigger conditions, evidence, and do-not-use-when boundaries

## Working Rules

1. record facts first; commentary and labels can be layered on afterward
2. preserve the original thesis and sell reason even when the later review disagrees
3. treat historical matching as personal sample recall, not prediction
4. make emotion, mistake, and lesson fields explicit because they drive long-term adaptation
5. bandit-style prioritization is a reminder mechanism, not an autonomous strategy
