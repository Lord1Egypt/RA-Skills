"""
M4: 综合评分模块
计算最终评分与阅读价值建议
"""

from typing import Dict, Tuple


class QualityScorer:
    """综合评分计算器"""

    GRADE_THRESHOLDS = {
        "A+": (90, 100),
        "A":  (80, 89),
        "B+": (70, 79),
        "B":  (60, 69),
        "C":  (40, 59),
        "D":  (0, 39)
    }

    TYPE_ADVICE = {
        "technical_article": {
            "target_audience": "技术从业者、开发者、学生",
            "time_range": "5-30分钟",
            "verdict_templates": {
                "A+": "极力推荐！深入透彻，实操性强，值得反复研读",
                "A":  "强烈推荐！内容扎实，适合认真阅读",
                "B+": "推荐阅读，观点有价值，适合目标读者",
                "B":  "可读性不错，碎片时间可看",
                "C":  "一般性内容，可选择性阅读",
                "D":  "不推荐，内容浅薄或存在错误"
            }
        },
        "essay": {
            "target_audience": "文学爱好者、情感需求者",
            "time_range": "3-15分钟",
            "verdict_templates": {
                "A+": "极力推荐！情感真挚，文笔优美，令人动容",
                "A":  "强烈推荐！情感丰富，值得一读",
                "B+": "推荐阅读，有感人之处",
                "B":  "可读性不错，可休闲阅读",
                "C":  "一般性内容，可略读",
                "D":  "不推荐，情感表达不足"
            }
        },
        "novel": {
            "target_audience": "小说读者、文学爱好者",
            "time_range": "30分钟-数小时",
            "verdict_templates": {
                "A+": "极力推荐！情节引人入胜，人物立体，令人沉浸",
                "A":  "强烈推荐！故事精彩，值得细读",
                "B+": "推荐阅读，有亮点可看",
                "B":  "可读性不错，可休闲阅读",
                "C":  "一般性内容，可略读",
                "D":  "不推荐，情节或人物塑造不足"
            }
        },
        "other": {
            "target_audience": "普通读者",
            "time_range": "5-20分钟",
            "verdict_templates": {
                "A+": "极力推荐！内容优秀，值得阅读",
                "A":  "强烈推荐！有阅读价值",
                "B+": "推荐阅读，内容有价值",
                "B":  "可读性不错",
                "C":  "一般性内容",
                "D":  "不推荐"
            }
        }
    }

    TYPE_MATCH_BONUS = {
        "technical_article": {"key_dims": ["technical_depth", "practicality"], "bonus": 0.10},
        "essay": {"key_dims": ["emotion_expression", "resonance"], "bonus": 0.10},
        "novel": {"key_dims": ["plot_structure", "character_craft"], "bonus": 0.10}
    }

    def calculate_overall_score(
        self,
        dimension_scores: Dict[str, float],
        weights: Dict[str, float],
        ai_probability: float,
        article_type: str
    ) -> Tuple[int, str, Dict]:
        """
        计算综合评分

        Args:
            dimension_scores: 各维度得分
            weights: 各维度权重
            ai_probability: AI生成概率 (0-1)
            article_type: 文章类型

        Returns:
            (overall_score, grade, breakdown)
        """
        # 加权求和
        weighted_sum = sum(
            dimension_scores.get(dim, 0) * weights.get(dim, 0)
            for dim in weights
        )

        # 类型匹配加成
        type_match_bonus = self._calc_type_match_bonus(article_type, dimension_scores)

        # AI惩罚
        ai_penalty = ai_probability * 0.3

        # 最终评分
        final_score = max(0, min(100,
            weighted_sum * (1 + type_match_bonus) * (1 - ai_penalty)
        ))

        grade = self._get_grade(final_score)

        breakdown = {
            "weighted_base": round(weighted_sum, 1),
            "type_bonus": round(type_match_bonus * 100, 1),
            "ai_penalty": round(ai_penalty * 100, 1),
            "final_score": round(final_score, 0)
        }

        return int(round(final_score)), grade, breakdown

    def generate_reading_advice(
        self,
        article_type: str,
        grade: str,
        dimension_scores: Dict[str, float],
        content: str = ""
    ) -> Dict:
        """
        生成阅读价值建议
        """
        type_info = self.TYPE_ADICE.get(article_type, self.TYPE_ADVICE["other"])
        verdict = type_info["verdict_templates"].get(grade, "一般性内容")

        # 关键收益点 (TOP3 维度)
        top_dims = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        key_benefits = [self._dim_to_benefit(d[0], d[1]) for d in top_dims if d[1] >= 70]

        # 适合阅读场景
        suitable_moments = self._get_suitable_moments(grade)

        return {
            "verdict": verdict,
            "target_audience": type_info["target_audience"],
            "time_estimation": type_info["time_range"],
            "key_benefits": key_benefits or ["内容有价值"],
            "suitable_moments": suitable_moments
        }

    def _calc_type_match_bonus(self, article_type: str, scores: Dict[str, float]) -> float:
        """计算类型匹配加成"""
        match_info = self.TYPE_MATCH_BONUS.get(article_type)
        if not match_info:
            return 0.05

        key_dims = match_info["key_dims"]
        avg_key_score = sum(scores.get(d, 0) for d in key_dims) / len(key_dims)

        if avg_key_score >= 85:
            return match_info["bonus"]
        elif avg_key_score >= 70:
            return match_info["bonus"] * 0.5
        return 0

    def _get_grade(self, score: float) -> str:
        """获取评分等级"""
        for grade, (low, high) in self.GRADE_THRESHOLDS.items():
            if low <= score <= high:
                return grade
        return "D"

    def _dim_to_benefit(self, dimension: str, score: float) -> str:
        """维度转收益描述"""
        benefits = {
            "technical_depth": f"技术深入透彻({score:.0f}分)",
            "structure": f"结构清晰有序({score:.0f}分)",
            "practicality": f"实操性强({score:.0f}分)",
            "originality": f"观点独特有见地({score:.0f}分)",
            "readability": f"表达流畅易读({score:.0f}分)",
            "emotion_expression": f"情感表达真挚({score:.0f}分)",
            "writing_style": f"文笔优美({score:.0f}分)",
            "narrative_structure": f"叙事结构巧妙({score:.0f}分)",
            "creativity": f"创意新颖({score:.0f}分)",
            "resonance": f"令人产生共鸣({score:.0f}分)",
            "plot_structure": f"情节结构优秀({score:.0f}分)",
            "character_craft": f"人物塑造立体({score:.0f}分)",
            "narrative_technique": f"叙事技巧娴熟({score:.0f}分)",
            "style_features": f"文风独特({score:.0f}分)",
            "world_building": f"世界观构建完善({score:.0f}分)"
        }
        return benefits.get(dimension, f"{dimension}({score:.0f}分)")

    def _get_suitable_moments(self, grade: str) -> list:
        """获取适合阅读场景"""
        if grade in ["A+", "A"]:
            return ["专注阅读", "深度学习", "收藏反复看"]
        elif grade in ["B+", "B"]:
            return ["休闲阅读", "通勤时间", "碎片时间"]
        else:
            return ["随意浏览"]


# 修正: TYPE_ADVICE 拼写
QualityScorer.TYPE_ADICE = QualityScorer.TYPE_ADVICE
