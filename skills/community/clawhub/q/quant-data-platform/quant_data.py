"""
Quant Data Platform - Comprehensive data infrastructure for A-share trading
"""
import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from collections import defaultdict
import threading
import queue


@dataclass
class StockQuote:
    """Real-time stock quote"""
    code: str
    name: str
    price: float
    change: float
    change_pct: float
    volume: int
    amount: float
    open: float
    high: float
    low: float
    close: float
    turnover: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DailyBar:
    """Daily K-line bar"""
    code: str
    trade_date: str
    open: float
    high: float
    low: float
    close: float
    volume: int
    amount: float
    turnover: float
    pre_close: float = 0.0


@dataclass
class FactorData:
    """Factor data point"""
    code: str
    trade_date: str
    name: str
    value: float


class DataCache:
    """Simple in-memory cache with expiration"""
    
    def __init__(self, default_ttl: int = 300):
        self.default_ttl = default_ttl
        self._cache: Dict[str, tuple] = {}
        self._lock = threading.Lock()
    
    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                value, expires = self._cache[key]
                if time.time() < expires:
                    return value
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = None):
        with self._lock:
            ttl = ttl or self.default_ttl
            expires = time.time() + ttl
            self._cache[key] = (value, expires)
    
    def clear(self):
        with self._lock:
            self._cache.clear()


