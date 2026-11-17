# system/hierarchical_consensus.py - 分层双环共识体系（地平线二·模块 3）
# ============================================================
# 职责：避免将全局强一致性共识（如传统 Raft/Paxos）直接暴露在广域网（WAN）上。
#   - DC 内部（Intra-DC Fast Path）：走微秒级高频内存共识，保证本地毫秒级物理推演。
#   - DC 跨域（Inter-DC Slow Path）：采用基于 Epoch（纪元）的异步增量共识
#     或 CRDT（无锁最终一致性数据结构），定期清算全局状态。
#
# 依赖：地平线一 共识真联机 + E 传输层
# ============================================================

import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class IntraDcConsensus:
    """DC 内共识（快环）：同机房微秒级内存共识。

    包装现有 ConsensusNetwork，聚焦本地高频提案。
    """

    def __init__(self, local_nodes: Optional[List[str]] = None):
        self.local_nodes = set(local_nodes or [])
        self._proposals: Dict[str, Dict] = {}
        self._votes: Dict[str, Dict[str, bool]] = {}
        self._threshold = 0.67  # ≥2/3

    def add_node(self, node_id: str) -> None:
        self.local_nodes.add(node_id)

    def propose(self, action: Dict, proposer: str) -> str:
        pid = f"intra_{proposer}_{int(time.time()*1000)}_{len(self._proposals)}"
        self._proposals[pid] = {
            "action": action,
            "proposer": proposer,
            "ts": time.time(),
            "status": "open",
        }
        self._votes[pid] = {}
        return pid

    def vote(self, proposal_id: str, node_id: str, approve: bool) -> bool:
        if proposal_id not in self._proposals:
            return False
        if node_id not in self.local_nodes:
            return False
        self._votes[proposal_id][node_id] = approve
        return True

    def approval_rate(self, proposal_id: str) -> float:
        total = len(self.local_nodes)
        if total == 0:
            return 0.0
        votes = self._votes.get(proposal_id, {})
        approves = sum(1 for v in votes.values() if v)
        return approves / total

    def has_consensus(self, proposal_id: str) -> bool:
        return self.approval_rate(proposal_id) >= self._threshold

    def close(self, proposal_id: str) -> str:
        if proposal_id not in self._proposals:
            return "unknown"
        status = "passed" if self.has_consensus(proposal_id) else "rejected"
        self._proposals[proposal_id]["status"] = status
        return status

    def node_count(self) -> int:
        return len(self.local_nodes)


class EpochState:
    """单个纪元（Epoch）的状态快照与 CRDT 增量。"""

    def __init__(self, epoch_id: int = 0):
        self.epoch_id = epoch_id
        self.start_ts = time.time()
        self.end_ts: Optional[float] = None
        self.proposals: List[Dict] = []
        self.merged: Dict[str, Any] = {}  # CRDT 最终合并后的状态

    def add_proposal(self, pid: str, action: Dict, source_dc: str) -> None:
        self.proposals.append({
            "pid": pid,
            "action": action,
            "source_dc": source_dc,
            "ts": time.time(),
        })

    def close(self) -> Dict:
        self.end_ts = time.time()
        return self.merged


