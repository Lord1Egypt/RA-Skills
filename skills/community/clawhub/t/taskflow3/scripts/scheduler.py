#!/usr/bin/env python3
"""
TaskFlow 3.0 - 项目调度器

核心理念：
- 从 PROJECT.yaml 读取配置，不硬编码
- 支持原创项目和转载类项目
- 清晰的状态报告
"""
import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

import yaml

WORKSPACE = Path.home() / '.openclaw' / 'workspace-zsxq'
PROJECTS_DIR = WORKSPACE / 'projects'


def load_project(project_id: str) -> dict:
    """加载项目配置"""
    project_file = PROJECTS_DIR / project_id / 'PROJECT.yaml'
    if not project_file.exists():
        return None
    with open(project_file, 'r') as f:
        return yaml.safe_load(f)


def list_projects() -> list:
    """列出所有启用项目"""
    projects = []
    if PROJECTS_DIR.exists():
        for proj_dir in PROJECTS_DIR.iterdir():
            if proj_dir.is_dir():
                meta = load_project(proj_dir.name)
                if meta and meta.get('meta', {}).get('enabled'):
                    projects.append(proj_dir.name)
    return projects


def count_today_posts(project_id: str) -> int:
    """统计今日发布数量"""
    history_file = PROJECTS_DIR / project_id / 'memory' / 'post' / 'history.md'
    if not history_file.exists():
        return 0
    
    content = history_file.read_text()
    today_str = datetime.now().strftime('%Y-%m-%d')
    today_count = 0
    in_today_section = False
    
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('## ') and today_str in line:
            in_today_section = True
            continue
        if line.startswith('## ') and today_str not in line:
            in_today_section = False
            continue
        if in_today_section and line.startswith('- **'):
            today_count += 1
    
    return today_count


def count_source_available(source_project: str) -> int:
    """统计来源项目今日可用内容数量"""
    return count_today_posts(source_project)


def check_republish_status(project_id: str, source_project: str) -> tuple:
    """检查转载状态，返回 (已转载数, 来源总数)"""
    republished_file = PROJECTS_DIR / project_id / 'memory' / 'post' / 'republished.json'
    
    republished_count = 0
    if republished_file.exists():
        try:
            data = json.loads(republished_file.read_text())
            republished = data.get('republished', [])
            # 统计今日已转载
            today_str = datetime.now().strftime('%Y-%m-%d')
            for item in republished:
                pub_time = item.get('republishedTime', '')
                if today_str in pub_time:
                    republished_count += 1
        except:
            pass
    
    source_count = count_source_available(source_project)
    return republished_count, source_count


def get_project_status(project_id: str) -> dict:
    """获取项目完整状态"""
    project = load_project(project_id)
    if not project:
        return None
    
    constraints = project.get('constraints', {})
    daily_max = constraints.get('daily_max', 8)
    daily_min = constraints.get('daily_min', 0)
    source_project = constraints.get('source_project')
    
    today_count = count_today_posts(project_id)
    
    status = {
        'id': project_id,
        'name': project['meta'].get('name', project_id),
        'today_count': today_count,
        'daily_max': daily_max,
        'daily_min': daily_min,
        'is_republish': source_project is not None,
        'source_project': source_project,
        'source_count': 0,
        'republished_count': 0,
        'pending_count': 0
    }
    
    if source_project:
        # 转载类项目
        republished_count, source_count = check_republish_status(project_id, source_project)
        status['republished_count'] = republished_count
        status['source_count'] = source_count
        status['pending_count'] = min(source_count - republished_count, daily_max - today_count)
        if status['pending_count'] < 0:
            status['pending_count'] = 0
    else:
        # 原创类项目
        status['pending_count'] = daily_max - today_count if today_count < daily_max else 0
    
    return status


def format_status_line(status: dict) -> str:
    """格式化单行状态"""
    name = status['name']
    progress = f"{status['today_count']}/{status['daily_max']}"
    
    # 状态和简短描述
    if status['is_republish']:
        # 转载类项目
        if status['source_count'] == 0:
            icon = "⏸️"
            desc = "等待来源内容"
        elif status['pending_count'] == 0:
            icon = "✅"
            desc = "已全量转载"
        else:
            icon = "🔄"
            desc = f"待转载{status['pending_count']}篇"
    else:
        # 原创类项目
        if status['today_count'] >= status['daily_max']:
            icon = "✅"
            desc = "已完成"
        elif status['pending_count'] > 0:
            icon = "📝"
            desc = f"待发布{status['pending_count']}篇"
        else:
            icon = "⏸️"
            desc = "等待条件"
    
    # 对齐：项目名占18字符，进度占6字符
    return f"{icon} {name:<16} {progress:>6}  {desc}"


def run_projects():
    """Heartbeat 入口：检查所有项目并生成状态报告"""
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    projects = list_projects()
    if not projects:
        print(f"[TaskFlow] {now_str} 调度检查\n  → 无活跃项目")
        return
    
    # 收集所有项目状态
    statuses = []
    total_pending = 0
    
    for project_id in projects:
        status = get_project_status(project_id)
        if not status:
            continue
        statuses.append(status)
        total_pending += status['pending_count']
    
    # 无任务时：简短报告
    if total_pending == 0:
        print(f"[TaskFlow] {now_str} 调度检查\n")
        for status in statuses:
            print(format_status_line(status))
        print("\n✅ 所有项目已完成，无需操作")
        return
    
    # 有任务时：详细报告
    print(f"[TaskFlow] {now_str} 调度检查\n")
    for status in statuses:
        print(format_status_line(status))
    print(f"\n待处理: {total_pending}项")


def show_status():
    """显示项目状态"""
    projects = list_projects()
    print(f"\n📊 TaskFlow 项目状态 ({len(projects)}个)")
    print("-" * 50)
    for pid in projects:
        status = get_project_status(pid)
        if status:
            print(format_status_line(status))
    print()


def show_help():
    print("""TaskFlow 3.0 - 项目调度

Commands:
  run-projects       Heartbeat 入口：检查所有项目状态
  status             显示项目状态

项目结构:
  projects/{project}/
    ├── PROJECT.yaml          # 项目定义
    └── memory/post/
        ├── history.md        # 发布历史
        └── republished.json  # 转载记录（转载类项目）
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "run-projects":
        run_projects()
    elif cmd == "status":
        show_status()
    else:
        show_help()


if __name__ == "__main__":
    main()
