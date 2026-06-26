import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentTimeAnchor:
    """Agent时间锚点 - 用于多Agent协作时的时间同步

    问题场景：
    - A Agent完成任务后通知B Agent
    - 两个Agent的时间锚点不一致会导致下游预测漂移

    解决方案：
    - 会话级统一时间锚点
    - 上游事件时间 → 本地时间的自动转换
    - 时间漂移自动检测与校准
    """
    agent_id: str
    session_id: str
    local_offset: float = 0.0
    last_sync_time: float = field(default_factory=time.time)
    upstream_sources: List[str] = field(default_factory=list)

    def sync_with_upstream(self, upstream_event_time: float, upstream_agent_id: str):
        """接收上游事件时间并校准本地锚点

        Args:
            upstream_event_time: 上游事件发生时的UTC时间戳
            upstream_agent_id: 上游Agent ID
        """
        current_time = time.time()
        self.local_offset = upstream_event_time - current_time
        self.last_sync_time = current_time
        if upstream_agent_id not in self.upstream_sources:
            self.upstream_sources.append(upstream_agent_id)

    def get_local_time(self, upstream_time: Optional[float] = None) -> float:
        """将上游时间转换为本地时间

        Args:
            upstream_time: 上游时间戳，如果为None则返回当前本地时间

        Returns:
            本地时间戳
        """
        current_time = time.time()
        if upstream_time is None:
            return current_time + self.local_offset
        return upstream_time + self.local_offset

    def to_upstream_time(self, local_time: float) -> float:
        """将本地时间转换为上游时间

        Args:
            local_time: 本地时间戳

        Returns:
            对应的上游时间戳
        """
        return local_time - self.local_offset


