# tools/formatters.py

from datetime import datetime


def _fmt_time_ms(ts):
    try:
        if ts is None:
            return "-"
        return datetime.fromtimestamp(float(ts) / 1000).strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(ts)


def _fmt_symbol_display(symbol: str):
    if not symbol:
        return "-"
    s = str(symbol).upper()
    if "/" in s:
        return s
    if s.endswith("USDT"):
        return s[:-4] + "/USDT"
    if s.endswith("USDC"):
        return s[:-4] + "/USDC"
    return s


def _fmt_contract_display(contract: str):
    if not contract:
        return "-"
    return str(contract).upper()


def _fmt_futures_status(status):
    mapping = {
        0: "初始",
        1: "新订单",
        2: "完全成交",
        3: "部分成交",
        4: "已取消/未成交结束",
        5: "部分成交后取消",
        6: "异常",
    }
    try:
        s = int(status)
        return mapping.get(s, str(status))
    except Exception:
        s = str(status).strip().upper()
        text_mapping = {
            "INIT": "初始",
            "NEW": "新订单",
            "FILLED": "完全成交",
            "PARTIALLY_FILLED": "部分成交",
            "PART_FILLED": "部分成交",
            "CANCELED": "已取消",
            "CANCELLED": "已取消",
            "REJECTED": "拒单",
            "ERROR": "异常",
        }
        return text_mapping.get(s, str(status))


def _fmt_position_type(position_type):
    mapping = {
        1: "全仓",
        2: "逐仓",
    }
    try:
        v = int(position_type)
        return mapping.get(v, str(position_type))
    except Exception:
        s = str(position_type).strip().lower()
        if s == "cross":
            return "全仓"
        if s == "isolated":
            return "逐仓"
        return str(position_type)


def _fmt_side(side):
    if side is None:
        return "-"
    s = str(side).upper()
    if s == "BUY":
        return "多"
    if s == "SELL":
        return "空"
    if s == "LONG":
        return "多"
    if s == "SHORT":
        return "空"
    return s


def _fmt_open_close(value):
    if value is None:
        return "-"
    s = str(value).upper()
    if s == "OPEN":
        return "开仓"
    if s == "CLOSE":
        return "平仓"
    return s


def _fmt_order_type(value):
    if value is None:
        return "-"
    s = str(value).upper()
    mapping = {
        "LIMIT": "限价",
        "MARKET": "市价",
        "IOC": "IOC",
        "FOK": "FOK",
        "POST_ONLY": "只做Maker",
    }
    return mapping.get(s, s)


def print_asset_balance_pretty(summary):
    print(f"币种: {summary.get('asset', '-')}")
    print(f"可用: {summary.get('free', '0')}")
    print(f"冻结: {summary.get('locked', '0')}")


def print_account_balances_pretty(balances):
    print("账户资产:")
    print()

    if not balances:
        print("没有可显示的资产")
        return

    for b in balances:
        asset = b.get("asset", "")
        free = b.get("free", "0")
        locked = b.get("locked", "0")
        print(f"{asset:<12} 可用: {free:<18} 冻结: {locked}")


# =========================
# Spot
# =========================

def print_ticker_pretty(symbol, data):
    print(f"交易对: {_fmt_symbol_display(symbol)}")
    print(f"最新价: {data.get('last', '-')}")
    print(f"买一: {data.get('bidPrice', data.get('buy', '-'))}")
    print(f"卖一: {data.get('askPrice', data.get('sell', '-'))}")
    print(f"24h最高: {data.get('high', '-')}")
    print(f"24h最低: {data.get('low', '-')}")
    print(f"24h成交量: {data.get('vol', '-')}")
    print(f"24h涨跌幅: {data.get('rose', '-')}")
    print(f"开盘价: {data.get('open', '-')}")
    print(f"时间: {_fmt_time_ms(data.get('time'))}")


def print_depth_pretty(symbol, depth, limit):
    print(f"交易对: {_fmt_symbol_display(symbol)}")
    print(f"深度档数: {limit}")
    print()

    bids = depth.get("bids", []) or []
    asks = depth.get("asks", []) or []

    print(f"买盘前{min(limit, len(bids))}档:")
    if not bids:
        print("无买盘数据")
    else:
        for i, b in enumerate(bids[:limit], start=1):
            price = b[0] if len(b) > 0 else "-"
            qty = b[1] if len(b) > 1 else "-"
            print(f"{i:2d}. 价格: {price} | 数量: {qty}")

    print()
    print(f"卖盘前{min(limit, len(asks))}档:")
    if not asks:
        print("无卖盘数据")
    else:
        for i, a in enumerate(asks[:limit], start=1):
            price = a[0] if len(a) > 0 else "-"
            qty = a[1] if len(a) > 1 else "-"
            print(f"{i:2d}. 价格: {price} | 数量: {qty}")


