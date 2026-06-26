#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日志记录模块 - invoice_downloader_v73
提供JSON格式的详细日志、处理结果记录和统计分析
"""

import os
import json
import time
import logging
import threading
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor


class ProcessStatus(Enum):
    """处理状态"""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    PARTIAL = "partial"  # 部分成功
    PROCESSING = "processing"
    RETRYING = "retrying"


class ProcessCategory(Enum):
    """处理分类"""
    ATTACHMENT = "A"      # 附件下载
    DIRECT_LINK = "B"     # 直接链接
    BROWSER = "C"         # 浏览器下载
    UNKNOWN = "U"


@dataclass
class EmailProcessResult:
    """单封邮件处理结果"""
    email_idx: int                    # 邮件索引
    email_subject: str                 # 邮件主题
    email_date: str                    # 邮件日期
    status: ProcessStatus              # 处理状态
    category: ProcessCategory          # 处理分类
    attachments_found: int = 0         # 发现的附件数
    attachments_success: int = 0       # 成功下载的附件数
    error_type: str = ""               # 错误类型
    error_message: str = ""            # 错误消息
    duration_seconds: float = 0.0      # 处理耗时
    saved_files: List[str] = field(default_factory=list)  # 保存的文件名
    retry_count: int = 0              # 重试次数
    strategy_used: str = ""            # 使用的策略
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "email_idx": self.email_idx,
            "email_subject": self.email_subject[:100] if self.email_subject else "",
            "email_date": self.email_date,
            "status": self.status.value,
            "category": self.category.value,
            "attachments_found": self.attachments_found,
            "attachments_success": self.attachments_success,
            "error_type": self.error_type,
            "error_message": self.error_message[:200] if self.error_message else "",
            "duration_seconds": round(self.duration_seconds, 2),
            "saved_files": self.saved_files,
            "retry_count": self.retry_count,
            "strategy_used": self.strategy_used,
            "timestamp": self.timestamp
        }


@dataclass
class DailyStats:
    """每日统计"""
    date: str
    total_emails: int = 0
    success_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    total_duration: float = 0.0
    errors_by_type: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    
    def to_dict(self) -> Dict:
        return {
            "date": self.date,
            "total_emails": self.total_emails,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
            "total_duration": round(self.total_duration, 2),
            "success_rate": round(self.success_count / self.total_emails * 100, 1) if self.total_emails > 0 else 0,
            "errors_by_type": dict(self.errors_by_type)
        }


class JSONLogger:
    """JSON格式日志记录器"""
    
    def __init__(self, log_dir: str, prefix: str = "invoice"):
        self.log_dir = log_dir
        self.prefix = prefix
        self._lock = threading.Lock()
        
        # 确保目录存在
        os.makedirs(log_dir, exist_ok=True)
        
        # 生成日志文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_file = os.path.join(log_dir, f"{prefix}_{timestamp}.json")
        
        # 初始化文件
        self._init_log_file()
        
        # 内存中的结果缓存
        self.results: List[EmailProcessResult] = []
        
        # 统计信息
        self.stats = DailyStats(date=date.today().isoformat())
    
    def _init_log_file(self):
        """初始化日志文件"""
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write('{\n')
            f.write(f'  "log_file": "{os.path.basename(self.log_file)}",\n')
            f.write(f'  "created_at": "{datetime.now().isoformat()}",\n')
            f.write('  "results": [\n')
    
    def log_result(self, result: EmailProcessResult):
        """记录处理结果"""
        with self._lock:
            self.results.append(result)
            
            # 更新统计
            self.stats.total_emails += 1
            if result.status == ProcessStatus.SUCCESS:
                self.stats.success_count += 1
            elif result.status == ProcessStatus.FAILED:
                self.stats.failed_count += 1
                if result.error_type:
                    self.stats.errors_by_type[result.error_type] += 1
            elif result.status == ProcessStatus.SKIPPED:
                self.stats.skipped_count += 1
            
            self.stats.total_duration += result.duration_seconds
            
            # 追加到JSON文件
            self._append_result(result)
    
    def _append_result(self, result: EmailProcessResult):
        """追加结果到JSON文件"""
        try:
            # 读取现有内容
            with open(self.log_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 移除最后的闭合括号和换行
            if content.rstrip().endswith(']'):
                content = content.rstrip()
                content = content[:-1]  # 移除 ]
                if not content.endswith('\n'):
                    content += '\n'
                content += ',\n'
            elif content.rstrip().endswith('  "results": ['):
                content = content.rstrip()
                content += '\n'
            
            # 添加新结果
            result_json = json.dumps(result.to_dict(), ensure_ascii=False, indent=2)
            # 缩进每行
            result_json = '\n'.join('    ' + line for line in result_json.split('\n'))
            content += result_json
            
            # 添加闭合
            content += '\n  ]\n}'
            
            # 写回
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
        except Exception as e:
            print(f"⚠️ 日志写入失败: {e}")
    
    def log_error(self, email_idx: int, subject: str, error_type: str, 
                  error_message: str, duration: float):
        """记录错误结果"""
        result = EmailProcessResult(
            email_idx=email_idx,
            email_subject=subject,
            email_date="",
            status=ProcessStatus.FAILED,
            category=ProcessCategory.UNKNOWN,
            error_type=error_type,
            error_message=error_message,
            duration_seconds=duration
        )
        self.log_result(result)
    
    def get_summary(self) -> Dict:
        """获取处理摘要"""
        return {
            "total": self.stats.total_emails,
            "success": self.stats.success_count,
            "failed": self.stats.failed_count,
            "skipped": self.stats.skipped_count,
            "success_rate": round(self.stats.success_count / self.stats.total_emails * 100, 1) 
                           if self.stats.total_emails > 0 else 0,
            "total_duration": round(self.stats.total_duration, 2),
            "errors_by_type": dict(self.stats.errors_by_type)
        }
    
    def close(self):
        """关闭日志文件"""
        # 记录统计信息到另一个文件
        stats_file = os.path.join(self.log_dir, f"{self.prefix}_stats.json")
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_summary(), f, ensure_ascii=False, indent=2)


class InvoiceLogger:
    """发票下载器日志记录器 - 整合控制台和JSON日志"""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.log_dir = os.path.join(output_dir, "logs")
        
        # 创建日志目录
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 设置Python日志
        self._setup_console_logger()
        
        # JSON日志记录器
        self.json_logger = JSONLogger(self.log_dir, prefix="invoice")
        
        # 内存缓存（用于Excel输出）
        self.all_records: List[Dict] = []
        self._records_lock = threading.Lock()
    
    def _setup_console_logger(self):
        """设置控制台日志"""
        self.logger = logging.getLogger("invoice_downloader")
        self.logger.setLevel(logging.INFO)
        
        # 清除现有handlers
        self.logger.handlers.clear()
        
        # 控制台处理器
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        
        # 格式化
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        )
        console.setFormatter(formatter)
        self.logger.addHandler(console)
    
    def log_email_start(self, idx: int, total: int, subject: str):
        """记录邮件开始处理"""
        self.logger.info(f"\n📧 [{idx}/{total}] 开始处理: {subject[:50]}...")
    
    def log_email_result(self, result: EmailProcessResult):
        """记录邮件处理结果"""
        # 记录到JSON
        self.json_logger.log_result(result)
        
        # 记录到内存
        record = {
            "序号": result.email_idx + 1,
            "邮件主题": result.email_subject[:50],
            "邮件时间": result.email_date[:19] if result.email_date else "",
            "分类": result.category.value,
            "状态": result.status.value,
            "保存名称": ", ".join(result.saved_files) if result.saved_files else "",
            "备注": result.error_message[:100] if result.error_message else "",
            "原因": "",
            "耗时": f"{result.duration_seconds:.2f}s"
        }
        
        with self._records_lock:
            self.all_records.append(record)
        
        # 控制台输出
        if result.status == ProcessStatus.SUCCESS:
            self.logger.info(f"   ✅ 成功 | 附件: {result.attachments_success}/{result.attachments_found} | 耗时: {result.duration_seconds:.2f}s")
        elif result.status == ProcessStatus.FAILED:
            self.logger.error(f"   ❌ 失败 | {result.error_type}: {result.error_message[:60]}...")
        elif result.status == ProcessStatus.SKIPPED:
            self.logger.warning(f"   ⏭️ 跳过 | {result.error_message[:60] if result.error_message else '文件已存在'}")
    
    def log_error(self, idx: int, subject: str, error_type: str, 
                  error_message: str, duration: float):
        """记录错误"""
        self.logger.error(f"   ❌ [{idx}] {error_type}: {error_message[:80]}...")
        
        # 记录到JSON
        self.json_logger.log_error(idx, subject, error_type, error_message, duration)
        
        # 记录到内存
        record = {
            "序号": idx + 1,
            "邮件主题": subject[:50] if subject else "",
            "邮件时间": "",
            "分类": "U",
            "状态": "failed",
            "保存名称": "",
            "备注": error_message[:100],
            "原因": error_type,
            "耗时": f"{duration:.2f}s"
        }
        
        with self._records_lock:
            self.all_records.append(record)
    
    def log_summary(self, total: int, success: int, failed: int, 
                    skipped: int, duration: float):
        """记录处理摘要"""
        self.logger.info(f"\n{'='*60}")
        self.logger.info(f"✅ 处理完成!")
        self.logger.info(f"   总计: {total} | 成功: {success} | 失败: {failed} | 跳过: {skipped}")
        self.logger.info(f"   耗时: {duration:.1f}秒")
        self.logger.info(f"{'='*60}")
    
    def get_records(self) -> List[Dict]:
        """获取所有记录"""
        with self._records_lock:
            return self.all_records.copy()
    
    def close(self):
        """关闭日志"""
        self.json_logger.close()
        # 保存详细JSON
        detail_file = os.path.join(self.log_dir, "details.json")
        with open(detail_file, 'w', encoding='utf-8') as f:
            json.dump(self.get_records(), f, ensure_ascii=False, indent=2)


class ProcessTimer:
    """处理计时器 - 用于记录耗时"""
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
    
    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return 0.0


def log_execution(logger: InvoiceLogger):
    """邮件处理日志装饰器"""
    def decorator(func):
        def wrapper(email_idx, msg_data, *args, **kwargs):
            subject = msg_data.get("subject", f"邮件{email_idx}")
            start_time = time.time()
            
            logger.log_email_start(email_idx + 1, msg_data.get("total", "?"), subject)
            
            try:
                result = func(email_idx, msg_data, *args, **kwargs)
                duration = time.time() - start_time
                
                # 转换为EmailProcessResult
                if isinstance(result, list):
                    # 返回多条记录
                    for record in result:
                        process_result = EmailProcessResult(
                            email_idx=email_idx,
                            email_subject=subject,
                            email_date=record.get("邮件时间", ""),
                            status=ProcessStatus.SUCCESS if record.get("状态") == "成功" 
                                  else ProcessStatus.FAILED if record.get("状态") == "失败"
                                  else ProcessStatus.SKIPPED,
                            category=ProcessCategory(record.get("分类", "U")),
                            duration_seconds=duration,
                            saved_files=[record.get("保存名称", "")]
                        )
                        logger.log_email_result(process_result)
                
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                logger.log_error(
                    email_idx, subject,
                    type(e).__name__, str(e), duration
                )
                raise
        
        return wrapper
    return decorator


# 便捷函数
def create_logger(output_dir: str) -> InvoiceLogger:
    """创建日志记录器"""
    return InvoiceLogger(output_dir)
