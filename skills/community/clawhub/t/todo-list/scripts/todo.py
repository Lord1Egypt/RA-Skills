#!/usr/bin/env python3
import json
import os
import uuid
import subprocess
import shutil
from datetime import datetime, timedelta
import argparse
from typing import List, Dict, Optional
import time

TODO_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo.json")
ATTACHMENTS_DIR = os.path.expanduser("~/.openclaw/workspace/memory/todo-attachments")
REMINDER_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo-reminders.json")
SESSION_CONFIG_FILE = os.path.expanduser("~/.openclaw/workspace/memory/todo-session-config.json")

def init_todo_file():
    """初始化待办文件"""
    os.makedirs(os.path.dirname(TODO_FILE), exist_ok=True)
    os.makedirs(ATTACHMENTS_DIR, exist_ok=True)
    if not os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'w') as f:
            json.dump({"tasks": [], "projects": {}, "tags": []}, f, indent=2, ensure_ascii=False)

def load_data() -> Dict:
    """加载所有数据"""
    init_todo_file()
    with open(TODO_FILE, 'r') as f:
        data = json.load(f)
    # 确保所有字段存在
    if "tasks" not in data:
        data["tasks"] = []
    if "projects" not in data:
        data["projects"] = {}
    if "tags" not in data:
        data["tags"] = []
    return data

def save_data(data: Dict):
    """保存数据到文件"""
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_tasks() -> List[Dict]:
    """加载所有任务"""
    return load_data().get("tasks", [])

def save_tasks(tasks: List[Dict]):
    """保存任务到文件"""
    data = load_data()
    data["tasks"] = tasks
    save_data(data)

def get_all_tags() -> List[str]:
    """获取所有标签"""
    data = load_data()
    tags = set(data.get("tags", []))
    # 从任务中收集标签
    for task in data.get("tasks", []):
        if "tags" in task:
            tags.update(task["tags"])
    return sorted(list(tags))

def update_tags_list():
    """更新标签列表"""
    data = load_data()
    tags = set(data.get("tags", []))
    for task in data.get("tasks", []):
        if "tags" in task:
            tags.update(task["tags"])
    data["tags"] = sorted(list(tags))
    save_data(data)

def load_reminders() -> Dict:
    """加载提醒数据"""
    if not os.path.exists(REMINDER_FILE):
        return {"reminders": {}}
    try:
        with open(REMINDER_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {"reminders": {}}

def save_reminders(reminders_data: Dict):
    """保存提醒数据"""
    os.makedirs(os.path.dirname(REMINDER_FILE), exist_ok=True)
    with open(REMINDER_FILE, 'w', encoding='utf-8') as f:
        json.dump(reminders_data, f, indent=2, ensure_ascii=False)

def create_cron_job(name: str, cron_time: str, message: str, channel: str = None, target: str = None) -> Optional[str]:
    """创建 cron 任务并返回 job_id
    
    Args:
        name: 任务名称
        cron_time: 时间，格式 "HH:MM YYYY-MM-DD"
        message: 提醒消息
        channel: 频道名称（如 feishu），如果不提供则从配置读取
        target: 目标ID（如 user:ou_xxx），如果不提供则从配置读取
    """
    # 获取会话配置
    session = load_session_context()
    if not channel:
        channel = session.get("channel")
    if not target:
        target = session.get("target")
    
    # 如果仍然没有，给出错误提示
    if not channel or not target:
        print(f"   ⚠️  缺少会话配置：请先使用 send-status 或 send-list 命令设置 channel 和 target")
        return None
    
    # 使用 args 列表形式（不使用 shell=True）避免命令注入风险
    cmd = [
        "openclaw", "cron", "add",
        "--name", name,
        "--at", cron_time,
        "--channel", channel,
        "--to", target,
        "--message", message
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            import re
            match = re.search(r'"id":\s*"([^"]+)"', result.stdout)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"   ⚠️  创建提醒失败：{str(e)}")
    return None

def get_time_bucket(timestamp: float, minutes: int = 15) -> str:
    """将时间戳转换为时间桶（用于合并相近时间的任务）"""
    dt = datetime.fromtimestamp(timestamp)
    # 向下取整到最近的N分钟
    bucket = dt.replace(minute=(dt.minute // minutes) * minutes, second=0, microsecond=0)
    return bucket.strftime("%Y-%m-%d %H:%M")

def find_tasks_in_time_bucket(target_bucket: str, minutes: int = 15) -> List[Dict]:
    """查找在同一个时间桶内的所有任务"""
    tasks = load_tasks()
    matching_tasks = []
    
    for task in tasks:
        if task["status"] != "pending" or not task.get("dueAt"):
            continue
        
        task_bucket = get_time_bucket(task["dueAt"], minutes)
        if task_bucket == target_bucket:
            matching_tasks.append(task)
    
    return matching_tasks

def create_or_update_merged_reminder(task_id: str, due_at: float, priority: str, title: str):
    """创建或更新合并提醒"""
    # 将时间对齐到15分钟的桶
    time_bucket = get_time_bucket(due_at, minutes=15)
    bucket_time = datetime.strptime(time_bucket, "%Y-%m-%d %H:%M")
    bucket_timestamp = bucket_time.timestamp()
    
    # 查找同一时间桶内的所有任务
    tasks_in_bucket = find_tasks_in_time_bucket(time_bucket, minutes=15)
    
    if len(tasks_in_bucket) == 0:
        # 如果没有任务，直接返回（理论上不应该发生）
        return
    
    # 加载提醒数据
    reminders_data = load_reminders()
    reminders = reminders_data.get("reminders", {})
    
    # 生成提醒名称
    reminder_name = f"todo-merged-{time_bucket.replace(' ', '-').replace(':', '')}"
    
    # 构建提醒消息
    message_lines = ["⏰ 待办提醒 - 以下任务即将到期：\n"]
    
    # 按优先级排序
    priority_order = {"high": 0, "medium": 1, "low": 2}
    tasks_in_bucket.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), t.get("dueAt", 0)))
    
    for task in tasks_in_bucket:
        task_due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "⚪")
        message_lines.append(f"{priority_emoji} [{task['id']}] {task['title']}")
        message_lines.append(f"   到期：{task_due_str}\n")
    
    reminder_message = "\n".join(message_lines)
    
    # 提醒时间：桶时间前30分钟和桶时间
    reminder_times = []
    
    # 计算桶时间
    bucket_dt = datetime.fromtimestamp(bucket_timestamp)
    now = datetime.now()
    
    # 30分钟前提醒
    reminder_30 = bucket_dt - timedelta(minutes=30)
    if reminder_30 > now:
        reminder_times.append(("30min", reminder_30))
    
    # 15分钟前提醒
    reminder_15 = bucket_dt - timedelta(minutes=15)
    if reminder_15 > now:
        reminder_times.append(("15min", reminder_15))
    
    # 准点提醒
    if bucket_dt > now:
        reminder_times.append(("ontime", bucket_dt))
    
    # 删除旧的提醒（如果存在）
    if reminder_name in reminders:
        for old_job_id in reminders[reminder_name].get("job_ids", []):
            try:
                subprocess.run(f"openclaw cron delete {old_job_id}", shell=True, capture_output=True)
            except:
                pass
    
    # 创建新提醒
    job_ids = []
    for label, reminder_time in reminder_times:
        cron_time = reminder_time.strftime("%H:%M %Y-%m-%d")
        
        # 根据提醒时间调整消息
        if label == "30min":
            msg = f"⏰ 待办提醒（30分钟后）：\n\n" + "\n".join(message_lines[1:])
        elif label == "15min":
            msg = f"⏰ 待办提醒（15分钟后）：\n\n" + "\n".join(message_lines[1:])
        else:
            msg = reminder_message
        
        full_name = f"{reminder_name}-{label}"
        job_id = create_cron_job(full_name, cron_time, msg)
        if job_id:
            job_ids.append(job_id)
    
    # 保存提醒信息
    reminders[reminder_name] = {
        "time_bucket": time_bucket,
        "task_ids": [t["id"] for t in tasks_in_bucket],
        "job_ids": job_ids,
        "created_at": datetime.now().isoformat()
    }
    save_reminders({"reminders": reminders})
    
    # 返回提醒信息
    return {
        "name": reminder_name,
        "tasks_count": len(tasks_in_bucket),
        "reminder_times": [rt[0] for rt in reminder_times]
    }

