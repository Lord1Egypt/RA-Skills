import time
import threading
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentClockInfo:
    """Agent时钟信息"""
    agent_id: str
    clock_offset: float
    round_trip_time: float
    last_sync_time: float
    is_online: bool
    priority: int


class DistributedClockSync:
    """多Agent时钟同步

    V2.0新增模块，解决多Agent协作时的时间混乱问题。

    采用NTP风格的时钟同步协议：
    1. 测量与各Agent的往返延迟
    2. 计算时钟偏移量
    3. 调整本地时钟与各Agent同步
    4. 提供跨Agent的一致时间视图
    """

    def __init__(
        self,
        agent_id: str,
        sync_interval: float = 60.0,
        max_offset_drift: float = 5.0,
        min_samples_for_sync: int = 3
    ):
        self.local_agent_id = agent_id
        self.sync_interval = sync_interval
        self.max_offset_drift = max_offset_drift
        self.min_samples_for_sync = min_samples_for_sync

        self.agents: Dict[str, AgentClockInfo] = {}
        self.local_clock_offset = 0.0
        self.last_full_sync_time = 0.0
        self.is_running = False
        self._lock = threading.Lock()

        self._sync_callbacks: List[Callable] = []
        self._measure_latency_func: Optional[Callable] = None

        self._sync_thread: Optional[threading.Thread] = None

        # 高频同步优化
        self._sync_mode = "normal"  # normal, lightweight, high_frequency
        self._sync_stats = {
            'total_syncs': 0,
            'failed_syncs': 0,
            'average_rtt': 0.0,
            'last_sync_quality': 1.0  # 0-1，1表示最佳
        }
        self._sync_cache: Dict[str, AgentClockInfo] = {}
        self._batch_sync_enabled = True
        self._adaptive_interval_enabled = True
        self._priority_sync_enabled = True

        # 自适应同步间隔参数
        self._min_sync_interval = 10.0  # 最小同步间隔
        self._max_sync_interval = 300.0  # 最大同步间隔
        self._interval_adjustment_factor = 0.1  # 间隔调整因子

    def register_agent(self, agent_id: str, priority: int = 1):
        """注册一个Agent到同步列表"""
        with self._lock:
            if agent_id not in self.agents:
                self.agents[agent_id] = AgentClockInfo(
                    agent_id=agent_id,
                    clock_offset=0.0,
                    round_trip_time=0.0,
                    last_sync_time=0.0,
                    is_online=False,
                    priority=priority
                )

    def unregister_agent(self, agent_id: str):
        """从同步列表移除Agent"""
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]

    def set_measure_latency_func(self, func: Callable[[str], float]):
        """设置测量延迟的函数"""
        self._measure_latency_func = func

    def measure_roundtrip(self, agent_id: str) -> Optional[float]:
        """测量与Agent的往返延迟"""
        if self._measure_latency_func:
            try:
                return self._measure_latency_func(agent_id)
            except Exception as e:
                logger.warning(f"测量延迟失败 {agent_id}: {e}")
                return None

        return self._mock_measure_latency(agent_id)

    def _mock_measure_latency(self, agent_id: str) -> float:
        """模拟延迟测量"""
        import random
        base_latency = 0.05
        jitter = random.uniform(0.01, 0.02)
        return base_latency + jitter

    def sync_single_agent(self, agent_id: str) -> bool:
        """同步单个Agent的时钟"""
        with self._lock:
            if agent_id not in self.agents:
                return False

            t0 = time.time()
            round_trip = self.measure_roundtrip(agent_id)

            if round_trip is None:
                self.agents[agent_id].is_online = False
                return False

            t3 = time.time()

            offset = (t3 - t0 - round_trip) / 2

            agent_info = self.agents[agent_id]
            old_offset = agent_info.clock_offset

            alpha = 0.7
            agent_info.clock_offset = alpha * old_offset + (1 - alpha) * offset if old_offset != 0 else offset
            agent_info.round_trip_time = round_trip
            agent_info.last_sync_time = time.time()
            agent_info.is_online = True

            if abs(agent_info.clock_offset - old_offset) > self.max_offset_drift:
                logger.warning(
                    f"Agent {agent_id} 时钟偏移过大: {old_offset:.3f} -> {agent_info.clock_offset:.3f}"
                )

            return True

    def sync_clocks(self, agent_list: Optional[List[str]] = None) -> Dict[str, bool]:
        """同步所有Agent的时钟"""
        if agent_list is None:
            agent_list = list(self.agents.keys())

        results = {}
        for agent_id in agent_list:
            results[agent_id] = self.sync_single_agent(agent_id)

        self.last_full_sync_time = time.time()

        self._emit_sync_event(results)

        return results

    def _emit_sync_event(self, results: Dict[str, bool]):
        """触发同步事件回调"""
        for callback in self._sync_callbacks:
            try:
                callback(self.local_agent_id, results)
            except Exception as e:
                logger.warning(f"同步回调执行失败: {e}")

    def on_sync(self, callback: Callable):
        """注册同步事件回调"""
        self._sync_callbacks.append(callback)

    def get_consistent_time(self) -> float:
        """获取所有Agent一致的时间视图"""
        return time.time() + self.local_clock_offset

    def get_consistent_datetime(self) -> datetime:
        """获取所有Agent一致的日期时间"""
        from datetime import timezone
        timestamp = self.get_consistent_time()
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    def get_agent_time(self, agent_id: str) -> Optional[float]:
        """获取指定Agent的本地时间视图"""
        with self._lock:
            if agent_id not in self.agents or not self.agents[agent_id].is_online:
                return None

            agent_offset = self.agents[agent_id].clock_offset
            return time.time() + agent_offset

    def get_time_difference(self, agent_id: str) -> Optional[float]:
        """获取本地时间与指定Agent时间的差异"""
        agent_time = self.get_agent_time(agent_id)
        if agent_time is None:
            return None
        return time.time() - agent_time

    def get_master_time(self) -> float:
        """获取主时钟时间"""
        with self._lock:
            online_agents = [
                agent.clock_offset for agent in self.agents.values()
                if agent.is_online
            ]

            if not online_agents:
                return time.time()

            sorted_offsets = sorted(online_agents)
            n = len(sorted_offsets)

            if n % 2 == 1:
                median_offset = sorted_offsets[n // 2]
            else:
                median_offset = (sorted_offsets[n // 2 - 1] + sorted_offsets[n // 2]) / 2

            return time.time() + median_offset

    def start_auto_sync(self):
        """启动自动定期同步"""
        if self.is_running:
            return

        self.is_running = True
        self._sync_thread = threading.Thread(target=self._auto_sync_loop, daemon=True)
        self._sync_thread.start()

    def stop_auto_sync(self):
        """停止自动定期同步"""
        self.is_running = False
        if self._sync_thread:
            self._sync_thread.join(timeout=2.0)
            self._sync_thread = None

    def _auto_sync_loop(self):
        """自动同步循环"""
        while self.is_running:
            try:
                self.sync_clocks()
            except Exception as e:
                logger.error(f"自动同步失败: {e}")

            time.sleep(self.sync_interval)

    def get_sync_status(self) -> Dict[str, Any]:
        """获取时钟同步状态"""
        with self._lock:
            online_count = sum(1 for a in self.agents.values() if a.is_online)
            total_count = len(self.agents)

            offsets = [a.clock_offset for a in self.agents.values() if a.is_online]

            return {
                'local_agent_id': self.local_agent_id,
                'local_clock_offset': self.local_clock_offset,
                'consistent_time': self.get_consistent_time(),
                'master_time': self.get_master_time(),
                'online_agents': online_count,
                'total_agents': total_count,
                'last_full_sync': self.last_full_sync_time,
                'sync_interval': self.sync_interval,
                'is_auto_syncing': self.is_running,
                'agents': {
                    agent_id: {
                        'offset': info.clock_offset,
                        'rtt': info.round_trip_time,
                        'last_sync': info.last_sync_time,
                        'is_online': info.is_online,
                        'priority': info.priority
                    }
                    for agent_id, info in self.agents.items()
                },
                'offset_statistics': {
                    'mean': sum(offsets) / len(offsets) if offsets else 0.0,
                    'max_drift': max(abs(o) for o in offsets) if offsets else 0.0,
                    'min_drift': min(abs(o) for o in offsets) if offsets else 0.0
                }
            }

    def adjust_agent_clock(self, agent_id: str, offset: float):
        """手动调整Agent时钟偏移"""
        with self._lock:
            if agent_id in self.agents:
                self.agents[agent_id].clock_offset = offset
                self.agents[agent_id].last_sync_time = time.time()

    def force_resync(self):
        """强制重新同步所有Agent"""
        with self._lock:
            for agent_info in self.agents.values():
                agent_info.last_sync_time = 0

        self.sync_clocks()

    # 高频同步协议优化
    def set_sync_mode(self, mode: str):
        """设置同步模式
        
        Args:
            mode: 同步模式，可选值：
                - normal: 正常模式
                - lightweight: 轻量模式（适用于高频低价值场景）
                - high_frequency: 高频模式（适用于关键路径）
        """
        if mode in ["normal", "lightweight", "high_frequency"]:
            self._sync_mode = mode
            if mode == "high_frequency":
                self.sync_interval = min(self.sync_interval, 10.0)
            elif mode == "lightweight":
                self.sync_interval = max(self.sync_interval, 120.0)

    def sync_clocks_lightweight(self, agent_list: Optional[List[str]] = None) -> Dict[str, bool]:
        """轻量同步模式
        
        适用于高频低价值场景，使用缓存和简化的同步逻辑
        """
        if agent_list is None:
            agent_list = list(self.agents.keys())

        results = {}
        with self._lock:
            for agent_id in agent_list:
                if agent_id in self._sync_cache and time.time() - self._sync_cache[agent_id].last_sync_time < 30.0:
                    # 使用缓存的同步结果
                    results[agent_id] = True
                    continue

                # 简化的同步逻辑
                t0 = time.time()
                round_trip = self.measure_roundtrip(agent_id)
                t3 = time.time()

                if round_trip is not None:
                    offset = (t3 - t0 - round_trip) / 2
                    if agent_id in self.agents:
                        self.agents[agent_id].clock_offset = offset
                        self.agents[agent_id].round_trip_time = round_trip
                        self.agents[agent_id].last_sync_time = time.time()
                        self.agents[agent_id].is_online = True
                        self._sync_cache[agent_id] = self.agents[agent_id]
                        results[agent_id] = True
                    else:
                        results[agent_id] = False
                else:
                    results[agent_id] = False

        return results

    def sync_clocks_batch(self, agent_list: Optional[List[str]] = None, batch_size: int = 5) -> Dict[str, bool]:
        """批量同步模式
        
        适用于多Agent场景，减少网络开销
        """
        if not self._batch_sync_enabled:
            return self.sync_clocks(agent_list)

        if agent_list is None:
            agent_list = list(self.agents.keys())

        results = {}
        for i in range(0, len(agent_list), batch_size):
            batch = agent_list[i:i+batch_size]
            batch_results = self.sync_clocks(batch)
            results.update(batch_results)

        return results

    def sync_clocks_priority(self) -> Dict[str, bool]:
        """优先级同步
        
        优先同步高优先级的Agent
        """
        if not self._priority_sync_enabled:
            return self.sync_clocks()

        with self._lock:
            sorted_agents = sorted(
                self.agents.keys(),
                key=lambda x: self.agents[x].priority
            )

        return self.sync_clocks(sorted_agents)

    def _adjust_sync_interval(self, sync_quality: float):
        """自适应调整同步间隔
        
        根据同步质量动态调整同步间隔
        """
        if not self._adaptive_interval_enabled:
            return

        # 质量越高，同步间隔越长
        adjustment = self._interval_adjustment_factor * (sync_quality - 0.5)
        new_interval = self.sync_interval * (1 + adjustment)
        
        # 限制在合理范围内
        self.sync_interval = max(
            self._min_sync_interval,
            min(new_interval, self._max_sync_interval)
        )

    def get_sync_quality(self) -> float:
        """评估同步质量
        
        Returns:
            0-1之间的同步质量分数，1表示最佳
        """
        with self._lock:
            online_agents = [a for a in self.agents.values() if a.is_online]
            if not online_agents:
                return 0.0

            # 计算平均偏移量
            avg_offset = sum(abs(a.clock_offset) for a in online_agents) / len(online_agents)
            # 计算平均往返时间
            avg_rtt = sum(a.round_trip_time for a in online_agents) / len(online_agents)
            # 计算在线率
            online_rate = len(online_agents) / len(self.agents) if self.agents else 0

            # 质量评分
            offset_score = max(0, 1 - avg_offset / 1.0)  # 偏移越小越好
            rtt_score = max(0, 1 - avg_rtt / 0.5)  # RTT越小越好
            online_score = online_rate

            # 加权平均
            quality = 0.4 * offset_score + 0.3 * rtt_score + 0.3 * online_score
            return min(1.0, max(0.0, quality))

    def get_sync_statistics(self) -> Dict[str, Any]:
        """获取同步统计信息"""
        quality = self.get_sync_quality()
        
        return {
            **self._sync_stats,
            'sync_mode': self._sync_mode,
            'current_sync_interval': self.sync_interval,
            'sync_quality': quality,
            'cache_size': len(self._sync_cache),
            'optimizations': {
                'batch_sync': self._batch_sync_enabled,
                'adaptive_interval': self._adaptive_interval_enabled,
                'priority_sync': self._priority_sync_enabled
            }
        }

    def enable_optimization(self, optimization: str, enabled: bool):
        """启用或禁用优化
        
        Args:
            optimization: 优化名称
            enabled: 是否启用
        """
        if optimization == "batch_sync":
            self._batch_sync_enabled = enabled
        elif optimization == "adaptive_interval":
            self._adaptive_interval_enabled = enabled
        elif optimization == "priority_sync":
            self._priority_sync_enabled = enabled

    def get_agent_sync_priority(self, agent_id: str) -> int:
        """获取Agent的同步优先级"""
        with self._lock:
            if agent_id in self.agents:
                return self.agents[agent_id].priority
            return 1

    def update_sync_statistics(self, success: bool, rtt: Optional[float] = None):
        """更新同步统计信息"""
        with self._lock:
            self._sync_stats['total_syncs'] += 1
            if not success:
                self._sync_stats['failed_syncs'] += 1
            if rtt:
                # 更新平均RTT
                alpha = 0.1
                self._sync_stats['average_rtt'] = alpha * rtt + (1 - alpha) * self._sync_stats['average_rtt']
            # 更新同步质量
            self._sync_stats['last_sync_quality'] = self.get_sync_quality()

    def sync_clocks_optimized(self, agent_list: Optional[List[str]] = None) -> Dict[str, bool]:
        """优化的同步方法
        
        根据当前模式和状态选择最佳同步策略
        """
        if self._sync_mode == "lightweight":
            results = self.sync_clocks_lightweight(agent_list)
        elif self._sync_mode == "high_frequency":
            results = self.sync_clocks_priority()
        else:
            results = self.sync_clocks_batch(agent_list)

        # 更新统计信息
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)
        success_rate = success_count / total_count if total_count > 0 else 0
        
        # 调整同步间隔
        quality = self.get_sync_quality()
        self._adjust_sync_interval(quality)
        
        # 更新统计
        self.update_sync_statistics(success_rate > 0.8)
        
        return results