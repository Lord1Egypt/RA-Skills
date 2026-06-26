#!/usr/bin/env python3
"""
盘口监控演示脚本 - 展示完整功能
"""

import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/odds-movement-monitor')

from change_detector import (
    CompositeAnalyzer, 
    AsianHandicapAnalyzer,
    EuropeanOddsAnalyzer,
    MarketSignal
)
from dataclasses import dataclass


def demo_full_analysis():
    """完整分析演示"""
    print("=" * 70)
    print("📊 盘口变化监控 - 完整功能演示")
    print("=" * 70)
    
    analyzer = CompositeAnalyzer()
    
    # 场景1: 临场诱盘
    print("\n\n🔴 场景1: 临场诱盘检测")
    print("-" * 70)
    
    trap_data = {
        "match_id": "trap_001",
        "home_team": "曼城 (联赛第1)",
        "away_team": "伯恩利 (联赛第19)",
        "hours_to_match": 0.5,
        "asian": {
            "initial_line": -2.0,
            "current_line": -1.5,
            "initial_home_odds": 0.95,
            "current_home_odds": 0.82
        },
        "european": {
            "Bet365": {"home": 1.20, "draw": 6.50, "away": 13.0},
            "Pinnacle": {"home": 1.18, "draw": 6.80, "away": 14.0}
        },
        "true_prob": {"home": 0.78, "draw": 0.15, "away": 0.07},
        "odds_history": [
            {"home": 1.25, "draw": 6.00, "away": 11.0},
            {"home": 1.22, "draw": 6.20, "away": 12.0},
            {"home": 1.20, "draw": 6.50, "away": 13.0}
        ]
    }
    
    result1 = analyzer.analyze_match(trap_data)
    print(f"⚽ {result1['home_team']} vs {result1['away_team']}")
    print(f"📊 信号数量: {result1['signals_count']} | 🔴 高优先级: {result1['high_priority_signals']}")
    
    for signal in result1['signals']:
        icon = "🔴" if signal['severity'] == 'high' else ("🟡" if signal['severity'] == 'medium' else "🟢")
        print(f"\n  {icon} {signal['description']}")
        print(f"     类型: {signal['type']} | 置信度: {signal['confidence']*100:.0f}%")
    
    print(f"\n💡 建议: {result1['recommendation']}")
    
    # 场景2: 大额注单信号
    print("\n\n🔴 场景2: 大额注单信号检测")
    print("-" * 70)
    
    heavy_betting_data = {
        "match_id": "heavy_001",
        "home_team": "利物浦",
        "away_team": "阿森纳",
        "hours_to_match": 2,
        "asian": {
            "initial_line": -0.5,
            "current_line": -0.75,
            "initial_home_odds": 0.95,
            "current_home_odds": 0.85
        },
        "european": {
            "Bet365": {"home": 1.85, "draw": 3.60, "away": 4.20},
            "Pinnacle": {"home": 1.80, "draw": 3.70, "away": 4.40}
        },
        "true_prob": {"home": 0.52, "draw": 0.26, "away": 0.22},
        "odds_history": [
            {"home": 1.95, "draw": 3.50, "away": 3.80},
            {"home": 1.90, "draw": 3.55, "away": 3.90},
            {"home": 1.85, "draw": 3.60, "away": 4.00},
            {"home": 1.80, "draw": 3.65, "away": 4.10}
        ]
    }
    
    result2 = analyzer.analyze_match(heavy_betting_data)
    print(f"⚽ {result2['home_team']} vs {result2['away_team']}")
    print(f"📊 信号数量: {result2['signals_count']} | 🔴 高优先级: {result2['high_priority_signals']}")
    
    for signal in result2['signals']:
        icon = "🔴" if signal['severity'] == 'high' else ("🟡" if signal['severity'] == 'medium' else "🟢")
        print(f"\n  {icon} {signal['description']}")
        print(f"     类型: {signal['type']} | 置信度: {signal['confidence']*100:.0f}%")
    
    print(f"\n💡 建议: {result2['recommendation']}")
    
    # 场景3: 价值投注机会
    print("\n\n💎 场景3: 价值投注机会发现")
    print("-" * 70)
    
    value_data = {
        "match_id": "value_001",
        "home_team": "布莱顿",
        "away_team": "纽卡斯尔",
        "hours_to_match": 24,
        "asian": {
            "initial_line": 0,
            "current_line": 0,
            "initial_home_odds": 0.95,
            "current_home_odds": 0.95
        },
        "european": {
            "Bet365": {"home": 2.60, "draw": 3.40, "away": 2.70},
            "Pinnacle": {"home": 2.45, "draw": 3.50, "away": 2.85},
            "Exchange": {"home": 2.80, "draw": 3.30, "away": 2.55}
        },
        "true_prob": {"home": 0.40, "draw": 0.28, "away": 0.32},
        "odds_history": [
            {"home": 2.50, "draw": 3.40, "away": 2.75}
        ]
    }
    
    result3 = analyzer.analyze_match(value_data)
    print(f"⚽ {result3['home_team']} vs {result3['away_team']}")
    print(f"📊 信号数量: {result3['signals_count']} | 🔴 高优先级: {result3['high_priority_signals']}")
    
    for signal in result3['signals']:
        icon = "🔴" if signal['severity'] == 'high' else ("🟡" if signal['severity'] == 'medium' else "🟢")
        print(f"\n  {icon} {signal['description']}")
        print(f"     类型: {signal['type']} | 置信度: {signal['confidence']*100:.0f}%")
    
    print(f"\n💡 建议: {result3['recommendation']}")
    
    # 场景4: 变盘反转风险
    print("\n\n⚠️ 场景4: 变盘反转风险预警")
    print("-" * 70)
    
    reversal_data = {
        "match_id": "reversal_001",
        "home_team": "皇马",
        "away_team": "巴萨",
        "hours_to_match": 1,
        "asian": {
            "initial_line": -0.25,
            "current_line": 0,
            "initial_home_odds": 0.95,
            "current_home_odds": 0.98
        },
        "european": {
            "Bet365": {"home": 2.10, "draw": 3.40, "away": 3.40},
            "Pinnacle": {"home": 2.05, "draw": 3.50, "away": 3.50}
        },
        "true_prob": {"home": 0.45, "draw": 0.28, "away": 0.27},
        "odds_history": [
            {"home": 2.30, "draw": 3.30, "away": 3.10},
            {"home": 2.25, "draw": 3.35, "away": 3.15},
            {"home": 2.20, "draw": 3.38, "away": 3.20},
            {"home": 2.15, "draw": 3.40, "away": 3.30},
            {"home": 2.10, "draw": 3.40, "away": 3.40}
        ]
    }
    
    result4 = analyzer.analyze_match(reversal_data)
    print(f"⚽ {result4['home_team']} vs {result4['away_team']}")
    print(f"📊 信号数量: {result4['signals_count']} | 🔴 高优先级: {result4['high_priority_signals']}")
    
    for signal in result4['signals']:
        icon = "🔴" if signal['severity'] == 'high' else ("🟡" if signal['severity'] == 'medium' else "🟢")
        print(f"\n  {icon} {signal['description']}")
        print(f"     类型: {signal['type']} | 置信度: {signal['confidence']*100:.0f}%")
    
    print(f"\n💡 建议: {result4['recommendation']}")
    
    # 总结
    print("\n\n" + "=" * 70)
    print("📈 监控信号类型总结")
    print("=" * 70)
    print("""
🔴 高风险信号 (需立即关注):
   • late_line_drop    - 临场降盘 (机构信心下降)
   • heavy_betting     - 大额注单 (资金大量流入)
   • trap_favorite     - 诱盘信号 (强队让球过浅)
   • reversal_warning  - 变盘反转 (欧赔亚盘背离)

🟡 中等风险信号 (值得关注):
   • late_line_rise    - 临场升盘
   • odds_drop/rise    - 水位异常波动
   • draw_anomaly      - 平局赔率异常
   • bookmaker_disagreement - 机构分歧

🟢 机会信号 (可深入研究):
   • value_opportunity - 价值投注机会
   • cross_pattern     - 交叉盘对比
   • home/away_drift   - 赔率持续倾向
    """)
    
    print("\n" + "=" * 70)
    print("💡 使用方法:")
    print("=" * 70)
    print("""
1. 启动实时监控:
   python monitor.py --monitor --sport soccer --interval 60

2. 查看历史报告:
   python monitor.py --report

3. 高级分析演示:
   python change_detector.py

4. 设置 API Key 获取真实数据:
   export ODDS_API_KEY='your_key'
    """)
    print("=" * 70)


if __name__ == "__main__":
    demo_full_analysis()
