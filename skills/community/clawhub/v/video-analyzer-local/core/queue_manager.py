"""批量队列管理模块 — SQLite 任务表 + 硬件档位并发控制"""

import os
import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Dict, List, Optional

from .logger import get_logger

logger = get_logger(__name__)


class QueueManager:
    """
    批量队列管理器。
    
    功能：
    1. SQLite 任务表（pending/running/done/failed/产物路径）
    2. 线程池并发数由 hardware.py 档位决定（low=1/mid=2/high=4）
    3. 支持中断后续跑（按状态恢复）
    4. 新增 CLI 批量入口 --dir 指向目录扫描视频文件逐个入队
    """
    
    # 支持的视频扩展名
    VIDEO_EXTENSIONS = {
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpg", ".mpeg", ".ts",
    }
    
    # 硬件档位对应的并发数
    HARDWARE_CONCURRENCY = {
        "low": 1,
        "mid": 2,
        "high": 4,
    }
    
    def __init__(self, config: Dict[str, Any], db_path: str = None):
        self.config = config
        self.cache_dir = config.get("processing", {}).get("cache_dir", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # SQLite 数据库路径
        if db_path is None:
            self.db_path = os.path.join(self.cache_dir, "queue.db")
        else:
            self.db_path = db_path
        
        # 硬件档位
        self._hardware_tier = None
        self._max_workers = None
        
        # 初始化数据库
        self._init_db()
    
    def _init_db(self):
        """初始化 SQLite 数据库"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    input_path TEXT NOT NULL,
                    output_dir TEXT,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 0,
                    created_at REAL,
                    started_at REAL,
                    completed_at REAL,
                    error_message TEXT,
                    artifact_paths TEXT,
                    progress REAL DEFAULT 0.0
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)
            """)
            conn.commit()
    
    def scan_directory(self, directory: str, recursive: bool = True) -> List[str]:
        """
        扫描目录中的视频文件。
        
        Args:
            directory: 目录路径
            recursive: 是否递归扫描子目录
            
        Returns:
            视频文件路径列表
        """
        video_files = []
        
        if not os.path.isdir(directory):
            raise ValueError(f"不是有效目录: {directory}")
        
        if recursive:
            for root, dirs, files in os.walk(directory):
                for f in sorted(files):
                    ext = os.path.splitext(f)[1].lower()
                    if ext in self.VIDEO_EXTENSIONS:
                        video_files.append(os.path.join(root, f))
        else:
            for f in sorted(os.listdir(directory)):
                ext = os.path.splitext(f)[1].lower()
                if ext in self.VIDEO_EXTENSIONS:
                    video_files.append(os.path.join(directory, f))
        
        logger.info(f"扫描目录 {directory}: 发现 {len(video_files)} 个视频文件")
        return video_files
    
    def enqueue(self, input_path: str, output_dir: str = None, priority: int = 0) -> int:
        """
        添加任务到队列。
        
        Args:
            input_path: 输入文件路径
            output_dir: 输出目录
            priority: 优先级（越大越优先）
            
        Returns:
            任务 ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO tasks (input_path, output_dir, status, priority, created_at) "
                "VALUES (?, ?, 'pending', ?, ?)",
                (input_path, output_dir, priority, time.time())
            )
            task_id = cursor.lastrowid
            conn.commit()
        
        logger.debug(f"任务已入队: {input_path} (ID: {task_id})")
        return task_id
    
    def enqueue_batch(self, input_paths: List[str], output_dir: str = None) -> List[int]:
        """
        批量添加任务到队列。
        
        Args:
            input_paths: 输入文件路径列表
            output_dir: 输出目录
            
        Returns:
            任务 ID 列表
        """
        task_ids = []
        for path in input_paths:
            task_id = self.enqueue(path, output_dir)
            task_ids.append(task_id)
        
        logger.info(f"批量入队: {len(task_ids)} 个任务")
        return task_ids
    
    def get_next_pending(self) -> Optional[Dict[str, Any]]:
        """
        获取下一个待处理任务。
        
        Returns:
            任务字典，无则返回 None
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE status = 'pending' "
                "ORDER BY priority DESC, created_at ASC LIMIT 1"
            )
            row = cursor.fetchone()
            
            if row:
                return dict(row)
        
        return None
    
    def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        获取指定状态的任务。
        
        Args:
            status: 任务状态
            
        Returns:
            任务字典列表
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE status = ? ORDER BY created_at ASC",
                (status,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def update_task_status(self, task_id: int, status: str, 
                          error_message: str = None,
                          artifact_paths: str = None,
                          progress: float = None):
        """
        更新任务状态。
        
        Args:
            task_id: 任务 ID
            status: 新状态
            error_message: 错误信息
            artifact_paths: 产物路径
            progress: 进度
        """
        with sqlite3.connect(self.db_path) as conn:
            updates = ["status = ?"]
            params = [status]
            
            if error_message is not None:
                updates.append("error_message = ?")
                params.append(error_message)
            
            if artifact_paths is not None:
                updates.append("artifact_paths = ?")
                params.append(artifact_paths)
            
            if progress is not None:
                updates.append("progress = ?")
                params.append(progress)
            
            if status == "running":
                updates.append("started_at = ?")
                params.append(time.time())
            
            if status in ("done", "failed"):
                updates.append("completed_at = ?")
                params.append(time.time())
            
            params.append(task_id)
            
            conn.execute(
                f"UPDATE tasks SET {', '.join(updates)} WHERE id = ?",
                params
            )
            conn.commit()
    
    def get_stats(self) -> Dict[str, int]:
        """
        获取队列统计。
        
        Returns:
            各状态任务数量
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT status, COUNT(*) FROM tasks GROUP BY status"
            )
            stats = dict(cursor.fetchall())
        
        return {
            "pending": stats.get("pending", 0),
            "running": stats.get("running", 0),
            "done": stats.get("done", 0),
            "failed": stats.get("failed", 0),
            "total": sum(stats.values()),
        }
    
    def reset_running_tasks(self):
        """重置所有 running 状态的任务为 pending（中断后恢复）"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE tasks SET status = 'pending' WHERE status = 'running'"
            )
            conn.commit()
        
        logger.info("已重置所有 running 任务为 pending")
    
    def cleanup_completed(self, keep_failed: bool = True):
        """
        清理已完成的任务。
        
        Args:
            keep_failed: 是否保留失败任务
        """
        with sqlite3.connect(self.db_path) as conn:
            if keep_failed:
                conn.execute("DELETE FROM tasks WHERE status = 'done'")
            else:
                conn.execute("DELETE FROM tasks WHERE status IN ('done', 'failed')")
            conn.commit()
    
    def set_hardware_tier(self, tier: str):
        """
        设置硬件档位。
        
        Args:
            tier: low/mid/high
        """
        self._hardware_tier = tier
        self._max_workers = self.HARDWARE_CONCURRENCY.get(tier, 2)
        logger.info(f"硬件档位: {tier}, 并发数: {self._max_workers}")
    
    def get_max_workers(self) -> int:
        """
        获取最大并发数。
        
        Returns:
            最大并发数
        """
        if self._max_workers is None:
            # 默认 mid
            self.set_hardware_tier("mid")
        
        return self._max_workers
    
    def run_batch(self, process_func: Callable[[Dict[str, Any]], Dict[str, Any]],
                 tier: str = "mid") -> Dict[str, Any]:
        """
        运行批量处理。
        
        Args:
            process_func: 处理函数，接收任务字典，返回结果字典
            tier: 硬件档位 (low/mid/high)
            
        Returns:
            批量处理结果统计
        """
        self.set_hardware_tier(tier)
        max_workers = self.get_max_workers()
        
        # 重置 running 任务
        self.reset_running_tasks()
        
        stats = {
            "total": 0,
            "success": 0,
            "failed": 0,
            "results": [],
        }
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            
            while True:
                # 获取下一个待处理任务
                task = self.get_next_pending()
                if task is None:
                    break
                
                # 提交任务
                self.update_task_status(task["id"], "running")
                future = executor.submit(process_func, task)
                futures[future] = task
                stats["total"] += 1
            
            # 等待所有任务完成
            for future in as_completed(futures):
                task = futures[future]
                try:
                    result = future.result()
                    self.update_task_status(
                        task["id"], "done",
                        artifact_paths=result.get("artifact_paths"),
                        progress=100.0
                    )
                    stats["success"] += 1
                    stats["results"].append(result)
                except Exception as e:
                    self.update_task_status(
                        task["id"], "failed",
                        error_message=str(e)
                    )
                    stats["failed"] += 1
                    logger.error(f"任务失败 {task['input_path']}: {e}")
        
        logger.info(f"批量处理完成: {stats['success']}/{stats['total']} 成功, {stats['failed']} 失败")
        return stats
