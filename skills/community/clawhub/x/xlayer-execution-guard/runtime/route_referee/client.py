from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, ROUND_DOWN
from typing import Any, Dict, Iterable, List, Optional
from urllib.parse import urlencode

import requests

API_BASE_URL = os.getenv("ONCHAINOS_API_BASE", "https://web3.okx.com").rstrip("/")
DEFAULT_CHAIN_INDEX = os.getenv("ONCHAINOS_CHAIN_INDEX", "196")


@dataclass(frozen=True)
class TokenInfo:
    symbol: str
    address: str
    decimals: int
    name: str = ""


class OnchainOSError(RuntimeError):
    pass


class OnchainOSClient:
    def __init__(self, api_key: str = "", api_secret: str = "", passphrase: str = ""):
        self.api_key = api_key or os.getenv("ONCHAINOS_API_KEY", "") or os.getenv("OKX_API_KEY", "") or os.getenv("OK_API_KEY", "")
        self.api_secret = api_secret or os.getenv("ONCHAINOS_API_SECRET", "") or os.getenv("OKX_SECRET_KEY", "") or os.getenv("OK_SECRET_KEY", "")
        self.passphrase = passphrase or os.getenv("ONCHAINOS_API_PASSPHRASE", "") or os.getenv("OKX_PASSPHRASE", "") or os.getenv("OK_PASSPHRASE", "")
        self.base_url = API_BASE_URL
        self.chain_index = DEFAULT_CHAIN_INDEX
        self.timeout = int(os.getenv("ONCHAINOS_TIMEOUT", "20"))
        self.proxy = os.getenv("ONCHAINOS_PROXY", "").strip() or os.getenv("HTTPS_PROXY", "").strip()
        self.session = requests.Session()
        if self.proxy:
            self.session.proxies.update({"http": self.proxy, "https": self.proxy})
        self._token_cache: Dict[str, TokenInfo] = {}
        self._liquidity_cache: Optional[List[Dict[str, str]]] = None

    @property
    def is_configured(self) -> bool:
        return bool(self.api_key and self.api_secret and self.passphrase)

    def _timestamp(self) -> str:
        now = datetime.now(timezone.utc)
        return now.isoformat(timespec="milliseconds").replace("+00:00", "Z")

    def _sign(self, timestamp: str, method: str, request_path: str, body: str = "") -> str:
        message = f"{timestamp}{method.upper()}{request_path}{body}"
        digest = hmac.new(self.api_secret.encode(), message.encode(), hashlib.sha256).digest()
        return base64.b64encode(digest).decode()

    def _headers(self, method: str, request_path: str, body: str = "") -> Dict[str, str]:
        if not self.is_configured:
            raise OnchainOSError("Missing ONCHAINOS_API_KEY / ONCHAINOS_API_SECRET / ONCHAINOS_API_PASSPHRASE")
        timestamp = self._timestamp()
        return {
            "OK-ACCESS-KEY": self.api_key,
            "OK-ACCESS-SIGN": self._sign(timestamp, method, request_path, body),
            "OK-ACCESS-TIMESTAMP": timestamp,
            "OK-ACCESS-PASSPHRASE": self.passphrase,
            "Content-Type": "application/json",
            "User-Agent": "xlayer-route-referee/1.0",
        }

    def _request(self, method: str, path: str, *, params: Optional[Dict[str, Any]] = None) -> Any:
        params = {k: v for k, v in (params or {}).items() if v is not None and v != ""}
        query = urlencode(params, doseq=True)
        request_path = path if not query else f"{path}?{query}"
        headers = self._headers(method, request_path)
        response = self.session.request(
            method=method.upper(),
            url=f"{self.base_url}{path}",
            params=params or None,
            headers=headers,
            timeout=self.timeout,
        )
        payload = response.json() if "application/json" in response.headers.get("content-type", "") else {"raw": response.text}
        if response.status_code >= 400:
            raise OnchainOSError(f"HTTP {response.status_code}: {payload}")
        if isinstance(payload, dict) and payload.get("code") not in (None, "0", 0):
            raise OnchainOSError(f"OKX API error {payload.get('code')}: {payload.get('msg') or payload}")
        return payload.get("data", payload)

    @staticmethod
    def to_base_units(amount: Decimal, decimals: int) -> str:
        scaled = amount * (Decimal(10) ** decimals)
        return str(int(scaled.to_integral_value(rounding=ROUND_DOWN)))

    @staticmethod
    def from_base_units(amount: str | int, decimals: int) -> Decimal:
        return Decimal(str(amount)) / (Decimal(10) ** decimals)

    def supported_tokens(self, *, refresh: bool = False) -> List[TokenInfo]:
        if self._token_cache and not refresh:
            return list(self._token_cache.values())
        data = self._request("GET", "/api/v6/dex/aggregator/all-tokens", params={"chainIndex": self.chain_index})
        cache: Dict[str, TokenInfo] = {}
        for item in data:
            symbol = str(item.get("tokenSymbol", "")).upper()
            address = item.get("tokenContractAddress", "")
            if not symbol or not address:
                continue
            cache[symbol] = TokenInfo(
                symbol=symbol,
                address=address,
                decimals=int(item.get("decimals", 18)),
                name=item.get("tokenName", ""),
            )
        self._token_cache = cache
        return list(cache.values())

    def resolve_token(self, symbol_or_address: str) -> TokenInfo:
        if symbol_or_address.startswith("0x") and len(symbol_or_address) == 42:
            for token in self.supported_tokens():
                if token.address.lower() == symbol_or_address.lower():
                    return token
            raise OnchainOSError(f"Token address not found on chain {self.chain_index}: {symbol_or_address}")
        symbol = symbol_or_address.upper()
        if symbol not in self._token_cache:
            self.supported_tokens()
        if symbol not in self._token_cache:
            raise OnchainOSError(f"Token symbol not found on chain {self.chain_index}: {symbol_or_address}")
        return self._token_cache[symbol]

    def liquidity_sources(self, *, refresh: bool = False) -> List[Dict[str, str]]:
        if self._liquidity_cache is not None and not refresh:
            return self._liquidity_cache
        data = self._request("GET", "/api/v6/dex/aggregator/get-liquidity", params={"chainIndex": self.chain_index})
        self._liquidity_cache = [{"id": str(item.get("id", "")), "name": item.get("name", "")} for item in data]
        return self._liquidity_cache

    def liquidity_id_map(self, names: Iterable[str]) -> Dict[str, str]:
        wanted = {name.lower(): name for name in names}
        resolved: Dict[str, str] = {}
        for item in self.liquidity_sources():
            normalized = item["name"].lower()
            for key, original in wanted.items():
                if key in normalized or normalized in key:
                    resolved[original] = item["id"]
        return resolved

    def quote(self, *, amount: str, from_token_address: str, to_token_address: str, dex_ids: Optional[str] = None) -> Dict[str, Any]:
        data = self._request(
            "GET",
            "/api/v6/dex/aggregator/quote",
            params={
                "chainIndex": self.chain_index,
                "amount": amount,
                "swapMode": "exactIn",
                "fromTokenAddress": from_token_address,
                "toTokenAddress": to_token_address,
                "dexIds": dex_ids,
                "singleRouteOnly": "true",
                "singlePoolPerHop": "true",
                "priceImpactProtectionPercent": "15",
            },
        )
        if not data:
            raise OnchainOSError("Empty quote response")
        return data[0]
