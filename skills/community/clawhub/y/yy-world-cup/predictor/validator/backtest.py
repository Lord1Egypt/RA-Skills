"""
回测验证器
用历史比赛数据验证预测模型的准确率
"""

import json
from typing import List, Dict
from pathlib import Path
from ..data.models import MatchInfo, Team, Stadium, RecentMatch
from ..data.api_client import BalldontlieFIFAClient
from ..core import WorldCupPredictor


# 2022世界杯各球队基础Elo（赛前）
TEAM_ELO_2022 = {
    "Brazil": 1920, "Argentina": 1910, "France": 1900, "Spain": 1880,
    "England": 1870, "Germany": 1860, "Netherlands": 1850, "Portugal": 1840,
    "Belgium": 1830, "Croatia": 1820, "Italy": 1810, "Uruguay": 1800,
    "USA": 1790, "Mexico": 1780, "Switzerland": 1770, "Denmark": 1760,
    "Poland": 1750, "Senegal": 1740, "Morocco": 1730, "Japan": 1720,
    "Australia": 1710, "South Korea": 1700, "Canada": 1690, "Cameroon": 1680,
    "Ghana": 1670, "Ecuador": 1660, "Qatar": 1650, "Iran": 1640,
    "Saudi Arabia": 1630, "Tunisia": 1620, "Costa Rica": 1610, "Wales": 1600,
}

# 球队战术风格
TEAM_STYLE_2022 = {
    "Brazil": "technical", "Argentina": "technical", "France": "balanced",
    "Spain": "technical", "England": "physical", "Germany": "physical",
    "Netherlands": "attacking", "Portugal": "technical", "Belgium": "attacking",
    "Croatia": "balanced", "Italy": "defensive", "Uruguay": "physical",
    "USA": "balanced", "Mexico": "technical", "Switzerland": "balanced",
    "Denmark": "balanced", "Poland": "physical", "Senegal": "physical",
    "Morocco": "defensive", "Japan": "technical", "South Korea": "physical",
    "Australia": "physical", "Canada": "physical", "Morocco": "defensive",
}


