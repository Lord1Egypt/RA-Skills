"""
任务追踪器 - 支持任务编号（T01, T02...）
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional


class TaskTracker:
    """任务追踪器"""
    
    def __init__(self, storage_dir: str = "./data/tasks"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    # ========== 任务 CRUD ==========
    
    def create_task(self, user_id: str, title: str, description: str = "") -> Dict:
        """创建新任务，自动分配编号"""
        tasks = self._load_tasks(user_id)
        
        # 生成编号
        task_id = f"T{len(tasks) + 1:02d}"
        
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "status": "pending",  # pending/in_progress/done/cancelled
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        tasks[task_id] = task
        self._save_tasks(user_id, tasks)
        return task
    
    def get_task(self, user_id: str, task_id: str) -> Optional[Dict]:
        """获取任务"""
        task_id = task_id.upper()
        tasks = self._load_tasks(user_id)
        return tasks.get(task_id)
    
    def update_status(self, user_id: str, task_id: str, status: str) -> Optional[Dict]:
        """更新任务状态"""
        task_id = task_id.upper()
        tasks = self._load_tasks(user_id)
        
        if task_id not in tasks:
            return None
        
        tasks[task_id]["status"] = status
        tasks[task_id]["updated_at"] = datetime.now().isoformat()
        self._save_tasks(user_id, tasks)
        return tasks[task_id]
    
    def list_tasks(self, user_id: str, status: str = None) -> List[Dict]:
        """列出任务"""
        tasks = self._load_tasks(user_id)
        result = list(tasks.values())
        
        if status:
            result = [t for t in result if t["status"] == status]
        
        return sorted(result, key=lambda x: x["id"])
    
    # ========== 任务识别 ==========
    
    def detect_task_reference(self, message: str) -> Optional[str]:
        """检测消息中是否引用了任务编号"""
        pattern = r'\b[Tt]\d{1,3}\b'
        match = re.search(pattern, message)
        if match:
            return match.group().upper()
        return None
    
    def detect_new_task(self, message: str, intent) -> bool:
        """检测是否是新任务"""
        from task_parser import TaskIntent
        task_keywords = ["帮我", "请", "需要", "要做", "实现", "创建", "开发", "优化"]
        is_command = intent == TaskIntent.COMMAND
        has_keyword = any(kw in message for kw in task_keywords)
        return is_command and has_keyword
    
    # ========== 格式化输出 ==========
    
    def format_task(self, task: Dict) -> str:
        """格式化单个任务"""
        status_emoji = {
            "pending": "⏳",
            "in_progress": "🔄",
            "done": "✅",
            "cancelled": "❌"
        }
        emoji = status_emoji.get(task["status"], "❓")
        return f"{emoji} [{task['id']}] {task['title']}"
    
    def format_task_list(self, tasks: List[Dict]) -> str:
        """格式化任务列表"""
        if not tasks:
            return "暂无任务"
        return "\n".join(self.format_task(t) for t in tasks)
    
    # ========== 存储 ==========
    
    def _load_tasks(self, user_id: str) -> Dict:
        path = os.path.join(self.storage_dir, f"{user_id}_tasks.json")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_tasks(self, user_id: str, tasks: Dict):
        path = os.path.join(self.storage_dir, f"{user_id}_tasks.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
