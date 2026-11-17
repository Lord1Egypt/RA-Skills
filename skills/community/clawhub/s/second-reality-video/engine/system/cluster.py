# system/cluster.py - 跨数据中心集群接线层（地平线二·接线）
# ============================================================
# 职责：把地平线二的五个跨 DC 模块真正接进运行时。此前它们只有
#   算法、没有调用点，导致跨节点流量恒为零，系统实际等价于单机。
#
#   1. ClusterConfig      集群拓扑配置（本地 DC / 端点 / 对端 / DC 成员 / 分片归属）
#   2. HeartbeatLoop      后台心跳线程 + 延迟任务泵（绝不阻塞 tick）
#   3. TransportDispatcher 入站 op 白名单分发（未知 op 降级，不写状态）
#
# 设计硬约束（不可违背，否则接线行为会推翻被修复的设计目标）：
#   - 心跳 / AOI 推送 / epoch 广播一律后台线程执行。TcpTransport 单
#     次连接超时 5s，若在 tick 内同步调用 N 个节点，最坏阻塞 5N 秒，
#     等于把 WAN 延迟重新焊回关键路径。
#   - 入站消息必须经 op 白名单。否则任意 TCP 报文可直写共识票表与
#     账本，等于开放一个未鉴权写口。
#   - cluster 为 None 时本模块完全不介入，行为与单机版逐字节一致。
#
# 依赖：无（只依赖标准库；具体 handler 由 runtime.World 注入）
# ============================================================

import logging
import os
import threading
from typing import Callable, Dict, List, Optional

logger = logging.getLogger(__name__)

DEFAULT_HEARTBEAT_INTERVAL = 5.0
DEFAULT_AOI_INTERVAL = 5.0


def _parse_kv_list(raw: str, sep: str, kv: str) -> Dict[str, List[str]]:
    """解析 "k=v1,v2;k=v3" 形态的配置串，返回 {k: [v1, v2]}。"""
    out: Dict[str, List[str]] = {}
    for item in (raw or "").split(sep):
        item = item.strip()
        if not item:
            continue
        key, _, val = item.partition(kv)
        if not key or not val:
            continue
        out[key.strip()] = [v.strip() for v in val.split(",") if v.strip()]
    return out


class ClusterConfig:
    """集群拓扑配置。

    local_dc       本节点所属数据中心 ID
    node_endpoint  本节点对外可达地址 "host:port"（None = 不监听，纯客户端）
    peers          node_id -> "host:port"，对端节点静态清单
    dc_peers       dc_id   -> [node_id, ...]，各 DC 的成员节点
    dc_shards      dc_id   -> [shard_id, ...]，分片归属（不配置则沿用默认归属）
    """

    def __init__(
        self,
        local_dc: str = "dc_local",
        node_endpoint: Optional[str] = None,
        peers: Optional[Dict[str, str]] = None,
        dc_peers: Optional[Dict[str, List[str]]] = None,
        dc_shards: Optional[Dict[str, List[str]]] = None,
        heartbeat_interval_sec: float = DEFAULT_HEARTBEAT_INTERVAL,
        aoi_interval_sec: float = DEFAULT_AOI_INTERVAL,
    ):
        self.local_dc = local_dc
        self.node_endpoint = node_endpoint
        self.peers = dict(peers or {})
        self.dc_peers = {k: list(v) for k, v in (dc_peers or {}).items()}
        self.dc_shards = {k: list(v) for k, v in (dc_shards or {}).items()}
        self.heartbeat_interval_sec = heartbeat_interval_sec
        self.aoi_interval_sec = aoi_interval_sec

    @staticmethod
    def from_env() -> Optional["ClusterConfig"]:
        """从环境变量加载集群拓扑。

        SR_NODE_ENDPOINT 缺失时返回 None → World 保持单机形态。
        SR_PEERS     = "node_b=10.0.0.2:9100,node_c=10.0.0.3:9100"
        SR_DC_PEERS  = "dc_a=node_a;dc_b=node_b;dc_c=node_c"
        SR_DC_SHARDS = "dc_b=shard_1_0_0;dc_c=shard_2_0_0"
        """
        endpoint = os.environ.get("SR_NODE_ENDPOINT", "").strip()
        if not endpoint:
            return None
        local_dc = os.environ.get("SR_LOCAL_DC", "dc_local").strip() or "dc_local"
        peers: Dict[str, str] = {}
        for item in os.environ.get("SR_PEERS", "").split(","):
            item = item.strip()
            if not item:
                continue
            nid, _, addr = item.partition("=")
            if nid and addr:
                peers[nid.strip()] = addr.strip()
        dc_peers = _parse_kv_list(os.environ.get("SR_DC_PEERS", ""), ";", "=")
        dc_shards = _parse_kv_list(os.environ.get("SR_DC_SHARDS", ""), ";", "=")
        return ClusterConfig(
            local_dc=local_dc,
            node_endpoint=endpoint,
            peers=peers,
            dc_peers=dc_peers,
            dc_shards=dc_shards,
            heartbeat_interval_sec=float(
                os.environ.get("SR_HEARTBEAT_INTERVAL", DEFAULT_HEARTBEAT_INTERVAL)
            ),
            aoi_interval_sec=float(
                os.environ.get("SR_AOI_INTERVAL", DEFAULT_AOI_INTERVAL)
            ),
        )

    # ---- 派生视图（全部确定性排序，避免顺序漂移）----
    def peer_ids(self) -> List[str]:
        return sorted(self.peers.keys())

    def remote_dcs(self) -> List[str]:
        """除本 DC 之外的其他 DC ID。"""
        return sorted(d for d in self.dc_peers if d != self.local_dc)

    def dc_nodes(self, dc_id: str) -> List[str]:
        return list(self.dc_peers.get(dc_id, []))

    def local_nodes(self) -> List[str]:
        """本 DC 成员节点，用于 Intra-DC 快环注册。"""
        return list(self.dc_peers.get(self.local_dc, []))


