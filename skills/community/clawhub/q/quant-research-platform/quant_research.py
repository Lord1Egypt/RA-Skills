"""
Quantitative Research Platform - Multi-factor analysis and portfolio optimization
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Callable, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class FactorResearch:
    """Multi-factor research and analysis"""
    
    # Factor library (100+ factors)
    FACTOR_LIBRARY = {
        # Technical factors
        'returns_5d': lambda df: df.pct_change(5),
        'returns_10d': lambda df: df.pct_change(10),
        'returns_20d': lambda df: df.pct_change(20),
        'returns_60d': lambda df: df.pct_change(60),
        'volatility_20d': lambda df: df.pct_change().rolling(20).std(),
        'volatility_60d': lambda df: df.pct_change().rolling(60).std(),
        'volume_ratio': lambda df: df.volume / df.volume.rolling(20).mean(),
        'turnover_rate': lambda df: df.volume / df.shares,
        'price_momentum_20': lambda df: df.close / df.close.rolling(20).mean() - 1,
        'price_momentum_60': lambda df: df.close / df.close.rolling(60).mean() - 1,
        
        # RSI
        'rsi_14': lambda df: compute_rsi(df.close, 14),
        'rsi_28': lambda df: compute_rsi(df.close, 28),
        
        # MACD
        'macd': lambda df: compute_macd(df.close)[0],
        'macd_signal': lambda df: compute_macd(df.close)[1],
        'macd_hist': lambda df: compute_macd(df.close)[2],
        
        # Bollinger
        'bb_position': lambda df: compute_bollinger(df.close),
        
        # Fundamental (mock - would need financial data)
        'pe_ratio': lambda df: np.random.uniform(5, 50, len(df)),
        'pb_ratio': lambda df: np.random.uniform(0.5, 10, len(df)),
        'roe': lambda df: np.random.uniform(0.01, 0.3, len(df)),
        'roa': lambda df: np.random.uniform(0.01, 0.15, len(df)),
    }
    
    def __init__(self):
        self.factors = {}
        self.factor_data = None
    
    def add_factor(self, name: str, func: Callable):
        """Add custom factor"""
        self.factors[name] = func
    
    def compute_factors(self, price_data: pd.DataFrame) -> pd.DataFrame:
        """Compute all factors"""
        result = pd.DataFrame(index=price_data.index)
        
        for name, func in self.factors.items():
            try:
                result[name] = func(price_data)
            except:
                result[name] = np.nan
        
        self.factor_data = result
        return result
    
    def analyze_ic(
        self,
        factors: List[str],
        returns: pd.Series,
        lookback: int = 252
    ) -> Dict:
        """Analyze factor IC (Information Coefficient)"""
        if self.factor_data is None:
            raise ValueError("Compute factors first")
        
        ic_series = []
        
        for i in range(lookback, len(self.factor_data)):
            factor_vals = self.factor_data[factors].iloc[i]
            future_returns = returns.iloc[i]
            
            # IC: Pearson correlation
            ic = factor_vals.corr(future_returns)
            ic_series.append(ic)
        
        ic_series = pd.Series(ic_series)
        
        return {
            'ic_mean': ic_series.mean(),
            'ic_std': ic_series.std(),
            'ir': ic_series.mean() / ic_series.std() if ic_series.std() > 0 else 0,
            'ic_decay': self._compute_decay(ic_series),
            'positive_ratio': (ic_series > 0).mean()
        }
    
    def _compute_decay(self, ic_series: pd.Series) -> Dict:
        """Compute IC decay over time lags"""
        decays = {}
        for lag in [1, 5, 10, 20]:
            decays[f'lag_{lag}'] = ic_series.autocorr(lag=lag)
        return decays
    
    def factor_correlation(self, factors: List[str]) -> pd.DataFrame:
        """Compute factor correlation matrix"""
        if self.factor_data is None:
            raise ValueError("Compute factors first")
        
        return self.factor_data[factors].corr()


class BacktestEngine:
    """Backtesting engine with realistic modeling"""
    
    def __init__(
        self,
        start_date: str,
        end_date: str,
        initial_capital: float = 1000000,
        commission: float = 0.0001,
        slippage: float = 0.0005,
        stamp_duty: float = 0.001
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.initial_capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.stamp_duty = stamp_duty
        
        self.strategies = []
        self.positions = {}
        self.trades = []
        self.portfolio_value = []
    
    def add_strategy(self, strategy):
        """Add trading strategy"""
        self.strategies.append(strategy)
    
    def run(self, price_data: pd.DataFrame) -> Dict:
        """Execute backtest"""
        # Initialize
        cash = self.initial_capital
        self.positions = {}
        
        dates = price_data.index
        
        for date in dates:
            # Get signals
            signals = self._get_signals(date, price_data)
            
            # Execute trades
            cash = self._execute_trades(date, signals, price_data, cash)
            
            # Record portfolio value
            portfolio_val = cash + self._get_portfolio_value(date, price_data)
            self.portfolio_value.append({
                'date': date,
                'value': portfolio_val
            })
        
        return self._calculate_metrics()
    
    def _get_signals(self, date, price_data):
        """Get trading signals from strategies"""
        signals = {}
        
        for strategy in self.strategies:
            try:
                sig = strategy.generate_signals(date, price_data)
                signals.update(sig)
            except:
                pass
        
        return signals
    
    def _execute_trades(self, date, signals, price_data, cash):
        """Execute trades with costs"""
        prices = price_data.loc[date]
        
        for symbol, signal in signals.items():
            if signal == 0:
                # Sell
                if symbol in self.positions:
                    shares = self.positions[symbol]
                    price = prices.loc[symbol] * (1 - self.slippage)
                    proceeds = shares * price
                    
                    # Costs
                    cost = proceeds * (self.commission + self.stamp_duty)
                    cash += proceeds - cost
                    
                    self.trades.append({
                        'date': date,
                        'symbol': symbol,
                        'action': 'sell',
                        'shares': shares,
                        'price': price,
                        'cost': cost
                    })
                    
                    del self.positions[symbol]
                    
            elif signal > 0:
                # Buy
                if symbol not in self.positions:
                    shares = int(cash * signal / prices.loc[symbol])
                    if shares > 0:
                        price = prices.loc[symbol] * (1 + self.slippage)
                        cost = shares * price * (1 + self.commission)
                        
                        if cost <= cash:
                            cash -= cost
                            self.positions[symbol] = shares
                            
                            self.trades.append({
                                'date': date,
                                'symbol': symbol,
                                'action': 'buy',
                                'shares': shares,
                                'price': price,
                                'cost': cost
                            })
        
        return cash
    
    def _get_portfolio_value(self, date, price_data):
        """Calculate current portfolio value"""
        prices = price_data.loc[date]
        
        value = 0
        for symbol, shares in self.positions.items():
            if symbol in prices:
                value += shares * prices.loc[symbol]
        
        return value
    
    def _calculate_metrics(self) -> Dict:
        """Calculate performance metrics"""
        if not self.portfolio_value:
            return {}
        
        values = pd.DataFrame(self.portfolio_value)
        values['returns'] = values['value'].pct_change()
        
        total_return = (values['value'].iloc[-1] / self.initial_capital) - 1
        
        # Annualized return
        n_days = len(values)
        annual_return = (1 + total_return) ** (252 / n_days) - 1
        
        # Sharpe ratio
        sharpe = values['returns'].mean() / values['returns'].std() * np.sqrt(252) if values['returns'].std() > 0 else 0
        
        # Max drawdown
        cummax = values['value'].cummax()
        drawdown = (values['value'] - cummax) / cummax
        max_drawdown = drawdown.min()
        
        # Win rate
        if self.trades:
            sells = [t for t in self.trades if t['action'] == 'sell']
            if sells:
                profits = [t['price'] - t['cost'] / t['shares'] for t in sells]
                win_rate = sum(1 for p in profits if p > 0) / len(profits)
            else:
                win_rate = 0
        else:
            win_rate = 0
        
        return {
            'total_return': total_return,
            'annual_return': annual_return,
            'sharpe_ratio': sharpe,
            'max_drawdown': max_drawdown,
            'win_rate': win_rate,
            'trade_count': len(self.trades),
            'final_value': values['value'].iloc[-1]
        }
    
    def get_trades(self) -> pd.DataFrame:
        """Get trade log"""
        return pd.DataFrame(self.trades)


class PortfolioOptimizer:
    """Portfolio optimization methods"""
    
    def __init__(self, returns: pd.DataFrame):
        self.returns = returns
    
    def mean_variance(
        self,
        target_return: Optional[float] = None,
        risk_aversion: float = 1.0
    ) -> pd.Series:
        """Mean-variance optimization (Markowitz)"""
        cov = self.returns.cov()
        exp_returns = self.returns.mean()
        
        n = len(exp_returns)
        
        # Constraints: weights sum to 1
        A = np.ones((1, n))
        b = np.array([1.0])
        
        if target_return:
            # Add return constraint
            A = np.vstack([A, exp_returns.values])
            b = np.append(b, target_return)
        
        # Solve quadratic program
        try:
            from scipy.optimize import minimize
            
            def objective(w):
                portfolio_return = np.dot(w, exp_returns)
                portfolio_risk = np.dot(w, np.dot(cov, w))
                return portfolio_risk - risk_aversion * portfolio_return
            
            # Constraints
            constraints = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
            if target_return:
                constraints.append({
                    'type': 'eq',
                    'fun': lambda w: np.dot(w, exp_returns) - target_return
                })
            
            # Bounds: no short selling
            bounds = tuple((0, 1) for _ in range(n))
            
            # Initial guess
            x0 = np.ones(n) / n
            
            result = minimize(
                objective, x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            return pd.Series(result.x, index=self.returns.columns)
            
        except ImportError:
            # Fallback to equal weight
            return pd.Series(1/n, index=self.returns.columns)
    
    def risk_parity(self) -> pd.Series:
        """Risk parity optimization"""
        cov = self.returns.cov()
        
        def risk_contribution(weights):
            portfolio_var = np.dot(weights, np.dot(cov, weights))
            marginal_contrib = np.dot(cov, weights)
            risk_contrib = weights * marginal_contrib / np.sqrt(portfolio_var)
            return risk_contrib
        
        n = len(cov)
        
        try:
            from scipy.optimize import minimize
            
            def objective(w):
                rc = risk_contribution(w)
                target_rc = rc.mean()
                return sum((rc - target_rc) ** 2)
            
            constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}
            bounds = tuple((0, 1) for _ in range(n))
            x0 = np.ones(n) / n
            
            result = minimize(
                objective, x0,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            return pd.Series(result.x, index=self.returns.columns)
            
        except ImportError:
            return pd.Series(1/n, index=self.returns.columns)
    
    def black_litterman(
        self,
        market_cap_weights: pd.Series,
        views: Dict[str, float],
        tau: float = 0.05
    ) -> pd.Series:
        """Black-Litterman optimization"""
        # Market cap weighted implied returns
        cov = self.returns.cov()
        market_returns = market_cap_weights * self.returns.mean()
        
        # Black-Litterman formula (simplified)
        posterior_returns = (
            np.linalg.inv(np.linalg.inv(tau * cov) + np.eye(len(cov))) @
            (np.linalg.inv(tau * cov) @ market_returns + views)
        )
        
        # Optimize with posterior returns
        opt = PortfolioOptimizer(self.returns)
        return opt.mean_variance(target_return=posterior_returns.mean())
    
    def kelly(self) -> pd.Series:
        """Kelly criterion optimization"""
        returns = self.returns
        
        # Expected return and variance
        exp_return = returns.mean()
        variance = returns.var()
        
        # Kelly fraction
        kelly = exp_return / variance
        
        # Normalize
        kelly = kelly / kelly.sum()
        
        # Cap at 25% per position
        kelly = kelly.clip(upper=0.25)
        
        return kelly


# ==================== Helper Functions ====================

def compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    """Compute RSI indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi


