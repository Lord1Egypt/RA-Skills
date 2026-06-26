---
name: vbrokers-trader
description: "VBrokers (华盛通 VCL HK) trading automation via OpenAPI Gateway running on localhost port 11111. Use when: setting up VBrokers or 华盛通 account access, authenticating trading sessions, checking portfolio or positions or funds, placing or cancelling orders for US, HK or A stocks, fetching real-time quotes or K-lines, building automated trading bots, or implementing stop-loss and take-profit logic. Handles AES-ECB password encryption, sessionType for pre/post-market trading, mktTmType for time-segment quotes, and all major trade/quote endpoints."
---

# VBrokers Trader

Automate trading on VBrokers (华盛通 VCL HK) via the OpenAPI Gateway running locally.

## Prerequisites

- **OpenAPI Gateway** must be running locally (GUI app: `华盛通OpenAPIGateway.app`)
- **Gateway URL**: `http://127.0.0.1:11111`
- **AES key** for password encryption: provided during account setup (see references/api-reference.md)
- Python packages: `pycryptodome` (`pip install pycryptodome`)

## Quick Start

Copy `scripts/vbrokers_client.py` to your project and import it:

```python
import sys
sys.path.insert(0, '/path/to/skill/scripts')
import vbrokers_client as vb

# 1. Login (required after Gateway restart)
vb.trade_login("your_trading_password")

# 2. Check account
funds = vb.get_account_funds("P")   # P=US, K=HK

# 3. Get real-time quote (use correct mktTmType for time segment)
quote = vb.get_quotes_batch(["AAPL"], session=-1)  # -1=pre-market

# 4. Place order
result = vb.place_order("AAPL", "P", "1", 1, 180.00)  # BUY 1 share limit $180

# 5. Check positions
positions = vb.get_positions("P")
```

## Key Concepts

### Request Format (Critical)
All HTTP requests must use nested `params`:
```json
{"timeout_sec": 10, "params": {"exchangeType": "P", ...}}
```

### Exchange Types
| Code | Market |
|------|--------|
| `P`  | US Stocks |
| `K`  | HK Stocks |
| `v`  | 深股通 |
| `t`  | 沪股通 |

### Session Types (for orders)
| Value | Meaning |
|-------|---------|
| `"0"` | Regular hours only |
| `"1"` | Extended (pre + post market) — use for US stocks |

### mktTmType (for real-time quotes)
| Value | Segment | Beijing Time |
|-------|---------|--------------|
| `1`   | Regular (盘中) | 22:30–05:00 |
| `-1`  | Pre-market (盘前) | 17:00–22:30 |
| `-2`  | After-hours (盘后) | 05:00–09:00 |
| `-3`  | Night session (夜盘) | 09:00–17:00 |
| omit  | Default (last close) | — |

⚠️ Always specify `mktTmType` for real-time prices — omitting it returns the previous close.

### Password Encryption
Trading password must be AES-ECB encrypted before login:
```python
# Already handled in vbrokers_client.py via encrypt_password()
# Key: base64-encoded 24-byte AES key (provided at account setup)
```

## Common Workflows

### Stop-Loss / Take-Profit Monitor
```python
result = vb.check_stop_loss("AAPL", "P", cost_price=150.0,
                             stop_loss_pct=0.08, take_profit_pct=0.10)
# Returns: {"action": "hold"/"stop_loss"/"take_profit", "current_price": ..., "pnl_pct": ...}
if result["action"] == "stop_loss":
    vb.place_order("AAPL", "P", "2", qty, 0, entrust_type="5")  # market sell
```

### Batch Quotes with Time Segment
```python
from datetime import datetime, timezone, timedelta
bj_hour = (datetime.now(tz=timezone.utc) + timedelta(hours=8)).hour
# Determine correct mktTmType based on Beijing time
session = 1 if (bj_hour >= 22 or bj_hour <= 4) else -1 if bj_hour >= 17 else -2 if bj_hour <= 8 else -3
quotes = vb.get_quotes_batch(["AAPL", "TSLA", "NVDA"], session=session)
```

### Cancel All Orders
```python
vb.cancel_all_orders("P")  # Cancel all pending US stock orders
```

## API Reference

For complete endpoint documentation, parameters, and response schemas:
→ See [references/api-reference.md](references/api-reference.md)

For the full verified client implementation:
→ See [scripts/vbrokers_client.py](scripts/vbrokers_client.py)
