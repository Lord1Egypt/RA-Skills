# -*- coding: utf-8 -*-
"""
大盘复盘模块
获取 A股/美股 主要指数和市场概况
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入 akshare
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False


class MarketSummary:
    """大盘复盘数据类"""
    
    def __init__(self, market: str = 'cn'):
        self.market = market
    
    def get(self) -> Dict[str, Any]:
        """获取大盘数据"""
        if self.market == 'cn':
            return self._get_cn_market()
        elif self.market == 'us':
            return self._get_us_market()
        else:
            return {'error': f'不支持的市场: {self.market}'}
    
    def _get_cn_market(self) -> Dict[str, Any]:
        """获取A股大盘数据"""
        result = {
            'name': 'A股',
            'indices': [],
            'statistics': {},
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # 上证指数
            df = ak.index_zh_a_hist(symbol="000001", period="daily", start_date=self._get_trade_date(), end_date=self._get_trade_date())
            if not df.empty:
                latest = df.iloc[-1]
                result['indices'].append({
                    'name': '上证指数',
                    'code': '000001',
                    'close': float(latest['收盘']),
                    'change': float(latest['涨跌幅']),
                    'volume': float(latest['成交量']),
                    'amount': float(latest['成交额'])
                })
        except Exception as e:
            logger.warning(f"上证指数获取失败: {e}")
        
        try:
            # 深证成指
            df = ak.index_zh_a_hist(symbol="399001", period="daily", start_date=self._get_trade_date(), end_date=self._get_trade_date())
            if not df.empty:
                latest = df.iloc[-1]
                result['indices'].append({
                    'name': '深证成指',
                    'code': '399001',
                    'close': float(latest['收盘']),
                    'change': float(latest['涨跌幅']),
                    'volume': float(latest['成交量'])
                })
        except Exception as e:
            logger.warning(f"深证成指获取失败: {e}")
        
        try:
            # 创业板指
            df = ak.index_zh_a_hist(symbol="399006", period="daily", start_date=self._get_trade_date(), end_date=self._get_trade_date())
            if not df.empty:
                latest = df.iloc[-1]
                result['indices'].append({
                    'name': '创业板指',
                    'code': '399006',
                    'close': float(latest['收盘']),
                    'change': float(latest['涨跌幅']),
                    'volume': float(latest['成交量'])
                })
        except Exception as e:
            logger.warning(f"创业板指获取失败: {e}")
        
        try:
            # 市场统计 (涨跌停)
            df = ak.stock_zt_pool_subordinate(start_date=self._get_trade_date(), end_date=self._get_trade_date())
            if not df.empty:
                # 简化统计
                result['statistics']['涨停'] = len(df)
                result['statistics']['跌停'] = 0  # 需要单独查询
        except Exception as e:
            logger.warning(f"涨跌停统计获取失败: {e}")
        
        return result
    
    def _get_us_market(self) -> Dict[str, Any]:
        """获取美股大盘数据"""
        result = {
            'name': '美股',
            'indices': [],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            # 道琼斯
            df = ak.macro_us_market()
            if not df.empty:
                for _, row in df.iterrows():
                    name = row.get('Index', '')
                    if 'Dow' in name or 'DJI' in name:
                        result['indices'].append({
                            'name': '道琼斯',
                            'code': 'DJI',
                            'close': row.get('Last', 0),
                            'change': row.get('Change', 0)
                        })
                    elif 'NASDAQ' in name or 'IXIC' in name:
                        result['indices'].append({
                            'name': '纳斯达克',
                            'code': 'IXIC',
                            'close': row.get('Last', 0),
                            'change': row.get('Change', 0)
                        })
                    elif 'S&P' in name or 'SPX' in name:
                        result['indices'].append({
                            'name': '标普500',
                            'code': 'SPX',
                            'close': row.get('Last', 0),
                            'change': row.get('Change', 0)
                        })
        except Exception as e:
            logger.warning(f"美股指数获取失败: {e}")
        
        # 如果上面失败，尝试 yfinance
        if not result['indices']:
            try:
                import yfinance as yf
                
                tickers = ['^DJI', '^IXIC', '^GSPC']
                names = ['道琼斯', '纳斯达克', '标普500']
                
                for ticker, name in zip(tickers, names):
                    data = yf.Ticker(ticker).history(period="1d")
                    if not data.empty:
                        latest = data.iloc[-1]
                        result['indices'].append({
                            'name': name,
                            'code': ticker,
                            'close': round(latest['Close'], 2),
                            'change': round(((latest['Close'] - latest['Open']) / latest['Open'] * 100), 2)
                        })
            except Exception as e:
                logger.warning(f"yfinance 获取失败: {e}")
        
        return result
    
    def _get_trade_date(self) -> str:
        """获取最近交易日"""
        from datetime import timedelta
        today = datetime.now()
        
        # 简单逻辑: 工作日
        for i in range(5):
            check_date = today - timedelta(days=i)
            if check_date.weekday() < 5:
                return check_date.strftime('%Y%m%d')
        
        return today.strftime('%Y%m%d')


def get_market_summary(market: str = 'cn') -> Dict[str, Any]:
    """
    获取大盘复盘数据
    
    Args:
        market: 'cn' / 'us' / 'both'
        
    Returns:
        大盘数据
    """
    if not HAS_AKSHARE:
        return {'error': 'akshare 未安装'}
    
    summary = MarketSummary(market)
    return summary.get()


def format_market_report(market_data: Dict[str, Any]) -> str:
    """格式化大盘报告"""
    lines = []
    
    if 'cn' in market_data:
        cn = market_data['cn']
        lines.append("📊 A股市场")
        
        for idx in cn.get('indices', []):
            change = idx.get('change', 0)
            emoji = '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
            lines.append(f"  {idx['name']}: {idx.get('close', '-')} ({emoji}{change:+.2f}%)")
        
        lines.append("")
    
    if 'us' in market_data:
        us = market_data['us']
        lines.append("📊 美股市场")
        
        for idx in us.get('indices', []):
            change = idx.get('change', 0)
            emoji = '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
            lines.append(f"  {idx['name']}: {idx.get('close', '-')} ({emoji}{change:+.2f}%)")
        
        lines.append("")
    
    return '\n'.join(lines)
