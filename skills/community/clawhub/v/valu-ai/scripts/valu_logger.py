"""
ValU AI 日志模块
统一的日志管理，支持文件和控制台输出
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from logging.handlers import RotatingFileHandler
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器"""

    # ANSI 颜色码
    COLORS = {
        'DEBUG': '\033[36m',     # 青色
        'INFO': '\033[32m',      # 绿色
        'WARNING': '\033[33m',   # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m',  # 紫色
        'RESET': '\033[0m'       # 重置
    }

    def format(self, record):
        # 保存原始时间戳
        from datetime import datetime
        original_time = getattr(record, 'asctime', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        # 添加颜色
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"

        # 添加时间戳颜色
        record.asctime = f"\033[90m{original_time}\033[0m"

        return super().format(record)


class Logger:
    """日志管理器"""

    _instance: Optional['Logger'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._logger: Optional[logging.Logger] = None
        self._initialized = True

    def setup(
        self,
        name: str = "ValU_AI",
        level: str = "INFO",
        log_file: Optional[str] = None,
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5
    ):
        """设置日志系统"""

        # 创建 logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.handlers.clear()  # 清除现有处理器

        # 日志格式
        fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        datefmt = '%Y-%m-%d %H:%M:%S'

        # 控制台处理器（彩色）
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_formatter = ColoredFormatter(fmt, datefmt)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 文件处理器（轮转）
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(exist_ok=True)

            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(fmt, datefmt)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        self._logger = logger
        return logger

    @property
    def logger(self) -> logging.Logger:
        """获取日志器"""
        if self._logger is None:
            self.setup()
        return self._logger

    def debug(self, msg: str, *args, **kwargs):
        """调试日志"""
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args, **kwargs):
        """信息日志"""
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg: str, *args, **kwargs):
        """警告日志"""
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg: str, *args, **kwargs):
        """错误日志"""
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg: str, *args, **kwargs):
        """严重错误日志"""
        self.logger.critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args, **kwargs):
        """异常日志（包含堆栈）"""
        self.logger.exception(msg, *args, **kwargs)


# 全局日志实例
_log: Optional[Logger] = None


def get_log(name: str = "ValU_AI") -> Logger:
    """获取日志管理器"""
    global _log
    if _log is None:
        _log = Logger()
        _log.setup(name=name)
    return _log


def setup_log(
    name: str = "ValU_AI",
    level: str = "INFO",
    log_file: Optional[str] = None
) -> logging.Logger:
    """设置日志并返回 logger（兼容旧代码）"""
    log = get_log(name)
    log.setup(name=name, level=level, log_file=log_file)
    return log.logger


# 便捷函数
def log_info(msg: str, *args, **kwargs):
    """记录信息日志"""
    get_log().info(msg, *args, **kwargs)


def log_error(msg: str, *args, **kwargs):
    """记录错误日志"""
    get_log().error(msg, *args, **kwargs)


def log_warning(msg: str, *args, **kwargs):
    """记录警告日志"""
    get_log().warning(msg, *args, **kwargs)


def log_debug(msg: str, *args, **kwargs):
    """记录调试日志"""
    get_log().debug(msg, *args, **kwargs)


if __name__ == "__main__":
    # 测试日志
    print("=" * 50)
    print("日志系统测试")
    print("=" * 50)

    log = get_log("Test")
    log.setup(level="DEBUG", log_file="test.log")

    log.debug("这是一条 DEBUG 日志")
    log.info("这是一条 INFO 日志")
    log.warning("这是一条 WARNING 日志")
    log.error("这是一条 ERROR 日志")

    print("\n[OK] Log test complete, check test.log")
