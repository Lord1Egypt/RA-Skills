#!/usr/bin/env python3
"""
投资跟踪模块

记录买入/卖出、查询持仓、计算收益率、汇总收益。
基础功能纯 Python 标准库；证券代码查询依赖 akshare（联网）。

用法:
    python invest.py --buy "沪深300ETF" 510050 1000 3.50 2026-01-15
    python invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01
    python invest.py --dividend "沪深300ETF" 45.60 2026-02-10
    python invest.py --price 510050 3.62
    python invest.py --portfolio
    python invest.py --return 510050
    python invest.py --summary
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List, Dict
import re

# ==================== 路径配置 ====================

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_DIR = SCRIPT_DIR.parent

# 用户数据目录（独立于 skill 安装目录，不受更新影响）
# ⚠️ 安全：环境变量指向的路径必须落在 ~/.openclaw/workspace/ 下，否则拒绝加载
_HOME_WS = str(Path.home() / ".openclaw" / "workspace")
_RAW_DIR = os.environ.get("LEDGER_DATA_DIR", "~/.openclaw/workspace/data/ledger")
_DATA_DIR_RAW = Path(_RAW_DIR).expanduser().resolve()
if str(_DATA_DIR_RAW).startswith(_HOME_WS):
    DATA_DIR = _DATA_DIR_RAW
else:
    # 环境变量被污染，拒绝加载，防止路径注入
    raise ValueError(f"LEDGER_DATA_DIR must be under {_HOME_WS}, got {_DATA_DIR_RAW}")
LEDGER_FILE = DATA_DIR / "investments.csv"

# 示例数据目录（skill 自带，仅供参考）
EXAMPLE_DATA_DIR = PROJECT_DIR / "data"


# ==================== 文件操作 ====================

def ensure_data_dir():
    """确保数据目录存在"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not LEDGER_FILE.exists():
        LEDGER_FILE.write_text(
            "# 日期,操作,代码,名称,数量,@成本价,成本金额,现价,账户\n"
            "# 格式说明:\n"
            "#   买入: 日期,买入,代码,名称,数量,@单价,金额,现价,账户\n"
            "#   卖出: 日期,卖出,代码,名称,数量,@单价,金额,现价,账户\n"
            "#   分红: 日期,分红,代码,名称,金额,,现价,账户\n"
            "# === 交易记录 ===\n\n",
            encoding="utf-8",
        )


def load_ledger():
    """加载投资账本，返回结构化交易列表"""
    ensure_data_dir()
    entries = []
    for line in LEDGER_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        entry = parse_csv_line(line)
        if entry:
            entries.append(entry)
    return entries


# LEDGER_CSV / _ALLOWED_WRITE_PREFIX 已移除（不再支持跨文件写入主账本）
# 安全：只允许写入 workspace 目录，防止路径注入攻击
_ALLOWED_WRITE_PREFIX = str(Path.home() / ".openclaw" / "workspace")


def _safe_ledger_path(path: Path) -> Optional[Path]:
    """验证路径在允许范围内，返回安全路径或 None（防止路径注入）"""
    try:
        resolved = path.resolve()
        if str(resolved).startswith(_ALLOWED_WRITE_PREFIX):
            return resolved
    except Exception:
        pass
    return None


# ==================== 输入校验（防注入/防畸形数据）====================

_STRIP_ANSI = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
_MAX_AMOUNT = 1_000_000_000  # 单笔交易上限 10 亿


def _sanitize(text: str) -> str:
    """去除终端控制字符，防止 ANSI 转义注入输出"""
    return _STRIP_ANSI.sub("", text)


def _validate_code(code: str) -> bool:
    """代码必须是 6 位数字"""
    return bool(re.fullmatch(r"\d{6}", str(code)))


def _validate_amount(amount: float, source: str = "金额") -> float:
    if not isinstance(amount, (int, float)) or amount <= 0 or amount > _MAX_AMOUNT:
        raise ValueError(f"{source}必须为正数且不超过 ¥{_MAX_AMOUNT:,.0f}")
    return float(amount)


def _validate_shares(shares: float) -> float:
    val = float(shares)
    if val <= 0:
        raise ValueError("份额必须为正数")
    return val


def _validate_price(price: float) -> float:
    val = float(price)
    if val <= 0 or val > _MAX_AMOUNT:
        raise ValueError(f"单价必须为正数且不超过 ¥{_MAX_AMOUNT:,.0f}")
    return val


def _safe_print(label, value):
    """安全打印：去掉 ANSI 和换行符，防止终端污染"""
    safe = _sanitize(str(value)).replace("\n", " ").replace("\r", "")
    print(f"   {label} {safe}")


def append_ledger(text):
    """追加一行到投资账本（路径已由 DATA_DIR 白名单保证安全）"""
    ensure_data_dir()
    safe_path = _safe_ledger_path(LEDGER_FILE)
    if not safe_path:
        raise ValueError(f"不允许写入 Ledger 路径: {LEDGER_FILE}")
    with open(safe_path, "a", encoding="utf-8") as f:
        f.write(_sanitize(text) + "\n")


def append_ledger_with_price(text, price):
    """追加一行到投资账本，同时写入现价"""
    ensure_data_dir()
    safe_path = _safe_ledger_path(LEDGER_FILE)
    if not safe_path:
        raise ValueError(f"不允许写入 Ledger 路径: {LEDGER_FILE}")
    with open(safe_path, "a", encoding="utf-8") as f:
        f.write(_sanitize(text) + f",{price:.4f}\n")


# append_to_main_ledger 已移除。
# 投资交易仅写入 investments.csv，不再支持自动同步到主账本。
# 如需将投资记录反映在日常账本中，请使用 simple-ledger 的记账功能手动记录。


