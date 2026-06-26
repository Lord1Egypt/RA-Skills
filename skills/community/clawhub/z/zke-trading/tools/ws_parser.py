import gzip
import json
from io import BytesIO
from typing import Any


def _decode_bytes_message(message: bytes) -> str:
    """
    优先按 gzip 解压；失败则按普通 utf-8 bytes 解析
    """
    try:
        with gzip.GzipFile(fileobj=BytesIO(message)) as f:
            return f.read().decode("utf-8")
    except Exception:
        return message.decode("utf-8", errors="ignore")


def decode_ws_message(message: Any):
    """
    处理 websocket 原始消息：
    - bytes: 尝试 gzip 解压
    - str: 直接使用
    - json text: 尝试转 dict/list
    - 非 json text: 返回 {"raw_text": "..."}
    """
    if isinstance(message, bytes):
        text = _decode_bytes_message(message)
    else:
        text = str(message)

    text = text.strip()
    if not text:
        return None

    try:
        return json.loads(text)
    except Exception:
        return {"raw_text": text}


def is_ping_message(data) -> bool:
    if not isinstance(data, dict):
        return False
    return "ping" in data


def build_pong(data):
    if not isinstance(data, dict):
        return None

    if "ping" in data:
        return {"pong": data["ping"]}

    return None


def get_channel(data) -> str:
    if not isinstance(data, dict):
        return ""
    return str(data.get("channel", "")).strip()


def get_event_rep(data) -> str:
    if not isinstance(data, dict):
        return ""
    return str(data.get("event_rep", "")).strip().lower()


def detect_channel_type(data):
    """
    根据 ZKE WS 文档识别消息类型
    """

    # 非 dict，可能是 connect success / sub success 等文本
    if not isinstance(data, dict):
        return "unknown"

    # 现货用户数据 WS
    event_name = str(data.get("e", "")).strip()
    if event_name == "outboundAccountPosition":
        return "spot_user_balance"
    if event_name == "executionReport":
        return "spot_user_order"

    # futures / system
    channel = get_channel(data).lower()
    event_rep = get_event_rep(data)

    if channel == "account_update":
        return "futures_account_update"

    if channel == "adl_price":
        return "futures_adl_price"

    if channel == "system":
        return "system"

    if channel == "order":
        return "futures_order"

    if channel == "trigorder":
        return "futures_trigger_order"

    # 市场 WS
    if "ticker" in channel and "trade_ticker" not in channel:
        return "ticker"

    if "depth" in channel:
        return "depth"

    if "kline" in channel:
        return "kline"

    if "trade_ticker" in channel:
        return "trade"

    if event_rep == "rep":
        return "reply"

    # 纯 pong / 其他
    if "pong" in data:
        return "pong"

    return "unknown"


def normalize_ws_message(data):
    """
    统一整理 ZKE WS 返回，方便 CLI / 上层服务使用
    """
    # 非 dict，兜底
    if not isinstance(data, dict):
        return {
            "type": "unknown",
            "raw": data,
        }

    # 纯文本消息包装后的结构
    if "raw_text" in data:
        raw_text = str(data.get("raw_text", "")).strip()
        lowered = raw_text.lower()

        if lowered == "connect success":
            return {
                "type": "connect_success",
                "raw_text": raw_text,
                "raw": data,
            }

        if lowered == "sub success":
            return {
                "type": "sub_success",
                "raw_text": raw_text,
                "raw": data,
            }

        return {
            "type": "text",
            "raw_text": raw_text,
            "raw": data,
        }

    kind = detect_channel_type(data)
    channel = get_channel(data)
    ts = data.get("ts")
    tick = data.get("tick")
    rows = data.get("data")
    status = data.get("status")
    cb_id = data.get("cb_id")

    result = {
        "type": kind,
        "channel": channel,
        "ts": ts,
        "raw": data,
    }

    if cb_id is not None:
        result["cb_id"] = cb_id

    if status is not None:
        result["status"] = status

    if isinstance(tick, dict):
        result["tick"] = tick

    if isinstance(rows, list):
        result["data"] = rows
        result["count"] = len(rows)

    # 市场 WS 历史回复
    if kind == "reply":
        result["reply_channel"] = channel

    # spot 用户资产变化
    if kind == "spot_user_balance":
        result["event"] = data.get("e")
        result["event_time"] = data.get("E")
        result["update_time"] = data.get("u")
        result["balances"] = data.get("B", [])

    # spot 用户订单变化
    if kind == "spot_user_order":
        result["event"] = data.get("e")
        result["event_time"] = data.get("E")
        result["symbol"] = data.get("s")
        result["order_id"] = data.get("i")
        result["side"] = data.get("S")
        result["order_type"] = data.get("o")
        result["price"] = data.get("p")
        result["orig_qty"] = data.get("q")
        result["quote_qty"] = data.get("Q")
        result["last_qty"] = data.get("l")
        result["cum_qty"] = data.get("z")
        result["last_price"] = data.get("L")
        result["last_amount"] = data.get("Y")
        result["cum_amount"] = data.get("Z")
        result["status"] = data.get("X")
        result["exec_type"] = data.get("x")
        result["fee"] = data.get("n")
        result["create_time"] = data.get("O")
        result["trade_time"] = data.get("T")

    # futures 账户/仓位变化
    if kind == "futures_account_update":
        result["uid"] = data.get("uid")
        result["event_time"] = data.get("t")
        result["detail"] = data.get("d", {})

    # futures ADL
    if kind == "futures_adl_price":
        result["uid"] = data.get("uid")
        result["positions"] = data.get("l", [])

    # futures 普通订单
    if kind == "futures_order":
        result["order"] = data.get("order", {})

    # futures 条件单
    if kind == "futures_trigger_order":
        result["trigger_order"] = data.get("trigOrder", {})

    # system
    if kind == "system":
        result["uid"] = data.get("uid")
        result["et"] = data.get("et")

    # pong
    if kind == "pong":
        result["pong"] = data.get("pong")

    return result
