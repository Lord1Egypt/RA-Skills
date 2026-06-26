"""
Agent状态管理器 - 跟踪Agent状态、任务分配和结果收集
"""
import time
import threading
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field
from enum import Enum
from .swarm_protocol import AgentType, CommandStatus


class AgentStatus(Enum):
    """Agent状态"""
    IDLE = "idle"           # 空闲
    BUSY = "busy"           # 忙碌
    OFFLINE = "offline"     # 离线
    ERROR = "error"         # 错误


@dataclass
class AgentInfo:
    """Agent信息"""
    agent_id: str
    agent_type: AgentType
    status: AgentStatus = AgentStatus.IDLE
    current_task: Optional[str] = None
    task_start_time: Optional[float] = None
    capabilities: Set[str] = field(default_factory=set)
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    last_heartbeat: float = field(default_factory=time.time)
    
    @property
    def is_available(self) -> bool:
        """检查Agent是否可用"""
        return self.status == AgentStatus.IDLE and self.current_task is None
    
    @property
    def task_duration(self) -> float:
        """获取当前任务持续时间（秒）"""
        if self.task_start_time and self.current_task:
            return time.time() - self.task_start_time
        return 0.0


class AgentManager:
    """Agent状态管理器"""
    
    def __init__(self):
        """初始化Agent管理器"""
        self.agents: Dict[str, AgentInfo] = {}
        self._lock = threading.RLock()
        
        # 初始化默认Agent（基于AGENTS.md）
        self._initialize_default_agents()
    
    def _initialize_default_agents(self):
        """初始化默认Agent"""
        default_agents = [
            ("001", AgentType.CEO, {"decision", "coordination", "architecture"}),
            ("002", AgentType.PM, {"scheduling", "validation", "coordination"}),
            ("003", AgentType.DEVELOPER_A, {"coding", "frontend", "backend", "debugging"}),
            ("004", AgentType.ANALYST_B, {"analysis", "reasoning", "optimization"}),
            ("005", AgentType.SPECIALIST_C, {"specialized_reasoning", "math", "algorithms"}),
            ("006", AgentType.MONITOR_D, {"monitoring", "reporting", "statistics"})
        ]
        
        for agent_id, agent_type, capabilities in default_agents:
            self.register_agent(agent_id, agent_type, capabilities)
    
    def register_agent(self, agent_id: str, agent_type: AgentType, 
                      capabilities: Set[str]) -> bool:
        """
        注册Agent
        
        Args:
            agent_id: Agent ID
            agent_type: Agent类型
            capabilities: 能力集合
            
        Returns:
            bool: 注册是否成功
        """
        with self._lock:
            if agent_id in self.agents:
                return False
            
            self.agents[agent_id] = AgentInfo(
                agent_id=agent_id,
                agent_type=agent_type,
                capabilities=capabilities,
                performance_metrics={
                    "success_rate": 1.0,
                    "avg_completion_time": 0.0,
                    "task_count": 0
                }
            )
            return True
    
    def unregister_agent(self, agent_id: str) -> bool:
        """
        注销Agent
        
        Args:
            agent_id: Agent ID
            
        Returns:
            bool: 注销是否成功
        """
        with self._lock:
            if agent_id in self.agents:
                del self.agents[agent_id]
                return True
            return False
    
    def update_agent_status(self, agent_id: str, status: AgentStatus, 
                           current_task: Optional[str] = None) -> bool:
        """
        更新Agent状态
        
        Args:
            agent_id: Agent ID
            status: 新状态
            current_task: 当前任务ID
            
        Returns:
            bool: 更新是否成功
        """
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            agent.status = status
            
            if current_task:
                agent.current_task = current_task
                agent.task_start_time = time.time()
            elif status == AgentStatus.IDLE:
                agent.current_task = None
                agent.task_start_time = None
            
            agent.last_heartbeat = time.time()
            return True
    
    def assign_task(self, agent_id: str, task_id: str) -> bool:
        """
        分配任务给Agent
        
        Args:
            agent_id: Agent ID
            task_id: 任务ID
            
        Returns:
            bool: 分配是否成功
        """
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            
            # 检查Agent是否可用
            if not agent.is_available:
                return False
            
            # 分配任务
            agent.current_task = task_id
            agent.task_start_time = time.time()
            agent.status = AgentStatus.BUSY
            agent.last_heartbeat = time.time()
            
            return True
    
    def complete_task(self, agent_id: str, task_id: str, 
                     success: bool = True, completion_time: Optional[float] = None) -> bool:
        """
        标记任务完成
        
        Args:
            agent_id: Agent ID
            task_id: 任务ID
            success: 是否成功
            completion_time: 完成时间（秒），如果为None则自动计算
            
        Returns:
            bool: 更新是否成功
        """
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            
            # 验证当前任务
            if agent.current_task != task_id:
                return False
            
            # 更新性能指标
            metrics = agent.performance_metrics
            task_count = metrics.get("task_count", 0)
            success_rate = metrics.get("success_rate", 1.0)
            avg_time = metrics.get("avg_completion_time", 0.0)
            
            # 计算完成时间
            if completion_time is None:
                completion_time = agent.task_duration if agent.task_start_time else 0.0
            
            # 更新指标
            new_task_count = task_count + 1
            new_success_rate = ((success_rate * task_count) + (1.0 if success else 0.0)) / new_task_count
            new_avg_time = ((avg_time * task_count) + completion_time) / new_task_count
            
            metrics["task_count"] = new_task_count
            metrics["success_rate"] = new_success_rate
            metrics["avg_completion_time"] = new_avg_time
            
            # 重置任务状态
            agent.current_task = None
            agent.task_start_time = None
            agent.status = AgentStatus.IDLE
            agent.last_heartbeat = time.time()
            
            return True
    
    def get_available_agents(self, agent_type: Optional[AgentType] = None, 
                            required_capabilities: Optional[Set[str]] = None) -> List[AgentInfo]:
        """
        获取可用Agent列表
        
        Args:
            agent_type: 筛选指定类型的Agent
            required_capabilities: 所需能力集合
            
        Returns:
            List[AgentInfo]: 可用Agent列表
        """
        with self._lock:
            available_agents = []
            
            for agent in self.agents.values():
                # 检查是否可用
                if not agent.is_available:
                    continue
                
                # 检查类型
                if agent_type and agent.agent_type != agent_type:
                    continue
                
                # 检查能力
                if required_capabilities:
                    if not required_capabilities.issubset(agent.capabilities):
                        continue
                
                available_agents.append(agent)
            
            return available_agents
    
    def find_best_agent(self, agent_type: Optional[AgentType] = None,
                       required_capabilities: Optional[Set[str]] = None) -> Optional[AgentInfo]:
        """
        寻找最佳可用Agent
        
        Args:
            agent_type: 筛选指定类型的Agent
            required_capabilities: 所需能力集合
            
        Returns:
            Optional[AgentInfo]: 最佳Agent，如果没有则返回None
        """
        available_agents = self.get_available_agents(agent_type, required_capabilities)
        
        if not available_agents:
            return None
        
        # 根据性能指标排序（成功率高、平均完成时间短的优先）
        available_agents.sort(
            key=lambda a: (
                -a.performance_metrics.get("success_rate", 0.0),
                a.performance_metrics.get("avg_completion_time", float('inf'))
            )
        )
        
        return available_agents[0]
    
    def get_agent_info(self, agent_id: str) -> Optional[AgentInfo]:
        """
        获取Agent信息
        
        Args:
            agent_id: Agent ID
            
        Returns:
            Optional[AgentInfo]: Agent信息，如果不存在则返回None
        """
        with self._lock:
            return self.agents.get(agent_id)
    
    def get_all_agents(self) -> List[AgentInfo]:
        """
        获取所有Agent
        
        Returns:
            List[AgentInfo]: 所有Agent列表
        """
        with self._lock:
            return list(self.agents.values())
    
    def get_agent_status_summary(self) -> Dict[str, Any]:
        """
        获取Agent状态摘要
        
        Returns:
            Dict[str, Any]: 状态摘要
        """
        with self._lock:
            total_agents = len(self.agents)
            idle_count = sum(1 for a in self.agents.values() if a.status == AgentStatus.IDLE)
            busy_count = sum(1 for a in self.agents.values() if a.status == AgentStatus.BUSY)
            offline_count = sum(1 for a in self.agents.values() if a.status == AgentStatus.OFFLINE)
            error_count = sum(1 for a in self.agents.values() if a.status == AgentStatus.ERROR)
            
            # 按类型统计
            type_stats = {}
            for agent_type in AgentType:
                type_agents = [a for a in self.agents.values() if a.agent_type == agent_type]
                type_stats[agent_type.value] = {
                    "count": len(type_agents),
                    "idle": sum(1 for a in type_agents if a.status == AgentStatus.IDLE),
                    "busy": sum(1 for a in type_agents if a.status == AgentStatus.BUSY)
                }
            
            return {
                "timestamp": time.time(),
                "total_agents": total_agents,
                "status_counts": {
                    "idle": idle_count,
                    "busy": busy_count,
                    "offline": offline_count,
                    "error": error_count
                },
                "availability_rate": idle_count / total_agents if total_agents > 0 else 0.0,
                "type_statistics": type_stats
            }
    
    def check_heartbeats(self, timeout_seconds: int = 300) -> List[str]:
        """
        检查心跳超时的Agent
        
        Args:
            timeout_seconds: 超时时间（秒）
            
        Returns:
            List[str]: 超时的Agent ID列表
        """
        with self._lock:
            current_time = time.time()
            timed_out_agents = []
            
            for agent_id, agent in self.agents.items():
                if current_time - agent.last_heartbeat > timeout_seconds:
                    # 标记为离线
                    if agent.status != AgentStatus.OFFLINE:
                        agent.status = AgentStatus.OFFLINE
                        timed_out_agents.append(agent_id)
            
            return timed_out_agents
    
    def update_heartbeat(self, agent_id: str) -> bool:
        """
        更新Agent心跳
        
        Args:
            agent_id: Agent ID
            
        Returns:
            bool: 更新是否成功
        """
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            agent.last_heartbeat = time.time()
            
            # 如果之前是离线状态，恢复为空闲
            if agent.status == AgentStatus.OFFLINE and agent.current_task is None:
                agent.status = AgentStatus.IDLE
            
            return True
    
    def get_agent_by_type(self, agent_type: AgentType) -> List[AgentInfo]:
        """
        获取指定类型的所有Agent
        
        Args:
            agent_type: Agent类型
            
        Returns:
            List[AgentInfo]: Agent列表
        """
        with self._lock:
            return [a for a in self.agents.values() if a.agent_type == agent_type]
    
    def reset_agent(self, agent_id: str) -> bool:
        """
        重置Agent状态
        
        Args:
            agent_id: Agent ID
            
        Returns:
            bool: 重置是否成功
        """
        with self._lock:
            if agent_id not in self.agents:
                return False
            
            agent = self.agents[agent_id]
            agent.status = AgentStatus.IDLE
            agent.current_task = None
            agent.task_start_time = None
            agent.last_heartbeat = time.time()
            
            return True


# 全局Agent管理器实例
_global_agent_manager: Optional[AgentManager] = None


def get_global_agent_manager() -> AgentManager:
    """
    获取全局Agent管理器实例（单例模式）
    
    Returns:
        AgentManager: 全局Agent管理器实例
    """
    global _global_agent_manager
    
    if _global_agent_manager is None:
        _global_agent_manager = AgentManager()
    
    return _global_agent_manager