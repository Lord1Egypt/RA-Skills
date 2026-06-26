"""
Data Sources Module

Provides unified interface for fetching stock data from multiple sources:
- Yahoo Finance (US/HK stocks)
- AkShare (A-shares)
- Tushare (A-shares backup)
- efinance (A-shares fallback)
- Alpha Vantage (US stocks fallback)
"""

import os
from .base import DataSourceBase


class YahooFinanceDataSource(DataSourceBase):
    """Yahoo Finance data source for US and HK stocks with Alpha Vantage fallback."""
    
    def __init__(self):
        super().__init__()
        try:
            import yfinance as yf
            self.yf = yf
            
            # Initialize Alpha Vantage as fallback for US stocks
            av_key = os.getenv('ALPHA_VANTAGE_API_KEY')
            if av_key:
                try:
                    from alpha_vantage.timeseries import TimeSeries
                    self.av_ts = TimeSeries(key=av_key, output_format='pandas')
                    self.has_alpha_vantage = True
                except ImportError:
                    self.av_ts = None
                    self.has_alpha_vantage = False
            else:
                self.av_ts = None
                self.has_alpha_vantage = False
        except ImportError:
            raise ImportError("yfinance is required. Install with: pip install yfinance")
    
    def get_quote(self, symbol: str) -> dict:
        """
        Get real-time quote from Yahoo Finance with Alpha Vantage fallback.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL', '0700.HK')
            
        Returns:
            Dictionary with quote data
        """
        # Try Yahoo Finance first
        try:
            ticker = self.yf.Ticker(symbol)
            data = ticker.info
            
            return {
                'symbol': symbol,
                'price': data.get('currentPrice', data.get('regularMarketPrice', data.get('previousClose', 0))),
                'change': data.get('regularMarketChange', 0),
                'change_percent': data.get('regularMarketChangePercent', 0),
                'volume': data.get('volume', 0),
                'market_cap': data.get('marketCap', 0),
                'pe_ratio': data.get('trailingPE', 0),
                'high_52w': data.get('fiftyTwoWeekHigh', 0),
                'low_52w': data.get('fiftyTwoWeekLow', 0),
                'source': 'yahoo',
            }
        except Exception as e:
            self.logger.warning(f"Yahoo Finance failed for {symbol}: {e}")
            
            # Fallback to Alpha Vantage for US stocks (free tier: daily data)
            if self.has_alpha_vantage and self.av_ts and not symbol.endswith('.HK'):
                try:
                    self.logger.info(f"Trying Alpha Vantage for {symbol}...")
                    # Use daily data (free tier)
                    data, _ = self.av_ts.get_daily(symbol, outputsize='compact')
                    if data is not None and len(data) > 0:
                        latest = data.iloc[0]
                        prev_close = data.iloc[1]['4. close'] if len(data) > 1 else latest['4. close']
                        change = latest['4. close'] - prev_close
                        change_pct = (change / prev_close) * 100
                        self.logger.info(f"Alpha Vantage succeeded for {symbol}")
                        return {
                            'symbol': symbol,
                            'price': float(latest['4. close']),
                            'change': float(change),
                            'change_percent': float(change_pct),
                            'volume': float(latest['5. volume']),
                            'market_cap': 0,
                            'pe_ratio': 0,
                            'high_52w': 0,
                            'low_52w': 0,
                            'source': 'alphavantage',
                        }
                except Exception as av_e:
                    self.logger.warning(f"Alpha Vantage failed for {symbol}: {av_e}")
            
            return {'symbol': symbol, 'price': 0, 'error': str(e), 'source': 'yahoo'}
    
    def get_history(self, symbol: str, period: str = '6mo') -> dict:
        """Get historical data."""
        try:
            ticker = self.yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if len(hist) == 0:
                return {}
            
            # Calculate moving averages
            ma5 = hist['Close'].rolling(window=5).mean().iloc[-1]
            ma10 = hist['Close'].rolling(window=10).mean().iloc[-1]
            ma20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            ma60 = hist['Close'].rolling(window=60).mean().iloc[-1]
            
            current_price = hist['Close'].iloc[-1]
            trend = 'bullish' if ma5 > ma10 > ma20 else 'bearish' if ma5 < ma10 < ma20 else 'neutral'
            
            return {
                'ma5': round(ma5, 2),
                'ma10': round(ma10, 2),
                'ma20': round(ma20, 2),
                'ma60': round(ma60, 2),
                'trend': trend,
                'source': 'yahoo',
            }
        except Exception as e:
            self.logger.error(f"Yahoo Finance history error for {symbol}: {e}")
            return {}


