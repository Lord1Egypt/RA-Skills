#!/usr/bin/env python3
"""
足彩分析器 - 主分析脚本
支持基本面分析、赔率分析、投注建议
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import requests


class FootballBettingAnalyzer:
    """足彩分析器主类"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FOOTBALL_API_KEY")
        self.base_url = "https://v3.football.api-sports.io"
        self.headers = {
            "x-rapidapi-host": "v3.football.api-sports.io",
            "x-rapidapi-key": self.api_key
        } if self.api_key else {}
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """发送API请求"""
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API请求失败: {e}")
            return {}
    
    def get_fixtures(self, date: str, league_id: Optional[int] = None) -> List[Dict]:
        """获取指定日期的比赛列表"""
        params = {"date": date}
        if league_id:
            params["league"] = league_id
        
        data = self._make_request("fixtures", params)
        return data.get("response", [])
    
    def get_team_statistics(self, team_id: int, league_id: int, season: int) -> Dict:
        """获取球队统计数据"""
        params = {
            "team": team_id,
            "league": league_id,
            "season": season
        }
        data = self._make_request("teams/statistics", params)
        return data.get("response", {})
    
    def get_head_to_head(self, team1_id: int, team2_id: int) -> List[Dict]:
        """获取两队历史对战记录"""
        params = {"h2h": f"{team1_id}-{team2_id}"}
        data = self._make_request("fixtures/headtohead", params)
        return data.get("response", [])
    
    def get_team_form(self, team_id: int, last_n: int = 5) -> List[Dict]:
        """获取球队近期战绩"""
        params = {"team": team_id, "last": last_n}
        data = self._make_request("fixtures", params)
        return data.get("response", [])
    
    def analyze_match(self, fixture_id: int) -> Dict:
        """分析单场比赛"""
        # 获取比赛详情
        fixture_data = self._make_request(f"fixtures?id={fixture_id}")
        if not fixture_data.get("response"):
            return {"error": "未找到比赛信息"}
        
        fixture = fixture_data["response"][0]
        home_team = fixture["teams"]["home"]
        away_team = fixture["teams"]["away"]
        league = fixture["league"]
        
        # 获取统计数据
        season = league["season"]
        home_stats = self.get_team_statistics(home_team["id"], league["id"], season)
        away_stats = self.get_team_statistics(away_team["id"], league["id"], season)
        
        # 获取历史对战
        h2h = self.get_head_to_head(home_team["id"], away_team["id"])
        
        # 获取近期战绩
        home_form = self.get_team_form(home_team["id"], 5)
        away_form = self.get_team_form(away_team["id"], 5)
        
        # 分析
        analysis = {
            "match_info": {
                "home_team": home_team["name"],
                "away_team": away_team["name"],
                "league": league["name"],
                "date": fixture["fixture"]["date"],
            },
            "home_analysis": self._analyze_team_form(home_form, home_team["id"]),
            "away_analysis": self._analyze_team_form(away_form, away_team["id"]),
            "head_to_head": self._analyze_h2h(h2h, home_team["id"]),
            "prediction": self._generate_prediction(
                home_stats, away_stats, home_form, away_form, h2h
            )
        }
        
        return analysis
    
    def _analyze_team_form(self, fixtures: List[Dict], team_id: int) -> Dict:
        """分析球队近期状态"""
        if not fixtures:
            return {"form_string": "?????", "points": 0, "goals_scored": 0, "goals_conceded": 0}
        
        form_string = ""
        points = 0
        goals_scored = 0
        goals_conceded = 0
        
        for fixture in fixtures:
            home = fixture["teams"]["home"]["id"] == team_id
            home_winner = fixture["teams"]["home"]["winner"]
            away_winner = fixture["teams"]["away"]["winner"]
            
            goals = fixture["goals"]
            if home:
                goals_scored += goals["home"] or 0
                goals_conceded += goals["away"] or 0
                if home_winner:
                    form_string += "W"
                    points += 3
                elif away_winner:
                    form_string += "L"
                else:
                    form_string += "D"
                    points += 1
            else:
                goals_scored += goals["away"] or 0
                goals_conceded += goals["home"] or 0
                if away_winner:
                    form_string += "W"
                    points += 3
                elif home_winner:
                    form_string += "L"
                else:
                    form_string += "D"
                    points += 1
        
        return {
            "form_string": form_string[::-1],  # 最近的比赛在前
            "points": points,
            "goals_scored": goals_scored,
            "goals_conceded": goals_conceded,
            "goal_diff": goals_scored - goals_conceded
        }
    
    def _analyze_h2h(self, h2h: List[Dict], home_team_id: int) -> Dict:
        """分析历史对战"""
        if not h2h:
            return {"total": 0, "home_wins": 0, "away_wins": 0, "draws": 0}
        
        home_wins = 0
        away_wins = 0
        draws = 0
        
        for match in h2h[:10]:  # 只看最近10场
            home_winner = match["teams"]["home"]["winner"]
            away_winner = match["teams"]["away"]["winner"]
            
            if home_winner and match["teams"]["home"]["id"] == home_team_id:
                home_wins += 1
            elif away_winner and match["teams"]["away"]["id"] == home_team_id:
                home_wins += 1
            elif home_winner or away_winner:
                away_wins += 1
            else:
                draws += 1
        
        return {
            "total": len(h2h[:10]),
            "home_wins": home_wins,
            "away_wins": away_wins,
            "draws": draws
        }
    
    def _generate_prediction(
        self, 
        home_stats: Dict, 
        away_stats: Dict,
        home_form: List[Dict],
        away_form: List[Dict],
        h2h: List[Dict]
    ) -> Dict:
        """生成预测"""
        # 简单的评分系统
        home_score = 0
        away_score = 0
        
        # 近期状态评分
        home_form_analysis = self._analyze_team_form(home_form, home_stats.get("team", {}).get("id", 0))
        away_form_analysis = self._analyze_team_form(away_form, away_stats.get("team", {}).get("id", 0))
        
        home_score += home_form_analysis["points"] * 0.5
        away_score += away_form_analysis["points"] * 0.5
        
        # 历史对战评分
        h2h_analysis = self._analyze_h2h(h2h, home_stats.get("team", {}).get("id", 0))
        home_score += h2h_analysis["home_wins"] * 2
        away_score += h2h_analysis["away_wins"] * 2
        
        # 主客场优势
        home_score += 3
        
        # 计算概率
        total = home_score + away_score + 5  # 5分给平局
        home_prob = home_score / total
        away_prob = away_score / total
        draw_prob = 5 / total
        
        # 确定推荐
        if home_prob > max(away_prob, draw_prob):
            recommendation = "主胜"
            confidence = home_prob
        elif away_prob > max(home_prob, draw_prob):
            recommendation = "客胜"
            confidence = away_prob
        else:
            recommendation = "平局"
            confidence = draw_prob
        
        return {
            "probabilities": {
                "home_win": round(home_prob, 3),
                "draw": round(draw_prob, 3),
                "away_win": round(away_prob, 3)
            },
            "recommendation": recommendation,
            "confidence": round(confidence, 3),
            "analysis_summary": self._generate_summary(home_form_analysis, away_form_analysis, h2h_analysis)
        }
    
    def _generate_summary(self, home_form: Dict, away_form: Dict, h2h: Dict) -> str:
        """生成分析摘要"""
        summary = []
        
        summary.append(f"主队近5场: {home_form['form_string']} ({home_form['points']}/15分)")
        summary.append(f"客队近5场: {away_form['form_string']} ({away_form['points']}/15分)")
        summary.append(f"历史对战: 主队{h2h['home_wins']}胜 客队{h2h['away_wins']}胜 平{h2h['draws']}")
        
        return " | ".join(summary)
    
    def print_analysis(self, analysis: Dict):
        """打印分析报告"""
        if "error" in analysis:
            print(f"❌ {analysis['error']}")
            return
        
        info = analysis["match_info"]
        print("=" * 60)
        print(f"⚽ {info['home_team']} vs {info['away_team']}")
        print(f"🏆 {info['league']} | 📅 {info['date'][:10]}")
        print("=" * 60)
        
        print("\n📊 近期状态:")
        home = analysis["home_analysis"]
        away = analysis["away_analysis"]
        print(f"  主队: {home['form_string']} | 进{home['goals_scored']} 失{home['goals_conceded']} 净{home['goal_diff']:+d}")
        print(f"  客队: {away['form_string']} | 进{away['goals_scored']} 失{away['goals_conceded']} 净{away['goal_diff']:+d}")
        
        print("\n📈 历史对战 (近10场):")
        h2h = analysis["head_to_head"]
        print(f"  主队胜: {h2h['home_wins']} | 客队胜: {h2h['away_wins']} | 平: {h2h['draws']}")
        
        print("\n🎯 预测结果:")
        pred = analysis["prediction"]
        probs = pred["probabilities"]
        print(f"  主胜概率: {probs['home_win']*100:.1f}%")
        print(f"  平局概率: {probs['draw']*100:.1f}%")
        print(f"  客胜概率: {probs['away_win']*100:.1f}%")
        print(f"\n  ⭐ 推荐: {pred['recommendation']} (置信度: {pred['confidence']*100:.1f}%)")
        
        print(f"\n📝 {pred['analysis_summary']}")
        print("=" * 60)


