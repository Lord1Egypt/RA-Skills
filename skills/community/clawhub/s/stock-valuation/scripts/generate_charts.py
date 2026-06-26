#!/usr/bin/env python3
"""Generate 4 stock analysis charts as PNGs. Outputs JSON with file paths."""
import argparse
import json
import sys

def main():
    parser = argparse.ArgumentParser(description="Generate stock analysis charts for a ticker.")
    parser.add_argument("ticker", help="Stock ticker symbol")
    args = parser.parse_args()

    try:
        import yfinance as yf
    except ImportError:
        print("ERROR: yfinance not installed. Run with: uv run --with yfinance,matplotlib", file=sys.stderr)
        sys.exit(1)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.dates as mdates
    except ImportError:
        print("ERROR: matplotlib not installed. Run with: uv run --with yfinance,matplotlib", file=sys.stderr)
        sys.exit(1)

    ticker = args.ticker.upper()
    t = yf.Ticker(ticker)
    charts = []

    # Shared style
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "#f8f9fa",
        "axes.grid": True,
        "grid.alpha": 0.3,
        "font.size": 10,
    })

    # --- Chart 1: 1yr price with 50/200 SMA ---
    try:
        hist = t.history(period="1y")
        if not hist.empty:
            close = hist["Close"]
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(close.index, close.values, label="Price", color="#1f77b4", linewidth=1.5)
            if len(close) >= 50:
                sma50 = close.rolling(50).mean()
                ax.plot(sma50.index, sma50.values, label="SMA 50", color="#ff7f0e", linewidth=1, linestyle="--")
            if len(close) >= 200:
                sma200 = close.rolling(200).mean()
                ax.plot(sma200.index, sma200.values, label="SMA 200", color="#2ca02c", linewidth=1, linestyle="--")
            ax.set_title(f"{ticker} — 1 Year Price with Moving Averages", fontweight="bold")
            ax.set_ylabel("Price ($)")
            ax.legend(loc="upper left")
            ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
            fig.autofmt_xdate()
            fig.tight_layout()
            path = f"/tmp/{ticker}_chart_price.png"
            fig.savefig(path, dpi=150)
            plt.close(fig)
            charts.append({"type": "price_sma", "path": path})
    except Exception as e:
        print(f"Warning: price chart failed: {e}", file=sys.stderr)

    # --- Chart 2: Quarterly revenue + net income bars ---
    try:
        qf = t.quarterly_income_stmt
        if qf is not None and not qf.empty:
            cols = list(qf.columns[:8])
            cols.reverse()
            periods = [str(c.date()) for c in cols]
            revenue = []
            net_income = []
            for c in cols:
                rev = qf.loc["Total Revenue", c] if "Total Revenue" in qf.index else None
                ni = qf.loc["Net Income", c] if "Net Income" in qf.index else None
                revenue.append(float(rev) / 1e9 if rev is not None and str(rev) != "nan" else 0)
                net_income.append(float(ni) / 1e9 if ni is not None and str(ni) != "nan" else 0)

            import numpy as np
            x = np.arange(len(periods))
            width = 0.35
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.bar(x - width / 2, revenue, width, label="Revenue", color="#1f77b4")
            ax.bar(x + width / 2, net_income, width, label="Net Income", color="#2ca02c")
            ax.set_title(f"{ticker} — Quarterly Revenue & Net Income", fontweight="bold")
            ax.set_ylabel("$ Billions")
            ax.set_xticks(x)
            ax.set_xticklabels(periods, rotation=45, ha="right")
            ax.legend()
            fig.tight_layout()
            path = f"/tmp/{ticker}_chart_revenue.png"
            fig.savefig(path, dpi=150)
            plt.close(fig)
            charts.append({"type": "revenue_income", "path": path})
    except Exception as e:
        print(f"Warning: revenue chart failed: {e}", file=sys.stderr)

    # --- Chart 3: Margin trends (gross/operating/net) ---
    try:
        qf = t.quarterly_income_stmt
        if qf is not None and not qf.empty:
            cols = list(qf.columns[:8])
            cols.reverse()
            periods = [str(c.date()) for c in cols]
            gross_m, op_m, net_m = [], [], []
            for c in cols:
                rev = qf.loc["Total Revenue", c] if "Total Revenue" in qf.index else None
                gp = qf.loc["Gross Profit", c] if "Gross Profit" in qf.index else None
                oi = qf.loc["Operating Income", c] if "Operating Income" in qf.index else None
                ni = qf.loc["Net Income", c] if "Net Income" in qf.index else None
                rev_f = float(rev) if rev is not None and str(rev) != "nan" else None
                if rev_f and rev_f != 0:
                    gross_m.append(float(gp) / rev_f * 100 if gp is not None and str(gp) != "nan" else None)
                    op_m.append(float(oi) / rev_f * 100 if oi is not None and str(oi) != "nan" else None)
                    net_m.append(float(ni) / rev_f * 100 if ni is not None and str(ni) != "nan" else None)
                else:
                    gross_m.append(None)
                    op_m.append(None)
                    net_m.append(None)

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(periods, gross_m, marker="o", label="Gross Margin", color="#1f77b4", linewidth=2)
            ax.plot(periods, op_m, marker="s", label="Operating Margin", color="#ff7f0e", linewidth=2)
            ax.plot(periods, net_m, marker="^", label="Net Margin", color="#2ca02c", linewidth=2)
            ax.set_title(f"{ticker} — Margin Trends", fontweight="bold")
            ax.set_ylabel("Margin (%)")
            ax.legend()
            plt.xticks(rotation=45, ha="right")
            fig.tight_layout()
            path = f"/tmp/{ticker}_chart_margins.png"
            fig.savefig(path, dpi=150)
            plt.close(fig)
            charts.append({"type": "margin_trends", "path": path})
    except Exception as e:
        print(f"Warning: margin chart failed: {e}", file=sys.stderr)

    # --- Chart 4: Historical PE with current marked ---
    try:
        hist = t.history(period="5y", interval="1mo")
        info = t.info
        if not hist.empty and "trailingEps" in info and info["trailingEps"]:
            eps = float(info["trailingEps"])
            if eps > 0:
                close_monthly = hist["Close"]
                pe_series = close_monthly / eps
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(pe_series.index, pe_series.values, label="Historical P/E", color="#1f77b4", linewidth=1.5)
                current_pe = info.get("trailingPE")
                if current_pe:
                    ax.axhline(y=float(current_pe), color="#d62728", linestyle="--", linewidth=1, label=f"Current P/E ({current_pe:.1f})")
                mean_pe = float(pe_series.mean())
                ax.axhline(y=mean_pe, color="#7f7f7f", linestyle=":", linewidth=1, label=f"Mean P/E ({mean_pe:.1f})")
                ax.set_title(f"{ticker} — Historical P/E Ratio", fontweight="bold")
                ax.set_ylabel("P/E Ratio")
                ax.legend()
                ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
                fig.autofmt_xdate()
                fig.tight_layout()
                path = f"/tmp/{ticker}_chart_pe.png"
                fig.savefig(path, dpi=150)
                plt.close(fig)
                charts.append({"type": "historical_pe", "path": path})
    except Exception as e:
        print(f"Warning: PE chart failed: {e}", file=sys.stderr)

    result = {
        "ticker": ticker,
        "charts_generated": len(charts),
        "charts": charts,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
