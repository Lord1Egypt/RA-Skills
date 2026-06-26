from typing import Any, Dict

from tools.zke_client import ZKEClient
from tools.common import ensure_spot_interval


class SpotPublicApi:
    def __init__(self, client: ZKEClient):
        self.client = client

    def ping(self) -> Dict[str, Any]:
        return self.client.request("GET", "/sapi/v2/ping")

    def time(self) -> Dict[str, Any]:
        return self.client.request("GET", "/sapi/v2/time")

    def symbols(self) -> Dict[str, Any]:
        return self.client.request("GET", "/sapi/v2/symbols")

    def ticker(self, symbol: Any) -> Dict[str, Any]:
        # 【修复】去除了 .upper() 和 .replace，忠实传递底层需要的 symbol 格式
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询 Ticker 失败：交易对 symbol 不能为空")
            
        return self.client.request("GET", "/sapi/v2/ticker", params={"symbol": safe_symbol})

    def depth(self, symbol: Any, limit: Any = 100) -> Dict[str, Any]:
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询深度失败：交易对 symbol 不能为空")
            
        # 【AI 加固】安全转换 limit 整数
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        return self.client.request(
            "GET",
            "/sapi/v2/depth",
            params={"symbol": safe_symbol, "limit": safe_limit}
        )

    def trades(self, symbol: Any, limit: Any = 100) -> Dict[str, Any]:
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询近期交易失败：交易对 symbol 不能为空")
            
        safe_limit = int(limit) if limit is not None and str(limit).strip() != "" else 100

        return self.client.request(
            "GET",
            "/sapi/v2/trades",
            params={"symbol": safe_symbol, "limit": safe_limit}
        )

    def klines(self, symbol: Any, interval: Any) -> Any:
        safe_symbol = str(symbol).strip() if symbol is not None else ""
        if not safe_symbol:
            raise ValueError("查询 K线 失败：交易对 symbol 不能为空")
            
        # 【AI 加固】防止 AI 传错时间间隔参数
        safe_interval = str(interval).strip() if interval is not None else ""
        interval_val = ensure_spot_interval(safe_interval)
        
        return self.client.request(
            "GET",
            "/sapi/v2/klines",
            params={"symbol": safe_symbol, "interval": interval_val}
        )