def extract_hashtags(text: str) -> List[str]:
    """从文本中提取#标签"""
    import re
    # 匹配 #标签名（支持中文、英文、数字、下划线、连字符）
    pattern = r'#([\w\u4e00-\u9fa5-]+)'
    hashtags = re.findall(pattern, text)
    return hashtags

def add_task(title: str, description: str = "", priority: str = "medium", due: str = None, tags: List[str] = None, attach: str = None):
    """添加新任务"""
    data = load_data()
    tasks = data.get("tasks", [])
    task_id = str(uuid.uuid4())[:8]
    now = datetime.now().timestamp()
    
    due_at = None
    if due:
        try:
            due_at = datetime.strptime(due, "%Y-%m-%d %H:%M").timestamp()
        except ValueError:
            try:
                due_at = datetime.strptime(due, "%Y-%m-%d").timestamp()
            except ValueError:
                print("❌ 时间格式错误，请使用 YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
                return
    
    # 处理标签
    if tags is None:
        tags = []
    
    # 自动提取标题和描述中的#标签
    extracted_tags = extract_hashtags(title) + extract_hashtags(description)
    
    # 合并标签（去重）
    all_tags = list(set(tags + extracted_tags))
    
    # 清理标题和描述中的#标签（可选，保留原文）
    # clean_title = re.sub(r'#([\w\u4e00-\u9fa5-]+)', r'\1', title)
    # clean_description = re.sub(r'#([\w\u4e00-\u9fa5-]+)', r'\1', description)
    
    # 处理附件
    attachments = []
    if attach:
        attachment_info = add_attachment(task_id, attach)
        if attachment_info:
            attachments.append(attachment_info)
    
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "pending",
        "tags": all_tags,
        "attachments": attachments,
        "createdAt": now,
        "dueAt": due_at,
        "completedAt": None,
        "projectName": None
    }
    
    # 检查标签是否属于某个项目
    projects = data.get("projects", {})
    for tag in all_tags:
        if tag in projects:
            task["projectName"] = projects[tag]["name"]
            break
    
    tasks.append(task)
    data["tasks"] = tasks
    
    # 更新标签列表
    existing_tags = set(data.get("tags", []))
    existing_tags.update(all_tags)
    data["tags"] = sorted(list(existing_tags))
    
    save_data(data)
    
    print(f"✅ 已添加任务：[{task_id}] {title}")
    if all_tags:
        print(f"   🏷️  标签：{', '.join(all_tags)}")
    if attachments:
        print(f"   📎 附件：{len(attachments)}个")
    if due_at:
        due_str = datetime.fromtimestamp(due_at).strftime("%Y-%m-%d %H:%M")
        print(f"   到期时间：{due_str}")
        
        # 使用合并提醒功能
        reminder_info = create_or_update_merged_reminder(task_id, due_at, priority, title)
        
        if reminder_info:
            tasks_count = reminder_info["tasks_count"]
            reminder_times = reminder_info["reminder_times"]
            
            if tasks_count > 1:
                print(f"   🕒 已创建/更新合并提醒（共{tasks_count}个任务）")
            else:
                print(f"   🕒 已创建提醒")
            
            if reminder_times:
                print(f"   📅 提醒时间：{', '.join(reminder_times)}")
    
    print(f"   优先级：{priority}")

def add_attachment(task_id: str, file_path: str) -> Optional[Dict]:
    """为任务添加附件
    
    安全措施：
    - 只允许访问用户明确指定的文件
    - 检查文件是否存在且可读
    - 限制文件大小（最大 50MB）
    - 不允许访问系统敏感目录（/etc, /root, /var 等）
    """
    # 安全检查：防止访问系统敏感目录
    sensitive_dirs = ["/etc", "/root", "/var/log", "/var/lib", "/proc", "/sys"]
    abs_path = os.path.abspath(file_path)
    for sensitive_dir in sensitive_dirs:
        if abs_path.startswith(sensitive_dir):
            print(f"❌ 安全限制：不允许访问系统目录 {sensitive_dir}")
            return None
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在：{file_path}")
        return None
    
    if not os.access(file_path, os.R_OK):
        print(f"❌ 文件不可读：{file_path}")
        return None
    
    # 检查文件大小（限制 50MB）
    file_size = os.path.getsize(file_path)
    max_size = 50 * 1024 * 1024  # 50MB
    if file_size > max_size:
        print(f"❌ 文件过大：{file_size / 1024 / 1024:.2f}MB（最大 50MB）")
        return None
    
    # 创建任务专属附件目录
    task_attach_dir = os.path.join(ATTACHMENTS_DIR, task_id)
    os.makedirs(task_attach_dir, exist_ok=True)
    
    # 复制文件
    file_name = os.path.basename(file_path)
    dest_path = os.path.join(task_attach_dir, file_name)
    
    # 如果文件名冲突，添加序号
    counter = 1
    base_name, ext = os.path.splitext(file_name)
    while os.path.exists(dest_path):
        file_name = f"{base_name}_{counter}{ext}"
        dest_path = os.path.join(task_attach_dir, file_name)
        counter += 1
    
    shutil.copy2(file_path, dest_path)
    
    return {
        "type": "file",
        "path": f"{task_id}/{file_name}",
        "name": file_name,
        "originalPath": file_path
    }

def attach_to_task(task_id: str, file_path: str):
    """为已有任务添加附件"""
    data = load_data()
    tasks = data.get("tasks", [])
    
    for task in tasks:
        if task["id"] == task_id:
            attachment_info = add_attachment(task_id, file_path)
            if attachment_info:
                if "attachments" not in task:
                    task["attachments"] = []
                task["attachments"].append(attachment_info)
                save_data(data)
                print(f"✅ 已添加附件：{attachment_info['name']}")
                print(f"   保存位置：{ATTACHMENTS_DIR}/{task_id}/")
            return
    
    print(f"❌ 未找到任务 ID：{task_id}")

def get_weekday_name(dt: datetime) -> str:
    """获取中文星期几"""
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    return weekdays[dt.weekday()]

def format_date_header(dt: datetime, now: datetime) -> str:
    """格式化日期标题"""
    date_str = dt.strftime("%Y-%m-%d")
    weekday = get_weekday_name(dt)
    
    # 判断是否是今天、明天、后天
    today = now.date()
    target_date = dt.date()
    delta = (target_date - today).days
    
    if delta == 0:
        return f"**📍 今天 - {date_str}（{weekday}）**"
    elif delta == 1:
        return f"**📍 明天 - {date_str}（{weekday}）**"
    elif delta == 2:
        return f"**📍 后天 - {date_str}（{weekday}）**"
    else:
        return f"**📍 {date_str}（{weekday}）**"

