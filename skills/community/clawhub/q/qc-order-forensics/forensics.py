"""
OrderForensics -- Forensic Diagnosis Engine for Backtest Orders
===============================================================
Consolidates 20+ parse_ordersXX.py scripts into a single high-level class.
Automatically converts orders.csv and result.json into an LLM-readable
diagnostic report.

Usage:
    forensics = OrderForensics(orders_csv, result_json)
    report = forensics.full_diagnosis()
    print(report)  # Feed directly to LLM context
"""
import os
import json
import argparse
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


class OrderForensics:
    """Extract trade quality diagnostics from orders.csv + result.json."""

    def __init__(
        self,
        orders_csv: str,
        result_json: str = None,
        equity_symbol: str = "QQQ",
    ):
        self.orders_csv = orders_csv
        self.result_json = result_json
        self.equity_symbol = equity_symbol

        # Load data
        self.df = pd.read_csv(orders_csv)
        self.df["fillPrice"] = pd.to_numeric(self.df["fillPrice"], errors="coerce")
        self.df["quantity"] = pd.to_numeric(self.df["quantity"], errors="coerce")
        self.df["underlying"] = self.df["symbol"].apply(self._get_underlying)

        # Separate filled orders into options vs equity
        self.df_filled = (
            self.df[self.df["status"] == "Filled"]
            if "status" in self.df.columns
            else self.df
        )
        self.options = self.df_filled[
            self.df_filled["underlying"] != self.equity_symbol
        ]
        self.equity = self.df_filled[
            self.df_filled["underlying"] == self.equity_symbol
        ]

        # Load result statistics if available
        self.stats: Dict[str, str] = {}
        if result_json and os.path.exists(result_json):
            with open(result_json) as f:
                data = json.load(f)
            result = data.get("backtest", data)
            self.stats = result.get("statistics", {})

    @staticmethod
    def _get_underlying(sym: str) -> str:
        """Extract the underlying ticker from an option symbol string."""
        try:
            return str(sym).split()[0].strip()
        except (ValueError, IndexError, AttributeError):
            return str(sym)

    # ================================================================
    # 1. Key Statistics
    # ================================================================
    def get_key_stats(self) -> Dict[str, str]:
        """Extract key performance statistics from result.json."""
        keys = [
            "Net Profit",
            "Compounding Annual Return",
            "Drawdown",
            "Sharpe Ratio",
            "Sortino Ratio",
            "Win Rate",
            "Loss Rate",
            "Average Win",
            "Average Loss",
            "Profit-Loss Ratio",
            "Expectancy",
            "Total Orders",
            "Total Fees",
            "Beta",
            "Alpha",
        ]
        return {k: self.stats.get(k, "N/A") for k in keys}

    # ================================================================
    # 2. Trade Quality Detection
    # ================================================================
    def trade_quality(self) -> Dict[str, any]:
        """Compute zero rate, windfall trade counts, and order statistics."""
        buys = self.options[self.options["direction"] == "buy"]
        sells = self.options[self.options["direction"] == "sell"]

        # Zero rate: options sold at <= $0.05 (expired worthless)
        zero_sells = sells[sells["fillPrice"] <= 0.05]
        zero_rate = len(zero_sells) / max(len(sells), 1)

        # Windfall trade detection
        avg_buys = buys.groupby("symbol")["fillPrice"].mean().to_dict()
        if len(sells) > 0:
            sells_c = sells.copy()
            sells_c["est_yield"] = sells_c.apply(
                lambda row: (
                    (row["fillPrice"] / avg_buys.get(row["symbol"], row["fillPrice"]))
                    - 1
                )
                if avg_buys.get(row["symbol"], 0) > 0
                else 0,
                axis=1,
            )
            big_wins_100 = len(sells_c[sells_c["est_yield"] > 1.0])
            big_wins_400 = len(sells_c[sells_c["est_yield"] > 4.0])
            big_wins_1000 = len(sells_c[sells_c["est_yield"] > 10.0])
        else:
            big_wins_100 = big_wins_400 = big_wins_1000 = 0

        return {
            "total_orders": len(self.df_filled),
            "option_orders": len(self.options),
            "equity_orders": len(self.equity),
            "option_buys": len(buys),
            "option_sells": len(sells),
            "avg_buy_price": float(buys["fillPrice"].mean()) if len(buys) > 0 else 0,
            "median_buy_price": (
                float(buys["fillPrice"].median()) if len(buys) > 0 else 0
            ),
            "unique_underlyings": buys["underlying"].nunique(),
            "zero_sell_count": len(zero_sells),
            "zero_rate": zero_rate,
            "big_wins_100pct": big_wins_100,
            "big_wins_400pct": big_wins_400,
            "big_wins_1000pct": big_wins_1000,
        }

    # ================================================================
    # 3. ROI Breakdown by Contract
    # ================================================================
    def roi_breakdown(self) -> pd.DataFrame:
        """Compute per-symbol ROI from option buy/sell cashflows."""
        opt = self.options.copy()
        opt["cash_flow"] = 0.0
        opt.loc[opt["direction"] == "buy", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )
        opt.loc[opt["direction"] == "sell", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )

        buys_df = opt[opt["direction"] == "buy"].groupby("symbol")["cash_flow"].sum()
        sells_df = opt[opt["direction"] == "sell"].groupby("symbol")["cash_flow"].sum()

        summary = pd.DataFrame({"Cost": -buys_df, "Return": sells_df}).fillna(0)
        summary["NetProfit"] = summary["Return"] - summary["Cost"]
        summary["ROI"] = summary["NetProfit"] / summary["Cost"].replace(0, 1)
        summary["Underlying"] = summary.index.map(self._get_underlying)

        return summary.sort_values("NetProfit", ascending=False)

    def roi_summary(self) -> Dict[str, any]:
        """Aggregate ROI summary across all option contracts."""
        roi = self.roi_breakdown()
        total_cost = roi["Cost"].sum()
        total_return = roi["Return"].sum()
        net = total_return - total_cost

        winners = roi[roi["NetProfit"] > 0]
        losers = roi[roi["NetProfit"] <= 0]

        return {
            "total_option_cost": total_cost,
            "total_option_return": total_return,
            "net_option_profit": net,
            "overall_roi": net / max(total_cost, 1),
            "winning_symbols": len(winners),
            "losing_symbols": len(losers),
            "avg_winner_roi": (
                float(winners["ROI"].mean()) if len(winners) > 0 else 0
            ),
            "avg_loser_roi": (
                float(losers["ROI"].mean()) if len(losers) > 0 else 0
            ),
            "top5_winners": list(winners.head(5).index),
            "top5_losers": list(losers.tail(5).index),
        }

    # ================================================================
    # 4. Monthly Cashflow
    # ================================================================
    def monthly_cashflow(self) -> pd.DataFrame:
        """Compute monthly net option cashflow with cumulative totals."""
        opt = self.options.copy()
        opt["cash_flow"] = 0.0
        opt.loc[opt["direction"] == "buy", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )
        opt.loc[opt["direction"] == "sell", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )

        time_col = "fillTime" if "fillTime" in opt.columns else "submitTime"
        opt["date"] = pd.to_datetime(
            opt[time_col].astype(str).str[:10], errors="coerce"
        )
        opt = opt.dropna(subset=["date"])
        opt["month"] = opt["date"].dt.to_period("M")

        monthly = opt.groupby("month").agg(
            net_cf=("cash_flow", "sum"),
            trades=("orderId", "count"),
            buys=("direction", lambda x: (x == "buy").sum()),
            sells=("direction", lambda x: (x == "sell").sum()),
        )
        monthly["cum_cf"] = monthly["net_cf"].cumsum()
        return monthly

    # ================================================================
    # 5. Drawdown Death Causes
    # ================================================================
    def find_drawdown_periods(self) -> List[Dict]:
        """Identify consecutive loss streaks exceeding $1,000."""
        monthly = self.monthly_cashflow()
        periods: List[Dict] = []
        streak_start = None
        streak_loss = 0

        for idx, row in monthly.iterrows():
            if row["net_cf"] < 0:
                if streak_start is None:
                    streak_start = str(idx)
                streak_loss += row["net_cf"]
            else:
                if streak_start and streak_loss < -1000:
                    periods.append(
                        {
                            "start": streak_start,
                            "end": str(idx),
                            "total_loss": streak_loss,
                            "description": (
                                f"{streak_start}~{idx} "
                                f"consecutive losses ${streak_loss:,.0f}"
                            ),
                        }
                    )
                streak_start = None
                streak_loss = 0

        # Handle trailing streak
        if streak_start and streak_loss < -1000:
            periods.append(
                {
                    "start": streak_start,
                    "end": str(monthly.index[-1]),
                    "total_loss": streak_loss,
                    "description": (
                        f"{streak_start}~{monthly.index[-1]} "
                        f"consecutive losses ${streak_loss:,.0f}"
                    ),
                }
            )

        return sorted(periods, key=lambda x: x["total_loss"])

    # ================================================================
    # 6. Yearly Breakdown
    # ================================================================
    def yearly_breakdown(self) -> pd.DataFrame:
        """Annual net option cashflow, trade count, and ticker diversity."""
        opt = self.options.copy()
        opt["cash_flow"] = 0.0
        opt.loc[opt["direction"] == "buy", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )
        opt.loc[opt["direction"] == "sell", "cash_flow"] = (
            -opt["quantity"] * opt["fillPrice"] * 100
        )

        time_col = "fillTime" if "fillTime" in opt.columns else "submitTime"
        opt["date"] = pd.to_datetime(
            opt[time_col].astype(str).str[:10], errors="coerce"
        )
        opt = opt.dropna(subset=["date"])
        opt["year"] = opt["date"].dt.year

        return opt.groupby("year").agg(
            net_cf=("cash_flow", "sum"),
            trades=("orderId", "count"),
            tickers=("underlying", "nunique"),
        )

    # ================================================================
    # 7. Full LLM-Readable Diagnosis Report
    # ================================================================
    def full_diagnosis(self) -> str:
        """Generate a complete text diagnostic report for LLM consumption."""
        lines: List[str] = []
        lines.append("=" * 60)
        lines.append("BACKTEST FORENSIC DIAGNOSIS REPORT")
        lines.append("=" * 60)

        # Key Statistics
        stats = self.get_key_stats()
        lines.append("\n## Key Statistics:")
        for k, v in stats.items():
            lines.append(f"  {k}: {v}")

        # Trade Quality
        tq = self.trade_quality()
        lines.append("\n## Trade Quality:")
        lines.append(
            f"  Total orders: {tq['total_orders']} "
            f"(options: {tq['option_orders']}, "
            f"{self.equity_symbol}: {tq['equity_orders']})"
        )
        lines.append(
            f"  Option buys: {tq['option_buys']} | sells: {tq['option_sells']}"
        )
        lines.append(
            f"  Avg buy price: ${tq['avg_buy_price']:.2f} | "
            f"median: ${tq['median_buy_price']:.2f}"
        )
        lines.append(f"  Unique underlyings: {tq['unique_underlyings']}")
        lines.append(
            f"  Zero rate: {tq['zero_rate']:.1%} "
            f"({tq['zero_sell_count']} orders)"
        )
        lines.append(
            f"  Windfall trades >100%: {tq['big_wins_100pct']} | "
            f">400%: {tq['big_wins_400pct']} | "
            f">1000%: {tq['big_wins_1000pct']}"
        )

        # ROI Analysis
        roi = self.roi_summary()
        lines.append("\n## ROI Analysis:")
        lines.append(f"  Total option cost: ${roi['total_option_cost']:,.0f}")
        lines.append(f"  Total option return: ${roi['total_option_return']:,.0f}")
        lines.append(f"  Net option profit: ${roi['net_option_profit']:,.0f}")
        lines.append(f"  Overall ROI: {roi['overall_roi']:.2%}")
        lines.append(
            f"  Winning symbols: {roi['winning_symbols']} | "
            f"Losing symbols: {roi['losing_symbols']}"
        )
        lines.append(f"  Avg winner ROI: {roi['avg_winner_roi']:.1%}")
        lines.append(f"  Avg loser ROI: {roi['avg_loser_roi']:.1%}")

        # Yearly Performance
        yearly = self.yearly_breakdown()
        lines.append("\n## Yearly Performance:")
        for yr, row in yearly.iterrows():
            indicator = "[+]" if row["net_cf"] > 0 else "[-]"
            lines.append(
                f"  {yr}: {indicator} Net flow ${row['net_cf']:>+10,.0f} | "
                f"{int(row['trades'])} trades | "
                f"{int(row['tickers'])} underlyings"
            )

        # Drawdown Death Causes
        dd_periods = self.find_drawdown_periods()
        if dd_periods:
            lines.append(
                f"\n## Drawdown Death Causes "
                f"({len(dd_periods)} consecutive loss streaks):"
            )
            for p in dd_periods[:5]:
                lines.append(f"  [-] {p['description']}")

        # Recent Monthly Cashflow (last 6 months)
        monthly = self.monthly_cashflow()
        lines.append("\n## Recent Monthly Cashflow (last 6 months):")
        for idx, row in monthly.tail(6).iterrows():
            indicator = "[+]" if row["net_cf"] > 0 else "[-]"
            lines.append(
                f"  {idx}: {indicator} ${row['net_cf']:>+10,.0f} | "
                f"Cumulative ${row['cum_cf']:>+10,.0f} | "
                f"{int(row['trades'])} trades"
            )

        lines.append("\n" + "=" * 60)
        lines.append("END OF FORENSIC REPORT")
        lines.append("=" * 60)

        return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Forensic diagnosis engine for backtest order data."
    )
    parser.add_argument("orders_csv", help="Path to orders.csv file")
    parser.add_argument(
        "result_json",
        nargs="?",
        default=None,
        help="Path to result.json file (optional)",
    )
    parser.add_argument(
        "--equity-symbol",
        default="QQQ",
        help="Equity symbol to separate from options (default: QQQ)",
    )
    args = parser.parse_args()

    forensics = OrderForensics(
        args.orders_csv,
        args.result_json,
        equity_symbol=args.equity_symbol,
    )
    print(forensics.full_diagnosis())
