import sys
import json
from cookie_extractor import (
    cdp_session,
    extract_cookies,
    get_userid,
    get_stock_watchlist_via_browser,
    get_stock_positions_via_browser,
    get_trade_records_via_browser,
)

def _looks_like_not_logged_in(error_msg: str) -> bool:
    msg = (error_msg or "").lower()
    return ("未检测到登录态" in error_msg) or ("missing userid" in msg)


def _to_float(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return 0.0


def _to_int(v):
    try:
        return int(v)
    except (TypeError, ValueError):
        return 0


def parse_stock_list(data: dict) -> list[dict]:
    """从 API 响应中解析自选股列表"""
    try:
        ex_data = data.get("ex_data", {})
        stock_list = ex_data.get("list", [])
        stocks = []
        for item in stock_list:
            # type: "1" = 股票, "2" = 基金等
            item_type = str(item.get("type", ""))
            if item_type not in ("1", "stock", ""):
                continue
            stocks.append(
                {
                    "stock_code": item.get("code", ""),
                    "stock_name": item.get("name", ""),
                    "market": item.get("hq_market", "") or item.get("market", ""),
                    "account_type": "stock" if item_type == "1" else item_type,
                }
            )
        return stocks
    except (KeyError, TypeError) as e:
        return []


def parse_positions(data: dict) -> tuple[list[dict], dict]:
    """解析持仓数据，返回 (持仓列表, 账户概览)"""
    ex = data.get("ex_data", {})
    positions = []
    for item in ex.get("position", []) or []:
        positions.append(
            {
                "stock_code": str(item.get("code", "")),
                "stock_name": item.get("name", ""),
                "market": str(item.get("market", "")),
                "hold_count": _to_int(item.get("count", 0)),
                "cost_price": _to_float(item.get("cost", 0)),
                "current_price": _to_float(item.get("price", 0)),
                "market_value": _to_float(item.get("value", 0)),
                "hold_profit": _to_float(item.get("hold_profit", 0)),
                "hold_rate": _to_float(item.get("hold_rate", 0)),
                "position_rate": _to_float(item.get("position_rate", 0)),
                "hold_days": _to_int(item.get("hold_days", 0)),
            }
        )
    overview = {
        "total_asset": _to_float(ex.get("total_asset", 0) or 0),
        "total_value": _to_float(ex.get("total_value", 0) or 0),
        "money_remain": _to_float(ex.get("money_remain", 0) or 0),
        "total_liability": _to_float(ex.get("total_liability", 0) or 0),
        "position_rate": _to_float(ex.get("position_rate", 0) or 0),
    }
    return positions, overview


def parse_trade_records(raw_records: list[dict]) -> list[dict]:
    """从 DOM 提取的原始数据解析交易记录"""
    records = []
    for item in raw_records:
        if not item.get("stock_code"):
            continue
        records.append(
            {
                "trade_date": item.get("trade_date", ""),
                "stock_code": item.get("stock_code", ""),
                "stock_name": item.get("stock_name", ""),
                "trade_type": item.get("trade_type", ""),
                "price": _to_float(item.get("price") or 0),
                "quantity": _to_int(item.get("quantity") or 0),
                "amount": _to_float(item.get("amount") or 0),
                "fee": _to_float(item.get("fee") or 0),
                "note": item.get("note", ""),
            }
        )
    return records


def _ok(data: dict) -> dict:
    return {"ok": True, "data": data}


def _err(error_code: str, error_msg: str) -> dict:
    return {"ok": False, "error": {"error_code": str(error_code), "error_msg": error_msg or ""}}


def fetch_watchlist(context=None, page=None) -> dict:
    data = get_stock_watchlist_via_browser(context=context, page=page)
    if data.get("error_code") != "0":
        error_msg = data.get("error_msg") or ""
        msg = error_msg
        if _looks_like_not_logged_in(error_msg):
            msg = f"{error_msg} | 请先在已开启远程调试的 Chrome 中登录 https://tzzb.10jqka.com.cn/ 后重试"
        return _err(data.get("error_code", "-1"), msg)
    stocks = parse_stock_list(data)
    return _ok({"items": stocks})


def fetch_positions(context=None, page=None) -> dict:
    data = get_stock_positions_via_browser(context=context, page=page)
    if data.get("error_code") != "0":
        error_msg = data.get("error_msg") or ""
        msg = error_msg
        if _looks_like_not_logged_in(error_msg):
            msg = f"{error_msg} | 请先在已开启远程调试的 Chrome 中登录 https://tzzb.10jqka.com.cn/ 后重试"
        return _err(data.get("error_code", "-1"), msg)
    positions, overview = parse_positions(data)
    return _ok({"overview": overview, "items": positions})


def fetch_trade_records(context=None, page=None) -> dict:
    try:
        raw_records = get_trade_records_via_browser(context=context, page=page)
    except RuntimeError as e:
        return _err("-1", str(e))
    if not raw_records:
        if context is not None and page is not None:
            userid = get_userid(context, page)
            if not userid:
                return _err("-1", "未检测到登录态，请先在 Chrome 中登录 https://tzzb.10jqka.com.cn/ 后重试")
            return _ok({"items": []})

        try:
            cookies = extract_cookies()
        except RuntimeError as e:
            return _err("-1", str(e))

        if not cookies.get("userid"):
            return _err("-1", "未检测到登录态，请先在 Chrome 中登录 https://tzzb.10jqka.com.cn/ 后重试")

        return _ok({"items": []})

    records = parse_trade_records(raw_records)
    return _ok({"items": records})


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="同花顺投资账本数据解析")
    parser.add_argument("--type", "-t", choices=["all", "watchlist", "positions", "trades"],
                        default="all", help="数据类型：all=全部, watchlist=自选股, positions=持仓, trades=交易记录")
    args = parser.parse_args()

    output: dict = {"type": args.type}
    exit_code = 0

    if args.type == "all":
        with cdp_session() as (context, page):
            output["watchlist"] = fetch_watchlist(context=context, page=page)
            if not output["watchlist"].get("ok"):
                exit_code = 1

            output["positions"] = fetch_positions(context=context, page=page)
            if not output["positions"].get("ok"):
                exit_code = 1

            output["trades"] = fetch_trade_records(context=context, page=page)
            if not output["trades"].get("ok"):
                exit_code = 1
    else:
        if args.type == "watchlist":
            output["watchlist"] = fetch_watchlist()
            if not output["watchlist"].get("ok"):
                exit_code = 1
        if args.type == "positions":
            output["positions"] = fetch_positions()
            if not output["positions"].get("ok"):
                exit_code = 1
        if args.type == "trades":
            output["trades"] = fetch_trade_records()
            if not output["trades"].get("ok"):
                exit_code = 1

    print(json.dumps(output, ensure_ascii=False))
    raise SystemExit(exit_code)
