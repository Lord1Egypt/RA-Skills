"""
Podcast Generator - 服务管理脚本

用法:
    python3 server.py --status    # 检查服务状态
    python3 server.py --start     # 启动服务
    python3 server.py --stop      # 停止服务
    python3 server.py --restart   # 重启服务
"""

import argparse
import json
import os
import subprocess
import sys
import time
import signal
from pathlib import Path

# 配置
PROJECT_DIR = Path("/home/wang/桌面/龙虾工作区/podcast-generator")
APP_PATH = PROJECT_DIR / "backend" / "app.py"
API_BASE = "http://localhost:5000"
PID_FILE = Path("/tmp/podcast-generator.pid")
LOG_FILE = Path("/tmp/podcast-generator.log")


def check_server_status() -> dict:
    """检查服务状态"""
    
    import requests
    
    status = {
        "running": False,
        "url": API_BASE,
        "pid": None,
        "ffmpeg": False,
        "tts": False,
    }
    
    # 检查 PID 文件
    if PID_FILE.exists():
        try:
            pid = int(PID_FILE.read_text().strip())
            # 检查进程是否存在
            os.kill(pid, 0)  # 信号 0 只是检查，不实际发送
            status["pid"] = pid
        except (ProcessLookupError, ValueError):
            # 进程不存在，清理 PID 文件
            PID_FILE.unlink(missing_ok=True)
    
    # 检查 API 是否响应
    try:
        response = requests.get(f"{API_BASE}/api/config", timeout=3)
        if response.status_code == 200:
            status["running"] = True
            data = response.json()
            status["ffmpeg"] = data.get("ffmpeg_available", False)
            status["tts"] = data.get("tts_available", False)
    except:
        pass
    
    return status


def start_server() -> dict:
    """启动服务"""
    
    # 先检查是否已运行
    status = check_server_status()
    if status["running"]:
        return {
            "success": True,
            "message": "服务已运行",
            "url": API_BASE,
            "pid": status["pid"],
        }
    
    # 启动 Flask
    log_file = open(LOG_FILE, "w")
    
    process = subprocess.Popen(
        ["python3", str(APP_PATH)],
        stdout=log_file,
        stderr=log_file,
        start_new_session=True,  # 新 session，不受父进程退出影响
    )
    
    # 保存 PID
    PID_FILE.write_text(str(process.pid))
    
    # 等待服务启动
    print("正在启动服务...", end=" ")
    
    for i in range(15):
        time.sleep(1)
        status = check_server_status()
        if status["running"]:
            print("✅")
            return {
                "success": True,
                "message": "服务启动成功",
                "url": API_BASE,
                "pid": process.pid,
            }
        print(".", end="", flush=True)
    
    print("❌")
    return {
        "success": False,
        "message": "服务启动超时",
        "log": str(LOG_FILE),
    }


def stop_server() -> dict:
    """停止服务"""
    
    status = check_server_status()
    
    if not status["running"]:
        # 服务未运行
        PID_FILE.unlink(missing_ok=True)
        return {
            "success": True,
            "message": "服务未运行",
        }
    
    # 发送 SIGTERM
    pid = status["pid"]
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            
            # 等待进程退出
            for _ in range(10):
                time.sleep(0.5)
                try:
                    os.kill(pid, 0)
                except ProcessLookupError:
                    # 进程已退出
                    PID_FILE.unlink(missing_ok=True)
                    return {
                        "success": True,
                        "message": "服务已停止",
                    }
            
            # 强制 kill
            os.kill(pid, signal.SIGKILL)
            PID_FILE.unlink(missing_ok=True)
            return {
                "success": True,
                "message": "服务已强制停止",
            }
            
        except ProcessLookupError:
            PID_FILE.unlink(missing_ok=True)
            return {
                "success": True,
                "message": "服务已停止",
            }
    
    return {
        "success": False,
        "message": "无法停止服务（PID 未知）",
    }


def restart_server() -> dict:
    """重启服务"""
    
    # 先停止
    stop_result = stop_server()
    if not stop_result["success"]:
        return stop_result
    
    # 等待完全停止
    time.sleep(2)
    
    # 启动
    return start_server()


def main():
    """命令行入口"""
    
    parser = argparse.ArgumentParser(
        description="播客生成器 - 服务管理",
    )
    
    parser.add_argument(
        "--status",
        action="store_true",
        help="检查服务状态",
    )
    
    parser.add_argument(
        "--start",
        action="store_true",
        help="启动服务",
    )
    
    parser.add_argument(
        "--stop",
        action="store_true",
        help="停止服务",
    )
    
    parser.add_argument(
        "--restart",
        action="store_true",
        help="重启服务",
    )
    
    args = parser.parse_args()
    
    # 默认显示状态
    if not (args.status or args.start or args.stop or args.restart):
        args.status = True
    
    result = {}
    
    if args.status:
        status = check_server_status()
        result = {
            "command": "status",
            "running": status["running"],
            "url": API_BASE,
            "pid": status["pid"],
            "ffmpeg": status["ffmpeg"],
            "tts": status["tts"],
        }
        
        if status["running"]:
            result["message"] = "✅ 服务运行中"
        else:
            result["message"] = "❌ 服务未运行"
    
    elif args.start:
        result = start_server()
        result["command"] = "start"
    
    elif args.stop:
        result = stop_server()
        result["command"] = "stop"
    
    elif args.restart:
        result = restart_server()
        result["command"] = "restart"
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 退出码
    if result.get("success") or result.get("running"):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()