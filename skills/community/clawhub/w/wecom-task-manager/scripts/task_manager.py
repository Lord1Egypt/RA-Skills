#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业微信任务管理技能 - 核心模块
提供任务创建、更新、查询、完成等功能
所有 agents 可通过主 agent 代理调用
"""

import json
import subprocess
import sys
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List

# 切换到 workspace 目录（确保 mcporter 能找到 MCP 配置）
WORKSPACE = Path.home() / ".openclaw" / "workspace"
os.chdir(WORKSPACE)

# ==================== 配置加载 ====================

def load_config() -> dict:
    """
    从配置文件加载技能配置
    
    Returns:
        dict: 配置字典
    """
    config_path = Path(__file__).parent.parent / "config.json"
    
    if not config_path.exists():
        print(f"⚠️ 配置文件不存在：{config_path}，使用默认配置")
        return {}
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"⚠️ 加载配置文件失败：{e}，使用默认配置")
        return {}


# 加载配置
CONFIG = load_config()

# ==================== 企业微信配置 ====================

DOCID = CONFIG.get("enterpriseWeChat", {}).get(
    "docId",
    "dcTCczAuKRidTOQ9ZlUOpXgW9JSuq7slNrR6Z6O-N80yqOaGNTJpcTyqYXgOF7aXURG1adBiAxIYCi5KQg7KAXvA"
)
SHEET_ID = CONFIG.get("enterpriseWeChat", {}).get(
    "sheetId",
    "q979lj"
)
MCPORTER_PATH = "/usr/local/Cellar/node/25.6.0/bin/mcporter"

# ==================== 访问控制配置 ====================

# 允许调用技能的 agents 列表（从配置文件读取）
ALLOWED_AGENTS = [
    agent["agentId"]
    for agent in CONFIG.get("accessControl", {}).get("allowedAgents", [])
]
if not ALLOWED_AGENTS:
    # 默认配置
    ALLOWED_AGENTS = [
        "da-yan",
        "techlead",
        "opsdirector",
        "investment_coordinator",
        "general_coordinator"
    ]

# 访问控制开关
ACCESS_CONTROL_ENABLED = CONFIG.get("accessControl", {}).get("enabled", True)

# 并发控制配置
MAX_CONCURRENT_TASKS = CONFIG.get("concurrency", {}).get("maxConcurrentTasks", 3)

# 重试配置
RETRY_ENABLED = CONFIG.get("retry", {}).get("enabled", True)
MAX_RETRIES = CONFIG.get("retry", {}).get("maxRetries", 3)
BACKOFF_SECONDS = CONFIG.get("retry", {}).get("backoffSeconds", 2)


def check_access(agent_id: str = "") -> bool:
    """
    检查 agent 是否有权限调用技能
    
    Args:
        agent_id: 调用者的 agent ID
    
    Returns:
        bool: 有权限返回 True，否则返回 False
    """
    if not ACCESS_CONTROL_ENABLED:
        return True
    
    if not agent_id:
        # 如果没有提供 agent_id，尝试从环境变量获取
        agent_id = os.environ.get("AGENT_ID", "")
    
    if not agent_id:
        print("⚠️ 无法获取调用者 ID，拒绝访问")
        return False
    
    # 检查是否在白名单中
    if agent_id in ALLOWED_AGENTS:
        return True
    
    # 拒绝访问
    print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限调用 wecom-task-manager 技能")
    print(f"   允许的 agents: {', '.join(ALLOWED_AGENTS)}")
    print(f"   请联系 da-yan 或您的团队负责人获取权限")
    return False


def require_access(agent_id: str = "") -> bool:
    """
    访问控制装饰器函数
    
    Args:
        agent_id: 调用者的 agent ID
    
    Returns:
        bool: 是否通过检查（True=通过，False=拒绝）
    """
    return check_access(agent_id)

# Agent 分派规则
AGENT_MAPPING = {
    "开发": "techlead",
    "后端": "backend",
    "前端": "frontend",
    "全栈": "fullstack",
    "运维": "opsdirector",
    "安全": "security_eng",
    "监控": "monitoring_eng",
    "投资": "investment_coordinator",
    "数据": "dataanalyst",
    "市场": "marketing",
    "客服": "customersvc",
    "学习": "copywriter",
    "文档": "general_coordinator",
}

# 任务类型关键词
TASK_TYPE_KEYWORDS = {
    "开发": ["开发", "后端", "前端", "全栈", "API", "功能", "模块", "系统"],
    "运维": ["运维", "部署", "监控", "安全", "服务器", "配置", "优化"],
    "投资": ["投资", "股票", "加密货币", "交易", "风控", "分析", "策略"],
    "学习": ["学习", "培训", "研究", "分析", "探索", "测试"],
    "文档": ["文档", "表格", "报告", "说明", "整理", "记录"],
    "市场": ["市场", "运营", "推广", "营销", "品牌", "活动"],
    "客服": ["客服", "支持", "反馈", "用户", "回复", "响应"],
}


# ==================== 核心函数 ====================

def run_mcporter(command: str, args_dict: dict) -> Optional[dict]:
    """执行 mcporter 命令"""
    args_json = json.dumps(args_dict, ensure_ascii=False)
    cmd = f'{MCPORTER_PATH} call wecom-doc.{command} --args \'{args_json}\' --output json'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running mcporter: {result.stderr}")
        return None
    
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON: {result.stdout}")
        return None


def get_all_tasks(agent_id: str = "") -> List[dict]:
    """获取所有任务"""
    # 访问控制检查
    if not check_access(agent_id):
        return []
    
    result = run_mcporter("smartsheet_get_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID
    })
    if not result or result.get("errcode") != 0:
        print(f"Failed to get tasks: {result}")
        return []
    return result.get("records", [])


def get_task_by_id(task_id: str, agent_id: str = "") -> Optional[dict]:
    """根据任务 ID 查询任务"""
    # 访问控制检查
    if not check_access(agent_id):
        return None
    
    tasks = get_all_tasks(agent_id)
    for task in tasks:
        values = task.get("values", {})
        tid = values.get("任务 ID", [{}])[0].get("text", "")
        if tid == task_id:
            return task
    return None


# ==================== P0 功能：任务编辑 ====================

def edit_task(task_id: str, fields: Dict[str, Any], agent_id: str = "") -> bool:
    """
    编辑任务信息
    
    Args:
        task_id: 任务 ID
        fields: 要更新的字段字典，例如：
                {
                    "优先级": "P0",
                    "负责人": "backend",
                    "截止时间": "2026-04-20",
                    "任务描述": "新的描述"
                }
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 更新成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    task = get_task_by_id(task_id, agent_id)
    if not task:
        print(f"❌ 任务不存在：{task_id}")
        return False
    
    values = {}
    
    for field_name, field_value in fields.items():
        # 时间字段特殊处理
        if field_name in ["截止时间", "实际开始时间", "实际完成时间"]:
            if isinstance(field_value, str):
                # 如果是字符串，尝试解析为时间戳
                try:
                    # 支持多种格式
                    for fmt in ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y年%m月%d日"]:
                        try:
                            dt = datetime.strptime(field_value, fmt)
                            field_value = str(int(dt.timestamp() * 1000))  # 13 位毫秒
                            break
                        except ValueError:
                            continue
                    else:
                        # 如果都不是，假设已经是时间戳字符串
                        field_value = str(field_value)
                except Exception as e:
                    print(f"⚠️ 时间格式解析失败：{field_value}, 错误：{e}")
                    continue
            values[field_name] = field_value
        # 单选字段
        elif field_name in ["状态", "优先级", "任务类型", "风险等级", "验收状态"]:
            values[field_name] = [{"text": field_value}]
        # 文本字段
        else:
            values[field_name] = [{"text": field_value}]
    
    if not values:
        print("⚠️ 没有有效的更新内容")
        return False
    
    result = run_mcporter("smartsheet_update_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
        "records": [{
            "record_id": task["record_id"],
            "values": values
        }]
    })
    
    if result and result.get("errcode") == 0:
        print(f"✅ 任务已更新：{task_id}")
        print(f"   更新字段：{', '.join(values.keys())}")
        return True
    else:
        print(f"❌ 任务更新失败：{result}")
        return False


