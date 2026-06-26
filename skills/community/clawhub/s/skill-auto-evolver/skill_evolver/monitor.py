"""
技能使用监控模块

负责记录技能使用情况、追踪性能指标
"""

import time
import functools
from typing import Optional, Dict, Any, Callable
from contextlib import contextmanager

from database.models import Database, SkillUsage


class SkillMonitor:
    """技能使用监控器"""
    
    def __init__(self, db: Optional[Database] = None):
        self.db = db or Database()
    
    def log_usage(
        self,
        skill_name: str,
        action: str,
        status: str = "success",
        duration_ms: int = 0,
        context: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> int:
        """
        记录技能使用
        
        Args:
            skill_name: 技能名称
            action: 执行的动作
            status: 状态 (success, failed, timeout)
            duration_ms: 执行耗时（毫秒）
            context: 上下文信息
            error_message: 错误信息（失败时）
        
        Returns:
            记录ID
        """
        usage = SkillUsage(
            skill_name=skill_name,
            action=action,
            status=status,
            duration_ms=duration_ms,
            context=context,
            error_message=error_message
        )
        return self.db.log_usage(usage)
    
    @contextmanager
    def track(self, skill_name: str, action: str, context: Optional[Dict[str, Any]] = None):
        """
        上下文管理器，自动追踪技能执行时间和结果
        
        Example:
            with monitor.track("my-skill", "process") as tracker:
                result = do_something()
                tracker.set_context({"input_size": len(data)})
        """
        tracker = _UsageTracker(self, skill_name, action, context)
        try:
            yield tracker
            tracker.success()
        except Exception as e:
            tracker.failed(str(e))
            raise
    
    def track_decorator(self, skill_name: str, action: Optional[str] = None):
        """
        装饰器，自动追踪函数执行
        
        Example:
            @monitor.track_decorator("my-skill")
            def my_function():
                pass
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                action_name = action or func.__name__
                with self.track(skill_name, action_name) as tracker:
                    tracker.set_context({
                        "args_count": len(args),
                        "kwargs_keys": list(kwargs.keys())
                    })
                    return func(*args, **kwargs)
            return wrapper
        return decorator
    
    def get_stats(self, skill_name: str, days: int = 30) -> Dict[str, Any]:
        """获取技能使用统计"""
        return self.db.get_usage_stats(skill_name, days)
    
    def get_recent_logs(self, skill_name: str, limit: int = 100):
        """获取最近的日志记录"""
        return self.db.get_recent_usage(skill_name, limit)


class _UsageTracker:
    """内部使用追踪器"""
    
    def __init__(
        self,
        monitor: SkillMonitor,
        skill_name: str,
        action: str,
        context: Optional[Dict[str, Any]] = None
    ):
        self.monitor = monitor
        self.skill_name = skill_name
        self.action = action
        self.context = context or {}
        self.start_time = time.time()
        self.status = "running"
        self.error_message = None
    
    def set_context(self, context: Dict[str, Any]):
        """设置上下文信息"""
        self.context.update(context)
    
    def success(self):
        """标记为成功"""
        self.status = "success"
        self._log()
    
    def failed(self, error_message: str):
        """标记为失败"""
        self.status = "failed"
        self.error_message = error_message
        self._log()
    
    def timeout(self):
        """标记为超时"""
        self.status = "timeout"
        self._log()
    
    def _log(self):
        """记录到数据库"""
        duration_ms = int((time.time() - self.start_time) * 1000)
        self.monitor.log_usage(
            skill_name=self.skill_name,
            action=self.action,
            status=self.status,
            duration_ms=duration_ms,
            context=self.context,
            error_message=self.error_message
        )


# 全局监控器实例
_default_monitor: Optional[SkillMonitor] = None


def get_monitor() -> SkillMonitor:
    """获取默认监控器实例"""
    global _default_monitor
    if _default_monitor is None:
        _default_monitor = SkillMonitor()
    return _default_monitor


def log_skill_usage(
    skill_name: str,
    action: str,
    status: str = "success",
    duration_ms: int = 0,
    context: Optional[Dict[str, Any]] = None,
    error_message: Optional[str] = None
) -> int:
    """
    便捷函数：记录技能使用
    
    无需创建 SkillMonitor 实例，直接使用
    """
    return get_monitor().log_usage(
        skill_name=skill_name,
        action=action,
        status=status,
        duration_ms=duration_ms,
        context=context,
        error_message=error_message
    )
