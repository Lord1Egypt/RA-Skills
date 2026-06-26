#!/usr/bin/env python3
"""
重试机制模块 - v1.0.0
提供指数退避重试装饰器和工具函数
"""

import time
import functools
import logging
from typing import Callable, TypeVar, Optional, Tuple, List, Type

logger = logging.getLogger(__name__)
T = TypeVar('T')

# 可重试的异常类型（默认）
DEFAULT_RETRY_EXCEPTIONS: Tuple[Type[Exception], ...] = (
    ConnectionError,
    TimeoutError,
    ConnectionResetError,
    ConnectionRefusedError,
)

class RetryExhaustedError(Exception):
    """重试次数耗尽异常"""
    def __init__(self, func_name: str, attempts: int, last_error: Exception):
        self.func_name = func_name
        self.attempts = attempts
        self.last_error = last_error
        super().__init__(f"Retry exhausted for {func_name} after {attempts} attempts: {last_error}")

def retry(
    max_attempts: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_RETRY_EXCEPTIONS,
    on_retry: Optional[Callable[[int, Exception], None]] = None,
    jitter: bool = True
):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数（含首次）
        base_delay: 基础延迟秒数
        max_delay: 最大延迟秒数
        exponential_base: 指数基数
        exceptions: 可重试的异常类型元组
        on_retry: 重试时的回调函数 (attempt, error)
        jitter: 是否添加随机抖动
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> T:
            func_name = getattr(func, '__name__', str(func))
            last_error = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_error = e
                    
                    if attempt == max_attempts:
                        logger.warning(f"[Retry] {func_name} exhausted after {max_attempts} attempts")
                        raise RetryExhaustedError(func_name, max_attempts, e) from e
                    
                    # 计算延迟
                    delay = min(base_delay * (exponential_base ** (attempt - 1)), max_delay)
                    if jitter:
                        import random
                        delay = delay * (0.5 + random.random() * 0.5)
                    
                    logger.info(f"[Retry] {func_name} attempt {attempt}/{max_attempts} failed: {e}. Retrying in {delay:.2f}s")
                    
                    if on_retry:
                        on_retry(attempt, e)
                    
                    time.sleep(delay)
            
            # 不应该走到这里，但以防万一
            if last_error:
                raise last_error
            raise RetryExhaustedError(func_name, max_attempts, Exception("Unknown error"))
        
        return wrapper
    return decorator

def retry_call(
    func: Callable[..., T],
    args: tuple = (),
    kwargs: dict = None,
    exceptions: Tuple[Type[Exception], ...] = DEFAULT_RETRY_EXCEPTIONS,
    max_attempts: int = 3,
    base_delay: float = 1.0,
    on_retry: Optional[Callable[[int, Exception], None]] = None
) -> T:
    """
    函数式重试调用
    
    Args:
        func: 要重试的函数
        args: 位置参数
        kwargs: 关键字参数
        exceptions: 可重试的异常类型
        max_attempts: 最大尝试次数
        base_delay: 基础延迟
        on_retry: 重试回调
    """
    kwargs = kwargs or {}
    wrapped = retry(max_attempts=max_attempts, base_delay=base_delay, exceptions=exceptions, on_retry=on_retry)(func)
    return wrapped(*args, **kwargs)

# ============ 便捷函数 ============

def retry_search(search_func: Callable[..., T], *args, **kwargs) -> T:
    """
    搜索函数专用重试包装（3次重试，1s基础延迟）
    """
    return retry(max_attempts=3, base_delay=1.0, exceptions=Exception)(search_func)(*args, **kwargs)

def retry_api(api_func: Callable[..., T], *args, **kwargs) -> T:
    """
    API调用专用重试包装（5次重试，2s基础延迟，捕获更广）
    """
    return retry(
        max_attempts=5,
        base_delay=2.0,
        exceptions=(Exception,),
        on_retry=lambda a, e: logger.warning(f"[API Retry] attempt {a}: {e}")
    )(api_func)(*args, **kwargs)

if __name__ == "__main__":
    # 测试代码
    print("=== retry.py 装饰器测试 ===")
    
    # 测试1: 成功函数
    @retry(max_attempts=3, base_delay=0.1)
    def succeed_once(counter):
        counter[0] += 1
        if counter[0] < 2:
            raise ConnectionError("not ready")
        return "success"
    
    c = [0]
    result = succeed_once(c)
    print(f"Test1 成功: {result}, attempts={c[0]}")
    
    # 测试2: 始终失败
    @retry(max_attempts=3, base_delay=0.05, exceptions=(ValueError,))
    def always_fail():
        raise ValueError("always fails")
    
    try:
        always_fail()
    except RetryExhaustedError as e:
        print(f"Test2 重试耗尽正常: {e.attempts}次")
    
    # 测试3: 指数退避
    print("\n=== 延迟模拟测试 ===")
    delays = []
    for attempt in range(1, 5):
        d = 1.0 * (2.0 ** (attempt - 1))
        delays.append(d)
    print(f"指数退避序列 (base=1, exp=2): {delays}")
    
    print("\n✅ retry.py 模块正常")
