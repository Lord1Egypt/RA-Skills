# Risk Management for Trading

## Patterns


---
  #### **Name**
Fixed Fractional Position Sizing
  #### **Description**
Risk a fixed percentage of account per trade
  #### **When**
Standard approach for most traders, simple and effective
  #### **Math**
Position Size = (Account × Risk%) / (Entry - Stop)
  #### **Example**
    Fixed Fractional Formula:
    
    Account: $100,000
    Risk per trade: 1% ($1,000)
    Entry: $50
    Stop: $47 (6% below entry)
    
    Position Size = Risk$ / Risk per Share
    Position Size = $1,000 / ($50 - $47)
    Position Size = $1,000 / $3
    Position Size = 333 shares
    
    Value: 333 × $50 = $16,650 (16.65% of account)
    Max Loss: 333 × $3 = $999 (≈1% of account) ✓
    
    def calculate_position_size(
        account_value: float,
        risk_percent: float,
        entry_price: float,
        stop_price: float
    ) -> dict:
        """Calculate position size for fixed fractional method"""
    
        risk_amount = account_value * risk_percent
        risk_per_share = abs(entry_price - stop_price)
    
        if risk_per_share == 0:
            raise ValueError("Entry and stop cannot be the same price")
    
        shares = int(risk_amount / risk_per_share)
        position_value = shares * entry_price
        position_percent = position_value / account_value
    
        return {
            'shares': shares,
            'position_value': position_value,
            'position_percent': position_percent,
            'risk_amount': risk_per_share * shares,
            'risk_percent_actual': (risk_per_share * shares) / account_value
        }
    

---
  #### **Name**
Kelly Criterion with Fractional Kelly
  #### **Description**
Mathematically optimal bet sizing based on edge and odds
  #### **When**
You have reliable win rate and average win/loss statistics
  #### **Math**
Kelly% = W - (1-W)/R where W=win rate, R=win/loss ratio
  #### **Example**
    Full Kelly Formula:
    
    f* = (bp - q) / b
    
    Where:
    - f* = fraction of bankroll to bet
    - b = odds received on bet (win/loss ratio)
    - p = probability of winning
    - q = probability of losing (1 - p)
    
    Simplified:
    Kelly% = W - (1-W)/R
    
    Example:
    Win rate: 55%
    Average win: $150
    Average loss: $100
    Win/Loss ratio: 1.5
    
    Kelly% = 0.55 - (0.45 / 1.5)
    Kelly% = 0.55 - 0.30
    Kelly% = 0.25 (25% of account)
    
    BUT: Full Kelly is too aggressive!
    
    Fractional Kelly Recommendations:
    - Half Kelly: 12.5% (most common)
    - Quarter Kelly: 6.25% (conservative)
    - Recommended: 25-50% of full Kelly
    
    Why Fractional:
    1. Win rate and R are estimates, not exact
    2. Full Kelly assumes infinite time horizon
    3. Variance is brutal at full Kelly
    4. One bad sequence can devastate account
    
    def kelly_criterion(
        win_rate: float,
        avg_win: float,
        avg_loss: float,
        kelly_fraction: float = 0.5  # Half Kelly
    ) -> dict:
        """Calculate Kelly bet size with fractional adjustment"""
    
        win_loss_ratio = avg_win / avg_loss
        full_kelly = win_rate - ((1 - win_rate) / win_loss_ratio)
    
        # Apply fractional Kelly
        adjusted_kelly = full_kelly * kelly_fraction
    
        # Never negative, cap at reasonable max
        adjusted_kelly = max(0, min(adjusted_kelly, 0.25))
    
        return {
            'full_kelly': full_kelly,
            'adjusted_kelly': adjusted_kelly,
            'kelly_fraction_used': kelly_fraction,
            'expected_growth': (1 + win_loss_ratio * adjusted_kelly) ** win_rate - 1
        }
    

---
  #### **Name**
Volatility-Adjusted Position Sizing
  #### **Description**
Size positions inversely to their volatility
  #### **When**
Trading multiple assets with different volatility profiles
  #### **Math**
Position Size = Target Vol / Asset Vol × Account
  #### **Example**
    Volatility Parity Approach:
    
    Goal: Each position contributes equal volatility to portfolio
    
    Step 1: Calculate asset volatility (ATR or historical vol)
    - BTC: 4% daily vol
    - ETH: 5% daily vol
    - SPY: 1% daily vol
    
    Step 2: Set target volatility contribution
    - Target: 0.5% daily portfolio vol per position
    
    Step 3: Calculate position sizes
    - BTC: 0.5% / 4% = 12.5% of portfolio
    - ETH: 0.5% / 5% = 10% of portfolio
    - SPY: 0.5% / 1% = 50% of portfolio
    
    Result: Each position moves portfolio ~0.5% per day
    
    import numpy as np
    
    def volatility_adjusted_sizing(
        account_value: float,
        target_volatility: float,  # e.g., 0.15 for 15% annual
        assets: list,  # [{'symbol': 'BTC', 'volatility': 0.80, 'price': 50000}, ...]
        max_position_pct: float = 0.25
    ) -> dict:
        """Size positions to achieve target portfolio volatility"""
    
        num_assets = len(assets)
        target_vol_per_asset = target_volatility / np.sqrt(num_assets)
    
        positions = {}
        for asset in assets:
            # Position size to achieve target vol contribution
            raw_allocation = target_vol_per_asset / asset['volatility']
    
            # Cap at maximum position size
            allocation = min(raw_allocation, max_position_pct)
    
            position_value = account_value * allocation
            shares = position_value / asset['price']
    
            positions[asset['symbol']] = {
                'allocation': allocation,
                'value': position_value,
                'shares': shares,
                'vol_contribution': allocation * asset['volatility']
            }
    
        return positions
    