# ==================== P0 功能：任务搜索/过滤 ====================

def search_tasks(keyword: str) -> List[dict]:
    """
    关键词搜索任务
    
    Args:
        keyword: 搜索关键词
    
    Returns:
        匹配的任务列表
    """
    tasks = get_all_tasks()
    results = []
    
    for task in tasks:
        values = task.get("values", {})
        # 在任务 ID、名称、描述中搜索
        for field in ["任务 ID", "任务名称", "任务描述"]:
            field_val = values.get(field, [{}])[0].get("text", "")
            if keyword.lower() in field_val.lower():
                results.append(task)
                break
    
    print(f"🔍 搜索关键词：'{keyword}'")
    print(f"✅ 找到 {len(results)} 个匹配任务")
    return results


def filter_tasks(status: str = "", owner: str = "", priority: str = "", 
                 task_type: str = "", risk_level: str = "") -> List[dict]:
    """
    多条件过滤任务
    
    Args:
        status: 状态筛选（待办/进行中/已完成/已取消）
        owner: 负责人筛选
        priority: 优先级筛选（P0/P1/P2）
        task_type: 任务类型筛选
        risk_level: 风险等级筛选
    
    Returns:
        匹配的任务列表
    """
    tasks = get_all_tasks()
    results = []
    
    for task in tasks:
        values = task.get("values", {})
        match = True
        
        # 状态筛选
        if status:
            task_status = values.get("状态", [{}])[0].get("text", "")
            if task_status != status:
                match = False
        
        # 负责人筛选
        if owner and match:
            task_owner = values.get("负责人", [{}])[0].get("text", "")
            if owner.lower() not in task_owner.lower():
                match = False
        
        # 优先级筛选
        if priority and match:
            task_priority = values.get("优先级", [{}])[0].get("text", "")
            if task_priority != priority:
                match = False
        
        # 任务类型筛选
        if task_type and match:
            task_type_val = values.get("任务类型", [{}])[0].get("text", "")
            if task_type not in task_type_val:
                match = False
        
        # 风险等级筛选
        if risk_level and match:
            task_risk = values.get("风险等级", [{}])[0].get("text", "")
            if task_risk != risk_level:
                match = False
        
        if match:
            results.append(task)
    
    # 构建筛选条件描述
    conditions = []
    if status: conditions.append(f"状态={status}")
    if owner: conditions.append(f"负责人={owner}")
    if priority: conditions.append(f"优先级={priority}")
    if task_type: conditions.append(f"类型={task_type}")
    if risk_level: conditions.append(f"风险等级={risk_level}")
    
    print(f"🔍 筛选条件：{', '.join(conditions) if conditions else '无'}")
    print(f"✅ 找到 {len(results)} 个匹配任务")
    return results


# ==================== P0 功能：错误处理增强 ====================

class TaskManagerError(Exception):
    """任务管理器异常基类"""
    pass


class TaskNotFoundError(TaskManagerError):
    """任务不存在异常"""
    pass


class APIError(TaskManagerError):
    """API 调用失败异常"""
    pass


def run_mcporter_with_retry(command: str, args_dict: dict, max_retries: int = 3) -> Optional[dict]:
    """
    执行 mcporter 命令（带重试机制）
    
    Args:
        command: mcporter 命令
        args_dict: 参数字典
        max_retries: 最大重试次数
    
    Returns:
        API 响应结果
    """
    last_error = None
    
    for attempt in range(1, max_retries + 1):
        args_json = json.dumps(args_dict, ensure_ascii=False)
        cmd = f'{MCPORTER_PATH} call wecom-doc.{command} --args \'{args_json}\' --output json'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            try:
                response = json.loads(result.stdout)
                if response.get("errcode") == 0:
                    return response
                else:
                    last_error = f"API 错误：{response.get('errmsg', 'Unknown')}"
            except json.JSONDecodeError as e:
                last_error = f"JSON 解析失败：{e}"
        else:
            last_error = f"命令执行失败：{result.stderr}"
        
        # 指数退避
        if attempt < max_retries:
            wait_time = attempt * 2  # 2s, 4s, 6s
            print(f"⚠️ 第 {attempt} 次尝试失败，{wait_time}秒后重试...")
            import time
            time.sleep(wait_time)
    
    # 所有重试失败
    error_msg = f"API 调用失败（已重试{max_retries}次）: {last_error}"
    print(f"❌ {error_msg}")
    raise APIError(error_msg)


