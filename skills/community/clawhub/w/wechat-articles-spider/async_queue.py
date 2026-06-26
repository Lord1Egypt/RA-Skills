#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Async Task Queue
异步任务队列 - 处理大额支付的异步爬取任务
"""

import json
import os
import time
import threading
from queue import Queue, PriorityQueue
from datetime import datetime
from typing import Dict, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

from config import QUEUE_CONFIG


DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "queue")
os.makedirs(DATA_DIR, exist_ok=True)


class TaskStatus(Enum):
    """任务状态"""
    PENDING_PAYMENT = "pending_payment"    # 等待支付
    PAYMENT_CONFIRMED = "payment_confirmed"  # 支付已确认
    PROCESSING = "processing"              # 处理中
    COMPLETED = "completed"                # 完成
    FAILED = "failed"                      # 失败


@dataclass
class CrawlTask:
    """爬取任务"""
    task_id: str
    user_id: str
    account_name: str
    max_articles: int
    payment_mode: str          # 'realtime' | 'async'
    amount: float
    status: str
    created_at: str
    payment_proof: Optional[Dict] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "CrawlTask":
        return cls(**data)


class AsyncTaskQueue:
    """异步任务队列"""
    
    def __init__(self):
        self.queue_file = os.path.join(DATA_DIR, "tasks.json")
        self.tasks: Dict[str, CrawlTask] = {}
        self.pending_queue = Queue()  # 等待支付确认
        self.processing_queue = Queue()  # 等待执行
        self._load_tasks()
        self._running = False
        self._worker_thread = None
    
    def _load_tasks(self) -> None:
        """加载任务"""
        if os.path.exists(self.queue_file):
            with open(self.queue_file, 'r') as f:
                data = json.load(f)
                for task_id, task_data in data.items():
                    self.tasks[task_id] = CrawlTask.from_dict(task_data)
    
    def _save_tasks(self) -> None:
        """保存任务"""
        data = {tid: t.to_dict() for tid, t in self.tasks.items()}
        with open(self.queue_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def create_task(
        self,
        user_id: str,
        account_name: str,
        max_articles: int,
        payment_mode: str,
        amount: float
    ) -> CrawlTask:
        """创建新任务"""
        task_id = f"TASK-{int(time.time())}-{hash(user_id + account_name) % 10000}"
        
        task = CrawlTask(
            task_id=task_id,
            user_id=user_id,
            account_name=account_name,
            max_articles=max_articles,
            payment_mode=payment_mode,
            amount=amount,
            status=TaskStatus.PENDING_PAYMENT.value,
            created_at=datetime.now().isoformat(),
        )
        
        self.tasks[task_id] = task
        self._save_tasks()
        
        # 如果是实时支付，直接加入处理队列
        if payment_mode == "realtime":
            self.processing_queue.put(task_id)
        
        return task
    
    def confirm_payment(self, task_id: str, payment_proof: Dict) -> bool:
        """确认支付"""
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        task.payment_proof = payment_proof
        task.status = TaskStatus.PAYMENT_CONFIRMED.value
        
        # 加入处理队列
        self.processing_queue.put(task_id)
        self._save_tasks()
        
        return True
    
    def get_task(self, task_id: str) -> Optional[CrawlTask]:
        """获取任务"""
        return self.tasks.get(task_id)
    
    def get_user_tasks(self, user_id: str, limit: int = 10) -> list:
        """获取用户的任务列表"""
        user_tasks = [
            t for t in self.tasks.values() 
            if t.user_id.lower() == user_id.lower()
        ]
        # 按创建时间倒序
        user_tasks.sort(key=lambda x: x.created_at, reverse=True)
        return user_tasks[:limit]
    
    def update_task_status(
        self, 
        task_id: str, 
        status: str,
        result: Optional[Dict] = None,
        error: Optional[str] = None
    ) -> None:
        """更新任务状态"""
        if task_id not in self.tasks:
            return
        
        task = self.tasks[task_id]
        task.status = status
        
        if status == TaskStatus.PROCESSING.value:
            task.started_at = datetime.now().isoformat()
        
        if status in [TaskStatus.COMPLETED.value, TaskStatus.FAILED.value]:
            task.completed_at = datetime.now().isoformat()
            task.result = result
            task.error = error
        
        self._save_tasks()
    
    def start_worker(self, crawl_callback: Callable) -> None:
        """启动后台工作线程"""
        if self._running:
            return
        
        self._running = True
        self._worker_thread = threading.Thread(
            target=self._worker_loop,
            args=(crawl_callback,),
            daemon=True
        )
        self._worker_thread.start()
        print(f"✅ 异步任务队列已启动")
    
    def stop_worker(self) -> None:
        """停止后台工作线程"""
        self._running = False
        if self._worker_thread:
            self._worker_thread.join(timeout=5)
    
    def _worker_loop(self, crawl_callback: Callable) -> None:
        """工作线程循环"""
        while self._running:
            try:
                # 获取任务（阻塞1秒）
                task_id = self.processing_queue.get(timeout=1)
                task = self.tasks.get(task_id)
                
                if not task:
                    continue
                
                print(f"🚀 开始执行任务: {task_id}")
                self.update_task_status(task_id, TaskStatus.PROCESSING.value)
                
                try:
                    # 执行爬取
                    result = crawl_callback(
                        account_name=task.account_name,
                        max_articles=task.max_articles
                    )
                    
                    self.update_task_status(
                        task_id, 
                        TaskStatus.COMPLETED.value,
                        result={"articles_count": len(result) if result else 0}
                    )
                    
                    print(f"✅ 任务完成: {task_id}")
                    
                    # TODO: 发送通知（飞书/webhook）
                    self._send_notification(task, success=True)
                    
                except Exception as e:
                    error_msg = str(e)
                    task.retry_count += 1
                    
                    if task.retry_count < QUEUE_CONFIG["max_retries"]:
                        # 重试
                        print(f"⚠️ 任务失败，准备重试 ({task.retry_count}/{QUEUE_CONFIG['max_retries']}): {task_id}")
                        time.sleep(QUEUE_CONFIG["retry_delay"])
                        self.processing_queue.put(task_id)
                    else:
                        # 最终失败
                        self.update_task_status(
                            task_id,
                            TaskStatus.FAILED.value,
                            error=error_msg
                        )
                        print(f"❌ 任务最终失败: {task_id}, 错误: {error_msg}")
                        self._send_notification(task, success=False, error=error_msg)
                
            except Exception as e:
                # 队列为空，继续循环
                pass
    
    def _send_notification(
        self, 
        task: CrawlTask, 
        success: bool,
        error: str = ""
    ) -> None:
        """发送任务完成通知"""
        # 简化版：打印到控制台
        # 实际应接入飞书/webhook
        
        if success:
            print(f"📧 通知用户 {task.user_id}: 任务 {task.task_id} 完成")
        else:
            print(f"📧 通知用户 {task.user_id}: 任务 {task.task_id} 失败 - {error}")


if __name__ == "__main__":
    # 测试
    queue = AsyncTaskQueue()
    
    # 创建测试任务
    task = queue.create_task(
        user_id="0xTestUser",
        account_name="机器之心",
        max_articles=50,
        payment_mode="async",
        amount=10.0
    )
    
    print(f"创建任务: {task.task_id}")
    print(f"状态: {task.status}")
    
    # 模拟支付确认
    queue.confirm_payment(task.task_id, {"tx_hash": "0x123", "amount": 10.0})
    
    updated = queue.get_task(task.task_id)
    print(f"支付确认后状态: {updated.status}")
