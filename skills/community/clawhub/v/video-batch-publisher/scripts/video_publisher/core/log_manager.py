import logging
import os
from datetime import datetime

class PublisherLogger:
    """发布器日志管理器
    
    目录结构：logs/YYYY-MM/DD/
    日志文件名：YYYY-MM-DD_HH-MM_平台名称_内容类型.log
    
    日志内容要求：
    - 视频名称、平台、内容类型、标题、描述
    - 提交方式、定时时间、发布状态
    - 错误信息（失败时必填）、封面上传状态
    """
    
    def __init__(self, platform="", content_type=""):
        self.platform = platform
        self.content_type = content_type
        self.logger = None
        self.log_file_path = ""
        self.setup_logger()
    
    def setup_logger(self):
        """设置日志记录器"""
        now = datetime.now()
        year_month = now.strftime("%Y-%m")
        day = now.strftime("%d")
        timestamp = now.strftime("%Y-%m-%d_%H-%M")
        
        # 构建日志目录路径：logs/YYYY-MM/DD/
        log_dir = os.path.join("logs", year_month, day)
        os.makedirs(log_dir, exist_ok=True)
        
        # 构建日志文件名：YYYY-MM-DD_HH-MM_平台_内容类型.log
        platform_part = self.platform if self.platform else "unknown"
        type_part = self.content_type if self.content_type else "unknown"
        log_filename = f"{timestamp}_{platform_part}_{type_part}.log"
        
        self.log_file_path = os.path.join(log_dir, log_filename)
        
        # 创建日志记录器
        self.logger = logging.getLogger(f"publisher_{platform_part}_{type_part}")
        self.logger.setLevel(logging.INFO)
        
        # 清除已存在的处理器
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件处理器
        file_handler = logging.FileHandler(self.log_file_path, encoding='utf-8')
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
    
    def log_publish_start(self, video_name, title="", description=""):
        """记录发布开始"""
        self.logger.info(f"=== 开始发布 ===")
        self.logger.info(f"视频名称: {video_name}")
        self.logger.info(f"平台: {self.platform}")
        self.logger.info(f"内容类型: {self.content_type}")
        self.logger.info(f"标题: {title}")
        self.logger.info(f"描述: {description[:100]}...")
    
    def log_publish_success(self, video_name, submit_mode="正式发布", 
                            schedule_time="", cover_status="成功"):
        """记录发布成功"""
        self.logger.info(f"【成功】视频: {video_name}")
        self.logger.info(f"平台: {self.platform}")
        self.logger.info(f"内容类型: {self.content_type}")
        self.logger.info(f"提交方式: {submit_mode}")
        self.logger.info(f"定时时间: {schedule_time or '立即发布'}")
        self.logger.info(f"发布状态: 成功")
        self.logger.info(f"封面上传状态: {cover_status}")
        self.logger.info(f"=== 发布完成 ===")
    
    def log_publish_failure(self, video_name, error_message, 
                            submit_mode="正式发布", schedule_time="", 
                            cover_status=""):
        """记录发布失败"""
        self.logger.error(f"【失败】视频: {video_name}")
        self.logger.error(f"平台: {self.platform}")
        self.logger.error(f"内容类型: {self.content_type}")
        self.logger.error(f"提交方式: {submit_mode}")
        self.logger.error(f"定时时间: {schedule_time or '立即发布'}")
        self.logger.error(f"发布状态: 失败")
        self.logger.error(f"错误信息: {error_message}")
        self.logger.error(f"封面上传状态: {cover_status}")
        self.logger.error(f"=== 发布失败 ===")
    
    def log_cover_upload(self, video_name, cover_path, success=True):
        """记录封面上传状态"""
        status = "成功" if success else "失败"
        self.logger.info(f"封面上传{status}: {video_name}")
        self.logger.info(f"封面路径: {cover_path}")
    
    def log_info(self, message):
        """记录普通信息"""
        self.logger.info(message)
    
    def log_error(self, message):
        """记录错误信息"""
        self.logger.error(message)
    
    def log_warning(self, message):
        """记录警告信息"""
        self.logger.warning(message)
    
    def get_log_file_path(self):
        """获取日志文件路径"""
        return os.path.abspath(self.log_file_path)
    
    def log_batch_summary(self, total_count, success_count, fail_count, failed_videos=None):
        """记录批量发布统计
        
        参数:
            total_count: 总条数
            success_count: 成功条数
            fail_count: 失败条数
            failed_videos: 失败视频名称列表
        """
        self.logger.info("=" * 50)
        self.logger.info("=== 批量发布统计 ===")
        self.logger.info(f"总条数: {total_count}")
        self.logger.info(f"成功条数: {success_count}")
        self.logger.info(f"失败条数: {fail_count}")
        if failed_videos and len(failed_videos) > 0:
            self.logger.info(f"失败视频名称: {', '.join(failed_videos)}")
        self.logger.info("=" * 50)

def setup_logger(name, log_prefix="video_publish", level=logging.DEBUG):
    """兼容旧接口的日志设置函数
    
    参数:
        name: 日志记录器名称
        log_prefix: 日志文件名前缀
        level: 日志级别
    
    返回:
        logger 对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    now = datetime.now()
    year_month = now.strftime("%Y-%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    
    log_dir = os.path.join("logs", year_month, day)
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f"{hour}.log")
    
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)
    
    return logger

def get_log_file_path(log_prefix="video_publish"):
    """获取当前日志文件的完整路径"""
    now = datetime.now()
    year_month = now.strftime("%Y-%m")
    day = now.strftime("%d")
    hour = now.strftime("%H")
    
    log_dir = os.path.join("logs", year_month, day)
    log_file = os.path.join(log_dir, f"{hour}.log")
    
    return os.path.abspath(log_file)