"""零稀泥模式 — 统一事务协调器 transaction_coordinator.py

替代 CompensationManager + UnitOfWork 双轨制。
所有副作用（文件、session、ndjson）注册到同一个协调器，
在任意阶段失败时按 LIFO 逆序执行回滚。

Usage:
    from .transaction_coordinator import TransactionCoordinator
    tx = TransactionCoordinator()
    tx.register("phase0", "bug_dir", lambda: shutil.rmtree(bug_dir))
    ...
    tx.compensate_from("phase2")  # 精确回滚到 phase2
    tx.clear()                    # 全部成功，清理
"""

import logging
from typing import Callable, List, Tuple

log = logging.getLogger("tx")

_PHASE_ORDER = ["phase0", "phase1", "phase2", "phase3", "phase4"]


class TransactionCoordinator:
    """统一事务协调器 — 跨 Phase 事务管理

    替代 CompensationManager + UnitOfWork 的双轨制。
    所有模块的副作用注册到同一个协调器。

    核心原则：
    1. 每个 Phase 的副作用通过 register() 注册
    2. 任意 Phase 失败时，compensate_from() 按逆序回滚
    3. 回滚操作是幂等的（可重复执行）
    4. clear() 在全部成功时清理
    5. 支持上下文管理器 begin_phase() 语法糖
    """

    def __init__(self):
        self._entries: List[Tuple[str, str, Callable]] = []
        # (phase_name, resource_id, undo_callable)
        self._rolled_back = False

    def register(self, phase: str, resource_id: str, undo: Callable):
        """注册一个可回滚操作

        Args:
            phase: 阶段名 (phase0-4)
            resource_id: 资源标识符（文件路径等，用于日志）
            undo: 无参可调用对象，执行回滚（必须幂等）
        """
        self._entries.append((phase, resource_id, undo))

    def compensate_from(self, failed_phase: str) -> List[str]:
        """从 failed_phase 向前回溯，执行所有 <= failed_phase 的 undo

        例如 compensate_from("phase2") 会回滚 phase0, phase1, phase2。

        Returns:
            已回滚的 resource_id 列表
        """
        if self._rolled_back:
            return []
        self._rolled_back = True

        failed_idx = _PHASE_ORDER.index(failed_phase) if failed_phase in _PHASE_ORDER else len(_PHASE_ORDER)
        rolled_back = []

        for phase, rid, undo in reversed(self._entries):
            phase_idx = _PHASE_ORDER.index(phase) if phase in _PHASE_ORDER else -1
            if phase_idx <= failed_idx:
                try:
                    undo()
                    rolled_back.append(rid)
                except Exception as e:
                    log.error("补偿回滚失败 %s/%s: %s", phase, rid, e)

        self._entries.clear()
        if rolled_back:
            log.info("补偿回滚完成: %d 个资源 (failed_phase=%s)", len(rolled_back), failed_phase)
        return rolled_back

    def compensate_all(self) -> List[str]:
        """回滚所有已注册的操作"""
        return self.compensate_from("phase4")

    def reset(self):
        """重置状态，允许在新的重试中使用同一个协调器

        与 clear() 的区别：
        - reset(): 同时清理 _entries 和 _rolled_back 标志（用于重试）
        - clear():  只清理 _entries，保留 _rolled_back 状态（用于成功后清理）
        """
        self._entries.clear()
        self._rolled_back = False

    def clear(self):
        """成功完成全部 Phase 后清理注册表（不执行回滚，不重置 _rolled_back）"""
        self._entries.clear()

    def begin_phase(self, phase: str):
        """上下文管理器：进入指定阶段，离开时自动处理异常

        用法:
            with tx.begin_phase("phase1"):
                # 执行 phase1 操作
                tx.register("phase1", "file", undo_fn)
                # 如果异常，__exit__ 自动 compensate_from("phase1")
        """
        return _PhaseContext(self, phase)

    def __len__(self):
        return len(self._entries)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and not self._rolled_back:
            self.compensate_all()
        return False


class _PhaseContext:
    """Phase 上下文管理器 — 由 TransactionCoordinator.begin_phase() 创建"""
    def __init__(self, tx: TransactionCoordinator, phase: str):
        self._tx = tx
        self._phase = phase

    def __enter__(self):
        return self._tx

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None and not self._tx._rolled_back:
            self._tx.compensate_from(self._phase)
        return False