class EpochManager:
    """纪元管理器：跨 DC 按 epoch 批量清算。

    每个 epoch 汇集本 DC 内全部已通过的提案，定期向其他 DC 广播
    epoch 摘要，并从其他 DC 接收 epoch 摘要进行 CRDT 合并。
    """

    def __init__(
        self,
        dc_id: str = "",
        epoch_interval_sec: float = 30.0,
        transport_send: Optional[Callable[[str, Dict], Optional[Dict]]] = None,
    ):
        self.dc_id = dc_id
        self.epoch_interval = epoch_interval_sec
        self._transport = transport_send
        self._current_epoch = EpochState(0)
        self._closed_epochs: List[EpochState] = []
        self._last_epoch_ts = time.time()
        self._remote_epochs: Dict[str, int] = {}  # remote_dc -> last_epoch_id

    def set_transport(self, transport_send: Callable[[str, Dict], Optional[Dict]]) -> None:
        self._transport = transport_send

    def record_proposal(self, pid: str, action: Dict, source_dc: str) -> None:
        """将本 DC 内通过的提案记录到当前 epoch。"""
        self._current_epoch.add_proposal(pid, action, source_dc)

    def should_advance(self) -> bool:
        return (time.time() - self._last_epoch_ts) >= self.epoch_interval

    def advance_epoch(self) -> EpochState:
        """关闭当前 epoch，开始新 epoch。"""
        closed = self._current_epoch
        closed.close()
        self._closed_epochs.append(closed)
        self._current_epoch = EpochState(closed.epoch_id + 1)
        self._last_epoch_ts = time.time()
        logger.info(
            "epoch advanced %d -> %d proposals=%d",
            closed.epoch_id, self._current_epoch.epoch_id,
            len(closed.proposals),
        )
        return closed

    def broadcast_epoch(self, target_dc: str) -> Optional[Dict]:
        """向其他 DC 广播当前已关闭的 epoch 摘要。"""
        if self._transport is None:
            return None
        pending = [
            e for e in self._closed_epochs
            if e.epoch_id > self._remote_epochs.get(target_dc, -1)
        ]
        for epoch in pending:
            payload = {
                "op": "epoch_sync",
                "source_dc": self.dc_id,
                "epoch_id": epoch.epoch_id,
                "proposals": epoch.proposals,
            }
            resp = self._transport(target_dc, payload)
            if resp is not None:
                self._remote_epochs[target_dc] = epoch.epoch_id
        return None

    def receive_epoch(self, remote_dc: str, epoch_id: int, proposals: List[Dict]) -> None:
        """接收远端 DC 的 epoch 摘要并合并。"""
        if remote_dc not in self._remote_epochs or epoch_id > self._remote_epochs[remote_dc]:
            self._remote_epochs[remote_dc] = epoch_id
            for p in proposals:
                # 将远端提案标记为已确认
                self._current_epoch.add_proposal(
                    p["pid"], p["action"], remote_dc
                )
            logger.info(
                "received epoch remote_dc=%s epoch=%d proposals=%d",
                remote_dc, epoch_id, len(proposals),
            )


class InterDcConsensus:
    """DC 跨域共识（慢环）：Epoch 批处理 + 最终一致性。

    不要求实时共识，而是通过 epoch 批量对账达成最终一致性。
    """

    def __init__(
        self,
        local_dc_consensus: Optional[IntraDcConsensus] = None,
        dc_id: str = "",
        transport_send: Optional[Callable[[str, Dict], Optional[Dict]]] = None,
    ):
        self.intra = local_dc_consensus or IntraDcConsensus()
        # dc_id 与传输未注入时，广播恒为 None（跨 DC 慢环无出口）。
        # 运行时必须显式注入，否则本模块退化为纯本地纪元计数。
        self.epoch_manager = EpochManager(
            dc_id=dc_id, transport_send=transport_send
        )
        self._dc_nodes: Dict[str, List[str]] = {}         # dc_id -> node_ids
        self._global_epoch_state: Dict[str, Dict] = {}    # 全局纪元状态

    def register_dc(self, dc_id: str, nodes: List[str]) -> None:
        self._dc_nodes[dc_id] = nodes

    def propose(self, action: Dict, proposer: str, dc_id: str) -> Optional[str]:
        """发起提案：先走 Intra-DC 快环，通过后记录到 epoch。"""
        pid = self.intra.propose(action, proposer)
        if self.intra.has_consensus(pid):
            self.intra.close(pid)
            self.epoch_manager.record_proposal(pid, action, dc_id)
            return pid
        return None

    def finalize_proposal(self, pid: str, action: Dict, proposer: str, dc_id: str) -> bool:
        """手动确认提案并记录到 epoch。"""
        if self.intra.has_consensus(pid):
            return True
        # 直接记录为跨 DC 提案
        self.epoch_manager.record_proposal(pid, action, dc_id)
        return True

    def sync_epochs(self, target_dc: str) -> Optional[Dict]:
        """向其他 DC 同步 epoch。"""
        return self.epoch_manager.broadcast_epoch(target_dc)

    def receive_epoch(self, remote_dc: str, epoch_id: int, proposals: List[Dict]) -> None:
        self.epoch_manager.receive_epoch(remote_dc, epoch_id, proposals)

    def tick(self) -> Dict:
        """每 tick 调用：检查是否需要推进 epoch。

        返回 target_dcs 供调用方（runtime）交给后台线程广播——本方法
        自身不发起任何网络调用，避免把 WAN 延迟带进主循环。
        """
        result: Dict[str, Any] = {
            "intra_consensus": None,
            "epoch_advance": None,
            "target_dcs": [],
        }
        if self.epoch_manager.should_advance():
            closed = self.epoch_manager.advance_epoch()
            result["epoch_advance"] = {
                "epoch_id": closed.epoch_id,
                "proposals": len(closed.proposals),
            }
            result["target_dcs"] = sorted(
                d for d in self._dc_nodes if d != self.epoch_manager.dc_id
            )
        return result


__all__ = [
    "IntraDcConsensus", "EpochState", "EpochManager", "InterDcConsensus",
]