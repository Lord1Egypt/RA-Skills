"""
日志系统
"""

import logging
import sys
from typing import Optional
from datetime import datetime
import os


def setup_logger(name: str = "ppt_maker", 
                log_level: str = "INFO",
                log_file: Optional[str] = None) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        log_level: 日志级别
        log_file: 日志文件路径
        
    Returns:
        配置好的日志记录器
    """
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 设置日志级别
    level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(level)
    
    # 清除现有处理器
    logger.handlers.clear()
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # 创建格式化器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # 添加控制台处理器
    logger.addHandler(console_handler)
    
    # 如果需要文件日志
    if log_file:
        try:
            # 确保日志目录存在
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            
            # 创建文件处理器
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.info(f"日志文件已启用: {log_file}")
            
        except Exception as e:
            logger.warning(f"无法创建日志文件: {e}")
    
    # 设置日志传播（避免重复记录）
    logger.propagate = False
    
    return logger


def get_logger(name: str = "ppt_maker") -> logging.Logger:
    """
    获取日志记录器（单例模式）
    
    Args:
        name: 日志记录器名称
        
    Returns:
        日志记录器实例
    """
    return logging.getLogger(name)


class LoggerMixin:
    """日志混合类，方便其他类使用"""
    
    @property
    def logger(self):
        """获取类特定的日志记录器"""
        if not hasattr(self, '_logger'):
            class_name = self.__class__.__name__
            self._logger = get_logger(f"ppt_maker.{class_name}")
        
        return self._logger


def log_execution_time(func):
    """
    记录函数执行时间的装饰器
    
    Args:
        func: 要装饰的函数
        
    Returns:
        装饰后的函数
    """
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = time.time()
        
        try:
            logger.debug(f"开始执行: {func.__name__}")
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"执行完成: {func.__name__}, 耗时: {execution_time:.2f}秒")
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"执行失败: {func.__name__}, 耗时: {execution_time:.2f}秒, 错误: {e}")
            raise
    
    return wrapper


class ProgressLogger:
    """进度日志记录器"""
    
    def __init__(self, total_steps: int, task_name: str = "任务"):
        """
        初始化进度日志记录器
        
        Args:
            total_steps: 总步骤数
            task_name: 任务名称
        """
        self.total_steps = total_steps
        self.task_name = task_name
        self.current_step = 0
        self.start_time = datetime.now()
        self.logger = get_logger("progress")
        
        self.logger.info(f"🚀 开始任务: {task_name} (共{total_steps}步)")
    
    def step(self, step_name: str, extra_info: str = ""):
        """
        记录步骤进度
        
        Args:
            step_name: 步骤名称
            extra_info: 额外信息
        """
        self.current_step += 1
        percentage = (self.current_step / self.total_steps) * 100
        
        message = f"📊 [{self.current_step}/{self.total_steps}] {step_name}"
        if extra_info:
            message += f" - {extra_info}"
        
        self.logger.info(message)
        
        # 每25%打印一次进度
        if percentage in [25, 50, 75, 100]:
            elapsed = (datetime.now() - self.start_time).total_seconds()
            self.logger.info(f"📈 进度: {percentage:.0f}%, 已耗时: {elapsed:.1f}秒")
    
    def complete(self, success: bool = True, message: str = ""):
        """
        完成任务
        
        Args:
            success: 是否成功
            message: 完成消息
        """
        elapsed = (datetime.now() - self.start_time).total_seconds()
        
        if success:
            status = "✅ 完成"
        else:
            status = "❌ 失败"
        
        log_message = f"{status} 任务: {self.task_name}, 总耗时: {elapsed:.1f}秒"
        if message:
            log_message += f", {message}"
        
        if success:
            self.logger.info(log_message)
        else:
            self.logger.error(log_message)
        
        return success


# 测试代码
if __name__ == "__main__":
    print("🔧 日志系统测试")
    print("=" * 50)
    
    # 设置日志
    logger = setup_logger(log_level="DEBUG", log_file="test.log")
    
    # 测试不同级别的日志
    logger.debug("这是调试信息")
    logger.info("这是信息信息")
    logger.warning("这是警告信息")
    logger.error("这是错误信息")
    
    # 测试进度记录器
    print("\n📊 测试进度记录器:")
    progress = ProgressLogger(5, "测试进度记录")
    
    for i in range(5):
        progress.step(f"步骤{i+1}", f"处理数据{i+1}")
    
    progress.complete(True, "所有步骤完成")
    
    print("\n✅ 日志系统测试完成")