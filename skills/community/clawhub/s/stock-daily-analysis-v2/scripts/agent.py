# -*- coding: utf-8 -*-
"""
Agent 问股模块 (简化版)
支持多轮策略问答
"""

import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class StockAgent:
    """股票问答 Agent"""
    
    # 内置策略模板
    STRATEGIES = {
        'bull_trend': {
            'name': '多头趋势',
            'description': 'MA5 > MA10 > MA20 的多头排列股票',
            'rules': ['MA5 > MA10', 'MA10 > MA20', '股价 > MA20']
        },
        'golden_cross': {
            'name': '均线金叉',
            'description': '短期均线上穿长期均线的股票',
            'rules': ['MA5 上穿 MA10', '成交量放大']
        },
        'breakout': {
            'name': '突破新高',
            'description': '突破近期高点的股票',
            'rules': ['收盘价 > 20日最高价', '成交量 > 20日平均']
        },
        'value': {
            'name': '价值投资',
            'description': '低估值、高分红的股票',
            'rules': ['PE < 20', 'PB < 3', '股息率 > 2%']
        },
        'momentum': {
            'name': '动量策略',
            'description': '近期涨幅靠前的股票',
            'rules': ['20日涨幅前20%', '成交量活跃']
        }
    }
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.api_key = config.get('api_key', '')
        self.provider = config.get('provider', 'openai')
        self.model = config.get('model', 'deepseek-chat')
        self.base_url = config.get('base_url', 'https://api.deepseek.com/v1')
        self.conversation_history = []
    
    def answer(self, question: str, stocks: List[str] = None) -> Dict[str, Any]:
        """
        回答股票相关问题
        
        Args:
            question: 用户问题
            stocks: 自选股列表
            
        Returns:
            回答结果
        """
        logger.info(f"Agent 收到问题: {question}")
        
        # 简单的意图识别
        intent = self._recognize_intent(question)
        
        # 构建回答
        if intent == 'recommend':
            return self._recommend_stocks(question, stocks)
        elif intent == 'analyze':
            return self._analyze_stock(question, stocks)
        elif intent == 'strategy':
            return self._explain_strategy(question)
        elif intent == 'general':
            return self._general_answer(question)
        else:
            return {
                'intent': intent,
                'answer': '我理解您的问题，让我为您分析...',
                'suggestion': '您可以问我:\n- "推荐银行股"\n- "分析一下茅台"\n- "什么是均线金叉"\n- "帮我选一只新能源股票"'
            }
    
    def _recognize_intent(self, question: str) -> str:
        """识别问题意图"""
        q = question.lower()
        
        if any(kw in q for kw in ['推荐', '帮我选', '有什么', '哪个好']):
            return 'recommend'
        elif any(kw in q for kw in ['分析', '怎么看', '走势', '买卖点']):
            return 'analyze'
        elif any(kw in q for kw in ['策略', '什么是', '解释', '怎么选']):
            return 'strategy'
        else:
            return 'general'
    
    def _recommend_stocks(self, question: str, stocks: List[str]) -> Dict[str, Any]:
        """推荐股票"""
        # 提取关键词
        sector_keywords = {
            '新能源': ['宁德时代', '比亚迪', '隆基绿能', '通威股份'],
            '银行': ['招商银行', '工商银行', '建设银行', '平安银行'],
            '科技': ['腾讯控股', '阿里巴巴', '美团', '小米集团'],
            '医药': ['恒瑞医药', '药明康德', '迈瑞医疗', '云南白药'],
            '消费': ['贵州茅台', '五粮液', '海天味业', '伊利股份'],
            '地产': ['万科A', '保利地产', '招商蛇口'],
            '军工': ['中航沈飞', '航发动力', '中国卫通']
        }
        
        found_sector = None
        for sector, _ in sector_keywords.items():
            if sector in question:
                found_sector = sector
                break
        
        if found_sector:
            recommendations = sector_keywords.get(found_sector, [])
            return {
                'intent': 'recommend',
                'sector': found_sector,
                'answer': f"根据您的要求，推荐 {found_sector} 板块:",
                'stocks': recommendations,
                'strategy': '建议关注行业龙头和基本面良好的标的'
            }
        
        # 默认推荐
        return {
            'intent': 'recommend',
            'answer': '请告诉我您关注的行业板块，比如: 新能源、银行、科技、医药等',
            'sectors': list(sector_keywords.keys())
        }
    
    def _analyze_stock(self, question: str, stocks: List[str]) -> Dict[str, Any]:
        """分析股票"""
        # 提取股票代码
        import re
        codes = re.findall(r'\b\d{6}\b', question)
        
        if codes:
            return {
                'intent': 'analyze',
                'codes': codes,
                'answer': f'我将分析股票: {", ".join(codes)}',
                'note': '使用 analyze_stock() 函数进行详细分析'
            }
        
        return {
            'intent': 'analyze',
            'answer': '请提供股票代码，例如: "分析 600519"',
            'example': '600519, 000858, AAPL'
        }
    
    def _explain_strategy(self, question: str) -> Dict[str, Any]:
        """解释策略"""
        q = question.lower()
        
        for strategy_id, strategy in self.STRATEGIES.items():
            if strategy_id in q or strategy['name'] in q:
                return {
                    'intent': 'strategy',
                    'strategy_id': strategy_id,
                    'name': strategy['name'],
                    'description': strategy['description'],
                    'rules': strategy['rules']
                }
        
        # 列出所有策略
        return {
            'intent': 'strategy',
            'answer': '以下是内置的选股策略:',
            'strategies': [
                {'id': k, 'name': v['name'], 'description': v['description']}
                for k, v in self.STRATEGIES.items()
            ]
        }
    
    def _general_answer(self, question: str) -> Dict[str, Any]:
        """通用问答"""
        # 简单规则匹配
        if '好' in question or '怎么样' in question:
            return {
                'intent': 'general',
                'answer': '股市有风险，投资需谨慎。建议您关注基本面和技术面结合的分析。',
                'tip': '可以尝试: "推荐银行股" 或 "分析 600519"'
            }
        
        return {
            'intent': 'general',
            'answer': '我是一个股票分析助手，可以帮您:',
            'capabilities': [
                '分析股票 (输入代码)',
                '推荐板块 (指定行业)',
                '解释策略 (均线金叉、多头排列等)',
                '大盘复盘',
                '板块分析'
            ]
        }


def create_agent(config: Dict[str, Any] = None) -> StockAgent:
    """创建 Agent 实例"""
    return StockAgent(config or {})
