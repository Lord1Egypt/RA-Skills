#!/usr/bin/env python3
"""
Stock Valuation Monitor Skill V2.5.1
股票和ETF估值监控工具 - 修复优化版

优化内容：
1. 熔断器性能优化（使用 deque 滑动窗口）
2. 增加 PE/PB 负值警告
3. 缓存键设计注释
4. 超时参数调整（保证数据获取时间）
5. Excel 导出空数据保护
6. 代码健壮性增强

Features:
- A股PE/PB Band估值分析（基于乐咕乐股/东方财富数据）
- ETF净值折溢价+技术分析
- 多数据源容错（东方财富/腾讯/新浪/AkShare）
- 实时行情+历史百分位
- 智能投资建议
- 数据导出支持（JSON/CSV/Excel）

Author: AI Assistant
License: MIT
Version: 4.5.1
"""

import json
import re
import requests
import pandas as pd
import numpy as np
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Callable, Union
from functools import wraps
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FutureTimeoutError
import threading
from dataclasses import dataclass, field, asdict
from enum import Enum
import io
import warnings
from collections import deque

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 尝试导入akshare
try:
    import akshare as ak
    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    logger.warning("akshare未安装，历史数据功能受限")
    ak = None

# 尝试导入导出功能
try:
    import openpyxl
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False

# 忽略pandas警告
warnings.filterwarnings('ignore', category=FutureWarning)


# ==================== 常量定义（集中管理） ====================

class AssetType(Enum):
    """资产类型"""
    STOCK = "stock"
    ETF = "etf"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Constants:
    """系统常量（不可变）"""
    # 股票代码前缀
    STOCK_PREFIXES: Tuple[str, ...] = ('60', '68', '30', '00', '43', '83', '87', '688', '689')
    ETF_PREFIXES: Tuple[str, ...] = ('51', '15', '16', '18', '58', '56', '58', '50')
    VALID_PREFIXES: Tuple[str, ...] = STOCK_PREFIXES + ETF_PREFIXES

    # 数据源字段（东方财富）
    EM_FIELDS = "f43,f44,f45,f46,f57,f58,f59,f60,f61,f92,f116,f162,f163,f170,f167,f234,f235,f236,f277"
    # f43:现价(分), f58:名称, f92:PB, f116:市值(元), f162:动态PE/100, f163:静态PE/100, f167:ROE/100
    # f234:振幅, f235:均价/净值, f236:量比, f277:涨速/折溢价
    # ETF特有字段
    ETF_NAV_FIELD = "f239"          # ETF净值（某些接口用f239，备用f235）
    ETF_PREMIUM_FIELD = "f237"      # ETF折溢价率

    # 阈值
    OPP_THRESHOLD: float = 30.0  # 机会区间
    RISK_THRESHOLD: float = 70.0  # 风险区间
    MAX_PE: float = 500.0
    MAX_PB: float = 50.0
    MIN_HISTORY_DAYS: int = 60
    HISTORY_YEARS: int = 5

    # 系统配置
    CACHE_TTL: int = 300  # 5分钟
    TIMEOUT: int = 10
    MAX_RETRIES: int = 3
    MAX_WORKERS: int = 3
    CIRCUIT_THRESHOLD: int = 5
    CIRCUIT_TIMEOUT: int = 300  # 5分钟熔断恢复期
    CIRCUIT_WINDOW: int = 600   # 10分钟错误窗口

    # 市值转换
    MARKET_CAP_DIV: float = 1e8

    # 财务数据列名（统一配置避免重复）
    EPS_KEYWORDS: Tuple[str, ...] = ('基本每股收益', '每股收益', 'EPS', 'BASIC_EPS', 'BASICEPS', 'EPS')
    BVPS_KEYWORDS: Tuple[str, ...] = ('每股净资产', 'BVPS', 'BPS', '每股账面价值', 'BOOK_VALUE_PER_SHARE')
    DATE_KEYWORDS: Tuple[str, ...] = ('报告期', '日期', 'DATE', 'REPORT_DATE', 'END_DATE', '季度', '报告日期')


# ==================== 工具函数 ====================

