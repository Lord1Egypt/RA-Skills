import time
import threading
import psutil
import logging
from typing import Dict, Any, List, Optional, Callable, Set
from collections import deque
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

# 检查依赖项
try:
    import numpy as np
except ImportError:
    raise ImportError("请安装numpy: pip install numpy")

logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """异常类型枚举"""
    TIME_STALL = "time_stall"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    DEPENDENCY_DEADLOCK = "dependency_deadlock"
    EXTERNAL_FAILURE = "external_failure"
    PROGRESS_STALL = "progress_stall"
    MEMORY_LEAK = "memory_leak"


@dataclass
class TaskContext:
    """任务上下文"""
    task_id: str
    task_type: str
    start_time: float
    expected_duration: float
    dependencies: Set[str]
    progress: float = 0.0
    last_progress_update: float = 0.0
    last_resource_check: float = 0.0
    state: str = "running"


class AnomalyDetector:
    """增强型异常检测模块

    V2.0增强版，支持多维异常检测：
    1. 时间停滞 (time_stall) - 任务执行时间异常
    2. 资源耗尽 (resource_exhaustion) - CPU/内存/磁盘资源不足
    3. 依赖死锁 (dependency_deadlock) - 依赖任务卡住
    4. 外部失败 (external_failure) - 外部服务调用失败
    5. 进度停滞 (progress_stall) - 进度长时间无更新
    6. 内存泄漏 (memory_leak) - 内存持续增长

    V1.0只有简单的Z-score时间异常检测
    """

    def __init__(
        self,
        window_size: int = 10,
        threshold: float = 2.0,
        resource_check_interval: float = 5.0,
        progress_stall_threshold: float = 300.0
    ):
        """
        Args:
            window_size: 滑动窗口大小
            threshold: Z-score异常阈值
            resource_check_interval: 资源检查间隔（秒）
            progress_stall_threshold: 进度停滞阈值（秒）
        """
        self.window_size = window_size
        self.threshold = threshold
        self.resource_check_interval = resource_check_interval
        self.progress_stall_threshold = progress_stall_threshold

        self.duration_history: Dict[str, deque] = {}
        self.task_contexts: Dict[str, TaskContext] = {}
        self.blocked_tasks: Dict[str, Set[str]] = {}
        self.external_failures: Dict[str, int] = {}
        self._lock = threading.Lock()
        self._callbacks: Dict[str, Callable] = {}

    def add_duration(self, event_type: str, duration: float):
        """添加事件持续时间

        Args:
            event_type: 事件类型
            duration: 持续时间
        """
        with self._lock:
            if event_type not in self.duration_history:
                self.duration_history[event_type] = deque(maxlen=self.window_size)
            self.duration_history[event_type].append(duration)

    def detect_anomaly(self, event_type: str, current_duration: float) -> bool:
        """检测异常（V1.0兼容方法）

        Args:
            event_type: 事件类型
            current_duration: 当前持续时间

        Returns:
            是否异常
        """
        if event_type not in self.duration_history or len(self.duration_history[event_type]) < 3:
            return False

        history = list(self.duration_history[event_type])
        mean_duration = np.mean(history)
        std_duration = np.std(history)

        if std_duration > 0:
            z_score = abs(current_duration - mean_duration) / std_duration
            return z_score > self.threshold
        else:
            return current_duration > mean_duration * self.threshold

    def detect_blockage(self, task_id: str) -> Dict[str, Any]:
        """多维异常检测

        Args:
            task_id: 任务ID

        Returns:
            多维检测结果字典
        """
        with self._lock:
            if task_id not in self.task_contexts:
                return {'task_id': task_id, 'has_anomaly': False}

            context = self.task_contexts[task_id]
            now = time.time()

            conditions = {
                'time_stall': self.is_time_stalled(context, now),
                'progress_stall': self.is_progress_stalled(context, now),
                'resource_exhaustion': self.check_resource(context, now),
                'dependency_deadlock': self.check_dependency(task_id),
                'external_failure': self.check_external(task_id),
                'memory_leak': self.check_memory_leak(context, now)
            }

            has_anomaly = any(conditions.values())

            result = {
                'task_id': task_id,
                'has_anomaly': has_anomaly,
                'anomaly_types': [k for k, v in conditions.items() if v],
                'conditions': conditions,
                'context': {
                    'elapsed': now - context.start_time,
                    'expected_duration': context.expected_duration,
                    'progress': context.progress
                }
            }

            if has_anomaly:
                self._emit('on_anomaly', result)

            return result

    def is_time_stalled(self, context: TaskContext, now: float) -> bool:
        """检测时间停滞

        Args:
            context: 任务上下文
            now: 当前时间

        Returns:
            是否时间停滞
        """
        elapsed = now - context.start_time
        expected = context.expected_duration

        if expected <= 0:
            return elapsed > 300

        progress_rate = context.progress / max(elapsed, 0.001)
        expected_progress = elapsed / expected

        if expected_progress > 0.5 and context.progress < expected_progress * 0.3:
            return True

        if elapsed > expected * 3:
            return True

        return False

    def is_progress_stalled(self, context: TaskContext, now: float) -> bool:
        """检测进度停滞

        Args:
            context: 任务上下文
            now: 当前时间

        Returns:
            是否进度停滞
        """
        if context.progress >= 1.0:
            return False

        time_since_last_update = now - context.last_progress_update

        if time_since_last_update > self.progress_stall_threshold:
            return True

        if context.progress > 0 and time_since_last_update > self.progress_stall_threshold / 2:
            progress_rate = context.progress / max(context.last_progress_update - context.start_time, 0.001)
            if progress_rate < 0.001:
                return True

        return False

    def check_resource(self, context: TaskContext, now: float) -> bool:
        """检查资源耗尽

        Args:
            context: 任务上下文
            now: 当前时间

        Returns:
            是否资源耗尽
        """
        if now - context.last_resource_check < self.resource_check_interval:
            return False

        context.last_resource_check = now

        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory_percent = psutil.virtual_memory().percent
            disk_percent = psutil.disk_usage('/').percent

            if cpu_percent > 95:
                return True
            if memory_percent > 95:
                return True
            if disk_percent > 95:
                return True

        except Exception as e:
            logger.warning(f"资源检查失败: {e}")

        return False

    def check_dependency(self, task_id: str) -> bool:
        """检查依赖死锁

        Args:
            task_id: 任务ID

        Returns:
            是否存在依赖死锁
        """
        if task_id not in self.blocked_tasks:
            return False

        blocked_set = self.blocked_tasks[task_id]
        if not blocked_set:
            return False

        for blocked_task in blocked_set:
            if blocked_task in self.blocked_tasks:
                if task_id in self.blocked_tasks[blocked_task]:
                    return True

        return False

    def check_external(self, task_id: str) -> bool:
        """检查外部失败

        Args:
            task_id: 任务ID

        Returns:
            是否外部失败
        """
        if task_id not in self.external_failures:
            return False

        failure_count = self.external_failures[task_id]
        return failure_count >= 3

    def check_memory_leak(self, context: TaskContext, now: float) -> bool:
        """检查内存泄漏

        Args:
            context: 任务上下文
            now: 当前时间

        Returns:
            是否可能内存泄漏
        """
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            current_rss = memory_info.rss

            if not hasattr(self, '_initial_memory'):
                self._initial_memory = current_rss
                self._memory_samples = deque(maxlen=10)
                return False

            self._memory_samples.append(current_rss)

            if len(self._memory_samples) < 5:
                return False

            memory_growth = current_rss - self._initial_memory
            growth_ratio = memory_growth / max(self._initial_memory, 1)

            if growth_ratio > 2.0:
                samples = list(self._memory_samples)
                if all(samples[i] <= samples[i+1] for i in range(len(samples)-1)):
                    return True

        except Exception:
            pass

        return False

    def register_task(
        self,
        task_id: str,
        task_type: str,
        expected_duration: float = 60.0,
        dependencies: Optional[List[str]] = None
    ):
        """注册任务

        Args:
            task_id: 任务ID
            task_type: 任务类型
            expected_duration: 预期执行时间（秒）
            dependencies: 依赖任务ID列表
        """
        with self._lock:
            self.task_contexts[task_id] = TaskContext(
                task_id=task_id,
                task_type=task_type,
                start_time=time.time(),
                expected_duration=expected_duration,
                dependencies=set(dependencies or []),
                last_progress_update=time.time(),
                last_resource_check=time.time()
            )

            if dependencies:
                for dep_id in dependencies:
                    if dep_id not in self.blocked_tasks:
                        self.blocked_tasks[dep_id] = set()
                    self.blocked_tasks[dep_id].add(task_id)

    def update_progress(self, task_id: str, progress: float):
        """更新任务进度

        Args:
            task_id: 任务ID
            progress: 进度 0.0 ~ 1.0
        """
        with self._lock:
            if task_id in self.task_contexts:
                self.task_contexts[task_id].progress = progress
                self.task_contexts[task_id].last_progress_update = time.time()

    def mark_dependency_blocked(self, task_id: str, blocked_by: str):
        """标记任务被依赖阻塞

        Args:
            task_id: 任务ID
            blocked_by: 阻塞它的任务ID
        """
        with self._lock:
            if task_id not in self.blocked_tasks:
                self.blocked_tasks[task_id] = set()
            self.blocked_tasks[task_id].add(blocked_by)

    def record_external_failure(self, task_id: str):
        """记录外部失败

        Args:
            task_id: 任务ID
        """
        with self._lock:
            if task_id not in self.external_failures:
                self.external_failures[task_id] = 0
            self.external_failures[task_id] += 1

    def clear_external_failures(self, task_id: str):
        """清除外部失败计数

        Args:
            task_id: 任务ID
        """
        with self._lock:
            if task_id in self.external_failures:
                del self.external_failures[task_id]

    def unregister_task(self, task_id: str):
        """注销任务

        Args:
            task_id: 任务ID
        """
        with self._lock:
            if task_id in self.task_contexts:
                del self.task_contexts[task_id]

            if task_id in self.blocked_tasks:
                del self.blocked_tasks[task_id]

            for blocked_set in self.blocked_tasks.values():
                blocked_set.discard(task_id)

            self.external_failures.pop(task_id, None)

    def on(self, event: str, callback: Callable):
        """注册事件回调

        Args:
            event: 事件名
            callback: 回调函数
        """
        self._callbacks[event] = callback

    def _emit(self, event: str, data: Dict[str, Any]):
        """触发事件

        Args:
            event: 事件名
            data: 事件数据
        """
        if event in self._callbacks:
            try:
                self._callbacks[event](data)
            except Exception as e:
                logger.warning(f"异常回调失败: {e}")

    def get_statistics(self, event_type: str) -> Dict[str, float]:
        """获取事件类型的统计信息

        Args:
            event_type: 事件类型

        Returns:
            统计信息
        """
        if event_type not in self.duration_history or len(self.duration_history[event_type]) == 0:
            return {
                'mean': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'count': 0
            }

        history = list(self.duration_history[event_type])
        return {
            'mean': np.mean(history),
            'std': np.std(history),
            'min': np.min(history),
            'max': np.max(history),
            'count': len(history)
        }

    def is_response_time_abnormal(self, event_type: str, duration: float) -> bool:
        """判断响应时间是否异常

        Args:
            event_type: 事件类型
            duration: 持续时间

        Returns:
            是否异常
        """
        self.add_duration(event_type, duration)
        return self.detect_anomaly(event_type, duration)

    def get_abnormal_events(self) -> List[Dict[str, Any]]:
        """获取所有异常事件类型

        Returns:
            异常事件类型列表
        """
        abnormal_events = []

        for event_type, history in self.duration_history.items():
            if len(history) >= 3:
                current_duration = history[-1]
                if self.detect_anomaly(event_type, current_duration):
                    stats = self.get_statistics(event_type)
                    abnormal_events.append({
                        'event_type': event_type,
                        'current_duration': current_duration,
                        'mean_duration': stats['mean'],
                        'std_duration': stats['std'],
                        'is_abnormal': True
                    })

        return abnormal_events

    def get_all_blockages(self) -> List[Dict[str, Any]]:
        """获取所有阻塞任务

        Returns:
            阻塞任务列表
        """
        blockages = []

        for task_id, blocked_by in self.blocked_tasks.items():
            if blocked_by and task_id in self.task_contexts:
                blockages.append({
                    'task_id': task_id,
                    'blocked_by': list(blocked_by),
                    'is_deadlock': self.check_dependency(task_id),
                    'context': self.task_contexts.get(task_id)
                })

        return blockages

    def clear_history(self, event_type: Optional[str] = None):
        """清空历史记录

        Args:
            event_type: 事件类型，None表示清空所有
        """
        with self._lock:
            if event_type:
                if event_type in self.duration_history:
                    del self.duration_history[event_type]
            else:
                self.duration_history = {}