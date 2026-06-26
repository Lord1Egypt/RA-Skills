"""
yfinance Client - A convenient wrapper for Yahoo Finance data retrieval.

This client provides methods for querying US and Hong Kong stock data,
including historical prices, company information, analyst data, and more.
"""

from datetime import datetime, timedelta
from typing import Optional, Union, List, Dict, Any

import yfinance as yf


class YFinanceClient:
    """
    A client for retrieving stock data from Yahoo Finance.

    Supports both US stocks (e.g., AAPL, MSFT) and Hong Kong stocks
    (e.g., 0700.HK, 9988.HK).

    Example usage:
        client = YFinanceClient()

        # Get stock price
        price = client.get_price("AAPL")

        # Get historical data
        hist = client.get_history("AAPL", period="1mo")

        # Get company info
        info = client.get_company_info("0700.HK")

        # Get recommendations
        recs = client.get_recommendations("MSFT")

        # Get day gainers
        gainers = client.get_screener("day_gainers")
    """

    def __init__(self, timeout: int = 30):
        """
        Initialize the yfinance client.

        Args:
            timeout: Request timeout in seconds (default: 30)
        """
        self.timeout = timeout
        yf.timeout = timeout

    def _get_ticker(self, symbol: str) -> yf.Ticker:
        """Get a yfinance Ticker object."""
        # Add .HK suffix for Hong Kong stocks if not present
        if symbol.isdigit() and len(symbol) == 4:
            symbol = f"{symbol}.HK"
        return yf.Ticker(symbol)

    # ==================== Price & History ====================

    def get_price(self, symbol: str) -> float:
        """
        Get current stock price.

        Args:
            symbol: Stock symbol (e.g., "AAPL" or "0700.HK")

        Returns:
            Current stock price as float
        """
        ticker = self._get_ticker(symbol)
        return ticker.info.get("currentPrice") or ticker.info.get("regularMarketPreviousClose")

    def get_history(
        self,
        symbol: str,
        period: Optional[str] = None,
        interval: str = "1d",
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> "pd.DataFrame":
        """
        Get historical stock data.

        Args:
            symbol: Stock symbol (e.g., "AAPL" or "0700.HK")
            period: Data period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Data interval (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 1wk, 1mo)
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)

        Returns:
            DataFrame with columns: Open, High, Low, Close, Volume, Dividends, Stock Splits
        """
        ticker = self._get_ticker(symbol)
        if period:
            return ticker.history(period=period, interval=interval)
        return ticker.history(interval=interval, start=start, end=end)

    def get_fast_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get fast stock information.

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with fast info (last_price, last_volume, etc.)
        """
        ticker = self._get_ticker(symbol)
        return ticker.fast_info

    # ==================== Company Info ====================

    def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get company information.

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with company info (name, industry, sector, employees, etc.)
        """
        ticker = self._get_ticker(symbol)
        return ticker.info

    def get_company_summary(self, symbol: str) -> str:
        """
        Get company business summary.

        Args:
            symbol: Stock symbol

        Returns:
            Company business summary as string
        """
        ticker = self._get_ticker(symbol)
        return ticker.info.get("longBusinessSummary", "")

    def get_major_holders(self, symbol: str) -> "pd.DataFrame":
        """
        Get major holders of the stock.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with holder information
        """
        ticker = self._get_ticker(symbol)
        return ticker.major_holders

    def get_institutional_holders(self, symbol: str) -> "pd.DataFrame":
        """
        Get institutional holders of the stock.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with institutional holder information
        """
        ticker = self._get_ticker(symbol)
        return ticker.institutional_holders

    def get_mutualfund_holders(self, symbol: str) -> "pd.DataFrame":
        """
        Get mutual fund holders of the stock.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with mutual fund holder information
        """
        ticker = self._get_ticker(symbol)
        return ticker.mutualfund_holders

    # ==================== Financials ====================

    def get_financials(self, symbol: str) -> "pd.DataFrame":
        """
        Get company financials (income statement).

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with financials
        """
        ticker = self._get_ticker(symbol)
        return ticker.financials

    def get_balance_sheet(self, symbol: str) -> "pd.DataFrame":
        """
        Get company balance sheet.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with balance sheet
        """
        ticker = self._get_ticker(symbol)
        return ticker.balance_sheet

    def get_cashflow(self, symbol: str) -> "pd.DataFrame":
        """
        Get company cash flow.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with cash flow data
        """
        ticker = self._get_ticker(symbol)
        return ticker.cashflow

    def get_earnings(self, symbol: str) -> "pd.DataFrame":
        """
        Get company earnings data.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with earnings data
        """
        ticker = self._get_ticker(symbol)
        return ticker.earnings

    # ==================== Analyst Data ====================

    def get_recommendations(self, symbol: str) -> "pd.DataFrame":
        """
        Get analyst recommendations.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with recommendations (firm, grade, to_date, from_grade, action)
        """
        ticker = self._get_ticker(symbol)
        return ticker.recommendations

    def get_analyst_price_targets(self, symbol: str) -> Dict[str, Any]:
        """
        Get analyst price targets.

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with price target data
        """
        ticker = self._get_ticker(symbol)
        return ticker.analyst_price_targets

    def get_earnings_estimate(self, symbol: str) -> "pd.DataFrame":
        """
        Get earnings estimate data.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with earnings estimates
        """
        ticker = self._get_ticker(symbol)
        return ticker.earnings_estimate

    def get_earnings_dates(self, symbol: str) -> "pd.DataFrame":
        """
        Get upcoming earnings dates.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with earnings dates
        """
        ticker = self._get_ticker(symbol)
        return ticker.earnings_dates

    def get_growth_estimates(self, symbol: str) -> "pd.DataFrame":
        """
        Get growth estimates.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with growth estimates
        """
        ticker = self._get_ticker(symbol)
        return ticker.growth_estimates

    # ==================== Insider & News ====================

    def get_insider_transactions(self, symbol: str) -> "pd.DataFrame":
        """
        Get insider transactions.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with insider transactions
        """
        ticker = self._get_ticker(symbol)
        return ticker.insider_transactions

    def get_insider_purchases(self, symbol: str) -> "pd.DataFrame":
        """
        Get insider purchases.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with insider purchases
        """
        ticker = self._get_ticker(symbol)
        return ticker.insider_purchases

    def get_insider_roster(self, symbol: str) -> "pd.DataFrame":
        """
        Get insider roster.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with insider roster
        """
        ticker = self._get_ticker(symbol)
        return ticker.insider_roster

    def get_news(self, symbol: str) -> List[Dict[str, Any]]:
        """
        Get latest news about the stock.

        Args:
            symbol: Stock symbol

        Returns:
            List of news articles with title, publisher, link, etc.
        """
        ticker = self._get_ticker(symbol)
        return ticker.news

    # ==================== Dividends & Splits ====================

    def get_dividends(self, symbol: str) -> "pd.DataFrame":
        """
        Get dividend history.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with dividend payments
        """
        ticker = self._get_ticker(symbol)
        return ticker.dividends

    def get_splits(self, symbol: str) -> "pd.DataFrame":
        """
        Get stock split history.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with stock splits
        """
        ticker = self._get_ticker(symbol)
        return ticker.splits

    def get_actions(self, symbol: str) -> "pd.DataFrame":
        """
        Get corporate actions (dividends and splits).

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with corporate actions
        """
        ticker = self._get_ticker(symbol)
        return ticker.actions

    # ==================== Sector & Industry ====================

    def get_sector(self, sector_name: str) -> yf.Sector:
        """
        Get sector information.

        Args:
            sector_name: Sector name (e.g., "technology", "healthcare", "financial")

        Returns:
            Sector object with top companies, holdings, etc.
        """
        return yf.Sector(sector_name)

    def get_industry(self, industry_key: str) -> yf.Industry:
        """
        Get industry information.

        Args:
            industry_key: Industry key (e.g., "technology-semiconductors", "consumer-cyclical-autos")

        Returns:
            Industry object with top companies, etc.
        """
        return yf.Industry(industry_key)

    # ==================== Screener ====================

    def get_screener(self, query_name: str) -> "pd.DataFrame":
        """
        Get screener results for predefined queries.

        Args:
            query_name: Screener query name. Available queries:
                - "aggressive_small_caps"
                - "day_gainers"
                - "day_losers"
                - "growth_technology_stocks"
                - "most_actives"
                - "most_shorted_stocks"
                - "small_cap_gainers"
                - "undervalued_growth_stocks"
                - "undervalued_large_caps"
                - "conservative_foreign_funds"

        Returns:
            DataFrame with screener results
        """
        import pandas as pd
        result = yf.screen(query_name)
        if isinstance(result, dict) and "quotes" in result:
            return pd.DataFrame(result["quotes"])
        return pd.DataFrame()

    # ==================== Search ====================

    def search(self, query: str) -> yf.Search:
        """
        Search for stocks.

        Args:
            query: Search query (e.g., "Apple")

        Returns:
            Search object with quotes and news
        """
        return yf.Search(query)

    # ==================== Options ====================

    def get_options(self, symbol: str) -> List[str]:
        """
        Get available option dates.

        Args:
            symbol: Stock symbol

        Returns:
            List of available option dates
        """
        ticker = self._get_ticker(symbol)
        return ticker.options

    def get_option_chain(self, symbol: str, date: str) -> Dict[str, "pd.DataFrame"]:
        """
        Get option chain for a specific date.

        Args:
            symbol: Stock symbol
            date: Option expiration date (YYYY-MM-DD)

        Returns:
            Dictionary with 'calls' and 'puts' DataFrames
        """
        ticker = self._get_ticker(symbol)
        opt = ticker.option_chain(date)
        return {"calls": opt.calls, "puts": opt.puts}

    # ==================== Calendar ====================

    def get_earnings_calendar(self, symbol: str) -> "pd.DataFrame":
        """
        Get earnings calendar.

        Args:
            symbol: Stock symbol

        Returns:
            DataFrame with earnings dates
        """
        ticker = self._get_ticker(symbol)
        return ticker.earnings_dates

    # ==================== Multi-ticker ====================

    def get_multiple_prices(self, symbols: List[str]) -> Dict[str, float]:
        """
        Get current prices for multiple stocks.

        Args:
            symbols: List of stock symbols

        Returns:
            Dictionary mapping symbol to current price
        """
        tickers = yf.Tickers(" ".join(symbols))
        return {
            symbol: getattr(tickers, symbol).info.get("currentPrice")
            for symbol in symbols
        }

    def download(
        self,
        symbols: Union[str, List[str]],
        period: str = "1y",
        interval: str = "1d",
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> "pd.DataFrame":
        """
        Download historical data for multiple symbols.

        Args:
            symbols: Single symbol or list of symbols
            period: Data period
            interval: Data interval
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)

        Returns:
            DataFrame with historical data
        """
        return yf.download(symbols, period=period, interval=interval, start=start, end=end)


# Type hint for pandas DataFrame (imported at runtime to avoid hard dependency)
"pd"  # noqa: F401