class HeartbeatLoop(threading.Thread):
    """后台心跳线程 + 延迟任务泵。

    两条职责合并进同一个 daemon 线程：
      1. 周期性探测对端活性，把结果喂给 PartitionDetector；
      2. 消费 tick 入队的跨 DC 同步任务（epoch 广播 / AOI 增量）。

    合并的原因：这两类工作都不能占用 tick 的时间片，且共享同一个
    周期节拍最省资源。分开成两个线程只会增加调度复杂度，没有收益。
    """

    def __init__(
        self,
        consensus,
        detector,
        send_fn: Optional[Callable[[str, Dict], Optional[Dict]]] = None,
        interval_sec: float = DEFAULT_HEARTBEAT_INTERVAL,
        skip_node_id: Optional[str] = None,
    ):
        super().__init__(daemon=True, name="sr-heartbeat")
        self._consensus = consensus
        self._detector = detector
        self._send = send_fn
        self._interval = interval_sec
        self._skip = skip_node_id
        self._stop = threading.Event()
        self._tasks: List[Callable[[], None]] = []
        self._lock = threading.Lock()

    # ---- 延迟任务泵：tick 侧入队（非阻塞）----
    def submit(self, task: Callable[[], None]) -> None:
        with self._lock:
            self._tasks.append(task)

    def pending_tasks(self) -> int:
        with self._lock:
            return len(self._tasks)

    def stop(self) -> None:
        self._stop.set()

    # ---- 线程主体 ----
    def run(self) -> None:
        while not self._stop.is_set():
            try:
                self._drain_tasks()
                self._probe_peers()
            except Exception:  # pragma: no cover - 后台线程不得崩溃
                logger.exception("cluster background loop error")
            self._stop.wait(self._interval)

    def _drain_tasks(self) -> None:
        with self._lock:
            tasks, self._tasks = self._tasks, []
        for task in tasks:
            try:
                task()
            except Exception:  # pragma: no cover
                logger.exception("deferred cluster task failed")

    def _probe_peers(self) -> None:
        """逐个探测对端活性，结果驱动分区检测。

        心跳本身由 ConsensusNetwork.heartbeat 经 transport 发出（注入了
        transport 时走真实 ping，否则退化为本地注册表判定）。

        只探测声明了可达地址的节点：创世占位节点没有端点，若一并探测
        会被恒定判为失活，进而把整个集群误判为分区。
        """
        reachable = getattr(self._consensus, "endpoints", None) or {}
        for node_id in sorted(self._consensus.nodes.keys()):
            if self._skip is not None and node_id == self._skip:
                continue
            if node_id not in reachable:
                continue
            try:
                alive = bool(self._consensus.heartbeat(node_id))
            except Exception:  # pragma: no cover
                alive = False
            self._detector.record_heartbeat(node_id, alive)


class TransportDispatcher:
    """入站消息白名单分发器。

    未在白名单内的 op 一律降级返回，不执行任何状态写入。这是入站侧
    唯一的闸门——绕过它等于让任意 TCP 报文直写共识票表与账本。
    """

    def __init__(self):
        self._handlers: Dict[str, Callable[[str, Dict], Optional[Dict]]] = {}

    def register(self, op: str, handler: Callable[[str, Dict], Optional[Dict]]) -> None:
        self._handlers[op] = handler

    def ops(self) -> List[str]:
        return sorted(self._handlers)

    def dispatch(self, source: str, payload: Dict) -> Dict:
        if not isinstance(payload, dict):
            return {"_error": "bad_payload"}
        op = payload.get("op")
        handler = self._handlers.get(op) if isinstance(op, str) else None
        if handler is None:
            logger.warning("rejected unknown op=%s source=%s", op, source)
            return {"_error": "unknown_op", "op": op}
        try:
            return handler(source, payload) or {"ok": True}
        except Exception:  # pragma: no cover
            logger.exception("op handler failed op=%s source=%s", op, source)
            return {"_error": "handler_failed", "op": op}


__all__ = ["ClusterConfig", "HeartbeatLoop", "TransportDispatcher"]
