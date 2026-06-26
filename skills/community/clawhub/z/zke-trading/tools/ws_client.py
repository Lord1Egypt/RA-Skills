import json
import threading
import time
from typing import Callable, List, Optional, Dict, Any

import websocket

from .ws_parser import decode_ws_message, is_ping_message, build_pong


class ZKEWebSocketClient:
    def __init__(
        self,
        url: str,
        subscriptions: Optional[List[dict]] = None,
        on_message: Optional[Callable[[Dict[str, Any]], None]] = None,
        reconnect: bool = True,
        reconnect_delay: int = 5,
        debug: bool = False,
        headers: Optional[Dict[str, str]] = None,
        heartbeat_interval: Optional[int] = None,
        heartbeat_payload_factory: Optional[Callable[[], dict]] = None,
    ):
        self.url = url
        self.subscriptions = subscriptions or []
        self.on_message_cb = on_message
        self.reconnect = reconnect
        self.reconnect_delay = reconnect_delay
        self.debug = debug
        self.headers = headers or {}

        # 主动心跳（适用于 futures 订单/仓位 WS、spot 用户数据 WS）
        self.heartbeat_interval = heartbeat_interval
        self.heartbeat_payload_factory = heartbeat_payload_factory

        self.ws_app = None
        self._stop = False
        self._thread = None
        self._heartbeat_thread = None

    def log(self, *args):
        if self.debug:
            print("[WS]", *args)

    def _build_header_list(self):
        """
        websocket-client 的 header 支持 list[str]
        例如:
        ["token: abc", "api-key: xxx"]
        """
        header_list = []
        for k, v in self.headers.items():
            header_list.append(f"{k}: {v}")
        return header_list

    def _heartbeat_loop(self):
        while not self._stop:
            try:
                if (
                    self.ws_app
                    and self.ws_app.sock
                    and self.ws_app.sock.connected
                    and self.heartbeat_interval
                    and self.heartbeat_payload_factory
                ):
                    payload = self.heartbeat_payload_factory()
                    if payload:
                        self.send(payload)
            except Exception as e:
                self.log("heartbeat error:", e)

            time.sleep(self.heartbeat_interval or 1)

    def _start_heartbeat(self):
        if self.heartbeat_interval and self.heartbeat_payload_factory:
            if self._heartbeat_thread and self._heartbeat_thread.is_alive():
                return

            self._heartbeat_thread = threading.Thread(
                target=self._heartbeat_loop,
                daemon=True
            )
            self._heartbeat_thread.start()

    def _on_open(self, ws):
        self.log("connected:", self.url)

        # 建连后先发订阅
        for sub in self.subscriptions:
            self.send(sub)

        # 启动主动心跳
        self._start_heartbeat()

    def _on_message(self, ws, message):
        data = decode_ws_message(message)

        if data is None:
            return

        # 市场 WS 常见：服务端发 ping，客户端回 pong
        if is_ping_message(data):
            pong = build_pong(data)
            if pong:
                self.send(pong)
            return

        # 某些 WS 也可能直接回 pong 文本
        if isinstance(data, dict) and "pong" in data:
            self.log("recv pong:", data)
            return

        # connect success / sub success 这类纯文本有可能被 parser 原样返回字符串
        if self.on_message_cb:
            self.on_message_cb(data)

    def _on_error(self, ws, error):
        print("[WS ERROR]", error)

    def _on_close(self, ws, code, msg):
        print(f"[WS CLOSED] code={code} msg={msg}")

    def send(self, payload: dict):
        if self.ws_app and self.ws_app.sock and self.ws_app.sock.connected:
            text = json.dumps(payload, ensure_ascii=False)
            self.log("send:", text)
            self.ws_app.send(text)

    def run_forever(self):
        while not self._stop:
            try:
                self.ws_app = websocket.WebSocketApp(
                    self.url,
                    header=self._build_header_list(),
                    on_open=self._on_open,
                    on_message=self._on_message,
                    on_error=self._on_error,
                    on_close=self._on_close,
                )
                self.ws_app.run_forever()
            except KeyboardInterrupt:
                self._stop = True
                raise
            except Exception as e:
                print("[WS RUN ERROR]", e)

            if self._stop:
                break

            if not self.reconnect:
                break

            print(f"[WS] reconnect after {self.reconnect_delay}s ...")
            time.sleep(self.reconnect_delay)

    def start_background(self):
        self._thread = threading.Thread(target=self.run_forever, daemon=True)
        self._thread.start()
        return self._thread

    def close(self):
        self._stop = True
        if self.ws_app:
            try:
                self.ws_app.close()
            except Exception:
                pass


