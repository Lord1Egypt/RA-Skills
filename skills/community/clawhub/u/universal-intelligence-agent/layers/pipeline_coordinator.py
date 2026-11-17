"""
管道协调器 — 纯调度引擎（单轨制）
────────────────────────────────
Phase 5.1 增强：
  - 全局超时机制（读取 NormalizedRequest.timeout）
  - 每个阶段完成后写入 WAL 快照
  - resume_session() 从 WAL 恢复并继续执行

职责：
  1. 接收标准化请求（NormalizedRequest）
  2. 按阶段顺序调度 Phase Containers
  3. 在每个阶段间通过 ACL 校验数据
  4. 异常时委托 RollbackCoordinator 回滚
"""
from __future__ import annotations

import logging
import signal
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional

from contracts.state_schema import PipelinePhase
from contracts.context_schema import (
    StageContext,
    PipelineBus,
    StageNotExecutedError,
    StageTypeError,
)
from contracts.search_schema import SearchOutput
from contracts.crawl_schema import CrawlOutput
from contracts.analysis_schema import AnalysisOutput

from layers.acl import (
    validate_search_to_crawl,
    validate_crawl_to_analyze,
    ACLViolationError,
)
from layers.input_adapter import NormalizedRequest, QueryIntent
from layers.output_adapter import OutputAdapter, OutputResult, DeliveryStatus
from layers.field_mapper import FieldMapper
from layers.degraded_handler import DegradedHandler
from layers.rollback_coordinator import RollbackCoordinator

from middlewares.circuit_breaker import TieredCircuitBreaker, CircuitBreakerOpenError
from middlewares.transaction import UnitOfWork, WALLogger, WALEntry
from middlewares.side_effect_log import SideEffectLogger, SideEffectType

logger = logging.getLogger(__name__)


class PipelineTimeoutError(Exception):
    """管道全局超时"""
    pass


@dataclass
class PipelineContext:
    """管道执行上下文 — 单轨制，数据只通过 PipelineBus 传递"""
    session_id: str
    request: NormalizedRequest
    current_phase: PipelinePhase = PipelinePhase.IDLE
    bus: PipelineBus = field(default_factory=lambda: PipelineBus(session_id=""))
    started_at: float = field(default_factory=time.time)
    circuit_breaker: TieredCircuitBreaker = field(default_factory=TieredCircuitBreaker)
    side_effect_logger: SideEffectLogger = field(default_factory=SideEffectLogger)

    def __post_init__(self):
        if not self.bus.session_id:
            self.bus = PipelineBus(session_id=self.session_id)


