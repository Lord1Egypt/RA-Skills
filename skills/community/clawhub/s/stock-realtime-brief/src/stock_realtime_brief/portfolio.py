"""
持仓管理 — 加载、合并、加权成本计算。

支持的持仓 JSON 格式（兼容 holdings/positions 两种字段名）:
{
  "margin_debt": 706059,            // 融资余额
  "positions": [                     // 或 holdings
    {
      "symbol": "300757",            // 或 code
      "name": "罗博特科",
      "buy_price": 346.37,           // 或 cost
      "amount": 2700,                 // 或 shares
      "account": "普通",             // 或 "融资"
      "sector": "CPO设备",
      "has_margin": false             // 当 account 不是"融资"时可显式标记
    }
  ]
}

同一股票多笔（多账户/多次买入）会自动合并加权成本。
"""
from __future__ import annotations

import json
import os
from pathlib import Path


def resolve_portfolio_path(arg_path: str | None = None) -> Path | None:
    """三层路径解析: 命令行参数 > 环境变量 > 当前目录"""
    if arg_path and Path(arg_path).exists():
        return Path(arg_path)
    env_path = os.environ.get("STOCK_BRIEF_PORTFOLIO")
    if env_path and Path(env_path).exists():
        return Path(env_path)
    cwd_path = Path("portfolio.json")
    if cwd_path.exists():
        return cwd_path
    return None


def load_portfolio(path: str | Path) -> tuple[list[dict], float]:
    """加载持仓 JSON，返回 (合并后的持仓列表, 融资余额)"""
    with open(path, encoding="utf-8") as f:
        pf = json.load(f)
    total_margin = pf.get("margin_debt", 0)
    raw = pf.get("positions") or pf.get("holdings") or []

    # 合并相同股票的多账户/多次买入
    agg: dict[str, dict] = {}
    for p in raw:
        code = p.get("code") or p.get("symbol")
        if not code:
            continue
        if code not in agg:
            agg[code] = {
                "code": code,
                "name": p.get("name", code),
                "sector": p.get("sector", ""),
                "amount": 0,
                "cost_total": 0,
                "has_margin": False,
            }
        amt = p.get("amount") or p.get("shares") or 0
        cost_each = p.get("buy_price") or p.get("cost") or 0
        agg[code]["amount"] += amt
        agg[code]["cost_total"] += cost_each * amt
        if p.get("account") == "融资" or p.get("has_margin"):
            agg[code]["has_margin"] = True

    holdings = []
    for code, x in agg.items():
        if x["amount"] <= 0:
            continue
        avg_cost = round(x["cost_total"] / x["amount"], 2)
        holdings.append({
            "code": code,
            "name": x["name"],
            "sector": x["sector"],
            "cost": avg_cost,
            "amount": x["amount"],
            "has_margin": x["has_margin"],
        })
    return holdings, total_margin


def calc_position_metrics(holdings: list[dict], realtime: dict[str, dict]) -> tuple[list[dict], float]:
    """根据实时价格计算市值、浮盈、仓位占比，返回 (更新后的持仓, 总市值)"""
    total_mv = 0.0
    for h in holdings:
        rt = realtime.get(h["code"]) or {}
        price = rt.get("price") or h["cost"]
        h["price"] = price
        h["rt"] = rt
        h["mv"] = round(price * h["amount"], 0)
        h["pnl"] = round((price - h["cost"]) * h["amount"], 0)
        h["pnl_pct"] = round((price - h["cost"]) / h["cost"] * 100, 2) if h["cost"] else 0
        h["is_loss"] = h["pnl"] < 0
        total_mv += h["mv"]
    for h in holdings:
        h["weight"] = round(h["mv"] / total_mv * 100, 2) if total_mv else 0
        h["is_heavy"] = h["weight"] >= 25
    return holdings, total_mv


def calc_guarantee_ratio(total_mv: float, total_margin: float) -> float | None:
    """担保比例 = (持仓总市值 + 融资买入证券市值) / 融资余额"""
    if not total_margin:
        return None
    return round(total_mv / total_margin * 100, 1)


def grade_guarantee_ratio(ratio: float | None) -> str:
    """五档预警标签"""
    if ratio is None:
        return ""
    if ratio < 150:
        return "🚨🚨🚨 **接近强平区！立即降仓**"
    if ratio < 160:
        return "🚨 **强警告：尽快降杠杆**"
    if ratio < 170:
        return "⚠️ **警戒区：建议主动降仓**"
    if ratio < 200:
        return "🟡 **可控区：仍需关注**"
    return "✅ **安全区**"


def risk_rank_key(h: dict) -> int:
    """风险排序键（亏损×融资×破MA20×重仓）"""
    score = 0
    if h.get("is_loss"):
        score += 2
    if h.get("has_margin"):
        score += 3
    if h.get("is_heavy"):
        score += 1
    hist = h.get("hist") or {}
    if hist.get("last") and hist.get("ma20") and hist["last"] < hist["ma20"]:
        score += 2
    return -score
