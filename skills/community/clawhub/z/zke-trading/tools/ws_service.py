import json
import time
from typing import Optional, Callable

from .ws_client import (
    ZKEWebSocketClient,
    build_market_ws_client,
    build_futures_position_order_ws_client,
    build_spot_user_data_ws_client,
)
from .ws_parser import normalize_ws_message


DEFAULT_MARKET_WS_URL = "wss://ws.zke.com/kline-api/ws"
DEFAULT_FUTURES_POSITION_ORDER_WS_URL = "wss://futuresws.zke.com/position_order/ws"
DEFAULT_SPOT_USER_DATA_WS_URL = "wss://ws2.zke.com/spotws_user/userData/ws"


def _print_json(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


def _norm_symbol(symbol: str) -> str:
    return str(symbol).strip().lower()


def build_sub(channel: str, cb_id: str = "1") -> dict:
    return {
        "event": "sub",
        "params": {
            "channel": channel,
            "cb_id": cb_id,
        }
    }


def build_unsub(channel: str, cb_id: str = "1") -> dict:
    return {
        "event": "unsub",
        "params": {
            "channel": channel,
            "cb_id": cb_id,
        }
    }


def build_req(
    channel: str,
    cb_id: str = "1",
    end_idx: Optional[str] = None,
    page_size: Optional[int] = None
) -> dict:
    params = {
        "channel": channel,
        "cb_id": cb_id,
    }

    if end_idx is not None:
        params["endIdx"] = str(end_idx)

    if page_size is not None:
        params["pageSize"] = int(page_size)

    return {
        "event": "req",
        "params": params,
    }


def build_ticker_sub(symbol: str, cb_id: str = "1") -> dict:
    symbol = _norm_symbol(symbol)
    return build_sub(f"market_{symbol}_ticker", cb_id)


def build_depth_sub(symbol: str, step: str = "step0", cb_id: str = "1") -> dict:
    symbol = _norm_symbol(symbol)
    return build_sub(f"market_{symbol}_depth_{step}", cb_id)


def build_kline_sub(symbol: str, interval: str = "1min", cb_id: str = "1") -> dict:
    symbol = _norm_symbol(symbol)
    return build_sub(f"market_{symbol}_kline_{interval}", cb_id)


def build_trade_sub(symbol: str, cb_id: str = "1") -> dict:
    symbol = _norm_symbol(symbol)
    return build_sub(f"market_{symbol}_trade_ticker", cb_id)


def build_kline_req(
    symbol: str,
    interval: str = "1min",
    cb_id: str = "1",
    end_idx: Optional[str] = None,
    page_size: Optional[int] = None
) -> dict:
    symbol = _norm_symbol(symbol)
    return build_req(
        f"market_{symbol}_kline_{interval}",
        cb_id,
        end_idx=end_idx,
        page_size=page_size
    )


def build_trade_req(symbol: str, cb_id: str = "1") -> dict:
    symbol = _norm_symbol(symbol)
    return build_req(f"market_{symbol}_trade_ticker", cb_id)


def build_futures_sub(token: Optional[str] = None, api_key: Optional[str] = None, broker: int = 1003) -> dict:
    payload = {
        "event": "sub",
        "broker": broker,
    }

    if token:
        payload["token"] = token
    elif api_key:
        payload["apiKey"] = api_key
    else:
        raise ValueError("必须提供 token 或 api_key。")

    return payload


def build_futures_unsub(token: Optional[str] = None, api_key: Optional[str] = None, broker: int = 1003) -> dict:
    payload = {
        "event": "unsub",
        "broker": broker,
    }

    if token:
        payload["token"] = token
    elif api_key:
        payload["apiKey"] = api_key
    else:
        raise ValueError("必须提供 token 或 api_key。")

    return payload


def build_spot_user_data_sub(token: Optional[str] = None, api_key: Optional[str] = None) -> dict:
    payload = {"event": "sub"}

    if token:
        payload["token"] = token
    elif api_key:
        # 按你给的文档示例，api-key 模式消息体仍用 token 字段
        payload["token"] = api_key
    else:
        raise ValueError("必须提供 token 或 api_key。")

    return payload


def build_spot_user_data_unsub(token: Optional[str] = None, api_key: Optional[str] = None) -> dict:
    payload = {"event": "unsub"}

    if token:
        payload["token"] = token
    elif api_key:
        payload["token"] = api_key
    else:
        raise ValueError("必须提供 token 或 api_key。")

    return payload


def default_message_handler(data):
    normalized = normalize_ws_message(data)
    kind = normalized.get("type", "unknown").upper()
    print(f"\n===== WS {kind} =====")
    _print_json(normalized)


def run_ws_once(
    ws_url: str,
    subscriptions: list,
    seconds: int = 30,
    debug: bool = False,
    on_message: Optional[Callable] = None,
    headers: Optional[dict] = None,
    heartbeat_interval: Optional[int] = None,
    heartbeat_payload_factory: Optional[Callable[[], dict]] = None,
):
    client = ZKEWebSocketClient(
        url=ws_url,
        subscriptions=subscriptions,
        on_message=on_message or default_message_handler,
        reconnect=True,
        reconnect_delay=3,
        debug=debug,
        headers=headers,
        heartbeat_interval=heartbeat_interval,
        heartbeat_payload_factory=heartbeat_payload_factory,
    )

    thread = client.start_background()

    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

    if thread:
        thread.join(timeout=2)


# =========================================================
# Market WS
# =========================================================

def run_ws_ticker(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    seconds: int = 30,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_ticker_sub(symbol)],
        seconds=seconds,
        debug=debug,
    )