def determine_task_type(task_name: str, description: str = "") -> str:
    """根据任务名称和描述确定任务类型"""
    text = task_name + " " + description
    
    for task_type, keywords in TASK_TYPE_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return task_type
    
    return "文档"  # 默认


def determine_agent(task_type: str) -> str:
    """根据任务类型确定负责的 agent"""
    return AGENT_MAPPING.get(task_type, "general_coordinator")


def create_task(
    task_id: str,
    task_name: str,
    task_type: str,
    priority: str = "P1",
    owner: str = "",
    deadline: str = "",
    description: str = "",
    acceptance: str = "",
    remarks: str = "",
    estimated_hours: int = 0,
    agent_id: str = ""
) -> dict:
    """
    创建新任务（带访问控制）
    
    Args:
        task_id: 任务 ID (如 TASK-019)
        task_name: 任务名称
        task_type: 任务类型 (开发/运维/投资/学习/文档/市场/客服)
        priority: 优先级 (P0/P1/P2)
        owner: 负责人 (可选，自动推断)
        deadline: 截止时间 (格式：2026 年 04 月 15 日)
        description: 任务描述（应包含具体细节）
        acceptance: 验收标准
        remarks: 备注（记录问题和解决方案）
        estimated_hours: 预计工时（小时，0 表示不填）
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        dict: {success: bool, record_id: str, task_id: str}
    """
    # 访问控制检查
    if not check_access(agent_id):
        return {"success": False, "error": "访问拒绝"}
    
    # 自动推断负责人
    if not owner:
        owner = determine_agent(task_type)
    
    # 格式化截止时间
    if not deadline:
        # 默认 7 天后
        from datetime import timedelta
        deadline_dt = datetime.now() + timedelta(days=7)
        deadline = deadline_dt.strftime("%Y年%m月%d日")
    
    # 时间字段格式根据企业微信字段配置：
    # - 创建时间：auto_fill=true，不需要手动写入
    # - 截止时间：yyyy-mm-dd hh:mm → 使用 Unix 时间戳（毫秒）
    
    # 格式化截止时间
    # 企业微信日期字段使用 13 位毫秒时间戳（字符串格式，不包裹数组）
    from datetime import timedelta
    if not deadline:
        deadline_dt = datetime.now() + timedelta(days=7)
        deadline_ts = str(int(deadline_dt.timestamp() * 1000))  # 13 位毫秒，字符串
    else:
        # 如果传入的是字符串，解析为时间戳
        try:
            # 支持多种格式，统一转换为毫秒时间戳
            for fmt in ["%Y年%m月%d日", "%Y-%m-%d %H:%M", "%Y-%m-%d"]:
                try:
                    deadline_dt = datetime.strptime(deadline, fmt)
                    break
                except ValueError:
                    continue
            else:
                deadline_dt = datetime.now() + timedelta(days=7)
            deadline_ts = str(int(deadline_dt.timestamp() * 1000))  # 13 位毫秒，字符串
        except:
            deadline_dt = datetime.now() + timedelta(days=7)
            deadline_ts = str(int(deadline_dt.timestamp() * 1000))  # 13 位毫秒，字符串
    
    # 构建记录
    values = {
        "任务 ID": [{"text": task_id}],
        "任务名称": [{"text": task_name}],
        "任务描述": [{"text": description}],
        "任务类型": [{"text": task_type}],
        "优先级": [{"text": priority}],
        "负责人": [{"text": owner}],
        "状态": [{"text": "待办"}],
        "截止时间": deadline_ts,  # Unix 时间戳（毫秒）
        "进度": 0,
        "验收标准": [{"text": acceptance}],
        "备注": [{"text": remarks}],
        # 创建时间：auto_fill=true，不需要写入
        "验收状态": [{"text": "待验收"}],
        "风险等级": [{"text": "中"}]
    }
    
    # 添加预计工时（如果有）
    if estimated_hours > 0:
        values["预计工时"] = estimated_hours
    
    result = run_mcporter("smartsheet_add_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "records": [{"values": values}]
    })
    
    if result and result.get("errcode") == 0:
        record_id = result.get("records", [{}])[0].get("record_id", "")
        print(f"✅ 任务创建成功：{task_id}")
        return {"success": True, "record_id": record_id, "task_id": task_id}
    else:
        print(f"❌ 任务创建失败：{result}")
        return {"success": False, "record_id": "", "task_id": task_id}


# ==================== 并发控制配置 ====================

MAX_CONCURRENT_TASKS = 3  # 最多同时 3 个任务进行中


def get_in_progress_count() -> int:
    """
    获取当前进行中的任务数量
    
    Returns:
        int: 进行中任务数量
    """
    tasks = get_all_tasks()
    count = 0
    for task in tasks:
        values = task.get("values", {})
        status = values.get("状态", [{}])[0].get("text", "")
        if status == "进行中":
            count += 1
    return count


