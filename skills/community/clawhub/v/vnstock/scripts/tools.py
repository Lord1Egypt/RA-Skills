from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_all_icb_industries(
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    List all ICB industries from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "list_all_icb_industries", arguments)

def list_all_companies_with_details(
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    List all companies from stock market with details
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "list_all_companies_with_details", arguments)

def get_company_overview(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company overview from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_overview", arguments)

def get_company_news(
    symbol: str,
    page_size: Optional[int] = 10.0,
    page: Optional[int] = 0.0,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company news from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        page_size: null
        page: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "page_size": page_size,
        "page": page,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_news", arguments)

def get_company_events(
    symbol: str,
    page_size: Optional[int] = 10.0,
    page: Optional[int] = 0.0,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company events from stock market
Args:
    symbol: str
    page_size: int = 10
    page: int = 0
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        page_size: null
        page: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "page_size": page_size,
        "page": page,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_events", arguments)

def get_company_shareholders(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company shareholders from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_shareholders", arguments)

def get_company_officers(
    symbol: str,
    filter_by: Optional[str] = "working",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company officers from stock market
Args:
    symbol: str
    filter_by: Literal['working', "all", 'resigned'] = 'working'
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        filter_by: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "filter_by": filter_by,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_officers", arguments)

def get_company_subsidiaries(
    symbol: str,
    filter_by: Optional[str] = "all",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company subsidiaries from stock market
Args:
    symbol: str
    filter_by: Literal["all", "subsidiary"] = "all"
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        filter_by: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "filter_by": filter_by,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_subsidiaries", arguments)

def get_company_reports(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company reports from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_reports", arguments)

def get_company_dividends(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company dividends from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_dividends", arguments)

def get_company_insider_deals(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company insider deals from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_insider_deals", arguments)

def get_company_ratio_summary(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company ratio summary from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_ratio_summary", arguments)

def get_company_trading_stats(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get company trading stats from stock market
Args:
    symbol: str
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_company_trading_stats", arguments)

def get_all_symbol_groups(
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get all symbol groups from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_all_symbol_groups", arguments)

def get_all_symbols_by_group(
    group: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get all symbols from stock market
Args:
    group: str (group name to get symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        group: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "group": group,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_all_symbols_by_group", arguments)

def get_all_symbols_by_industry(
    industry: Optional[str] = None,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get all symbols from stock market
Args:
    industry: str = None (if None, return all symbols)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json
    
    Args:
        industry: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "industry": industry,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_all_symbols_by_industry", arguments)

def get_all_symbols(
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get all symbols from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame or json
    
    Args:
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_all_symbols", arguments)

def get_all_symbols_detailed(
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get all symbols detailed from stock market
    Args:
        output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_all_symbols_detailed", arguments)

def get_income_statements(
    symbol: str,
    period: Optional[str] = "year",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get income statements of a company from stock market
Args:   
    symbol: str (symbol of the company to get income statements)
    period: Literal['quarter', 'year'] = 'year' (period to get income statements)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        period: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_income_statements", arguments)

def get_balance_sheets(
    symbol: str,
    period: Optional[str] = "year",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get balance sheets of a company from stock market
Args:
    symbol: str (symbol of the company to get balance sheets)
    period: Literal['quarter', 'year'] = 'year' (period to get balance sheets)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        period: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_balance_sheets", arguments)

def get_cash_flows(
    symbol: str,
    period: Optional[str] = "year",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get cash flows of a company from stock market
Args:
    symbol: str (symbol of the company to get cash flows)
    period: Literal['quarter', 'year'] = 'year' (period to get cash flows)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        period: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_cash_flows", arguments)

def get_finance_ratios(
    symbol: str,
    period: Optional[str] = "year",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get finance ratios of a company from stock market
Args:
    symbol: str (symbol of the company to get finance ratios)
    period: Literal['quarter', 'year'] = 'year' (period to get finance ratios)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        period: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_finance_ratios", arguments)

def get_raw_report(
    symbol: str,
    period: Optional[str] = "year",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get raw report of a company from stock market
Args:
    symbol: str (symbol of the company to get raw report)
    period: Literal['quarter', 'year'] = 'year' (period to get raw report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        period: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "period": period,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_raw_report", arguments)

def list_all_funds(
    fund_type: Optional[null] = None,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    List all funds from stock market
Args:
    fund_type: Literal['BALANCED', 'BOND', 'STOCK', None ] = None (if None, return funds in all types)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        fund_type: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "fund_type": fund_type,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "list_all_funds", arguments)

def search_fund(
    keyword: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Search fund by name from stock market
Args:
    keyword: str (partial match for fund name to search)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        keyword: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "keyword": keyword,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "search_fund", arguments)

def get_fund_nav_report(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get nav report of a fund from stock market
Args:
    symbol: str (symbol of the fund to get nav report)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_fund_nav_report", arguments)

def get_fund_top_holding(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get top holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get top holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_fund_top_holding", arguments)

def get_fund_industry_holding(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get industry holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get industry holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_fund_industry_holding", arguments)

def get_fund_asset_holding(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get asset holding of a fund from stock market
Args:
    symbol: str (symbol of the fund to get asset holding)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_fund_asset_holding", arguments)

def get_gold_price(
    date: Optional[str] = None,
    source: Optional[str] = "SJC",
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get gold price from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    source: Literal['SJC', 'BTMC'] = 'SJC' (source to get gold price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        date: null
        source: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "source": source,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_gold_price", arguments)

def get_exchange_rate(
    date: Optional[str] = None,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get exchange rate of all currency pairs from stock market
Args:
    date: str = None (if None, return today's price. Format: YYYY-MM-DD)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        date: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "date": date,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_exchange_rate", arguments)

def get_quote_price_with_indicators(
    symbol: str,
    indicators: null,
    start_date: str,
    end_date: Optional[str] = None,
    interval: Optional[str] = "1D",
    drop_market_close: Optional[bool] = True,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get quote price with indicators of a symbol from stock market.

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
    
    Args:
        symbol: null
        indicators: null
        start_date: null
        end_date: null
        interval: null
        drop_market_close: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "indicators": indicators,
        "start_date": start_date,
        "end_date": end_date,
        "interval": interval,
        "drop_market_close": drop_market_close,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_quote_price_with_indicators", arguments)

def get_quote_history_price(
    symbol: str,
    start_date: str,
    end_date: Optional[str] = None,
    interval: Optional[str] = "1D",
    drop_market_close: Optional[bool] = True,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get quote price history of a symbol from stock market
Args:
    symbol: str (symbol to get history price)
    start_date: str (format: YYYY-MM-DD)
    end_date: str = None (end date to get history price. None means today)
    interval: Literal['1m', '5m', '15m', '30m', '1H', '1D', '1W', '1M'] = '1D' (interval to get history price)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        start_date: null
        end_date: null
        interval: null
        drop_market_close: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "start_date": start_date,
        "end_date": end_date,
        "interval": interval,
        "drop_market_close": drop_market_close,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_quote_history_price", arguments)

def get_quote_intraday_price(
    symbol: str,
    page_size: Optional[int] = 100.0,
    page: Optional[int] = 1.0,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get quote intraday price from stock market
Args:
    symbol: str (symbol to get intraday price)
    page_size: int = 500 (max: 100000) (number of rows to return)
    page: int = 1 (page number to get intraday price from)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        page_size: null
        page: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "page_size": page_size,
        "page": page,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_quote_intraday_price", arguments)

def get_quote_price_depth(
    symbol: str,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get quote price depth from stock market
Args:
    symbol: str (symbol to get price depth)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbol: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbol": symbol,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_quote_price_depth", arguments)

def get_price_board(
    symbols: null,
    output_format: Optional[str] = "toon"
) -> Dict[str, Any]:
    """
    Get price board from stock market
Args:
    symbols: list[str] (list of symbols to get price board)
    output_format: Literal['json', 'dataframe', 'toon'] = 'toon' (output format, 'toon' is optimized for AI)
Returns:
    pd.DataFrame
    
    Args:
        symbols: null
        output_format: null
    
    Returns:
        
    """
    arguments = {
        "symbols": symbols,
        "output_format": output_format
    }
    
    return call_api("1777419071036419", "get_price_board", arguments)

