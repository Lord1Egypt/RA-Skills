from __future__ import annotations
"""
async_manager.py - 异步任务管理器

功能：
1. 管理异步任务的执行
2. 处理耗时操作，如文件处理、LLM调用、向量嵌入计算等
3. 提供任务队列和状态管理
4. 支持任务取消和结果获取

使用方式：
    from async_manager import AsyncManager
    async_manager = AsyncManager()
    
    # 提交异步任务
    task_id = await async_manager.submit_task(process_file, file_path)
    
    # 获取任务状态
    status = async_manager.get_task_status(task_id)
    
    # 获取任务结果
    result = await async_manager.get_task_result(task_id)
"""

import asyncio
import uuid
import time
import logging
from typing import Any, Callable, Dict, Optional

logger = logging.getLogger(__name__)


class TaskStatus:
    """任务状态"""
    PENDING = "pending"      # 等待执行
    RUNNING = "running"      # 执行中
    COMPLETED = "completed"  # 执行完成
    FAILED = "failed"        # 执行失败
    CANCELLED = "cancelled"  # 任务取消


class AsyncTask:
    """异步任务"""
    
    def __init__(self, task_id: str, coro: Callable, args: tuple = (), kwargs: dict = None):
        """
        初始化异步任务
        
        Args:
            task_id: 任务ID
            coro: 异步函数
            args: 位置参数
            kwargs: 关键字参数
        """
        self.task_id = task_id
        self.coro = coro
        self.args = args
        self.kwargs = kwargs or {}
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.start_time = None
        self.end_time = None
        self.task = None

    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "status": self.status,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "error": self.error,
            "result": str(self.result) if self.result else None
        }


