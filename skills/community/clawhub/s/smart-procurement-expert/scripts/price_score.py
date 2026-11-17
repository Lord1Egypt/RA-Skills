#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智慧招采专家 · 深度节点 C — 价格分自动算分引擎
================================================
依据《评标办法》中的价格分计算规则，对一组投标报价自动计算价格得分。
支持现行招投标/政府采购中最常见的三类算法：

  1. low_price_first  低价优先法（政府采购货物/服务常用）
     满足要求的最低报价为评标基准价，得满分；其余报价按比例折算：
         S_i = (P_min / P_i) × 满分

  2. benchmark         基准价法 / 合理低价法（工程常用）
     先按规则算评标基准价 P_base，报价每偏离 1% 扣相应分值：
         偏差率 d% = (P_i − P_base) / P_base × 100
         d% ≥ 0 : S = 满分 − d × 扣减(高于)
         d% < 0 : S = 满分 − |d| × 扣减(低于)
         S 下限 0
     P_base 计算方式（base.mode）可选：
         average      所有有效报价均值
         average_k    均值下浮 K（如 0.98）
         median       中位数
         lowest_n_avg 最低 N 家均值
         weighted     加权 = w*均值 + (1-w)*最低价
         fixed        直接使用给定基准价（如招标控制价/标底）

  3. interval          区间法 / 限值法
     报价落入 [low, high] 得满分；超出区间按比例扣减。

输入：
  - CLI：--method ... --quotes 980,1000,1020 --names A,B,C --full-score 30
  - 配置：--config price_config.json（见 demo/price_config.json）
输出：
  - 终端打印 Markdown 报价得分表（含排名、偏差率、得分）
  - --format json 时同时输出可机读结果；--output 落盘

安全边界：
  - 本引擎只做「按既定规则算分」，**不替用户决定报多少价**，也不臆造评标基准价；
  - 真实项目多采用复合基准（剔除极端值、二次平均等），使用前须核对招标文件原文；
  - 所有结果标注「⚠️ 需人工复核」，不得直接作为定标依据。

