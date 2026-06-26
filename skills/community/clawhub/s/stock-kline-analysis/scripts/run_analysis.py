"""
run_analysis.py — End-to-end orchestrator for the stock-kline-analysis skill.

Runs Steps 1–8: resolve → fetch → indicators → chart → valuation → events → output.

Usage:
    python run_analysis.py 000063
    python run_analysis.py 贵州茅台
    python run_analysis.py AAPL
    python run_analysis.py 000063 --out-dir /tmp/reports
"""

from __future__ import annotations

import argparse
import sys
import os
import numpy as np
from datetime import date, timedelta
from pathlib import Path

# Allow running from any working directory
_SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(_SCRIPTS_DIR))

import akshare as ak
from fetch_kline  import fetch_all_timeframes
from indicators   import add_indicators, add_tf_indicators
from chart        import plot_kline
from valuation    import fetch_valuation, compute_pe_pb
from events       import fetch_events


# ────────────────────────────────────────────────────────────────────────────
# Step 1 — Resolve Identifier
# ────────────────────────────────────────────────────────────────────────────

def resolve_symbol(raw: str) -> tuple[str, str, str]:
    """
    Return (code, name, market_label).

    Auto-detection rules:
      6-digit starting with 6      → A-share Shanghai
      6-digit starting with 0 or 3 → A-share Shenzhen
      5-digit starting with 0      → HK
      letters (4-5 chars)          → US
      otherwise                    → search A-share name list
    """
    raw = raw.strip()

    # Purely numeric
    if raw.isdigit():
        if len(raw) == 6:
            if raw.startswith("6"):
                market = "A股上交所"
            else:
                market = "A股深交所"
            # Confirm name via symbol list
            try:
                sym_df = ak.stock_info_a_code_name()
                hit = sym_df[sym_df["code"] == raw]
                name = hit["name"].iloc[0] if not hit.empty else raw
            except Exception:
                name = raw
            return raw, name, market
        if len(raw) == 5 and raw.startswith("0"):
            return raw, raw, "港股 HK"

    # Letters → US
    if raw.isalpha() and 1 <= len(raw) <= 5:
        return raw.upper(), raw.upper(), "美股 US"

    # Chinese name → search A-share list
    try:
        sym_df = ak.stock_info_a_code_name()
        # Exact match first, then substring
        exact = sym_df[sym_df["name"] == raw]
        if not exact.empty:
            code = exact["code"].iloc[0]
            return resolve_symbol(code)  # re-enter with numeric code
        partial = sym_df[sym_df["name"].str.contains(raw, na=False)]
        if len(partial) == 1:
            code = partial["code"].iloc[0]
            return resolve_symbol(code)
        if len(partial) > 1:
            candidates = partial.head(3)[["code", "name"]].to_string(index=False)
            raise ValueError(
                f"Ambiguous name '{raw}'. Top matches:\n{candidates}\n"
                "Please re-run with the exact 6-digit code."
            )
    except ValueError:
        raise
    except Exception as e:
        print(f"[resolve] Symbol list lookup failed: {e}")

    raise ValueError(f"Cannot resolve '{raw}' to a known stock symbol.")


# ────────────────────────────────────────────────────────────────────────────
# Step 8 — Format structured output
# ────────────────────────────────────────────────────────────────────────────

def _pct(val) -> str:
    return f"{val:+.1f}%" if val is not None and not np.isnan(val) else "N/A"


def _fmt(val, decimals=2, prefix="¥") -> str:
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    return f"{prefix}{val:.{decimals}f}"


