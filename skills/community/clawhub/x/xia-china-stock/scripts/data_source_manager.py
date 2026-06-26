#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
统一数据源管理器 - Unified Data Source Manager
实现数据源优先级管理和自动 fallback 机制
"""

import time
import json
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path
import sys

try:
    import pandas as pd
except ImportError:
    print("请安装依赖: pip install pandas")
    sys.exit(1)


class DataSourceMetrics:
    """数据源性能指标记录"""
    
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.max_history = 100
    
    def record(self, source_name: str, success: bool, response_time: float):
        """记录一次调用结果"""
        self.history.append({
            'source': source_name,
            'success': success,
            'response_time': response_time,
            'timestamp': datetime.now().isoformat()
        })
        
        # 限制历史记录数量
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]
    
    def get_stats(self, source_name: str) -> Dict[str, Any]:
        """获取指定数据源的统计信息"""
        records = [r for r in self.history if r['source'] == source_name]
        
        if not records:
            return {
                'total_calls': 0,
                'success_rate': 0,
                'avg_response_time': 0
            }
        
        success_count = sum(1 for r in records if r['success'])
        total_time = sum(r['response_time'] for r in records)
        
        return {
            'total_calls': len(records),
            'success_rate': success_count / len(records) * 100,
            'avg_response_time': total_time / len(records),
            'last_success': any(r['success'] for r in records[-5:])  # 最近5次是否有成功
        }


class DataSource:
    """数据源基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.priority = 0  # 优先级，数字越小优先级越高
    
    def is_available(self) -> bool:
        """检查数据源是否可用"""
        raise NotImplementedError
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        """获取数据"""
        raise NotImplementedError


class SinaSource(DataSource):
    """新浪财经数据源 (优先级1) - 免费、无需API Key、稳定可靠"""
    
    def __init__(self):
        super().__init__("Sina Finance")
        self.priority = 1
    
    def is_available(self) -> bool:
        try:
            import requests
            return True
        except ImportError:
            return False
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        try:
            from sina_finance import fetch_kline
            df = fetch_kline(symbol, period)
            if df is not None and not df.empty:
                return df
        except Exception as e:
            print(f"Sina Finance failed: {e}")
        return None


class EastMoneySource(DataSource):
    """东方财富数据源 (优先级2)"""
    
    def __init__(self):
        super().__init__("东方财富")
        self.priority = 2
        self.session = None
    
    def is_available(self) -> bool:
        try:
            import requests
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry
            self.requests = requests
            self.HTTPAdapter = HTTPAdapter
            self.Retry = Retry
            return True
        except ImportError:
            return False
    
    def _create_session(self):
        """创建带重试机制的session"""
        session = self.requests.Session()
        retry = self.Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = self.HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    
    def _convert_symbol(self, symbol: str) -> tuple:
        """转换股票代码为东方财富格式"""
        symbol = symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '')
        
        if symbol.startswith(('6', '9', '5')):
            return ('1', symbol)  # 沪市
        else:
            return ('0', symbol)  # 深市
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not hasattr(self, 'requests'):
            return None
        
        session = self._create_session()
        
        try:
            from datetime import timedelta
            market, code = self._convert_symbol(symbol)
            
            # 计算日期范围
            end_date = datetime.now()
            period_map = {
                '1mo': 30, '3mo': 90, '6mo': 180, '1y': 365
            }
            days = period_map.get(period, 180)
            start_date = end_date - timedelta(days=days)
            
            # 使用更稳定的东方财富接口
            url = "https://push2his.eastmoney.com/api/qt/stock/kline/get"
            params = {
                'secid': f'{market}.{code}',
                'fields1': 'f1,f2,f3,f4,f5,f6',
                'fields2': 'f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61',
                'klt': '101',  # 日K
                'fqt': '1',    # 前复权
                'beg': start_date.strftime('%Y%m%d'),
                'end': end_date.strftime('%Y%m%d'),
                'ut': 'fa5fd1943c7b386f172d6893dbfba10b'
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://quote.eastmoney.com/'
            }
            
            resp = session.get(url, params=params, headers=headers, timeout=15)
            data = resp.json()
            
            if data.get('data') and data['data'].get('klines'):
                klines = data['data']['klines']
                
                records = []
                for line in klines:
                    parts = line.split(',')
                    records.append({
                        'date': parts[0],
                        'open': float(parts[1]),
                        'close': float(parts[2]),
                        'high': float(parts[3]),
                        'low': float(parts[4]),
                        'volume': float(parts[5]),
                        'amount': float(parts[6])
                    })
                
                df = pd.DataFrame(records)
                df['date'] = pd.to_datetime(df['date'])
                df = df.set_index('date')
                
                return df[['open', 'high', 'low', 'close', 'volume']]
            
            return None
            
        except Exception as e:
            print(f"东方财富获取失败: {e}")
            return None
        finally:
            session.close()


