# Hermes三层记忆系统实现

## 一、系统概述

本文档设计义乌小商品AI智能贸易系统的Hermes三层记忆架构落地实现，实现会话记忆、持久记忆和用户画像的统一管理。

### 1.1 三层记忆架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    Hermes三层记忆系统                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────────────────────────────────────────────┐     │
│   │                   Layer 1: 会话记忆                     │     │
│   │                      (Redis)                          │     │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │     │
│   │  │当前对话│ │上下文  │ │临时变量│ │会话状态│        │     │
│   │  └────────┘ └────────┘ └────────┘ └────────┘        │     │
│   │  TTL: 30分钟 | 自动过期 | 高频读写                    │     │
│   └──────────────────────────────────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│   ┌──────────────────────────────────────────────────────┐     │
│   │                   Layer 2: 持久记忆                    │     │
│   │                    (SQLite)                           │     │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │     │
│   │  │历史会话│ │商品偏好│ │供应商库│ │价格基准│        │     │
│   │  └────────┘ └────────┘ └────────┘ └────────┘        │     │
│   │  永久存储 | FTS5搜索 | 知识积累                       │     │
│   └──────────────────────────────────────────────────────┘     │
│                              │                                  │
│                              ▼                                  │
│   ┌──────────────────────────────────────────────────────┐     │
│   │                   Layer 3: 用户画像                    │     │
│   │                   (Redis + SQLite)                    │     │
│   │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │     │
│   │  │行为特征│ │交易特征│ │偏好标签│ │价值分层│        │     │
│   │  └────────┘ └────────┘ └────────┘ └────────┘        │     │
│   │  实时更新 | 定期计算 | 精准画像                        │     │
│   └──────────────────────────────────────────────────────┘     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 设计目标

| 目标 | 说明 |
|------|------|
| 低延迟 | 会话记忆读写 < 5ms |
| 高可靠 | 持久记忆零丢失 |
| 可扩展 | 支持千万级用户画像 |
| 易检索 | FTS5毫秒级全文搜索 |

---

## 二、会话记忆（Redis）

### 2.1 数据结构设计