def list_tasks(status: str = "pending", priority: str = None, show_all: bool = False, tag: str = None):
    """列出任务"""
    data = load_data()
    tasks = data.get("tasks", [])
    projects = data.get("projects", {})
    now = datetime.now()

    # 按标签过滤
    if tag:
        tasks = [t for t in tasks if "tags" in t and tag in t["tags"]]
        
        # 检查是否是项目标签
        if tag in projects:
            project = projects[tag]
            project_tasks = tasks
            completed_count = len([t for t in project_tasks if t["status"] == "completed"])
            total_count = len(project_tasks)
            progress = (completed_count / total_count * 100) if total_count > 0 else 0
            
            print(f"\n📦 项目：{project['name']}")
            print(f"🏷️  标签：{tag}")
            print(f"📊 进度：{completed_count}/{total_count} 任务完成 ({progress:.1f}%)")
            print(f"📝 描述：{project.get('description', '无')}")
            print("-" * 80)

    # 分离已完成和未完成任务
    completed_tasks = [t for t in tasks if t["status"] == "completed"]
    pending_tasks = [t for t in tasks if t["status"] == "pending"]

    # 过滤优先级
    if priority:
        completed_tasks = [t for t in completed_tasks if t["priority"] == priority]
        pending_tasks = [t for t in pending_tasks if t["priority"] == priority]

    total_count = 0

    if status == "all":
        total_count = len(completed_tasks) + len(pending_tasks)
    elif status == "completed":
        total_count = len(completed_tasks)
        pending_tasks = []
    elif status == "pending":
        total_count = len(pending_tasks)
        completed_tasks = []

    if total_count == 0:
        print("📭 没有找到符合条件的任务")
        return

    # 打印标题
    if not tag:
        print(f"📋 待办事项时间线（共{total_count}个）")
        if status == "all" and completed_tasks:
            print(f"✅ 已完成：{len(completed_tasks)}个")
        print("---")
        print("⏰ 未完成任务（按到期时间排序）")

    # 显示已完成任务（简化格式）
    if completed_tasks:
        display_completed = completed_tasks if show_all else completed_tasks[:3]
        hidden_count = len(completed_tasks) - len(display_completed) if not show_all else 0

        # 按完成时间排序
        display_completed.sort(key=lambda x: x.get("completedAt") or 0, reverse=True)

        print(f"\n**✅ 已完成（共{len(completed_tasks)}个）**")
        for task in display_completed:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
            tags_str = f" 🏷️ [{', '.join(task.get('tags', []))}]" if task.get("tags") else ""
            print(f"- [x] {priority_icon} {task['title']} [{task['id']}]{tags_str}")

        if hidden_count > 0:
            print(f"  ... 还有 {hidden_count} 个已完成任务（使用 -a 查看全部）")
        print("---")

    # 显示未完成任务（新格式：按日期分组，带分割线）
    if pending_tasks:
        # 按到期时间排序（无到期时间的排最后）
        priority_order = {"high": 0, "medium": 1, "low": 2}
        pending_tasks.sort(key=lambda x: (
            x.get("dueAt") is None,  # 无到期时间的排最后
            x.get("dueAt") or float('inf'),
            priority_order.get(x.get("priority", "medium"), 1)
        ))

        # 按日期分组
        from collections import defaultdict
        tasks_by_date = defaultdict(list)
        no_due_tasks = []
        
        for task in pending_tasks:
            if task.get("dueAt"):
                due_date = datetime.fromtimestamp(task["dueAt"]).date()
                tasks_by_date[due_date].append(task)
            else:
                no_due_tasks.append(task)

        # 按日期顺序显示
        dates = sorted(tasks_by_date.keys())
        for i, date in enumerate(dates):
            date_tasks = tasks_by_date[date]
            first_task_time = datetime.fromtimestamp(date_tasks[0]["dueAt"])
            
            # 打印日期标题
            print(format_date_header(first_task_time, now))
            
            # 按时间分组
            tasks_by_time = defaultdict(list)
            for task in date_tasks:
                time_str = datetime.fromtimestamp(task["dueAt"]).strftime("%H:%M")
                tasks_by_time[time_str].append(task)
            
            # 按时间顺序显示
            for time_str in sorted(tasks_by_time.keys()):
                time_tasks = tasks_by_time[time_str]
                if len(time_tasks) > 1:
                    print(f"{time_str} 到期（共{len(time_tasks)}个任务）")
                else:
                    print(f"{time_str} 到期")
                
                for task in time_tasks:
                    priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                    tags_str = f" 🏷️ [{', '.join(task.get('tags', []))}]" if task.get("tags") else ""
                    print(f"- [ ] {priority_icon} {task['title']} [{task['id']}]{tags_str}")
            
            # 添加分割线（最后一个日期除外，除非后面还有无到期时间的任务）
            if i < len(dates) - 1 or no_due_tasks:
                print("---")

        # 显示无到期时间的任务（按优先级分组）
        if no_due_tasks:
            print("**📍 无明确截止时间**")
            
            # 按优先级分组
            high_tasks = [t for t in no_due_tasks if t.get("priority") == "high"]
            medium_tasks = [t for t in no_due_tasks if t.get("priority") == "medium"]
            low_tasks = [t for t in no_due_tasks if t.get("priority") == "low"]
            
            if high_tasks:
                print("🔴 **高优先级：**")
                for task in high_tasks:
                    tags_str = f" 🏷️ [{', '.join(task.get('tags', []))}]" if task.get("tags") else ""
                    print(f"- [ ] 🔴 {task['title']} [{task['id']}]{tags_str}")
            
            if medium_tasks:
                print("🟡 **中优先级：**")
                for task in medium_tasks:
                    tags_str = f" 🏷️ [{', '.join(task.get('tags', []))}]" if task.get("tags") else ""
                    print(f"- [ ] 🟡 {task['title']} [{task['id']}]{tags_str}")
            
            if low_tasks:
                print("🟢 **低优先级：**")
                for task in low_tasks:
                    tags_str = f" 🏷️ [{', '.join(task.get('tags', []))}]" if task.get("tags") else ""
                    print(f"- [ ] 🟢 {task['title']} [{task['id']}]{tags_str}")
        
        # 紧急提醒
        today = now.date()
        today_tasks = tasks_by_date.get(today, [])
        if today_tasks:
            # 找最近的到期时间
            earliest_time = min(datetime.fromtimestamp(t["dueAt"]) for t in today_tasks)
            time_left = earliest_time - now
            hours_left = time_left.total_seconds() / 3600
            
            if hours_left > 0 and hours_left <= 12:
                print()
                print("---")
                print("**⚠️ 紧急提醒**")
                if hours_left < 1:
                    minutes_left = int(time_left.total_seconds() / 60)
                    print(f"距离今天 {earliest_time.strftime('%H:%M')} 还剩约 **{minutes_left}分钟**，有 **{len(today_tasks)}个任务** 需要完成！")
                else:
                    print(f"距离今天 {earliest_time.strftime('%H:%M')} 还剩约 **{int(hours_left)}小时**，有 **{len(today_tasks)}个任务** 需要完成！")
                print("｡٩(ˊωˋ*)و✧ 加油哥哥！")

def list_tags():
    """列出所有标签"""
    tags = get_all_tags()
    data = load_data()
    projects = data.get("projects", {})
    
    if not tags:
        print("📭 还没有任何标签")
        return
    
    print("🏷️  所有标签：")
    print("-" * 40)
    
    for tag in tags:
        # 统计该标签下的任务数量
        task_count = len([t for t in load_tasks() if "tags" in t and tag in t["tags"]])
        is_project = tag in projects
        project_marker = " 📦[项目]" if is_project else ""
        print(f"  • {tag}{project_marker} ({task_count}个任务)")