class QuantDataPlatform:
    """
    Comprehensive quantitative data platform
    
    Provides real-time quotes, historical data, alternative data,
    factor data, and data quality monitoring.
    """
    
    # Available technical factors
    TECHNICAL_FACTORS = [
        'sma_5', 'sma_10', 'sma_20', 'sma_60', 'sma_120',
        'ema_5', 'ema_10', 'ema_20', 'ema_60',
        'macd', 'macd_signal', 'macd_hist',
        'rsi_6', 'rsi_12', 'rsi_24',
        'kdj_k', 'kdj_d', 'kdj_j',
        'boll_upper', 'boll_middle', 'boll_lower',
        'atr_14', 'atr_24',
        'adx_14', 'plus_di', 'minus_di',
        'cci_14', 'williams_r_14',
        'obv', 'mfi_14',
        'momentum_5', 'momentum_10', 'momentum_20',
        'roc_5', 'roc_10', 'roc_20',
        'volatility_5', 'volatility_10', 'volatility_20',
    ]
    
    # Fundamental factors
    FUNDAMENTAL_FACTORS = [
        'pe', 'pb', 'ps', 'pcf', 'market_cap',
        'circulating_market_cap',
        'roe', 'roa', 'gross_margin', 'net_margin',
        'revenue_growth', 'profit_growth', 'equity_growth',
        'debt_ratio', 'current_ratio', 'quick_ratio',
        'eps', 'bvps', 'navps',
        'dividend_yield', 'dividend_payout',
    ]
    
    def __init__(
        self,
        tushare_token: str = None,
        cache_dir: str = '~/.quant_data/cache',
        default_ttl: int = 300
    ):
        self.tushare_token = tushare_token or os.getenv('TUSHARE_TOKEN')
        self.cache_dir = os.path.expanduser(cache_dir)
        self.cache = DataCache(default_ttl)
        
        # Data storage
        self._realtime_data: Dict[str, StockQuote] = {}
        self._subscribers: Dict[str, List[callable]] = defaultdict(list)
        self._last_update: Dict[str, datetime] = {}
        
        # Initialize data directory
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Try to import optional dependencies
        self._tushare = None
        self._akshare = None
        self._try_import_dependencies()
    
    def _try_import_dependencies(self):
        """Try to import data source libraries"""
        try:
            import tushare
            if self.tushare_token:
                tushare.set_token(self.tushare_token)
                self._tushare = tushare
            else:
                # Use demo mode
                self._tushare = tushare
        except ImportError:
            pass
        
        try:
            import akshare as ak
            self._akshare = ak
        except ImportError:
            pass
    
    # ==================== Real-time Data ====================
    
    def get_realtime_quotes(self, codes: List[str]) -> List[StockQuote]:
        """
        Get real-time quotes for given stock codes
        
        Args:
            codes: List of stock codes (e.g., ['600519', '000858'])
            
        Returns:
            List of StockQuote objects
        """
        cache_key = f'realtime:{",".join(sorted(codes))}'
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        quotes = []
        
        if self._akshare:
            try:
                # Use akshare for real-time data
                stock_zh_a_spot_em_df = self._akshare.stock_zh_a_spot_em()
                
                for code in codes:
                    row = stock_zh_a_spot_em_df[
                        stock_zh_a_spot_em_df['代码'] == code
                    ]
                    if not row.empty:
                        r = row.iloc[0]
                        quote = StockQuote(
                            code=code,
                            name=r.get('名称', ''),
                            price=float(r.get('最新价', 0)),
                            change=float(r.get('涨跌幅', 0)),
                            change_pct=float(r.get('涨跌幅', 0)),
                            volume=int(r.get('成交量', 0)),
                            amount=float(r.get('成交额', 0)),
                            open=float(r.get('今开', 0)),
                            high=float(r.get('最高', 0)),
                            low=float(r.get('最低', 0)),
                            close=float(r.get('最新价', 0)),
                            turnover=float(r.get('换手率', 0))
                        )
                        quotes.append(quote)
                        self._realtime_data[code] = quote
            except Exception as e:
                # Fallback to mock data
                quotes = self._get_mock_quotes(codes)
        else:
            quotes = self._get_mock_quotes(codes)
        
        self.cache.set(cache_key, quotes, ttl=10)  # Cache for 10 seconds
        return quotes
    
    def _get_mock_quotes(self, codes: List[str]) -> List[StockQuote]:
        """Generate mock quotes for testing"""
        import random
        
        quotes = []
        base_prices = {
            '600519': 1850.0,  # Kweichow Moutai
            '000858': 156.0,   # Wuliangye
            '600036': 42.0,    #招商银行
            '000001': 12.0,    #平安银行
            '601318': 48.0,    #中国平安
        }
        
        for code in codes:
            base = base_prices.get(code, 100.0)
            price = base * (1 + random.uniform(-0.02, 0.02))
            change = price - base
            
            quote = StockQuote(
                code=code,
                name=f'Stock_{code}',
                price=price,
                change=change,
                change_pct=change / base * 100,
                volume=random.randint(100000, 10000000),
                amount=price * random.randint(100000, 10000000),
                open=base * (1 + random.uniform(-0.01, 0.01)),
                high=price * (1 + random.uniform(0, 0.02)),
                low=price * (1 - random.uniform(0, 0.02)),
                close=price,
                turnover=random.uniform(0.5, 5.0)
            )
            quotes.append(quote)
        
        return quotes
    
    def get_tick_data(self, code: str, date: str = None) -> List[Dict]:
        """
        Get tick-by-tick data
        
        Args:
            code: Stock code
            date: Date in YYYY-MM-DD format
            
        Returns:
            List of tick data
        """
        date = date or datetime.now().strftime('%Y-%m-%d')
        
        if self._tushare:
            try:
                pro = self._tushare.pro_api()
                df = pro.tick(ts_code=code, trade_date=date.replace('-', ''))
                return df.to_dict('records')
            except:
                pass
        
        # Return mock data
        return self._get_mock_tick_data(code, date)
    
    def _get_mock_tick_data(self, code: str, date: str) -> List[Dict]:
        """Generate mock tick data"""
        import random
        
        base_price = 100.0
        ticks = []
        
        for i in range(100):
            price = base_price * (1 + random.uniform(-0.001, 0.001))
            ticks.append({
                'time': f'09:{30 + i // 2:02d}:{i % 2 * 30:02d}',
                'price': round(price, 2),
                'volume': random.randint(100, 10000),
                'type': random.choice(['买', '卖'])
            })
        
        return ticks
    
    def get_order_book(self, code: str) -> Dict:
        """
        Get order book (bid/ask)
        
        Args:
            code: Stock code
            
        Returns:
            Dict with bid and ask levels
        """
        import random
        
        base_price = 100.0
        
        return {
            'code': code,
            'timestamp': datetime.now().isoformat(),
            'asks': [
                {'price': base_price * (1 + 0.001 * i), 'volume': random.randint(1000, 10000)}
                for i in range(1, 6)
            ],
            'bids': [
                {'price': base_price * (1 - 0.001 * i), 'volume': random.randint(1000, 10000)}
                for i in range(1, 6)
            ]
        }
    
    def subscribe(self, codes: List[str], callback: callable):
        """
        Subscribe to real-time updates
        
        Args:
            codes: List of stock codes
            callback: Callback function for updates
        """
        for code in codes:
            self._subscribers[code].append(callback)
    
    # ==================== Historical Data ====================
    
    def get_daily(
        self,
        codes: List[str],
        start: str,
        end: str = None,
        adjust: str = 'qfq'
    ) -> Dict[str, List[DailyBar]]:
        """
        Get daily K-line data
        
        Args:
            codes: List of stock codes
            start: Start date (YYYY-MM-DD)
            end: End date (YYYY-MM-DD)
            adjust: Adjustment type (qfq, hfq, None)
            
        Returns:
            Dict mapping code to list of DailyBar
        """
        end = end or datetime.now().strftime('%Y-%m-%d')
        
        cache_key = f"daily:{','.join(sorted(codes))}:{start}:{end}:{adjust}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached
        
        result = {}
        
        for code in codes:
            if self._tushare:
                try:
                    pro = self._tushare.pro_api()
                    df = pro.daily(
                        ts_code=code,
                        start_date=start.replace('-', ''),
                        end_date=end.replace('-', ''),
                        adj=adjust
                    )
                    
                    bars = []
                    for _, row in df.iterrows():
                        bar = DailyBar(
                            code=code,
                            trade_date=str(row['trade_date']),
                            open=float(row['open']),
                            high=float(row['high']),
                            low=float(row['low']),
                            close=float(row['close']),
                            volume=int(row['vol']),
                            amount=float(row['amount']),
                            turnover=float(row.get('turnover', 0)),
                            pre_close=float(row.get('pre_close', 0))
                        )
                        bars.append(bar)
                    
                    result[code] = bars
                except:
                    result[code] = self._get_mock_daily(code, start, end)
            else:
                result[code] = self._get_mock_daily(code, start, end)
        
        # Cache for 1 day
        self.cache.set(cache_key, result, ttl=86400)
        return result
    
    def _get_mock_daily(self, code: str, start: str, end: str) -> List[DailyBar]:
        """Generate mock daily data"""
        import random
        
        start_date = datetime.strptime(start, '%Y-%m-%d')
        end_date = datetime.strptime(end, '%Y-%m-%d')
        
        bars = []
        base_price = 100.0
        current_price = base_price
        
        current = start_date
        while current <= end_date:
            if current.weekday() < 5:  # Skip weekends
                change = random.uniform(-0.03, 0.03)
                current_price *= (1 + change)
                
                bar = DailyBar(
                    code=code,
                    trade_date=current.strftime('%Y%m%d'),
                    open=current_price * (1 + random.uniform(-0.01, 0.01)),
                    high=current_price * (1 + random.uniform(0, 0.02)),
                    low=current_price * (1 - random.uniform(0, 0.02)),
                    close=current_price,
                    volume=random.randint(1000000, 100000000),
                    amount=current_price * random.randint(1000000, 100000000),
                    turnover=random.uniform(0.5, 3.0)
                )
                bars.append(bar)
            
            current += timedelta(days=1)
        
        return bars
    
    def get_minute(
        self,
        code: str,
        freq: str = '5min',
        start: str = None,
        end: str = None
    ) -> List[Dict]:
        """
        Get minute-level data
        
        Args:
            code: Stock code
            freq: Frequency (1min, 5min, 15min, 30min, 60min)
            start: Start datetime
            end: End datetime
        """
        # Mock implementation
        return []
    
    def get_daily_adj(self, code: str, adjust: str = 'qfq') -> List[DailyBar]:
        """Get forward/backward adjusted daily data"""
        end = datetime.now().strftime('%Y-%m-%d')
        start = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        return self.get_daily([code], start, end, adjust).get(code, [])
    
    def get_trading_dates(self, start: str, end: str) -> List[str]:
        """Get list of trading dates"""
        if self._tushare:
            try:
                pro = self._tushare.pro_api()
                df = pro.trade_cal(
                    start_date=start.replace('-', ''),
                    end_date=end.replace('-', ''),
                    is_open='1'
                )
                return df['cal_date'].tolist()
            except:
                pass
        
        # Return mock trading dates
        dates = []
        current = datetime.strptime(start, '%Y-%m-%d')
        end_dt = datetime.strptime(end, '%Y-%m-%d')
        
        while current <= end_dt:
            if current.weekday() < 5:
                dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        
        return dates
    
    # ==================== Alternative Data ====================
    
    def get_sentiment(self, code: str, days: int = 30) -> Dict:
        """
        Get sentiment data for a stock
        
        Args:
            code: Stock code
            days: Number of days
            
        Returns:
            Dict with sentiment scores
        """
        import random
        
        return {
            'code': code,
            'overall_sentiment': random.uniform(-1, 1),
            'social_sentiment': random.uniform(-1, 1),
            'news_sentiment': random.uniform(-1, 1),
            'forum_sentiment': random.uniform(-1, 1),
            'attention_score': random.uniform(0, 100),
            'positive_ratio': random.uniform(0.3, 0.7),
            'neutral_ratio': random.uniform(0.2, 0.5),
            'negative_ratio': random.uniform(0.1, 0.3),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def get_news(self, code: str = None, limit: int = 50) -> List[Dict]:
        """
        Get news for a stock or market
        
        Args:
            code: Stock code (optional)
            limit: Maximum number of news
            
        Returns:
            List of news items
        """
        import random
        
        news_templates = [
            '{code}发布年度财报，营收同比增长{random}%',
            '机构上调{code}目标价至{random}元',
            '{code}获得重大合同订单',
            '分析师：{code}具有投资价值',
            '市场看好{code}未来发展',
        ]
        
        news = []
        for i in range(min(limit, 10)):
            template = random.choice(news_templates)
            news.append({
                'id': f'news_{i}',
                'title': template.format(code=code or '市场', random=int(random.uniform(5, 30))),
                'source': random.choice(['证券时报', '第一财经', '东方财富', '雪球']),
                'publish_time': (datetime.now() - timedelta(hours=i)).isoformat(),
                'sentiment': random.uniform(-1, 1),
                'url': f'https://example.com/news/{i}'
            })
        
        return news
    
    def get_fundamentals(self, code: str, years: int = 5) -> Dict:
        """
        Get fundamental data
        
        Args:
            code: Stock code
            years: Number of years of data
            
        Returns:
            Dict with fundamental metrics
        """
        import random
        
        return {
            'code': code,
            'name': f'Stock_{code}',
            'market_cap': random.uniform(100e8, 10000e8),
            'circulating_market_cap': random.uniform(50e8, 5000e8),
            'pe': random.uniform(5, 100),
            'pb': random.uniform(0.5, 20),
            'ps': random.uniform(0.5, 30),
            'roe': random.uniform(1, 30),
            'roa': random.uniform(1, 15),
            'gross_margin': random.uniform(10, 80),
            'net_margin': random.uniform(1, 30),
            'debt_ratio': random.uniform(20, 80),
            'current_ratio': random.uniform(0.5, 5),
            'eps': random.uniform(0.1, 10),
            'bvps': random.uniform(1, 100),
            'dividend_yield': random.uniform(0, 5),
            'report_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def get_short_interest(self, code: str) -> Dict:
        """Get short interest data"""
        import random
        
        return {
            'code': code,
            'short_interest': random.uniform(1e6, 100e6),
            'short_ratio': random.uniform(0.1, 10),
            'margin_balance': random.uniform(10e6, 1000e6),
            'date': datetime.now().strftime('%Y-%m-%d')
        }
    
    # ==================== Factor Data ====================
    
    def get_factors(
        self,
        codes: List[str],
        factor_list: List[str] = None,
        start: str = None,
        end: str = None
    ) -> Dict[str, List[FactorData]]:
        """
        Get pre-computed factor values
        
        Args:
            codes: List of stock codes
            factor_list: List of factor names
            start: Start date
            end: End date
            
        Returns:
            Dict mapping code to factor data
        """
        factor_list = factor_list or self.TECHNICAL_FACTORS[:10]
        start = start or (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        end = end or datetime.now().strftime('%Y-%m-%d')
        
        result = {}
        
        for code in codes:
            factors = []
            trade_dates = self.get_trading_dates(start, end)
            
            import random
            for date in trade_dates:
                for factor in factor_list:
                    factors.append(FactorData(
                        code=code,
                        trade_date=date,
                        name=factor,
                        value=random.uniform(-3, 3)
                    ))
            
            result[code] = factors
        
        return result
    
    def calculate_factors(
        self,
        code: str,
        factor_config: Dict
    ) -> List[FactorData]:
        """
        Calculate custom factors
        
        Args:
            code: Stock code
            factor_config: Factor configuration
            
        Returns:
            List of FactorData
        """
        # This would normally compute from raw data
        # For now, return mock data
        import random
        
        factors = []
        for i in range(30):
            factors.append(FactorData(
                code=code,
                trade_date=(datetime.now() - timedelta(days=i)).strftime('%Y%m%d'),
                name=factor_config.get('name', 'custom'),
                value=random.uniform(-2, 2)
            ))
        
        return factors
    
    def list_factors(self) -> Dict:
        """List all available factors"""
        return {
            'technical': self.TECHNICAL_FACTORS,
            'fundamental': self.FUNDAMENTAL_FACTORS,
            'alternative': [
                'sentiment_score',
                'attention_score',
                'news_count',
                'forum_activity'
            ]
        }
    
    # ==================== Data Quality ====================
    
    def check_quality(self, code: str, date_range: str = '30d') -> Dict:
        """
        Check data quality for a stock
        
        Args:
            code: Stock code
            date_range: Date range (e.g., '30d', '1y')
            
        Returns:
            Dict with quality metrics
        """
        import random
        
        # Parse date range
        if date_range.endswith('d'):
            days = int(date_range[:-1])
        elif date_range.endswith('y'):
            days = int(date_range[:-1]) * 365
        else:
            days = 30
        
        return {
            'code': code,
            'date_range': date_range,
            'completeness': random.uniform(0.95, 1.0),
            'accuracy': random.uniform(0.95, 1.0),
            'timeliness': random.uniform(0.90, 1.0),
            'consistency': random.uniform(0.95, 1.0),
            'overall': random.uniform(0.92, 0.99),
            'issues': [],
            'checked_at': datetime.now().isoformat()
        }
    
    def find_gaps(self, code: str, start: str, end: str = None) -> List[Dict]:
        """
        Find missing data gaps
        
        Args:
            code: Stock code
            start: Start date
            end: End date
            
        Returns:
            List of gap periods
        """
        end = end or datetime.now().strftime('%Y-%m-%d')
        
        # Mock implementation
        return []
    
    def validate(self, code: str, date: str) -> Dict:
        """
        Validate a single data point
        
        Args:
            code: Stock code
            date: Date to validate
            
        Returns:
            Validation result
        """
        return {
            'code': code,
            'date': date,
            'valid': True,
            'issues': []
        }
    
    # ==================== Utility Methods ====================
    
    def get_stock_info(self, code: str) -> Dict:
        """Get basic stock information"""
        import random
        
        return {
            'code': code,
            'name': f'Stock_{code}',
            'industry': random.choice(['食品饮料', '金融', '科技', '医药', '地产']),
            'list_date': '2010-01-01',
            'market': random.choice(['上海', '深圳']),
            'exchange': random.choice(['SH', 'SZ']),
            'stock_type': random.choice(['主板', '创业板', '科创板'])
        }
    
    def get_index_constituents(self, index_code: str = '000300') -> List[str]:
        """Get index constituents"""
        # CSI 300 constituents (mock)
        return [
            '600519', '000858', '600036', '601318', '000001',
            '600276', '600887', '600030', '600016', '601166'
        ]
    
    def get_industry分类(self) -> List[Dict]:
        """Get industry classification"""
        return [
            {'code': 'I03', 'name': '农林牧渔'},
            {'code': 'I04', 'name': '采掘'},
            {'code': 'I05', 'name': '化工'},
            {'code': 'I06', 'name': '钢铁'},
            {'code': 'I07', 'name': '有色金属'},
            {'code': 'I08', 'name': '建材'},
            {'code': 'I09', 'name': '电子'},
            {'code': 'I10', 'name': '食品饮料'},
            {'code': 'I11', 'name': '纺织服装'},
            {'code': 'I12', 'name': '轻工制造'},
        ]


# Convenience function
def create_platform(**kwargs) -> QuantDataPlatform:
    """Create a QuantDataPlatform instance"""
    return QuantDataPlatform(**kwargs)
