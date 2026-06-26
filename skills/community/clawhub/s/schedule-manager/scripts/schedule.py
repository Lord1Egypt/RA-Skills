#!/usr/bin/env python3
"""
日程任务管理脚本
用法：python schedule.py <command> [options]
"""

import argparse
import subprocess
import sys
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

# ==================== 配置 ====================
WORKSPACE = Path.home() / ".openclaw" / "workspace"
TASKS_FILE = WORKSPACE / "daily-tasks.md"
TEMP_TASKS_FILE = WORKSPACE / "calendar" / "temp-tasks.md"
RUN_TASK_SCRIPT = WORKSPACE / "scripts" / "run-task.sh"

# ==================== 工具函数 ====================

def log(level, message):
    """日志输出"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [{level}] {message}")

def ensure_calendar_dir():
    """确保 calendar 目录存在"""
    (WORKSPACE / "calendar").mkdir(parents=True, exist_ok=True)

def read_markdown_table(filepath):
    """读取 Markdown 表格"""
    if not filepath.exists():
        return []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取表格行
    lines = content.split('\n')
    rows = []
    in_table = False
    
    for line in lines:
        if line.strip().startswith('|') and '---' not in line:
            # 解析表格行
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) >= 7:
                rows.append({
                    'time': cells[0],
                    'name': cells[1],
                    'type': cells[2],
                    'content': cells[3],
                    'weekday': cells[4],
                    'notify': cells[5],
                    'status': cells[6]
                })
    
    return rows

def write_markdown_table(filepath, rows, headers=None):
    """写入 Markdown 表格"""
    if headers is None:
        headers = ["时间", "任务名", "类型", "内容/参数", "星期", "通知方式", "状态"]
    
    # 读取文件内容（保留表头和说明）
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到表格开始位置
        table_start = content.find('| 时间 |')
        if table_start == -1:
            table_start = content.find('| 时间|')
        
        if table_start != -1:
            # 找到表格结束位置
            table_end = content.find('\n\n---', table_start)
            if table_end == -1:
                table_end = len(content)
            
            # 构建新表格
            new_table = build_markdown_table(rows, headers)
            content = content[:table_start] + new_table + content[table_end:]
        else:
            # 没有表格，追加到文件末尾
            content += "\n\n" + build_markdown_table(rows, headers)
    else:
        # 创建新文件
        content = "# 每日定时任务\n\n" + build_markdown_table(rows, headers)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def build_markdown_table(rows, headers):
    """构建 Markdown 表格字符串"""
    lines = []
    
    # 表头
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["------"] * len(headers)) + "|")
    
    # 数据行
    for row in rows:
        lines.append("| " + " | ".join([
            row.get('time', ''),
            row.get('name', ''),
            row.get('type', ''),
            row.get('content', ''),
            row.get('weekday', ''),
            row.get('notify', ''),
            row.get('status', '✅')
        ]) + " |")
    
    return '\n'.join(lines) + '\n'

def read_temp_tasks():
    """读取临时任务（YAML 格式）"""
    if not TEMP_TASKS_FILE.exists():
        return []
    
    tasks = []
    current_task = None
    
    with open(TEMP_TASKS_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip()
            if line.startswith('  - id:'):
                if current_task:
                    tasks.append(current_task)
                current_task = {'id': line.split(':', 1)[1].strip().strip('"')}
            elif current_task and line.startswith('    '):
                key, value = line.strip().split(':', 1)
                current_task[key.strip()] = value.strip().strip('"')
        
        if current_task:
            tasks.append(current_task)
    
    return tasks

def write_temp_tasks(tasks):
    """写入临时任务"""
    ensure_calendar_dir()
    
    lines = ["tasks:"]
    for task in tasks:
        lines.append(f'  - id: "{task["id"]}"')
        lines.append(f'    time: "{task["time"]}"')
        lines.append(f'    message: "{task["message"]}"')
        lines.append(f'    notify: "{task.get("notify", "本地播放")}"')
        lines.append(f'    status: "{task.get("status", "pending")}"')
        lines.append(f'    created_at: "{task.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M"))}"')
    
    with open(TEMP_TASKS_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

def generate_task_id():
    """生成临时任务 ID"""
    return f"temp_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def update_crontab(tasks):
    """更新 crontab"""
    lines = [
        "# OpenClaw 定时任务",
        "# 编辑：crontab -e",
        "# 查看：crontab -l",
        "",
        "# 环境变量",
        "SHELL=/bin/bash",
        "PATH=/usr/local/bin:/usr/bin:/bin:/home/wang/.npm-global/bin",
        "",
        "# 每日定时任务"
    ]
    
    for task in tasks:
        if task.get('status') == '✅':
            time_parts = task['time'].split(':')
            hour = time_parts[0]
            minute = time_parts[1]
            
            # 转换星期规格为 cron 格式
            weekday = task.get('weekday', '1-7')
            if weekday == '1-5':
                day_of_week = "1-5"
            elif weekday == '1-7' or weekday == '*':
                day_of_week = "*"
            else:
                day_of_week = weekday
            
            lines.append(f"{minute} {hour} * * {day_of_week}  {RUN_TASK_SCRIPT} \"{task['name']}\"")
    
    # 写入 crontab
    crontab_content = '\n'.join(lines) + '\n'
    
    # 使用 crontab 命令
    try:
        proc = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = proc.communicate(crontab_content.encode())
        if proc.returncode == 0:
            log("INFO", "✓ crontab 已更新")
        else:
            log("ERROR", f"crontab 更新失败：{stderr.decode()}")
    except Exception as e:
        log("ERROR", f"crontab 更新失败：{e}")

# ==================== 命令实现 ====================

def cmd_list(args):
    """列出任务"""
    if args.temp:
        # 列出临时任务
        tasks = read_temp_tasks()
        if not tasks:
            print("暂无临时任务")
            return
        
        print("\n📋 临时任务列表:\n")
        print(f"{'ID':<20} {'时间':<20} {'消息':<30} {'状态'}")
        print("-" * 80)
        for task in tasks:
            status_icon = "⏳" if task.get('status') == 'pending' else "✅" if task.get('status') == 'done' else "❌"
            print(f"{task['id']:<20} {task['time']:<20} {task['message'][:28]:<30} {status_icon}")
        print("-" * 80)
    else:
        # 列出定时任务
        tasks = read_markdown_table(TASKS_FILE)
        if not tasks:
            print("暂无定时任务")
            return
        
        print("\n📅 定时任务列表:\n")
        print(f"{'时间':<10} {'任务名':<15} {'类型':<8} {'星期':<10} {'通知方式':<15} {'状态'}")
        print("-" * 80)
        for task in tasks:
            status_icon = task.get('status', '✅')
            print(f"{task['time']:<10} {task['name']:<15} {task['type']:<8} {task['weekday']:<10} {task['notify']:<15} {status_icon}")
        print("-" * 80)
        
        # 显示 crontab 状态
        print("\n⏰ crontab 状态:")
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            if result.returncode == 0:
                task_count = len([t for t in tasks if t.get('status') == '✅'])
                print(f"已配置 {task_count} 个启用的任务")
            else:
                print("⚠️  crontab 未配置")
        except:
            print("⚠️  无法读取 crontab")

def cmd_add(args):
    """添加定时任务"""
    tasks = read_markdown_table(TASKS_FILE)
    
    # 检查任务名是否重复
    for task in tasks:
        if task['name'] == args.name:
            log("ERROR", f"任务已存在：{args.name}")
            return
    
    # 添加新任务
    new_task = {
        'time': args.time,
        'name': args.name,
        'type': args.type,
        'content': args.content,
        'weekday': args.weekday or '1-7',
        'notify': args.notify or '本地播放',
        'status': '✅'
    }
    tasks.append(new_task)
    
    # 写入文件
    write_markdown_table(TASKS_FILE, tasks)
    log("INFO", f"✓ 任务已添加：{args.name}")
    
    # 更新 crontab
    update_crontab(tasks)

def cmd_edit(args):
    """修改任务"""
    tasks = read_markdown_table(TASKS_FILE)
    
    found = False
    for task in tasks:
        if task['name'] == args.name:
            found = True
            if args.time:
                task['time'] = args.time
            if args.content:
                task['content'] = args.content
            if args.weekday:
                task['weekday'] = args.weekday
            if args.notify:
                task['notify'] = args.notify
            
            log("INFO", f"✓ 任务已更新：{args.name}")
            break
    
    if not found:
        log("ERROR", f"未找到任务：{args.name}")
        return
    
    # 写入文件
    write_markdown_table(TASKS_FILE, tasks)
    
    # 更新 crontab
    update_crontab(tasks)

def cmd_toggle(args):
    """切换任务状态"""
    tasks = read_markdown_table(TASKS_FILE)
    
    for task in tasks:
        if task['name'] == args.name:
            if task['status'] == '✅':
                task['status'] = '⏳'
                log("INFO", f"⏸️  已暂停：{args.name}")
            else:
                task['status'] = '✅'
                log("INFO", f"▶️  已启用：{args.name}")
            
            write_markdown_table(TASKS_FILE, tasks)
            update_crontab(tasks)
            return
    
    log("ERROR", f"未找到任务：{args.name}")

def cmd_enable(args):
    """启用任务"""
    tasks = read_markdown_table(TASKS_FILE)
    
    for task in tasks:
        if task['name'] == args.name:
            task['status'] = '✅'
            log("INFO", f"▶️  已启用：{args.name}")
            write_markdown_table(TASKS_FILE, tasks)
            update_crontab(tasks)
            return
    
    log("ERROR", f"未找到任务：{args.name}")

def cmd_disable(args):
    """暂停任务"""
    tasks = read_markdown_table(TASKS_FILE)
    
    for task in tasks:
        if task['name'] == args.name:
            task['status'] = '⏳'
            log("INFO", f"⏸️  已暂停：{args.name}")
            write_markdown_table(TASKS_FILE, tasks)
            update_crontab(tasks)
            return
    
    log("ERROR", f"未找到任务：{args.name}")

def cmd_delete(args):
    """删除任务"""
    if args.temp:
        # 删除临时任务
        tasks = read_temp_tasks()
        tasks = [t for t in tasks if t['id'] != args.name]
        write_temp_tasks(tasks)
        log("INFO", f"✓ 临时任务已删除：{args.name}")
    else:
        # 删除定时任务
        tasks = read_markdown_table(TASKS_FILE)
        original_count = len(tasks)
        tasks = [t for t in tasks if t['name'] != args.name]
        
        if len(tasks) < original_count:
            log("INFO", f"✓ 任务已删除：{args.name}")
            write_markdown_table(TASKS_FILE, tasks)
            update_crontab(tasks)
        else:
            log("ERROR", f"未找到任务：{args.name}")

def cmd_temp(args):
    """添加临时任务"""
    ensure_calendar_dir()
    
    # 解析时间
    if args.time:
        # 绝对时间
        try:
            task_time = datetime.strptime(args.time, "%Y-%m-%d %H:%M")
        except ValueError:
            log("ERROR", f"时间格式错误，应为：YYYY-MM-DD HH:MM")
            return
    elif args.in_time:
        # 相对时间
        now = datetime.now()
        match = re.match(r'(\d+)([mhd])', args.in_time)
        if not match:
            log("ERROR", "相对时间格式错误，示例：30m, 1h, 2d")
            return
        
        value = int(match.group(1))
        unit = match.group(2)
        
        if unit == 'm':
            task_time = now + timedelta(minutes=value)
        elif unit == 'h':
            task_time = now + timedelta(hours=value)
        elif unit == 'd':
            task_time = now + timedelta(days=value)
    elif args.tomorrow:
        # 明天
        tomorrow = datetime.now() + timedelta(days=1)
        hour, minute = args.tomorrow.split(':')
        task_time = tomorrow.replace(hour=int(hour), minute=int(minute), second=0, microsecond=0)
    else:
        log("ERROR", "请指定时间：--time, --in, 或 --tomorrow")
        return
    
    # 创建任务
    task = {
        'id': generate_task_id(),
        'time': task_time.strftime("%Y-%m-%d %H:%M"),
        'message': args.message,
        'notify': args.notify or '本地播放',
        'status': 'pending',
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # 读取现有任务并添加
    tasks = read_temp_tasks()
    tasks.append(task)
    write_temp_tasks(tasks)
    
    log("INFO", f"✓ 临时任务已添加：{task['id']}")
    log("INFO", f"  执行时间：{task['time']}")
    log("INFO", f"  提醒内容：{task['message']}")

def cmd_check_temp(args):
    """检查并执行到期的临时任务"""
    tasks = read_temp_tasks()
    now = datetime.now()
    
    executed = []
    
    for task in tasks:
        if task.get('status') != 'pending':
            continue
        
        try:
            task_time = datetime.strptime(task['time'], "%Y-%m-%d %H:%M")
        except ValueError:
            continue
        
        if task_time <= now:
            # 执行任务
            log("INFO", f"执行临时任务：{task['message']}")
            
            # 播放语音
            if '本地播放' in task.get('notify', ''):
                try:
                    tts_script = WORKSPACE / "skills" / "edge-tts" / "scripts" / "tts.py"
                    subprocess.run(['python3', str(tts_script), '--play', task['message']], 
                                 timeout=30, capture_output=True)
                except Exception as e:
                    log("ERROR", f"语音播放失败：{e}")
            
            # 记录日志
            task['status'] = 'done'
            task['executed_at'] = now.strftime("%Y-%m-%d %H:%M")
            executed.append(task)
    
    # 保存状态
    write_temp_tasks(tasks)
    
    if executed:
        log("INFO", f"✓ 执行了 {len(executed)} 个临时任务")
    else:
        log("INFO", "暂无到期的临时任务")

def cmd_cleanup(args):
    """清理已过期的临时任务"""
    tasks = read_temp_tasks()
    original_count = len(tasks)
    
    # 保留 pending 和最近完成的任务
    now = datetime.now()
    tasks = [t for t in tasks if t.get('status') == 'pending' or 
             (t.get('status') == 'done' and 
              datetime.strptime(t.get('executed_at', '2000-01-01 00:00'), '%Y-%m-%d %H:%M') > now - timedelta(days=7))]
    
    removed = original_count - len(tasks)
    write_temp_tasks(tasks)
    
    log("INFO", f"✓ 清理了 {removed} 个过期任务")

# ==================== 主程序 ====================

def main():
    parser = argparse.ArgumentParser(description="日程任务管理")
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--temp', action='store_true', help='列出临时任务')
    list_parser.add_argument('--today', action='store_true', help='列出今日临时任务')
    
    # add 命令
    add_parser = subparsers.add_parser('add', help='添加定时任务')
    add_parser.add_argument('--time', required=True, help='执行时间 (HH:MM)')
    add_parser.add_argument('--name', required=True, help='任务名称')
    add_parser.add_argument('--type', required=True, choices=['tts', 'news'], help='任务类型')
    add_parser.add_argument('--content', required=True, help='TTS 文本或新闻目录')
    add_parser.add_argument('--weekday', default='1-7', help='星期规格 (默认：1-7)')
    add_parser.add_argument('--notify', default='本地播放', help='通知方式')
    
    # edit 命令
    edit_parser = subparsers.add_parser('edit', help='修改任务')
    edit_parser.add_argument('name', help='任务名称')
    edit_parser.add_argument('--time', help='新时间')
    edit_parser.add_argument('--content', help='新内容')
    edit_parser.add_argument('--weekday', help='新星期规格')
    edit_parser.add_argument('--notify', help='新通知方式')
    
    # toggle 命令
    toggle_parser = subparsers.add_parser('toggle', help='切换任务状态')
    toggle_parser.add_argument('name', help='任务名称')
    
    # enable 命令
    enable_parser = subparsers.add_parser('enable', help='启用任务')
    enable_parser.add_argument('name', help='任务名称')
    
    # disable 命令
    disable_parser = subparsers.add_parser('disable', help='暂停任务')
    disable_parser.add_argument('name', help='任务名称')
    
    # delete 命令
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('name', help='任务名称')
    delete_parser.add_argument('--temp', action='store_true', help='删除临时任务')
    
    # temp 命令
    temp_parser = subparsers.add_parser('temp', help='添加临时任务')
    temp_parser.add_argument('--time', help='绝对时间 (YYYY-MM-DD HH:MM)')
    temp_parser.add_argument('--in', dest='in_time', help='相对时间 (30m, 1h, 2d)')
    temp_parser.add_argument('--tomorrow', help='明天指定时间 (HH:MM)')
    temp_parser.add_argument('--message', required=True, help='提醒内容')
    temp_parser.add_argument('--notify', default='本地播放', help='通知方式')
    
    # check-temp 命令
    check_parser = subparsers.add_parser('check-temp', help='检查临时任务')
    
    # cleanup 命令
    cleanup_parser = subparsers.add_parser('cleanup', help='清理过期任务')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行命令
    commands = {
        'list': cmd_list,
        'add': cmd_add,
        'edit': cmd_edit,
        'toggle': cmd_toggle,
        'enable': cmd_enable,
        'disable': cmd_disable,
        'delete': cmd_delete,
        'temp': cmd_temp,
        'check-temp': cmd_check_temp,
        'cleanup': cmd_cleanup
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
