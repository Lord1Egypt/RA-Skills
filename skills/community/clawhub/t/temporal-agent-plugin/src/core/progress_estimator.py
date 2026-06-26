import time
from typing import Dict, Any, Optional, Callable

class ProgressEstimator:
    """进度预估系统
    
    负责预测任务的执行进度和剩余时间
    """
    
    def __init__(self):
        self.tasks = {}
        self.progress_callbacks = {}
    
    def start_task(self, task_id: str, task_type: str, total_steps: int = 100):
        """开始任务
        
        Args:
            task_id: 任务ID
            task_type: 任务类型
            total_steps: 总步骤数
        """
        self.tasks[task_id] = {
            'task_type': task_type,
            'total_steps': total_steps,
            'current_step': 0,
            'start_time': time.time(),
            'last_update_time': time.time(),
            'progress_history': []
        }
    
    def update_progress(self, task_id: str, current_step: int, **kwargs):
        """更新任务进度
        
        Args:
            task_id: 任务ID
            current_step: 当前步骤
            **kwargs: 额外信息
        """
        if task_id in self.tasks:
            now = time.time()
            task = self.tasks[task_id]
            
            # 计算进度百分比
            progress = min(current_step / task['total_steps'], 1.0)
            
            # 计算已用时间
            elapsed_time = now - task['start_time']
            
            # 计算剩余时间
            if progress > 0:
                estimated_total_time = elapsed_time / progress
                remaining_time = estimated_total_time - elapsed_time
            else:
                remaining_time = 0
            
            # 更新任务信息
            task['current_step'] = current_step
            task['last_update_time'] = now
            task['progress'] = progress
            task['elapsed_time'] = elapsed_time
            task['remaining_time'] = remaining_time
            
            # 记录进度历史
            task['progress_history'].append({
                'timestamp': now,
                'progress': progress,
                'elapsed_time': elapsed_time,
                'remaining_time': remaining_time,
                **kwargs
            })
            
            # 调用回调函数
            if task_id in self.progress_callbacks:
                self.progress_callbacks[task_id](task)
    
    def get_progress(self, task_id: str) -> Dict[str, Any]:
        """获取任务进度
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务进度信息
        """
        if task_id in self.tasks:
            task = self.tasks[task_id]
            return {
                'task_type': task['task_type'],
                'total_steps': task['total_steps'],
                'current_step': task['current_step'],
                'progress': task.get('progress', 0),
                'elapsed_time': task.get('elapsed_time', 0),
                'remaining_time': task.get('remaining_time', 0),
                'start_time': task['start_time'],
                'last_update_time': task['last_update_time']
            }
        return {}
    
    def get_remaining_time(self, task_id: str) -> float:
        """获取剩余时间
        
        Args:
            task_id: 任务ID
            
        Returns:
            剩余时间（秒）
        """
        if task_id in self.tasks:
            return self.tasks[task_id].get('remaining_time', 0)
        return 0
    
    def register_progress_callback(self, task_id: str, callback: Callable):
        """注册进度回调函数
        
        Args:
            task_id: 任务ID
            callback: 回调函数
        """
        self.progress_callbacks[task_id] = callback
    
    def remove_task(self, task_id: str):
        """移除任务
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
        if task_id in self.progress_callbacks:
            del self.progress_callbacks[task_id]
    
    def get_all_tasks(self) -> Dict[str, Dict[str, Any]]:
        """获取所有任务
        
        Returns:
            所有任务信息
        """
        return self.tasks