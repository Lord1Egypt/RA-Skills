#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
错误处理模块 - invoice_downloader_v73
提供完善的异常捕获、错误分类和重试机制
"""

import time
import functools
import traceback
from enum import Enum
from typing import Callable, Any, Dict, Optional, Type
from dataclasses import dataclass, field
from datetime import datetime


class ErrorType(Enum):
    """错误类型分类"""
    # 网络相关
    NETWORK_ERROR = "network_error"           # 网络连接错误
    TIMEOUT_ERROR = "timeout_error"           # 请求超时
    HTTP_ERROR = "http_error"                 # HTTP错误码
    
    # 浏览器相关
    BROWSER_ERROR = "browser_error"           # 浏览器初始化/操作错误
    BROWSER_CRASH = "browser_crash"           # 浏览器崩溃
    DOWNLOAD_ERROR = "download_error"         # 下载失败
    
    # 文件相关
    FILE_ERROR = "file_error"                 # 文件读写错误
    FILE_EXISTS = "file_exists"               # 文件已存在
    PERMISSION_ERROR = "permission_error"     # 权限错误
    
    # 邮件相关
    EMAIL_AUTH_ERROR = "email_auth_error"     # 邮件认证失败
    EMAIL_FETCH_ERROR = "email_fetch_error"   # 邮件获取失败
    EMAIL_PARSE_ERROR = "email_parse_error"    # 邮件解析错误
    
    # 未知
    UNKNOWN_ERROR = "unknown_error"           # 未知错误


class ErrorSeverity(Enum):
    """错误严重程度"""
    LOW = "low"        # 低 - 可忽略，继续执行
    MEDIUM = "medium"  # 中 - 记录但继续
    HIGH = "high"      # 高 - 需要关注
    CRITICAL = "critical"  # 严重 - 可能是配置问题


@dataclass
class ErrorContext:
    """错误上下文"""
    error_type: ErrorType
    severity: ErrorSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    traceback: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict:
        return {
            "error_type": self.error_type.value,
            "severity": self.severity.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp.isoformat(),
            "traceback": self.traceback
        }


class ErrorClassifier:
    """错误分类器 - 根据异常自动识别错误类型"""
    
    # 错误关键词映射
    ERROR_MAPPINGS = {
        # 网络错误
        (ErrorType.NETWORK_ERROR, ErrorSeverity.HIGH): [
            "connection refused", "connection reset", "connection timeout",
            "network is unreachable", "no route to host", "ssl error",
            "certificate verify failed", "handshake timeout"
        ],
        (ErrorType.TIMEOUT_ERROR, ErrorSeverity.MEDIUM): [
            "timeout", "timed out", "request timeout", "read timeout",
            "connect timeout", "pool timeout"
        ],
        (ErrorType.HTTP_ERROR, ErrorSeverity.MEDIUM): [
            "status code", "http error", "400", "401", "403", "404", 
            "500", "502", "503", "504"
        ],
        
        # 浏览器错误
        (ErrorType.BROWSER_ERROR, ErrorSeverity.HIGH): [
            "playwright", "browser", "chromium", "page error",
            "element not found", "locator", "navigation"
        ],
        (ErrorType.BROWSER_CRASH, ErrorSeverity.HIGH): [
            "crash", "aborted", "terminated"
        ],
        (ErrorType.DOWNLOAD_ERROR, ErrorSeverity.MEDIUM): [
            "download", "save_as", "download failed"
        ],
        
        # 文件错误
        (ErrorType.FILE_ERROR, ErrorSeverity.MEDIUM): [
            "no such file", "cannot open", "permission denied",
            "io error", "disk full", "read only"
        ],
        (ErrorType.PERMISSION_ERROR, ErrorSeverity.HIGH): [
            "permission denied", "access denied", "not permitted"
        ],
        
        # 邮件错误
        (ErrorType.EMAIL_AUTH_ERROR, ErrorSeverity.CRITICAL): [
            "authentication failed", "login failed", "invalid credentials",
            "imap auth", "smtp auth"
        ],
        (ErrorType.EMAIL_FETCH_ERROR, ErrorSeverity.MEDIUM): [
            "fetch failed", "cannot fetch", "mailbox error",
            "imap error", "select failed"
        ],
        (ErrorType.EMAIL_PARSE_ERROR, ErrorSeverity.LOW): [
            "parse error", "decode error", "invalid encoding",
            "malformed", "charset"
        ],
    }
    
    # 异常类型映射
    EXCEPTION_MAPPINGS = {
        ConnectionError: (ErrorType.NETWORK_ERROR, ErrorSeverity.HIGH),
        TimeoutError: (ErrorType.TIMEOUT_ERROR, ErrorSeverity.MEDIUM),
        requests.exceptions.RequestException: (ErrorType.NETWORK_ERROR, ErrorSeverity.MEDIUM),
        requests.exceptions.Timeout: (ErrorType.TIMEOUT_ERROR, ErrorSeverity.MEDIUM),
        requests.exceptions.HTTPError: (ErrorType.HTTP_ERROR, ErrorSeverity.MEDIUM),
        FileNotFoundError: (ErrorType.FILE_ERROR, ErrorSeverity.MEDIUM),
        PermissionError: (ErrorType.PERMISSION_ERROR, ErrorSeverity.CRITICAL),
        IOError: (ErrorType.FILE_ERROR, ErrorSeverity.MEDIUM),
        OSError: (ErrorType.FILE_ERROR, ErrorSeverity.MEDIUM),
    }
    
    @classmethod
    def classify(cls, exception: Exception) -> ErrorContext:
        """分类异常"""
        error_type = ErrorType.UNKNOWN_ERROR
        severity = ErrorSeverity.MEDIUM
        
        # 1. 检查异常类型
        exc_type = type(exception)
        for exc_cls, (e_type, sev) in cls.EXCEPTION_MAPPINGS.items():
            if isinstance(exception, exc_cls):
                error_type = e_type
                severity = sev
                break
        
        # 2. 检查错误消息
        error_msg = str(exception).lower()
        for (e_type, sev), keywords in cls.ERROR_MAPPINGS.items():
            if any(kw in error_msg for kw in keywords):
                # 如果找到更高严重性的分类，升级
                severity_order = [ErrorSeverity.LOW, ErrorSeverity.MEDIUM, ErrorSeverity.HIGH, ErrorSeverity.CRITICAL]
                if severity_order.index(sev) > severity_order.index(severity):
                    severity = sev
                if e_type != ErrorType.UNKNOWN_ERROR:
                    error_type = e_type
                break
        
        # 获取完整traceback
        tb_str = traceback.format_exc()
        
        return ErrorContext(
            error_type=error_type,
            severity=severity,
            message=str(exception)[:500],
            traceback=tb_str
        )


class ErrorHandler:
    """错误处理器"""
    
    def __init__(self, logger=None):
        self.logger = logger
        self.error_count = {et.value: 0 for et in ErrorType}
        self.errors = []
    
    def handle(self, exception: Exception, context: Dict = None) -> ErrorContext:
        """处理错误"""
        error_ctx = ErrorClassifier.classify(exception)
        
        if context:
            error_ctx.details = context
        
        # 记录错误
        self.error_count[error_ctx.error_type.value] += 1
        self.errors.append(error_ctx)
        
        # 打印日志
        if self.logger:
            self.logger.error(
                f"❌ [{error_ctx.error_type.value}] {error_ctx.message[:100]} | "
                f"严重程度: {error_ctx.severity.value}"
            )
        
        return error_ctx
    
    def get_stats(self) -> Dict:
        """获取错误统计"""
        return {
            "total_errors": len(self.errors),
            "by_type": self.error_count,
            "recent_errors": [e.to_dict() for e in self.errors[-10:]]
        }
    
    def should_continue(self, error_ctx: ErrorContext) -> bool:
        """判断是否继续执行"""
        # 严重错误终止
        if error_ctx.severity == ErrorSeverity.CRITICAL:
            return False
        # 认证错误终止
        if error_ctx.error_type == ErrorType.EMAIL_AUTH_ERROR:
            return False
        return True


def safe_execute(func: Callable = None, *, 
                 default_return=None,
                 error_handler: ErrorHandler = None,
                 context: Dict = None,
                 suppress_errors: bool = True):
    """
    安全执行装饰器 - 捕获异常并继续执行
    
    用法:
    @safe_execute(default_return=[], error_handler=handler)
    def process_email(msg):
        ...
    """
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                return f(*args, **kwargs)
            except Exception as e:
                duration = time.time() - start_time
                
                # 分类错误
                ctx = context or {}
                ctx["function"] = f.__name__
                ctx["duration"] = round(duration, 2)
                
                if error_handler:
                    error_ctx = error_handler.handle(e, ctx)
                    
                    # 打印详细错误
                    if error_handler.logger:
                        error_handler.logger.error(
                            f"   ⏱️ 耗时: {duration:.2f}s | "
                            f"错误: {str(e)[:80]}"
                        )
                    
                    # 检查是否继续
                    if not error_handler.should_continue(error_ctx):
                        raise
                
                if suppress_errors:
                    return default_return
                else:
                    raise
        
        return wrapper
    
    if func is None:
        return decorator
    else:
        return decorator(func)


def retry_on_error(max_retries: int = 3, 
                   delay: float = 1.0,
                   backoff: float = 2.0,
                   exceptions: tuple = (Exception,),
                   error_handler: ErrorHandler = None):
    """
    重试装饰器 - 失败时自动重试
    
    用法:
    @retry_on_error(max_retries=3, delay=2.0)
    def download_invoice(url):
        ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        wait_time = delay * (backoff ** attempt)
                        if error_handler and error_handler.logger:
                            error_handler.logger.warning(
                                f"   🔄 重试 {attempt + 1}/{max_retries} | "
                                f"等待 {wait_time:.1f}s | 错误: {str(e)[:60]}"
                            )
                        time.sleep(wait_time)
                    else:
                        if error_handler:
                            error_handler.handle(e, {
                                "function": func.__name__,
                                "attempt": attempt + 1,
                                "max_retries": max_retries
                            })
            
            raise last_exception
        
        return wrapper
    
    return decorator


class EmailProcessError(Exception):
    """邮件处理错误 - 不中断主流程"""
    def __init__(self, message: str, email_idx: int = None, 
                 email_subject: str = None, error_type: ErrorType = ErrorType.UNKNOWN_ERROR):
        self.email_idx = email_idx
        self.email_subject = email_subject
        self.error_type = error_type
        super().__init__(message)


def create_error_context(error_type: ErrorType, message: str, 
                         details: Dict = None) -> Dict:
    """创建错误上下文字典"""
    ctx = {
        "error_type": error_type.value,
        "message": message,
        "timestamp": datetime.now().isoformat()
    }
    if details:
        ctx.update(details)
    return ctx
