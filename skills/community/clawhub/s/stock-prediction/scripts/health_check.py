#!/usr/bin/env python3
"""
服务健康检查与自启动脚本
"""
import time
import subprocess
import sys
from pathlib import Path

# 路径常量
BACKEND_DIR = r"C:\Users\Administrator\Desktop\kronos\kronos-ai\backend"
HEALTH_URL = "http://localhost:8000/health"
TARGET_MODEL = "kronos-base"
CONDA_ENV = "my_project_env"


def check_health():
    """检查服务健康状态"""
    import urllib.request
    import json
    
    try:
        req = urllib.request.Request(HEALTH_URL, method='GET')
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('status') == 'healthy', data
    except Exception as e:
        print(f"Health check failed: {e}")
        return False, None


def start_service():
    """启动服务"""
    print("服务未运行，正在启动...")
    
    cmd = f'conda activate {CONDA_ENV} && python .\\main.py'
    
    # 使用 PowerShell 启动
    subprocess.Popen(
        ['powershell', '-Command', cmd],
        cwd=BACKEND_DIR,
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    
    print(f"服务启动中... 等待 10 秒")
    time.sleep(10)


def ensure_service():
    """确保服务正常运行"""
    healthy, data = check_health()
    
    if healthy:
        print(f"服务正常运行，当前模型: {data.get('model', {}).get('model', 'unknown')}")
        return data
    
    # 尝试启动服务
    start_service()
    
    # 重试检查（最多3次）
    for i in range(3):
        healthy, data = check_health()
        if healthy:
            print("服务启动成功")
            return data
        print(f"等待服务就绪... ({i+1}/3)")
        time.sleep(5)
    
    raise RuntimeError("服务启动失败，请检查后端配置")


if __name__ == "__main__":
    try:
        result = ensure_service()
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
