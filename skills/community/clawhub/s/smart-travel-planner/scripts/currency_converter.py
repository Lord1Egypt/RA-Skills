#!/usr/bin/env python3
"""
travel-planner/scripts/currency_converter.py
实时汇率转换工具
"""

import argparse
import json
import os
import urllib.request


def get_exchange_rate(from_currency: str, to_currency: str):
    """Get exchange rate using exchangerate-api.com (free tier)"""
    try:
        url = f"https://api.exchangerate-api.com/v4/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode())
            rate = data['rates'].get(to_currency.upper())
            if rate:
                return rate, data['date']
    except Exception as e:
        print(f"Error fetching rate: {e}")
    
    # Fallback to approximate rates
    fallback_rates = {
        'USD': {'CNY': 7.2, 'EUR': 0.92, 'JPY': 150, 'GBP': 0.79},
        'CNY': {'USD': 0.14, 'EUR': 0.13, 'JPY': 21, 'GBP': 0.11},
        'EUR': {'USD': 1.09, 'CNY': 7.85, 'JPY': 163, 'GBP': 0.86},
        'JPY': {'USD': 0.0067, 'CNY': 0.048, 'EUR': 0.0061, 'GBP': 0.0053},
        'GBP': {'USD': 1.27, 'CNY': 9.15, 'EUR': 1.17, 'JPY': 190},
    }
    
    from_rates = fallback_rates.get(from_currency.upper(), {})
    rate = from_rates.get(to_currency.upper())
    if rate:
        return rate, 'fallback'
    return None, None


def convert(amount: float, from_currency: str, to_currency: str):
    rate, source = get_exchange_rate(from_currency, to_currency)
    if rate is None:
        return None
    
    result = amount * rate
    return {
        'amount': amount,
        'from': from_currency.upper(),
        'to': to_currency.upper(),
        'rate': rate,
        'result': round(result, 2),
        'source': 'api' if source != 'fallback' else 'fallback_approximate',
        'rate_date': source if source != 'fallback' else 'N/A',
    }


def main():
    parser = argparse.ArgumentParser(description='Currency converter')
    parser.add_argument('--amount', '-a', type=float, required=True, help='Amount to convert')
    parser.add_argument('--from', '-f', dest='from_currency', required=True, help='Source currency')
    parser.add_argument('--to', '-t', required=True, help='Target currency')
    parser.add_argument('--output', '-o', help='Output JSON file')
    args = parser.parse_args()
    
    result = convert(args.amount, args.from_currency, args.to)
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
    else:
        print(f"Error: Could not convert {args.from_currency} to {args.to}")


if __name__ == '__main__':
    main()
