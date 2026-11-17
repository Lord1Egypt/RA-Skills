#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
持仓台账与评分快照管理

管理三类数据：
  positions.json  —— 持仓（代码/数量/成本价），来源为截图解析或用户录入
  watchlist.json  —— 自选清单（连接器不可用时的降级数据源）
  history/*.json  —— 每次运行的评分快照，用于追踪评分变化

用法:
    python portfolio_ledger.py init [--dir 工作区路径]
    python portfolio_ledger.py save-positions --data '<json>' [--dir ...]
    python portfolio_ledger.py show [--dir ...]
    python portfolio_ledger.py snapshot --result result.json --date 2026-08-30 [--dir ...]
    python portfolio_ledger.py latest [--dir ...]
    python portfolio_ledger.py history --code sh600519 [--dir ...]
    python portfolio_ledger.py weights --dir ...      # 按现价计算当前持仓权重
"""

import argparse
import json
import math
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_DIR = "workspace/portfolio_ledger"

# 代码前缀推断：6开头沪、0/3开头深、4/8开头北交所、5位港股
def normalize_code(code):
    code = str(code).strip().lower()
    if code.startswith(("sh", "sz", "bj", "hk", "us")):
        return code
    digits = "".join(ch for ch in code if ch.isdigit())
    if len(digits) == 6:
        if digits[0] == "6":
            return "sh" + digits
        if digits[0] in "03":
            return "sz" + digits
        if digits[0] in "489":
            return "bj" + digits
    if len(digits) == 5:
        return "hk" + digits
    return code


def ledger_dir(base):
    p = Path(base) if base else Path(DEFAULT_DIR)
    p.mkdir(parents=True, exist_ok=True)
    (p / "history").mkdir(parents=True, exist_ok=True)
    return p


def cmd_init(args):
    d = ledger_dir(args.dir)
    for fname, default in (("positions.json", {"updated": None, "source": None,
                                               "positions": []}),
                           ("watchlist.json", {"updated": None, "source": None,
                                               "codes": []})):
        f = d / fname
        if not f.exists():
            f.write_text(json.dumps(default, ensure_ascii=False, indent=2),
                         encoding="utf-8")
    print(f"[OK] 台账已就绪: {d.resolve()}")
    print(f"     {d / 'positions.json'}")
    print(f"     {d / 'watchlist.json'}")
    print(f"     {d / 'history/'}")
    return 0


def cmd_save_positions(args):
    d = ledger_dir(args.dir)
    data = json.loads(args.data)
    raw = data["positions"] if isinstance(data, dict) else data
    positions = []
    for r in raw:
        code = normalize_code(r.get("code") or r.get("股票代码") or "")
        if not code:
            print(f"[WARN] 跳过无代码条目: {r}")
            continue
        positions.append({
            "code": code,
            "name": r.get("name") or r.get("名称") or r.get("股票名称"),
            "shares": r.get("shares") or r.get("持仓数量") or r.get("数量"),
            "cost_price": r.get("cost_price") or r.get("成本价") or r.get("摊薄成本"),
            "current_price": r.get("current_price") or r.get("现价"),
            "currency": r.get("currency", "CNY"),
            "margin": bool(r.get("margin", False)),
        })
    payload = {
        "updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": data.get("source", "screenshot") if isinstance(data, dict) else "screenshot",
        "positions": positions,
    }
    (d / "positions.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"[OK] 已保存 {len(positions)} 条持仓 -> {d / 'positions.json'}")
    print("\n请核对以下识别结果（确认无误后才会用于评分与配置计算）：\n")
    print(f"{'代码':<12}{'名称':<10}{'数量':>10}{'成本价':>10}{'现价':>10}")
    print("-" * 52)
    for p in positions:
        print(f"{p['code']:<12}{str(p['name'] or '-'):<10}"
              f"{str(p['shares'] or '-'):>10}{str(p['cost_price'] or '-'):>10}"
              f"{str(p['current_price'] or '-'):>10}")
    return 0


def cmd_save_watchlist(args):
    d = ledger_dir(args.dir)
    codes = [normalize_code(c) for c in json.loads(args.codes)]
    payload = {"updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "source": "user", "codes": codes}
    (d / "watchlist.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 已保存 {len(codes)} 只自选 -> {d / 'watchlist.json'}")
    return 0


def cmd_show(args):
    d = ledger_dir(args.dir)
    pf, wf = d / "positions.json", d / "watchlist.json"
    if pf.exists():
        p = json.loads(pf.read_text(encoding="utf-8"))
        print(f"持仓（更新于 {p.get('updated')}，来源 {p.get('source')}）:")
        if not p["positions"]:
            print("  （空）")
        for x in p["positions"]:
            print(f"  {x['code']:<12}{str(x.get('name') or '-'):<10}"
                  f"  数量 {str(x.get('shares') or '-'):>8}"
                  f"  成本 {str(x.get('cost_price') or '-'):>8}")
    if wf.exists():
        w = json.loads(wf.read_text(encoding="utf-8"))
        print(f"\n自选（更新于 {w.get('updated')}）: {', '.join(w['codes']) or '（空）'}")
    return 0


def cmd_snapshot(args):
    d = ledger_dir(args.dir)
    result = json.loads(Path(args.result).read_text(encoding="utf-8"))
    date = args.date or result.get("date") or datetime.now().strftime("%Y-%m-%d")
    target = d / "history" / f"{date}.json"
    result["date"] = date
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] 快照已保存: {target}")
    return 0


def cmd_latest(args):
    d = ledger_dir(args.dir)
    files = sorted((d / "history").glob("*.json"))
    if not files:
        print("")
        return 0
    exclude = args.exclude_date
    picked = None
    for f in files:
        if exclude and f.stem == exclude:
            continue
        picked = f
    print(str(picked) if picked else "")
    return 0


def cmd_history(args):
    d = ledger_dir(args.dir)
    rows = []
    for f in sorted((d / "history").glob("*.json")):
        snap = json.loads(f.read_text(encoding="utf-8"))
        for s in snap.get("stocks", []):
            if args.code and s.get("code") != args.code:
                continue
            rows.append((f.stem, s.get("code"), s.get("name"),
                         s.get("total"), s.get("grade")))
    if not rows:
        print("暂无历史评分记录")
        return 0
    print(f"{'日期':<12}{'代码':<12}{'名称':<10}{'总分':>8}{'评级':>6}")
    print("-" * 50)
    for r in rows:
        print(f"{r[0]:<12}{str(r[1]):<12}{str(r[2]):<10}{str(r[3]):>8}{str(r[4]):>6}")
    return 0


def cmd_weights(args):
    """按现价与数量计算当前持仓权重，回写为 positions weights JSON"""
    d = ledger_dir(args.dir)
    p = json.loads((d / "positions.json").read_text(encoding="utf-8"))
    prices = json.loads(args.prices) if args.prices else {}
    rows, total = [], 0.0
    has_margin = any(x.get('margin') for x in p['positions'])
    for x in p["positions"]:
        px = prices.get(x["code"]) or x.get("current_price")
        mv = None
        if px and x.get("shares"):
            mv = float(px) * float(x["shares"])
            if not math.isfinite(mv) or mv <= 0:
                raise ValueError('市值必须为有限正数')
            total += mv
        rows.append({"code": x["code"], "name": x.get("name"),
                     "price": px, "shares": x.get("shares"),
                     "cost_price": x.get("cost_price"),
                     "market_value": round(mv, 2) if mv else None,
                     "pnl_pct": (round((float(px) - float(x["cost_price"]))
                                       / float(x["cost_price"]) * 100, 2)
                                 if (px and x.get("cost_price")) else None)})
    total_assets = args.total_assets
    if total_assets is not None and (not math.isfinite(total_assets) or total_assets <= 0 or total_assets < total):
        raise ValueError('--total-assets需为有限正数且不低于股票市值合计；负债账户不适用')
    complete = all(r['market_value'] is not None for r in rows) and not has_margin
    for r in rows:
        r['stock_sleeve_weight'] = round(r['market_value'] / total * 100, 2) if r['market_value'] and total and complete else None
        r['current_weight'] = round(r['market_value'] / total_assets * 100, 2) if r['market_value'] and total_assets and complete else None
    warnings = []
    if total_assets is None:
        warnings.append('缺少--total-assets：股票内部占比仅供展示，current_weight不生成')
    if not complete:
        warnings.append('持仓市值不完整或存在融资负债，暂不计算配置权重')
    print(json.dumps({"total_market_value": round(total, 2), "total_assets": total_assets,
                      "weight_basis": "total_assets" if total_assets and complete else None,
                      "warnings": warnings, "positions": rows},
                     ensure_ascii=False, indent=2))
    return 0


def main():
    ap = argparse.ArgumentParser(description="持仓台账与评分快照管理")
    ap.add_argument("command", choices=["init", "save-positions", "save-watchlist",
                                        "show", "snapshot", "latest", "history",
                                        "weights"])
    ap.add_argument("--dir", default=None, help="台账目录，默认 workspace/portfolio_ledger")
    ap.add_argument("--data", help="save-positions: 持仓 JSON 字符串")
    ap.add_argument("--codes", help="save-watchlist: JSON 数组字符串")
    ap.add_argument("--result", help="snapshot: 评分结果 JSON 路径")
    ap.add_argument("--date", help="snapshot/history: 日期 YYYY-MM-DD")
    ap.add_argument("--code", help="history: 股票代码过滤")
    ap.add_argument("--prices", help="weights: JSON {code: price}")
    ap.add_argument('--total-assets', type=float, help='weights: 包含股票、现金与其他资产的总资产（元），缺失时不生成current_weight')
    ap.add_argument("--exclude-date", dest="exclude_date",
                    help="latest: 排除该日期（用于取上一次快照）")
    args = ap.parse_args()

    fn = {"init": cmd_init, "save-positions": cmd_save_positions,
          "save-watchlist": cmd_save_watchlist, "show": cmd_show,
          "snapshot": cmd_snapshot, "latest": cmd_latest,
          "history": cmd_history, "weights": cmd_weights}[args.command]
    return fn(args)


if __name__ == "__main__":
    sys.exit(main())