def confirm_buy(name, code, shares, price, amount, account, dt):
    """打印买入摘要并要求交互式确认，返回 True/False。"""
    print("\n📋 买入确认：")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name}（{code}）")
    _safe_print("🔢", f"{shares}股 × ¥{price:.2f} = ¥{amount:,.2f}")
    _safe_print("💳", account)
    _safe_print("💸", f"支出 ¥{amount:,.2f} 将从「{account}」扣减")
    if not sys.stdin.isatty():
        print("❌ 买入操作需要交互式 Y/N 确认；非交互环境不会写入投资账本")
        return False
    try:
        ans = input("\n确认买入? (Y/N): ").strip().lower()
        return ans in ("y", "yes")
    except (EOFError, IOError, KeyboardInterrupt):
        return False


def confirm_sell(name, code, shares, price, amount, account, dt):
    """打印卖出摘要并要求交互式确认，返回 True/False。"""
    print("\n📋 卖出确认：")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name}（{code}）")
    _safe_print("🔢", f"{shares}股 × ¥{price:.2f} = ¥{amount:,.2f}")
    _safe_print("💳", account)
    _safe_print("💰", f"收入 ¥{amount:,.2f} 将进入「{account}」")
    if not sys.stdin.isatty():
        print("❌ 卖出操作需要交互式 Y/N 确认；非交互环境不会写入投资账本")
        return False
    try:
        ans = input("\n确认卖出? (Y/N): ").strip().lower()
        return ans in ("y", "yes")
    except (EOFError, IOError, KeyboardInterrupt):
        return False


def load_prices():
    """从 CSV 中提取现价（不再依赖 prices.json）"""
    entries = load_ledger()
    prices = {}
    for e in entries:
        code = e.get("code", "")
        cur = e.get("current_price", 0)
        if code and cur > 0:
            prices[code] = cur
    return prices


def auto_refresh_enabled() -> bool:
    """检查用户是否开启了自动联网刷新（通过 .env 配置文件）"""
    env_file = DATA_DIR / ".env"
    if not env_file.exists():
        return False
    try:
        content = env_file.read_text(encoding="utf-8")
        return "AUTO_REFRESH=1" in content or "AUTO_REFRESH=true" in content
    except Exception:
        return False


def save_prices(prices):
    """更新 CSV 中的现价列"""
    ensure_data_dir()
    safe_path = _safe_ledger_path(LEDGER_FILE)
    if not safe_path:
        raise ValueError(f"不允许写入 Ledger 路径: {LEDGER_FILE}")
    lines = safe_path.read_text(encoding="utf-8").splitlines()
    new_lines = []
    for line in lines:
        if not line.strip() or line.strip().startswith("#"):
            new_lines.append(line)
            continue
        parts = line.split(",")
        if len(parts) >= 9:
            code = parts[2].strip()
            if code in prices:
                parts[7] = f"{prices[code]:.4f}"
            new_lines.append(",".join(parts))
        else:
            new_lines.append(line)
    safe_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")


def set_price(code, price):
    """设置某只证券的当前价格"""
    if not _validate_code(code):
        raise ValueError(f"证券代码必须为6位数字，当前：{code}")
    val_price = _validate_price(price)
    prices = load_prices()
    prices[code] = val_price
    save_prices(prices)
    return prices


def do_cost(code: str, new_price: float):
    """修改指定证券最近一笔买入的成本单价（及对应金额）"""
    if not _validate_code(code):
        raise ValueError(f"证券代码必须为6位数字：{code}")
    val_price = _validate_price(new_price)
    entries = load_ledger()
    # 找到该代码最近一笔买入记录（倒序）
    buy_indices = [i for i, e in enumerate(entries) if e["code"] == code and e["action"] == "买入"]
    if not buy_indices:
        print(f"❌ 未找到 {code} 的买入记录")
        return
    last_idx = buy_indices[-1]
    old_price = entries[last_idx]["price"]
    shares = entries[last_idx]["shares"]
    entries[last_idx]["price"] = val_price
    entries[last_idx]["amount"] = round(shares * val_price, 2)

    safe_ledger = _safe_ledger_path(LEDGER_FILE)
    if not safe_ledger:
        raise ValueError(f"不允许写入 Ledger 路径: {LEDGER_FILE}")
    # 加载当前现价
    prices = load_prices()
    safe_lines = []
    for e in entries:
        name_s = _sanitize(e["name"])
        cur = prices.get(e["code"], 0)
        if e["action"] == "买入":
            safe_lines.append(f"{e['date']},买入,{e['code']},{name_s},{e['shares']},@{e['price']},{e['amount']},{cur:.4f},{e['account']}")
        elif e["action"] == "卖出":
            safe_lines.append(f"{e['date']},卖出,{e['code']},{name_s},{e['shares']},@{e['price']},{e['amount']},{cur:.4f},{e['account']}")
        elif e["action"] == "分红":
            safe_lines.append(f"{e['date']},分红,{e['code']},{name_s},{e['amount']},,{cur:.4f},{e['account']}")
    header = "# 投资账本\n# 格式：日期,操作,代码,名称,数量,@成本价,成本金额,现价,账户\n# 操作：买入 / 卖出 / 分红\n# === 交易记录 ===\n\n"
    safe_ledger.write_text(header + "\n".join(safe_lines) + "\n", encoding="utf-8")
    print(f"✅ 已修改 {code} 最近买入单价：¥{old_price:.3f} → ¥{val_price:.3f}")
    _safe_print("数量", f"{shares}股，总成本：¥{entries[last_idx]['amount']:,.2f}")


# ==================== 实时行情 ====================

