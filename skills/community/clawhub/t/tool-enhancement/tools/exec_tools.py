#!/usr/bin/env python3
"""
Shell 执行工具集

提供命令执行、后台进程、sudo 等能力
参考 Claude Code 的 shell 执行工具设计
"""

from __future__ import annotations

import os
import sys
import asyncio
import subprocess
import shlex
import signal
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor

# 复用 schema.py 的基础类
import sys as _sys
_sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class ShellCommandTool(BaseTool):
    """Shell 命令执行工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="shell_exec",
            description="执行 Shell 命令，返回标准输出和错误",
            input_schema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要执行的命令"},
                    "cwd": {"type": "string", "description": "工作目录"},
                    "timeout": {"type": "number", "default": 30, "description": "超时秒数"},
                    "env": {"type": "object", "description": "环境变量"},
                    "shell": {"type": "boolean", "default": True, "description": "使用 shell"}
                },
                "required": ["command"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["shell", "exec", "command", "bash"],
            examples=[
                "执行命令: command='ls -la'",
                "带超时: command='sleep 10', timeout=5"
            ]
        ))
        self._executor = ThreadPoolExecutor(max_workers=10)
    
    async def execute(self, **kwargs) -> ToolResult:
        command = kwargs.get("command")
        cwd = kwargs.get("cwd")
        timeout = kwargs.get("timeout", 30)
        env = kwargs.get("env")
        use_shell = kwargs.get("shell", True)
        
        try:
            # 安全检查：禁止危险命令
            dangerous = ["rm -rf /", "mkfs", "dd if=/dev/zero", ":(){:|:&};:"]
            for d in dangerous:
                if d in command:
                    return ToolResult(success=False, error=f"危险命令被拒绝: {d}")
            
            # 构建环境
            cmd_env = os.environ.copy()
            if env:
                cmd_env.update(env)
            
            # 执行命令
            loop = asyncio.get_event_loop()
            
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd,
                env=cmd_env
            )
            
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                return ToolResult(success=False, error=f"命令超时 ({timeout}s)")
            
            return ToolResult(
                success=process.returncode == 0,
                data={
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "returncode": process.returncode,
                    "command": command
                },
                metadata={"timeout": timeout}
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class BackgroundProcessTool(BaseTool):
    """后台进程工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="shell_background",
            description="在后台启动进程，返回进程 ID",
            input_schema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要执行的命令"},
                    "cwd": {"type": "string", "description": "工作目录"},
                    "name": {"type": "string", "description": "进程名称"},
                    "log_file": {"type": "string", "description": "日志文件路径"}
                },
                "required": ["command"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["shell", "background", "daemon", "process"]
        ))
        self._processes: Dict[str, asyncio.subprocess.Process] = {}
    
    async def execute(self, **kwargs) -> ToolResult:
        command = kwargs.get("command")
        cwd = kwargs.get("cwd")
        name = kwargs.get("name", f"bg_{int(time.time())}")
        log_file = kwargs.get("log_file")
        
        try:
            # 启动进程
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                log_fd = open(log_file, "w")
                
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=log_fd,
                    stderr=asyncio.subprocess.STDOUT,
                    cwd=cwd
                )
            else:
                process = await asyncio.create_subprocess_shell(
                    command,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL,
                    cwd=cwd
                )
            
            self._processes[name] = process
            
            return ToolResult(
                success=True,
                data={
                    "pid": process.pid,
                    "name": name,
                    "running": process.returncode is None,
                    "log_file": log_file
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    def is_running(self, name: str) -> bool:
        """检查进程是否在运行"""
        if name not in self._processes:
            return False
        return self._processes[name].returncode is None
    
    def kill(self, name: str) -> bool:
        """终止后台进程"""
        if name in self._processes:
            proc = self._processes[name]
            if proc.returncode is None:
                proc.kill()
                return True
        return False


class ProcessListTool(BaseTool):
    """进程列表工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="process_list",
            description="列出正在运行的进程",
            input_schema={
                "type": "object",
                "properties": {
                    "user": {"type": "string", "description": "按用户过滤"},
                    "keyword": {"type": "string", "description": "按关键字过滤"},
                    "limit": {"type": "integer", "default": 20}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["process", "ps", "list"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        user = kwargs.get("user")
        keyword = kwargs.get("keyword")
        limit = kwargs.get("limit", 20)
        
        try:
            cmd = ["ps", "aux"]
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await proc.communicate()
            
            lines = stdout.decode().strip().split("\n")[1:]  # 跳过表头
            processes = []
            
            for line in lines[:limit]:
                parts = line.split(None, 10)
                if len(parts) >= 11:
                    proc_info = {
                        "user": parts[0],
                        "pid": parts[1],
                        "cpu": parts[2],
                        "mem": parts[3],
                        "command": parts[10]
                    }
                    
                    # 过滤
                    if user and proc_info["user"] != user:
                        continue
                    if keyword and keyword.lower() not in proc_info["command"].lower():
                        continue
                    
                    processes.append(proc_info)
            
            return ToolResult(
                success=True,
                data={
                    "processes": processes,
                    "count": len(processes)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ProcessKillTool(BaseTool):
    """进程终止工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="process_kill",
            description="终止进程",
            input_schema={
                "type": "object",
                "properties": {
                    "pid": {"type": "integer", "description": "进程 ID"},
                    "force": {"type": "boolean", "default": False, "description": "强制终止"},
                    "signal": {"type": "string", "default": "TERM", "description": "信号"}
                },
                "required": ["pid"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["process", "kill", "terminate"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        pid = kwargs.get("pid")
        force = kwargs.get("force", False)
        signal_name = kwargs.get("signal", "TERM")
        
        try:
            sig = getattr(signal, f"SIG{signal_name}", signal.SIGTERM)
            
            if force:
                os.kill(pid, signal.SIGKILL)
            else:
                os.kill(pid, sig)
            
            return ToolResult(
                success=True,
                data={"pid": pid, "signal": signal_name, "killed": True}
            )
            
        except ProcessLookupError:
            return ToolResult(success=False, error=f"进程不存在: {pid}")
        except PermissionError:
            return ToolResult(success=False, error=f"权限不足: {pid}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SudoCommandTool(BaseTool):
    """sudo 命令执行工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="shell_sudo",
            description="使用 sudo 执行特权命令",
            input_schema={
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "要执行的命令"},
                    "password": {"type": "string", "description": "sudo 密码（可选，默认从 stdin 读取）"},
                    "timeout": {"type": "number", "default": 30}
                },
                "required": ["command"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["shell", "sudo", "root", "privilege"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        command = kwargs.get("command")
        password = kwargs.get("password")
        timeout = kwargs.get("timeout", 30)
        
        try:
            # 构建 sudo 命令
            sudo_cmd = f"sudo {command}"
            
            # 如果提供了密码，使用 -S 从 stdin 读取
            if password:
                full_cmd = f"echo {shlex.quote(password)} | sudo -S {command}"
            else:
                full_cmd = sudo_cmd
            
            process = await asyncio.create_subprocess_shell(
                full_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if not password else asyncio.subprocess.DEVNULL
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
            
            return ToolResult(
                success=process.returncode == 0,
                data={
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "returncode": process.returncode
                },
                metadata={"used_password": bool(password)}
            )
            
        except asyncio.TimeoutError:
            return ToolResult(success=False, error="命令超时")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ScriptRunnerTool(BaseTool):
    """脚本运行工具 - 支持 Python/Bash/Node"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="script_run",
            description="运行脚本文件 (Python/Bash/Node)",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "脚本路径"},
                    "interpreter": {"type": "string", "description": "解释器 (auto/python/bash/node)"},
                    "args": {"type": "array", "description": "脚本参数"},
                    "env": {"type": "object", "description": "环境变量"},
                    "timeout": {"type": "number", "default": 60}
                },
                "required": ["path"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["script", "run", "python", "bash", "node"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path")
        interpreter = kwargs.get("interpreter", "auto")
        args = kwargs.get("args", [])
        env = kwargs.get("env")
        timeout = kwargs.get("timeout", 60)
        
        try:
            script_path = Path(path)
            if not script_path.exists():
                return ToolResult(success=False, error=f"脚本不存在: {path}")
            
            # 自动检测解释器
            if interpreter == "auto":
                ext = script_path.suffix.lower()
                if ext == ".py":
                    interpreter = "python"
                elif ext in [".sh", ".bash"]:
                    interpreter = "bash"
                elif ext == ".js":
                    interpreter = "node"
                else:
                    return ToolResult(success=False, error=f"无法自动检测解释器: {ext}")
            
            # 构建命令
            cmd = [interpreter, str(script_path)] + args
            
            # 环境变量
            cmd_env = os.environ.copy()
            if env:
                cmd_env.update(env)
            
            # 执行
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=cmd_env
            )
            
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(),
                timeout=timeout
            )
            
            return ToolResult(
                success=proc.returncode == 0,
                data={
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": stderr.decode("utf-8", errors="replace"),
                    "returncode": proc.returncode,
                    "interpreter": interpreter
                },
                metadata={"script": path, "timeout": timeout}
            )
            
        except asyncio.TimeoutError:
            return ToolResult(success=False, error=f"脚本执行超时: {timeout}s")
        except FileNotFoundError:
            return ToolResult(success=False, error=f"解释器不存在: {interpreter}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SystemInfoTool(BaseTool):
    """系统信息工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="system_info",
            description="获取系统信息",
            input_schema={
                "type": "object",
                "properties": {
                    "detail": {"type": "boolean", "default": False, "description": "详细信息"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["system", "info", "os", "kernel"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        detail = kwargs.get("detail", False)
        
        try:
            import platform
            import socket
            
            info = {
                "hostname": socket.gethostname(),
                "os": platform.system(),
                "os_version": platform.version(),
                "os_release": platform.release(),
                "arch": platform.machine(),
                "python_version": platform.python_version(),
                "processor": platform.processor(),
            }
            
            if detail:
                # CPU 信息
                try:
                    with open("/proc/cpuinfo", "r") as f:
                        cpu_lines = [l for l in f.readlines() if "model name" in l]
                        if cpu_lines:
                            info["cpu_model"] = cpu_lines[0].split(":")[1].strip()
                except:
                    pass
                
                # 内存信息
                try:
                    with open("/proc/meminfo", "r") as f:
                        mem_lines = f.readlines()
                        for line in mem_lines:
                            if line.startswith("MemTotal:"):
                                info["memory_total"] = line.split()[1]
                            elif line.startswith("MemAvailable:"):
                                info["memory_available"] = line.split()[1]
                except:
                    pass
            
            return ToolResult(success=True, data=info)
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
EXEC_TOOLS = [
    ShellCommandTool,
    BackgroundProcessTool,
    ProcessListTool,
    ProcessKillTool,
    SudoCommandTool,
    ScriptRunnerTool,
    SystemInfoTool,
]


def register_tools(registry):
    """注册所有执行工具到注册表"""
    for tool_class in EXEC_TOOLS:
        tool = tool_class()
        registry.register(tool, "execute")
    return len(EXEC_TOOLS)