"""
分析阶段契约 — Pydantic v2
───────────────────────────
定义分析阶段(NLP + LLM + 可信度)的输入输出严格类型。
这是 Phase 1 核心新增：让 analyzer 的裸 dict 出口变成契约锁死。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional, Literal


class NLPResults(BaseModel):
    """NLP 分析结果"""
    keywords: list[str] = Field(default_factory=list, description="关键词")
    entities: dict[str, list[str]] = Field(
        default_factory=lambda: {"人物": [], "地点": [], "机构": [], "时间": []},
        description="实体识别结果",
    )
    summary: str = Field(default="", description="文本摘要")
    text_length: int = Field(default=0, ge=0, description="原文长度")

    @field_validator("summary")
    @classmethod
    def summary_should_be_meaningful(cls, v: str, info) -> str:
        if info.data.get("text_length", 0) > 100 and len(v.strip()) < 10:
            raise ValueError(f"summary too short for {info.data['text_length']} chars of text")
        return v


class CredibilityScore(BaseModel):
    """单条来源可信度评分"""
    url: str = Field(..., description="URL")
    title: str = Field(default="", description="标题")
    domain_score: int = Field(ge=1, le=5, description="域名权威性(1-5)")
    content_score: int = Field(ge=1, le=5, description="内容质量(1-5)")
    total_score: float = Field(ge=0.0, le=5.0, description="综合评分")
    level: Literal["高可信", "中等可信", "低可信", "存疑"] = Field(default="中等可信", description="可信度等级")


class CredibilityResults(BaseModel):
    """可信度评分汇总"""
    scores: list[CredibilityScore] = Field(default_factory=list, description="逐项评分")
    high: int = Field(default=0, ge=0, description="高可信数量")
    medium: int = Field(default=0, ge=0, description="中等可信数量")
    low: int = Field(default=0, ge=0, description="低可信数量")
    dubious: int = Field(default=0, ge=0, description="存疑数量")
    average_score: float = Field(default=0.0, ge=0.0, le=5.0, description="平均可信度")

    @field_validator("average_score")
    @classmethod
    def average_must_match_scores(cls, v: float, info) -> float:
        scores = info.data.get("scores", [])
        if scores:
            expected = round(
                sum(s.total_score if hasattr(s, 'total_score') else s.get("total_score", 0)
                    for s in scores) / len(scores), 2
            )
            if abs(v - expected) > 0.01:
                raise ValueError(f"average_score ({v}) does not match computed avg ({expected})")
        return v


class SentimentResult(BaseModel):
    """情感分析结果"""
    overall: Literal["正面", "负面", "中性"] = Field(default="中性", description="整体倾向")
    positive_count: int = Field(default=0, ge=0, description="正面关键词数")
    negative_count: int = Field(default=0, ge=0, description="负面关键词数")


class CrossValidationResult(BaseModel):
    """交叉验证结果"""
    consistent: list[str] = Field(default_factory=list, description="一致的内容")
    divergent: list[str] = Field(default_factory=list, description="分歧的内容")
    unverified: list[str] = Field(default_factory=list, description="待核实的内容")
    total_sources: int = Field(default=0, ge=0, description="总来源数")


class LLMAnalysis(BaseModel):
    """LLM 分析结果"""
    key_findings: list[str] = Field(default_factory=list, description="关键发现")
    cross_validation: CrossValidationResult = Field(
        default_factory=CrossValidationResult, description="交叉验证"
    )
    sentiment: SentimentResult = Field(
        default_factory=SentimentResult, description="情感分析"
    )
    conclusions: list[str] = Field(default_factory=list, description="结论")
    provider: str = Field(default="rule_based", description="使用的Provider")


class SourceEntry(BaseModel):
    """来源条目"""
    source: str = Field(default="未知", description="来源引擎")
    title: str = Field(default="无标题", description="标题")
    url: str = Field(default="", description="URL")
    trust_level: float = Field(default=2.0, ge=0.0, le=5.0, description="可信度")
    date: str = Field(default="N/A", description="日期")


class AnalysisOutput(BaseModel):
    """
    分析阶段输出 — 传给报告阶段的唯一合法格式

    任何不符合此契约的分析结果在出口处就被拦截。
    这是 Phase 1 的核心产物：锁死分析阶段的数据格式。
    """
    query: str = Field(..., min_length=1, max_length=500, description="原始查询")
    nlp_results: NLPResults = Field(default_factory=NLPResults, description="NLP分析结果")
    credibility_scores: CredibilityResults = Field(
        default_factory=CredibilityResults, description="可信度评分"
    )
    llm_analysis: LLMAnalysis = Field(
        default_factory=LLMAnalysis, description="LLM分析结果"
    )
    decision_framework: str = Field(default="系统思维", description="决策框架")
    key_findings: list[str] = Field(default_factory=list, description="关键发现")
    entities: dict[str, list[str]] = Field(
        default_factory=lambda: {"人物": [], "地点": [], "机构": [], "时间": []},
        description="实体",
    )
    sentiment: SentimentResult = Field(
        default_factory=SentimentResult, description="情感分析"
    )
    cross_validation: CrossValidationResult = Field(
        default_factory=CrossValidationResult, description="交叉验证"
    )
    conclusions: list[str] = Field(default_factory=list, description="结论")
    sources: list[SourceEntry] = Field(default_factory=list, description="来源列表")
    status: Literal["complete", "partial", "failed"] = Field(
        default="complete", description="分析状态"
    )
    errors: list[str] = Field(default_factory=list, description="错误")
    warnings: list[str] = Field(default_factory=list, description="警告")

    @model_validator(mode='after')
    def validate_status_consistency(self):
        """确保 status=complete 时 key_findings 和 conclusions 非空"""
        if self.status == "complete":
            if not self.key_findings:
                raise ValueError("status=complete but key_findings is empty")
            if not self.conclusions:
                raise ValueError("status=complete but conclusions is empty")
        return self

    @field_validator("sources")
    @classmethod
    def sources_have_valid_urls(cls, v: list[SourceEntry], info) -> list[SourceEntry]:
        for s in v:
            if s.url and not s.url.startswith(("http://", "https://")):
                raise ValueError(f"Invalid URL in source: {s.url}")
        return v