def create_project(tag: str, name: str, description: str = ""):
    """创建项目"""
    data = load_data()
    projects = data.get("projects", {})
    
    if tag in projects:
        print(f"❌ 标签 '{tag}' 已经是项目了")
        return
    
    # 创建项目
    projects[tag] = {
        "name": name,
        "tag": tag,
        "description": description,
        "createdAt": datetime.now().timestamp()
    }
    data["projects"] = projects
    
    # 更新所有包含该标签的任务
    tasks = data.get("tasks", [])
    for task in tasks:
        if "tags" in task and tag in task["tags"]:
            task["projectName"] = name
    
    save_data(data)
    print(f"✅ 已创建项目：{name}")
    print(f"   标签：{tag}")
    if description:
        print(f"   描述：{description}")

def list_projects():
    """列出所有项目"""
    data = load_data()
    projects = data.get("projects", {})
    tasks = data.get("tasks", [])
    
    if not projects:
        print("📭 还没有任何项目")
        return
    
    print("📦 所有项目：")
    print("-" * 60)
    
    for tag, project in projects.items():
        # 统计该项目下的任务
        project_tasks = [t for t in tasks if "tags" in t and tag in t["tags"]]
        completed_count = len([t for t in project_tasks if t["status"] == "completed"])
        total_count = len(project_tasks)
        progress = (completed_count / total_count * 100) if total_count > 0 else 0
        
        print(f"  📦 {project['name']}")
        print(f"     标签：{tag}")
        print(f"     进度：{completed_count}/{total_count} ({progress:.1f}%)")
        if project.get("description"):
            print(f"     描述：{project['description']}")
        print()

def show_project(tag: str):
    """显示项目详情"""
    data = load_data()
    projects = data.get("projects", {})
    
    if tag not in projects:
        print(f"❌ 项目标签 '{tag}' 不存在")
        return
    
    project = projects[tag]
    list_tasks(status="all", show_all=True, tag=tag)

def remove_task_from_time_bucket(task_id: str, due_at: float):
    """从时间桶中移除任务，并更新或删除对应的 cron 提醒
    
    Args:
        task_id: 要移除的任务ID
        due_at: 任务的截止时间戳
    """
    if not due_at:
        return  # 没有截止时间，不需要处理时间桶
    
    # 计算时间桶名称
    time_bucket = get_time_bucket(due_at, minutes=15)
    reminder_name = f"todo-merged-{time_bucket.replace(' ', '-').replace(':', '')}"
    
    reminders_data = load_reminders()
    reminders = reminders_data.get("reminders", {})
    
    if reminder_name not in reminders:
        return  # 时间桶不存在
    
    reminder = reminders[reminder_name]
    task_ids = reminder.get("task_ids", [])
    
    # 从时间桶中移除该任务
    if task_id not in task_ids:
        return  # 任务不在这个时间桶中
    
    task_ids.remove(task_id)
    
    if len(task_ids) == 0:
        # 时间桶变空，删除整个时间桶的所有 cron 任务
        for job_id in reminder.get("job_ids", []):
            try:
                subprocess.run(["openclaw", "cron", "rm", job_id], capture_output=True)
            except:
                pass
        del reminders[reminder_name]
        save_reminders({"reminders": reminders})
        print(f"   🗑️  已删除空的时间桶提醒：{time_bucket}")
    else:
        # 时间桶还有其他任务，需要重建提醒（不包含当前任务）
        # 先删除旧的 cron 任务
        for job_id in reminder.get("job_ids", []):
            try:
                subprocess.run(["openclaw", "cron", "rm", job_id], capture_output=True)
            except:
                pass
        
        # 获取剩余任务
        tasks = load_tasks()
        remaining_tasks = []
        for tid in task_ids:
            for t in tasks:
                if t["id"] == tid and t["status"] == "pending":
                    remaining_tasks.append(t)
                    break
        
        if remaining_tasks:
            # 重建提醒消息
            message_lines = ["⏰ 待办提醒 - 以下任务即将到期：\n"]
            priority_order = {"high": 0, "medium": 1, "low": 2}
            remaining_tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), t.get("dueAt", 0)))
            
            for task in remaining_tasks:
                task_due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
                priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "⚪")
                message_lines.append(f"{priority_emoji} [{task['id']}] {task['title']}")
                message_lines.append(f"   到期：{task_due_str}\n")
            
            reminder_message = "\n".join(message_lines)
            
            # 计算提醒时间
            bucket_dt = datetime.strptime(time_bucket, "%Y-%m-%d %H:%M")
            now = datetime.now()
            reminder_times = []
            
            reminder_30 = bucket_dt - timedelta(minutes=30)
            if reminder_30 > now:
                reminder_times.append(("30min", reminder_30))
            
            reminder_15 = bucket_dt - timedelta(minutes=15)
            if reminder_15 > now:
                reminder_times.append(("15min", reminder_15))
            
            if bucket_dt > now:
                reminder_times.append(("ontime", bucket_dt))
            
            # 创建新的 cron 任务
            new_job_ids = []
            session = load_session_context()
            channel = session.get("channel") if session else None
            target = session.get("target") if session else None
            
            for label, reminder_time in reminder_times:
                cron_time = reminder_time.strftime("%H:%M %Y-%m-%d")
                
                if label == "30min":
                    msg = f"⏰ 待办提醒（30分钟后）：\n\n" + "\n".join(message_lines[1:])
                elif label == "15min":
                    msg = f"⏰ 待办提醒（15分钟后）：\n\n" + "\n".join(message_lines[1:])
                else:
                    msg = reminder_message
                
                full_name = f"{reminder_name}-{label}"
                job_id = create_cron_job(full_name, cron_time, msg, channel, target)
                if job_id:
                    new_job_ids.append(job_id)
            
            # 更新提醒数据
            reminders_data = load_reminders()
            reminders = reminders_data.get("reminders", {})
            if reminder_name in reminders:
                reminders[reminder_name]["job_ids"] = new_job_ids
                reminders[reminder_name]["task_ids"] = task_ids
                save_reminders({"reminders": reminders})
            
            print(f"   🔄 已更新时间桶提醒（剩余 {len(remaining_tasks)} 个任务）")

def mark_done(task_id: str):
    """标记任务为完成"""
    data = load_data()
    tasks = data.get("tasks", [])
    
    for task in tasks:
        if task["id"] == task_id:
            # 先处理时间桶（在修改状态之前）
            due_at = task.get("dueAt")
            if due_at:
                remove_task_from_time_bucket(task_id, due_at)
            
            # 再更新任务状态
            task["status"] = "completed"
            task["completedAt"] = datetime.now().timestamp()
            save_data(data)
            print(f"✅ 已完成任务：[{task_id}] {task['title']}")
            
            # 显示附件信息
            if task.get("attachments"):
                print(f"📎 该任务有 {len(task['attachments'])} 个附件")
                print(f"   附件路径：{ATTACHMENTS_DIR}/{task_id}/")
            return
    
    print(f"❌ 未找到任务 ID：{task_id}")

