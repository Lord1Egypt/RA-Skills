"""
日志模块 - 自动日志记录、轮转和清理
使用 Python logging 模块 + TimedRotatingFileHandler
"""
import logging
import os
import sys
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class TeeOutput:
    """同时输出到控制台和日志的包装器"""
    def __init__(self, console_stream, logger_func):
        self.console = console_stream
        self.logger_func = logger_func
    
    def write(self, data):
        if data and data.strip():  # 忽略空行
            self.logger_func(data.rstrip())
        self.console.write(data)
    
    def flush(self):
        self.console.flush()


def setup_logging(command_name: str, log_dir: Path = None, auto_redirect_print: bool = True):
    """
    设置日志系统
    
    Args:
        command_name: 命令名称 (check/digest/analyze等)
        log_dir: 日志目录，默认使用 ~/.openclaw/workspace/smart-email-data/logs
        auto_redirect_print: 是否自动将 print 输出重定向到日志
    
    Returns:
        logger: 配置好的 logger 实例
    """
    if log_dir is None:
        log_dir = Path.home() / '.openclaw' / 'workspace' / 'smart-email-data' / 'logs'
    
    log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 日志文件路径
    log_file = log_dir / f"{command_name}.log"
    
    # 创建 logger
    logger = logging.getLogger(f'smart_email.{command_name}')
    logger.setLevel(logging.INFO)
    
    # 清除已有的 handlers（避免重复）
    logger.handlers = []
    
    # 文件 handler - 按天轮转，保留30天
    file_handler = TimedRotatingFileHandler(
        log_file,
        when='midnight',      # 每天午夜轮转
        interval=1,
        backupCount=30,       # 保留30个备份
        encoding='utf-8',
        utc=False
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(file_handler)
    
    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    logger.addHandler(console_handler)
    
    # 可选：将 print 重定向到日志
    if auto_redirect_print:
        _patch_print_to_logger(logger)
    
    # 清理旧日志
    clean_old_logs(log_dir, days=30)
    
    logger.info("=" * 50)
    logger.info(f"日志系统初始化完成: {command_name}")
    logger.info(f"日志文件: {log_file}")
    logger.info("=" * 50)
    
    return logger


def _patch_print_to_logger(logger):
    """将内置 print 函数重定向到 logger"""
    import builtins
    
    # 保存原始 print
    if not hasattr(builtins, '_original_print'):
        builtins._original_print = builtins.print
    
    def logged_print(*args, sep=' ', end='\n', **kwargs):
        # 构建消息（不保留 end 后的换行，避免日志中多余空行）
        message = sep.join(str(arg) for arg in args)
        if message.strip():
            logger.info(message)
        # 不再调用 original_print，因为 logger 的 console_handler 已经处理控制台输出
        # 避免双重输出
    
    builtins.print = logged_print


def restore_print():
    """恢复原始 print 函数"""
    import builtins
    if hasattr(builtins, '_original_print'):
        builtins.print = builtins._original_print
        delattr(builtins, '_original_print')


def clean_old_logs(log_dir: Path, days: int = 30):
    """
    清理超过指定天数的日志文件
    
    Args:
        log_dir: 日志目录
        days: 保留天数，默认30天
    """
    if not log_dir.exists():
        return
    
    cutoff = datetime.now() - timedelta(days=days)
    deleted_count = 0
    
    for file_path in log_dir.iterdir():
        if not file_path.is_file():
            continue
        
        # 只处理 .log 文件和轮转备份文件
        if not file_path.suffix in ['.log', '.log.1', '.log.2'] and not '.log.' in file_path.name:
            continue
        
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff:
                file_path.unlink()
                deleted_count += 1
        except Exception:
            pass  # 忽略删除失败
    
    if deleted_count > 0:
        # 使用原始 print 避免递归
        import builtins
        if hasattr(builtins, '_original_print'):
            builtins._original_print(f"  已清理 {deleted_count} 个旧日志文件")


def get_logger(name: str) -> logging.Logger:
    """获取已配置的 logger"""
    return logging.getLogger(f'smart_email.{name}')
