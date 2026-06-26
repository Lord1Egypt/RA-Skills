"""
Swarm指令协议 - 标准化多Agent指令格式和协商协议
"""
import json
import uuid
import time
from typing import Dict, List, Optional, Any, Union, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import jsonschema
from pydantic import BaseModel, Field, validator


class AgentType(Enum):
    """Agent类型枚举"""
    CEO = "小小兵CEO"  # 001
    PM = "豆包PM"      # 002
    DEVELOPER_A = "牢A"  # 003
    ANALYST_B = "牢B"   # 004
    SPECIALIST_C = "牢C" # 005
    MONITOR_D = "牢D"   # 006


class CommandPriority(Enum):
    """指令优先级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class CommandStatus(Enum):
    """指令状态"""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OutputFormat(Enum):
    """输出格式"""
    PYTHON_CODE = "python_code"
    JSON = "json"
    MARKDOWN = "markdown"
    TEXT = "text"
    HTML = "html"
    IMAGE = "image"


@dataclass
class SwarmCommand:
    """Swarm指令数据结构"""
    command_id: str = field(default_factory=lambda: f"cmd_{uuid.uuid4().hex[:8]}")
    timestamp: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    
    # 发送方信息
    sender_type: AgentType = AgentType.CEO
    sender_id: str = "001"
    
    # 接收方信息
    target_type: AgentType = AgentType.DEVELOPER_A
    target_id: str = "003"
    
    # 指令内容
    command: Dict[str, Any] = field(default_factory=dict)
    
    # 元数据
    priority: CommandPriority = CommandPriority.MEDIUM
    token_budget: int = 1000
    deadline: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    
    # 协商相关
    negotiation_allowed: bool = True
    negotiation_timeout: int = 300  # 秒
    
    # 状态跟踪
    status: CommandStatus = CommandStatus.PENDING
    assigned_to: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "command_id": self.command_id,
            "timestamp": self.timestamp,
            "sender": {
                "type": self.sender_type.value,
                "id": self.sender_id
            },
            "target": {
                "type": self.target_type.value,
                "id": self.target_id
            },
            "command": self.command,
            "metadata": {
                "priority": self.priority.value,
                "token_budget": self.token_budget,
                "deadline": self.deadline,
                "dependencies": self.dependencies
            },
            "negotiation": {
                "allowed": self.negotiation_allowed,
                "timeout": self.negotiation_timeout
            },
            "status": {
                "current": self.status.value,
                "assigned_to": self.assigned_to,
                "started_at": self.started_at,
                "completed_at": self.completed_at,
                "result": self.result,
                "error_message": self.error_message
            }
        }
    
    def to_json(self) -> str:
        """转换为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SwarmCommand':
        """从字典创建SwarmCommand"""
        # 提取数据
        command_id = data.get("command_id", f"cmd_{uuid.uuid4().hex[:8]}")
        timestamp = data.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        
        # 发送方
        sender_data = data.get("sender", {})
        sender_type = AgentType(sender_data.get("type", "小小兵CEO"))
        sender_id = sender_data.get("id", "001")
        
        # 接收方
        target_data = data.get("target", {})
        target_type = AgentType(target_data.get("type", "牢A"))
        target_id = target_data.get("id", "003")
        
        # 指令内容
        command = data.get("command", {})
        
        # 元数据
        metadata = data.get("metadata", {})
        priority = CommandPriority(metadata.get("priority", "medium"))
        token_budget = metadata.get("token_budget", 1000)
        deadline = metadata.get("deadline")
        dependencies = metadata.get("dependencies", [])
        
        # 协商
        negotiation = data.get("negotiation", {})
        negotiation_allowed = negotiation.get("allowed", True)
        negotiation_timeout = negotiation.get("timeout", 300)
        
        # 状态
        status_data = data.get("status", {})
        status = CommandStatus(status_data.get("current", "pending"))
        assigned_to = status_data.get("assigned_to")
        started_at = status_data.get("started_at")
        completed_at = status_data.get("completed_at")
        result = status_data.get("result")
        error_message = status_data.get("error_message")
        
        return cls(
            command_id=command_id,
            timestamp=timestamp,
            sender_type=sender_type,
            sender_id=sender_id,
            target_type=target_type,
            target_id=target_id,
            command=command,
            priority=priority,
            token_budget=token_budget,
            deadline=deadline,
            dependencies=dependencies,
            negotiation_allowed=negotiation_allowed,
            negotiation_timeout=negotiation_timeout,
            status=status,
            assigned_to=assigned_to,
            started_at=started_at,
            completed_at=completed_at,
            result=result,
            error_message=error_message
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'SwarmCommand':
        """从JSON字符串创建SwarmCommand"""
        data = json.loads(json_str)
        return cls.from_dict(data)


class SwarmProtocol:
    """Swarm协议处理器"""
    
    def __init__(self):
        """初始化Swarm协议处理器"""
        self._command_schema = self._load_command_schema()
    
    def _load_command_schema(self) -> Dict[str, Any]:
        """加载指令JSON Schema"""
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["command_id", "timestamp", "sender", "target", "command"],
            "properties": {
                "command_id": {"type": "string", "pattern": "^cmd_[a-f0-9]{8}$"},
                "timestamp": {"type": "string", "format": "date-time"},
                "sender": {
                    "type": "object",
                    "required": ["type", "id"],
                    "properties": {
                        "type": {"type": "string", "enum": [a.value for a in AgentType]},
                        "id": {"type": "string", "pattern": "^[0-9]{3}$"}
                    }
                },
                "target": {
                    "type": "object",
                    "required": ["type", "id"],
                    "properties": {
                        "type": {"type": "string", "enum": [a.value for a in AgentType]},
                        "id": {"type": "string", "pattern": "^[0-9]{3}$"}
                    }
                },
                "command": {"type": "object"},
                "metadata": {
                    "type": "object",
                    "properties": {
                        "priority": {"type": "string", "enum": [p.value for p in CommandPriority]},
                        "token_budget": {"type": "integer", "minimum": 1, "maximum": 10000},
                        "deadline": {"type": "string", "format": "date-time"},
                        "dependencies": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "negotiation": {
                    "type": "object",
                    "properties": {
                        "allowed": {"type": "boolean"},
                        "timeout": {"type": "integer", "minimum": 1, "maximum": 3600}
                    }
                },
                "status": {
                    "type": "object",
                    "properties": {
                        "current": {"type": "string", "enum": [s.value for s in CommandStatus]},
                        "assigned_to": {"type": ["string", "null"]},
                        "started_at": {"type": ["string", "null"], "format": "date-time"},
                        "completed_at": {"type": ["string", "null"], "format": "date-time"},
                        "result": {"type": ["object", "null"]},
                        "error_message": {"type": ["string", "null"]}
                    }
                }
            }
        }
    
    def create_command(self, agent_type: Union[str, AgentType], command: Dict[str, Any],
                      priority: Union[str, CommandPriority] = CommandPriority.MEDIUM,
                      token_budget: int = 1000, deadline: Optional[str] = None,
                      dependencies: Optional[List[str]] = None) -> SwarmCommand:
        """
        创建标准化Swarm指令
        
        Args:
            agent_type: 目标Agent类型
            command: 指令内容
            priority: 优先级
            token_budget: Token预算
            deadline: 截止时间
            dependencies: 依赖任务ID列表
            
        Returns:
            SwarmCommand: 标准化指令
        """
        # 转换参数类型
        if isinstance(agent_type, str):
            try:
                target_type = AgentType(agent_type)
            except ValueError:
                # 尝试模糊匹配
                target_type = next((a for a in AgentType if a.value == agent_type), AgentType.DEVELOPER_A)
        else:
            target_type = agent_type
        
        if isinstance(priority, str):
            priority = CommandPriority(priority)
        
        # 创建指令
        swarm_command = SwarmCommand(
            target_type=target_type,
            command=command,
            priority=priority,
            token_budget=token_budget,
            deadline=deadline,
            dependencies=dependencies or []
        )
        
        return swarm_command
    
    def validate_command(self, command: Union[Dict[str, Any], SwarmCommand]) -> Tuple[bool, List[str]]:
        """
        验证指令格式
        
        Args:
            command: 指令数据或SwarmCommand对象
            
        Returns:
            Tuple[bool, List[str]]: (是否有效, 错误消息列表)
        """
        try:
            # 转换为字典
            if isinstance(command, SwarmCommand):
                command_dict = command.to_dict()
            else:
                command_dict = command
            
            # 验证JSON Schema
            jsonschema.validate(instance=command_dict, schema=self._command_schema)
            
            # 额外验证
            errors = []
            
            # 验证时间格式
            if command_dict.get("deadline"):
                try:
                    time.strptime(command_dict["deadline"], "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    errors.append("deadline格式无效，应为YYYY-MM-DDTHH:MM:SSZ")
            
            # 验证依赖项格式
            dependencies = command_dict.get("metadata", {}).get("dependencies", [])
            for dep in dependencies:
                if not isinstance(dep, str) or not dep.startswith("cmd_"):
                    errors.append(f"依赖项格式无效: {dep}")
            
            return len(errors) == 0, errors
            
        except jsonschema.ValidationError as e:
            return False, [f"JSON Schema验证失败: {e.message}"]
        except Exception as e:
            return False, [f"验证过程中发生错误: {str(e)}"]
    
    def parse_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析Agent响应
        
        Args:
            response: Agent响应数据
            
        Returns:
            Dict[str, Any]: 标准化响应
        """
        standardized_response = {
            "response_id": f"resp_{uuid.uuid4().hex[:8]}",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "success",
            "data": {},
            "metadata": {
                "processing_time": 0,
                "tokens_used": 0,
                "model_used": "unknown"
            }
        }
        
        # 合并响应数据
        if isinstance(response, dict):
            # 检查是否已经是标准化格式
            if "response_id" in response and "timestamp" in response:
                return response
            
            # 否则合并到data字段
            standardized_response["data"] = response
            
            # 提取可能的元数据
            if "metadata" in response:
                standardized_response["metadata"].update(response["metadata"])
                del response["metadata"]
        
        return standardized_response
    
    def create_negotiation_request(self, task_id: str, agents: List[Dict[str, str]], 
                                  constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建协商请求
        
        Args:
            task_id: 任务ID
            agents: 参与协商的Agent列表
            constraints: 约束条件
            
        Returns:
            Dict[str, Any]: 协商请求
        """
        return {
            "negotiation_id": f"neg_{uuid.uuid4().hex[:8]}",
            "task_id": task_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "participants": agents,
            "constraints": constraints,
            "status": "pending",
            "proposals": [],
            "deadline": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 300)),
            "result": None
        }
    
    def create_task_assignment(self, command: SwarmCommand, assigned_agent: str) -> Dict[str, Any]:
        """
        创建任务分配通知
        
        Args:
            command: Swarm指令
            assigned_agent: 分配的Agent ID
            
        Returns:
            Dict[str, Any]: 任务分配通知
        """
        return {
            "assignment_id": f"assign_{uuid.uuid4().hex[:8]}",
            "command_id": command.command_id,
            "assigned_to": assigned_agent,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "expected_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 60)),
            "priority": command.priority.value,
            "token_budget": command.token_budget,
            "deadline": command.deadline,
            "status": "assigned"
        }
    
    def create_completion_notification(self, command: SwarmCommand, 
                                      result: Dict[str, Any]) -> Dict[str, Any]:
        """
        创建任务完成通知
        
        Args:
            command: Swarm指令
            result: 任务结果
            
        Returns:
            Dict[str, Any]: 完成通知
        """
        return {
            "completion_id": f"complete_{uuid.uuid4().hex[:8]}",
            "command_id": command.command_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "completed",
            "result": result,
            "processing_time": 0,  # 可以计算实际处理时间
            "tokens_used": 0,      # 可以记录实际Token使用量
            "quality_score": 1.0   # 可以添加质量评分
        }


# 全局协议处理器实例
_global_protocol: Optional[SwarmProtocol] = None


def get_global_protocol() -> SwarmProtocol:
    """
    获取全局协议处理器实例（单例模式）
    
    Returns:
        SwarmProtocol: 全局协议处理器实例
    """
    global _global_protocol
    
    if _global_protocol is None:
        _global_protocol = SwarmProtocol()
    
    return _global_protocol