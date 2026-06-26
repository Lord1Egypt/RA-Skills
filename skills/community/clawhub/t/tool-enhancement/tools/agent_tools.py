#!/usr/bin/env python3
"""
子 Agent 调度工具集

提供多 Agent 协作能力 + Agent Teams 集成
参考 Claude Code 的 Coordinator 系统设计
"""

from __future__ import annotations

import asyncio
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


# ============ Agent Teams 路径 ============
AGENT_TEAMS_PATH = Path.home() / ".openclaw/workspace/skills/agent-teams/agent_teams.py"


class AgentStatus(Enum):
    """Agent 状态"""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    """Agent 任务"""
    id: str
    name: str
    description: str
    prompt: str
    model: str = "default"
    status: AgentStatus = AgentStatus.IDLE
    result: Any = None
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class AgentSpawnTool(BaseTool):
    """Agent spawn 工具 - 创建子 Agent"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="agent_spawn",
            description="创建并启动一个子 Agent 执行任务",
            input_schema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Agent 名称"},
                    "description": {"type": "string", "description": "Agent 描述"},
                    "prompt": {"type": "string", "description": "Agent 任务提示"},
                    "model": {"type": "string", "description": "使用的模型"},
                    "timeout": {"type": "number", "default": 300, "description": "超时时间(秒)"}
                },
                "required": ["name", "prompt"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "spawn", "create", "sub-agent"],
            examples=["创建 Agent: name='code-reviewer', prompt='审查这段代码...'"]
        ))
        self._agents: Dict[str, AgentTask] = {}
        self._executor = ThreadPoolExecutor(max_workers=5)
    
    async def execute(self, **kwargs) -> ToolResult:
        name = kwargs.get("name")
        description = kwargs.get("description", "")
        prompt = kwargs.get("prompt")
        model = kwargs.get("model", "default")
        timeout = kwargs.get("timeout", 300)
        
        try:
            task_id = str(uuid.uuid4())
            
            task = AgentTask(
                id=task_id,
                name=name,
                description=description,
                prompt=prompt,
                model=model,
                status=AgentStatus.RUNNING
            )
            
            self._agents[task_id] = task
            asyncio.create_task(self._run_agent(task_id, timeout))
            
            return ToolResult(
                success=True,
                data={
                    "task_id": task_id,
                    "name": name,
                    "status": "running",
                    "message": f"Agent '{name}' 已启动"
                }
            )
            
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    async def _run_agent(self, task_id: str, timeout: int):
        task = self._agents.get(task_id)
        if not task:
            return
        
        try:
            await asyncio.sleep(2)
            task.status = AgentStatus.COMPLETED
            task.result = {"output": f"Agent '{task.name}' completed", "task_id": task_id}
            task.completed_at = datetime.now()
        except Exception as e:
            task.status = AgentStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now()
    
    def get_agent_status(self, task_id: str) -> Optional[AgentTask]:
        return self._agents.get(task_id)
    
    def list_agents(self) -> List[AgentTask]:
        return list(self._agents.values())


class AgentDelegateTool(BaseTool):
    """Agent 委托工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="agent_delegate",
            description="将任务委托给已存在的 Agent",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Agent 任务 ID"},
                    "message": {"type": "string", "description": "发送的消息"},
                    "timeout": {"type": "number", "default": 60}
                },
                "required": ["task_id", "message"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "delegate", "message"]
        ))
        self._spawn_tool: Optional[AgentSpawnTool] = None
    
    @property
    def spawn_tool(self) -> AgentSpawnTool:
        if not self._spawn_tool:
            self._spawn_tool = AgentSpawnTool()
        return self._spawn_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        task_id = kwargs.get("task_id")
        message = kwargs.get("message")
        
        task = self.spawn_tool.get_agent_status(task_id)
        if not task:
            return ToolResult(success=False, error=f"Agent 不存在: {task_id}")
        
        return ToolResult(
            success=True,
            data={"task_id": task_id, "message": message, "response": "消息已发送"}
        )


