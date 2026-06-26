import json
import time
import uuid
from typing import Any, Optional

def prepare_order(registry, symbol, volume, price, order_type):
    """
    统一校验并格式化订单参数
    """
    validated = registry.validate_order(symbol, volume, price, order_type)

    return {
        "display_symbol": validated["display_symbol"],
        "api_symbol": validated["api_symbol"],
        "volume": validated["fixed_volume"],
        "price": validated["fixed_price"]
    }


def test_order(
    private_api,
    registry,
    symbol: Any,
    side: Any,
    order_type: Any,
    volume: Any,
    price: Optional[Any] = None,
    new_client_order_id: Any = "",
    recv_window: Any = 5000,
):
    """
    测试下单接口（不真实下单）
    """
    data = prepare_order(registry, symbol, volume, price, order_type)

    result = private_api.test_order(
        symbol=data["api_symbol"],
        volume=data["volume"],
        side=side,
        order_type=order_type,
        price=data["price"],
        new_client_order_id=new_client_order_id,
        recv_window=recv_window,
    )

    return data, result


def create_order(
    private_api,
    registry,
    symbol: Any,
    side: Any,
    order_type: Any,
    volume: Any,
    price: Optional[Any] = None,
    new_client_order_id: Any = "",
    recv_window: Any = 5000,
    trigger_price: Optional[Any] = None,
):
    """
    创建真实订单 - 保留生成 ZKE-AI 防重前缀的优良传统
    """
    safe_cid = str(new_client_order_id).strip() if new_client_order_id else f"ZKE-AI-{str(side).upper()}-{str(uuid.uuid4())[:4]}"
    
    data = prepare_order(registry, symbol, volume, price, order_type)

    result = private_api.create_order(
        symbol=data["api_symbol"],
        volume=data["volume"],
        side=side,
        order_type=order_type,
        price=data["price"],
        new_client_order_id=safe_cid,
        recv_window=recv_window,
    )

    # 把生成的 clientOrderId 塞回结果，原始 ID 会在最外层（FastMCP 返回前）统一被转为字符串
    if isinstance(result, dict):
        result["clientOrderId"] = str(safe_cid)

    return data, result


def cancel_order(
    private_api,
    registry,
    symbol: Any,
    order_id: Optional[Any] = None,
    client_order_id: Optional[Any] = None,
):
    """
    撤销订单 - 同时支持数字 order_id 和字母 client_order_id
    """
    api_symbol = registry.get_api_symbol(symbol)

    safe_oid = str(order_id).strip() if order_id is not None and str(order_id).strip() != "" else None
    safe_cid = str(client_order_id).strip() if client_order_id is not None and str(client_order_id).strip() != "" else None

    if not safe_oid and not safe_cid:
        raise ValueError("撤单失败：必须提供 order_id 或 client_order_id 其中之一")

    return private_api.cancel_order(
        api_symbol,
        order_id=safe_oid,
        client_order_id=safe_cid,
    )


def open_orders(private_api, registry, symbol: Any, limit: Any = 100):
    """
    查询当前挂单 - 纯净转发，交给最外层统一处理字符串化
    """
    api_symbol = registry.get_api_symbol(symbol)
    safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100
    
    return private_api.open_orders(api_symbol, limit=safe_limit)
