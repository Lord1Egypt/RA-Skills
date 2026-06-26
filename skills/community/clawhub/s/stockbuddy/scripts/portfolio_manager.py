#!/usr/bin/env python3
"""
多市场股票持仓/关注池管理工具 - 基于 SQLite 管理关注股票、持仓并批量分析。

用法:
    python3 portfolio_manager.py list
    python3 portfolio_manager.py add <代码> --price <买入价> --shares <数量> [--date <日期>] [--note <备注>] [--account <账户名或ID>]
    python3 portfolio_manager.py remove <代码>
    python3 portfolio_manager.py update <代码> [--price <价格>] [--shares <数量>] [--note <备注>] [--account <账户名或ID>]
    python3 portfolio_manager.py analyze [--output <输出文件>]
    python3 portfolio_manager.py account-list
    python3 portfolio_manager.py account-upsert <账户名> [--market <市场>] [--currency <币种>] [--cash <总现金>] [--available-cash <可用现金>] [--note <备注>]
    python3 portfolio_manager.py rule-set <代码> [--lot-size <每手股数>] [--tick-size <最小价位>] [--odd-lot]
    python3 portfolio_manager.py watch-list
    python3 portfolio_manager.py watch-add <代码>
    python3 portfolio_manager.py watch-remove <代码>

数据默认保存在: ~/.stockbuddy/stockbuddy.db
"""

import sys
import json
import argparse
import os
import time
from collections import defaultdict
from datetime import datetime

try:
    from db import (
        DB_PATH,
        get_account,
        get_watchlist_item,
        init_db,
        list_accounts as db_list_accounts,
        list_positions as db_list_positions,
        list_watchlist as db_list_watchlist,
        remove_position as db_remove_position,
        set_watch_status,
        update_position_fields,
        upsert_account,
        upsert_position,
        upsert_stock_rule,
        upsert_watchlist_item,
    )
    from analyze_stock import fetch_tencent_quote, normalize_stock_code, analyze_stock
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from db import (
        DB_PATH,
        get_account,
        get_watchlist_item,
        init_db,
        list_accounts as db_list_accounts,
        list_positions as db_list_positions,
        list_watchlist as db_list_watchlist,
        remove_position as db_remove_position,
        set_watch_status,
        update_position_fields,
        upsert_account,
        upsert_position,
        upsert_stock_rule,
        upsert_watchlist_item,
    )
    from analyze_stock import fetch_tencent_quote, normalize_stock_code, analyze_stock


def normalize_code(code: str) -> str:
    return normalize_stock_code(code)["code"]


def resolve_account(account_ref: str | None):
    if not account_ref:
        return None
    account = get_account(account_ref)
    if not account:
        raise ValueError(f"账户不存在: {account_ref}")
    return account


def ensure_watch_item(code: str, watched: bool = False) -> dict:
    stock = normalize_stock_code(code)
    quote = fetch_tencent_quote(stock["code"])
    name = quote.get("name") if quote else None
    return upsert_watchlist_item(
        code=stock["code"],
        market=stock["market"],
        tencent_symbol=stock["tencent_symbol"],
        name=name,
        exchange=quote.get("exchange", stock.get("exchange")) if quote else stock.get("exchange"),
        currency=quote.get("currency") if quote else None,
        last_price=quote.get("price") if quote else None,
        pe=quote.get("pe") if quote else None,
        pb=quote.get("pb") if quote else None,
        market_cap=quote.get("market_cap") if quote else None,
        week52_high=quote.get("52w_high") if quote else None,
        week52_low=quote.get("52w_low") if quote else None,
        quote_time=quote.get("timestamp") if quote else None,
        is_watched=watched,
        meta=quote or stock,
    )


def derive_execution_constraints(position: dict, current_price: float | None = None) -> dict:
    shares = int(position.get("shares") or 0)
    lot_size = position.get("lot_size")
    allows_odd_lot = bool(position.get("allows_odd_lot") or False)
    if lot_size is None or lot_size <= 0:
        whole_lots = None
        remainder = None
        can_partial_sell = None
        sellable_min_unit = 1 if allows_odd_lot else None
    else:
        whole_lots = shares // lot_size
        remainder = shares % lot_size
        can_partial_sell = allows_odd_lot or whole_lots >= 2 or remainder > 0
        sellable_min_unit = 1 if allows_odd_lot else lot_size

    estimated_cash_if_sell_all = round(shares * current_price, 2) if current_price is not None else None
    return {
        "lot_size": lot_size,
        "allows_odd_lot": allows_odd_lot,
        "sellable_min_unit": sellable_min_unit,
        "whole_lots": whole_lots,
        "odd_lot_remainder": remainder,
        "can_partial_sell": can_partial_sell,
        "estimated_cash_if_sell_all": estimated_cash_if_sell_all,
    }