def build_market_ws_client(
    symbol: str,
    channel: str,
    on_message: Optional[Callable[[Dict[str, Any]], None]] = None,
    debug: bool = False,
):
    """
    现货市场 WS:
    wss://ws.zke.com/kline-api/ws

    channel 示例:
    - market_btcusdt_ticker
    - market_btcusdt_trade_ticker
    - market_btcusdt_depth_step0
    - market_btcusdt_kline_1min
    """
    url = "wss://ws.zke.com/kline-api/ws"

    sub = {
        "event": "sub",
        "params": {
            "channel": channel,
            "cb_id": "1"
        }
    }

    return ZKEWebSocketClient(
        url=url,
        subscriptions=[sub],
        on_message=on_message,
        reconnect=True,
        reconnect_delay=5,
        debug=debug,
    )


def build_futures_position_order_ws_client(
    api_key: Optional[str] = None,
    token: Optional[str] = None,
    broker: int = 1003,
    on_message: Optional[Callable[[Dict[str, Any]], None]] = None,
    debug: bool = False,
):
    """
    Futures 订单/仓位 WS:
    wss://futuresws.zke.com/position_order/ws

    连接 header:
    - token: xxx
    或
    - api-key: xxx

    订阅:
    {"event":"sub","token|apiKey":"...","broker":1003}

    主动心跳:
    每 30 秒发送 {"ping": ts}
    """
    url = "wss://futuresws.zke.com/position_order/ws"

    headers = {}
    sub = {
        "event": "sub",
        "broker": broker,
    }

    if token:
        headers["token"] = token
        sub["token"] = token
    elif api_key:
        headers["api-key"] = api_key
        sub["apiKey"] = api_key
    else:
        raise ValueError("futures ws 连接必须提供 token 或 api_key。")

    def heartbeat_payload():
        return {"ping": int(time.time() * 1000)}

    return ZKEWebSocketClient(
        url=url,
        headers=headers,
        subscriptions=[sub],
        on_message=on_message,
        reconnect=True,
        reconnect_delay=5,
        debug=debug,
        heartbeat_interval=30,
        heartbeat_payload_factory=heartbeat_payload,
    )


def build_spot_user_data_ws_client(
    api_key: Optional[str] = None,
    token: Optional[str] = None,
    on_message: Optional[Callable[[Dict[str, Any]], None]] = None,
    debug: bool = False,
):
    """
    Spot 用户数据 WS:
    wss://ws2.zke.com/spotws_user/userData/ws

    连接 header:
    - token: xxx
    或
    - api-key: xxx

    订阅:
    {"event":"sub","token":"..."}  # 文档示例如此
    （即便 api-key 模式，消息体文档也仍写 token 字段）

    主动心跳:
    每 30 秒发送 {"ping": ts}
    """
    url = "wss://ws2.zke.com/spotws_user/userData/ws"

    headers = {}
    sub = {"event": "sub"}

    if token:
        headers["token"] = token
        sub["token"] = token
    elif api_key:
        headers["api-key"] = api_key
        # 按你给的文档示例，这里消息体仍使用 token 字段承载 api-key
        sub["token"] = api_key
    else:
        raise ValueError("spot user data ws 连接必须提供 token 或 api_key。")

    def heartbeat_payload():
        return {"ping": int(time.time() * 1000)}

    return ZKEWebSocketClient(
        url=url,
        headers=headers,
        subscriptions=[sub],
        on_message=on_message,
        reconnect=True,
        reconnect_delay=5,
        debug=debug,
        heartbeat_interval=30,
        heartbeat_payload_factory=heartbeat_payload,
    )
