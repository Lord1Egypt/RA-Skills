#!/usr/bin/env python3
"""
Quant Trading System - Automated Trading
"""
import json
import time
import requests
import numpy as np
from typing import Dict, List

class AutoTrader:
    """Automated Trading System"""
    
    def __init__(self):
        self.balance = 10000.0
        self.initial_balance = 10000.0
        self.positions = []
        self.trade_history = []
        self.wallet = "0x3462abb0b7f4e48580c3b14ea85c3493d656f8ee"
        
        # Config
        self.max_position_pct = 0.1
        self.stop_loss = 0.05
        self.take_profit = 0.10
        
        # Strategies to run
        self.strategies = ["momentum", "mean_reversion", "macd_cross", "supertrend"]
        self.coins = ["BTC", "ETH", "SOL", "XRP"]
    
    def get_price(self, symbol: str) -> float:
        try:
            r = requests.post("https://api.hyperliquid.xyz/info", 
                           json={"type": "allMids"}, timeout=10)
            coin = symbol.replace("USDT", "")
            return float(r.json().get(coin, 0))
        except:
            return 0
    
    def get_indicators(self, symbol: str) -> Dict:
        """Calculate indicators"""
        price = self.get_price(symbol)
        # Simplified - would calculate real RSI/MACD
        np.random.seed(hash(symbol) % 10000)
        return {
            "price": price,
            "rsi": np.random.uniform(30, 70),
            "macd_hist": np.random.uniform(-50, 50),
            "ma5": price * 0.99,
            "ma20": price
        }
    
    def run_strategy(self, name: str, indicators: Dict) -> str:
        """Run strategy and return signal"""
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd_hist", 0)
        
        if name == "momentum":
            return "LONG" if rsi < 40 else "SHORT" if rsi > 60 else "HOLD"
        elif name == "mean_reversion":
            return "LONG" if rsi < 30 else "SHORT" if rsi > 70 else "HOLD"
        elif name == "macd_cross":
            return "LONG" if macd > 0 else "SHORT" if macd < 0 else "HOLD"
        elif name == "supertrend":
            return "LONG" if indicators.get("price", 0) > indicators.get("ma20", 0) else "SHORT"
        return "HOLD"
    
    def check_positions(self):
        """Check and close positions with stop loss / take profit"""
        to_close = []
        for pos in self.positions:
            current_price = self.get_price(pos["symbol"])
            if current_price == 0:
                continue
            
            pnl_pct = (current_price - pos["entry"]) / pos["entry"] if pos["side"] == "long" else \
                      (pos["entry"] - current_price) / pos["entry"]
            
            # Check stop loss
            if pnl_pct < -self.stop_loss:
                to_close.append((pos, "SL"))
            # Check take profit
            elif pnl_pct > self.take_profit:
                to_close.append((pos, "TP"))
        
        # Close positions
        for pos, reason in to_close:
            current_price = self.get_price(pos["symbol"])
            pnl_pct = (current_price - pos["entry"]) / pos["entry"] if pos["side"] == "long" else \
                      (pos["entry"] - current_price) / pos["entry"]
            self.balance *= (1 + pnl_pct)
            self.positions = [p for p in self.positions if p["id"] != pos["id"]]
            print(f"Closed {pos['symbol']} {reason}: PnL {pnl_pct*100:.2f}%")
    
    def open_position(self, symbol: str, side: str):
        """Open new position"""
        price = self.get_price(symbol)
        if price == 0:
            return
        
        # Check if already have position
        if any(p["symbol"] == symbol for p in self.positions):
            return
        
        position_value = self.balance * self.max_position_pct
        size = position_value / price
        
        pos = {
            "id": f"pos_{len(self.positions)}",
            "symbol": symbol,
            "side": side,
            "size": size,
            "entry": price,
            "time": int(time.time())
        }
        
        self.positions.append(pos)
        print(f"Opened {side} {symbol} @ ${price}")
    
    def run(self):
        """Run automated trading"""
        print("\n" + "="*50)
        print("📈 AUTO TRADER RUNNING")
        print("="*50)
        
        # Check existing positions
        self.check_positions()
        
        # Generate signals for each coin
        signals = {}
        for coin in self.coins:
            symbol = f"{coin}USDT"
            indicators = self.get_indicators(symbol)
            
            # Get consensus from strategies
            votes = []
            for strategy in self.strategies:
                signal = self.run_strategy(strategy, indicators)
                votes.append(signal)
            
            # Majority vote
            long_count = votes.count("LONG")
            short_count = votes.count("SHORT")
            
            if long_count > short_count:
                signals[symbol] = "LONG"
            elif short_count > long_count:
                signals[symbol] = "SHORT"
            else:
                signals[symbol] = "HOLD"
        
        # Execute trades
        for symbol, signal in signals.items():
            if signal != "HOLD":
                self.open_position(symbol, signal)
        
        # Summary
        print(f"\nBalance: ${self.balance:.2f}")
        print(f"Positions: {len(self.positions)}")
        for pos in self.positions:
            print(f"  {pos['symbol']}: {pos['side']} @ ${pos['entry']:.2f}")
        
        return {
            "balance": self.balance,
            "positions": len(self.positions),
            "signals": signals
        }
    
    def status(self) -> Dict:
        return {
            "balance": self.balance,
            "return_pct": (self.balance - self.initial_balance) / self.initial_balance * 100,
            "positions": len(self.positions),
            "wallet": self.wallet[:10] + "...",
            "mode": "auto"
        }

if __name__ == "__main__":
    import sys
    trader = AutoTrader()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(trader.status(), indent=2))
        elif sys.argv[1] == "run":
            result = trader.run()
            print(json.dumps(result, indent=2))
    else:
        print(json.dumps(trader.status(), indent=2))
