# system/partition_guard.py - 网络分区与降级保护器（地平线二·模块 5）
# ============================================================
# 职责：应对跨洋海底光纤切断等网络分区（Network Partition / 脑裂）事故。
#   在分区发生时自动切入"局部自治"降级模式；并在网络恢复后通过
#   Merkle Differential Tree（增量哈希树）完成无冲突状态合并与追责审计。
#
# 依赖：地平线一 A（Merkle Root）+ D（增量快照 delta_since）
# ============================================================

import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class PartitionDetector:
    """网络分区检测器：基于心跳活性表判断是否发生脑裂。

    当连续 N 次心跳超时认为对端不可达；当不可达节点数超过半数时
    触发脑裂状态。
    """

    STATE_NORMAL = "normal"
    STATE_PARTITION = "partition"

    def __init__(self, max_missed_heartbeats: int = 3, check_interval: float = 5.0):
        self.max_missed = max_missed_heartbeats
        self.check_interval = check_interval
        self._heartbeat_count: Dict[str, int] = {}
        self._state = self.STATE_NORMAL
        self._last_check = 0.0
        self._partition_ts: Optional[float] = None

    def record_heartbeat(self, node_id: str, success: bool) -> None:
        """记录某节点的心跳成功/失败。"""
        if success:
            self._heartbeat_count[node_id] = 0
        else:
            self._heartbeat_count[node_id] = (
                self._heartbeat_count.get(node_id, 0) + 1
            )

    def check(self, node_ids: List[str]) -> str:
        """检查是否发生网络分区。返回当前状态。"""
        now = time.time()
        if now - self._last_check < self.check_interval:
            return self._state
        self._last_check = now

        missed = sum(
            1
            for n in node_ids
            if self._heartbeat_count.get(n, 0) >= self.max_missed
        )
        total = max(len(node_ids), 1)

        if missed > total / 2:
            if self._state == self.STATE_NORMAL:
                self._state = self.STATE_PARTITION
                self._partition_ts = now
                logger.warning(
                    "network partition detected missed=%d/%d",
                    missed, total,
                )
        else:
            if self._state == self.STATE_PARTITION:
                logger.info("network partition recovered missed=%d/%d", missed, total)
            self._state = self.STATE_NORMAL
            self._partition_ts = None

        return self._state

    @property
    def in_partition(self) -> bool:
        return self._state == self.STATE_PARTITION

    @property
    def partition_since(self) -> Optional[float]:
        return self._partition_ts

    def reset(self, node_ids: List[str]) -> None:
        for n in node_ids:
            self._heartbeat_count[n] = 0
        self._state = self.STATE_NORMAL
        self._partition_ts = None


class LocalAutonomyMode:
    """局部自治降级模式：分区期间本 DC 独立运行，记录操作日志。

    恢复后通过操作日志与 Merkle 差分树合并。
    """

    def __init__(self):
        self._active = False
        self._log: List[Dict] = []  # 降级期间的操作日志

    def enter(self) -> None:
        """进入局部自治模式。"""
        self._active = True
        logger.info("local autonomy mode entered")

    def exit(self) -> List[Dict]:
        """退出局部自治模式，返回降级期间的操作日志。"""
        self._active = False
        log = list(self._log)
        self._log.clear()
        logger.info("local autonomy mode exited, log_entries=%d", len(log))
        return log

    @property
    def active(self) -> bool:
        return self._active

    def record(self, operation: Dict) -> None:
        """记录降级期间的操作（用于后续合并审计）。"""
        if self._active:
            self._log.append({
                **operation,
                "_ts": time.time(),
                "_seq": len(self._log),
            })

    def log_size(self) -> int:
        return len(self._log)


