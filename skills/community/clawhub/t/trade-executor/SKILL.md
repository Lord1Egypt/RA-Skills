---
name: trade-executor
version: "0.1.0"
description: Execute cryptocurrency trades on exchanges (Binance, OKX) with risk controls, user confirmation, and audit logging.
homepage: https://www.binance.com
metadata:
  {
    "openclaw":
      {
        "emoji": "💹",
        "requires": { "env": ["BINANCE_API_KEY", "BINANCE_API_SECRET"] },
        "primaryEnv": "BINANCE_API_KEY",
      },
  }
---

# Skill: trade-executor（接口定义）

> **接口层**：定义前置条件、风控流程、用户确认格式、审计记录结构，与具体交易所无关。
> 各交易所的下单 API 和签名方式见 `impl/` 目录：
>
> - `impl/binance.md` — Binance 实现
> - `impl/okx.md` — OKX 实现
>
> 新增交易所时，只需添加对应 `impl/{exchange}.md`，本文件无需修改。

## 概述

执行加密货币交易，包含完整的风控检查和用户确认流程。

## 触发条件

- 用户明确要求下单
- market-monitor 产生信号且用户已预授权（`confidence ≥ 0.85`）

## 前置条件（全部满足才执行）

1. 用户已明确确认交易意图
2. 风控检查全部通过（见下方清单）
3. 交易对在白名单中（见 openclaw.json `allowedPairs`）
4. 目标交易所的 API Key 已配置且有效

## 风控检查清单

```
[RISK CHECK] 执行前逐项验证:
├── [ ] 交易对在白名单? (BTC/USDT, ETH/USDT, SOL/USDT)
├── [ ] 单笔金额 ≤ 1,000 USDT?
├── [ ] 今日交易笔数 < 20?  ← 由网关跨 session 追踪
├── [ ] 今日累计亏损 < 500 USDT? ← 由网关跨 session 追踪
├── [ ] 操作类型安全? (非提币/转账/改权限)
├── [ ] 用户已确认?
└── [ ] 止损已设置?
```

任何一项未通过 → 拒绝执行，向用户说明具体原因。

## 执行流程

### 1. 参数验证

```
必需: exchange, pair, side (buy/sell), type (limit/market), quantity
可选: price（limit 单必须）, stopLoss, takeProfit
```

### 2. 用户确认展示

```
交易确认:
  交易所: {exchange}
  交易对: {pair}
  方向:   买入 / 卖出
  类型:   限价单 / 市价单
  价格:   ${price}
  数量:   {quantity} {base}
  金额:   ${amount}
  止损:   ${stopLoss} (-{pct}%)
  止盈:   ${takeProfit} (+{pct}%)

请回复 "确认" 执行，或 "取消" 放弃
```

### 3. 下单

根据 `exchange` 参数加载对应 `impl/{exchange}.md`，调用其下单 API。

### 4. 结果处理

- 成功：返回订单 ID 和成交详情
- 部分成交：通知用户，继续监控剩余数量
- 失败：返回错误说明，建议处理方式

## 审计记录格式

每笔交易由网关自动记录（Vega 无需写入）：

```json
{
  "tradeId": "uuid",
  "timestamp": "ISO8601",
  "exchange": "binance | okx",
  "pair": "BTC/USDT",
  "side": "buy | sell",
  "type": "limit | market",
  "price": 0.0,
  "quantity": 0.0,
  "amountUSD": 0.0,
  "stopLoss": 0.0,
  "takeProfit": 0.0,
  "orderId": "exchange_order_id",
  "status": "filled | partial | rejected | cancelled",
  "riskChecks": { "allPassed": true, "details": [] },
  "userConfirmed": true
}
```

## 安全约束

- 用户确认是强制流程，不可跳过，不可由代码自动确认
- exec = deny，write = deny（Vega 自身不写任何文件）
- 所有交易记录由网关写入审计日志
- 风控违规自动拒绝并告警