---
  #### **Name**
Maximum Drawdown Limits
  #### **Description**
Reduce or stop trading when drawdown exceeds thresholds
  #### **When**
Protecting capital during losing streaks
  #### **Math**
At X% drawdown, reduce size by Y%. At Z% drawdown, stop trading.
  #### **Example**
    Drawdown Circuit Breakers:
    
    Tier 1: 10% drawdown
    - Reduce position size by 50%
    - Review all open positions
    - No new trades until +5% from lows
    
    Tier 2: 20% drawdown
    - Reduce to 25% of normal size
    - Close all losing positions
    - Only high-conviction setups
    
    Tier 3: 30% drawdown
    - Stop trading completely
    - Full strategy review
    - Consider system is broken
    
    Implementation:
    
    class DrawdownManager:
        def __init__(self, peak_equity, current_equity):
            self.peak = peak_equity
            self.current = current_equity
    
        @property
        def drawdown_pct(self):
            return (self.peak - self.current) / self.peak
    
        def get_size_multiplier(self):
            dd = self.drawdown_pct
    
            if dd < 0.10:
                return 1.0  # Full size
            elif dd < 0.20:
                return 0.5  # Half size
            elif dd < 0.30:
                return 0.25  # Quarter size
            else:
                return 0.0  # Stop trading
    
        def update_equity(self, new_equity):
            self.current = new_equity
            if new_equity > self.peak:
                self.peak = new_equity  # New high water mark
    

---
  #### **Name**
Correlation-Adjusted Portfolio Risk
  #### **Description**
Account for correlated positions in total portfolio risk
  #### **When**
Holding multiple positions that might move together
  #### **Math**
Portfolio Var = Σ(w²σ²) + ΣΣ(w_i × w_j × σ_i × σ_j × ρ_ij)
  #### **Example**
    The Correlation Problem:
    
    You think you have:
    - 5 positions at 2% risk each = 10% total risk
    
    But with 0.7 correlation:
    - Effective risk = much higher
    - In crisis, all 5 drop together
    
    Correlation-Adjusted Risk:
    
    import numpy as np
    
    def portfolio_risk(
        positions: list,  # [{'weight': 0.1, 'vol': 0.3}, ...]
        correlation_matrix: np.ndarray
    ) -> float:
        """Calculate portfolio volatility accounting for correlation"""
    
        weights = np.array([p['weight'] for p in positions])
        vols = np.array([p['vol'] for p in positions])
    
        # Covariance matrix = correlation × outer(vols, vols)
        cov_matrix = correlation_matrix * np.outer(vols, vols)
    
        # Portfolio variance = w' × Cov × w
        port_variance = np.dot(weights, np.dot(cov_matrix, weights))
        port_vol = np.sqrt(port_variance)
    
        return port_vol
    
    # Example
    positions = [
        {'weight': 0.20, 'vol': 0.80},  # BTC
        {'weight': 0.20, 'vol': 0.90},  # ETH
        {'weight': 0.20, 'vol': 0.30},  # TSLA
        {'weight': 0.20, 'vol': 0.20},  # SPY
        {'weight': 0.20, 'vol': 0.15},  # Bonds
    ]
    
    # Crisis correlation matrix (all correlated)
    crisis_corr = np.array([
        [1.0, 0.9, 0.7, 0.6, 0.3],
        [0.9, 1.0, 0.7, 0.6, 0.3],
        [0.7, 0.7, 1.0, 0.8, 0.2],
        [0.6, 0.6, 0.8, 1.0, -0.1],
        [0.3, 0.3, 0.2, -0.1, 1.0],
    ])
    
    risk = portfolio_risk(positions, crisis_corr)
    # Much higher than sum of individual risks!
    

---
  #### **Name**
Stop Loss Optimization
  #### **Description**
Setting stops based on volatility, not arbitrary percentages
  #### **When**
Determining where to place stop losses
  #### **Math**