class AkShareDataSource(DataSourceBase):
    """AkShare data source for A-shares with efinance fallback."""
    
    def __init__(self):
        super().__init__()
        try:
            import akshare as ak
            self.ak = ak
            # Initialize efinance as fallback
            try:
                import efinance as ef
                self.ef = ef
                self.has_efinance = True
            except ImportError:
                self.ef = None
                self.has_efinance = False
        except ImportError:
            raise ImportError("akshare is required. Install with: pip install akshare")
    
    def get_quote(self, code: str) -> dict:
        """
        Get real-time quote from AkShare with efinance fallback.
        
        Args:
            code: A-share stock code (e.g., '600519', '000001')
            
        Returns:
            Dictionary with quote data
        """
        # Try AkShare first
        try:
            df = self.ak.stock_zh_a_spot_em()
            stock_data = df[df['代码'] == code]
            
            if len(stock_data) > 0:
                stock_data = stock_data.iloc[0]
                return {
                    'symbol': code,
                    'price': float(stock_data['最新价']),
                    'change': float(stock_data['涨跌额']),
                    'change_percent': float(stock_data['涨跌幅']),
                    'volume': float(stock_data['成交量']),
                    'market_cap': float(stock_data['总市值']),
                    'pe_ratio': float(stock_data['市盈率 - 动态']),
                    'source': 'akshare',
                }
        except Exception as e:
            self.logger.warning(f"AkShare failed for {code}: {e}")
        
        # Fallback to efinance
        if self.has_efinance:
            try:
                df = self.ef.stock.get_latest_quote(code)
                if df is not None and len(df) > 0:
                    row = df.iloc[0]
                    return {
                        'symbol': code,
                        'price': float(row['最新价']),
                        'change': float(row['涨跌额']),
                        'change_percent': float(row['涨跌幅']),
                        'volume': float(row['成交量']),
                        'market_cap': float(row['总市值']),
                        'pe_ratio': float(row['动态市盈率']),
                        'source': 'efinance',
                    }
            except Exception as e:
                self.logger.warning(f"efinance failed for {code}: {e}")
        
        return {'symbol': code, 'price': 0, 'error': 'All data sources failed', 'source': 'none'}
    
    def get_history(self, code: str, period: str = '6mo') -> dict:
        """Get historical data from AkShare."""
        # Simplified - return basic technical indicators
        return {
            'ma5': 0,
            'ma10': 0,
            'ma20': 0,
            'ma60': 0,
            'trend': 'neutral',
            'source': 'akshare',
        }


class TushareDataSource(DataSourceBase):
    """Tushare data source for A-shares (backup)."""
    
    def __init__(self, token: str = None):
        super().__init__()
        self.token = token or os.getenv('TUSHARE_TOKEN')
        
        if not self.token:
            self.logger.warning("TUSHARE_TOKEN not configured")
            return
        
        try:
            import tushare as ts
            ts.set_token(self.token)
            self.pro = ts.pro_api()
        except ImportError:
            raise ImportError("tushare is required. Install with: pip install tushare")


class EFinanceDataSource(DataSourceBase):
    """efinance data source for A-shares (fallback)."""
    
    def __init__(self):
        super().__init__()
        try:
            import efinance as ef
            self.ef = ef
        except ImportError:
            raise ImportError("efinance is required. Install with: pip install efinance")


