#!/usr/bin/env python3
"""
subagent_isolation.py - 子 Agent 工具隔离

参考 Hermes Agent 的 DelegateTool 隔离机制：
- 子 Agent 禁止的工具列表
- 工作空间路径验证
- 进度回调机制
- 并行委托限制

用途：
    - 子 Agent 安全隔离
    - 防止恶意工具调用
    - 资源限制
"""

import asyncio
import logging
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# ============================================================================
# 常量
# ============================================================================

# 子 Agent 永远禁止的工具（参考 Hermes Agent）
DELEGATE_BLOCKED_TOOLS: Set[str] = {
    "delegate_task",   # 禁止递归委托
    "clarify",         # 禁止用户交互
    "memory",          # 禁止写入共享记忆
    "send_message",    # 禁止跨平台副作用
    "execute_code",    # 应推理而非写脚本
    "sudo",            # 禁止提权
    "shell_elevated",  # 禁止提升权限
    "delete_memory",   # 禁止删除记忆
    "admin_tools",     # 禁止管理工具
}

# 允许的工具（白名单模式）
DELEGATE_ALLOWED_TOOLS: Set[str] = {
    "terminal",        # 终端命令
    "file_read",       # 读文件
    "file_write",      # 写文件
    "file_list",       # 列出目录
    "web_search",      # 搜索
    "web_fetch",       # 获取网页
    "run_script",      # 运行脚本
}

# 并行限制
MAX_CONCURRENT_CHILDREN = 3
MAX_DEPTH = 2  # parent(0) -> child(1) -> grandchild(2, 拒绝)


# ============================================================================
# 数据结构
# ============================================================================

@dataclass
class IsolationConfig:
    """隔离配置"""
    blocked_tools: Set[str] = field(default_factory=lambda: DELEGATE_BLOCKED_TOOLS.copy())
    allowed_tools: Optional[Set[str]] = None  # None 表示允许所有非 blocked
    max_depth: int = MAX_DEPTH
    max_concurrent: int = MAX_CONCURRENT_CHILDREN
    workspace_validation: bool = True
    progress_callback: Optional[Callable] = None


@dataclass
class SubAgentResult:
    """子 Agent 结果"""
    success: bool
    output: str
    error: Optional[str] = None
    tools_used: List[str] = field(default_factory=list)
    tokens_consumed: int = 0


# ============================================================================
# 工具隔离器
# ============================================================================

class ToolIsolation:
    """工具隔离器"""
    
    def __init__(self, config: Optional[IsolationConfig] = None):
        self.config = config or IsolationConfig()
        self._used_tools: List[str] = []
    
    def is_allowed(self, tool_name: str) -> bool:
        """检查工具是否允许"""
        # 检查黑名单
        if tool_name in self.config.blocked_tools:
            logger.warning(f"Tool {tool_name} is blocked")
            return False
        
        # 检查白名单（如果设置）
        if self.config.allowed_tools is not None:
            return tool_name in self.config.allowed_tools
        
        return True
    
    def filter_tools(self, tools: List[str]) -> List[str]:
        """过滤工具列表"""
        allowed = []
        for tool in tools:
            if self.is_allowed(tool):
                allowed.append(tool)
            else:
                logger.info(f"Filtered out blocked tool: {tool}")
        return allowed
    
    def record_tool_use(self, tool_name: str):
        """记录工具使用"""
        self._used_tools.append(tool_name)
    
    @property
    def tools_used(self) -> List[str]:
        return self._used_tools.copy()


# ============================================================================
# 工作空间验证
# ============================================================================

def validate_workspace_path(path: str, allowed_base: Optional[str] = None) -> tuple[bool, Optional[str]]:
    """
    验证工作空间路径。
    
    Returns:
        (is_valid, error_message)
    """
    if not path:
        return False, "Path is empty"
    
    p = Path(path)
    
    # 检查绝对路径
    if not p.is_absolute():
        return False, "Must be absolute path"
    
    # 检查是否在允许的基础目录下
    if allowed_base:
        try:
            p.resolve().relative_to(Path(allowed_base).resolve())
        except ValueError:
            return False, f"Path must be within {allowed_base}"
    
    # 检查是否存在
    if not p.exists():
        return False, "Path does not exist"
    
    return True, None


def resolve_workspace_hint(cwd: Optional[str] = None) -> Optional[str]:
    """
    解析真实本地路径，避免误教容器路径。
    
    参考 Hermes Agent 的 _resolve_workspace_hint
    """
    candidates = [
        os.getenv("TERMINAL_CWD"),
        cwd,
        os.getcwd(),
    ]
    
    for candidate in candidates:
        if candidate and Path(candidate).is_absolute() and Path(candidate).exists():
            return str(Path(candidate).resolve())
    
    return None


# ============================================================================
# 子 Agent 构建器
# ============================================================================

