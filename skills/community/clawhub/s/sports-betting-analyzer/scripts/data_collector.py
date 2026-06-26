#!/usr/bin/env python3
"""
数据收集模块

功能：
- 收集比赛基础数据
- 提取特征
- 存储历史数据
"""

import json
import random
from typing import Dict, List
from datetime import datetime, timedelta
import os


class DataCollector:
    """数据收集器"""

    def __init__(self, config: Dict):
        self.config = config
        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data'
        )
        os.makedirs(self.data_dir, exist_ok=True)

    def collect_match_data(self, sport: str, team1: str, team2: str, **kwargs) -> Dict:
        """
        收集比赛数据

        Args:
            sport: 体育项目
            team1: 主队
            team2: 客队
            **kwargs: 其他参数

        Returns:
            比赛数据字典
        """
        # MVP版本：模拟数据收集
        # 实际版本应该连接真实数据源

        match_date = kwargs.get('date', datetime.now().strftime('%Y-%m-%d'))

        data = {
            "sport": sport,
            "team1": team1,
            "team2": team2,
            "match_date": match_date,
            "venue": f"{team1}主场" if sport.lower() == 'nba' else f"{team1}主场",
            "timestamp": datetime.now().isoformat()
        }

        # 收集球队基础数据
        data['team1_stats'] = self._collect_team_stats(sport, team1, is_home=True)
        data['team2_stats'] = self._collect_team_stats(sport, team2, is_home=False)

        # 收集历史对战
        data['h2h'] = self._collect_head_to_head(sport, team1, team2)

        # 收集赔率数据
        data['odds'] = self._collect_odds(sport, team1, team2)

        # 收集伤病信息
        data['injuries'] = self._collect_injuries(sport, team1, team2)

        return data

    def _collect_team_stats(self, sport: str, team: str, is_home: bool) -> Dict:
        """收集球队统计数据"""
        # MVP版本：模拟数据
        # 实际版本应该从真实数据源获取

        if sport.lower() == 'nba':
            return self._generate_nba_stats(team, is_home)
        else:
            return self._generate_football_stats(team, is_home)

    def _generate_nba_stats(self, team: str, is_home: bool) -> Dict:
        """生成NBA统计数据（模拟）"""
        base_win_rate = random.uniform(0.4, 0.7)
        home_advantage = 0.1 if is_home else 0

        return {
            "team": team,
            "season_win_rate": round(base_win_rate, 3),
            "home_win_rate": round(base_win_rate + home_advantage, 3),
            "away_win_rate": round(base_win_rate - home_advantage, 3),
            "recent_5_games": [random.choice(['W', 'L']) for _ in range(5)],
            "points_per_game": round(random.uniform(100, 120), 1),
            "points_against_per_game": round(random.uniform(95, 115), 1),
            "division_rank": random.randint(1, 5),
            "conference_rank": random.randint(1, 15),
            "key_players": [
                {"name": f"{team}球星1", "status": random.choice(['active', 'injured', 'doubtful'])},
                {"name": f"{team}球星2", "status": random.choice(['active', 'injured', 'doubtful'])}
            ]
        }

    def _generate_football_stats(self, team: str, is_home: bool) -> Dict:
        """生成足球统计数据（模拟）"""
        base_win_rate = random.uniform(0.3, 0.65)
        home_advantage = 0.08 if is_home else 0

        return {
            "team": team,
            "season_win_rate": round(base_win_rate, 3),
            "draw_rate": round(random.uniform(0.2, 0.35), 3),
            "home_win_rate": round(base_win_rate + home_advantage, 3),
            "away_win_rate": round(base_win_rate - home_advantage, 3),
            "recent_5_games": [random.choice(['W', 'D', 'L']) for _ in range(5)],
            "goals_per_game": round(random.uniform(1.0, 2.5), 2),
            "goals_against_per_game": round(random.uniform(0.8, 2.0), 2),
            "league_position": random.randint(1, 20),
            "points": random.randint(30, 80),
            "key_players": [
                {"name": f"{team}核心球员1", "status": random.choice(['active', 'injured', 'doubtful'])},
                {"name": f"{team}核心球员2", "status": random.choice(['active', 'injured', 'doubtful'])}
            ]
        }

    def _collect_head_to_head(self, sport: str, team1: str, team2: str) -> Dict:
        """收集历史对战记录"""
        # 模拟历史对战
        num_games = random.randint(5, 10)
        results = [random.choice(['team1', 'team2', 'draw' if sport.lower() != 'nba' else None])
                   for _ in range(num_games)]

        team1_wins = sum(1 for r in results if r == 'team1')
        team2_wins = sum(1 for r in results if r == 'team2')
        draws = sum(1 for r in results if r == 'draw')

        return {
            "total_games": num_games,
            "team1_wins": team1_wins,
            "team2_wins": team2_wins,
            "draws": draws,
            "team1_win_rate": round(team1_wins / num_games, 3) if num_games > 0 else 0,
            "recent_form": results[-5:]
        }

    def _collect_odds(self, sport: str, team1: str, team2: str) -> Dict:
        """收集赔率数据"""
        # 模拟多个博彩公司的赔率
        bookmakers = ["威廉希尔", "立博", "Bet365", "平博", "10Bet"]

        odds_data = {}

        for bookie in bookmakers:
            if sport.lower() == 'nba':
                odds_data[bookie] = {
                    "team1": round(random.uniform(1.5, 3.0), 2),
                    "team2": round(random.uniform(1.3, 2.8), 2),
                    "spread": round(random.uniform(-8, 8), 1)
                }
            else:
                odds_data[bookie] = {
                    "team1": round(random.uniform(1.5, 4.0), 2),
                    "draw": round(random.uniform(3.0, 4.5), 2),
                    "team2": round(random.uniform(1.3, 5.0), 2),
                    "over_2_5": round(random.uniform(1.7, 2.2), 2),
                    "under_2_5": round(random.uniform(1.6, 2.1), 2)
                }

        # 计算平均赔率
        avg_odds = self._calculate_average_odds(odds_data)

        return {
            "bookmakers": odds_data,
            "average": avg_odds
        }

    def _calculate_average_odds(self, odds_data: Dict) -> Dict:
        """计算平均赔率"""
        # 简化版：取第一个bookmaker的结构
        first_key = list(odds_data.keys())[0]
        avg = {}

        for key in odds_data[first_key].keys():
            values = [odds_data[bookie][key] for bookie in odds_data]
            avg[key] = round(sum(values) / len(values), 2)

        return avg

    def _collect_injuries(self, sport: str, team1: str, team2: str) -> Dict:
        """收集伤病信息"""
        injuries = {}

        for team in [team1, team2]:
            num_injuries = random.randint(0, 3)
            team_injuries = []

            for i in range(num_injuries):
                team_injuries.append({
                    "player": f"{team}球员{i+1}",
                    "position": random.choice(['前锋', '中锋', '后卫'] if sport.lower() == 'nba' else ['前锋', '中场', '后卫', '门将']),
                    "injury_type": random.choice(['脚踝扭伤', '膝盖问题', '背部问题', '生病', '停赛']),
                    "status": random.choice(['缺阵', '存疑', '可能出战']),
                    "expected_return": random.choice([None, '1周后', '2周后', '1月后'])
                })

            injuries[team] = team_injuries

        return injuries

    def extract_features(self, match_data: Dict) -> Dict:
        """
        提取特征

        Args:
            match_data: 比赛数据

        Returns:
            特征字典
        """
        team1_stats = match_data.get('team1_stats', {})
        team2_stats = match_data.get('team2_stats', {})
        h2h = match_data.get('h2h', {})
        injuries = match_data.get('injuries', {})

        features = {
            # 基础实力对比
            "strength_diff": team1_stats.get('season_win_rate', 0.5) - team2_stats.get('season_win_rate', 0.5),

            # 主客场优势
            "home_advantage": team1_stats.get('home_win_rate', 0.5) - team2_stats.get('away_win_rate', 0.5),

            # 近期状态
            "team1_recent_form": self._calculate_recent_form(team1_stats.get('recent_5_games', [])),
            "team2_recent_form": self._calculate_recent_form(team2_stats.get('recent_5_games', [])),

            # 历史对战优势
            "h2h_advantage": h2h.get('team1_win_rate', 0.5) - h2h.get('team2_win_rate', 0.5),

            # 伤病影响
            "team1_injury_impact": len([i for i in injuries.get(match_data['team1'], []) if i['status'] in ['缺阵', '存疑']]),
            "team2_injury_impact": len([i for i in injuries.get(match_data['team2'], []) if i['status'] in ['缺阵', '存疑']]),

            # 赔率隐含概率
            "implied_prob_team1": self._odds_to_prob(match_data.get('odds', {}).get('average', {}), 'team1'),
            "implied_prob_team2": self._odds_to_prob(match_data.get('odds', {}).get('average', {}), 'team2'),
        }

        return features

    def _calculate_recent_form(self, recent_games: List) -> float:
        """计算近期状态得分"""
        if not recent_games:
            return 0.5

        wins = sum(1 for g in recent_games if g == 'W')
        draws = sum(1 for g in recent_games if g == 'D')

        # 胜利得1分，平局得0.5分，输球得0分
        score = (wins * 1 + draws * 0.5) / len(recent_games)
        return round(score, 3)

    def _odds_to_prob(self, odds: Dict, team: str) -> float:
        """将赔率转换为隐含概率"""
        team_odds = odds.get(team, 2.0)
        # 简化版：不考虑博彩公司抽水
        return round(1 / team_odds, 3) if team_odds > 0 else 0.5

    def save_match_data(self, match_data: Dict):
        """保存比赛数据"""
        data_file = os.path.join(
            self.data_dir,
            f"match_{match_data.get('sport', 'unknown')}_{match_data.get('timestamp', datetime.now().timestamp())}.json"
        )

        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(match_data, f, indent=2, ensure_ascii=False)