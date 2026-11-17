"""
LLM 分析契约 — Pydantic v2
───────────────────────────
定义 LLM 分析阶段的输入输出严格类型。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional, Literal


class LLMProvider(str, Enum):
    OLLAMA = "ollama"
    GATEWAY = "gateway"
    DEEPSEEK = "deepseek"
    DASHSCOPE = "dashscope"
    NONE = "none"


class LLMRequest(BaseModel):
    """LLM 分析请求"""
    query: str = Field(..., min_length=1, max_length=500, description="查询")
    content: str = Field(..., description="待分析内容")
    provider: Optional[LLMProvider] = Field(default=None, description="指定Provider(不指定则自动发现)")
    max_tokens: int = Field(default=2000, ge=100, le=16000, description="最大token数")
    temperature: float = Field(default=0.3, ge=0.0, le=2.0, description="温度")

    @field_validator("content")
    @classmethod
    def content_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("分析内容不能为空")
        return v


class ProviderStatus(BaseModel):
    """Provider 状态"""
    provider: LLMProvider = Field(..., description="Provider名称")
    available: bool = Field(default=False, description="是否可用")
    error: str = Field(default="", description="错误信息")
    latency_ms: float = Field(default=0.0, description="延迟(毫秒)")


class FallbackChain(BaseModel):
    """降级链 — Provider 优先级列表"""
    providers: list[LLMProvider] = Field(
        default_factory=lambda: [
            LLMProvider.OLLAMA,
            LLMProvider.GATEWAY,
            LLMProvider.DEEPSEEK,
            LLMProvider.DASHSCOPE,
            LLMProvider.NONE,
        ],
        description="Provider优先级(从高到低)"
    )
    current_provider: LLMProvider = Field(default=LLMProvider.NONE, description="当前使用的Provider")


class CrossValidation(BaseModel):
    """多源交叉验证结果"""
    consistent: list[str] = Field(default_factory=list, description="一致的内容")
    divergent: list[str] = Field(default_factory=list, description="分歧的内容")
    unverified: list[str] = Field(default_factory=list, description="待核实的内容")
    total_sources: int = Field(default=0, ge=0, description="总来源数")


class SentimentAnalysis(BaseModel):
    """情感分析结果"""
    overall: Literal["正面", "负面", "中性"] = Field(default="中性", description="整体倾向")
    positive_count: int = Field(default=0, ge=0, description="正面关键词数")
    negative_count: int = Field(default=0, ge=0, description="负面关键词数")
    confidence: float = Field(default=0.5, ge=0.0, le=1.0, description="置信度")


class LLMResponse(BaseModel):
    """LLM 分析响应"""
    provider: LLMProvider = Field(..., description="使用的Provider")
    key_findings: list[str] = Field(default_factory=list, description="关键发现")
    cross_validation: CrossValidation = Field(default_factory=CrossValidation, description="交叉验证")
    sentiment: SentimentAnalysis = Field(default_factory=SentimentAnalysis, description="情感分析")
    conclusions: list[str] = Field(default_factory=list, description="结论")
    summary: str = Field(default="", description="摘要")
    tokens_used: int = Field(default=0, ge=0, description="消耗的token数")
    fallback_used: bool = Field(default=False, description="是否使用了降级方案")