```python
# session_memory.py
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import json
import hashlib

class SessionKeyPrefix:
    """会话键前缀定义"""
    SESSION = "session:"           # 会话基本信息
    CONTEXT = "ctx:"             # 对话上下文
    VARIABLE = "var:"            # 临时变量
    STATE = "state:"             # 会话状态
    LOCK = "lock:"               # 分布式锁

@dataclass
class SessionData:
    """会话数据结构"""
    session_id: str
    user_id: str
    created_at: int  # Unix timestamp
    updated_at: int
    messages: List[Dict[str, Any]] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

class SessionMemory:
    """会话记忆管理器"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 1800  # 30分钟
    
    # ============ 会话基础操作 ============
    
    async def create_session(
        self,
        user_id: str,
        session_id: str = None,
        metadata: dict = None
    ) -> str:
        """创建新会话"""
        
        if not session_id:
            import uuid
            session_id = f"sess_{uuid.uuid4().hex[:16]}"
        
        session = SessionData(
            session_id=session_id,
            user_id=user_id,
            created_at=int(time.time()),
            updated_at=int(time.time()),
            metadata=metadata or {}
        )
        
        # 存储会话信息
        await self.redis.setex(
            f"{SessionKeyPrefix.SESSION}{session_id}",
            self.default_ttl,
            json.dumps(asdict(session))
        )
        
        # 更新用户的会话列表
        await self._add_to_user_sessions(user_id, session_id)
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[SessionData]:
        """获取会话"""
        key = f"{SessionKeyPrefix.SESSION}{session_id}"
        data = await self.redis.get(key)
        
        if data:
            return SessionData(**json.loads(data))
        return None
    
    async def update_session(self, session: SessionData):
        """更新会话"""
        session.updated_at = int(time.time())
        
        key = f"{SessionKeyPrefix.SESSION}{session.session_id}"
        await self.redis.setex(
            key,
            self.default_ttl,
            json.dumps(asdict(session))
        )
    
    # ============ 消息操作 ============
    
    async def append_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: dict = None
    ):
        """追加消息"""
        session = await self.get_session(session_id)
        if not session:
            raise ValueError(f"Session not found: {session_id}")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": int(time.time()),
            "metadata": metadata or {}
        }
        
        session.messages.append(message)
        await self.update_session(session)
    
    async def get_messages(
        self,
        session_id: str,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """获取消息历史"""
        session = await self.get_session(session_id)
        if not session:
            return []
        
        messages = session.messages
        return messages[offset:offset+limit]
    
    # ============ 上下文管理 ============
    
    async def set_context(
        self,
        session_id: str,
        key: str,
        value: Any,
        ttl: int = None
    ):
        """设置上下文"""
        ctx_key = f"{SessionKeyPrefix.CONTEXT}{session_id}:{key}"
        expire = ttl or self.default_ttl
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await self.redis.setex(ctx_key, expire, value)
    
    async def get_context(
        self,
        session_id: str,
        key: str
    ) -> Optional[Any]:
        """获取上下文"""
        ctx_key = f"{SessionKeyPrefix.CONTEXT}{session_id}:{key}"
        value = await self.redis.get(ctx_key)
        
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    # ============ 变量管理 ============
    
    async def set_variable(
        self,
        session_id: str,
        name: str,
        value: Any
    ):
        """设置临时变量"""
        var_key = f"{SessionKeyPrefix.VARIABLE}{session_id}:{name}"
        
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        
        await self.redis.setex(var_key, self.default_ttl, value)
    
    async def get_variable(
        self,
        session_id: str,
        name: str
    ) -> Optional[Any]:
        """获取临时变量"""
        var_key = f"{SessionKeyPrefix.VARIABLE}{session_id}:{name}"
        value = await self.redis.get(var_key)
        
        if value:
            try:
                return json.loads(value)
            except:
                return value
        return None
    
    # ============ 分布式锁 ============
    
    async def acquire_lock(
        self,
        session_id: str,
        owner: str,
        ttl: int = 10
    ) -> bool:
        """获取会话锁"""
        lock_key = f"{SessionKeyPrefix.LOCK}{session_id}"
        return await self.redis.set(lock_key, owner, nx=True, ex=ttl)
    
    async def release_lock(self, session_id: str, owner: str):
        """释放会话锁"""
        lock_key = f"{SessionKeyPrefix.LOCK}{session_id}"
        
        # 只释放自己的锁
        current = await self.redis.get(lock_key)
        if current == owner:
            await self.redis.delete(lock_key)
    
    # ============ 辅助方法 ============
    
    async def _add_to_user_sessions(self, user_id: str, session_id: str):
        """添加到用户会话列表"""
        key = f"user_sessions:{user_id}"
        await self.redis.sadd(key, session_id)
        await self.redis.expire(key, 86400)  # 24小时过期
    
    async def get_user_sessions(self, user_id: str) -> List[str]:
        """获取用户所有会话"""
        key = f"user_sessions:{user_id}"
        return list(await self.redis.smembers(key))
```

### 2.2 消息格式

```python
# message_format.py

class MessageFormat:
    """消息格式定义"""
    
    @staticmethod
    def user_message(content: str, metadata: dict = None) -> dict:
        return {
            "role": "user",
            "content": content,
            "timestamp": int(time.time()),
            "metadata": metadata or {}
        }
    
    @staticmethod
    def assistant_message(
        content: str,
        agent: str = None,
        skill: str = None,
        metadata: dict = None
    ) -> dict:
        return {
            "role": "assistant",
            "content": content,
            "agent": agent,
            "skill": skill,
            "timestamp": int(time.time()),
            "metadata": metadata or {}
        }
    
    @staticmethod
    def system_message(content: str) -> dict:
        return {
            "role": "system",
            "content": content,
            "timestamp": int(time.time())
        }
    
    @staticmethod
    def format_for_llm(messages: list, system_prompt: str = None) -> list:
        """格式化为LLM输入"""
        result = []
        
        if system_prompt:
            result.append(MessageFormat.system_message(system_prompt))
        
        for msg in messages:
            result.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return result
```

---

## 三、持久记忆（SQLite + FTS5）

### 3.1 数据库架构

