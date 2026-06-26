#!/usr/bin/env python3
import sys
import json
import argparse

def main():
    parser = argparse.ArgumentParser(description='计算 TCA 节省金额')
    parser.add_argument('--tca-metrics', required=True, help='TCA metrics JSON 字符串')
    args = parser.parse_args()

    try:
        metrics = json.loads(args.tca_metrics)

        avg_fill = metrics['AvgFill']
        twap_slippage = metrics['TwapSlippage']
        vwap_slippage = metrics['VwapSlippage']
        take_make_fee_diff = metrics['TakeMakeFeeDiff']
        make_qty = metrics['MakeQty']
        take_qty = metrics['TakeQty']

        total_qty = make_qty + take_qty
        total_notional = total_qty * avg_fill
        maker_rate = make_qty / total_qty if total_qty > 0 else 0

        twap_savings = total_notional * twap_slippage
        vwap_savings = total_notional * vwap_slippage
        fee_savings = total_notional * take_make_fee_diff * maker_rate

        result = {
            "success": True,
            "total_notional": round(total_notional, 4),
            "twap_savings": round(twap_savings, 4),
            "vwap_savings": round(vwap_savings, 4),
            "fee_savings": round(fee_savings, 4),
            "maker_rate": round(maker_rate, 4)
        }
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
