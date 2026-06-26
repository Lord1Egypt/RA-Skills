#!/usr/bin/env python3
"""
Zworker API 客户端
提供与zworker HTTP接口交互的通用函数
"""

import json
import sys
import time
from typing import Optional, Dict, Any, List, Union

# 尝试导入requests，如果不可用则使用urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.parse
    HAS_REQUESTS = False

# 配置
BASE_URL = "http://localhost:18803"
TIMEOUT = 10  # 秒

class ZworkerAPIError(Exception):
    """Zworker API 错误"""
    pass

def _make_request(method: str, endpoint: str, params: Optional[Dict] = None, 
                  data: Optional[Dict] = None) -> Dict[str, Any]:
    """
    发送HTTP请求到zworker API
    
    Args:
        method: HTTP方法 ('GET' 或 'POST')
        endpoint: API端点 (如 '/control/getTaskList')
        params: URL查询参数
        data: POST请求的JSON数据
    
    Returns:
        解析后的JSON响应
    
    Raises:
        ZworkerAPIError: 请求失败或响应格式错误
    """
    url = f"{BASE_URL}{endpoint}"
    
    if HAS_REQUESTS:
        # 使用requests库
        try:
            if method.upper() == 'GET':
                response = requests.get(url, params=params, timeout=TIMEOUT)
            else:  # POST
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, params=params, json=data, 
                                        headers=headers, timeout=TIMEOUT)
            response.raise_for_status()
            result = response.json()
        except requests.exceptions.RequestException as e:
            raise ZworkerAPIError(f"HTTP请求失败: {e}")
        except json.JSONDecodeError as e:
            raise ZworkerAPIError(f"响应JSON解析失败: {e}")
    else:
        # 使用urllib (备用方案)
        try:
            if params:
                # 构建查询字符串
                from urllib.parse import urlencode
                url = f"{url}?{urlencode(params)}"
            
            req_data = None
            headers = {}
            if method.upper() == 'POST' and data:
                req_data = json.dumps(data).encode('utf-8')
                headers = {'Content-Type': 'application/json'}
            
            req = urllib.request.Request(url, data=req_data, headers=headers, method=method.upper())
            with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
                response_data = response.read().decode('utf-8')
                result = json.loads(response_data)
        except urllib.error.URLError as e:
            raise ZworkerAPIError(f"HTTP请求失败: {e}")
        except json.JSONDecodeError as e:
            raise ZworkerAPIError(f"响应JSON解析失败: {e}")
    
    # 检查业务逻辑成功标志
    if isinstance(result, dict) and 'success' in result and not result['success']:
        error_msg = result.get('message', '未知错误')
        raise ZworkerAPIError(f"业务逻辑失败: {error_msg}")
    
    return result

# ==================== 任务管理 ====================

def get_task_list(name: Optional[str] = None, page_number: int = 0, limit: int = 24) -> Dict[str, Any]:
    """
    获取任务列表
    
    Args:
        name: 任务名称模糊匹配
        page_number: 页码 (从0开始)
        limit: 每页数量
    
    Returns:
        {'tasks': list, 'total': int, 'pageNumber': int, 'limit': int}
    """
    params = {}
    if name:
        params['name'] = name
    if page_number is not None:
        params['pageNumber'] = page_number
    if limit is not None:
        params['limit'] = limit
    
    return _make_request('GET', '/control/getTaskList', params=params)

def run_task(task_id: Optional[int] = None, task_name: Optional[str] = None) -> Dict[str, Any]:
    """
    执行任务
    
    Args:
        task_id: 任务ID
        task_name: 任务名称
    
    Returns:
        {'success': True} 或 {'success': False, 'message': str}
    
    Note:
        task_id 和 task_name 至少提供一个
    """
    data = {}
    if task_id is not None:
        data['id'] = task_id
    if task_name:
        data['name'] = task_name
    
    if not data:
        raise ValueError("必须提供 task_id 或 task_name 之一")
    
    return _make_request('POST', '/control/runTask', data=data)

# ==================== 定时计划管理 ====================

def get_schedule_list(name: Optional[str] = None, page_number: int = 0, limit: int = 24) -> Dict[str, Any]:
    """
    获取定时计划列表
    
    Args:
        name: 计划名称模糊匹配
        page_number: 页码 (从0开始)
        limit: 每页数量
    
    Returns:
        {'schedules': list, 'total': int, 'pageNumber': int, 'limit': int}
    """
    params = {}
    if name:
        params['name'] = name
    if page_number is not None:
        params['pageNumber'] = page_number
    if limit is not None:
        params['limit'] = limit
    
    return _make_request('GET', '/control/getScheduleList', params=params)