def fetch_realtime_price(code: str) -> dict:
    """
    通过 akshare 新浪接口获取单只证券实时/收盘行情。
    支持股票（sh/sz前缀）和ETF。
    返回 {"code": str, "name": str, "price": float, "change_pct": float, "date": str} 或 None。
    """
    # 判断交易所前缀
    if code.startswith("6"):
        prefix = f"sh{code}"
    elif code.startswith("0") or code.startswith("3"):
        prefix = f"sz{code}"
    elif code.isdigit():
        prefix = f"sh{code}"
    else:
        prefix = code

    try:
        import akshare as ak
        import inspect

        # 方法1: option_sse_underlying_spot_price_sina（实时行情，含买卖盘）
        try:
            df = ak.option_sse_underlying_spot_price_sina(symbol=prefix)
            if df is not None and not df.empty:
                data = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
                price_str = data.get("最近成交价")
                if price_str and float(price_str) > 0:
                    prev_close = float(data.get("昨日收盘价", 0))
                    name = data.get("证券简称", "")
                    current = float(price_str)
                    change_pct = ((current - prev_close) / prev_close * 100) if prev_close > 0 else 0
                    trade_date = data.get("行情日期", "")
                    return {
                        "code": code,
                        "name": name,
                        "price": current,
                        "change_pct": change_pct,
                        "date": trade_date,
                    }
        except Exception:
            pass

        # 方法2: stock_intraday_sina（分时数据，取最后一根）
        try:
            today = date.today().strftime("%Y%m%d")
            df = ak.stock_intraday_sina(symbol=prefix, date=today)
            if df is not None and not df.empty:
                last = df.iloc[-1]
                current = float(last["price"])
                name = last["name"]
                prev_price = float(last["prev_price"])
                change_pct = ((current - prev_price) / prev_price * 100) if prev_price > 0 else 0
                return {
                    "code": code,
                    "name": name,
                    "price": current,
                    "change_pct": change_pct,
                    "date": str(date.today()),
                }
        except Exception:
            pass

        # 方法3: fund_etf_hist_sina（ETF历史行情，取最新一条）
        try:
            df = ak.fund_etf_hist_sina(symbol=prefix)
            if df is not None and not df.empty:
                last = df.iloc[-1]
                return {
                    "code": code,
                    "name": "",
                    "price": float(last["close"]),
                    "change_pct": 0,
                    "date": str(last["date"]),
                }
        except Exception:
            pass

        # 方法4: 东方财富场外基金净值（适用于非ETF基金，如混合型、股票型基金）
        try:
            df = ak.fund_open_fund_info_em(symbol=code, indicator="单位净值走势", period="近1月")
            if df is not None and not df.empty:
                last = df.iloc[-1]
                raw_chg = last.get("日增长率", "")
                change_pct = 0.0
                if raw_chg is not None and str(raw_chg).strip():
                    change_pct = float(str(raw_chg).rstrip("%"))
                return {
                    "code": code,
                    "name": "",
                    "price": float(last["单位净值"]),
                    "change_pct": change_pct,
                    "date": str(last["净值日期"]),
                }
        except Exception:
            pass

    except ImportError:
        print("⚠️ akshare 未安装，无法获取实时行情")
        return None
    except Exception as e:
        print(f"⚠️ 获取 {code} 行情失败: {e}")
        return None

    return None


def _network_denied(action: str):
    print(f"❌ {action} 需要联网；请在命令中显式添加 --allow-network 后再执行")
    print("   隐私提示：联网查询会把证券代码/名称发送到第三方行情接口，但不会发送账本、余额或交易记录。")


def do_refresh(entries: list, allow_network: bool = False):
    """刷新所有持仓的实时/收盘价格（需显式允许联网）"""
    if not allow_network:
        _network_denied("刷新实时行情")
        return
    holdings = compute_holdings(entries)
    active = {k: v for k, v in holdings.items() if v["total_shares"] > 0}
    if not active:
        print("📭 当前无持仓，无需刷新")
        return

    prices = load_prices()
    updated = 0
    failed = 0
    results = []

    print(f"🔄 正在刷新 {len(active)} 只证券的行情...\n")

    for code, info in active.items():
        name = info["name"]
        result = fetch_realtime_price(code)
        if result:
            prices[code] = result["price"]
            updated += 1
            arrow = "🟢" if result["change_pct"] >= 0 else "🔴"
            results.append(f"  {arrow} {name}({code})  ¥{result['price']:.2f}  ({result['change_pct']:+.2f}%)  [{result['date']}]")
        else:
            failed += 1
            results.append(f"  ⚪ {name}({code})  获取失败，保留原价 ¥{prices.get(code, 0):.2f}")

    save_prices(prices)

    for r in results:
        print(r)

    print(f"\n✅ 刷新完成：{updated} 成功，{failed} 失败")
    if updated > 0:
        print(f"   💡 使用 --portfolio 或 --summary 查看更新后的收益")


