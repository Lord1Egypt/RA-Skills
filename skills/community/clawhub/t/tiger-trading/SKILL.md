---
name: tiger-trading
version: 1.0.0
description: 老虎证券美股交易能力。支持账户余额查询、持仓查询、买卖下单、订单管理。用户只需提供 tiger_id、account、license 和 private_key 即可使用。触发场景：(1) 查询老虎账户状态 (2) 买卖美股 (3) 查看持仓 (4) 取消订单
---

# Tiger Trading Skill

使用 Tiger 客户端进行美股交易。

## 快速开始

用户提供以下信息即可使用：
- `tiger_id`: Tiger ID
- `account`: 账户ID
- `license`: 许可证 (通常为 TBNZ)
- `private_key`: 私钥内容或私钥文件路径

## 使用方式

### 1. 初始化客户端

```python
import sys
sys.path.insert(0, 'skills/tiger-trading/scripts')
from tiger_client import TigerClient

# 方式1: 使用私钥文件路径
client = TigerClient(
    tiger_id='YOUR_TIGER_ID',
    account='YOUR_ACCOUNT_ID',
    license='TBNZ',
    private_key='/path/to/private_key.pem'
)

# 方式2: 使用私钥内容
client = TigerClient(
    tiger_id='YOUR_TIGER_ID',
    account='YOUR_ACCOUNT_ID',
    license='TBNZ',
    private_key='MIICXAIBAAKBgQ...'
)
```

### 2. 查询功能

```python
# 查询账户
client.get_account()

# 查询持仓
client.get_positions()

# 查询余额
client.get_balance()

# 查询订单 (传入状态列表过滤)
client.get_orders()  # 所有订单
```

### 3. 交易功能

```python
# 限价买单
client.place_order(
    symbol='AAPL',
    side='buy',
    quantity=100,
    order_type='LMT',  # LMT=限价单, MKT=市价单
    price=150.0
)

# 市价卖单
client.place_order(
    symbol='AAPL',
    side='sell',
    quantity=50,
    order_type='MKT'
)
```

### 4. 订单管理

```python
# 取消订单
client.cancel_order(order_id='123456')
```

## CLI 用法

```bash
# 余额查询
python skills/tiger-trading/scripts/tiger_client.py \
  --tiger-id YOUR_TIGER_ID \
  --account YOUR_ACCOUNT_ID \
  --license TBNZ \
  --private-key /path/to/private_key.pem balance

# 持仓查询
python skills/tiger-trading/scripts/tiger_client.py \
  --tiger-id YOUR_TIGER_ID \
  --account YOUR_ACCOUNT_ID \
  --license TBNZ \
  --private-key /path/to/private_key.pem positions

# 下单
python skills/tiger-trading/scripts/tiger_client.py \
  --tiger-id YOUR_TIGER_ID \
  --account YOUR_ACCOUNT_ID \
  --license TBNZ \
  --private-key /path/to/private_key.pem order \
  --symbol AAPL --side buy --quantity 100 --price 150.0
```

## 返回格式示例

### 余额
```json
{
  "success": true,
  "balance": {
    "cash": 100000.0,
    "buying_power": 400000.0,
    "net_liquidation": 100000.0,
    "unrealized_pnl": 0.0,
    "currency": "USD"
  }
}
```

### 持仓
```json
{
  "success": true,
  "positions": [
    {
      "symbol": "AAPL",
      "quantity": 100,
      "avg_cost": 150.0,
      "market_value": 15000.0,
      "unrealized_pnl": 0.0,
      "unrealized_pnl_percent": 0.0
    }
  ]
}
```

## 注意事项

1. 私钥支持文件路径或直接内容两种方式
2. 默认使用模拟盘环境 (license=TBNZ)
3. order_type: LMT=限价单, MKT=市价单
4. 真实账户需要提供真实的 license 和账户信息
