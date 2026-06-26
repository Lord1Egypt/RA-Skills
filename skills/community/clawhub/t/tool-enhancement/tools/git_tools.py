#!/usr/bin/env python3
"""
Git 操作工具集

提供完整的 Git 操作能力
参考 Claude Code 的 Git 工具设计
"""

from __future__ import annotations

import os
import asyncio
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

import sys
sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


class GitStatusTool(BaseTool):
    """Git 状态工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_status",
            description="查看 Git 仓库状态",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "short": {"type": "boolean", "default": False, "description": "简短格式"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "status", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        short = kwargs.get("short", False)
        
        try:
            repo_path = Path(path)
            if not (repo_path / ".git").exists():
                return ToolResult(success=False, error=f"不是 Git 仓库: {path}")
            
            cmd = ["git", "-C", str(repo_path), "status"]
            if short:
                cmd.append("--short")
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            return ToolResult(
                success=True,
                data={
                    "status": stdout.decode(),
                    "path": str(repo_path.absolute())
                }
            )
            
        except FileNotFoundError:
            return ToolResult(success=False, error="Git 未安装")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitLogTool(BaseTool):
    """Git 日志工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_log",
            description="查看 Git 提交日志",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "limit": {"type": "integer", "default": 10, "description": "提交数量"},
                    "oneline": {"type": "boolean", "default": False, "description": "单行格式"},
                    "author": {"type": "string", "description": "按作者过滤"},
                    "since": {"type": "string", "description": "起始日期"},
                    "until": {"type": "string", "description": "结束日期"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "log", "history", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        limit = kwargs.get("limit", 10)
        oneline = kwargs.get("oneline", False)
        author = kwargs.get("author")
        
        try:
            repo_path = Path(path)
            if not (repo_path / ".git").exists():
                return ToolResult(success=False, error=f"不是 Git 仓库: {path}")
            
            cmd = ["git", "-C", str(repo_path), "log", f"-n{limit}", "--format=%H|%an|%ae|%ad|%s"]
            if oneline:
                cmd.append("--oneline")
            if author:
                cmd.extend(["--author", author])
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            commits = []
            for line in stdout.decode().strip().split("\n"):
                if not line:
                    continue
                if "|" in line:
                    parts = line.split("|")
                    if len(parts) == 5:
                        commits.append({
                            "hash": parts[0][:8],
                            "author": parts[1],
                            "email": parts[2],
                            "date": parts[3],
                            "message": parts[4]
                        })
            
            return ToolResult(
                success=True,
                data={
                    "commits": commits,
                    "count": len(commits)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitDiffTool(BaseTool):
    """Git 差异工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_diff",
            description="查看 Git 差异",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "commit": {"type": "string", "description": "比较的提交"},
                    "cached": {"type": "boolean", "default": False, "description": "暂存区差异"},
                    "stat": {"type": "boolean", "default": False, "description": "统计信息"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "diff", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        commit = kwargs.get("commit")
        cached = kwargs.get("cached", False)
        stat = kwargs.get("stat", False)
        
        try:
            repo_path = Path(path)
            
            cmd = ["git", "-C", str(repo_path), "diff"]
            if cached:
                cmd.append("--cached")
            if stat:
                cmd.append("--stat")
            if commit:
                cmd.append(commit)
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            return ToolResult(
                success=proc.returncode == 0,
                data={
                    "diff": stdout.decode(),
                    "path": str(repo_path.absolute())
                },
                metadata={"returncode": proc.returncode}
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitCommitTool(BaseTool):
    """Git 提交工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_commit",
            description="提交更改到 Git 仓库",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "message": {"type": "string", "description": "提交信息"},
                    "all": {"type": "boolean", "default": True, "description": "提交所有修改"},
                    "amend": {"type": "boolean", "default": False, "description": "修改上次提交"},
                    "author": {"type": "string", "description": "作者信息"}
                },
                "required": ["message"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "commit", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        message = kwargs.get("message")
        all_changes = kwargs.get("all", True)
        amend = kwargs.get("amend", False)
        author = kwargs.get("author")
        
        try:
            repo_path = Path(path)
            
            # 先 add 所有文件
            if all_changes:
                add_proc = await asyncio.create_subprocess_exec(
                    "git", "-C", str(repo_path), "add", "-A",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                await add_proc.communicate()
            
            # 构建 commit 命令
            cmd = ["git", "-C", str(repo_path), "commit", "-m", message]
            if amend:
                cmd.append("--amend")
            if author:
                cmd.extend(["--author", author])
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            # 获取 commit hash
            hash_proc = await asyncio.create_subprocess_exec(
                "git", "-C", str(repo_path), "rev-parse", "HEAD",
                stdout=asyncio.subprocess.PIPE
            )
            hash_stdout, _ = await hash_proc.communicate()
            commit_hash = hash_stdout.decode().strip()[:8]
            
            return ToolResult(
                success=True,
                data={
                    "commit": commit_hash,
                    "message": message,
                    "path": str(repo_path.absolute())
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitPushTool(BaseTool):
    """Git 推送工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_push",
            description="推送提交到远程仓库",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "remote": {"type": "string", "default": "origin", "description": "远程名称"},
                    "branch": {"type": "string", "description": "分支名称"},
                    "force": {"type": "boolean", "default": False, "description": "强制推送"},
                    "set_upstream": {"type": "boolean", "default": False, "description": "设置上游"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "push", "remote", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        remote = kwargs.get("remote", "origin")
        branch = kwargs.get("branch")
        force = kwargs.get("force", False)
        set_upstream = kwargs.get("set_upstream", False)
        
        try:
            repo_path = Path(path)
            
            cmd = ["git", "-C", str(repo_path), "push"]
            if force:
                cmd.append("--force")
            if set_upstream:
                cmd.append("-u")
            if remote:
                cmd.append(remote)
            if branch:
                cmd.append(branch)
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            return ToolResult(
                success=True,
                data={
                    "remote": remote,
                    "branch": branch or "current",
                    "pushed": True,
                    "output": stdout.decode()
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitPullTool(BaseTool):
    """Git 拉取工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_pull",
            description="从远程仓库拉取更新",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "remote": {"type": "string", "default": "origin", "description": "远程名称"},
                    "branch": {"type": "string", "description": "分支名称"},
                    "rebase": {"type": "boolean", "default": False, "description": "使用 rebase"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "pull", "remote", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        remote = kwargs.get("remote", "origin")
        branch = kwargs.get("branch")
        rebase = kwargs.get("rebase", False)
        
        try:
            repo_path = Path(path)
            
            cmd = ["git", "-C", str(repo_path), "pull"]
            if rebase:
                cmd.append("--rebase")
            if remote:
                cmd.append(remote)
            if branch:
                cmd.append(branch)
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            return ToolResult(
                success=True,
                data={
                    "remote": remote,
                    "branch": branch or "current",
                    "pulled": True,
                    "output": stdout.decode()
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitBranchTool(BaseTool):
    """Git 分支工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_branch",
            description="管理 Git 分支",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "action": {"type": "string", "enum": ["list", "create", "delete", "checkout"], "description": "操作"},
                    "name": {"type": "string", "description": "分支名称"},
                    "force": {"type": "boolean", "default": False, "description": "强制操作"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "branch", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        action = kwargs.get("action", "list")
        name = kwargs.get("name")
        force = kwargs.get("force", False)
        
        try:
            repo_path = Path(path)
            
            cmd = ["git", "-C", str(repo_path), "branch"]
            
            if action == "list":
                cmd.append("-a")
            elif action == "create" and name:
                cmd.extend(["-c", name])
            elif action == "delete" and name:
                if force:
                    cmd.extend(["-D", name])
                else:
                    cmd.extend(["-d", name])
            elif action == "checkout" and name:
                cmd = ["git", "-C", str(repo_path), "checkout", name]
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            branches = [b.strip().replace("* ", "") for b in stdout.decode().strip().split("\n") if b.strip()]
            
            return ToolResult(
                success=True,
                data={
                    "action": action,
                    "branches": branches,
                    "count": len(branches)
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GitRemoteTool(BaseTool):
    """Git 远程仓库工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="git_remote",
            description="管理 Git 远程仓库",
            input_schema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "仓库路径", "default": "."},
                    "action": {"type": "string", "enum": ["list", "add", "remove"], "description": "操作"},
                    "name": {"type": "string", "description": "远程名称"},
                    "url": {"type": "string", "description": "远程 URL"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["git", "remote", "vcs"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        path = kwargs.get("path", ".")
        action = kwargs.get("action", "list")
        name = kwargs.get("name")
        url = kwargs.get("url")
        
        try:
            repo_path = Path(path)
            
            if action == "list":
                cmd = ["git", "-C", str(repo_path), "remote", "-v"]
            elif action == "add" and name and url:
                cmd = ["git", "-C", str(repo_path), "remote", "add", name, url]
            elif action == "remove" and name:
                cmd = ["git", "-C", str(repo_path), "remote", "remove", name]
            else:
                return ToolResult(success=False, error="无效参数")
            
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                return ToolResult(success=False, error=stderr.decode())
            
            remotes = []
            for line in stdout.decode().strip().split("\n"):
                if line:
                    parts = line.split()
                    if len(parts) >= 2:
                        remotes.append({"name": parts[0], "url": parts[1], "type": parts[2] if len(parts) > 2 else ""})
            
            return ToolResult(
                success=True,
                data={
                    "action": action,
                    "remotes": remotes
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
GIT_TOOLS = [
    GitStatusTool,
    GitLogTool,
    GitDiffTool,
    GitCommitTool,
    GitPushTool,
    GitPullTool,
    GitBranchTool,
    GitRemoteTool,
]


def register_tools(registry):
    """注册所有 Git 工具到注册表"""
    for tool_class in GIT_TOOLS:
        tool = tool_class()
        registry.register(tool, "vcs")
    return len(GIT_TOOLS)