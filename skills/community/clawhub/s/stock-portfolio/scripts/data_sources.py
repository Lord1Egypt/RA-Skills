#!/usr/bin/env python3
"""
数据源适配器模块
提供统一的数据源接口和轮询负载均衡
"""

import urllib.request
import re
import json
from abc import ABC, abstractmethod
from datetime import datetime


def normalize_symbol(symbol, target_format='tencent'):
    """
    将用户输入的股票代码转换为各数据源格式

    Args:
        symbol: 原始股票代码 (如 600519, AAPL, 00700)
        target_format: 目标格式 ('tencent', 'sina', 'eastmoney')

    Returns:
        转换后的代码格式
    """
    symbol = str(symbol).strip()

    # 美股（字母）
    if re.match(r'^[A-Za-z]+$', symbol):
        if target_format == 'tencent':
            return f"us{symbol.upper()}"
        elif target_format == 'sina':
            return f"gb_{symbol.lower()}"
        elif target_format == 'eastmoney':
            return f"105.{symbol.upper()}"  # 美股市场代码 105
        return symbol

    # 港股（0 开头 5 位数字）
    if re.match(r'^0\d{4}$', symbol):
        if target_format == 'tencent':
            return f"hk{symbol}"
        elif target_format == 'sina':
            return f"hk{symbol}"
        elif target_format == 'eastmoney':
            return f"116.{symbol}"  # 港股市场代码 116
        return symbol

    # A 股（6 位数字）
    if re.match(r'^\d{6}$', symbol):
        if target_format in ('tencent', 'sina'):
            if symbol.startswith('6'):
                return f"sh{symbol}"
            else:
                return f"sz{symbol}"
        elif target_format == 'eastmoney':
            if symbol.startswith('6'):
                return f"1.{symbol}"  # 上证市场代码 1
            else:
                return f"0.{symbol}"  # 深证市场代码 0
        return symbol

    # 已经是完整格式
    if symbol.startswith(('sh', 'sz', 'hk', 'us')):
        return symbol

    raise ValueError(f"无法识别的股票代码格式：{symbol}")


def get_market_code(symbol):
    """
    获取东方财富市场代码
    """
    symbol = str(symbol).strip()

    # 美股
    if re.match(r'^[A-Za-z]+$', symbol):
        return 105

    # 港股
    if re.match(r'^0\d{4}$', symbol):
        return 116

    # A 股
    if re.match(r'^\d{6}$', symbol):
        if symbol.startswith('6'):
            return 1  # 上证
        else:
            return 0  # 深证

    return 1  # 默认上证


class DataSource(ABC):
    """数据源抽象基类"""

    @property
    @abstractmethod
    def name(self) -> str:
        """数据源名称"""
        pass

    @abstractmethod
    def fetch(self, symbol: str) -> dict | None:
        """
        获取股票行情

        Args:
            symbol: 股票代码

        Returns:
            统一格式字典，失败返回 None
        """
        pass


