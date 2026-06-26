#!/usr/bin/env python3
"""
shell_embed.py - Skill Shell Embedding

在 prompt 或配置中支持 !command 语法，
执行命令并将结果注入上下文。

用法：
    python3 shell_embed.py "!git status"
    python3 shell_embed.py "!pwd && !ls -la"

特性：
    - 识别 !command 格式
    - 支持多命令链 (!cmd1 && !cmd2)
    - 安全白名单模式（仅允许预定义命令）
    - 超时控制
    - 结果自动格式化
"""

import subprocess
import shlex
import re
import sys
import os
from typing import Optional

# 安全白名单 - 仅允许这些命令（可扩展）
ALLOWED_COMMANDS = {
    # Git
    "git": ["status", "log", "diff", "branch", "remote -v", "tag"],
    # 系统信息
    "pwd": [],
    "whoami": [],
    "date": [],
    "uptime": [],
    "df": ["-h"],
    "free": ["-h"],
    "ls": ["-la", "-l", "-a"],
    "ps": ["aux"],
    "top": ["-bn1"],
    # 网络
    "ping": ["-c 3 127.0.0.1"],
    "curl": ["-s", "-I"],
    # 文件
    "cat": [],
    "head": [],
    "tail": [],
    "wc": [],
    "find": [],
    "grep": [],
    # Python/脚本
    "python3": ["--version"],
    "node": ["--version"],
    "npm": ["--version", "list"],
    # OpenClaw
    "openclaw": ["status", "gateway status"],
}

# 超时时间（秒）
DEFAULT_TIMEOUT = 10

# 禁止的模式
FORBIDDEN_PATTERNS = ["$(", "`", "&&", "||", ">>", "<<", ">|", ";"]


def parse_shell_commands(text: str) -> list:
    r"""
    从文本中解析 !command 格式的命令
    
    示例：
        "!git status" -> ["git status"]
        "!pwd && !ls -la" -> ["pwd", "ls -la"]
    """
    # 匹配 !command 格式，支持 && 链式
    # 匹配 ! 开头到 &&、下一个 !、字符串结尾或 } 之前
    pattern = r'!([^!]+?)(?=\s*&&\s*!|\s*!|\s*$|\})'
    matches = re.findall(pattern, text)
    # 清理每个命令
    commands = []
    for cmd in matches:
        cmd = cmd.strip()
        # 移除开头的 ! 如果有
        if cmd.startswith('!'):
            cmd = cmd[1:]
        if cmd and cmd not in commands:
            commands.append(cmd)
    return commands


def is_command_safe(cmd: str, allowed_commands: dict) -> bool:
    """
    检查命令是否在白名单中
    """
    parts = cmd.strip().split()
    if not parts:
        return False
    
    command = parts[0]
    
    # 完全匹配
    if command in allowed_commands:
        return True
    
    # 别名检查
    aliases = {
        "ll": "ls",
        "la": "ls",
        "dir": "ls",
    }
    if aliases.get(command) in allowed_commands:
        return True
    
    return False


def execute_command(cmd: str, timeout: int = DEFAULT_TIMEOUT, cwd: Optional[str] = None) -> dict:
    """
    执行单个命令，返回结果
    
    返回:
        {
            "success": bool,
            "output": str,
            "error": str,
            "returncode": int
        }
    """
    try:
        # 安全检查：检查禁止的模式
        for pattern in FORBIDDEN_PATTERNS:
            if pattern in cmd:
                return {
                    "success": False,
                    "output": "",
                    "error": f"Forbidden pattern '{pattern}' not allowed",
                    "returncode": 1
                }
        
        # 使用 shlex.split 解析命令
        parts = shlex.split(cmd)
        if not parts:
            return {"success": False, "output": "", "error": "Empty command", "returncode": 1}
        
        command = parts[0]
        args = parts[1:]
        
        # 白名单检查
        if command not in ALLOWED_COMMANDS and command not in ["ll", "la", "dir"]:
            return {
                "success": False,
                "output": "",
                "error": f"Command '{command}' is not in whitelist",
                "returncode": 1
            }
        
        # 简单命令：用列表形式，shell=False 更安全
        result = subprocess.run(
            [command] + args,
            shell=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=cwd
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout.strip(),
            "error": result.stderr.strip(),
            "returncode": result.returncode
        }
        
    except subprocess.TimeoutExpired:
        return {"success": False, "output": "", "error": f"Command timed out after {timeout}s", "returncode": 124}
    except Exception as e:
        return {"success": False, "output": "", "error": str(e), "returncode": 1}


def embed_shell_commands(text: str, cwd: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT) -> str:
    """
    主函数：从文本中解析并执行所有 !command，返回增强后的文本
    
    示例输入：
        "当前目录：!pwd\nGit状态：!git status"
    
    示例输出：
        当前目录：/home/user/project
        Git状态：
        On branch main
        Your branch is up to date with 'origin/main'.
    """
    commands = parse_shell_commands(text)
    
    if not commands:
        return text
    
    results = {}
    for cmd in commands:
        result = execute_command(cmd, timeout=timeout, cwd=cwd)
        results[cmd] = result
    
    # 替换文本中的 !command 为执行结果
    output = text
    for cmd, result in results.items():
        # 构造替换文本
        if result["success"]:
            replacement = result["output"]
        else:
            replacement = f"[执行失败] {result['error']}"
        
        # 替换第一个匹配
        pattern = rf'!{re.escape(cmd)}'
        output = re.sub(pattern, replacement, output, count=1)
        
        # 也处理 && 链式
        if "&&" in output:
            # 链式命令整体执行
            pass
    
    return output


def format_results_for_context(results: dict) -> str:
    """
    格式化结果，便于注入上下文
    """
    if not results:
        return ""
    
    lines = ["```"]
    lines.append("# Shell 执行结果")
    for cmd, result in results.items():
        lines.append(f"$ {cmd}")
        if result["success"]:
            if result["output"]:
                lines.append(result["output"])
            else:
                lines.append("(无输出)")
        else:
            lines.append(f"[错误] {result['error']}")
        lines.append("")
    
    lines.append("```")
    return "\n".join(lines)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("Usage: python3 shell_embed.py '!command' [text with !commands]")
        print("\nExamples:")
        print("  python3 shell_embed.py '!git status'")
        print("  python3 shell_embed.py '!pwd' 'Current dir: !pwd'")
        sys.exit(1)
    
    # 单命令模式
    if len(sys.argv) == 2:
        cmd = sys.argv[1].strip()
        if cmd.startswith("!"):
            cmd = cmd[1:]
        result = execute_command(cmd)
        if result["success"]:
            print(result["output"])
        else:
            print(f"[错误] {result['error']}", file=sys.stderr)
            sys.exit(1)
    else:
        # 嵌入模式
        text = " ".join(sys.argv[1:])
        output = embed_shell_commands(text)
        print(output)


if __name__ == "__main__":
    main()
