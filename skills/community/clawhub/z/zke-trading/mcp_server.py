import json
import time
import os
from pathlib import Path
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from tools.zke_client import ZKEClient
from tools.spot_public import SpotPublicApi
from tools.spot_private import SpotPrivateApi
from tools.futures_public import FuturesPublicApi
from tools.futures_private import FuturesPrivateApi
from tools.margin_private import MarginPrivateApi

from tools import market_service
from tools import account_service
from tools import order_service
from tools import futures_service
from tools import futures_account_service
from tools import futures_order_service
from tools import margin_order_service
from tools import withdraw_service
from tools import transfer_service
from tools.field_mapper import map_side, map_position_type, map_order_status
from tools.ws_client import ZKEWebSocketClient
from tools.ws_parser import normalize_ws_message
from tools import ws_service

BASE_DIR = Path(__file__).resolve().parent

mcp = FastMCP("zke-trading")

def build_spot_client() -> ZKEClient:
    api_key = os.environ.get("ZKE_API_KEY", "")
    api_secret = os.environ.get("ZKE_SECRET_KEY", "")
    
    return ZKEClient(
        base_url="https://openapi.zke.com",
        api_key=api_key,
        api_secret=api_secret,
        recv_window=5000,
    )

def build_futures_client() -> ZKEClient:
    api_key = os.environ.get("ZKE_API_KEY", "")
    api_secret = os.environ.get("ZKE_SECRET_KEY", "")
    
    return ZKEClient(
        base_url="https://futuresopenapi.zke.com",
        api_key=api_key,
        api_secret=api_secret,
        recv_window=5000,
    )

def get_ws_url() -> str:
    return "wss://ws.zke.com/kline-api/ws"

SPOT_CLIENT = build_spot_client()
SPOT_PUBLIC = SpotPublicApi(SPOT_CLIENT)
SPOT_PRIVATE = SpotPrivateApi(SPOT_CLIENT)
MARGIN_PRIVATE = MarginPrivateApi(SPOT_CLIENT)

FUTURES_CLIENT = build_futures_client()
FUTURES_PUBLIC = FuturesPublicApi(FUTURES_CLIENT)
FUTURES_PRIVATE = FuturesPrivateApi(FUTURES_CLIENT)

SPOT_REGISTRY = market_service.get_registry(SPOT_PUBLIC)
FUTURES_REGISTRY = futures_service.get_registry(FUTURES_PUBLIC)


def _sanitize_id(obj: Any):
    """
    统一将所有容易导致 JS 和大模型精度丢失的 ID 或大数值字段转为字符串。
    """
    if isinstance(obj, list):
        for item in obj:
            _sanitize_id(item)
    elif isinstance(obj, dict):
        # 将常见的大整数/ID 字段转为字符串
        id_keys = [
            "orderId", "order_id", "orderIdString", 
            "clientOrderId", "client_order_id", 
            "position_id", "positionId", 
            "tradeId", "trade_id", "id"
        ]
        for key in id_keys:
            if key in obj and obj[key] is not None:
                obj[key] = str(obj[key])
                
        for val in obj.values():
            if isinstance(val, (dict, list)):
                _sanitize_id(val)

def _normalize_list_result(raw: Any) -> List[Dict[str, Any]]:
    res = []
    if isinstance(raw, dict):
        if isinstance(raw.get("list"), list): res = raw["list"]
        elif isinstance(raw.get("data"), list): res = raw["data"]
        elif raw.get("data") is None and str(raw.get("code")) == "0": res = []
    elif isinstance(raw, list):
        res = raw
    
    _sanitize_id(res) # 返回前强制清洗伪装
    return res


# =========================================================
# WebSocket helpers
# =========================================================