def start_task(task_id: str, owner: str = "", agent_id: str = "") -> bool:
    """
    开始执行任务（更新状态为进行中，记录实际开始时间）
    
    Args:
        task_id: 任务 ID
        owner: 负责人
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 更新成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    task = get_task_by_id(task_id, agent_id)
    if not task:
        print(f"❌ 任务不存在：{task_id}")
        return False
    
    # 检查并发限制
    in_progress_count = get_in_progress_count()
    if in_progress_count >= MAX_CONCURRENT_TASKS:
        print(f"⚠️ 已达到最大并发任务数限制（{MAX_CONCURRENT_TASKS}个）")
        print(f"   当前进行中任务：{in_progress_count}个")
        print(f"   任务 {task_id} 暂时无法开始，请等待其他任务完成")
        return False
    
    # 时间字段格式：使用 Unix 时间戳（毫秒）
    now_ts = str(int(datetime.now().timestamp() * 1000))  # 13 位毫秒，字符串
    now_datetime_full = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 读取当前备注，添加开始时间记录
    current_values = task.get("values", {})
    remarks_val = current_values.get("备注", [{}])[0].get("text", "") if current_values.get("备注") else ""
    
    # 添加开始时间记录到备注
    if remarks_val:
        remarks_update = f"{remarks_val}\n\n---\n【开始执行】{now_datetime_full}"
    else:
        remarks_update = f"【开始执行】{now_datetime_full}"
    
    # 时间字段使用 Unix 时间戳（毫秒）
    values = {
        "状态": [{"text": "进行中"}],
        "实际开始时间": now_ts,  # Unix 时间戳（毫秒）
        "备注": [{"text": remarks_update}]
    }
    
    if owner:
        values["负责人"] = [{"text": owner}]
    
    result = run_mcporter("smartsheet_update_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
        "records": [{
            "record_id": task["record_id"],
            "values": values
        }]
    })
    
    if result and result.get("errcode") == 0:
        print(f"✅ 任务已开始：{task_id} (开始时间：{now_str})")
        return True
    else:
        print(f"❌ 任务更新失败：{result}")
        return False


def update_progress(task_id: str, progress: int, blocker: str = "", agent_id: str = "") -> bool:
    """
    更新任务进度
    
    Args:
        task_id: 任务 ID
        progress: 进度 (0-100)
        blocker: 阻塞原因（可选）
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 更新成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    task = get_task_by_id(task_id, agent_id)
    if not task:
        print(f"❌ 任务不存在：{task_id}")
        return False
    
    values = {
        "进度": progress
    }
    
    if blocker:
        values["阻塞原因"] = [{"text": blocker}]
        values["风险等级"] = [{"text": "高"}]
    
    result = run_mcporter("smartsheet_update_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
        "records": [{
            "record_id": task["record_id"],
            "values": values
        }]
    })
    
    if result and result.get("errcode") == 0:
        print(f"✅ 进度已更新：{task_id} -> {progress}%")
        return True
    else:
        print(f"❌ 进度更新失败：{result}")
        return False


def complete_task(
    task_id: str,
    output_url: str = "",
    acceptor: str = "系统",
    notes: str = "",
    agent_id: str = ""
) -> bool:
    """
    标记任务完成
    
    Args:
        task_id: 任务 ID
        output_url: 输出物链接（如报告 URL）
        acceptor: 验收人
        notes: 完成说明（遇到的问题及解决方案）
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 更新成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    task = get_task_by_id(task_id, agent_id)
    if not task:
        print(f"❌ 任务不存在：{task_id}")
        return False
    
    # 企业微信日期字段：13 位毫秒时间戳（字符串格式）
    now_ts = str(int(datetime.now().timestamp() * 1000))  # 13 位毫秒，字符串
    now_datetime_full = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
    
    # 计算实际工时
    values = task.get("values", {})
    start_time = values.get("实际开始时间", [{}])[0] if values.get("实际开始时间") else {}
    
    # 从时间戳计算工时（支持字符串格式）
    if start_time:
        try:
            # 转换为数字
            ts = float(start_time) if isinstance(start_time, str) else start_time
            # 判断是秒还是毫秒
            if ts > 10000000000:  # 13 位毫秒
                start_date = datetime.fromtimestamp(ts / 1000)
            else:  # 10 位秒
                start_date = datetime.fromtimestamp(ts)
            days = (datetime.now() - start_date).days
            actual_hours = max(1, days * 8)
        except:
            actual_hours = 1
    else:
        actual_hours = 1
    
    # 读取当前备注，添加完成记录
    remarks_val = values.get("备注", [{}])[0].get("text", "") if values.get("备注") else ""
    
    # 构建完成记录
    completion_record = f"\n\n---\n【完成任务】{now_datetime_full}\n"
    completion_record += f"实际工时：{actual_hours} 小时\n"
    if output_url:
        completion_record += f"输出物：{output_url}\n"
    if notes:
        completion_record += f"\n【问题与解决】\n{notes}\n"
    completion_record += "\n等待验收..."
    
    remarks_update = remarks_val + completion_record if remarks_val else completion_record
    
    # 时间字段使用 13 位毫秒时间戳（字符串格式）
    values_to_update = {
        "状态": [{"text": "已完成"}],
        "进度": 100,
        "实际完成时间": now_ts,  # 13 位毫秒时间戳（字符串）
        "验收状态": [{"text": "待验收"}],
        "实际工时": actual_hours,
        "备注": [{"text": remarks_update}]
    }
    
    if output_url:
        values_to_update["输出物"] = [{
            "type": "url",
            "text": "查看",
            "link": output_url
        }]
    
    if acceptor:
        values_to_update["验收人"] = [{"text": acceptor}]
    
    result = run_mcporter("smartsheet_update_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
        "records": [{
            "record_id": task["record_id"],
            "values": values_to_update
        }]
    })
    
    if result and result.get("errcode") == 0:
        print(f"✅ 任务已完成：{task_id} (工时：{actual_hours}h, 完成时间：{now_datetime_full})")
        return True
    else:
        print(f"❌ 任务完成更新失败：{result}")
        return False


def get_task_status_report() -> dict:
    """
    生成任务状态报告
    
    Returns:
        dict: 包含任务统计信息
    """
    tasks = get_all_tasks()
    
    report = {
        "total": len(tasks),
        "completed": 0,
        "in_progress": 0,
        "pending": 0,
        "cancelled": 0,
        "tasks_by_status": {
            "已完成": [],
            "进行中": [],
            "待办": [],
            "已取消": []
        }
    }
    
    for task in tasks:
        values = task.get("values", {})
        status = values.get("状态", [{}])[0].get("text", "待办")
        task_id = values.get("任务 ID", [{}])[0].get("text", "")
        task_name = values.get("任务名称", [{}])[0].get("text", "")
        progress = values.get("进度", 0)
        owner = values.get("负责人", [{}])[0].get("text", "")
        
        task_info = {
            "id": task_id,
            "name": task_name,
            "progress": progress,
            "owner": owner
        }
        
        if status in report["tasks_by_status"]:
            report["tasks_by_status"][status].append(task_info)
        
        status_key = status.lower().replace("已", "").replace("中", "").replace("办", "")
        if status == "已完成":
            report["completed"] += 1
        elif status == "进行中":
            report["in_progress"] += 1
        elif status == "待办":
            report["pending"] += 1
        elif status == "已取消":
            report["cancelled"] += 1
    
    return report


def print_status_report():
    """打印任务状态报告"""
    report = get_task_status_report()
    
    print("\n" + "=" * 60)
    print("📊 企业微信任务状态报告")
    print("=" * 60)
    print(f"总任务数：{report['total']}")
    print(f"✅ 已完成：{report['completed']}")
    print(f"🔄 进行中：{report['in_progress']}")
    print(f"⏸️ 待办：{report['pending']}")
    print(f"❌ 已取消：{report['cancelled']}")
    
    if report["tasks_by_status"]["进行中"]:
        print("\n🔄 进行中任务:")
        for task in report["tasks_by_status"]["进行中"]:
            print(f"  - {task['id']}: {task['name']} ({task['progress']}%) - {task['owner']}")
    
    if report["tasks_by_status"]["待办"]:
        print("\n⏸️ 待办任务:")
        for task in report["tasks_by_status"]["待办"]:
            print(f"  - {task['id']}: {task['name']} - {task['owner']}")
    
    print("=" * 60 + "\n")


# ==================== 目标管理功能（整合自 proactive-tasks） ====================

GOAL_DATA_FILE = Path.home() / ".openclaw" / "skills" / "wecom-task-manager" / "data" / "goals.json"


def load_goal_data() -> dict:
    """加载目标数据"""
    if GOAL_DATA_FILE.exists():
        with open(GOAL_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"goals": [], "history": []}


def save_goal_data(data: dict):
    """保存目标数据"""
    GOAL_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GOAL_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def create_goal(
    goal_id: str,
    title: str,
    priority: str = "medium",
    context: str = "",
    owner: str = ""
) -> bool:
    """
    创建新目标
    
    Args:
        goal_id: 目标 ID (如 GOAL-001)
        title: 目标标题
        priority: 优先级 (critical/high/medium/low)
        context: 目标背景说明
        owner: 负责人
    
    Returns:
        bool: 创建成功返回 True
    """
    data = load_goal_data()
    
    # 检查 ID 是否重复
    for goal in data["goals"]:
        if goal["id"] == goal_id:
            print(f"❌ 目标已存在：{goal_id}")
            return False
    
    goal = {
        "id": goal_id,
        "title": title,
        "priority": priority,
        "context": context,
        "owner": owner,
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "tasks": []
    }
    
    data["goals"].append(goal)
    save_goal_data(data)
    
    print(f"✅ 目标创建成功：{goal_id} - {title}")
    return True


def decompose_goal(
    goal_id: str,
    task_title: str,
    task_id: str = "",
    priority: str = "medium",
    depends_on: List[str] = None,
    agent: str = "",
    description: str = "",
    estimated_hours: int = 0
) -> bool:
    """
    将目标分解为任务（在企业微信表格中创建）
    
    Args:
        goal_id: 目标 ID
        task_title: 任务标题
        task_id: 任务 ID（可选，自动生成）
        priority: 优先级 (critical/high/medium/low)
        depends_on: 依赖的任务 ID 列表
        agent: 负责人
        description: 任务描述
    
    Returns:
        bool: 创建成功返回 True
    """
    data = load_goal_data()
    
    # 查找目标
    goal = None
    for g in data["goals"]:
        if g["id"] == goal_id:
            goal = g
            break
    
    if not goal:
        print(f"❌ 目标不存在：{goal_id}")
        return False
    
    # 生成任务 ID
    if not task_id:
        task_num = len(goal["tasks"]) + 1
        task_id = f"{goal_id}-TASK-{task_num:03d}"
    
    # 映射优先级
    priority_map = {
        "critical": "P0",
        "high": "P1",
        "medium": "P2",
        "low": "P2"
    }
    wecom_priority = priority_map.get(priority, "P2")
    
    # 在企业微信表格中创建任务
    task_type = determine_task_type(task_title, description)
    if not agent:
        agent = determine_agent(task_type)
    
    # 计算截止时间（默认 7 天）
    from datetime import timedelta
    deadline_dt = datetime.now() + timedelta(days=7)
    deadline = deadline_dt.strftime("%Y年%m月%d日")
    
    # 构建详细的任务描述
    if not description:
        description = f"""【任务背景】
{task_title} 是目标 "{goal.get('title', goal_id)}" 的关键组成部分。