class AkshareSource(DataSource):
    """Akshare数据源 (优先级3)"""
    
    def __init__(self):
        super().__init__("Akshare")
        self.priority = 3
        self.ak = None
    
    def is_available(self) -> bool:
        try:
            import akshare as ak
            self.ak = ak
            return True
        except ImportError:
            return False
    
    def _convert_symbol(self, symbol: str) -> str:
        """转换股票代码"""
        return symbol.replace('.SZ', '').replace('.SH', '').replace('.SS', '')
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        if not self.ak:
            return None
        
        code = self._convert_symbol(symbol)
        
        # 尝试多个akshare接口
        methods = [
            self._fetch_via_em_hist,
            self._fetch_via_sina,
        ]
        
        for method in methods:
            try:
                df = method(code, period)
                if df is not None and not df.empty:
                    return df
            except Exception:
                continue
        
        return None
    
    def _fetch_via_em_hist(self, code: str, period: str) -> Optional[pd.DataFrame]:
        """通过东方财富历史数据接口"""
        from datetime import timedelta
        import time
        
        # 日期范围
        period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
        days = period_days.get(period, 180)
        
        # 重试机制
        for attempt in range(3):
            try:
                df = self.ak.stock_zh_a_hist(
                    symbol=code,
                    period="daily",
                    adjust="qfq",
                    start_date=(datetime.now() - timedelta(days=days*2)).strftime('%Y%m%d'),
                    end_date=datetime.now().strftime('%Y%m%d')
                )
                
                if df is not None and not df.empty:
                    # 筛选日期范围
                    cutoff = datetime.now() - timedelta(days=days)
                    df['日期'] = pd.to_datetime(df['日期'])
                    df = df[df['日期'] >= cutoff]
                    df = df.set_index('日期')
                    
                    # 标准化列名
                    df = df.rename(columns={
                        '开盘': 'open',
                        '收盘': 'close',
                        '最高': 'high',
                        '最低': 'low',
                        '成交量': 'volume'
                    })
                    
                    return df[['open', 'high', 'low', 'close', 'volume']]
                    
            except Exception as e:
                if attempt < 2:
                    time.sleep(0.5)
                    continue
                print(f"Akshare东方财富接口失败: {e}")
        
        return None
    
    def _fetch_via_sina(self, code: str, period: str) -> Optional[pd.DataFrame]:
        """通过新浪接口（备用）"""
        from datetime import timedelta
        
        try:
            df = self.ak.stock_zh_a_daily(symbol=f"sh{code}" if code.startswith('6') else f"sz{code}", adjust="qfq")
            
            if df is not None and not df.empty:
                period_days = {'1mo': 30, '3mo': 90, '6mo': 180, '1y': 365}
                days = period_days.get(period, 180)
                cutoff = datetime.now() - timedelta(days=days)
                
                df = df.reset_index()
                # 新浪接口日期列可能叫 'date' 或 '日期'
                date_col = 'date' if 'date' in df.columns else '日期'
                df[date_col] = pd.to_datetime(df[date_col])
                df = df[df[date_col] >= cutoff]
                df = df.set_index(date_col)
                
                return df[['open', 'high', 'low', 'close', 'volume']]
        except Exception as e:
            print(f"Akshare新浪接口失败: {e}")
        
        return None


