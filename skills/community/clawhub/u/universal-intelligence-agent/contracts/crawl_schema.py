"""
爬取请求契约 — Pydantic v2
───────────────────────────
定义爬取阶段的输入输出严格类型。
"""
from __future__ import annotations

from pydantic import BaseModel, Field, HttpUrl, field_validator
from typing import Optional, Literal


class CrawlRequest(BaseModel):
    """爬取请求"""
    urls: list[str] = Field(..., min_length=1, max_length=10, description="待爬取URL列表")
    session_id: str = Field(default="", description="会话ID")
    max_pages: int = Field(default=10, ge=1, le=50, description="最大页面数")
    timeout_per_page: int = Field(default=30, ge=5, le=120, description="单页超时(秒)")
    max_retries: int = Field(default=3, ge=0, le=5, description="最大重试次数")

    @field_validator("urls")
    @classmethod
    def urls_must_be_valid(cls, v: list[str]) -> list[str]:
        invalid = [u for u in v if not u or not u.startswith(("http://", "https://"))]
        if invalid:
            raise ValueError(f"Invalid URLs: {invalid}")
        return v


class CrawledPage(BaseModel):
    """单页爬取结果"""
    url: str = Field(..., min_length=5, description="页面URL")
    title: str = Field(default="", description="页面标题")
    content_md: str = Field(default="", description="Markdown内容")
    content_length: int = Field(default=0, ge=0, description="内容长度")
    status_code: int = Field(default=0, ge=0, le=599, description="HTTP状态码")
    from_cache: bool = Field(default=False, description="是否来自缓存")
    error: str = Field(default="", description="错误信息")

    model_config = {"frozen": True}

    @field_validator("url")
    @classmethod
    def url_must_be_valid(cls, v: str) -> str:
        """Phase 3: URL 必须可解析"""
        from urllib.parse import urlparse
        if not v:
            raise ValueError("URL cannot be empty")
        parsed = urlparse(v)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError(f"URL must have scheme and netloc: {v}")
        return v

    @field_validator("content_length")
    @classmethod
    def content_length_matches_content(cls, v: int, info) -> int:
        """Phase 3: content_length 应与 content_md 长度一致"""
        if "content_md" in info.data:
            actual_len = len(info.data["content_md"])
            if v != actual_len and v != 0:
                raise ValueError(
                    f"content_length ({v}) does not match content_md length ({actual_len})"
                )
        return v


class CrawlOutput(BaseModel):
    """爬取阶段输出 — 传给分析阶段的唯一合法格式"""
    pages: list[CrawledPage] = Field(default_factory=list, description="爬取页面列表")
    total_pages: int = Field(default=0, ge=0, description="总页面数")
    successful_pages: int = Field(default=0, ge=0, description="成功页面数")
    failed_urls: list[str] = Field(default_factory=list, description="失败的URL")
    errors: list[str] = Field(default_factory=list, description="错误")
    status: Literal["complete", "partial", "failed"] = Field(default="complete", description="状态")

    @field_validator("successful_pages")
    @classmethod
    def successful_not_exceed_total(cls, v: int, info) -> int:
        if "total_pages" in info.data and v > info.data["total_pages"]:
            raise ValueError("successful_pages cannot exceed total_pages")
        return v


class AntiBlockConfig(BaseModel):
    """反封配置"""
    user_agent_rotation: bool = Field(default=True, description="是否轮换UA")
    request_interval_min: float = Field(default=1.0, ge=0.1, description="最小间隔(秒)")
    request_interval_max: float = Field(default=3.0, ge=0.1, description="最大间隔(秒)")
    max_retries_per_page: int = Field(default=3, ge=1, le=5, description="单页最大重试")
    use_referer_spoofing: bool = Field(default=True, description="是否伪造Referer")