def do_quote(code: str, allow_network: bool = False):
    """查询单只证券的实时行情，支持代码或名称（需显式允许联网）"""
    if not allow_network:
        _network_denied("查询实时行情")
        return
    # 如果是名称（非6位数字），先查找代码
    resolved_code = code.strip()
    resolved_name = ""  # will be updated if code was resolved from name
    if not (resolved_code.isdigit() and len(resolved_code) == 6):
        print(f"🔍 正在联网查询「{resolved_code}」的代码...")
        lookup = auto_lookup_code(resolved_code, allow_network=True)
        if not lookup.get("found"):
            print(f"\n❌ 未找到「{resolved_code}」的代码")
            return
        # 优先用 primary，否则用第一个结果
        primary = lookup.get("primary", {})
        results = lookup.get("results", [])
        chosen = primary if primary else (results[0] if results else {})
        resolved_code = chosen.get("code")
        resolved_name = chosen.get("name", code)
        if not resolved_code:
            print(f"\n❌ 未找到「{code}」的代码")
            return
        print(f"✅ 找到：{resolved_name}（{resolved_code}）\n")

    result = fetch_realtime_price(resolved_code)
    if result:
        arrow = "📈" if result["change_pct"] >= 0 else "📉"
        display_name = result["name"] if result["name"] else resolved_name
        print(f"{arrow} {display_name}({resolved_code})")
        print(f"   最新价: ¥{result['price']:.4f}")
        print(f"   涨跌幅: {result['change_pct']:+.2f}%")
        print(f"   行情日期: {result['date']}")
    else:
        print(f"\n⚠️ 无法获取 {resolved_code} 的行情数据")
        print(f"   提示：请确认代码正确（如 600487 或 025209）")


# ==================== 解析 CSV 行 ====================

def parse_csv_line(line: str) -> dict:
    """
    解析投资账本 CSV 单行，返回结构化字典或 None
    格式: 日期,类型,代码,名称,数量,@单价,金额,账户
    """
    parts = line.split(",")
    if len(parts) < 5:
        return None

    entry = {"raw": line}

    date_str = parts[0].strip()
    action = parts[1].strip()
    code = parts[2].strip()
    name = parts[3].strip()

    entry["date"] = date_str
    entry["action"] = action
    entry["code"] = code
    entry["name"] = name
    entry["current_price"] = 0

    if action in ("买入", "卖出"):
        if len(parts) < 8:
            return None
        # 数量（去掉"股"字）
        shares_str = parts[4].strip().replace("股", "").strip()
        price_str = parts[5].strip().lstrip("@").strip()
        amount_str = parts[6].strip()
        account = parts[8].strip() if len(parts) > 8 else (parts[7].strip() if len(parts) > 7 else "银行卡")

        # 现价列（第8列，index 7）
        cur_price = 0
        try:
            cur_price = float(parts[7].strip()) if len(parts) > 7 else 0
        except (ValueError, IndexError):
            cur_price = 0
        entry["current_price"] = cur_price

        try:
            shares = float(shares_str) if shares_str else 0
            price = float(price_str) if price_str else 0
            amount = float(amount_str) if amount_str else shares * price
        except ValueError:
            return None

        entry["shares"] = shares
        entry["price"] = price
        entry["amount"] = amount
        entry["account"] = account

        if action == "买入":
            entry["cost"] = amount
        else:
            entry["proceeds"] = amount

    elif action == "分红":
        if len(parts) < 5:
            return None
        try:
            amount = float(parts[4].strip())
        except ValueError:
            return None
        # 分红格式：日期,分红,代码,名称,金额,,现价,账户（9列）
        if len(parts) > 7:
            try:
                entry["current_price"] = float(parts[7].strip())
            except (ValueError, IndexError):
                entry["current_price"] = 0
        account = parts[8].strip() if len(parts) > 8 else (parts[7].strip() if len(parts) > 7 else "银行卡")
        entry["amount"] = amount
        entry["account"] = account

    else:
        return None

    return entry


# ==================== 交易操作 ====================

def do_buy(name, code, shares, price, dt, account):
    """记录买入"""
    if not _validate_code(code):
        raise ValueError(f"证券代码必须为6位数字：{code}")
    val_shares = _validate_shares(shares)
    val_price = _validate_price(price)
    amount = val_shares * val_price
    _validate_amount(amount)
    # 二次确认
    if not confirm_buy(name, code, val_shares, val_price, amount, account, dt):
        print("❌ 已取消买入")
        return
    append_ledger_with_price(f"{dt},买入,{code},{_sanitize(name)},{val_shares},@{val_price:.2f},{amount:.2f},{account}", val_price)
    # 投资交易仅写入 investments.csv，不同步到主账本
    print(f"✅ 已记录买入")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name} ({code})")
    _safe_print("🔢", f"{val_shares}股 × ¥{val_price:.2f} = ¥{amount:,.2f}")
    _safe_print("💳", account)

    # 更新 CSV 中的现价
    prices = load_prices()
    prices[code] = val_price
    save_prices(prices)


def do_sell(name, code, shares, price, dt, account):
    """记录卖出"""
    if not _validate_code(code):
        raise ValueError(f"证券代码必须为6位数字：{code}")
    val_shares = _validate_shares(shares)
    val_price = _validate_price(price)
    amount = val_shares * val_price
    _validate_amount(amount)
    # 卖出前预检查：当前持仓是否足够
    entries = load_ledger()
    holdings = compute_holdings(entries)
    current = holdings.get(code, {})
    current_shares = current.get("total_shares", 0)
    if current_shares <= 0:
        print(f"❌ {name}（{code}）当前无持仓，无法卖出")
        return
    if val_shares > current_shares:
        print(f"❌ 持仓不足：当前持有 {current_shares} 股，最多可卖 {current_shares} 股")
        return
    # 二次确认
    if not confirm_sell(name, code, val_shares, val_price, amount, account, dt):
        print("❌ 已取消卖出")
        return
    append_ledger_with_price(f"{dt},卖出,{code},{_sanitize(name)},{val_shares},@{val_price:.2f},{amount:.2f},{account}", val_price)
    # 投资交易仅写入 investments.csv，不同步到主账本
    print(f"✅ 已记录卖出")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name} ({code})")
    _safe_print("🔢", f"{val_shares}股 × ¥{val_price:.2f} = ¥{amount:,.2f}")
    _safe_print("💳", account)

    prices = load_prices()
    prices[code] = val_price
    save_prices(prices)