def safe_float(value: Any, default: Optional[float] = None, allow_negative: bool = True) -> Optional[float]:
    """安全转换为浮点数（增强版）

    Args:
        value: 输入值
        default: 默认值
        allow_negative: 是否允许负数（对于某些指标如PE/PB不应为负）
    """
    if value is None:
        return default

    # 处理字符串
    if isinstance(value, str):
        v = value.strip()
        if v.lower() in ('none', 'null', 'nan', '--', '-', '', 'null'):
            return default
        # 移除常见单位符号
        v = v.replace('%', '').replace(',', '').replace('元', '').replace('亿', '').replace('万', '')
        try:
            value = float(v)
        except ValueError:
            # 尝试正则提取
            match = re.search(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?', v)
            if match:
                try:
                    value = float(match.group())
                except ValueError:
                    return default
            else:
                return default

    # 处理数字类型
    if isinstance(value, (int, float, np.number)):
        try:
            val = float(value)
            # 检查NaN和Inf
            if np.isnan(val) or np.isinf(val):
                return default
            # 检查负数
            if not allow_negative and val < 0:
                return default
            return val
        except (ValueError, TypeError, OverflowError):
            return default

    return default


def validate_timestamp(ts: str, fmt: str = '%Y%m%d%H%M') -> bool:
    """验证时间戳格式"""
    try:
        datetime.strptime(ts, fmt)
        return True
    except ValueError:
        return False


def get_asset_type(code: str) -> AssetType:
    """判断资产类型"""
    if not code or len(code) != 6:
        return AssetType.UNKNOWN
    # ETF前缀检查（更精确）
    if code.startswith(('51', '15', '16', '18', '56', '58', '50')):
        return AssetType.ETF
    # 股票前缀检查
    if code.startswith(('60', '68', '30', '00', '43', '83', '87', '688', '689')):
        return AssetType.STOCK
    return AssetType.UNKNOWN


def validate_code(code: str) -> Tuple[bool, str, AssetType]:
    """验证代码有效性（增强版）"""
    if not code or not isinstance(code, str):
        return False, "代码不能为空", AssetType.UNKNOWN
    if not re.match(r'^[0-9]{6}$', code):
        return False, "代码必须是6位数字", AssetType.UNKNOWN

    asset_type = get_asset_type(code)
    if asset_type == AssetType.UNKNOWN:
        return False, f"代码前缀无效: {code[:2]}（不支持新三板/北交所等）", AssetType.UNKNOWN

    return True, "", asset_type


def retry_on_failure(max_retries: int = Constants.MAX_RETRIES,
                     exceptions: Tuple = (Exception,),
                     delay_base: float = 1.0):
    """重试装饰器（增强版，支持指数退避）"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    if attempt < max_retries - 1:
                        # 指数退避 + 随机抖动
                        delay = min(delay_base * (2 ** attempt), 30) + np.random.uniform(0, 0.5)
                        logger.debug(f"{func.__name__} 第{attempt+1}次失败，{delay:.2f}s后重试: {e}")
                        time.sleep(delay)
            logger.error(f"{func.__name__} 失败 {max_retries} 次: {last_exc}")
            raise last_exc
        return wrapper
    return decorator


# ==================== 缓存系统 ====================

class ThreadSafeCache:
    """线程安全缓存（优化版：支持细粒度过期）"""

    def __init__(self, ttl: int = Constants.CACHE_TTL):
        self.ttl = ttl
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._lock = threading.RLock()
        self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            if key in self._cache:
                value, ts = self._cache[key]
                if time.time() - ts < self.ttl:
                    self._stats['hits'] += 1
                    return value
                # 过期，删除
                del self._cache[key]
                self._stats['evictions'] += 1
            self._stats['misses'] += 1
            return None

    def set(self, key: str, value: Any):
        with self._lock:
            # 简单的LRU：如果缓存过大，清除最旧的10%
            if len(self._cache) > 1000:
                sorted_items = sorted(self._cache.items(), key=lambda x: x[1][1])
                for old_key, _ in sorted_items[:100]:
                    del self._cache[old_key]
                    self._stats['evictions'] += 1
            self._cache[key] = (value, time.time())

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._stats = {'hits': 0, 'misses': 0, 'evictions': 0}

    def stats(self) -> Dict:
        with self._lock:
            total = self._stats['hits'] + self._stats['misses']
            return {
                'size': len(self._cache),
                'hit_rate': self._stats['hits'] / total if total > 0 else 0,
                **self._stats
            }


# ==================== 数据模型 ====================

@dataclass
class StockBasicInfo:
    """基础信息"""
    code: str
    name: str
    asset_type: AssetType = AssetType.STOCK
    price: Optional[float] = None
    pre_close: Optional[float] = None
    change_pct: Optional[float] = None
    pe_dynamic: Optional[float] = None  # 动态PE
    pe_ttm: Optional[float] = None      # TTM PE
    pb: Optional[float] = None
    roe: Optional[float] = None
    market_cap: Optional[float] = None  # 亿元
    nav: Optional[float] = None         # ETF净值（元）
    premium_rate: Optional[float] = None # 折溢价率（%）
    volume: Optional[float] = None       # 成交量（手）
    turnover: Optional[float] = None     # 成交额（元）
    update_time: Optional[str] = None    # 数据更新时间

    @property
    def is_valid(self) -> bool:
        return self.price is not None and self.price > 0 and self.name is not None


@dataclass
class ValuationMetrics:
    """估值指标"""
    current: float
    percentile: float
    min: float
    max: float
    median: float
    band_20: float
    band_50: float
    band_80: float
    points: int
    warning: Optional[str] = None
    calculation_method: str = "unknown"  # 新增：计算方法说明

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class ValuationResult:
    """估值结果"""
    code: str
    success: bool
    asset_type: AssetType = AssetType.STOCK
    message: str = ""
    basic_info: Optional[StockBasicInfo] = None
    pe: Optional[ValuationMetrics] = None
    pb: Optional[ValuationMetrics] = None
    roe: Optional[Dict] = None
    etf: Optional[Dict] = None
    zone: str = "未知"
    suggestion: str = ""
    data_sources: List[str] = field(default_factory=list)  # 新增：使用的数据源
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict:
        """转换为字典（用于JSON导出）"""
        result = {
            'code': self.code,
            'success': self.success,
            'asset_type': self.asset_type.value,
            'message': self.message,
            'zone': self.zone,
            'suggestion': self.suggestion,
            'data_sources': self.data_sources,
            'timestamp': self.timestamp
        }
        if self.basic_info:
            result['basic'] = {
                'name': self.basic_info.name,
                'price': self.basic_info.price,
                'pre_close': self.basic_info.pre_close,
                'change_pct': self.basic_info.change_pct,
                'market_cap': self.basic_info.market_cap,
                'update_time': self.basic_info.update_time
            }
        if self.pe:
            result['pe'] = self.pe.to_dict()
        if self.pb:
            result['pb'] = self.pb.to_dict()
        if self.roe:
            result['roe'] = self.roe
        if self.etf:
            result['etf'] = self.etf
        return result


# ==================== 数据源基类 ====================

class DataSource:
    """数据源基类（优化版熔断器：滑动窗口 + deque）"""

    def __init__(self, name: str, priority: int):
        self.name = name
        self.priority = priority
        self._enabled = True
        # 使用 deque 维护错误时间窗口，自动保持 maxlen 但需手动清理过期
        self._error_times = deque()
        self._last_error: Optional[float] = None
        self._lock = threading.Lock()
        self._success_count = 0
        self._error_count = 0

    @property
    def enabled(self) -> bool:
        with self._lock:
            if not self._enabled:
                if self._last_error and time.time() - self._last_error > Constants.CIRCUIT_TIMEOUT:
                    logger.info(f"{self.name} 熔断恢复")
                    self._enabled = True
                    self._error_times.clear()
                    self._last_error = None
                    return True
                return False
            # 清理窗口外过期错误
            now = time.time()
            cutoff = now - Constants.CIRCUIT_WINDOW
            while self._error_times and self._error_times[0] < cutoff:
                self._error_times.popleft()
            return len(self._error_times) < Constants.CIRCUIT_THRESHOLD

    def record_error(self):
        with self._lock:
            now = time.time()
            self._error_times.append(now)
            self._error_count += 1
            self._last_error = now
            # 清理窗口外过期错误
            cutoff = now - Constants.CIRCUIT_WINDOW
            while self._error_times and self._error_times[0] < cutoff:
                self._error_times.popleft()
            if len(self._error_times) >= Constants.CIRCUIT_THRESHOLD:
                self._enabled = False
                logger.warning(f"{self.name} 熔断触发（10分钟内{len(self._error_times)}次错误）")

    def record_success(self):
        with self._lock:
            self._success_count += 1
            # 连续成功3次，清除一半错误记录（渐进恢复）
            if self._success_count % 3 == 0 and self._error_times:
                # 移除最早的 len//2 个错误记录
                for _ in range(len(self._error_times) // 2):
                    self._error_times.popleft()

    def get_stats(self) -> Dict:
        with self._lock:
            total = self._success_count + self._error_count
            return {
                'name': self.name,
                'enabled': self._enabled,
                'error_rate': self._error_count / total if total > 0 else 0,
                'success_count': self._success_count,
                'error_count': self._error_count,
                'recent_errors': len(self._error_times)
            }

    def fetch(self, code: str, asset_type: AssetType) -> Optional[StockBasicInfo]:
        raise NotImplementedError


# ==================== 具体数据源 ====================

class EastMoneyDataSource(DataSource):
    """东方财富数据源（修复：ETF净值解析，增加字段验证）"""

    def __init__(self):
        super().__init__("EastMoney", 1)
        self.base_url = "https://push2.eastmoney.com/api/qt/stock/get"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://quote.eastmoney.com/",
            "Accept": "application/json"
        }

    @staticmethod
    def _parse(data: Dict, field: str, divisor: float = 1, default: Any = None) -> Any:
        """解析字段值"""
        val = data.get(field)
        if val is not None and val != '' and val != '-' and str(val).lower() != 'null':
            if divisor == 1 and isinstance(val, (int, float)):
                return val
            parsed = safe_float(val)
            if parsed is not None:
                result = parsed / divisor if divisor != 1 else parsed
                return result if np.isfinite(result) else default
        return default

    @retry_on_failure(max_retries=3, exceptions=(requests.RequestException, json.JSONDecodeError))
    def fetch(self, code: str, asset_type: AssetType) -> Optional[StockBasicInfo]:
        try:
            secid = f"1.{code}" if code.startswith(('6', '5', '688', '689')) else f"0.{code}"

            resp = requests.get(
                self.base_url,
                params={"secid": secid, "fields": Constants.EM_FIELDS},
                headers=self.headers,
                timeout=Constants.TIMEOUT
            )
            resp.raise_for_status()
            data = resp.json()

            if not data.get('data'):
                logger.warning(f"EastMoney {code}: 返回空数据")
                return None

            d = data['data']

            # 基础价格数据（东方财富价格字段通常需要除以100）
            price = self._parse(d, 'f43', 100)
            pre_close = self._parse(d, 'f60', 100)

            if not price or price <= 0:
                logger.warning(f"EastMoney {code}: 无效价格 {price}")
                return None

            # 涨跌幅（f170通常已包含%符号处理，但这里需要除以100转换为小数）
            change_pct = self._parse(d, 'f170', 100)
            if change_pct is None and pre_close and pre_close > 0:
                change_pct = round((price - pre_close) / pre_close * 100, 2)

            # PE/PB/ROE处理（f162,f163通常需要除以100得到实际PE值）
            pe_d = self._parse(d, 'f162', 100)
            pe_ttm = self._parse(d, 'f163', 100)
            pb = self._parse(d, 'f92', 1)          # PB通常不需要除数
            roe = self._parse(d, 'f167', 100)     # ROE百分比转换为小数

            # 验证PE/PB合理性
            if pe_d is not None and (pe_d < 0 or pe_d > Constants.MAX_PE):
                pe_d = None
            if pe_ttm is not None and (pe_ttm < 0 or pe_ttm > Constants.MAX_PE):
                pe_ttm = None
            if pb is not None and (pb < 0 or pb > Constants.MAX_PB):
                pb = None

            # 市值处理（元转亿元）
            mc = self._parse(d, 'f116', 1)
            if mc:
                mc = mc / Constants.MARKET_CAP_DIV

            # ETF特有数据
            nav = None
            premium = None
            if asset_type == AssetType.ETF:
                # 尝试多个可能的净值字段
                nav = self._parse(d, 'f239', 1) or self._parse(d, 'f235', 100) or self._parse(d, 'f22', 100)
                premium = self._parse(d, 'f237', 100) or self._parse(d, 'f277', 100)

                # 如果 NAV 无效但 price 有效，尝试用 price 作为 NAV（LOF情况）
                if nav is None or nav <= 0:
                    # LOF可能净值字段不同，暂时用price作为参考
                    pass

            # 成交量/额
            volume = self._parse(d, 'f47', 1)  # 手
            turnover = self._parse(d, 'f48', 1)  # 元

            self.record_success()

            return StockBasicInfo(
                code=code,
                name=str(d.get('f58', '')).strip(),
                asset_type=asset_type,
                price=round(price, 2),
                pre_close=round(pre_close, 2) if pre_close else None,
                change_pct=change_pct,
                pe_dynamic=pe_d,
                pe_ttm=pe_ttm,
                pb=pb,
                roe=roe,
                market_cap=round(mc, 2) if mc else None,
                nav=round(nav, 4) if nav else None,
                premium_rate=premium,
                volume=volume,
                turnover=turnover,
                update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

        except Exception as e:
            self.record_error()
            logger.error(f"EastMoney {code} 失败: {e}")
            return None


class TencentDataSource(DataSource):
    """腾讯财经数据源"""

    def __init__(self):
        super().__init__("Tencent", 2)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    @retry_on_failure(max_retries=3, exceptions=(requests.RequestException,))
    def fetch(self, code: str, asset_type: AssetType) -> Optional[StockBasicInfo]:
        try:
            symbol = f"sh{code}" if code.startswith(('6', '5', '688', '689')) else f"sz{code}"

            resp = requests.get(
                f"https://qt.gtimg.cn/q={symbol}",
                headers=self.headers,
                timeout=Constants.TIMEOUT
            )

            # 编码自适应
            for enc in ['gb2312', 'gbk', 'utf-8']:
                try:
                    resp.encoding = enc
                    content = resp.text
                    break
                except:
                    continue

            if '"' not in content:
                return None

            parts = content.split('"')[1].split('~')
            if len(parts) < 45:
                return None

            pre_close = safe_float(parts[4])
            price = safe_float(parts[3])

            if not price or price <= 0:
                return None

            change_pct = safe_float(parts[32])
            if change_pct is None and pre_close and pre_close > 0:
                change_pct = round((price - pre_close) / pre_close * 100, 2)

            # 市值转换（万元->亿元）
            mc = safe_float(parts[44])
            if mc:
                mc = mc / 10000

            # PE/PB合理性检查
            pe = safe_float(parts[39])
            if pe and (pe < 0 or pe > Constants.MAX_PE):
                pe = None
            pb = safe_float(parts[46])
            if pb and (pb < 0 or pb > Constants.MAX_PB):
                pb = None

            self.record_success()

            return StockBasicInfo(
                code=code,
                name=parts[1],
                asset_type=asset_type,
                price=price,
                pre_close=pre_close,
                change_pct=change_pct,
                pe_dynamic=pe,
                pb=pb,
                market_cap=mc,
                update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

        except Exception as e:
            self.record_error()
            logger.error(f"Tencent {code} 失败: {e}")
            return None


class SinaDataSource(DataSource):
    """新浪财经数据源"""

    def __init__(self):
        super().__init__("Sina", 3)
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    @retry_on_failure(max_retries=2, exceptions=(requests.RequestException,))
    def fetch(self, code: str, asset_type: AssetType) -> Optional[StockBasicInfo]:
        try:
            symbol = f"sh{code}" if code.startswith(('6', '5', '688', '689')) else f"sz{code}"

            resp = requests.get(
                f"https://hq.sinajs.cn/list={symbol}",
                headers=self.headers,
                timeout=Constants.TIMEOUT
            )

            for enc in ['gb2312', 'gbk', 'utf-8']:
                try:
                    resp.encoding = enc
                    data = resp.text
                    break
                except:
                    continue

            if '=' in data and '"' in data:
                content = data.split('"')[1]
                if content:
                    parts = content.split(',')
                    if len(parts) >= 33:
                        pre_close = safe_float(parts[2])
                        price = safe_float(parts[3])

                        if not price or price <= 0:
                            return None

                        change_pct = round((price - pre_close) / pre_close * 100, 2) if pre_close and pre_close > 0 else None

                        self.record_success()

                        return StockBasicInfo(
                            code=code,
                            name=parts[0],
                            asset_type=asset_type,
                            price=price,
                            pre_close=pre_close,
                            change_pct=change_pct,
                            update_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        )
            return None

        except Exception as e:
            self.record_error()
            logger.error(f"Sina {code} 失败: {e}")
            return None


class AkShareDataSource(DataSource):
    """AkShare数据源（优化版：使用stock_a_lg_indicator获取历史PE/PB）"""

    def __init__(self):
        super().__init__("AkShare", 4)
        self.available = AKSHARE_AVAILABLE

    @property
    def enabled(self) -> bool:
        return self.available and super().enabled

    def fetch_history(self, code: str) -> Optional[pd.DataFrame]:
        """获取历史价格（备用）"""
        if not self.available or ak is None:
            return None

        try:
            end = datetime.now().strftime('%Y%m%d')
            start = (datetime.now() - pd.DateOffset(years=Constants.HISTORY_YEARS)).strftime('%Y%m%d')

            df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=start, end_date=end, adjust="qfq")

            if df is not None and not df.empty:
                df = df.dropna(subset=['收盘'])
                if len(df) >= Constants.MIN_HISTORY_DAYS:
                    self.record_success()
                    return df
            return None

        except Exception as e:
            logger.debug(f"AkShare历史 {code} 失败: {e}")
            return None

    def fetch_valuation_history(self, code: str) -> Optional[pd.DataFrame]:
        """获取历史估值数据（PE/PB序列）- 使用stock_a_lg_indicator"""
        if not self.available or ak is None:
            return None

        if get_asset_type(code) == AssetType.ETF:
            return None

        try:
            # 使用乐咕乐股接口获取历史PE/PB
            df = ak.stock_a_lg_indicator(stock=code)

            if df is not None and not df.empty:
                # 确保列名正确
                df = df.rename(columns={
                    'trade_date': '日期',
                    'pe': 'pe',
                    'pe_ttm': 'pe_ttm', 
                    'pb': 'pb',
                    'dv_ratio': '股息率',
                    'total_mv': '总市值'
                })
                # 数据清洗
                df = df.dropna(subset=['pe', 'pb'], how='all')
                if len(df) >= Constants.MIN_HISTORY_DAYS:
                    self.record_success()
                    return df
            return None

        except Exception as e:
            logger.debug(f"AkShare估值历史 {code} 失败: {e}")

        # 备用方案：使用stock_a_indicator（新接口名称）
        try:
            df = ak.stock_a_indicator_lg(symbol=code)
            if df is not None and not df.empty:
                df = df.rename(columns={
                    'trade_date': '日期',
                    'pe': 'pe',
                    'pe_ttm': 'pe_ttm',
                    'pb': 'pb'
                })
                df = df.dropna(subset=['pe', 'pb'], how='all')
                if len(df) >= Constants.MIN_HISTORY_DAYS:
                    self.record_success()
                    return df
        except Exception as e2:
            logger.debug(f"AkShare备用接口 {code} 失败: {e2}")

        return None

    def fetch_financial(self, code: str) -> Optional[pd.DataFrame]:
        """获取财务数据（优化：ETF跳过，主备接口都尝试）"""
        if not self.available or ak is None:
            return None
        if get_asset_type(code) == AssetType.ETF:
            return None

        # 主接口：财务分析指标
        try:
            df = ak.stock_financial_analysis_indicator(symbol=code)
            if df is not None and not df.empty:
                self.record_success()
                return df
        except Exception as e:
            logger.debug(f"主财务接口失败: {e}")

        # 备用接口：新浪财报
        try:
            df = ak.stock_financial_report_sina(stock=code)
            if df is not None and not df.empty:
                self.record_success()
                return df
        except Exception as e:
            logger.debug(f"备用财务接口失败: {e}")

        self.record_error()
        return None


# ==================== 数据管理器 ====================

class DataManager:
    """数据管理器（优化版：支持健康检查）"""

    def __init__(self):
        self.cache = ThreadSafeCache()
        self.sources = [EastMoneyDataSource(), TencentDataSource(), SinaDataSource()]
        self.akshare = AkShareDataSource()
        self._executor = ThreadPoolExecutor(max_workers=Constants.MAX_WORKERS, thread_name_prefix="stock_fetch")
        self._shutdown = False

    def _cache_key(self, prefix: str, code: str) -> str:
        """生成10分钟级缓存键（如2025031113_2表示13:20-13:29），与TTL=5分钟配合，
        确保缓存最多存活10分钟，同时避免每秒变化带来的频繁重建。"""
        ts = datetime.now().strftime('%Y%m%d%H') + str(datetime.now().minute // 10)
        return f"{prefix}:{code}:{ts}"

    def get_realtime(self, code: str, asset_type: AssetType) -> Tuple[Optional[StockBasicInfo], List[str]]:
        """获取实时数据（返回数据和使用的数据源列表）"""
        key = self._cache_key("rt", code)
        cached = self.cache.get(key)
        if cached:
            return cached, ['cache']

        sources_used = []
        for src in sorted([s for s in self.sources if s.enabled], key=lambda x: x.priority):
            if self._shutdown:
                break
            try:
                data = src.fetch(code, asset_type)
                if data and data.is_valid:
                    self.cache.set(key, data)
                    sources_used.append(src.name)
                    return data, sources_used
                sources_used.append(f"{src.name}(fail)")
            except Exception as e:
                logger.debug(f"{src.name} 失败: {e}")
                sources_used.append(f"{src.name}(error)")

        return None, sources_used

    def get_batch(self, codes: List[Tuple[str, AssetType]], timeout: int = 30) -> Dict[str, Tuple[Optional[StockBasicInfo], List[str]]]:
        """批量获取（带超时控制）"""
        results = {}

        def fetch_one(c: str, at: AssetType):
            return c, self.get_realtime(c, at)

        futures = {self._executor.submit(fetch_one, c, at): c for c, at in codes}

        try:
            for future in as_completed(futures, timeout=timeout):
                code = futures[future]
                try:
                    c, (data, sources) = future.result()
                    results[c] = (data, sources)
                except Exception as e:
                    logger.debug(f"获取 {code} 结果异常: {e}")
                    results[code] = (None, ['error'])
        except FutureTimeoutError:
            logger.warning("批量获取超时，取消未完成任务")
            for future in futures:
                future.cancel()

        # 确保所有code都有结果
        for c, at in codes:
            if c not in results:
                results[c] = (None, ['timeout'])

        return results

    def get_history(self, code: str) -> Optional[pd.DataFrame]:
        """获取历史价格数据"""
        key = self._cache_key("hist", code)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        if self.akshare.enabled:
            df = self.akshare.fetch_history(code)
            if df is not None:
                self.cache.set(key, df)
                return df
        return None

    def get_valuation_history(self, code: str) -> Optional[pd.DataFrame]:
        """获取历史估值数据（PE/PB序列）"""
        key = self._cache_key("val", code)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        if self.akshare.enabled:
            df = self.akshare.fetch_valuation_history(code)
            if df is not None:
                self.cache.set(key, df)
                return df
        return None

    def get_financial(self, code: str) -> Optional[pd.DataFrame]:
        """获取财务数据"""
        if get_asset_type(code) == AssetType.ETF:
            return None

        key = self._cache_key("fin", code)
        cached = self.cache.get(key)
        if cached is not None:
            return cached

        if self.akshare.enabled:
            df = self.akshare.fetch_financial(code)
            if df is not None:
                self.cache.set(key, df)
                return df
        return None

    def health_check(self) -> Dict:
        """系统健康检查"""
        return {
            'cache': self.cache.stats(),
            'sources': [s.get_stats() for s in self.sources + [self.akshare]],
            'akshare_available': AKSHARE_AVAILABLE,
            'excel_available': EXCEL_AVAILABLE
        }

    def shutdown(self):
        """优雅关闭"""
        self._shutdown = True
        self._executor.shutdown(wait=True, cancel_futures=True)
        logger.info("DataManager已关闭")

    def __del__(self):
        if not self._shutdown:
            self.shutdown()


# ==================== 估值分析器 ====================

class ValuationAnalyzer:
    """估值分析器（优化版：使用akshare直接获取PE/PB历史，更准确）"""

    def __init__(self, dm: DataManager):
        self.dm = dm

    def _find_column(self, df: pd.DataFrame, keywords: Tuple[str, ...], exact_match_first: bool = True) -> Optional[str]:
        """根据关键词查找列名（优化：支持精确匹配优先）"""
        cols = list(df.columns)

        # 精确匹配（不区分大小写）
        if exact_match_first:
            for col in cols:
                if col.upper() in [kw.upper() for kw in keywords]:
                    return col

        # 包含匹配
        for col in cols:
            col_upper = col.upper().replace(' ', '').replace('_', '')
            for kw in keywords:
                if kw.upper().replace(' ', '').replace('_', '') in col_upper:
                    return col
        return None

    def _get_latest_financials(self, code: str) -> Tuple[Optional[float], Optional[float]]:
        """获取最新财务数据（EPS和BVPS）"""
        if get_asset_type(code) == AssetType.ETF:
            return None, None

        fin = self.dm.get_financial(code)
        if fin is None or fin.empty:
            return None, None

        try:
            eps_col = self._find_column(fin, Constants.EPS_KEYWORDS)
            bvps_col = self._find_column(fin, Constants.BVPS_KEYWORDS)
            date_col = self._find_column(fin, Constants.DATE_KEYWORDS)

            if not all([eps_col, bvps_col, date_col]):
                logger.debug(f"{code} 财务数据列匹配失败: eps={eps_col}, bvps={bvps_col}, date={date_col}")
                return None, None

            # 转换日期并排序
            fin[date_col] = pd.to_datetime(fin[date_col], errors='coerce')
            fin = fin.dropna(subset=[date_col, eps_col, bvps_col]).sort_values(date_col)

            if fin.empty:
                return None, None

            latest = fin.iloc[-1]
            eps = safe_float(latest[eps_col], allow_negative=True)  # EPS可能为负（亏损）
            bvps = safe_float(latest[bvps_col], allow_negative=False)

            return eps, bvps
        except Exception as e:
            logger.error(f"解析财务数据 {code} 失败: {e}")
            return None, None

    def calc_metrics(self, current: Optional[float], series: Optional[pd.Series],
                    name: str) -> Optional[ValuationMetrics]:
        """计算估值指标（优化版：支持空序列和无效值）"""
        if series is None or series.empty:
            return None

        threshold = Constants.MAX_PE if name == "PE" else Constants.MAX_PB

        # 数据清洗：去除无效值
        series = pd.to_numeric(series, errors='coerce')
        series = series[(series.notna()) & (series > 0) & (series < threshold)]

        if len(series) < Constants.MIN_HISTORY_DAYS:
            return None

        # 如果没有提供current，使用最新值
        if current is None or current <= 0 or current > threshold:
            current = float(series.iloc[-1])

        current = float(current)

        # 异常值警告
        warning = None
        if current < 0:
            warning = f"{name}为负，公司当前亏损（若为PE）或净资产为负（若为PB）"
        elif name == "PE" and current > 100:
            warning = "PE过高（>100），可能处于亏损边缘或成长性极高"
        elif name == "PB" and current > 10:
            warning = "PB过高（>10），注意资产泡沫风险"

        # 计算百分位（使用rank方法更准确）
        percentile = (series < current).mean() * 100

        return ValuationMetrics(
            current=round(current, 2),
            percentile=round(percentile, 2),
            min=round(float(series.min()), 2),
            max=round(float(series.max()), 2),
            median=round(float(series.median()), 2),
            band_20=round(float(series.quantile(0.2)), 2),
            band_50=round(float(series.quantile(0.5)), 2),
            band_80=round(float(series.quantile(0.8)), 2),
            points=len(series),
            warning=warning,
            calculation_method="historical_distribution"
        )

    def analyze_etf(self, code: str, rt: StockBasicInfo) -> ValuationResult:
        """ETF分析（修复版：更准确的净值逻辑）"""
        result = ValuationResult(
            code=code, 
            success=True, 
            asset_type=AssetType.ETF, 
            basic_info=rt,
            data_sources=['realtime']
        )

        # 净值和折溢价计算
        if rt.nav and rt.nav > 0:
            # 计算折溢价率（如果数据源未提供）
            if rt.premium_rate is None and rt.price:
                premium = ((rt.price - rt.nav) / rt.nav) * 100
            else:
                premium = rt.premium_rate

            result.etf = {
                'nav': round(rt.nav, 4),
                'price': rt.price,
                'premium_rate': round(premium, 2) if premium else None,
                'premium_status': '溢价' if premium and premium > 0.5 else '折价' if premium and premium < -0.5 else '合理'
            }
        else:
            # 无法获取净值，仅做价格分析
            result.etf = {
                'nav': None,
                'note': '无法获取实时净值，可能为LOF或非主流ETF'
            }

        # 历史价格分析（用于判断高低位）
        hist = self.dm.get_history(code)
        if hist is not None and not hist.empty:
            try:
                prices = pd.to_numeric(hist['收盘'], errors='coerce').dropna()
                if len(prices) >= Constants.MIN_HISTORY_DAYS:
                    current = rt.price
                    percentile = (prices < current).mean() * 100

                    ma20 = prices.rolling(20, min_periods=1).mean().iloc[-1]
                    ma60 = prices.rolling(60, min_periods=1).mean().iloc[-1]

                    # 趋势判断
                    if current > ma20 * 1.02 and ma20 > ma60 * 1.01:
                        trend = "强势上升"
                    elif current < ma20 * 0.98 and ma20 < ma60 * 0.99:
                        trend = "下降趋势"
                    else:
                        trend = "震荡整理"

                    if result.etf is None:
                        result.etf = {}
                    result.etf.update({
                        'price_percentile': round(percentile, 2),
                        'ma20': round(ma20, 3),
                        'ma60': round(ma60, 3),
                        'trend': trend,
                        'points': len(prices),
                        'historical_high': round(prices.max(), 2),
                        'historical_low': round(prices.min(), 2)
                    })

                    # 综合判断
                    nav_warning = result.etf.get('premium_status') == '溢价' and result.etf.get('premium_rate', 0) > 2

                    if percentile < 30 and not nav_warning:
                        result.zone = "机会区间"
                        result.suggestion = "价格处于历史低位且无明显溢价，可考虑定投或分批买入"
                    elif percentile > 70 or nav_warning:
                        result.zone = "风险区间"
                        if nav_warning:
                            result.suggestion = f"溢价过高（{result.etf['premium_rate']:.2f}%），建议等待折价或平价时买入"
                        else:
                            result.suggestion = "价格处于历史高位，注意回调风险，分批止盈"
                    else:
                        result.zone = "合理区间"
                        result.suggestion = "价格合理，持有观望，或按纪律定投"
                else:
                    result.zone = "数据不足"
                    result.suggestion = "历史数据不足（需至少60个交易日）"
            except Exception as e:
                logger.error(f"ETF历史分析 {code} 失败: {e}")
                result.zone = "分析错误"
                result.suggestion = "历史数据分析异常"
        else:
            result.zone = "数据不足"
            result.suggestion = "无法获取历史数据，建议参考实时净值折溢价判断"

        return result

    def analyze_stock(self, code: str, rt: StockBasicInfo) -> ValuationResult:
        """股票分析（优化版：优先使用akshare历史估值数据）"""
        result = ValuationResult(
            code=code, 
            success=True, 
            asset_type=AssetType.STOCK, 
            basic_info=rt,
            data_sources=['realtime']
        )

        # 首先尝试获取akshare的历史估值数据（更可靠）
        val_hist = self.dm.get_valuation_history(code)

        if val_hist is not None and not val_hist.empty:
            # 使用akshare直接提供的PE/PB历史
            pe_series = val_hist['pe_ttm'].dropna() if 'pe_ttm' in val_hist.columns else val_hist['pe'].dropna() if 'pe' in val_hist.columns else None
            pb_series = val_hist['pb'].dropna() if 'pb' in val_hist.columns else None

            if pe_series is not None and len(pe_series) >= Constants.MIN_HISTORY_DAYS:
                current_pe = rt.pe_ttm or rt.pe_dynamic
                result.pe = self.calc_metrics(current_pe, pe_series, "PE")

            if pb_series is not None and len(pb_series) >= Constants.MIN_HISTORY_DAYS:
                current_pb = rt.pb
                result.pb = self.calc_metrics(current_pb, pb_series, "PB")

            if result.pe or result.pb:
                result.data_sources.append('akshare_valuation_history')

        # 如果akshare没有数据，尝试计算PE/PB序列（降级方案）
        if result.pe is None or result.pb is None:
            pe_series, pb_series = self._calc_pe_pb_series_fallback(code, rt)

            if result.pe is None and pe_series is not None:
                current_pe = rt.pe_ttm or rt.pe_dynamic
                if current_pe is None or current_pe <= 0:
                    eps, _ = self._get_latest_financials(code)
                    if eps and eps > 0 and rt.price:
                        current_pe = rt.price / eps
                    elif pe_series is not None and not pe_series.empty:
                        current_pe = float(pe_series.iloc[-1])
                result.pe = self.calc_metrics(current_pe, pe_series, "PE")

            if result.pb is None and pb_series is not None:
                current_pb = rt.pb
                if current_pb is None or current_pb <= 0:
                    _, bvps = self._get_latest_financials(code)
                    if bvps and bvps > 0 and rt.price:
                        current_pb = rt.price / bvps
                    elif pb_series is not None and not pb_series.empty:
                        current_pb = float(pb_series.iloc[-1])
                result.pb = self.calc_metrics(current_pb, pb_series, "PB")

            if result.pe or result.pb:
                result.data_sources.append('calculated_fallback')

        # ROE处理
        if rt.roe and rt.roe > 0:
            result.roe = {
                'current': round(rt.roe, 2),
                'level': self._eval_roe(rt.roe),
                'note': self._roe_note(rt.roe)
            }
        else:
            # 尝试从财务数据计算ROE
            try:
                fin = self.dm.get_financial(code)
                if fin is not None:
                    roe_col = self._find_column(fin, ('ROE', '净资产收益率', 'RETURN_ON_EQUITY'))
                    if roe_col:
                        latest_roe = safe_float(fin.iloc[-1][roe_col])
                        if latest_roe and latest_roe > 0:
                            result.roe = {
                                'current': round(latest_roe, 2),
                                'level': self._eval_roe(latest_roe),
                                'note': self._roe_note(latest_roe)
                            }
            except Exception as e:
                logger.debug(f"获取ROE失败 {code}: {e}")

        result.zone, result.suggestion = self._determine_zone(result)
        return result

    def _calc_pe_pb_series_fallback(self, code: str, rt: StockBasicInfo) -> Tuple[Optional[pd.Series], Optional[pd.Series]]:
        """降级方案：通过财务数据和历史价格计算PE/PB序列"""
        if get_asset_type(code) == AssetType.ETF:
            return None, None

        hist = self.dm.get_history(code)
        fin = self.dm.get_financial(code)

        if hist is None or fin is None:
            return None, None

        try:
            # 标准化列名
            fin.columns = [c.upper() for c in fin.columns]

            eps_col = self._find_column(fin, Constants.EPS_KEYWORDS)
            bvps_col = self._find_column(fin, Constants.BVPS_KEYWORDS)
            date_col = self._find_column(fin, Constants.DATE_KEYWORDS)

            if not all([eps_col, bvps_col, date_col]):
                return None, None

            # 处理财务数据日期
            fin[date_col] = pd.to_datetime(fin[date_col], errors='coerce')
            fin = fin.dropna(subset=[date_col, eps_col, bvps_col]).sort_values(date_col)

            if fin.empty:
                return None, None

            # 处理历史价格数据
            price_col = '收盘' if '收盘' in hist.columns else 'close' if 'close' in hist.columns else None
            date_col_price = '日期' if '日期' in hist.columns else 'date' if 'date' in hist.columns else None

            if not price_col or not date_col_price:
                return None, None

            hist[date_col_price] = pd.to_datetime(hist[date_col_price])
            hist[price_col] = pd.to_numeric(hist[price_col], errors='coerce')
            hist = hist.dropna(subset=[date_col_price, price_col]).sort_values(date_col_price)

            # 合并数据（使用asof合并）
            merged = pd.merge_asof(
                hist[[date_col_price, price_col]], 
                fin[[date_col, eps_col, bvps_col]],
                left_on=date_col_price, 
                right_on=date_col, 
                direction='backward'
            )

            if merged.empty:
                return None, None

            # 计算PE/PB
            prices = merged[price_col].values
            eps = pd.to_numeric(merged[eps_col], errors='coerce').values
            bvps = pd.to_numeric(merged[bvps_col], errors='coerce').values

            # 只保留正值
            pe_vals = np.where((eps > 0) & (eps < 1000) & (prices > 0), prices / eps, np.nan)
            pb_vals = np.where((bvps > 0) & (bvps < 1000) & (prices > 0), prices / bvps, np.nan)

            pe_series = pd.Series(pe_vals, index=merged[date_col_price]).dropna()
            pb_series = pd.Series(pb_vals, index=merged[date_col_price]).dropna()

            # 过滤异常值
            pe_series = pe_series[(pe_series > 0) & (pe_series < Constants.MAX_PE)]
            pb_series = pb_series[(pb_series > 0) & (pb_series < Constants.MAX_PB)]

            return pe_series, pb_series

        except Exception as e:
            logger.error(f"计算PE/PB序列 {code} 失败: {e}")
            return None, None

    def analyze(self, code: str, rt: Optional[StockBasicInfo]) -> ValuationResult:
        """分析入口"""
        at = get_asset_type(code)

        if rt is None:
            return ValuationResult(
                code=code, 
                success=False, 
                asset_type=at,
                message=f"无法获取 {code} 的实时数据，请检查代码是否正确或网络连接"
            )

        if at == AssetType.ETF:
            return self.analyze_etf(code, rt)
        else:
            return self.analyze_stock(code, rt)

    def _eval_roe(self, roe: float) -> str:
        """评估ROE水平"""
        if roe > 20: return "优秀"
        elif roe > 15: return "良好"
        elif roe > 10: return "一般"
        elif roe > 5: return "较低"
        elif roe > 0: return "差"
        else: return "亏损"

    def _roe_note(self, roe: float) -> str:
        """ROE评价说明"""
        if roe > 20: return "高盈利能力，可能具备护城河"
        elif roe > 15: return "盈利能力较强，值得持续关注"
        elif roe > 10: return "盈利能力一般，需结合行业判断"
        elif roe > 0: return "盈利能力较弱"
        else: return "当前亏损，谨慎评估"

    def _determine_zone(self, r: ValuationResult) -> Tuple[str, str]:
        """确定估值区间（优化版：更细致的判断逻辑）"""
        opp, risk = Constants.OPP_THRESHOLD, Constants.RISK_THRESHOLD

        pe_zone = self._get_zone(r.pe, opp, risk) if r.pe else '未知'
        pb_zone = self._get_zone(r.pb, opp, risk) if r.pb else '未知'

        # 两者都有数据
        if pe_zone != '未知' and pb_zone != '未知':
            if '机会' in pe_zone and '机会' in pb_zone:
                return '机会区间（双重低估）', "PE和PB均处于历史低位，具备安全边际，可关注买入机会"
            elif '风险' in pe_zone and '风险' in pb_zone:
                return '风险区间（双重高估）', "PE和PB均处于历史高位，估值泡沫风险较大，建议分批止盈"
            elif pe_zone == pb_zone:
                return pe_zone, self._get_suggestion(pe_zone)
            else:
                # 指标分化
                if '机会' in pe_zone or '机会' in pb_zone:
                    return '低估倾向', "部分指标处于低位，但存在分化，建议深入研究基本面"
                elif '风险' in pe_zone or '风险' in pb_zone:
                    return '高估倾向', "部分指标处于高位，建议谨慎，等待回调或分化收敛"
                else:
                    return '合理区间（分化）', "指标分化，需结合ROE、成长性等因素综合判断"

        # 只有单一指标
        if pe_zone != '未知':
            return f"PE{pe_zone}", self._get_suggestion(pe_zone)
        if pb_zone != '未知':
            return f"PB{pb_zone}", self._get_suggestion(pb_zone)

        return '数据不足', '无法获取足够的历史估值数据，建议参考绝对估值或同业比较'

    def _get_zone(self, m: ValuationMetrics, opp: float, risk: float) -> str:
        """获取区间"""
        if m.percentile < opp: return '机会区间'
        elif m.percentile > risk: return '风险区间'
        return '合理区间'

    def _get_suggestion(self, zone: str) -> str:
        """获取建议"""
        return {
            '机会区间': '估值偏低，具备安全边际，可关注分批买入机会',
            '合理区间': '估值合理，持有观望，或按纪律定投',
            '风险区间': '估值偏高，注意回撤风险，建议分批止盈或等待回调'
        }.get(zone, '数据不足，建议参考其他分析方法')


# ==================== 主类 ====================

class StockValuationMonitor:
    """估值监控主类（借鉴QVeris风格：标准化接口+导出功能+健康检查）"""

    def __init__(self):
        self.dm = DataManager()
        self.analyzer = ValuationAnalyzer(self.dm)
        self._initialized = True

    def extract_codes(self, message: str) -> List[Tuple[str, AssetType]]:
        """提取代码（优化：更严格的验证）"""
        if not message:
            return []

        # 支持6位数字，前后不能是数字
        pattern = re.compile(r'(?<![0-9])([0-9]{6})(?![0-9])')
        matches = pattern.finditer(message)

        codes = []
        for m in matches:
            code = m.group(1)
            valid, err_msg, at = validate_code(code)
            if valid:
                codes.append((code, at))
            else:
                logger.debug(f"代码 {code} 验证失败: {err_msg}")

        # 去重并保持顺序
        seen = set()
        unique_codes = []
        for c, at in codes:
            if c not in seen:
                seen.add(c)
                unique_codes.append((c, at))
        return unique_codes

    def format_output(self, r: ValuationResult) -> str:
        """格式化输出（QVeris风格：结构化+emoji，优化排版）"""
        if not r.success:
            return f"❌ {r.code}: {r.message}\n"

        info = r.basic_info
        is_etf = r.asset_type == AssetType.ETF

        lines = [
            "=" * 72,
            f"📊 {info.name or '未知'} ({r.code}) {'ETF' if is_etf else 'A股'} 估值分析报告",
            f"⏰ 数据时间: {info.update_time or '未知'} | 数据源: {', '.join(r.data_sources)}",
            "=" * 72,
            "",
            "💰 实时行情:",
            f"  当前价格: ¥{info.price:.2f}" + (f" ({info.change_pct:+.2f}%)" if info.change_pct is not None else ""),
        ]

        if info.market_cap:
            lines.append(f"  总市值: {info.market_cap:.2f}亿")
        if info.volume:
            lines.append(f"  成交量: {info.volume:,.0f}手")

        if is_etf:
            if r.etf:
                lines.append("")
                lines.append("📈 ETF净值分析:")
                if r.etf.get('nav'):
                    lines.append(f"  单位净值: ¥{r.etf['nav']:.4f}")
                    if r.etf.get('premium_rate') is not None:
                        status_emoji = "🔴" if r.etf['premium_status'] == '溢价' else "🟢" if r.etf['premium_status'] == '折价' else "⚪"
                        lines.append(f"  折溢价率: {r.etf['premium_rate']:+.2f}% {status_emoji} ({r.etf['premium_status']})")

                if r.etf.get('price_percentile') is not None:
                    p = r.etf['price_percentile']
                    emoji = "🟢" if p < 30 else "🟡" if p < 70 else "🔴"
                    lines.append("")
                    lines.append("📉 技术分析:")
                    lines.append(f"  价格历史分位: {p:.1f}% {emoji}")
                    if r.etf.get('trend'):
                        lines.append(f"  趋势判断: {r.etf['trend']}")
                    if r.etf.get('ma20') and r.etf.get('ma60'):
                        lines.append(f"  均线系统: MA20=¥{r.etf['ma20']:.3f}, MA60=¥{r.etf['ma60']:.3f}")
                    if r.etf.get('historical_high') and r.etf.get('historical_low'):
                        lines.append(f"  历史区间: ¥{r.etf['historical_low']:.2f} - ¥{r.etf['historical_high']:.2f}")
        else:
            # 股票估值分析
            if r.pe or r.pb:
                lines.append("")
                lines.append("📈 估值指标:")

            if r.pe:
                emoji = "🟢" if r.pe.percentile < 30 else "🟡" if r.pe.percentile < 70 else "🔴"
                lines.append(f"  PE-TTM: {r.pe.current:.2f} | 历史百分位: {r.pe.percentile:.1f}% {emoji}")
                lines.append(f"         区间: {r.pe.min:.2f} - {r.pe.max:.2f} | 中位数: {r.pe.median:.2f}")
                lines.append(f"         20%/50%/80%分位: {r.pe.band_20:.2f} / {r.pe.band_50:.2f} / {r.pe.band_80:.2f}")
                if r.pe.warning:
                    lines.append(f"         ⚠️  {r.pe.warning}")
                lines.append("")

            if r.pb:
                emoji = "🟢" if r.pb.percentile < 30 else "🟡" if r.pb.percentile < 70 else "🔴"
                lines.append(f"  PB: {r.pb.current:.2f} | 历史百分位: {r.pb.percentile:.1f}% {emoji}")
                lines.append(f"      区间: {r.pb.min:.2f} - {r.pb.max:.2f} | 中位数: {r.pb.median:.2f}")
                lines.append(f"      20%/50%/80%分位: {r.pb.band_20:.2f} / {r.pb.band_50:.2f} / {r.pb.band_80:.2f}")
                if r.pb.warning:
                    lines.append(f"      ⚠️  {r.pb.warning}")
                lines.append("")

            if r.roe:
                emoji = "🟢" if r.roe['current'] > 15 else "🟡" if r.roe['current'] > 10 else "🔴"
                lines.append(f"  ROE: {r.roe['current']:.2f}% ({r.roe['level']}) {emoji}")
                if r.roe.get('note'):
                    lines.append(f"       {r.roe['note']}")

        lines.extend([
            "",
            "=" * 72,
            "🎯 综合评估:",
            f"  估值区间: {r.zone}",
            f"  投资建议: {r.suggestion}",
            "",
            "=" * 72,
            "⚠️ 免责声明: 本分析仅供参考，不构成投资建议。投资有风险，决策需谨慎。",
            "=" * 72,
        ])

        return "\n".join(lines)

    def analyze_batch(self, codes: List[Tuple[str, AssetType]], timeout: int = 60) -> List[ValuationResult]:
        """批量分析（带超时）"""
        codes = codes[:5]  # 限制5只

        # 确保数据获取有足够时间，至少15秒
        data_timeout = max(15, timeout // 2)
        rt_data = self.dm.get_batch(codes, timeout=data_timeout)

        results = []
        with ThreadPoolExecutor(max_workers=min(len(codes), Constants.MAX_WORKERS)) as executor:
            futures = {
                executor.submit(self.analyzer.analyze, code, rt_data.get(code, (None, []))[0]): code
                for code, _ in codes
            }

            try:
                # 分析过程剩余时间
                analysis_timeout = max(5, timeout - data_timeout)
                for future in as_completed(futures, timeout=analysis_timeout):
                    code = futures[future]
                    try:
                        result = future.result()
                        # 补充数据源信息
                        if code in rt_data:
                            _, sources = rt_data[code]
                            result.data_sources.extend(sources)
                        results.append(result)
                    except Exception as e:
                        logger.error(f"分析 {code} 异常: {e}")
                        results.append(ValuationResult(
                            code=code, 
                            success=False, 
                            message=f"分析异常: {str(e)}"
                        ))
            except FutureTimeoutError:
                logger.warning("批量分析超时")

        # 按原顺序排序
        code_map = {r.code: r for r in results}
        return [code_map.get(code, ValuationResult(code=code, success=False, message="未找到结果")) 
                for code, _ in codes]

    def export_to_json(self, results: List[ValuationResult]) -> str:
        """导出为JSON"""
        data = [r.to_dict() for r in results]
        return json.dumps(data, ensure_ascii=False, indent=2)

    def export_to_csv(self, results: List[ValuationResult]) -> str:
        """导出为CSV（安全判断优化）"""
        import csv
        import io

        output = io.StringIO()
        writer = csv.writer(output)

        # 写入表头
        headers = ['代码', '名称', '类型', '价格', '涨跌幅%', 'PE', 'PE百分位', 'PE预警',
                   'PB', 'PB百分位', 'PB预警', 'ROE%', 'ROE评级', '估值区间', '建议', '数据源', '时间戳']
        writer.writerow(headers)

        for r in results:
            if not r.success or not r.basic_info:
                writer.writerow([r.code, '', '', '', '', '', '', '', '', '', '', '', '', r.message, '', ''])
                continue

            bi = r.basic_info
            pe_warning = r.pe.warning if r.pe else ''
            pb_warning = r.pb.warning if r.pb else ''

            writer.writerow([
                r.code,
                bi.name or '',
                'ETF' if r.asset_type == AssetType.ETF else '股票',
                bi.price if bi.price else '',
                bi.change_pct if bi.change_pct is not None else '',
                r.pe.current if r.pe else '',
                r.pe.percentile if r.pe else '',
                pe_warning,
                r.pb.current if r.pb else '',
                r.pb.percentile if r.pb else '',
                pb_warning,
                r.roe['current'] if r.roe else '',
                r.roe['level'] if r.roe else '',
                r.zone,
                r.suggestion,
                ','.join(r.data_sources),
                r.timestamp
            ])

        return output.getvalue()

    def export_to_excel(self, results: List[ValuationResult]) -> Optional[bytes]:
        """导出为Excel（需要openpyxl），若无数据则返回带表头的空文件"""
        if not EXCEL_AVAILABLE:
            return None

        import io
        output = io.BytesIO()

        data = []
        for r in results:
            if not r.success or not r.basic_info:
                continue
            bi = r.basic_info
            data.append({
                '代码': r.code,
                '名称': bi.name,
                '类型': 'ETF' if r.asset_type == AssetType.ETF else '股票',
                '价格': bi.price,
                '涨跌幅%': bi.change_pct,
                'PE': r.pe.current if r.pe else None,
                'PE百分位': r.pe.percentile if r.pe else None,
                'PB': r.pb.current if r.pb else None,
                'PB百分位': r.pb.percentile if r.pb else None,
                'ROE%': r.roe['current'] if r.roe else None,
                '估值区间': r.zone,
                '建议': r.suggestion,
                '数据源': ','.join(r.data_sources),
                '时间': r.timestamp
            })

        # 如果没有数据，创建一个只有表头的 DataFrame
        if not data:
            df = pd.DataFrame(columns=['代码', '名称', '类型', '价格', '涨跌幅%', 'PE', 'PE百分位',
                                       'PB', 'PB百分位', 'ROE%', '估值区间', '建议', '数据源', '时间'])
        else:
            df = pd.DataFrame(data)

        df.to_excel(output, index=False, engine='openpyxl')
        return output.getvalue()

    def health_check(self) -> Dict:
        """系统健康检查"""
        return self.dm.health_check()

    def shutdown(self):
        """优雅关闭"""
        self.dm.shutdown()


# ==================== SKILL入口 ====================

def handle(request: Dict) -> Dict:
    """SKILL入口（QVeris风格：标准化输入输出，增强错误处理）"""
    try:
        if not isinstance(request, dict):
            return {"status": "error", "message": "请求格式错误", "code": "INVALID_REQUEST"}

        message = request.get("message", "")
        if not message:
            return {"status": "error", "message": "请输入查询内容", "example": "查询600519的估值", "code": "EMPTY_MESSAGE"}

        # 支持导出格式参数
        export_format = request.get("export", "text")  # text, json, csv, excel

        # 超时设置
        timeout = request.get("timeout", 60)
        if not isinstance(timeout, int) or timeout < 10 or timeout > 120:
            timeout = 60

        monitor = StockValuationMonitor()
        try:
            codes = monitor.extract_codes(message)

            if not codes:
                return {
                    "status": "error", 
                    "message": "未识别有效代码（请输入6位数字代码，如600519）", 
                    "example": "查询600519、000001、510050",
                    "code": "NO_VALID_CODES"
                }

            if len(codes) > 5:
                return {
                    "status": "error", 
                    "message": f"最多支持5只，当前{len(codes)}只，请减少数量", 
                    "code": "TOO_MANY_CODES"
                }

            results = monitor.analyze_batch(codes, timeout=timeout)

            # 根据格式返回
            if export_format == "json":
                return {
                    "status": "success",
                    "message": monitor.export_to_json(results),
                    "data": {
                        "format": "json", 
                        "count": len(results),
                        "codes": [c for c, _ in codes],
                        "health": monitor.health_check()
                    },
                    "code": "SUCCESS"
                }
            elif export_format == "csv":
                return {
                    "status": "success",
                    "message": monitor.export_to_csv(results),
                    "data": {
                        "format": "csv", 
                        "count": len(results),
                        "codes": [c for c, _ in codes]
                    },
                    "code": "SUCCESS"
                }
            elif export_format == "excel":
                excel_data = monitor.export_to_excel(results)
                if excel_data:
                    import base64
                    return {
                        "status": "success",
                        "message": "Excel导出成功",
                        "data": {
                            "format": "excel",
                            "content": base64.b64encode(excel_data).decode('utf-8'),
                            "count": len(results)
                        },
                        "code": "SUCCESS"
                    }
                else:
                    return {
                        "status": "error",
                        "message": "Excel导出失败（可能缺少openpyxl库）",
                        "code": "EXPORT_FAILED"
                    }
            else:
                formatted = [monitor.format_output(r) for r in results]
                return {
                    "status": "success",
                    "message": "\n\n".join(formatted),
                    "data": {
                        "codes": [c for c, _ in codes],
                        "count": len(codes),
                        "results": [
                            {
                                "code": r.code, 
                                "type": r.asset_type.value,
                                "zone": r.zone,
                                "success": r.success,
                                "sources": r.data_sources
                            } for r in results
                        ],
                        "health": monitor.health_check()
                    },
                    "code": "SUCCESS"
                }
        finally:
            monitor.shutdown()

    except Exception as e:
        logger.exception("系统异常")
        return {
            "status": "error", 
            "message": f"系统异常: {type(e).__name__}: {str(e)}", 
            "suggestion": "请稍后重试或联系管理员",
            "code": "SYSTEM_ERROR"
        }


# ==================== 测试 ====================

if __name__ == "__main__":
    test_cases = [
        {"message": "查询300327的估值", "export": "text"},
        {"message": "看看688981和002594怎么样", "export": "text"},
        {"message": "分析600519", "export": "text"},
        {"message": "查一下510050 ETF", "export": "text"},
        {"message": "查询000001、000002、600036", "export": "json"},
        {"message": "查询999999", "export": "text"},  # 无效代码测试
    ]

    print("🚀 Stock Valuation Monitor V4.5.1 - 测试运行")
    print("=" * 72)

    for req in test_cases:
        print(f"\n📝 请求: {req}")
        print("-" * 72)
        try:
            resp = handle(req)
            print(f"状态: {resp['status']} ({resp.get('code', 'N/A')})")
            if resp['status'] == "success":
                msg = resp['message']
                if len(msg) > 500:
                    print(msg[:500] + "...\n[内容过长，已截断]")
                else:
                    print(msg)
                if 'health' in resp.get('data', {}):
                    print(f"\n[系统健康] 缓存命中率: {resp['data']['health']['cache']['hit_rate']:.1%}")
            else:
                print(f"错误: {resp['message']}")
                if 'suggestion' in resp:
                    print(f"建议: {resp['suggestion']}")
        except Exception as e:
            print(f"异常: {e}")
            import traceback
            traceback.print_exc()
        print("\n" + "=" * 72)