def print_open_orders_pretty(display_symbol, orders):
    if isinstance(orders, dict):
        if isinstance(orders.get("list"), list):
            order_list = orders.get("list", [])
        elif isinstance(orders.get("data"), list):
            order_list = orders.get("data", [])
        elif orders.get("data") is None and str(orders.get("code")) == "0":
            order_list = []
        else:
            order_list = []
    elif isinstance(orders, list):
        order_list = orders
    else:
        order_list = []

    print(f"交易对: {_fmt_symbol_display(display_symbol)}")
    print(f"当前挂单数量: {len(order_list)}")
    print()

    if not order_list:
        print("当前没有挂单")
        return

    for i, o in enumerate(order_list, start=1):
        side = o.get("side", "-")
        price = o.get("price", "-")
        qty = o.get("volume", o.get("origQty", "-"))
        executed = o.get("dealVolume", o.get("executedQty", "-"))
        status = o.get("status", "-")
        ts = o.get("time", o.get("transactTime"))

        print(f"{i}. 方向: {side}")
        print(f"   价格: {price}")
        print(f"   数量: {qty}")
        print(f"   已成交: {executed}")
        print(f"   状态: {status}")
        if ts is not None:
            print(f"   时间: {_fmt_time_ms(ts)}")
        print()


def print_my_trades_pretty(display_symbol, trades):
    if isinstance(trades, dict):
        if isinstance(trades.get("list"), list):
            trade_list = trades.get("list", [])
        elif isinstance(trades.get("data"), list):
            trade_list = trades.get("data", [])
        else:
            trade_list = []
    elif isinstance(trades, list):
        trade_list = trades
    else:
        trade_list = []

    print(f"交易对: {_fmt_symbol_display(display_symbol)}")
    print(f"成交记录数量: {len(trade_list)}")
    print()

    if not trade_list:
        print("当前没有成交记录")
        return

    for i, t in enumerate(trade_list, start=1):
        side = t.get("side", "BUY" if t.get("isBuyer") else "SELL")
        price = t.get("price", "-")
        qty = t.get("qty", t.get("volume", "-"))
        fee = t.get("fee", "-")
        fee_coin = t.get("feeCoin", "-")
        trade_time = t.get("time", "-")
        is_maker = t.get("isMaker", "-")

        print(f"{i}. 方向: {side}")
        print(f"   价格: {price}")
        print(f"   数量: {qty}")
        print(f"   手续费: {fee} {fee_coin}")
        print(f"   Maker: {is_maker}")
        print(f"   时间: {_fmt_time_ms(trade_time)}")
        print()


# =========================
# Futures
# =========================

def print_futures_ticker_pretty(contract, data):
    print(f"合约: {_fmt_contract_display(contract)}")
    print(f"最新价: {data.get('last', '-')}")
    print(f"买一: {data.get('buy', data.get('bidPrice', '-'))}")
    print(f"卖一: {data.get('sell', data.get('askPrice', '-'))}")
    print(f"24h最高: {data.get('high', '-')}")
    print(f"24h最低: {data.get('low', '-')}")
    print(f"24h成交量: {data.get('vol', '-')}")
    print(f"涨跌幅: {data.get('rose', '-')}")
    print(f"时间: {_fmt_time_ms(data.get('time'))}")


def print_futures_index_pretty(contract, data):
    print(f"合约: {_fmt_contract_display(contract)}")
    print(f"标记价格: {data.get('tagPrice', data.get('markPrice', '-'))}")
    print(f"指数价格: {data.get('indexPrice', '-')}")
    print(f"当前资金费率: {data.get('currentFundRate', data.get('lastFundingRate', '-'))}")
    print(f"下一期资金费率: {data.get('nextFundRate', '-')}")
    print(f"时间: {_fmt_time_ms(data.get('time'))}")


def print_futures_balance_pretty(data):
    print("合约账户资产:")
    print()

    account_list = data.get("account", []) if isinstance(data, dict) else []

    if not account_list:
        print("没有账户数据")
        return

    for acc in account_list:
        coin = acc.get("marginCoin", "-")
        normal = acc.get("accountNormal", 0)
        equity = acc.get("totalEquity", 0)
        unrealized = acc.get("unrealizedAmount", 0)
        print(f"{coin:<10} 余额: {normal:<15} 权益: {equity:<15} 未实现盈亏: {unrealized}")