def delete_task(task_id: str):
    """删除任务"""
    data = load_data()
    tasks = data.get("tasks", [])
    
    # 查找要删除的任务
    target_task = None
    for task in tasks:
        if task["id"] == task_id:
            target_task = task
            break
    
    if not target_task:
        print(f"❌ 未找到任务 ID：{task_id}")
        return
    
    # 先处理时间桶（在删除任务之前）
    due_at = target_task.get("dueAt")
    if due_at:
        remove_task_from_time_bucket(task_id, due_at)
    
    # 删除任务
    tasks = [t for t in tasks if t["id"] != task_id]
    data["tasks"] = tasks
    save_data(data)
    
    # 删除附件文件夹
    task_attach_dir = os.path.join(ATTACHMENTS_DIR, task_id)
    if os.path.exists(task_attach_dir):
        shutil.rmtree(task_attach_dir)
        print(f"   📎 已删除附件文件夹")
    
    print(f"🗑️  已删除任务：[{task_id}] {target_task['title']}")

def show_task(task_id: str):
    """显示任务详情"""
    data = load_data()
    tasks = data.get("tasks", [])
    projects = data.get("projects", {})
    
    for task in tasks:
        if task["id"] == task_id:
            print(f"📌 任务详情 [{task_id}]")
            print("-" * 50)
            print(f"标题：{task['title']}")
            print(f"描述：{task['description'] or '无'}")
            print(f"优先级：{task['priority']}")
            print(f"状态：{'已完成' if task['status'] == 'completed' else '待处理'}")
            
            if task.get("tags"):
                tags_str = ", ".join(task["tags"])
                print(f"标签：{tags_str}")
            
            if task.get("projectName"):
                print(f"所属项目：{task['projectName']}")
            
            print(f"创建时间：{datetime.fromtimestamp(task['createdAt']).strftime('%Y-%m-%d %H:%M')}")
            
            if task["dueAt"]:
                print(f"到期时间：{datetime.fromtimestamp(task['dueAt']).strftime('%Y-%m-%d %H:%M')}")
            
            if task["completedAt"]:
                print(f"完成时间：{datetime.fromtimestamp(task['completedAt']).strftime('%Y-%m-%d %H:%M')}")
            
            # 显示附件
            if task.get("attachments"):
                print(f"\n📎 附件（{len(task['attachments'])}个）：")
                for att in task["attachments"]:
                    full_path = os.path.join(ATTACHMENTS_DIR, att["path"])
                    print(f"   • {att['name']}")
                    print(f"     路径：{full_path}")
            
            return
    
    print(f"❌ 未找到任务 ID：{task_id}")

def delete_reminder_for_bucket(reminder_name: str):
    """删除指定时间桶的所有 cron 提醒"""
    reminders_data = load_reminders()
    reminders = reminders_data.get("reminders", {})
    
    if reminder_name not in reminders:
        return False
    
    # 删除所有关联的 cron 任务
    for job_id in reminders[reminder_name].get("job_ids", []):
        try:
            subprocess.run(f"openclaw cron delete {job_id}", shell=True, capture_output=True)
        except:
            pass
    
    # 从提醒数据中删除
    del reminders[reminder_name]
    save_reminders({"reminders": reminders})
    return True

