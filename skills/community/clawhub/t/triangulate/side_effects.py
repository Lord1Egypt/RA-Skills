"""
副作用收集器 — 统一追踪 Saga/无 Saga 路径下的副作用。

合并了 SessionRegistry 的功能：
- 按步骤追踪和回滚 sessions
- 回滚失败记录（不静默丢失）
- 存活状态检查
- 内置 _rolled_back 集合防止双重回滚
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


class SideEffectCollector:
    """副作用收集器 — 确保所有路径下的副作用都被追踪和可回滚。

    合并了原 SessionRegistry 的回滚失败记录和存活检查功能，
    消除两个模块 90% 功能重叠的维护负担。

    用法:
        collector = SideEffectCollector()
        collector.track_step("strategy", ctx)
        collector.track_step("execute", ctx)
        collector.rollback_step("strategy", session_manager)
        collector.rollback_all(session_manager)
    """

    def __init__(self):
        self._step_sessions: Dict[str, List[str]] = {}
        self._all_sessions: Set[str] = set()
        self._step_order: List[str] = []
        self._rolled_back: Set[str] = set()
        self._failed_rollbacks: List[Dict[str, str]] = []  # 回滚失败记录

    # ------------------------------------------------------------------
    # 追踪
    # ------------------------------------------------------------------

    def track_step(self, step_name: str, ctx: Any) -> None:
        """记录步骤产生的副作用。

        Args:
            step_name: 步骤名称
            ctx: PipelineContext（从中提取 sessions）
        """
        sessions: List[str] = []

        if hasattr(ctx, 'strategy_sessions') and step_name == 'strategy':
            sessions = list(ctx.strategy_sessions)
        elif hasattr(ctx, 'execution_sessions') and step_name == 'execute':
            sessions = list(ctx.execution_sessions)

        if sessions:
            if step_name not in self._step_sessions:
                self._step_order.append(step_name)
            # 使用 set 合并去重（同一步骤可能被多次 track）
            existing = set(self._step_sessions.get(step_name, []))
            existing.update(sessions)
            self._step_sessions[step_name] = list(existing)
            self._all_sessions.update(sessions)

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------

    def get_all_sessions(self) -> List[str]:
        """获取所有被追踪的 session IDs"""
        return list(self._all_sessions)

    def get_step_sessions(self, step_name: str) -> List[str]:
        """获取特定步骤产生的 sessions"""
        return list(self._step_sessions.get(step_name, []))

    def get_step_order(self) -> List[str]:
        """获取步骤注册顺序"""
        return list(self._step_order)

    def get_failed_rollbacks(self) -> List[Dict[str, str]]:
        """获取回滚失败的记录（不清空，供调试用）"""
        return list(self._failed_rollbacks)

    @property
    def tracked_step_count(self) -> int:
        return len(self._step_sessions)

    @property
    def total_session_count(self) -> int:
        return len(self._all_sessions)

    # ------------------------------------------------------------------
    # 回滚
    # ------------------------------------------------------------------

    def rollback_step(self, step_name: str, session_manager: Any = None) -> List[str]:
        """回滚单个步骤的副作用。使用 _rolled_back 标记防止重复回滚。"""
        if step_name in self._rolled_back:
            logger.debug(f"步骤 '{step_name}' 已回滚过，跳过")
            return []

        if not session_manager:
            logger.warning("session_manager 未注入，无法回滚")
            self._failed_rollbacks.append({
                "step": step_name,
                "reason": "session_manager 未注入",
                "session_count": len(self._step_sessions.get(step_name, [])),
            })
            return []

        self._rolled_back.add(step_name)
        sessions = self._step_sessions.get(step_name, [])
        if not sessions:
            return []

        terminated: List[str] = []
        for sid in sessions:
            try:
                session_manager.terminate(sid)
                terminated.append(sid)
                logger.info(f"回滚: 终止 session {sid} (步骤: {step_name})")
            except Exception as e:
                logger.error(f"终止 session {sid} 失败: {e}")
                self._failed_rollbacks.append({
                    "step": step_name,
                    "session_id": sid,
                    "error": str(e),
                })

        return terminated

    def rollback_all(self, session_manager: Any) -> Dict[str, Any]:
        """逆序回滚所有已追踪的副作用，返回成功/失败汇总。

        Returns:
            Dict: 包含 terminated（成功终止的 sessions）、
                  terminated_count、failed（失败记录）、failed_count
        """
        if not session_manager:
            logger.warning("session_manager 未注入，无法回滚副作用")
            return {"terminated": [], "terminated_count": 0, "failed": [], "failed_count": 0}

        terminated: List[str] = []
        for step_name in reversed(self._step_order):
            result = self.rollback_step(step_name, session_manager)
            terminated.extend(result)

        failed = list(self._failed_rollbacks)
        summary = {
            "terminated": terminated,
            "terminated_count": len(terminated),
            "failed": failed,
            "failed_count": len(failed),
        }

        if failed:
            logger.error(f"回滚完成但 {len(failed)} 个 session 终止失败: {failed}")

        self.clear()
        return summary

    # ------------------------------------------------------------------
    # 存活检查
    # ------------------------------------------------------------------

    def validate_sessions(self, session_manager: Any) -> Dict[str, Any]:
        """验证所有已注册 sessions 的存活状态。

        Args:
            session_manager: 具有 is_alive(session_id) 方法的会话管理器

        Returns:
            Dict: alive（存活）和 dead（已失效）的 session IDs
        """
        alive: List[str] = []
        dead: List[str] = []

        if not session_manager:
            return {"alive": list(self._all_sessions), "dead": []}

        for sid in self._all_sessions:
            try:
                if session_manager.is_alive(sid):
                    alive.append(sid)
                else:
                    dead.append(sid)
            except Exception:
                alive.append(sid)  # 保守地认为存活

        if dead:
            logger.warning(f"发现 {len(dead)} 个已失效的 sessions: {dead}")

        return {"alive": alive, "dead": dead}

    # ------------------------------------------------------------------
    # 生命周期
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """清空所有追踪记录"""
        self._step_sessions.clear()
        self._all_sessions.clear()
        self._step_order.clear()
        self._rolled_back.clear()
        self._failed_rollbacks.clear()
