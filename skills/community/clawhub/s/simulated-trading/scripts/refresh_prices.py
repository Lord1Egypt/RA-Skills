#!/usr/bin/env python3
"""模拟交易系统 - 从东方财富妙想API刷新持仓标的实时行情"""

import sys
import json
import uuid
import re
import urllib.request
import urllib.error
import os
from db import get_conn, init_db, output_json, output_error

# 妙想数据 API（优先使用，更稳定）
MX_API_URL = "https://ai-saas.eastmoney.com/proxy/b/mcp/tool/searchData"


def _load_em_api_key():
    """加载 EM_API_KEY，优先环境变量，回退读取 ~/.bashrc"""
    key = os.environ.get("EM_API_KEY", "")
    if key:
        return key
    # 尝试从 bashrc 读取
    bashrc = os.path.expanduser("~/.bashrc")
    try:
        with open(bashrc) as f:
            for line in f:
                m = re.match(r'export\s+EM_API_KEY\s*=\s*"(.+)"', line.strip())
                if m:
                    return m.group(1)
    except Exception:
        pass
    return ""


EM_API_KEY = _load_em_api_key()

# 旧版东方财富直接 API 作为回退
EASTMONEY_API = "https://push2.eastmoney.com/api/qt/stock/get"


def _extract_symbol_from_name(name_str):
    """从实体名称提取代码，如 '国泰中证全指通信设备ETF(515880.SH)' -> '515880'"""
    m = re.search(r'\((\d+)\.', str(name_str))
    return m.group(1) if m else None


def _parse_price_value(raw):
    """解析价格值，去除单位后缀（如 元、%）"""
    if raw is None:
        return None
    s = str(raw).replace("元", "").replace("%", "").replace(",", "").strip()
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def _extract_dto_list(data):
    """从API响应中提取 dataTableDTOList"""
    if not isinstance(data, dict):
        return None
    search = data.get("data", {}).get("searchDataResultDTO", {})
    dto_list = search.get("dataTableDTOList")
    if dto_list:
        return dto_list
    dto_list = data.get("dataTableDTOList")
    if dto_list:
        return dto_list
    return data.get("dataTableDTOList")


