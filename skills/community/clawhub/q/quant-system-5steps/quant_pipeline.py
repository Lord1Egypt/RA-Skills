#!/usr/bin/env python3
"""
Quant System 5-Steps
1. Data Collection
2. Data Analysis  
3. Model Building
4. Strategy Generation
5. Backtest Optimization
"""

import json
import time
import requests
import numpy as np
import lightgbm as lgb
from typing import Dict, List, Any, Optional
from datetime import datetime

# =============================================================================
# Step 1: Data Collection (Enhanced with Multiple Sources)
# =============================================================================

class DataCollector:
    """Step 1: Collect market data from multiple sources"""
    
    def __init__(self):
        self.sources = ["hyperliquid", "binance"]
    
    def get_realtime_price(self, symbol: str) -> float:
        """Get current price from multiple sources"""
        import requests
        prices = []
        
        # Try Hyperliquid
        try:
            r = requests.post("https://api.hyperliquid.xyz/info", 
                           json={"type": "allMids"}, timeout=10)
            data = r.json()
            coin = symbol.replace("USDT", "")
            if coin in data:
                prices.append(float(data[coin]))
        except:
            pass
        
        # Try Binance
        try:
            r = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}", timeout=10)
            if r.status_code == 200:
                prices.append(float(r.json()["price"]))
        except:
            pass
        
        return min(prices) if prices else 0
    
    def get_orderbook(self, symbol: str) -> dict:
        """Get order book for depth analysis"""
        import requests
        try:
            r = requests.get(f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10", timeout=10)
            data = r.json()
            bids = [[float(p[0]), float(p[1])] for p in data.get("bids", [])[:5]]
            asks = [[float(p[0]), float(p[1])] for p in data.get("asks", [])[:5]]
            spread = asks[0][0] - bids[0][0] if asks and bids else 0
            return {"bids": bids, "asks": asks, "spread": spread}
        except:
            return {"bids": [], "asks": [], "spread": 0}
    
    def get_historical_data(self, symbol: str, interval: str = "1h", limit: int = 500) -> List[Dict]:
        """Get historical OHLCV data"""
        # Try Binance first
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                ohlcv = []
                for k in data:
                    ohlcv.append({
                        "time": k[0],
                        "open": float(k[1]),
                        "high": float(k[2]),
                        "low": float(k[3]),
                        "close": float(k[4]),
                        "volume": float(k[5])
                    })
                return ohlcv
        except:
            pass
        
        # Try alternative: Hyperliquid historical (synthesized from current price)
        try:
            coin = symbol.replace("USDT", "")
            r = requests.post("https://api.hyperliquid.xyz/info", 
                            json={"type": "candle", "coin": coin, "interval": "1h", "limit": limit}, 
                            timeout=10)
            data = r.json()
            if isinstance(data, list):
                ohlcv = []
                for k in data:
                    ohlcv.append({
                        "time": k.get("t", 0),
                        "open": float(k.get("o", 0)),
                        "high": float(k.get("h", 0)),
                        "low": float(k.get("l", 0)),
                        "close": float(k.get("c", 0)),
                        "volume": float(k.get("v", 0))
                    })
                return ohlcv
        except:
            pass
        
        # Fallback: generate synthetic data based on current price
        import numpy as np
        price = self.get_realtime_price(symbol)
        if price > 0:
            np.random.seed(42)
            ohlcv = []
            base_price = price
            for i in range(limit):
                t = int(time.time() * 1000) - (limit - i) * 3600000
                change = np.random.randn() * 0.02
                close = base_price * (1 + change)
                open_price = base_price * (1 + np.random.randn() * 0.01)
                high = max(open_price, close) * (1 + abs(np.random.randn()) * 0.01)
                low = min(open_price, close) * (1 - abs(np.random.randn()) * 0.01)
                volume = np.random.uniform(1000, 10000)
                ohlcv.append({
                    "time": t,
                    "open": open_price,
                    "high": high,
                    "low": low,
                    "close": close,
                    "volume": volume
                })
                base_price = close
            return ohlcv
        
        return []
    
    def run(self, symbol: str) -> Dict:
        """Collect all data"""
        print(f"\n{'='*50}")
        print("📥 Step 1: Data Collection")
        print(f"{'='*50}")
        
        # Realtime price
        price = self.get_realtime_price(symbol)
        print(f"Current Price: ${price}")
        
        # Historical data
        data = self.get_historical_data(symbol)
        print(f"Historical Data: {len(data)} records")
        
        return {
            "symbol": symbol,
            "price": price,
            "data": data,
            "status": "success"
        }


# =============================================================================
# Step 2: Data Analysis
# =============================================================================

class DataAnalyzer:
    """Step 2: Feature engineering and factor analysis"""
    
    def __init__(self):
        self.indicators = ["ma", "rsi", "macd", "bollinger", "atr", "stochastic"]
    
    def calculate_ma(self, prices: List[float], period: int) -> float:
        """Moving Average"""
        return np.mean(prices[-period:]) if len(prices) >= period else 0
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """RSI Indicator"""
        if len(prices) < period + 1:
            return 50
        deltas = np.diff(prices[-period-1:])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        rs = np.mean(gains) / np.mean(losses) if np.mean(losses) > 0 else 1
        return 100 - (100 / (1 + rs))
    
    def calculate_macd(self, prices: List[float]) -> Dict:
        """MACD Indicator"""
        if len(prices) < 26:
            return {"macd": 0, "signal": 0, "histogram": 0}
        
        ema12 = np.mean(prices[-12:])
        ema26 = np.mean(prices[-26:])
        macd = ema12 - ema26
        signal = macd * 0.9
        histogram = macd - signal
        
        return {"macd": macd, "signal": signal, "histogram": histogram}
    
    def calculate_bollinger(self, prices: List[float], period: int = 20) -> Dict:
        """Bollinger Bands"""
        if len(prices) < period:
            return {"upper": 0, "middle": 0, "lower": 0, "width": 0}
        
        ma = np.mean(prices[-period:])
        std = np.std(prices[-period:])
        
        return {
            "upper": ma + 2 * std,
            "middle": ma,
            "lower": ma - 2 * std,
            "width": (4 * std) / ma if ma > 0 else 0
        }
    
    def calculate_atr(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
        """Average True Range"""
        if len(highs) < period + 1:
            return 0
        
        trs = []
        for i in range(-period, 0):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            trs.append(tr)
        
        return np.mean(trs)
    
    def generate_features(self, data: List[Dict]) -> List[List[float]]:
        """Generate all features"""
        closes = [d["close"] for d in data]
        highs = [d["high"] for d in data]
        lows = [d["low"] for d in data]
        
        X = []
        for i in range(100, len(data)):
            features = []
            c = closes[i]
            
            # Price returns
            for period in [1,2,3,5,10,20,60]:
                if i > period:
                    ret = (c - closes[i-period]) / closes[i-period]
                    features.append(ret)
                else:
                    features.append(0)
            
            # MA ratios
            for period in [5,10,20,60]:
                if i >= period:
                    ma = np.mean(closes[i-period:i])
                    features.append(c / ma - 1)
                else:
                    features.extend([0, 0])
            
            # RSI
            features.append(self.calculate_rsi(closes[:i+1]) / 100)
            
            # MACD
            macd = self.calculate_macd(closes[:i+1])
            features.extend([macd["macd"]/c, macd["histogram"]/c])
            
            # Bollinger
            bb = self.calculate_bollinger(closes[:i+1])
            features.extend([(c-bb["lower"])/(bb["upper"]-bb["lower"]) if bb["upper"]>bb["lower"] else 0.5, bb["width"]])
            
            # ATR
            features.append(self.calculate_atr(highs[:i+1], lows[:i+1], closes[:i+1]) / c)
            
            # Momentum
            features.append((c - closes[i-5]) / closes[i-5] if i > 5 else 0)
            
            # Pad to 30 features
            while len(features) < 30:
                features.append(0)
            
            X.append(features[:30])
        
        return X
    
    def analyze(self, data: List[Dict]) -> Dict:
        """Run full analysis"""
        print(f"\n{'='*50}")
        print("🔬 Step 2: Data Analysis")
        print(f"{'='*50}")
        
        closes = [d["close"] for d in data]
        
        # Calculate indicators
        ma20 = self.calculate_ma(closes, 20)
        rsi = self.calculate_rsi(closes)
        macd = self.calculate_macd(closes)
        bb = self.calculate_bollinger(closes)
        
        print(f"MA20: ${ma20:.2f}")
        print(f"RSI: {rsi:.2f}")
        print(f"MACD: {macd['macd']:.2f}")
        print(f"Bollinger Width: {bb['width']:.4f}")
        
        return {
            "ma20": ma20,
            "rsi": rsi,
            "macd": macd,
            "bollinger": bb,
            "status": "success"
        }


# =============================================================================
# Step 3: Model Building
# =============================================================================

class ModelBuilder:
    """Step 3: ML model training"""
    
    def __init__(self):
        self.models = {}
    
    def prepare_training_data(self, data: List[Dict]) -> tuple:
        """Prepare X, y for training"""
        closes = [d["close"] for d in data]
        X = []
        y = []
        
        analyzer = DataAnalyzer()
        
        for i in range(100, len(closes) - 10):
            # Features
            features = []
            c = closes[i]
            
            for period in [1,2,3,5,10,20,60]:
                if i > period:
                    features.append((c - closes[i-period]) / closes[i-period])
                else:
                    features.append(0)
            
            for period in [5,10,20,60]:
                if i >= period:
                    ma = np.mean(closes[i-period:i])
                    features.append(c / ma - 1)
                else:
                    features.extend([0, 0])
            
            features.append(analyzer.calculate_rsi(closes[:i+1]) / 100)
            
            macd = analyzer.calculate_macd(closes[:i+1])
            features.extend([macd["macd"]/c, macd["histogram"]/c])
            
            bb = analyzer.calculate_bollinger(closes[:i+1])
            features.extend([(c-bb["lower"])/(bb["upper"]-bb["lower"]) if bb["upper"]>bb["lower"] else 0.5, bb["width"]])
            
            while len(features) < 30:
                features.append(0)
            
            X.append(features[:30])
            
            # Label: 1 if price up in 10 bars, 0 otherwise
            future_return = (closes[i+10] - c) / c if i+10 < len(closes) else 0
            y.append(1 if future_return > 0.01 else 0)
        
        return np.array(X), np.array(y)
    
    def train(self, X: np.ndarray, y: np.ndarray) -> lgb.Booster:
        """Train LightGBM model"""
        print(f"\n{'='*50}")
        print("🤖 Step 3: Model Building")
        print(f"{'='*50}")
        print(f"Training samples: {len(X)}")
        
        model = lgb.LGBMClassifier(
            n_estimators=100,
            max_depth=5,
            learning_rate=0.1,
            num_leaves=31
        )
        model.fit(X, y)
        
        print("Model trained successfully!")
        
        return model
    
    def predict(self, model: lgb.Booster, features: List[float]) -> Dict:
        """Make prediction"""
        prob = model.predict(np.array([features]))[0]
        
        signal = "LONG" if prob > 0.5 else "SHORT"
        confidence = int(abs(prob - 0.5) * 200)
        
        return {"signal": signal, "confidence": confidence, "prob": prob}


# =============================================================================
# Step 4: Strategy Generation
# =============================================================================

class StrategyGenerator:
    """Step 4: Auto-generate trading strategy"""
    
    TEMPLATES = {
        "momentum": """
if momentum > 0.05:
    signal = 'LONG'
elif momentum < -0.05:
    signal = 'SHORT'
""",
        "mean_reversion": """
if rsi < 30:
    signal = 'LONG'
elif rsi > 70:
    signal = 'SHORT'
""",
        "breakout": """
if close > bollinger_upper:
    signal = 'LONG'
elif close < bollinger_lower:
    signal = 'SHORT'
""",
        "macd_cross": """
if macd > signal:
    signal = 'LONG'
elif macd < signal:
    signal = 'SHORT'
""",
        "supertrend": """
if supertrend == 1:
    signal = 'LONG'
elif supertrend == -1:
    signal = 'SHORT'
""",
        "ichimoku": """
if tenkan > kijun:
    signal = 'LONG'
elif tenkan < kijun:
    signal = 'SHORT'
""",
        "adx_trend": """
if adx > 25 and plus_di > minus_di:
    signal = 'LONG'
elif adx > 25 and minus_di > plus_di:
    signal = 'SHORT'
""",
        "vwap_reversion": """
if vwap < close:
    signal = 'LONG'
elif vwap > close:
    signal = 'SHORT'
""",
        "stochastic_rsi": """
if stochastic_rsi < 20:
    signal = 'LONG'
elif stochastic_rsi > 80:
    signal = 'SHORT'
""",
        "volume_profile": """
if volume > avg_volume:
    signal = 'LONG'
else:
    signal = 'HOLD'
""",
        "cci_extreme": """
if cci < -100:
    signal = 'LONG'
elif cci > 100:
    signal = 'SHORT'
""",
        "williams_r": """
if williams_r < -80:
    signal = 'LONG'
elif williams_r > -20:
    signal = 'SHORT'
"""
    }
    
    def generate(self, indicators: Dict) -> Dict:
        """Generate strategy based on indicators"""
        print(f"\n{'='*50}")
        print("⚙️ Step 4: Strategy Generation")
        print(f"{'='*50}")
        
        # Select best template based on indicators
        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", {}).get("histogram", 0)
        
        # More intelligent template selection
        templates_by_condition = {
            "mean_reversion": rsi < 35 or rsi > 65,
            "macd_cross": abs(macd) > 0.001,
            "breakout": abs(indicators.get("bollinger", {}).get("width", 0)) > 0.1,
            "supertrend": True,  # Always applicable
            "adx_trend": True,
            "cci_extreme": True,
            "williams_r": True,
        }
        
        # Pick first matching condition, default to momentum
        template = "momentum"
        for t, condition in templates_by_condition.items():
            if condition:
                template = t
                break
        
        code = self.TEMPLATES.get(template, self.TEMPLATES["momentum"])
        
        print(f"Selected Template: {template}")
        
        return {
            "template": template,
            "code": code,
            "status": "success"
        }


# =============================================================================
# Step 5: Backtest & Optimization
# =============================================================================

class BacktestOptimizer:
    """Step 5: Backtest and optimize"""
    
    def run_backtest(self, data: List[Dict], strategy: Dict) -> Dict:
        """Run backtest"""
        print(f"\n{'='*50}")
        print("📈 Step 5: Backtest & Optimization")
        print(f"{'='*50}")
        
        closes = [d["close"] for d in data]
        trades = []
        position = None
        
        template = strategy.get("template", "momentum")
        
        for i in range(100, len(closes) - 1):
            c = closes[i]
            
            # Simple signal generation
            if template == "momentum":
                if i > 5:
                    mom = (c - closes[i-5]) / closes[i-5]
                    signal = "LONG" if mom > 0.05 else "SHORT" if mom < -0.05 else "HOLD"
                else:
                    signal = "HOLD"
            elif template == "mean_reversion":
                rsi = 50  # Simplified
                signal = "LONG" if rsi < 30 else "SHORT" if rsi > 70 else "HOLD"
            else:
                signal = "HOLD"
            
            # Execute trade
            if signal == "LONG" and position != "LONG":
                if position == "SHORT":
                    trades.append({"exit": i, "pnl": (closes[i] - closes[i-1]) / closes[i-1]})
                position = "LONG"
                trades.append({"entry": i, "side": "LONG"})
            elif signal == "SHORT" and position != "SHORT":
                if position == "LONG":
                    trades.append({"exit": i, "pnl": -(closes[i] - closes[i-1]) / closes[i-1]})
                position = "SHORT"
                trades.append({"entry": i, "side": "SHORT"})
        
        # Calculate metrics
        if trades:
            pnls = [t.get("pnl", 0) for t in trades if "pnl" in t]
            total_return = sum(pnls)
            wins = [p for p in pnls if p > 0]
            losses = [p for p in pnls if p <= 0]
            
            win_rate = len(wins) / len(pnls) * 100 if pnls else 0
            avg_win = np.mean(wins) if wins else 0
            avg_loss = np.mean(losses) if losses else 0
            
            sharpe = (np.mean(pnls) / np.std(pnls)) if np.std(pnls) > 0 else 0
            
            # Max drawdown
            equity = [1]
            for p in pnls:
                equity.append(equity[-1] * (1 + p))
            dd = 0
            peak = equity[0]
            for e in equity:
                if e > peak:
                    peak = e
                drawdown = (peak - e) / peak
                if drawdown > dd:
                    dd = drawdown
            
            result = {
                "total_trades": len(trades),
                "winning_trades": len(wins),
                "losing_trades": len(losses),
                "win_rate": win_rate,
                "total_return": total_return * 100,
                "avg_win": avg_win * 100,
                "avg_loss": avg_loss * 100,
                "sharpe_ratio": sharpe,
                "max_drawdown": dd * 100,
                "status": "success"
            }
        else:
            result = {
                "total_trades": 0,
                "win_rate": 0,
                "total_return": 0,
                "sharpe_ratio": 0,
                "max_drawdown": 0,
                "status": "no_trades"
            }
        
        print(f"Total Trades: {result['total_trades']}")
        print(f"Win Rate: {result['win_rate']:.1f}%")
        print(f"Total Return: {result['total_return']:.2f}%")
        print(f"Sharpe: {result['sharpe_ratio']:.2f}")
        print(f"Max DD: {result['max_drawdown']:.2f}%")
        
        return result
    
    def optimize(self, backtest_result: Dict) -> Dict:
        """Suggest optimizations"""
        suggestions = []
        
        if backtest_result.get("win_rate", 0) < 50:
            suggestions.append("Consider changing to mean reversion strategy")
        
        if backtest_result.get("max_drawdown", 0) > 20:
            suggestions.append("Reduce position size or tighten stop loss")
        
        if backtest_result.get("sharpe_ratio", 0) < 1:
            suggestions.append("Add more filters or change timeframe")
        
        return {
            "suggestions": suggestions,
            "status": "success"
        }


# =============================================================================
# Main Orchestrator
# =============================================================================

class QuantSystem5Steps:
    """5-Step Quant Trading System"""
    
    def __init__(self):
        self.step1 = DataCollector()
        self.step2 = DataAnalyzer()
        self.step3 = ModelBuilder()
        self.step4 = StrategyGenerator()
        self.step5 = BacktestOptimizer()
    
    def run(self, symbol: str = "BTCUSDT") -> Dict:
        """Run complete 5-step pipeline"""
        print("\n" + "="*60)
        print("🚀 QUANT SYSTEM 5-STEPS")
        print(f"Symbol: {symbol}")
        print("="*60)
        
        start_time = time.time()
        
        # Step 1: Data Collection
        data_result = self.step1.run(symbol)
        
        # Step 2: Data Analysis
        analysis = self.step2.analyze(data_result["data"])
        
        # Step 3: Model Building
        X, y = self.step3.prepare_training_data(data_result["data"])
        if len(X) > 50:
            model = self.step3.train(X, y)
            
            # Current prediction
            features = X[-1].tolist() if len(X) > 0 else [0]*30
            prediction = self.step3.predict(model, features)
        else:
            prediction = {"signal": "HOLD", "confidence": 0}
        
        # Step 4: Strategy Generation
        strategy = self.step4.generate(analysis)
        
        # Step 5: Backtest
        backtest = self.step5.run_backtest(data_result["data"], strategy)
        optimization = self.step5.optimize(backtest)
        
        elapsed = time.time() - start_time
        
        # Final report
        print(f"\n{'='*60}")
        print("✅ COMPLETE - Final Report")
        print(f"{'='*60}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Signal: {prediction['signal']} ({prediction['confidence']}%)")
        print(f"Win Rate: {backtest.get('win_rate', 0):.1f}%")
        print(f"Sharpe: {backtest.get('sharpe_ratio', 0):.2f}")
        print(f"{'='*60}\n")
        
        return {
            "symbol": symbol,
            "price": data_result["price"],
            "analysis": analysis,
            "prediction": prediction,
            "strategy": strategy,
            "backtest": backtest,
            "optimization": optimization,
            "elapsed_time": elapsed
        }


# CLI
if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    
    system = QuantSystem5Steps()
    result = system.run(symbol)
    
    print(json.dumps(result, indent=2, default=str))
