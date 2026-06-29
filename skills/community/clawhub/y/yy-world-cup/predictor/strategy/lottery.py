"""
中国体彩足球竞猜策略引擎
封装胜平负、让球、比分、总进球、半全场5种玩法
"""

from typing import Dict, List, Tuple
from ..data.models import PredictionResult, BettingStrategy


class LotteryStrategyEngine:
    """体彩策略引擎基类"""

    # 赔率计算参考表（基于真实体彩赔率经验）
    # 概率→赔率的反向映射：保留庄家利润约15-20%
    PROB_TO_ODDS = [
        (0.90, 1.05), (0.85, 1.10), (0.80, 1.15), (0.75, 1.20), (0.70, 1.30),
        (0.65, 1.40), (0.60, 1.50), (0.55, 1.65), (0.50, 1.80), (0.45, 2.00),
        (0.40, 2.25), (0.35, 2.60), (0.30, 3.00), (0.25, 3.60), (0.20, 4.50),
        (0.15, 6.00), (0.10, 9.00), (0.05, 18.00), (0.02, 40.00),
    ]

    @staticmethod
    def prob_to_odds(prob: float) -> float:
        """
        概率转换为参考赔率
        修复了之前prob_to_odds字典的bug（之前用dict[key]查找总返回20.0）
        """
        if prob >= 0.90:
            return 1.05
        if prob <= 0.02:
            return 40.00

        # 线性插值查找
        for i in range(len(LotteryStrategyEngine.PROB_TO_ODDS) - 1):
            p1, o1 = LotteryStrategyEngine.PROB_TO_ODDS[i]
            p2, o2 = LotteryStrategyEngine.PROB_TO_ODDS[i + 1]
            if p1 >= prob >= p2:
                # 线性插值
                ratio = (p1 - prob) / (p1 - p2) if p1 != p2 else 0
                return round(o1 + (o2 - o1) * ratio, 2)

        return 1.05  # 默认

    @staticmethod
    def get_winner_outcome(win_prob: float, draw_prob: float, loss_prob: float) -> str:
        """获取概率最高的胜平负结果"""
        max_prob = max(win_prob, draw_prob, loss_prob)
        if max_prob == win_prob:
            return "主胜"
        elif max_prob == draw_prob:
            return "平局"
        else:
            return "客胜"

    @staticmethod
    def get_winner_prob(win_prob: float, draw_prob: float, loss_prob: float) -> float:
        """获取胜平负最高概率"""
        return max(win_prob, draw_prob, loss_prob)

    def create_win_draw_loss_strategy(
        self, prediction: PredictionResult
    ) -> Dict:
        """创建胜平负玩法推荐"""
        outcome = self.get_winner_outcome(
            prediction.home_win_prob, prediction.draw_prob, prediction.away_win_prob
        )
        prob = self.get_winner_prob(
            prediction.home_win_prob, prediction.draw_prob, prediction.away_win_prob
        )
        return {
            "玩法": "胜平负",
            "投注选项": outcome,
            "概率": f"{prob*100:.1f}%",
            "参考赔率": self.prob_to_odds(prob),
        }

    def create_total_goals_strategy(
        self, prediction: PredictionResult
    ) -> List[Dict]:
        """创建总进球数玩法推荐（取最高概率的2个）"""
        strategies = []
        for goals, prob in prediction.total_goals_prob[:2]:
            strategies.append({
                "玩法": "总进球数",
                "投注选项": str(goals),
                "概率": f"{prob*100:.1f}%",
                "参考赔率": self.prob_to_odds(prob),
            })
        return strategies

    def create_score_strategy(
        self, prediction: PredictionResult
    ) -> Dict:
        """创建比分玩法推荐（最可能比分）"""
        score, prob = prediction.predicted_scores[0]
        return {
            "玩法": "比分",
            "投注选项": score,
            "概率": f"{prob*100:.1f}%",
            "参考赔率": self.prob_to_odds(prob),
        }

    def create_ht_ft_strategy(
        self, prediction: PredictionResult
    ) -> Dict:
        """创建半全场玩法推荐（最高概率组合）"""
        best_combo = max(prediction.ht_ft_probs.items(), key=lambda x: x[1])
        return {
            "玩法": "半全场",
            "投注选项": best_combo[0],
            "概率": f"{best_combo[1]*100:.1f}%",
            "参考赔率": self.prob_to_odds(best_combo[1]),
        }

    def create_handicap_strategy(
        self, prediction: PredictionResult, handicap: float = 0
    ) -> Dict:
        """
        创建让球胜平负策略
        Args:
            prediction: 预测结果
            handicap: 让球数（正数让主队，负数让客队）
        """
        # 简化处理：根据让球调整概率
        if handicap > 0:
            # 让主队
            adjusted_win = prediction.home_win_prob * 0.7
            adjusted_draw = prediction.draw_prob * 1.1
            adjusted_loss = prediction.away_win_prob * 1.2
        else:
            # 让客队
            adjusted_win = prediction.home_win_prob * 1.2
            adjusted_draw = prediction.draw_prob * 1.1
            adjusted_loss = prediction.away_win_prob * 0.7

        total = adjusted_win + adjusted_draw + adjusted_loss
        adjusted_win /= total
        adjusted_draw /= total
        adjusted_loss /= total

        outcome = self.get_winner_outcome(adjusted_win, adjusted_draw, adjusted_loss)
        prob = self.get_winner_prob(adjusted_win, adjusted_draw, adjusted_loss)
        handicap_str = f"主队让{abs(handicap)}球" if handicap > 0 else f"客队让{abs(handicap)}球"

        return {
            "玩法": f"让球胜平负（{handicap_str}）",
            "投注选项": outcome,
            "概率": f"{prob*100:.1f}%",
            "参考赔率": self.prob_to_odds(prob),
        }
