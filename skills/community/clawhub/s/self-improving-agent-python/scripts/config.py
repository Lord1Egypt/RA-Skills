#!/usr/bin/env python3
"""
Self-Improvement Agent Configuration
自动检测当前工作区并设置路径
"""

import os
import json
import glob
from pathlib import Path
from typing import Optional

# 默认工作区目录
DEFAULT_OPENCLAW_DIR = os.path.expanduser("~/.workbuddy")
SELF_IMPROVEMENT_DIR = "self-improvement"
SHARED_CONTEXT_DIR = "shared-context/self-improvement"


def get_workspace() -> str:
    """检测当前工作区"""
    openclaw_dir = DEFAULT_OPENCLAW_DIR
    
    if not os.path.exists(openclaw_dir):
        raise FileNotFoundError(f"WorkBuddy directory not found: {openclaw_dir}")
    
    # 查找所有 workspace-* 目录
    workspaces = [d for d in glob.glob(os.path.join(openclaw_dir, "workspace-*")) 
                 if os.path.isdir(d)]
    
    if not workspaces:
        # 尝试当前工作目录
        cwd = os.getcwd()
        if DEFAULT_OPENCLAW_DIR in cwd:
            return os.path.dirname(cwd)
        raise FileNotFoundError("No workspace found in .workbuddy directory")
    
    if len(workspaces) == 1:
        return workspaces[0]
    
    # 多个工作区，通过当前目录判断
    cwd = os.getcwd()
    for ws in workspaces:
        if cwd.startswith(ws):
            return ws
    
    # 默认返回第一个
    return workspaces[0]


def get_self_improvement_dir() -> str:
    """获取自我改进数据目录"""
    workspace = get_workspace()
    si_dir = os.path.join(workspace, SELF_IMPROVEMENT_DIR)
    os.makedirs(si_dir, exist_ok=True)
    return si_dir


def get_shared_context_dir() -> str:
    """获取共享知识目录"""
    workspace = get_workspace()
    shared_dir = os.path.join(workspace, SHARED_CONTEXT_DIR)
    os.makedirs(shared_dir, exist_ok=True)
    return shared_dir


def load_json(filepath: str, default: dict = None) -> dict:
    """加载 JSON 文件"""
    if default is None:
        default = {"evaluations": []} if "evaluation" in filepath else {"lessons": []}
    
    if not os.path.exists(filepath):
        return default
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return default


def save_json(filepath: str, data: dict) -> None:
    """保存 JSON 文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(f"Workspace: {get_workspace()}")
    print(f"Self-Improvement Dir: {get_self_improvement_dir()}")
    print(f"Shared Context Dir: {get_shared_context_dir()}")
