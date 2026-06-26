#!/usr/bin/env python3
"""
熔断器模块 - v1.0.0
防止资源耗尽的熔断保护机制

状态转换:
  CLOSE → OPEN: 失败次数达到阈值
  OPEN → HALF_OPEN: 冷却时间结束
  HALF_OPEN → CLOSE: 探测成功
  HALF_OPEN → OPEN: 探测失败
"""

import time
import threading
import logging
import functools
from enum import Enum
from typing import Callable, TypeVar, Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)
T = TypeVar('T')

class CircuitState(Enum):
    CLOSE = "close"      # 正常熔断器，调用直接通过
    OPEN = "open"        # 熔断开启，调用被拒绝
    HALF_OPEN = "half"   # 半开状态，允许一个探测调用

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5       # 触发熔断的连续失败次数
    success_threshold: int = 2       # 半开后触发恢复的连续成功次数
    timeout: float = 60.0           # OPEN状态的冷却时间（秒）
    excluded_exceptions: tuple = ()  # 不计入失败的异常类型

@dataclass
class CircuitStats:
    total_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    rejected_calls: int = 0
    state_changes: int = 0
    last_failure_time: float = 0
    last_success_time: float = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    attempt_history: list = field(default_factory=list)  # 借鉴 DeerFlow Run 模型：记录每次调用

class CircuitBreakerOpenError(Exception):
    """熔断器开启异常"""
    def __init__(self, name: str, remaining_time: float):
        self.name = name
        self.remaining_time = remaining_time
        super().__init__(f"CircuitBreaker '{name}' is OPEN. Retry in {remaining_time:.1f}s")

class CircuitBreaker:
    """
    熔断器实现
    
    用法:
        cb = CircuitBreaker("search", failure_threshold=5, timeout=60)
        
        @cb
        def fragile_search(query):
            ...
    """
    
    def __init__(
        self,
        name: str,
        config: Optional[CircuitBreakerConfig] = None,
        auto_gc: bool = True
    ):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self._state = CircuitState.CLOSE
        self._stats = CircuitStats()
        self._lock = threading.RLock()
        self._last_state_change = time.time()
        self._half_open_call_done = False
        self._auto_gc = auto_gc
        self._recovery_start_time: float = 0  # 借鉴 DeerFlow：记录恢复开始时间
        
    @property
    def state(self) -> CircuitState:
        with self._lock:
            if self._state == CircuitState.OPEN:
                elapsed = time.time() - self._last_state_change
                if elapsed >= self.config.timeout:
                    self._transition_to(CircuitState.HALF_OPEN)
            return self._state
    
    @property
    def stats(self) -> CircuitStats:
        with self._lock:
            return CircuitStats(
                total_calls=self._stats.total_calls,
                successful_calls=self._stats.successful_calls,
                failed_calls=self._stats.failed_calls,
                rejected_calls=self._stats.rejected_calls,
                state_changes=self._stats.state_changes,
                last_failure_time=self._stats.last_failure_time,
                last_success_time=self._stats.last_success_time,
                consecutive_failures=self._stats.consecutive_failures,
                consecutive_successes=self._stats.consecutive_successes
            )
    
    def _transition_to(self, new_state: CircuitState):
        if self._state == new_state:
            return
        old_state = self._state
        self._state = new_state
        self._last_state_change = time.time()
        self._stats.state_changes += 1
        self._half_open_call_done = False
        if new_state == CircuitState.HALF_OPEN:
            self._recovery_start_time = time.time()  # 借鉴 DeerFlow：记录恢复开始时间
        logger.info(f"[CircuitBreaker] {self.name}: {old_state.value} → {new_state.value}")
    
    def _record_success(self):
        with self._lock:
            self._stats.successful_calls += 1
            self._stats.consecutive_failures = 0
            self._stats.consecutive_successes += 1
            self._stats.last_success_time = time.time()
            
            if self._state == CircuitState.HALF_OPEN:
                if self._stats.consecutive_successes >= self.config.success_threshold:
                    self._transition_to(CircuitState.CLOSE)
                    self._stats.consecutive_successes = 0
    
    def _record_failure(self):
        with self._lock:
            self._stats.failed_calls += 1
            self._stats.consecutive_successes = 0
            self._stats.consecutive_failures += 1
            self._stats.last_failure_time = time.time()
            
            if self._state == CircuitState.CLOSE:
                if self._stats.consecutive_failures >= self.config.failure_threshold:
                    self._transition_to(CircuitState.OPEN)
            elif self._state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
    
    def _can_execute(self) -> bool:
        if self._state == CircuitState.CLOSE:
            return True
        elif self._state == CircuitState.OPEN:
            elapsed = time.time() - self._last_state_change
            if elapsed >= self.config.timeout:
                self._transition_to(CircuitState.HALF_OPEN)
                return True
            return False
        elif self._state == CircuitState.HALF_OPEN:
            # 半开状态只允许一个探测调用
            if self._half_open_call_done:
                return False
            self._half_open_call_done = True
            return True
        return False
    
    def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        """直接调用方式"""
        if not self._can_execute():
            self._stats.rejected_calls += 1
            remaining = max(0, self.config.timeout - (time.time() - self._last_state_change))
            raise CircuitBreakerOpenError(self.name, remaining)
        
        self._stats.total_calls += 1
        try:
            result = func(*args, **kwargs)
            self._record_success()
            return result
        except self.config.excluded_exceptions:
            # 排除的异常不计入失败
            raise
        except Exception:
            self._record_failure()
            raise
    
    def __call__(self, func: Callable[..., T]) -> Callable[..., T]:
        """装饰器方式"""
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return self.call(func, *args, **kwargs)
        return wrapper
    
    def reset(self):
        """手动重置熔断器"""
        with self._lock:
            self._state = CircuitState.CLOSE
            self._stats.consecutive_failures = 0
            self._stats.consecutive_successes = 0
            self._last_state_change = time.time()
            logger.info(f"[CircuitBreaker] {self.name}: manually reset")
    
    def report(self) -> dict:
        """获取熔断器状态报告 - 借鉴 DeerFlow Run 模型"""
        s = self.stats
        remaining = max(0, self.config.timeout - (time.time() - self._last_state_change)) if self.state == CircuitState.OPEN else 0
        recovery_elapsed = time.time() - self._recovery_start_time if self._recovery_start_time > 0 and self.state == CircuitState.HALF_OPEN else 0
        return {
            "name": self.name,
            "state": self.state.value,
            "recovery_state": "recovering" if self.state == CircuitState.HALF_OPEN else ('ready' if self.state == CircuitState.OPEN and remaining > 0 else 'normal'),
            "config": {
                "failure_threshold": self.config.failure_threshold,
                "success_threshold": self.config.success_threshold,
                "timeout": self.config.timeout
            },
            "stats": {
                "total_calls": s.total_calls,
                "success_rate": f"{s.successful_calls/max(s.total_calls,1)*100:.1f}%",
                "consecutive_failures": s.consecutive_failures,
                "consecutive_successes": s.consecutive_successes,
                "rejected_calls": s.rejected_calls
            },
            "open_remaining_seconds": f"{remaining:.1f}s" if remaining > 0 else "N/A",
            "recovery_elapsed_seconds": f"{recovery_elapsed:.1f}s" if recovery_elapsed > 0 else "N/A"
        }

