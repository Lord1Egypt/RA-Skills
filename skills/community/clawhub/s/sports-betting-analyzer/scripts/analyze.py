#!/usr/bin/env python3
"""
体育彩票分析助手 - 主分析脚本

功能：
- 数据收集与处理
- 基础统计分析
- 简单预测模型
- 生成分析报告
"""

import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random
import os

# 添加脚本路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_collector import DataCollector
from prediction_model import PredictionModel
from report_generator import ReportGenerator

class SportsBettingAnalyzer:
    """体育彩票分析助手主类"""

    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.data_collector = DataCollector(self.config)
        self.prediction_model = PredictionModel(self.config)
        self.report_generator = ReportGenerator(self.config)

    def _load_config(self, config_path):
        """加载配置文件"""
        if config_path is None:
            config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'config',
                'sports-betting.json'
            )

        default_config = {
            "risk_level": "moderate",
            "default_bet_percentage": 2,
            "preferred_leagues": ["NBA", "Premier League", "La Liga", "World Cup"],
            "data_sources": ["official", "free_api"],
            "min_confidence": 0.6,
            "max_daily_bets": 3
        }

        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
        else:
            # 创建默认配置目录和文件
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)

        return default_config

    def analyze_match(self, sport: str, team1: str, team2: str, **kwargs) -> Dict:
        """
        分析一场比赛

        Args:
            sport: 体育项目 (NBA, football等)
            team1: 主队名称
            team2: 客队名称
            **kwargs: 其他参数（比赛日期、赔率等）

        Returns:
            分析结果字典
        """
        print(f"\n{'='*60}")
        print(f"开始分析 {sport} 比赛: {team1} vs {team2}")
        print(f"{'='*60}\n")

        # 1. 数据收集
        print("📊 收集比赛数据...")
        match_data = self.data_collector.collect_match_data(sport, team1, team2, **kwargs)

        if not match_data:
            return {"error": "无法获取比赛数据"}

        # 2. 特征提取
        print("🔍 提取特征...")
        features = self.data_collector.extract_features(match_data)

        # 3. 预测
        print("🎯 生成预测...")
        prediction = self.prediction_model.predict(sport, features)

        # 4. 风险评估
        print("⚠️  评估风险...")
        risk_assessment = self._assess_risk(prediction, match_data)

        # 5. 生成报告
        print("📝 生成分析报告...")
        report = self.report_generator.generate_report(
            sport=SportType.NBA if sport.lower() == 'nba' else SportType.FOOTBALL,
            team1=team1,
            team2=team2,
            match_data=match_data,
            features=features,
            prediction=prediction,
            risk_assessment=risk_assessment
        )

        # 6. 保存历史记录
        self._save_analysis_history(report)

        return report

    def _assess_risk(self, prediction: Dict, match_data: Dict) -> Dict:
        """评估风险"""
        confidence = prediction.get('confidence', 0.5)
        odds = match_data.get('odds', {})

        risk_level = "high"
        if confidence > 0.75:
            risk_level = "low"
        elif confidence > 0.65:
            risk_level = "moderate"

        return {
            "risk_level": risk_level,
            "confidence": confidence,
            "value_bet": self._is_value_bet(prediction, odds),
            "suggested_bet_percentage": self._calculate_bet_percentage(confidence, risk_level)
        }

    def _is_value_bet(self, prediction: Dict, odds: Dict) -> bool:
        """判断是否为价值投注"""
        # 简化的价值投注判断
        # 实际应该比较隐含概率和模型概率
        return random.choice([True, False, False])  # 模拟

    def _calculate_bet_percentage(self, confidence: float, risk_level: str) -> float:
        """计算建议投注比例"""
        base_percentage = self.config['default_bet_percentage']

        if confidence > 0.8:
            return base_percentage * 1.5
        elif confidence > 0.7:
            return base_percentage
        else:
            return base_percentage * 0.5

    def _save_analysis_history(self, report: Dict):
        """保存分析历史"""
        history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'analysis_history.json'
        )

        history = []
        if os.path.exists(history_file):
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)

        history.append({
            "timestamp": datetime.now().isoformat(),
            "report": report
        })

        # 只保留最近50条记录
        history = history[-50:]

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)

    def get_today_recommendations(self, sport: str = None) -> List[Dict]:
        """获取今日推荐"""
        # 模拟获取今日推荐
        print(f"\n{'='*60}")
        print(f"获取今日 {sport or '所有'} 推荐比赛")
        print(f"{'='*60}\n")

        recommendations = []

        # 模拟一些推荐
        if sport is None or sport.lower() == 'nba':
            recommendations.append({
                "sport": "NBA",
                "match": "湖人 vs 勇士",
                "prediction": "湖人胜",
                "confidence": 0.72,
                "risk": "moderate",
                "bet_percentage": 2
            })

        if sport is None or sport.lower() in ['football', 'soccer']:
            recommendations.append({
                "sport": "Football",
                "match": "巴萨 vs 皇马",
                "prediction": "巴萨胜",
                "confidence": 0.68,
                "risk": "moderate",
                "bet_percentage": 2
            })

        return recommendations

    def show_analysis_history(self, limit: int = 10) -> List[Dict]:
        """显示分析历史"""
        history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data',
            'analysis_history.json'
        )

        if not os.path.exists(history_file):
            return []

        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)

        # 返回最近的记录
        return history[-limit:]


# 运动类型枚举
class SportType:
    NBA = "NBA"
    FOOTBALL = "Football"
    WORLD_CUP = "World Cup"


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  analyze.py <sport> <team1> <team2> [options]")
        print("  analyze.py today [sport]")
        print("  analyze.py history [limit]")
        sys.exit(1)

    command = sys.argv[1]
    analyzer = SportsBettingAnalyzer()

    if command == 'today':
        sport = sys.argv[2] if len(sys.argv) > 2 else None
        recommendations = analyzer.get_today_recommendations(sport)
        print("\n📋 今日推荐:")
        for rec in recommendations:
            print(f"\n{rec['sport']}: {rec['match']}")
            print(f"  预测: {rec['prediction']}")
            print(f"  置信度: {rec['confidence']:.2%}")
            print(f"  风险: {rec['risk']}")
            print(f"  建议投注: {rec['bet_percentage']}%")

    elif command == 'history':
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = analyzer.show_analysis_history(limit)
        print(f"\n📚 最近 {len(history)} 条分析记录:")
        for item in history:
            timestamp = item['timestamp']
            report = item['report']
            print(f"\n{timestamp}")
            print(f"  {report.get('sport', '')}: {report.get('match', '')}")
            print(f"  预测: {report.get('prediction', '')}")

    else:
        # 分析比赛
        sport = command
        team1 = sys.argv[2]
        team2 = sys.argv[3]

        report = analyzer.analyze_match(sport, team1, team2)

        # 打印报告
        print("\n" + "="*60)
        print("📊 分析报告")
        print("="*60)
        print(f"\n{report.get('summary', '')}")


if __name__ == "__main__":
    main()