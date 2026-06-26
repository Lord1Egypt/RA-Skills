# Algorithmic Trading - Validations

## Optimization Without Walk-Forward

### **Id**
no-walk-forward
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - optimize.*(?!walk.?forward|time.?series.?split)
  - grid.?search(?!.*TimeSeriesSplit)
### **Message**
Use walk-forward validation for time series to prevent overfitting.
### **Fix Action**
Use: TimeSeriesSplit for cross-validation
### **Applies To**
  - **/*backtest*.py
  - **/*strategy*.py

## Backtest Without Slippage Model

### **Id**
missing-slippage
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - backtest\((?!.*slippage|.*commission|.*cost)
### **Message**
Include realistic transaction costs in backtest.
### **Fix Action**
Add slippage and commission parameters
### **Applies To**
  - **/*.py

## Signal Without Time Shift

### **Id**
no-signal-shift
### **Severity**
error
### **Type**
regex
### **Pattern**
  - position.*=.*signal(?!.*shift)
  - trade.*=.*indicator(?!.*shift)
### **Message**
Shift signals to avoid look-ahead bias - can't trade on today's close.
### **Fix Action**
Add: signal.shift(1) before generating positions
### **Applies To**
  - **/*strategy*.py

## Hardcoded Strategy Parameters

### **Id**
hardcoded-parameters
### **Severity**
info
### **Type**
regex
### **Pattern**
  - lookback\s*=\s*\d+[^#]*$
  - threshold\s*=\s*[0-9.]+[^#]*$
### **Message**
Consider making parameters configurable for optimization.
### **Fix Action**
Use config dict or dataclass for parameters
### **Applies To**
  - **/*strategy*.py

## No Maximum Drawdown Limit

### **Id**
no-max-drawdown-check
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - class.*Strategy(?!.*max_drawdown|.*drawdown_limit)
### **Message**
Implement maximum drawdown limit for risk management.
### **Fix Action**
Add drawdown monitoring and position reduction
### **Applies To**
  - **/*strategy*.py

## Fixed Position Sizing

### **Id**
no-position-sizing
### **Severity**
info
### **Type**
regex
### **Pattern**
  - position.*=.*1\.0|position.*=.*-1\.0
  - shares.*=.*\d+\s*$
### **Message**
Use risk-based position sizing instead of fixed sizes.
### **Fix Action**
Implement Kelly criterion or volatility-adjusted sizing
### **Applies To**
  - **/*.py