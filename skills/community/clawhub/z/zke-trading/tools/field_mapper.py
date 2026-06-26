# tools/field_mapper.py


def map_side(side):
    """
    BUY -> long
    SELL -> short
    兼容 long/short/buy/sell 原样归一
    """
    if side is None:
        return "-"

    s = str(side).strip().upper()

    mapping = {
        "BUY": "long",
        "SELL": "short",
        "LONG": "long",
        "SHORT": "short",
    }

    return mapping.get(s, s.lower())


def map_open_close(value):
    """
    OPEN -> open
    CLOSE -> close
    """
    if value is None:
        return "-"

    s = str(value).strip().upper()

    mapping = {
        "OPEN": "open",
        "CLOSE": "close",
    }

    return mapping.get(s, s.lower())


def map_position_type(value):
    """
    1 -> cross
    2 -> isolated
    """
    try:
        v = int(value)
    except Exception:
        return str(value)

    if v == 1:
        return "cross"
    if v == 2:
        return "isolated"

    return str(v)


def map_order_status(value):
    """
    futures status:
    兼容数字 / 字符串状态
    """
    if value is None:
        return "-"

    # 先兼容字符串状态
    s = str(value).strip().upper()
    str_mapping = {
        "INIT": "init",
        "NEW": "new",
        "PARTIALLY_FILLED": "partial",
        "PART_FILLED": "partial",
        "FILLED": "filled",
        "CANCELED": "canceled",
        "CANCELLED": "canceled",
        "PENDING_CANCEL": "pending_cancel",
        "REJECTED": "rejected",
        "ERROR": "error",
    }
    if s in str_mapping:
        return str_mapping[s]

    # 再兼容旧数字状态
    try:
        v = int(value)
    except Exception:
        return s.lower()

    num_mapping = {
        0: "init",
        1: "new",
        2: "filled",
        3: "partial",
        4: "canceled",
        5: "partial_canceled",
        6: "error",
    }

    return num_mapping.get(v, str(v))


def map_spot_order_status(value):
    """
    spot status -> normalized lowercase
    """
    if value is None:
        return "-"

    s = str(value).strip().upper()

    mapping = {
        "NEW": "new",
        "PARTIALLY_FILLED": "partial",
        "PART_FILLED": "partial",
        "FILLED": "filled",
        "CANCELED": "canceled",
        "CANCELLED": "canceled",
        "PENDING_CANCEL": "pending_cancel",
        "REJECTED": "rejected",
    }

    return mapping.get(s, s.lower())


def map_order_type(value):
    """
    LIMIT / MARKET / IOC / FOK / POST_ONLY / STOP -> lowercase normalized
    某些 futures 历史记录可能返回数字，保留原始字符串
    """
    if value is None:
        return "-"

    s = str(value).strip().upper()

    mapping = {
        "LIMIT": "limit",
        "MARKET": "market",
        "IOC": "ioc",
        "FOK": "fok",
        "POST_ONLY": "post_only",
        "STOP": "stop",
    }

    return mapping.get(s, s.lower())


def map_bool_flag(value):
    """
    True/False -> yes/no
    """
    if isinstance(value, bool):
        return "yes" if value else "no"

    if value is None:
        return "-"

    return str(value)