def derive_position_snapshot(position: dict, analysis: dict) -> dict:
    current_price = analysis.get("current_price")
    buy_price = position.get("buy_price")
    shares = int(position.get("shares") or 0)
    cost = round((buy_price or 0) * shares, 2)
    market_value = round((current_price or 0) * shares, 2) if current_price is not None else None
    pnl = round((current_price - buy_price) * shares, 2) if current_price is not None and buy_price is not None else None
    pnl_pct = round((current_price - buy_price) / buy_price * 100, 2) if current_price is not None and buy_price not in (None, 0) else None
    execution = derive_execution_constraints(position, current_price)
    return {
        "buy_price": buy_price,
        "shares": shares,
        "buy_date": position.get("buy_date"),
        "cost": cost,
        "market_value": market_value,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
        "note": position.get("note", ""),
        "currency": position.get("currency"),
        "market": position.get("market"),
        "account": {
            "id": position.get("account_id"),
            "name": position.get("account_name"),
            "market": position.get("account_market"),
            "currency": position.get("account_currency"),
            "cash_balance": position.get("account_cash_balance"),
            "available_cash": position.get("account_available_cash"),
        },
        "execution_constraints": execution,
    }


# ─────────────────────────────────────────────
#  持仓管理
# ─────────────────────────────────────────────

def list_positions():
    init_db()
    positions = db_list_positions()
    if not positions:
        print(json.dumps({"message": "持仓为空", "positions": []}, ensure_ascii=False, indent=2))
        return
    print(json.dumps({
        "total_positions": len(positions),
        "positions": positions,
        "portfolio_db": str(DB_PATH),
        "updated_at": datetime.now().isoformat(),
    }, ensure_ascii=False, indent=2))


def add_position(code: str, price: float, shares: int, date: str = None, note: str = "", account_ref: str = None):
    init_db()
    normalized = normalize_stock_code(code)
    existing = next((p for p in db_list_positions() if p["code"] == normalized["code"]), None)
    if existing:
        print(json.dumps({"error": f"{normalized['code']} 已在持仓中，请使用 update 命令更新"}, ensure_ascii=False))
        return

    account = resolve_account(account_ref)
    watch = ensure_watch_item(normalized["code"], watched=True)
    position = upsert_position(
        code=normalized["code"],
        market=normalized["market"],
        tencent_symbol=normalized["tencent_symbol"],
        buy_price=price,
        shares=shares,
        buy_date=date or datetime.now().strftime("%Y-%m-%d"),
        note=note,
        account_id=account.get("id") if account else None,
        name=watch.get("name"),
        currency=watch.get("currency"),
        meta=json.loads(watch["meta_json"]) if watch.get("meta_json") else None,
    )
    print(json.dumps({"message": f"已添加 {normalized['code']}", "position": position}, ensure_ascii=False, indent=2))


def remove_position(code: str):
    init_db()
    normalized_code = normalize_code(code)
    removed = db_remove_position(normalized_code)
    if not removed:
        print(json.dumps({"error": f"{normalized_code} 不在持仓中"}, ensure_ascii=False))
        return
    print(json.dumps({"message": f"已移除 {normalized_code}"}, ensure_ascii=False, indent=2))


