import time
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime, timedelta
from enum import Enum
import threading


class TaskState(Enum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    SUSPENDED = "suspended"
    CHECKPOINTED = "checkpointed"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class CronTaskContext:
    """定时任务时间上下文

    管理Cron任务的执行时间上下文，解决定时任务无时序感知的问题。

    V2.0新增模块，用于：
    1. 对齐 scheduled_time（计划执行时间）和 actual_start_time（实际开始时间）
    2. 管理任务的elapsed（已用时长）和remaining（剩余时间）
    3. 判断是否需要checkpoint保存状态
    4. 判断是否需要回来看结果
    """

    def __init__(
        self,
        task_id: str,
        scheduled_time: datetime,
        deadline: Optional[datetime] = None,
        checkpoint_interval: float = 300.0,
        min_expected_duration: float = 10.0,
        max_expected_duration: float = 3600.0
    ):
        """
        Args:
            task_id: 任务ID
            scheduled_time: 计划执行时间
            deadline: 截止时间（可选）
            checkpoint_interval: 检查点保存间隔（秒），默认5分钟
            min_expected_duration: 最小预期执行时间（秒），默认10秒
            max_expected_duration: 最大预期执行时间（秒），默认1小时
        """
        self.task_id = task_id
        self.scheduled_at = scheduled_time
        self.started_at: Optional[datetime] = None
        self.deadline = deadline
        self.checkpoint_interval = checkpoint_interval
        self.min_expected_duration = min_expected_duration
        self.max_expected_duration = max_expected_duration

        self.state = TaskState.PENDING
        self.checkpoint_times: List[datetime] = []
        self.checkpoint_count = 0
        self.progress = 0.0
        self.last_check_time = time.time()

        # 暂停时间管理
        self.suspended_time: float = 0.0
        self.suspended_count: int = 0
        self.last_suspend_time: Optional[datetime] = None

        self._lock = threading.RLock()
        self._callbacks: Dict[str, Callable] = {}

    def start(self, actual_start_time: Optional[datetime] = None):
        """标记任务开始执行

        Args:
            actual_start_time: 实际开始时间，默认当前时间
        """
        with self._lock:
            self.started_at = actual_start_time or datetime.now()
            self.state = TaskState.RUNNING
            self.last_check_time = time.time()

            delay = (self.started_at - self.scheduled_at).total_seconds()
            if delay > 60:
                self._emit('on_delay', delay)

    def _get_elapsed(self) -> float:
        """获取已用时长（秒），包含暂停时间

        Returns:
            已用时长
        """
        if self.started_at is None:
            return 0.0
        return (datetime.now() - self.started_at).total_seconds()

    def _get_active_elapsed(self) -> float:
        """获取实际执行时长（秒），不包含暂停时间

        Returns:
            实际执行时长
        """
        if self.started_at is None:
            return 0.0

        total_elapsed = (datetime.now() - self.started_at).total_seconds()

        # 如果当前处于暂停状态，需要累加当前暂停时段
        current_suspend_time = self.suspended_time
        if self.state == TaskState.SUSPENDED and self.last_suspend_time is not None:
            current_suspend_time += (datetime.now() - self.last_suspend_time).total_seconds()

        return max(0.0, total_elapsed - current_suspend_time)

    def _get_remaining(self) -> float:
        """获取剩余时间（秒）

        Returns:
            剩余时间，如果无deadline则返回-1
        """
        if self.deadline is None:
            return -1.0
        remaining = (self.deadline - datetime.now()).total_seconds()
        return max(0.0, remaining)

    def _get_next_check_interval(self) -> float:
        """计算下次检查间隔

        Returns:
            下次检查间隔（秒）
        """
        elapsed = self._get_elapsed()

        if elapsed < self.min_expected_duration:
            return self.min_expected_duration / 2
        elif elapsed < self.max_expected_duration / 4:
            return 60.0
        elif elapsed < self.max_expected_duration / 2:
            return 180.0
        else:
            return 300.0

    def update_progress(self, progress: float):
        """更新任务进度

        Args:
            progress: 进度 0.0 ~ 1.0
        """
        with self._lock:
            self.progress = max(0.0, min(1.0, progress))
            self.last_check_time = time.time()

    def should_checkpoint(self) -> bool:
        """判断是否需要保存检查点

        检查条件：
        1. 已用时间超过checkpoint_interval
        2. 任务仍处于RUNNING状态

        Returns:
            是否需要保存检查点
        """
        with self._lock:
            if self.state != TaskState.RUNNING:
                return False

            elapsed = self._get_elapsed()
            time_since_last_checkpoint = elapsed - (
                self.checkpoint_times[-1] - self.started_at
            ).total_seconds() if self.checkpoint_times else elapsed

            return time_since_last_checkpoint >= self.checkpoint_interval

    def save_checkpoint(self, state_data: Dict[str, Any]):
        """保存检查点

        Args:
            state_data: 需要保存的状态数据
        """
        with self._lock:
            checkpoint_time = datetime.now()
            self.checkpoint_times.append(checkpoint_time)
            self.checkpoint_count += 1
            self.state = TaskState.CHECKPOINTED

            checkpoint_info = {
                'task_id': self.task_id,
                'checkpoint_time': checkpoint_time,
                'elapsed': self._get_elapsed(),
                'progress': self.progress,
                'state': self.state.value,
                'data': state_data
            }

            self._emit('on_checkpoint', checkpoint_info)
            self.state = TaskState.RUNNING

    def should_recheck(self) -> bool:
        """判断是否需要回来看结果

        检查条件：
        1. 已用时间 >= min_duration
        2. 已用时间 < max_expected_duration
        3. 进度 < 100%

        Returns:
            是否需要回来看结果
        """
        with self._lock:
            elapsed = self._get_elapsed()

            if elapsed < self.min_expected_duration:
                return False

            if elapsed >= self.max_expected_duration:
                return False

            if self.progress >= 1.0:
                return False

            time_since_last_check = time.time() - self.last_check_time
            next_check_interval = self._get_next_check_interval()

            return time_since_last_check >= next_check_interval

    def should_timeout(self) -> bool:
        """判断是否超时（使用实际执行时间，不包含暂停时间）

        Returns:
            是否超时
        """
        with self._lock:
            if self.deadline is None:
                active_elapsed = self._get_active_elapsed()
                return active_elapsed >= self.max_expected_duration
            else:
                return self._get_remaining() <= 0

    def complete(self, success: bool = True):
        """标记任务完成

        Args:
            success: 是否成功完成
        """
        with self._lock:
            self.state = TaskState.COMPLETED if success else TaskState.FAILED
            self.progress = 1.0 if success else self.progress

            completion_info = {
                'task_id': self.task_id,
                'completed_at': datetime.now(),
                'elapsed': self._get_elapsed(),
                'success': success,
                'scheduled_delay': (self.started_at - self.scheduled_at).total_seconds() if self.started_at else 0,
                'checkpoint_count': self.checkpoint_count
            }

            self._emit('on_complete', completion_info)

    def cancel(self):
        """取消任务"""
        with self._lock:
            self.state = TaskState.CANCELLED
            self._emit('on_cancel', {'task_id': self.task_id})

    def suspend(self, reason: str = "waiting_external_signal"):
        """暂停任务执行

        暂停时间不计入超时计时，适用于需要等待用户确认或外部信号的场景。

        Args:
            reason: 暂停原因
        """
        with self._lock:
            if self.state != TaskState.RUNNING:
                return

            self.state = TaskState.SUSPENDED
            self.last_suspend_time = datetime.now()
            self.suspended_count += 1

            suspend_info = {
                'task_id': self.task_id,
                'suspended_at': self.last_suspend_time,
                'reason': reason,
                'elapsed_before_suspend': self._get_active_elapsed(),
                'suspended_count': self.suspended_count
            }

            self._emit('on_suspend', suspend_info)

    def resume(self):
        """恢复任务执行

        恢复后继续计时，暂停时间不计入超时计时。
        """
        with self._lock:
            if self.state != TaskState.SUSPENDED:
                return

            if self.last_suspend_time is not None:
                suspend_duration = (datetime.now() - self.last_suspend_time).total_seconds()
                self.suspended_time += suspend_duration
                self.last_suspend_time = None

            self.state = TaskState.RUNNING
            self.last_check_time = time.time()

            resume_info = {
                'task_id': self.task_id,
                'resumed_at': datetime.now(),
                'suspended_duration': self.suspended_time,
                'active_elapsed': self._get_active_elapsed()
            }

            self._emit('on_resume', resume_info)

    def get_context(self) -> Dict[str, Any]:
        """获取完整时间上下文

        Returns:
            时间上下文信息字典
        """
        with self._lock:
            elapsed = self._get_elapsed()
            active_elapsed = self._get_active_elapsed()
            remaining = self._get_remaining()

            # 计算当前暂停时间（如果处于暂停状态）
            current_suspend = 0.0
            if self.state == TaskState.SUSPENDED and self.last_suspend_time is not None:
                current_suspend = (datetime.now() - self.last_suspend_time).total_seconds()

            total_suspended = self.suspended_time + current_suspend

            return {
                'task_id': self.task_id,
                'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
                'started_at': self.started_at.isoformat() if self.started_at else None,
                'deadline': self.deadline.isoformat() if self.deadline else None,
                'total_elapsed': elapsed,
                'active_elapsed': active_elapsed,
                'suspended_time': total_suspended,
                'suspended_count': self.suspended_count,
                'remaining': remaining,
                'progress': self.progress,
                'state': self.state.value,
                'is_delayed': self._is_delayed(),
                'is_at_risk': self._is_at_risk(),
                'checkpoint_count': self.checkpoint_count,
                'next_check_interval': self._get_next_check_interval(),
                'should_checkpoint': self.should_checkpoint(),
                'should_recheck': self.should_recheck(),
                'should_timeout': self.should_timeout()
            }

    def _is_delayed(self) -> bool:
        """判断任务是否延迟执行

        Returns:
            是否延迟
        """
        if self.started_at is None:
            return False
        delay = (self.started_at - self.scheduled_at).total_seconds()
        return delay > 60

    def _is_at_risk(self) -> bool:
        """判断任务是否处于风险状态

        Returns:
            是否处于风险
        """
        elapsed = self._get_elapsed()
        remaining = self._get_remaining()

        if remaining < 0:
            return elapsed >= self.max_expected_duration

        return remaining < (self.max_expected_duration - elapsed) * 0.3

    def on(self, event: str, callback: Callable):
        """注册事件回调

        Args:
            event: 事件名 (on_delay, on_checkpoint, on_complete, on_cancel)
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
            except Exception:
                pass

    def get_schedule_lag(self) -> float:
        """获取调度延迟

        Returns:
            调度延迟（秒），正值表示延迟启动，负值表示提前启动
        """
        if self.started_at is None:
            return (datetime.now() - self.scheduled_at).total_seconds()
        return (self.started_at - self.scheduled_at).total_seconds()

    def estimate_completion_time(self) -> Optional[datetime]:
        """预估完成时间

        Returns:
            预估完成时间，如果无法预估则返回None
        """
        with self._lock:
            if self.started_at is None or self.progress <= 0:
                return None

            elapsed = self._get_elapsed()
            if elapsed <= 0:
                return None

            total_estimated = elapsed / self.progress
            remaining = total_estimated - elapsed

            return datetime.now() + timedelta(seconds=remaining)