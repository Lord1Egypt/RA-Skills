import sys
import json
import csv
import argparse
import os
from qc_api.client import QCApiClient
from qc_api.config import get_default_project_id

ORDER_TYPE = {0: "Market", 1: "Limit", 2: "StopMarket", 3: "StopLimit", 4: "MarketOnOpen", 5: "MarketOnClose"}
ORDER_STATUS = {0: "New", 1: "Submitted", 2: "PartiallyFilled", 3: "Filled", 4: "Cancelled", 5: "Invalid"}

def main():
    parser = argparse.ArgumentParser(description="Get results of a completed backtest")
    parser.add_argument("backtest_id", help="Backtest ID")
    parser.add_argument("--project-id", type=int, default=get_default_project_id(), help="QuantConnect Project ID")
    parser.add_argument("--output-dir", default=".", help="Directory to save results")

    args = parser.parse_args()
    os.makedirs(args.output_dir, exist_ok=True)
    client = QCApiClient()

    print(f"Fetching results for Backtest {args.backtest_id}...")

    try:
        # 1. Get main backtest object
        resp = client.read_backtest(args.project_id, args.backtest_id)
        result = resp.get('backtest', resp)

        # Save full stats JSON
        json_path = os.path.join(args.output_dir, f"{args.backtest_id}_result.json")
        with open(json_path, 'w') as f:
            json.dump(resp, f, indent=2)
        print(f"Full result saved to {json_path}")

        # Check for runtime error
        if result.get('error'):
            print(f"\nBacktest ended with error: {result['error']}")

        # 2. Key Statistics
        stats = result.get('statistics', {})
        if stats:
            print("\nKey Statistics:")
            for k in ["Total Orders", "Net Profit", "Sharpe Ratio", "Drawdown", "Win Rate", "Total Fees"]:
                if k in stats:
                    print(f"  - {k}: {stats[k]}")

        # 3. Orders via dedicated endpoint
        all_orders = []
        start_idx = 0
        limit = 100
        while True:
            orders_resp = client.read_backtest_orders(args.project_id, args.backtest_id, start=start_idx, end=start_idx + limit)
            batch = orders_resp.get('orders', [])
            if not batch:
                break
            all_orders.extend(batch)
            # Break if fewer than limit items returned (last page)
            if len(batch) < limit:
                break
            start_idx += limit

        if all_orders:
            csv_path = os.path.join(args.output_dir, f"{args.backtest_id}_orders.csv")
            rows = []
            for o in all_orders:
                symbol = o.get('symbol', {}).get('value', '')
                fill_event = next((e for e in o.get('events', []) if e.get('status') == 'filled'), None)
                rows.append({
                    'orderId':     o.get('id'),
                    'symbol':      symbol,
                    'type':        ORDER_TYPE.get(o.get('type'), o.get('type')),
                    'direction':   'buy' if o.get('direction') == 0 else 'sell',
                    'quantity':    o.get('quantity'),
                    'fillPrice':   fill_event['fillPrice'] if fill_event else '',
                    'fillQty':     fill_event['fillQuantity'] if fill_event else '',
                    'fee':         fill_event.get('orderFeeAmount', '') if fill_event else '',
                    'status':      ORDER_STATUS.get(o.get('status'), o.get('status')),
                    'submitTime':  o.get('time'),
                    'fillTime':    o.get('lastFillTime'),
                    'tag':         o.get('tag'),
                })
            with open(csv_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"Orders ({len(rows)}) saved to {csv_path}")
        else:
            print("No orders in this backtest.")

        # 4. Logs -- not available via QC REST API v2
        # Logs can only be downloaded from the QuantConnect web UI (Backtest > Logs tab).
        print("Logs: not available via API. Download from QC web UI -> Backtest -> Logs tab.")

    except Exception as e:
        print(f"Failed to fetch results: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
