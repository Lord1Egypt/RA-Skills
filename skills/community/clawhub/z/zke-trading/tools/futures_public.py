from typing import Any, Dict, List, Union

from tools.common import ensure_futures_interval
from tools.zke_client import ZKEClient


class FuturesPublicApi:
    def __init__(self, client: ZKEClient):
        self.client = client

    def ping(self) -> Dict[str, Any]:
        """
        GET /fapi/v1/ping
        """
        return self.client.request("GET", "/fapi/v1/ping")

    def time(self) -> Dict[str, Any]:
        """
        GET /fapi/v1/time
        """
        return self.client.request("GET", "/fapi/v1/time")

    def contracts(self) -> List[Dict[str, Any]]:
        """
        GET /fapi/v1/contracts
        """
        return self.client.request("GET", "/fapi/v1/contracts")

    def ticker(self, contract_name: Any) -> Dict[str, Any]:
        """
        GET /fapi/v1/ticker
        params: contractName
        """
        # 【修复】去除了 .upper()，忠实传递上层传来的 contractName 原貌
        safe_contract = str(contract_name).strip() if contract_name is not None else ""
        if not safe_contract:
            raise ValueError("查询合约 Ticker 失败：contractName 不能为空")

        return self.client.request(
            "GET",
            "/fapi/v1/ticker",
            params={"contractName": safe_contract}
        )

    def ticker_all(self) -> Dict[str, Any]:
        """
        GET /fapi/v1/ticker_all
        """
        return self.client.request("GET", "/fapi/v1/ticker_all")

    def depth(self, contract_name: Any, limit: Any = 100) -> Dict[str, Any]:
        """
        GET /fapi/v1/depth
        params: contractName, limit
        """
        safe_contract = str(contract_name).strip() if contract_name is not None else ""
        if not safe_contract:
            raise ValueError("查询合约深度失败：contractName 不能为空")
            
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        return self.client.request(
            "GET",
            "/fapi/v1/depth",
            params={"contractName": safe_contract, "limit": safe_limit}
        )

    def index(self, contract_name: Any) -> Dict[str, Any]:
        """
        GET /fapi/v1/index
        params: contractName
        """
        safe_contract = str(contract_name).strip() if contract_name is not None else ""
        if not safe_contract:
            raise ValueError("查询合约指数失败：contractName 不能为空")

        return self.client.request(
            "GET",
            "/fapi/v1/index",
            params={"contractName": safe_contract}
        )

    def klines(
        self,
        contract_name: Any,
        interval: Any,
        limit: Any = 100
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        GET /fapi/v1/klines
        params: contractName, interval, limit
        """
        safe_contract = str(contract_name).strip() if contract_name is not None else ""
        if not safe_contract:
            raise ValueError("查询合约 K线 失败：contractName 不能为空")
            
        safe_interval = str(interval).strip() if interval is not None else ""
        interval_val = ensure_futures_interval(safe_interval)
        
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        return self.client.request(
            "GET",
            "/fapi/v1/klines",
            params={
                "contractName": safe_contract,
                "interval": interval_val,
                "limit": safe_limit
            }
        )
