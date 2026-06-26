---
name: quant-trading-api
description: Professional quantitative trading API integration for Chinese securities. Supports major Chinese brokers (华泰, 银河, 广发, 中信建投) with order management, position tracking, real-time market data, and automated trading workflows.
tags:
  - quant
  - trading
  - api
  - broker
  - automation
  - chinese-stock
version: 1.0.0
author: chenq
---

# Quant Trading API

Professional trading API for Chinese securities brokers.

## Supported Brokers

| Broker | Status | Features |
|--------|--------|----------|
| **华泰证券 (Huatai)** | ✅ | Full API |
| **银河证券 (Galaxy)** | ✅ | Full API |
| **广发证券 (GF)** | ✅ | Full API |
| **中信建投 (CITIC)** | ✅ | Full API |
| **同花顺 (iFinD)** | ✅ | 通用接口 |

## Features

### 1. Market Data
- **Real-time Quotes**: Level 1/2 market data
- **K-line Data**: 1min/5min/15min/30min/60min/Daily
- **Order Book**: Top 50 bids/asks
- **Trading Calendar**: A-share trading days
- **Market Status**: Open/Close/Auction

### 2. Order Management
- **Place Orders**: Limit, Market, Stop orders
- **Cancel Orders**: Cancel pending orders
- **Modify Orders**: Change order price/qty
- **Order Status**: Tracking order lifecycle
- **Order History**: Historical order records

### 3. Position Tracking
- **Real-time Positions**: Current holdings
- **Position P&L**: Unrealized/realized P&L
- **Trading History**: Fill records
- **Daily Trades**: Today's transactions

### 4. Account Management
- **Account Balance**: Cash, positions, total assets
- **Margin Info**: Margin ratio, available margin
- **Permissions**: Market/limit order permissions

### 5. Automation
- **Scheduled Trading**: Time-based execution
- **Conditional Orders**: Price/volume triggers
- **Strategy Framework**: Built-in strategy runner
- **Risk Controls**: Auto-stop loss/take profit

## Installation

```bash
pip install requests pycryptodome websocket-client
```

## Configuration

```python
# config.py
BROKER_CONFIG = {
    'broker': 'huatai',  # huatai, galaxy, gf, citic, tonghuashun
    'account': '123456789',
    'password': 'your_password',
    'server': 'trade.htsc.com.cn',  # Trading server
    'market': 'sz'  # sh, sz
}
```

## Usage

### Initialize Trading API
```python
from quant_trading import TradingAPI

api = TradingAPI(
    broker='huatai',
    account='123456789',
    password='your_password'
)

# Login
api.login()
print(f"Login successful: {api.account_info['account_name']}")
```

### Get Market Data
```python
# Real-time quote
quote = api.get_quote('600519')
print(f"Price: {quote['price']}, Volume: {quote['volume']}")

# K-line data
kline = api.get_kline('000858', period='60min', count=100)
print(kline.tail())
```

### Place Order
```python
# Buy stock
order = api.buy(
    symbol='600519',
    price=1850.0,
    volume=100
)
print(f"Order ID: {order['order_id']}")

# Sell stock
order = api.sell(
    symbol='600519',
    price=1900.0,
    volume=100
)
```

### Order Management
```python
# Cancel order
api.cancel_order(order_id='123456')

# Get order status
status = api.get_order(order_id='123456')
print(f"Status: {status['status']}")

# Get all orders
orders = api.get_orders(status='pending')
```

### Position & Account
```python
# Get positions
positions = api.get_positions()
for pos in positions:
    print(f"{pos['symbol']}: {pos['volume']} shares, P&L: {pos['pnl']}")

# Get account balance
balance = api.get_balance()
print(f"Total Assets: {balance['total_assets']}")
print(f"Available Cash: {balance['available']}")
```

## API Reference

### Connection
| Method | Description |
|--------|-------------|
| `login()` | Login to broker |
| `logout()` | Logout |
| `heartbeat()` | Keep connection alive |

### Market Data
| Method | Description |
|--------|-------------|
| `get_quote(symbol)` | Get real-time quote |
| `get_kline(symbol, period, count)` | Get K-line data |
| `get_orderbook(symbol)` | Get order book |
| `get_trading_calendar(start, end)` | Get trading days |

### Orders
| Method | Description |
|--------|-------------|
| `buy(symbol, price, volume)` | Place buy order |
| `sell(symbol, price, volume)` | Place sell order |
| `cancel_order(order_id)` | Cancel order |
| `get_order(order_id)` | Get order status |
| `get_orders(status)` | Get all orders |

### Positions
| Method | Description |
|--------|-------------|
| `get_positions()` | Get current positions |
| `get_trades()` | Get today's trades |
| `get_history(start, end)` | Historical records |

### Account
| Method | Description |
|--------|-------------|
| `get_balance()` | Get account balance |
| `get_margin()` | Get margin info |

## Advanced Usage

### Automated Trading Strategy
```python
from quant_trading import TradingAPI, Strategy

class MomentumStrategy(Strategy):
    def __init__(self, api):
        self.api = api
    
    def on_bar(self, bar):
        # Check signal
        if self.check_signal(bar):
            # Place order
            self.api.buy(bar['symbol'], bar['close'], 100)
    
    def check_signal(self, bar):
        # Your logic
        return bar['volume'] > 1000000

# Run strategy
api = TradingAPI(...)
strategy = MomentumStrategy(api)
api.run_strategy(strategy)
```

### Scheduled Trading
```python
# Execute at specific time
api.schedule_order(
    symbol='600519',
    direction='buy',
    price=1850.0,
    volume=100,
    execute_time='09:35:00'
)
```

### Stop Loss / Take Profit
```python
# Set stop loss
api.set_stop_loss(
    symbol='600519',
    entry_price=1850.0,
    stop_loss_pct=0.05  # 5% stop loss
)

# Set take profit
api.set_take_profit(
    symbol='600519',
    entry_price=1850.0,
    take_profit_pct=0.15  # 15% take profit
)
```

## Error Handling

```python
try:
    order = api.buy('600519', 1850.0, 100)
except OrderError as e:
    print(f"Order failed: {e.message}")
    if e.code == 'INSUFFICIENT_BALANCE':
        print("Insufficient balance")
    elif e.code == 'LIMIT_UP':
        print("Stock hit limit up")
    elif e.code == 'SUSPENDED':
        print("Stock suspended")
```

## Common Error Codes

| Code | Description |
|------|-------------|
| `SUCCESS` | Order successful |
| `INSUFFICIENT_BALANCE` | Insufficient cash |
| `INSUFFICIENT_POSITION` | Insufficient shares |
| `LIMIT_UP` | Stock at limit up |
| `LIMIT_DOWN` | Stock at limit down |
| `SUSPENDED` | Stock suspended |
| `NOT_TRADING` | Outside trading hours |
| `INVALID_PRICE` | Price out of range |

## Best Practices

1. **Connection Management**: Reconnect on failure
2. **Rate Limiting**: Don't exceed API limits
3. **Order Validation**: Validate before placing
4. **Error Handling**: Always handle exceptions
5. **Logging**: Log all trading activities
6. **Risk Controls**: Set stop loss/take profit

## Links

- [华泰API文档](https://openapi.htsc.com)
- [银河API文档](https://api.galaxy.com)
- [同花顺API](https://tushare.pro)