class PipelineCoordinator:
    """管道协调器 — 纯调度，PipelineBus 单轨制"""

    _PHASE_ORDER = [
        PipelinePhase.SEARCHING,
        PipelinePhase.CRAWLING,
        PipelinePhase.ANALYZING,
        PipelinePhase.REPORTING,
        PipelinePhase.DELIVERING,
    ]

    def __init__(self):
        self.output_adapter = OutputAdapter()
        self._field_mapper = FieldMapper()
        self._degraded_handler = DegradedHandler()
        self._rollback_coordinator = RollbackCoordinator()
        self._wal_logger = WALLogger()

    def execute(self, request: NormalizedRequest) -> OutputResult:
        """执行完整管道"""
        session_id = request.session_id or f"uia_{uuid.uuid4().hex[:12]}"
        ctx = PipelineContext(session_id=session_id, request=request)

        # Phase 5.1: 全局超时 — 使用 signal.alarm（Unix）或 threading.Timer（Windows）
        self._setup_timeout(ctx)

        logger.info(f"[Pipeline:{session_id}] Starting for query: {request.query[:50]}...")

        try:
            # Phase 0: 预检
            self._check_timeout_flag(ctx)
            if not self._preflight(ctx):
                return self._degraded_output(ctx, "Preflight check failed")

            # Phase 1: 搜索
            self._check_timeout_flag(ctx)
            if not self._execute_search(ctx):
                return self._degraded_output(ctx, "Search phase failed")
            self._save_wal_snapshot(ctx, "searching")

            # ACL: 搜索→爬取（类型安全）
            self._check_timeout_flag(ctx)
            try:
                validated_search = validate_search_to_crawl(ctx.bus)
            except ACLViolationError as e:
                logger.error(f"ACL: Search→Crawl failed: {e.errors}")
                return self._degraded_output(ctx, f"Search output validation failed: {e.errors}")

            # Phase 2: 爬取
            self._check_timeout_flag(ctx)
            self._execute_crawl(ctx, validated_search)
            self._save_wal_snapshot(ctx, "crawling")

            # Phase 3: 分析
            self._check_timeout_flag(ctx)
            analysis_input = (
                ctx.bus.get_crawl_data()
                if ctx.bus.has_crawl_succeeded()
                else ctx.bus.get_search_data()
            )
            try:
                validated_crawl = validate_crawl_to_analyze(ctx.bus)
            except ACLViolationError as e:
                logger.error(f"ACL: Crawl→Analyze failed: {e.errors}")
                validated_crawl = analysis_input

            self._check_timeout_flag(ctx)
            if not self._execute_analyze(ctx, validated_crawl):
                return self._degraded_output(ctx, "Analysis phase failed")
            self._save_wal_snapshot(ctx, "analyzing")

            # 通过 PipelineBus 获取强类型 AnalysisOutput
            self._check_timeout_flag(ctx)
            try:
                analysis_output = ctx.bus.get_analysis_output()
                validated_analysis = self._field_mapper.map_analysis_to_output(analysis_output)
            except (StageNotExecutedError, StageTypeError) as e:
                logger.error(f"PipelineBus: {e}")
                return self._degraded_output(ctx, f"Analysis context error: {e}")

            # Phase 4: 报告生成
            self._check_timeout_flag(ctx)
            report_result = self._execute_report(ctx, validated_analysis)
            if not report_result:
                return self._degraded_output(ctx, "Report generation failed")

            # Phase 5: 交付
            self._check_timeout_flag(ctx)
            deliver_result = self._execute_deliver(ctx, report_result)

            ctx.current_phase = PipelinePhase.DONE
            self._save_wal_snapshot(ctx, "done")
            logger.info(f"[Pipeline:{session_id}] Completed in {time.time() - ctx.started_at:.1f}s")

            return deliver_result

        except CircuitBreakerOpenError as e:
            logger.critical(f"[Pipeline:{session_id}] Global circuit breaker open: {e}")
            return self._degraded_output(ctx, f"System overloaded: {e}")

        except Exception as e:
            logger.exception(f"[Pipeline:{session_id}] Unhandled pipeline error: {e}")
            ctx.current_phase = PipelinePhase.FAILED
            self._rollback_coordinator.rollback(ctx.session_id, ctx.side_effect_logger)
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[f"Pipeline crashed: {type(e).__name__}: {e}"],
            )

    def _setup_timeout(self, ctx: PipelineContext):
        """Phase 5.1: 设置全局超时

        Unix: 使用 signal.alarm（主线程可捕获 SIGALRM）
        Windows: 使用 threading.Timer + 共享标志位（子线程异常无法跨线程捕获）
        """
        timeout = ctx.request.timeout
        if timeout <= 0:
            return

        def _on_timeout():
            elapsed = time.time() - ctx.started_at
            logger.critical(
                f"[Pipeline:{ctx.session_id}] Global timeout reached ({timeout}s), "
                f"elapsed: {elapsed:.1f}s"
            )
            raise PipelineTimeoutError(
                f"Pipeline exceeded global timeout of {timeout}s (elapsed: {elapsed:.1f}s)"
            )

        try:
            signal.signal(signal.SIGALRM, lambda *_: _on_timeout())
            signal.alarm(timeout)
        except (AttributeError, ValueError):
            # Windows: 使用共享标志位 + 轮询（子线程异常无法跨线程传播）
            import threading
            ctx._timed_out = False

            def _set_timeout_flag():
                ctx._timed_out = True
                logger.critical(
                    f"[Pipeline:{ctx.session_id}] Global timeout reached ({timeout}s)"
                )

            timer = threading.Timer(timeout, _set_timeout_flag)
            timer.daemon = True
            timer.start()

            # 将原始 execute 逻辑包装为带超时检查的版本
            # 在每个阶段前后检查超时标志
            self._check_timeout = lambda: (
                (_ for _ in ()).throw(PipelineTimeoutError(
                    f"Pipeline exceeded global timeout of {timeout}s"
                )) if getattr(ctx, '_timed_out', False) else None
            )

    def _check_timeout_flag(self, ctx: PipelineContext):
        """Phase 5.2: 检查 Windows 超时标志"""
        if getattr(ctx, '_timed_out', False):
            raise PipelineTimeoutError(
                f"Pipeline exceeded global timeout of {ctx.request.timeout}s"
            )

    def _save_wal_snapshot(self, ctx: PipelineContext, phase: str):
        """Phase 5.1: 将 PipelineBus 快照写入 WAL"""
        try:
            snapshot = ctx.bus.to_snapshot()
            import json
            self._wal_logger.write(WALEntry(
                session_id=ctx.session_id,
                phase=phase,
                action="snapshot",
                status="committed",
                details=json.dumps(snapshot, ensure_ascii=False, default=str),
            ))
        except Exception as e:
            logger.warning(f"[Pipeline:{ctx.session_id}] WAL snapshot failed: {e}")

    def _preflight(self, ctx: PipelineContext) -> bool:
        from layers.preflight import PreflightChecker
        checker = PreflightChecker()
        result = checker.check()
        if not result.all_passed:
            ctx.side_effect_logger.log(
                session_id=ctx.session_id,
                phase="preflight",
                effect_type=SideEffectType.STATE_CHANGE,
                target="preflight_failed",
                details={"failures": result.failures},
            )
        return result.all_passed

    def _execute_search(self, ctx: PipelineContext) -> bool:
        """Phase 1: 搜索"""
        ctx.current_phase = PipelinePhase.SEARCHING
        ctx.side_effect_logger.log_state_change(ctx.session_id, "pipeline", "IDLE", "SEARCHING")

        try:
            from layers.search_engine import SearchEngine
            engine = SearchEngine(circuit_breaker=ctx.circuit_breaker)

            start = time.time()
            result_data = engine.search(
                query=ctx.request.query,
                language=ctx.request.language.value,
                engine_group=ctx.request.engine_group,
                max_results=ctx.request.max_results,
                session_id=ctx.session_id,
            )

            elapsed = (time.time() - start) * 1000

            try:
                search_output = SearchOutput.model_validate(result_data)
                ctx.bus.search_ctx = StageContext(
                    session_id=ctx.session_id,
                    phase=PipelinePhase.SEARCHING,
                    success=True,
                    payload=search_output,
                    elapsed_ms=elapsed,
                )
            except Exception as ve:
                logger.error(f"Search output schema validation failed: {ve}")
                try:
                    search_output = SearchOutput(
                        request_id=ctx.session_id,
                        query=ctx.request.query,
                        status="failed",
                        total_engines=0,
                    )
                except Exception:
                    search_output = None
                ctx.bus.search_ctx = StageContext(
                    session_id=ctx.session_id,
                    phase=PipelinePhase.SEARCHING,
                    success=True,
                    payload=search_output,
                    elapsed_ms=elapsed,
                    warnings=[str(ve)],
                )
            return True
        except Exception as e:
            logger.error(f"Search phase error: {e}")
            ctx.bus.search_ctx = StageContext(
                session_id=ctx.session_id,
                phase=PipelinePhase.SEARCHING,
                success=False,
                errors=[str(e)],
            )
            return False

    def _execute_crawl(self, ctx: PipelineContext, search_data: dict) -> bool:
        """Phase 2: 爬取"""
        ctx.current_phase = PipelinePhase.CRAWLING
        ctx.side_effect_logger.log_state_change(ctx.session_id, "pipeline", "SEARCHING", "CRAWLING")

        try:
            from layers.scraper import Scraper
            scraper = Scraper(circuit_breaker=ctx.circuit_breaker)

            start = time.time()
            result_data = scraper.crawl(
                search_results=search_data.get("deduplicated_results", []),
                session_id=ctx.session_id,
            )
            elapsed = (time.time() - start) * 1000

            try:
                crawl_output = CrawlOutput.model_validate(result_data)
                ctx.bus.crawl_ctx = StageContext(
                    session_id=ctx.session_id,
                    phase=PipelinePhase.CRAWLING,
                    success=True,
                    payload=crawl_output,
                    elapsed_ms=elapsed,
                )
            except Exception as ve:
                logger.error(f"Crawl output schema validation failed: {ve}")
                try:
                    crawl_output = CrawlOutput(
                        pages=[], total_pages=0, successful_pages=0,
                        status="failed", errors=[str(ve)],
                    )
                except Exception:
                    crawl_output = None
                ctx.bus.crawl_ctx = StageContext(
                    session_id=ctx.session_id,
                    phase=PipelinePhase.CRAWLING,
                    success=False,
                    payload=crawl_output,
                    elapsed_ms=elapsed,
                    errors=[str(ve)],
                )
                return False
            return True
        except Exception as e:
            logger.error(f"Crawl phase error: {e}")
            ctx.bus.crawl_ctx = StageContext(
                session_id=ctx.session_id,
                phase=PipelinePhase.CRAWLING,
                success=False,
                errors=[str(e)],
            )
            return False

    def _execute_analyze(self, ctx: PipelineContext, crawl_data: dict) -> bool:
        """Phase 3: 分析"""
        ctx.current_phase = PipelinePhase.ANALYZING
        ctx.side_effect_logger.log_state_change(ctx.session_id, "pipeline", "CRAWLING", "ANALYZING")

        try:
            from layers.analyzer import Analyzer
            analyzer = Analyzer(circuit_breaker=ctx.circuit_breaker)

            start = time.time()
            analysis_output = analyzer.analyze(
                query=ctx.request.query,
                crawl_data=crawl_data,
                intent=ctx.request.intent.value,
                session_id=ctx.session_id,
            )

            ctx.bus.analysis_ctx = StageContext(
                session_id=ctx.session_id,
                phase=PipelinePhase.ANALYZING,
                success=True,
                payload=analysis_output,
                elapsed_ms=(time.time() - start) * 1000,
            )
            return True
        except Exception as e:
            logger.error(f"Analyze phase error: {e}")
            ctx.bus.analysis_ctx = StageContext(
                session_id=ctx.session_id,
                phase=PipelinePhase.ANALYZING,
                success=False,
                errors=[str(e)],
            )
            return False

    def _execute_report(self, ctx: PipelineContext, analysis_data: dict) -> Optional[OutputResult]:
        """Phase 4: 报告生成"""
        ctx.current_phase = PipelinePhase.REPORTING
        uow = UnitOfWork(session_id=ctx.session_id, wal_logger=self._wal_logger)

        try:
            intent = ctx.request.intent
            with uow:
                if intent == QueryIntent.QUICK:
                    output = self.output_adapter.generate_brief(analysis_data, ctx.session_id, uow=uow)
                elif intent == QueryIntent.COMPARE:
                    output = self.output_adapter.generate_comparison(analysis_data, ctx.session_id, uow=uow)
                else:
                    output = self.output_adapter.generate_analysis(analysis_data, ctx.session_id, uow=uow)
            return output
        except Exception as e:
            logger.error(f"Report phase error: {e}")
            return None

    def _execute_deliver(self, ctx: PipelineContext, output: OutputResult) -> OutputResult:
        """Phase 5: 交付"""
        ctx.current_phase = PipelinePhase.DELIVERING
        return output

    def _degraded_output(self, ctx: PipelineContext, reason: str) -> OutputResult:
        """降级输出"""
        logger.warning(f"[Pipeline:{ctx.session_id}] Degraded: {reason}")

        try:
            degraded_analysis = self._degraded_handler.build_degraded_analysis(
                bus=ctx.bus, query=ctx.request.query, reason=reason,
            )
            resolved = self._field_mapper.map_analysis_to_output(degraded_analysis)
            return self.output_adapter.generate_brief(resolved, ctx.session_id)
        except Exception:
            return OutputResult(
                status=DeliveryStatus.FAILED,
                errors=[reason],
                warnings=[f"Pipeline degraded at phase: {ctx.current_phase.value}"],
            )