```sql
-- 持久记忆数据库 schema

-- 1. 历史会话表
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    started_at INTEGER NOT NULL,
    ended_at INTEGER,
    message_count INTEGER DEFAULT 0,
    summary TEXT,
    tags TEXT,  -- JSON数组
    metadata TEXT,  -- JSON对象
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_conversations_started ON conversations(started_at DESC);

-- 2. 消息历史表
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- user, assistant, system
    content TEXT NOT NULL,
    agent TEXT,
    skill TEXT,
    tokens INTEGER,
    metadata TEXT,  -- JSON对象
    created_at INTEGER NOT NULL,
    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);

-- 3. 商品偏好表
CREATE TABLE product_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    product_id TEXT,
    category_id TEXT,
    action TEXT NOT NULL,  -- view, click, search, purchase
    rating INTEGER,  -- 1-5
    metadata TEXT,
    created_at INTEGER NOT NULL
);

CREATE INDEX idx_preferences_user ON product_preferences(user_id);
CREATE INDEX idx_preferences_product ON product_preferences(product_id);
CREATE INDEX idx_preferences_action ON product_preferences(action);

-- 4. 供应商偏好表
CREATE TABLE supplier_preferences (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    supplier_id TEXT NOT NULL,
    interaction_count INTEGER DEFAULT 1,
    total_order_amount REAL DEFAULT 0,
    avg_rating REAL,
    tags TEXT,  -- JSON数组
    metadata TEXT,
    updated_at INTEGER NOT NULL
);

CREATE INDEX idx_supplier_prefs_user ON supplier_preferences(user_id);

-- 5. 知识库表
CREATE TABLE knowledge_base (
    id TEXT PRIMARY KEY,
    category TEXT NOT NULL,  -- faq, policy, product, supplier
    question TEXT,
    answer TEXT,
    keywords TEXT,
    embedding BLOB,  -- 向量
    metadata TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX idx_knowledge_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_keywords ON knowledge_base(keywords);

-- 6. FTS5 全文搜索索引
CREATE VIRTUAL TABLE messages_fts USING fts5(
    content,
    content= messages,
    content_rowid= rowid
);

-- 触发器保持FTS同步
CREATE TRIGGER messages_ai AFTER INSERT ON messages BEGIN
    INSERT INTO messages_fts(rowid, content) VALUES (new.rowid, new.content);
END;

CREATE TRIGGER messages_ad AFTER DELETE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content) VALUES('delete', old.rowid, old.content);
END;

CREATE TRIGGER messages_au AFTER UPDATE ON messages BEGIN
    INSERT INTO messages_fts(messages_fts, rowid, content) VALUES('delete', old.rowid, old.content);
    INSERT INTO messages_fts(rowid, content) VALUES (new.rowid, new.content);
END;
```

### 3.2 持久记忆实现

