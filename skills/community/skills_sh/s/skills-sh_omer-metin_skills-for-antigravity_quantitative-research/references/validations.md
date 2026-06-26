# Quantitative Research - Validations

## Train/Test Split Required

### **Id**
check-train-test-split
### **Description**
Backtests must separate training and testing data
### **Pattern**
train|test|split|walk.*forward
### **File Glob**
**/*.{py,ipynb}
### **Match**
present
### **Context Pattern**
backtest|simulate|strategy
### **Message**
Backtests require train/test split to avoid overfitting
### **Severity**
error
### **Autofix**


## Transaction Costs Included

### **Id**
check-transaction-costs
### **Description**
Backtests should include realistic transaction costs
### **Pattern**
backtest|simulate|return
### **File Glob**
**/*.{py,ipynb}
### **Match**
present
### **Context Pattern**
cost|slippage|commission|fee
### **Message**
Include transaction costs in backtest - they often exceed alpha
### **Severity**
error
### **Autofix**


## Sharpe Ratio Sanity Check

### **Id**
check-sharpe-sanity
### **Description**
Sharpe ratios above 3 are almost certainly overfit
### **Pattern**
sharpe.*[4-9]\.|sharpe.*[1-9]\d
### **File Glob**
**/*.{py,ipynb}
### **Match**
present
### **Message**
Sharpe ratio appears unrealistically high - check for overfitting
### **Severity**
warning
### **Autofix**


## Look-Ahead Bias Check

### **Id**
check-lookahead-shift
### **Description**
Forward shifts on data indicate potential look-ahead bias
### **Pattern**
shift\(-|\[:-
### **File Glob**
**/*.{py,ipynb}
### **Match**
present
### **Message**
Negative shift detected - verify no look-ahead bias
### **Severity**
warning
### **Autofix**


## Minimum Sample Size

### **Id**
check-sample-size
### **Description**
Strategies need sufficient trades for statistical significance
### **Pattern**
n_trades|num_trades|trade_count
### **File Glob**
**/*.{py,ipynb}
### **Match**
absent
### **Message**
Track number of trades - need 30+ for statistical significance
### **Severity**
warning
### **Autofix**


## Statistical Significance Testing

### **Id**
check-statistical-significance
### **Description**
Results should include significance tests
### **Pattern**
t_stat|p_value|confidence|significance
### **File Glob**
**/*.{py,ipynb}
### **Match**
absent
### **Context Pattern**
backtest|strategy|alpha
### **Message**
Include statistical significance testing for strategy validation
### **Severity**
warning
### **Autofix**


## Out-of-Sample Testing

### **Id**
check-out-of-sample
### **Description**
Strategies must be validated on out-of-sample data
### **Pattern**
out.*sample|oos|holdout|test.*set
### **File Glob**
**/*.{py,ipynb}
### **Match**
absent
### **Context Pattern**
backtest|validate|strategy
### **Message**
Validate strategy on out-of-sample data before deployment
### **Severity**
warning
### **Autofix**


## Survivorship Bias Awareness

### **Id**
check-survivorship-bias
### **Description**
Strategy should account for delisted/dead assets
### **Pattern**
delist|survivor|dead.*asset|bankrupt
### **File Glob**
**/*.{py,ipynb}
### **Match**
absent
### **Context Pattern**
universe|constituent|index
### **Message**
Consider survivorship bias if using historical universe data
### **Severity**
info
### **Autofix**


## Multiple Regime Testing

### **Id**
check-regime-testing
### **Description**
Strategies should be tested across market regimes
### **Pattern**
regime|bull|bear|volatility.*regime|market.*state
### **File Glob**
**/*.{py,ipynb}
### **Match**
absent
### **Context Pattern**
backtest|strategy|performance
### **Message**
Test strategy across different market regimes (bull, bear, sideways)
### **Severity**
info
### **Autofix**


## Parameter Complexity Check

### **Id**
check-parameter-count
### **Description**
Too many parameters indicates potential overfitting
### **Pattern**
param|hyperparameter|tune|optimize
### **File Glob**
**/*.{py,ipynb}
### **Match**
present
### **Message**
Keep parameters minimal (< 5) to reduce overfitting risk
### **Severity**
info
### **Autofix**
