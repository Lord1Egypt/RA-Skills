"""
Windows应用启动器脚本
支持通过PowerShell启动各种Windows应用程序
"""

import subprocess
import json
import sys
from pathlib import Path

def start_app(app_path, arguments=None, working_dir=None, wait=False, timeout=30):
    """
    启动Windows应用程序

    Args:
        app_path (str): 应用程序路径(可以是可执行文件、URL或已注册应用名称)
        arguments (str, optional): 启动参数
        working_dir (str, optional): 工作目录
        wait (bool): 是否等待应用退出
        timeout (int): 等待超时时间(秒)

    Returns:
        dict: 操作结果
    """
    try:
        # 构建PowerShell命令
        ps_cmd = f"Start-Process -FilePath '{app_path}'"

        if arguments:
            ps_cmd += f" -ArgumentList '{arguments}'"

        if working_dir:
            ps_cmd += f" -WorkingDirectory '{working_dir}'"

        if wait:
            ps_cmd += f" -Wait -Timeout {timeout}"

        # 执行PowerShell命令
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True,
            timeout=timeout + 10
        )

        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully started: {app_path}",
                "output": result.stdout
            }
        else:
            return {
                "success": False,
                "message": f"Failed to start: {app_path}",
                "error": result.stderr
            }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": f"Timeout after {timeout} seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error: {str(e)}"
        }

def open_url(url):
    """
    打开URL(使用默认浏览器)

    Args:
        url (str): URL地址

    Returns:
        dict: 操作结果
    """
    return start_app(url, arguments="")

def list_running_processes():
    """
    列出所有运行的进程

    Returns:
        dict: 操作结果
    """
    try:
        ps_cmd = "Get-Process | Select-Object Name, Id, Path | ConvertTo-Json"
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            processes = json.loads(result.stdout)
            return {
                "success": True,
                "processes": processes
            }
        else:
            return {
                "success": False,
                "error": result.stderr
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def kill_app(process_name):
    """
    强制结束应用

    Args:
        process_name (str): 进程名称

    Returns:
        dict: 操作结果
    """
    try:
        ps_cmd = f"Stop-Process -Name '{process_name}' -Force"
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            return {
                "success": True,
                "message": f"Successfully killed: {process_name}"
            }
        else:
            return {
                "success": False,
                "message": f"Failed to kill: {process_name}",
                "error": result.stderr
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    # 示例用法
    if len(sys.argv) < 2:
        print("Usage: python app_launcher.py <command> [args...]")
        print("Commands: start, url, list, kill")
        sys.exit(1)

    command = sys.argv[1]

    if command == "start" and len(sys.argv) >= 3:
        result = start_app(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif command == "url" and len(sys.argv) >= 3:
        result = open_url(sys.argv[2])
        print(json.dumps(result, indent=2))
    elif command == "list":
        result = list_running_processes()
        print(json.dumps(result, indent=2))
    elif command == "kill" and len(sys.argv) >= 3:
        result = kill_app(sys.argv[2])
        print(json.dumps(result, indent=2))
    else:
        print("Invalid command or missing arguments")
        sys.exit(1)