def confirm_dividend(name, code, amount, account, dt):
    """打印分红摘要并询问确认，返回 True/False。"""
    print("\n📋 分红确认：")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name}（{code}）")
    _safe_print("💰", f"¥{amount:,.2f}")
    _safe_print("💳", account)
    try:
        ans = input("\n确认记录分红? (Y/N): ").strip().lower()
        return ans in ("y", "yes")
    except (EOFError, IOError, KeyboardInterrupt):
        return False


def do_dividend(name, code, amount, dt, account):
    """记录分红"""
    if not _validate_code(code):
        raise ValueError(f"证券代码必须为6位数字：{code}")
    val_amount = _validate_amount(amount, "分红金额")
    if not confirm_dividend(name, code, val_amount, account, dt):
        print("❌ 已取消分红记录")
        return
    entry = f"{dt},分红,{code},{_sanitize(name)},{val_amount:.2f},,,{account}"
    append_ledger(entry)
    print(f"✅ 已记录分红")
    _safe_print("📅", dt)
    _safe_print("📊", f"{name} ({code})")
    _safe_print("💰", f"¥{val_amount:.2f}")
    _safe_print("💳", account)


# ==================== 持仓计算 ====================

def compute_holdings(entries: list) -> dict:
    """
    计算当前持仓。
    持仓成本 = 总买入金额 - 总卖出金额（净成本法）。
    盈亏 = 当前市值 - 净成本。
    """
    holdings = {}

    for e in entries:
        raw_code = e.get("code", "")
        raw_name = e.get("name", "")
        if raw_code and raw_code[0].isdigit():
            code = raw_code
            cname = raw_name
        elif raw_name and raw_name[0].isdigit():
            code = raw_name
            cname = raw_code
        else:
            continue

        if code not in holdings:
            holdings[code] = {
                "name": cname,
                "code": code,
                "total_shares": 0.0,
                "total_cost": 0.0,
                "realized_pnl": 0.0,
                "dividends": 0.0,
                "buy_count": 0,
                "sell_count": 0,
            }

        h = holdings[code]

        if e["action"] == "买入":
            cost = e.get("cost", e["shares"] * e["price"])
            h["total_cost"] += cost
            h["total_shares"] += e["shares"]
            h["buy_count"] += 1

        elif e["action"] == "卖出":
            proceeds = e.get("proceeds", e["shares"] * e["price"])
            h["total_cost"] -= proceeds
            h["total_shares"] -= e["shares"]
            h["sell_count"] += 1
            if h["total_shares"] < 0:
                # 持仓为负属于数据异常（do_sell 已阻止正常超卖），仅截断份额；
                # 保留 total_cost 以反映已实现盈亏，避免清零吞掉收益数据。
                h["total_shares"] = 0

        elif e["action"] == "分红":
            h["dividends"] += e["amount"]

    return holdings


# ==================== 输出函数 ====================

def do_portfolio(entries: list, prices: dict, allow_network: bool = False):
    """
    输出持仓概览。
    若 allow_network=True（命令行参数 --auto-refresh）或用户已开启自动联网刷新，
    自动联网获取实时价格后再计算。
    """
    should_refresh = allow_network or auto_refresh_enabled()
    if should_refresh:
        print("🌐 联网刷新实时行情中...")
        do_refresh(entries, allow_network=True)
        prices = load_prices()  # 重新加载更新后的价格

    holdings = compute_holdings(entries)
    active = {k: v for k, v in holdings.items() if v["total_shares"] > 0}

    if not active:
        print("📭 当前无持仓")
        return

    header = (
        f"{'基金/股票':<12} {'持仓':>6} {'成本':>12} {'现价':>8} "
        f"{'市值':>12} {'收益':>10} {'收益率':>8}"
    )
    sep = "─" * 72

    print(f"📈 投资持仓概览\n")
    print(header)
    print(sep)

    total_cost = 0.0
    total_market = 0.0

    for code in sorted(active.keys()):
        h = active[code]
        cur_price = prices.get(code, 0)
        market = h["total_shares"] * cur_price
        pnl = market - h["total_cost"]
        pnl_pct = (pnl / h["total_cost"] * 100) if h["total_cost"] > 0 else 0
        sign = "+" if pnl >= 0 else ""
        emoji = "✅" if pnl >= 0 else "🔴"

        pnl_str = f"{sign}¥{abs(pnl):,.2f}" if pnl >= 0 else f"-¥{abs(pnl):,.2f}"
        pct_str = f"+{abs(pnl_pct):.1f}%" if pnl >= 0 else f"-{abs(pnl_pct):.1f}%"

        print(
            f"{h['name']:<12} {h['total_shares']:>5.0f}股 "
            f"¥{h['total_cost']:>10,.2f} ¥{cur_price:>6.2f} "
            f"¥{market:>10,.2f} {pnl_str} {pct_str} {emoji}"
        )

        total_cost += h["total_cost"]
        total_market += market

    total_pnl = total_market - total_cost
    total_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
    ts = "+" if total_pnl >= 0 else ""

    print(sep)
    print(
        f"{'合计':<12} {'':>6} "
        f"¥{total_cost:>10,.2f} {'':>8} "
        f"¥{total_market:>10,.2f} {ts}¥{abs(total_pnl):,.2f} {ts}{abs(total_pct):.1f}%"
    )

    total_dividends = sum(h["dividends"] for h in active.values())
    if total_dividends > 0:
        print(f"\n💰 累计分红：¥{total_dividends:,.2f}")

    missing = [active[c]["name"] for c in active if c not in prices]
    if missing:
        print(f"\n⚠️  以下持仓未设置当前价格：{', '.join(missing)}")
        print(f"   使用 --price <代码> <价格> 更新（如: --price 510050 3.62）")


