"""
agent_network.py - 多 Agent 共享记忆网络
每个 Agent 有自己的视角，共享一个记忆层，但有权限隔离

架构：
  Agent A (编程) ──┐
  Agent B (写作) ──┼── 共享记忆层 (SQLite + Chroma) ──→ 统一认知
  Agent C (分析) ──┘

核心能力：
1. Agent 注册与身份管理
2. 记忆可见性控制（private / team / public）
3. 细粒度权限授予/撤销
4. 跨 Agent 记忆联想
5. 权限感知的检索
"""

from __future__ import annotations

import time
import logging
from .store import MemoryStore

logger = logging.getLogger(__name__)


class AgentIdentity:
    """Agent 身份"""

    def __init__(self, agent_id: str, agent_name: str, team_id: str = "default", capabilities: list[str] = None):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.team_id = team_id
        self.capabilities = capabilities or []

    def to_dict(self) -> dict:
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "team_id": self.team_id,
            "capabilities": self.capabilities,
        }

    def __repr__(self):
        return f"Agent({self.agent_id}, team={self.team_id})"


class AgentMemoryNetwork:
    """
    多 Agent 共享记忆网络。

    用法：
        network = AgentMemoryNetwork(store)

        # 注册 Agent
        network.register(AgentIdentity("coder", "编程 Agent", "team1", ["coding"]))
        network.register(AgentIdentity("writer", "写作 Agent", "team1", ["writing"]))

        # Agent A 写入（默认 private，仅自己可见）
        network.write("coder", "决定用 Chroma 做向量库")

        # Agent A 写入并共享给团队
        network.write("coder", "团队决策：用 Chroma", visibility="team")

        # Agent B 检索（自动看到 Agent A 的 team 级记忆）
        results = network.recall("coder", "向量库选型")

        # Agent A 私密写入
        network.write("coder", "我的 API key 是 xxx", visibility="private")

        # Agent B 看不到私密记忆
        results = network.recall("writer", "API key")  # 空

        # 授权特定记忆给其他 Agent
        network.grant("coder", memory_id, "writer", permission="read")

        # 跨 Agent 联想
        associations = network.cross_agent联想("writer", "向量库")

    ⚠️ 安全: 默认 visibility 为 private，防止错误/敏感记忆在团队内传播。
    仅在明确需要共享时使用 visibility="team" 或 "public"。
    """

    def __init__(self, store: MemoryStore):
        self.store = store
        self._agents: dict[str, AgentIdentity] = {}

    # ── Agent 注册 ─────────────────────────────────────

    def register(self, agent: AgentIdentity) -> dict:
        """注册一个 Agent"""
        self._agents[agent.agent_id] = agent
        self.store.register_agent(
            agent_id=agent.agent_id,
            agent_name=agent.agent_name,
            team_id=agent.team_id,
            capabilities=agent.capabilities,
        )
        logger.info(f"📝 Agent 注册: {agent}")
        return agent.to_dict()

    def get_agent(self, agent_id: str) -> AgentIdentity | None:
        """获取 Agent 身份"""
        if agent_id in self._agents:
            return self._agents[agent_id]
        row = self.store.get_agent(agent_id)
        if row:
            agent = AgentIdentity(
                agent_id=row["agent_id"],
                agent_name=row["agent_name"],
                team_id=row["team_id"],
                capabilities=row.get("capabilities", []),
            )
            self._agents[agent_id] = agent
            return agent
        return None

    def list_agents(self, team_id: str = None) -> list[dict]:
        """列出 Agent"""
        return self.store.list_agents(team_id=team_id)

    # ── 写入 ───────────────────────────────────────────

    def write(
        self,
        agent_id: str,
        content: str,
        visibility: str = "private",
        importance: str = "medium",
        topics: list[str] = None,
        **kwargs,
    ) -> dict:
        """
        Agent 写入记忆。

        参数:
            agent_id: 写入者 Agent ID
            content: 记忆内容
            visibility: 可见性 private / team / public（默认 private，防止跨 Agent 传播）
            importance: 重要度
            topics: 主题列表
        """
        from encoder import DimensionEncoder
        import hashlib

        agent = self.get_agent(agent_id)
        if not agent:
            return {"written": False, "reason": f"未注册的 Agent: {agent_id}"}

        # 编码
        ts = time.time()
        encoder = DimensionEncoder()
        time_id = encoder.encode_time(ts, precision="second")
        memory_id = encoder.generate_memory_id(
            time_id=time_id,
            person_id=agent_id,
            topic_codes=topics or ["misc"],
            nature_id=encoder.encode_nature(kwargs.get("nature_code", "note")),
        )
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # 写入
        self.store.insert_memory(
            memory_id=memory_id,
            time_id=time_id,
            time_ts=int(ts),
            person_id=agent_id,
            nature_id=kwargs.get("nature_id", "D05"),
            content=content,
            content_hash=content_hash,
            topics=topics,
            importance=importance,
            owner_agent_id=agent_id,
            visibility=visibility,
        )

        # 记录跨 Agent 关联（同 team 其他 Agent 的近期记忆）
        if visibility == "team":
            self._auto_associate(agent, memory_id, topics)

        logger.info(f"💾 [{agent_id}] {visibility} 写入: {content[:50]}...")
        return {
            "written": True,
            "memory_id": memory_id,
            "owner_agent_id": agent_id,
            "visibility": visibility,
        }

    # ── 检索（权限感知）────────────────────────────────

    def recall(
        self,
        agent_id: str,
        query: str = None,
        owner_agent_id: str = None,
        include_private: bool = False,
        include_public: bool = True,
        limit: int = 20,
        **kwargs,
    ) -> dict:
        """
        权限感知的检索。

        可见范围：
        1. 自己的记忆（所有可见性）
        2. 团队共享的记忆（team 级，同一 team 的 Agent）
        3. 全局公开的记忆（public 级）
        4. 被显式授权的记忆

        参数:
            agent_id: 查询者 Agent ID
            query: 查询文本
            owner_agent_id: 只查某个 Agent 的记忆（可选）
            include_private: 是否包含其他 Agent 的 private 记忆（仅限被授权的）
            include_public: 是否包含 public 记忆
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return {"error": f"未注册的 Agent: {agent_id}", "primary": []}

        # 用权限过滤查询
        results = self.store.query_agent_memories(
            agent_id=owner_agent_id,
            team_id=agent.team_id,
            query_agent_id=agent_id,
            include_public=include_public,
            limit=limit,
            keyword=query,
            **kwargs,
        )

        # 如果有 query，用语义搜索补充
        # （这里简化处理，完整版应集成 RecallEngine）

        return {
            "agent_id": agent_id,
            "total": len(results),
            "primary": results,
            "query": query or "",
        }

    # ── 权限管理 ───────────────────────────────────────

    def grant(
        self,
        owner_agent_id: str,
        memory_id: str,
        target_agent_id: str,
        permission: str = "read",
        ttl_hours: int = None,
    ) -> dict:
        """
        授予其他 Agent 访问自己记忆的权限。

        参数:
            owner_agent_id: 记忆所有者
            memory_id: 记忆 ID
            target_agent_id: 被授权者
            permission: read / write / admin
            ttl_hours: 授权有效期（None=永久）
        """
        # 验证记忆属于该 Agent
        mem = self.store.get_memory(memory_id)
        if not mem:
            return {"granted": False, "reason": "记忆不存在"}
        if mem.get("owner_agent_id") != owner_agent_id and mem.get("owner_agent_id") != "_system":
            return {"granted": False, "reason": "无权授权他人的记忆"}

        expires_at = None
        if ttl_hours:
            expires_at = int(time.time()) + ttl_hours * 3600

        success = self.store.grant_permission(
            memory_id=memory_id,
            agent_id=target_agent_id,
            granted_by=owner_agent_id,
            permission=permission,
            expires_at=expires_at,
        )

        if success:
            logger.info(f"🔑 {owner_agent_id} → {target_agent_id}: {permission} on {memory_id[:30]}")

        return {
            "granted": success,
            "memory_id": memory_id,
            "from": owner_agent_id,
            "to": target_agent_id,
            "permission": permission,
        }

    def revoke(self, owner_agent_id: str, memory_id: str, target_agent_id: str) -> dict:
        """撤销权限"""
        success = self.store.revoke_permission(memory_id, target_agent_id)
        return {"revoked": success}

    def share_all(
        self,
        agent_id: str,
        target_agent_id: str,
        visibility: str = "private",
        permission: str = "read",
    ) -> dict:
        """
        将自己的所有记忆共享给另一个 Agent。

        快捷操作：批量授权。

        ⚠️ 安全: 默认只共享 private 级别记忆（需显式授权），
        避免意外暴露敏感内容。
        """
        memories = self.store.query(limit=1000)
        agent_memories = [m for m in memories if m.get("owner_agent_id") == agent_id]

        granted = 0
        for mem in agent_memories:
            if mem.get("visibility") != "private":
                self.store.grant_permission(
                    memory_id=mem["memory_id"],
                    agent_id=target_agent_id,
                    granted_by=agent_id,
                    permission=permission,
                )
                granted += 1

        return {"granted": granted, "total": len(agent_memories)}

    # ── 跨 Agent 联想 ──────────────────────────────────

    def cross_agent联想(
        self,
        agent_id: str,
        topic: str = None,
        max_agents: int = 5,
    ) -> list[dict]:
        """
        跨 Agent 知识联想。

        查找其他 Agent 在相关主题上的记忆和决策，
        避免重复工作、发现知识缺口。
        """
        agent = self.get_agent(agent_id)
        if not agent:
            return []

        # 查找同一 team 的其他 Agent
        teammates = self.store.list_agents(team_id=agent.team_id)
        other_agents = [a for a in teammates if a["agent_id"] != agent_id]

        associations = []
        for other in other_agents[:max_agents]:
            # 查找该 Agent 在相关主题上的记忆
            if topic:
                other_mems = self.store.query_agent_memories(
                    agent_id=other["agent_id"],
                    team_id=agent.team_id,
                    query_agent_id=agent_id,
                    limit=5,
                    keyword=topic,
                )
            else:
                other_mems = self.store.query_agent_memories(
                    agent_id=other["agent_id"],
                    team_id=agent.team_id,
                    query_agent_id=agent_id,
                    limit=5,
                )

            if other_mems:
                associations.append({
                    "agent_id": other["agent_id"],
                    "agent_name": other.get("agent_name", ""),
                    "capabilities": other.get("capabilities", []),
                    "related_memories": [
                        {
                            "memory_id": m["memory_id"],
                            "content": m.get("content", "")[:100],
                            "importance": m.get("importance", ""),
                            "time_ts": m.get("time_ts", 0),
                        }
                        for m in other_mems[:3]
                    ],
                })

        return associations

    def _auto_associate(self, agent: AgentIdentity, memory_id: str, topics: list[str]):
        """自动建立跨 Agent 关联（同主题的近期记忆）"""
        teammates = self.store.list_agents(team_id=agent.team_id)
        for teammate in teammates:
            if teammate["agent_id"] == agent.agent_id:
                continue
            # 查找该 Agent 近期同主题记忆
            recent = self.store.query(
                limit=3,
                keyword=topics[0] if topics else None,
            )
            for mem in recent:
                if mem.get("owner_agent_id") == teammate["agent_id"]:
                    self.store.add_agent_association(
                        source_agent=agent.agent_id,
                        target_agent=teammate["agent_id"],
                        memory_id=memory_id,
                        assoc_type="shares_knowledge",
                        reason=f"同主题: {topics}",
                    )
                    break

    # ── 统计 ───────────────────────────────────────────

    def get_stats(self) -> dict:
        """网络统计"""
        agents = self.store.list_agents()
        memories = self.store.query(limit=10000)

        by_visibility = {}
        by_agent = {}
        for m in memories:
            vis = m.get("visibility", "team")
            by_visibility[vis] = by_visibility.get(vis, 0) + 1
            owner = m.get("owner_agent_id", "_system")
            by_agent[owner] = by_agent.get(owner, 0) + 1

        return {
            "total_agents": len(agents),
            "total_memories": len(memories),
            "by_visibility": by_visibility,
            "by_agent": by_agent,
            "agents": [a["agent_id"] for a in agents],
        }
