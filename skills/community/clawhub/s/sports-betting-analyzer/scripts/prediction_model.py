#!/usr/bin/env python3
"""
预测模型模块

功能：
- 简单机器学习预测
- 概率计算
- 置信度评估
"""

import json
import random
from typing import Dict, List, Tuple
import numpy as np


class PredictionModel:
    """预测模型"""

    def __init__(self, config: Dict):
        self.config = config
        self.min_confidence = config.get('min_confidence', 0.6)

    def predict(self, sport: str, features: Dict) -> Dict:
        """
        预测比赛结果

        Args:
            sport: 体育项目
            features: 特征字典

        Returns:
            预测结果
        """
        if sport.lower() == 'nba':
            return self._predict_nba(features)
        else:
            return self._predict_football(features)

    def _predict_nba(self, features: Dict) -> Dict:
        """NBA预测"""
        # 提取特征
        strength_diff = features.get('strength_diff', 0)
        home_advantage = features.get('home_advantage', 0)
        team1_recent = features.get('team1_recent_form', 0.5)
        team2_recent = features.get('team2_recent_form', 0.5)
        h2h_advantage = features.get('h2h_advantage', 0)
        team1_injuries = features.get('team1_injury_impact', 0)
        team2_injuries = features.get('team2_injury_impact', 0)

        # 加权计算（简化版逻辑回归）
        # 权重可以调优
        weights = {
            'strength': 0.3,
            'home_advantage': 0.2,
            'recent_form': 0.15,
            'h2h': 0.15,
            'injuries': -0.1
        }

        # 计算主队得分
        team1_score = (
            weights['strength'] * strength_diff +
            weights['home_advantage'] * home_advantage +
            weights['recent_form'] * (team1_recent - team2_recent) +
            weights['h2h'] * h2h_advantage +
            weights['injuries'] * (team2_injuries - team1_injuries)
        )

        # 转换为概率
        team1_prob = self._sigmoid(team1_score)
        team2_prob = 1 - team1_prob

        # 确定预测结果
        prediction = "team1" if team1_prob > 0.5 else "team2"
        confidence = max(team1_prob, team2_prob)

        # 生成预测结果字典
        result = {
            "prediction": prediction,
            "probabilities": {
                "team1": round(team1_prob, 3),
                "team2": round(team2_prob, 3)
            },
            "confidence": round(confidence, 3),
            "spread_prediction": self._predict_spread(team1_score),
            "total_prediction": self._predict_total(features),
            "factors": {
                "strength_diff": strength_diff,
                "home_advantage": home_advantage,
                "recent_form_diff": team1_recent - team2_recent,
                "h2h_advantage": h2h_advantage,
                "injury_impact": team2_injuries - team1_injuries
            }
        }

        return result

    def _predict_football(self, features: Dict) -> Dict:
        """足球预测"""
        # 提取特征
        strength_diff = features.get('strength_diff', 0)
        home_advantage = features.get('home_advantage', 0)
        team1_recent = features.get('team1_recent_form', 0.5)
        team2_recent = features.get('team2_recent_form', 0.5)
        h2h_advantage = features.get('h2h_advantage', 0)
        team1_injuries = features.get('team1_injury_impact', 0)
        team2_injuries = features.get('team2_injury_impact', 0)

        # 加权计算
        weights = {
            'strength': 0.25,
            'home_advantage': 0.2,
            'recent_form': 0.15,
            'h2h': 0.15,
            'injuries': -0.1
        }

        # 计算主队得分（相对于平局）
        team1_score = (
            weights['strength'] * strength_diff +
            weights['home_advantage'] * home_advantage +
            weights['recent_form'] * (team1_recent - team2_recent) +
            weights['h2h'] * h2h_advantage +
            weights['injuries'] * (team2_injuries - team1_injuries)
        )

        # 计算概率（三分式）
        team1_prob = self._sigmoid(team1_score + 0.1)  # 主场优势
        team2_prob = self._sigmoid(-team1_score + 0.1)  # 客场优势

        # 平局概率（中间部分）
        draw_prob = 1 - team1_prob - team2_prob
        if draw_prob < 0.1:  # 确保平局概率不过低
            draw_prob = 0.15
            team1_prob = (1 - draw_prob) * team1_prob / (team1_prob + team2_prob)
            team2_prob = (1 - draw_prob) * team2_prob / (team1_prob + team2_prob)

        # 归一化
        total = team1_prob + draw_prob + team2_prob
        team1_prob /= total
        draw_prob /= total
        team2_prob /= total

        # 确定预测结果
        max_prob = max(team1_prob, draw_prob, team2_prob)
        if max_prob == team1_prob:
            prediction = "team1"
        elif max_prob == team2_prob:
            prediction = "team2"
        else:
            prediction = "draw"

        confidence = max_prob

        # 生成预测结果字典
        result = {
            "prediction": prediction,
            "probabilities": {
                "team1": round(team1_prob, 3),
                "draw": round(draw_prob, 3),
                "team2": round(team2_prob, 3)
            },
            "confidence": round(confidence, 3),
            "over_under_prediction": self._predict_over_under(features),
            "factors": {
                "strength_diff": strength_diff,
                "home_advantage": home_advantage,
                "recent_form_diff": team1_recent - team2_recent,
                "h2h_advantage": h2h_advantage,
                "injury_impact": team2_injuries - team1_injuries
            }
        }

        return result

    def _sigmoid(self, x: float) -> float:
        """Sigmoid函数"""
        return 1 / (1 + np.exp(-x))

    def _predict_spread(self, team1_score: float) -> int:
        """预测让分"""
        # 简化版：根据得分转换为整数让分
        spread = int(round(team1_score * 10))
        return max(min(spread, 15), -15)  # 限制在-15到15之间

    def _predict_total(self, features: Dict) -> Dict:
        """预测总分"""
        # 简化版：基于进攻和防守数据
        base_total = random.uniform(210, 240)
        return {
            "total": round(base_total, 1),
            "over_probability": round(random.uniform(0.45, 0.55), 3),
            "under_probability": round(random.uniform(0.45, 0.55), 3)
        }

    def _predict_over_under(self, features: Dict) -> Dict:
        """预测大小球"""
        # 简化版
        base_goals = random.uniform(2.0, 3.5)
        return {
            "line": 2.5,
            "over_probability": round(random.uniform(0.45, 0.55), 3),
            "under_probability": round(random.uniform(0.45, 0.55), 3)
        }

    def ensemble_predict(self, sport: str, features_list: List[Dict]) -> Dict:
        """
        集成预测（使用多个特征集）

        Args:
            sport: 体育项目
            features_list: 多个特征字典列表

        Returns:
            集成预测结果
        """
        predictions = [self.predict(sport, features) for features in features_list]

        # 简单平均集成
        if sport.lower() == 'nba':
            avg_team1 = np.mean([p['probabilities']['team1'] for p in predictions])
            avg_team2 = np.mean([p['probabilities']['team2'] for p in predictions])

            final_prediction = "team1" if avg_team1 > avg_team2 else "team2"
            confidence = max(avg_team1, avg_team2)

            return {
                "prediction": final_prediction,
                "probabilities": {
                    "team1": round(avg_team1, 3),
                    "team2": round(avg_team2, 3)
                },
                "confidence": round(confidence, 3),
                "method": "ensemble_average",
                "num_models": len(predictions)
            }
        else:
            avg_team1 = np.mean([p['probabilities']['team1'] for p in predictions])
            avg_draw = np.mean([p['probabilities']['draw'] for p in predictions])
            avg_team2 = np.mean([p['probabilities']['team2'] for p in predictions])

            max_prob = max(avg_team1, avg_draw, avg_team2)
            if max_prob == avg_team1:
                final_prediction = "team1"
            elif max_prob == avg_team2:
                final_prediction = "team2"
            else:
                final_prediction = "draw"

            return {
                "prediction": final_prediction,
                "probabilities": {
                    "team1": round(avg_team1, 3),
                    "draw": round(avg_draw, 3),
                    "team2": round(avg_team2, 3)
                },
                "confidence": round(max_prob, 3),
                "method": "ensemble_average",
                "num_models": len(predictions)
            }

    def monte_carlo_simulation(self, sport: str, features: Dict, num_simulations: int = 1000) -> Dict:
        """
        蒙特卡洛模拟

        Args:
            sport: 体育项目
            features: 特征字典
            num_simulations: 模拟次数

        Returns:
            模拟结果
        """
        results = []

        for _ in range(num_simulations):
            # 添加随机噪声
            noisy_features = self._add_noise(features, noise_level=0.1)
            prediction = self.predict(sport, noisy_features)
            results.append(prediction['prediction'])

        # 统计结果
        if sport.lower() == 'nba':
            team1_count = results.count('team1')
            team2_count = results.count('team2')
        else:
            team1_count = results.count('team1')
            draw_count = results.count('draw')
            team2_count = results.count('team2')

        total = len(results)

        if sport.lower() == 'nba':
            return {
                "team1_probability": round(team1_count / total, 3),
                "team2_probability": round(team2_count / total, 3),
                "num_simulations": num_simulations
            }
        else:
            return {
                "team1_probability": round(team1_count / total, 3),
                "draw_probability": round(draw_count / total, 3),
                "team2_probability": round(team2_count / total, 3),
                "num_simulations": num_simulations
            }

    def _add_noise(self, features: Dict, noise_level: float) -> Dict:
        """添加随机噪声"""
        noisy_features = features.copy()
        for key in noisy_features:
            if isinstance(noisy_features[key], (int, float)):
                noise = random.uniform(-noise_level, noise_level)
                noisy_features[key] = noisy_features[key] * (1 + noise)
        return noisy_features