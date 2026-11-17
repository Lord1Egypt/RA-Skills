"""统一日志模块"""

import logging
import sys
from typing import Optional

_loggers = {}


def get_logger(name: str = "video_analyzer", level: int = logging.INFO) -> logging.Logger:
    """
    获取具名日志器。
    
    Args:
        name: 日志器名称
        level: 日志级别
        
    Returns:
        logging.Logger 实例
    """
    if name in _loggers:
        return _loggers[name]
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加 handler
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(level)
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    _loggers[name] = logger
    return logger


def set_level(level: int):
    """设置全局日志级别"""
    for logger in _loggers.values():
        logger.setLevel(level)
        for handler in logger.handlers:
            handler.setLevel(level)
