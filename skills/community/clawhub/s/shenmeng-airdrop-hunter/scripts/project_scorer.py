#!/usr/bin/env python3
"""
空投项目评分工具
根据多维度标准评估空投项目价值
"""

from dataclasses import dataclass
from typing import List, Dict
from enum import Enum

class RiskLevel(Enum):
    LOW = "低风险"
    MEDIUM = "中风险"
    HIGH = "高风险"
    EXTREME = "极高风险"

@dataclass
class ProjectScore:
    """项目评分结果"""
    name: str
    funding_score: int
    narrative_score: int
    certainty_score: int
    cost_score: int
    total_score: int
    risk_level: RiskLevel
    tier: str
    recommendation: str

class AirdropScorer:
    """空投项目评分器"""
    
    # 投资机构评分
    INVESTOR_TIERS = {
        "Binance Labs": 3, "Polychain": 3, "Sequoia": 3,
        "a16z": 3, "Paradigm": 3, "Coinbase Ventures": 2,
        "Hack VC": 2, "Jump Crypto": 2, "Multicoin": 2,
        "Dragonfly": 2, "Delphi Digital": 2, "Hashed": 1,
    }
    
    def __init__(self):
        self.projects = []
    
    def calculate_funding_score(
        self,
        funding_amount: float,  # 百万美元
        investors: List[str]
    ) -> int:
        """计算融资评分"""
        score = 0
        
        # 融资额评分
        if funding_amount >= 100:
            score += 6
        elif funding_amount >= 50:
            score += 5
        elif funding_amount >= 30:
            score += 4
        elif funding_amount >= 10:
            score += 3
        elif funding_amount >= 5:
            score += 2
        else:
            score += 1
        
        # 投资机构评分
        investor_score = 0
        for inv in investors:
            for tier_inv, tier_score in self.INVESTOR_TIERS.items():
                if tier_inv.lower() in inv.lower():
                    investor_score = max(investor_score, tier_score)
        
        score += investor_score
        return min(score, 10)  # 最高10分
    
    def calculate_narrative_score(
        self,
        is_new_narrative: bool = False,
        is_hot_sector: bool = False,
        has_product: bool = False,
        community_active: bool = False
    ) -> int:
        """计算叙事热度评分"""
        score = 0
        
        if is_new_narrative:
            score += 3
        if is_hot_sector:
            score += 2
        if has_product:
            score += 1
        if community_active:
            score += 1
        
        return min(score, 7)
    
    def calculate_certainty_score(
        self,
        official_confirmed: bool = False,
        has_points_system: bool = False,
        testnet_incentivized: bool = False
    ) -> int:
        """计算空投确定性评分"""
        score = 0
        
        if official_confirmed:
            score += 3
        if has_points_system:
            score += 2
        if testnet_incentivized:
            score += 1
        
        return min(score, 6)
    
    def calculate_cost_score(
        self,
        is_testnet: bool = False,
        gas_cost: str = "low",  # low, medium, high
        requires_kyc: bool = False
    ) -> int:
        """计算成本效益评分（越高越好）"""
        score = 0
        
        if is_testnet:
            score += 3
        
        if gas_cost == "low":
            score += 2
        elif gas_cost == "medium":
            score += 1
        
        if not requires_kyc:
            score += 1
        
        return min(score, 6)
    
    def calculate_anti_sybil_risk(
        self,
        has_kyc: bool = False,
        strict_rules: bool = False,
        historical_bans: bool = False
    ) -> int:
        """计算反撸风险分数（越高越危险）"""
        score = 0
        
        if has_kyc:
            score += 3
        if strict_rules:
            score += 2
        if historical_bans:
            score += 2
        
        return score
    
    def evaluate_project(
        self,
        name: str,
        funding_amount: float,
        investors: List[str],
        is_new_narrative: bool = False,
        is_hot_sector: bool = False,
        has_product: bool = False,
        community_active: bool = False,
        official_confirmed: bool = False,
        has_points_system: bool = False,
        testnet_incentivized: bool = False,
        is_testnet: bool = False,
        gas_cost: str = "low",
        requires_kyc: bool = False,
        has_anti_sybil: bool = False,
        strict_rules: bool = False,
        historical_bans: bool = False
    ) -> ProjectScore:
        """完整评估一个项目"""
        
        # 计算各维度得分
        funding_score = self.calculate_funding_score(funding_amount, investors)
        narrative_score = self.calculate_narrative_score(
            is_new_narrative, is_hot_sector, has_product, community_active
        )
        certainty_score = self.calculate_certainty_score(
            official_confirmed, has_points_system, testnet_incentivized
        )
        cost_score = self.calculate_cost_score(is_testnet, gas_cost, requires_kyc)
        
        # 总分（满分30）
        total_score = funding_score + narrative_score + certainty_score + cost_score
        
        # 反撸风险调整
        anti_sybil_risk = self.calculate_anti_sybil_risk(
            requires_kyc, strict_rules, historical_bans
        )
        
        # 风险等级
        if anti_sybil_risk >= 5 or has_anti_sybil:
            risk_level = RiskLevel.EXTREME
        elif anti_sybil_risk >= 3:
            risk_level = RiskLevel.HIGH
        elif anti_sybil_risk >= 1:
            risk_level = RiskLevel.MEDIUM
        else:
            risk_level = RiskLevel.LOW
        
        # 分级
        if total_score >= 22 and risk_level in [RiskLevel.LOW, RiskLevel.MEDIUM]:
            tier = "Tier 1 - 必做"
        elif total_score >= 16:
            tier = "Tier 2 - 推荐"
        elif total_score >= 10:
            tier = "Tier 3 - 关注"
        else:
            tier = "Tier 4 - 观望"
        
        # 建议
        if risk_level == RiskLevel.EXTREME:
            recommendation = "精品号策略（1-2个），深度交互，避免批量"
        elif risk_level == RiskLevel.HIGH:
            recommendation = "少量精品号（3-5个），注意行为差异化"
        elif tier == "Tier 1 - 必做":
            recommendation = "批量操作，但注意防关联"
        else:
            recommendation = "根据自身情况选择参与"
        
        return ProjectScore(
            name=name,
            funding_score=funding_score,
            narrative_score=narrative_score,
            certainty_score=certainty_score,
            cost_score=cost_score,
            total_score=total_score,
            risk_level=risk_level,
            tier=tier,
            recommendation=recommendation
        )
    
    def print_report(self, score: ProjectScore):
        """打印评分报告"""
        print(f"\n{'='*60}")
        print(f"📊 {score.name} 项目评分报告")
        print(f"{'='*60}")
        
        print(f"\n🎯 综合得分: {score.total_score}/30")
        print(f"📈 等级: {score.tier}")
        print(f"⚠️  风险等级: {score.risk_level.value}")
        
        print(f"\n📋 分项得分:")
        print(f"   融资背景: {score.funding_score}/10")
        print(f"   叙事热度: {score.narrative_score}/7")
        print(f"   空投确定性: {score.certainty_score}/6")
        print(f"   成本效益: {score.cost_score}/6")
        
        print(f"\n💡 策略建议: {score.recommendation}")
        print(f"{'='*60}\n")


