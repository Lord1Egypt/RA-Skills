# system/spatial_sharding.py - 空间分片与跨域迁移协议（地平线二·模块 1）
# ============================================================
# 职责：按虚拟物理坐标将世界切割为多个 Geo-Shard，分配给离用户
#   物理距离最近的数据中心。当智能体移动至边界区域时，触发无缝
#   握手协议（Handover Protocol）完成状态锁转移与上下文平滑迁移，
#   避免跨数据中心频发强一致性锁。
#
# 依赖：地平线一 A（空间网格 cell 索引）
# ============================================================

import json
import logging
import time
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class GeoShard:
    """单个地理分片定义：边界包围盒 + 归属 DC ID。"""

    def __init__(
        self,
        shard_id: str,
        dc_id: str,
        bounds: Tuple[float, float, float, float, float, float],
        # (x_min, y_min, z_min, x_max, y_max, z_max)
    ):
        self.shard_id = shard_id
        self.dc_id = dc_id
        self.bounds = bounds  # (x_min, y_min, z_min, x_max, y_max, z_max)

    def contains(self, pos: List[float]) -> bool:
        """位置是否在此分片包围盒内。"""
        if len(pos) < 3:
            return False
        x, y, z = pos[0], pos[1], pos[2]
        x1, y1, z1, x2, y2, z2 = self.bounds
        return x1 <= x <= x2 and y1 <= y <= y2 and z1 <= z <= z2

    def overlap(self, other: "GeoShard") -> bool:
        """两个分片是否有重叠区域（边界缓冲区重叠）。"""
        a1, b1, c1, a2, b2, c2 = self.bounds
        d1, e1, f1, d2, e2, f2 = other.bounds
        return not (a2 < d1 or d2 < a1 or b2 < e1 or e2 < b1 or c2 < f1 or f2 < c1)


class ShardRouter:
    """分片路由表：坐标 → 归属分片 → 归属 DC。"""

    def __init__(self):
        self.shards: List[GeoShard] = []
        self._default_shard: Optional[str] = None

    def add_shard(self, shard: GeoShard) -> None:
        self.shards.append(shard)

    def set_default(self, shard_id: str) -> None:
        self._default_shard = shard_id

    def shard_of(self, pos: List[float]) -> Optional[str]:
        """返回坐标所在的分片 ID（首个匹配。无匹配回落默认）。"""
        for s in self.shards:
            if s.contains(pos):
                return s.shard_id
        return self._default_shard

    def dc_of(self, pos: List[float]) -> Optional[str]:
        """返回坐标所属的 DC ID。"""
        sid = self.shard_of(pos)
        if sid is None:
            return None
        for s in self.shards:
            if s.shard_id == sid:
                return s.dc_id
        return None

    def shard_info(self, shard_id: str) -> Optional[GeoShard]:
        for s in self.shards:
            if s.shard_id == shard_id:
                return s
        return None

    def neighbor_shards(self, shard_id: str) -> List[str]:
        """返回与指定分片有重叠边界的分片 ID 列表。"""
        target = self.shard_info(shard_id)
        if target is None:
            return []
        return [
            s.shard_id
            for s in self.shards
            if s.shard_id != shard_id and target.overlap(s)
        ]


