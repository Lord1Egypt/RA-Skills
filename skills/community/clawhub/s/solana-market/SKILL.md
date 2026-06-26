---
name: solana-market
description: 查询 Solana 生态代币实时价格和市场概览。当用户想知道代币价格、行情、市场状况时触发。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: ["node"]
    emoji: "💲"
---

# Solana 市场情报

## When to Use

- 用户问代币价格（"SOL 多少钱"）
- 用户想看整体市场行情
- 用户提到"价格"、"行情"、"市场"、"多少钱"

## Workflow

### 用户问某个代币的价格

1. 从用户消息中提取代币名称
2. `node skills/solana-market/scripts/get-price.js <SYMBOL>`
   - 支持的代币：SOL、USDC、USDT、JUP、RAY、BONK
3. 展示价格，并主动提供相关操作建议：
   - "SOL 目前 $150。需要设置价格警报吗？"
   - "JUP 目前 $0.82。要看看你持有多少吗？"

### 用户想看市场概览

1. `node skills/solana-market/scripts/market-overview.js`
2. 展示所有代币价格列表
3. 如果用户已连接钱包，可以主动建议："要看看你的持仓在这个行情下的表现吗？"

### 代币不支持时

如果用户查询的代币不在支持列表中，友善告知：
> "目前支持查询 SOL、USDC、USDT、JUP、RAY、BONK 的价格。你想查哪个？"

## Guardrails

- **不预测走势** — 不说"看起来要涨/跌了"
- **数据来源透明** — 可以告知用户"价格来自 CoinGecko"
- **不推荐交易** — 展示价格后不建议买入/卖出
- **缓存说明** — 如果用户反复查询相同代币，告知价格有 30 秒缓存

## Available Scripts

| 脚本 | 用途 | 参数 |
|------|------|------|
| `get-price.js` | 查询价格 | `<SYMBOL> [--lang en]` |
| `market-overview.js` | 市场概览 | `[--lang en]` |
