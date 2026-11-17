from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from contextlib import suppress
from dataclasses import dataclass
from typing import Iterable

from models import Bar, StockDefinition, StockQuote


QUOTE_BATCH_SIZE = 80
SECURITY_LIST_PAGE_SIZE = 1000
SINA_PAGE_SIZE = 80
SINA_COUNT_URL = (
    "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
    "Market_Center.getHQNodeStockCount"
)
SINA_LIST_URL = (
    "http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/"
    "Market_Center.getHQNodeData"
)

MARKET_MAP = {
    "6": 1,
    "5": 1,
    "9": 1,
    "0": 0,
    "3": 0,
    "2": 0,
    "8": 2,
    "4": 2,
}

MARKET_A_SHARE_PREFIXES = {
    0: ("000", "001", "002", "003", "300", "301"),
    1: ("600", "601", "603", "605", "688", "689"),
    2: ("920",),
}


@dataclass(frozen=True)
class TdxServer:
    name: str
    host: str
    port: int = 7709


def market_from_code(code: str) -> int:
    if code.startswith("920"):
        return 2
    return MARKET_MAP.get(code[:1], 0)


def is_a_share_code(code: str, market: int | None = None) -> bool:
    clean_code = str(code).strip()
    if len(clean_code) != 6 or not clean_code.isdigit():
        return False
    prefixes = MARKET_A_SHARE_PREFIXES.get(market) if market is not None else None
    if prefixes:
        return clean_code.startswith(prefixes)
    return any(clean_code.startswith(items) for items in MARKET_A_SHARE_PREFIXES.values())


