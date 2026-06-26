#!/usr/bin/env python3
"""
Quant Trading System - Simple CLI Version
"""
import json
import sys

# Core functions
def status():
    print(json.dumps({"capital": 10000, "return": 0, "positions": 0, "strategies": 10}, indent=2))

def list_strategies():
    strategies = ["momentum", "mean_reversion", "breakout", "macd_cross", "supertrend", 
                 "rsi_extreme", "bollinger_bounce", "trend_following", "volatility_breakout", "ai_hybrid"]
    for s in strategies:
        print(f"  - {s}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "status":
            status()
        elif cmd == "strategies":
            list_strategies()
        else:
            print("Usage: python trading_system_simple.py [status|strategies]")
    else:
        status()
