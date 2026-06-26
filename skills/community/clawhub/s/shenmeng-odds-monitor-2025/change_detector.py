#!/usr/bin/env python3
"""
高级变化检测算法 - 识别盘口异常和投注信号
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class MarketSignal:
    """市场信号"""
    signal_type: str          # 信号类型
    confidence: float         # 置信度 0-1
    description: str          # 描述
    severity: str             # 严重程度: low, medium, high


class AsianHandicapAnalyzer:
    """亚盘分析器"""
    
    @staticmethod
    def analyze_line_movement(
        initial_line: float,
        current_line: float,
        initial_home_odds: float,
        current_home_odds: float,
        match_time_hours: float
    ) -> List[MarketSignal]:
        """
        分析盘口变化
        
        Args:
            initial_line: 初盘盘口
            current_line: 即时盘口
            initial_home_odds: 初盘主队水位
            current_home_odds: 即时主队水位
            match_time_hours: 距离比赛开始的小时数
        """
        signals = []
        
        # 盘口升降
        line_change = current_line - initial_line
        odds_change = current_home_odds - initial_home_odds
        
        # 临场变盘信号 (赛前2小时内)
        if match_time_hours <= 2 and abs(line_change) >= 0.25:
            if line_change < 0:  # 盘口下降，主队让球减少
                signals.append(MarketSignal(
                    signal_type="late_line_drop",
                    confidence=0.8,
                    description=f"临场降盘 {abs(line_change)}，机构对主队信心下降",
                    severity="high"
                ))
            else:
                signals.append(MarketSignal(
                    signal_type="late_line_rise",
                    confidence=0.75,
                    description=f"临场升盘 {line_change}，机构看好主队",
                    severity="medium"
                ))
        
        # 水位异常信号
        if abs(odds_change) > 0.15:
            if odds_change < 0:
                signals.append(MarketSignal(
                    signal_type="odds_drop",
                    confidence=0.7,
                    description=f"主队水位下降 {abs(odds_change):.2f}，可能有资金流入",
                    severity="medium"
                ))
            else:
                signals.append(MarketSignal(
                    signal_type="odds_rise",
                    confidence=0.6,
                    description=f"主队水位上升 {odds_change:.2f}，投注压力小",
                    severity="low"
                ))
        
        # 盘口水位背离信号
        if line_change < 0 and odds_change > 0:
            signals.append(MarketSignal(
                signal_type="divergence",
                confidence=0.75,
                description="盘口下降但水位上升，可能存在诱盘",
                severity="high"
            ))
        
        return signals
    
    @staticmethod
    def detect_trap_line(
        line: float,
        home_odds: float,
        away_odds: float,
        team_strength_diff: float
    ) -> Optional[MarketSignal]:
        """
        检测诱盘
        
        Args:
            team_strength_diff: 实力差 (+主队强，-客队强)
        """
        # 强队让盘过浅
        if team_strength_diff > 0.5 and line < -0.5:
            if home_odds < 0.90:  # 低水位诱惑
                return MarketSignal(
                    signal_type="trap_favorite",
                    confidence=0.7,
                    description=f"强队让 {line} 盘且水位 {home_odds}，可能诱上",
                    severity="high"
                )
        
        # 弱队受让过深
        if team_strength_diff < -0.5 and line > 0.75:
            if away_odds < 0.90:
                return MarketSignal(
                    signal_type="trap_underdog",
                    confidence=0.65,
                    description=f"弱队受让 {line} 盘且水位 {away_odds}，可能诱下",
                    severity="medium"
                )
        
        return None


class EuropeanOddsAnalyzer:
    """欧赔分析器"""
    
    @staticmethod
    def detect_value_discrepancy(
        bookmaker_odds: Dict[str, Dict[str, float]],
        true_probabilities: Dict[str, float]
    ) -> List[MarketSignal]:
        """
        检测赔率差异和价值投注机会
        
        Args:
            bookmaker_odds: {bookmaker: {outcome: odds}}
            true_probabilities: {outcome: probability}
        """
        signals = []
        
        # 计算平均赔率
        avg_odds = {}
        for outcome in ["home", "draw", "away"]:
            odds_list = [b[outcome] for b in bookmaker_odds.values() if outcome in b]
            if odds_list:
                avg_odds[outcome] = sum(odds_list) / len(odds_list)
        
        # 检测最高赔率 vs 真实概率
        for outcome, prob in true_probabilities.items():
            if outcome in avg_odds:
                expected_odds = 1 / prob
                discrepancy = avg_odds[outcome] - expected_odds
                
                if discrepancy > 0.3:  # 赔率高于理论值
                    signals.append(MarketSignal(
                        signal_type="value_opportunity",
                        confidence=min(discrepancy * 0.5, 0.9),
                        description=f"{outcome} 赔率 {avg_odds[outcome]:.2f} 高于理论值 {expected_odds:.2f}",
                        severity="medium"
                    ))
        
        # 检测机构分歧
        for outcome in ["home", "draw", "away"]:
            odds_list = [b.get(outcome) for b in bookmaker_odds.values() if b.get(outcome)]
            if len(odds_list) >= 3:
                max_odds = max(odds_list)
                min_odds = min(odds_list)
                spread = (max_odds - min_odds) / min_odds
                
                if spread > 0.15:  # 15% 以上分歧
                    signals.append(MarketSignal(
                        signal_type="bookmaker_disagreement",
                        confidence=min(spread, 0.85),
                        description=f"{outcome} 机构分歧 {spread*100:.1f}%，最高 {max_odds:.2f} 最低 {min_odds:.2f}",
                        severity="medium"
                    ))
        
        return signals
    
    @staticmethod
    def analyze_odds_trend(
        odds_history: List[Dict[str, float]]
    ) -> List[MarketSignal]:
        """
        分析赔率变化趋势
        
        Args:
            odds_history: [{timestamp, home, draw, away}, ...]
        """
        signals = []
        
        if len(odds_history) < 3:
            return signals
        
        # 计算趋势
        first = odds_history[0]
        last = odds_history[-1]
        
        home_trend = (last["home"] - first["home"]) / first["home"]
        draw_trend = (last["draw"] - first["draw"]) / first["draw"]
        away_trend = (last["away"] - first["away"]) / first["away"]
        
        # 主胜持续下降 - 机构看好主队
        if home_trend < -0.10 and len(odds_history) >= 5:
            signals.append(MarketSignal(
                signal_type="home_drift",
                confidence=min(abs(home_trend) * 2, 0.9),
                description=f"主胜赔率持续下降 {abs(home_trend)*100:.1f}%，机构看好主队",
                severity="high"
            ))
        
        # 客胜持续下降
        if away_trend < -0.10 and len(odds_history) >= 5:
            signals.append(MarketSignal(
                signal_type="away_drift",
                confidence=min(abs(away_trend) * 2, 0.9),
                description=f"客胜赔率持续下降 {abs(away_trend)*100:.1f}%，机构看好客队",
                severity="high"
            ))
        
        # 平局异常
        if abs(draw_trend) > 0.15:
            direction = "上升" if draw_trend > 0 else "下降"
            signals.append(MarketSignal(
                signal_type="draw_anomaly",
                confidence=min(abs(draw_trend), 0.8),
                description=f"平局赔率异常{direction} {abs(draw_trend)*100:.1f}%",
                severity="medium"
            ))
        
        return signals


class PatternRecognizer:
    """模式识别器"""
    
    @staticmethod
    def recognize_cross_pattern(
        matches: List[Dict],
        target_match: Dict
    ) -> Optional[MarketSignal]:
        """
        识别交叉盘模式
        
        同时间段相似盘口对比
        """
        similar_lines = [
            m for m in matches
            if abs(m.get("line", 0) - target_match.get("line", 0)) < 0.25
            and m.get("match_id") != target_match.get("match_id")
        ]
        
        if len(similar_lines) >= 2:
            return MarketSignal(
                signal_type="cross_pattern",
                confidence=0.6,
                description=f"发现 {len(similar_lines)} 场交叉盘，可对比参考",
                severity="low"
            )
        
        return None
    
    @staticmethod
    def detect_reversal_pattern(
        odds_history: List[Dict],
        asian_line_history: List[float]
    ) -> Optional[MarketSignal]:
        """
        检测变盘反转模式
        """
        if len(odds_history) < 5 or len(asian_line_history) < 5:
            return None
        
        # 欧赔和亚盘背离反转
        home_trend = odds_history[-1]["home"] - odds_history[0]["home"]
        line_trend = asian_line_history[-1] - asian_line_history[0]
        
        # 欧赔下降但亚盘上升 (看好主队但让球变少)
        if home_trend < -0.05 and line_trend > 0.25:
            return MarketSignal(
                signal_type="reversal_warning",
                confidence=0.75,
                description="欧赔和亚盘背离，存在变盘反转风险",
                severity="high"
            )
        
        return None


class CompositeAnalyzer:
    """综合分析器"""
    
    def __init__(self):
        self.asian = AsianHandicapAnalyzer()
        self.european = EuropeanOddsAnalyzer()
        self.pattern = PatternRecognizer()
    
    def analyze_match(self, data: Dict) -> Dict:
        """
        综合分析一场比赛
        
        Args:
            data: {
                "match_id": str,
                "home_team": str,
                "away_team": str,
                "asian": {...},
                "european": {...},
                "history": {...}
            }
        """
        all_signals = []
        
        # 亚盘分析
        if "asian" in data:
            asian_signals = self.asian.analyze_line_movement(
                data["asian"].get("initial_line", 0),
                data["asian"].get("current_line", 0),
                data["asian"].get("initial_home_odds", 0),
                data["asian"].get("current_home_odds", 0),
                data.get("hours_to_match", 24)
            )
            all_signals.extend(asian_signals)
        
        # 欧赔分析
        if "european" in data and "true_prob" in data:
            euro_signals = self.european.detect_value_discrepancy(
                data["european"],
                data["true_prob"]
            )
            all_signals.extend(euro_signals)
        
        if "odds_history" in data:
            trend_signals = self.european.analyze_odds_trend(data["odds_history"])
            all_signals.extend(trend_signals)
        
        # 按严重程度排序
        severity_order = {"high": 0, "medium": 1, "low": 2}
        all_signals.sort(key=lambda s: severity_order.get(s.severity, 3))
        
        # 生成建议
        recommendation = self._generate_recommendation(all_signals, data)
        
        return {
            "match_id": data.get("match_id"),
            "home_team": data.get("home_team"),
            "away_team": data.get("away_team"),
            "signals_count": len(all_signals),
            "high_priority_signals": len([s for s in all_signals if s.severity == "high"]),
            "signals": [
                {
                    "type": s.signal_type,
                    "confidence": s.confidence,
                    "description": s.description,
                    "severity": s.severity
                }
                for s in all_signals
            ],
            "recommendation": recommendation
        }
    
    def _generate_recommendation(self, signals: List[MarketSignal], data: Dict) -> str:
        """生成综合建议"""
        if not signals:
            return "✅ 盘口稳定，无异常信号"
        
        high_risk = [s for s in signals if s.severity == "high"]
        
        if len(high_risk) >= 2:
            return "⚠️ 高风险 - 多个异常信号，建议观望"
        
        if any(s.signal_type == "value_opportunity" for s in signals):
            return "💎 发现价值投注机会，建议深入研究"
        
        if any(s.signal_type == "trap_favorite" for s in signals):
            return "🚫 疑似诱盘，建议回避强队"
        
        if any(s.signal_type in ["home_drift", "away_drift"] for s in signals):
            return "📈 赔率趋势明显，可顺势跟进"
        
        return "➖ 中性 - 继续监控，等待更明确信号"


# 演示
def demo_analysis():
    """演示高级分析"""
    print("=" * 60)
    print("高级盘口分析演示")
    print("=" * 60)
    
    analyzer = CompositeAnalyzer()
    
    # 模拟数据
    test_data = {
        "match_id": "test_001",
        "home_team": "拜仁慕尼黑",
        "away_team": "多特蒙德",
        "hours_to_match": 1.5,
        "asian": {
            "initial_line": -0.75,
            "current_line": -0.50,
            "initial_home_odds": 0.95,
            "current_home_odds": 0.88
        },
        "european": {
            "Bet365": {"home": 1.70, "draw": 4.00, "away": 4.50},
            "Pinnacle": {"home": 1.65, "draw": 4.10, "away": 4.80},
            "Smarkets": {"home": 1.75, "draw": 3.90, "away": 4.30}
        },
        "true_prob": {
            "home": 0.60,
            "draw": 0.22,
            "away": 0.18
        },
        "odds_history": [
            {"timestamp": "t-4h", "home": 1.80, "draw": 3.80, "away": 4.20},
            {"timestamp": "t-3h", "home": 1.75, "draw": 3.85, "away": 4.30},
            {"timestamp": "t-2h", "home": 1.72, "draw": 3.90, "away": 4.40},
            {"timestamp": "t-1h", "home": 1.70, "draw": 4.00, "away": 4.50}
        ]
    }
    
    result = analyzer.analyze_match(test_data)
    
    print(f"\n⚽ {result['home_team']} vs {result['away_team']}")
    print(f"📊 检测到 {result['signals_count']} 个信号")
    print(f"🔴 高优先级: {result['high_priority_signals']} 个")
    
    print("\n📋 详细信号:")
    for signal in result['signals']:
        icon = "🔴" if signal['severity'] == 'high' else ("🟡" if signal['severity'] == 'medium' else "🟢")
        print(f"  {icon} [{signal['type']}] {signal['description']}")
        print(f"     置信度: {signal['confidence']*100:.0f}%")
    
    print(f"\n💡 综合建议: {result['recommendation']}")
    print("=" * 60)


if __name__ == "__main__":
    demo_analysis()
