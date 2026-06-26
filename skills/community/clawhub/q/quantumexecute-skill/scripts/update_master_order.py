#!/usr/bin/env python3
"""修改母单参数。需认证。"""
import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    parser = argparse.ArgumentParser(description="Update master order parameters")
    parser.add_argument("--master-order-id", type=str, required=True, help="Master order ID to update")
    parser.add_argument("--order-notional", type=float, default=None, help="Order notional (USDT)")
    parser.add_argument("--total-quantity", type=float, default=None, help="Total quantity")
    parser.add_argument("--up-tolerance", type=str, default=None, help="Up tolerance")
    parser.add_argument("--low-tolerance", type=str, default=None, help="Low tolerance")
    parser.add_argument("--enable-make", type=str, default=None, help="Enable maker orders (true/false)")
    parser.add_argument("--maker-rate-limit", type=float, default=None, help="Minimum maker rate (0-1)")
    parser.add_argument("--strict-up-bound", type=str, default=None, help="Strict upper bound (true/false)")
    parser.add_argument("--pov-limit", type=float, default=None, help="Max market volume ratio (0-1)")
    parser.add_argument("--pov-min-limit", type=float, default=None, help="Min market volume ratio (0-1)")
    parser.add_argument("--worst-price", type=float, default=None, help="Worst acceptable price, -1 for no limit")
    parser.add_argument("--tail-order-protection", type=str, default=None, help="Tail order protection (true/false)")
    parser.add_argument("--must-complete", type=str, default=None, help="Must complete within duration (true/false)")
    parser.add_argument("--execution-duration-seconds", type=int, default=None, help="Execution duration in seconds (>10)")
    parser.add_argument("--execution-duration", type=int, default=None, help="Execution duration in minutes (>=1)")
    args = parser.parse_args()

    if args.execution_duration_seconds is not None and args.execution_duration is not None:
        print(
            json.dumps(
                {"success": False, "error": "execution-duration-seconds and execution-duration are mutually exclusive"},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        from _client import get_client

        client = get_client()

        # 构建参数
        params = {}
        if args.order_notional is not None:
            params["orderNotional"] = args.order_notional
        if args.total_quantity is not None:
            params["totalQuantity"] = args.total_quantity
        if args.up_tolerance is not None:
            params["upTolerance"] = args.up_tolerance
        if args.low_tolerance is not None:
            params["lowTolerance"] = args.low_tolerance
        if args.enable_make is not None:
            params["enableMake"] = args.enable_make.lower() == "true"
        if args.maker_rate_limit is not None:
            params["makerRateLimit"] = args.maker_rate_limit
        if args.strict_up_bound is not None:
            params["strictUpBound"] = args.strict_up_bound.lower() == "true"
        if args.pov_limit is not None:
            params["povLimit"] = args.pov_limit
        if args.pov_min_limit is not None:
            params["povMinLimit"] = args.pov_min_limit
        if args.worst_price is not None:
            params["worstPrice"] = args.worst_price
        if args.tail_order_protection is not None:
            params["tailOrderProtection"] = args.tail_order_protection.lower() == "true"
        if args.must_complete is not None:
            params["mustComplete"] = args.must_complete.lower() == "true"
        if args.execution_duration_seconds is not None:
            params["executionDurationSeconds"] = args.execution_duration_seconds
        if args.execution_duration is not None:
            params["executionDuration"] = args.execution_duration

        result = client.update_master_order_params(
            masterOrderId=args.master_order_id,
            **params
        )

        print(json.dumps(result, ensure_ascii=False))

    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
