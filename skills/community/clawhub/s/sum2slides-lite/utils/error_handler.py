"""
错误处理模块
"""

import time
import traceback
from typing import Optional, Callable, Any, Type, Union
from functools import wraps
from .logger import get_logger


logger = get_logger("error_handler")


class PPTMakerError(Exception):
    """PPT制作工具基础异常类"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, 
                original_error: Optional[Exception] = None):
        """
        初始化异常
        
        Args:
            message: 错误消息
            error_code: 错误代码
            original_error: 原始异常
        """
        self.message = message
        self.error_code = error_code
        self.original_error = original_error
        super().__init__(self.message)
    
    def __str__(self):
        """字符串表示"""
        if self.error_code:
            return f"[{self.error_code}] {self.message}"
        return self.message


class GeneratorError(PPTMakerError):
    """生成器相关异常"""
    pass


class PlatformError(PPTMakerError):
    """平台相关异常"""
    pass


class ConfigError(PPTMakerError):
    """配置相关异常"""
    pass


class FileError(PPTMakerError):
    """文件相关异常"""
    pass


def handle_error(error_message: str = "操作失败", 
                error_code: Optional[str] = None,
                log_level: str = "error",
                raise_exception: bool = True):
    """
    错误处理装饰器
    
    Args:
        error_message: 错误消息
        error_code: 错误代码
        log_level: 日志级别
        raise_exception: 是否抛出异常
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
                
            except PPTMakerError:
                # 如果是我们定义的异常，直接抛出
                raise
                
            except Exception as e:
                # 记录错误
                log_func = getattr(logger, log_level.lower(), logger.error)
                log_func(f"{error_message}: {e}")
                log_func(f"函数: {func.__name__}")
                log_func(f"参数: args={args}, kwargs={kwargs}")
                log_func(f"堆栈跟踪:\n{traceback.format_exc()}")
                
                if raise_exception:
                    # 转换为我们的异常类型
                    raise PPTMakerError(
                        message=error_message,
                        error_code=error_code,
                        original_error=e
                    )
                else:
                    return None
        
        return wrapper
    return decorator


def retry_with_backoff(max_retries: int = 3, 
                      initial_delay: float = 1.0,
                      max_delay: float = 30.0,
                      backoff_factor: float = 2.0,
                      exceptions: Union[Type[Exception], tuple] = Exception):
    """
    带指数退避的重试装饰器
    
    Args:
        max_retries: 最大重试次数
        initial_delay: 初始延迟（秒）
        max_delay: 最大延迟（秒）
        backoff_factor: 退避因子
        exceptions: 要捕获的异常类型
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    if attempt > 0:
                        logger.info(f"🔄 重试 {attempt}/{max_retries}: {func.__name__}")
                        logger.info(f"   等待 {delay:.1f}秒后重试...")
                    
                    return func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt < max_retries:
                        # 计算下一次延迟
                        delay = min(delay * backoff_factor, max_delay)
                        
                        # 记录错误但不抛出
                        logger.warning(f"尝试 {attempt+1} 失败: {e}")
                        logger.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
                        
                        # 等待
                        time.sleep(delay)
                    else:
                        # 最后一次尝试也失败
                        logger.error(f"所有 {max_retries+1} 次尝试都失败")
                        raise
            
            # 理论上不会执行到这里
            raise last_exception if last_exception else Exception("未知错误")
        
        return wrapper
    return decorator


def safe_execute(func: Callable, *args, default_return: Any = None, **kwargs) -> Any:
    """
    安全执行函数，捕获所有异常
    
    Args:
        func: 要执行的函数
        *args: 函数参数
        default_return: 异常时的默认返回值
        **kwargs: 函数关键字参数
        
    Returns:
        函数返回值或默认值
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"安全执行失败: {func.__name__} - {e}")
        logger.debug(f"堆栈跟踪:\n{traceback.format_exc()}")
        return default_return


class ErrorContext:
    """错误上下文管理器"""
    
    def __init__(self, error_message: str = "操作失败", 
                error_code: Optional[str] = None,
                log_error: bool = True):
        """
        初始化错误上下文
        
        Args:
            error_message: 错误消息
            error_code: 错误代码
            log_error: 是否记录错误
        """
        self.error_message = error_message
        self.error_code = error_code
        self.log_error = log_error
    
    def __enter__(self):
        """进入上下文"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文"""
        if exc_type is not None:
            if self.log_error:
                logger.error(f"{self.error_message}: {exc_val}")
                if exc_tb:
                    logger.error(f"堆栈跟踪:\n{''.join(traceback.format_tb(exc_tb))}")
            
            # 转换为我们的异常类型
            if not issubclass(exc_type, PPTMakerError):
                raise PPTMakerError(
                    message=self.error_message,
                    error_code=self.error_code,
                    original_error=exc_val
                )
        
        # 返回True表示异常已处理
        return True


def validate_condition(condition: bool, 
                      error_message: str,
                      error_code: Optional[str] = None,
                      exception_type: Type[PPTMakerError] = PPTMakerError):
    """
    验证条件，如果不满足则抛出异常
    
    Args:
        condition: 要验证的条件
        error_message: 错误消息
        error_code: 错误代码
        exception_type: 异常类型
        
    Raises:
        exception_type: 如果条件不满足
    """
    if not condition:
        raise exception_type(error_message, error_code)


# 测试代码
if __name__ == "__main__":
    print("🔧 错误处理模块测试")
    print("=" * 50)
    
    # 测试错误处理装饰器
    @handle_error("测试函数执行失败", "TEST_001")
    def test_function(should_fail: bool = False):
        if should_fail:
            raise ValueError("测试错误")
        return "成功"
    
    # 测试正常执行
    try:
        result = test_function(False)
        print(f"✅ 正常执行: {result}")
    except Exception as e:
        print(f"❌ 意外错误: {e}")
    
    # 测试错误执行
    try:
        result = test_function(True)
        print(f"❌ 应该抛出异常但没有: {result}")
    except PPTMakerError as e:
        print(f"✅ 正确捕获异常: {e}")
    
    # 测试重试装饰器
    attempt_count = 0
    
    @retry_with_backoff(max_retries=2, initial_delay=0.1)
    def test_retry():
        global attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError(f"第{attempt_count}次失败")
        return f"第{attempt_count}次成功"
    
    try:
        result = test_retry()
        print(f"✅ 重试成功: {result}")
    except Exception as e:
        print(f"❌ 重试失败: {e}")
    
    # 测试安全执行
    def risky_function():
        raise RuntimeError("危险操作")
    
    result = safe_execute(risky_function, default_return="默认值")
    print(f"✅ 安全执行结果: {result}")
    
    # 测试错误上下文
    with ErrorContext("上下文测试失败"):
        print("✅ 上下文正常执行")
    
    try:
        with ErrorContext("上下文测试失败"):
            raise ValueError("上下文中的错误")
    except PPTMakerError as e:
        print(f"✅ 上下文错误处理: {e}")
    
    print("\n✅ 错误处理模块测试完成")