def update_task_due(task_id: str, new_due: str):
    """更新任务的截止时间
    
    步骤：
    1. 删除原有 openclaw 对应的时间桶
    2. 根据时间数据内容重建一个没有该任务的对应时间桶
    3. 更改该任务在本地的时间桶内容
    4. 检验是否新的时间已经有时间桶
    5. 如果有的话，则删除原有并创建一个新的包含新任务的时间桶
    6. 如果没有，创建一个新的 openclaw 任务
    """
    data = load_data()
    tasks = data.get("tasks", [])
    
    # 查找任务
    target_task = None
    for task in tasks:
        if task["id"] == task_id:
            target_task = task
            break
    
    if not target_task:
        print(f"❌ 未找到任务 ID：{task_id}")
        return
    
    if target_task["status"] == "completed":
        print(f"❌ 任务 [{task_id}] 已完成，无法修改截止时间")
        return
    
    # 解析新的截止时间
    try:
        new_due_at = datetime.strptime(new_due, "%Y-%m-%d %H:%M").timestamp()
    except ValueError:
        try:
            new_due_at = datetime.strptime(new_due, "%Y-%m-%d").timestamp()
        except ValueError:
            print("❌ 时间格式错误，请使用 YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
            return
    
    old_due_at = target_task.get("dueAt")
    
    # 如果原来没有截止时间
    if not old_due_at:
        # 直接更新任务的截止时间
        target_task["dueAt"] = new_due_at
        save_data(data)
        
        # 创建新的提醒
        reminder_info = create_or_update_merged_reminder(
            task_id, new_due_at, target_task.get("priority", "medium"), target_task["title"]
        )
        
        new_due_str = datetime.fromtimestamp(new_due_at).strftime("%Y-%m-%d %H:%M")
        print(f"✅ 已为任务 [{task_id}] {target_task['title']} 设置截止时间：{new_due_str}")
        if reminder_info:
            print(f"   🕒 已创建提醒")
        return
    
    # 计算旧时间桶和新时间桶
    old_time_bucket = get_time_bucket(old_due_at, minutes=15)
    new_time_bucket = get_time_bucket(new_due_at, minutes=15)
    
    old_bucket_dt = datetime.strptime(old_time_bucket, "%Y-%m-%d %H:%M")
    new_bucket_dt = datetime.strptime(new_time_bucket, "%Y-%m-%d %H:%M")
    
    old_reminder_name = f"todo-merged-{old_time_bucket.replace(' ', '-').replace(':', '')}"
    new_reminder_name = f"todo-merged-{new_time_bucket.replace(' ', '-').replace(':', '')}"
    
    reminders_data = load_reminders()
    reminders = reminders_data.get("reminders", {})
    
    # 步骤 1-2: 处理旧时间桶
    if old_reminder_name in reminders:
        old_reminder = reminders[old_reminder_name]
        old_task_ids = old_reminder.get("task_ids", [])
        
        # 从旧时间桶中移除该任务
        if task_id in old_task_ids:
            old_task_ids.remove(task_id)
            old_reminder["task_ids"] = old_task_ids
        
        if len(old_task_ids) == 0:
            # 没有其他任务了，删除整个时间桶
            delete_reminder_for_bucket(old_reminder_name)
            print(f"   🗑️  已删除空的时间桶：{old_time_bucket}")
        else:
            # 还有其他任务，需要重建该时间桶的提醒（不包含当前任务）
            # 先删除旧的 cron
            for job_id in old_reminder.get("job_ids", []):
                try:
                    subprocess.run(f"openclaw cron delete {job_id}", shell=True, capture_output=True)
                except:
                    pass
            old_reminder["job_ids"] = []
            
            # 重新加载提醒数据（可能已被 delete_reminder_for_bucket 修改）
            reminders_data = load_reminders()
            reminders = reminders_data.get("reminders", {})
            
            # 如果旧时间桶还存在，重建提醒
            if old_reminder_name in reminders:
                # 获取剩余任务的信息
                remaining_tasks = []
                for tid in old_task_ids:
                    for t in tasks:
                        if t["id"] == tid and t["status"] == "pending":
                            remaining_tasks.append(t)
                            break
                
                if remaining_tasks:
                    # 重建提醒消息
                    message_lines = ["⏰ 待办提醒 - 以下任务即将到期：\n"]
                    priority_order = {"high": 0, "medium": 1, "low": 2}
                    remaining_tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), t.get("dueAt", 0)))
                    
                    for task in remaining_tasks:
                        task_due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
                        priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "⚪")
                        message_lines.append(f"{priority_emoji} [{task['id']}] {task['title']}")
                        message_lines.append(f"   到期：{task_due_str}\n")
                    
                    reminder_message = "\n".join(message_lines)
                    
                    # 计算提醒时间
                    now = datetime.now()
                    bucket_timestamp = old_bucket_dt.timestamp()
                    reminder_times = []
                    
                    reminder_30 = old_bucket_dt - timedelta(minutes=30)
                    if reminder_30 > now:
                        reminder_times.append(("30min", reminder_30))
                    
                    reminder_15 = old_bucket_dt - timedelta(minutes=15)
                    if reminder_15 > now:
                        reminder_times.append(("15min", reminder_15))
                    
                    if old_bucket_dt > now:
                        reminder_times.append(("ontime", old_bucket_dt))
                    
                    # 创建新的 cron 任务
                    new_job_ids = []
                    for label, reminder_time in reminder_times:
                        cron_time = reminder_time.strftime("%H:%M %Y-%m-%d")
                        
                        if label == "30min":
                            msg = f"⏰ 待办提醒（30分钟后）：\n\n" + "\n".join(message_lines[1:])
                        elif label == "15min":
                            msg = f"⏰ 待办提醒（15分钟后）：\n\n" + "\n".join(message_lines[1:])
                        else:
                            msg = reminder_message
                        
                        full_name = f"{old_reminder_name}-{label}"
                        job_id = create_cron_job(full_name, cron_time, msg)
                        if job_id:
                            new_job_ids.append(job_id)
                    
                    # 更新提醒数据
                    reminders_data = load_reminders()
                    reminders = reminders_data.get("reminders", {})
                    if old_reminder_name in reminders:
                        reminders[old_reminder_name]["job_ids"] = new_job_ids
                        save_reminders({"reminders": reminders})
                    
                    print(f"   🔄 已重建时间桶 {old_time_bucket}（剩余 {len(remaining_tasks)} 个任务）")
    
    # 步骤 3: 更新任务的截止时间
    target_task["dueAt"] = new_due_at
    save_data(data)
    
    # 步骤 4-6: 处理新时间桶
    # 重新加载提醒数据
    reminders_data = load_reminders()
    reminders = reminders_data.get("reminders", {})
    
    if new_reminder_name in reminders:
        # 新时间桶已存在，需要更新它
        new_reminder = reminders[new_reminder_name]
        
        # 添加当前任务到新时间桶（如果还没有）
        if task_id not in new_reminder.get("task_ids", []):
            new_reminder["task_ids"].append(task_id)
        
        # 删除旧的 cron 任务
        for job_id in new_reminder.get("job_ids", []):
            try:
                subprocess.run(f"openclaw cron delete {job_id}", shell=True, capture_output=True)
            except:
                pass
        
        # 获取新时间桶中的所有任务
        new_bucket_tasks = []
        for tid in new_reminder.get("task_ids", []):
            for t in tasks:
                if t["id"] == tid and t["status"] == "pending":
                    new_bucket_tasks.append(t)
                    break
        
        # 重建提醒消息
        message_lines = ["⏰ 待办提醒 - 以下任务即将到期：\n"]
        priority_order = {"high": 0, "medium": 1, "low": 2}
        new_bucket_tasks.sort(key=lambda t: (priority_order.get(t.get("priority", "medium"), 1), t.get("dueAt", 0)))
        
        for task in new_bucket_tasks:
            task_due_str = datetime.fromtimestamp(task["dueAt"]).strftime("%Y-%m-%d %H:%M")
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "⚪")
            message_lines.append(f"{priority_emoji} [{task['id']}] {task['title']}")
            message_lines.append(f"   到期：{task_due_str}\n")
        
        reminder_message = "\n".join(message_lines)
        
        # 计算提醒时间
        now = datetime.now()
        reminder_times = []
        
        reminder_30 = new_bucket_dt - timedelta(minutes=30)
        if reminder_30 > now:
            reminder_times.append(("30min", reminder_30))
        
        reminder_15 = new_bucket_dt - timedelta(minutes=15)
        if reminder_15 > now:
            reminder_times.append(("15min", reminder_15))
        
        if new_bucket_dt > now:
            reminder_times.append(("ontime", new_bucket_dt))
        
        # 创建新的 cron 任务
        new_job_ids = []
        for label, reminder_time in reminder_times:
            cron_time = reminder_time.strftime("%H:%M %Y-%m-%d")
            
            if label == "30min":
                msg = f"⏰ 待办提醒（30分钟后）：\n\n" + "\n".join(message_lines[1:])
            elif label == "15min":
                msg = f"⏰ 待办提醒（15分钟后）：\n\n" + "\n".join(message_lines[1:])
            else:
                msg = reminder_message
            
            full_name = f"{new_reminder_name}-{label}"
            job_id = create_cron_job(full_name, cron_time, msg)
            if job_id:
                new_job_ids.append(job_id)
        
        # 更新提醒数据
        reminders_data = load_reminders()
        reminders = reminders_data.get("reminders", {})
        if new_reminder_name in reminders:
            reminders[new_reminder_name]["job_ids"] = new_job_ids
            reminders[new_reminder_name]["task_ids"] = [t["id"] for t in new_bucket_tasks]
            save_reminders({"reminders": reminders})
        
        print(f"   🔄 已更新新时间桶 {new_time_bucket}（共 {len(new_bucket_tasks)} 个任务）")
    else:
        # 新时间桶不存在，创建新的
        reminder_info = create_or_update_merged_reminder(
            task_id, new_due_at, target_task.get("priority", "medium"), target_task["title"]
        )
        print(f"   🕒 已创建新时间桶 {new_time_bucket}")
    
    # 输出结果
    old_due_str = datetime.fromtimestamp(old_due_at).strftime("%Y-%m-%d %H:%M") if old_due_at else "无"
    new_due_str = datetime.fromtimestamp(new_due_at).strftime("%Y-%m-%d %H:%M")
    print(f"✅ 已更新任务 [{task_id}] {target_task['title']}")
    print(f"   原截止时间：{old_due_str}")
    print(f"   新截止时间：{new_due_str}")

def add_tag_to_task(task_id: str, tags: List[str]):
    """为任务添加标签"""
    data = load_data()
    tasks = data.get("tasks", [])
    
    for task in tasks:
        if task["id"] == task_id:
            existing_tags = set(task.get("tags", []))
            new_tags = []
            
            for tag in tags:
                if tag not in existing_tags:
                    existing_tags.add(tag)
                    new_tags.append(tag)
            
            task["tags"] = list(existing_tags)
            
            # 检查标签是否属于某个项目
            projects = data.get("projects", {})
            for tag in task["tags"]:
                if tag in projects:
                    task["projectName"] = projects[tag]["name"]
                    break
            
            # 更新全局标签列表
            all_tags = set(data.get("tags", []))
            all_tags.update(existing_tags)
            data["tags"] = sorted(list(all_tags))
            
            save_data(data)
            
            if new_tags:
                print(f"✅ 已为任务 [{task_id}] {task['title']} 添加标签：{', '.join(new_tags)}")
            else:
                print(f"ℹ️  任务 [{task_id}] 已包含这些标签")
            print(f"   当前标签：{', '.join(sorted(task['tags']))}")
            return
    
    print(f"❌ 未找到任务 ID：{task_id}")

def check_due_tasks():
    """检查即将到期的任务"""
    tasks = load_tasks()
    now = datetime.now()
    pending_tasks = [t for t in tasks if t["status"] == "pending" and t["dueAt"]]
    
    due_soon = []
    for task in pending_tasks:
        due_time = datetime.fromtimestamp(task["dueAt"])
        if now < due_time <= now + timedelta(hours=1):
            due_soon.append((task, "1小时内到期"))
        elif due_time <= now:
            due_soon.append((task, "已逾期"))
        elif task["priority"] == "high" and now < due_time <= now + timedelta(hours=2):
            due_soon.append((task, "2小时内到期（高优先级）"))
    
    return due_soon