def do_return(code: str, entries: list, prices: dict):
    """计算单只证券的收益率"""
    holdings = compute_holdings(entries)
    h = holdings.get(code)

    if not h:
        print(f"❌ 未找到代码 {code} 的交易记录")
        return

    shares = h["total_shares"]
    avg_cost = h["total_cost"] / shares if shares > 0 else 0
    cur_price = prices.get(code, 0)
    market = shares * cur_price
    unrealized_pnl = market - h["total_cost"]

    print(f"📊 {h['name']} ({code}) 收益分析\n")
    print(f"{'买入次数':>8}：{h['buy_count']} 次")
    print(f"{'卖出次数':>8}：{h['sell_count']} 次")
    print(f"{'当前持仓':>8}：{shares:.0f} 股")
    print(f"{'平均成本':>8}：¥{avg_cost:.4f}")
    print(f"{'总成本':>8}：¥{h['total_cost']:,.2f}")

    if shares > 0:
        pnl_pct = (unrealized_pnl / h["total_cost"] * 100) if h["total_cost"] > 0 else 0
        sign = "+" if unrealized_pnl >= 0 else ""
        print(f"{'当前价格':>8}：¥{cur_price:.2f}")
        print(f"{'当前市值':>8}：¥{market:,.2f}")
        print(f"{'持仓盈亏':>8}：{sign}¥{unrealized_pnl:,.2f} ({sign}{pnl_pct:.1f}%)")

    if h["dividends"] > 0:
        div_yield = (h["dividends"] / h["total_cost"] * 100) if h["total_cost"] > 0 else 0
        print(f"{'累计分红':>8}：¥{h['dividends']:,.2f} (分红率 {div_yield:.1f}%)")

    # 净成本法下总收益 = 持仓盈亏 + 分红
    total_return = unrealized_pnl + h["dividends"]
    total_pct = (total_return / h["total_cost"] * 100) if h["total_cost"] > 0 else 0
    tsign = "+" if total_return >= 0 else ""

    print(f"\n{'═' * 32}")
    print(f"  总收益：{tsign}¥{total_return:,.2f} ({tsign}{total_pct:.1f}%)")
    print(f"  （持仓盈亏 + 分红）")

    if code not in prices:
        print(f"\n⚠️  未设置当前价格，持仓盈亏按 ¥0 计算")
        print(f"   使用 --price {code} <价格> 更新")


def do_summary(entries: list, prices: dict, allow_network: bool = False):
    """
    汇总所有投资收益。
    若 allow_network=True（命令行参数 --auto-refresh）或用户已开启自动联网刷新，
    自动联网获取实时价格后再汇总。
    """
    should_refresh = allow_network or auto_refresh_enabled()
    if should_refresh:
        print("🌐 联网刷新实时行情中...")
        do_refresh(entries, allow_network=True)
        prices = load_prices()  # 重新加载更新后的价格

    holdings = compute_holdings(entries)

    if not holdings:
        print("📭 暂无投资记录")
        return

    active = {k: v for k, v in holdings.items() if v["total_shares"] > 0}
    closed = {k: v for k, v in holdings.items() if v["total_shares"] <= 0 and v["total_cost"] != 0}

    header = f"{'基金/股票':<12} {'成本':>12} {'市值':>12} {'收益':>10} {'收益率':>8}"
    sep = "─" * 56

    if active:
        print(f"📈 投资收益汇总\n")
        print(header)
        print(sep)

        total_cost = 0.0
        total_market = 0.0

        for code in sorted(active.keys()):
            h = active[code]
            cur_price = prices.get(code, 0)
            market = h["total_shares"] * cur_price
            pnl = market - h["total_cost"]
            pnl_pct = (pnl / h["total_cost"] * 100) if h["total_cost"] > 0 else 0
            sign = "+" if pnl >= 0 else ""
            emoji = "✅" if pnl >= 0 else "🔴"

            pnl_str = f"{sign}¥{abs(pnl):,.2f}" if pnl >= 0 else f"-¥{abs(pnl):,.2f}"
            pct_str = f"+{abs(pnl_pct):.1f}%" if pnl >= 0 else f"-{abs(pnl_pct):.1f}%"

            print(
                f"{h['name']:<12} ¥{h['total_cost']:>10,.2f} "
                f"¥{market:>10,.2f} {pnl_str} {pct_str} {emoji}"
            )
            total_cost += h["total_cost"]
            total_market += market

        total_pnl = total_market - total_cost
        total_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
        ts = "+" if total_pnl >= 0 else ""

        print(sep)
        print(
            f"{'合计':<12} ¥{total_cost:>10,.2f} "
            f"¥{total_market:>10,.2f} {ts}¥{abs(total_pnl):,.2f} {ts}{abs(total_pct):.1f}%"
        )

    if closed:
        print(f"\n📋 已清仓记录")
        print(sep)
        for code in sorted(closed.keys()):
            h = closed[code]
            # 净成本法：已清仓盈亏 = -total_cost（卖出金额已从成本中扣减）
            closed_pnl = -h["total_cost"]
            csign = "+" if closed_pnl >= 0 else ""
            div = f"  分红 ¥{h['dividends']:,.2f}" if h["dividends"] > 0 else ""
            print(f"  {h['name']} ({code}): {csign}¥{closed_pnl:,.2f}{div}")

    total_dividends = sum(h["dividends"] for h in holdings.values())
    total_closed_pnl = sum(-h["total_cost"] for k, h in holdings.items() if h["total_shares"] <= 0)
    unrealized = total_market - total_cost if active else 0

    total_all = unrealized + total_closed_pnl + total_dividends
    all_pct = (total_all / total_cost * 100) if total_cost > 0 else 0
    ts = "+" if total_all >= 0 else ""

    if total_dividends > 0 or total_closed_pnl != 0:
        print(f"\n{'─' * 56}")
        print(f"  持仓盈亏：  {('+' if unrealized >= 0 else '')}¥{unrealized:,.2f}")
        if total_closed_pnl != 0:
            print(f"  已清仓盈亏：{('+' if total_closed_pnl >= 0 else '')}¥{total_closed_pnl:,.2f}")
        if total_dividends > 0:
            print(f"  现金分红：  ¥{total_dividends:,.2f}")
        print(f"{'─' * 56}")
        print(f"  总收益：    {ts}¥{total_all:,.2f} ({ts}{all_pct:.1f}%)")

    missing = [active[c]["name"] for c in active if c not in prices]
    if missing:
        print(f"\n⚠️  未设置价格：{', '.join(missing)}")
        print(f"   使用 --price <代码> <价格> 更新")


