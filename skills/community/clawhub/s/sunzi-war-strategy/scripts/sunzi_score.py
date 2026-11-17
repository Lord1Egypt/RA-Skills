#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sunzi_score.py  v1.2.1
孙子兵法六维评分计算器。
输入子项数据（dict），输出各维得分（0-10 clamp）+ 兵法总分（归一化 0-10）。

用法：
  python3 sunzi_score.py --json '{"price":21.12,"prev_close":21.59,...}'
  python3 sunzi_score.py --demo
  python3 sunzi_score.py --config config.yaml   # 读取仓位配置
"""

import json
import sys
import argparse
import os
import math


# ── 工具 ────────────────────────────────────────────────────────────
def clamp(v, lo=0, hi=10):
    return max(lo, min(hi, round(v, 1)))


def safe_get(d, key, default=None):
    return d.get(key, default)


# ── 六维评分（基准分 5 + 加减分，clamp 0-10）──────────────────────
def score_ji(m):
    """计篇·综合评估"""
    s = 5.0
    mt = m.get("market_trend", "震荡")
    s += {"多": 3, "震荡": 1, "空": -2}.get(mt, 0)
    sec = m.get("sector_strength", "平")
    s += {"强": 3, "平": 1, "弱": -2}.get(sec, 0)
    if all(k in m for k in ("ma5", "ma10", "ma20")):
        if m["ma5"] > m["ma10"] > m["ma20"]: s += 2
        elif m["ma5"] < m["ma10"] < m["ma20"]: s -= 2
    cat = m.get("catalyst", "概念")
    s += {"利好": 2, "概念": 0, "利空": -3}.get(cat, 0)
    return clamp(s)


def score_shi(m):
    """势篇·造势"""
    s = 5.0
    if all(k in m for k in ("ma5", "ma10", "ma20")):
        if m["ma5"] > m["ma10"] > m["ma20"]: s += 3
        elif m["ma5"] < m["ma10"] < m["ma20"]: s -= 3
    # 放量突破
    vr = m.get("volume_ratio", 0)
    if vr and m.get("new_20d_high"):
        if vr > 1.5 and m["new_20d_high"]: s += 3
    # 收盘站稳
    if m.get("price") and m.get("prev_close"):
        if m["price"] > m["prev_close"]: s += 1.5
    rsi = m.get("rsi14")
    if rsi is not None:
        if 50 <= rsi <= 70: s += 1
        elif rsi > 80: s -= 2
        # <30 超卖：弱势信号，不给正向分，保持基准
    # 势尽信号
    if m.get("long_upper_shadow"): s -= 3
    tr = m.get("turnover_rate", 0)
    if tr and m.get("price") and m.get("high"):
        if m["price"] < m["high"] * 0.97:  # 回落超3% = 滞涨
            s -= 2
    return clamp(s)


def score_xu_shi(m):
    """虚实篇·避实击虚（换手率分三档）"""
    s = 5.0
    g20 = m.get("gain_20d")
    if g20 is not None:
        if g20 > 30: s -= 3
        elif g20 < 10: s += 2
    # 换手率分档
    tr = m.get("turnover_rate")
    cap = m.get("float_cap", 200)  # 默认中盘200亿
    if tr is not None:
        if cap < 50:          # 小盘
            if 5 <= tr <= 15: s += 2
            else: s -= 2
        elif cap <= 500:      # 中盘
            if 3 <= tr <= 8: s += 2
            else: s -= 2
        else:                 # 大盘
            if 1 <= tr <= 5: s += 2
            else: s -= 2
    # 估值
    pe = m.get("pe_ratio"); ipe = m.get("industry_pe")
    if pe and ipe and ipe > 0 and pe > ipe * 1.5: s -= 2
    pb = m.get("pb_ratio"); ipb = m.get("industry_pb")
    if pb and ipb and ipb > 0 and pb > ipb * 1.5: s -= 1
    # 筹码位置
    p, h60, l60 = m.get("price"), m.get("high_60d"), m.get("low_60d")
    if p and h60 and h60 > 0 and (h60 - p) / h60 < 0.10: s -= 1
    if p and l60 and l60 > 0 and (p - l60) / p < 0.15: s += 2
    return clamp(s)


def score_jun_zheng(m, total_score, cfg):
    """军争篇·兵力（依赖兵法总分）"""
    s = 5.0
    if total_score >= 8: s += 3
    elif total_score >= 6: s += 1
    else: s -= 3
    pc = m.get("position_count", 0)
    if pc and pc > cfg.get("max_positions", 8): s -= 2
    cr = m.get("cash_ratio")
    if cr is not None and cr < cfg.get("min_cash_ratio", 0.20): s -= 2
    return clamp(s)


def score_jiu_bian(m):
    """九变篇·应变"""
    s = 5.0
    if m.get("has_stop_loss"): s += 2
    if m.get("has_take_profit"): s += 2
    if m.get("has_black_swan_plan"): s += 1
    vol = m.get("volatility", 0)
    if vol and vol > 6: s -= 2
    return clamp(s)


def score_yong_jian(m):
    """用间篇·情报验证"""
    s = 5.0
    if m.get("news_conflict"): s -= 3
    if m.get("company_denial"): s -= 2
    if m.get("insider_buy"): s += 2
    if m.get("institutional_inflow"): s += 1.5
    if m.get("supervision_inquiry"): s -= 2
    if m.get("large_holder_pledged"): s -= 2
    if m.get("large_holder_increase"): s += 2
    return clamp(s)


# ── 主流程 ──────────────────────────────────────────────────────────
def compute(data, cfg=None):
    if cfg is None:
        cfg = {}
    scores = {
        "计篇_综合评估": score_ji(data),
        "势篇_造势": score_shi(data),
        "虚实篇": score_xu_shi(data),
        "九变篇": score_jiu_bian(data),
        "用间篇": score_yong_jian(data),
    }
    # 军争篇依赖兵法总分，先算其余五维
    weights = {
        "计篇_综合评估": 0.25,
        "势篇_造势": 0.20,
        "虚实篇": 0.20,
        "军争篇": 0.15,
        "九变篇": 0.15,
        "用间篇": 0.05,
    }
    # 五维加权（不含军争篇）
    partial = sum(scores[k] * weights[k] for k in scores)
    # 兵法总分（归一化）= (partial + 军争×0.15) / 1.0
    # 先估算军争分（用总分预估值）
    est_total = partial / (1 - weights["军争篇"])
    scores["军争篇"] = score_jun_zheng(data, est_total, cfg)
    total = sum(scores[k] * weights[k] for k in scores)
    total = round(total, 1)

    if total >= 8:
        verdict = "胜（可重仓出击）"
        pos = f"≤{int(cfg.get('single_position_max_high', 0.20)*100)}% 总仓"
    elif total >= 6:
        verdict = "可战（轻仓试探）"
        pos = f"≤{int(cfg.get('single_position_max_mid', 0.10)*100)}% 总仓"
    else:
        verdict = "不战（庙算不足）"
        pos = "0%（不建仓）"

    return {
        "scores": scores,
        "total": total,
        "verdict": verdict,
        "position": pos,
        "weights": weights,
    }


def load_config(path="config.yaml"):
    try:
        import yaml
        with open(path) as f:
            return yaml.safe_load(f)
    except Exception:
        return {}


def main():
    parser = argparse.ArgumentParser(description="孙子兵法六维评分 v1.1.0")
    parser.add_argument("--json", help="行情数据 JSON")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")
    parser.add_argument("--demo", action="store_true", help="跑和而泰示例")
    args = parser.parse_args()

    cfg = load_config(args.config)

    if args.demo:
        data = {
            "price": 21.12, "prev_close": 21.59, "high": 21.88, "low": 21.12,
            "volume_ratio": 0.8, "new_20d_high": False,
            "rsi14": 50.6, "turnover_rate": 1.1, "float_cap": 198,
            "gain_20d": -5, "high_60d": 60.71, "low_60d": 18.92,
            "pe_ratio": 30.25, "industry_pe": 33.35,
            "pb_ratio": 2.88, "industry_pb": 2.27,
            "market_trend": "震荡", "sector_strength": "强",
            "catalyst": "利好", "long_upper_shadow": False,
            "has_stop_loss": True, "has_take_profit": True,
            "has_black_swan_plan": True,
            "news_conflict": False, "company_denial": False,
            "supervision_inquiry": False, "large_holder_pledged": True,
            "position_count": 10, "cash_ratio": 0.34,
        }
    else:
        if not args.json:
            print("用法: --json '{...}' 或 --demo", file=sys.stderr)
            sys.exit(1)
        data = json.loads(args.json)

    result = compute(data, cfg)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