class ZhipuSource(DataSource):
    """智谱搜索数据源 (优先级4) - 通过MCP"""
    
    def __init__(self):
        super().__init__("智谱搜索")
        self.priority = 4
    
    def is_available(self) -> bool:
        # 检查 mcporter 命令是否可用
        try:
            import subprocess
            result = subprocess.run(['mcporter', '--help'], capture_output=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        # 智谱搜索主要用于资讯搜索，不适合获取技术指标数据
        # 这里返回 None，让 fallback 机制继续
        return None


class TavilySource(DataSource):
    """Tavily搜索数据源 (优先级5) - 通过本地脚本"""
    
    def __init__(self):
        super().__init__("Tavily搜索")
        self.priority = 5
    
    def is_available(self) -> bool:
        # 检查 Tavily 脚本是否存在
        tavily_path = Path(__file__).parent.parent.parent / "tavily-search-1.0.0" / "scripts" / "search.mjs"
        return tavily_path.exists()
    
    def fetch(self, symbol: str, period: str = "6mo") -> Optional[pd.DataFrame]:
        # Tavily 主要用于资讯搜索，不适合获取技术指标数据
        # 这里返回 None，让 fallback 机制继续
        return None


class DataSourceManager:
    """Unified Data Source Manager with automatic fallback"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.metrics = DataSourceMetrics()
        self.api_key = api_key
        
        # Initialize all data sources (no API key required)
        self.sources: List[DataSource] = [
            SinaSource(),
            EastMoneySource(),
            AkshareSource(),
            ZhipuSource(),
            TavilySource()
        ]
        
        # Sort by priority
        self.sources.sort(key=lambda s: s.priority)
    
    def fetch_with_fallback(self, symbol: str, period: str = "6mo") -> Tuple[Optional[pd.DataFrame], str]:
        """
        使用 fallback 机制获取数据
        :return: (DataFrame, source_name)
        """
        for source in self.sources:
            if not source.is_available():
                continue
            
            start_time = time.time()
            
            try:
                df = source.fetch(symbol, period)
                response_time = time.time() - start_time
                
                if df is not None and not df.empty:
                    # 记录成功
                    self.metrics.record(source.name, True, response_time)
                    try:
                        print(f"[OK] 数据来源: {source.name} (耗时: {response_time:.2f}秒)")
                    except UnicodeEncodeError:
                        print(f"[OK] Data source: {source.name} (Time: {response_time:.2f}s)")
                    return df, source.name
                    
            except Exception as e:
                response_time = time.time() - start_time
                # 记录失败
                self.metrics.record(source.name, False, response_time)
                try:
                    print(f"[WARN] {source.name} 失败: {e}")
                except UnicodeEncodeError:
                    print(f"[WARN] {source.name} failed: {e}")
                continue
        
        try:
            print("[FAIL] 所有数据源均获取失败")
        except UnicodeEncodeError:
            print("[FAIL] All data sources failed")
        return None, ""
    
    def get_source_stats(self) -> Dict[str, Any]:
        """获取所有数据源的统计信息"""
        stats = {}
        for source in self.sources:
            stats[source.name] = {
                'priority': source.priority,
                'available': source.is_available(),
                **self.metrics.get_stats(source.name)
            }
        return stats
    
    def print_stats(self):
        """打印数据源统计信息"""
        stats = self.get_source_stats()
        try:
            print("\n[STATS] 数据源性能统计:")
        except UnicodeEncodeError:
            print("\n[STATS] Data Source Performance:")
        print("-" * 80)
        print(f"{'数据源':<15} {'优先级':<8} {'可用':<6} {'调用次数':<10} {'成功率':<10} {'平均响应时间'}")
        print("-" * 80)
        
        for source_name, data in stats.items():
            available_mark = "[OK]" if data['available'] else "[FAIL]"
            print(f"{source_name:<15} {data['priority']:<8} {available_mark:<6} "
                  f"{data['total_calls']:<10} {data['success_rate']:.1f}%{'':<5} "
                  f"{data['avg_response_time']:.2f}秒")
        
        print("-" * 80)


def main():
    """测试入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='统一数据源管理器')
    parser.add_argument('symbol', help='股票代码')
    parser.add_argument('--period', default='6mo', help='数据周期')
    parser.add_argument('--stats', action='store_true', help='显示数据源统计')
    
    args = parser.parse_args()
    
    manager = DataSourceManager()
    
    if args.stats:
        manager.print_stats()
        return
    
    print(f"🔍 获取 {args.symbol} 数据 (周期: {args.period})...\n")
    
    df, source_name = manager.fetch_with_fallback(args.symbol, args.period)
    
    if df is not None:
        print(f"\n✅ 成功获取数据")
        print(f"数据源: {source_name}")
        print(f"数据量: {len(df)} 条")
        print(f"\n最新5条数据:")
        print(df.tail())
    else:
        print("\n❌ 获取数据失败")
    
    # 显示统计
    manager.print_stats()


if __name__ == '__main__':
    main()