def _collect_ws_messages(subscriptions: List[dict], seconds: int = 3, limit: int = 20, debug: bool = False) -> Dict[str, Any]:
    messages: List[Dict[str, Any]] = []
    def _handler(data: Any):
        try: normalized = normalize_ws_message(data)
        except Exception: normalized = {"type": "unknown", "raw": data}
        if len(messages) < limit: messages.append(normalized)
    client = ZKEWebSocketClient(url=get_ws_url(), subscriptions=subscriptions, on_message=_handler, reconnect=False, reconnect_delay=1, debug=debug)
    thread = client.start_background()
    try: time.sleep(max(1, int(seconds)))
    finally: client.close()
    if thread: thread.join(timeout=2)
    return {"ws_url": get_ws_url(), "seconds": max(1, int(seconds)), "count": len(messages), "messages": messages}


# =========================================================
# Spot - Readonly
# =========================================================

@mcp.tool()
def get_spot_ticker(symbol: str) -> Dict[str, Any]:
    data = market_service.get_ticker(SPOT_PUBLIC, SPOT_REGISTRY, symbol)
    return {"symbol": symbol.upper(), "last": data.get("last"), "buy": data.get("buy", data.get("bidPrice")), "sell": data.get("sell", data.get("askPrice")), "high": data.get("high"), "low": data.get("low"), "vol": data.get("vol"), "rose": data.get("rose"), "open": data.get("open"), "time": data.get("time")}

@mcp.tool()
def get_spot_depth(symbol: str, limit: int = 20) -> Dict[str, Any]:
    data = market_service.get_depth(SPOT_PUBLIC, SPOT_REGISTRY, symbol, limit)
    return {"symbol": symbol.upper(), "limit": limit, "bids": data.get("bids", []), "asks": data.get("asks", [])}

@mcp.tool()
def get_spot_klines(symbol: str, interval: str = "1day") -> Dict[str, Any]:
    data = market_service.get_klines(SPOT_PUBLIC, SPOT_REGISTRY, symbol, interval)
    return {"symbol": symbol.upper(), "interval": interval, "klines": data, "count": len(data) if isinstance(data, list) else 0}

@mcp.tool()
def get_spot_account() -> Dict[str, Any]:
    data = SPOT_PRIVATE.account()
    _sanitize_id(data); return data

@mcp.tool()
def get_spot_nonzero_balances() -> Dict[str, Any]:
    account_data = SPOT_PRIVATE.account()
    balances = account_service.extract_account_balances(account_data)
    nonzero = account_service.filter_nonzero_balances(balances)
    return {"balances": nonzero, "count": len(nonzero)}

@mcp.tool()
def get_spot_balance(asset: str) -> Dict[str, Any]:
    account_data = SPOT_PRIVATE.account()
    balances = account_service.extract_account_balances(account_data)
    summary = account_service.get_asset_balance_summary(balances, asset)
    return {"asset": summary.get("asset"), "free": summary.get("free"), "locked": summary.get("locked")}

@mcp.tool()
def get_spot_account_by_type(account_type: str) -> Dict[str, Any]:
    data = SPOT_PRIVATE.account_by_type(account_type)
    _sanitize_id(data); return data

