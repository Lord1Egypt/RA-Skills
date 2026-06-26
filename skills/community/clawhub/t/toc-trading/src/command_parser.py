"""
TOC Trading System - 命令解析器
"""
import re
from typing import Dict, Optional, Tuple, List
from enum import Enum

class CommandType(Enum):
    """命令类型"""
    ADD_STOCK = "add_stock"
    REMOVE_STOCK = "remove_stock"
    LIST_STOCKS = "list_stocks"
    SEARCH_STOCK = "search_stock"
    BUY = "buy"
    SELL = "sell"
    POSITIONS = "positions"
    TRADES = "trades"
    DRILL = "drill"
    RECOMMEND = "recommend"
    HOT_SIGNALS = "hot_signals"
    DAILY_STOCK = "daily_stock"
    START_CHALLENGE = "start_challenge"
    END_CHALLENGE = "end_challenge"
    CHALLENGE_STATUS = "challenge_status"
    CHALLENGE_STATS = "challenge_stats"
    FOUR_INDUSTRIES = "four_industries"
    MARKET_SUMMARY = "market_summary"
    HELP = "help"
    UNKNOWN = "unknown"

class Parser:
    """命令解析器"""
    
    def __init__(self):
        self.patterns = {
            CommandType.ADD_STOCK: [
                r'加[一只个份几]+\s*(.+)',
                r'添加\s*(.+)',
                r'自选[中加]\s*(.+)',
            ],
            CommandType.REMOVE_STOCK: [
                r'^去掉\s+(.+)$',
                r'^删除\s+(.+)$',
                r'^移除\s+(.+)$',
            ],
            CommandType.LIST_STOCKS: [
                r'股票池',
                r'自选[股池]',
                r'看看?[股池]',
                r'我的[股池股票]',
            ],
            CommandType.SEARCH_STOCK: [
                r'搜索?\s*(.+)',
                r'查找?\s*(.+)',
                r'(.+)怎么[看不找]',
            ],
            CommandType.BUY: [
                r'买[入]?\s*(\d+)\s*手?\s*[@每]\s*([\d.]+)\s*(?:元)?\s*(.*)',
                r'买[入]?\s*(.+)\s*(\d+)\s*手?\s*[@每]\s*([\d.]+)',
                r'买入\s*(.+?)\s*(\d+)手\s*([\d.]+)',
            ],
            CommandType.SELL: [
                r'卖[出]?\s*(\d+)?\s*手?\s*(.+)',
                r'清仓\s*(.+)',
            ],
            CommandType.POSITIONS: [
                r'持仓',
                r'我的持仓',
                r'当前[持仓仓位]',
            ],
            CommandType.TRADES: [
                r'交易记录',
                r'历史交易',
                r'成交记录',
            ],
            CommandType.DRILL: [
                r'如果[在是]?(.+)买入',
                r'昨天[开盘]?买[入]?\s*(.+)',
                r'(.+)赚多少',
                r'持有(.+)赚',
                r'(.+)涨[了多少]?',
            ],
            CommandType.RECOMMEND: [
                r'推荐[一三支只个票股]+',
                r'有什么好股',
                r'买什么好',
            ],
            CommandType.HOT_SIGNALS: [
                r'有什么消息',
                r'市场[动态热点]',
                r'今日信号',
            ],
            CommandType.DAILY_STOCK: [
                r'今日金股',
                r'每天[推荐一]只',
            ],
            CommandType.START_CHALLENGE: [
                r'开启?挑战',
                r'开始挑战',
                r'参加挑战',
            ],
            CommandType.END_CHALLENGE: [
                r'结束挑战',
                r'停止挑战',
            ],
            CommandType.CHALLENGE_STATUS: [
                r'挑战状态',
                r'我的挑战',
                r'当前挑战',
            ],
            CommandType.CHALLENGE_STATS: [
                r'挑战统计',
                r'挑战记录',
            ],
            CommandType.FOUR_INDUSTRIES: [
                r'四大行业',
                r'行业分析',
                r'AI.*消费品.*汽车.*医疗',
                r'看看行业',
            ],
            CommandType.MARKET_SUMMARY: [
                r'市场概况',
                r'大盘',
                r'整体市场',
            ],
            CommandType.HELP: [
                r'帮助',
                r'怎么用',
                r'help',
                r'命令',
            ],
        }
    
    def parse(self, text: str) -> Tuple[CommandType, Dict]:
        """
        解析命令
        Returns: (command_type, params)
        """
        text = text.strip()
        
        for cmd_type, patterns in self.patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    params = self._extract_params(cmd_type, match, text)
                    return cmd_type, params
        
        return CommandType.UNKNOWN, {'original': text}
    
    def _extract_params(self, cmd_type: CommandType, match: re.Match, text: str) -> Dict:
        """提取命令参数"""
        params = {}
        groups = match.groups()
        
        if cmd_type == CommandType.ADD_STOCK:
            params['stock_name'] = groups[0].strip() if groups else ''
            # 提取推荐理由
            reason_match = re.search(r'理由[是为]*(.+)', text)
            if reason_match:
                params['reason'] = reason_match.group(1)
            # 提取备注
            remark_match = re.search(r'备注[是为]*(.+)', text)
            if remark_match:
                params['remark'] = remark_match.group(1)
        
        elif cmd_type == CommandType.REMOVE_STOCK:
            params['stock_name'] = groups[0].strip() if groups else ''
            # 去掉"招商银行" -> "招商银行"
            if params['stock_name'].startswith('去掉'):
                params['stock_name'] = params['stock_name'][2:].strip()
            elif params['stock_name'].startswith('删除'):
                params['stock_name'] = params['stock_name'][2:].strip()
            elif params['stock_name'].startswith('移除'):
                params['stock_name'] = params['stock_name'][2:].strip()
        
        elif cmd_type == CommandType.SEARCH_STOCK:
            params['keyword'] = groups[0].strip() if groups else ''
        
        elif cmd_type == CommandType.BUY:
            if len(groups) >= 3:
                # 格式: 买 100 手 @ 15.6 元 招商银行
                params['quantity'] = int(groups[0]) if groups[0].isdigit() else 0
                params['price'] = float(groups[1]) if groups[1].replace('.','').isdigit() else 0
                params['stock_name'] = groups[2].strip() if len(groups) > 2 else ''
            else:
                params['stock_name'] = groups[0].strip() if groups else ''
                params['quantity'] = 100  # 默认100手
        
        elif cmd_type == CommandType.SELL:
            if groups[0] and groups[0].isdigit():
                params['quantity'] = int(groups[0])
                params['stock_name'] = groups[1].strip() if len(groups) > 1 else ''
            else:
                params['stock_name'] = groups[0].strip() if groups else ''
        
        elif cmd_type == CommandType.DRILL:
            params['scenario'] = text
        
        elif cmd_type == CommandType.RECOMMEND:
            # 提取筛选条件
            if '低估值' in text:
                params['criteria'] = 'low_pe'
            elif '高ROE' in text or '高增长' in text:
                params['criteria'] = 'high_roe'
            elif '北向' in text or '外资' in text:
                params['criteria'] = 'hsgt'
        
        params['original'] = text
        return params