def fetch_sina_a_share_list(timeout: int = 10) -> list[StockDefinition]:
    stocks: dict[str, StockDefinition] = {}
    total = _fetch_sina_count(timeout)
    page_count = max(1, (total + SINA_PAGE_SIZE - 1) // SINA_PAGE_SIZE)
    for page in range(1, page_count + 1):
        rows = _fetch_sina_page(page, timeout)
        for row in rows:
            code = str(row.get("code", "")).strip()
            name = str(row.get("name", "")).strip()
            if is_a_share_code(code) and name:
                stocks[code] = StockDefinition(code=code, name=name)
    return sorted(stocks.values(), key=lambda item: (market_from_code(item.code), item.code))


def _fetch_sina_count(timeout: int) -> int:
    payload = _open_json_url(SINA_COUNT_URL, {"node": "hs_a"}, timeout)
    return int(payload)


def _fetch_sina_page(page: int, timeout: int) -> list[dict]:
    return _open_json_url(
        SINA_LIST_URL,
        {
            "page": page,
            "num": SINA_PAGE_SIZE,
            "sort": "symbol",
            "asc": 1,
            "node": "hs_a",
            "symbol": "",
            "_s_r_a": "page",
        },
        timeout,
    )


def _open_json_url(url: str, params: dict, timeout: int):
    full_url = f"{url}?{urllib.parse.urlencode(params)}"
    request = urllib.request.Request(
        full_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "http://finance.sina.com.cn/",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(0.4 * (attempt + 1))
    raise RuntimeError(f"Sina stock list fetch failed: {last_error}")


class TdxClient:
    def __init__(
        self,
        servers: list[TdxServer],
        timeout: int = 5,
        retry_count: int = 3,
    ) -> None:
        self.servers = servers
        self.timeout = timeout
        self.retry_count = retry_count
        self._api = None
        self.connected_server: TdxServer | None = None

    def connect(self) -> bool:
        from pytdx.hq import TdxHq_API

        self.disconnect()
        attempts = max(1, self.retry_count)
        for _ in range(attempts):
            for server in self.servers:
                api = TdxHq_API(heartbeat=True, auto_retry=True, raise_exception=False)
                with suppress(Exception):
                    if api.connect(server.host, server.port, time_out=self.timeout):
                        self._api = api
                        self.connected_server = server
                        return True
                with suppress(Exception):
                    api.disconnect()
        return False

    def disconnect(self) -> None:
        if self._api is not None:
            with suppress(Exception):
                self._api.disconnect()
        self._api = None
        self.connected_server = None

    def __enter__(self) -> "TdxClient":
        if not self.connect():
            raise ConnectionError("Unable to connect to TDX market data server")
        return self

    def __exit__(self, *_args: object) -> None:
        self.disconnect()

    def get_quotes(self, stocks: Iterable[StockDefinition]) -> dict[str, StockQuote]:
        if self._api is None:
            raise ConnectionError("TDX not connected")

        stock_list = list(stocks)
        name_map = {stock.code: stock.name for stock in stock_list}
        result: dict[str, StockQuote] = {}
        for start in range(0, len(stock_list), QUOTE_BATCH_SIZE):
            batch = stock_list[start : start + QUOTE_BATCH_SIZE]
            pairs = [(market_from_code(stock.code), stock.code) for stock in batch]
            try:
                raw_quotes = self._api.get_security_quotes(pairs)
            except Exception:
                raw_quotes = None
            if not raw_quotes:
                if len(batch) > 1:
                    result.update(self._get_quotes_one_by_one(batch, name_map))
                continue
            result.update(self._parse_quotes(raw_quotes, name_map))
        return result

    def _get_quotes_one_by_one(
        self,
        stocks: list[StockDefinition],
        name_map: dict[str, str],
    ) -> dict[str, StockQuote]:
        result: dict[str, StockQuote] = {}
        for stock in stocks:
            with suppress(Exception):
                raw_quote = self._api.get_security_quotes([(market_from_code(stock.code), stock.code)])
                if raw_quote:
                    result.update(self._parse_quotes(raw_quote, name_map))
        return result

    def _parse_quotes(
        self,
        raw_quotes: Iterable[dict],
        name_map: dict[str, str],
    ) -> dict[str, StockQuote]:
        result: dict[str, StockQuote] = {}
        for item in raw_quotes:
            code = str(item.get("code", ""))
            price = float(item.get("price") or item.get("last_close") or 0)
            previous_close = float(item.get("last_close") or price or 0)
            pct_chg = 0.0
            if previous_close:
                pct_chg = (price - previous_close) / previous_close * 100
            result[code] = StockQuote(
                code=code,
                name=name_map.get(code, code),
                price=price,
                previous_close=previous_close,
                open_price=float(item.get("open") or price or 0),
                high=float(item.get("high") or price or 0),
                low=float(item.get("low") or price or 0),
                volume=float(item.get("vol") or item.get("volume") or 0),
                amount=float(item.get("amount") or 0),
                pct_chg=pct_chg,
                source="tdx",
            )
        return result

    def get_a_share_list(self) -> list[StockDefinition]:
        if self._api is None:
            raise ConnectionError("TDX not connected")

        with suppress(Exception):
            stocks = fetch_sina_a_share_list(timeout=self.timeout)
            if stocks:
                return stocks

        stocks: dict[str, StockDefinition] = {}
        for market in (0, 1, 2):
            try:
                count = int(self._api.get_security_count(market) or 0)
            except Exception:
                continue

            for start in range(0, count, SECURITY_LIST_PAGE_SIZE):
                try:
                    items = self._api.get_security_list(market, start) or []
                except Exception:
                    continue
                for item in items:
                    code = str(item.get("code", "")).strip()
                    name = str(item.get("name", "")).strip()
                    if is_a_share_code(code, market) and name:
                        stocks[code] = StockDefinition(code=code, name=name)

        return sorted(stocks.values(), key=lambda item: (market_from_code(item.code), item.code))

    def get_bars(self, stock: StockDefinition, count: int = 80) -> list[Bar]:
        if self._api is None:
            raise ConnectionError("TDX not connected")
        raw_bars = self._api.get_security_bars(
            9,
            market_from_code(stock.code),
            stock.code,
            0,
            count,
        )
        if not raw_bars:
            return []
        bars: list[Bar] = []
        for item in raw_bars:
            bars.append(
                Bar(
                    open=float(item.get("open") or 0),
                    close=float(item.get("close") or 0),
                    high=float(item.get("high") or 0),
                    low=float(item.get("low") or 0),
                    volume=float(item.get("vol") or item.get("volume") or 0),
                    amount=float(item.get("amount") or 0),
                )
            )
        return bars