# 示例项目数据
def demo():
    scorer = AirdropScorer()
    
    # Monad 评分
    monad = scorer.evaluate_project(
        name="Monad",
        funding_amount=244,
        investors=["Paradigm", "Coinbase Ventures", "Electric Capital"],
        is_new_narrative=True,
        is_hot_sector=True,
        has_product=True,
        community_active=True,
        official_confirmed=True,
        has_points_system=True,
        testnet_incentivized=True,
        is_testnet=True,
        gas_cost="low"
    )
    scorer.print_report(monad)
    
    # Sahara AI 评分
    sahara = scorer.evaluate_project(
        name="Sahara AI",
        funding_amount=49,
        investors=["Pantera Capital", "Polychain", "Sequoia"],
        is_new_narrative=True,
        is_hot_sector=True,
        community_active=True,
        official_confirmed=True,
        has_points_system=True,
        is_testnet=True,
        gas_cost="low"
    )
    scorer.print_report(sahara)
    
    # Azuro 评分（高风险）
    azuro = scorer.evaluate_project(
        name="Azuro",
        funding_amount=25,
        investors=["Wintermute", "Gnosis"],
        has_product=True,
        official_confirmed=True,
        has_points_system=True,
        is_testnet=False,
        gas_cost="medium",
        has_anti_sybil=True,
        strict_rules=True,
        historical_bans=True
    )
    scorer.print_report(azuro)


if __name__ == "__main__":
    demo()
