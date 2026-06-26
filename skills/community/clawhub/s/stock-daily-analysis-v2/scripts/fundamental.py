# -*- coding: utf-8 -*-
"""
基本面分析模块
基于 AkShare 获取财务数据、估值、机构持仓等信息
"""

import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

# 尝试导入 akshare
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False
    logger.warning("akshare 未安装，基本面分析功能受限")


class FundamentalAnalyzer:
    """基本面分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
    
    def analyze(self, code: str) -> Dict[str, Any]:
        """
        获取股票基本面数据
        
        Args:
            code: 股票代码
            
        Returns:
            基本面数据字典
        """
        if not HAS_AKSHARE:
            return {'error': 'akshare 未安装'}
        
        result = {
            'code': code,
            'valuation': {},
            'earnings': {},
            'growth': {},
            'institution': {},
            'capital_flow': {}
        }
        
        try:
            # 估值数据
            result['valuation'] = self._get_valuation(code)
        except Exception as e:
            logger.warning(f"估值数据获取失败: {e}")
        
        try:
            # 盈利数据
            result['earnings'] = self._get_earnings(code)
        except Exception as e:
            logger.warning(f"盈利数据获取失败: {e}")
        
        try:
            # 成长性数据
            result['growth'] = self._get_growth(code)
        except Exception as e:
            logger.warning(f"成长性数据获取失败: {e}")
        
        try:
            # 机构持仓
            result['institution'] = self._get_institution_holder(code)
        except Exception as e:
            logger.warning(f"机构持仓获取失败: {e}")
        
        try:
            # 资金流向
            result['capital_flow'] = self._get_capital_flow(code)
        except Exception as e:
            logger.warning(f"资金流向获取失败: {e}")
        
        return result
    
    def _get_valuation(self, code: str) -> Dict[str, Any]:
        """获取估值数据"""
        # 统一股票代码格式
        symbol = self._format_code(code)
        
        try:
            # 市盈率、市净率
            df = ak.stock_individual_info_em(symbol=symbol)
            
            valuation = {}
            for _, row in df.iterrows():
                item = row.get('item', '')
                value = row.get('value', '')
                
                if '市盈率' in item:
                    valuation['pe'] = value
                elif '市净率' in item:
                    valuation['pb'] = value
                elif '总市值' in item:
                    valuation['market_cap'] = value
                elif '流通市值' in item:
                    valuation['float_cap'] = value
                elif '股息率' in item:
                    valuation['dividend_yield'] = value
            
            return valuation
        except Exception as e:
            logger.debug(f"估值数据获取失败: {e}")
            return {}
    
    def _get_earnings(self, code: str) -> Dict[str, Any]:
        """获取盈利数据"""
        # 简化的盈利数据
        return {
            'report_date': '最新财报',
            'note': '需配置 Tushare Token 获取详细数据'
        }
    
    def _get_growth(self, code: str) -> Dict[str, Any]:
        """获取成长性数据"""
        return {
            'note': '需配置 Tushare Token 获取详细数据'
        }
    
    def _get_institution_holder(self, code: str) -> Dict[str, Any]:
        """获取机构持仓"""
        return {
            'note': '需配置 Tushare Token 获取详细数据'
        }
    
    def _get_capital_flow(self, code: str) -> Dict[str, Any]:
        """获取资金流向"""
        symbol = self._format_code(code)
        
        try:
            # 主力资金流向
            df = ak.stock_individual_fund_flow(stock=symbol, market='sh')
            
            if not df.empty:
                latest = df.iloc[0]
                return {
                    'main_inflow': str(latest.get('主力净流入', 0)),
                    'main_inflow_rate': str(latest.get('主力净流入占比', 0)),
                    'super_inflow': str(latest.get('超大单净流入', 0)),
                    'large_inflow': str(latest.get('大单净流入', 0)),
                    'medium_inflow': str(latest.get('中单净流入', 0)),
                    'small_inflow': str(latest.get('小单净流入', 0))
                }
        except Exception as e:
            logger.debug(f"资金流向获取失败: {e}")
        
        return {}
    
    def _format_code(self, code: str) -> str:
        """格式化股票代码"""
        code = str(code).strip()
        
        # A股
        if code.isdigit() and len(code) == 6:
            if code.startswith('6'):
                return f"sh{code}"
            elif code.startswith(('0', '3')):
                return f"sz{code}"
        
        return code


def get_fundamental_summary(code: str) -> str:
    """获取基本面摘要文本"""
    analyzer = FundamentalAnalyzer()
    data = analyzer.analyze(code)
    
    parts = []
    
    # 估值
    val = data.get('valuation', {})
    if val:
        pe = val.get('pe', '-')
        pb = val.get('pb', '-')
        parts.append(f"PE: {pe}, PB: {pb}")
    
    # 资金流向
    cf = data.get('capital_flow', {})
    if cf:
        inflow = cf.get('main_inflow', '-')
        parts.append(f"主力净流入: {inflow}")
    
    return ' | '.join(parts) if parts else '基本面数据获取中...'