# ── 跨会话恢复 ──────────────────────────────────────────────

def resume_session(session_id: str) -> Optional[OutputResult]:
    """Phase 5.1: 从 WAL 恢复中断的会话并继续执行

    读取 WAL 日志，找到上次完成的阶段和 PipelineBus 快照，
    从下一个阶段继续执行管道。
    """
    import json

    wal = WALLogger()
    entries = wal.read(session_id)

    if not entries:
        logger.info(f"Session {session_id}: No WAL entries found, cannot resume")
        return None

    # 找到最后一个 committed 的阶段和最新的快照
    last_phase = None
    last_snapshot = None
    for entry in reversed(entries):
        if entry.status == "committed":
            if entry.action == "snapshot" and last_snapshot is None:
                try:
                    last_snapshot = json.loads(entry.details)
                except Exception:
                    pass
            if last_phase is None:
                last_phase = entry.phase

    if last_phase is None:
        logger.info(f"Session {session_id}: No committed phase found, cannot resume")
        return None

    logger.info(f"Session {session_id}: Resuming from phase '{last_phase}'")

    # 根据最后完成的阶段确定下一步
    phase_order = ["searching", "crawling", "analyzing", "reporting", "delivering", "done"]
    try:
        idx = phase_order.index(last_phase)
    except ValueError:
        idx = 0

    if idx >= len(phase_order) - 1:
        logger.info(f"Session {session_id}: Already at final phase '{last_phase}', nothing to resume")
        return None

    next_phase = phase_order[idx + 1]
    logger.info(f"Session {session_id}: Next phase to execute: '{next_phase}'")

    # 从快照恢复 PipelineBus
    bus = None
    if last_snapshot:
        try:
            bus = PipelineBus.from_snapshot(last_snapshot)
        except Exception as e:
            logger.warning(f"Session {session_id}: Failed to restore snapshot: {e}")

    if bus is None:
        logger.warning(f"Session {session_id}: No valid snapshot, cannot reconstruct context")
        return None

    # 重建 PipelineContext 并继续执行
    # 注意：需要原始 query，从 WAL 快照中恢复
    query = last_snapshot.get("query", "unknown") if last_snapshot else "unknown"
    request = NormalizedRequest(
        query=query,
        intent=QueryIntent.DEEP,
        session_id=session_id,
    )

    coordinator = PipelineCoordinator()
    ctx = PipelineContext(session_id=session_id, request=request, bus=bus)

    try:
        if next_phase == "reporting":
            try:
                analysis_output = ctx.bus.get_analysis_output()
                validated = coordinator._field_mapper.map_analysis_to_output(analysis_output)
                return coordinator._execute_report(ctx, validated) or OutputResult(
                    status=DeliveryStatus.FAILED,
                    errors=["Report phase returned None during resume"],
                )
            except (StageNotExecutedError, StageTypeError):
                return None
        elif next_phase == "delivering":
            report_result = coordinator._execute_report(ctx, {})
            if report_result:
                return coordinator._execute_deliver(ctx, report_result)
        else:
            logger.info(f"Session {session_id}: Phase '{next_phase}' resume not fully implemented")
            return None
    except Exception as e:
        logger.error(f"Session {session_id}: Resume failed: {e}")
        return None
