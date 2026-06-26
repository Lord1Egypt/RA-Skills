from typing import Any, Dict, Optional

from tools.zke_client import ZKEClient


class FuturesPrivateApi:
    def __init__(self, client: ZKEClient):
        self.client = client

    def account(self):
        """
        GET /fapi/v1/account
        """
        return self.client.request("GET", "/fapi/v1/account", signed=True)

    def order(
        self,
        contract_name: str,
        order_id: Optional[str] = None,
        client_order_id: Optional[str] = None
    ):
        """
        GET /fapi/v1/order
        """
        params: Dict[str, Any] = {"contractName": contract_name}

        if order_id:
            params["orderId"] = order_id
        if client_order_id:
            params["clientOrderId"] = client_order_id

        return self.client.request("GET", "/fapi/v1/order", params=params, signed=True)

    def open_orders(self, contract_name: Optional[str] = None):
        """
        GET /fapi/v1/openOrders
        contractName 可选；不传则查询全部合约当前挂单
        """
        params: Dict[str, Any] = {}
        if contract_name:
            params["contractName"] = contract_name

        return self.client.request(
            "GET",
            "/fapi/v1/openOrders",
            params=params,
            signed=True
        )

    def my_trades(
        self,
        contract_name: str,
        limit: int = 100,
        from_id: Optional[int] = None
    ):
        """
        GET /fapi/v1/myTrades
        """
        params: Dict[str, Any] = {
            "contractName": contract_name,
            "limit": limit
        }

        if from_id is not None:
            params["fromId"] = from_id

        return self.client.request("GET", "/fapi/v1/myTrades", params=params, signed=True)

    def order_historical(
        self,
        contract_name: str,
        limit: int = 100,
        from_id: Optional[int] = None
    ):
        """
        POST /fapi/v1/orderHistorical
        """
        body: Dict[str, Any] = {
            "contractName": contract_name,
            "limit": limit
        }

        if from_id is not None:
            body["fromId"] = from_id

        return self.client.request("POST", "/fapi/v1/orderHistorical", body=body, signed=True)

    def profit_historical(
        self,
        contract_name: Optional[str] = None,
        limit: int = 100,
        from_id: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ):
        """
        POST /fapi/v1/profitHistorical
        """
        body: Dict[str, Any] = {
            "limit": limit
        }

        if contract_name:
            body["contractName"] = contract_name
        if from_id is not None:
            body["fromId"] = from_id
        if start_time is not None and end_time is not None:
            body["startTime"] = start_time
            body["endTime"] = end_time

        return self.client.request("POST", "/fapi/v1/profitHistorical", body=body, signed=True)

    def create_order(
        self,
        contract_name: str,
        side: str,
        open_action: str,
        position_type: int,
        order_type: str,
        volume: str,
        price: Optional[str] = None,
        client_order_id: str = "",
        time_in_force: str = "",
        order_unit: int = 2,
    ):
        """
        POST /fapi/v1/order
        需要 futures-version: 101
        """
        body: Dict[str, Any] = {
            "contractName": contract_name,
            "side": str(side).upper(),
            "open": str(open_action).upper(),
            "positionType": position_type,
            "type": str(order_type).upper(),
            "volume": volume,
            "orderUnit": order_unit,
        }

        if price is not None:
            body["price"] = price
        if client_order_id:
            body["clientOrderId"] = client_order_id
        if time_in_force:
            body["timeInForce"] = time_in_force

        return self.client.request(
            "POST",
            "/fapi/v1/order",
            body=body,
            signed=True,
            extra_headers={"futures-version": "101"},
        )

    def create_condition_order(
        self,
        contract_name: str,
        side: str,
        open_action: str,
        position_type: int,
        order_type: str,
        volume: str,
        trigger_type: str,
        trigger_price: str,
        price: Optional[str] = None,
        order_unit: int = 2,
    ):
        """
        POST /fapi/v1/conditionOrder
        需要 futures-version: 101
        """
        body: Dict[str, Any] = {
            "contractName": contract_name,
            "side": str(side).upper(),
            "open": str(open_action).upper(),
            "positionType": position_type,
            "type": str(order_type).upper(),
            "volume": volume,
            "triggerType": trigger_type,
            "triggerPrice": trigger_price,
            "orderUnit": order_unit,
        }

        if price is not None:
            body["price"] = price

        return self.client.request(
            "POST",
            "/fapi/v1/conditionOrder",
            body=body,
            signed=True,
            extra_headers={"futures-version": "101"},
        )

    def cancel_order(self, contract_name: str, order_id: str):
        """
        POST /fapi/v1/cancel
        """
        body = {
            "contractName": contract_name,
            "orderId": order_id
        }
        return self.client.request("POST", "/fapi/v1/cancel", body=body, signed=True)

    def cancel_all_orders(self, contract_name: Optional[str] = None):
        """
        POST /fapi/v1/cancel_all
        文档未强制要求 body 字段，但一般可传 contractName 做定向撤单
        """
        body: Dict[str, Any] = {}
        if contract_name:
            body["contractName"] = contract_name

        return self.client.request("POST", "/fapi/v1/cancel_all", body=body, signed=True)

    def edit_position_mode(self, contract_name: str, position_model: int):
        """
        POST /fapi/v1/edit_user_position_model
        """
        body = {
            "contractName": contract_name,
            "positionModel": position_model,
        }
        return self.client.request("POST", "/fapi/v1/edit_user_position_model", body=body, signed=True)

    def edit_margin_mode(self, contract_name: str, margin_model: int):
        """
        POST /fapi/v1/edit_user_margin_model
        """
        body = {
            "contractName": contract_name,
            "marginModel": margin_model,
        }
        return self.client.request("POST", "/fapi/v1/edit_user_margin_model", body=body, signed=True)

    def edit_position_margin(self, position_id: int, amount):
        """
        POST /fapi/v1/edit_position_margin
        """
        body = {
            "positionId": position_id,
            "amount": amount,
        }
        return self.client.request("POST", "/fapi/v1/edit_position_margin", body=body, signed=True)

    def edit_leverage(self, contract_name: str, now_level: int):
        """
        POST /fapi/v1/edit_lever
        """
        body = {
            "contractName": contract_name,
            "nowLevel": now_level,
        }
        return self.client.request("POST", "/fapi/v1/edit_lever", body=body, signed=True)

    def get_user_transaction(
        self,
        begin_time: str,
        end_time: str,
        symbol: str,
        page: int = 1,
        limit: int = 200,
        asset_type: Optional[int] = None,
        lang_key: Optional[str] = None,
        tx_type: Optional[str] = None,
    ):
        """
        POST /fapi/v1/get_user_transaction
        """
        body: Dict[str, Any] = {
            "beginTime": begin_time,
            "endTime": end_time,
            "symbol": symbol,
            "page": page,
            "limit": limit,
        }

        if asset_type is not None:
            body["assetType"] = asset_type
        if lang_key:
            body["langKey"] = lang_key
        if tx_type:
            body["type"] = tx_type

        return self.client.request("POST", "/fapi/v1/get_user_transaction", body=body, signed=True)
