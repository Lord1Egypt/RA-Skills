"""v8.6 — agent_team.py — 多 Agent 协作团队

基于 agent_network.py 的高级团队协作层:
    - RBAC: read / write / share 三级权限
    - 共享记忆广播
    - 团队记忆池
    - 跨 Agent 角色感知

用法:
    team = AgentTeam("engineering-team")
    team.add_agent("alice", role="backend")
    team.add_agent("bob", role="frontend")
    team.share_memory("alice", "数据库已从 MySQL 迁移到 PostgreSQL")
    # → 自动广播到 team 成员的可读范围
"""

from __future__ import annotations

import time
import json
import hashlib
import logging
from typing import Optional
from dataclasses import dataclass, field

from .agent_network import AgentMemoryNetwork, AgentIdentity

logger = logging.getLogger(__name__)


@dataclass
class TeamRole:
    name: str
    permissions: set = field(default_factory=lambda: {"read"})

    def has_permission(self, perm: str) -> bool:
        return perm in self.permissions


@dataclass
class TeamMember:
    agent_id: str
    agent_name: str
    role: TeamRole
    joined_at: int = field(default_factory=lambda: int(time.time()))

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "role": self.role.name,
            "permissions": list(self.role.permissions),
            "joined_at": self.joined_at,
        }


DEFAULT_ROLES = {
    "admin": TeamRole("admin", {"read", "write", "share", "manage"}),
    "lead": TeamRole("lead", {"read", "write", "share"}),
    "member": TeamRole("member", {"read", "write"}),
    "viewer": TeamRole("viewer", {"read"}),
    "backend": TeamRole("backend", {"read", "write", "share"}),
    "frontend": TeamRole("frontend", {"read", "write", "share"}),
    "analyst": TeamRole("analyst", {"read", "write"}),
    "qa": TeamRole("qa", {"read", "write"}),
}

SHAREABLE_ROLES = {"admin", "lead", "backend", "frontend"}