依赖：仅 Python 标准库。
"""

import argparse
import json
import math
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional


# ============================================================
# 数据模型
# ============================================================
@dataclass
class Quote:
    name: str
    price: float


@dataclass
class PriceResult:
    method: str
    full_score: float
    base: Optional[float]
    quotes: List[dict] = field(default_factory=list)  # [{name, price, deviation_pct, score}]
    warnings: List[str] = field(default_factory=list)

    def sorted(self):
        return sorted(self.quotes, key=lambda q: q.get("score", 0), reverse=True)


# ============================================================
# 评标基准价计算
# ============================================================
def compute_base(prices: List[float], base_cfg: dict) -> tuple[float, List[str]]:
    warnings: List[str] = []
    mode = (base_cfg or {}).get("mode", "average")
    if not prices:
        raise ValueError("报价列表为空，无法计算评标基准价")

    if mode == "fixed":
        val = float(base_cfg.get("value", 0))
        if val <= 0:
            raise ValueError("base.mode=fixed 但未提供合法的 base.value")
        return val, warnings

    if mode == "average":
        return sum(prices) / len(prices), warnings

    if mode == "median":
        s = sorted(prices)
        n = len(s)
        mid = s[n // 2]
        return (mid if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2.0), warnings

    if mode == "average_k":
        k = float(base_cfg.get("k", 1.0))
        return (sum(prices) / len(prices)) * k, warnings

    if mode == "lowest_n_avg":
        n = int(base_cfg.get("lowest_n", 3))
        if n <= 0 or n > len(prices):
            warnings.append(f"lowest_n={n} 超出有效报价数 {len(prices)}，回退为全部均值")
            return sum(prices) / len(prices), warnings
        return sum(sorted(prices)[:n]) / n, warnings

    if mode == "weighted":
        w = float(base_cfg.get("w", 0.6))
        mean = sum(prices) / len(prices)
        low = min(prices)
        return w * mean + (1 - w) * low, warnings

    warnings.append(f"未知 base.mode={mode}，回退为平均价")
    return sum(prices) / len(prices), warnings


# ============================================================
# 各算法
# ============================================================
def score_low_price_first(quotes: List[Quote], full: float) -> PriceResult:
    prices = [q.price for q in quotes]
    base = min(prices)
    res = PriceResult(method="low_price_first", full_score=full, base=base)
    for q in quotes:
        s = (base / q.price) * full if q.price > 0 else 0.0
        s = min(s, full)  # 安全钳制
        res.quotes.append({
            "name": q.name, "price": q.price,
            "deviation_pct": None,
            "score": round(s, 4)
        })
    return res


def score_benchmark(quotes: List[Quote], full: float, base_cfg: dict, ded: dict) -> PriceResult:
    prices = [q.price for q in quotes]
    base, warns = compute_base(prices, base_cfg)
    ded_above = float(ded.get("above", 0.5))
    ded_below = float(ded.get("below", 0.3))
    res = PriceResult(method="benchmark", full_score=full, base=round(base, 4), warnings=warns)
    for q in quotes:
        if base <= 0:
            res.quotes.append({"name": q.name, "price": q.price, "deviation_pct": None, "score": 0.0})
            continue
        dev = (q.price - base) / base * 100.0
        if dev >= 0:
            s = full - dev * ded_above
        else:
            s = full - abs(dev) * ded_below
        s = max(0.0, min(s, full))
        res.quotes.append({
            "name": q.name, "price": q.price,
            "deviation_pct": round(dev, 3),
            "score": round(s, 4)
        })
    return res


def score_interval(quotes: List[Quote], full: float, interval_cfg: dict) -> PriceResult:
    low = float(interval_cfg.get("low", 0))
    high = float(interval_cfg.get("high", 0))
    ded = float(interval_cfg.get("deduction_per_pct", 1.0))
    res = PriceResult(method="interval", full_score=full, base=None)
    if low <= 0 or high <= 0 or low >= high:
        res.warnings.append("interval.low/high 配置非法，结果不可信")
    for q in quotes:
        if low <= q.price <= high:
            s = full
        elif q.price < low:
            pct = (low - q.price) / q.price * 100.0 if q.price > 0 else 0
            s = full - pct * ded
        else:
            pct = (q.price - high) / high * 100.0 if high > 0 else 0
            s = full - pct * ded
        s = max(0.0, min(s, full))
        res.quotes.append({
            "name": q.name, "price": q.price,
            "deviation_pct": None,
            "score": round(s, 4)
        })
    return res


# ============================================================
# 配置解析
# ============================================================
def load_spec(args) -> dict:
    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            spec = json.load(f)
        return spec
    # CLI 快速模式
    quotes_raw = [x.strip() for x in (args.quotes or "").split(",") if x.strip()]
    prices = [float(x) for x in quotes_raw]
    names = [x.strip() for x in (args.names or "").split(",") if x.strip()]
    while len(names) < len(prices):
        names.append(f"投标人{len(names)+1}")
    quotes = [Quote(name=names[i], price=prices[i]) for i in range(len(prices))]
    return {
        "method": args.method or "low_price_first",
        "full_score": float(args.full_score or 30),
        "base": {"mode": args.base_mode or "average"},
        "deduction": {"above": float(args.ded_above or 0.5), "below": float(args.ded_below or 0.3)},
        "interval": {"low": float(args.interval_low or 0), "high": float(args.interval_high or 0)},
        "quotes": [{"name": q.name, "price": q.price} for q in quotes],
    }


def run(spec: dict) -> PriceResult:
    method = spec.get("method", "low_price_first")
    full = float(spec.get("full_score", 30))
    quotes = [Quote(name=q.get("name", "?"), price=float(q["price"])) for q in spec.get("quotes", [])]
    if not quotes:
        raise ValueError("spec.quotes 为空")
    if method == "low_price_first":
        return score_low_price_first(quotes, full)
    if method == "benchmark":
        return score_benchmark(quotes, full, spec.get("base", {}), spec.get("deduction", {}))
    if method == "interval":
        return score_interval(quotes, full, spec.get("interval", {}))
    raise ValueError(f"未知 method={method}（支持 low_price_first / benchmark / interval）")


# ============================================================
# 输出
# ============================================================
def render_table(res: PriceResult) -> str:
    lines = []
    lines.append(f"### 价格分计算结果（{res.method}，满分 {res.full_score}）")
    if res.base is not None:
        lines.append(f"- 评标基准价（计算值）：**{res.base:,.4f}**  ⚠️ 需人工复核是否与招标文件规则一致")
    for w in res.warnings:
        lines.append(f"- ⚠️ 注意：{w}")
    lines.append("")
    lines.append("| 排名 | 投标人 | 报价 | 偏差率(%) | 价格分 |")
    lines.append("|---|---|---|---|---|")
    for i, q in enumerate(res.sorted(), 1):
        dev = "" if q["deviation_pct"] is None else f"{q['deviation_pct']:+.3f}"
        lines.append(f"| {i} | {q['name']} | {q['price']:,.2f} | {dev} | {q['score']:.4f} |")
    lines.append("")
    lines.append("> ⚠️ 本表为依据既定规则的自动算分结果，**不构成报价建议**；真实评标基准价计算（剔除极端值、二次平均等）以招标文件原文为准，投标报价与商务策略须由用户决策。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="智慧招采专家 · 价格分自动算分引擎")
    ap.add_argument("--method", choices=["low_price_first", "benchmark", "interval"],
                    help="算分算法")
    ap.add_argument("--quotes", help="报价列表，逗号分隔，如 980,1000,1020,950")
    ap.add_argument("--names", help="投标人名称，逗号分隔，与 quotes 对齐")
    ap.add_argument("--full-score", type=float, help="价格分满分")
    ap.add_argument("--base-mode", help="benchmark 基准价算法 average/average_k/median/lowest_n_avg/weighted/fixed")
    ap.add_argument("--ded-above", type=float, help="benchmark 高于基准价每 1% 扣分值")
    ap.add_argument("--ded-below", type=float, help="benchmark 低于基准价每 1% 扣分值")
    ap.add_argument("--interval-low", type=float, help="interval 区间下限")
    ap.add_argument("--interval-high", type=float, help="interval 区间上限")
    ap.add_argument("--config", help="JSON 配置文件路径（结构与 demo/price_config.json 一致）")
    ap.add_argument("--format", choices=["table", "json"], default="table")
    ap.add_argument("--output", help="结果落盘路径（json 模式写 JSON，table 模式写 md）")
    args = ap.parse_args()

    try:
        spec = load_spec(args)
        res = run(spec)
    except Exception as e:
        print(f"[错误] {e}", file=sys.stderr)
        sys.exit(1)

    if args.format == "json":
        out = {
            "method": res.method,
            "full_score": res.full_score,
            "base": res.base,
            "warnings": res.warnings,
            "ranked": res.sorted(),
        }
        text = json.dumps(out, ensure_ascii=False, indent=2)
    else:
        text = render_table(res)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[OK] 已写入 {args.output}")
    else:
        print(text)


if __name__ == "__main__":
    main()