```python
# persistent_memory.py
import sqlite3
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import json
import asyncio
from datetime import datetime

class DatabaseConfig:
    DB_PATH = "data/hermes_memory.db"
    WAL_MODE = True
    CACHE_SIZE = -64000  # 64MB
    BUSY_TIMEOUT = 5000  # 5秒

@dataclass
class Conversation:
    id: str
    user_id: str
    session_id: str
    started_at: int
    ended_at: Optional[int] = None
    message_count: int = 0
    summary: Optional[str] = None
    tags: Optional[str] = None
    metadata: Optional[str] = None
    created_at: int = None
    updated_at: int = None

class PersistentMemory:
    """持久记忆管理器"""
    
    def __init__(self, db_path: str = DatabaseConfig.DB_PATH):
        self.db_path = db_path
        self._pool = None
        self._init_database()
    
    def _init_database(self):
        """初始化数据库"""
        with self._get_connection() as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA cache_size=64000")
            conn.execute("PRAGMA busy_timeout=5000")
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False,
            isolation_level=None
        )
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    # ============ 会话历史操作 ============
    
    async def save_conversation(
        self,
        conversation_id: str,
        user_id: str,
        session_id: str,
        messages: List[Dict],
        summary: str = None,
        tags: List[str] = None,
        metadata: Dict = None
    ):
        """保存会话历史"""
        
        now = int(datetime.utcnow().timestamp())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO conversations 
                (id, user_id, session_id, started_at, message_count, 
                 summary, tags, metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                conversation_id,
                user_id,
                session_id,
                now,
                len(messages),
                summary,
                json.dumps(tags) if tags else None,
                json.dumps(metadata) if metadata else None,
                now,
                now
            ))
            
            # 保存消息
            for msg in messages:
                conn.execute("""
                    INSERT INTO messages 
                    (id, conversation_id, role, content, agent, skill, 
                     tokens, metadata, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"msg_{now}_{msg['role']}",
                    conversation_id,
                    msg["role"],
                    msg["content"],
                    msg.get("agent"),
                    msg.get("skill"),
                    msg.get("tokens"),
                    json.dumps(msg.get("metadata")),
                    msg.get("timestamp", now)
                ))
    
    async def get_conversation(self, conversation_id: str) -> Optional[Conversation]:
        """获取会话"""
        
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT * FROM conversations WHERE id = ?",
                (conversation_id,)
            ).fetchone()
            
            if row:
                return Conversation(**dict(row))
        return None
    
    async def get_conversation_messages(
        self,
        conversation_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """获取会话消息"""
        
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM messages 
                WHERE conversation_id = ?
                ORDER BY created_at ASC
                LIMIT ?
            """, (conversation_id, limit)).fetchall()
            
            return [dict(row) for row in rows]
    
    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20,
        offset: int = 0
    ) -> List[Conversation]:
        """获取用户历史会话"""
        
        with self._get_connection() as conn:
            rows = conn.execute("""
                SELECT * FROM conversations
                WHERE user_id = ?
                ORDER BY updated_at DESC
                LIMIT ? OFFSET ?
            """, (user_id, limit, offset)).fetchall()
            
            return [Conversation(**dict(row)) for row in rows]
    
    # ============ 全文搜索 ============
    
    async def search_messages(
        self,
        user_id: str,
        query: str,
        limit: int = 20
    ) -> List[Dict]:
        """搜索消息"""
        
        with self._get_connection() as conn:
            # 使用FTS5搜索
            rows = conn.execute("""
                SELECT m.*, c.user_id
                FROM messages_fts fts
                JOIN messages m ON m.rowid = fts.rowid
                JOIN conversations c ON c.id = m.conversation_id
                WHERE fts.content MATCH ?
                AND c.user_id = ?
                ORDER BY m.created_at DESC
                LIMIT ?
            """, (query, user_id, limit)).fetchall()
            
            return [dict(row) for row in rows]
    
    # ============ 商品偏好 ============
    
    async def record_product_action(
        self,
        user_id: str,
        product_id: str = None,
        category_id: str = None,
        action: str = "view",
        rating: int = None,
        metadata: Dict = None
    ):
        """记录商品行为"""
        
        now = int(datetime.utcnow().timestamp())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO product_preferences
                (id, user_id, product_id, category_id, action, 
                 rating, metadata, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"pref_{now}_{user_id[:8]}",
                user_id,
                product_id,
                category_id,
                action,
                rating,
                json.dumps(metadata) if metadata else None,
                now
            ))
    
    async def get_user_product_history(
        self,
        user_id: str,
        action: str = None,
        limit: int = 100
    ) -> List[Dict]:
        """获取用户商品历史"""
        
        with self._get_connection() as conn:
            sql = """
                SELECT * FROM product_preferences
                WHERE user_id = ?
            """
            params = [user_id]
            
            if action:
                sql += " AND action = ?"
                params.append(action)
            
            sql += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            return [dict(row) for row in rows]
    
    # ============ 供应商偏好 ============
    
    async def update_supplier_preference(
        self,
        user_id: str,
        supplier_id: str,
        order_amount: float = 0,
        rating: float = None,
        tags: List[str] = None
    ):
        """更新供应商偏好"""
        
        now = int(datetime.utcnow().timestamp())
        
        with self._get_connection() as conn:
            # 尝试更新
            conn.execute("""
                UPDATE supplier_preferences
                SET interaction_count = interaction_count + 1,
                    total_order_amount = total_order_amount + ?,
                    avg_rating = COALESCE(?, avg_rating),
                    tags = ?,
                    updated_at = ?
                WHERE user_id = ? AND supplier_id = ?
            """, (
                order_amount,
                rating,
                json.dumps(tags) if tags else None,
                now,
                user_id,
                supplier_id
            ))
            
            # 如果没有更新，插入
            if conn.total_changes == 0:
                conn.execute("""
                    INSERT INTO supplier_preferences
                    (id, user_id, supplier_id, interaction_count,
                     total_order_amount, avg_rating, tags, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    f"sp_{user_id[:8]}_{supplier_id[:8]}",
                    user_id,
                    supplier_id,
                    1,
                    order_amount,
                    rating,
                    json.dumps(tags) if tags else None,
                    now
                ))
    
    # ============ 知识库 ============
    
    async def add_knowledge(
        self,
        category: str,
        question: str,
        answer: str,
        keywords: List[str] = None,
        metadata: Dict = None
    ):
        """添加知识"""
        
        now = int(datetime.utcnow().timestamp())
        
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO knowledge_base
                (id, category, question, answer, keywords,
                 metadata, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                f"kb_{now}",
                category,
                question,
                answer,
                ",".join(keywords) if keywords else None,
                json.dumps(metadata) if metadata else None,
                now,
                now
            ))
    
    async def search_knowledge(
        self,
        query: str,
        category: str = None,
        limit: int = 10
    ) -> List[Dict]:
        """搜索知识库"""
        
        with self._get_connection() as conn:
            sql = """
                SELECT * FROM knowledge_base
                WHERE keywords LIKE ?
            """
            params = [f"%{query}%"]
            
            if category:
                sql += " AND category = ?"
                params.append(category)
            
            sql += " ORDER BY updated_at DESC LIMIT ?"
            params.append(limit)
            
            rows = conn.execute(sql, params).fetchall()
            return [dict(row) for row in rows]
```

