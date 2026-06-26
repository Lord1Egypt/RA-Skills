# -*- coding: utf-8 -*-
"""
板块分析模块
获取行业/概念板块涨跌排行
"""

import logging
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

# 尝试导入 akshare
try:
    import akshare as ak
    HAS_AKSHARE = True
except ImportError:
    HAS_AKSHARE = False


class SectorAnalyzer:
    """板块分析器"""
    
    def __init__(self):
        pass
    
    def get_performance(self) -> List[Dict[str, Any]]:
        """获取板块涨跌排行"""
        sectors = []
        
        # 尝试获取行业板块
        try:
            df = ak.sector_stock_rank(indicator="今日涨幅", sector_type="行业板块")
            if not df.empty:
                for i, row in df.head(10).iterrows():
                    sectors.append({
                        'name': row.get('板块名称', ''),
                        'change': row.get('今日涨跌幅', 0),
                        'type': 'industry'
                    })
        except Exception as e:
            logger.warning(f"行业板块获取失败: {e}")
        
        # 尝试获取概念板块
        try:
            df = ak.sector_stock_rank(indicator="今日涨幅", sector_type="概念板块")
            if not df.empty:
                for i, row in df.head(10).iterrows():
                    sectors.append({
                        'name': row.get('板块名称', ''),
                        'change': row.get('今日涨跌幅', 0),
                        'type': 'concept'
                    })
        except Exception as e:
            logger.warning(f"概念板块获取失败: {e}")
        
        return sectors
    
    def get_hot_sectors(self, limit: int = 5) -> List[Dict[str, Any]]:
        """获取热门板块"""
        try:
            # 东方财富热榜
            df = ak.sector_fund_flow_rank(indicator="今日", sector_type="行业资金流")
            
            if not df.empty:
                hot = []
                for i, row in df.head(limit).iterrows():
                    hot.append({
                        'name': row.get('名称', ''),
                        'inflow': row.get('今日涨跌幅', 0),  # 这里实际是资金流入
                        'change': 0  # 需要关联行情
                    })
                return hot
        except Exception as e:
            logger.warning(f"热门板块获取失败: {e}")
        
        return []


def get_sector_performance() -> List[Dict[str, Any]]:
    """
    获取板块表现
    
    Returns:
        板块涨跌列表
    """
    if not HAS_AKSHARE:
        return [{'error': 'akshare 未安装'}]
    
    analyzer = SectorAnalyzer()
    return analyzer.get_performance()


def format_sector_report(sectors: List[Dict[str, Any]]) -> str:
    """格式化板块报告"""
    if not sectors:
        return "暂无板块数据"
    
    lines = ["🔥 板块涨跌榜", ""]
    
    # 分类显示
    industry = [s for s in sectors if s.get('type') == 'industry']
    concept = [s for s in sectors if s.get('type') == 'concept']
    
    if industry:
        lines.append("🏭 行业板块 Top10:")
        for s in industry[:10]:
            change = s.get('change', 0)
            emoji = '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
            lines.append(f"  {s.get('name', '')} {emoji}{change:+.2f}%")
        lines.append("")
    
    if concept:
        lines.append("💡 概念板块 Top10:")
        for s in concept[:10]:
            change = s.get('change', 0)
            emoji = '🟢' if change > 0 else '🔴' if change < 0 else '⚪'
            lines.append(f"  {s.get('name', '')} {emoji}{change:+.2f}%")
    
    return '\n'.join(lines)
