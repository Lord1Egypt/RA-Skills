"""
协商协议 - 支持Agent间的任务协商和冲突解决
"""
import time
import uuid
import threading
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from .swarm_protocol import AgentType


class NegotiationStatus(Enum):
    """协商状态"""
    PENDING = "pending"      # 等待中
    IN_PROGRESS = "in_progress"  # 进行中
    AGREED = "agreed"       # 达成一致
    REJECTED = "rejected"   # 被拒绝
    TIMEOUT = "timeout"     # 超时
    CANCELLED = "cancelled" # 已取消


class ProposalStatus(Enum):
    """提案状态"""
    PENDING = "pending"     # 待处理
    ACCEPTED = "accepted"   # 已接受
    REJECTED = "rejected"   # 已拒绝
    COUNTERED = "countered" # 已还价


@dataclass
class Proposal:
    """协商提案"""
    proposal_id: str = field(default_factory=lambda: f"prop_{uuid.uuid4().hex[:8]}")
    negotiation_id: str = ""
    proposer_id: str = ""
    timestamp: float = field(default_factory=time.time)
    
    # 提案内容
    terms: Dict[str, Any] = field(default_factory=dict)
    
    # 状态
    status: ProposalStatus = ProposalStatus.PENDING
    responses: Dict[str, str] = field(default_factory=dict)  # agent_id -> response
    
    @property
    def is_accepted(self) -> bool:
        """检查提案是否被接受"""
        return self.status == ProposalStatus.ACCEPTED
    
    @property
    def acceptance_rate(self) -> float:
        """计算接受率"""
        if not self.responses:
            return 0.0
        
        accepted_count = sum(1 for r in self.responses.values() if r == "accept")
        return accepted_count / len(self.responses)


@dataclass
class Negotiation:
    """协商会话"""
    negotiation_id: str = field(default_factory=lambda: f"neg_{uuid.uuid4().hex[:8]}")
    task_id: str = ""
    initiator_id: str = ""
    timestamp: float = field(default_factory=time.time)
    
    # 参与者
    participants: Set[str] = field(default_factory=set)  # agent_id集合
    required_acceptances: int = 1  # 需要多少参与者接受
    
    # 协商内容
    constraints: Dict[str, Any] = field(default_factory=dict)
    proposals: List[Proposal] = field(default_factory=list)
    
    # 状态
    status: NegotiationStatus = NegotiationStatus.PENDING
    deadline: float = field(default_factory=lambda: time.time() + 300)  # 默认5分钟
    result: Optional[Dict[str, Any]] = None
    
    @property
    def current_proposal(self) -> Optional[Proposal]:
        """获取当前提案"""
        if self.proposals:
            return self.proposals[-1]
        return None
    
    @property
    def is_active(self) -> bool:
        """检查协商是否活跃"""
        return self.status in [NegotiationStatus.PENDING, NegotiationStatus.IN_PROGRESS]
    
    @property
    def time_remaining(self) -> float:
        """获取剩余时间（秒）"""
        return max(0, self.deadline - time.time())