---

## 四、用户画像存储

### 4.1 画像数据结构

```python
# user_profile.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json

@dataclass
class UserProfile:
    """用户画像"""
    user_id: str
    created_at: int
    updated_at: int
    
    # 基础属性
    name: Optional[str] = None
    country: Optional[str] = None
    language: str = "zh-CN"
    timezone: str = "Asia/Shanghai"
    
    # 行为特征
    behavior_tags: List[str] = field(default_factory=list)
    interests: List[str] = field(default_factory=list)
    
    # 交易特征
    total_orders: int = 0
    total_amount: float = 0
    avg_order_value: float = 0
    favorite_categories: List[str] = field(default_factory=list)
    favorite_suppliers: List[str] = field(default_factory=list)
    
    # 偏好特征
    price_sensitivity: str = "medium"  # low, medium, high
    quality_preference: str = "medium"  # low, medium, high
    preferred_moq: str = "medium"  # small, medium, large
    
    # 价值分层
    customer_tier: str = "normal"  # vip, premium, normal, new
    lifetime_value: float = 0
    
    # 状态
    last_active_at: int = None
    last_order_at: int = None
    churn_risk: str = "low"  # low, medium, high
    
    # 扩展数据
    metadata: Dict[str, Any] = field(default_factory=dict)

class UserProfileManager:
    """用户画像管理器"""
    
    def __init__(self, redis_client, persistent_memory: PersistentMemory):
        self.redis = redis_client
        self.persistent = persistent_memory
    
    # ============ 基础操作 ============
    
    async def get_profile(self, user_id: str) -> Optional[UserProfile]:
        """获取用户画像"""
        
        # 先从Redis获取
        key = f"user_profile:{user_id}"
        cached = await self.redis.get(key)
        
        if cached:
            data = json.loads(cached)
            return UserProfile(**data)
        
        # 从持久化存储获取
        profile = await self._load_from_db(user_id)
        
        if profile:
            await self._cache_profile(profile)
        
        return profile
    
    async def save_profile(self, profile: UserProfile):
        """保存用户画像"""
        
        profile.updated_at = int(datetime.utcnow().timestamp())
        
        # 保存到Redis缓存
        await self._cache_profile(profile)
        
        # 异步保存到数据库
        asyncio.create_task(self._save_to_db(profile))
    
    async def update_profile(
        self,
        user_id: str,
        updates: Dict[str, Any]
    ):
        """更新画像字段"""
        
        profile = await self.get_profile(user_id)
        
        if not profile:
            profile = UserProfile(
                user_id=user_id,
                created_at=int(datetime.utcnow().timestamp()),
                updated_at=int(datetime.utcnow().timestamp())
            )
        
        # 更新字段
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        await self.save_profile(profile)
    
    # ============ 特征更新 ============
    
    async def record_behavior(
        self,
        user_id: str,
        behavior_type: str,
        data: Dict[str, Any]
    ):
        """记录用户行为"""
        
        profile = await self.get_profile(user_id)
        if not profile:
            return
        
        # 更新行为标签
        if behavior_type == "browse":
            category = data.get("category")
            if category and category not in profile.interests:
                profile.interests.append(category)
        
        elif behavior_type == "purchase":
            profile.total_orders += 1
            profile.total_amount += data.get("amount", 0)
            profile.avg_order_value = profile.total_amount / profile.total_orders
            profile.last_order_at = int(datetime.utcnow().timestamp())
            
            # 更新喜欢的类目
            category = data.get("category")
            if category and category not in profile.favorite_categories:
                profile.favorite_categories.append(category)
        
        # 更新活跃时间
        profile.last_active_at = int(datetime.utcnow().timestamp())
        
        await self.save_profile(profile)
        
        # 记录到持久化
        await self.persistent.record_product_action(
            user_id=user_id,
            product_id=data.get("product_id"),
            category_id=data.get("category"),
            action=behavior_type
        )
    
    async def recalculate_tier(self, user_id: str):
        """重新计算用户分层"""
        
        profile = await self.get_profile(user_id)
        if not profile:
            return
        
        # 计算LTV
        profile.lifetime_value = profile.total_amount
        
        # 根据LTV和订单数确定分层
        if profile.total_amount >= 100000 or profile.total_orders >= 100:
            profile.customer_tier = "vip"
        elif profile.total_amount >= 10000 or profile.total_orders >= 10:
            profile.customer_tier = "premium"
        elif profile.total_orders > 0:
            profile.customer_tier = "normal"
        else:
            profile.customer_tier = "new"
        
        # 流失风险评估
        if profile.last_order_at:
            days_since_order = (
                datetime.utcnow().timestamp() - profile.last_order_at
            ) / 86400
            
            if days_since_order > 180:
                profile.churn_risk = "high"
            elif days_since_order > 90:
                profile.churn_risk = "medium"
            else:
                profile.churn_risk = "low"
        
        await self.save_profile(profile)
    
    # ============ 批量操作 ============
    
    async def batch_get_profiles(
        self,
        user_ids: List[str]
    ) -> Dict[str, UserProfile]:
        """批量获取用户画像"""
        
        profiles = {}
        
        for uid in user_ids:
            profile = await self.get_profile(uid)
            if profile:
                profiles[uid] = profile
        
        return profiles
    
    # ============ 辅助方法 ============
    
    async def _cache_profile(self, profile: UserProfile):
        """缓存画像"""
        key = f"user_profile:{profile.user_id}"
        data = json.dumps(asdict(profile))
        
        # VIP用户缓存1小时，普通用户缓存10分钟
        ttl = 3600 if profile.customer_tier == "vip" else 600
        
        await self.redis.setex(key, ttl, data)
    
    async def _load_from_db(self, user_id: str) -> Optional[UserProfile]:
        """从数据库加载"""
        # 简化实现，实际应该从SQLite读取
        return None
    
    async def _save_to_db(self, profile: UserProfile):
        """保存到数据库"""
        # 异步保存到SQLite
        pass
```