class MerkleDiffTree:
    """Merkle 差分树：比较两个状态并逐层定位差异。

    直接比较规范化 JSON 的顶层键差异（与 SnapshotRegistry.delta_since
    一致），在分区恢复后用于决定合并策略。
    """

    @staticmethod
    def diff(
        local_state: Dict,
        remote_state: Dict,
    ) -> Dict:
        """比较本地与远端状态，返回差异树。

        返回 {added, removed, changed, conflict, can_auto_merge}
        - can_auto_merge: 差异键无重叠（无冲突）→ 可自动合并
        """
        local_keys = set(local_state.keys())
        remote_keys = set(remote_state.keys())
        added = sorted(local_keys - remote_keys)
        removed = sorted(remote_keys - local_keys)
        common = sorted(local_keys & remote_keys)
        changed = []
        for k in common:
            lv = json.dumps(local_state[k], sort_keys=True)
            rv = json.dumps(remote_state[k], sort_keys=True)
            if lv != rv:
                changed.append(k)
        # 冲突：双方同时对同一键做了不同修改
        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "conflict": changed,  # 同时修改的键需要仲裁
            "can_auto_merge": len(added) + len(removed) == len(added) + len(removed) + len(changed)
            and len(changed) == 0,
        }

    @staticmethod
    def auto_merge(
        base_state: Dict,
        local_state: Dict,
        remote_state: Dict,
        conflict_resolver: Optional[Callable[[str, Any, Any, Any], Any]] = None,
    ) -> Dict:
        """三路合并：base→local（本地变更） + base→remote（远端变更）。

        合并规则：
          - 以 base 为起点
          - 本地修改/新增全部应用
          - 远端新增（local 没有的键）追加
          - 冲突键（双方同时修改）调用 resolver 仲裁，默认取 local
        """
        result = dict(base_state)
        # 本地修改/新增全部应用
        for k, v in local_state.items():
            result[k] = v
        # 远端新增（local 没有的键）
        for k, v in remote_state.items():
            if k not in local_state:
                result[k] = v
        # 冲突仲裁
        diff = MerkleDiffTree.diff(local_state, remote_state)
        for k in diff["conflict"]:
            base_v = base_state.get(k)
            local_v = local_state.get(k)
            remote_v = remote_state.get(k)
            if conflict_resolver:
                result[k] = conflict_resolver(k, base_v, local_v, remote_v)
            else:
                result[k] = local_v  # 默认取本地
        return result


class MergeEngine:
    """分区恢复后的状态合并引擎：整合自治日志 + Merkle 差分。

    流程：检测恢复 → 冻结当前状态 → 对比差分 → 自动合并 → 审计追责
    """

    def __init__(self):
        self._merge_log: List[Dict] = []

    def merge(
        self,
        local_state: Dict,
        remote_state: Dict,
        base_state: Optional[Dict] = None,
        local_ops: Optional[List[Dict]] = None,
        remote_ops: Optional[List[Dict]] = None,
        conflict_resolver: Optional[Callable[[str, Any, Any, Any], Any]] = None,
    ) -> Dict:
        """执行合并，返回合并后的状态 + 审计报告。

        base_state 为分区前的基线状态（可从快照快照恢复）。
        无 base_state 时以 local_state 为基线。
        """
        base = base_state or local_state
        merged = MerkleDiffTree.auto_merge(base, local_state, remote_state, conflict_resolver)
        report = {
            "merged_at": time.time(),
            "base_keys": len(base),
            "local_keys": len(local_state),
            "remote_keys": len(remote_state),
            "merged_keys": len(merged),
            "local_ops_count": len(local_ops or []),
            "remote_ops_count": len(remote_ops or []),
            "diff": MerkleDiffTree.diff(local_state, remote_state),
        }
        self._merge_log.append(report)
        logger.info(
            "merge completed base=%d local=%d remote=%d merged=%d conflicts=%d",
            len(base), len(local_state), len(remote_state),
            len(merged), report["diff"]["conflict"],
        )
        return merged

    def merge_history(self) -> List[Dict]:
        return list(self._merge_log)


class PartitionGuard:
    """分区保护器：整合检测器 + 降级模式 + 合并引擎。

    对外暴露唯一入口：tick 时调用 guard() 方法检查状态。
    """

    def __init__(self, node_id: str = ""):
        self.node_id = node_id
        self.detector = PartitionDetector()
        self.autonomy = LocalAutonomyMode()
        self.merge_engine = MergeEngine()

    def guard(self, known_nodes: List[str]) -> str:
        """每 tick 调用：检查分区状态，自动切换降级/恢复。

        返回当前状态（normal / partition）。
        """
        state = self.detector.check(known_nodes)
        if state == PartitionDetector.STATE_PARTITION:
            if not self.autonomy.active:
                self.autonomy.enter()
        else:
            if self.autonomy.active:
                self.autonomy.exit()
        return state

    def record_operation(self, op: Dict) -> None:
        if self.autonomy.active:
            self.autonomy.record(op)

    @property
    def in_partition(self) -> bool:
        return self.detector.in_partition


__all__ = [
    "PartitionDetector", "LocalAutonomyMode", "MerkleDiffTree",
    "MergeEngine", "PartitionGuard",
]