from __future__ import annotations

import logging
import time

logger = logging.getLogger(__name__)


class MaintenanceMixin:
    def analyze_decay(self) -> dict:
        """分析记忆衰减状态"""
        return self.decay.analyze_all()

    def detect_causality(self, window_hours: int = 24) -> list[dict]:
        """自动检测因果关系（v5.3: 完整分析含时间线+链式+主题相似）"""
        result = self.causal.full_causal_analysis(
            window_hours=window_hours,
            embedding_store=self.embedding_store,
        )
        return result.get("heuristic", []) + result.get("timeline", [])

    def self_heal(self) -> dict:
        """执行自我修复扫描"""
        return self.self_healing.full_scan()

    def generate_graph(self, topic: str = None, format: str = "mermaid") -> str:
        """生成记忆图谱"""
        return self.graph.generate(center_topic=topic, format=format)

    def maintain(self, operations=None, **kwargs) -> dict:
        """
        一键维护：执行全生命周期流转。

        步骤：
        1. 核心维护（通过 MaintainEngine 或 fallback）
        2. 记忆蒸馏
        3. 自动快照
        4. 身份画像更新
        5. 数字孪生

        参数:
            operations: 指定维护操作列表（None 则执行全部）

        返回: 各阶段统计
        """
        try:
            from ..trace_logger import get_tracer
            tracer = get_tracer()
        except (ImportError, ValueError):
            tracer = None
        trace_id = tracer._next_id() if (tracer and getattr(tracer, '_enabled', False)) else None

        def _log_stage(name, ms, data):
            if tracer:
                try:
                    tracer.log_maintain_stage(name, ms, data, trace_id=trace_id)
                except Exception:
                    pass

        result = {}
        stages = {}

        # ── 核心维护 ──────────────────────────────────────
        if getattr(self, '_maintain_engine', None) is not None:
            result = self._maintain_engine.maintain(operations=operations)
        else:
            # Fallback：直接执行核心维护步骤
            # 1. L1 consolidation
            t0 = time.perf_counter()
            try:
                hier_result = self.hierarchy.maintain(
                    pipeline=self.pipeline,
                    deduplicator=self.dedup,
                    decay=self.decay,
                )
                result.update(hier_result)
            except Exception as e:
                result["hierarchy"] = {"error": str(e)}
            stages["hierarchy"] = (time.perf_counter() - t0) * 1000
            _log_stage("hierarchy", stages["hierarchy"], result.get("hierarchy"))

            # 2. 自我修复
            t0 = time.perf_counter()
            try:
                heal_result = self.self_healing.run()
                result["self_healing"] = heal_result
            except Exception as e:
                result["self_healing"] = {"error": str(e)}
            stages["self_healing"] = (time.perf_counter() - t0) * 1000
            _log_stage("self_healing", stages["self_healing"], result.get("self_healing"))

            # 3. 完整因果分析
            t0 = time.perf_counter()
            try:
                causal_result = self.causal.full_causal_analysis(
                    window_hours=6,
                    embedding_store=self.embedding_store,
                )
                result["causal_links"] = causal_result["total"]
            except Exception:
                result["causal_links"] = 0
            stages["causal_analysis"] = (time.perf_counter() - t0) * 1000
            _log_stage("causal_analysis", stages["causal_analysis"], {"links": result.get("causal_links")})

            # 4. 主动反应器扫描
            t0 = time.perf_counter()
            try:
                reactor_result = self.reactor.scan(
                    store=self.store,
                    decay=self.decay,
                    self_healing=self.self_healing,
                    causal=self.causal,
                )
                result["reactor"] = {
                    "total_actions": reactor_result["total_actions"],
                    "contradictions": len(reactor_result["contradictions"]),
                    "decay_reviews": len(reactor_result["decay_reviews"]),
                    "decisions": len(reactor_result["decisions"]),
                }
            except Exception as e:
                result["reactor"] = {"error": str(e)}
            stages["reactor"] = (time.perf_counter() - t0) * 1000
            _log_stage("reactor", stages["reactor"], result.get("reactor"))

            # 5. 数据库维护
            t0 = time.perf_counter()
            try:
                self.store.auto_maintain(embedding_store=self.embedding_store)
                result["db_maintain"] = "ok"
            except Exception as e:
                result["db_maintain"] = {"error": str(e)}
            stages["db_maintain"] = (time.perf_counter() - t0) * 1000
            _log_stage("db_maintain", stages["db_maintain"], result.get("db_maintain"))

        # ── 扩展维护步骤（从 v9 合并，始终执行）──────────

        # 记忆蒸馏
        t0 = time.perf_counter()
        try:
            distill_result = self.distiller.distill()
            result["distill"] = distill_result
            self._distill_fail_count = 0
        except Exception as e:
            result["distill"] = {"error": str(e)}
            if not hasattr(self, "_distill_fail_count"):
                self._distill_fail_count = 0
            self._distill_fail_count += 1
            if self._distill_fail_count >= 3:
                logger.warning(
                    f"⚠️ 蒸馏连续失败 {self._distill_fail_count} 次: {e}。"
                    f"请检查 distill 模块配置或 LLM 接口。"
                )
        stages["distill"] = (time.perf_counter() - t0) * 1000
        _log_stage("distill", stages["distill"], result.get("distill"))

        # 自动快照（MaintainEngine 可能已处理，避免重复）
        if "snapshot" not in result:
            t0 = time.perf_counter()
            try:
                snap_result = self.timeline.auto_snapshot_if_needed(interval_hours=24)
                if snap_result:
                    result["auto_snapshot"] = {
                        "taken": True,
                        "label": snap_result.get("label"),
                        "memory_count": snap_result.get("memory_count"),
                    }
                else:
                    result["auto_snapshot"] = {"taken": False}
            except Exception as e:
                result["auto_snapshot"] = {"error": str(e)}
            stages["auto_snapshot"] = (time.perf_counter() - t0) * 1000
            _log_stage("auto_snapshot", stages["auto_snapshot"], result.get("auto_snapshot"))

        # 更新内在状态（Phase 4）
        if "motivation" not in result:
            t0 = time.perf_counter()
            try:
                recent = self.store.query(limit=10)
                state, mot_trace = self.motivation.update_state(recent)
                result["motivation"] = {
                    "mood": state.mood_summary,
                    "curiosity": state.curiosity,
                    "boredom": state.boredom,
                    "trace": mot_trace,
                }
            except Exception as e:
                result["motivation"] = {"error": str(e)}
            stages["motivation"] = (time.perf_counter() - t0) * 1000
            _log_stage("motivation", stages["motivation"], result.get("motivation"))

        # 身份画像更新（Phase 5/6）
        t0 = time.perf_counter()
        try:
            identity_result = self.narrative.build_identity_profile()
            result["narrative_update"] = {
                "status": "ok",
                "identity_trace": identity_result.get("_trace", {}),
            }
        except Exception as e:
            result["narrative_update"] = {"error": str(e)}
        stages["narrative_update"] = (time.perf_counter() - t0) * 1000
        _log_stage("narrative_update", stages["narrative_update"], result.get("narrative_update"))

        # 数字孪生（Phase 6）
        t0 = time.perf_counter()
        try:
            profile = self.digital_twin.build_unified_profile()
            result["digital_twin"] = {
                "status": "ok",
                "profile_id": profile.get("profile_id"),
                "confidence": profile.get("overall_confidence", 0.7),
            }
        except Exception as e:
            result["digital_twin"] = {"error": str(e)}
        stages["digital_twin"] = (time.perf_counter() - t0) * 1000
        _log_stage("digital_twin", stages["digital_twin"], result.get("digital_twin"))

        # 汇总阶段耗时
        result["_stage_timing_ms"] = {k: round(v, 2) for k, v in stages.items()}
        result["_total_timing_ms"] = round(sum(stages.values()), 2)

        # Auto-compression check
        self._check_auto_compress()

        return result