【具体工作内容】
1. 分析需求并制定执行计划
2. 按步骤执行任务
3. 记录过程和问题
4. 生成完成报告

【交付物】
- 任务完成报告：/workspace/tasks/{task_id}-completion-report.md
- 相关代码/文档（如适用）

【注意事项】
- 如有依赖任务，请先确认依赖已完成
- 遇到问题及时记录到备注字段
- 完成后更新任务状态"""
    
    # 构建备注（记录问题和解决方案的模板）
    remarks_template = f"""【任务来源】
来源目标：{goal_id}
分解时间：{datetime.now().strftime("%Y-%m-%d %H:%M")}

【问题记录】
（执行过程中遇到的问题及解决方案，待填写）

【注意事项】
（需要特别注意的事项，待填写）"""
    
    # 构建依赖描述
    if depends_on:
        deps_str = ", ".join(depends_on)
        dep_desc = f"⚠️ 前置依赖：{deps_str}\n请先确认以下任务已完成：{deps_str}"
        description = f"{description}\n\n{dep_desc}"
        remarks_template = f"{remarks_template}\n\n前置依赖：{deps_str}"
    
    # 调用 create_task 创建任务
    result = create_task(
        task_id=task_id,
        task_name=task_title,
        task_type=task_type,
        priority=wecom_priority,
        owner=agent,
        deadline=deadline,
        description=description,
        acceptance=f"完成标准：{task_title} 完成并通过验收",
        remarks=remarks_template,
        estimated_hours=estimated_hours
    )
    
    if result["success"]:
        # 如果有依赖，更新前置依赖字段
        if depends_on:
            task = get_task_by_id(task_id)
            if task:
                run_mcporter("smartsheet_update_records", {
                    "docid": DOCID,
                    "sheet_id": SHEET_ID,
                    "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
                    "records": [{
                        "record_id": task["record_id"],
                        "values": {
                            "前置依赖": [{"text": deps_str}]
                        }
                    }]
                })
                print(f"   已设置前置依赖：{deps_str}")
        
        # 记录目标与任务的关系
        goal["tasks"].append({
            "task_id": task_id,
            "title": task_title,
            "priority": priority,
            "depends_on": depends_on or [],
            "agent": agent,
            "created_at": datetime.now().isoformat()
        })
        save_goal_data(data)
        
        print(f"✅ 任务分解成功：{task_id}")
        if depends_on:
            print(f"   依赖：{', '.join(depends_on)}")
        
        return True
    else:
        return False
    
    if success:
        # 记录目标与任务的关系
        goal["tasks"].append({
            "task_id": task_id,
            "title": task_title,
            "priority": priority,
            "depends_on": depends_on or [],
            "agent": agent,
            "created_at": datetime.now().isoformat()
        })
        save_goal_data(data)
        
        print(f"✅ 任务分解成功：{task_id}")
        if depends_on:
            print(f"   依赖：{', '.join(depends_on)}")
    
    return success


def list_goals() -> List[dict]:
    """列出所有目标"""
    data = load_goal_data()
    return data["goals"]


def print_goals():
    """打印目标列表"""
    data = load_goal_data()
    
    if not data["goals"]:
        print("\n📭 暂无目标\n")
        return
    
    print("\n" + "=" * 70)
    print("🎯 目标列表")
    print("=" * 70)
    
    for goal in data["goals"]:
        status_emoji = "🟢" if goal["status"] == "active" else "⚪"
        priority_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢"
        }.get(goal.get("priority", "medium"), "🟡")
        
        print(f"\n{status_emoji} {priority_emoji} [{goal['id']}] {goal['title']}")
        print(f"   负责人：{goal.get('owner', '未分配')} | 状态：{goal['status']}")
        print(f"   创建时间：{goal['created_at'][:10]}")
        
        if goal.get("context"):
            print(f"   背景：{goal['context'][:50]}...")
        
        if goal.get("tasks"):
            print(f"   已分解任务：{len(goal['tasks'])} 个")
            for t in goal["tasks"][:3]:  # 只显示前 3 个
                dep = f" (依赖：{', '.join(t['depends_on'])})" if t.get('depends_on') else ""
                print(f"     - {t['task_id']}: {t['title']}{dep}")
            if len(goal["tasks"]) > 3:
                print(f"     ... 还有 {len(goal['tasks']) - 3} 个任务")
    
    print("\n" + "=" * 70 + "\n")


def get_next_task() -> Optional[dict]:
    """
    获取下一个可执行任务（无未满足依赖的最高优先级任务）
    
    Returns:
        dict: 下一个任务信息，或 None
    """
    tasks = get_all_tasks()
    
    # 构建任务状态映射
    task_status_map = {}
    for task in tasks:
        values = task.get("values", {})
        task_id = values.get("任务 ID", [{}])[0].get("text", "")
        status = values.get("状态", [{}])[0].get("text", "")
        task_status_map[task_id] = status
    
    # 过滤出待办任务
    pending = []
    for task in tasks:
        values = task.get("values", {})
        status = values.get("状态", [{}])[0].get("text", "")
        if status == "待办":
            task_id = values.get("任务 ID", [{}])[0].get("text", "")
            task_name = values.get("任务名称", [{}])[0].get("text", "")
            priority = values.get("优先级", [{}])[0].get("text", "P2")
            owner = values.get("负责人", [{}])[0].get("text", "")
            deps_str = values.get("前置依赖", [{}])[0].get("text", "")
            
            # 解析依赖
            depends_on = []
            if deps_str:
                depends_on = [d.strip() for d in deps_str.split(",")]
            
            pending.append({
                "id": task_id,
                "title": task_name,
                "priority": priority,
                "owner": owner,
                "depends_on": depends_on
            })
    
    if not pending:
        return None
    
    # 检查依赖是否满足
    def deps_met(task):
        if not task["depends_on"]:
            return True
        
        # 检查依赖任务是否已完成
        for dep_id in task["depends_on"]:
            dep_status = task_status_map.get(dep_id, "")
            if dep_status != "已完成":
                return False
        return True
    
    available = [t for t in pending if deps_met(t)]
    
    if not available:
        return None
    
    # 按优先级排序
    priority_order = {"P0": 0, "P1": 1, "P2": 2}
    available.sort(key=lambda t: priority_order.get(t["priority"], 2))
    
    return available[0]


def print_next_task():
    """打印下一个可执行任务"""
    task = get_next_task()
    
    if task:
        print("\n🚀 下一个任务:")
        print(f"ID: {task['id']}")
        print(f"标题：{task['title']}")
        print(f"优先级：{task['priority']}")
        print(f"负责人：{task.get('owner', '未分配')}")
        if task.get('depends_on'):
            print(f"依赖：{', '.join(task['depends_on'])}")
        print()
    else:
        print("\n✅ 没有待处理的任务\n")


# ==================== P1 功能：任务删除 ====================

def delete_task(task_id: str, agent_id: str = "") -> bool:
    """
    删除任务
    
    Args:
        task_id: 任务 ID
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 删除成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    task = get_task_by_id(task_id, agent_id)
    if not task:
        print(f"❌ 任务不存在：{task_id}")
        return False
    
    record_id = task["record_id"]
    
    result = run_mcporter_with_retry("smartsheet_delete_records", {
        "docid": DOCID,
        "sheet_id": SHEET_ID,
        "record_ids": [record_id]
    })
    
    if result and result.get("errcode") == 0:
        print(f"✅ 任务已删除：{task_id}")
        return True
    else:
        print(f"❌ 任务删除失败：{result}")
        return False


