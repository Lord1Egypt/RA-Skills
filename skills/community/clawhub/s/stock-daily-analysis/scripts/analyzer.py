# -*- coding: utf-8 -*-
"""
股票每日分析 - 主入口模块

整合数据获取、技术分析和报告生成
提供简单的调用接口
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from pathlib import Path

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入模块
from scripts.data_fetcher import get_daily_data, get_realtime_quote, get_stock_name
from scripts.trend_analyzer import StockTrendAnalyzer
from scripts.ai_analyzer import AIAnalyzer
from scripts.notifier import AnalysisReport, format_analysis_report, format_dashboard_report


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """加载配置文件"""
    if config_path is None:
        skill_dir = Path(__file__).parent.parent
        config_path = skill_dir / "config.json"
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"加载配置文件失败: {e}，使用默认配置")
        return {
            "data": {"days": 60, "realtime_enabled": True},
            "analysis": {"bias_threshold": 5.0}
        }


def analyze_stock(code: str, config: Optional[Dict] = None) -> Dict[str, Any]:
    """
    分析单只股票
    
    Args:
        code: 股票代码 (如 '600519', 'AAPL', '00700')
        config: 配置字典，可选
        
    Returns:
        包含技术分析结果的字典
    """
    if config is None:
        config = load_config()
    
    logger.info(f"开始分析股票: {code}")
    
    # 获取股票名称
    name = get_stock_name(code)
    
    # 获取历史数据
    days = config.get('data', {}).get('days', 60)
    df = get_daily_data(code, days=days)
    
    if df is None or df.empty:
        logger.error(f"无法获取 {code} 的数据")
        return {
            'code': code,
            'name': name,
            'error': '数据获取失败',
            'technical_indicators': {},
            'ai_analysis': {'operation_advice': '数据不足', 'sentiment_score': 0}
        }
    
    # 技术分析
    analyzer = StockTrendAnalyzer()
    trend_result = analyzer.analyze(df, code)
    
    # 获取实时行情
    quote = get_realtime_quote(code)
    if quote:
        name = quote.name or name
    
    # AI 深度分析
    ai_config = config.get('ai', {})
    ai_analyzer = AIAnalyzer(ai_config)
    ai_result = ai_analyzer.analyze(code, name, trend_result.to_dict())
    
    # 整合结果
    result = {
        'code': code,
        'name': name,
        'technical_indicators': trend_result.to_dict(),
        'ai_analysis': ai_result
    }
    
    logger.info(f"{code} 分析完成，评分: {ai_result.get('sentiment_score', trend_result.signal_score)}")
    return result


def analyze_stocks(codes: List[str], config: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """
    分析多只股票
    
    Args:
        codes: 股票代码列表
        config: 配置字典，可选
        
    Returns:
        分析结果列表
    """
    results = []
    for code in codes:
        try:
            result = analyze_stock(code, config)
            results.append(result)
        except Exception as e:
            logger.error(f"分析 {code} 时出错: {e}")
            results.append({
                'code': code,
                'name': code,
                'error': str(e),
                'ai_analysis': {'operation_advice': '分析失败', 'sentiment_score': 0}
            })
    
    return results


def print_analysis(codes: List[str]) -> None:
    """
    分析股票并打印报告
    
    Args:
        codes: 股票代码列表
    """
    results = analyze_stocks(codes)
    
    # 转换为报告格式并打印
    reports = []
    for result in results:
        if 'error' not in result:
            from scripts.notifier import create_report_from_result
            report = create_report_from_result(result)
            reports.append(report)
    
    if reports:
        print("\n" + format_dashboard_report(reports))
        
        # 打印每个股票的详细报告
        for report in reports:
            print("\n" + format_analysis_report(report))
    else:
        print("没有可显示的报告")


# 便捷函数
if __name__ == "__main__":
    # 测试
    print("=== 股票每日分析系统 ===\n")
    print("正在测试分析茅台 (600519)...\n")
    print_analysis(['600519'])