class TencentSource(DataSource):
    """腾讯财经数据源"""

    @property
    def name(self) -> str:
        return 'tencent'

    def fetch(self, symbol: str) -> dict | None:
        try:
            norm_symbol = normalize_symbol(symbol, 'tencent')
            url = f"http://qt.gtimg.cn/q={norm_symbol}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('Referer', 'https://stockapp.finance.qq.com/')

            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('gbk', errors='ignore')

            match = re.search(r'="([^"]+)"', content)
            if not match:
                return None

            data = match.group(1).split('~')

            if len(data) < 35:
                return None

            name = data[1] if len(data) > 1 else ''
            code = data[2] if len(data) > 2 else ''
            current = float(data[3]) if len(data) > 3 and data[3] else 0
            prev_close = float(data[4]) if len(data) > 4 and data[4] else 0
            open_price = float(data[5]) if len(data) > 5 and data[5] else 0
            volume = int(float(data[6])) * 100 if len(data) > 6 and data[6] else 0
            high = float(data[33]) if len(data) > 33 and data[33] else 0
            low = float(data[34]) if len(data) > 34 and data[34] else 0
            change = float(data[31]) if len(data) > 31 and data[31] else 0
            change_pct = float(data[32]) if len(data) > 32 and data[32] else 0
            turnover = float(data[47]) * 10000 if len(data) > 47 and data[47] else 0

            return {
                'symbol': code or symbol,
                'name': name,
                'current': current,
                'open': open_price,
                'high': high,
                'low': low,
                'prev_close': prev_close,
                'change': change,
                'change_pct': change_pct,
                'volume': volume,
                'turnover': turnover,
                'source': self.name,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception:
            return None


class SinaSource(DataSource):
    """新浪财经数据源"""

    @property
    def name(self) -> str:
        return 'sina'

    def fetch(self, symbol: str) -> dict | None:
        try:
            norm_symbol = normalize_symbol(symbol, 'sina')
            url = f"http://hq.sinajs.cn/s={norm_symbol}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('Referer', 'https://finance.sina.com.cn/')

            with urllib.request.urlopen(req, timeout=10) as response:
                content = response.read().decode('gbk', errors='ignore')

            match = re.search(r'="([^"]+)"', content)
            if not match:
                return None

            data_str = match.group(1)
            if not data_str:
                return None

            data = data_str.split(',')

            if len(data) < 32:
                return None

            name = data[0]
            open_price = float(data[1]) if data[1] else 0
            prev_close = float(data[2]) if data[2] else 0
            current = float(data[3]) if data[3] else 0
            high = float(data[4]) if data[4] else 0
            low = float(data[5]) if data[5] else 0
            volume = int(float(data[8])) if data[8] else 0
            turnover = float(data[9]) if data[9] else 0

            # 计算涨跌
            change = current - prev_close if current and prev_close else 0
            change_pct = (change / prev_close * 100) if prev_close else 0

            return {
                'symbol': symbol,
                'name': name,
                'current': current,
                'open': open_price,
                'high': high,
                'low': low,
                'prev_close': prev_close,
                'change': round(change, 2),
                'change_pct': round(change_pct, 2),
                'volume': volume,
                'turnover': turnover,
                'source': self.name,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception:
            return None


class EastMoneySource(DataSource):
    """东方财富数据源"""

    @property
    def name(self) -> str:
        return 'eastmoney'

    def fetch(self, symbol: str) -> dict | None:
        try:
            market = get_market_code(symbol)
            code = normalize_symbol(symbol, 'eastmoney')

            # 东方财富字段代码
            fields = [
                'f43',  # 最新价
                'f44',  # 最高
                'f45',  # 最低
                'f46',  # 今开
                'f47',  # 成交量
                'f48',  # 成交额
                'f50',  # 昨收
                'f51',  # 涨跌额
                'f52',  # 涨跌幅
                'f58',  # 股票名称
                'f60',  # 股票代码
            ]

            url = f"http://push2.eastmoney.com/api/qt/stock/get?secid={code}&fields={','.join(fields)}"

            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            req.add_header('Referer', 'https://quote.eastmoney.com/')

            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))

            if not result or 'data' not in result or not result['data']:
                return None

            data = result['data']

            # 东方财富返回的数据需要除以 100（价格精度处理）
            current = data.get('f43', 0) / 100 if data.get('f43') else 0
            high = data.get('f44', 0) / 100 if data.get('f44') else 0
            low = data.get('f45', 0) / 100 if data.get('f45') else 0
            open_price = data.get('f46', 0) / 100 if data.get('f46') else 0
            volume = data.get('f47', 0)  # 成交量（手）
            turnover = data.get('f48', 0)  # 成交额
            prev_close = data.get('f50', 0) / 100 if data.get('f50') else 0
            change = data.get('f51', 0) / 100 if data.get('f51') else 0
            change_pct = data.get('f52', 0) / 100 if data.get('f52') else 0
            name = data.get('f58', '')
            code_str = data.get('f60', symbol)

            return {
                'symbol': code_str or symbol,
                'name': name,
                'current': current,
                'open': open_price,
                'high': high,
                'low': low,
                'prev_close': prev_close,
                'change': change,
                'change_pct': change_pct,
                'volume': volume * 100,  # 手转股
                'turnover': turnover,
                'source': self.name,
                'update_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception:
            return None


class DataSourceManager:
    """数据源管理器 - 轮询负载均衡"""

    _instance = None

    def __new__(cls, sources=None):
        """单例模式，保证全局只有一个管理器"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, sources: list[DataSource] | None = None):
        if self._initialized:
            return

        if sources is None:
            # 默认使用三个数据源，按优先级排序
            sources = [
                TencentSource(),
                SinaSource(),
                EastMoneySource(),
            ]

        self.sources = sources
        self.index = 0
        self._initialized = True

    def fetch(self, symbol: str) -> dict:
        """
        轮询获取数据，失败则尝试下一个数据源

        Args:
            symbol: 股票代码

        Returns:
            统一格式的股票行情字典
        """
        errors = []

        for _ in range(len(self.sources)):
            source = self.sources[self.index]
            self.index = (self.index + 1) % len(self.sources)

            result = source.fetch(symbol)
            if result and result.get('current', 0) > 0:
                return result

            errors.append(f"{source.name}: 获取失败")

        return {'error': '所有数据源均获取失败', 'details': errors}

    def reset_index(self):
        """重置轮询索引"""
        self.index = 0

    def add_source(self, source: DataSource):
        """添加数据源"""
        if source not in self.sources:
            self.sources.append(source)


# 全局管理器实例
_manager = None


def get_manager() -> DataSourceManager:
    """获取全局数据源管理器"""
    global _manager
    if _manager is None:
        _manager = DataSourceManager()
    return _manager


def fetch_stock_price(symbol: str) -> dict:
    """
    便捷函数：使用全局管理器获取股票行情

    Args:
        symbol: 股票代码

    Returns:
        统一格式的股票行情字典
    """
    return get_manager().fetch(symbol)