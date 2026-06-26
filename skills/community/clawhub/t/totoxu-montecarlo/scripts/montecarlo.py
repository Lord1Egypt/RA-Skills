#!/usr/bin/env python3
"""
Monte Carlo Crypto Trading Core
Simulates thousands of potential price paths using Geometric Brownian Motion (GBM)
to evaluate trading strategies, stop-loss risks, and expected value.

SECURITY MANIFEST:
- Pure math operations, no external network requests (except billing)
- No filesystem writes
"""

import sys
import json
import argparse
import math
import random

def run_monte_carlo(
    current_price: float,
    volatility: float,
    drift: float,
    days: int,
    paths: int,
    stop_loss: float = None,
    take_profit: float = None,
    position_type: str = 'long'
) -> dict:
    """
    Run Monte Carlo simulation using Geometric Brownian Motion
    volatility and drift should be daily values.
    """
    if paths > 20000:
        return {"error": "Maximum allowed paths is 20000 to prevent timeout."}
    if days > 365:
        return {"error": "Maximum allowed simulation days is 365."}
        
    final_prices = []
    hit_stop_loss_count = 0
    hit_take_profit_count = 0
    win_count = 0
    
    # Calculate daily dt (1 day)
    dt = 1
    
    for _ in range(paths):
        path_price = current_price
        path_terminated = False
        
        for _ in range(days):
            # GBM formula: S_t = S_{t-1} * exp((mu - sigma^2/2) * dt + sigma * z * sqrt(dt))
            # Where z is a random standard normal variable
            
            # Using Box-Muller transform for normal distribution since we avoid importing heavy libraries like numpy in basic skills
            u1 = random.random()
            u2 = random.random()
            z = math.sqrt(-2.0 * math.log(max(u1, 1e-10))) * math.cos(2.0 * math.pi * u2)
            
            exponent = (drift - (volatility ** 2) / 2) * dt + volatility * z * math.sqrt(dt)
            path_price = path_price * math.exp(exponent)
            
            if position_type == 'long':
                if stop_loss is not None and path_price <= stop_loss:
                    hit_stop_loss_count += 1
                    path_terminated = True
                    break
                if take_profit is not None and path_price >= take_profit:
                    hit_take_profit_count += 1
                    path_terminated = True
                    break
            else: # short
                if stop_loss is not None and path_price >= stop_loss:
                    hit_stop_loss_count += 1
                    path_terminated = True
                    break
                if take_profit is not None and path_price <= take_profit:
                    hit_take_profit_count += 1
                    path_terminated = True
                    break
                    
        if not path_terminated:
            final_prices.append(path_price)
            if position_type == 'long' and path_price > current_price:
                win_count += 1
            elif position_type == 'short' and path_price < current_price:
                win_count += 1

    # Statistical Analysis
    if len(final_prices) > 0:
        final_prices.sort()
        expected_price = sum(final_prices) / len(final_prices)
        median_price = final_prices[len(final_prices) // 2]
        
        # 5th and 95th percentiles (Value at Risk)
        idx_5 = int(len(final_prices) * 0.05)
        idx_95 = int(len(final_prices) * 0.95)
        p5_price = final_prices[idx_5] if idx_5 < len(final_prices) else final_prices[0]
        p95_price = final_prices[idx_95] if idx_95 < len(final_prices) else final_prices[-1]
    else:
        expected_price = median_price = p5_price = p95_price = 0

    total_wins = win_count + hit_take_profit_count
    win_probability = (total_wins / paths) * 100
    stop_loss_probability = (hit_stop_loss_count / paths) * 100
    take_profit_probability = (hit_take_profit_count / paths) * 100

    return {
        "status": "success",
        "inputs": {
            "current_price": current_price,
            "volatility_daily": volatility,
            "drift_daily": drift,
            "days": days,
            "paths": paths,
            "position_type": position_type,
            "stop_loss": stop_loss,
            "take_profit": take_profit
        },
        "results": {
            "expected_price": round(expected_price, 2),
            "median_price": round(median_price, 2),
            "p5_worst_case_price": round(p5_price, 2),
            "p95_best_case_price": round(p95_price, 2)
        },
        "risk_metrics": {
            "win_probability_pct": round(win_probability, 2),
            "hit_stop_loss_pct": round(stop_loss_probability, 2),
            "hit_take_profit_pct": round(take_profit_probability, 2),
            "survived_paths": len(final_prices)
        },
        "conclusion": "FAVORABLE" if win_probability > 50 else "UNFAVORABLE"
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monte Carlo Trading Engine")
    parser.add_argument("--price", type=float, required=True, help="Current asset price")
    parser.add_argument("--vol", type=float, required=True, help="Daily volatility (e.g. 0.05 for 5%)")
    parser.add_argument("--drift", type=float, default=0.0, help="Daily expected return/drift (e.g. 0.001)")
    parser.add_argument("--days", type=int, default=30, help="Days to simulate")
    parser.add_argument("--paths", type=int, default=10000, help="Number of Monte Carlo paths")
    parser.add_argument("--stop-loss", type=float, default=None, help="Stop loss price level")
    parser.add_argument("--take-profit", type=float, default=None, help="Take profit price level")
    parser.add_argument("--position", choices=['long', 'short'], default='long', help="Position type")
    
    parser.add_argument("--user", required=True, help="User ID for billing")
    parser.add_argument("--skip-billing", action="store_true", help="Skip billing for testing")
    
    args = parser.parse_args()
    
    if not args.skip_billing:
        from billing import charge_user
        bill = charge_user(args.user)
        if not bill["ok"]:
            print(json.dumps({"error": "Payment required", "payment_url": bill.get("payment_url")}, indent=2))
            sys.exit(1)
            
    result = run_monte_carlo(
        args.price, args.vol, args.drift, args.days, args.paths, 
        args.stop_loss, args.take_profit, args.position
    )
    print(json.dumps(result, indent=2))