Stop = Entry - (ATR × Multiplier)
  #### **Example**
    ATR-Based Stop Losses:
    
    Why not fixed percentages:
    - 5% stop on BTC (80% vol) = too tight, constant stops
    - 5% stop on SPY (15% vol) = too wide, too much risk
    
    ATR Method:
    - ATR measures average daily range
    - Stop at 2-3 ATR gives room for normal volatility
    - Adapts to each asset's behavior
    
    import pandas as pd
    
    def calculate_atr_stop(
        df: pd.DataFrame,
        entry_price: float,
        atr_period: int = 14,
        atr_multiplier: float = 2.0,
        direction: str = 'long'
    ) -> dict:
        """Calculate stop loss based on ATR"""
    
        # Calculate ATR
        high_low = df['high'] - df['low']
        high_close = abs(df['high'] - df['close'].shift())
        low_close = abs(df['low'] - df['close'].shift())
    
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = tr.rolling(atr_period).mean().iloc[-1]
    
        # Calculate stop
        stop_distance = atr * atr_multiplier
    
        if direction == 'long':
            stop_price = entry_price - stop_distance
        else:
            stop_price = entry_price + stop_distance
    
        return {
            'atr': atr,
            'stop_distance': stop_distance,
            'stop_price': stop_price,
            'stop_percent': stop_distance / entry_price
        }
    
    # Comparison
    # BTC: ATR = $2000, Stop = $4000 below (8% on $50k)
    # SPY: ATR = $4, Stop = $8 below (1.8% on $450)
    # Both stops account for normal volatility
    

## Anti-Patterns


---
  #### **Name**
Martingale and Averaging Down
  #### **Description**
Doubling position size after losses to recover
  #### **Why**
Mathematically guaranteed to blow up given enough time
  #### **Instead**
    Martingale Logic:
    - Lose $100, bet $200
    - Lose $200, bet $400
    - Eventually win and recover all losses!
    
    Reality:
    - 10 losses in a row: $102,400 bet to recover $100
    - This WILL happen given enough trades
    - Account cannot survive the sequence
    
    Anti-Martingale (Correct):
    - Win: Increase size slightly
    - Lose: Decrease size
    - Protect capital, let winners run
    

---
  #### **Name**
No Stop Loss ("Diamond Hands")
  #### **Description**
Holding losing positions indefinitely hoping for recovery
  #### **Why**
Small losses become account-destroying losses
  #### **Instead**
    "Diamond Hands" Reality:
    - -10%: "I'll wait for recovery"
    - -30%: "It'll come back"
    - -50%: "I can't sell now"
    - -70%: "Might as well hold"
    - -90%: Account destroyed
    
    Every position needs:
    1. Pre-defined stop before entry
    2. Automatic execution (set and forget)
    3. Acceptance that some stops will be wrong
    
    Being stopped out is not failure.
    Account destruction is failure.
    

---
  #### **Name**
Risk of Ruin Ignorance
  #### **Description**
Not calculating probability of account destruction
  #### **Why**
Even positive expectancy systems can go bust with wrong sizing
  #### **Instead**
    Risk of Ruin Formula (simplified):
    
    RoR = ((1 - Edge) / (1 + Edge)) ^ Units
    
    With 55% win rate, 1:1 R:R (10% edge):
    - Risk 10% per trade: 13% ruin probability
    - Risk 5% per trade: 1.7% ruin probability
    - Risk 2% per trade: 0.02% ruin probability
    
    Rule: Risk of ruin should be < 1%
    
    Calculate before trading:
    - What's my edge? (Be conservative)
    - What's my max consecutive losses?
    - What risk per trade keeps ruin near 0%?
    

---
  #### **Name**
Leverage Without Understanding
  #### **Description**
Using high leverage without understanding implications
  #### **Why**
Leverage magnifies losses AND creates path dependency
  #### **Instead**
    Leverage Illusion:
    "10x leverage = 10x returns!"
    
    Leverage Reality:
    - 10% move against you = 100% loss (margin call)
    - Funding costs eat returns
    - Liquidation cascades cause extreme moves
    - You're first to get liquidated in volatility
    
    Safe Leverage Rules:
    - Spot > 3x leverage for most traders
    - Account for volatility (lower leverage for crypto)
    - Position size as if no leverage, then add leverage
    - Stop loss BEFORE liquidation price
    

---
  #### **Name**
Ignoring Correlation in Portfolio
  #### **Description**
Treating correlated assets as independent bets
  #### **Why**
All correlations go to 1 in crisis - you have one big position
  #### **Instead**
    False Diversification:
    - Long BTC
    - Long ETH
    - Long SOL
    "I'm diversified across 3 assets!"
    
    Reality: Correlation > 0.9
    - All drop together in crypto winter
    - Portfolio drawdown = worst asset drawdown
    - No diversification benefit
    
    True Diversification:
    - Uncorrelated return streams
    - Assets that zig when others zag
    - Negative correlation in crises (hard to find)
    

---
  #### **Name**
Sizing Up After Wins
  #### **Description**
Increasing position size after winning streak
  #### **Why**
Mean reversion applies to P&L too - losing streak follows
  #### **Instead**
    Emotional Sizing:
    - 5 wins: "I'm hot, let's go bigger!"
    - Big size trade: Lose
    - Give back all 5 wins in one trade
    
    Correct Approach:
    - Fixed position size rules
    - Same % risk whether winning or losing
    - Let account growth naturally increase $ risk
    - Never manually increase after hot streak
    