"""
NLP 分析契约 — Pydantic v2
───────────────────────────
定义 NLP 分析阶段的输入输出严格类型。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


class NLPAnalysisRequest(BaseModel):
    """NLP 分析请求"""
    text: str = Field(..., min_length=1, description="待分析文本")
    language: str = Field(default="zh", description="语言")
    extract_entities: bool = Field(default=True, description="是否提取实体")
    extract_keywords: bool = Field(default=True, description="是否提取关键词")
    generate_summary: bool = Field(default=True, description="是否生成摘要")
    max_keywords: int = Field(default=20, ge=5, le=100, description="最大关键词数")
    max_summary_length: int = Field(default=500, ge=50, le=2000, description="最大摘要长度")

    @field_validator("text")
    @classmethod
    def text_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("NLP分析文本不能为空")
        return v


class EntityList(BaseModel):
    """实体列表"""
    persons: list[str] = Field(default_factory=list, description="人物")
    locations: list[str] = Field(default_factory=list, description="地点")
    organizations: list[str] = Field(default_factory=list, description="机构")
    dates: list[str] = Field(default_factory=list, description="时间")
    other: list[str] = Field(default_factory=list, description="其他")


class NLPAnalysisOutput(BaseModel):
    """NLP 分析输出"""
    keywords: list[str] = Field(default_factory=list, description="关键词")
    entities: EntityList = Field(default_factory=EntityList, description="实体")
    summary: str = Field(default="", description="文本摘要")
    text_length: int = Field(default=0, ge=0, description="原文长度")
    language_detected: str = Field(default="unknown", description="检测到的语言")
    processing_time_ms: float = Field(default=0.0, ge=0, description="处理耗时(毫秒)")
