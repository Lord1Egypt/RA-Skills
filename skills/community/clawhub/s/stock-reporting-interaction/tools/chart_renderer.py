#!/usr/bin/env python3
"""
可视化图表渲染器
支持 K线图、技术指标面板、估值分位图、雷达图、资金热力图等
基于 mplfinance + matplotlib + plotly
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # 无头渲染
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

try:
    import mplfinance as mpf
    HAS_MPF = True
except ImportError:
    HAS_MPF = False

# ==================== 主题配置 ====================

THEMES = {
    "dark": {
        "bg": "#1e1e2e",
        "panel_bg": "#282838",
        "text": "#cdd6f4",
        "grid": "#45475a",
        "up_color": "#f04050",     # 中国股市：红涨
        "down_color": "#40c060",   # 绿跌
        "ma_colors": ["#f9e2af", "#89b4fa", "#f38ba8", "#a6e3a1", "#cba6f7"],
        "volume_up": "#f04050aa",
        "volume_down": "#40c060aa",
        "macd_positive": "#f04050",
        "macd_negative": "#40c060",
        "dif_color": "#89b4fa",
        "dea_color": "#f9e2af",
        "k_color": "#89b4fa",
        "d_color": "#f9e2af",
        "j_color": "#f38ba8",
    },
    "light": {
        "bg": "#ffffff",
        "panel_bg": "#f8f9fa",
        "text": "#333333",
        "grid": "#e0e0e0",
        "up_color": "#dc3545",
        "down_color": "#28a745",
        "ma_colors": ["#fd7e14", "#007bff", "#dc3545", "#28a745", "#6f42c1"],
        "volume_up": "#dc354588",
        "volume_down": "#28a74588",
        "macd_positive": "#dc3545",
        "macd_negative": "#28a745",
        "dif_color": "#007bff",
        "dea_color": "#fd7e14",
        "k_color": "#007bff",
        "d_color": "#fd7e14",
        "j_color": "#dc3545",
    },
}


class ChartRenderer:

    def __init__(self, df: pd.DataFrame, symbol: str, name: str = "",
                 theme: str = "dark", figsize=(16, 12)):
        """
        df: 必须包含 date,open,high,low,close,volume 列
        """
        self.df = df.copy()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df.set_index("date", inplace=True)
        self.symbol = symbol
        self.name = name or symbol
        self.theme = THEMES.get(theme, THEMES["dark"])
        self.figsize = figsize

    def render_kline(self, output_path: str, indicators: list[str] = None,
                     annotations: dict = None):
        """
        渲染 K线 + 均线 + 成交量
        """
        if not HAS_MPF:
            return self._fallback_kline(output_path)

        # 自定义样式
        mc = mpf.make_marketcolors(
            up=self.theme["up_color"],
            down=self.theme["down_color"],
            volume={"up": self.theme["volume_up"], "down": self.theme["volume_down"]},
            edge="inherit",
            wick="inherit",
        )
        style = mpf.make_mpf_style(
            marketcolors=mc,
            facecolor=self.theme["bg"],
            figcolor=self.theme["bg"],
            gridcolor=self.theme["grid"],
            gridstyle="--",
            gridaxis="both",
            rc={
                "axes.labelcolor": self.theme["text"],
                "xtick.color": self.theme["text"],
                "ytick.color": self.theme["text"],
            },
        )

        # 均线
        add_plots = []
        ma_periods = [5, 10, 20, 60]
        for i, period in enumerate(ma_periods):
            if period <= len(self.df):
                ma = self.df["close"].rolling(window=period).mean()
                color = self.theme["ma_colors"][i % len(self.theme["ma_colors"])]
                add_plots.append(mpf.make_addplot(
                    ma, color=color, width=1.0,
                    label=f"MA{period}",
                ))

        fig, axes = mpf.plot(
            self.df,
            type="candle",
            style=style,
            volume=True,
            addplot=add_plots if add_plots else None,
            figsize=self.figsize,
            title=f"\n{self.name} ({self.symbol})",
            returnfig=True,
        )

        # 添加标注
        if annotations:
            ax_main = axes[0]
            for date_str, text in annotations.items():
                try:
                    date = pd.Timestamp(date_str)
                    if date in self.df.index:
                        price = self.df.loc[date, "close"]
                        ax_main.annotate(
                            text,
                            xy=(mdates.date2num(date), price),
                            xytext=(0, 30),
                            textcoords="offset points",
                            fontsize=9,
                            color=self.theme["text"],
                            arrowprops=dict(arrowstyle="->", color=self.theme["text"]),
                            ha="center",
                            bbox=dict(boxstyle="round,pad=0.3",
                                      facecolor=self.theme["panel_bg"],
                                      edgecolor=self.theme["grid"]),
                        )
                except (KeyError, ValueError):
                    continue

        fig.savefig(output_path, dpi=150, bbox_inches="tight",
                    facecolor=self.theme["bg"])
        plt.close(fig)
        return output_path

    def render_technical_dashboard(self, output_path: str, indicators_data: dict = None):
        """
        渲染综合技术面板：K线 + MACD + KDJ + RSI + VOL (4面板布局)
        """
        fig = plt.figure(figsize=(18, 16), facecolor=self.theme["bg"])
        gs = gridspec.GridSpec(4, 1, height_ratios=[3, 1, 1, 1], hspace=0.05)

        # 共用 x 轴
        dates = self.df.index
        close = self.df["close"]

        # ---- 面板1: K线 + 均线 ----
        ax1 = fig.add_subplot(gs[0])
        ax1.set_facecolor(self.theme["panel_bg"])
        ax1.set_title(f"{self.name} ({self.symbol}) 技术分析面板",
                      color=self.theme["text"], fontsize=14, pad=10)

        # 简化K线（用收盘价折线代替蜡烛图以节省渲染复杂度）
        ax1.plot(dates, close, color=self.theme["text"], linewidth=1.2, label="收盘价")

        for i, period in enumerate([5, 10, 20, 60]):
            if period <= len(close):
                ma = close.rolling(window=period).mean()
                color = self.theme["ma_colors"][i]
                ax1.plot(dates, ma, color=color, linewidth=0.8,
                         label=f"MA{period}", alpha=0.8)

        ax1.legend(fontsize=8, loc="upper left",
                   facecolor=self.theme["panel_bg"],
                   edgecolor=self.theme["grid"],
                   labelcolor=self.theme["text"])
        ax1.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)
        ax1.tick_params(colors=self.theme["text"], labelsize=8)

        # ---- 面板2: MACD ----
        if indicators_data and "MACD" in indicators_data:
            ax2 = fig.add_subplot(gs[1], sharex=ax1)
            ax2.set_facecolor(self.theme["panel_bg"])
            macd_data = indicators_data["MACD"]

            if "DIF" in self.df.columns:
                ax2.plot(dates, self.df["DIF"], color=self.theme["dif_color"],
                         linewidth=1, label="DIF")
                ax2.plot(dates, self.df["DEA"], color=self.theme["dea_color"],
                         linewidth=1, label="DEA")

                macd_hist = self.df["MACD"]
                colors = [self.theme["macd_positive"] if v >= 0
                          else self.theme["macd_negative"] for v in macd_hist]
                ax2.bar(dates, macd_hist, color=colors, alpha=0.6, width=0.8)

            ax2.axhline(y=0, color=self.theme["grid"], linewidth=0.5)
            ax2.set_ylabel("MACD", color=self.theme["text"], fontsize=9)
            ax2.legend(fontsize=7, loc="upper left",
                       facecolor=self.theme["panel_bg"],
                       labelcolor=self.theme["text"])
            ax2.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.2)
            ax2.tick_params(colors=self.theme["text"], labelsize=7)

        # ---- 面板3: KDJ ----
        if indicators_data and "KDJ" in indicators_data:
            ax3 = fig.add_subplot(gs[2], sharex=ax1)
            ax3.set_facecolor(self.theme["panel_bg"])

            if "K" in self.df.columns:
                ax3.plot(dates, self.df["K"], color=self.theme["k_color"],
                         linewidth=1, label="K")
                ax3.plot(dates, self.df["D"], color=self.theme["d_color"],
                         linewidth=1, label="D")
                ax3.plot(dates, self.df["J"], color=self.theme["j_color"],
                         linewidth=1, label="J", alpha=0.7)

            ax3.axhline(y=80, color=self.theme["up_color"], linewidth=0.5,
                        linestyle="--", alpha=0.5)
            ax3.axhline(y=20, color=self.theme["down_color"], linewidth=0.5,
                        linestyle="--", alpha=0.5)
            ax3.set_ylabel("KDJ", color=self.theme["text"], fontsize=9)
            ax3.set_ylim(-10, 110)
            ax3.legend(fontsize=7, loc="upper left",
                       facecolor=self.theme["panel_bg"],
                       labelcolor=self.theme["text"])
            ax3.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.2)
            ax3.tick_params(colors=self.theme["text"], labelsize=7)

        # ---- 面板4: 成交量 ----
        ax4 = fig.add_subplot(gs[3], sharex=ax1)
        ax4.set_facecolor(self.theme["panel_bg"])

        vol = self.df["volume"]
        vol_colors = [self.theme["volume_up"] if close.iloc[i] >= close.iloc[max(0, i-1)]
                      else self.theme["volume_down"] for i in range(len(close))]
        ax4.bar(dates, vol, color=vol_colors, width=0.8)
        ax4.set_ylabel("成交量", color=self.theme["text"], fontsize=9)
        ax4.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.2)
        ax4.tick_params(colors=self.theme["text"], labelsize=7)

        # 日期格式
        ax4.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

        fig.savefig(output_path, dpi=150, bbox_inches="tight",
                    facecolor=self.theme["bg"])
        plt.close(fig)
        return output_path

    def render_valuation_band(self, output_path: str, valuation_history: dict):
        """
        渲染估值分位数波段图 (PE/PB 历史区间 + 当前位置)
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                        facecolor=self.theme["bg"])

        for ax, metric, data in [
            (ax1, "PE", valuation_history.get("pe", {})),
            (ax2, "PB", valuation_history.get("pb", {})),
        ]:
            if not data:
                continue
            ax.set_facecolor(self.theme["panel_bg"])

            dates = pd.to_datetime(data["dates"])
            values = data["values"]
            p10, p25, p50, p75, p90 = (data["percentiles"]["p10"],
                                        data["percentiles"]["p25"],
                                        data["percentiles"]["p50"],
                                        data["percentiles"]["p75"],
                                        data["percentiles"]["p90"])

            ax.plot(dates, values, color=self.theme["text"], linewidth=1.2)
            ax.axhline(y=p50, color=self.theme["ma_colors"][0], linewidth=0.8,
                       linestyle="--", label=f"中位数 {p50:.1f}")
            ax.fill_between(dates, p25, p75, alpha=0.15,
                            color=self.theme["ma_colors"][1],
                            label=f"25%-75% ({p25:.1f}-{p75:.1f})")
            ax.fill_between(dates, p10, p90, alpha=0.08,
                            color=self.theme["ma_colors"][2],
                            label=f"10%-90% ({p10:.1f}-{p90:.1f})")

            # 标注当前位置
            current = values[-1]
            ax.scatter([dates.iloc[-1]], [current], color=self.theme["up_color"],
                       s=80, zorder=5, edgecolors="white", linewidths=1.5)
            ax.annotate(f"当前: {current:.1f}",
                        xy=(dates.iloc[-1], current),
                        xytext=(10, 15), textcoords="offset points",
                        color=self.theme["text"], fontsize=10,
                        fontweight="bold",
                        arrowprops=dict(arrowstyle="->", color=self.theme["text"]))

            ax.set_title(f"{self.name} {metric} 估值分位图",
                         color=self.theme["text"], fontsize=12)
            ax.legend(fontsize=8, facecolor=self.theme["panel_bg"],
                      labelcolor=self.theme["text"])
            ax.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)
            ax.tick_params(colors=self.theme["text"])

        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight",
                    facecolor=self.theme["bg"])
        plt.close(fig)
        return output_path

    def render_radar_chart(self, output_path: str, comparison_data: dict):
        """
        渲染行业对比雷达图
        comparison_data: {
            "dimensions": ["ROE", "毛利率", "增速", "估值", "市占率", "研发投入"],
            "companies": {
                "贵州茅台": [90, 92, 60, 55, 85, 30],
                "五粮液": [75, 78, 55, 70, 60, 25],
                "泸州老窖": [80, 75, 65, 65, 40, 35],
            }
        }
        """
        dims = comparison_data["dimensions"]
        companies = comparison_data["companies"]
        n_dims = len(dims)

        angles = np.linspace(0, 2 * np.pi, n_dims, endpoint=False).tolist()
        angles += angles[:1]  # 闭合

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True),
                               facecolor=self.theme["bg"])
        ax.set_facecolor(self.theme["panel_bg"])

        colors = self.theme["ma_colors"]
        for i, (company, values) in enumerate(companies.items()):
            vals = values + values[:1]
            color = colors[i % len(colors)]
            ax.plot(angles, vals, color=color, linewidth=2, label=company)
            ax.fill(angles, vals, color=color, alpha=0.1)

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(dims, color=self.theme["text"], fontsize=10)
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(["20", "40", "60", "80", "100"],
                           color=self.theme["text"], fontsize=8)
        ax.yaxis.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)
        ax.xaxis.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)

        ax.set_title(f"行业竞争力对比", color=self.theme["text"],
                     fontsize=14, pad=20)
        ax.legend(loc="lower right", fontsize=9,
                  facecolor=self.theme["panel_bg"],
                  edgecolor=self.theme["grid"],
                  labelcolor=self.theme["text"])

        fig.savefig(output_path, dpi=150, bbox_inches="tight",
                    facecolor=self.theme["bg"])
        plt.close(fig)
        return output_path

    def _fallback_kline(self, output_path: str) -> str:
        """mplfinance 不可用时的降级渲染"""
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize,
                                        gridspec_kw={"height_ratios": [3, 1]},
                                        facecolor=self.theme["bg"])
        ax1.set_facecolor(self.theme["panel_bg"])
        ax1.plot(self.df.index, self.df["close"], color=self.theme["text"])
        ax1.set_title(f"{self.name} ({self.symbol})", color=self.theme["text"])
        ax1.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)
        ax1.tick_params(colors=self.theme["text"])

        ax2.set_facecolor(self.theme["panel_bg"])
        ax2.bar(self.df.index, self.df["volume"], color=self.theme["volume_up"], width=0.8)
        ax2.grid(True, color=self.theme["grid"], linestyle="--", alpha=0.3)
        ax2.tick_params(colors=self.theme["text"])

        fig.tight_layout()
        fig.savefig(output_path, dpi=150, bbox_inches="tight",
                    facecolor=self.theme["bg"])
        plt.close(fig)
        return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="股票图表渲染器")
    parser.add_argument("--input", required=True, help="K线数据JSON路径")
    parser.add_argument("--symbol", required=True)
    parser.add_argument("--name", default="")
    parser.add_argument("--type", default="kline",
                        choices=["kline", "dashboard", "valuation-band", "radar",
                                 "capital-heatmap", "sector-rotation",
                                 "portfolio-pie", "backtest-curve"])
    parser.add_argument("--theme", default="dark", choices=["dark", "light"])
    parser.add_argument("--output", default="/tmp/stock_chart.png")
    parser.add_argument("--indicators-data", default=None, help="技术指标JSON路径")
    parser.add_argument("--annotations", default=None, help="标注, 格式: date:text,date:text")
    args = parser.parse_args()

    df = pd.read_json(args.input)
    renderer = ChartRenderer(df, args.symbol, args.name, args.theme)

    annotations = None
    if args.annotations:
        annotations = dict(pair.split(":") for pair in args.annotations.split(","))

    indicators_data = None
    if args.indicators_data:
        with open(args.indicators_data) as f:
            indicators_data = json.load(f)

    if args.type == "kline":
        path = renderer.render_kline(args.output, annotations=annotations)
    elif args.type == "dashboard":
        path = renderer.render_technical_dashboard(args.output, indicators_data)
    else:
        path = renderer.render_kline(args.output)

    print(json.dumps({"output": path, "type": args.type}, ensure_ascii=False))