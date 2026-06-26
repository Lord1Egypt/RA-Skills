#!/usr/bin/env python3
"""创建主订单（TWAP/VWAP/POV 等）。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _normalize_strategy_type(value: str) -> str:
    normalized = (value or "").strip().upper().replace("_", "-")
    if normalized == "TWAP-1":
        return "TWAP-1"
    if normalized == "POV":
        return "POV"
    return value


def main():
    parser = argparse.ArgumentParser(description="Create master order")
    # 必传
    parser.add_argument("--strategy-type", type=str, required=True, help="TWAP-1 or POV (TWAP_1 is also accepted)")
    parser.add_argument("--algorithm", type=str, required=True, help="TWAP, VWAP, POV")
    parser.add_argument("--exchange", type=str, required=True, help="Binance, OKX, LTP, Deribit, Hyperliquid")
    parser.add_argument("--symbol", type=str, required=True, help="e.g. BTCUSDT")
    parser.add_argument("--market-type", type=str, required=True, help="SPOT or PERP")
    parser.add_argument("--side", type=str, required=True, help="buy or sell")
    parser.add_argument("--api-key-id", type=str, required=True, help="Exchange API key ID from list_exchange_apis")
    # 数量二选一
    parser.add_argument("--total-quantity", type=float, default=None, help="Total quantity (or use --order-notional)")
    parser.add_argument("--order-notional", type=float, default=None, help="Order notional amount (or use --total-quantity)")
    # 可选
    parser.add_argument("--is-target-position", action="store_true", help="Target position mode")
    parser.add_argument("--start-time", type=str, default=None, help="ISO8601 e.g. 2025-09-03T01:30:00+08:00")
    parser.add_argument("--execution-duration", type=int, default=None, help="Max execution duration in minutes")
    parser.add_argument("--execution-duration-seconds", type=int, default=None, help="Execution duration seconds (TWAP-1/POV, >10)")
    parser.add_argument("--must-complete", action="store_true", help="Must complete within duration")
    parser.add_argument("--maker-rate-limit", type=float, default=None, help="Maker ratio 0-1")
    parser.add_argument("--pov-limit", type=str, default=None, help="POV limit 0-1")
    parser.add_argument("--pov-min-limit", type=float, default=None, help="POV min limit")
    parser.add_argument("--limit-price", type=float, default=None, help="Price limit, -1 for no limit")
    parser.add_argument("--up-tolerance", type=str, default=None, help="Up tolerance 0-1")
    parser.add_argument("--low-tolerance", type=str, default=None, help="Low tolerance 0-1")
    parser.add_argument("--strict-up-bound", action="store_true", help="Strict up bound")
    parser.add_argument("--tail-order-protection", action="store_true", help="Tail order protection")
    parser.add_argument("--no-tail-order-protection", action="store_true", help="Disable tail order protection")
    parser.add_argument("--reduce-only", action="store_true", help="Reduce only (futures)")
    parser.add_argument("--margin-type", type=str, default=None, help="U or C (required for PERP)")
    parser.add_argument("--is-margin", action="store_true", help="Use spot margin")
    parser.add_argument("--notes", type=str, default=None, help="Order notes")
    parser.add_argument("--enable-make", action="store_true", help="Allow maker orders")
    parser.add_argument("--no-enable-make", action="store_true", help="Disable maker orders")
    parser.add_argument("--client-order-id", type=str, default=None, help="Custom client order ID")
    args = parser.parse_args()

    if (args.total_quantity is None) == (args.order_notional is None):
        print(json.dumps({"error": "Exactly one of --total-quantity or --order-notional required"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    if args.is_target_position and args.order_notional is not None:
        print(json.dumps({"error": "When --is-target-position, use only --total-quantity"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    try:
        from _client import get_client
        client = get_client()
        params = {
            "strategyType": _normalize_strategy_type(args.strategy_type),
            "algorithm": args.algorithm,
            "exchange": args.exchange,
            "symbol": args.symbol,
            "marketType": args.market_type,
            "side": args.side,
            "apiKeyId": args.api_key_id,
        }
        if args.total_quantity is not None:
            params["totalQuantity"] = args.total_quantity
        else:
            params["orderNotional"] = args.order_notional
        if args.is_target_position:
            params["isTargetPosition"] = True
        if args.start_time is not None:
            params["startTime"] = args.start_time
        if args.execution_duration is not None:
            params["executionDuration"] = args.execution_duration
        if args.execution_duration_seconds is not None:
            params["executionDurationSeconds"] = args.execution_duration_seconds
        if args.must_complete:
            params["mustComplete"] = True
        if args.maker_rate_limit is not None:
            params["makerRateLimit"] = args.maker_rate_limit
        if args.pov_limit is not None:
            params["povLimit"] = args.pov_limit
        if args.pov_min_limit is not None:
            params["povMinLimit"] = args.pov_min_limit
        if args.limit_price is not None:
            params["limitPrice"] = args.limit_price
        if args.up_tolerance is not None:
            params["upTolerance"] = args.up_tolerance
        if args.low_tolerance is not None:
            params["lowTolerance"] = args.low_tolerance
        if args.strict_up_bound:
            params["strictUpBound"] = True
        if args.tail_order_protection:
            params["tailOrderProtection"] = True
        if args.no_tail_order_protection:
            params["tailOrderProtection"] = False
        if args.reduce_only:
            params["reduceOnly"] = True
        if args.margin_type is not None:
            params["marginType"] = args.margin_type
        if args.is_margin:
            params["isMargin"] = True
        if args.notes is not None:
            params["notes"] = args.notes
        if args.enable_make:
            params["enableMake"] = True
        if args.no_enable_make:
            params["enableMake"] = False
        if args.client_order_id is not None:
            params["clientOrderId"] = args.client_order_id
        result = client.create_master_order(**params)
        print(json.dumps(result, ensure_ascii=False, default=str))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
