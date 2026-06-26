#!/usr/bin/env python3
"""
日志工具模块
"""

import os
import sys
import logging
from datetime import datetime
from typing import Optional

def setup_logger(name: str, level: Optional[str] = None) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
    
    Returns:
        配置好的日志记录器
    """
    # 获取日志级别
    if level is None:
        level = 'INFO'  # 默认日志级别
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    
    # 避免重复添加处理器
    if logger.handlers:
        return logger
    
    # 设置日志级别
    numeric_level = getattr(logging, level, logging.INFO)
    logger.setLevel(numeric_level)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    
    # 创建格式化器
    formatter = ColoredFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 添加文件处理器（使用默认日志文件）
    try:
        # 创建日志目录
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(log_dir, f"task_push_{timestamp}.log")
        
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        logger.info(f"日志文件: {log_file}")
    except Exception as e:
        logger.warning(f"无法创建日志文件处理器: {str(e)}")
    
    return logger

class ColoredFormatter(logging.Formatter):
    """带颜色的日志格式化器（Windows兼容版本）"""
    
    # 颜色代码（Windows CMD可能不支持，所以提供无颜色版本）
    COLORS = {
        'DEBUG': '',    # 无颜色
        'INFO': '',     # 无颜色
        'WARNING': '',  # 无颜色
        'ERROR': '',    # 无颜色
        'CRITICAL': '', # 无颜色
        'RESET': ''     # 无颜色
    }
    
    def format(self, record):
        """格式化日志记录"""
        # 保存原始级别名称
        original_levelname = record.levelname
        
        # 添加颜色（在Windows上通常不添加颜色以避免编码问题）
        if record.levelname in self.COLORS:
            color = self.COLORS[record.levelname]
            reset = self.COLORS['RESET']
            record.levelname = f"{color}{record.levelname}{reset}"
        
        # 调用父类格式化
        result = super().format(record)
        
        # 恢复原始级别名称
        record.levelname = original_levelname
        
        return result

def get_log_file_path(base_name: str = 'task_push') -> str:
    """
    获取日志文件路径
    
    Args:
        base_name: 日志文件基础名称
    
    Returns:
        日志文件完整路径
    """
    # 创建日志目录
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 生成日志文件名
    timestamp = datetime.now().strftime('%Y%m%d')
    log_file = os.path.join(log_dir, f"{base_name}_{timestamp}.log")
    
    return log_file

def log_task_start(task_name: str, task_id: str = None):
    """
    记录任务开始日志
    
    Args:
        task_name: 任务名称
        task_id: 任务ID
    """
    logger = logging.getLogger(__name__)
    
    log_msg = f"开始任务: {task_name}"
    if task_id:
        log_msg += f" (ID: {task_id})"
    
    logger.info("=" * 60)
    logger.info(log_msg)
    logger.info(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

def log_task_end(task_name: str, success: bool, duration: float = None):
    """
    记录任务结束日志
    
    Args:
        task_name: 任务名称
        success: 是否成功
        duration: 执行时长（秒）
    """
    logger = logging.getLogger(__name__)
    
    status = "[SUCCESS] 成功" if success else "[ERROR] 失败"
    log_msg = f"任务结束: {task_name} - {status}"
    
    if duration is not None:
        log_msg += f" (用时: {duration:.2f}秒)"
    
    logger.info("=" * 60)
    logger.info(log_msg)
    logger.info(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

def log_push_summary(push_data: dict, success: bool, response: dict = None):
    """
    记录推送摘要
    
    Args:
        push_data: 推送数据
        success: 是否成功
        response: 响应数据
    """
    logger = logging.getLogger(__name__)
    
    # 提取关键信息
    auth_code = push_data.get('authCode', '')
    msg_content = push_data.get('msgContent', [])
    
    if msg_content:
        first_msg = msg_content[0]
        msg_id = first_msg.get('msgId', '')
        summary = first_msg.get('summary', '')
        result = first_msg.get('result', '')
        content_length = len(first_msg.get('content', ''))
    else:
        msg_id = summary = result = ''
        content_length = 0
    
    # 记录摘要
    logger.info("📊 推送摘要:")
    logger.info(f"  任务ID: {msg_id}")
    logger.info(f"  任务摘要: {summary}")
    logger.info(f"  执行结果: {result}")
    logger.info(f"  内容长度: {content_length}字符")
    logger.info(f"  授权码: {auth_code[:4]}***" if auth_code else "  授权码: 未设置")
    logger.info(f"  推送状态: {'[SUCCESS] 成功' if success else '[ERROR] 失败'}")
    
    if response and not success:
        logger.info(f"  错误信息: {response}")

# 测试代码
if __name__ == "__main__":
    # 测试日志系统
    print("测试日志系统...")
    
    # 设置日志
    logger = setup_logger('test_logger', 'DEBUG')
    
    # 测试不同级别的日志
    logger.debug("这是一条调试信息")
    logger.info("这是一条信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条严重错误")
    
    # 测试任务日志
    log_task_start("测试任务", "test_123")
    log_task_end("测试任务", True, 2.5)
    
    # 测试推送摘要
    test_push_data = {
        "authCode": "test_auth",
        "msgContent": [
            {
                "msgId": "test_123",
                "scheduleTaskId": "test_123",
                "summary": "测试任务",
                "result": "完成",
                "content": "测试内容"
            }
        ]
    }
    
    log_push_summary(test_push_data, True)
    
    print("\n测试完成!")