class AlphaVantageDataSource(DataSourceBase):
    """Alpha Vantage data source for US stocks (fallback)."""
    
    def __init__(self, api_key: str = None):
        super().__init__()
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not self.api_key:
            self.logger.warning("ALPHA_VANTAGE_API_KEY not configured")
            return
        
        try:
            from alpha_vantage.timeseries import TimeSeries
            self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        except ImportError:
            raise ImportError("alpha-vantage is required. Install with: pip install alpha-vantage")
    
    def get_quote(self, symbol: str) -> dict:
        """
        Get real-time quote from Alpha Vantage.
        
        Args:
            symbol: US stock symbol (e.g., 'AAPL', 'TSLA')
            
        Returns:
            Dictionary with quote data
        """
        if not self.api_key:
            return {'symbol': symbol, 'price': 0, 'error': 'API key not configured', 'source': 'alphavantage'}
        
        try:
            # Use Time Series for latest data
            data, _ = self.ts.get_intraday(symbol, interval='1min', outputsize='compact')
            
            if data is None or len(data) == 0:
                return {'symbol': symbol, 'price': 0, 'error': 'Stock not found', 'source': 'alphavantage'}
            
            # Get latest timestamp
            latest = data.iloc[0]
            
            return {
                'symbol': symbol,
                'price': float(latest['3. close']),
                'change': 0,  # Need to calculate
                'change_percent': 0,
                'volume': float(latest['5. volume']),
                'market_cap': 0,
                'pe_ratio': 0,
                'source': 'alphavantage',
            }
        except Exception as e:
            self.logger.error(f"Alpha Vantage error for {symbol}: {e}")
            return {'symbol': symbol, 'price': 0, 'error': str(e), 'source': 'alphavantage'}
    
    def get_history(self, symbol: str, period: str = '6mo') -> dict:
        """Get historical data from Alpha Vantage."""
        return {
            'ma5': 0,
            'ma10': 0,
            'ma20': 0,
            'ma60': 0,
            'trend': 'neutral',
            'source': 'alphavantage',
        }
    
    def get_quote(self, code: str) -> dict:
        """
        Get real-time quote from efinance.
        
        Args:
            code: A-share stock code (e.g., '600519', '000001')
            
        Returns:
            Dictionary with quote data
        """
        try:
            # efinance returns DataFrame
            df = self.ef.stock.get_latest_quote(code)
            
            if df is None or len(df) == 0:
                return {'symbol': code, 'price': 0, 'error': 'Stock not found', 'source': 'efinance'}
            
            # Get first row
            row = df.iloc[0]
            
            return {
                'symbol': code,
                'price': float(row['最新价']),
                'change': float(row['涨跌额']),
                'change_percent': float(row['涨跌幅']),
                'volume': float(row['成交量']),
                'market_cap': float(row['总市值']),
                'pe_ratio': float(row['动态市盈率']),
                'source': 'efinance',
            }
        except Exception as e:
            self.logger.error(f"efinance error for {code}: {e}")
            return {'symbol': code, 'price': 0, 'error': str(e), 'source': 'efinance'}
    
    def get_history(self, code: str, period: str = '6mo') -> dict:
        """Get historical data from efinance."""
        return {
            'ma5': 0,
            'ma10': 0,
            'ma20': 0,
            'ma60': 0,
            'trend': 'neutral',
            'source': 'efinance',
        }
    
    def get_quote(self, code: str) -> dict:
        """
        Get real-time quote from Tushare.
        
        Args:
            code: A-share stock code (e.g., '600519', '000001')
            
        Returns:
            Dictionary with quote data
        """
        if not self.token:
            return {'symbol': code, 'price': 0, 'error': 'Tushare token not configured', 'source': 'tushare'}
        
        try:
            # Convert code to Tushare format
            if code.startswith('6'):
                ts_code = f"{code}.SH"
            else:
                ts_code = f"{code}.SZ"
            
            # Get quote
            df = self.pro.quote(ts_code=ts_code)
            
            if len(df) == 0:
                return {'symbol': code, 'price': 0, 'error': 'Stock not found', 'source': 'tushare'}
            
            data = df.iloc[0]
            
            return {
                'symbol': code,
                'price': float(data.get('close', 0)),
                'change': float(data.get('change', 0)),
                'change_percent': float(data.get('pct_chg', 0)),
                'volume': float(data.get('vol', 0)) * 100,  # Convert to shares
                'market_cap': float(data.get('total_mv', 0)) * 10000,  # Convert to yuan
                'pe_ratio': float(data.get('pe', 0)),
                'source': 'tushare',
            }
        except Exception as e:
            self.logger.error(f"Tushare error for {code}: {e}")
            return {'symbol': code, 'price': 0, 'error': str(e), 'source': 'tushare'}
    
    def get_history(self, code: str, period: str = '6mo') -> dict:
        """Get historical data from Tushare."""
        return {
            'ma5': 0,
            'ma10': 0,
            'ma20': 0,
            'ma60': 0,
            'trend': 'neutral',
            'source': 'tushare',
        }
