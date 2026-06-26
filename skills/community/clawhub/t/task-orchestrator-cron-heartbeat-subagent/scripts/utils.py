#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Orchestrator v2.0 - Utility Scripts

提供任务识别、时间解析、复杂度评分、配置加载等工具函数

v2.0 新增:
- 动态配置加载
- 防死循环检测
- 智能汇总规则
- 4 级风险分类
"""

import re
import json
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# 工作区路径
WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
TASK_REGISTRY = MEMORY_DIR / "task-registry.json"
TASK_DASHBOARD = MEMORY_DIR / "task-dashboard.md"
CONFIG_DIR = Path.home() / ".openclaw" / "skills" / "task-orchestrator" / "config"
CONFIG_FILE = CONFIG_DIR / "task-orchestrator-config.yaml"


def parse_time(time_str: str) -> Optional[datetime]:
    """
    解析时间表达式，返回 datetime 对象
    
    支持格式:
    - 相对时间："10 分钟后"、"1 小时后"、"2 天后"
    - 相对时间（英文）："in 10 minutes"、"in 1 hour"
    - 绝对时间："今晚 8 点"、"明天上午 10 点"
    - ISO 格式："2026-04-04T10:00:00+08:00"
    """
    now = datetime.now()
    
    # 相对时间 - 中文
    relative_patterns = [
        (r'(\d+)\s*分钟后?', 'minutes'),
        (r'(\d+)\s*小时后?', 'hours'),
        (r'(\d+)\s*天后?', 'days'),
        (r'(\d+)\s*周后?', 'weeks'),
    ]
    
    for pattern, unit in relative_patterns:
        match = re.search(pattern, time_str)
        if match:
            value = int(match.group(1))
            if unit == 'minutes':
                return now + timedelta(minutes=value)
            elif unit == 'hours':
                return now + timedelta(hours=value)
            elif unit == 'days':
                return now + timedelta(days=value)
            elif unit == 'weeks':
                return now + timedelta(weeks=value)
    
    # 相对时间 - 英文
    english_patterns = [
        (r'in\s+(\d+)\s*minutes?', 'minutes'),
        (r'in\s+(\d+)\s*hours?', 'hours'),
        (r'in\s+(\d+)\s*days?', 'days'),
    ]
    
    for pattern, unit in english_patterns:
        match = re.search(pattern, time_str, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            if unit == 'minutes':
                return now + timedelta(minutes=value)
            elif unit == 'hours':
                return now + timedelta(hours=value)
            elif unit == 'days':
                return now + timedelta(days=value)
    
    # 绝对时间 - 中文
    if '今晚' in time_str:
        match = re.search(r'今晚\s*(\d+)[点時]', time_str)
        if match:
            hour = int(match.group(1))
            return now.replace(hour=hour, minute=0, second=0, microsecond=0)
    
    if '明天' in time_str:
        match = re.search(r'明天\s*(\d+)[点時]', time_str)
        if match:
            hour = int(match.group(1))
            tomorrow = now + timedelta(days=1)
            return tomorrow.replace(hour=hour, minute=0, second=0, microsecond=0)
    
    # ISO 格式
    try:
        # 尝试解析 ISO 8601 格式
        return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    except ValueError:
        pass
    
    return None


def is_cron_task(user_input: str) -> bool:
    """
    判断是否为 Cron 任务
    
    触发特征:
    - 时间表达式："每天"、"每周"、"每月"、"X 点后"
    - 定时相关："定时"、"提醒"、"闹钟"
    - Cron 表达式格式
    """
    # 时间表达式
    time_patterns = [
        r'每天\s*\d+[:点]',
        r'每周\s*\w+',
        r'每月\s*\d+号',
        r'\d+\s*(分钟 | 小时 | 天 | 周)\s*后',
        r'in\s+\d+\s*(minute|hour|day|week)s?',
        r'\d+\s+[*\d\s]+\d+',  # Cron 表达式
    ]
    
    # 关键词
    cron_keywords = ['定时', '提醒', '闹钟', 'scheduled', 'cron', 'alarm']
    
    has_time_expr = any(re.search(p, user_input) for p in time_patterns)
    has_keyword = any(k in user_input.lower() for k in cron_keywords)
    
    return has_time_expr or has_keyword


def is_heartbeat_task(user_input: str) -> bool:
    """
    判断是否为 Heartbeat 任务
    
    触发特征:
    - "心跳"、"heartbeat"、"定期"、"每次检查"
    - "监控"、"轮询"、"周期性"
    - 排除精确时间表达式（那是 Cron）
    """
    # 先排除 Cron 任务
    if is_cron_task(user_input):
        return False
    
    heartbeat_keywords = [
        '心跳', 'heartbeat', '定期', '每次',
        '监控', '轮询', 'polling', 'periodic',
        '保持在线', '自动检查', 'background'
    ]
    
    return any(k in user_input.lower() for k in heartbeat_keywords)


def is_subagent_task(user_input: str) -> bool:
    """
    判断是否为 Subagent 任务
    
    触发特征:
    - 动作数 >= 3
    - 复杂度评分 >= 5
    - 有"多步骤"、"拆解"等关键词
    """
    # 关键词快速判断
    subagent_keywords = ['多步骤', '拆解', '分步', '复杂', '调研', '分析', '并行']
    if any(k in user_input for k in subagent_keywords):
        return True
    
    # 复杂度评分
    complexity = calculate_complexity(user_input)
    return complexity >= 5


def is_task_record(user_input: str) -> bool:
    """
    判断是否需要 Task 记录
    
    触发特征:
    - "持续"、"追踪"、"跟踪"
    - "长期"、"ongoing"、"project"
    """
    task_keywords = ['持续', '追踪', '跟踪', '长期', 'ongoing', 'project', '记录']
    return any(k in user_input.lower() for k in task_keywords)


def identify_task_type(user_input: str) -> str:
    """
    识别任务类型
    
    返回：cron | heartbeat | subagent | task | immediate
    """
    if is_cron_task(user_input):
        return "cron"
    elif is_heartbeat_task(user_input):
        return "heartbeat"
    elif is_subagent_task(user_input):
        return "subagent"
    elif is_task_record(user_input):
        return "task"
    else:
        return "immediate"


def count_actions(user_input: str) -> int:
    """
    计算用户请求中的动作数量
    
    动作类型:
    - 文件操作：创建、编辑、删除、读取
    - 命令执行：运行、执行、调用
    - 网络请求：搜索、查询、获取
    - 内容生成：写、生成、创建
    """
    action_keywords = [
        # 文件操作
        '创建', '编辑', '删除', '读取', 'write', 'edit', 'delete', 'read',
        # 命令执行
        '运行', '执行', '调用', 'run', 'execute', 'call',
        # 网络请求
        '搜索', '查询', '获取', 'search', 'query', 'fetch',
        # 内容生成
        '写', '生成', '创建', '整理', '总结', 'write', 'generate', 'create', 'summarize',
        # 其他
        '分析', '调研', '测试', '部署', 'analyze', 'research', 'test', 'deploy'
    ]
    
    count = 0
    for keyword in action_keywords:
        if keyword in user_input.lower():
            count += 1
    
    # 去重：同一动作不重复计数
    return min(count, 10)  # 最多计为 10


def calculate_complexity(user_input: str) -> int:
    """
    计算任务复杂度评分（0-10）
    
    评分维度:
    - 动作数量（0-4 分）：每个动作 1 分，最多 4 分
    - 依赖关系（0-3 分）：有依赖 +2 分，强依赖 +3 分
    - 范围大小（0-3 分）："整个"、"complete" +2 分，"所有" +3 分
    """
    score = 0
    
    # 动作数量（0-4 分）
    actions = count_actions(user_input)
    score += min(actions, 4)
    
    # 依赖关系（0-3 分）
    dependency_keywords = ['基于', 'using', '然后', '之后', 'after', 'then', 'step', '分步']
    if any(k in user_input.lower() for k in dependency_keywords):
        score += 2
        if 'step' in user_input.lower() or '分步' in user_input:
            score += 1
    
    # 范围大小（0-3 分）
    scope_keywords = ['整个', 'complete', '所有', 'all', 'full', 'entire']
    if any(k in user_input.lower() for k in scope_keywords):
        score += 2
    
    return min(score, 10)


def get_complexity_level(score: int) -> str:
    """
    根据复杂度评分返回等级
    
    1-3: 简单
    4-6: 一般
    7-10: 复杂
    """
    if score <= 3:
        return "简单"
    elif score <= 6:
        return "一般"
    else:
        return "复杂"


def assess_risk_level(user_input: str) -> Tuple[str, str]:
    """
    评估任务风险等级
    
    返回：(风险等级，风险描述)
    
    4 级风险分类:
    - 🟢 LOW: 可逆操作，无副作用
    - 🟡 MEDIUM: 有限副作用，可回滚
    - 🔴 HIGH: 重大操作，需备份
    - ⚫ CRITICAL: 不可逆，永久影响
    """
    # 关键词匹配
    critical_keywords = ['删除', 'delete', '永久', 'permanent', '生产', 'production', '权限', 'permission']
    high_keywords = ['修改', 'modify', '配置', 'config', '部署', 'deploy', '发布', 'publish']
    medium_keywords = ['创建', 'create', '编辑', 'edit', '更新', 'update']
    
    input_lower = user_input.lower()
    
    # 检查关键词
    if any(k in input_lower for k in critical_keywords):
        return ("CRITICAL", "⚫ 不可逆操作，需要明确授权")
    elif any(k in input_lower for k in high_keywords):
        return ("HIGH", "🔴 重大操作，需要详细确认")
    elif any(k in input_lower for k in medium_keywords):
        return ("MEDIUM", "🟡 有限副作用，需要简要确认")
    else:
        return ("LOW", "🟢 可逆操作，可自动执行")


def load_config() -> Dict:
    """
    加载配置文件
    
    返回配置字典，如果配置文件不存在则返回默认配置
    """
    if not CONFIG_FILE.exists():
        return get_default_config()
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def get_default_config() -> Dict:
    """
    返回默认配置
    """
    return {
        "pipelines": {
            "simple": {"complexity_range": [1, 3]},
            "standard": {"complexity_range": [4, 6]},
            "complex": {"complexity_range": [7, 10]}
        },
        "thresholds": {
            "complexity": {
                "simple_max_steps": 1,
                "normal_max_steps": 3,
                "complex_min_steps": 4
            },
            "deadlock_prevention": {
                "max_token_per_task": 100000,
                "max_time_minutes": 30,
                "max_retries": 2,
                "progress_check_interval": 5
            }
        },
        "business_rules": {
            "confirm_requirements": {
                "auto_execute": ["LOW"],
                "brief_confirm": ["MEDIUM"],
                "detailed_confirm": ["HIGH"],
                "explicit_authorization": ["CRITICAL"]
            }
        }
    }


def select_pipeline(complexity_score: int, config: Dict = None) -> str:
    """
    根据复杂度评分选择管道
    
    返回：pipeline name (simple | standard | complex)
    """
    if config is None:
        config = load_config()
    
    pipelines = config.get("pipelines", {})
    
    for name, pipeline in pipelines.items():
        range_min, range_max = pipeline.get("complexity_range", [0, 10])
        if range_min <= complexity_score <= range_max:
            return name
    
    # 默认返回 standard
    return "standard"


def check_deadlock_prevention(task_state: Dict, config: Dict = None) -> Dict:
    """
    检查防死循环状态
    
    返回：{
        "status": "ok" | "warning" | "critical",
        "message": "描述信息",
        "action": "continue" | "retry" | "abort"
    }
    """
    if config is None:
        config = load_config()
    
    thresholds = config.get("thresholds", {}).get("deadlock_prevention", {})
    max_token = thresholds.get("max_token_per_task", 100000)
    max_time = thresholds.get("max_time_minutes", 30)
    max_retries = thresholds.get("max_retries", 2)
    
    # 检查 token 消耗
    used_token = task_state.get("used_token", 0)
    if used_token >= max_token:
        return {
            "status": "critical",
            "message": f"Token 消耗已达上限 ({used_token}/{max_token})",
            "action": "abort"
        }
    elif used_token >= max_token * 0.8:
        return {
            "status": "warning",
            "message": f"Token 消耗已达 80% ({used_token}/{max_token})",
            "action": "continue"
        }
    
    # 检查时间
    elapsed = task_state.get("elapsed_minutes", 0)
    if elapsed >= max_time:
        return {
            "status": "critical",
            "message": f"任务超时 ({elapsed}/{max_time}分钟)",
            "action": "retry" if task_state.get("retries", 0) < max_retries else "abort"
        }
    
    # 检查进度
    no_progress_count = task_state.get("no_progress_count", 0)
    if no_progress_count >= 3:
        return {
            "status": "critical",
            "message": f"连续{no_progress_count}次检查无进展",
            "action": "retry" if task_state.get("retries", 0) < max_retries else "abort"
        }
    
    return {
        "status": "ok",
        "message": "任务正常进行中",
        "action": "continue"
    }


def load_task_registry() -> Dict:
    """加载任务注册表"""
    if not TASK_REGISTRY.exists():
        return {"tasks": [], "last_updated": None}
    
    with open(TASK_REGISTRY, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_task_registry(data: Dict):
    """保存任务注册表"""
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    data["last_updated"] = datetime.now().isoformat()
    
    with open(TASK_REGISTRY, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def register_task(task_id: str, task_type: str, name: str, metadata: Dict = None):
    """注册新任务"""
    registry = load_task_registry()
    
    task = {
        "id": task_id,
        "type": task_type,
        "name": name,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "last_run": None,
        "next_run": None,
        "run_count": 0,
        "last_error": None,
        "metadata": metadata or {}
    }
    
    registry["tasks"].append(task)
    save_task_registry(registry)
    
    return task


def update_task_status(task_id: str, status: str, metadata: Dict = None):
    """更新任务状态"""
    registry = load_task_registry()
    
    for task in registry["tasks"]:
        if task["id"] == task_id:
            task["status"] = status
            if metadata:
                task.update(metadata)
            break
    
    save_task_registry(registry)


def generate_dashboard() -> str:
    """生成任务统计面板"""
    registry = load_task_registry()
    tasks = registry.get("tasks", [])
    
    # 统计
    active_count = sum(1 for t in tasks if t["status"] == "active")
    completed_count = sum(1 for t in tasks if t["status"] == "completed")
    
    cron_count = sum(1 for t in tasks if t["type"] == "cron")
    heartbeat_count = sum(1 for t in tasks if t["type"] == "heartbeat")
    subagent_count = sum(1 for t in tasks if t["type"] == "subagent")
    task_count = sum(1 for t in tasks if t["type"] == "task")
    
    # 生成 Markdown
    dashboard = f"""# 任务统计面板

