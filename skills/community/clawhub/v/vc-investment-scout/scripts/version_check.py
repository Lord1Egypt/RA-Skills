#!/usr/bin/env python3
"""
版本检查与自动更新提醒

检查本地vc-investment-scout版本与ClawHub最新版本，如落后则提醒用户更新。
"""

import os
import sys
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_VERSION_FILE = os.path.join(SCRIPT_DIR, "VERSION")
SLUG = "vc-investment-scout"

def get_local_version():
    """读取本地版本号"""
    if os.path.exists(LOCAL_VERSION_FILE):
        with open(LOCAL_VERSION_FILE) as f:
            return f.read().strip()
    return "0.0.0"

def get_remote_version():
    """查询ClawHub最新版本"""
    try:
        result = subprocess.run(
            ["clawhub", "inspect", SLUG],
            capture_output=True, text=True, timeout=15
        )
        for line in result.stdout.split("\n"):
            line = line.strip()
            if line.startswith("Latest:"):
                return line.split(":", 1)[1].strip()
    except Exception:
        pass
    return None

def compare_versions(v1, v2):
    """比较两个版本号，v1 < v2 返回 True"""
    try:
        parts1 = [int(x) for x in v1.split(".")]
        parts2 = [int(x) for x in v2.split(".")]
        return parts1 < parts2
    except Exception:
        return False

def check():
    """
    检查版本，返回结果字典
    
    Returns:
        {
            "local": "1.2.0",
            "remote": "1.3.0", 
            "update_available": True,
            "message": "有新版本 v1.3.0 可用，请执行 clawhub update vc-investment-scout"
        }
    """
    local = get_local_version()
    remote = get_remote_version()
    
    if remote is None:
        return {
            "local": local,
            "remote": None,
            "update_available": False,
            "message": "无法检查远程版本（网络问题或ClawHub不可达）"
        }
    
    if compare_versions(local, remote):
        return {
            "local": local,
            "remote": remote,
            "update_available": True,
            "message": f"VC投资筛选工具有新版本 v{remote} 可用（当前 v{local}），请执行：clawhub update {SLUG}"
        }
    
    return {
        "local": local,
        "remote": remote,
        "update_available": False,
        "message": f"已是最新版本 v{local}"
    }

if __name__ == "__main__":
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
