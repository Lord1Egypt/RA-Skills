"""
chart.py — Step 4: Render a 4-panel K-line chart using matplotlib (Agg backend).

Panels: Candlestick + MAs + Bollinger | Volume | MACD | RSI-14

Usage:
    from chart import plot_kline
    plot_kline(df_daily, code="000063", name="中兴通讯", out_path="kline.png")

Requires df_daily to already have indicators applied (via indicators.add_indicators).
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")  # non-interactive; must be set before pyplot import
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker
import pandas as pd


# ── Theme ────────────────────────────────────────────────────────────────────
BG       = "#1a1a2e"
GRID     = "#2a2a4a"
COL_UP   = "#26a69a"
COL_DOWN = "#ef5350"


def _style_ax(ax: plt.Axes) -> None:
    ax.set_facecolor(BG)
    ax.tick_params(colors="#aaaacc", labelsize=8)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(GRID)
    ax.yaxis.grid(True, color=GRID, linewidth=0.5)
    ax.xaxis.grid(True, color=GRID, linewidth=0.5, alpha=0.3)


def plot_kline(
    df: pd.DataFrame,
    code: str,
    name: str,
    out_path: str = "kline.png",
    market_label: str = "A股",
    dpi: int = 130,
) -> str:
    """
    Generate and save a 4-panel K-line chart.

    Parameters
    ----------
    df         : Daily OHLCV frame with indicator columns added.
    code       : Stock symbol string, e.g. "000063".
    name       : Human-readable stock name, e.g. "中兴通讯".
    out_path   : File path for the saved PNG.
    market_label: Short label shown in chart title.
    dpi        : Output resolution.

    Returns
    -------
    out_path   : The path the chart was saved to.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])
    xs = mdates.date2num(df["date"])
    bar_w = 0.6

    fig, axes = plt.subplots(
        4, 1, figsize=(16, 14),
        gridspec_kw={"height_ratios": [4, 1.2, 1.2, 1]},
        facecolor=BG,
    )
    fig.subplots_adjust(hspace=0.05)
    axp, axv, axm, axr = axes

    for ax in axes:
        _style_ax(ax)

    # ── Panel 0: Candlesticks + MAs + Bollinger ──────────────────────────────
    for _, row in df.iterrows():
        x = mdates.date2num(row["date"])
        c = COL_UP if row["close"] >= row["open"] else COL_DOWN
        axp.plot([x, x], [row["low"], row["high"]], color=c, linewidth=0.8)
        axp.add_patch(plt.Rectangle(
            (x - bar_w / 2, min(row["open"], row["close"])),
            bar_w, abs(row["close"] - row["open"]),
            color=c, zorder=3,
        ))

    axp.plot(xs, df["ma5"],      color="#2196F3", lw=0.9, label="MA5",    alpha=0.9)
    axp.plot(xs, df["ma20"],     color="#FF9800", lw=0.9, label="MA20",   alpha=0.9)
    axp.plot(xs, df["ma60"],     color="#CE93D8", lw=0.9, label="MA60",   alpha=0.9)
    axp.plot(xs, df["bb_upper"], color="#90CAF9", lw=0.7, ls="--", alpha=0.7, label="BB±2σ")
    axp.plot(xs, df["bb_lower"], color="#90CAF9", lw=0.7, ls="--", alpha=0.7)
    axp.plot(xs, df["bb_mid"],   color="#90CAF9", lw=0.4, ls=":",  alpha=0.5)
    axp.fill_between(xs, df["bb_upper"], df["bb_lower"], alpha=0.05, color="#2196F3")

    axp.set_title(
        f"{name} ({code}) · {market_label} · 日线 6个月 · 前复权",
        color="white", fontsize=13,
    )
    axp.legend(loc="upper left", fontsize=7.5, facecolor=BG, edgecolor=GRID, labelcolor="#ccccdd")
    axp.xaxis.set_major_formatter(mdates.DateFormatter("%y/%m"))
    axp.xaxis.set_major_locator(mdates.MonthLocator())
    axp.set_xlim(xs[0] - 1, xs[-1] + 1)
    axp.tick_params(labelbottom=False)
    last_close = df["close"].iloc[-1]
    axp.annotate(
        f"¥{last_close:.2f}", xy=(xs[-1], last_close),
        fontsize=8, color="yellow", ha="right",
    )

    # ── Panel 1: Volume ───────────────────────────────────────────────────────
    vol_colors = [
        COL_UP if df["close"].iloc[i] >= df["open"].iloc[i] else COL_DOWN
        for i in range(len(df))
    ]
    axv.bar(xs, df["volume"], color=vol_colors, width=bar_w, alpha=0.75)
    axv.plot(xs, df["volume"].rolling(20).mean(), color="#FF9800", lw=0.8, alpha=0.8)
    axv.set_ylabel("Vol", color="#aaaacc", fontsize=8)
    axv.set_xlim(xs[0] - 1, xs[-1] + 1)
    axv.tick_params(labelbottom=False)
    axv.yaxis.set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: f"{x / 1e6:.0f}M")
    )

    # ── Panel 2: MACD ─────────────────────────────────────────────────────────
    axm.plot(xs, df["macd"],        color="#4CAF50", lw=0.9, label="MACD")
    axm.plot(xs, df["macd_signal"], color="#F44336", lw=0.9, label="Signal")
    hist_colors = ["#26a69a" if v >= 0 else "#ef5350" for v in df["macd_hist"]]
    axm.bar(xs, df["macd_hist"], color=hist_colors, width=bar_w, alpha=0.6)
    axm.axhline(0, color=GRID, lw=0.6)
    axm.set_ylabel("MACD", color="#aaaacc", fontsize=8)
    axm.legend(loc="upper left", fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor="#ccccdd")
    axm.set_xlim(xs[0] - 1, xs[-1] + 1)
    axm.tick_params(labelbottom=False)

    # ── Panel 3: RSI-14 ───────────────────────────────────────────────────────
    axr.plot(xs, df["rsi14"], color="#00BCD4", lw=0.9, label="RSI-14")
    axr.axhline(70, color="#ef5350", lw=0.6, ls="--", alpha=0.7)
    axr.axhline(30, color="#4CAF50", lw=0.6, ls="--", alpha=0.7)
    axr.axhline(50, color=GRID, lw=0.4, ls=":")
    axr.fill_between(xs, df["rsi14"], 70, where=(df["rsi14"] > 70), alpha=0.3, color="#ef5350")
    axr.fill_between(xs, df["rsi14"], 30, where=(df["rsi14"] < 30), alpha=0.3, color="#4CAF50")
    axr.set_ylim(0, 100)
    axr.set_ylabel("RSI-14", color="#aaaacc", fontsize=8)
    axr.set_xlim(xs[0] - 1, xs[-1] + 1)
    axr.xaxis.set_major_formatter(mdates.DateFormatter("%y/%m"))
    axr.xaxis.set_major_locator(mdates.MonthLocator())
    axr.legend(loc="upper left", fontsize=7, facecolor=BG, edgecolor=GRID, labelcolor="#ccccdd")

    plt.tight_layout()
    plt.savefig(out_path, dpi=dpi, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"[chart] Saved → {out_path}")
    return out_path


# ── Quick smoke-test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    sys.path.insert(0, __file__.rsplit("/", 1)[0])
    from fetch_kline import fetch_all_timeframes
    from indicators import add_indicators

    symbol = sys.argv[1] if len(sys.argv) > 1 else "000063"
    name   = sys.argv[2] if len(sys.argv) > 2 else symbol
    df_d, _, _ = fetch_all_timeframes(symbol)
    df_d = add_indicators(df_d)
    plot_kline(df_d, code=symbol, name=name, out_path=f"{symbol}_kline.png")
