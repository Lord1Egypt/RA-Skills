---
name: solana-investor
description: 顶层投资助手编排器 — 协调 portfolio、dca、alerts、market 技能，处理复杂的多步骤投资请求。当用户的请求涉及多个操作或需要跨技能协调时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: ["node"]
    emoji: "🦅"
---

# Solana 投资助手 — 多技能编排

## When to Use

当用户的请求涉及多个技能的组合时使用此技能：
- "显示我的组合，然后设置 SOL 的价格警报"
- "SOL 多少钱？如果低于 100 就提醒我"
- "看看我有多少 JUP，然后定投 50 USDC"
- "总结一下我的投资状况"（需要 portfolio + market）

**单一技能请求不使用此技能**，直接使用对应的子技能。

## Workflow

### 编排原则

1. **先查询后操作** — 查价格、看组合等读操作先执行
2. **操作前确认** — 创建策略、设置警报等写操作前确认参数
3. **上下文传递** — 前一步的结果作为后一步的上下文
4. **逐步反馈** — 每完成一步告知用户，不要等全部完成

### 常见编排模式

#### 模式 A: 查看 + 设置
> "看看 SOL 价格，然后设置提醒"

1. 调用 `solana-market` 的 `get-price.js SOL`
2. 展示当前价格
3. 询问："SOL 目前 $X，你想在什么价格时收到通知？"
4. 调用 `solana-alerts` 的 `create-alert.js`

#### 模式 B: 组合 + 行动
> "看看我持有多少 SOL，然后每周定投"

1. 调用 `solana-portfolio` 的 `get-portfolio.js`
2. 展示持仓中的 SOL 数量和价值
3. 询问："你目前持有 X SOL（$Y），想每周定投多少 USDC？"
4. 调用 `solana-dca` 的 `create-dca.js`

#### 模式 C: 全面总结
> "总结我的投资状况"

1. 调用 `solana-portfolio` 的 `get-portfolio.js` — 获取持仓
2. 调用 `solana-market` 的 `market-overview.js` — 获取当前行情
3. 调用 `solana-dca` 的 `list-strategies.js` — 获取策略状态
4. 调用 `solana-alerts` 的 `list-alerts.js` — 获取警报状态
5. 综合所有信息，给出结构化总结

## Guardrails

- **不自作主张** — 只执行用户明确要求的组合操作
- **分步确认** — 多步操作中每个写操作都需确认
- **失败隔离** — 一个技能失败不影响其他技能的结果展示
- **保持简洁** — 组合结果不要过度冗长，突出关键信息

## Available Scripts

| 脚本 | 用途 | 参数 |
|------|------|------|
| *(无直接脚本)* | 此技能为纯 Prompt 编排器，通过协调子技能的脚本完成任务 | — |
