---
name: 越南股市数据服务
description: 一个非官方的MCP服务器，提供访问越南股市数据的工具，包括实时和历史股票价格、公司财务数据、市场统计和基金信息等。
version: 1.0.0
---

# 越南股市数据服务

一个非官方的MCP服务器，提供访问越南股市数据的工具，包括实时和历史股票价格、公司财务数据、市场统计和基金信息等。

---

## ⚠️ 强制要求：API 密钥

**此 Skill 必须配置 API 密钥才能使用。**

- 首次使用时，如果 `.env` 中没有 `XBY_APIKEY`，**必须使用 AskUserQuestion 工具向用户询问 API 密钥**
- 拿到用户提供的密钥后，调用 `scripts.config.set_api_key(api_key)` 保存，然后继续处理
- 获取 API 密钥：https://xiaobenyang.com
- **禁止**在缺少 API 密钥时自行搜索或编造数据

---

## 工作流程（必须遵守）

你（大模型）是路由层，负责理解用户意图、选择工具、提取参数。代码只负责调用API。

```
用户输入 → 你选择工具 → 提取该工具需要的参数 → 调用 scripts.tools 中的函数 → 返回结果给用户
```

### 步骤

1. **检查 API 密钥**：如果 `scripts.config.settings.api_key` 为空，使用 AskUserQuestion 询问用户，拿到后调用 `scripts.config.set_api_key(key)` 保存
2. **选择工具**：根据用户意图从下方工具列表中选择对应的工具函数
3. **提取参数**：根据选中的工具，提取该工具需要的参数
4. **调用工具**：使用**关键字参数**调用 `scripts.tools` 中的函数，例如 `scripts.tools.search_schools(score='520', province='北京', category='综合')`
5. **返回结果**：将工具返回的 `raw` 数据整理后展示给用户

---
## 工具选择规则

根据用户意图选择对应的工具函数：

