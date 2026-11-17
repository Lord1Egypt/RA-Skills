"""
搜索请求契约 — Pydantic v2
───────────────────────────
定义搜索阶段的输入输出严格类型。
任何不符合此契约的数据在入口处就被拦截。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl, field_validator
from enum import Enum
from typing import Optional, Literal
from datetime import datetime


class QueryIntent(str, Enum):
    QUICK = "quick"
    DEEP = "deep"
    COMPARE = "compare"
    VERIFY = "verify"
    MONITOR = "monitor"
    TREND = "trend"


class QueryLanguage(str, Enum):
    ZH = "zh"
    EN = "en"
    AUTO = "auto"


class SearchRequest(BaseModel):
    """搜索请求 — 输入契约"""
    query: str = Field(..., min_length=1, max_length=500, description="搜索查询")
    intent: QueryIntent = Field(default=QueryIntent.DEEP, description="查询意图")
    language: QueryLanguage = Field(default=QueryLanguage.AUTO, description="语言")
    max_results: int = Field(default=100, ge=10, le=500, description="最大结果数")
    engine_group: Literal["cn", "global", "all"] = Field(default="all", description="引擎组")
    timeout: int = Field(default=600, ge=30, le=3600, description="全局超时(秒)")
    session_id: Optional[str] = Field(default=None, description="会话ID")

    @field_validator("query")
    @classmethod
    def query_must_be_meaningful(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError("查询内容过短，至少需要2个字符")
        return v.strip()


class SearchHit(BaseModel):
    """单条搜索结果"""
    url: str = Field(..., min_length=5, description="结果URL")
    title: str = Field(..., min_length=1, description="标题")
    snippet: str = Field(default="", description="摘要")
    source_engine: str = Field(..., min_length=1, description="来源引擎")
    source_region: Literal["cn", "global"] = Field(default="global", description="来源区域")
    rank: int = Field(ge=1, le=10, description="引擎内排名")
    fingerprint: str = Field(default="", description="内容指纹(去重用)")

    model_config = {"frozen": True}

    @field_validator("url")
    @classmethod
    def url_must_be_valid(cls, v: str) -> str:
        """Phase 3: URL 必须可解析且有 scheme"""
        from urllib.parse import urlparse
        if not v:
            raise ValueError("URL cannot be empty")
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"URL must have scheme and netloc: {v}")
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"URL scheme must be http or https, got: {parsed.scheme}")
        return v


class SearchBatch(BaseModel):
    """批次搜索结果"""
    batch_id: str = Field(..., description="批次ID")
    engine_name: str = Field(..., description="引擎名称")
    results: list[SearchHit] = Field(default_factory=list, description="结果列表")
    errors: list[str] = Field(default_factory=list, description="批次错误")
    elapsed_ms: float = Field(default=0.0, description="耗时(毫秒)")


class SearchOutput(BaseModel):
    """搜索阶段输出 — 传给爬取阶段的唯一合法格式"""
    request_id: str = Field(..., description="请求ID")
    query: str = Field(..., description="原始查询")
    batches: list[SearchBatch] = Field(default_factory=list, description="批次列表")
    deduplicated_results: list[SearchHit] = Field(default_factory=list, description="去重后结果")
    total_raw: int = Field(default=0, ge=0, description="原始结果数")
    total_deduped: int = Field(default=0, ge=0, description="去重后结果数")
    total_engines: int = Field(default=0, ge=0, description="使用的引擎数")
    failed_engines: list[str] = Field(default_factory=list, description="失败的引擎")
    warnings: list[str] = Field(default_factory=list, description="警告")
    status: Literal["complete", "partial", "failed"] = Field(default="complete", description="状态")

    @field_validator("total_deduped")
    @classmethod
    def deduped_not_exceed_raw(cls, v: int, info) -> int:
        if "total_raw" in info.data and v > info.data["total_raw"]:
            raise ValueError(f"total_deduped ({v}) cannot exceed total_raw ({info.data['total_raw']})")
        return v