def set_schedule(enable: bool, schedule_id: Optional[int] = None, schedule_name: Optional[str] = None) -> Dict[str, Any]:
    """
    启动或关闭定时计划
    
    Args:
        enable: True表示启动，False表示关闭
        schedule_id: 计划ID
        schedule_name: 计划名称
    
    Returns:
        {'success': True} 或 {'success': False, 'message': str}
    
    Note:
        schedule_id 和 schedule_name 至少提供一个
    """
    data = {'enable': 1 if enable else 0}
    if schedule_id is not None:
        data['id'] = schedule_id
    if schedule_name:
        data['name'] = schedule_name
    
    if not ('id' in data or 'name' in data):
        raise ValueError("必须提供 schedule_id 或 schedule_name 之一")
    
    return _make_request('POST', '/control/setSchedule', data=data)

# ==================== 消息通知 ====================

def get_claw_message(claw_type: str) -> Dict[str, Any]:
    """
    获取通知信息
    
    Args:
        claw_type: claw类型，如 'openClaw', 'QClaw' 等
    
    Returns:
        {'success': True, 'channel': str, 'userid': str, 'message': str} 或 {'success': False, 'message': str}
    """
    params = {'clawType': claw_type}
    return _make_request('GET', '/control/getClawMessage', params=params)

# ==================== 系统配置 ====================

def set_user_info(users: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    同步用户信息到zworker
    
    Args:
        users: 用户列表，每个元素为 {'channel': 'xxx', 'userid': 'xxx'}
    
    Returns:
        {'success': True} 或 {'success': False, 'message': str}
    """
    data = {'users': users}
    return _make_request('POST', '/control/setClawUserInfo', data=data)

def set_cron_id(cron_id: str, claw_type: str) -> Dict[str, Any]:
    """
    传输Cron ID到zworker
    
    Args:
        cron_id: cron任务ID
        claw_type: claw类型，如 'openClaw', 'QClaw' 等
    
    Returns:
        {'success': True} 或 {'success': False, 'message': str}
    """
    data = {'id': cron_id, 'clawType': claw_type}
    return _make_request('POST', '/control/setClawCronId', data=data)

# ==================== 辅助函数 ====================

def health_check() -> bool:
    """检查zworker服务是否可用"""
    try:
        # 尝试获取任务列表（空参数）
        get_task_list(limit=1)
        return True
    except Exception:
        return False

def format_task_list(tasks: List[Dict]) -> str:
    """格式化任务列表为list字符串"""
    if not tasks:
        return "暂无任务"
    
    lines = []
    
    for task in tasks:
        task_id = task.get('id', 'N/A')
        task_name = task.get('name', 'N/A')
        lines.append(f"- {task_name}（任务ID：{task_id}）")
    
    return "\n".join(lines)

def format_schedule_list(schedules: List[Dict]) -> str:
    """格式化定时计划列表为list字符串"""
    if not schedules:
        return "暂无定时计划"
    
    lines = []
    
    for schedule in schedules:
        schedule_id = schedule.get('id', 'N/A')
        schedule_name = schedule.get('name', 'N/A')
        schedule_status = schedule.get('status', 'N/A')
        lines.append(f"- {schedule_name}（计划ID：{schedule_id}，状态：{schedule_status}）")
    
    return "\n".join(lines)

# ==================== 命令行接口 ====================

if __name__ == "__main__":
    # 简单测试
    import argparse
    
    parser = argparse.ArgumentParser(description='Zworker API 客户端')
    parser.add_argument('--health', action='store_true', help='健康检查')
    parser.add_argument('--tasks', action='store_true', help='获取任务列表')
    parser.add_argument('--schedules', action='store_true', help='获取定时计划列表')
    
    args = parser.parse_args()
    
    try:
        if args.health:
            if health_check():
                print("✅ Zworker服务正常")
                sys.exit(0)
            else:
                print("❌ Zworker服务不可用")
                sys.exit(1)
        
        if args.tasks:
            result = get_task_list(limit=5)
            tasks = result.get('tasks', [])
            print(f"任务总数: {result.get('total', 0)}")
            print(format_task_list(tasks))
        
        if args.schedules:
            result = get_schedule_list(limit=5)
            schedules = result.get('schedules', [])
            print(f"计划总数: {result.get('total', 0)}")
            print(format_schedule_list(schedules))
            
    except ZworkerAPIError as e:
        print(f"错误: {e}")
        sys.exit(1)