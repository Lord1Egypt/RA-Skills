"""
Pi-Rating 足球评分系统
计算主客队进攻/防守评分，预测胜负平概率
"""
import math


class PiRating:
    """Pi-Rating 评分系统"""

    def __init__(self, home_adv=0.05):
        self.home_adv = home_adv  # 主场优势参数

    def calc_expected_score(self, home_att, home_def, away_att, away_def, home_adv=None):
        """计算预期得失分"""
        if home_adv is None:
            home_adv = self.home_adv
        expected_home = home_att - away_def + home_adv
        expected_away = away_att - home_def
        return max(expected_home, 0), max(expected_away, 0)

    def score_to_prob(self, home_exp, away_exp):
        """基于Poisson分布将预期得分转为胜平负概率"""
        # 简化为：主队得分期望 > 客队+0.3 → 胜，< -0.3 → 负，否则平
        diff = home_exp - away_exp
        if diff > 0.3:
            p_win = 0.45 + 0.35 * min(diff / 2.0, 1.0)
            p_draw = 0.28 - 0.1 * min(diff / 2.0, 1.0)
        elif diff < -0.3:
            p_win = 0.20 + 0.30 * max(diff / 2.0, -1.0)
            p_draw = 0.28 - 0.1 * max(diff / 2.0, -1.0)
        else:
            # 接近时平局概率升高
            spread = abs(diff) / 0.3
            p_draw = 0.35 + 0.10 * (1 - spread)
            p_win = (1 - p_draw) / 2 + diff * 0.15

        p_win = max(0.15, min(0.65, p_win))
        p_draw = max(0.15, min(0.45, p_draw))
        p_lose = 1 - p_win - p_draw
        p_lose = max(0.10, min(0.55, p_lose))
        # 归一化
        total = p_win + p_draw + p_lose
        return p_win / total, p_draw / total, p_lose / total

    def fit_team_ratings(self, matches, iterations=10):
        """
        根据历史比赛拟合球队评分
        matches: [(home_team, away_team, home_goals, away_goals), ...]
        返回: {team: (attack, defense)}
        """
        teams = sorted(set(t for m in matches for t in (m[0], m[1])))
        ratings = {t: (1.0, 1.0) for t in teams}

        for _ in range(iterations):
            for home, away, hg, ag in matches:
                # 更新主队进攻/客队防守
                exp_h, exp_a = self.calc_expected_score(
                    ratings[home][0], ratings[home][1],
                    ratings[away][0], ratings[away][1]
                )
                # 实际进球与预期差值
                err_h = hg - exp_h
                err_a = ag - exp_a
                lr = 0.1
                r = ratings[home]
                ratings[home] = (r[0] + lr * err_h * 0.5, r[1] - lr * err_a * 0.3)
                r = ratings[away]
                ratings[away] = (r[0] - lr * err_h * 0.3, r[1] + lr * err_a * 0.5)

        return ratings

    def predict(self, home_team, away_team, ratings, home_adv=None):
        """预测单场比赛，返回 (胜率, 平率, 负率)"""
        h_att, h_def = ratings.get(home_team, (1.0, 1.0))
        a_att, a_def = ratings.get(away_team, (1.0, 1.0))
        exp_h, exp_a = self.calc_expected_score(h_att, h_def, a_att, a_def, home_adv)
        return self.score_to_prob(exp_h, exp_a)