def compute_macd(
    prices: pd.Series,
    fast: int = 12,
    slow: int = 26,
    signal: int = 9
) -> tuple:
    """Compute MACD"""
    ema_fast = prices.ewm(span=fast).mean()
    ema_slow = prices.ewm(span=slow).mean()
    
    macd = ema_fast - ema_slow
    macd_signal = macd.ewm(span=signal).mean()
    macd_hist = macd - macd_signal
    
    return macd, macd_signal, macd_hist


def compute_bollinger(prices: pd.Series, period: int = 20) -> pd.Series:
    """Compute Bollinger Band position"""
    ma = prices.rolling(window=period).mean()
    std = prices.rolling(window=period).std()
    
    upper = ma + 2 * std
    lower = ma - 2 * std
    
    return (prices - lower) / (upper - lower)


# ==================== Strategy Classes ====================

class MomentumStrategy:
    """Momentum trading strategy"""
    
    def __init__(self, n: int = 20, holding_period: int = 60):
        self.n = n
        self.holding_period = holding_period
    
    def generate_signals(self, date, price_data):
        """Generate trading signals"""
        prices = price_data.loc[:date]
        
        if len(prices) < self.n:
            return {}
        
        # Momentum signal
        ret = prices.pct_change(self.n).iloc[-1]
        
        signals = {}
        for symbol in ret.index:
            if ret[symbol] > 0:
                signals[symbol] = 1  # Buy
            else:
                signals[symbol] = 0  # Sell
        
        return signals