def update_position(code: str, price: float = None, shares: int = None, note: str = None, account_ref: str = None):
    init_db()
    normalized_code = normalize_code(code)
    account = resolve_account(account_ref) if account_ref else None
    position = update_position_fields(normalized_code, price=price, shares=shares, note=note, account_id=account.get("id") if account else None)
    if not position:
        print(json.dumps({"error": f"{normalized_code} 不在持仓中"}, ensure_ascii=False))
        return
    print(json.dumps({"message": f"已更新 {normalized_code}", "position": position}, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────
#  账户与交易规则管理
# ─────────────────────────────────────────────

def list_accounts():
    init_db()
    accounts = db_list_accounts()
    print(json.dumps({
        "total_accounts": len(accounts),
        "accounts": accounts,
        "portfolio_db": str(DB_PATH),
        "updated_at": datetime.now().isoformat(),
    }, ensure_ascii=False, indent=2))


def save_account(name: str, market: str = None, currency: str = None, cash: float = None, available_cash: float = None, note: str = ""):
    init_db()
    account = upsert_account(
        name=name,
        market=market,
        currency=currency,
        cash_balance=cash,
        available_cash=available_cash,
        note=note,
    )
    print(json.dumps({"message": f"已保存账户 {name}", "account": account}, ensure_ascii=False, indent=2))


def set_rule(code: str, lot_size: int = None, tick_size: float = None, odd_lot: bool = False):
    init_db()
    normalized_code = normalize_code(code)
    ensure_watch_item(normalized_code, watched=False)
    rule = upsert_stock_rule(code=normalized_code, lot_size=lot_size, tick_size=tick_size, allows_odd_lot=odd_lot)
    print(json.dumps({"message": f"已设置 {normalized_code} 的交易规则", "rule": rule}, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────
#  关注池管理
# ─────────────────────────────────────────────

def list_watchlist():
    init_db()
    items = db_list_watchlist(only_watched=True)
    print(json.dumps({
        "total_watchlist": len(items),
        "watchlist": items,
        "portfolio_db": str(DB_PATH),
        "updated_at": datetime.now().isoformat(),
    }, ensure_ascii=False, indent=2))


def add_watch(code: str):
    init_db()
    watch = ensure_watch_item(code, watched=True)
    print(json.dumps({"message": f"已关注 {watch['code']}", "watch": watch}, ensure_ascii=False, indent=2))


def remove_watch(code: str):
    init_db()
    normalized_code = normalize_code(code)
    watch = set_watch_status(normalized_code, False)
    if not watch:
        print(json.dumps({"error": f"{normalized_code} 不在关注池中"}, ensure_ascii=False))
        return
    print(json.dumps({"message": f"已取消关注 {normalized_code}", "watch": watch}, ensure_ascii=False, indent=2))


# ─────────────────────────────────────────────
#  批量分析
# ─────────────────────────────────────────────

def analyze_portfolio(output_file: str = None):
    init_db()
    positions = db_list_positions()
    if not positions:
        print(json.dumps({"message": "持仓为空，无法分析"}, ensure_ascii=False, indent=2))
        return

    results = []
    account_totals = defaultdict(lambda: {"cost": 0.0, "market_value": 0.0})
    market_currency_totals = defaultdict(lambda: {"cost": 0.0, "market_value": 0.0})

    for i, pos in enumerate(positions):
        code = pos["code"]
        print(f"正在分析 {code} ({i+1}/{len(positions)})...", file=sys.stderr)
        analysis = analyze_stock(code)
        analysis["portfolio_info"] = derive_position_snapshot(pos, analysis)
        results.append(analysis)

        snapshot = analysis["portfolio_info"]
        market_value = snapshot.get("market_value") or 0.0
        cost = snapshot.get("cost") or 0.0

        account_name = snapshot.get("account", {}).get("name") or "未分配账户"
        account_totals[account_name]["cost"] += cost
        account_totals[account_name]["market_value"] += market_value

        mc_key = f"{snapshot.get('market') or 'UNKNOWN'}:{snapshot.get('currency') or 'UNKNOWN'}"
        market_currency_totals[mc_key]["cost"] += cost
        market_currency_totals[mc_key]["market_value"] += market_value

        if i < len(positions) - 1 and not analysis.get("_from_cache"):
            time.sleep(2)

    total_cost = sum(r.get("portfolio_info", {}).get("cost", 0) or 0 for r in results)
    total_value = sum(r.get("portfolio_info", {}).get("market_value", 0) or 0 for r in results)
    total_pnl = total_value - total_cost

    for analysis in results:
        snapshot = analysis.get("portfolio_info", {})
        market_value = snapshot.get("market_value") or 0.0
        account = snapshot.get("account") or {}
        account_name = account.get("name") or "未分配账户"
        account_total_value = account_totals[account_name]["market_value"]
        snapshot["position_weight_of_portfolio_pct"] = round(market_value / total_value * 100, 2) if total_value > 0 else None
        snapshot["position_weight_of_account_pct"] = round(market_value / account_total_value * 100, 2) if account_total_value > 0 else None

    summary = {
        "analysis_time": datetime.now().isoformat(),
        "total_positions": len(results),
        "total_cost": round(total_cost, 2),
        "total_market_value": round(total_value, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl / total_cost * 100, 2) if total_cost > 0 else 0,
        "accounts": [
            {
                "name": name,
                "total_cost": round(v["cost"], 2),
                "total_market_value": round(v["market_value"], 2),
                "total_pnl": round(v["market_value"] - v["cost"], 2),
            }
            for name, v in sorted(account_totals.items())
        ],
        "market_currency_breakdown": [
            {
                "market_currency": key,
                "total_cost": round(v["cost"], 2),
                "total_market_value": round(v["market_value"], 2),
                "total_pnl": round(v["market_value"] - v["cost"], 2),
            }
            for key, v in sorted(market_currency_totals.items())
        ],
        "positions": results,
    }

    output = json.dumps(summary, ensure_ascii=False, indent=2, default=str)

    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"分析结果已保存至 {output_file}", file=sys.stderr)

    print(output)


def main():
    parser = argparse.ArgumentParser(description="多市场股票持仓/关注池管理工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    subparsers.add_parser("list", help="列出所有持仓")
    subparsers.add_parser("account-list", help="列出账户")

    add_parser = subparsers.add_parser("add", help="添加持仓")
    add_parser.add_argument("code", help="股票代码")
    add_parser.add_argument("--price", type=float, required=True, help="买入价格")
    add_parser.add_argument("--shares", type=int, required=True, help="持有数量")
    add_parser.add_argument("--date", help="买入日期 (YYYY-MM-DD)")
    add_parser.add_argument("--note", default="", help="备注")
    add_parser.add_argument("--account", help="账户名或账户ID")

    rm_parser = subparsers.add_parser("remove", help="移除持仓")
    rm_parser.add_argument("code", help="股票代码")

    up_parser = subparsers.add_parser("update", help="更新持仓")
    up_parser.add_argument("code", help="股票代码")
    up_parser.add_argument("--price", type=float, help="买入价格")
    up_parser.add_argument("--shares", type=int, help="持有数量")
    up_parser.add_argument("--note", help="备注")
    up_parser.add_argument("--account", help="账户名或账户ID")

    analyze_parser = subparsers.add_parser("analyze", help="批量分析持仓")
    analyze_parser.add_argument("--output", help="输出JSON文件")

    account_parser = subparsers.add_parser("account-upsert", help="新增或更新账户")
    account_parser.add_argument("name", help="账户名")
    account_parser.add_argument("--market", help="市场，例如 HK/CN/US")
    account_parser.add_argument("--currency", help="币种，例如 HKD/CNY/USD")
    account_parser.add_argument("--cash", type=float, help="账户总现金")
    account_parser.add_argument("--available-cash", type=float, help="账户可用现金")
    account_parser.add_argument("--note", default="", help="备注")

    rule_parser = subparsers.add_parser("rule-set", help="设置股票交易规则")
    rule_parser.add_argument("code", help="股票代码")
    rule_parser.add_argument("--lot-size", type=int, help="一手股数")
    rule_parser.add_argument("--tick-size", type=float, help="最小价位变动")
    rule_parser.add_argument("--odd-lot", action="store_true", help="允许碎股")

    subparsers.add_parser("watch-list", help="列出关注池")
    watch_add_parser = subparsers.add_parser("watch-add", help="添加关注股票")
    watch_add_parser.add_argument("code", help="股票代码")
    watch_remove_parser = subparsers.add_parser("watch-remove", help="取消关注股票")
    watch_remove_parser.add_argument("code", help="股票代码")

    args = parser.parse_args()

    try:
        if args.command == "list":
            list_positions()
        elif args.command == "add":
            add_position(args.code, args.price, args.shares, args.date, args.note, args.account)
        elif args.command == "remove":
            remove_position(args.code)
        elif args.command == "update":
            update_position(args.code, args.price, args.shares, args.note, args.account)
        elif args.command == "analyze":
            analyze_portfolio(args.output)
        elif args.command == "account-list":
            list_accounts()
        elif args.command == "account-upsert":
            save_account(args.name, args.market, args.currency, args.cash, args.available_cash, args.note)
        elif args.command == "rule-set":
            set_rule(args.code, args.lot_size, args.tick_size, args.odd_lot)
        elif args.command == "watch-list":
            list_watchlist()
        elif args.command == "watch-add":
            add_watch(args.code)
        elif args.command == "watch-remove":
            remove_watch(args.code)
        else:
            parser.print_help()
    except ValueError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
