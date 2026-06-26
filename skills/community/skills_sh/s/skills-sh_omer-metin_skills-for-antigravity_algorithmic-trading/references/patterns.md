# Algorithmic Trading

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Never optimize on all data
    ##### **Reason**
Out-of-sample testing prevents overfitting
  
---
    ##### **Rule**
Include realistic costs
    ##### **Reason**
Slippage and commissions kill edge
  
---
    ##### **Rule**
Use event-driven backtests
    ##### **Reason**
Time-based sampling creates look-ahead bias
  
---
    ##### **Rule**
Version everything
    ##### **Reason**
Data, code, models, and parameters
  
---
    ##### **Rule**
Paper trade before live
    ##### **Reason**
Exposes slippage and execution bugs
### **Framework 8 Step**
  #### **Steps**
    - HYPOTHESIS - Define market inefficiency
    - DATA - Collect clean, adjusted data
    - SIGNAL - Generate trading signals
    - BACKTEST - Event-driven with realistic costs
    - OPTIMIZE - Walk-forward optimization
    - VALIDATE - Out-of-sample testing
    - DEPLOY - Paper trade first
    - MONITOR - Track performance, drift
### **Inefficiency Types**
  #### **Microstructure**
Order flow imbalances, bid-ask dynamics
  #### **Behavioral**
Overreaction, anchoring, herding
  #### **Fundamental**
Earnings surprises, value anomalies
  #### **Technical**
Momentum, mean reversion, breakouts
  #### **Statistical**
Pairs trading, factor arbitrage
  #### **Event**
Corporate actions, economic releases
### **Execution Algorithms**
  #### **Twap**
Time-Weighted Average Price
  #### **Vwap**
Volume-Weighted Average Price
  #### **Is**
Implementation Shortfall
  #### **Pov**
Percentage of Volume

## Anti-Patterns


---
  #### **Pattern**
Optimizing on full dataset
  #### **Problem**
Massive overfitting
  #### **Solution**
Walk-forward validation

---
  #### **Pattern**
Ignoring transaction costs
  #### **Problem**
Strategy unprofitable live
  #### **Solution**
Include realistic cost model

---
  #### **Pattern**
Single market testing
  #### **Problem**
Regime-dependent strategy
  #### **Solution**
Test across multiple periods

---
  #### **Pattern**
No position limits
  #### **Problem**
Catastrophic losses
  #### **Solution**
Max position and drawdown limits

---
  #### **Pattern**
Hardcoded parameters
  #### **Problem**
Fails on regime change
  #### **Solution**
Adaptive or robust parameters

---
  #### **Pattern**
Looking at P&L first
  #### **Problem**
Curve fitting
  #### **Solution**
Focus on process, not results