def do_list(code: str = None):
    """查看交易记录"""
    entries = load_ledger()

    if code:
        entries = [e for e in entries if e.get("code") == code]
        print(f"📋 {code} 交易记录\n")
    else:
        print(f"📋 全部交易记录\n")

    if not entries:
        print("  （无记录）")
        return

    for e in entries:
        if e["action"] == "买入":
            cost = e.get("cost", e["shares"] * e["price"])
            print(
                f"  {e['date']}  🟢买入  {e['name']}  "
                f"{e['shares']:.0f}股 × ¥{e['price']:.2f} = ¥{cost:,.2f}"
            )
        elif e["action"] == "卖出":
            print(
                f"  {e['date']}  🔴卖出  {e['name']}  "
                f"{e['shares']:.0f}股 × ¥{e['price']:.2f} = ¥{e['proceeds']:,.2f}"
            )
        elif e["action"] == "分红":
            print(
                f"  {e['date']}  💰分红  {e['name']}  ¥{e['amount']:,.2f}"
            )


# ==================== 代码自动查找 ====================

def is_numeric_code(s: str) -> bool:
    """判断字符串是否像股票/基金代码（6位纯数字）"""
    return bool(s.strip().isdigit() and len(s.strip()) == 6)


def auto_lookup_code(name: str, allow_network: bool = False) -> dict:
    """
    调用 lookup_code.py 自动查询代码（需显式允许联网）。
    返回 dict: {"found": bool, "code": str, "name": str, "results": list, ...}
    """
    if not allow_network:
        _network_denied("自动查询证券代码")
        return {"found": False, "code": None, "name": name, "results": [], "network_denied": True}
    script_path = SCRIPT_DIR / "lookup_code.py"
    try:
        result = subprocess.run(
            [sys.executable, str(script_path), name],
            capture_output=True, text=True, timeout=30,
            cwd=str(SCRIPT_DIR),
        )
        output = result.stdout
        # 解析 JSON（在第一个 { 开始）
        try:
            json_start = output.index("{")
            json_text = output[json_start:]
            return json.loads(json_text)
        except (ValueError, json.JSONDecodeError):
            return {"found": False, "code": None, "name": name, "results": []}
    except Exception as e:
        return {"found": False, "code": None, "name": name, "results": [], "error": str(e)}


def resolve_code(name: str, code_arg: str, allow_network: bool = False) -> dict:
    """
    解析代码参数。

    - 如果 code_arg 是 6 位数字 → 直接使用
    - 如果 code_arg 是 "auto" 或其他非数字 → 需 --allow-network 后联网搜索

    返回: {"code": str, "name": str, "lookup_info": dict}
    - code=None 表示需要用户确认（多个候选或未找到）
    """
    code_arg = code_arg.strip()

    if is_numeric_code(code_arg):
        return {"code": code_arg, "name": name, "lookup_info": None}

    # 需要联网查找
    print(f"🔍 正在联网查询「{name}」的代码...")
    lookup_result = auto_lookup_code(name, allow_network=allow_network)

    if not lookup_result.get("found"):
        print(f"\n❌ 未找到「{name}」的代码，请手动提供股票/基金代码")
        return {"code": None, "name": name, "lookup_info": lookup_result}

    results = lookup_result.get("results", [])

    if len(results) == 1:
        r = results[0]
        print(f"\n✅ 找到代码：{r['name']}（{r['code']}）<{r['type']}>")
        return {"code": r["code"], "name": r["name"], "lookup_info": lookup_result}

    # 多个候选：打印选项，退出让用户选择
    primary = lookup_result.get("primary") or results[0]
    print(f"\n⚠️  找到 {len(results)} 个候选，请手动确认代码：")
    for i, r in enumerate(results, 1):
        marker = "← 推荐" if r == primary else ""
        print(f"   {i}. {r['name']}（{r['code']}）<{r['type']}> {marker}")
    print(f"\n   请重新输入：--buy \"{name}\" <代码> <数量> <单价> <日期>")
    return {"code": None, "name": name, "lookup_info": lookup_result}


# ==================== CLI ====================

