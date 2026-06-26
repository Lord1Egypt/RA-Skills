# Algorithmic Trading - Sharp Edges

## Strategy Uses Future Data

### **Id**
look-ahead-bias
### **Severity**
critical
### **Summary**
Signal uses information not available at trade time
### **Symptoms**
  - Backtest returns unrealistically high
  - Live trading dramatically underperforms
  - Strategy 'knows' exact highs and lows
### **Why**
  Look-ahead bias occurs when the backtest uses data that wouldn't
  have been available at the time of the trading decision.
  Common sources: using same-day close for signals, peak prices,
  or data that gets revised after publication.
  
### **Gotcha**
  # Using today's close to trade today
  signal = df['close'].pct_change(20)  # 20-day momentum
  df['position'] = np.where(signal > 0, 1, -1)
  
  # This trades on close using close price - impossible!
  
### **Solution**
  # Shift signal by 1 to trade on next bar
  signal = df['close'].pct_change(20)
  df['position'] = np.where(signal.shift(1) > 0, 1, -1)
  
  # Or use event-driven backtest that respects time
  

## Testing on Survivor-Only Data

### **Id**
survivorship-bias
### **Severity**
critical
### **Summary**
Backtest excludes delisted stocks
### **Symptoms**
  - Strategy performs well on historical data
  - Selecting 'value' stocks that all recovered
  - Missing the companies that went bankrupt
### **Why**
  Most data providers only include currently listed stocks.
  This biases results because you're only seeing winners.
  The stocks that failed are missing from your universe.
  
### **Gotcha**
  # Getting S&P 500 constituents
  sp500_tickers = get_current_sp500()  # Today's list
  
  # Backtesting 2010-2020 with 2024 constituents
  # Excludes companies that were in S&P in 2010 but not now
  
### **Solution**
  # Use point-in-time constituents
  for date in trading_dates:
      constituents = get_sp500_at_date(date)
      signals = generate_signals(constituents, date)
  
  # Use survivorship-bias-free data sources
  # - Sharadar, Quandl/Nasdaq, Bloomberg include delistings
  

## Too Many Optimized Parameters

### **Id**
overfitting-params
### **Severity**
high
### **Summary**
Strategy has more parameters than predictive value
### **Symptoms**
  - Perfect in-sample performance
  - Terrible out-of-sample performance
  - Strategy breaks on slight market changes
### **Why**
  With enough parameters, you can fit any historical pattern.
  But this memorizes noise, not signal.
  Rule of thumb: need 252 observations per parameter.
  
### **Gotcha**
  # Too many parameters
  def strategy(lookback1, lookback2, threshold1, threshold2,
               ma_period1, ma_period2, atr_mult, vol_window):
      # 8 parameters = needs 2000+ observations minimum
      pass
  
  # Grid search over 10x10x10x10x10x10x10x10 = 100M combinations
  
### **Solution**
  # Keep it simple
  def strategy(lookback: int, threshold: float):
      # 2 parameters - much more robust
      pass
  
  # Use cross-validation
  from sklearn.model_selection import TimeSeriesSplit
  
  tscv = TimeSeriesSplit(n_splits=5)
  for train_idx, test_idx in tscv.split(data):
      # Optimize on train, validate on test
  

## Ignoring Real Trading Costs

### **Id**
transaction-cost-underestimate
### **Severity**
high
### **Summary**
Backtest assumes zero or minimal costs
### **Symptoms**
  - Profitable backtest, losing live trades
  - High turnover strategy
  - Trading illiquid instruments
### **Why**
  Real costs include: commissions, bid-ask spread, slippage,
  market impact. For high-frequency, impact dominates.
  A strategy with 2% annual edge can easily lose 3% to costs.
  
### **Gotcha**
  # No costs
  returns = position_changes * price_changes
  
  # Or unrealistic costs
  commission = 0.001  # $1 per $1000 traded
  # But spread + slippage can be 0.5-2% for small caps!
  
### **Solution**
  @dataclass
  class RealisticCosts:
      commission_per_share: float = 0.005
      spread_bps: float = 10.0  # Half spread
      slippage_bps: float = 10.0  # Market impact
      min_commission: float = 1.0
  
      def calculate(self, shares, price):
          commission = max(shares * self.commission_per_share, self.min_commission)
          spread = shares * price * (self.spread_bps / 10000)
          slippage = shares * price * (self.slippage_bps / 10000)
          return commission + spread + slippage
  

## Strategy Can't Scale

### **Id**
capacity-ignored
### **Severity**
medium
### **Summary**
Profitable at $10K, fails at $10M
### **Symptoms**
  - Works on paper, fails with real capital
  - Market impact exceeds expected returns
  - Can't get fills at expected prices
### **Why**
  Small strategies have unlimited capacity.
  Large strategies move markets.
  A 1% edge disappears when you need 5% of daily volume to enter.
  
### **Gotcha**
  # Testing with infinite liquidity
  position_size = portfolio_value * signal_strength
  
  # No check if you can actually get that position
  
### **Solution**
  def calculate_capacity(
      target_shares: int,
      average_daily_volume: int,
      max_participation: float = 0.10  # 10% of ADV
  ) -> int:
      """Limit position to what market can absorb."""
      max_shares = int(average_daily_volume * max_participation)
      return min(target_shares, max_shares)
  
  # Also consider: number of days to enter/exit
  