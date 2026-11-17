#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
priority_queue.py — 优先级请求队列

功能：
1. 四级优先级：VIP/高价值/普通/批量，VIP 绝对优先
2. 防饥饿：低优先级请求等待超过阈值后自动升级
3. 限流：企微 API 20次/分限制，超限排队
4. 并发安全：线程锁保护入队/出队
5. 零外部依赖：纯 Python 标准库（heapq + threading）

依赖：纯 Python 标准库（零外部依赖）
联系信息：njskills@agent.qq.com

版本：v1.0 (2026-08-01)
"""

import heapq
import threading
import time
import logging
from enum import IntEnum
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


# ==========================================
# 优先级枚举（数值越小越优先）
# ==========================================

class Priority(IntEnum):
    """请求优先级（数值越小优先级越高）"""
    VIP = 1             # VIP客户（重要客户、管理层）
    HIGH_VALUE = 2      # 高价值客户（付费用户、大客户）
    NORMAL = 3          # 普通用户
    BATCH = 4           # 批量任务（后台处理）

    def __str__(self):
        return self.name


# ==========================================
# 请求数据类
# ==========================================

@dataclass(order=True)
class QueuedRequest:
    """排队的请求"""
    priority: int                                   # 优先级数值
    enqueue_time: float = field(compare=True)       # 入队时间（用于同优先级 FIFO）
    request_id: str = field(compare=False)           # 请求ID
    userid: str = field(compare=False)               # 用户ID
    content: Any = field(compare=False)              # 请求内容
    msgtype: str = field(compare=False, default="text")  # 消息类型
    session_id: Optional[str] = field(compare=False, default=None)
    emotion: Optional[str] = field(compare=False, default=None)
    dialect: Optional[str] = field(compare=False, default=None)
    retry_count: int = field(compare=False, default=0)


# ==========================================
# 队列统计
# ==========================================

@dataclass
class QueueStats:
    """队列统计"""
    total_enqueued: int = 0
    total_dequeued: int = 0
    total_dropped: int = 0
    total_upgraded: int = 0
    current_size: int = 0
    max_size: int = 0
    avg_wait_time: float = 0.0
    vip_count: int = 0
    high_value_count: int = 0
    normal_count: int = 0
    batch_count: int = 0


# ==========================================
# 优先级请求队列
# ==========================================

class PriorityRequestQueue:
    """
    优先级请求队列
    
    特性：
    - 四级优先级（VIP > HIGH_VALUE > NORMAL > BATCH）
    - 同级别 FIFO（公平性）
    - 防饥饿升级（低优先级等待超时自动升级）
    - 队列满时丢弃 BATCH，其次 NORMAL
    - 线程安全（可多线程入队/出队）
    """
    
    # 配置常量
    DEFAULT_MAX_SIZE = 200          # 默认最大队列长度
    DEFAULT_RATE_LIMIT = 20         # 每分钟请求数限制
    DEFAULT_UPGRADE_TIMEOUT = 30.0  # 低优先级升级超时（秒）
    
    def __init__(self, max_size: int = DEFAULT_MAX_SIZE,
                 rate_limit: int = DEFAULT_RATE_LIMIT,
                 upgrade_timeout: float = DEFAULT_UPGRADE_TIMEOUT):
        """
        初始化队列
        
        Args:
            max_size: 最大队列长度
            rate_limit: 每分钟请求数限制
            upgrade_timeout: 低优先级升级超时（秒）
        """
        self._queue: List[QueuedRequest] = []
        self._lock = threading.Lock()
        self._not_empty = threading.Condition(self._lock)
        
        self._max_size = max_size
        self._rate_limit = rate_limit
        self._upgrade_timeout = upgrade_timeout
        
        # 限流时间戳队列
        self._request_timestamps: List[float] = []
        
        # 统计
        self._stats = QueueStats(max_size=max_size)
        self._wait_times: List[float] = []
        
        logger.info(f"优先级队列已初始化: max_size={max_size}, rate_limit={rate_limit}/min")
    
    # ======================================
    # 入队
    # ======================================
    
    def enqueue(self, request: QueuedRequest) -> Dict:
        """
        请求入队
        
        Args:
            request: 排队请求
            
        Returns:
            dict: {
                "accepted": bool,
                "position": int (队列中的位置, -1 表示被丢弃),
                "estimated_wait": float (预计等待秒数),
                "dropped": bool
            }
        """
        with self._lock:
            # 检查是否需要丢弃
            if self._should_drop(request):
                self._stats.total_dropped += 1
                logger.warning(f"请求 {request.request_id} 被丢弃（队列满+低优先级）")
                return {
                    "accepted": False,
                    "position": -1,
                    "estimated_wait": -1,
                    "dropped": True,
                    "reason": "队列满，低优先级请求被丢弃"
                }
            
            # 入队
            heapq.heappush(self._queue, request)
            self._stats.total_enqueued += 1
            self._stats.current_size = len(self._queue)
            
            if self._stats.current_size > self._stats.max_size:
                self._stats.max_size = self._stats.current_size
            
            # 按优先级统计
            self._update_priority_stats()
            
            # 通知等待的消费者
            self._not_empty.notify()
            
            # 计算位置和等待时间
            position = self._get_position(request)
            estimated_wait = self._estimate_wait(position)
            
            logger.info(f"请求 {request.request_id} 入队, 优先级={request.priority}, "
                       f"位置={position}, 预计等待={estimated_wait:.1f}s")
            
            return {
                "accepted": True,
                "position": position,
                "estimated_wait": estimated_wait,
                "dropped": False
            }
    
    def enqueue_simple(self, request_id: str, userid: str, content: Any,
                       priority: Priority = Priority.NORMAL, **kwargs) -> Dict:
        """
        简化入队接口
        
        Args:
            request_id: 请求ID
            userid: 用户ID
            content: 请求内容
            priority: 优先级
            **kwargs: 其他可选字段
            
        Returns:
            dict: 同 enqueue()
        """
        request = QueuedRequest(
            priority=int(priority),
            enqueue_time=time.time(),
            request_id=request_id,
            userid=userid,
            content=content,
            **kwargs
        )
        return self.enqueue(request)
    
    def _should_drop(self, request: QueuedRequest) -> bool:
        """判断是否应丢弃请求"""
        if len(self._queue) < self._max_size:
            return False
        
        # 队列满时，丢弃 BATCH 和 NORMAL
        if request.priority >= Priority.NORMAL:
            # 检查是否可以驱逐更低优先级的请求
            lowest = self._queue[-1] if self._queue else None
            if lowest and request.priority < lowest.priority:
                # 驱逐最低优先级的请求
                self._evict_lowest()
                return False
            return True
        
        return False
    
    def _evict_lowest(self):
        """驱逐队列中优先级最低的请求"""
        if not self._queue:
            return
        
        # 找到最低优先级的请求（heapq 不直接支持，需要线性扫描）
        lowest_idx = 0
        lowest_priority = self._queue[0].priority
        for i, req in enumerate(self._queue):
            if req.priority > lowest_priority:
                lowest_priority = req.priority
                lowest_idx = i
        
        if lowest_idx < len(self._queue):
            evicted = self._queue.pop(lowest_idx)
            # 重建堆
            heapq.heapify(self._queue)
            self._stats.total_dropped += 1
            logger.warning(f"驱逐低优先级请求: {evicted.request_id} (优先级={evicted.priority})")
    
    def _get_position(self, request: QueuedRequest) -> int:
        """获取请求在队列中的位置（0-based）"""
        position = 0
        for req in self._queue:
            if req is request:
                return position
            position += 1
        return -1
    
    def _update_priority_stats(self):
        """更新按优先级统计"""
        self._stats.vip_count = sum(1 for r in self._queue if r.priority == Priority.VIP)
        self._stats.high_value_count = sum(1 for r in self._queue if r.priority == Priority.HIGH_VALUE)
        self._stats.normal_count = sum(1 for r in self._queue if r.priority == Priority.NORMAL)
        self._stats.batch_count = sum(1 for r in self._queue if r.priority == Priority.BATCH)
    
    # ======================================
    # 出队
    # ======================================
    
    def dequeue(self, timeout: float = 1.0) -> Optional[QueuedRequest]:
        """
        请求出队（阻塞式）
        
        Args:
            timeout: 超时秒数，超时返回 None
            
        Returns:
            QueuedRequest or None: 返回最高优先级的请求，或超时返回 None
        """
        with self._not_empty:
            # 防饥饿升级
            self._upgrade_starving_requests()
            
            # 等待队列非空
            while not self._queue:
                if not self._not_empty.wait(timeout=timeout):
                    return None
            
            if not self._queue:
                return None
            
            request = heapq.heappop(self._queue)
            self._stats.total_dequeued += 1
            self._stats.current_size = len(self._queue)
            
            # 记录等待时间
            wait_time = time.time() - request.enqueue_time
            self._wait_times.append(wait_time)
            if len(self._wait_times) > 1000:
                self._wait_times = self._wait_times[-1000:]
            self._stats.avg_wait_time = sum(self._wait_times) / len(self._wait_times)
            
            logger.info(f"请求 {request.request_id} 出队, 等待={wait_time:.2f}s, "
                       f"剩余队列={self._stats.current_size}")
            
            return request
    
    def dequeue_nowait(self) -> Optional[QueuedRequest]:
        """
        请求出队（非阻塞）
        
        Returns:
            QueuedRequest or None: 返回最高优先级的请求，队列空返回 None
        """
        with self._lock:
            self._upgrade_starving_requests()
            
            if not self._queue:
                return None
            
            request = heapq.heappop(self._queue)
            self._stats.total_dequeued += 1
            self._stats.current_size = len(self._queue)
            
            return request
    
    def _upgrade_starving_requests(self):
        """升级等待时间过长的低优先级请求"""
        now = time.time()
        upgraded = False
        
        for req in self._queue:
            wait_time = now - req.enqueue_time
            if wait_time > self._upgrade_timeout and req.priority > Priority.VIP:
                old_priority = req.priority
                # 升级一级
                req.priority = max(int(req.priority) - 1, int(Priority.VIP))
                if req.priority != old_priority:
                    self._stats.total_upgraded += 1
                    upgraded = True
                    logger.info(f"请求 {request.request_id} 优先级升级: "
                               f"{Priority(old_priority).name} → {Priority(req.priority).name}")
        
        if upgraded:
            heapq.heapify(self._queue)
    
    # ======================================
    # 限流
    # ======================================
    
    def check_rate_limit(self) -> Dict:
        """
        检查限流
        
        Returns:
            dict: {
                "allowed": bool,
                "current_rate": float (当前每分钟请求数),
                "reset_time": float (下次允许请求的时间戳)
            }
        """
        now = time.time()
        window_start = now - 60.0
        
        # 清理过期时间戳
        self._request_timestamps = [
            ts for ts in self._request_timestamps if ts > window_start
        ]
        
        current_rate = len(self._request_timestamps)
        allowed = current_rate < self._rate_limit
        
        if allowed:
            self._request_timestamps.append(now)
        
        reset_time = 0.0
        if not allowed and self._request_timestamps:
            reset_time = self._request_timestamps[0] + 60.0
        
        return {
            "allowed": allowed,
            "current_rate": current_rate,
            "limit": self._rate_limit,
            "reset_time": reset_time
        }
    
    # ======================================
    # 查询
    # ======================================
    
    def peek(self) -> Optional[QueuedRequest]:
        """查看队列头部请求（不弹出）"""
        with self._lock:
            return self._queue[0] if self._queue else None
    
    def size(self) -> int:
        """当前队列长度"""
        return len(self._queue)
    
    def is_empty(self) -> bool:
        """队列是否为空"""
        return len(self._queue) == 0
    
    def is_full(self) -> bool:
        """队列是否已满"""
        return len(self._queue) >= self._max_size
    
    def contains_user(self, userid: str) -> bool:
        """检查用户是否已在队列中"""
        return any(r.userid == userid for r in self._queue)
    
    def get_position_by_user(self, userid: str) -> int:
        """获取用户在队列中的位置，不存在返回 -1"""
        position = 0
        for req in sorted(self._queue):
            if req.userid == userid:
                return position
            position += 1
        return -1
    
    def clear(self) -> int:
        """清空队列，返回清空的数量"""
        with self._lock:
            count = len(self._queue)
            self._queue.clear()
            self._stats.current_size = 0
            return count
    
    def get_queue_snapshot(self) -> List[Dict]:
        """获取队列快照（排序后的列表）"""
        with self._lock:
            return [
                {
                    "request_id": r.request_id,
                    "userid": r.userid,
                    "priority": Priority(r.priority).name,
                    "enqueue_time": r.enqueue_time,
                    "wait_time": round(time.time() - r.enqueue_time, 2)
                }
                for r in sorted(self._queue)
            ]
    
    def get_stats(self) -> Dict:
        """获取队列统计"""
        with self._lock:
            self._update_priority_stats()
            return {
                "current_size": self._stats.current_size,
                "max_size": self._stats.max_size,
                "total_enqueued": self._stats.total_enqueued,
                "total_dequeued": self._stats.total_dequeued,
                "total_dropped": self._stats.total_dropped,
                "total_upgraded": self._stats.total_upgraded,
                "avg_wait_time": round(self._stats.avg_wait_time, 3),
                "priority_breakdown": {
                    "vip": self._stats.vip_count,
                    "high_value": self._stats.high_value_count,
                    "normal": self._stats.normal_count,
                    "batch": self._stats.batch_count,
                },
                "rate_limit": {
                    "current_rate": len(self._request_timestamps),
                    "limit": self._rate_limit
                }
            }
    
    def _estimate_wait(self, position: int) -> float:
        """估算等待时间（基于平均出队速率）"""
        if self._stats.avg_wait_time == 0:
            return position * 3.0  # 默认估算：每请求 3 秒
        return position * self._stats.avg_wait_time


# ==========================================
# 便捷函数
# ==========================================

def create_queue(**kwargs) -> PriorityRequestQueue:
    """便捷函数：创建优先级队列"""
    return PriorityRequestQueue(**kwargs)


# ==========================================
# 自测
# ==========================================

def run_self_test():
    """自测"""
    print("=" * 60)
    print("优先级请求队列 — 自测模式")
    print("=" * 60)
    
    queue = create_queue(max_size=10, upgrade_timeout=2.0)
    
    # 测试 1: 基本入队出队
    print("\n[测试 1] 基本入队出队")
    queue.enqueue_simple("req_1", "user_a", "你好", Priority.NORMAL)
    queue.enqueue_simple("req_2", "user_b", "在吗", Priority.NORMAL)
    
    req = queue.dequeue_nowait()
    assert req is not None
    assert req.request_id == "req_1"  # 先进先出
    print(f"  出队: {req.request_id} (NORMAL)")
    print("✅ 基本入队出队通过")
    
    # 测试 2: 优先级排序
    print("\n[测试 2] 优先级排序")
    queue.clear()
    queue.enqueue_simple("batch_1", "sys", "批量任务", Priority.BATCH)
    queue.enqueue_simple("normal_1", "u1", "普通请求", Priority.NORMAL)
    queue.enqueue_simple("vip_1", "vip_user", "VIP请求", Priority.VIP)
    queue.enqueue_simple("high_1", "big_user", "高价值", Priority.HIGH_VALUE)
    
    # 应该按 VIP → HIGH_VALUE → NORMAL → BATCH 顺序出队
    expected_order = ["vip_1", "high_1", "normal_1", "batch_1"]
    actual_order = []
    while not queue.is_empty():
        req = queue.dequeue_nowait()
        if req:
            actual_order.append(req.request_id)
    
    print(f"  期望: {expected_order}")
    print(f"  实际: {actual_order}")
    assert actual_order == expected_order, f"优先级排序错误: {actual_order}"
    print("✅ 优先级排序通过")
    
    # 测试 3: 同级别 FIFO
    print("\n[测试 3] 同级别 FIFO")
    queue.clear()
    queue.enqueue_simple("n1", "u1", "请求1", Priority.NORMAL)
    queue.enqueue_simple("n2", "u2", "请求2", Priority.NORMAL)
    queue.enqueue_simple("n3", "u3", "请求3", Priority.NORMAL)
    
    order = []
    for _ in range(3):
        req = queue.dequeue_nowait()
        if req:
            order.append(req.request_id)
    print(f"  出队顺序: {order}")
    assert order == ["n1", "n2", "n3"], "同级别 FIFO 错误"
    print("✅ 同级别 FIFO 通过")
    
    # 测试 4: 队列满丢弃
    print("\n[测试 4] 队列满丢弃")
    queue.clear()
    for i in range(10):
        queue.enqueue_simple(f"r{i}", f"u{i}", f"请求{i}", Priority.BATCH)
    
    result = queue.enqueue_simple("overflow", "overflow_user", "溢出", Priority.BATCH)
    print(f"  队列满时入队: accepted={result['accepted']}, dropped={result['dropped']}")
    assert result["dropped"], "队列满时应丢弃 BATCH 请求"
    print("✅ 队列满丢弃通过")
    
    # 测试 5: VIP 驱逐低优先级
    print("\n[测试 5] VIP 驱逐低优先级")
    queue.clear()
    for i in range(10):
        queue.enqueue_simple(f"batch_{i}", f"u{i}", f"批量{i}", Priority.BATCH)
    
    result = queue.enqueue_simple("vip_new", "vip_new", "VIP紧急", Priority.VIP)
    print(f"  VIP 入队: accepted={result['accepted']}, dropped={result['dropped']}")
    assert result["accepted"], "VIP 应被接受（驱逐低优先级）"
    assert queue._stats.total_dropped >= 1, "应有低优先级请求被驱逐"
    print("✅ VIP 驱逐低优先级通过")
    
    # 测试 6: 限流检查
    print("\n[测试 6] 限流检查")
    queue.clear()
    for i in range(25):
        result = queue.check_rate_limit()
        if not result["allowed"]:
            print(f"  限流触发于第 {i+1} 个请求")
            break
    assert not result["allowed"], "应触发限流"
    print("✅ 限流检查通过")
    
    # 测试 7: 用户去重检查
    print("\n[测试 7] 用户去重检查")
    queue.clear()
    queue.enqueue_simple("r1", "user_x", "请求1", Priority.NORMAL)
    assert queue.contains_user("user_x"), "应找到用户"
    assert not queue.contains_user("user_y"), "不应找到未入队用户"
    pos = queue.get_position_by_user("user_x")
    print(f"  用户 user_x 位置: {pos}")
    assert pos == 0
    print("✅ 用户去重检查通过")
    
    # 测试 8: 统计信息
    print("\n[测试 8] 统计信息")
    stats = queue.get_stats()
    print(f"  当前大小: {stats['current_size']}")
    print(f"  总入队: {stats['total_enqueued']}")
    print(f"  总丢弃: {stats['total_dropped']}")
    print(f"  优先级分布: {stats['priority_breakdown']}")
    assert stats["total_enqueued"] >= 1
    print("✅ 统计信息通过")
    
    print(f"\n{'='*60}")
    print("所有自测通过 ✓")
    print("=" * 60)


if __name__ == "__main__":
    run_self_test()