def format_time_remaining(due_at: float, now: datetime) -> str:
    """格式化剩余时间显示"""
    due_time = datetime.fromtimestamp(due_at)
    time_left = due_time - now
    
    if time_left.total_seconds() <= 0:
        return "已逾期"
    
    hours = time_left.total_seconds() / 3600
    
    if hours < 1:
        minutes = int(time_left.total_seconds() / 60)
        return f"约{minutes}分钟"
    elif hours < 24:
        return f"约{int(hours)}小时"
    else:
        days = int(hours / 24)
        remaining_hours = int(hours % 24)
        if remaining_hours > 0:
            return f"{days}天{remaining_hours}小时"
        return f"{days}天"

def format_due_time_short(due_at: float, now: datetime) -> str:
    """格式化截止时间（短格式）"""
    due_time = datetime.fromtimestamp(due_at)
    today = now.date()
    target_date = due_time.date()
    delta = (target_date - today).days
    
    time_str = due_time.strftime("%H:%M")
    
    if delta == 0:
        return f"{time_str} ({format_time_remaining(due_at, now)})"
    elif delta == 1:
        return f"明天 {time_str}"
    elif delta == 2:
        return f"后天 {time_str}"
    else:
        return due_time.strftime("%m-%d %H:%M")

def save_session_context(channel: str, target: str):
    """保存当前会话配置"""
    config = {
        "channel": channel,
        "target": target,
        "updated_at": datetime.now().isoformat()
    }
    os.makedirs(os.path.dirname(SESSION_CONFIG_FILE), exist_ok=True)
    with open(SESSION_CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def load_session_context() -> Optional[Dict]:
    """加载当前会话配置
    
    返回：
        如果配置文件存在且有效，返回 {"channel": "xxx", "target": "xxx"}
        否则返回 None
    """
    if not os.path.exists(SESSION_CONFIG_FILE):
        return None
    try:
        with open(SESSION_CONFIG_FILE, 'r') as f:
            config = json.load(f)
            # 验证配置是否有效
            if config.get("channel") and config.get("target"):
                return config
            return None
    except:
        return None

def send_message_direct(channel: str, target: str, message: str) -> bool:
    """直接发送消息到指定频道"""
    try:
        cmd = [
            "openclaw", "message", "send",
            "--channel", channel,
            "--target", target,
            "--message", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"❌ 发送失败: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 发送消息失败: {str(e)}")
        return False

def cmd_send_status(channel: str = None, target: str = None):
    """发送状态页到当前会话"""
    # 获取会话信息（参数优先，否则从配置文件读取）
    if channel and target:
        save_session_context(channel, target)
    else:
        session = load_session_context()
        if not session:
            print("❌ 错误：缺少会话配置")
            print("   请提供 --channel 和 --target 参数")
            print("   示例：todo send-status --channel feishu --target user:ou_xxx")
            return
        channel = session.get("channel")
        target = session.get("target")
    
    # 生成状态页内容（复用现有的 show_status 函数）
    import io
    import sys
    from contextlib import redirect_stdout
    
    # 捕获 show_status 的输出
    output = io.StringIO()
    with redirect_stdout(output):
        show_status()
    
    message = output.getvalue()
    
    # 发送消息
    if send_message_direct(channel, target, message):
        print(f"✅ 状态页已发送到 {channel}:{target}")
        print("NO_REPLY")  # 告诉 AI 不需要回复
    else:
        print("❌ 状态页发送失败")

def cmd_send_list(channel: str = None, target: str = None, status: str = "pending", 
                  priority: str = None, tag: str = None, show_all: bool = False):
    """发送待办列表到当前会话"""
    # 获取会话信息
    if channel and target:
        save_session_context(channel, target)
    else:
        session = load_session_context()
        if not session:
            print("❌ 错误：缺少会话配置")
            print("   请提供 --channel 和 --target 参数")
            print("   示例：todo send-list --channel feishu --target user:ou_xxx")
            return
        channel = session.get("channel")
        target = session.get("target")
    
    # 生成列表内容
    import io
    from contextlib import redirect_stdout
    
    output = io.StringIO()
    with redirect_stdout(output):
        list_tasks(status=status, priority=priority, tag=tag, show_all=show_all)
    
    message = output.getvalue()
    
    # 发送消息
    if send_message_direct(channel, target, message):
        print(f"✅ 待办列表已发送到 {channel}:{target}")
        print("NO_REPLY")
    else:
        print("❌ 待办列表发送失败")

def show_status():
    """显示状态页（Markdown格式）"""
    data = load_data()
    tasks = data.get("tasks", [])
    projects = data.get("projects", {})
    all_tags = get_all_tags()
    now = datetime.now()

    # 分离已完成和未完成任务
    completed_tasks = [t for t in tasks if t["status"] == "completed"]
    pending_tasks = [t for t in tasks if t["status"] == "pending"]

    # 有截止时间的未完成任务（按时间排序）
    pending_with_due = [t for t in pending_tasks if t.get("dueAt")]
    pending_with_due.sort(key=lambda x: x.get("dueAt", float('inf')))

    print("📊 **Todo 状态概览**")
    print("---")

    # 1. 全局最近截止时间
    if pending_with_due:
        earliest = pending_with_due[0]
        due_time = datetime.fromtimestamp(earliest["dueAt"])
        time_str = due_time.strftime("%Y-%m-%d %H:%M")
        remaining = format_time_remaining(earliest["dueAt"], now)
        print(f"\n⏰ **全局最近截止**：{time_str} ({remaining})")
    else:
        print(f"\n⏰ **全局最近截止**：无截止任务")

    # 2. 项目进度
    print(f"\n📦 **项目进度**")
    print("--------------------------------------------------")

    # 过滤已完成的项目（进度100%）
    active_projects = []
    for tag, project in projects.items():
        project_tasks = [t for t in tasks if "tags" in t and tag in t["tags"]]
        completed_count = len([t for t in project_tasks if t["status"] == "completed"])
        total_count = len(project_tasks)
        progress = (completed_count / total_count * 100) if total_count > 0 else 0

        # 只显示未完成的项目
        if progress < 100:
            active_projects.append({
                "tag": tag,
                "name": project["name"],
                "completed": completed_count,
                "total": total_count,
                "progress": progress,
                "tasks": project_tasks
            })

    if active_projects:
        for project in active_projects:
            # 项目下最近的未完成任务（有截止时间）
            project_pending = [t for t in project["tasks"] if t["status"] == "pending" and t.get("dueAt")]
            project_pending.sort(key=lambda x: x.get("dueAt", float('inf')))

            # 项目最近截止时间
            if project_pending:
                earliest = project_pending[0]
                due_short = format_due_time_short(earliest["dueAt"], now)
                deadline_str = f" | ⏰ {due_short}"
            else:
                deadline_str = " | 无截止"

            print(f"- {project['name']} [{project['tag']}] {project['completed']}/{project['total']} ({project['progress']:.1f}%){deadline_str}")

            # 显示最近2-3个任务
            recent_tasks = project_pending[:3] if project_pending else [t for t in project["tasks"] if t["status"] == "pending"][:3]
            if recent_tasks:
                task_titles = [t["title"][:15] + "..." if len(t["title"]) > 15 else t["title"] for t in recent_tasks]
                print(f"  - 最近任务：{'、'.join(task_titles)}")
    else:
        print("- 暂无进行中的项目")

    # 3. 待办概览
    print(f"\n📋 **待办概览**")
    print("--------------------------------------------------")
    print(f"- ✅ 已完成：{len(completed_tasks)} 个")
    print(f"- ⏳ 未完成：{len(pending_tasks)} 个")

    if pending_with_due:
        print(f"\n⏰ **最近待办：**")
        for task in pending_with_due[:3]:
            priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get("priority", "medium"), "⚪")
            time_short = datetime.fromtimestamp(task["dueAt"]).strftime("%H:%M")
            title_short = task["title"][:20] + "..." if len(task["title"]) > 20 else task["title"]
            print(f"   - {priority_icon} {title_short} ({time_short})")

    # 4. 标签统计
    print(f"\n🏷️ **标签统计**")
    print("--------------------------------------------------")

    tag_stats = []
    for tag in all_tags:
        tag_tasks = [t for t in tasks if "tags" in t and tag in t["tags"]]
        total = len(tag_tasks)
        pending = len([t for t in tag_tasks if t["status"] == "pending"])
        tag_stats.append({
            "tag": tag,
            "pending": pending,
            "total": total,
            "is_project": tag in projects
        })

    # 按未完成数量排序
    tag_stats.sort(key=lambda x: (-x["pending"], -x["total"]))

    # 显示标签（每行3个）
    for i in range(0, len(tag_stats), 3):
        batch = tag_stats[i:i+3]
        line_parts = []
        for stat in batch:
            marker = "📦" if stat["is_project"] else "  "
            line_parts.append(f"{marker}{stat['tag']}: {stat['pending']}/{stat['total']}")
        print("- " + "  |  ".join(line_parts))

    print("\n---")

