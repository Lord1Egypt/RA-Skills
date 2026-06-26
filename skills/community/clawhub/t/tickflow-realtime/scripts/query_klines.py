#!/usr/bin/env python3

import argparse

from tickflow_common import (
    DEFAULT_BASE_URL,
    TickFlowAPIError,
    TickFlowError,
    compact_kline_to_rows,
    ensure_dict,
    format_epoch_ms,
    format_number,
    join_csv,
    parse_csv_arg,
    render_table,
    request_json,
    resolve_api_key,
    to_pretty_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query TickFlow K-lines.")
    parser.add_argument("--symbol", help="Single symbol")
    parser.add_argument("--symbols", help="Comma-separated symbols for batch query")
    parser.add_argument("--period", default="1d", help="K-line period, default: 1d")
    parser.add_argument("--count", type=int, help="Number of bars")
    parser.add_argument("--start-time", type=int, help="Start time in epoch milliseconds")
    parser.add_argument("--end-time", type=int, help="End time in epoch milliseconds")
    parser.add_argument("--adjust", help="Adjust type")
    parser.add_argument("--rows", type=int, default=10, help="Rows to show in table format")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="TickFlow API base URL")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument("--format", choices=["json", "summary", "table"], default="summary")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def fetch_single(args: argparse.Namespace, api_key: str) -> dict:
    params = {
        "symbol": args.symbol,
        "period": args.period,
        "count": args.count,
        "start_time": args.start_time,
        "end_time": args.end_time,
        "adjust": args.adjust,
    }
    payload = request_json(
        "GET",
        "/v1/klines",
        api_key,
        base_url=args.base_url,
        params=params,
        timeout=args.timeout,
    )
    payload = ensure_dict(payload, name="response")
    payload["data"] = compact_kline_to_rows(payload.get("data"))
    return payload


def fetch_batch(args: argparse.Namespace, api_key: str, symbols: list[str]) -> dict:
    params = {
        "symbols": join_csv(symbols),
        "period": args.period,
        "count": args.count,
        "start_time": args.start_time,
        "end_time": args.end_time,
        "adjust": args.adjust,
    }
    payload = request_json(
        "GET",
        "/v1/klines/batch",
        api_key,
        base_url=args.base_url,
        params=params,
        timeout=args.timeout,
    )
    payload = ensure_dict(payload, name="response")
    raw_data = ensure_dict(payload.get("data"), name="response.data")
    payload["data"] = {symbol: compact_kline_to_rows(value) for symbol, value in raw_data.items()}
    return payload


def kline_row(symbol: str, period: str, item: dict) -> dict[str, str]:
    return {
        "symbol": symbol,
        "period": period,
        "time": format_epoch_ms(item.get("timestamp")),
        "open": format_number(item.get("open")),
        "high": format_number(item.get("high")),
        "low": format_number(item.get("low")),
        "close": format_number(item.get("close")),
        "volume": format_number(item.get("volume"), 0),
        "amount": format_number(item.get("amount")),
    }


def render_single_summary(symbol: str, period: str, rows: list[dict]) -> str:
    if not rows:
        return "No data returned."
    latest = kline_row(symbol, period, rows[-1])
    return "\n".join(
        [
            f"{symbol} period={period} bars={len(rows)}",
            f"time={latest['time']} open={latest['open']} high={latest['high']} low={latest['low']} close={latest['close']}",
            f"volume={latest['volume']} amount={latest['amount']}",
        ]
    )


def render_batch_summary(period: str, payload: dict[str, list[dict]]) -> str:
    if not payload:
        return "No data returned."
    blocks = []
    for symbol, rows in payload.items():
        if not rows:
            blocks.append(f"{symbol} period={period} No data returned.")
            continue
        latest = kline_row(symbol, period, rows[-1])
        blocks.append(
            "\n".join(
                [
                    f"{symbol} period={period}",
                    f"time={latest['time']} open={latest['open']} high={latest['high']} low={latest['low']} close={latest['close']}",
                    f"volume={latest['volume']} amount={latest['amount']}",
                ]
            )
        )
    return "\n\n".join(blocks)


def render_single_table(symbol: str, period: str, rows: list[dict], limit: int) -> str:
    selected = rows[-limit:] if limit > 0 else rows
    table_rows = [kline_row(symbol, period, item) for item in selected]
    columns = [
        ("time", "time"),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
        ("amount", "amount"),
    ]
    return render_table(table_rows, columns)


def render_batch_table(period: str, payload: dict[str, list[dict]]) -> str:
    rows = []
    for symbol, items in payload.items():
        if not items:
            rows.append(
                {
                    "symbol": symbol,
                    "period": period,
                    "time": "-",
                    "open": "-",
                    "high": "-",
                    "low": "-",
                    "close": "-",
                    "volume": "-",
                }
            )
            continue
        rows.append(kline_row(symbol, period, items[-1]))
    columns = [
        ("symbol", "symbol"),
        ("period", "period"),
        ("time", "time"),
        ("open", "open"),
        ("high", "high"),
        ("low", "low"),
        ("close", "close"),
        ("volume", "volume"),
    ]
    return render_table(rows, columns)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if bool(args.symbol) == bool(args.symbols):
        raise SystemExit("Provide exactly one of --symbol or --symbols.")

    api_key = resolve_api_key()

    try:
        if args.symbol:
            payload = fetch_single(args, api_key)
            if args.format == "json":
                print(to_pretty_json(payload, args.pretty))
                return
            if args.format == "table":
                print(render_single_table(args.symbol, args.period, payload["data"], args.rows))
                return
            print(render_single_summary(args.symbol, args.period, payload["data"]))
            return

        symbols = parse_csv_arg(args.symbols)
        if not symbols:
            raise TickFlowError("No symbols provided.")

        payload = fetch_batch(args, api_key, symbols)
        if args.format == "json":
            print(to_pretty_json(payload, args.pretty))
            return
        if args.format == "table":
            print(render_batch_table(args.period, payload["data"]))
            return
        print(render_batch_summary(args.period, payload["data"]))
    except TickFlowAPIError as exc:
        raise SystemExit(str(exc))
    except TickFlowError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