# ============ 全局熔断器管理器 ============

_breakers: dict[str, CircuitBreaker] = {}
_breakers_lock = threading.Lock()

def get_circuit_breaker(
    name: str,
    config: Optional[CircuitBreakerConfig] = None
) -> CircuitBreaker:
    """获取或创建命名熔断器"""
    with _breakers_lock:
        if name not in _breakers:
            _breakers[name] = CircuitBreaker(name, config)
        return _breakers[name]

def circuit_break(
    name: str,
    failure_threshold: int = 5,
    timeout: float = 60.0
):
    """装饰器形式创建熔断器"""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        cb = get_circuit_breaker(name, CircuitBreakerConfig(
            failure_threshold=failure_threshold,
            timeout=timeout
        ))
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            return cb.call(func, *args, **kwargs)
        return wrapper
    return decorator

# ============ 便捷函数 ============

def circuit_search(query_func: Callable[..., T], *args, **kwargs) -> T:
    """
    搜索函数专用熔断包装
    """
    cb = get_circuit_breaker("search", CircuitBreakerConfig(
        failure_threshold=3,
        timeout=30.0
    ))
    return cb.call(query_func, *args, **kwargs)

def circuit_api(api_func: Callable[..., T], *args, **kwargs) -> T:
    """
    API调用专用熔断包装
    """
    cb = get_circuit_breaker("api", CircuitBreakerConfig(
        failure_threshold=5,
        timeout=60.0
    ))
    return cb.call(api_func, *args, **kwargs)

if __name__ == "__main__":
    print("=== circuit_breaker.py 测试 ===")
    
    # 测试1: 正常调用
    cb = CircuitBreaker("test1", CircuitBreakerConfig(failure_threshold=3, timeout=1.0))
    
    @cb
    def succeed():
        return "ok"
    
    print(f"Test1: {succeed()} state={cb.state.value}")
    
    # 测试2: 熔断触发
    cb2 = CircuitBreaker("test2", CircuitBreakerConfig(failure_threshold=2, timeout=2.0))
    call_count = [0]
    
    @cb2
    def fail_twice():
        call_count[0] += 1
        if call_count[0] <= 2:
            raise ConnectionError("connection failed")
        return "recovered"
    
    try:
        fail_twice()
    except ConnectionError:
        print(f"Test2: 第一次失败 (state={cb2.state.value})")
    
    try:
        fail_twice()
    except ConnectionError:
        print(f"Test2: 第二次失败 (state={cb2.state.value})")
    
    try:
        fail_twice()
    except CircuitBreakerOpenError as e:
        print(f"Test2: 熔断开启! 剩余{e.remaining_time:.1f}s")
    
    # 测试3: 状态报告
    print(f"\nTest3 状态报告:")
    print(cb2.report())
    
    # 测试4: 半开恢复
    print(f"\n=== 等待冷却 ===")
    time.sleep(2.5)
    print(f"等待后状态: {cb2.state.value}")
    
    try:
        result = fail_twice()
        print(f"半开探测成功: {result}, 状态={cb2.state.value}")
    except Exception as e:
        print(f"半开探测失败: {e}")
    
    print("\n✅ circuit_breaker.py 模块正常")