class HandoverProtocol:
    """跨域握手协议：Agent 跨分片边界时进行状态锁转移与上下文迁移。

    流程：发起方(Origin DC) → 锁定 → 序列化 → 移交 → 接收方(Target DC) → 确认 → 释放
    """

    STATUS_PENDING = "pending"
    STATUS_LOCKED = "locked"
    STATUS_TRANSFERRING = "transferring"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    def __init__(
        self,
        transport_send: Optional[Callable[[str, Dict], Optional[Dict]]] = None,
    ):
        self._transport = transport_send
        self._active: Dict[str, Dict] = {}  # soul_hash -> handover state

    def set_transport(
        self, transport_send: Callable[[str, Dict], Optional[Dict]]
    ) -> None:
        self._transport = transport_send

    def initiate(
        self,
        soul_hash: str,
        target_shard_id: str,
        target_dc: str,
        context: Dict,
    ) -> str:
        """发起跨域迁移，返回 handover_id。"""
        hid = f"ho_{soul_hash}_{int(time.time()*1000)}"
        self._active[hid] = {
            "soul": soul_hash,
            "target_shard": target_shard_id,
            "target_dc": target_dc,
            "context": context,
            "status": self.STATUS_PENDING,
            "ts": time.time(),
        }
        logger.info(
            "handover initiated hid=%s soul=%s target=%s",
            hid, soul_hash, target_dc,
        )
        return hid

    def lock(self, hid: str) -> bool:
        """锁定源分片上的 Agent 状态（开始迁移，不可变）。"""
        state = self._active.get(hid)
        if state is None:
            return False
        state["status"] = self.STATUS_LOCKED
        return True

    def transfer(self, hid: str) -> Optional[Dict]:
        """通过传输层将 Agent 上下文发送到目标 DC。

        返回目标 DC 的确认响应；传输层未配置则返回 None。
        """
        state = self._active.get(hid)
        if state is None or self._transport is None:
            return None
        state["status"] = self.STATUS_TRANSFERRING
        payload = {
            "op": "handover_transfer",
            "handover_id": hid,
            "soul": state["soul"],
            "target_shard": state["target_shard"],
            "context": state["context"],
        }
        resp = self._transport(state["target_dc"], payload)
        if resp is not None:
            state["status"] = self.STATUS_COMPLETED
        else:
            state["status"] = self.STATUS_FAILED
        return resp

    def complete(self, hid: str) -> bool:
        """确认迁移完成，释放源分片状态。"""
        state = self._active.get(hid)
        if state is None:
            return False
        state["status"] = self.STATUS_COMPLETED
        return True

    def status(self, hid: str) -> Optional[str]:
        state = self._active.get(hid)
        return state["status"] if state else None

    def active_handovers(self) -> List[str]:
        return [h for h, s in self._active.items() if s["status"] != self.STATUS_COMPLETED]

    def cleanup(self, hid: str, ttl: float = 300.0) -> None:
        """清理已完成或超时的 handover。"""
        state = self._active.get(hid)
        if state is None:
            return
        if time.time() - state["ts"] > ttl:
            del self._active[hid]


class ShardManager:
    """分片管理器：整合路由 + 手协，管理当前节点负责的分片。

    在 World 初始化时实例化，管理分片加载/卸载和 Agent 迁移。
    """

    def __init__(self, local_dc: str = "dc_local"):
        self.local_dc = local_dc
        self.router = ShardRouter()
        self.handover = HandoverProtocol()
        self.local_shards: set = set()          # 本节点负责的分片 ID
        self.remote_shards: Dict[str, str] = {}  # shard_id -> dc_id

    def init_default_shards(self, grid_size: Tuple[int, int, int] = (10, 10, 10)) -> None:
        """按固定网格创建默认分片（测试/单 DC 用）。"""
        cx, cy, cz = grid_size
        for ix in range(cx):
            for iy in range(cy):
                for iz in range(cz):
                    sid = f"shard_{ix}_{iy}_{iz}"
                    s = GeoShard(
                        sid,
                        self.local_dc,
                        (ix, iy, iz, ix + 1, iy + 1, iz + 1),
                    )
                    self.router.add_shard(s)
                    self.local_shards.add(sid)
        self.router.set_default("shard_0_0_0")

    def assign_shard(self, shard_id: str, dc_id: str) -> None:
        """将分片分配给某 DC。

        除更新归属集合外，还必须同步更新路由表里该分片对象的 dc_id——
        否则 router.dc_of() 永远读到初始 dc_local，就近路由形同虚设。
        """
        if dc_id == self.local_dc:
            self.local_shards.add(shard_id)
            self.remote_shards.pop(shard_id, None)
        else:
            # 分片不能同时归属本地与远端：不摘出本地集合会导致该分片
            # 永远被判为本地所有，跨域迁移握手永不触发。
            self.local_shards.discard(shard_id)
            self.remote_shards[shard_id] = dc_id
        # 同步路由表：GeoShard.dc_id 是 dc_of 的唯一读源，必须随分配更新
        shard = self.router.shard_info(shard_id)
        if shard is not None:
            shard.dc_id = dc_id

    def is_local(self, pos: List[float]) -> bool:
        """位置是否属于本节点负责的分片。"""
        sid = self.router.shard_of(pos)
        if sid is None:
            return True
        return sid in self.local_shards

    def owner_dc(self, pos: List[float]) -> Optional[str]:
        """返回位置所属的 DC ID。"""
        sid = self.router.shard_of(pos)
        if sid is None:
            return self.local_dc
        if sid in self.local_shards:
            return self.local_dc
        return self.remote_shards.get(sid)


__all__ = [
    "GeoShard", "ShardRouter", "HandoverProtocol", "ShardManager",
]