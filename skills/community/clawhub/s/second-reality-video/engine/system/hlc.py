# system/hlc.py - 混合逻辑时钟预言机（地平线二·模块 2）
# ============================================================
# 职责：解决全球不同数据中心物理时钟漂移（Clock Drift）导致的因果倒置。
#   结合物理时间（NTP 底座）与 Lamport 逻辑计数，生成跨数据中心
#   全局单调递增的 HLC 时间戳，确保全球事件在异地重放时具备
#   绝对唯一的因果定序。
#
# 依赖：无（纯算法，不依赖任何 second-reality 模块）
# ============================================================

import json
import time
from typing import Dict, Optional, Tuple


class HlcTimestamp:
    """HLC 时间戳：{hh: 物理毫秒(挂钟), ll: 逻辑计数}

    全局单调规则：
      - 物理毫秒永不回退（max(now_ms, last.pt)）
      - 同物理毫秒内用逻辑计数打破冲突
      - 可比较：hh 优先，ll 次之
    """

    __slots__ = ("hh", "ll")

    def __init__(self, hh: int = 0, ll: int = 0):
        self.hh = hh
        self.ll = ll

    def __lt__(self, other: "HlcTimestamp") -> bool:
        return (self.hh, self.ll) < (other.hh, other.ll)

    def __le__(self, other: "HlcTimestamp") -> bool:
        return (self.hh, self.ll) <= (other.hh, other.ll)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HlcTimestamp):
            return NotImplemented
        return self.hh == other.hh and self.ll == other.ll

    def __repr__(self) -> str:
        return f"Hlc({self.hh},{self.ll})"

    def to_dict(self) -> Dict:
        return {"hh": self.hh, "ll": self.ll}

    @staticmethod
    def from_dict(d: Dict) -> "HlcTimestamp":
        return HlcTimestamp(hh=d.get("hh", 0), ll=d.get("ll", 0))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(s: str) -> "HlcTimestamp":
        return HlcTimestamp.from_dict(json.loads(s))


class HybridLogicalClock:
    """混合逻辑时钟：NTP 物理底座 + L lamport 逻辑计数。

    用于跨数据中心（Geo-Distributed）的全局因果定序。
    支持接收远端时间戳以自增（receive 方法），确保因果传递。
    """

    def __init__(self, node_id: str = "", ntp_offset_ms: float = 0.0):
        self.node_id = node_id
        self._pt = 0       # 物理时间（毫秒）
        self._ll = 0       # 逻辑计数
        self._offset = ntp_offset_ms  # NTP 偏差（毫秒，负值=本地慢）

    def _now_ms(self) -> int:
        """当前物理毫秒（经 NTP 偏差修正）。"""
        return int((time.time() * 1000) + self._offset)

    def send(self) -> HlcTimestamp:
        """本地事件产生：生成新的 HLC 时间戳（物理时间不回落）。"""
        now = self._now_ms()
        if now <= self._pt:
            self._ll += 1
        else:
            self._pt = now
            self._ll = 0
        return HlcTimestamp(self._pt, self._ll)

    def receive(self, remote: HlcTimestamp) -> HlcTimestamp:
        """接收远端 HLC 时间戳后自增：取 max(本地, 远端) 再递增。

        确保因果序：收到的事件的时间戳一定小于接收后产生的时间戳。
        """
        now = self._now_ms()
        self._pt = max(self._pt, remote.hh, now)
        self._ll = max(self._ll, remote.ll) + 1
        return HlcTimestamp(self._pt, self._ll)

    def peek(self) -> HlcTimestamp:
        """查看当前 HLC 时间戳（不产生新事件）。"""
        now = max(self._now_ms(), self._pt)
        ll = self._ll
        if now > self._pt:
            ll = 0
        return HlcTimestamp(now, ll)

    def state(self) -> Dict:
        return {"pt": self._pt, "ll": self._ll, "node_id": self.node_id}

    def reset(self) -> None:
        self._pt = 0
        self._ll = 0

    @staticmethod
    def set_ntp_offset(
        reference_time_ms: int, local_time_ms: int
    ) -> float:
        """根据 NTP 参考时间与本地时间的差值，计算 NTP 偏差。

        用法：NTP client 获取参考时间后调用此方法，将返回值传入构造函数。
        """
        return reference_time_ms - local_time_ms


__all__ = ["HlcTimestamp", "HybridLogicalClock"]