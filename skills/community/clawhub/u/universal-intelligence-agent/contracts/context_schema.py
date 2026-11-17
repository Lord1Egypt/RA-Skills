"""
Typed Context Bus 契约 — Pydantic v2
────────────────────────────────────
定义管道阶段间类型安全的数据传递契约。

Phase 4.1 核心新增：消除 PhaseResult.data: dict[str, Any] 的类型黑洞。
阶段间数据传递从弱类型 dict 升级为强类型 StageContext，
确保 Pydantic Schema 的类型信息在整个管道中不丢失。
"""
from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, Union

from contracts.search_schema import SearchOutput
from contracts.crawl_schema import CrawlOutput
from contracts.analysis_schema import AnalysisOutput
from contracts.state_schema import PipelinePhase


class StageContext(BaseModel):
    """阶段上下文 — 类型安全的阶段产物包装

    替代 PhaseResult.data: dict[str, Any]。
    payload 是具体的 Pydantic Schema 对象，类型信息在此处不丢失。

    用法:
        ctx = StageContext(
            session_id="abc",
            phase=PipelinePhase.SEARCHING,
            success=True,
            payload=SearchOutput(...),
        )
        # 下游通过 PipelineBus.get_search_output() 类型安全获取
    """
    session_id: str
    phase: PipelinePhase
    success: bool
    payload: Optional[Union[SearchOutput, CrawlOutput, AnalysisOutput]] = None
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    elapsed_ms: float = 0.0


class PipelineBus(BaseModel):
    """管道总线 — 类型安全的阶段间数据传递

    替代 PipelineContext.phase_results: dict[PipelinePhase, PhaseResult]。
    通过 get_* 方法获取特定阶段的产出，None 时抛明确异常而非静默退化。

    用法:
        bus = PipelineBus(session_id="abc")
        # 设置阶段产出
        bus.search_ctx = StageContext(payload=search_output, ...)
        # 类型安全获取
        search_out = bus.get_search_output()  # → SearchOutput
    """
    session_id: str
    search_ctx: Optional[StageContext] = None
    crawl_ctx: Optional[StageContext] = None
    analysis_ctx: Optional[StageContext] = None

    def get_search_output(self) -> SearchOutput:
        """类型安全获取搜索输出"""
        if self.search_ctx is None or self.search_ctx.payload is None:
            raise StageNotExecutedError("Search stage not executed or produced no output")
        if not isinstance(self.search_ctx.payload, SearchOutput):
            raise StageTypeError(
                f"Expected SearchOutput, got {type(self.search_ctx.payload).__name__}"
            )
        return self.search_ctx.payload

    def get_crawl_output(self) -> CrawlOutput:
        """类型安全获取爬取输出"""
        if self.crawl_ctx is None or self.crawl_ctx.payload is None:
            raise StageNotExecutedError("Crawl stage not executed or produced no output")
        if not isinstance(self.crawl_ctx.payload, CrawlOutput):
            raise StageTypeError(
                f"Expected CrawlOutput, got {type(self.crawl_ctx.payload).__name__}"
            )
        return self.crawl_ctx.payload

    def get_analysis_output(self) -> AnalysisOutput:
        """类型安全获取分析输出"""
        if self.analysis_ctx is None or self.analysis_ctx.payload is None:
            raise StageNotExecutedError("Analysis stage not executed or produced no output")
        if not isinstance(self.analysis_ctx.payload, AnalysisOutput):
            raise StageTypeError(
                f"Expected AnalysisOutput, got {type(self.analysis_ctx.payload).__name__}"
            )
        return self.analysis_ctx.payload

    def get_search_data(self) -> dict:
        """兼容旧接口：获取搜索阶段的 dict 数据（用于传给爬取阶段）"""
        output = self.get_search_output()
        return output.model_dump()

    def get_crawl_data(self) -> dict:
        """兼容旧接口：获取爬取阶段的 dict 数据（用于传给分析阶段）"""
        output = self.get_crawl_output()
        return output.model_dump()

    def has_search_succeeded(self) -> bool:
        """检查搜索阶段是否成功执行"""
        return self.search_ctx is not None and self.search_ctx.success

    def has_crawl_succeeded(self) -> bool:
        """检查爬取阶段是否成功执行"""
        return self.crawl_ctx is not None and self.crawl_ctx.success

    def to_snapshot(self) -> dict:
        """导出为可序列化的快照（用于跨会话恢复的持久化）"""
        import json
        data = self.model_dump()
        # 将 Pydantic 对象转为 dict 以便 JSON 序列化
        for key in ("search_ctx", "crawl_ctx", "analysis_ctx"):
            if data.get(key) and data[key].get("payload"):
                payload = data[key]["payload"]
                if hasattr(payload, 'model_dump'):
                    data[key]["payload"] = payload.model_dump()
        return data

    @classmethod
    def from_snapshot(cls, data: dict) -> "PipelineBus":
        """从快照恢复 PipelineBus（用于跨会话恢复）"""
        bus = cls(session_id=data.get("session_id", ""))
        for key in ("search_ctx", "crawl_ctx", "analysis_ctx"):
            ctx_data = data.get(key)
            if ctx_data:
                bus.__dict__[key] = StageContext(**ctx_data)
        return bus


class StageNotExecutedError(Exception):
    """阶段未执行或产出为 None — 明确的失败信号"""
    pass


class StageTypeError(Exception):
    """阶段产出类型不匹配 — 编译时类型安全在运行时的最后防线"""
    pass