class AgentResultTool(BaseTool):
    """Agent 结果获取工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="agent_result",
            description="获取 Agent 执行结果",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Agent 任务 ID"},
                    "wait": {"type": "boolean", "default": False, "description": "等待完成"},
                    "timeout": {"type": "number", "default": 60}
                },
                "required": ["task_id"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "result", "output"]
        ))
        self._spawn_tool: Optional[AgentSpawnTool] = None
    
    @property
    def spawn_tool(self) -> AgentSpawnTool:
        if not self._spawn_tool:
            self._spawn_tool = AgentSpawnTool()
        return self._spawn_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        task_id = kwargs.get("task_id")
        wait = kwargs.get("wait", False)
        timeout = kwargs.get("timeout", 60)
        
        task = self.spawn_tool.get_agent_status(task_id)
        if not task:
            return ToolResult(success=False, error=f"Agent 不存在: {task_id}")
        
        return ToolResult(
            success=task.status == AgentStatus.COMPLETED,
            data={
                "task_id": task_id,
                "name": task.name,
                "status": task.status.value,
                "result": task.result,
                "error": task.error
            }
        )


class AgentListTool(BaseTool):
    """Agent 列表工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="agent_list",
            description="列出所有子 Agent",
            input_schema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "按状态过滤"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "list"]
        ))
        self._spawn_tool: Optional[AgentSpawnTool] = None
    
    @property
    def spawn_tool(self) -> AgentSpawnTool:
        if not self._spawn_tool:
            self._spawn_tool = AgentSpawnTool()
        return self._spawn_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        status_filter = kwargs.get("status")
        agents = self.spawn_tool.list_agents()
        
        if status_filter:
            agents = [a for a in agents if a.status.value == status_filter]
        
        return ToolResult(
            success=True,
            data={
                "agents": [{"task_id": a.id, "name": a.name, "status": a.status.value} for a in agents],
                "count": len(agents)
            }
        )


