"""
分析器 — 三种模式的高层 API。
"""
from __future__ import annotations

from dataclasses import dataclass

from .announcements import fetch_announcements
from .data_sources import fetch_hist_kline, fetch_realtime
from .indicators import (
    calc_composite_score,
    calc_history_features,
    derive_stop_loss,
)
from .portfolio import (
    calc_position_metrics,
    load_portfolio,
    resolve_portfolio_path,
)
from .renderers import render_multi, render_portfolio, render_single


@dataclass
class AnalysisResult:
    mode: str
    markdown: str
    raw: dict | list

    def __str__(self) -> str:
        return self.markdown


def analyze_single(code: str) -> AnalysisResult:
    """模式 S：单股深度分析"""
    rt_map = fetch_realtime([code])
    rt = rt_map.get(code) or {}
    df = fetch_hist_kline(code)
    hist = calc_history_features(df) if df is not None else {}
    md = render_single(code, rt, hist)
    return AnalysisResult(
        mode="single",
        markdown=md,
        raw={"code": code, "realtime": rt, "hist": hist},
    )


def analyze_multi(codes: list[str]) -> AnalysisResult:
    """模式 M：多股对比分析"""
    rt_map = fetch_realtime(codes)
    rows = []
    for code in codes:
        rt = rt_map.get(code) or {}
        df = fetch_hist_kline(code)
        hist = calc_history_features(df) if df is not None else {}
        if not rt or not hist:
            continue
        last = hist.get("last") or rt.get("price") or 0
        ma5 = hist.get("ma5") or last
        ma20 = hist.get("ma20") or last
        rows.append({
            "code": code,
            "name": rt.get("name", code),
            "price": rt.get("price"),
            "pct": rt.get("pct_change"),
            "ma5_dev": round((last - ma5) / ma5 * 100, 2) if ma5 else 0,
            "ma20_dev": round((last - ma20) / ma20 * 100, 2) if ma20 else 0,
            "turnover": rt.get("turnover_rate"),
            "pct_40d": hist.get("pct_40d"),
            "score": calc_composite_score(rt, hist),
        })
    md = render_multi(rows)
    return AnalysisResult(mode="multi", markdown=md, raw=rows)


def analyze_portfolio(
    portfolio_path: str | None = None,
    skip_announce: bool = False,
) -> AnalysisResult:
    """模式 P：持仓简报"""
    path = resolve_portfolio_path(portfolio_path)
    if not path:
        raise FileNotFoundError(
            "未找到 portfolio.json。请通过 --portfolio 参数、"
            "STOCK_BRIEF_PORTFOLIO 环境变量、或在当前目录放置 portfolio.json"
        )

    holdings, total_margin = load_portfolio(path)
    codes = [h["code"] for h in holdings]
    rt_map = fetch_realtime(codes)
    holdings, total_mv = calc_position_metrics(holdings, rt_map)

    # 历史 K 线 + 止损 + 公告
    for h in holdings:
        df = fetch_hist_kline(h["code"])
        h["hist"] = calc_history_features(df) if df is not None else {}
        h["sl"] = derive_stop_loss(
            h["rt"], h["hist"],
            is_heavy=h.get("is_heavy", False),
            has_margin=h.get("has_margin", False),
            cost=h.get("cost"),
        )
        if not skip_announce:
            ann = fetch_announcements(h["code"], days=14)
            h["announce"] = [a for a in ann if a.get("level") in ("HIGH", "MED")]
        else:
            h["announce"] = []

    md = render_portfolio(holdings, total_mv, total_margin)
    return AnalysisResult(
        mode="portfolio",
        markdown=md,
        raw={"holdings": holdings, "total_mv": total_mv, "total_margin": total_margin},
    )
