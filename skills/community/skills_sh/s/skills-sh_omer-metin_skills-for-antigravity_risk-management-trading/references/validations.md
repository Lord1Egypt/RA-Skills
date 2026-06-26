# Risk Management Trading - Validations

## Stop Loss Required

### **Id**
check-stop-loss-defined
### **Description**
Every position must have a defined stop loss
### **Pattern**
position|entry|trade
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
stop|stop_loss|exit
### **Message**
Define stop loss for every position
### **Severity**
error
### **Autofix**


## Position Size Calculation

### **Id**
check-position-size-calculation
### **Description**
Position size should be calculated from risk parameters
### **Pattern**
position.*size|size.*position|quantity
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
risk|account|stop
### **Message**
Calculate position size from risk parameters, not arbitrary amounts
### **Severity**
error
### **Autofix**


## Risk Percentage Limits

### **Id**
check-risk-percentage
### **Description**
Risk per trade should be within safe bounds
### **Pattern**
risk.*[5-9]\d*%|risk.*[1-9]\d+%
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Message**
Risk per trade above 5% is dangerous - consider 1-2%
### **Severity**
warning
### **Autofix**


## Leverage Safety Check

### **Id**
check-leverage-limits
### **Description**
High leverage should be flagged
### **Pattern**
leverage.*[5-9]\d*x|leverage.*[1-9]\d+x|10x|20x|50x|100x
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Message**
High leverage (>5x) dramatically increases risk of ruin
### **Severity**
warning
### **Autofix**


## Maximum Drawdown Limit

### **Id**
check-max-drawdown-limit
### **Description**
Strategy should have defined max drawdown threshold
### **Pattern**
max.*drawdown|drawdown.*limit
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Message**
Define maximum acceptable drawdown threshold
### **Severity**
warning
### **Autofix**


## Correlation Analysis

### **Id**
check-correlation-analysis
### **Description**
Multi-asset portfolios should analyze correlation
### **Pattern**
portfolio|multiple.*position|positions
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
correlation|corr|covariance
### **Message**
Analyze correlation for multi-asset portfolios
### **Severity**
info
### **Autofix**


## Risk of Ruin Calculation

### **Id**
check-risk-of-ruin
### **Description**
Systems should calculate probability of account destruction
### **Pattern**
backtest|system|strategy
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
ruin|survive|survival
### **Message**
Calculate risk of ruin before live trading
### **Severity**
info
### **Autofix**


## Volatility-Adjusted Sizing

### **Id**
check-volatility-adjustment
### **Description**
Position sizes should account for asset volatility
### **Pattern**
position.*size
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
volatility|atr|vol
### **Message**
Consider volatility-adjusted position sizing
### **Severity**
info
### **Autofix**


## Slippage in Calculations

### **Id**
check-slippage-modeling
### **Description**
Risk calculations should include slippage estimates
### **Pattern**
backtest|pnl|return
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
slippage|execution.*cost
### **Message**
Include slippage in risk calculations
### **Severity**
warning
### **Autofix**


## Gap Risk Consideration

### **Id**
check-gap-risk
### **Description**
Overnight positions should account for gap risk
### **Pattern**
overnight|hold.*position|swing
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
gap|weekend|overnight.*risk
### **Message**
Account for gap risk in overnight positions
### **Severity**
warning
### **Autofix**