def format_output(
    code: str, name: str, market_label: str,
    df_daily, df_weekly, df_monthly,
    val: dict,
    event_lines: list[str],
) -> str:
    last   = df_daily.iloc[-1]
    prev   = df_daily.iloc[-2]
    today  = date.today()

    pct_chg  = (last["close"] - prev["close"]) / prev["close"] * 100
    abs_chg  = last["close"] - prev["close"]
    vol_avg20 = df_daily["volume"].tail(20).mean()
    vol_ratio = last["volume"] / vol_avg20

    r5   = (last["close"] / df_daily["close"].iloc[-6]  - 1) * 100
    r10  = (last["close"] / df_daily["close"].iloc[-11] - 1) * 100
    r20  = (last["close"] / df_daily["close"].iloc[-21] - 1) * 100
    ann_vol = df_daily["close"].pct_change().tail(60).std() * np.sqrt(252) * 100

    high20 = df_daily["high"].tail(20).max()
    low20  = df_daily["low"].tail(20).min()

    ma_bull = (
        last["close"] > last["ma5"] > last["ma20"] > last["ma60"]
        if not any(np.isnan(v) for v in [last["ma5"], last["ma20"], last["ma60"]])
        else False
    )
    ma_stack = "排列多头 Bullish stack" if ma_bull else "空头排列 Bearish stack"

    # Multi-timeframe
    w_trend = m_trend = "N/A"
    if df_weekly is not None and "ma20" in df_weekly.columns:
        wl = df_weekly.iloc[-1]
        w_trend = "Uptrend ✓" if wl["close"] > wl["ma20"] else "Downtrend ✗"
    if df_monthly is not None and "ma20" in df_monthly.columns:
        ml = df_monthly.iloc[-1]
        m_trend = "Uptrend ✓" if ml["close"] > ml["ma20"] else "Holding Support (above MA20) ✓" \
            if ml["close"] >= ml["ma20"] * 0.98 else "Downtrend ✗"

    # MACD direction
    hist_last5 = df_daily["macd_hist"].tail(5).tolist()
    macd_desc = (
        "MACD & Signal below zero; histogram converging → bearish momentum fading"
        if last["macd"] < 0 and abs(last["macd_hist"]) < 0.05
        else "MACD above Signal, histogram positive → bullish momentum"
        if last["macd"] > last["macd_signal"] and last["macd_hist"] > 0
        else "MACD below Signal, histogram negative → bearish momentum"
    )

    # BB squeeze
    bb_desc = (
        "Squeeze — band narrowing, breakout pending"
        if last["bb_width"] < 10
        else "Expanding — volatility breakout in progress"
        if last["bb_width"] > 20
        else "Normal bandwidth"
    )

    trailing_stop = last["close"] - 1.5 * last["atr14"]

    start_date = df_daily["date"].iloc[0]

    lines = [
        "",
        "═" * 65,
        f"  {name} ({code}) · K线分析报告",
        "═" * 65,
        "",
        "[Symbol Summary]",
        f"  名称/代码   : {name} ({code}) · {market_label}",
        f"  分析区间   : {start_date} → {today} (日线 6M, 前复权 qfq)",
        f"  多周期确认 : Weekly: {w_trend}  |  Monthly: {m_trend}",
        "",
        "[K-Line Snapshot]",
        f"  最新收盘         : ¥{last['close']:.2f}",
        f"  1日涨跌          : {pct_chg:+.2f}%  ({abs_chg:+.2f})",
        f"  MA5 / MA20 / MA60: ¥{last['ma5']:.2f} / ¥{last['ma20']:.2f} / ¥{last['ma60']:.2f}  ({ma_stack})",
        f"  布林带 Bollinger : Upper ¥{last['bb_upper']:.2f} | Mid ¥{last['bb_mid']:.2f} | Lower ¥{last['bb_lower']:.2f}  (Width: {last['bb_width']:.1f}%)",
        f"  ATR-14 (波动幅)  : ¥{last['atr14']:.2f}/day  ({last['atr_pct']:.1f}% of price)",
        f"  20日区间         : ¥{low20:.2f} – ¥{high20:.2f}",
        f"  成交量 vs 20日均 : {(vol_ratio-1)*100:+.0f}%  ({'放量' if vol_ratio > 1.2 else '缩量' if vol_ratio < 0.8 else '平量'})",
        "",
        "[Technical View — 技术面]",
        f"  趋势 Trend   : {ma_stack}",
        f"                 Weekly: {w_trend}",
        f"                 Monthly: {m_trend}",
        f"  动量 Momentum: 5D {_pct(r5)} | 10D {_pct(r10)} | 20D {_pct(r20)} | Ann.Vol {ann_vol:.1f}%",
        f"  MACD         : {macd_desc}",
        f"                 Hist(last 5): {[round(h,4) for h in hist_last5]}",
        f"  RSI-14       : {last['rsi14']:.1f}  ({'超买 overbought' if last['rsi14']>70 else '超卖 oversold' if last['rsi14']<30 else '中性 neutral'})",
        f"  BB Squeeze   : Width {last['bb_width']:.1f}% — {bb_desc}",
        f"  支撑 Support : ¥{df_daily.attrs.get('support', 0):.2f}",
        f"  阻力 Resist  : ¥{df_daily.attrs.get('resistance', 0):.2f}",
        f"  ATR止损参考  : last close − 1.5×ATR = ¥{last['close']:.2f} − ¥{1.5*last['atr14']:.2f} ≈ ¥{trailing_stop:.2f}",
    ]

    # Valuation
    lines += ["", "[Valuation — 估值]"]
    if val.get("pe_ttm") is not None:
        lines.append(f"  PE (TTM)  : {val['pe_ttm']}x  (EPS ¥{val.get('eps','N/A')})")
    else:
        lines.append("  PE (TTM)  : N/A (EPS unavailable)")
    if val.get("pb") is not None:
        lines.append(f"  PB        : {val['pb']}x  (BVPS ¥{val.get('book_value_per_share','N/A')})")
    lines += [
        f"  ROE       : {val.get('roe','N/A')}%",
        f"  毛利率    : {val.get('gross_margin','N/A')}%",
        f"  营收 YoY  : {_pct(val.get('revenue_yoy'))}",
        f"  净利 YoY  : {_pct(val.get('net_profit_yoy'))}",
        f"  行业      : {val.get('industry','N/A')}",
        f"  最新公告  : {val.get('report_date','N/A')}",
        "  (历史PE百分位: 不可用 — stock_a_lg_indicator 接口已下线)",
    ]

    # Events
    lines += ["", "[Event Overlay — 事件]"]
    lines += event_lines

    # Risk
    lines += [
        "",
        "[Risk & Watchpoints — 风险]",
        f"  多单失效   : 若收盘跌破 MA20 (¥{last['ma20']:.2f}) + 放量 → 趋势走弱",
        f"  布林下轨   : 跌破 BB Lower (¥{last['bb_lower']:.2f}) = 下行波动放大",
        f"  RSI超买    : RSI {last['rsi14']:.1f}{'  — 接近超买，注意回调' if last['rsi14'] > 65 else '  — 中性区，无明显超买'}",
        f"  ATR止损    : 仓位管理参考 1 ATR = ¥{last['atr14']:.2f}",
        f"  突破条件   : 重返 MA20 (¥{last['ma20']:.2f}) + MACD金叉 + 成交量 >+50% → 反转确认",
        "",
        "  ⚠ 本报告仅供信息参考，不构成任何投资建议。",
        "═" * 65,
        "",
    ]

    return "\n".join(lines)