class AsyncManager:
    """异步任务管理器"""
    
    def __init__(self, max_concurrent_tasks: int = 5):
        """
        初始化异步任务管理器
        
        Args:
            max_concurrent_tasks: 最大并发任务数
        """
        self.max_concurrent_tasks = max_concurrent_tasks
        self.tasks: Dict[str, AsyncTask] = {}
        self.task_queue = asyncio.Queue()
        self.running_tasks = 0
        self._stop_event = asyncio.Event()
        self._worker_task = None

    async def start(self):
        """启动任务管理器"""
        if self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker())
            logger.info("异步任务管理器已启动")

    async def stop(self):
        """停止任务管理器"""
        self._stop_event.set()
        if self._worker_task:
            await self._worker_task
            self._worker_task = None
        logger.info("异步任务管理器已停止")

    async def submit_task(self, coro: Callable, *args, **kwargs) -> str:
        """
        提交异步任务
        
        Args:
            coro: 异步函数
            *args: 位置参数
            **kwargs: 关键字参数
        
        Returns:
            str: 任务ID
        """
        task_id = str(uuid.uuid4())[:12]
        task = AsyncTask(task_id, coro, args, kwargs)
        self.tasks[task_id] = task
        await self.task_queue.put(task)
        
        # 如果任务管理器未启动，自动启动
        if self._worker_task is None:
            await self.start()
        
        return task_id

    async def get_task_status(self, task_id: str) -> Optional[Dict]:
        """
        获取任务状态
        
        Args:
            task_id: 任务ID
        
        Returns:
            Optional[Dict]: 任务状态信息
        """
        task = self.tasks.get(task_id)
        if task:
            return task.to_dict()
        return None

    async def get_task_result(self, task_id: str, timeout: float = None) -> Any:
        """
        获取任务结果
        
        Args:
            task_id: 任务ID
            timeout: 超时时间（秒）
        
        Returns:
            Any: 任务结果
        """
        task = self.tasks.get(task_id)
        if not task:
            raise ValueError(f"任务不存在: {task_id}")
        
        # 等待任务完成
        start_time = time.time()
        while task.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED]:
            if timeout and time.time() - start_time > timeout:
                raise asyncio.TimeoutError(f"任务超时: {task_id}")
            await asyncio.sleep(0.1)
        
        if task.status == TaskStatus.FAILED:
            raise Exception(f"任务执行失败: {task.error}")
        elif task.status == TaskStatus.CANCELLED:
            raise asyncio.CancelledError("任务已取消")
        
        return task.result

    async def cancel_task(self, task_id: str) -> bool:
        """
        取消任务
        
        Args:
            task_id: 任务ID
        
        Returns:
            bool: 是否取消成功
        """
        task = self.tasks.get(task_id)
        if not task:
            return False
        
        if task.status == TaskStatus.RUNNING and task.task:
            task.task.cancel()
            task.status = TaskStatus.CANCELLED
            return True
        elif task.status == TaskStatus.PENDING:
            # 从队列中移除
            new_queue = asyncio.Queue()
            while not self.task_queue.empty():
                queue_task = await self.task_queue.get()
                if queue_task.task_id != task_id:
                    await new_queue.put(queue_task)
            self.task_queue = new_queue
            task.status = TaskStatus.CANCELLED
            return True
        
        return False

    async def _worker(self):
        """工作线程"""
        while not self._stop_event.is_set():
            try:
                # 等待任务，设置超时以检查停止事件
                task = await asyncio.wait_for(self.task_queue.get(), timeout=0.1)
                
                # 检查是否达到最大并发任务数
                while self.running_tasks >= self.max_concurrent_tasks:
                    await asyncio.sleep(0.1)
                
                # 执行任务
                self.running_tasks += 1
                await self._execute_task(task)
                self.running_tasks -= 1
                
                # 标记任务队列项为完成
                self.task_queue.task_done()
            except asyncio.TimeoutError:
                # 超时，检查停止事件
                continue
            except Exception as e:
                logger.error(f"工作线程错误: {e}")

    async def _execute_task(self, task: AsyncTask):
        """执行任务"""
        task.status = TaskStatus.RUNNING
        task.start_time = time.time()
        
        try:
            # 执行异步函数
            task.result = await task.coro(*task.args, **task.kwargs)
            task.status = TaskStatus.COMPLETED
            task.end_time = time.time()
            logger.info(f"任务完成: {task.task_id}")
        except asyncio.CancelledError:
            task.status = TaskStatus.CANCELLED
            task.end_time = time.time()
            logger.info(f"任务取消: {task.task_id}")
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.end_time = time.time()
            logger.error(f"任务失败: {task.task_id}, 错误: {e}")

    def get_stats(self) -> Dict:
        """
        获取统计信息
        
        Returns:
            Dict: 统计信息
        """
        status_counts = {}
        for task in self.tasks.values():
            status_counts[task.status] = status_counts.get(task.status, 0) + 1
        
        return {
            "total_tasks": len(self.tasks),
            "status_counts": status_counts,
            "running_tasks": self.running_tasks,
            "queue_size": self.task_queue.qsize(),
            "max_concurrent_tasks": self.max_concurrent_tasks
        }


# 全局异步任务管理器实例
_async_manager = None

def get_async_manager() -> AsyncManager:
    """
    获取全局异步任务管理器实例
    
    Returns:
        AsyncManager: 异步任务管理器实例
    """
    global _async_manager
    if _async_manager is None:
        _async_manager = AsyncManager()
    return _async_manager


# 异步工具函数
async def async_wrap(func: Callable, *args, **kwargs) -> Any:
    """
    将同步函数包装为异步函数
    
    Args:
        func: 同步函数
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        Any: 函数结果
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


async def process_file_async(file_path: str, processor: Callable) -> Dict:
    """
    异步处理文件
    
    Args:
        file_path: 文件路径
        processor: 文件处理器函数
    
    Returns:
        Dict: 处理结果
    """
    return await async_wrap(processor, file_path)


async def llm_call_async(prompt: str, llm_fn: Callable) -> str:
    """
    异步调用LLM
    
    Args:
        prompt: 提示词
        llm_fn: LLM函数
    
    Returns:
        str: LLM响应
    """
    return await async_wrap(llm_fn, prompt)


async def embedding_async(text: str, embed_fn: Callable) -> list:
    """
    异步计算向量嵌入
    
    Args:
        text: 文本
        embed_fn: 嵌入函数
    
    Returns:
        list: 向量嵌入
    """
    return await async_wrap(embed_fn, text)
