#!/usr/bin/env python3
import argparse
import json
import sys

import akshare as ak
import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Evaluate a small AKShare expression with ak preloaded.')
    parser.add_argument('--expr', required=True, help='Python expression using ak, pd, or json.')
    parser.add_argument('--max-rows', type=int, default=20, help='Max rows to print for tabular outputs.')
    parser.add_argument('--format', choices=['csv', 'json', 'text'], default='csv')
    args = parser.parse_args()

    env = {'ak': ak, 'pd': pd, 'json': json}
    try:
        result = eval(args.expr, {'__builtins__': __builtins__}, env)
    except Exception as e:
        print(f'EVAL_ERROR: {e}', file=sys.stderr)
        raise

    if isinstance(result, pd.DataFrame):
        out = result.head(args.max_rows)
        if args.format == 'json':
            print(out.to_json(orient='records', force_ascii=False))
        else:
            print(out.to_csv(index=False))
        return

    if isinstance(result, pd.Series):
        out = result.head(args.max_rows)
        if args.format == 'json':
            print(out.to_json(force_ascii=False))
        else:
            print(out.to_csv())
        return

    if isinstance(result, (list, dict, tuple)):
        if args.format == 'text':
            print(result)
        else:
            print(json.dumps(result, ensure_ascii=False, default=str, indent=2))
        return

    print(result)


if __name__ == '__main__':
    main()
