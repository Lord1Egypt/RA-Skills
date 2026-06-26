# Sentiment Analysis Trading - Validations

## Sentiment Signal Backtested

### **Id**
check-sentiment-backtested
### **Description**
Sentiment signals must be backtested before use
### **Pattern**
sentiment|social|twitter|reddit|news
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
backtest|test|validate|ic|correlation
### **Message**
Backtest sentiment signals before using in production
### **Severity**
error
### **Autofix**


## Lead/Lag Analysis Required

### **Id**
check-lag-analysis
### **Description**
Must analyze if sentiment leads or lags price
### **Pattern**
sentiment.*signal|sentiment.*trade
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
lag|lead|granger|causality
### **Message**
Analyze lead/lag relationship - sentiment often lags price
### **Severity**
warning
### **Autofix**


## Data Quality Filtering

### **Id**
check-data-quality-filter
### **Description**
Social data needs quality filters (bots, spam)
### **Pattern**
twitter|reddit|social|discord
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
filter|quality|bot|spam|account.*age
### **Message**
Filter for data quality - bots and spam are prevalent
### **Severity**
warning
### **Autofix**


## Multiple Data Sources

### **Id**
check-multiple-sources
### **Description**
Don't rely on single sentiment source
### **Pattern**
sentiment.*index|composite.*sentiment
### **File Glob**
**/*.{py,js,ts}
### **Match**
absent
### **Context Pattern**
single.*source|only.*twitter
### **Message**
Use multiple sentiment sources for robustness
### **Severity**
info
### **Autofix**


## Manipulation Detection

### **Id**
check-manipulation-detection
### **Description**
Check for coordinated manipulation campaigns
### **Pattern**
twitter|reddit|social
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
coordinate|manipulate|campaign|bot.*detect
### **Message**
Implement manipulation detection for social signals
### **Severity**
info
### **Autofix**


## News Latency Awareness

### **Id**
check-news-latency
### **Description**
Account for news processing latency
### **Pattern**
news.*trade|headline|breaking
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
latency|delay|speed|fast
### **Message**
Account for news latency - by the time you read it, price has moved
### **Severity**
warning
### **Autofix**


## On-Chain Data Verification

### **Id**
check-onchain-verification
### **Description**
Verify on-chain data interpretation
### **Pattern**
on.*chain|whale|exchange.*flow
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
verify|label|known|exchange.*wallet
### **Message**
Verify on-chain data labels and interpretations
### **Severity**
info
### **Autofix**


## Extreme Sentiment Persistence

### **Id**
check-extreme-persistence
### **Description**
Account for persistent extremes in strategy
### **Pattern**
extreme|contrarian|fear|greed
### **File Glob**
**/*.{py,js,ts}
### **Match**
present
### **Context Pattern**
duration|persist|confirm|wait
### **Message**
Account for sentiment extreme persistence in contrarian trades
### **Severity**
info
### **Autofix**