---

## 五、记忆检索与更新策略

### 5.1 统一检索接口

```python
# memory_retriever.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class RetrievalRequest:
    """检索请求"""
    query: str
    memory_types: List[str] = None  # session, persistent, profile
    user_id: str = None
    session_id: str = None
    limit: int = 10
    filters: Dict[str, Any] = None

@dataclass
class RetrievalResult:
    """检索结果"""
    content: str
    memory_type: str
    relevance_score: float
    metadata: Dict[str, Any]

class MemoryRetriever:
    """统一记忆检索器"""
    
    def __init__(
        self,
        session_memory: SessionMemory,
        persistent_memory: PersistentMemory,
        profile_manager: UserProfileManager
    ):
        self.session = session_memory
        self.persistent = persistent_memory
        self.profile = profile_manager
    
    async def retrieve(self, request: RetrievalRequest) -> List[RetrievalResult]:
        """统一检索"""
        results = []
        
        memory_types = request.memory_types or ["session", "persistent", "profile"]
        
        if "session" in memory_types and request.session_id:
            session_results = await self._retrieve_from_session(request)
            results.extend(session_results)
        
        if "persistent" in memory_types and request.user_id:
            persistent_results = await self._retrieve_from_persistent(request)
            results.extend(persistent_results)
        
        if "profile" in memory_types and request.user_id:
            profile_results = await self._retrieve_from_profile(request)
            results.extend(profile_results)
        
        # 按相关性排序
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:request.limit]
    
    async def _retrieve_from_session(
        self,
        request: RetrievalRequest
    ) -> List[RetrievalResult]:
        """从会话记忆检索"""
        
        messages = await self.session.get_messages(
            request.session_id,
            limit=50
        )
        
        results = []
        query_lower = request.query.lower()
        
        for msg in messages:
            content = msg.get("content", "")
            if query_lower in content.lower():
                # 简单的相关性计算
                score = content.lower().count(query_lower) / len(content)
                
                results.append(RetrievalResult(
                    content=content,
                    memory_type="session",
                    relevance_score=score,
                    metadata={
                        "role": msg.get("role"),
                        "timestamp": msg.get("timestamp"),
                        "session_id": request.session_id
                    }
                ))
        
        return results
    
    async def _retrieve_from_persistent(
        self,
        request: RetrievalRequest
    ) -> List[RetrievalResult]:
        """从持久记忆检索"""
        
        messages = await self.persistent.search_messages(
            request.user_id,
            request.query,
            limit=request.limit
        )
        
        return [
            RetrievalResult(
                content=msg.get("content", ""),
                memory_type="persistent",
                relevance_score=0.8,  # 简化
                metadata={
                    "conversation_id": msg.get("conversation_id"),
                    "role": msg.get("role"),
                    "timestamp": msg.get("created_at")
                }
            )
            for msg in messages
        ]
    
    async def _retrieve_from_profile(
        self,
        request: RetrievalRequest
    ) -> List[RetrievalResult]:
        """从用户画像检索"""
        
        profile = await self.profile.get_profile(request.user_id)
        if not profile:
            return []
        
        results = []
        
        # 检索兴趣类目
        if request.query.lower() in " ".join(profile.interests).lower():
            results.append(RetrievalResult(
                content=f"用户兴趣: {', '.join(profile.interests)}",
                memory_type="profile",
                relevance_score=0.9,
                metadata={"category": "interests"}
            ))
        
        # 检索偏好
        if "偏好" in request.query or "preference" in request.query.lower():
            results.append(RetrievalResult(
                content=f"价格敏感度: {profile.price_sensitivity}, "
                       f"质量偏好: {profile.quality_preference}, "
                       f"MOQ偏好: {profile.preferred_moq}",
                memory_type="profile",
                relevance_score=0.85,
                metadata={"category": "preferences"}
            ))
        
        return results
```