def print_futures_positions_pretty(positions):
    if not positions:
        print("当前没有持仓")
        return

    print("当前持仓:")
    print()

    for p in positions:
        contract = p.get("_contractName", p.get("contract", "-"))
        side = _fmt_side(p.get("side", "-"))
        pos_type = _fmt_position_type(p.get("positionType", p.get("position_type", "-")))
        volume = p.get("volume", 0)
        open_price = p.get("openPrice", p.get("open_price", "-"))
        avg_price = p.get("avgPrice", p.get("avg_price", "-"))
        leverage = p.get("leverageLevel", p.get("leverage", "-"))
        unrealized = p.get("unRealizedAmount", p.get("unrealizedAmount", p.get("unrealized_pnl", "-")))
        margin_coin = p.get("_marginCoin", p.get("margin_coin", "-"))

        print(f"合约: {contract}")
        print(f"方向: {side}")
        print(f"仓位类型: {pos_type}")
        print(f"数量: {volume} 张")
        print(f"开仓价: {open_price}")
        print(f"持仓均价: {avg_price}")
        print(f"杠杆: {leverage}x")
        print(f"未实现盈亏: {unrealized} {margin_coin}")
        print()


def print_futures_my_trades_pretty(trades):
    if isinstance(trades, dict):
        if isinstance(trades.get("data"), list):
            trade_list = trades.get("data", [])
        elif isinstance(trades.get("list"), list):
            trade_list = trades.get("list", [])
        else:
            trade_list = []
    elif isinstance(trades, list):
        trade_list = trades
    else:
        trade_list = []

    if not trade_list:
        print("没有成交记录")
        return

    print("成交记录:")
    print()

    for t in trade_list:
        contract = t.get("contract") or t.get("contractName") or "-"
        price = t.get("price", "-")
        qty = t.get("qty", t.get("volume", "-"))
        side = str(t.get("side", "-")).upper()
        fee = t.get("fee", "-")
        ts = t.get("time")

        print(f"{side} {qty}张 {contract}")
        print(f"价格: {price} USDT")
        print(f"手续费: {fee} USDT")
        print(f"时间: {_fmt_time_ms(ts)}")
        print()


def print_futures_order_history_pretty(orders):
    if isinstance(orders, dict):
        if isinstance(orders.get("data"), list):
            order_list = orders.get("data", [])
        elif isinstance(orders.get("list"), list):
            order_list = orders.get("list", [])
        else:
            order_list = []
    elif isinstance(orders, list):
        order_list = orders
    else:
        order_list = []

    if not order_list:
        print("没有历史订单")
        return

    print("历史订单:")
    print()

    for o in order_list:
        contract = o.get("contractName", o.get("contract", "-"))
        side = _fmt_side(o.get("side", "-"))
        price = o.get("price", "-")
        volume = o.get("volume", "-")
        status = _fmt_futures_status(o.get("status", "-"))
        open_or_close = _fmt_open_close(o.get("openOrClose", o.get("action", "-")))
        deal_volume = o.get("dealVolume", o.get("deal_volume", "-"))
        pos_type = _fmt_position_type(o.get("positionType", o.get("position_mode", "-")))
        order_type = _fmt_order_type(o.get("type", o.get("order_type", "-")))
        ctime = o.get("ctimeMs", o.get("ctime", o.get("time")))

        print(f"合约: {contract}")
        print(f"方向: {side}")
        print(f"开平: {open_or_close}")
        print(f"仓位类型: {pos_type}")
        print(f"订单类型: {order_type}")
        print(f"价格: {price}")
        print(f"数量: {volume} 张")
        print(f"成交数量: {deal_volume} 张")
        print(f"状态: {status}")
        print(f"时间: {_fmt_time_ms(ctime) if isinstance(ctime, (int, float)) else ctime}")
        print()


def print_futures_profit_pretty(records):
    if isinstance(records, dict):
        if isinstance(records.get("data"), list):
            record_list = records.get("data", [])
        elif isinstance(records.get("list"), list):
            record_list = records.get("list", [])
        else:
            record_list = []
    elif isinstance(records, list):
        record_list = records
    else:
        record_list = []

    if not record_list:
        print("没有盈亏记录")
        return

    print("盈亏记录:")
    print()

    for r in record_list:
        contract = r.get("contractName", r.get("contract", "-"))
        side = _fmt_side(r.get("side", "-"))
        profit = r.get("closeProfit", r.get("profit", "-"))
        fee = r.get("tradeFee", r.get("fee", "-"))
        leverage = r.get("leverageLevel", r.get("leverage", "-"))
        open_price = r.get("openPrice", r.get("open_price", "-"))
        pos_type = _fmt_position_type(r.get("positionType", r.get("position_mode", "-")))
        ctime = r.get("ctime", r.get("time"))

        print(f"合约: {contract}")
        print(f"方向: {side}")
        print(f"仓位类型: {pos_type}")
        print(f"开仓价: {open_price}")
        print(f"杠杆: {leverage}x")
        print(f"平仓盈亏: {profit}")
        print(f"手续费: {fee}")
        print(f"时间: {_fmt_time_ms(ctime) if isinstance(ctime, (int, float)) else ctime}")
        print()
