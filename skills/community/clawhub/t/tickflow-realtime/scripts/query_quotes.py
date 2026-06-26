#!/usr/bin/env python3

import argparse

from tickflow_common import (
    DEFAULT_BASE_URL,
    TickFlowAPIError,
    TickFlowError,
    ensure_dict,
    ensure_list,
    format_epoch_ms,
    format_number,
    format_percent,
    join_csv,
    parse_csv_arg,
    render_table,
    request_json,
    resolve_api_key,
    to_pretty_json,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Query TickFlow real-time quotes.")
    parser.add_argument("--symbols", help="Comma-separated symbols, for example 600519.SH,AAPL.US")
    parser.add_argument("--universes", help="Comma-separated universe ids")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="TickFlow API base URL")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument("--format", choices=["json", "summary", "table"], default="summary")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    parser.add_argument("--force-post", action="store_true", help="Use POST /v1/quotes")
    return parser


def choose_method(symbols: list[str], universes: list[str], force_post: bool) -> str:
    if force_post:
        return "POST"

    total_items = len(symbols) + len(universes)
    joined_length = len(",".join(symbols)) + len(",".join(universes))
    if total_items > 20 or joined_length > 800:
        return "POST"
    return "GET"


def fetch_quotes(args: argparse.Namespace) -> dict:
    symbols = parse_csv_arg(args.symbols)
    universes = parse_csv_arg(args.universes)
    if not symbols and not universes:
        raise TickFlowError("Provide at least one of --symbols or --universes.")

    api_key = resolve_api_key()
    method = choose_method(symbols, universes, args.force_post)

    if method == "POST":
        body = {
            "symbols": symbols or None,
            "universes": universes or None,
        }
        payload = request_json(
            "POST",
            "/v1/quotes",
            api_key,
            base_url=args.base_url,
            json_body=body,
            timeout=args.timeout,
        )
    else:
        params = {
            "symbols": join_csv(symbols) or None,
            "universes": join_csv(universes) or None,
        }
        payload = request_json(
            "GET",
            "/v1/quotes",
            api_key,
            base_url=args.base_url,
            params=params,
            timeout=args.timeout,
        )

    payload = ensure_dict(payload, name="response")
    payload["data"] = ensure_list(payload.get("data"), name="response.data")
    return payload


def quote_to_row(item: dict) -> dict[str, str]:
    ext = item.get("ext") if isinstance(item.get("ext"), dict) else {}
    return {
        "symbol": str(item.get("symbol", "-")),
        "name": str(ext.get("name") or "-"),
        "region": str(item.get("region", "-")),
        "last": format_number(item.get("last_price")),
        "chg": format_number(ext.get("change_amount")),
        "chg_pct": format_percent(ext.get("change_pct")),
        "volume": format_number(item.get("volume"), 0),
        "session": str(item.get("session") or "-"),
        "time": format_epoch_ms(item.get("timestamp")),
        "amount": format_number(item.get("amount")),
        "open": format_number(item.get("open")),
        "high": format_number(item.get("high")),
        "low": format_number(item.get("low")),
        "prev_close": format_number(item.get("prev_close")),
        "ext_type": str(ext.get("type") or "-"),
    }


def render_summary(data: list[dict]) -> str:
    if not data:
        return "No data returned."

    blocks = []
    for item in data:
        row = quote_to_row(item)
        blocks.append(
            "\n".join(
                [
                    f"{row['symbol']} {row['name']}",
                    f"region={row['region']} last={row['last']} change={row['chg']} ({row['chg_pct']})",
                    f"open={row['open']} high={row['high']} low={row['low']} prev_close={row['prev_close']}",
                    f"volume={row['volume']} amount={row['amount']} session={row['session']}",
                    f"time={row['time']} ext={row['ext_type']}",
                ]
            )
        )
    return "\n\n".join(blocks)


def render_quotes_table(data: list[dict]) -> str:
    rows = [quote_to_row(item) for item in data]
    columns = [
        ("symbol", "symbol"),
        ("name", "name"),
        ("region", "region"),
        ("last", "last"),
        ("chg", "chg"),
        ("chg_pct", "chg%"),
        ("volume", "volume"),
        ("session", "session"),
        ("time", "time"),
    ]
    return render_table(rows, columns)


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        payload = fetch_quotes(args)
        if args.format == "json":
            print(to_pretty_json(payload, args.pretty))
            return

        data = payload["data"]
        if args.format == "table":
            print(render_quotes_table(data))
            return

        print(render_summary(data))
    except TickFlowAPIError as exc:
        raise SystemExit(str(exc))
    except TickFlowError as exc:
        raise SystemExit(str(exc))


if __name__ == "__main__":
    main()