| 用户意图 | 工具函数 | 
|---------|---------|
| List all ICB industries from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.list_all_icb_industries` |
| List all companies from stock market with details
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.list_all_companies_with_details` |
| Get company overview from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_overview` |
| Get company news from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_news` |
| Get company events from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_events` |
| Get company shareholders from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_shareholders` |
| Get company officers from stock market
Args:
    symbol: str
    filter_by: Literal['working', "all", 'resigned'] = 'working'
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_officers` |
| Get company subsidiaries from stock market
Args:
    symbol: str
    filter_by: Literal["all", "subsidiary"] = "all"
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_subsidiaries` |
| Get company reports from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_reports` |
| Get company dividends from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_dividends` |
| Get company insider deals from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_insider_deals` |
| Get company ratio summary from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_ratio_summary` |
| Get company trading stats from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_company_trading_stats` |
| Get all symbol groups from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_all_symbol_groups` |
| Get all symbols from stock market
Args:
    group: str (group name to get symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_all_symbols_by_group` |
| Get all symbols from stock market
Args:
    industry: str = None (if None, return all symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json | `scripts.tools.get_all_symbols_by_industry` |
| Get all symbols from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json | `scripts.tools.get_all_symbols` |
| Get all symbols detailed from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_all_symbols_detailed` |
| Get income statements of a company from stock market
Args:   
    symbol: str (symbol of the company to get income statements)
    period: Literal['quarter', 'year'] = 'year' (period to get income statements)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_income_statements` |
| Get balance sheets of a company from stock market
Args:
    symbol: str (symbol of the company to get balance sheets)
    period: Literal['quarter', 'year'] = 'year' (period to get balance sheets)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_balance_sheets` |
| Get cash flows of a company from stock market
Args:
    symbol: str (symbol of the company to get cash flows)
    period: Literal['quarter', 'year'] = 'year' (period to get cash flows)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_cash_flows` |
| Get finance ratios of a company from stock market
Args:
    symbol: str (symbol of the company to get finance ratios)
    period: Literal['quarter', 'year'] = 'year' (period to get finance ratios)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_finance_ratios` |
| Get raw report of a company from stock market
Args:
    symbol: str (symbol of the company to get raw report)
    period: Literal['quarter', 'year'] = 'year' (period to get raw report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_raw_report` |
| List all funds from stock market
Args:
    fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None (if None, return funds in all types)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.list_all_funds` |
| Search fund by name from stock market
Args:
    keyword: str (partial match for fund name to search)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.search_fund` |
| Get nav report of a fund from stock market
Args:
    symbol: str (symbol of the fund to get nav report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_fund_nav_report` |
| Get top holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get top holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_fund_top_holding` |
| Get industry holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get industry holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_fund_industry_holding` |
| Get asset holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get asset holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_fund_asset_holding` |
| Get gold price from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    source: Literal['SJC', 'BTMC'] = 'SJC' (source to get gold price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_gold_price` |
| Get exchange rate of all currency pairs from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_exchange_rate` |
| Get quote price with indicators of a symbol from stock market.

Indicators can be specified with or without parameters:
- Simple: "rsi", "macd", "stochastic"
- With params: "rsi(window=21)", "macd(fast=12, slow=26, signal=9)"

Args:
    symbol: str (symbol to get price)
    indicators: list[str] (list of indicators with optional parameters)
        Examples:
        - ["rsi", "macd"] - use default parameters
        - ["rsi(window=21)", "macd(fast=12, slow=26)"] - custom parameters
        - ["stochastic(k=14, d=3)", "cci(window=20)"] - mixed
    start_date: str (format: YYYY-MM-DD)
    end_date: str = None (end date to get price. None means today)
    interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame with OHLCV data and requested indicator columns | `scripts.tools.get_quote_price_with_indicators` |
| Get quote price history of a symbol from stock market
Args:
    symbol: str (symbol to get history price)
    start_date: str (format: YYYY-MM-DD)
    end_date: str = None (end date to get history price. None means today)
    interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get history price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_quote_history_price` |
| Get quote intraday price from stock market
Args:
    symbol: str (symbol to get intraday price)
    page_size: int = 500 (max: 100000) (number of rows to return)
    page: int = 1 (page number to get intraday price from)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_quote_intraday_price` |
| Get quote price depth from stock market
Args:
    symbol: str (symbol to get price depth)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_quote_price_depth` |
| Get price board from stock market
Args:
    symbols: list[str] (list of symbols to get price board)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame | `scripts.tools.get_price_board` |

**如果参数不完整，使用 AskUserQuestion 向用户询问缺失的参数。**

---

## 工具函数说明

---

## scripts.tools.list_all_icb_industries
工具描述：List all ICB industries from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_format|string|false|"toon"|null|

---

## scripts.tools.list_all_companies_with_details
工具描述：List all companies from stock market with details
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_overview
工具描述：Get company overview from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_news
工具描述：Get company news from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|page_size|integer|false|10.0|null|
|page|integer|false|0.0|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_events
工具描述：Get company events from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|page_size|integer|false|10.0|null|
|page|integer|false|0.0|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_shareholders
工具描述：Get company shareholders from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_officers
工具描述：Get company officers from stock market
Args:
    symbol: str
    filter_by: Literal['working', "all", 'resigned'] = 'working'
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|filter_by|string|false|"working"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_subsidiaries
工具描述：Get company subsidiaries from stock market
Args:
    symbol: str
    filter_by: Literal["all", "subsidiary"] = "all"
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|filter_by|string|false|"all"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_reports
工具描述：Get company reports from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_dividends
工具描述：Get company dividends from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_insider_deals
工具描述：Get company insider deals from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_ratio_summary
工具描述：Get company ratio summary from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_company_trading_stats
工具描述：Get company trading stats from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_all_symbol_groups
工具描述：Get all symbol groups from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_all_symbols_by_group
工具描述：Get all symbols from stock market
Args:
    group: str (group name to get symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|group|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_all_symbols_by_industry
工具描述：Get all symbols from stock market
Args:
    industry: str = None (if None, return all symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|industry|string|false| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_all_symbols
工具描述：Get all symbols from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_all_symbols_detailed
工具描述：Get all symbols detailed from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_income_statements
工具描述：Get income statements of a company from stock market
Args:   
    symbol: str (symbol of the company to get income statements)
    period: Literal['quarter', 'year'] = 'year' (period to get income statements)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|period|string|false|"year"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_balance_sheets
工具描述：Get balance sheets of a company from stock market
Args:
    symbol: str (symbol of the company to get balance sheets)
    period: Literal['quarter', 'year'] = 'year' (period to get balance sheets)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|period|string|false|"year"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_cash_flows
工具描述：Get cash flows of a company from stock market
Args:
    symbol: str (symbol of the company to get cash flows)
    period: Literal['quarter', 'year'] = 'year' (period to get cash flows)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|period|string|false|"year"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_finance_ratios
工具描述：Get finance ratios of a company from stock market
Args:
    symbol: str (symbol of the company to get finance ratios)
    period: Literal['quarter', 'year'] = 'year' (period to get finance ratios)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|period|string|false|"year"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_raw_report
工具描述：Get raw report of a company from stock market
Args:
    symbol: str (symbol of the company to get raw report)
    period: Literal['quarter', 'year'] = 'year' (period to get raw report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|period|string|false|"year"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.list_all_funds
工具描述：List all funds from stock market
Args:
    fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None (if None, return funds in all types)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|fund_type|null|false| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.search_fund
工具描述：Search fund by name from stock market
Args:
    keyword: str (partial match for fund name to search)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|keyword|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_fund_nav_report
工具描述：Get nav report of a fund from stock market
Args:
    symbol: str (symbol of the fund to get nav report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_fund_top_holding
工具描述：Get top holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get top holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_fund_industry_holding
工具描述：Get industry holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get industry holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_fund_asset_holding
工具描述：Get asset holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get asset holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_gold_price
工具描述：Get gold price from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    source: Literal['SJC', 'BTMC'] = 'SJC' (source to get gold price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|false| |null|
|source|string|false|"SJC"|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_exchange_rate
工具描述：Get exchange rate of all currency pairs from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|date|string|false| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_quote_price_with_indicators
工具描述：Get quote price with indicators of a symbol from stock market.

Indicators can be specified with or without parameters:
- Simple: "rsi", "macd", "stochastic"
- With params: "rsi(window=21)", "macd(fast=12, slow=26, signal=9)"

Args:
    symbol: str (symbol to get price)
    indicators: list[str] (list of indicators with optional parameters)
        Examples:
        - ["rsi", "macd"] - use default parameters
        - ["rsi(window=21)", "macd(fast=12, slow=26)"] - custom parameters
        - ["stochastic(k=14, d=3)", "cci(window=20)"] - mixed
    start_date: str (format: YYYY-MM-DD)
    end_date: str = None (end date to get price. None means today)
    interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame with OHLCV data and requested indicator columns
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|indicators|array|true| |null|
|start_date|string|true| |null|
|end_date|string|false| |null|
|interval|string|false|"1D"|null|
|drop_market_close|boolean|false|true|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_quote_history_price
工具描述：Get quote price history of a symbol from stock market
Args:
    symbol: str (symbol to get history price)
    start_date: str (format: YYYY-MM-DD)
    end_date: str = None (end date to get history price. None means today)
    interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get history price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|start_date|string|true| |null|
|end_date|string|false| |null|
|interval|string|false|"1D"|null|
|drop_market_close|boolean|false|true|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_quote_intraday_price
工具描述：Get quote intraday price from stock market
Args:
    symbol: str (symbol to get intraday price)
    page_size: int = 500 (max: 100000) (number of rows to return)
    page: int = 1 (page number to get intraday price from)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|page_size|integer|false|100.0|null|
|page|integer|false|1.0|null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_quote_price_depth
工具描述：Get quote price depth from stock market
Args:
    symbol: str (symbol to get price depth)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbol|string|true| |null|
|output_format|string|false|"toon"|null|

---

## scripts.tools.get_price_board
工具描述：Get price board from stock market
Args:
    symbols: list[str] (list of symbols to get price board)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
### 参数定义
|参数名称|参数类型|是否必填|默认值|描述|
|------|-------|------|-----|----|
|symbols|array|true| |null|
|output_format|string|false|"toon"|null|

---


---

## 返回值处理

工具函数返回 `dict` 对象：
- `result["raw"]` - API 原始返回数据（JSON），**直接将此数据整理后展示给用户**
- `result["success"]` - 是否成功（True/False）
- `result["message"]` - 状态消息

---

## 项目结构

```
xiaobenyang_gaokao_skill/
├── scripts/
│   ├── __init__.py
│   ├── config.py       # 配置管理 + set_api_key()
│   ├── call_api.py      # API 客户端 + call_api()
│   └── tools.py         # 工具函数（直接调用）
├── requirements.txt
└── SKILL.md
```

---

## 注意事项

1. **API 密钥是必需的**，无密钥时必须通过 AskUserQuestion 询问用户
2. **禁止**在缺少 API 密钥时自行搜索或编造数据