def delete_goal(goal_id: str, agent_id: str = "") -> bool:
    """
    删除目标及关联任务
    
    Args:
        goal_id: 目标 ID
        agent_id: 调用者 agent ID（用于访问控制）
    
    Returns:
        bool: 删除成功返回 True
    """
    # 访问控制检查
    if not check_access(agent_id):
        print(f"❌ 访问拒绝：agent '{agent_id}' 没有权限")
        return False
    
    # 获取所有任务
    tasks = get_all_tasks(agent_id)
    
    # 找到属于该目标的所有任务
    goal_tasks = []
    for task in tasks:
        values = task.get("values", {})
        tid = values.get("任务 ID", [{}])[0].get("text", "")
        if tid.startswith(f"{goal_id}-"):
            goal_tasks.append(task)
    
    print(f"🗑️ 准备删除目标 {goal_id} 及其 {len(goal_tasks)} 个关联任务")
    
    # 删除所有任务
    success_count = 0
    for task in goal_tasks:
        tid = task["values"].get("任务 ID", [{}])[0].get("text", "")
        if delete_task(tid):
            success_count += 1
    
    print(f"✅ 已删除 {success_count}/{len(goal_tasks)} 个任务")
    return True


# ==================== P1 功能：到期提醒 ====================

def check_due_tasks(days: int = 3) -> List[dict]:
    """
    检查即将到期的任务
    
    Args:
        days: 检查未来 N 天
    
    Returns:
        即将到期的任务列表
    """
    tasks = get_all_tasks()
    due_tasks = []
    now = datetime.now()
    
    for task in tasks:
        values = task.get("values", {})
        status = values.get("状态", [{}])[0].get("text", "")
        
        # 只检查进行中和待办的任务
        if status not in ["进行中", "待办"]:
            continue
        
        # 获取截止时间
        deadline_val = values.get("截止时间", "")
        if not deadline_val:
            continue
        
        try:
            # 解析时间戳（13 位毫秒）
            deadline_ts = int(deadline_val)
            deadline = datetime.fromtimestamp(deadline_ts / 1000)
            
            # 计算剩余天数
            delta = deadline - now
            remaining_days = delta.days
            
            # 如果即将到期（默认 3 天内）
            if 0 <= remaining_days <= days:
                due_tasks.append({
                    "task": task,
                    "remaining_days": remaining_days,
                    "deadline": deadline
                })
        except Exception as e:
            print(f"⚠️ 解析截止时间失败：{deadline_val}, 错误：{e}")
            continue
    
    # 按剩余天数排序
    due_tasks.sort(key=lambda x: x["remaining_days"])
    
    print(f"⏰ 检查未来 {days} 天到期的任务")
    print(f"✅ 找到 {len(due_tasks)} 个即将到期的任务")
    
    for item in due_tasks:
        task = item["task"]
        values = task.get("values", {})
        tid = values.get("任务 ID", [{}])[0].get("text", "")
        name = values.get("任务名称", [{}])[0].get("text", "")
        owner = values.get("负责人", [{}])[0].get("text", "")
        remaining = item["remaining_days"]
        
        if remaining == 0:
            print(f"  🔴 今日到期：{tid} - {name}（负责人：{owner}）")
        elif remaining == 1:
            print(f"  🟠 明天到期：{tid} - {name}（负责人：{owner}）")
        else:
            print(f"  🟡 {remaining}天后到期：{tid} - {name}（负责人：{owner}）")
    
    return due_tasks


