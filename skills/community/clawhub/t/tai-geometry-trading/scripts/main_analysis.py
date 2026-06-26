#!/usr/bin/env python3
"""
太几何交易 - 综合股票分析主程序
整合几何结构、MACD风洞、缩量短线分析
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional
import json

from kline_geometry import analyze_geometry_structure
from macd_wind_tunnel import analyze_multi_period_macd, calculate_macd
from volume_shrinkage import analyze_multi_period_shrinkage


def get_dummy_data(period: str, n: int = 100) -> pd.DataFrame:
    """
    生成模拟数据用于测试
    实际使用时替换为真实数据获取
    """
    np.random.seed(42)
    
    if period == 'monthly':
        # 月线波动更大
        close = pd.Series(np.cumsum(np.random.randn(n) * 3 + 1) + 100)
    elif period == 'weekly':
        close = pd.Series(np.cumsum(np.random.randn(n) * 2 + 0.5) + 100)
    else:
        close = pd.Series(np.cumsum(np.random.randn(n) * 1 + 0.2) + 100)
    
    high = close + np.abs(np.random.randn(n) * close * 0.02)
    low = close - np.abs(np.random.randn(n) * close * 0.02)
    
    # 成交量
    base_volume = 1000000 if period == 'monthly' else (500000 if period == 'weekly' else 100000)
    volume = np.abs(np.random.randn(n) * base_volume * 0.3) + base_volume
    
    return pd.DataFrame({
        'open': close - np.abs(np.random.randn(n) * close * 0.01),
        'high': high,
        'low': low,
        'close': close,
        'volume': volume
    })


def analyze_stock(stock_code: str, data_dict: Optional[Dict[str, pd.DataFrame]] = None) -> Dict:
    """
    股票综合分析主函数
    
    Args:
        stock_code: 股票代码
        data_dict: 多周期数据 {'monthly': df, 'weekly': df, 'daily': df}
                   如果为None，使用模拟数据
    """
    
    # 如果没有提供数据，生成模拟数据
    if data_dict is None:
        data_dict = {
            'monthly': get_dummy_data('monthly'),
            'weekly': get_dummy_data('weekly'),
            'daily': get_dummy_data('daily')
        }
    
    result = {
        'stock_code': stock_code,
        'scores': {
            'geometry': 0,      # 几何结构 0-25
            'macd_wind': 0,    # MACD风洞 0-30
            'shrinkage': 0,    # 缩量短线 0-15
            'fundamental': 0,  # 基本面 0-10
            'sentiment': 0,    # 情绪面 0-10
            'ai_prediction': 0 # AI预测 0-10
        },
        'total_score': 0,      # 总分 0-100
        'details': {},
        'signals': [],
        'risk_warning': '',
        'recommendation': ''
    }
    
    # 1. 几何结构分析 (25分)
    if 'daily' in data_dict:
        geometry = analyze_geometry_structure(data_dict['daily'])
        result['scores']['geometry'] = geometry['total_score']
        result['details']['geometry'] = geometry
    
    # 2. MACD风洞共振分析 (30分)
    if 'monthly' in data_dict and 'weekly' in data_dict and 'daily' in data_dict:
        macd_analysis = analyze_multi_period_macd(data_dict)
        result['scores']['macd_wind'] = macd_analysis['resonance_score']
        result['details']['macd_wind'] = macd_analysis
    
    # 3. 缩量短线分析 (15分)
    shrinkage = analyze_multi_period_shrinkage(data_dict)
    result['scores']['shrinkage'] = shrinkage['total_score']
    result['details']['shrinkage'] = shrinkage
    
    # 4. 基本面分析 (10分)
    # 这里使用简化分析，实际应接入真实基本面数据
    result['scores']['fundamental'] = 6  # 模拟得分
    result['details']['fundamental'] = {
        'score': 6,
        'description': '基本面分析需要接入真实财务数据',
        'factors': ['PE处于合理区间', '营收稳定增长', '行业地位稳固']
    }
    
    # 5. 主流情绪分析 (10分)
    result['scores']['sentiment'] = 6  # 模拟得分
    result['details']['sentiment'] = {
        'score': 6,
        'description': '情绪分析需要接入实时市场数据',
        'factors': ['市场整体偏多', '板块资金净流入', '龙头股表现强势']
    }
    
    # 6. AI预测分析 (10分)
    result['scores']['ai_prediction'] = 6  # 模拟得分
    result['details']['ai_prediction'] = {
        'score': 6,
        'description': '基于技术面的AI预测分析',
        'factors': ['短期趋势偏多', '支撑位支撑有效', '突破概率较高']
    }
    
    # 计算总分
    result['total_score'] = sum(result['scores'].values())
    
    # 生成信号
    if result['scores']['macd_wind'] >= 20:
        result['signals'].append('MACD风洞结构共振强烈')
    elif result['scores']['macd_wind'] >= 10:
        result['signals'].append('MACD风洞结构偏多')
    
    if result['scores']['geometry'] >= 15:
        result['signals'].append('几何结构清晰')
    elif result['scores']['geometry'] >= 10:
        result['signals'].append('几何结构中性')
    
    if result['scores']['shrinkage'] >= 10:
        result['signals'].append('成交量收缩，面临方向选择')
    
    if result['scores']['fundamental'] >= 7:
        result['signals'].append('基本面良好')
    
    if result['scores']['sentiment'] >= 7:
        result['signals'].append('市场情绪偏暖')
    
    # 风险提示
    if result['total_score'] < 50:
        result['risk_warning'] = '综合评分较低，建议谨慎操作'
    elif result['total_score'] < 70:
        result['risk_warning'] = '存在不确定性，注意风险'
    else:
        result['risk_warning'] = '综合评分良好，但仍需关注市场风险'
    
    # 操作建议
    if result['total_score'] >= 70:
        if result['scores']['macd_wind'] >= 20:
            result['recommendation'] = '强烈看涨，可适当加仓，目标位XX，止损位XX'
        else:
            result['recommendation'] = '看涨，可适量买入'
    elif result['total_score'] >= 50:
        result['recommendation'] = '中性观望，等待更明确信号'
    else:
        result['recommendation'] = '看跌，建议观望或减仓'
    
    return result


def format_report(result: Dict) -> str:
    """格式化分析报告"""
    report = []
    report.append("=" * 60)
    report.append(f"  股票分析报告 - {result['stock_code']}")
    report.append("=" * 60)
    
    # 综合评分
    report.append(f"\n【综合评分】{result['total_score']}/100分")
    
    # 分项得分
    report.append("\n【分项得分】")
    scores = result['scores']
    report.append(f"  几何结构分析:   {scores['geometry']:>2}/25分")
    report.append(f"  MACD风洞共振:   {scores['macd_wind']:>2}/30分")
    report.append(f"  缩量短线:       {scores['shrinkage']:>2}/15分")
    report.append(f"  基本面分析:     {scores['fundamental']:>2}/10分")
    report.append(f"  情绪面分析:     {scores['sentiment']:>2}/10分")
    report.append(f"  AI预测分析:     {scores['ai_prediction']:>2}/10分")
    
    # 核心信号
    if result['signals']:
        report.append("\n【核心信号】")
        for signal in result['signals']:
            report.append(f"  • {signal}")
    
    # 风险提示
    if result['risk_warning']:
        report.append(f"\n【风险提示】 {result['risk_warning']}")
    
    # 操作建议
    if result['recommendation']:
        report.append(f"\n【操作建议】 {result['recommendation']}")
    
    report.append("\n" + "=" * 60)
    
    return "\n".join(report)


# 测试代码
if __name__ == '__main__':
    print("太几何交易 - 股票综合分析系统")
    print("=" * 60)
    
    # 分析示例股票
    result = analyze_stock("600519")  # 贵州茅台
    
    # 输出报告
    print(format_report(result))
    
    # 输出JSON格式详情
    print("\n【JSON详情】")
    print(json.dumps(result['scores'], indent=2, ensure_ascii=False))
