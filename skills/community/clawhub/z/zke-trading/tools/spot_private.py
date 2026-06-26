from typing import Any, Dict, Optional

from tools.zke_client import ZKEClient
from tools.common import ensure_order_type, ensure_side


class SpotPrivateApi:
    def __init__(self, client: ZKEClient):
        self.client = client

    # =========================================================
    # Account
    # =========================================================

    def account(self) -> Dict[str, Any]:
        """
        账户信息
        """
        return self.client.request("GET", "/sapi/v1/account", signed=True)

    def exchange_account(self) -> Dict[str, Any]:
        """
        查询用户现货账户资产
        """
        return self.client.request(
            "POST",
            "/sapi/v1/asset/exchange/account",
            body={},
            signed=True,
        )

    def account_by_type(self, account_type: Any) -> Dict[str, Any]:
        """
        查询用户可划转资产 / 指定账户资产
        """
        safe_type = str(account_type).strip() if account_type is not None else ""
        if not safe_type:
            raise ValueError("accountType 不能为空")
            
        body = {"accountType": safe_type}
        return self.client.request(
            "POST",
            "/sapi/v1/asset/account/by_type",
            body=body,
            signed=True,
        )

    # =========================================================
    # Spot Order Query / Open Orders / Trades
    # =========================================================

    def order_query(
        self,
        symbol: Any,
        order_id: Optional[Any] = None,
        client_order_id: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        查询订单
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询订单失败：symbol 不能为空")

        params: Dict[str, Any] = {"symbol": safe_symbol}

        if order_id is not None and str(order_id).strip() != "":
            params["orderId"] = str(order_id).strip()
        if client_order_id is not None and str(client_order_id).strip() != "":
            params["newClientorderId"] = str(client_order_id).strip()

        return self.client.request("GET", "/sapi/v2/order", params=params, signed=True)

    def open_orders(self, symbol: Any, limit: Any = 100) -> Any:
        """
        当前挂单
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询挂单失败：symbol 不能为空")
            
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        params: Dict[str, Any] = {
            "symbol": safe_symbol,
            "limit": safe_limit,
        }
        return self.client.request("GET", "/sapi/v2/openOrders", params=params, signed=True)

    def my_trades(self, symbol: Any, limit: Any = 100, from_id: Optional[Any] = None) -> Any:
        """
        现货成交记录 v2
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询成交记录失败：symbol 不能为空")
            
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        params: Dict[str, Any] = {
            "symbol": safe_symbol,
            "limit": safe_limit,
        }

        if from_id is not None and str(from_id).strip() != "":
            params["fromId"] = str(from_id).strip()

        return self.client.request("GET", "/sapi/v2/myTrades", params=params, signed=True)

    def my_trades_v3(
        self,
        symbol: Optional[Any] = None,
        limit: Any = 50,
        start_time: Optional[Any] = None,
        end_time: Optional[Any] = None,
    ) -> Any:
        """
        现货成交记录 v3
        """
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 50
        params: Dict[str, Any] = {"limit": safe_limit}

        if symbol is not None and str(symbol).strip() != "":
            params["symbol"] = str(symbol).strip()
            
        # 兼容时间戳 0 和 AI 空字符串
        if start_time is not None and str(start_time).strip() != "":
            params["startTime"] = int(start_time)
        if end_time is not None and str(end_time).strip() != "":
            params["endTime"] = int(end_time)

        return self.client.request("GET", "/sapi/v3/myTrades", params=params, signed=True)

    def history_orders(
        self,
        symbol: Optional[Any] = None,
        limit: Any = 50,
        start_time: Optional[Any] = None,
        end_time: Optional[Any] = None,
    ) -> Any:
        """
        现货历史订单
        """
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 50
        params: Dict[str, Any] = {"limit": safe_limit}

        if symbol is not None and str(symbol).strip() != "":
            params["symbol"] = str(symbol).strip()
            
        if start_time is not None and str(start_time).strip() != "":
            params["startTime"] = int(start_time)
        if end_time is not None and str(end_time).strip() != "":
            params["endTime"] = int(end_time)

        return self.client.request("GET", "/sapi/v3/historyOrders", params=params, signed=True)

    # =========================================================
    # Spot Order Create / Test / Cancel
    # =========================================================

    def test_order(
        self,
        symbol: Any,
        volume: Any,
        side: Any,
        order_type: Any,
        price: Optional[Any] = None,
        new_client_order_id: Any = "",
        recv_window: Any = 5000,
    ) -> Dict[str, Any]:
        """
        测试下单
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        safe_vol = str(volume).strip() if volume is not None else ""
        
        if not safe_symbol: raise ValueError("下单失败：symbol 不能为空")
        if not safe_vol: raise ValueError("下单失败：volume 不能为空")

        safe_side = ensure_side(str(side))
        safe_type = ensure_order_type(str(order_type))
        safe_recv = int(recv_window) if recv_window is not None and str(recv_window).strip() != "" else 5000

        body: Dict[str, Any] = {
            "symbol": safe_symbol,
            "volume": safe_vol,
            "side": safe_side,
            "type": safe_type,
            "recvWindow": safe_recv,
        }

        if safe_type == "LIMIT":
            if price is None or str(price).strip() == "":
                raise ValueError("LIMIT 订单必须提供 price。")
            body["price"] = str(price).strip()

        if new_client_order_id is not None and str(new_client_order_id).strip() != "":
            body["newClientorderId"] = str(new_client_order_id).strip()

        return self.client.request("POST", "/sapi/v2/order/test", body=body, signed=True)

    def create_order(
        self,
        symbol: Any,
        volume: Any,
        side: Any,
        order_type: Any,
        price: Optional[Any] = None,
        new_client_order_id: Any = "",
        recv_window: Any = 5000,
    ) -> Dict[str, Any]:
        """
        创建订单
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        safe_vol = str(volume).strip() if volume is not None else ""
        
        if not safe_symbol: raise ValueError("下单失败：symbol 不能为空")
        if not safe_vol: raise ValueError("下单失败：volume 不能为空")

        safe_side = ensure_side(str(side))
        safe_type = ensure_order_type(str(order_type))
        safe_recv = int(recv_window) if recv_window is not None and str(recv_window).strip() != "" else 5000

        body: Dict[str, Any] = {
            "symbol": safe_symbol,
            "volume": safe_vol,
            "side": safe_side,
            "type": safe_type,
            "recvWindow": safe_recv,
        }

        if safe_type == "LIMIT":
            if price is None or str(price).strip() == "":
                raise ValueError("LIMIT 订单必须提供 price。")
            body["price"] = str(price).strip()

        if new_client_order_id is not None and str(new_client_order_id).strip() != "":
            body["newClientOrderId"] = str(new_client_order_id).strip()

        return self.client.request("POST", "/sapi/v2/order", body=body, signed=True)

    def cancel_order(
        self,
        symbol: Any,
        order_id: Optional[Any] = None,
        client_order_id: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        撤单
        """
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol: 
            raise ValueError("撤单失败：symbol 不能为空")

        body: Dict[str, Any] = {"symbol": safe_symbol}

        if order_id is not None and str(order_id).strip() != "":
            body["orderId"] = str(order_id).strip()
        if client_order_id is not None and str(client_order_id).strip() != "":
            body["newClientOrderId"] = str(client_order_id).strip()

        return self.client.request("POST", "/sapi/v2/cancel", body=body, signed=True)

    # =========================================================
    # Asset Transfer
    # =========================================================

    def asset_transfer(
        self,
        coin_symbol: Any,
        amount: Any,
        from_account: Any,
        to_account: Any,
    ) -> Dict[str, Any]:
        """
        账户划转
        """
        safe_coin = str(coin_symbol).strip() if coin_symbol is not None else ""
        safe_amt = str(amount).strip() if amount is not None else ""
        safe_from = str(from_account).strip() if from_account is not None else ""
        safe_to = str(to_account).strip() if to_account is not None else ""

        if not safe_coin or not safe_amt or not safe_from or not safe_to:
            raise ValueError("划转失败：参数不完整。")

        body: Dict[str, Any] = {
            "coinSymbol": safe_coin,
            "amount": safe_amt,
            "fromAccount": safe_from,
            "toAccount": safe_to,
        }

        return self.client.request("POST", "/sapi/v1/asset/transfer", body=body, signed=True)

    def asset_transfer_query(
        self,
        transfer_id: Optional[Any] = None,
        coin_symbol: Optional[Any] = None,
        from_account: Optional[Any] = None,
        to_account: Optional[Any] = None,
        start_time: Optional[Any] = None,
        end_time: Optional[Any] = None,
        page: Optional[Any] = None,
        limit: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        划转记录查询
        """
        body: Dict[str, Any] = {}

        if transfer_id is not None and str(transfer_id).strip() != "":
            body["transferId"] = str(transfer_id).strip()
        if coin_symbol is not None and str(coin_symbol).strip() != "":
            body["coinSymbol"] = str(coin_symbol).strip()
        if from_account is not None and str(from_account).strip() != "":
            body["fromAccount"] = str(from_account).strip()
        if to_account is not None and str(to_account).strip() != "":
            body["toAccount"] = str(to_account).strip()
            
        if start_time is not None and str(start_time).strip() != "":
            body["startTime"] = int(start_time)
        if end_time is not None and str(end_time).strip() != "":
            body["endTime"] = int(end_time)
        if page is not None and str(page).strip() != "":
            body["page"] = int(page)
        if limit is not None and str(limit).strip() != "":
            body["limit"] = int(limit)

        return self.client.request("POST", "/sapi/v1/asset/transferQuery", body=body, signed=True)

    # =========================================================
    # Withdraw
    # =========================================================

    def withdraw_apply(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request("POST", "/sapi/v1/withdraw/apply", body=body, signed=True)

    def withdraw_history(self, params: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request("POST", "/sapi/v1/withdraw/query", body=params, signed=True)