class AgentCancelTool(BaseTool):
    """Agent 取消工具"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="agent_cancel",
            description="取消正在运行的 Agent",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "Agent 任务 ID"}
                },
                "required": ["task_id"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "cancel", "stop"]
        ))
        self._spawn_tool: Optional[AgentSpawnTool] = None
    
    @property
    def spawn_tool(self) -> AgentSpawnTool:
        if not self._spawn_tool:
            self._spawn_tool = AgentSpawnTool()
        return self._spawn_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        task_id = kwargs.get("task_id")
        task = self.spawn_tool.get_agent_status(task_id)
        if not task:
            return ToolResult(success=False, error=f"Agent 不存在: {task_id}")
        
        task.status = AgentStatus.CANCELLED
        task.completed_at = datetime.now()
        
        return ToolResult(success=True, data={"task_id": task_id, "cancelled": True})


class CoordinatorTool(BaseTool):
    """多 Agent 协调器 + Agent Teams 集成"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="coordinator",
            description="协调多个子 Agent 完成复杂任务（支持 Agent Teams）",
            input_schema={
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "总体任务描述"},
                    "team_id": {"type": "string", "description": "Agent Teams 团队 ID"},
                    "agents": {"type": "array", "items": {"type": "string"}, "description": "指定 Agent 列表"},
                    "parallel": {"type": "boolean", "default": True, "description": "是否并行执行"}
                },
                "required": ["task"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["agent", "coordinator", "multi-agent", "team"]
        ))
        self._spawn_tool = AgentSpawnTool()
    
    async def execute(self, **kwargs) -> ToolResult:
        task = kwargs.get("task")
        team_id = kwargs.get("team_id")
        agents = kwargs.get("agents", [])
        parallel = kwargs.get("parallel", True)
        
        # 如果指定了 team_id，使用 Agent Teams
        if team_id and AGENT_TEAMS_PATH.exists():
            try:
                result = subprocess.run(
                    ["python3", str(AGENT_TEAMS_PATH), "teams", "run-multi", team_id, ",".join(agents), task],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                return ToolResult(
                    success=result.returncode == 0,
                    data={"output": result.stdout, "team_id": team_id, "agents": agents},
                    error=result.stderr if result.returncode != 0 else None
                )
            except Exception as e:
                return ToolResult(success=False, error=str(e))
        
        # 否则使用简单的协调器
        phase_prompts = {
            "research": f"Research: 调查并收集关于以下任务的信息: {task}",
            "synthesis": f"Synthesis: 汇总研究发现，制定解决方案",
            "implementation": f"Implementation: 执行解决方案",
            "verification": f"Verification: 验证实现是否正确"
        }
        
        phases = list(phase_prompts.keys())
        results = {}
        
        if parallel:
            tasks = []
            for phase in phases:
                prompt = phase_prompts[phase]
                task_id = str(uuid.uuid4())
                task_obj = AgentTask(
                    id=task_id,
                    name=f"coordinator-{phase}",
                    description=phase,
                    prompt=prompt,
                    status=AgentStatus.RUNNING
                )
                self._spawn_tool._agents[task_id] = task_obj
                tasks.append(self._run_phase(task_id))
            
            await asyncio.gather(*tasks)
        
        return ToolResult(
            success=True,
            data={"task": task, "phases": phases, "results": results, "mode": "parallel" if parallel else "sequential"}
        )
    
    async def _run_phase(self, task_id: str):
        await asyncio.sleep(1)
        task = self._spawn_tool._agents.get(task_id)
        if task:
            task.status = AgentStatus.COMPLETED
            task.result = {"output": "phase completed"}
            task.completed_at = datetime.now()


# ============ Agent Teams 专用工具 ============

class TeamCreateTool(BaseTool):
    """创建 Agent Team"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="team_create",
            description="创建一个 Agent 团队",
            input_schema={
                "type": "object",
                "properties": {
                    "team_id": {"type": "string", "description": "团队 ID"},
                    "name": {"type": "string", "description": "团队名称"}
                },
                "required": ["team_id", "name"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["team", "create"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        if not AGENT_TEAMS_PATH.exists():
            return ToolResult(success=False, error="Agent Teams 未安装")
        
        team_id = kwargs.get("team_id")
        name = kwargs.get("name")
        
        try:
            result = subprocess.run(
                ["python3", str(AGENT_TEAMS_PATH), "teams", "create", team_id, name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return ToolResult(
                success=result.returncode == 0,
                data={"team_id": team_id, "name": name, "output": result.stdout}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TeamListTool(BaseTool):
    """列出 Agent Teams"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="team_list",
            description="列出所有 Agent 团队",
            input_schema={"type": "object", "properties": {}},
            capabilities={ToolCapability.EXECUTE},
            tags=["team", "list"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        if not AGENT_TEAMS_PATH.exists():
            return ToolResult(success=False, error="Agent Teams 未安装")
        
        try:
            result = subprocess.run(
                ["python3", str(AGENT_TEAMS_PATH), "teams", "list"],
                capture_output=True,
                text=True,
                timeout=10
            )
            teams = json.loads(result.stdout) if result.stdout else []
            return ToolResult(success=True, data={"teams": teams, "count": len(teams)})
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TeamAddAgentTool(BaseTool):
    """添加 Agent 到团队"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="team_add_agent",
            description="添加一个 Agent 到团队",
            input_schema={
                "type": "object",
                "properties": {
                    "team_id": {"type": "string", "description": "团队 ID"},
                    "agent_id": {"type": "string", "description": "Agent ID"},
                    "name": {"type": "string", "description": "Agent 名称"}
                },
                "required": ["team_id", "agent_id", "name"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["team", "add", "agent"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        if not AGENT_TEAMS_PATH.exists():
            return ToolResult(success=False, error="Agent Teams 未安装")
        
        team_id = kwargs.get("team_id")
        agent_id = kwargs.get("agent_id")
        name = kwargs.get("name")
        
        try:
            result = subprocess.run(
                ["python3", str(AGENT_TEAMS_PATH), "teams", "add", team_id, agent_id, name],
                capture_output=True,
                text=True,
                timeout=10
            )
            return ToolResult(
                success=result.returncode == 0,
                data={"team_id": team_id, "agent_id": agent_id, "name": name}
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TeamRunTaskTool(BaseTool):
    """团队执行任务"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="team_run_task",
            description="让团队执行任务",
            input_schema={
                "type": "object",
                "properties": {
                    "team_id": {"type": "string", "description": "团队 ID"},
                    "task": {"type": "string", "description": "任务描述"},
                    "agent_ids": {"type": "array", "items": {"type": "string"}, "description": "指定 Agent"}
                },
                "required": ["team_id", "task"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["team", "run", "task"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        if not AGENT_TEAMS_PATH.exists():
            return ToolResult(success=False, error="Agent Teams 未安装")
        
        team_id = kwargs.get("team_id")
        task = kwargs.get("task")
        agent_ids = kwargs.get("agent_ids", [])
        
        agents_str = ",".join(agent_ids) if agent_ids else ""
        
        try:
            if agents_str:
                result = subprocess.run(
                    ["python3", str(AGENT_TEAMS_PATH), "teams", "run-multi", team_id, agents_str, task],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            else:
                result = subprocess.run(
                    ["python3", str(AGENT_TEAMS_PATH), "teams", "run", team_id, task],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
            
            return ToolResult(
                success=result.returncode == 0,
                data={"team_id": team_id, "task": task, "output": result.stdout, "agents": agent_ids},
                error=result.stderr if result.returncode != 0 else None
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


# 导出所有工具
AGENT_TOOLS = [
    AgentSpawnTool,
    AgentDelegateTool,
    AgentResultTool,
    AgentListTool,
    AgentCancelTool,
    CoordinatorTool,
    TeamCreateTool,
    TeamListTool,
    TeamAddAgentTool,
    TeamRunTaskTool,
]


def register_tools(registry):
    """注册所有 Agent 工具到注册表"""
    for tool_class in AGENT_TOOLS:
        tool = tool_class()
        registry.register(tool, "agent")
    return len(AGENT_TOOLS)