### 5.2 记忆更新策略

```python
# memory_updater.py
from typing import List, Dict, Any
import asyncio

class MemoryUpdater:
    """记忆更新器"""
    
    def __init__(
        self,
        session_memory: SessionMemory,
        persistent_memory: PersistentMemory,
        profile_manager: UserProfileManager
    ):
        self.session = session_memory
        self.persistent = persistent_memory
        self.profile = profile_manager
    
    async def update_after_interaction(
        self,
        user_id: str,
        session_id: str,
        interaction: Dict[str, Any]
    ):
        """交互后更新记忆"""
        
        interaction_type = interaction.get("type")
        
        if interaction_type == "product_view":
            await self._handle_product_view(user_id, interaction)
        
        elif interaction_type == "product_search":
            await self._handle_product_search(user_id, interaction)
        
        elif interaction_type == "order":
            await self._handle_order(user_id, interaction)
        
        elif interaction_type == "message":
            await self._handle_message(user_id, session_id, interaction)
        
        # 定期更新用户分层
        if interaction_type == "order":
            asyncio.create_task(
                self.profile.recalculate_tier(user_id)
            )
    
    async def _handle_product_view(
        self,
        user_id: str,
        interaction: Dict
    ):
        """处理商品浏览"""
        await self.profile.record_behavior(
            user_id=user_id,
            behavior_type="browse",
            data={
                "product_id": interaction.get("product_id"),
                "category": interaction.get("category"),
                "duration": interaction.get("duration")
            }
        )
    
    async def _handle_product_search(
        self,
        user_id: str,
        interaction: Dict
    ):
        """处理商品搜索"""
        # 更新搜索历史
        keywords = interaction.get("keywords", [])
        
        for keyword in keywords:
            await self.session.set_context(
                user_id,  # 这里应该是session_id
                f"search_{keyword}",
                {"count": 1, "timestamp": int(time.time())}
            )
    
    async def _handle_order(
        self,
        user_id: str,
        interaction: Dict
    ):
        """处理订单"""
        await self.profile.record_behavior(
            user_id=user_id,
            behavior_type="purchase",
            data={
                "product_id": interaction.get("product_id"),
                "category": interaction.get("category"),
                "amount": interaction.get("amount"),
                "supplier_id": interaction.get("supplier_id")
            }
        )
        
        # 更新供应商偏好
        if interaction.get("supplier_id"):
            await self.persistent.update_supplier_preference(
                user_id=user_id,
                supplier_id=interaction["supplier_id"],
                order_amount=interaction.get("amount", 0),
                rating=interaction.get("rating")
            )
    
    async def _handle_message(
        self,
        user_id: str,
        session_id: str,
        interaction: Dict
    ):
        """处理消息"""
        await self.session.append_message(
            session_id=session_id,
            role=interaction.get("role", "user"),
            content=interaction.get("content", ""),
            metadata=interaction.get("metadata")
        )
    
    async def periodic_consolidation(self, user_id: str):
        """定期整合记忆"""
        
        # 获取最近会话
        conversations = await self.persistent.get_user_conversations(user_id, limit=10)
        
        if len(conversations) >= 5:
            # 生成会话摘要
            summary = await self._generate_conversation_summary(conversations)
            
            # 更新用户画像
            await self.profile.update_profile(
                user_id,
                {"metadata.summary": summary}
            )
    
    async def _generate_conversation_summary(
        self,
        conversations: List
    ) -> str:
        """生成会话摘要"""
        # 可以使用LLM生成摘要
        return "用户近期关注XXX类商品，多次询价但未下单"
```