# ────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────

def run(raw_input: str, out_dir: str = ".") -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Step 1 — Resolve
    print(f"[run] Resolving '{raw_input}' ...")
    code, name, market_label = resolve_symbol(raw_input)
    print(f"[run] → {name} ({code}) · {market_label}")

    # Step 2 — Fetch
    print("[run] Fetching K-line data ...")
    df_daily, df_weekly, df_monthly = fetch_all_timeframes(code)

    # Step 3 — Indicators
    print("[run] Computing indicators ...")
    df_daily = add_indicators(df_daily)
    df_weekly, df_monthly = add_tf_indicators(df_weekly, df_monthly)

    # Step 4 — Chart
    chart_path = str(out_dir / f"{code}_kline.png")
    print("[run] Rendering chart ...")
    plot_kline(df_daily, code=code, name=name, market_label=market_label, out_path=chart_path)

    # Step 5 — Valuation
    print("[run] Fetching valuation ...")
    val = fetch_valuation(code)
    val = compute_pe_pb(val, last_close=float(df_daily["close"].iloc[-1]))

    # Step 7 — Events
    print("[run] Fetching events ...")
    event_lines = fetch_events()

    # Step 8 — Output
    report = format_output(
        code, name, market_label,
        df_daily, df_weekly, df_monthly,
        val, event_lines,
    )
    print(report)

    # Optionally save report text
    report_path = out_dir / f"{code}_analysis.txt"
    report_path.write_text(report, encoding="utf-8")
    print(f"[run] Report saved → {report_path}")
    print(f"[run] Chart saved  → {chart_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock K-Line Analysis")
    parser.add_argument("symbol", help="Stock code (e.g. 000063) or name (e.g. 中兴通讯) or US ticker (e.g. AAPL)")
    parser.add_argument("--out-dir", default=".", help="Directory for output files (default: current dir)")
    args = parser.parse_args()
    run(args.symbol, out_dir=args.out_dir)
