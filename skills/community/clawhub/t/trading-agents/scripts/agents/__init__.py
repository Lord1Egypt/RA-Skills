"""智能体模块

基于 AgentScope 框架实现:
- 分析师团队: 使用 ReActAgent 自主调用工具
- 研究员团队: 使用 AgentBase 实现辩论机制
- 交易员/风控/经理: LLM 驱动的决策智能体
"""

# 分析师（AgentScope ReActAgent）
from .analysts import (
    MarketAnalystAgent,
    FundamentalsAnalystAgent,
    NewsAnalystAgent,
    create_analyst_team,
)

# 研究员（AgentScope AgentBase）
from .researchers import (
    BullishResearcherAgent,
    BearishResearcherAgent,
    ResearchFacilitatorAgent,
    create_research_team,
)

# 交易员
from .trader import Trader

# 风险管理团队
from .risk_managers import (
    AggressiveRisk, 
    NeutralRisk, 
    ConservativeRisk, 
    RiskFacilitator,
)

# 基金经理
from .manager import Manager

__all__ = [
    # 分析师
    "MarketAnalystAgent",
    "FundamentalsAnalystAgent",
    "NewsAnalystAgent",
    "create_analyst_team",
    
    # 研究员
    "BullishResearcherAgent",
    "BearishResearcherAgent",
    "ResearchFacilitatorAgent",
    "create_research_team",
    
    # 交易与风控
    "Trader",
    "AggressiveRisk",
    "NeutralRisk",
    "ConservativeRisk",
    "RiskFacilitator",
    "Manager",
]
