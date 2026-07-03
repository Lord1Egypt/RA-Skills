"""统一错误处理模块"""

import logging
import sys
from typing import Optional, Callable, Any

logger: logging.Logger = logging.getLogger(__name__)

class StockTrackerError(Exception):
    """基础异常类"""
    def __init__(self, message: str, code: Optional[str] = None) -> None:
        super().__init__(message)
        self.code: Optional[str] = code

class DatabaseError(StockTrackerError):
    """数据库相关错误"""
    pass

class APIError(StockTrackerError):
    """API调用错误"""
    pass

class ConfigError(StockTrackerError):
    """配置错误"""
    pass

class CookieError(StockTrackerError):
    """Cookie相关错误"""
    pass

class DataError(StockTrackerError):
    """数据相关错误"""
    pass

def handle_error(error: Exception, context: str = "", exit_on_error: bool = False) -> None:
    """统一错误处理"""
    if isinstance(error, StockTrackerError):
        logger.error(f"{context}: {error} (code: {error.code})")
    else:
        logger.error(f"{context}: {error}")
    
    if exit_on_error:
        sys.exit(1)

def safe_execute(func: Callable[..., Any], *args: Any, exit_on_error: bool = False, **kwargs: Any) -> Any:
    """安全执行函数，捕获异常"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        handle_error(e, context=func.__name__, exit_on_error=exit_on_error)
        return None
