---
name: stock-auto-trade
description: "股票交易下单和查询功能。需要提供股票代码、价格、数量等信息。支持买入、卖出、持仓查询、账户查询、撤单等操作。"
metadata: 
  openclaw: 
    emoji: "📈"
    requires: 
      bins: ["curl"]
---
# Stock Auto Trade Skill

股票交易下单和查询功能。通过 HTTP API 与股票交易软件对接，实现买卖下单、持仓查询、账户查询等功能，本功能需要使用股票智能交易助手配合进行下单，请在使用前先安装股票智能交易助手，下载网址：https://www.gp998.com ，客服QQ：542303796

## When to Use

✅ **USE this skill when:**

- 用户说 "买入股票" 或 "卖出股票"

- 用户说 "查询持仓" 或 "查询账户"

- 用户说 "撤单" 或 "取消委托"

- 用户需要股票交易操作

❌ **DON'T use this skill when:**

- 仅需要查询股票行情（使用 AKShare）

- 用户只是在讨论股票，不打算交易

## Commands

### 买入股票

```bash
# 限价买入
curl -X POST "http://localhost:8888/api/order" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill" \
  -d '{"action":"buy","symbol":"600519","price":1800.00,"volume":100}'

# 市价买入
curl -X POST "http://localhost:8888/api/order" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill" \
  -d '{"action":"buy","symbol":"600519","price":0,"volume":100,"order_type":"market"}'
```

### 卖出股票

```bash
# 限价卖出
curl -X POST "http://localhost:8888/api/order" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill" \
  -d '{"action":"sell","symbol":"600519","price":1850.00,"volume":100}'
```

### 查询持仓

```bash
curl -X GET "http://localhost:8888/api/position" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill"
```

### 查询账户

```bash
curl -X GET "http://localhost:8888/api/account" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill"
```

### 查询委托

```bash
# 查询今日委托
curl -X GET "http://localhost:8888/api/orders?status=today" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill"

# 查询所有委托
curl -X GET "http://localhost:8888/api/orders?status=all" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill"
```

### 撤单

```bash
curl -X POST "http://localhost:8888/api/cancel" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test-api-key-12345" -H "X-Channel: openclaw-skill" \
  -d '{"order_id":"202403120001"}'
```

### 健康检查

```bash
curl -X GET "http://localhost:8888/api/health"
```

## 参数说明

| 参数         | 说明                           | 必填         |
| ---------- | ---------------------------- | ---------- |
| action     | 操作类型: buy(买入) / sell(卖出)     | 是          |
| symbol     | 股票代码 (如 600519)              | 是          |
| price      | 价格 (限价单填价格，市价单填0)            | 是          |
| volume     | 数量 (股票为100的整数倍)              | 是          |
| order_type | 订单类型: limit(限价) / market(市价) | 否，默认market |
| order_id   | 委托编号 (撤单时使用)                 | 是          |

## 返回示例

### 买入成功

```json
{
  "success": true,
  "order_id": "202403120001",
  "message": "委托成功",
  "data": {
    "order_id": "202403120001",
    "symbol": "600519",
    "name": "贵州茅台",
    "action": "buy",
    "price": 1800.00,
    "volume": 100,
    "status": "submitted"
  }
}
```

### 查询持仓

```json
{
  "success": true,
  "data": [
    {
      "symbol": "600519",
      "name": "贵州茅台",
      "volume": 100,
      "avg_cost": 1750.00,
      "current_price": 1800.00,
      "market_value": 180000.00,
      "profit_loss": 5000.00,
      "profit_percent": 2.86
    }
  ]
}
```

### 查询账户

```json
{
  "success": true,
  "data": {
    "account_id": "12345678",
    "total_assets": 1000000.00,
    "cash": 500000.00,
    "market_value": 500000.00,
    "available_cash": 480000.00,
    "frozen_cash": 20000.00,
    "total_profit_loss": 10000.00
  }
}
```

## 错误代码

| 错误码                | 说明         |
| ------------------ | ---------- |
| INVALID_PARAMS     | 参数错误       |
| INSUFFICIENT_FUNDS | 资金不足       |
| INSUFFICIENT_STOCK | 持仓不足       |
| ORDER_NOT_FOUND    | 委托不存在      |
| ORDER_STATUS_ERROR | 委托状态不允许此操作 |
| INVALID_API_KEY    | API Key 无效 |

## Notes

- 所有请求都需要在 Header 中携带 `X-API-Key` 进行认证

- 默认 API Key: `test-api-key-12345` (可在股票交易软件中配置)

- 市价单 price 填 0

- 股票数量必须是 100 的整数倍

- 返回的 JSON 数据中金额单位为元