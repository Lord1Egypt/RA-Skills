# system/aoi_sync.py - 关注域 AOI 与 WAN 增量复制器（地平线二·模块 4）
# ============================================================
# 职责：基于智能体的关注域（Area of Interest），仅对存在跨区感知
#   与交互关系的算力节点同步增量 Delta 状态，剔除 90% 以上
#   无意义的广域网全量广播，节省跨数据中心专线带宽。
#
# 依赖：地平线一 A（空间网格 agents_near）+ C（事件全序 delta）
# ============================================================

import json
import logging
import time
from typing import Callable, Dict, List, Optional, Set, Tuple

logger = logging.getLogger(__name__)


class AoiRegion:
    """单个关注域定义：中心位置 + 感知半径。"""

    def __init__(self, center: List[float], radius: float = 100.0):
        self.center = list(center)
        self.radius = radius

    def contains(self, pos: List[float]) -> bool:
        """位置是否在关注域内（欧几里得距离）。"""
        if len(pos) < 3 or len(self.center) < 3:
            return False
        d2 = sum((a - b) ** 2 for a, b in zip(pos, self.center))
        return d2 <= self.radius * self.radius

    def to_dict(self) -> Dict:
        return {"center": self.center, "radius": self.radius}


class AoiTracker:
    """AOI 跟踪器：维护每个 Agent 的关注域，判断哪些跨节点实体需要同步。"""

    def __init__(self, default_radius: float = 100.0):
        self.default_radius = default_radius
        self._regions: Dict[str, AoiRegion] = {}  # soul_hash -> AoiRegion
        self._remote_entities: Dict[str, List[float]] = {}  # 远端实体 -> 位置

    def set_aoi(self, soul_hash: str, center: List[float], radius: Optional[float] = None) -> None:
        """设置 Agent 的关注域中心与半径。"""
        self._regions[soul_hash] = AoiRegion(center, radius or self.default_radius)

    def remove_aoi(self, soul_hash: str) -> None:
        self._regions.pop(soul_hash, None)

    def track_remote(self, soul_hash: str, pos: List[float]) -> None:
        """注册远端实体位置（来自其他 DC 的 Agent）。"""
        self._remote_entities[soul_hash] = list(pos)

    def untrack_remote(self, soul_hash: str) -> None:
        self._remote_entities.pop(soul_hash, None)

    def relevant_remotes(self, soul_hash: str) -> List[str]:
        """返回某 Agent 的关注域内需要同步的远端实体。"""
        region = self._regions.get(soul_hash)
        if region is None:
            return []
        return sorted(
            s for s, p in self._remote_entities.items() if region.contains(p)
        )

    def all_relevant_remotes(self) -> Set[str]:
        """返回当前所有本地 Agent 需要关注的远端实体集合（去重）。"""
        relevant: Set[str] = set()
        for soul in list(self._regions.keys()):
            relevant.update(self.relevant_remotes(soul))
        return relevant

    def needs_sync_from(self, remote_node: str, remote_positions: Dict[str, List[float]]) -> bool:
        """判断是否需要从某远端节点同步（该节点是否有实体在我的 AOI 内）。"""
        for soul, pos in remote_positions.items():
            for region in self._regions.values():
                if region.contains(pos):
                    return True
        return False


class DeltaSync:
    """增量同步器：计算 AOI 范围内的最小状态变化。

    只同步 changed/added/removed 的实体，不发送全量状态。
    """

    @staticmethod
    def diff(
        local_state: Dict[str, Dict],
        remote_state: Dict[str, Dict],
    ) -> Dict:
        """计算本地相较于远端的状态差异。

        local_state/remote_state: {soul_hash: {key: value}}
        返回: {added: [...], removed: [...], changed: [...], bits: <总变化量>}
        """
        local_keys = set(local_state.keys())
        remote_keys = set(remote_state.keys())
        added = sorted(local_keys - remote_keys)
        removed = sorted(remote_keys - local_keys)
        changed = sorted(
            k
            for k in (local_keys & remote_keys)
            if json.dumps(local_state[k], sort_keys=True)
            != json.dumps(remote_state[k], sort_keys=True)
        )
        return {
            "added": added,
            "removed": removed,
            "changed": changed,
            "bits": len(added) + len(removed) + len(changed),
        }

    @staticmethod
    def apply_delta(
        state: Dict[str, Dict],
        delta: Dict,
        added_data: Optional[Dict[str, Dict]] = None,
    ) -> Dict[str, Dict]:
        """将增量应用到现有状态上。返回新状态（不影响入参）。"""
        result = dict(state)
        for soul in delta.get("added", []):
            if added_data and soul in added_data:
                result[soul] = dict(added_data[soul])
        for soul in delta.get("changed", []):
            if added_data and soul in added_data:
                result[soul] = dict(added_data[soul])
        for soul in delta.get("removed", []):
            result.pop(soul, None)
        return result


class SyncScheduler:
    """WAN 同步调度器：定时推拉 AOI 增量。

    带宽控制：可通过 min_interval_sec 控制最小同步间隔。
    """

    def __init__(
        self,
        push_fn: Optional[Callable[[str, Dict], Optional[Dict]]] = None,
        min_interval_sec: float = 5.0,
    ):
        self._push_fn = push_fn
        self._min_interval = min_interval_sec
        self._last_sync: Dict[str, float] = {}  # remote_node -> last sync time

    def set_push(self, push_fn: Callable[[str, Dict], Optional[Dict]]) -> None:
        self._push_fn = push_fn

    def should_sync(self, remote_node: str) -> bool:
        """判断是否应当向某远端节点发起同步（带宽控制）。"""
        last = self._last_sync.get(remote_node, 0.0)
        return (time.time() - last) >= self._min_interval

    def mark_synced(self, remote_node: str) -> None:
        self._last_sync[remote_node] = time.time()

    def push_delta(self, remote_node: str, delta: Dict) -> Optional[Dict]:
        """向远端节点推送增量。"""
        if self._push_fn is None:
            return None
        return self._push_fn(remote_node, {"op": "aoi_delta", "delta": delta})

    def clear(self) -> None:
        self._last_sync.clear()


__all__ = ["AoiRegion", "AoiTracker", "DeltaSync", "SyncScheduler"]