class OddsAnalyzer:
    """赔率分析器"""
    
    @staticmethod
    def calculate_kelly(probability: float, odds: float) -> float:
        """计算凯利指数"""
        return (probability * odds - 1) / (odds - 1) if odds > 1 else 0
    
    @staticmethod
    def calculate_return_rate(odds_1: float, odds_x: float, odds_2: float) -> float:
        """计算返还率"""
        return 1 / (1/odds_1 + 1/odds_x + 1/odds_2)
    
    @staticmethod
    def detect_value_bet(model_prob: float, market_odds: float) -> Tuple[bool, float]:
        """检测价值投注"""
        implied_prob = 1 / market_odds
        edge = model_prob - implied_prob
        return edge > 0.05, edge  # 5% 的边际


def demo_analysis():
    """演示分析"""
    print("足彩分析助手 v1.0")
    print("=" * 60)
    print("\n提示: 要使用完整功能，请设置 FOOTBALL_API_KEY 环境变量")
    print("获取 API Key: https://www.api-football.com/")
    print("\n示例分析 (模拟数据):")
    print("-" * 60)
    
    # 模拟分析结果
    mock_analysis = {
        "match_info": {
            "home_team": "曼城",
            "away_team": "阿森纳",
            "league": "英超",
            "date": "2024-03-31T16:30:00+00:00"
        },
        "home_analysis": {
            "form_string": "WWWDW",
            "points": 13,
            "goals_scored": 14,
            "goals_conceded": 4,
            "goal_diff": 10
        },
        "away_analysis": {
            "form_string": "WDWWL",
            "points": 10,
            "goals_scored": 11,
            "goals_conceded": 6,
            "goal_diff": 5
        },
        "head_to_head": {
            "total": 10,
            "home_wins": 6,
            "away_wins": 2,
            "draws": 2
        },
        "prediction": {
            "probabilities": {
                "home_win": 0.55,
                "draw": 0.25,
                "away_win": 0.20
            },
            "recommendation": "主胜",
            "confidence": 0.55,
            "analysis_summary": "主队近5场: WWWDW (13/15分) | 客队近5场: WDWWL (10/15分) | 历史对战: 主队6胜 客队2胜 平2"
        }
    }
    
    analyzer = FootballBettingAnalyzer()
    analyzer.print_analysis(mock_analysis)
    
    print("\n" + "=" * 60)
    print("💡 使用示例:")
    print("  1. 设置 API Key: export FOOTBALL_API_KEY='your_key'")
    print("  2. 运行分析: python analyzer.py --match 12345")
    print("  3. 查看今日比赛: python analyzer.py --today")
    print("=" * 60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="足彩分析助手")
    parser.add_argument("--match", type=int, help="比赛ID")
    parser.add_argument("--today", action="store_true", help="查看今日比赛")
    parser.add_argument("--demo", action="store_true", help="运行演示")
    
    args = parser.parse_args()
    
    if args.demo or (not args.match and not args.today):
        demo_analysis()
    elif args.match:
        analyzer = FootballBettingAnalyzer()
        analysis = analyzer.analyze_match(args.match)
        analyzer.print_analysis(analysis)
    elif args.today:
        today = datetime.now().strftime("%Y-%m-%d")
        analyzer = FootballBettingAnalyzer()
        fixtures = analyzer.get_fixtures(today)
        print(f"今日比赛 ({today}):\n")
        for fixture in fixtures[:10]:  # 只显示前10场
            home = fixture["teams"]["home"]["name"]
            away = fixture["teams"]["away"]["name"]
            league = fixture["league"]["name"]
            time = fixture["fixture"]["date"][11:16]
            print(f"  [{league}] {time} {home} vs {away}")
