#!/usr/bin/env python3
"""
多会话 Agent 协作系统

Manager (main) → 分发任务 → Helper Agents → 执行 → 返回结果 → Manager 验收
"""

import asyncio
import json
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

sys.path.insert(0, str(Path(__file__).parent))
from schema import BaseTool, ToolDefinition, ToolResult, ToolCapability


# ============ 常量定义 ============
SESSION_STORE_PATH = Path.home() / ".openclaw/sessions.json"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    DISTRIBUTED = "distributed"  # 已分发
    RUNNING = "running"          # 执行中
    COMPLETED = "completed"      # 已完成
    FAILED = "failed"            # 失败
    RETURNED = "returned"        # 已返回
    APPROVED = "approved"        # 已验收
    REJECTED = "rejected"        # 已拒绝


@dataclass
class DistributedTask:
    """分发后的任务"""
    id: str                      # 任务 ID
    description: str             # 任务描述
    assignee_session: str        # 分配的会话
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[str] = None # 执行结果
    feedback: Optional[str] = None  # 反馈/验收意见
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    distributed_at: Optional[str] = None
    completed_at: Optional[str] = None
    approved_at: Optional[str] = None


# ============ 会话管理工具 ============

# 全局任务存储（所有实例共享）
_global_tasks: Dict[str, DistributedTask] = {}


class SessionsListTool(BaseTool):
    """列出所有活跃会话"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="sessions_list",
            description="列出所有活跃的会话（可用于分发任务）",
            input_schema={
                "type": "object",
                "properties": {
                    "active_minutes": {"type": "number", "default": 60, "description": "最近活跃的分钟数"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["session", "list", "agents"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        active_minutes = kwargs.get("active_minutes", 60)
        
        try:
            result = subprocess.run(
                ["openclaw", "sessions", "--active", str(active_minutes), "--json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return ToolResult(success=False, error=result.stderr)
            
            # 解析 JSON（可能是 dict 或 list）
            try:
                data = json.loads(result.stdout) if result.stdout else {}
            except json.JSONDecodeError:
                return ToolResult(success=False, error=f"JSON解析失败: {result.stdout[:100]}")
            
            # 处理不同的返回格式
            if isinstance(data, dict):
                sessions = data.get("sessions", [])
            elif isinstance(data, list):
                sessions = data
            else:
                sessions = []
            
            # 过滤掉 main 会话本身，保留其他会话
            if isinstance(sessions, list):
                sessions = [s for s in sessions if isinstance(s, dict) and "main" not in s.get("key", "")]
            
            return ToolResult(
                success=True,
                data={
                    "sessions": sessions,
                    "count": len(sessions) if isinstance(sessions, list) else 0
                }
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))
    
    def _get_current_session(self) -> str:
        """获取当前会话 ID"""
        # 尝试从环境变量获取
        return ""  # 简化实现


class SessionSendTool(BaseTool):
    """发送任务到指定会话"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="session_send",
            description="发送任务消息到指定的 helper 会话",
            input_schema={
                "type": "object",
                "properties": {
                    "session_key": {"type": "string", "description": "目标会话的 key"},
                    "message": {"type": "string", "description": "要发送的任务描述"},
                    "wait_result": {"type": "boolean", "default": False, "description": "是否等待结果"}
                },
                "required": ["session_key", "message"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["session", "send", "message", "delegate"]
        ))
    
    async def execute(self, **kwargs) -> ToolResult:
        session_key = kwargs.get("session_key")
        message = kwargs.get("message")
        wait_result = kwargs.get("wait_result", False)
        
        try:
            # 使用 sessions_send 发送消息
            cmd = ["python3", "-c", f"""
import sys
sys.path.insert(0, '{Path(__file__).parent}')
from sessions_send import send_message
asyncio.run(send_message('{session_key}', '{message.replace("'", "\\'")}'))
"""]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return ToolResult(
                success=result.returncode == 0,
                data={
                    "session_key": session_key,
                    "message": message,
                    "sent": result.returncode == 0,
                    "output": result.stdout
                },
                error=result.stderr if result.returncode != 0 else None
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TaskDistributeTool(BaseTool):
    """分发任务给多个会话"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="task_distribute",
            description="将任务分发到多个 helper 会话执行",
            input_schema={
                "type": "object",
                "properties": {
                    "task": {"type": "string", "description": "任务描述"},
                    "sessions": {"type": "array", "items": {"type": "string"}, "description": "目标会话列表"},
                    "mode": {"type": "string", "enum": ["parallel", "sequential"], "default": "parallel", "description": "分发模式"}
                },
                "required": ["task", "sessions"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["task", "distribute", "multi-agent", "delegate"]
        ))
    
    def get_tasks(self) -> Dict[str, DistributedTask]:
        """获取全局任务存储"""
        return _global_tasks
    
    async def execute(self, **kwargs) -> ToolResult:
        task = kwargs.get("task")
        sessions = kwargs.get("sessions", [])
        mode = kwargs.get("mode", "parallel")
        
        if not sessions:
            return ToolResult(success=False, error="没有指定目标会话")
        
        results = {}
        
        if mode == "parallel":
            # 并行分发
            tasks = []
            for session in sessions:
                task_id = str(uuid.uuid4())[:8]
                dt = DistributedTask(
                    id=task_id,
                    description=task,
                    assignee_session=session,
                    status=TaskStatus.DISTRIBUTED,
                    distributed_at=datetime.now().isoformat()
                )
                self.get_tasks()[task_id] = dt
                tasks.append(self._distribute_to_session(task_id, session, task))
            
            # 等待所有完成
            task_results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for i, session in enumerate(sessions):
                results[session] = task_results[i] if not isinstance(task_results[i], Exception) else str(task_results[i])
        else:
            # 顺序分发
            for session in sessions:
                task_id = str(uuid.uuid4())[:8]
                dt = DistributedTask(
                    id=task_id,
                    description=task,
                    assignee_session=session,
                    status=TaskStatus.DISTRIBUTED,
                    distributed_at=datetime.now().isoformat()
                )
                self.get_tasks()[task_id] = dt
                
                result = await self._distribute_to_session(task_id, session, task)
                results[session] = result
        
        return ToolResult(
            success=True,
            data={
                "task": task,
                "sessions": sessions,
                "mode": mode,
                "results": results
            }
        )
    
    async def _distribute_to_session(self, task_id: str, session_key: str, task: str) -> str:
        """分发任务到单个会话"""
        tasks = self.get_tasks()
        try:
            # 发送任务消息
            # 这里简化实现，实际应该调用 sessions_send
            dt = tasks.get(task_id)
            if dt:
                dt.status = TaskStatus.RUNNING
            
            # 模拟执行（实际需要等待会话返回结果）
            await asyncio.sleep(2)
            
            if dt:
                dt.status = TaskStatus.RETURNED
                dt.result = f"Helper {session_key} 已完成: {task}"
                dt.completed_at = datetime.now().isoformat()
            
            return dt.result if dt else "完成"
            
        except Exception as e:
            if task_id in tasks:
                tasks[task_id].status = TaskStatus.FAILED
            return f"失败: {str(e)}"
    
    def get_task_status(self, task_id: str) -> Optional[DistributedTask]:
        """获取任务状态"""
        return self.get_tasks().get(task_id)


class TaskApproveTool(BaseTool):
    """验收任务结果"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="task_approve",
            description="验收任务结果（通过或拒绝）",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务 ID"},
                    "approved": {"type": "boolean", "description": "是否通过"},
                    "feedback": {"type": "string", "description": "反馈意见"}
                },
                "required": ["task_id", "approved"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["task", "approve", "review", "accept"]
        ))
        self._distribute_tool: Optional[TaskDistributeTool] = None
    
    @property
    def distribute_tool(self) -> TaskDistributeTool:
        if not self._distribute_tool:
            self._distribute_tool = TaskDistributeTool()
        return self._distribute_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        task_id = kwargs.get("task_id")
        approved = kwargs.get("approved", False)
        feedback = kwargs.get("feedback", "")
        
        task = self.distribute_tool.get_task_status(task_id)
        if not task:
            return ToolResult(success=False, error=f"任务不存在: {task_id}")
        
        if approved:
            task.status = TaskStatus.APPROVED
            task.feedback = feedback or "验收通过"
            task.approved_at = datetime.now().isoformat()
        else:
            task.status = TaskStatus.REJECTED
            task.feedback = feedback or "需要修改"
        
        return ToolResult(
            success=True,
            data={
                "task_id": task_id,
                "approved": approved,
                "feedback": task.feedback,
                "status": task.status.value
            }
        )


