#!/usr/bin/env python3
"""
Quant Trading System V3 - Strategy Library + Portfolio + Dashboard + API
"""
import json
import time
import requests
import numpy as np
from typing import Dict, List, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# =============================================================================
# Strategy Library (10+ Strategies)
# =============================================================================

class StrategyLibrary:
    """10+ Trading Strategies"""
    
    STRATEGIES = {
        "momentum": {"name": "Momentum", "logic": lambda f: "LONG" if f.get("rsi", 50) < 35 else "SHORT" if f.get("rsi", 50) > 65 else "HOLD"},
        "mean_reversion": {"name": "Mean Reversion", "logic": lambda f: "LONG" if f.get("rsi", 50) < 30 else "SHORT" if f.get("rsi", 50) > 70 else "HOLD"},
        "breakout": {"name": "Breakout", "logic": lambda f: "LONG" if f.get("close", 0) > f.get("high_20", 0) else "SHORT" if f.get("close", 0) < f.get("low_20", 0) else "HOLD"},
        "macd_cross": {"name": "MACD Crossover", "logic": lambda f: "LONG" if f.get("macd_hist", 0) > 0 else "SHORT" if f.get("macd_hist", 0) < 0 else "HOLD"},
        "supertrend": {"name": "SuperTrend", "logic": lambda f: "LONG" if f.get("close", 0) > f.get("ma20", 0) else "SHORT" if f.get("close", 0) < f.get("ma20", 0) else "HOLD"},
        "rsi_extreme": {"name": "RSI Extreme", "logic": lambda f: "LONG" if f.get("rsi", 50) < 25 else "SHORT" if f.get("rsi", 50) > 75 else "HOLD"},
        "bollinger_bounce": {"name": "Bollinger Bounce", "logic": lambda f: "LONG" if f.get("close", 0) < f.get("bb_lower", 0) else "SHORT" if f.get("close", 0) > f.get("bb_upper", 0) else "HOLD"},
        "trend_following": {"name": "Trend Following", "logic": lambda f: "LONG" if f.get("ma5", 0) > f.get("ma20", 0) else "SHORT" if f.get("ma5", 0) < f.get("ma20", 0) else "HOLD"},
        "volatility_breakout": {"name": "Volatility Breakout", "logic": lambda f: "LONG" if f.get("atr", 0) > f.get("atr_avg", 0) * 1.5 else "SHORT" if f.get("atr", 0) < f.get("atr_avg", 0) * 0.5 else "HOLD"},
        "ai_hybrid": {"name": "AI Hybrid", "logic": lambda f: "LONG" if f.get("rsi", 50) < 40 and f.get("macd_hist", 0) > 0 else "SHORT" if f.get("rsi", 50) > 60 and f.get("macd_hist", 0) < 0 else "HOLD"}
    }
    
    @classmethod
    def list_strategies(cls): return list(cls.STRATEGIES.keys())
    
    @classmethod
    def get_signal(cls, strategy_name: str, factors: Dict) -> Dict:
        if strategy_name not in cls.STRATEGIES:
            return {"signal": "HOLD", "reason": "Unknown"}
        try:
            signal = cls.STRATEGIES[strategy_name]["logic"](factors)
            return {"signal": signal, "strategy": strategy_name}
        except:
            return {"signal": "HOLD", "reason": "Error"}


# =============================================================================
# Portfolio Manager
# =============================================================================

class PortfolioManager:
    def __init__(self, initial_capital: float = 10000):
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.positions = {}
        self.strategies = {s: {"enabled": True, "allocation": 1.0/10} for s in StrategyLibrary.STRATEGIES}
        self.trade_log = []
    
    def update_position(self, symbol: str, strategy: str, signal: str, price: float):
        key = f"{symbol}_{strategy}"
        if signal == "HOLD": return
        
        if key not in self.positions and signal in ["LONG", "SHORT"]:
            alloc = self.capital * self.strategies.get(strategy, {}).get("allocation", 0.1)
            self.positions[key] = {"symbol": symbol, "strategy": strategy, "side": signal.lower(), "size": alloc/price, "entry": price, "time": int(time.time())}
            self.trade_log.append({"action": "OPEN", "symbol": symbol, "side": signal.lower(), "price": price})
        elif key in self.positions:
            p = self.positions[key]
            if (p["side"] == "long" and signal == "SHORT") or (p["side"] == "short" and signal == "LONG"):
                pnl = (price - p["entry"]) / p["entry"] if p["side"] == "long" else (p["entry"] - price) / p["entry"]
                self.capital *= (1 + pnl)
                del self.positions[key]
                self.trade_log.append({"action": "CLOSE", "pnl": pnl})
    
    def get_status(self) -> Dict:
        return {"capital": self.capital, "return": (self.capital-self.initial_capital)/self.initial_capital*100, "positions": len(self.positions), "strategies": list(self.strategies.keys())}


# =============================================================================
# Simple Dashboard
# =============================================================================

class DashboardServer:
    def __init__(self, portfolio: PortfolioManager, port: int = 5000):
        self.portfolio = portfolio
        self.port = port
    
    def start(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if self.path == "/status":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(self.server.portfolio.get_status()).encode())
                elif self.path == "/strategies":
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(StrategyLibrary.list_strategies()).encode())
                else:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h1>Quant Trading System V3</h1><p><a href='/status'>Status</a> | <a href='/strategies'>Strategies</a></p>")
        
        server = HTTPServer(("0.0.0.0", self.port), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()
        return f"Dashboard: http://localhost:{self.port}"


# =============================================================================
# Main System
# =============================================================================

class QuantTradingSystemV3:
    def __init__(self):
        self.portfolio = PortfolioManager()
        self.dashboard = DashboardServer(self.portfolio)
    
    def run_strategy(self, symbol: str, strategy: str, factors: Dict, price: float) -> Dict:
        signal = StrategyLibrary.get_signal(strategy, factors)
        self.portfolio.update_position(symbol, strategy, signal.get("signal", "HOLD"), price)
        return signal
    
    def run_all(self, symbol: str, factors: Dict, price: float) -> Dict:
        results = {}
        for s in self.portfolio.strategies:
            if self.portfolio.strategies[s]["enabled"]:
                results[s] = self.run_strategy(symbol, s, factors, price)
        return results
    
    def start_dashboard(self, port: int = 5000):
        return DashboardServer(self.portfolio, port).start()


if __name__ == "__main__":
    import sys
    system = QuantTradingSystemV3()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "status":
            print(json.dumps(system.portfolio.get_status(), indent=2))
        elif sys.argv[1] == "dashboard":
            print(system.start_dashboard())
        else:
            symbol, strategy = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "momentum"
            factors = {"rsi": 45, "macd_hist": 10}
            print(json.dumps(system.run_strategy(symbol, strategy, factors, 67000), indent=2))
    else:
        factors = {"rsi": 45, "macd_hist": 10, "ma5": 67000, "ma20": 66500}
        results = system.run_all("BTCUSDT", factors, 67000)
        for s, r in results.items():
            print(f"{s}: {r}")
        print("\n", system.portfolio.get_status())
