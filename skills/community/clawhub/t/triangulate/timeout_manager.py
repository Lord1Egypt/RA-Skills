"""
统一超时管理器 — Triangulate 工作流的所有超时检查。

统一管理全局超时、阶段超时、Saga 超时、子任务超时。
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, Optional

from schemas import WorkflowPhase

logger = logging.getLogger(__name__)


# ============================================================================
# 超时配置
# ============================================================================

class TimeoutScope(str, Enum):
    """超时作用域"""
    WORKFLOW = "workflow"     # 全局工作流超时
    PHASE = "phase"           # 阶段超时
    SAGA = "saga"             # Saga 事务超时
    SUBTASK = "subtask"       # 子任务超时


@dataclass
class TimeoutConfig:
    """超时配置"""
    scope: TimeoutScope
    timeout_seconds: float
    phase: Optional[WorkflowPhase] = None

    def __post_init__(self):
        if self.scope == TimeoutScope.PHASE and self.phase is None:
            raise ValueError("PHASE 作用域必须指定 phase")


# ============================================================================
# 超时管理器
# ============================================================================

class TimeoutManager:
    """统一超时管理器

    用法:
        tm = TimeoutManager(global_timeout=600)
        tm.start()

        # 阶段超时检查
        tm.start_phase(WorkflowPhase.STRATEGY, timeout=180)
        # ... 执行阶段逻辑 ...
        tm.end_phase(WorkflowPhase.STRATEGY)

        # 全局超时检查
        if tm.is_global_timeout():
            raise TimeoutError("全局超时")
    """

    # 默认阶段超时
    DEFAULT_PHASE_TIMEOUTS: Dict[WorkflowPhase, float] = {
        WorkflowPhase.INPUT_VALIDATION: 30,
        WorkflowPhase.STRATEGY: 180,
        WorkflowPhase.DISPATCH: 60,
        WorkflowPhase.EXECUTE: 300,
        WorkflowPhase.REVIEW: 120,
        WorkflowPhase.RENDER: 30,
    }

    def __init__(
        self,
        global_timeout: float = 600,
        phase_timeouts: Optional[Dict[WorkflowPhase, float]] = None,
    ):
        self.global_timeout = global_timeout
        self.phase_timeouts = phase_timeouts or dict(self.DEFAULT_PHASE_TIMEOUTS)
        self._workflow_start: float = 0.0
        self._phase_starts: Dict[WorkflowPhase, float] = {}
        self._phase_ends: Dict[WorkflowPhase, float] = {}
        self._timed_out_phases: list[WorkflowPhase] = []

    # ------------------------------------------------------------------
    # 生命周期
    # ------------------------------------------------------------------

    def start(self):
        """启动全局计时"""
        self._workflow_start = time.time()
        self._phase_starts.clear()
        self._phase_ends.clear()
        self._timed_out_phases.clear()

    def start_phase(self, phase: WorkflowPhase, timeout: Optional[float] = None):
        """开始阶段计时"""
        self._phase_starts[phase] = time.time()
        effective_timeout = timeout or self.phase_timeouts.get(phase, 60)
        logger.info(f"超时管理器：进入阶段 {phase.value} (超时: {effective_timeout}s)")

    def end_phase(self, phase: WorkflowPhase):
        """结束阶段计时"""
        self._phase_ends[phase] = time.time()
        elapsed = self.get_phase_elapsed(phase)
        logger.info(f"超时管理器：阶段 {phase.value} 完成 (耗时: {elapsed:.1f}s)")

    # ------------------------------------------------------------------
    # 超时检查
    # ------------------------------------------------------------------

    def is_global_timeout(self) -> bool:
        """检查全局超时"""
        if self._workflow_start == 0.0:
            return False
        elapsed = time.time() - self._workflow_start
        return elapsed > self.global_timeout

    def get_global_elapsed(self) -> float:
        """获取全局已运行时间"""
        if self._workflow_start == 0.0:
            return 0.0
        return time.time() - self._workflow_start

    def get_global_remaining(self) -> float:
        """获取全局剩余时间"""
        elapsed = self.get_global_elapsed()
        return max(0.0, self.global_timeout - elapsed)

    def is_phase_timeout(self, phase: WorkflowPhase) -> bool:
        """检查阶段超时"""
        elapsed = self.get_phase_elapsed(phase)
        timeout = self.phase_timeouts.get(phase, 60)
        return elapsed > timeout

    def get_phase_elapsed(self, phase: WorkflowPhase) -> float:
        """获取阶段已运行时间"""
        if phase not in self._phase_starts:
            return 0.0
        end = self._phase_ends.get(phase, time.time())
        return end - self._phase_starts[phase]

    def get_phase_remaining(self, phase: WorkflowPhase) -> float:
        """获取阶段剩余时间"""
        elapsed = self.get_phase_elapsed(phase)
        timeout = self.phase_timeouts.get(phase, 60)
        return max(0.0, timeout - elapsed)

    # ------------------------------------------------------------------
    # 批量检查
    # ------------------------------------------------------------------

    def check_all(self) -> Dict[str, bool]:
        """批量检查所有超时状态"""
        return {
            "global_timeout": self.is_global_timeout(),
            "global_elapsed": self.get_global_elapsed(),
            "global_remaining": self.get_global_remaining(),
            "phases": {
                phase.value: {
                    "elapsed": self.get_phase_elapsed(phase),
                    "remaining": self.get_phase_remaining(phase),
                    "timeout": self.is_phase_timeout(phase),
                }
                for phase in self._phase_starts
            },
        }

    # ------------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------------

    def set_phase_timeout(self, phase: WorkflowPhase, seconds: float):
        """动态设置阶段超时"""
        self.phase_timeouts[phase] = seconds

    def set_global_timeout(self, seconds: float):
        """动态设置全局超时"""
        self.global_timeout = seconds

    def get_report(self) -> Dict[str, Any]:
        """获取超时状态报告"""
        return self.check_all()
