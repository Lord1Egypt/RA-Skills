from decimal import Decimal, ROUND_DOWN
from typing import Optional


# 现货新版文档支持:
# LIMIT / MARKET / FOK / POST_ONLY / IOC / STOP
# 合约新版文档常见:
# LIMIT / MARKET
VALID_ORDER_TYPES = {
    "LIMIT",
    "MARKET",
    "FOK",
    "POST_ONLY",
    "IOC",
    "STOP",
}

VALID_SIDES = {"BUY", "SELL"}

VALID_SPOT_INTERVALS = {
    "1min", "5min", "15min", "30min", "60min",
    "1day", "1week", "1month"
}

VALID_FUTURES_INTERVALS = {
    "1min", "5min", "15min", "30min", "1h",
    "1day", "1week", "1month"
}


def normalize_symbol(symbol: str) -> str:
    return str(symbol).strip().upper()


def normalize_spot_api_symbol(symbol: str) -> str:
    return str(symbol).strip().lower()


def ensure_order_type(order_type: str) -> str:
    value = str(order_type).strip().upper()
    if value not in VALID_ORDER_TYPES:
        raise ValueError(f"无效订单类型: {order_type}")
    return value


def ensure_side(side: str) -> str:
    value = str(side).strip().upper()
    if value not in VALID_SIDES:
        raise ValueError(f"无效买卖方向: {side}")
    return value


def ensure_spot_interval(interval: str) -> str:
    value = str(interval).strip()
    if value not in VALID_SPOT_INTERVALS:
        raise ValueError(f"无效现货K线周期: {interval}")
    return value


def ensure_futures_interval(interval: str) -> str:
    value = str(interval).strip()
    if value not in VALID_FUTURES_INTERVALS:
        raise ValueError(f"无效合约K线周期: {interval}")
    return value


def format_decimal_by_precision(value: str, precision: int) -> str:
    q = Decimal("1").scaleb(-precision)
    return str(Decimal(str(value)).quantize(q, rounding=ROUND_DOWN))


def decimal_ge(a: str, b: str) -> bool:
    return Decimal(str(a)) >= Decimal(str(b))


def decimal_mul(a: str, b: str) -> str:
    return str(Decimal(str(a)) * Decimal(str(b)))


def decimal_le(a: str, b: str) -> bool:
    return Decimal(str(a)) <= Decimal(str(b))


def decimal_gt(a: str, b: str) -> bool:
    return Decimal(str(a)) > Decimal(str(b))


def decimal_lt(a: str, b: str) -> bool:
    return Decimal(str(a)) < Decimal(str(b))


def optional_str(value: Optional[object]) -> Optional[str]:
    if value is None:
        return None
    return str(value)