def check_overdue_tasks() -> List[dict]:
    """
    检查已超期的任务
    
    Returns:
        超期任务列表
    """
    tasks = get_all_tasks()
    overdue_tasks = []
    now = datetime.now()
    
    for task in tasks:
        values = task.get("values", {})
        status = values.get("状态", [{}])[0].get("text", "")
        
        # 只检查进行中和待办的任务
        if status not in ["进行中", "待办"]:
            continue
        
        # 获取截止时间
        deadline_val = values.get("截止时间", "")
        if not deadline_val:
            continue
        
        try:
            # 解析时间戳（13 位毫秒）
            deadline_ts = int(deadline_val)
            deadline = datetime.fromtimestamp(deadline_ts / 1000)
            
            # 如果已超期
            if deadline < now:
                delta = now - deadline
                overdue_days = delta.days
                overdue_tasks.append({
                    "task": task,
                    "overdue_days": overdue_days,
                    "deadline": deadline
                })
        except Exception as e:
            print(f"⚠️ 解析截止时间失败：{deadline_val}, 错误：{e}")
            continue
    
    # 按超期天数排序
    overdue_tasks.sort(key=lambda x: x["overdue_days"], reverse=True)
    
    print(f"⚠️ 检查超期任务")
    print(f"✅ 找到 {len(overdue_tasks)} 个超期任务")
    
    for item in overdue_tasks:
        task = item["task"]
        values = task.get("values", {})
        tid = values.get("任务 ID", [{}])[0].get("text", "")
        name = values.get("任务名称", [{}])[0].get("text", "")
        owner = values.get("负责人", [{}])[0].get("text", "")
        overdue = item["overdue_days"]
        
        print(f"  🔴 超期 {overdue}天：{tid} - {name}（负责人：{owner}）")
    
    return overdue_tasks


# ==================== P2 功能：数据统计 ====================

def get_statistics() -> Dict[str, Any]:
    """
    获取任务统计数据
    
    Returns:
        统计数据字典
    """
    tasks = get_all_tasks()
    
    # 基础统计
    total = len(tasks)
    status_count = {"待办": 0, "进行中": 0, "已完成": 0, "已取消": 0}
    type_count = {}
    owner_count = {}
    priority_count = {"P0": 0, "P1": 0, "P2": 0}
    
    completed_count = 0
    
    for task in tasks:
        values = task.get("values", {})
        
        # 状态统计
        status = values.get("状态", [{}])[0].get("text", "未知")
        if status in status_count:
            status_count[status] += 1
        
        if status == "已完成":
            completed_count += 1
        
        # 任务类型统计
        task_type = values.get("任务类型", [{}])[0].get("text", "未知")
        type_count[task_type] = type_count.get(task_type, 0) + 1
        
        # 负责人统计
        owner = values.get("负责人", [{}])[0].get("text", "未分配")
        owner_count[owner] = owner_count.get(owner, 0) + 1
        
        # 优先级统计
        priority = values.get("优先级", [{}])[0].get("text", "P2")
        if priority in priority_count:
            priority_count[priority] += 1
    
    # 计算按时完成率（简化版）
    on_time_rate = (completed_count / total * 100) if total > 0 else 0
    
    stats = {
        "总任务数": total,
        "已完成": status_count["已完成"],
        "进行中": status_count["进行中"],
        "待办": status_count["待办"],
        "已取消": status_count["已取消"],
        "按时完成率": f"{on_time_rate:.1f}%",
        "按优先级": priority_count,
        "按负责人": owner_count,
        "按类型": type_count
    }
    
    return stats


