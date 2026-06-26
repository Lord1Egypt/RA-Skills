from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from statistics import mean

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from performance_metrics import (  # noqa: E402
    annualized_return,
    annualized_volatility,
    average_turnover,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
    total_return,
)


def read_signals(path: Path) -> dict[str, list[tuple[str, float]]]:
    signals: dict[str, list[tuple[str, float]]] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader.fieldnames, {"date", "ticker", "score"}, path)
        for row in reader:
            date = required_value(row, "date", path)
            ticker = required_value(row, "ticker", path)
            score = float(required_value(row, "score", path))
            signals.setdefault(date, []).append((ticker, score))
    return signals


def read_prices(path: Path) -> tuple[dict[str, dict[str, float]], list[str]]:
    prices: dict[str, dict[str, float]] = {}
    dates: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        require_columns(reader.fieldnames, {"date", "ticker", "close"}, path)
        for row in reader:
            date = required_value(row, "date", path)
            ticker = required_value(row, "ticker", path)
            close = float(required_value(row, "close", path))
            prices.setdefault(ticker, {})[date] = close
            dates.add(date)
    return prices, sorted(dates)


def require_columns(fieldnames: list[str] | None, required: set[str], path: Path) -> None:
    columns = set(fieldnames or [])
    missing = sorted(required - columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {', '.join(missing)}")


def required_value(row: dict[str, str], field: str, path: Path) -> str:
    value = row.get(field, "").strip()
    if value == "":
        raise ValueError(f"{path} has an empty {field} value")
    return value


def entry_price_date(signal_date: str, price_dates: list[str]) -> str | None:
    for price_date in price_dates:
        if price_date >= signal_date:
            return price_date
    return None


def next_price_date(entry_date: str, price_dates: list[str]) -> str | None:
    for price_date in price_dates:
        if price_date > entry_date:
            return price_date
    return None


def select_top(scored_tickers: list[tuple[str, float]], top_n: int) -> list[str]:
    ranked = sorted(scored_tickers, key=lambda item: (-item[1], item[0]))
    return [ticker for ticker, _score in ranked[:top_n]]


def equal_weight_return(
    selected: list[str],
    start_date: str,
    end_date: str,
    prices: dict[str, dict[str, float]],
) -> float:
    returns = []
    for ticker in selected:
        ticker_prices = prices.get(ticker, {})
        if start_date not in ticker_prices or end_date not in ticker_prices:
            raise ValueError(
                f"missing price for ticker {ticker} between {start_date} and {end_date}"
            )
        start_close = ticker_prices[start_date]
        end_close = ticker_prices[end_date]
        if start_close <= 0:
            raise ValueError(f"non-positive entry price for ticker {ticker} on {start_date}")
        returns.append(end_close / start_close - 1.0)
    return mean(returns)


def turnover(previous: set[str] | None, current: set[str]) -> float:
    if not current:
        return 0.0
    if previous is None:
        return 1.0
    return len(current - previous) / len(current)


def run_backtest(
    signals: dict[str, list[tuple[str, float]]],
    prices: dict[str, dict[str, float]],
    price_dates: list[str],
    top_n: int,
    fee_bps: float,
    slippage_bps: float,
    periods_per_year: int,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    if top_n <= 0:
        raise ValueError("--top-n must be greater than zero")
    if periods_per_year <= 0:
        raise ValueError("--periods-per-year must be greater than zero")
    if fee_bps < 0:
        raise ValueError("--fee-bps must be non-negative")
    if slippage_bps < 0:
        raise ValueError("--slippage-bps must be non-negative")

    cost_rate = (fee_bps + slippage_bps) / 10000.0
    periods: list[dict[str, object]] = []
    selected_history: list[set[str]] = []
    previous_selection: set[str] | None = None

    for signal_date in sorted(signals):
        candidates = signals[signal_date]
        if top_n > len(candidates):
            raise ValueError(
                f"--top-n {top_n} exceeds {len(candidates)} signal candidates on {signal_date}"
            )
        entry_date = entry_price_date(signal_date, price_dates)
        if entry_date is None:
            raise ValueError(f"no entry price date found on or after signal date {signal_date}")
        exit_date = next_price_date(entry_date, price_dates)
        if exit_date is None:
            raise ValueError(f"no exit price date found after entry date {entry_date}")

        selected = select_top(candidates, top_n)
        current_selection = set(selected)
        gross_return = equal_weight_return(selected, entry_date, exit_date, prices)
        period_turnover = turnover(previous_selection, current_selection)
        cost = period_turnover * cost_rate
        net_return = gross_return - cost
        if net_return <= -1.0:
            raise ValueError(
                f"cost assumptions make net return <= -100% for signal date {signal_date}"
            )

        periods.append(
            {
                "signal_date": signal_date,
                "entry_date": entry_date,
                "exit_date": exit_date,
                "selected_tickers": selected,
                "gross_return": gross_return,
                "turnover": period_turnover,
                "cost": cost,
                "net_return": net_return,
            }
        )
        selected_history.append(current_selection)
        previous_selection = current_selection

    returns = [float(period["net_return"]) for period in periods]
    summary: dict[str, object] = {
        "number_of_periods": len(periods),
        "top_n": top_n,
        "fee_bps": fee_bps,
        "slippage_bps": slippage_bps,
        "periods_per_year": periods_per_year,
        "total_return": total_return(returns),
        "annualized_return": annualized_return(returns, periods_per_year),
        "annualized_volatility": annualized_volatility(returns, periods_per_year),
        "max_drawdown": max_drawdown(returns),
        "sharpe_ratio": sharpe_ratio(returns, periods_per_year),
        "sortino_ratio": sortino_ratio(returns, periods_per_year),
        "average_turnover": average_turnover(selected_history),
        "hit_rate": mean([1.0 if item > 0 else 0.0 for item in returns]) if returns else None,
    }
    if periods:
        summary["start_signal_date"] = periods[0]["signal_date"]
        summary["end_signal_date"] = periods[-1]["signal_date"]
    return summary, periods


def write_outputs(outdir: Path, summary: dict[str, object], periods: list[dict[str, object]]) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    summary_path = outdir / "backtest_summary.json"
    periods_path = outdir / "backtest_periods.csv"

    with summary_path.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, sort_keys=True)
        handle.write("\n")

    with periods_path.open("w", newline="", encoding="utf-8") as handle:
        fieldnames = [
            "signal_date",
            "entry_date",
            "exit_date",
            "selected_tickers",
            "gross_return",
            "turnover",
            "cost",
            "net_return",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for period in periods:
            row = dict(period)
            row["selected_tickers"] = ";".join(period["selected_tickers"])
            writer.writerow(row)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Backtest top-N equal-weight ranking strategies from CSV inputs.",
    )
    parser.add_argument("--signals-file", required=True, type=Path)
    parser.add_argument("--prices-file", required=True, type=Path)
    parser.add_argument("--outdir", required=True, type=Path)
    parser.add_argument("--top-n", required=True, type=int)
    parser.add_argument("--fee-bps", default=0.0, type=float)
    parser.add_argument("--slippage-bps", default=0.0, type=float)
    parser.add_argument("--periods-per-year", default=12, type=int)
    return parser


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    return build_parser().parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        signals = read_signals(args.signals_file)
        prices, price_dates = read_prices(args.prices_file)
        summary, periods = run_backtest(
            signals=signals,
            prices=prices,
            price_dates=price_dates,
            top_n=args.top_n,
            fee_bps=args.fee_bps,
            slippage_bps=args.slippage_bps,
            periods_per_year=args.periods_per_year,
        )
        write_outputs(args.outdir, summary, periods)
        print(json.dumps(summary, indent=2, sort_keys=True))
    except ValueError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
