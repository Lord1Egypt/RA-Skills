#!/usr/bin/env python3
"""
合并现有待办任务的提醒
"""
import json
import subprocess
import os
from datetime import datetime, timedelta
from collections import defaultdict

TODO_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo.json")
REMINDER_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo-reminders.json")
SESSION_CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo-session-config.json")

def load_session_context():
    """加载当前会话配置"""
    if not os.path.exists(SESSION_CONFIG_FILE):
        return None
    try:
        with open(SESSION_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            if config.get("channel") and config.get("target"):
                return config
            return None
    except:
        return None

def get_time_bucket(timestamp: float, minutes: int = 15) -> str:
    """将时间戳对齐到时间桶"""
    dt = datetime.fromtimestamp(timestamp)
    bucket = dt.replace(minute=(dt.minute // minutes) * minutes, second=0, microsecond=0)
    return bucket.strftime("%Y-%m-%d %H:%M")

def create_cron_reminder(name: str, at_time: str, message: str) -> bool:
    """创建 cron 提醒"""
    # 获取会话配置
    session = load_session_context()
    if not session:
        print("❌ 错误：缺少会话配置，请先运行 send-status 或 send-list 设置会话信息")
        return False
    
    cmd = [
        "openclaw", "cron", "add",
        "--name", name,
        "--at", at_time,
        "--channel", session["channel"],
        "--to", session["target"],
        "--message", message
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception as e:
        print(f"   ❌ 创建失败：{str(e)}")
        return False

def main():
    # 读取待办任务
    with open(TODO_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    tasks = data.get("tasks", [])
    
    # 筛选未完成且有到期时间的任务
    pending_tasks = [
        t for t in tasks 
        if t["status"] == "pending" and t.get("dueAt")
    ]
    
    print(f"📋 找到 {len(pending_tasks)} 个未完成且有到期时间的任务\n")
    
    # 按时间桶分组
    buckets = defaultdict(list)
    for task in pending_tasks:
        bucket = get_time_bucket(task["dueAt"])
        buckets[bucket].append(task)
    
    # 显示分组结果
    print("📦 时间桶分组结果：")
    print("-" * 80)
    for bucket, bucket_tasks in sorted(buckets.items()):
        print(f"\n时间桶：{bucket}（{len(bucket_tasks)}个任务）")
        for task in bucket_tasks:
            due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
            print(f"  [{task['id']}] {task['title']} - 到期：{due_str}")
    
    print("\n" + "=" * 80)
    print("开始创建合并提醒...\n")
    
    # 保存提醒数据
    reminders_data = {"reminders": {}}
    created_count = 0
    
    for bucket_time, bucket_tasks in sorted(buckets.items()):
        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        bucket_tasks.sort(key=lambda t: (
            priority_order.get(t.get("priority", "medium"), 1),
            t.get("dueAt", 0)
        ))
        
        # 构建提醒消息
        message_lines = ["⏰ 待办提醒 - 以下任务即将到期：\n"]
        for task in bucket_tasks:
            task_due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
            priority_emoji = {
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(task.get("priority", "medium"), "⚪")
            message_lines.append(f"{priority_emoji} [{task['id']}] {task['title']}")
            message_lines.append(f"   到期：{task_due_str}\n")
        
        # 提醒时间
        bucket_dt = datetime.strptime(bucket_time, "%Y-%m-%d %H:%M")
        now = datetime.now()
        
        # 只为未来的任务创建提醒
        if bucket_dt <= now:
            print(f"⏭️  跳过已过期的时间桶：{bucket_time}")
            continue
        
        reminder_times = []
        reminder_30 = bucket_dt - timedelta(minutes=30)
        reminder_15 = bucket_dt - timedelta(minutes=15)
        
        if reminder_30 > now:
            reminder_times.append(("30min", reminder_30))
        if reminder_15 > now:
            reminder_times.append(("15min", reminder_15))
        reminder_times.append(("ontime", bucket_dt))
        
        # 创建提醒
        reminder_name = f"todo-merged-{bucket_time.replace(' ', '-').replace(':', '')}"
        job_ids = []
        
        for label, reminder_time in reminder_times:
            cron_time = reminder_time.strftime("%H:%M %Y-%m-%d")
            full_name = f"{reminder_name}-{label}"
            
            # 根据提醒时间调整消息
            if label == "30min":
                msg = f"⏰ 待办提醒（30分钟后）：\n\n" + "\n".join(message_lines[1:])
            elif label == "15min":
                msg = f"⏰ 待办提醒（15分钟后）：\n\n" + "\n".join(message_lines[1:])
            else:
                msg = "\n".join(message_lines)
            
            # 创建提醒
            if create_cron_reminder(full_name, cron_time, msg):
                created_count += 1
                job_ids.append(full_name)
        
        # 保存提醒信息
        reminders_data["reminders"][reminder_name] = {
            "time_bucket": bucket_time,
            "task_ids": [t["id"] for t in bucket_tasks],
            "job_ids": job_ids,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"✅ 已创建合并提醒：{bucket_time}（{len(bucket_tasks)}个任务，{len(job_ids)}个提醒时间点）")
    
    # 保存提醒数据
    os.makedirs(os.path.dirname(REMINDER_FILE), exist_ok=True)
    with open(REMINDER_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'=' * 80}")
    print(f"🎉 完成！共创建 {created_count} 个提醒任务")
    print(f"💾 提醒数据已保存到：{REMINDER_FILE}")

if __name__ == "__main__":
    main()
