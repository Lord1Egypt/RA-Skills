#!/usr/bin/env python3
"""配对下单：同时创建两个订单"""
import argparse
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_order(client, params):
    return client.create_master_order(**params)


def extract_master_order_id(result):
    if not isinstance(result, dict):
        return None
    for key in ("masterOrderId", "master_order_id", "id", "orderId"):
        value = result.get(key)
        if value:
            return value
    for key in ("data", "result", "order"):
        value = result.get(key)
        if isinstance(value, dict):
            nested = extract_master_order_id(value)
            if nested:
                return nested
    return None


def cancel_created_order(client, master_order_id):
    try:
        return client.cancel_master_order(
            masterOrderId=master_order_id,
            reason="paired order rollback: other leg failed",
        )
    except Exception as exc:
        return {
            "success": False,
            "masterOrderId": master_order_id,
            "error": str(exc),
            "manualActionRequired": True,
        }

def main():
    parser = argparse.ArgumentParser(description="Create paired orders")
    parser.add_argument("--strategy-type", type=str, default="TWAP_1")
    parser.add_argument("--algorithm", type=str, default="TWAP")
    parser.add_argument("--exchange", type=str, required=True)
    parser.add_argument("--api-key-id", type=str, required=True)
    parser.add_argument("--execution-duration", type=int, default=5)
    parser.add_argument("--start-time", type=str, default=None)
    parser.add_argument("--must-complete", action="store_true")

    # Order 1
    parser.add_argument("--symbol-1", type=str, required=True)
    parser.add_argument("--market-type-1", type=str, required=True)
    parser.add_argument("--side-1", type=str, required=True)
    parser.add_argument("--total-quantity-1", type=float, default=None)
    parser.add_argument("--order-notional-1", type=float, default=None)
    parser.add_argument("--margin-type-1", type=str, default=None)

    # Order 2
    parser.add_argument("--symbol-2", type=str, required=True)
    parser.add_argument("--market-type-2", type=str, required=True)
    parser.add_argument("--side-2", type=str, required=True)
    parser.add_argument("--total-quantity-2", type=float, default=None)
    parser.add_argument("--order-notional-2", type=float, default=None)
    parser.add_argument("--margin-type-2", type=str, default=None)

    args = parser.parse_args()

    if (args.total_quantity_1 is None) == (args.order_notional_1 is None):
        print(json.dumps({"error": "Order 1: exactly one of --total-quantity-1 or --order-notional-1 required"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    if (args.total_quantity_2 is None) == (args.order_notional_2 is None):
        print(json.dumps({"error": "Order 2: exactly one of --total-quantity-2 or --order-notional-2 required"}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    try:
        from _client import get_client
        client = get_client()

        # Order 1
        params_1 = {
            "strategyType": args.strategy_type,
            "algorithm": args.algorithm,
            "exchange": args.exchange,
            "symbol": args.symbol_1,
            "marketType": args.market_type_1,
            "side": args.side_1,
            "apiKeyId": args.api_key_id,
            "executionDuration": args.execution_duration,
            "upTolerance": "0.05",
            "lowTolerance": "0.10",
            "strictUpBound": True,
            "notes": "Paired order 1"
        }
        if args.total_quantity_1 is not None:
            params_1["totalQuantity"] = args.total_quantity_1
        else:
            params_1["orderNotional"] = args.order_notional_1
        if args.margin_type_1:
            params_1["marginType"] = args.margin_type_1

        # Order 2
        params_2 = {
            "strategyType": args.strategy_type,
            "algorithm": args.algorithm,
            "exchange": args.exchange,
            "symbol": args.symbol_2,
            "marketType": args.market_type_2,
            "side": args.side_2,
            "apiKeyId": args.api_key_id,
            "executionDuration": args.execution_duration,
            "upTolerance": "0.05",
            "lowTolerance": "0.10",
            "strictUpBound": True,
            "notes": "Paired order 2"
        }
        if args.total_quantity_2 is not None:
            params_2["totalQuantity"] = args.total_quantity_2
        else:
            params_2["orderNotional"] = args.order_notional_2
        if args.margin_type_2:
            params_2["marginType"] = args.margin_type_2

        # 可选参数
        if args.start_time:
            params_1["startTime"] = args.start_time
            params_2["startTime"] = args.start_time
        if args.must_complete:
            params_1["mustComplete"] = True
            params_2["mustComplete"] = True

        # 并发创建
        with ThreadPoolExecutor(max_workers=2) as executor:
            futures = {
                executor.submit(create_order, client, params_1): "order_1",
                executor.submit(create_order, client, params_2): "order_2"
            }

            results = {}
            for future in as_completed(futures):
                order_type = futures[future]
                try:
                    results[order_type] = future.result()
                except Exception as e:
                    results[order_type] = {"error": str(e)}

        has_failure = any(isinstance(value, dict) and value.get("error") for value in results.values())
        if has_failure:
            rollback = {}
            for order_type, result in results.items():
                if isinstance(result, dict) and result.get("error"):
                    continue
                master_order_id = extract_master_order_id(result)
                if master_order_id:
                    rollback[order_type] = cancel_created_order(client, master_order_id)
                else:
                    rollback[order_type] = {
                        "success": False,
                        "error": "masterOrderId not found in successful leg result; manual review required",
                        "manualActionRequired": True,
                    }
            results["rollback"] = rollback
            results["error"] = "paired order failed; attempted rollback for any successfully created leg"
            print(json.dumps(results, ensure_ascii=False, default=str), file=sys.stderr)
            sys.exit(1)

        print(json.dumps(results, ensure_ascii=False, default=str))

    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