def main():
    parser = argparse.ArgumentParser(
        description="投资跟踪工具（CSV格式）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 手动提供代码（最常用）
  python invest.py --buy "沪深300ETF" 510050 1000 3.50 2026-01-15

  # 自动查代码（需显式允许联网；用户 Y/N 确认后才写入）
  python invest.py --buy "沪深300ETF" auto 1000 3.50 2026-01-15 --allow-network

  # 其他操作
  python invest.py --sell "沪深300ETF" 510050 500 4.00 2026-03-01
  python invest.py --dividend "沪深300ETF" 45.60 2026-02-10
  python invest.py --price 510050 3.62
  python invest.py --cost 600487 75.631
  python invest.py --portfolio
  python invest.py --return 510050
  python invest.py --summary
  python invest.py --list
  python invest.py --list 510050
  python invest.py --quote 600487 --allow-network
  python invest.py --refresh --allow-network
  # 查询持仓时自动联网刷新行情
  python invest.py --portfolio --auto-refresh
  python invest.py --summary --auto-refresh
        """,
    )

    parser.add_argument("--buy", nargs=5, metavar=("名称", "代码", "数量", "单价", "日期"),
                        help="记录买入（代码处写 auto 可自动联网搜索）")
    parser.add_argument("--sell", nargs=5, metavar=("名称", "代码", "数量", "单价", "日期"),
                        help="记录卖出")
    parser.add_argument("--account", metavar="账户", default="银行卡",
                        help="交易账户（默认：银行卡）")
    parser.add_argument("--price", nargs=2, metavar=("代码", "价格"),
                        help="设置当前价格")
    parser.add_argument("--cost", nargs=2, metavar=("代码", "成本单价"),
                        help="修改最近一笔买入的成本单价")
    parser.add_argument("--portfolio", action="store_true", help="查看持仓概览")
    parser.add_argument("--return", dest="calc_return", metavar="代码", help="计算单只收益率")
    parser.add_argument("--summary", action="store_true", help="汇总全部收益")
    parser.add_argument("--list", nargs="?", const="__ALL__", metavar="代码", help="查看交易记录")
    parser.add_argument("--refresh", action="store_true",
                        help="联网刷新所有持仓的实时/收盘价格")
    parser.add_argument("--auto-refresh", action="store_true",
                        help="查询持仓/汇总时自动联网刷新实时行情（等同于先执行 --refresh，再展示结果）")
    parser.add_argument("--quote", metavar="代码",
                        help="查询单只证券实时行情（需同时加 --allow-network）")
    parser.add_argument("--allow-network", action="store_true",
                        help="显式允许联网查询证券代码或行情；不会上传个人账本数据")
    parser.add_argument("--enable-auto-refresh", action="store_true",
                        help="开启自动联网刷新行情（写入 .env 配置文件）")
    parser.add_argument("--disable-auto-refresh", action="store_true",
                        help="关闭自动联网刷新行情（删除 .env 配置文件）")

    args = parser.parse_args()

    def default_date(dt_str: str) -> str:
        if dt_str.lower() == "today":
            return date.today().isoformat()
        try:
            datetime.strptime(dt_str, "%Y-%m-%d")
            return dt_str
        except ValueError:
            return date.today().isoformat()

    if args.buy:
        name, code_arg, shares, price, dt = args.buy
        resolved = resolve_code(name, code_arg, allow_network=args.allow_network)
        resolved_code = resolved["code"]
        if resolved_code is None:
            # 多个候选或未找到，已打印提示，退出
            sys.exit(1)
        display_name = resolved["name"]
        do_buy(display_name, resolved_code, float(shares), float(price), default_date(dt), args.account)

    elif args.sell:
        name, code, shares, price, dt = args.sell
        do_sell(name, code, float(shares), float(price), default_date(dt), args.account)

    elif args.price:
        code, price = args.price
        set_price(code, float(price))
        print(f"✅ 已更新 {code} 当前价格：¥{float(price):.2f}")

    elif args.cost:
        code, new_price = args.cost
        do_cost(code, float(new_price))

    elif args.portfolio:
        entries = load_ledger()
        prices = load_prices()
        do_portfolio(entries, prices, allow_network=args.auto_refresh)

    elif args.calc_return:
        entries = load_ledger()
        prices = load_prices()
        do_return(args.calc_return, entries, prices)

    elif args.summary:
        entries = load_ledger()
        prices = load_prices()
        do_summary(entries, prices, allow_network=args.auto_refresh)

    elif args.list:
        do_list(None if args.list == "__ALL__" else args.list)

    elif args.refresh:
        entries = load_ledger()
        do_refresh(entries, allow_network=args.allow_network)

    elif args.quote:
        do_quote(args.quote, allow_network=args.allow_network)

    elif args.enable_auto_refresh:
        env_file = DATA_DIR / ".env"
        ensure_data_dir()
        # 读取现有内容，去掉 AUTO_REFRESH 行
        content = ""
        if env_file.exists():
            content = env_file.read_text(encoding="utf-8")
            content = "\n".join(l for l in content.splitlines() if not l.startswith("AUTO_REFRESH"))
        content = content.strip()
        new_content = (content + "\nAUTO_REFRESH=1\n").strip() + "\n"
        env_file.write_text(new_content, encoding="utf-8")
        print("✅ 已开启自动联网刷新行情")
        print(f"   配置文件：{env_file}")
        print("   以后查询持仓/收益时会自动联网刷新价格，无需每次加参数")
        print("   关闭方法：python invest.py --disable-auto-refresh")

    elif args.disable_auto_refresh:
        env_file = DATA_DIR / ".env"
        if not env_file.exists():
            print("📭 自动联网未开启，无需关闭")
        else:
            content = env_file.read_text(encoding="utf-8")
            new_content = "\n".join(l for l in content.splitlines() if not l.startswith("AUTO_REFRESH"))
            if new_content.strip():
                env_file.write_text(new_content.strip() + "\n", encoding="utf-8")
            else:
                env_file.unlink()
            print("✅ 已关闭自动联网刷新行情")
            print("   以后查询持仓使用手动设置的价格")
            print("   开启方法：python invest.py --enable-auto-refresh")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()