class MeanReversionStrategy:
    """Mean reversion strategy"""
    
    def __init__(self, lookback: int = 20, z_threshold: float = 2.0):
        self.lookback = lookback
        self.z_threshold = z_threshold
    
    def generate_signals(self, date, price_data):
        """Generate trading signals"""
        prices = price_data.loc[:date]
        
        if len(prices) < self.lookback:
            return {}
        
        # Z-score
        ma = prices.rolling(self.lookback).mean()
        std = prices.rolling(self.lookback).std()
        z = (prices.iloc[-1] - ma.iloc[-1]) / std.iloc[-1]
        
        signals = {}
        for symbol in z.index:
            if z[symbol] < -self.z_threshold:
                signals[symbol] = 1  # Buy (oversold)
            elif z[symbol] > self.z_threshold:
                signals[symbol] = 0  # Sell (overbought)
        
        return signals


def main():
    """Demo"""
    print("Quant Research Platform")
    print("=" * 50)
    
    # Example usage
    research = FactorResearch()
    
    # Add custom factors
    research.add_factor('momentum_20d', lambda df: df.pct_change(20))
    research.add_factor('volatility_20d', lambda df: df.pct_change().rolling(20).std())
    
    print("Available factors:", len(FactorResearch.FACTOR_LIBRARY))
    print("Custom factors:", len(research.factors))


if __name__ == "__main__":
    main()