class ConversationTimeAnchorManager:
    """会话级时间锚点管理器 - 解决多Agent时间同步问题

    核心功能：
    1. 为每个Agent维护独立的时间锚点
    2. 支持上游到下游的时间传播
    3. 自动检测和校正时间漂移
    4. 高频同步支持

    使用场景：
    - Agent A 完成任务 → 记录完成时间T_A
    - 通知 Agent B → 传递 T_A
    - Agent B 用 T_A 校准自己的锚点
    - Agent B 的下游预测不再漂移
    """

    def __init__(self, max_drift_threshold: float = 0.5, sync_interval: float = 1.0):
        """

        Args:
            max_drift_threshold: 最大允许时间漂移（秒），超过则告警
            sync_interval: 高频同步间隔（秒）
        """
        self.max_drift_threshold = max_drift_threshold
        self.sync_interval = sync_interval
        self._anchors: Dict[str, Dict[str, AgentTimeAnchor]] = {}
        self._session_master_clock: Dict[str, float] = {}
        self._lock = threading.RLock()

    def create_agent_anchor(self, session_id: str, agent_id: str) -> AgentTimeAnchor:
        """为Agent创建时间锚点

        Args:
            session_id: 会话ID
            agent_id: Agent ID

        Returns:
            Agent时间锚点
        """
        with self._lock:
            if session_id not in self._anchors:
                self._anchors[session_id] = {}
                self._session_master_clock[session_id] = time.time()

            if agent_id not in self._anchors[session_id]:
                anchor = AgentTimeAnchor(
                    agent_id=agent_id,
                    session_id=session_id
                )
                self._anchors[session_id][agent_id] = anchor
                return anchor
            return self._anchors[session_id][agent_id]

    def get_agent_anchor(self, session_id: str, agent_id: str) -> Optional[AgentTimeAnchor]:
        """获取Agent的时间锚点

        Args:
            session_id: 会话ID
            agent_id: Agent ID

        Returns:
            Agent时间锚点，如果不存在返回None
        """
        with self._lock:
            return self._anchors.get(session_id, {}).get(agent_id)

    def sync_upstream_to_downstream(
        self,
        session_id: str,
        upstream_agent_id: str,
        downstream_agent_id: str,
        upstream_event_time: Optional[float] = None
    ):
        """将上游Agent的时间同步到下游Agent

        Args:
            session_id: 会话ID
            upstream_agent_id: 上游Agent ID
            downstream_agent_id: 下游Agent ID
            upstream_event_time: 上游事件时间，如果为None则使用当前时间
        """
        with self._lock:
            upstream_anchor = self.get_agent_anchor(session_id, upstream_agent_id)
            downstream_anchor = self.get_agent_anchor(session_id, downstream_agent_id)

            if not upstream_anchor or not downstream_anchor:
                logger.warning(f"Anchor not found for sync: {upstream_agent_id} -> {downstream_agent_id}")
                return

            event_time = upstream_event_time or upstream_anchor.get_local_time()
            downstream_anchor.sync_with_upstream(event_time, upstream_agent_id)

            logger.debug(
                f"Synced {downstream_agent_id} with {upstream_agent_id} at {event_time}, "
                f"offset: {downstream_anchor.local_offset:.4f}s"
            )

    def broadcast_time_from_upstream(
        self,
        session_id: str,
        source_agent_id: str,
        event_time: Optional[float] = None
    ):
        """将上游Agent的时间广播到所有下游Agent

        Args:
            session_id: 会话ID
            source_agent_id: 源Agent ID
            event_time: 事件时间，如果为None则使用当前时间
        """
        with self._lock:
            anchors = self._anchors.get(session_id, {})
            source_anchor = anchors.get(source_agent_id)

            if not source_anchor:
                return

            broadcast_time = event_time or source_anchor.get_local_time()

            for agent_id, anchor in anchors.items():
                if agent_id != source_agent_id:
                    anchor.sync_with_upstream(broadcast_time, source_agent_id)

    def get_master_clock(self, session_id: str) -> Optional[float]:
        """获取会话主时钟时间

        Args:
            session_id: 会话ID

        Returns:
            主时钟时间戳
        """
        with self._lock:
            return self._session_master_clock.get(session_id)

    def update_master_clock(self, session_id: str, timestamp: Optional[float] = None):
        """更新会话主时钟

        Args:
            session_id: 会话ID
            timestamp: 时间戳，如果为None则使用当前时间
        """
        with self._lock:
            self._session_master_clock[session_id] = timestamp or time.time()

    def check_drift(self, session_id: str, agent_id: str) -> float:
        """检查指定Agent的时间漂移

        Args:
            session_id: 会话ID
            agent_id: Agent ID

        Returns:
            时间漂移量（秒）
        """
        anchor = self.get_agent_anchor(session_id, agent_id)
        if not anchor:
            return 0.0
        return abs(anchor.local_offset)

    def is_drift_excessive(self, session_id: str, agent_id: str) -> bool:
        """判断时间漂移是否过大

        Args:
            session_id: 会话ID
            agent_id: Agent ID

        Returns:
            是否漂移过大
        """
        return self.check_drift(session_id, agent_id) > self.max_drift_threshold

    def get_all_agents_in_session(self, session_id: str) -> List[str]:
        """获取会话中的所有Agent ID

        Args:
            session_id: 会话ID

        Returns:
            Agent ID列表
        """
        with self._lock:
            return list(self._anchors.get(session_id, {}).keys())

    def get_session_sync_status(self, session_id: str) -> Dict[str, Any]:
        """获取会话同步状态

        Args:
            session_id: 会话ID

        Returns:
            同步状态信息
        """
        with self._lock:
            anchors = self._anchors.get(session_id, {})
            master_time = self._session_master_clock.get(session_id)

            agents_status = []
            for agent_id, anchor in anchors.items():
                drift = abs(anchor.local_offset)
                agents_status.append({
                    'agent_id': agent_id,
                    'offset': anchor.local_offset,
                    'drift': drift,
                    'is_excessive': drift > self.max_drift_threshold,
                    'last_sync': anchor.last_sync_time,
                    'upstream_sources': anchor.upstream_sources
                })

            return {
                'session_id': session_id,
                'master_clock': master_time,
                'agent_count': len(anchors),
                'agents': agents_status,
                'any_excessive_drift': any(a['is_excessive'] for a in agents_status)
            }

    def remove_agent(self, session_id: str, agent_id: str):
        """移除Agent的时间锚点

        Args:
            session_id: 会话ID
            agent_id: Agent ID
        """
        with self._lock:
            if session_id in self._anchors and agent_id in self._anchors[session_id]:
                del self._anchors[session_id][agent_id]

    def remove_session(self, session_id: str):
        """移除整个会话

        Args:
            session_id: 会话ID
        """
        with self._lock:
            if session_id in self._anchors:
                del self._anchors[session_id]
            if session_id in self._session_master_clock:
                del self._session_master_clock[session_id]

    def clear_all(self):
        """清除所有会话和锚点"""
        with self._lock:
            self._anchors.clear()
            self._session_master_clock.clear()