class BacktestValidator:
    """回测验证器：用历史比赛数据验证模型准确率"""

    def __init__(self, api_key: str = None):
        """
        Args:
            api_key: balldontlie API key（可选）
        """
        self.api_key = api_key
        self.predictor = WorldCupPredictor()
        self.results = []

    def _create_team(self, name: str) -> Team:
        """创建Team对象"""
        elo = TEAM_ELO_2022.get(name, 1750)
        style_str = TEAM_STYLE_2022.get(name, "balanced")
        from ..data.models import TeamStyle
        return Team(
            id=hash(name) % 1000,
            name=name,
            abbreviation=name[:3].upper(),
            country_code=name[:3].upper(),
            confederation="UEFA",
            elo=elo,
            style=TeamStyle(style_str),
        )

    def _create_stadium(self, name: str = "Test Stadium") -> Stadium:
        """创建Stadium对象"""
        return Stadium(
            id=1, name=name, city="Doha", country="Qatar", capacity=40000
        )

    def _create_sample_recent(self) -> List[RecentMatch]:
        """创建示例近期比赛数据（中性）"""
        return [
            RecentMatch(result="win", goals=2, conceded=1, opponent_elo=1750),
            RecentMatch(result="draw", goals=1, conceded=1, opponent_elo=1750),
            RecentMatch(result="win", goals=2, conceded=0, opponent_elo=1750),
        ]

    def validate_2022_worldcup(self) -> Dict:
        """
        验证2022世界杯小组赛关键比赛
        使用已知的真实比赛结果
        """
        # 关键比赛样本（小组赛部分经典比赛）
        sample_matches = [
            # 实际结果: 沙特 2-1 阿根廷（爆冷）
            {
                "home": "Argentina", "away": "Saudi Arabia",
                "home_goals": 1.3, "away_goals": 1.0,
                "home_conceded": 0.5, "away_conceded": 1.5,
                "actual_result": "loss",  # 主队阿根廷输
                "actual_score": "1-2",
                "description": "阿根廷 vs 沙特（爆冷）"
            },
            # 实际结果: 日本 2-1 德国（爆冷）
            {
                "home": "Germany", "away": "Japan",
                "home_goals": 1.8, "away_goals": 1.2,
                "home_conceded": 0.8, "away_conceded": 1.0,
                "actual_result": "loss",
                "actual_score": "1-2",
                "description": "德国 vs 日本（爆冷）"
            },
            # 实际结果: 法国 4-1 澳大利亚
            {
                "home": "France", "away": "Australia",
                "home_goals": 2.0, "away_goals": 1.0,
                "home_conceded": 0.7, "away_conceded": 1.5,
                "actual_result": "win",
                "actual_score": "4-1",
                "description": "法国 vs 澳大利亚"
            },
            # 实际结果: 英格兰 6-2 伊朗
            {
                "home": "England", "away": "Iran",
                "home_goals": 2.2, "away_goals": 0.8,
                "home_conceded": 0.6, "away_conceded": 1.8,
                "actual_result": "win",
                "actual_score": "6-2",
                "description": "英格兰 vs 伊朗"
            },
            # 实际结果: 西班牙 7-0 哥斯达黎加
            {
                "home": "Spain", "away": "Costa Rica",
                "home_goals": 1.8, "away_goals": 0.7,
                "home_conceded": 0.7, "away_conceded": 2.0,
                "actual_result": "win",
                "actual_score": "7-0",
                "description": "西班牙 vs 哥斯达黎加"
            },
            # 实际结果: 卡塔尔 0-2 厄瓜多尔（揭幕战）
            {
                "home": "Qatar", "away": "Ecuador",
                "home_goals": 1.0, "away_goals": 1.0,
                "home_conceded": 1.5, "away_conceded": 1.3,
                "actual_result": "loss",
                "actual_score": "0-2",
                "description": "卡塔尔 vs 厄瓜多尔"
            },
            # 实际结果: 美国 1-1 威尔士
            {
                "home": "USA", "away": "Wales",
                "home_goals": 1.3, "away_goals": 1.0,
                "home_conceded": 1.0, "away_conceded": 1.2,
                "actual_result": "draw",
                "actual_score": "1-1",
                "description": "美国 vs 威尔士"
            },
            # 实际结果: 丹麦 0-0 突尼斯
            {
                "home": "Denmark", "away": "Tunisia",
                "home_goals": 1.3, "away_goals": 0.8,
                "home_conceded": 0.9, "away_conceded": 1.2,
                "actual_result": "draw",
                "actual_score": "0-0",
                "description": "丹麦 vs 突尼斯"
            },
        ]

        results = []
        correct_count = 0
        total = len(sample_matches)

        for match_data in sample_matches:
            match = MatchInfo(
                match_id=None,
                home_team=self._create_team(match_data["home"]),
                away_team=self._create_team(match_data["away"]),
                match_time="2022-11",
                stadium=self._create_stadium(),
                stage="group",
                is_neutral=True,  # 2022世界杯在中立场馆进行
                home_goals_per_match=match_data["home_goals"],
                away_goals_per_match=match_data["away_goals"],
                home_conceded_per_match=match_data["home_conceded"],
                away_conceded_per_match=match_data["away_conceded"],
                home_recent=self._create_sample_recent(),
                away_recent=self._create_sample_recent(),
            )

            prediction = self.predictor.predict(match)
            predicted_result = self._get_predicted_outcome(prediction)
            actual_result = match_data["actual_result"]
            is_correct = predicted_result == actual_result

            if is_correct:
                correct_count += 1

            results.append({
                "match": match_data["description"],
                "predicted": predicted_result,
                "actual": actual_result,
                "win_prob": f"{prediction.home_win_prob*100:.1f}%",
                "draw_prob": f"{prediction.draw_prob*100:.1f}%",
                "loss_prob": f"{prediction.away_win_prob*100:.1f}%",
                "predicted_score": prediction.predicted_scores[0][0],
                "actual_score": match_data["actual_score"],
                "mode": prediction.predict_mode,
                "is_correct": is_correct,
            })

        accuracy = correct_count / total if total > 0 else 0
        report = {
            "test_set": "2022 World Cup Group Stage (Sample)",
            "total_matches": total,
            "correct_predictions": correct_count,
            "accuracy": f"{accuracy*100:.1f}%",
            "results": results,
            "summary": {
                "strong_team_wins": sum(1 for r in results if r["is_correct"] and r["actual"] == "win"),
                "upsets_caught": sum(1 for r in results if r["is_correct"] and r["actual"] in ["loss", "draw"] and r["predicted"] != r["actual"]),
                "missed_upsets": sum(1 for r in results if not r["is_correct"]),
            }
        }

        self.results = results
        return report

    def _get_predicted_outcome(self, prediction) -> str:
        """根据预测概率获取最可能的结果"""
        probs = {
            "win": prediction.home_win_prob,
            "draw": prediction.draw_prob,
            "loss": prediction.away_win_prob,
        }
        return max(probs.items(), key=lambda x: x[1])[0]

    def print_report(self, report: Dict) -> None:
        """打印回测报告"""
        print(f"\n{'='*70}")
        print(f"📊 2022世界杯预测模型回测报告")
        print(f"{'='*70}")
        print(f"测试集: {report['test_set']}")
        print(f"比赛总数: {report['total_matches']}")
        print(f"正确预测: {report['correct_predictions']}")
        print(f"准确率: {report['accuracy']}")
        print(f"\n{'比赛':<30} {'预测':<8} {'实际':<8} {'主胜%':<8} {'平%':<8} {'客胜%':<8} {'是否正确':<8}")
        print("-" * 90)

        for r in report['results']:
            mark = "✅" if r['is_correct'] else "❌"
            print(f"{r['match']:<30} {r['predicted']:<8} {r['actual']:<8} "
                  f"{r['win_prob']:<8} {r['draw_prob']:<8} {r['loss_prob']:<8} {mark}")

        print(f"\n📈 分类统计:")
        print(f"  强队获胜命中: {report['summary']['strong_team_wins']}")
        print(f"  爆冷预测命中: {report['summary']['upsets_caught']}")
        print(f"  预测错误: {report['summary']['missed_upsets']}")