class SubAgentBuilder:
    """子 Agent 构建器"""
    
    def __init__(
        self,
        goal: str,
        context: str,
        parent_cwd: Optional[str] = None,
        config: Optional[IsolationConfig] = None,
    ):
        self.goal = goal
        self.context = context
        self.config = config or IsolationConfig()
        self.isolation = ToolIsolation(self.config)
        self.parent_cwd = resolve_workspace_hint(parent_cwd)
    
    def build_system_prompt(self) -> str:
        """构建子 Agent 系统提示"""
        parts = [
            "You are a focused subagent working on a specific delegated task.",
            "",
            f"YOUR TASK:\n{self.goal}",
            "",
            f"CONTEXT:\n{self.context}",
            "",
            "RULES:",
            "1. Complete the task without asking for confirmation",
            "2. Report progress and result clearly",
            "3. If blocked, explain why and suggest alternatives",
            "4. Do NOT ask the user for clarification",
            "5. Do NOT delegate to other agents",
            "6. Do NOT use tools outside the allowed list",
            "",
        ]
        
        if self.parent_cwd:
            parts.append(f"WORKSPACE PATH:\n{self.parent_cwd}")
            parts.append("")
        
        parts.append("AVAILABLE TOOLS:")
        allowed = list(self.config.allowed_tools or ["terminal", "file", "web"])
        parts.append(", ".join(allowed))
        parts.append("")
        
        parts.append("BLOCKED TOOLS:")
        parts.append(", ".join(sorted(self.config.blocked_tools)))
        parts.append("")
        
        return "\n".join(parts)
    
    def get_allowed_tools(self) -> List[str]:
        """获取允许的工具列表"""
        if self.config.allowed_tools:
            return self.isolation.filter_tools(list(self.config.allowed_tools))
        
        # 默认返回常用工具
        return ["terminal", "file_read", "file_write", "web_search"]


# ============================================================================
# 并行委托管理
# ============================================================================

class DelegationPool:
    """委托池，管理并行子 Agent"""
    
    def __init__(self, max_concurrent: int = MAX_CONCURRENT_CHILDREN):
        self.max_concurrent = max_concurrent
        self._active: Dict[str, asyncio.Task] = {}
        self._results: Dict[str, SubAgentResult] = {}
    
    async def submit(self, agent_id: str, coro) -> SubAgentResult:
        """提交子 Agent 任务"""
        # 检查并发限制
        while len(self._active) >= self.max_concurrent:
            # 等待一个完成
            done, _ = await asyncio.wait(
                self._active.values(),
                return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                agent_id_finished = None
                for k, v in self._active.items():
                    if v == task:
                        agent_id_finished = k
                        break
                if agent_id_finished:
                    result = await task
                    self._results[agent_id_finished] = result
                    del self._active[agent_id_finished]
        
        # 提交新任务
        task = asyncio.create_task(coro)
        self._active[agent_id] = task
        return await task
    
    async def wait_all(self) -> Dict[str, SubAgentResult]:
        """等待所有任务完成"""
        if self._active:
            results = await asyncio.gather(*self._active.values(), return_exceptions=True)
            for i, (agent_id, task) in enumerate(self._active.items()):
                if isinstance(results[i], Exception):
                    self._results[agent_id] = SubAgentResult(
                        success=False,
                        output="",
                        error=str(results[i])
                    )
                else:
                    self._results[agent_id] = results[i]
            self._active.clear()
        
        return self._results.copy()


# ============================================================================
# 进度回调
# ============================================================================

class ProgressCallback:
    """进度回调"""
    
    def __init__(self, callback: Optional[Callable] = None):
        self.callback = callback
        self.steps: List[Dict] = []
    
    def emit(self, agent_id: str, status: str, message: str):
        """发出进度更新"""
        step = {
            "agent_id": agent_id,
            "status": status,  # started/running/completed/failed
            "message": message,
        }
        self.steps.append(step)
        
        if self.callback:
            self.callback(step)
    
    def get_tree_view(self) -> str:
        """获取树形视图"""
        lines = []
        for step in self.steps:
            icon = {
                "started": "🌱",
                "running": "⏳",
                "completed": "✅",
                "failed": "❌",
            }.get(step["status"], "•")
            lines.append(f"{icon} [{step['agent_id']}] {step['message']}")
        return "\n".join(lines)


# ============================================================================
# CLI 入口
# ============================================================================

def main():
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description="SubAgent Tool Isolation")
    parser.add_argument("--goal", "-g", required=True, help="Task goal")
    parser.add_argument("--context", "-c", help="Context information")
    parser.add_argument("--cwd", help="Parent working directory")
    parser.add_argument("--list-tools", action="store_true", help="List allowed tools")
    
    args = parser.parse_args()
    
    if args.list_tools:
        config = IsolationConfig()
        print("Allowed Tools:", ", ".join(sorted(config.allowed_tools or DELEGATE_ALLOWED_TOOLS)))
        print("")
        print("Blocked Tools:", ", ".join(sorted(config.blocked_tools)))
        return
    
    # 构建子 Agent
    builder = SubAgentBuilder(args.goal, args.context or "", args.cwd)
    
    print("=== SubAgent System Prompt ===")
    print(builder.build_system_prompt())
    print("")
    print("=== Allowed Tools ===")
    print(", ".join(builder.get_allowed_tools()))


if __name__ == "__main__":
    main()