def run_ws_depth(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    step: str = "step0",
    seconds: int = 30,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_depth_sub(symbol, step=step)],
        seconds=seconds,
        debug=debug,
    )


def run_ws_kline(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    interval: str = "1min",
    seconds: int = 30,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_kline_sub(symbol, interval=interval)],
        seconds=seconds,
        debug=debug,
    )


def run_ws_trades(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    seconds: int = 30,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_trade_sub(symbol)],
        seconds=seconds,
        debug=debug,
    )


def run_ws_kline_req(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    interval: str = "1min",
    seconds: int = 10,
    end_idx: Optional[str] = None,
    page_size: Optional[int] = None,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_kline_req(symbol, interval=interval, end_idx=end_idx, page_size=page_size)],
        seconds=seconds,
        debug=debug,
    )


def run_ws_trade_req(
    ws_url: str = DEFAULT_MARKET_WS_URL,
    symbol: str = "",
    seconds: int = 10,
    debug: bool = False,
):
    run_ws_once(
        ws_url=ws_url,
        subscriptions=[build_trade_req(symbol)],
        seconds=seconds,
        debug=debug,
    )


# =========================================================
# Futures Position / Order WS
# =========================================================

def run_futures_position_order_ws(
    seconds: int = 30,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    broker: int = 1003,
    debug: bool = False,
):
    client = build_futures_position_order_ws_client(
        token=token,
        api_key=api_key,
        broker=broker,
        on_message=default_message_handler,
        debug=debug,
    )

    thread = client.start_background()

    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

    if thread:
        thread.join(timeout=2)


# =========================================================
# Spot User Data WS
# =========================================================

def run_spot_user_data_ws(
    seconds: int = 30,
    token: Optional[str] = None,
    api_key: Optional[str] = None,
    debug: bool = False,
):
    client = build_spot_user_data_ws_client(
        token=token,
        api_key=api_key,
        on_message=default_message_handler,
        debug=debug,
    )

    thread = client.start_background()

    try:
        time.sleep(seconds)
    except KeyboardInterrupt:
        pass
    finally:
        client.close()

    if thread:
        thread.join(timeout=2)