class TaskResultTool(BaseTool):
    """获取任务结果"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="task_result",
            description="获取任务执行结果",
            input_schema={
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "任务 ID"}
                },
                "required": ["task_id"]
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["task", "result", "output"]
        ))
        self._distribute_tool: Optional[TaskDistributeTool] = None
    
    @property
    def distribute_tool(self) -> TaskDistributeTool:
        if not self._distribute_tool:
            self._distribute_tool = TaskDistributeTool()
        return self._distribute_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        task_id = kwargs.get("task_id")
        
        task = self.distribute_tool.get_task_status(task_id)
        if not task:
            return ToolResult(success=False, error=f"任务不存在: {task_id}")
        
        return ToolResult(
            success=True,
            data={
                "task_id": task.id,
                "description": task.description,
                "assignee": task.assignee_session,
                "status": task.status.value,
                "result": task.result,
                "feedback": task.feedback,
                "created_at": task.created_at,
                "completed_at": task.completed_at
            }
        )


class TasksListTool(BaseTool):
    """列出所有任务"""
    
    def __init__(self):
        super().__init__(ToolDefinition(
            name="tasks_list",
            description="列出所有分发出去的任务",
            input_schema={
                "type": "object",
                "properties": {
                    "status": {"type": "string", "description": "按状态过滤"}
                }
            },
            capabilities={ToolCapability.EXECUTE},
            tags=["task", "list", "status"]
        ))
        self._distribute_tool: Optional[TaskDistributeTool] = None
    
    @property
    def distribute_tool(self) -> TaskDistributeTool:
        if not self._distribute_tool:
            self._distribute_tool = TaskDistributeTool()
        return self._distribute_tool
    
    async def execute(self, **kwargs) -> ToolResult:
        status_filter = kwargs.get("status")
        
        tasks = list(self.distribute_tool.get_tasks().values())
        
        if status_filter:
            tasks = [t for t in tasks if t.status.value == status_filter]
        
        return ToolResult(
            success=True,
            data={
                "tasks": [
                    {
                        "id": t.id,
                        "description": t.description[:50],
                        "assignee": t.assignee_session,
                        "status": t.status.value,
                        "result": t.result[:100] if t.result else None
                    }
                    for t in tasks
                ],
                "count": len(tasks)
            }
        )


# ============ 导出 ============

SESSION_TOOLS = [
    SessionsListTool,
    SessionSendTool,
    TaskDistributeTool,
    TaskApproveTool,
    TaskResultTool,
    TasksListTool,
]


def register_tools(registry):
    """注册所有会话工具"""
    for tool_class in SESSION_TOOLS:
        tool = tool_class()
        registry.register(tool, "session")
    return len(SESSION_TOOLS)