class AgentTeam:
    """多 Agent 协作团队

    功能:
    - 团队创建与管理
    - RBAC 权限控制 (read/write/share/manage)
    - 共享记忆自动广播
    - 团队记忆池
    - 角色感知操作
    """

    def __init__(self, team_id: str, network: AgentMemoryNetwork = None, store=None):
        self._team_id = team_id
        self._members: dict[str, TeamMember] = {}
        self._network = network
        self._store = store or (network.store if network else None)
        self._created_at = int(time.time())
        self._shared_memory_pool: list[str] = []

    @property
    def team_id(self) -> str:
        return self._team_id

    @property
    def member_count(self) -> int:
        return len(self._members)

    def add_agent(self, agent_id: str, role: str = "member",
                  agent_name: str = "", capabilities: list[str] = None) -> dict:
        """添加 Agent 到团队"""
        if agent_id in self._members:
            return {"added": False, "reason": f"Agent {agent_id} already in team"}

        team_role = DEFAULT_ROLES.get(role, DEFAULT_ROLES["member"])
        member = TeamMember(
            agent_id=agent_id,
            agent_name=agent_name or agent_id,
            role=team_role,
        )
        self._members[agent_id] = member

        if self._network:
            identity = AgentIdentity(
                agent_id=agent_id,
                agent_name=agent_name or agent_id,
                team_id=self._team_id,
                capabilities=capabilities or [],
            )
            self._network.register(identity)

        logger.info(f"Agent {agent_id} ({role}) joined team {self._team_id}")
        return {"added": True, "member": member.to_dict()}

    def remove_agent(self, agent_id: str) -> dict:
        """从团队移除 Agent"""
        if agent_id not in self._members:
            return {"removed": False, "reason": f"Agent {agent_id} not in team"}
        del self._members[agent_id]
        logger.info(f"Agent {agent_id} removed from team {self._team_id}")
        return {"removed": True, "agent_id": agent_id}

    def get_member(self, agent_id: str) -> Optional[TeamMember]:
        return self._members.get(agent_id)

    def list_members(self) -> list[dict]:
        return [m.to_dict() for m in self._members.values()]

    def check_permission(self, agent_id: str, perm: str) -> bool:
        """检查 Agent 是否有指定权限"""
        member = self._members.get(agent_id)
        if not member:
            return False
        return member.role.has_permission(perm)

    def set_role(self, agent_id: str, role: str) -> dict:
        """更新 Agent 角色"""
        if agent_id not in self._members:
            return {"updated": False, "reason": f"Agent {agent_id} not in team"}
        team_role = DEFAULT_ROLES.get(role, DEFAULT_ROLES["member"])
        self._members[agent_id].role = team_role
        logger.info(f"Agent {agent_id} role changed to {role} in team {self._team_id}")
        return {"updated": True, "member": self._members[agent_id].to_dict()}

    def share_memory(self, from_agent_id: str, content: str,
                     importance: str = "medium", topics: list[str] = None,
                     target_agents: list[str] = None) -> dict:
        """共享记忆到团队

        访问控制逻辑：
        - 无 target_agents：visibility="team"，对团队内所有具有 read 权限的成员可见
        - 有 target_agents：visibility="restricted"，仅对指定成员授予细粒度权限，
          避免受限内容暴露给全队成员

        参数:
            from_agent_id: 写入者 Agent ID
            content: 记忆内容
            importance: 重要度
            topics: 主题列表
            target_agents: 目标 Agent ID 列表（None=广播全队）
        """
        if not self.check_permission(from_agent_id, "share"):
            return {"shared": False, "reason": f"Agent {from_agent_id} lacks share permission"}

        if not self._network:
            return {"shared": False, "reason": "No network configured"}

        actual_targets = target_agents or list(self._members.keys())

        # 访问控制：指定目标 Agent 时使用 restricted 可见性，避免暴露给全队
        is_restricted = target_agents is not None

        encoder_result = self._write_shared_memory(
            from_agent_id, content, importance, topics, actual_targets,
            is_restricted=is_restricted,
        )

        self._shared_memory_pool.append(encoder_result.get("memory_id", ""))

        if not target_agents:
            logger.info(f"Agent {from_agent_id} shared to team {self._team_id}: {content[:60]}...")

        return {
            "shared": True,
            "from": from_agent_id,
            "to": actual_targets,
            "content_preview": content[:100],
            "memory_id": encoder_result.get("memory_id"),
        }

    def _write_shared_memory(self, from_agent_id: str, content: str,
                              importance: str, topics: list[str],
                              target_agents: list[str],
                              is_restricted: bool = False) -> dict:
        """写入共享记忆

        访问控制：is_restricted=True 时 visibility="restricted"，仅目标 Agent 可见；
        is_restricted=False 时 visibility="team"，全队可读。
        """
        from encoder import DimensionEncoder

        ts = time.time()
        encoder = DimensionEncoder()
        time_id = encoder.encode_time(ts, precision="second")
        memory_id = encoder.generate_memory_id(
            time_id=time_id,
            person_id=from_agent_id,
            topic_codes=topics or ["team"],
            nature_id=encoder.encode_nature("team_share"),
        )
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        self._store.insert_memory(
            memory_id=memory_id,
            time_id=time_id,
            time_ts=int(ts),
            person_id=from_agent_id,
            nature_id=encoder.encode_nature("note"),
            content=content,
            content_hash=content_hash,
            topics=topics or ["team", self._team_id],
            importance=importance,
            owner_agent_id=from_agent_id,
            visibility="restricted" if is_restricted else "team",
        )

        for target_id in target_agents:
            if target_id != from_agent_id:
                try:
                    self._network.grant(from_agent_id, memory_id, target_id, permission="read")
                except Exception as e:
                    logger.warning("agent_team: %s", e)

        return {"memory_id": memory_id}

    def write_private(self, agent_id: str, content: str,
                      importance: str = "medium", topics: list[str] = None) -> dict:
        """写入私有记忆（仅 Agent 自己可见）"""
        if not self._network:
            return {"written": False, "reason": "No network configured"}

        return self._network.write(
            agent_id=agent_id,
            content=content,
            visibility="private",
            importance=importance,
            topics=topics,
        )

    def recall(self, agent_id: str, query: str, top_k: int = 10) -> dict:
        """Agent 检索记忆（可见范围 = private + team + public）"""
        if not self._network:
            return {"recalled": False, "reason": "No network configured"}

        results = self._network.recall(agent_id, query, top_k=top_k)
        return {
            "recalled": True,
            "agent_id": agent_id,
            "query": query,
            "count": len(results) if results else 0,
            "results": results,
        }

    def get_team_memories(self, requesting_agent_id: str,
                          limit: int = 50, offset: int = 0) -> dict:
        """获取团队共享记忆池

        按 team_id 过滤，仅返回属于本团队的记忆（visibility=team 或
        通过 memory_permissions 授权给请求者的 restricted 记忆），
        而非仅按 owner_agent_id 成员关系匹配。
        """
        if not self.check_permission(requesting_agent_id, "read"):
            return {"memories": [], "reason": "Insufficient permission"}

        if not self._store:
            return {"memories": []}

        rows = self._store.query(
            query_agent_id=requesting_agent_id,
            team_id=self._team_id,
            limit=limit,
            offset=offset,
        )

        return {"memories": rows, "count": len(rows)}

    def get_team_stats(self, requesting_agent_id: str) -> dict:
        """获取团队统计"""
        if not self.check_permission(requesting_agent_id, "read"):
            return {"stats": {}, "reason": "Insufficient permission"}

        member_count = len(self._members)
        shared_count = len(self._shared_memory_pool)

        role_distribution = {}
        for member in self._members.values():
            role_distribution[member.role.name] = role_distribution.get(member.role.name, 0) + 1

        return {
            "team_id": self._team_id,
            "member_count": member_count,
            "shared_memories": shared_count,
            "role_distribution": role_distribution,
            "created_at": self._created_at,
        }

    def broadcast(self, from_agent_id: str, message: str) -> dict:
        """向团队广播消息（写入为 team 级记忆）"""
        if not self.check_permission(from_agent_id, "share"):
            return {"broadcast": False, "reason": f"Agent {from_agent_id} lacks share permission"}

        return self.share_memory(
            from_agent_id=from_agent_id,
            content=message,
            importance="high",
            topics=["broadcast", self._team_id],
        )

    def raise_task(self, from_agent_id: str, task_description: str,
                   assignee_ids: list[str] = None) -> dict:
        """向团队提出任务（创建任务记忆）"""
        if not self.check_permission(from_agent_id, "write"):
            return {"raised": False, "reason": f"Agent {from_agent_id} lacks write permission"}

        if not self._store:
            return {"raised": False, "reason": "No store configured"}

        from encoder import DimensionEncoder

        ts = time.time()
        encoder = DimensionEncoder()
        time_id = encoder.encode_time(ts, precision="second")
        task_id = encoder.generate_memory_id(
            time_id=time_id,
            person_id=from_agent_id,
            topic_codes=["task", self._team_id],
            nature_id=encoder.encode_nature("task"),
        )

        assignees = assignee_ids or list(self._members.keys())
        task_tags = json.dumps({
            "team_id": self._team_id,
            "assignees": assignees,
            "status": "open",
            "task_type": "team_task",
        }, ensure_ascii=False)

        content_hash = hashlib.sha256(task_description.encode()).hexdigest()

        self._store.insert_memory(
            memory_id=task_id,
            time_id=time_id,
            time_ts=int(ts),
            person_id=from_agent_id,
            nature_id=encoder.encode_nature("task"),
            content=task_description,
            content_hash=content_hash,
            topics=["task", self._team_id],
            importance="high",
            owner_agent_id=from_agent_id,
            visibility="team",
        )

        for assignee in assignees:
            if assignee != from_agent_id and assignee in self._members:
                try:
                    self._network.grant(from_agent_id, task_id, assignee, permission="write")
                except Exception as e:
                    logger.warning("agent_team: %s", e)

        return {"raised": True, "task_id": task_id, "from": from_agent_id, "assignees": assignees}

    def create_role(self, role_name: str, permissions: set) -> TeamRole:
        """创建自定义角色"""
        role = TeamRole(role_name, permissions)
        DEFAULT_ROLES[role_name] = role
        return role

    def get_roles(self) -> dict:
        """获取所有角色定义"""
        return {name: list(role.permissions) for name, role in DEFAULT_ROLES.items()}

    def cross_agent_discovery(self, requesting_agent_id: str,
                               query: str, top_k: int = 10) -> dict:
        """跨 Agent 发现 — 搜索团队内其他 Agent 的团队级记忆"""
        if not self.check_permission(requesting_agent_id, "read"):
            return {"discovered": [], "reason": "Insufficient permission"}

        all_results = []
        for member_id in self._members:
            if member_id == requesting_agent_id:
                continue
            try:
                results = self._network.recall(requesting_agent_id, query, top_k=top_k)
                if results:
                    all_results.extend(results)
            except Exception as e:
                logger.warning("agent_team: %s", e)

        all_results.sort(key=lambda r: r.get("relevance", 0), reverse=True)
        return {
            "discovered": True,
            "query": query,
            "count": len(all_results[:top_k]),
            "results": all_results[:top_k],
        }