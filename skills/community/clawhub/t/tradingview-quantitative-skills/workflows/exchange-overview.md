---
description: Exchange Overview Workflow - View exchange information and market configuration
---

# Exchange Overview Workflow

View the list of exchanges supported by TradingView, market configurations, and available asset types.

## Execution Steps

### Step 1: Determine Query Type

Determine query type based on user needs:
- **exchanges**: View exchange list
- **markets**: View market codes
- **tabs**: View leaderboard category tabs
- **columnsets**: View data column configurations
- **languages**: View supported languages

### Step 2: Call Metadata Tool

Call `tradingview_get_metadata` to get configuration information:

```
Parameter description:
- type: Metadata type (required)
  - markets: Market code list (68+ markets)
  - tabs: Leaderboard tabs (categorized by asset type)
  - columnsets: Data column configurations (categorized by asset type)
  - languages: Supported language list
  - exchanges: Exchange list (353+ exchanges)
- asset_type: Asset type filter (optional, only for tabs)
  - stocks, indices, crypto, futures, forex, bonds, corporate_bonds, etfs
```

### Step 3: Format Output

Format output based on query type:

**Exchange List**:
- Stock exchanges: NASDAQ, NYSE, HKEX, SSE, SZSE, TSE, LSE, etc.
- Cryptocurrency exchanges: Binance, Coinbase, Kraken, OKX, Bybit, etc.

**Market Codes**:
- North America: america, canada
- Europe: uk, germany, france
- Asia: china, japan, korea, india
- Others: australia, brazil, etc.

**Leaderboard Tabs**:
- Stocks: gainers, losers, large-cap, active, etc.
- Crypto: all, gainers, losers, large-cap, etc.
- Other asset type tabs

### Step 4: Provide Usage Guidance

Guide users on how to use the obtained information:
- How to use market codes to query leaderboards
- How to use exchange prefixes to search symbols
- How to select appropriate leaderboard tabs

## Example Conversations

**User**: "Which exchanges does TradingView support?"

**Execution**:
1. Call `tradingview_get_metadata`, type="exchanges"
2. Display stock exchanges and cryptocurrency exchanges by category
3. Indicate total number of exchanges (353+)

---

**User**: "What leaderboards are available for US stocks?"

**Execution**:
1. Call `tradingview_get_metadata`, type="tabs", asset_type="stocks"
2. Display stock leaderboard tabs: gainers, losers, large-cap, etc.
3. Explain how to use these tabs to query leaderboards

---

**User**: "Which countries' stock markets are supported?"

**Execution**:
1. Call `tradingview_get_metadata`, type="markets"
2. Display market code list: america, china, japan, uk, etc.
3. Explain that market codes are used for leaderboard queries

---

**User**: "What data columns can be displayed on leaderboards?"

**Execution**:
1. Call `tradingview_get_metadata`, type="columnsets"
2. Display available data columns by asset type:
   - Stocks: overview, performance, valuation, dividends, etc.
   - Crypto: overview, performance, etc.
3. Explain how to use the columnset parameter in leaderboard queries
