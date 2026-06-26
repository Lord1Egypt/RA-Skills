import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import pandas as pd

from tqsdk import TqApi, TqAuth


class TqSdkClient:
    """天勤量化 API 封装"""
    
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self._api = None
    
    async def __aenter__(self):
        self._api = TqApi(auth=TqAuth(self.username, self.password))
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._api:
            await self._api.close()
    
    async def get_quote(self, symbols: List[str]) -> List[Dict]:
        """获取多个合约的实时报价"""
        quotes = []
        for sym in symbols:
            quote = self._api.get_quote(sym)
            await self._api.wait_update()
            quotes.append({
                "symbol": sym,
                "last_price": quote.last_price,
                "ask_price1": quote.ask_price1,
                "bid_price1": quote.bid_price1,
                "volume": quote.volume,
                "open_interest": quote.open_interest,
                "datetime": str(quote.datetime),
            })
        return quotes
    
    async def get_kline_serial(self, symbols: Union[str, List[str]], duration: int, length: int) -> pd.DataFrame:
        """获取实时K线序列"""
        return self._api.get_kline_serial(symbols, duration, data_length=length)
    
    async def get_kline_data(self, symbol: str, duration: int, start_dt: datetime, end_dt: datetime) -> pd.DataFrame:
        """获取历史K线数据"""
        return self._api.get_kline_data_series(symbol, duration, start_dt=start_dt, end_dt=end_dt)