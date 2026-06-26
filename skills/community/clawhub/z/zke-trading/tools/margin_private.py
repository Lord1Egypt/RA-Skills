from typing import Any, Dict, Optional

from tools.zke_client import ZKEClient


class MarginPrivateApi:
    """
    杠杆私有接口封装

    新版文档：
    - POST /sapi/v2/margin/order
    - GET  /sapi/v2/margin/order
    - POST /sapi/v2/margin/cancel
    - GET  /sapi/v2/margin/openOrders
    - GET  /sapi/v2/margin/myTrades
    """

    def __init__(self, client: ZKEClient):
        self.client = client

    def create_order(
        self,
        symbol: Any,
        side: Any,
        order_type: Any,
        volume: Any,
        price: Optional[Any] = None,
        new_client_order_id: Optional[Any] = None,
    ):
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("杠杆下单失败：symbol 不能为空")

        safe_side = str(side).strip().upper() if side is not None else ""
        if not safe_side: 
            raise ValueError("杠杆下单失败：side 不能为空")

        safe_type = str(order_type).strip().upper() if order_type is not None else ""
        if not safe_type: 
            raise ValueError("杠杆下单失败：order_type 不能为空")

        safe_volume = str(volume).strip() if volume is not None else ""
        if not safe_volume: 
            raise ValueError("杠杆下单失败：volume 不能为空")

        body: Dict[str, Any] = {
            "symbol": safe_symbol,
            "side": safe_side,
            "type": safe_type,
            "volume": safe_volume,
        }

        # 拦截 AI 可能传入的空字符串 ""
        if price is not None and str(price).strip() != "":
            body["price"] = str(price).strip()

        if new_client_order_id is not None and str(new_client_order_id).strip() != "":
            body["newClientOrderId"] = str(new_client_order_id).strip()

        return self.client.request("POST", "/sapi/v2/margin/order", body=body, signed=True)

    def order_query(
        self,
        symbol: Any,
        order_id: Optional[Any] = None,
        new_client_order_id: Optional[Any] = None,
    ):
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("杠杆查询订单失败：symbol 不能为空")

        params: Dict[str, Any] = {
            "symbol": safe_symbol,
        }

        if order_id is not None and str(order_id).strip() != "":
            params["orderId"] = str(order_id).strip()

        if new_client_order_id is not None and str(new_client_order_id).strip() != "":
            params["newClientOrderId"] = str(new_client_order_id).strip()

        return self.client.request("GET", "/sapi/v2/margin/order", params=params, signed=True)

    def cancel_order(
        self,
        symbol: Any,
        order_id: Optional[Any] = None,
        new_client_order_id: Optional[Any] = None,
    ):
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("杠杆撤单失败：symbol 不能为空")

        body: Dict[str, Any] = {
            "symbol": safe_symbol,
        }

        if order_id is not None and str(order_id).strip() != "":
            body["orderId"] = str(order_id).strip()

        if new_client_order_id is not None and str(new_client_order_id).strip() != "":
            body["newClientOrderId"] = str(new_client_order_id).strip()

        return self.client.request("POST", "/sapi/v2/margin/cancel", body=body, signed=True)

    def open_orders(self, symbol: Any, limit: Optional[Any] = None):
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("杠杆查询挂单失败：symbol 不能为空")

        params: Dict[str, Any] = {
            "symbol": safe_symbol,
        }

        if limit is not None and str(limit).strip() != "":
            params["limit"] = int(limit)

        return self.client.request("GET", "/sapi/v2/margin/openOrders", params=params, signed=True)

    def my_trades(
        self,
        symbol: Any,
        limit: Optional[Any] = None,
        from_id: Optional[Any] = None,
    ):
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("杠杆查询成交记录失败：symbol 不能为空")

        params: Dict[str, Any] = {
            "symbol": safe_symbol,
        }

        if limit is not None and str(limit).strip() != "":
            params["limit"] = int(limit)

        if from_id is not None and str(from_id).strip() != "":
            params["fromId"] = str(from_id).strip()

        return self.client.request("GET", "/sapi/v2/margin/myTrades", params=params, signed=True)
