"""
role_template.py - 角色模板系统（v8.3 增强版）

v8.0: 个人风格 Agent
- 角色模板定义
- 风格混合机制
- 外部导入支持
- 会话隔离

v8.3: 专属记忆隔离 + 知识反哺
- 角色专属记忆空间
- 知识反哺机制（角色知识 → 全局知识库）
- 角色间知识共享策略
"""

from __future__ import annotations

import json
import os
import logging
import time
from dataclasses import dataclass, asdict, field
from typing import Dict, Optional, Any, List

logger = logging.getLogger(__name__)

from .store import _chunked_placeholders, SQLITE_MAX_VARIABLES


@dataclass
class RoleTemplate:
    """角色模板"""
    name: str
    prompt_template: str
    personality_traits: Dict[str, Any]
    speaking_style: str = ""
    topic_preferences: List[str] = None
    emotional_tone: str = ""
    source: str = "built-in"
    version: str = "1.0"
    memory_scope: str = "shared"
    knowledge_feed_enabled: bool = True
    feed_threshold: float = 0.7
    shared_topics: List[str] = None

    def __post_init__(self):
        if self.topic_preferences is None:
            self.topic_preferences = []
        if self.shared_topics is None:
            self.shared_topics = []


class RoleManager:
    """角色管理器（v8.3 增强版）"""

    def __init__(self, roles_dir: str = None, store=None):
        self.roles_dir = roles_dir or os.path.join(os.path.dirname(__file__), "roles")
        self.store = store
        self.roles = {}
        self._role_sessions = {}
        self._load_builtin_roles()
        self._load_custom_roles()
        self._ensure_role_schema()
    
    def _load_builtin_roles(self):
        """加载内置角色"""
        builtin_roles = {
            "tech_expert": RoleTemplate(
                name="技术专家",
                prompt_template="你是一位资深技术专家，擅长分析复杂问题，提供专业、准确的技术解决方案。你的回答应该包含技术细节和最佳实践。",
                personality_traits={
                    "reflective_depth": 0.8,
                    "intuition_bias": 0.3,
                    "risk_tolerance": 0.7,
                    "complexity_preference": 0.8
                },
                speaking_style="专业、简洁、逻辑清晰",
                topic_preferences=["技术", "编程", "系统架构", "性能优化"],
                emotional_tone="冷静、客观"
            ),
            "product_manager": RoleTemplate(
                name="产品经理",
                prompt_template="你是一位产品经理，注重用户体验和商业价值，擅长从用户角度思考问题，提供产品策略和功能设计建议。",
                personality_traits={
                    "reflective_depth": 0.6,
                    "intuition_bias": 0.6,
                    "risk_tolerance": 0.5,
                    "complexity_preference": 0.4
                },
                speaking_style="用户导向、商业思维",
                topic_preferences=["产品设计", "用户体验", "市场分析", "商业模式"],
                emotional_tone="积极、创新"
            ),
            "creative_writer": RoleTemplate(
                name="创意作家",
                prompt_template="你是一位创意作家，擅长用生动的语言和丰富的想象力创作内容，能够将抽象概念转化为引人入胜的故事。",
                personality_traits={
                    "reflective_depth": 0.5,
                    "intuition_bias": 0.8,
                    "risk_tolerance": 0.8,
                    "complexity_preference": 0.7
                },
                speaking_style="生动、富有想象力、情感丰富",
                topic_preferences=["创意写作", "故事创作", "艺术", "文化"],
                emotional_tone="富有表现力"
            ),
            "business_leader": RoleTemplate(
                name="商业领袖",
                prompt_template="你是一位商业领袖，具有战略思维和决策能力，擅长分析商业环境，制定发展策略，激励团队实现目标。",
                personality_traits={
                    "reflective_depth": 0.7,
                    "intuition_bias": 0.5,
                    "risk_tolerance": 0.6,
                    "complexity_preference": 0.6
                },
                speaking_style="战略性、激励性、决策导向",
                topic_preferences=["商业战略", "领导力", "团队管理", "市场策略"],
                emotional_tone="自信、果断"
            )
        }
        
        for role_id, role in builtin_roles.items():
            self.roles[role_id] = role
    
    def _load_custom_roles(self):
        """加载自定义角色"""
        if not os.path.exists(self.roles_dir):
            os.makedirs(self.roles_dir, exist_ok=True)
            return
        
        for filename in os.listdir(self.roles_dir):
            if filename.endswith(".json"):
                try:
                    role_path = os.path.join(self.roles_dir, filename)
                    with open(role_path, "r", encoding="utf-8") as f:
                        role_data = json.load(f)
                    role_id = os.path.splitext(filename)[0]
                    role = RoleTemplate(**role_data)
                    role.source = "custom"
                    self.roles[role_id] = role
                except Exception as e:
                    print(f"加载角色 {filename} 失败: {e}")
    
    def get_role(self, role_id: str) -> Optional[RoleTemplate]:
        """获取角色模板"""
        return self.roles.get(role_id)
    
    def list_roles(self) -> Dict[str, Dict[str, Any]]:
        """列出所有角色"""
        result = {}
        for role_id, role in self.roles.items():
            result[role_id] = {
                "name": role.name,
                "source": role.source,
                "version": role.version,
                "speaking_style": role.speaking_style,
                "topic_preferences": role.topic_preferences
            }
        return result
    
    def create_role(self, role_id: str, role: RoleTemplate):
        """创建新角色"""
        self.roles[role_id] = role
        # 保存到文件
        role_path = os.path.join(self.roles_dir, f"{role_id}.json")
        with open(role_path, "w", encoding="utf-8") as f:
            json.dump(asdict(role), f, ensure_ascii=False, indent=2)
    
    def delete_role(self, role_id: str):
        """删除角色"""
        if role_id in self.roles and self.roles[role_id].source == "custom":
            del self.roles[role_id]
            # 删除文件
            role_path = os.path.join(self.roles_dir, f"{role_id}.json")
            if os.path.exists(role_path):
                os.remove(role_path)
    
    def load_role_from_file(self, file_path: str) -> Optional[RoleTemplate]:
        """从文件加载角色"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                role_data = json.load(f)
            role = RoleTemplate(**role_data)
            role.source = "external"
            return role
        except Exception as e:
            logger.warning("role_template: %s", e)
            return None

    # ══════════════════════════════════════════════════════
    # v8.3: 专属记忆隔离
    # ══════════════════════════════════════════════════════

    def _ensure_role_schema(self):
        """确保角色记忆相关表存在"""
        if not self.store:
            return
        try:
            self.store.conn.executescript('''
                CREATE TABLE IF NOT EXISTS role_memory_scope (
                    role_id TEXT NOT NULL,
                    memory_id TEXT NOT NULL,
                    scope TEXT DEFAULT 'private',
                    created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
                    PRIMARY KEY (role_id, memory_id)
                );

                CREATE TABLE IF NOT EXISTS role_knowledge_feed (
                    feed_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_role TEXT NOT NULL,
                    memory_id TEXT NOT NULL,
                    topic_code TEXT,
                    confidence REAL DEFAULT 0.5,
                    fed_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
                    status TEXT DEFAULT 'pending'
                );
            ''')
        except Exception as e:
            logger.debug(f"角色 schema 初始化: {e}")

    def assign_memory_to_role(
        self, role_id: str, memory_id: str, scope: str = "private"
    ) -> dict:
        """
        将记忆分配给角色的专属空间。

        参数:
            role_id: 角色 ID
            memory_id: 记忆 ID
            scope: 记忆范围
                - "private": 仅该角色可见
                - "shared": 所有角色可见
                - "team": 同团队角色可见

        返回: {"assigned": bool, "role_id": str, "memory_id": str, "scope": str}
        """
        if not self.store:
            return {"assigned": False, "reason": "store unavailable"}

        try:
            self.store.conn.execute(
                "INSERT OR REPLACE INTO role_memory_scope (role_id, memory_id, scope, created_at) "
                "VALUES (?, ?, ?, ?)",
                (role_id, memory_id, scope, int(time.time())),
            )
            return {
                "assigned": True,
                "role_id": role_id,
                "memory_id": memory_id,
                "scope": scope,
            }
        except Exception as e:
            logger.warning("role_template: %s", e)
            return {"assigned": False, "reason": str(e)}

    def get_role_memories(
        self, role_id: str, limit: int = 20, include_shared: bool = True
    ) -> list[dict]:
        """
        获取角色可见的记忆。

        参数:
            role_id: 角色 ID
            limit: 返回条数
            include_shared: 是否包含共享记忆

        返回: 记忆列表
        """
        if not self.store:
            return []

        role = self.roles.get(role_id)
        if not role:
            return []

        try:
            if role.memory_scope == "shared" or include_shared:
                rows = self.store.conn.execute(
                    "SELECT m.* FROM memories m "
                    "LEFT JOIN role_memory_scope rms ON m.memory_id = rms.memory_id AND rms.role_id = ? "
                    "WHERE rms.memory_id IS NULL OR rms.scope IN ('shared', 'team') "
                    "ORDER BY m.time_ts DESC LIMIT ?",
                    (role_id, limit),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT m.* FROM memories m "
                    "INNER JOIN role_memory_scope rms ON m.memory_id = rms.memory_id "
                    "WHERE rms.role_id = ? AND rms.scope = 'private' "
                    "ORDER BY m.time_ts DESC LIMIT ?",
                    (role_id, limit),
                ).fetchall()

            return [dict(r) for r in rows]
        except Exception as e:
            logger.warning("role_template: %s", e)
            return []

    def start_role_session(self, role_id: str) -> dict:
        """
        启动角色会话。

        返回: {"session_id": str, "role_id": str, "scope": str}
        """
        import uuid
        session_id = f"session_{role_id}_{uuid.uuid4().hex[:8]}"
        role = self.roles.get(role_id)

        self._role_sessions[session_id] = {
            "role_id": role_id,
            "started_at": int(time.time()),
            "scope": role.memory_scope if role else "shared",
            "memory_count": 0,
        }

        return {
            "session_id": session_id,
            "role_id": role_id,
            "scope": role.memory_scope if role else "shared",
        }

    def end_role_session(self, session_id: str) -> dict:
        """
        结束角色会话，触发知识反哺。

        返回: {"session_id": str, "fed_count": int}
        """
        session = self._role_sessions.pop(session_id, None)
        if not session:
            return {"session_id": session_id, "fed_count": 0}

        role = self.roles.get(session["role_id"])
        fed_count = 0
        if role and role.knowledge_feed_enabled:
            fed_count = self._feed_knowledge_to_global(session["role_id"])

        return {"session_id": session_id, "fed_count": fed_count}

    # ══════════════════════════════════════════════════════
    # v8.3: 知识反哺机制
    # ══════════════════════════════════════════════════════

    def _feed_knowledge_to_global(self, role_id: str) -> int:
        """
        将角色的高质量私有知识反哺到全局知识库。

        策略：
        1. 查找该角色的私有记忆中 confidence >= threshold 的
        2. 筛选主题在 shared_topics 列表中的（如果有定义）
        3. 将符合条件的记忆标记为可共享

        参数:
            role_id: 角色 ID

        返回: 反哺的记忆数
        """
        if not self.store:
            return 0

        role = self.roles.get(role_id)
        if not role or not role.knowledge_feed_enabled:
            return 0

        try:
            query = (
                "SELECT rms.memory_id FROM role_memory_scope rms "
                "JOIN memories m ON rms.memory_id = m.memory_id "
                "WHERE rms.role_id = ? AND rms.scope = 'private' "
                "AND m.confidence >= ?"
            )
            params = [role_id, role.feed_threshold]

            if role.shared_topics:
                chunks = _chunked_placeholders(role.shared_topics, SQLITE_MAX_VARIABLES - 2)
                if len(chunks) == 1:
                    query += (
                        f" AND m.memory_id IN ("
                        f"SELECT memory_id FROM memory_topics WHERE topic_code IN ({chunks[0][0]})"
                        f")"
                    )
                    params.extend(chunks[0][1])
                else:
                    or_parts = []
                    for ph, chunk_ids in chunks:
                        or_parts.append(f"topic_code IN ({ph})")
                        params.extend(chunk_ids)
                    query += f" AND m.memory_id IN (SELECT memory_id FROM memory_topics WHERE {' OR '.join(or_parts)})"

            candidates = self.store.conn.execute(query, params).fetchall()

            fed_count = 0
            for row in candidates:
                memory_id = row[0]
                try:
                    self.store.conn.execute(
                        "INSERT OR REPLACE INTO role_memory_scope "
                        "(role_id, memory_id, scope, created_at) VALUES (?, ?, 'shared', ?)",
                        (role_id, memory_id, int(time.time())),
                    )
                    self.store.conn.execute(
                        "INSERT INTO role_knowledge_feed "
                        "(source_role, memory_id, confidence, fed_at, status) "
                        "VALUES (?, ?, ?, ?, 'completed')",
                        (role_id, memory_id, role.feed_threshold, int(time.time())),
                    )
                    fed_count += 1
                except Exception:
                    continue

            if fed_count > 0:
                logger.info(f"🔄 知识反哺: 角色 {role_id} 反哺 {fed_count} 条知识到全局")

            return fed_count
        except Exception as e:
            logger.warning("role_template: %s", e)
            return 0

    def get_knowledge_feed_status(self, role_id: str = None) -> list[dict]:
        """
        获取知识反哺状态。

        参数:
            role_id: 角色 ID（None=全部）

        返回: [{"source_role": str, "memory_id": str, "confidence": float, "fed_at": int, "status": str}]
        """
        if not self.store:
            return []

        try:
            if role_id:
                rows = self.store.conn.execute(
                    "SELECT * FROM role_knowledge_feed WHERE source_role = ? ORDER BY fed_at DESC LIMIT 50",
                    (role_id,),
                ).fetchall()
            else:
                rows = self.store.conn.execute(
                    "SELECT * FROM role_knowledge_feed ORDER BY fed_at DESC LIMIT 50",
                ).fetchall()
            return [dict(r) for r in rows]
        except Exception:
            return []

    def share_knowledge_between_roles(
        self, from_role: str, to_role: str, topic_code: str = None, limit: int = 10
    ) -> dict:
        """
        在两个角色之间共享知识。

        参数:
            from_role: 源角色 ID
            to_role: 目标角色 ID
            topic_code: 限定主题（None=全部共享主题）
            limit: 最大共享条数

        返回: {"shared_count": int, "from_role": str, "to_role": str}
        """
        if not self.store:
            return {"shared_count": 0, "from_role": from_role, "to_role": to_role}

        from_template = self.roles.get(from_role)
        to_template = self.roles.get(to_role)

        if not from_template or not to_template:
            return {"shared_count": 0, "from_role": from_role, "to_role": to_role}

        try:
            query = (
                "SELECT memory_id FROM role_memory_scope "
                "WHERE role_id = ? AND scope = 'shared'"
            )
            params = [from_role]

            if topic_code:
                query += " AND memory_id IN (SELECT memory_id FROM memory_topics WHERE topic_code = ?)"
                params.append(topic_code)

            query += f" LIMIT {limit}"

            rows = self.store.conn.execute(query, params).fetchall()

            shared_count = 0
            for row in rows:
                memory_id = row[0]
                try:
                    self.store.conn.execute(
                        "INSERT OR IGNORE INTO role_memory_scope "
                        "(role_id, memory_id, scope, created_at) VALUES (?, ?, 'shared', ?)",
                        (to_role, memory_id, int(time.time())),
                    )
                    shared_count += 1
                except Exception:
                    continue

            logger.info(f"📤 知识共享: {from_role} → {to_role}, {shared_count} 条")
            return {"shared_count": shared_count, "from_role": from_role, "to_role": to_role}
        except Exception as e:
            logger.warning("role_template: %s", e)
            return {"shared_count": 0, "from_role": from_role, "to_role": to_role}


def merge_styles(base_style: Dict[str, float], role_style: Dict[str, float], weight: float = 0.4) -> Dict[str, float]:
    """混合风格
    
    Args:
        base_style: 基础风格（个人核心人格）
        role_style: 角色风格
        weight: 角色风格权重
    
    Returns:
        混合后的风格
    """
    merged = {}
    for key in set(base_style.keys()) | set(role_style.keys()):
        base_value = base_style.get(key, 0.5)
        role_value = role_style.get(key, 0.5)
        merged[key] = base_value * (1 - weight) + role_value * weight
    return merged


def extract_style_from_content(content: str) -> Dict[str, Any]:
    """从内容中提取风格特征
    
    Args:
        content: 文本内容
    
    Returns:
        风格特征
    """
    # 简化实现，实际应该使用更复杂的NLP分析
    style = {
        "speaking_style": "",
        "emotional_tone": "",
        "cognitive_patterns": {
            "reflective_depth": 0.5,
            "intuition_bias": 0.5,
            "risk_tolerance": 0.5,
            "complexity_preference": 0.5
        }
    }
    
    # 基于关键词分析
    content_lower = content.lower()
    
    # 分析说话风格
    if any(word in content_lower for word in ["专业", "技术", "架构", "优化"]):
        style["speaking_style"] = "专业、技术导向"
    elif any(word in content_lower for word in ["用户", "体验", "产品", "设计"]):
        style["speaking_style"] = "用户导向、产品思维"
    elif any(word in content_lower for word in ["创意", "故事", "艺术", "想象"]):
        style["speaking_style"] = "创意、富有想象力"
    elif any(word in content_lower for word in ["战略", "商业", "团队", "领导"]):
        style["speaking_style"] = "战略性、领导力"
    
    # 分析情感基调
    positive_words = ["积极", "创新", "机遇", "成长", "成功"]
    negative_words = ["挑战", "风险", "问题", "困难", "失败"]
    
    positive_count = sum(1 for word in positive_words if word in content_lower)
    negative_count = sum(1 for word in negative_words if word in content_lower)
    
    if positive_count > negative_count:
        style["emotional_tone"] = "积极、乐观"
    elif negative_count > positive_count:
        style["emotional_tone"] = "谨慎、现实"
    else:
        style["emotional_tone"] = "平衡、客观"
    
    # 分析认知模式
    if "分析" in content_lower or "思考" in content_lower:
        style["cognitive_patterns"]["reflective_depth"] = 0.7
    if "直觉" in content_lower or "感觉" in content_lower:
        style["cognitive_patterns"]["intuition_bias"] = 0.7
    if "风险" in content_lower or "挑战" in content_lower:
        style["cognitive_patterns"]["risk_tolerance"] = 0.6
    if "复杂" in content_lower or "系统" in content_lower:
        style["cognitive_patterns"]["complexity_preference"] = 0.7
    
    return style
