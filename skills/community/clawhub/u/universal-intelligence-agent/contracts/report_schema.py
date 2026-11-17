"""
报告输出契约 — Pydantic v2
───────────────────────────
定义报告生成和输出的严格类型。
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from pathlib import Path


class ReportFormat(str, Enum):
    BRIEF = "brief"           # 快速简报
    ANALYSIS = "analysis"     # 深度分析
    COMPARISON = "comparison" # 对比报告
    MARKDOWN = "markdown"     # Markdown
    JSON = "json"             # JSON


class DeliveryStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"


class ReportRequest(BaseModel):
    """报告生成请求"""
    analysis_data: dict = Field(..., description="分析数据")
    format: ReportFormat = Field(default=ReportFormat.MARKDOWN, description="输出格式")
    session_id: str = Field(..., min_length=1, description="会话ID")
    include_sources: bool = Field(default=True, description="是否包含来源")
    include_entities: bool = Field(default=True, description="是否包含实体")
    language: str = Field(default="zh", description="报告语言")


# Phase 4.1: 统一 SourceEntry 定义 — 从 analysis_schema 导入
# 消除 trust_level: int vs trust_level: float 的不一致
from contracts.analysis_schema import SourceEntry


class ReportOutput(BaseModel):
    """报告输出"""
    status: DeliveryStatus = Field(..., description="交付状态")
    format: ReportFormat = Field(..., description="输出格式")
    content_preview: str = Field(default="", description="内容预览(前200字符)")
    output_path: Optional[Path] = Field(default=None, description="输出文件路径")
    data: dict = Field(default_factory=dict, description="结构化数据")
    errors: list[str] = Field(default_factory=list, description="错误")
    warnings: list[str] = Field(default_factory=list, description="警告")

    @property
    def is_success(self) -> bool:
        return self.status in (DeliveryStatus.SUCCESS, DeliveryStatus.PARTIAL)

    @property
    def is_complete_success(self) -> bool:
        return self.status == DeliveryStatus.SUCCESS