_最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M')}__

## 总览
- **活跃任务**: {active_count}
- **已完成**: {completed_count}
- **总任务数**: {len(tasks)}

## 按类型分布
- **Cron 任务**: {cron_count}
- **Heartbeat 任务**: {heartbeat_count}
- **Subagent 任务**: {subagent_count}
- **Task 记录**: {task_count}

## 最近任务
| 任务名称 | 类型 | 状态 | 创建时间 |
|----------|------|------|----------|
"""
    
    # 最近 10 个任务
    recent_tasks = sorted(tasks, key=lambda t: t["created_at"], reverse=True)[:10]
    for task in recent_tasks:
        status_emoji = {"active": "🟢", "completed": "✅", "paused": "⏸️", "failed": "❌"}.get(task["status"], "⚪")
        dashboard += f"| {task['name']} | {task['type']} | {status_emoji} {task['status']} | {task['created_at'][:10]} |\n"
    
    return dashboard


def main():
    """主函数 - 命令行工具"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python task_orchestrator_utils.py <command> [args]")
        print("Commands:")
        print("  identify <text>     - 识别任务类型")
        print("  parse_time <text>   - 解析时间")
        print("  complexity <text>   - 计算复杂度")
        print("  risk <text>         - 评估风险等级")
        print("  pipeline <score>    - 根据复杂度选择管道")
        print("  dashboard           - 生成统计面板")
        print("  register <id> <type> <name> - 注册任务")
        print("  config              - 显示当前配置")
        return
    
    command = sys.argv[1]
    
    if command == "identify":
        text = " ".join(sys.argv[2:])
        task_type = identify_task_type(text)
        complexity = calculate_complexity(text)
        risk_level, risk_desc = assess_risk_level(text)
        print(f"任务类型：{task_type}")
        print(f"复杂度评分：{complexity}/10 ({get_complexity_level(complexity)})")
        print(f"风险等级：{risk_desc}")
    
    elif command == "parse_time":
        text = " ".join(sys.argv[2:])
        parsed = parse_time(text)
        if parsed:
            print(f"解析结果：{parsed.isoformat()}")
        else:
            print("无法解析时间表达式")
    
    elif command == "complexity":
        text = " ".join(sys.argv[2:])
        complexity = calculate_complexity(text)
        print(f"复杂度评分：{complexity}/10 ({get_complexity_level(complexity)})")
    
    elif command == "risk":
        text = " ".join(sys.argv[2:])
        risk_level, risk_desc = assess_risk_level(text)
        print(f"风险等级：{risk_desc}")
    
    elif command == "pipeline":
        if len(sys.argv) < 2:
            print("Usage: pipeline <complexity_score>")
            return
        score = int(sys.argv[2])
        pipeline = select_pipeline(score)
        print(f"推荐管道：{pipeline}")
    
    elif command == "dashboard":
        dashboard = generate_dashboard()
        print(dashboard)
    
    elif command == "register":
        if len(sys.argv) < 5:
            print("Usage: register <id> <type> <name>")
            return
        task_id = sys.argv[2]
        task_type = sys.argv[3]
        name = sys.argv[4]
        register_task(task_id, task_type, name)
        print(f"任务已注册：{name} ({task_type})")
    
    elif command == "config":
        config = load_config()
        print("当前配置:")
        print(yaml.dump(config, default_flow_style=False, allow_unicode=True))
    
    else:
        print(f"未知命令：{command}")


if __name__ == "__main__":
    main()
