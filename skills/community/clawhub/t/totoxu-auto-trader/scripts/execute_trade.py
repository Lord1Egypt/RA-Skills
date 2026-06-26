#!/usr/bin/env python3
"""
Trade Execution Script - Auto Crypto Trader
Executes market buy/sell orders on Binance via ccxt.

SECURITY MANIFEST:
- This script uses environment variables for API keys to execute trades
- Keys are never logged or stored to disk
- Uses the official ccxt library for secure exchange communication
- No shell execution
"""

import sys
import json
import argparse
import os

def execute_trade(symbol: str, side: str, amount: float, test_mode: bool) -> dict:
    # We require ccxt for secure exchange communication
    try:
        import ccxt
    except ImportError:
        return {"error": "The 'ccxt' library is required to execute trades. Ask the user to run: pip install ccxt"}

    api_key = os.environ.get('BINANCE_API_KEY')
    secret = os.environ.get('BINANCE_SECRET')

    if not api_key or not secret:
        return {
            "error": "Missing Binance API credentials.",
            "message": "The user must provide BINANCE_API_KEY and BINANCE_SECRET environment variables securely."
        }

    side = side.lower()
    if side not in ['buy', 'sell']:
        return {"error": f"Invalid trade side: {side}. Must be 'buy' or 'sell'."}

    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret,
        'enableRateLimit': True,
        'options': {'defaultType': 'spot'}  # Default to spot trading
    })

    # In test mode, we use the create_test_order function (if supported) or just simulate it
    if test_mode:
        exchange.set_sandbox_mode(True)  # Use Binance Testnet
        
    try:
        # Fetch markets to validate symbol
        exchange.load_markets()
        if symbol not in exchange.markets:
            return {"error": f"Invalid symbol: {symbol}. Make sure it is formatted correctly. Space separated? E.g., BTC/USDT"}

        # Fetch ticker to check current price just for the log
        ticker = exchange.fetch_ticker(symbol)
        current_price = ticker['last']

        # Execute Market Order
        order = exchange.create_market_order(symbol, side, amount)
        
        return {
            "status": "success",
            "message": f"Successfully executed {side.upper()} order for {amount} {symbol}",
            "order_id": order.get('id'),
            "symbol": symbol,
            "side": side,
            "amount": amount,
            "price_executed": order.get('price', current_price), # Sometimes market orders don't return avg fill price immediately
            "status_from_exchange": order.get('status', 'open'),
            "is_testnet": test_mode
        }

    except ccxt.InsufficientFunds as e:
        return {"error": "Insufficient funds in your Binance account to execute this trade.", "details": str(e)}
    except ccxt.InvalidOrder as e:
        return {"error": "Invalid order parameters.", "details": str(e)}
    except ccxt.AuthenticationError as e:
        return {"error": "Authentication failed. Check if API keys are valid and have trading permissions.", "details": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred during trade execution: {str(e)}"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trade execution on Binance")
    parser.add_argument("--symbol", required=True, help="Trading pair (e.g., BTC/USDT)")
    parser.add_argument("--side", required=True, choices=["buy", "sell"], help="buy or sell")
    parser.add_argument("--amount", type=float, required=True, help="Amount in base currency (e.g., amount of BTC)")
    parser.add_argument("--user", required=True, help="User ID for billing")
    parser.add_argument("--testnet", action="store_true", help="Use Binance Testnet instead of Production")
    parser.add_argument("--skip-billing", action="store_true", help="Skip billing for testing")
    
    args = parser.parse_args()
    
    if not args.skip_billing:
        from billing import charge_user
        bill = charge_user(args.user)
        if not bill["ok"]:
            print(json.dumps({"error": "Payment required before executing trade", "payment_url": bill.get("payment_url")}, indent=2))
            sys.exit(1)
            
    print(json.dumps(execute_trade(args.symbol, args.side, args.amount, args.testnet), indent=2))
