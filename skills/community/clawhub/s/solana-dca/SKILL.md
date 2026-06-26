---
name: solana-dca
description: 创建和管理 DCA 定投策略 — 支持自动周期性购买 Solana 代币。当用户想设置定投、查看策略或调整自动购买计划时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: ["SOLANA_NETWORK"]
      bins: ["node"]
    emoji: "📈"
---

# Solana DCA 定投策略引擎

## When to Use

- 用户想设置自动定投（DCA / 定期购买）
- 用户想查看、暂停或恢复已有策略
- 用户提到"定投"、"DCA"、"自动买"、"每周/每天买"

## Workflow

### 用户想创建定投策略

用户可能不会一次给齐所有参数，逐步引导：

1. **确定目标代币** — 如果未指定，询问："你想定投哪个代币？（SOL / JUP / BONK / RAY）"
2. **确定金额** — 如果未指定，询问："每次投入多少 USDC？"
3. **确定频率** — 如果未指定，询问："多久执行一次？"
   - 可选：`daily`（每天）、`weekly`（每周）、`monthly`（每月）、`6hours`（每6小时）
4. **确认参数** — 执行前总结：
   > "确认创建策略：每周投入 100 USDC 购买 SOL，确定吗？"
5. **执行** — `node skills/solana-dca/scripts/create-dca.js <user_id> <token> <amount> <schedule>`
6. **后续建议** — "策略已创建！你可以随时说'查看策略'来查看状态"

### 用户想查看策略

1. `node skills/solana-dca/scripts/list-strategies.js <user_id>`
2. 如果无策略，引导创建："还没有策略，要创建一个吗？"
3. 如果有策略，清晰展示每个策略的状态

### 用户想暂停策略

1. 如果用户没指定 ID，先列出所有策略让用户选择
2. 确认操作："确定暂停策略 #X 吗？"
3. `node skills/solana-dca/scripts/pause-strategy.js <user_id> <strategy_id>`

### 用户想恢复策略

1. 列出已暂停的策略
2. `node skills/solana-dca/scripts/resume-strategy.js <user_id> <strategy_id>`

## Guardrails

- **首次使用必须告知** — "当前 DCA 为模拟功能，记录策略但不实际执行链上交换"
- **确认后再创建** — 永远在执行前让用户确认参数
- **不推荐频率** — 不说"建议每周定投"，让用户自己决定
- **金额限制** — 提醒用户根据自身风险承受能力设置金额

## Available Scripts

| 脚本 | 用途 | 参数 |
|------|------|------|
| `create-dca.js` | 创建策略 | `<user_id> <token> <amount_usdc> <daily\|weekly\|monthly\|6hours>` |
| `list-strategies.js` | 列出策略 | `<user_id> [--lang en]` |
| `pause-strategy.js` | 暂停策略 | `<user_id> <strategy_id>` |
| `resume-strategy.js` | 恢复策略 | `<user_id> <strategy_id>` |
