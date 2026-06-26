"""Base class for restaurant cross-checking logic. Shared by all crosscheck variants."""

from typing import List, Dict
from dataclasses import dataclass

from config import SCORING_WEIGHTS, OUTPUT_CONFIG
from match_restaurants import (
    MatchedRestaurant,
    normalize_engagement,
    calculate_consistency
)


@dataclass
class RecommendationResult:
    """Final recommendation with scores. Single definition used everywhere."""
    name: str
    dianping_rating: float
    dianping_reviews: int
    dianping_tags: List[str]
    dianping_address: str
    dianping_price: str
    xhs_engagement_display: str
    xhs_keywords: List[str]
    recommendation_score: float  # 0-10
    consistency_level: str  # "高", "中", "低"
    consistency_score: float  # 0-1
    similarity_score: float  # 0-1, match confidence


class CrossCheckBase:
    """Base logic for recommendation scoring and output formatting."""

    def __init__(self, scoring_weights: Dict = None):
        self.scoring_weights = scoring_weights or SCORING_WEIGHTS

    def calculate_recommendation(self, match: MatchedRestaurant) -> RecommendationResult:
        """Calculate final recommendation score from a matched restaurant."""
        dp = match.dianping_data
        xhs = match.xhs_data

        # Normalize XHS engagement to 0-5 scale
        xhs_rating = normalize_engagement(xhs)

        # Calculate consistency
        consistency = calculate_consistency(
            dp.rating,
            xhs_rating,
            xhs.sentiment_score
        )

        # Calculate recommendation score (0-10)
        raw_score = (
            (dp.rating * self.scoring_weights['dianping_rating']) +
            (xhs_rating * self.scoring_weights['xhs_engagement']) +
            (consistency * 5 * self.scoring_weights['consistency'])
        ) * 2

        # 严格 clamp 到 0-10
        recommendation_score = round(max(0.0, min(10.0, raw_score)), 1)

        # Determine consistency level
        if consistency >= 0.7:
            consistency_level = "高"
        elif consistency >= 0.5:
            consistency_level = "中"
        else:
            consistency_level = "低"

        return RecommendationResult(
            name=dp.name,
            dianping_rating=dp.rating,
            dianping_reviews=dp.review_count,
            dianping_tags=dp.tags,
            dianping_address=dp.address,
            dianping_price=dp.price_range,
            xhs_engagement_display=f"{xhs_rating:.1f}⭐ ({xhs.likes}赞/{xhs.saves}收藏)",
            xhs_keywords=xhs.keywords,
            recommendation_score=recommendation_score,
            consistency_level=consistency_level,
            consistency_score=round(consistency, 2),
            similarity_score=round(match.similarity_score, 2)
        )

    def build_results(self, matches: List[MatchedRestaurant]) -> List[RecommendationResult]:
        """Convert matched restaurants to sorted recommendation results."""
        results = [self.calculate_recommendation(m) for m in matches]
        results.sort(key=lambda x: x.recommendation_score, reverse=True)
        return results

    @staticmethod
    def format_output(
        results: List[RecommendationResult],
        location: str,
        cuisine: str,
        max_restaurants: int = None
    ) -> str:
        """Format results for display."""
        if max_restaurants is None:
            max_restaurants = OUTPUT_CONFIG.get('max_restaurants', 10)

        if not results:
            return f"❌ 未找到符合条件的餐厅: {location} - {cuisine}"

        output = []
        output.append(f"📍 {location} {cuisine} 餐厅推荐\n")
        output.append("=" * 60 + "\n")

        for i, r in enumerate(results[:max_restaurants], 1):
            output.append(f"{i}. {r.name}")
            output.append(f"   🏆 推荐指数: {r.recommendation_score}/10")
            output.append(f"   ⭐ 大众点评: {r.dianping_rating}⭐ ({r.dianping_reviews}评价)")
            output.append(f"   💬 小红书: {r.xhs_engagement_display}")
            output.append(f"   📍 地址: {r.dianping_address}")
            output.append(f"   💰 人均: {r.dianping_price}")
            output.append(f"   ✅ 一致性: {r.consistency_level} ({r.consistency_score:.2f})")

            if OUTPUT_CONFIG.get('show_details', True):
                output.append(f"\n   📊 平台对比:")
                output.append(f"   - 大众点评标签: {', '.join(r.dianping_tags)}")
                output.append(f"   - 小红书热词: {', '.join(r.xhs_keywords)}")

                if r.consistency_level == "低":
                    output.append(f"\n   ⚠️ 注意: 两平台评价差异较大，建议进一步了解")

            output.append("")

        return "\n".join(output)