@mcp.tool()
def get_spot_open_orders(symbol: str, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    raw = SPOT_PRIVATE.open_orders(api_symbol, limit)
    orders = _normalize_list_result(raw)
    return {"symbol": symbol.upper(), "orders": orders, "count": len(orders)}

@mcp.tool()
def get_spot_my_trades(symbol: str, limit: int = 10) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    raw = SPOT_PRIVATE.my_trades(api_symbol, limit)
    trades = _normalize_list_result(raw)
    return {"symbol": symbol.upper(), "trades": trades, "count": len(trades)}

@mcp.tool()
def get_spot_my_trades_v3(symbol: str, limit: int = 10) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    raw = SPOT_PRIVATE.my_trades_v3(symbol=api_symbol, limit=limit)
    trades = _normalize_list_result(raw)
    return {"symbol": symbol.upper(), "trades": trades, "count": len(trades)}

@mcp.tool()
def get_spot_history_orders(symbol: str, limit: int = 10) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    raw = SPOT_PRIVATE.history_orders(symbol=api_symbol, limit=limit)
    orders = _normalize_list_result(raw)
    return {"symbol": symbol.upper(), "orders": orders, "count": len(orders)}


# =========================================================
# Spot - Trading
# =========================================================

@mcp.tool()
def create_spot_order(symbol: str, side: str, order_type: str, volume: str, price: str = "") -> Dict[str, Any]:
    p = price.strip() if isinstance(price, str) else price
    if p == "": p = None
    data, result = order_service.create_order(SPOT_PRIVATE, SPOT_REGISTRY, symbol, side, order_type, volume, p)
    _sanitize_id(result)
    return {"request": data, "result": result}

@mcp.tool()
def cancel_spot_order(symbol: str, order_id: str = "", client_order_id: str = "") -> Dict[str, Any]:
    """
    撤销现货订单。
    """
    safe_oid = str(order_id).strip() if order_id else ""
    safe_cid = str(client_order_id).strip() if client_order_id else ""

    result = order_service.cancel_order(SPOT_PRIVATE, SPOT_REGISTRY, symbol, order_id=safe_oid, client_order_id=safe_cid)
    _sanitize_id(result)
    return {"symbol": symbol.upper(), "result": result}


# =========================================================
# Spot Transfer
# =========================================================

@mcp.tool()
def transfer_spot_to_futures(coin_symbol: str, amount: str) -> Dict[str, Any]:
    res = transfer_service.transfer_spot_to_futures(SPOT_PRIVATE, coin_symbol, amount)
    _sanitize_id(res); return res

@mcp.tool()
def transfer_futures_to_spot(coin_symbol: str, amount: str) -> Dict[str, Any]:
    res = transfer_service.transfer_futures_to_spot(SPOT_PRIVATE, coin_symbol, amount)
    _sanitize_id(res); return res

@mcp.tool()
def get_transfer_history(coin_symbol: str = "", from_account: str = "", to_account: str = "", limit: int = 20) -> Dict[str, Any]:
    rows = transfer_service.query_transfer_history(api=SPOT_PRIVATE, coin_symbol=coin_symbol if coin_symbol else None, from_account=from_account if from_account else None, to_account=to_account if to_account else None, limit=limit)
    _sanitize_id(rows)
    return {"coin_symbol": coin_symbol, "from_account": from_account, "to_account": to_account, "records": rows, "count": len(rows)}


# =========================================================
# Withdraw
# =========================================================

@mcp.tool()
def create_withdraw(coin: str, address: str, amount: str, network: str = "", memo: str = "") -> Dict[str, Any]:
    result = withdraw_service.apply_withdraw(SPOT_PRIVATE, coin, address, amount, network if network else None, memo if memo else None)
    _sanitize_id(result); return result

@mcp.tool()
def get_withdraw_history(coin: str = "", limit: int = 20) -> Dict[str, Any]:
    rows = withdraw_service.withdraw_history(SPOT_PRIVATE, coin if coin else None, limit)
    _sanitize_id(rows)
    return {"coin": coin, "records": rows, "count": len(rows)}


# =========================================================
# Margin
# =========================================================

@mcp.tool()
def create_margin_order(symbol: str, side: str, order_type: str, volume: str, price: str = "") -> Dict[str, Any]:
    p = price.strip() if isinstance(price, str) else price
    if p == "": p = None
    data, result = margin_order_service.create_order(MARGIN_PRIVATE, SPOT_REGISTRY, symbol, side, order_type, volume, p)
    _sanitize_id(result)
    return {"request": data, "result": result}

@mcp.tool()
def get_margin_order(symbol: str, order_id: str = "", client_order_id: str = "") -> Dict[str, Any]:
    safe_oid = str(order_id).strip() if order_id else ""
    result = margin_order_service.order_query(MARGIN_PRIVATE, SPOT_REGISTRY, symbol, order_id=safe_oid, new_client_order_id=client_order_id)
    _sanitize_id(result); return result

@mcp.tool()
def cancel_margin_order(symbol: str, order_id: str = "", client_order_id: str = "") -> Dict[str, Any]:
    """
    撤销杠杆订单。
    """
    safe_oid = str(order_id).strip() if order_id else ""
    safe_cid = str(client_order_id).strip() if client_order_id else ""

    result = margin_order_service.cancel_order(MARGIN_PRIVATE, SPOT_REGISTRY, symbol, order_id=safe_oid, new_client_order_id=safe_cid)
    _sanitize_id(result)
    return {"symbol": symbol.upper(), "result": result}

@mcp.tool()
def get_margin_open_orders(symbol: str, limit: int = 100) -> Dict[str, Any]:
    rows = margin_order_service.open_orders(MARGIN_PRIVATE, SPOT_REGISTRY, symbol, limit=limit)
    _sanitize_id(rows)
    return {"symbol": symbol.upper(), "orders": rows, "count": len(rows)}

@mcp.tool()
def get_margin_my_trades(symbol: str, limit: int = 100) -> Dict[str, Any]:
    rows = margin_order_service.my_trades(MARGIN_PRIVATE, SPOT_REGISTRY, symbol, limit=limit)
    _sanitize_id(rows)
    return {"symbol": symbol.upper(), "trades": rows, "count": len(rows)}


# =========================================================
# Futures - Readonly
# =========================================================

@mcp.tool()
def get_futures_ticker(symbol: str) -> Dict[str, Any]:
    data = futures_service.get_ticker(FUTURES_PUBLIC, FUTURES_REGISTRY, symbol)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    return {"contract": contract, "last": data.get("last"), "buy": data.get("buy", data.get("bidPrice")), "sell": data.get("sell", data.get("askPrice")), "high": data.get("high"), "low": data.get("low"), "vol": data.get("vol"), "rose": data.get("rose"), "time": data.get("time")}

@mcp.tool()
def get_futures_index(symbol: str) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    data = futures_service.get_index(FUTURES_PUBLIC, FUTURES_REGISTRY, symbol)
    return {"contract": contract, "tagPrice": data.get("tagPrice", data.get("markPrice")), "indexPrice": data.get("indexPrice"), "currentFundRate": data.get("currentFundRate", data.get("lastFundingRate")), "nextFundRate": data.get("nextFundRate"), "time": data.get("time")}

@mcp.tool()
def get_futures_depth(symbol: str, limit: int = 20) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    data = futures_service.get_depth(FUTURES_PUBLIC, FUTURES_REGISTRY, symbol, limit)
    return {"contract": contract, "limit": limit, "bids": data.get("bids", []), "asks": data.get("asks", [])}

@mcp.tool()
def get_futures_klines(symbol: str, interval: str = "1min", limit: int = 20) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    data = futures_service.get_klines(FUTURES_PUBLIC, FUTURES_REGISTRY, symbol, interval, limit)
    return {"contract": contract, "interval": interval, "limit": limit, "klines": data, "count": len(data) if isinstance(data, list) else 0}

@mcp.tool()
def get_futures_balance(margin_coin: str = "USDT") -> Dict[str, Any]:
    data = FUTURES_PRIVATE.account()
    accounts = futures_account_service.extract_accounts(data)
    summary = futures_account_service.get_margin_coin_summary(accounts, margin_coin)
    _sanitize_id(summary); return summary

@mcp.tool()
def get_futures_positions() -> Dict[str, Any]:
    data = FUTURES_PRIVATE.account()
    accounts = futures_account_service.extract_accounts(data)
    positions = futures_account_service.flatten_positions(accounts)
    positions = futures_account_service.filter_nonzero_positions(positions)

    normalized = []
    for p in positions:
        normalized.append({
            "contract": p.get("_contractName"),
            "contract_symbol": p.get("_contractSymbol"),
            "margin_coin": p.get("_marginCoin"),
            "side": map_side(p.get("side")),
            "position_type": map_position_type(p.get("positionType")),
            "volume": p.get("volume"),
            "open_price": p.get("openPrice"),
            "avg_price": p.get("avgPrice"),
            "leverage": p.get("leverageLevel"),
            "unrealized_pnl": p.get("unRealizedAmount", p.get("unrealizedAmount")),
            "realized_pnl": p.get("realizedAmount"),
            "margin_rate": p.get("marginRate"),
            "liquidation_hint_price": p.get("reducePrice"),
            "return_rate": p.get("returnRate"),
            "position_balance": p.get("positionBalance"),
            "mark_price": p.get("indexPrice"),
        })

    _sanitize_id(normalized)
    return {"positions": normalized, "count": len(normalized)}

@mcp.tool()
def get_futures_order(symbol: str, order_id: str = "", client_order_id: str = "") -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    
    safe_oid = str(order_id).strip() if order_id else ""
        
    raw = FUTURES_PRIVATE.order(contract_name=contract, order_id=safe_oid if safe_oid else None, client_order_id=str(client_order_id) if client_order_id else None)
    
    rows = raw if isinstance(raw, list) else [raw] if isinstance(raw, dict) else []
    normalized = []
    for o in rows:
        normalized.append({
            "contract": o.get("contractName", contract), "side": map_side(o.get("side")), "price": o.get("price"),
            "orig_qty": o.get("origQty"), "executed_qty": o.get("executedQty"), "avg_price": o.get("avgPrice"),
            "status": o.get("status"), "action": o.get("action"), "trade_fee": o.get("tradeFee"),
            "realized_amount": o.get("realizedAmount"), "order_id": o.get("orderId"), "time": o.get("transactTime"), "raw": o,
        })
    _sanitize_id(normalized)
    return {"contract": contract, "orders": normalized, "count": len(normalized)}

@mcp.tool()
def get_futures_open_orders(symbol: str) -> Dict[str, Any]:
    rows = futures_order_service.open_orders(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    normalized = []
    for o in rows:
        normalized.append({
            "contract": o.get("contractName") or contract, "side": map_side(o.get("side")), "position_type": map_position_type(o.get("positionType")),
            "price": o.get("price"), "volume": o.get("volume"), "deal_volume": o.get("dealVolume"), "status": map_order_status(o.get("status")),
            "order_id": o.get("orderId"), "time": o.get("ctimeMs") or o.get("ctime") or o.get("transactTime"),
        })
    _sanitize_id(normalized)
    return {"contract": contract, "orders": normalized, "count": len(normalized)}

@mcp.tool()
def get_futures_my_trades(symbol: str, limit: int = 10) -> Dict[str, Any]:
    trades = futures_order_service.my_trades(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol, limit)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    _sanitize_id(trades)
    return {"contract": contract, "trades": trades, "count": len(trades)}

@mcp.tool()
def get_futures_order_history(symbol: str, limit: int = 10) -> Dict[str, Any]:
    rows = futures_order_service.order_historical(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol, limit)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    _sanitize_id(rows)
    return {"contract": contract, "orders": rows, "count": len(rows)}

@mcp.tool()
def get_futures_profit_history(symbol: str, limit: int = 10) -> Dict[str, Any]:
    rows = futures_order_service.profit_historical(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol, limit)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    _sanitize_id(rows)
    return {"contract": contract, "records": rows, "count": len(rows)}

@mcp.tool()
def get_futures_transaction_history(begin_time: str, end_time: str, symbol: str, page: int = 1, limit: int = 200, asset_type: int = 0, lang_key: str = "en_US", tx_type: str = "") -> Dict[str, Any]:
    raw = FUTURES_PRIVATE.get_user_transaction(begin_time=begin_time, end_time=end_time, symbol=symbol, page=page, limit=limit, asset_type=asset_type, lang_key=lang_key, tx_type=tx_type if tx_type else None)
    _sanitize_id(raw)
    return {"symbol": symbol, "page": page, "limit": limit, "result": raw}


# =========================================================
# Futures - Trading
# =========================================================

@mcp.tool()
def create_futures_order(symbol: str, side: str, open_action: str, position_type: int, order_type: str, volume: str, price: str = "") -> Dict[str, Any]:
    p = price.strip() if isinstance(price, str) else price
    if p == "": p = None
    data, result = futures_order_service.create_order(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol, side, open_action, position_type, order_type, volume, p)
    _sanitize_id(result)
    return {"request": data, "result": result}

@mcp.tool()
def create_futures_condition_order(symbol: str, side: str, open_action: str, position_type: int, order_type: str, volume: str, trigger_type: str, trigger_price: str, price: str = "") -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    p = price.strip() if isinstance(price, str) else price
    if p == "": p = None
    result = FUTURES_PRIVATE.create_condition_order(contract_name=contract, side=side, open_action=open_action, position_type=position_type, order_type=order_type, volume=volume, trigger_type=trigger_type, trigger_price=trigger_price, price=p)
    _sanitize_id(result)
    return {
        "request": {"contractName": contract, "side": str(side).upper(), "open": str(open_action).upper(), "positionType": position_type, "type": str(order_type).upper(), "volume": str(volume), "triggerType": str(trigger_type), "triggerPrice": str(trigger_price), "price": p},
        "result": result,
    }

@mcp.tool()
def cancel_futures_order(symbol: str, order_id: str) -> Dict[str, Any]:
    """
    撤销合约订单。
    """
    safe_oid = str(order_id).strip()
        
    result = futures_order_service.cancel_order(FUTURES_PRIVATE, FUTURES_REGISTRY, symbol, safe_oid)
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    _sanitize_id(result)
    return {"contract": contract, "order_id": str(order_id), "result": result}

@mcp.tool()
def cancel_all_futures_orders(symbol: str = "") -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol) if symbol else None
    result = FUTURES_PRIVATE.cancel_all_orders(contract_name=contract)
    _sanitize_id(result)
    return {"contract": contract, "result": result}

@mcp.tool()
def edit_futures_position_mode(symbol: str, position_model: int) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    result = FUTURES_PRIVATE.edit_position_mode(contract, position_model)
    _sanitize_id(result)
    return {"contract": contract, "position_model": position_model, "result": result}

@mcp.tool()
def edit_futures_margin_mode(symbol: str, margin_model: int) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    result = FUTURES_PRIVATE.edit_margin_mode(contract, margin_model)
    _sanitize_id(result)
    return {"contract": contract, "margin_model": margin_model, "result": result}

@mcp.tool()
def adjust_futures_position_margin(position_id: int, amount: str) -> Dict[str, Any]:
    result = FUTURES_PRIVATE.edit_position_margin(position_id=position_id, amount=amount)
    _sanitize_id(result)
    return {"position_id": str(position_id), "amount": amount, "result": result}

@mcp.tool()
def edit_futures_leverage(symbol: str, now_level: int) -> Dict[str, Any]:
    contract = FUTURES_REGISTRY.resolve_contract_name(symbol)
    result = FUTURES_PRIVATE.edit_leverage(contract_name=contract, now_level=now_level)
    _sanitize_id(result)
    return {"contract": contract, "now_level": now_level, "result": result}


# =========================================================
# Spot WS - Public
# =========================================================

@mcp.tool()
def ws_spot_ticker_once(symbol: str, seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_ticker_sub(api_symbol)], seconds=seconds, limit=limit)

@mcp.tool()
def ws_spot_depth_once(symbol: str, step: str = "step0", seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_depth_sub(api_symbol, step=step)], seconds=seconds, limit=limit)

@mcp.tool()
def ws_spot_kline_once(symbol: str, interval: str = "1min", seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_kline_sub(api_symbol, interval=interval)], seconds=seconds, limit=limit)

@mcp.tool()
def ws_spot_trades_once(symbol: str, seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_trade_sub(api_symbol)], seconds=seconds, limit=limit)

@mcp.tool()
def ws_spot_kline_history_once(symbol: str, interval: str = "1min", page_size: int = 100, end_idx: str = "", seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_kline_req(api_symbol, interval=interval, end_idx=end_idx if end_idx else None, page_size=page_size)], seconds=seconds, limit=limit)

@mcp.tool()
def ws_spot_trade_history_once(symbol: str, seconds: int = 3, limit: int = 20) -> Dict[str, Any]:
    api_symbol = SPOT_REGISTRY.get_api_symbol(symbol)
    return _collect_ws_messages(subscriptions=[ws_service.build_trade_req(api_symbol)], seconds=seconds, limit=limit)


if __name__ == "__main__":
    mcp.run()