def main():
    parser = argparse.ArgumentParser(description="待办事项管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # 添加任务
    add_parser = subparsers.add_parser("add", help="添加新待办")
    add_parser.add_argument("title", help="任务标题")
    add_parser.add_argument("--description", "-d", default="", help="任务描述")
    add_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], default="medium", help="优先级")
    add_parser.add_argument("--due", help="到期时间，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
    add_parser.add_argument("--tags", "-t", help="标签，多个标签用逗号分隔，如：学习,RAG")
    add_parser.add_argument("--attach", "-a", help="附件文件路径")
    
    # 列出任务
    list_parser = subparsers.add_parser("list", help="列出待办")
    list_parser.add_argument("--status", "-s", choices=["all", "pending", "completed"], default="pending", help="状态过滤")
    list_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], help="优先级过滤")
    list_parser.add_argument("--all", "-a", action="store_true", help="显示全部已完成任务")
    list_parser.add_argument("--tag", "-t", help="按标签筛选任务")
    
    # 标签管理
    tags_parser = subparsers.add_parser("tags", help="列出所有标签")
    
    # 项目管理
    project_parser = subparsers.add_parser("project", help="项目管理")
    project_subparsers = project_parser.add_subparsers(dest="project_command", required=True)
    
    # 创建项目
    project_create = project_subparsers.add_parser("create", help="创建项目")
    project_create.add_argument("tag", help="项目标签")
    project_create.add_argument("name", help="项目名称")
    project_create.add_argument("--description", "-d", default="", help="项目描述")
    
    # 列出项目
    project_subparsers.add_parser("list", help="列出所有项目")
    
    # 显示项目详情
    project_show = project_subparsers.add_parser("show", help="显示项目详情")
    project_show.add_argument("tag", help="项目标签")
    
    # 添加附件
    attach_parser = subparsers.add_parser("attach", help="为任务添加附件")
    attach_parser.add_argument("task_id", help="任务ID")
    attach_parser.add_argument("file_path", help="文件路径")
    
    # 标记完成
    done_parser = subparsers.add_parser("done", help="标记任务完成")
    done_parser.add_argument("task_id", help="任务ID")
    
    # 删除任务
    delete_parser = subparsers.add_parser("delete", help="删除任务")
    delete_parser.add_argument("task_id", help="任务ID")
    
    # 显示详情
    show_parser = subparsers.add_parser("show", help="显示任务详情")
    show_parser.add_argument("task_id", help="任务ID")
    
    # 添加标签
    addtag_parser = subparsers.add_parser("add-tag", help="为任务添加标签")
    addtag_parser.add_argument("task_id", help="任务ID")
    addtag_parser.add_argument("tags", help="标签，多个标签用逗号分隔")
    
    # 更新截止时间
    updatedue_parser = subparsers.add_parser("update-due", help="更新任务的截止时间")
    updatedue_parser.add_argument("task_id", help="任务ID")
    updatedue_parser.add_argument("new_due", help="新的截止时间，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
    
    # 检查到期任务
    subparsers.add_parser("check-due", help="检查即将到期的任务")
    
    # 状态页
    subparsers.add_parser("status", help="显示状态概览页")
    
    # 发送状态页到当前会话
    send_status_parser = subparsers.add_parser("send-status", help="发送状态页到当前会话")
    send_status_parser.add_argument("--channel", help="频道名称 (如: feishu)")
    send_status_parser.add_argument("--target", help="目标ID (如: user:ou_xxx)")
    
    # 发送待办列表到当前会话
    send_list_parser = subparsers.add_parser("send-list", help="发送待办列表到当前会话")
    send_list_parser.add_argument("--channel", help="频道名称")
    send_list_parser.add_argument("--target", help="目标ID")
    send_list_parser.add_argument("--status", "-s", choices=["all", "pending", "completed"], default="pending", help="状态过滤")
    send_list_parser.add_argument("--priority", "-p", choices=["high", "medium", "low"], help="优先级过滤")
    send_list_parser.add_argument("--tag", "-t", help="按标签筛选任务")
    send_list_parser.add_argument("--all", "-a", action="store_true", help="显示全部已完成任务")
    
    args = parser.parse_args()
    
    if args.command == "add":
        tags_list = []
        if args.tags:
            tags_list = [t.strip() for t in args.tags.split(",")]
        add_task(args.title, args.description, args.priority, args.due, tags_list, args.attach)
    elif args.command == "list":
        list_tasks(args.status, args.priority, args.all, args.tag)
    elif args.command == "tags":
        list_tags()
    elif args.command == "project":
        if args.project_command == "create":
            create_project(args.tag, args.name, args.description)
        elif args.project_command == "list":
            list_projects()
        elif args.project_command == "show":
            show_project(args.tag)
    elif args.command == "attach":
        attach_to_task(args.task_id, args.file_path)
    elif args.command == "done":
        mark_done(args.task_id)
    elif args.command == "delete":
        delete_task(args.task_id)
    elif args.command == "show":
        show_task(args.task_id)
    elif args.command == "add-tag":
        tags_list = [t.strip() for t in args.tags.split(",")]
        add_tag_to_task(args.task_id, tags_list)
    elif args.command == "update-due":
        update_task_due(args.task_id, args.new_due)
    elif args.command == "check-due":
        due_tasks = check_due_tasks()
        if due_tasks:
            print("⚠️  到期提醒：")
            for task, reason in due_tasks:
                print(f"[{task['id']}] {task['title']} - {reason}")
    elif args.command == "status":
        show_status()
    elif args.command == "send-status":
        cmd_send_status(args.channel, args.target)
    elif args.command == "send-list":
        cmd_send_list(args.channel, args.target, args.status, args.priority, args.tag, args.all)

if __name__ == "__main__":
    main()
