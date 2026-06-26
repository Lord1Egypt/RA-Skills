import os
import json
import uuid
import re
import glob
from datetime import datetime, timedelta

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.tasks')

if not os.path.exists(TASKS_DIR):
    os.makedirs(TASKS_DIR)

def clean_old_tasks(days_to_keep=7, max_tasks=1000):
    """清理旧任务文件"""
    try:
        files = glob.glob(os.path.join(TASKS_DIR, "*.json"))
        
        # 1. 按时间清理
        now = datetime.now()
        cutoff = now - timedelta(days=days_to_keep)
        
        kept_files = []
        for f in files:
            try:
                mtime = datetime.fromtimestamp(os.path.getmtime(f))
                if mtime < cutoff:
                    os.remove(f)
                else:
                    kept_files.append((mtime, f))
            except OSError:
                pass
        
        # 2. 按数量清理（保留最新的N个）
        if len(kept_files) > max_tasks:
            kept_files.sort(key=lambda x: x[0], reverse=True)
            for _, f in kept_files[max_tasks:]:
                try:
                    os.remove(f)
                except OSError:
                    pass
                    
    except Exception as e:
        print(f"清理任务失败: {e}")

def repair_json(json_str):
    """尝试修复不合法的 JSON 字符串"""
    if not json_str:
        return {}
        
    # 尝试直接解析
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass
        
    # 1. 提取 Markdown 代码块中的 JSON
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', json_str)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
            
    # 2. 尝试修复常见的尾部逗号
    clean_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    try:
        return json.loads(clean_str)
    except json.JSONDecodeError:
        pass
        
    # 3. 尝试截取第一个 { 到最后一个 }
    start = json_str.find('{')
    end = json_str.rfind('}')
    if start != -1 and end != -1:
        try:
            return json.loads(json_str[start:end+1])
        except json.JSONDecodeError:
            pass
            
    # 无法修复，返回原始字符串封装
    return {"raw_content": json_str, "error": "JSON解析失败"}

def create_task(task_type, params):
    """创建新任务"""
    # 每次创建任务时顺便触发一次清理（简单粗暴但有效）
    # 在生产环境中应该由独立 cron 触发，这里为了简单直接集成
    if os.environ.get("VISION_AUTO_CLEANUP", "true").lower() == "true":
        # 简单的概率触发，避免每次都扫盘
        import random
        if random.random() < 0.1: 
            clean_old_tasks()

    task_id = str(uuid.uuid4())
    task_data = {
        "id": task_id,
        "type": task_type,
        "params": params,
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "result": None,
        "error": None
    }
    save_task(task_id, task_data)
    return task_id

def get_task(task_id):
    """获取任务信息"""
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    if not os.path.exists(task_file):
        return None
    try:
        with open(task_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"id": task_id, "status": "error", "error": f"读取任务文件失败: {str(e)}"}

def update_task(task_id, updates):
    """更新任务信息"""
    task = get_task(task_id)
    if not task:
        return False
    
    task.update(updates)
    task['updated_at'] = datetime.now().isoformat()
    save_task(task_id, task)
    return True

def save_task(task_id, data):
    """保存任务信息到文件"""
    task_file = os.path.join(TASKS_DIR, f"{task_id}.json")
    with open(task_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