def _call_mx_api(symbols):
    """通过妙想API批量查询实时价格，返回 {symbol: price}"""
    if not EM_API_KEY:
        return {}, "EM_API_KEY 未设置"

    symbols_str = "、".join(symbols)
    query = f"查询{symbols_str}的最新价"
    body = {
        "query": query,
        "toolContext": {
            "callId": f"call_{uuid.uuid4().hex[:8]}",
            "userInfo": {"userId": f"user_{uuid.uuid4().hex[:8]}"},
        },
    }

    try:
        req = urllib.request.Request(
            MX_API_URL,
            data=json.dumps(body).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "em_api_key": EM_API_KEY,
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {}, f"妙想API请求失败: {e}"

    dto_list = _extract_dto_list(data)
    if not dto_list:
        return {}, "妙想API返回无数据"

    results = {}

    for dto in dto_list:
        table = dto.get("table", {})
        if not isinstance(table, dict):
            continue

        entity_name = str(dto.get("entityName", ""))
        order = dto.get("indicatorOrder", [])

        if "最新价" in entity_name:
            # 批量查询格式: entityName="最新价", indicatorOrder=各标的名称
            for key in order:
                key_str = str(key)
                sym = _extract_symbol_from_name(key_str)
                if not sym:
                    continue
                values = table.get(key_str, [])
                raw = values[0] if isinstance(values, list) and values else values
                p = _parse_price_value(raw)
                if p is not None:
                    results[sym] = p
        else:
            # 单标的格式: entityName 含标的代码, table 中 key=指标名
            sym = _extract_symbol_from_name(entity_name)
            if not sym:
                continue
            for key in order:
                key_str = str(key)
                values = table.get(key_str, [])
                if not isinstance(values, list):
                    values = [values]
                if len(values) > 0:
                    p = _parse_price_value(values[0])
                    if p is not None:
                        results[sym] = p
                        break

    return results, None


def _fetch_single_eastmoney(symbol):
    """从东方财富直接API获取单个标的价格（回退方案）"""
    for prefix in ["1", "0"]:
        secid = f"{prefix}.{symbol}"
        url = f"{EASTMONEY_API}?secid={secid}&fields=f43,f57,f58"
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", "Mozilla/5.0")
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if data.get("rc") == 0 and data.get("data"):
                    d = data["data"]
                    price_raw = d.get("f43")
                    name = d.get("f58", "")
                    if price_raw is not None:
                        return price_raw / 1000, name
        except Exception:
            continue
    return None, None


def fetch_prices(symbols):
    """
    获取一组标的的实时价格。
    优先走妙想API，失败则逐一下降直连API。
    返回 ({symbol: {"price": float, "name": str}}, [failed_symbols])
    """
    results = {}
    failed = []

    # 步骤1: 批量走妙想API
    if EM_API_KEY:
        mx_prices, mx_err = _call_mx_api(symbols)
        if not mx_err:
            for sym in symbols:
                if sym in mx_prices:
                    results[sym] = {"price": mx_prices[sym], "name": ""}
                else:
                    failed.append(sym)
        else:
            failed = list(symbols)
    else:
        failed = list(symbols)

    # 步骤2: 失败的逐个走直连API
    still_failed = []
    for sym in failed:
        price, name = _fetch_single_eastmoney(sym)
        if price is not None:
            results[sym] = {"price": price, "name": name}
        else:
            still_failed.append(sym)

    return results, still_failed


def _update_db_prices(conn, prices_data):
    """将价格写入 market_prices 表，返回结果列表"""
    results = []
    for symbol, info in prices_data.items():
        price = info["price"]
        name = info["name"]
        existing = conn.execute(
            "SELECT * FROM market_prices WHERE symbol=?", (symbol,)
        ).fetchone()
        old_price = existing["price"] if existing else None

        if existing:
            conn.execute(
                """UPDATE market_prices
                   SET price=?, name=?, updated_at=datetime('now','localtime')
                   WHERE symbol=?""",
                (price, name if name else existing["name"], symbol),
            )
        else:
            conn.execute(
                "INSERT INTO market_prices (symbol,name,price) VALUES (?,?,?)",
                (symbol, name if name else symbol, price),
            )

        change_pct = None
        if old_price and old_price > 0:
            change_pct = round((price - old_price) / old_price * 100, 2)

        results.append({
            "symbol": symbol,
            "success": True,
            "name": name if name else symbol,
            "price": round(price, 3),
            "old_price": old_price,
            "change_pct": change_pct,
        })
    return results


def refresh_portfolio_prices(portfolio_id):
    """刷新指定组合所有持仓的实时价格"""
    conn = get_conn()
    p = conn.execute("SELECT * FROM portfolios WHERE id=?", (portfolio_id,)).fetchone()
    if not p:
        conn.close()
        output_error(f"组合不存在: {portfolio_id}")

    holdings = conn.execute(
        "SELECT DISTINCT symbol FROM holdings WHERE portfolio_id=? AND quantity>0",
        (portfolio_id,),
    ).fetchall()

    if not holdings:
        conn.close()
        return {"status": "ok", "refreshed": [], "count": 0, "message": "无持仓"}

    symbols = [h["symbol"] for h in holdings]
    prices, failed = fetch_prices(symbols)

    results = _update_db_prices(conn, prices)
    for sym in failed:
        results.append({
            "symbol": sym,
            "success": False,
            "error": "无法获取实时价格（妙想API和直连API均失败）",
        })

    conn.commit()
    conn.close()

    return {
        "status": "ok",
        "refreshed": results,
        "count": len(results),
        "portfolio_id": portfolio_id,
        "failed_count": len(failed),
    }


def main():
    if len(sys.argv) < 3:
        output_error(
            "用法: refresh_prices.py <action> [args...]\n"
            "  portfolio <portfolio_id>  刷新组合持仓的实时价格\n"
            "  symbols <sym1,sym2,...>   刷新指定标的的实时价格"
        )

    init_db()
    action = sys.argv[1]

    if action == "portfolio":
        result = refresh_portfolio_prices(sys.argv[2])
        output_json(result)
    elif action == "symbols":
        symbols = [s.strip() for s in sys.argv[2].split(",") if s.strip()]
        if not symbols:
            output_error("请提供至少一个标的代码")

        prices, failed = fetch_prices(symbols)

        conn = get_conn()
        results = _update_db_prices(conn, prices)
        for sym in failed:
            results.append({
                "symbol": sym,
                "success": False,
                "error": "无法获取实时价格",
            })

        conn.commit()
        conn.close()
        output_json({"status": "ok", "refreshed": results, "count": len(results)})
    else:
        output_error(f"未知操作: {action}")


if __name__ == "__main__":
    main()
