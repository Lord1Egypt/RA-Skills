#!/usr/bin/env python3
"""
团队协调器 - 基于多 Agent 协作架构
实现任务分发、并行执行、结果整合
"""

import json
import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum

# 配置
SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "architecture.json"


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentTask:
    """代理任务"""
    id: str
    agent: str
    action: str
    input_data: dict
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[dict] = None
    error: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class Workflow:
    """工作流"""
    name: str
    steps: List[dict]
    current_step: int = 0
    status: TaskStatus = TaskStatus.PENDING
    results: Dict[str, dict] = field(default_factory=dict)


class MessageBus:
    """消息总线 - Agent 间通信"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.message_history: List[Dict] = []
    
    def subscribe(self, topic: str, callback: Callable):
        """订阅消息主题"""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
    
    def publish(self, topic: str, message: Dict, sender: str = None):
        """发布消息"""
        msg = {
            "id": f"msg_{len(self.message_history)}",
            "topic": topic,
            "message": message,
            "sender": sender,
            "timestamp": datetime.now().isoformat()
        }
        
        self.message_history.append(msg)
        
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                try:
                    callback(msg)
                except Exception as e:
                    print(f"[MessageBus] 消息投递失败: {e}")
    
    def get_history(self, topic: str = None, limit: int = 100) -> List[Dict]:
        """获取消息历史"""
        messages = self.message_history
        if topic:
            messages = [m for m in messages if m["topic"] == topic]
        return messages[-limit:]


class TeamCoordinator:
    """团队协调器"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path or CONFIG_FILE)
        self.message_bus = MessageBus()
        self.agents = self.config.get("agents", {})
        self.workflows = self.config.get("workflows", {})
        self.active_tasks: Dict[str, AgentTask] = {}
        self.active_workflows: Dict[str, Workflow] = {}
    
    def _load_config(self, config_path: str) -> dict:
        """加载配置"""
        path = Path(config_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def get_agent(self, agent_id: str) -> Optional[dict]:
        """获取代理配置"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[dict]:
        """列出所有代理"""
        result = []
        for agent_id, config in self.agents.items():
            result.append({
                "id": agent_id,
                "name": config.get("name", agent_id),
                "role": config.get("role", ""),
                "icon": config.get("icon", "🤖"),
                "capabilities": config.get("capabilities", [])
            })
        return result
    
    def create_task(self, agent_id: str, action: str, input_data: dict) -> AgentTask:
        """创建任务"""
        task_id = f"task_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.active_tasks)}"
        
        task = AgentTask(
            id=task_id,
            agent=agent_id,
            action=action,
            input_data=input_data
        )
        
        self.active_tasks[task_id] = task
        
        # 发布任务创建事件
        self.message_bus.publish("tasks", {
            "event": "task_created",
            "task_id": task_id,
            "agent": agent_id,
            "action": action
        })
        
        return task
    
    def execute_task(self, task: AgentTask) -> dict:
        """执行任务（模拟执行，实际需要调用 OpenClaw）"""
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.now().isoformat()
        
        # 发布任务开始事件
        self.message_bus.publish("tasks", {
            "event": "task_started",
            "task_id": task.id
        })
        
        # 这里应该调用实际的 OpenClaw sessions_send
        # 目前返回模拟结果
        result = {
            "task_id": task.id,
            "agent": task.agent,
            "action": task.action,
            "status": "completed",
            "output": f"[{task.agent}] 完成任务: {task.action}"
        }
        
        task.status = TaskStatus.COMPLETED
        task.result = result
        task.completed_at = datetime.now().isoformat()
        
        # 发布任务完成事件
        self.message_bus.publish("results", {
            "event": "task_completed",
            "task_id": task.id,
            "result": result
        })
        
        return result
    
    def start_workflow(self, workflow_name: str, input_data: dict) -> Workflow:
        """启动工作流"""
        if workflow_name not in self.workflows:
            raise ValueError(f"工作流 '{workflow_name}' 不存在")
        
        workflow_config = self.workflows[workflow_name]
        
        workflow = Workflow(
            name=workflow_name,
            steps=workflow_config.get("steps", [])
        )
        
        self.active_workflows[workflow_name] = workflow
        
        # 发布工作流启动事件
        self.message_bus.publish("tasks", {
            "event": "workflow_started",
            "workflow": workflow_name
        })
        
        return workflow
    
    def get_workflow_status(self, workflow_name: str) -> Optional[dict]:
        """获取工作流状态"""
        workflow = self.active_workflows.get(workflow_name)
        if not workflow:
            return None
        
        return {
            "name": workflow.name,
            "status": workflow.status.value,
            "current_step": workflow.current_step,
            "total_steps": len(workflow.steps),
            "results": workflow.results
        }
    
    def route_task(self, user_input: str) -> tuple:
        """
        根据用户输入路由到合适的代理
        
        Returns:
            (agent_id, confidence)
        """
        # 关键词路由规则
        routing_rules = {
            "schedule-manager": {
                "keywords": ["日程", "会议", "提醒", "预约", "日历", "安排"],
                "weight": 1.0
            },
            "email-processor": {
                "keywords": ["邮件", "回复", "信件", "inbox", "email"],
                "weight": 1.0
            },
            "document-manager": {
                "keywords": ["文档", "格式", "排版", "word", "pdf", "归档"],
                "weight": 1.0
            },
            "meeting-assistant": {
                "keywords": ["会议纪要", "纪要", "待办", "决议", "会议记录"],
                "weight": 1.0
            },
            "mindmap-builder": {
                "keywords": ["思维导图", "脑图", "结构化", "mindmap", "导图"],
                "weight": 1.0
            }
        }
        
        scores = {}
        user_input_lower = user_input.lower()
        
        for agent_id, rules in routing_rules.items():
            score = 0
            for keyword in rules["keywords"]:
                if keyword in user_input_lower:
                    score += rules["weight"]
            scores[agent_id] = score
        
        if not scores or max(scores.values()) == 0:
            return None, 0.0
        
        best_agent = max(scores, key=scores.get)
        confidence = scores[best_agent] / len(routing_rules[best_agent]["keywords"])
        
        return best_agent, confidence
    
    def delegate(self, user_input: str) -> dict:
        """
        智能委托 - 根据用户输入自动分配任务
        
        Args:
            user_input: 用户输入
        
        Returns:
            委托结果
        """
        agent_id, confidence = self.route_task(user_input)
        
        if not agent_id or confidence < 0.3:
            return {
                "success": False,
                "message": "无法确定合适的处理角色，请更明确地描述需求",
                "confidence": confidence,
                "available_agents": [a["name"] for a in self.list_agents()]
            }
        
        agent = self.get_agent(agent_id)
        
        # 创建并执行任务
        task = self.create_task(agent_id, "process", {"input": user_input})
        
        return {
            "success": True,
            "agent_id": agent_id,
            "agent_name": agent.get("name", agent_id),
            "icon": agent.get("icon", "🤖"),
            "confidence": confidence,
            "task_id": task.id,
            "capabilities": agent.get("capabilities", [])
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="团队协调器")
    parser.add_argument("command", choices=["list", "route", "delegate", "workflow"])
    parser.add_argument("--input", "-i", help="用户输入")
    parser.add_argument("--workflow", "-w", help="工作流名称")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    
    args = parser.parse_args()
    
    coordinator = TeamCoordinator()
    
    if args.command == "list":
        agents = coordinator.list_agents()
        if args.json:
            print(json.dumps(agents, ensure_ascii=False, indent=2))
        else:
            print("📋 团队成员列表:")
            for agent in agents:
                print(f"  {agent['icon']} {agent['name']} ({agent['id']})")
                print(f"     职责: {agent['role']}")
    
    elif args.command == "route":
        if not args.input:
            print("请提供 --input 参数")
            sys.exit(1)
        
        agent_id, confidence = coordinator.route_task(args.input)
        
        if args.json:
            print(json.dumps({
                "agent_id": agent_id,
                "confidence": confidence
            }, ensure_ascii=False, indent=2))
        else:
            if agent_id:
                agent = coordinator.get_agent(agent_id)
                print(f"🎯 路由到: {agent.get('icon', '🤖')} {agent.get('name', agent_id)}")
                print(f"   置信度: {confidence:.2f}")
            else:
                print("❓ 无法确定目标角色")
    
    elif args.command == "delegate":
        if not args.input:
            print("请提供 --input 参数")
            sys.exit(1)
        
        result = coordinator.delegate(args.input)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "workflow":
        if args.workflow:
            status = coordinator.get_workflow_status(args.workflow)
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print("可用工作流:")
            for name in coordinator.workflows.keys():
                print(f"  - {name}")


if __name__ == "__main__":
    main()