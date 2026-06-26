import uuid
from .field_mapper import map_spot_order_status, map_order_type
from typing import Any, Dict, List, Optional


def _normalize_side_for_margin(side: Any) -> str:
    if side is None or str(side).strip() == "":
        return "-"

    s = str(side).strip().upper()

    if s == "BUY":
        return "buy"
    if s == "SELL":
        return "sell"

    return s.lower()


def _normalize_list_result(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, dict):
        if isinstance(raw.get("list"), list):
            return raw["list"]
        if isinstance(raw.get("data"), list):
            return raw["data"]
        if raw.get("data") is None and str(raw.get("code")) == "0":
            return []
        return []

    if isinstance(raw, list):
        return raw

    return []


def create_order(
    api,
    registry,
    symbol: Any,
    side: Any,
    order_type: Any,
    volume: Any,
    price: Optional[Any] = None,
    new_client_order_id: Optional[Any] = None,
):
    api_symbol = registry.get_api_symbol(str(symbol).strip())
    display_symbol = registry.get_display_symbol(str(symbol).strip())

    safe_side = str(side).strip().upper() if side is not None else ""
    safe_type = str(order_type).strip().upper() if order_type is not None else ""
    safe_vol = str(volume).strip() if volume is not None else ""
    safe_price = str(price).strip() if price is not None and str(price).strip() != "" else None
    
    # 【业务保留】：自动生成杠杆专用的 AI 防重 ID
    safe_cid = str(new_client_order_id).strip() if new_client_order_id else f"ZKE-AI-MARGIN-{safe_side}-{str(uuid.uuid4())[:4]}"

    data = {
        "display_symbol": display_symbol,
        "api_symbol": api_symbol,
        "side": safe_side,
        "order_type": safe_type,
        "volume": safe_vol,
        "price": safe_price,
        "newClientOrderId": safe_cid,
    }

    result = api.create_order(
        symbol=api_symbol,
        side=safe_side,
        order_type=safe_type,
        volume=safe_vol,
        price=safe_price,
        new_client_order_id=safe_cid,
    )

    return data, result


def order_query(api, registry, symbol: Any, order_id: Optional[Any] = None, new_client_order_id: Optional[Any] = None):
    api_symbol = registry.get_api_symbol(str(symbol).strip())

    safe_oid = str(order_id).strip() if order_id is not None and str(order_id).strip() != "" else None
    safe_cid = str(new_client_order_id).strip() if new_client_order_id is not None and str(new_client_order_id).strip() != "" else None

    result = api.order_query(
        symbol=api_symbol,
        order_id=safe_oid,
        new_client_order_id=safe_cid,
    )

    if not isinstance(result, dict):
        return result

    oid = result.get("orderId") or result.get("orderIdString")
    cid = result.get("clientOrderId") or result.get("clientorderId")

    return {
        "symbol": result.get("symbol", api_symbol),
        "order_id": str(oid) if oid is not None else None,
        "client_order_id": str(cid) if cid is not None else None,
        "side": _normalize_side_for_margin(result.get("side")),
        "type": map_order_type(result.get("type")),
        "price": result.get("price"),
        "orig_qty": result.get("origQty"),
        "executed_qty": result.get("executedQty"),
        "avg_price": result.get("avgPrice"),
        "status": map_spot_order_status(result.get("status")),
        "time": result.get("transactTime") or result.get("time"),
        "raw": result,
    }


def cancel_order(api, registry, symbol: Any, order_id: Optional[Any] = None, new_client_order_id: Optional[Any] = None):
    api_symbol = registry.get_api_symbol(str(symbol).strip())

    safe_oid = str(order_id).strip() if order_id is not None and str(order_id).strip() != "" else None
    safe_cid = str(new_client_order_id).strip() if new_client_order_id is not None and str(new_client_order_id).strip() != "" else None

    result = api.cancel_order(
        symbol=api_symbol,
        order_id=safe_oid,
        new_client_order_id=safe_cid,
    )

    if not isinstance(result, dict):
        return result

    oid = result.get("orderId") or result.get("orderIdString")
    cid = result.get("clientOrderId") or result.get("clientorderId")

    return {
        "symbol": result.get("symbol", api_symbol),
        "order_id": str(oid) if oid is not None else None,
        "client_order_id": str(cid) if cid is not None else None,
        "status": map_spot_order_status(result.get("status")),
        "raw": result,
    }


def open_orders(api, registry, symbol: Any, limit: Any = 100):
    api_symbol = registry.get_api_symbol(str(symbol).strip())
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

    raw = api.open_orders(api_symbol, safe_limit)
    rows = _normalize_list_result(raw)

    clean = []
    for o in rows:
        oid = o.get("orderId") or o.get("orderIdString")
        cid = o.get("clientOrderId") or o.get("clientorderId")

        clean.append({
            "symbol": o.get("symbol", api_symbol),
            "order_id": str(oid) if oid is not None else None,
            "client_order_id": str(cid) if cid is not None else None,
            "side": _normalize_side_for_margin(o.get("side")),
            "type": map_order_type(o.get("type")),
            "price": o.get("price"),
            "orig_qty": o.get("origQty"),
            "executed_qty": o.get("executedQty"),
            "avg_price": o.get("avgPrice"),
            "status": map_spot_order_status(o.get("status")),
            "time": o.get("transactTime") or o.get("time"),
            "raw": o,
        })

    return clean


def my_trades(api, registry, symbol: Any, limit: Any = 100, from_id: Optional[Any] = None):
    api_symbol = registry.get_api_symbol(str(symbol).strip())
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100
    safe_from = str(from_id).strip() if from_id is not None and str(from_id).strip() != "" else None

    raw = api.my_trades(
        symbol=api_symbol,
        limit=safe_limit,
        from_id=safe_from,
    )

    rows = _normalize_list_result(raw)

    clean = []
    for t in rows:
        t_id = t.get("id")
        b_id = t.get("bidId")
        a_id = t.get("askId")

        clean.append({
            "symbol": t.get("symbol", api_symbol),
            "trade_id": str(t_id) if t_id is not None else None,
            "bid_id": str(b_id) if b_id is not None else None,
            "ask_id": str(a_id) if a_id is not None else None,
            "price": t.get("price"),
            "qty": t.get("qty"),
            "time": t.get("time"),
            "side": _normalize_side_for_margin(t.get("side")),
            "is_maker": t.get("isMaker"),
            "fee": t.get("fee"),
            "fee_coin": t.get("feeCoin"),
            "raw": t,
        })

    return clean
