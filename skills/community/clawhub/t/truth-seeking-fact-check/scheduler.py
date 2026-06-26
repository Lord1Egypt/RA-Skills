#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.5.0 - 定时核查模块
功能：支持定时重复核查，资源可控适配2核2G，默认关闭，用户配置开启
设计原则：默认关闭，最大频率每天一次，单次不超过10篇，变化≥2分才告警，最大并发=2
"""

from typing import Dict, List, Optional, Callable
import logging
import time
from dataclasses import dataclass
from threading import Thread
from typing import Dict, List, Optional, Callable

logger = logging.getLogger(__name__)

@dataclass
class TimedCheckTask:
    """定时核查任务"""
    text: str
    last_score: Optional[float] = None
    interval_hours: int = 24  # 默认每天一次
    last_check: float = 0
    callback: Optional[Callable] = None
    enabled: bool = True


class TimedScheduler:
    """定时核查调度器，适配2核2G资源约束"""
    
    def __init__(self, skill_instance, config: Dict):
        """
        初始化定时调度器
        config: {
            "interval_hours": 24,  # 默认间隔，最小24小时
            "max_tasks": 10,       # 最大任务数，控制资源
            "alert_threshold": 2,  # 分数变化超过这个值才告警
            "max_concurrency": 2   # 最大并发，和批量一致，适配2核2G
        }
        """
        self.skill = skill_instance
        self.config = config
        self.default_interval = max(24, config.get('interval_hours', 24))  # 最小间隔24小时
        self.max_tasks = min(10, config.get('max_tasks', 10))  # 最大10个任务，控制资源
        self.alert_threshold = max(1, config.get('alert_threshold', 2))
        self.max_concurrency = min(2, config.get('max_concurrency', 2))
        
        self.tasks: Dict[str, TimedCheckTask] = {}
        self.running = False
        self.thread: Optional[Thread] = None
    
    def add_task(self, text: str, callback: Optional[Callable] = None) -> Dict:
        """添加定时核查任务"""
        if len(self.tasks) >= self.max_tasks:
            return {
                "status": "error",
                "message": f"已达到最大任务数{self.max_tasks}，请删除旧任务后添加"
            }
        
        # 使用文本hash作为任务id
        task_id = str(hash(text))[:16]
        task = TimedCheckTask(
            text=text,
            interval_hours=self.default_interval,
            callback=callback,
            enabled=True
        )
        self.tasks[task_id] = task
        logger.info(f"添加定时核查任务: {task_id}")
        return {
            "status": "ok",
            "task_id": task_id,
            "message": f"定时核查任务已添加，间隔{self.default_interval}小时"
        }
    
    def remove_task(self, task_id: str) -> Dict:
        """移除定时核查任务"""
        if task_id in self.tasks:
            del self.tasks[task_id]
            return {"status": "ok", "message": f"任务{task_id}已移除"}
        else:
            return {"status": "error", "message": f"任务{task_id}不存在"}
    
    def _run_loop(self):
        """定时检查循环，在后台线程运行"""
        logger.info("定时核查调度器启动")
        while self.running:
            current_time = time.time()
            for task_id, task in self.tasks.items():
                if not task.enabled:
                    continue
                # 检查是否到时间
                interval_seconds = task.interval_hours * 3600
                if current_time - task.last_check >= interval_seconds:
                    logger.info(f"执行定时核查: {task_id}")
                    # 执行核查
                    try:
                        result = self.skill.check_text(task.text, output_format="json")
                        current_score = result.get('credibility_score', 0)
                        # 更新最后检查时间
                        task.last_check = current_time
                        
                        # 判断是否需要告警
                        if task.last_score is not None:
                            change = abs(current_score - task.last_score)
                            if change >= self.alert_threshold:
                                # 触发告警回调
                                if task.callback:
                                    task.callback(task_id, task.last_score, current_score, result)
                                logger.info(f"定时核查{task_id}: 分数变化{change:.1f}，已触发告警")
                        
                        # 更新上次分数
                        task.last_score = current_score
                    except Exception as e:
                        logger.error(f"定时核查{task_id}执行失败: {str(e)}")
            
            # 睡眠1小时再检查，避免频繁占用资源
            time.sleep(3600)
    
    def start(self):
        """启动定时调度器"""
        if self.running:
            return {"status": "ok", "message": "定时核查调度器已在运行中"}
        
        self.running = True
        self.thread = Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        logger.info("定时核查调度器后台线程已启动")
        return {"status": "ok", "message": "定时核查调度器已启动，后台运行"}
    
    def stop(self):
        """停止定时调度器"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
            self.thread = None
        logger.info("定时核查调度器已停止")
        return {"status": "ok", "message": "定时核查调度器已停止"}
    
    def list_tasks(self) -> Dict:
        """列出所有定时任务"""
        tasks_info = []
        for task_id, task in self.tasks.items():
            tasks_info.append({
                "task_id": task_id,
                "last_score": task.last_score,
                "last_check": task.last_check,
                "interval_hours": task.interval_hours,
                "enabled": task.enabled,
                "text_length": len(task.text)
            })
        return {
            "status": "ok",
            "tasks": tasks_info,
            "total": len(tasks_info),
            "max_tasks": self.max_tasks
        }
