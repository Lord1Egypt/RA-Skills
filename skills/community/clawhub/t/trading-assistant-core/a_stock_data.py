#!/usr/bin/env python3
"""
A 股数据支持模块
A-Share Data Support

数据来源:
- 新浪财经 API (免费实时数据)
- 东方财富网 (备选)
"""

import os
import sys
import json
import urllib.request
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Security: Removed sys.path manipulation to prevent importing external packages.
# This module is self-contained and does not import from sibling directories.


class AStockDataFetcher:
    """A 股数据获取器"""
    
    def __init__(self):
        # A 股代码映射
        self.market_prefix = {
            'SH': 'sh',  # 上交所
            'SZ': 'sz',  # 深交所
        }
    
    def format_symbol(self, symbol: str) -> str:
        """
        格式化 A 股代码
        
        Args:
            symbol: 股票代码 (600000, 000001, 300750)
            
        Returns:
            格式化后的代码 (sh600000, sz000001)
        """
        symbol = str(symbol).strip()
        
        # 如果已经有前缀，直接返回
        if symbol.startswith('sh') or symbol.startswith('sz'):
            return symbol
        
        # 根据代码判断市场
        if symbol.startswith('6'):
            return f'sh{symbol}'
        elif symbol.startswith('0') or symbol.startswith('3'):
            return f'sz{symbol}'
        else:
            # 默认深交所
            return f'sz{symbol}'
    
    def get_realtime_quote(self, symbol: str) -> Optional[Dict]:
        """
        获取实时行情
        
        Args:
            symbol: 股票代码
            
        Returns:
            实时行情数据
        """
        formatted_symbol = self.format_symbol(symbol)
        
        # 检查缓存 (1 分钟)
        cached = api_cache.get('a_stock_quote', {'symbol': symbol})
        if cached:
            return cached
        
        try:
            # 新浪财经实时行情 API
            url = f"http://hq.sinajs.cn/list={formatted_symbol}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=10) as resp:
                content = resp.read().decode('gbk')
                
                # 解析数据
                # var hq_str_sh600000="浦发银行，10.50,10.48,10.47,10.51,10.46..."
                match = re.search(r'= "([^"]+)"', content)
                if not match:
                    return None
                
                data_str = match.group(1).split(',')
                
                if len(data_str) < 32:
                    return None
                
                result = {
                    'symbol': symbol,
                    'name': data_str[0],
                    'open': float(data_str[1]) if data_str[1] else 0,
                    'close': float(data_str[2]) if data_str[2] else 0,  # 昨收
                    'current': float(data_str[3]) if data_str[3] else 0,  # 现价
                    'high': float(data_str[4]) if data_str[4] else 0,
                    'low': float(data_str[5]) if data_str[5] else 0,
                    'bid': float(data_str[6]) if data_str[6] else 0,  # 买一价
                    'ask': float(data_str[7]) if data_str[7] else 0,  # 卖一价
                    'volume': int(data_str[8]) if data_str[8] else 0,  # 成交量 (手)
                    'amount': float(data_str[9]) if data_str[9] else 0,  # 成交额 (元)
                    'bid1_vol': int(data_str[10]) if data_str[10] else 0,
                    'bid1': float(data_str[11]) if data_str[11] else 0,
                    'bid2_vol': int(data_str[12]) if data_str[12] else 0,
                    'bid2': float(data_str[13]) if data_str[13] else 0,
                    'bid3_vol': int(data_str[14]) if data_str[14] else 0,
                    'bid3': float(data_str[15]) if data_str[15] else 0,
                    'bid4_vol': int(data_str[16]) if data_str[16] else 0,
                    'bid4': float(data_str[17]) if data_str[17] else 0,
                    'bid5_vol': int(data_str[18]) if data_str[18] else 0,
                    'bid5': float(data_str[19]) if data_str[19] else 0,
                    'ask1_vol': int(data_str[20]) if data_str[20] else 0,
                    'ask1': float(data_str[21]) if data_str[21] else 0,
                    'ask2_vol': int(data_str[22]) if data_str[22] else 0,
                    'ask2': float(data_str[23]) if data_str[23] else 0,
                    'ask3_vol': int(data_str[24]) if data_str[24] else 0,
                    'ask3': float(data_str[25]) if data_str[25] else 0,
                    'ask4_vol': int(data_str[26]) if data_str[26] else 0,
                    'ask4': float(data_str[27]) if data_str[27] else 0,
                    'ask5_vol': int(data_str[28]) if data_str[28] else 0,
                    'ask5': float(data_str[29]) if data_str[29] else 0,
                    'date': data_str[30] if len(data_str) > 30 else '',
                    'time': data_str[31] if len(data_str) > 31 else '',
                    'change': 0,
                    'change_percent': 0,
                }
                
                # 计算涨跌幅
                if result['close'] > 0:
                    result['change'] = result['current'] - result['close']
                    result['change_percent'] = (result['change'] / result['close']) * 100
                
                # 保存缓存 (1 分钟)
                api_cache.set('a_stock_quote', {'symbol': symbol}, result)
                
                return result
                
        except Exception as e:
            print(f"⚠️ 获取 A 股行情失败：{e}")
            return None
    
    def get_kline_data(self, symbol: str, days: int = 60) -> Optional[List[Dict]]:
        """
        获取 K 线数据
        
        Args:
            symbol: 股票代码
            days: 天数
            
        Returns:
            K 线数据列表
        """
        formatted_symbol = self.format_symbol(symbol)
        
        # 检查缓存
        cached = api_cache.get('a_stock_kline', {'symbol': symbol, 'days': days})
        if cached:
            return cached
        
        try:
            # 新浪财经 K 线 API (日线)
            # 格式：ma=5,10,20
            url = f"http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol={formatted_symbol}&scale=240&ma=5&datalen={days}"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode()
                data = json.loads(content)
                
                kline = []
                for item in data:
                    kline.append({
                        'datetime': item.get('day', ''),
                        'open': float(item.get('open', 0)),
                        'high': float(item.get('high', 0)),
                        'low': float(item.get('low', 0)),
                        'close': float(item.get('close', 0)),
                        'volume': int(item.get('volume', 0)),
                    })
                
                # 保存缓存
                api_cache.set('a_stock_kline', {'symbol': symbol, 'days': days}, kline)
                
                return kline
                
        except Exception as e:
            print(f"⚠️ 获取 A 股 K 线失败：{e}")
            return None
    
    def get_stock_list(self, market: str = 'all') -> List[Dict]:
        """
        获取股票列表
        
        Args:
            market: 市场 (SH, SZ, all)
            
        Returns:
            股票列表
        """
        # 简化实现：返回常见股票
        stock_list = {
            'SH': [
                {'symbol': '600000', 'name': '浦发银行'},
                {'symbol': '600036', 'name': '招商银行'},
                {'symbol': '600519', 'name': '贵州茅台'},
                {'symbol': '601318', 'name': '中国平安'},
                {'symbol': '601398', 'name': '工商银行'},
            ],
            'SZ': [
                {'symbol': '000001', 'name': '平安银行'},
                {'symbol': '000858', 'name': '五粮液'},
                {'symbol': '002594', 'name': '比亚迪'},
                {'symbol': '300750', 'name': '宁德时代'},
                {'symbol': '300059', 'name': '东方财富'},
            ]
        }
        
        if market == 'all':
            return stock_list['SH'] + stock_list['SZ']
        elif market in stock_list:
            return stock_list[market]
        else:
            return stock_list['SH'] + stock_list['SZ']
    
    def is_trading_time(self) -> bool:
        """
        判断是否在交易时间
        
        Returns:
            是否在交易时间
        """
        now = datetime.now()
        weekday = now.weekday()
        
        # 周末不交易
        if weekday >= 5:
            return False
        
        # 交易时间：9:30-11:30, 13:00-15:00 (北京时间 = UTC+8)
        hour = now.hour
        minute = now.minute
        
        # 转换为北京时间
        beijing_hour = (hour + 8) % 24
        
        if beijing_hour < 9 or beijing_hour >= 15:
            return False
        
        if beijing_hour == 9 and minute < 30:
            return False
        
        if beijing_hour == 11 and minute >= 30:
            if beijing_hour == 12 or (beijing_hour == 13 and minute < 0):
                return False
        
        return True
    
    def get_market_status(self) -> Dict:
        """
        获取市场状态
        
        Returns:
            市场状态信息
        """
        now = datetime.now()
        beijing_time = now + timedelta(hours=8)
        
        return {
            'is_trading': self.is_trading_time(),
            'current_time': beijing_time.strftime('%Y-%m-%d %H:%M:%S (北京时间)'),
            'next_open': '下一个交易日 9:30',
            'next_close': '今日 15:00' if self.is_trading_time() else '今日已收盘'
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='A 股数据查询')
    parser.add_argument('symbol', nargs='?', default='600519', help='股票代码')
    parser.add_argument('--kline', action='store_true', help='获取 K 线数据')
    parser.add_argument('--days', type=int, default=60, help='K 线天数')
    parser.add_argument('--list', action='store_true', help='获取股票列表')
    parser.add_argument('--status', action='store_true', help='市场状态')
    
    args = parser.parse_args()
    
    fetcher = AStockDataFetcher()
    
    if args.status:
        status = fetcher.get_market_status()
        print(f"\n📊 A 股市场状态")
        print(f"   交易时间：{'是' if status['is_trading'] else '否'}")
        print(f"   当前时间：{status['current_time']}")
        print(f"   {status['next_close']}")
        return
    
    if args.list:
        stocks = fetcher.get_stock_list()
        print(f"\n📋 A 股股票列表 (部分)")
        for stock in stocks[:20]:
            print(f"   {stock['symbol']} - {stock['name']}")
        return
    
    if args.kline:
        kline = fetcher.get_kline_data(args.symbol, args.days)
        if kline:
            print(f"\n📈 {args.symbol} K 线数据 (近{args.days}天)")
            print(f"   共 {len(kline)} 条记录")
            if kline:
                latest = kline[-1]
                print(f"   最新：{latest['datetime']} O:{latest['open']} H:{latest['high']} L:{latest['low']} C:{latest['close']}")
        else:
            print("❌ 获取 K 线失败")
        return
    
    # 实时行情
    quote = fetcher.get_realtime_quote(args.symbol)
    if quote:
        print(f"\n📊 {quote['symbol']} - {quote['name']} 实时行情")
        print("=" * 50)
        print(f"   现价：¥{quote['current']:.2f}")
        print(f"   涨跌：{quote['change']:+.2f} ({quote['change_percent']:+.2f}%)")
        print(f"   今开：¥{quote['open']:.2f}")
        print(f"   昨收：¥{quote['close']:.2f}")
        print(f"   最高：¥{quote['high']:.2f}")
        print(f"   最低：¥{quote['low']:.2f}")
        print(f"   成交量：{quote['volume']:,} 手")
        print(f"   成交额：¥{quote['amount']/10000:.1f} 万")
        print(f"   买一：¥{quote['bid1']} x {quote['bid1_vol']}")
        print(f"   卖一：¥{quote['ask1']} x {quote['ask1_vol']}")
        print(f"   时间：{quote['date']} {quote['time']}")
        print("=" * 50)
    else:
        print("❌ 获取行情失败")


if __name__ == '__main__':
    main()
