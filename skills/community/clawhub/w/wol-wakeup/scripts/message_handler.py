#!/usr/bin/env python3
"""
WoL 消息处理器（支持工作流模式）
处理微信消息，匹配关键词并执行相应动作
支持多轮对话工作流
"""

import json
import re
import sys
import os
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from wol_manager import add_device, remove_device, list_devices, wake_device
from workflow_engine import engine, WorkflowResult
from wol_workflow import init_wol_workflows

# 初始化工作流
init_wol_workflows()


def get_session_id_from_message(message_data: dict) -> str:
    """
    从消息数据中提取会话 ID
    优先使用 sender_id，如果没有则使用 conversation_id
    """
    # 微信消息通常有 sender 或 from_user
    if isinstance(message_data, dict):
        return (
            message_data.get('sender_id') or
            message_data.get('from_user_id') or
            message_data.get('conversation_id') or
            message_data.get('session_id') or
            'default_session'
        )
    return str(message_data)


def parse_message(text):
    """
    解析消息内容，返回动作和参数
    返回：(action, params) 或 (None, None)
    """
    if not text:
        return None, None
    
    text = text.strip()
    
    # 1. 开机命令（不带参数）- 列出设备
    if text in ['帮我开机', '电脑开机', '开电脑', '开机']:
        return 'list', {}
    
    # 2. 开机 - 设备名/编号
    match = re.match(r'^开机 [-\s]+(.+)$', text)
    if match:
        identifier = match.group(1).strip()
        return 'wake', {'identifier': identifier}
    
    # 3. 添加网络唤醒|MAC|备注（传统单行模式）
    match = re.match(r'^添加网络唤醒\|([0-9A-Fa-f:]+)\|?(.*)$', text)
    if match:
        mac = match.group(1).strip()
        note = match.group(2).strip() if match.group(2) else ''
        name = note if note else f"设备_{mac.replace(':', '').upper()[-6:]}"
        return 'add', {'name': name, 'mac': mac, 'note': note}
    
    # 3b. 启动添加设备工作流
    if text in ['添加网络唤醒', '添加设备', '新增设备']:
        return 'start_add_workflow', {}
    
    # 4. 列表/设备列表
    if text in ['列表', '设备列表']:
        return 'list', {}
    
    # 5. 删除 - 设备名（传统单行模式）
    match = re.match(r'^删除 [-\s]+(.+)$', text)
    if match:
        name = match.group(1).strip()
        return 'remove', {'name': name}
    
    # 5b. 启动删除设备工作流
    if text in ['删除设备', '移除设备']:
        return 'start_remove_workflow', {}
    
    return None, None


def handle_message(text, session_id: str = None):
    """
    处理消息，返回回复文本
    支持工作流模式和传统模式
    """
    if not session_id:
        session_id = 'default_session'
    
    # 1. 检查是否处于工作流中
    session_state = engine.state_manager.get_session(session_id)
    if session_state:
        # 用户正在工作流中，所有消息都交给工作流处理
        result_type, response = engine.process_message(session_id, text)
        return response
    
    # 2. 不在工作流中，解析命令
    action, params = parse_message(text)
    
    if action is None:
        return None  # 不匹配任何命令
    
    # 3. 处理工作流启动命令
    if action == 'start_add_workflow':
        response = engine.start_workflow(session_id, "wol_add_device", timeout_seconds=60)
        return response
    
    elif action == 'start_remove_workflow':
        response = engine.start_workflow(session_id, "wol_remove_device", timeout_seconds=60)
        return response
    
    # 4. 处理传统命令
    if action == 'list':
        return list_devices()
    
    elif action == 'add':
        success, msg = add_device(params['name'], params['mac'], params['note'])
        return msg
    
    elif action == 'remove':
        success, msg = remove_device(params['name'])
        return msg
    
    elif action == 'wake':
        success, msg = wake_device(params['identifier'])
        return msg
    
    return "未知命令"


def handle_openclaw_message(message_data: dict):
    """
    处理 OpenClaw message 工具传入的消息
    支持从 message_data 中提取会话 ID 和文本内容
    """
    # 提取会话 ID
    session_id = get_session_id_from_message(message_data)
    
    # 提取消息文本
    text = None
    if isinstance(message_data, dict):
        text = (
            message_data.get('text') or
            message_data.get('content') or
            message_data.get('message') or
            message_data.get('body')
        )
    
    if not text:
        return None
    
    return handle_message(text, session_id)


def check_timeouts():
    """检查并清理超时会话"""
    return engine.check_timeouts()


def get_session_info(session_id: str):
    """获取会话信息（用于调试）"""
    return engine.get_session_status(session_id)


def main():
    """命令行测试"""
    if len(sys.argv) < 2:
        print("用法：python3 message_handler.py <消息文本> [会话 ID]")
        print("示例:")
        print('  python3 message_handler.py "帮我开机"')
        print('  python3 message_handler.py "开机 - 我的电脑"')
        print('  python3 message_handler.py "添加网络唤醒" user123  # 启动工作流')
        print('  python3 message_handler.py "测试电脑" user123      # 工作流中输入')
        sys.exit(1)
    
    text = sys.argv[1]
    session_id = sys.argv[2] if len(sys.argv) > 2 else 'cli_test'
    
    response = handle_message(text, session_id)
    
    if response:
        print(response)
    else:
        print("（未匹配 WoL 命令）")


if __name__ == '__main__':
    main()
