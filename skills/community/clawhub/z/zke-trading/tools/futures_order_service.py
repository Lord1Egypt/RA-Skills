from .field_mapper import (
    map_side,
    map_open_close,
    map_position_type,
    map_order_status,
)


def _normalize_list_result(raw):
    if isinstance(raw, dict):
        if isinstance(raw.get("data"), list):
            return raw["data"]
        if isinstance(raw.get("list"), list):
            return raw["list"]
        if isinstance(raw.get("data"), dict):
            return [raw["data"]]
        if raw.get("data") is None and str(raw.get("code")) == "0":
            return []
        return []

    if isinstance(raw, list):
        return raw

    return []


def open_orders(api, registry, symbol=None):
    contract = registry.resolve_contract_name(symbol) if symbol else None
    result = api.open_orders(contract)
    return _normalize_list_result(result)


def order_query(api, registry, symbol, order_id=None, client_order_id=None):
    contract = registry.resolve_contract_name(symbol)
    safe_oid = str(order_id).strip() if order_id is not None and str(order_id).strip() != "" else None
    safe_cid = str(client_order_id).strip() if client_order_id is not None and str(client_order_id).strip() != "" else None
    return api.order(contract, order_id=safe_oid, client_order_id=safe_cid)


def my_trades(api, registry, symbol, limit=10, from_id=None):
    contract = registry.resolve_contract_name(symbol)
    safe_from = str(from_id).strip() if from_id is not None and str(from_id).strip() != "" else None

    trades = api.my_trades(contract, limit=limit, from_id=safe_from)
    trade_list = _normalize_list_result(trades)

    clean = []
    for t in trade_list:
        clean.append({
            "contract": t.get("contractName", t.get("symbol")),
            "side": map_side(t.get("side")),
            "price": t.get("price"),
            "qty": t.get("qty", t.get("volume")),
            "fee": t.get("fee"),
            "time": t.get("time"),
            "raw": t,
        })

    return clean


def order_historical(api, registry, symbol, limit=10, from_id=None):
    contract = registry.resolve_contract_name(symbol)
    safe_from = str(from_id).strip() if from_id is not None and str(from_id).strip() != "" else None

    orders = api.order_historical(contract, limit=limit, from_id=safe_from)
    order_list = _normalize_list_result(orders)

    clean = []
    for o in order_list:
        clean.append({
            "contract": o.get("contractName", o.get("symbol")),
            "side": map_side(o.get("side")),
            "action": map_open_close(o.get("openOrClose", o.get("action"))),
            "position_mode": map_position_type(o.get("positionType")),
            "price": o.get("price"),
            "volume": o.get("volume", o.get("origQty")),
            "deal_volume": o.get("dealVolume", o.get("executedQty")),
            "status": map_order_status(o.get("status")),
            "time": o.get("ctimeMs", o.get("ctime", o.get("transactTime"))),
            "raw": o,
        })

    return clean


def profit_historical(
    api,
    registry,
    symbol=None,
    limit=10,
    from_id=None,
    start_time=None,
    end_time=None,
):
    contract = registry.resolve_contract_name(symbol) if symbol else None
    safe_from = str(from_id).strip() if from_id is not None and str(from_id).strip() != "" else None

    records = api.profit_historical(
        contract_name=contract,
        limit=limit,
        from_id=safe_from,
        start_time=start_time,
        end_time=end_time,
    )
    record_list = _normalize_list_result(records)

    clean = []
    for r in record_list:
        clean.append({
            "contract": r.get("contractName", r.get("symbol")),
            "side": map_side(r.get("side")),
            "position_mode": map_position_type(r.get("positionType")),
            "open_price": r.get("openPrice"),
            "profit": r.get("closeProfit"),
            "fee": r.get("tradeFee"),
            "leverage": r.get("leverageLevel"),
            "time": r.get("ctime", r.get("mtime")),
            "raw": r,
        })

    return clean


def create_order(
    api,
    registry,
    symbol,
    side,
    open_action,
    position_type,
    order_type,
    volume,
    price=None,
    client_order_id="",
    time_in_force="",
    order_unit=2,
):
    contract = registry.resolve_contract_name(symbol)
    
    safe_cid = str(client_order_id).strip() if client_order_id else ""

    data = {
        "contractName": contract,
        "side": str(side).upper(),
        "open": str(open_action).upper(),
        "positionType": position_type,
        "type": str(order_type).upper(),
        "volume": volume,
        "price": price,
        "clientOrderId": safe_cid,
        "timeInForce": time_in_force,
        "orderUnit": order_unit,
    }

    result = api.create_order(
        contract_name=contract,
        side=side,
        open_action=open_action,
        position_type=position_type,
        order_type=order_type,
        volume=volume,
        price=price,
        client_order_id=safe_cid,
        time_in_force=time_in_force,
        order_unit=order_unit,
    )

    return data, result


def create_condition_order(
    api,
    registry,
    symbol,
    side,
    open_action,
    position_type,
    order_type,
    volume,
    trigger_type,
    trigger_price,
    price=None,
    order_unit=2,
):
    contract = registry.resolve_contract_name(symbol)

    data = {
        "contractName": contract,
        "side": str(side).upper(),
        "open": str(open_action).upper(),
        "positionType": position_type,
        "type": str(order_type).upper(),
        "volume": volume,
        "triggerType": trigger_type,
        "triggerPrice": trigger_price,
        "price": price,
        "orderUnit": order_unit,
    }

    result = api.create_condition_order(
        contract_name=contract,
        side=side,
        open_action=open_action,
        position_type=position_type,
        order_type=order_type,
        volume=volume,
        trigger_type=trigger_type,
        trigger_price=trigger_price,
        price=price,
        order_unit=order_unit,
    )

    return data, result


def cancel_order(api, registry, symbol, order_id):
    contract = registry.resolve_contract_name(symbol)
    safe_oid = str(order_id).strip() if order_id is not None and str(order_id).strip() != "" else ""
    return api.cancel_order(contract, safe_oid)


def cancel_all_orders(api, registry, symbol=None):
    contract = registry.resolve_contract_name(symbol) if symbol else None
    return api.cancel_all_orders(contract_name=contract)


def edit_position_mode(api, registry, symbol, position_model):
    contract = registry.resolve_contract_name(symbol)
    return api.edit_position_mode(contract, position_model)


def edit_margin_mode(api, registry, symbol, margin_model):
    contract = registry.resolve_contract_name(symbol)
    return api.edit_margin_mode(contract, margin_model)


def edit_position_margin(api, position_id, amount):
    safe_pid = str(position_id).strip() if position_id is not None else ""
    return api.edit_position_margin(safe_pid, amount)


def edit_leverage(api, registry, symbol, now_level):
    contract = registry.resolve_contract_name(symbol)
    return api.edit_leverage(contract, now_level)


def get_user_transaction(
    api,
    begin_time,
    end_time,
    symbol,
    page=1,
    limit=200,
    asset_type=None,
    lang_key=None,
    tx_type=None,
):
    return api.get_user_transaction(
        begin_time=begin_time,
        end_time=end_time,
        symbol=symbol,
        page=page,
        limit=limit,
        asset_type=asset_type,
        lang_key=lang_key,
        tx_type=tx_type,
    )