---

## 六、与Agent集成接口

### 6.1 Agent记忆接口

```python
# agent_memory_interface.py

class AgentMemoryInterface:
    """Agent记忆接口"""
    
    def __init__(self, retriever: MemoryRetriever, updater: MemoryUpdater):
        self.retriever = retriever
        self.updater = updater
    
    async def get_context_for_agent(
        self,
        agent_type: str,
        user_id: str,
        session_id: str,
        current_query: str
    ) -> Dict[str, Any]:
        """为Agent获取上下文"""
        
        # 1. 检索相关记忆
        results = await self.retriever.retrieve(RetrievalRequest(
            query=current_query,
            memory_types=["session", "persistent", "profile"],
            user_id=user_id,
            session_id=session_id,
            limit=10
        ))
        
        # 2. 根据Agent类型格式化
        context = {
            "relevant_memories": results,
            "user_profile": None,
            "session_history": []
        }
        
        # 获取用户画像
        from user_profile import UserProfileManager
        if hasattr(self.retriever.profile, 'get_profile'):
            profile = await self.retriever.profile.get_profile(user_id)
            context["user_profile"] = profile
        
        # 获取会话历史
        session_messages = await self.retriever.session.get_messages(
            session_id, limit=10
        )
        context["session_history"] = session_messages
        
        return context
    
    async def record_agent_action(
        self,
        agent_type: str,
        user_id: str,
        session_id: str,
        action: str,
        result: Any
    ):
        """记录Agent行为"""
        
        await self.updater.update_after_interaction(
            user_id=user_id,
            session_id=session_id,
            interaction={
                "type": "agent_action",
                "agent_type": agent_type,
                "action": action,
                "result": result
            }
        )
```

### 6.2 集成示例

```python
# integration_example.py

class ProductAgentMemory:
    """Product Agent 记忆集成"""
    
    def __init__(self, memory_interface: AgentMemoryInterface):
        self.memory = memory_interface
    
    async def prepare_product_matching(
        self,
        user_id: str,
        session_id: str,
        query: str
    ) -> Dict:
        """准备商品匹配上下文"""
        
        context = await self.memory.get_context_for_agent(
            agent_type="product",
            user_id=user_id,
            session_id=session_id,
            current_query=query
        )
        
        # 提取用户偏好
        profile = context.get("user_profile")
        preferences = {}
        
        if profile:
            preferences = {
                "favorite_categories": profile.favorite_categories,
                "price_sensitivity": profile.price_sensitivity,
                "quality_preference": profile.quality_preference,
                "preferred_moq": profile.preferred_moq
            }
        
        # 构建Prompt上下文
        return {
            "query": query,
            "user_preferences": preferences,
            "recent_views": self._extract_recent_views(context),
            "similar_searches": self._extract_similar_searches(context),
            "hot_products": await self._get_hot_products()
        }
    
    def _extract_recent_views(self, context: Dict) -> List[str]:
        """提取最近浏览"""
        views = []
        for memory in context.get("relevant_memories", []):
            if memory.memory_type == "persistent" and \
               memory.metadata.get("role") == "assistant":
                # 提取推荐过的商品
                pass
        return views[:5]
    
    def _extract_similar_searches(self, context: Dict) -> List[str]:
        """提取相似搜索"""
        searches = []
        for msg in context.get("session_history", []):
            if msg.get("role") == "user":
                searches.append(msg.get("content", ""))
        return searches[-3:]
    
    async def _get_hot_products(self) -> List[Dict]:
        """获取热门商品"""
        return []  # 从商品服务获取
```

---

## 七、性能与成本

### 7.1 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 会话记忆读写 | < 5ms | P99 |
| 持久记忆查询 | < 100ms | 含FTS |
| 用户画像读取 | < 10ms | 含缓存 |
| 记忆检索 | < 200ms | 全层检索 |
| 数据持久化 | < 1s | 异步批量 |

### 7.2 存储成本估算

| 存储类型 | 数据量 | 月成本(¥) |
|---------|--------|----------|
| Redis会话 | 100GB | 500 |
| SQLite持久 | 50GB | 100 |
| 用户画像 | 10GB | 50 |
| **合计** | 160GB | **650** |