class NegotiationProtocol:
    """协商协议处理器"""
    
    def __init__(self):
        """初始化协商协议处理器"""
        self.negotiations: Dict[str, Negotiation] = {}
        self._lock = threading.RLock()
    
    def create_negotiation(self, task_id: str, initiator_id: str, 
                          participants: List[str], constraints: Dict[str, Any],
                          timeout_seconds: int = 300) -> Optional[Negotiation]:
        """
        创建新的协商
        
        Args:
            task_id: 任务ID
            initiator_id: 发起者ID
            participants: 参与者ID列表
            constraints: 约束条件
            timeout_seconds: 超时时间（秒）
            
        Returns:
            Optional[Negotiation]: 创建的协商，如果失败则返回None
        """
        with self._lock:
            # 创建协商
            negotiation = Negotiation(
                task_id=task_id,
                initiator_id=initiator_id,
                participants=set(participants),
                constraints=constraints,
                deadline=time.time() + timeout_seconds,
                required_acceptances=len(participants)  # 默认需要所有参与者接受
            )
            
            # 存储协商
            self.negotiations[negotiation.negotiation_id] = negotiation
            
            return negotiation
    
    def submit_proposal(self, negotiation_id: str, proposer_id: str, 
                       terms: Dict[str, Any]) -> Optional[Proposal]:
        """
        提交提案
        
        Args:
            negotiation_id: 协商ID
            proposer_id: 提案者ID
            terms: 提案条款
            
        Returns:
            Optional[Proposal]: 创建的提案，如果失败则返回None
        """
        with self._lock:
            if negotiation_id not in self.negotiations:
                return None
            
            negotiation = self.negotiations[negotiation_id]
            
            # 检查协商状态
            if not negotiation.is_active:
                return None
            
            # 检查提案者是否是参与者
            if proposer_id not in negotiation.participants:
                return None
            
            # 创建提案
            proposal = Proposal(
                negotiation_id=negotiation_id,
                proposer_id=proposer_id,
                terms=terms
            )
            
            # 添加到协商
            negotiation.proposals.append(proposal)
            negotiation.status = NegotiationStatus.IN_PROGRESS
            
            return proposal
    
    def respond_to_proposal(self, negotiation_id: str, proposal_id: str, 
                           responder_id: str, response: str, 
                           counter_terms: Optional[Dict[str, Any]] = None) -> bool:
        """
        响应提案
        
        Args:
            negotiation_id: 协商ID
            proposal_id: 提案ID
            responder_id: 响应者ID
            response: 响应（"accept", "reject", "counter"）
            counter_terms: 还价条款（当response="counter"时使用）
            
        Returns:
            bool: 响应是否成功
        """
        with self._lock:
            if negotiation_id not in self.negotiations:
                return False
            
            negotiation = self.negotiations[negotiation_id]
            
            # 检查协商状态
            if not negotiation.is_active:
                return False
            
            # 检查响应者是否是参与者
            if responder_id not in negotiation.participants:
                return False
            
            # 查找提案
            proposal = None
            for p in negotiation.proposals:
                if p.proposal_id == proposal_id:
                    proposal = p
                    break
            
            if not proposal:
                return False
            
            # 记录响应
            proposal.responses[responder_id] = response
            
            # 处理还价
            if response == "counter" and counter_terms:
                # 创建新的还价提案
                counter_proposal = Proposal(
                    negotiation_id=negotiation_id,
                    proposer_id=responder_id,
                    terms=counter_terms
                )
                negotiation.proposals.append(counter_proposal)
                proposal.status = ProposalStatus.COUNTERED
            
            # 检查是否达成一致
            self._check_agreement(negotiation, proposal)
            
            return True
    
    def _check_agreement(self, negotiation: Negotiation, proposal: Proposal):
        """检查是否达成一致"""
        # 计算接受数量
        accept_count = sum(1 for r in proposal.responses.values() if r == "accept")
        
        # 检查是否达到所需接受数量
        if accept_count >= negotiation.required_acceptances:
            proposal.status = ProposalStatus.ACCEPTED
            negotiation.status = NegotiationStatus.AGREED
            negotiation.result = {
                "agreed_terms": proposal.terms,
                "accepted_by": [aid for aid, resp in proposal.responses.items() if resp == "accept"],
                "timestamp": time.time()
            }
    
    def get_negotiation(self, negotiation_id: str) -> Optional[Negotiation]:
        """
        获取协商信息
        
        Args:
            negotiation_id: 协商ID
            
        Returns:
            Optional[Negotiation]: 协商信息，如果不存在则返回None
        """
        with self._lock:
            return self.negotiations.get(negotiation_id)
    
    def cancel_negotiation(self, negotiation_id: str, canceller_id: str) -> bool:
        """
        取消协商
        
        Args:
            negotiation_id: 协商ID
            canceller_id: 取消者ID
            
        Returns:
            bool: 取消是否成功
        """
        with self._lock:
            if negotiation_id not in self.negotiations:
                return False
            
            negotiation = self.negotiations[negotiation_id]
            
            # 检查取消者权限（发起者或管理员）
            if canceller_id != negotiation.initiator_id and canceller_id != "001":  # CEO可以取消任何协商
                return False
            
            # 取消协商
            negotiation.status = NegotiationStatus.CANCELLED
            negotiation.result = {
                "cancelled_by": canceller_id,
                "timestamp": time.time(),
                "reason": "manual_cancellation"
            }
            
            return True
    
    def check_timeouts(self) -> List[str]:
        """
        检查超时的协商
        
        Returns:
            List[str]: 超时的协商ID列表
        """
        with self._lock:
            current_time = time.time()
            timed_out_negotiations = []
            
            for neg_id, negotiation in self.negotiations.items():
                if negotiation.is_active and current_time > negotiation.deadline:
                    # 标记为超时
                    negotiation.status = NegotiationStatus.TIMEOUT
                    negotiation.result = {
                        "reason": "timeout",
                        "timestamp": current_time,
                        "last_proposal": negotiation.current_proposal.terms if negotiation.current_proposal else None
                    }
                    timed_out_negotiations.append(neg_id)
            
            return timed_out_negotiations
    
    def get_active_negotiations(self) -> List[Negotiation]:
        """
        获取活跃的协商
        
        Returns:
            List[Negotiation]: 活跃协商列表
        """
        with self._lock:
            return [n for n in self.negotiations.values() if n.is_active]
    
    def get_negotiation_summary(self, negotiation_id: str) -> Optional[Dict[str, Any]]:
        """
        获取协商摘要
        
        Args:
            negotiation_id: 协商ID
            
        Returns:
            Optional[Dict[str, Any]]: 协商摘要，如果不存在则返回None
        """
        with self._lock:
            if negotiation_id not in self.negotiations:
                return None
            
            negotiation = self.negotiations[negotiation_id]
            
            return {
                "negotiation_id": negotiation.negotiation_id,
                "task_id": negotiation.task_id,
                "initiator": negotiation.initiator_id,
                "status": negotiation.status.value,
                "participants": list(negotiation.participants),
                "proposal_count": len(negotiation.proposals),
                "current_proposal": negotiation.current_proposal.terms if negotiation.current_proposal else None,
                "time_remaining": negotiation.time_remaining,
                "created_at": negotiation.timestamp,
                "constraints": negotiation.constraints
            }
    
    def cleanup_old_negotiations(self, max_age_hours: int = 24):
        """
        清理旧的协商
        
        Args:
            max_age_hours: 最大保留时间（小时）
        """
        with self._lock:
            cutoff_time = time.time() - (max_age_hours * 3600)
            
            # 找出需要清理的协商
            to_remove = []
            for neg_id, negotiation in self.negotiations.items():
                if negotiation.timestamp < cutoff_time and not negotiation.is_active:
                    to_remove.append(neg_id)
            
            # 清理
            for neg_id in to_remove:
                del self.negotiations[neg_id]
    
    def get_negotiation_history(self, task_id: Optional[str] = None, 
                               participant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取协商历史
        
        Args:
            task_id: 筛选指定任务的协商
            participant_id: 筛选指定参与者的协商
            
        Returns:
            List[Dict[str, Any]]: 协商历史列表
        """
        with self._lock:
            history = []
            
            for negotiation in self.negotiations.values():
                # 应用筛选条件
                if task_id and negotiation.task_id != task_id:
                    continue
                
                if participant_id and participant_id not in negotiation.participants:
                    continue
                
                history.append(self.get_negotiation_summary(negotiation.negotiation_id))
            
            # 按时间排序（最新的在前）
            history.sort(key=lambda x: x["created_at"] if x else 0, reverse=True)
            
            return history


# 协商策略
class NegotiationStrategy:
    """协商策略基类"""
    
    def generate_initial_proposal(self, constraints: Dict[str, Any], 
                                 agent_capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成初始提案
        
        Args:
            constraints: 约束条件
            agent_capabilities: Agent能力信息
            
        Returns:
            Dict[str, Any]: 初始提案
        """
        raise NotImplementedError
    
    def evaluate_proposal(self, proposal: Dict[str, Any], 
                         agent_preferences: Dict[str, Any]) -> Tuple[float, str]:
        """
        评估提案
        
        Args:
            proposal: 提案条款
            agent_preferences: Agent偏好
            
        Returns:
            Tuple[float, str]: (评分, 建议响应)
        """
        raise NotImplementedError
    
    def generate_counter_proposal(self, original_proposal: Dict[str, Any],
                                 evaluation_score: float,
                                 agent_preferences: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        生成还价提案
        
        Args:
            original_proposal: 原始提案
            evaluation_score: 评估分数
            agent_preferences: Agent偏好
            
        Returns:
            Optional[Dict[str, Any]]: 还价提案，如果不还价则返回None
        """
        raise NotImplementedError


class SimpleNegotiationStrategy(NegotiationStrategy):
    """简单协商策略"""
    
    def generate_initial_proposal(self, constraints: Dict[str, Any], 
                                 agent_capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """生成初始提案"""
        proposal = {
            "task_distribution": {},
            "resource_allocation": {},
            "timeline": {},
            "quality_requirements": {}
        }
        
        # 基于约束和能力生成提案
        if "task_type" in constraints:
            proposal["task_distribution"] = {
                "primary_agent": list(agent_capabilities.keys())[0] if agent_capabilities else "003",
                "support_agents": []
            }
        
        if "deadline" in constraints:
            proposal["timeline"] = {
                "start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "deadline": constraints["deadline"],
                "milestones": []
            }
        
        if "quality" in constraints:
            proposal["quality_requirements"] = {
                "success_rate": constraints.get("quality", 0.9),
                "review_required": True
            }
        
        return proposal
    
    def evaluate_proposal(self, proposal: Dict[str, Any], 
                         agent_preferences: Dict[str, Any]) -> Tuple[float, str]:
        """评估提案"""
        score = 0.5  # 基础分数
        
        # 检查任务分配
        if "task_distribution" in proposal:
            primary_agent = proposal["task_distribution"].get("primary_agent")
            if primary_agent == agent_preferences.get("preferred_agent"):
                score += 0.3
        
        # 检查时间线
        if "timeline" in proposal:
            deadline = proposal["timeline"].get("deadline")
            if deadline:
                # 简单检查：截止时间是否合理
                try:
                    import datetime
                    deadline_dt = datetime.datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                    now_dt = datetime.datetime.now(datetime.timezone.utc)
                    days_until = (deadline_dt - now_dt).days
                    if 1 <= days_until <= 7:  # 1-7天被认为是合理的
                        score += 0.2
                except:
                    pass
        
        # 决定响应
        if score >= 0.7:
            return score, "accept"
        elif score >= 0.4:
            return score, "counter"
        else:
            return score, "reject"
    
    def generate_counter_proposal(self, original_proposal: Dict[str, Any],
                                 evaluation_score: float,
                                 agent_preferences: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """生成还价提案"""
        if evaluation_score >= 0.7:
            return None  # 不还价，直接接受
        
        counter_proposal = original_proposal.copy()
        
        # 调整任务分配
        if "task_distribution" in counter_proposal:
            if agent_preferences.get("preferred_agent"):
                counter_proposal["task_distribution"]["primary_agent"] = agent_preferences["preferred_agent"]
        
        # 调整时间线（如果需要更多时间）
        if "timeline" in counter_proposal and evaluation_score < 0.4:
            # 延长截止时间
            try:
                import datetime
                deadline = counter_proposal["timeline"].get("deadline")
                if deadline:
                    deadline_dt = datetime.datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                    new_deadline = deadline_dt + datetime.timedelta(days=2)
                    counter_proposal["timeline"]["