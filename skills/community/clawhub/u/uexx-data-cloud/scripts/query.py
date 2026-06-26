import argparse
import json
from typing import Any

from uexx_client import authed_get


ENDPOINTS = {
    "fear-greed": "/api/v1/query/fear-greed/latest",
    "altcoin-season": "/api/v1/query/altcoin-season/latest",
    "funding-rate": "/api/v1/query/symbol/{symbol}/funding-rate/latest",
    "oi": "/api/v1/query/symbol/{symbol}/oi/latest",
    "long-short": "/api/v1/query/symbol/{symbol}/long-short/latest",
}


def normalize_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    return value if value.endswith("USDT") else f"{value}USDT"


def main() -> None:
    parser = argparse.ArgumentParser(description="Query UEXX Data Cloud latest market data.")
    parser.add_argument("intent", choices=sorted(ENDPOINTS))
    parser.add_argument("--symbol", default="BTCUSDT")
    args = parser.parse_args()
    symbol = normalize_symbol(args.symbol)
    endpoint = ENDPOINTS[args.intent].format(symbol=symbol)
    payload: dict[str, Any] = authed_get(endpoint)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