def print_statistics():
    """打印统计数据"""
    stats = get_statistics()
    
    print("=" * 60)
    print("📊 任务统计数据")
    print("=" * 60)
    print(f"总任务数：{stats['总任务数']}")
    print(f"✅ 已完成：{stats['已完成']}")
    print(f"🔄 进行中：{stats['进行中']}")
    print(f"⏸️ 待办：{stats['待办']}")
    print(f"❌ 已取消：{stats['已取消']}")
    print(f"📈 按时完成率：{stats['按时完成率']}")
    print()
    print("按优先级:")
    for priority, count in stats['按优先级'].items():
        print(f"  {priority}: {count}")
    print()
    print("按负责人:")
    for owner, count in sorted(stats['按负责人'].items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {owner}: {count}")
    print()
    print("按类型:")
    for task_type, count in sorted(stats['按类型'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {task_type}: {count}")
    print("=" * 60)


# ==================== CLI 入口 ====================

def main():
    """CLI 入口"""
    if len(sys.argv) < 2:
        print("用法：python task_manager.py <command> [args]")
        print("\n可用命令:")
        print("\n📋 任务管理:")
        print("  list                  - 列出所有任务")
        print("  report                - 生成状态报告")
        print("  stats                 - 查看统计数据")
        print("  concurrency           - 查看并发状态 ⭐ 新增")
        print("  create <id> <name>    - 创建任务")
        print("  start <id>            - 开始任务（受并发限制）")
        print("  progress <id> <num>   - 更新进度")
        print("  complete <id>         - 完成任务")
        print("  query <id>            - 查询任务")
        print("  edit <id> <field=value>  - 编辑任务")
        print("  delete <id>           - 删除任务")
        print("  search <keyword>      - 搜索任务")
        print("  filter [status=xxx] [owner=xxx] [priority=xxx] - 过滤任务")
        print("  due [days]            - 检查即将到期的任务")
        print("  overdue               - 检查超期任务")
        print("\n🎯 目标管理:")
        print("  create-goal <id> <title> [priority] [context]  - 创建目标")
        print("  decompose <goal_id> <task_title> [priority] [depends_on] - 分解目标为任务")
        print("  goals                 - 列出所有目标")
        print("  next-task             - 获取下一个可执行任务")
        print("  delete-goal <id>      - 删除目标及关联任务")
        return 1
    
    command = sys.argv[1]
    
    if command == "list":
        tasks = get_all_tasks()
        print(f"共 {len(tasks)} 个任务:")
        for task in tasks:
            values = task.get("values", {})
            tid = values.get("任务 ID", [{}])[0].get("text", "")
            name = values.get("任务名称", [{}])[0].get("text", "")
            status = values.get("状态", [{}])[0].get("text", "")
            print(f"  {tid}: {name} [{status}]")
    
    elif command == "report":
        print_status_report()
    
    elif command == "create" and len(sys.argv) >= 4:
        task_id = sys.argv[2]
        task_name = sys.argv[3]
        description = sys.argv[4] if len(sys.argv) > 4 else f"任务：{task_name}"
        result = create_task(task_id, task_name, "文档", description=description)
        if not result.get("success"):
            sys.exit(1)
    
    elif command == "start" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        start_task(task_id)
    
    elif command == "progress" and len(sys.argv) >= 4:
        task_id = sys.argv[2]
        progress = int(sys.argv[3])
        update_progress(task_id, progress)
    
    elif command == "complete" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        complete_task(task_id)
    
    elif command == "query" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        task = get_task_by_id(task_id)
        if task:
            print(f"任务：{task_id}")
            values = task.get("values", {})
            for key, val in values.items():
                if isinstance(val, list) and len(val) > 0:
                    if isinstance(val[0], dict):
                        print(f"  {key}: {val[0].get('text', val[0])}")
                    else:
                        print(f"  {key}: {val[0]}")
                else:
                    print(f"  {key}: {val}")
        else:
            print(f"任务不存在：{task_id}")
    
    # 目标管理命令
    elif command == "create-goal" and len(sys.argv) >= 4:
        goal_id = sys.argv[2]
        title = sys.argv[3]
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        context = sys.argv[5] if len(sys.argv) > 5 else ""
        create_goal(goal_id, title, priority, context)
    
    elif command == "decompose" and len(sys.argv) >= 4:
        goal_id = sys.argv[2]
        task_title = sys.argv[3]
        priority = sys.argv[4] if len(sys.argv) > 4 else "medium"
        depends_on = sys.argv[5].split(",") if len(sys.argv) > 5 and sys.argv[5] != "-" else None
        decompose_goal(goal_id, task_title, priority=priority, depends_on=depends_on)
    
    elif command == "goals":
        print_goals()
    
    elif command == "next-task":
        print_next_task()
    
    elif command == "delete-goal" and len(sys.argv) >= 3:
        goal_id = sys.argv[2]
        delete_goal(goal_id)
    
    # 新增功能命令
    elif command == "stats":
        print_statistics()
    
    elif command == "edit" and len(sys.argv) >= 4:
        task_id = sys.argv[2]
        # 解析 field=value 格式
        fields = {}
        for arg in sys.argv[3:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                fields[key] = value
        if fields:
            edit_task(task_id, fields)
        else:
            print("❌ 请提供至少一个 field=value 参数")
    
    elif command == "delete" and len(sys.argv) >= 3:
        task_id = sys.argv[2]
        delete_task(task_id)
    
    elif command == "search" and len(sys.argv) >= 3:
        keyword = sys.argv[2]
        search_tasks(keyword)
    
    elif command == "filter":
        # 解析 filter 参数
        kwargs = {}
        for arg in sys.argv[2:]:
            if "=" in arg:
                key, value = arg.split("=", 1)
                kwargs[key] = value
        filter_tasks(**kwargs)
    
    elif command == "due":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        check_due_tasks(days)
    
    elif command == "overdue":
        check_overdue_tasks()
    
    elif command == "concurrency":
        # 查看并发状态
        count = get_in_progress_count()
        print(f"📊 当前并发状态")
        print(f"   进行中任务：{count}/{MAX_CONCURRENT_TASKS}")
        print(f"   可用槽位：{MAX_CONCURRENT_TASKS - count}")
        
        # 列出进行中的任务
        tasks = get_all_tasks()
        print(f"\n🔄 进行中任务列表:")
        for task in tasks:
            values = task.get("values", {})
            status = values.get("状态", [{}])[0].get("text", "")
            if status == "进行中":
                tid = values.get("任务 ID", [{}])[0].get("text", "")
                name = values.get("任务名称", [{}])[0].get("text", "")
                owner = values.get("负责人", [{}])[0].get("text", "")
                progress = values.get("进度", 0)
                print(f"   - {tid}: {name} (负责人：{owner}, 进度：{progress}%)")
    
    else:
        print(f"未知命令或参数不足：{command}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
