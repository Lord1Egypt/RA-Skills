#!/usr/bin/env python3
"""
TagMemory - SQLite FTS5 数据库模块
支持 BM25 搜索的标签化记忆存储
"""

import sqlite3
import json
import uuid
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from pathlib import Path
import os

@dataclass
class Memory:
    id: str
    content: str
    summary: str = ""
    tags: List[str] = None
    time_label: str = ""  # YYYY-MM 格式
    created_at: str = ""
    updated_at: str = ""
    verified: bool = False
    verified_at: Optional[str] = None
    source: str = "dialogue"  # dialogue, summary, manual
    agent_id: str = "main"  # 哪个 agent 产生的
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.id:
            self.id = str(uuid.uuid4())
    
    def to_dict(self):
        return asdict(self)
    
    @staticmethod
    def from_dict(d):
        return Memory(**d)


class MemoryDatabase:
    """SQLite FTS5 记忆数据库"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = os.path.expanduser("~/.openclaw/workspace/skills/tag-memory/data/memory.db")
        
        # 确保目录存在
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self):
        """初始化数据库 schema"""
        cursor = self.conn.cursor()
        
        # 主表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                summary TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                time_label TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                verified INTEGER DEFAULT 0,
                verified_at TEXT,
                source TEXT DEFAULT 'dialogue',
                agent_id TEXT DEFAULT 'main'
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_time_label ON memories(time_label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON memories(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_verified ON memories(verified)")
        
        # FTS5 虚拟表（如果不存在）
        try:
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                    content,
                    tags,
                    content='memories',
                    content_rowid='rowid'
                )
            """)
        except sqlite3.OperationalError as e:
            if "already exists" not in str(e):
                raise
        
        # 触发器：自动同步 FTS
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
                INSERT INTO memories_fts(rowid, content, tags) 
                VALUES (new.rowid, new.content, new.tags);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content, tags) 
                VALUES ('delete', old.rowid, old.content, old.tags);
            END
        """)
        
        cursor.execute("""
            CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
                INSERT INTO memories_fts(memories_fts, rowid, content, tags) 
                VALUES ('delete', old.rowid, old.content, old.tags);
                INSERT INTO memories_fts(rowid, content, tags) 
                VALUES (new.rowid, new.content, new.tags);
            END
        """)
        
        self.conn.commit()
    
    def insert(self, memory: Memory) -> str:
        """插入记忆，返回 ID"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memories (id, content, summary, tags, time_label, 
                                  created_at, updated_at, verified, source, agent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            memory.id,
            memory.content,
            memory.summary,
            json.dumps(memory.tags, ensure_ascii=False),
            memory.time_label,
            memory.created_at,
            memory.updated_at,
            1 if memory.verified else 0,
            memory.source,
            memory.agent_id
        ))
        self.conn.commit()
        return memory.id
    
    def update(self, memory_id: str, updates: dict) -> bool:
        """更新记忆"""
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now().isoformat()
        
        # 处理 tags 列表
        if 'tags' in updates and isinstance(updates['tags'], list):
            updates['tags'] = json.dumps(updates['tags'], ensure_ascii=False)
        
        # 处理 verified 布尔值
        if 'verified' in updates:
            updates['verified'] = 1 if updates['verified'] else 0
        
        set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
        values = list(updates.values()) + [memory_id]
        
        cursor = self.conn.cursor()
        cursor.execute(f"UPDATE memories SET {set_clause} WHERE id = ?", values)
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete(self, memory_id: str) -> bool:
        """删除记忆"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def get(self, memory_id: str) -> Optional[Memory]:
        """获取单条记忆"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM memories WHERE id = ?", (memory_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_memory(row)
        return None
    
    def get_all(self, limit: int = 100, offset: int = 0, 
                verified_only: bool = False, tags: List[str] = None,
                agent_id: str = None) -> List[Memory]:
        """获取所有记忆
        
        Args:
            agent_id: 可选，按 agent 过滤
        """
        cursor = self.conn.cursor()
        
        where_clauses = []
        params = []
        
        if verified_only:
            where_clauses.append("verified = 1")
        
        if tags:
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            where_clauses.append(f"({tag_conditions})")
            params.extend([f'%"{t}"%' for t in tags])
        
        if agent_id:
            where_clauses.append("agent_id = ?")
            params.append(agent_id)
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        cursor.execute(f"""
            SELECT * FROM memories 
            WHERE {where_sql}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (*params, limit, offset))
        
        return [self._row_to_memory(row) for row in cursor.fetchall()]
    
    def count(self, verified_only: bool = False, tags: List[str] = None,
              agent_id: str = None) -> int:
        """统计记忆数量"""
        cursor = self.conn.cursor()
        
        where_clauses = []
        params = []
        
        if verified_only:
            where_clauses.append("verified = 1")
        
        if tags:
            tag_conditions = " OR ".join(["tags LIKE ?" for _ in tags])
            where_clauses.append(f"({tag_conditions})")
            params.extend([f'%"{t}"%' for t in tags])
        
        if agent_id:
            where_clauses.append("agent_id = ?")
            params.append(agent_id)
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        cursor.execute(f"SELECT COUNT(*) FROM memories WHERE {where_sql}", params)
        return cursor.fetchone()[0]
    
    def _row_to_memory(self, row: sqlite3.Row) -> Memory:
        """将数据库行转换为 Memory 对象"""
        tags = row['tags']
        if isinstance(tags, str):
            tags = json.loads(tags)
        
        # agent_id 可能不存在于旧数据
        try:
            agent_id = row['agent_id']
        except (KeyError, IndexError):
            agent_id = 'main'
        
        return Memory(
            id=row['id'],
            content=row['content'],
            summary=row['summary'] or '',
            tags=tags,
            time_label=row['time_label'] or '',
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            verified=bool(row['verified']),
            verified_at=row['verified_at'],
            source=row['source'] or 'dialogue',
            agent_id=agent_id or 'main'
        )
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()
    
    def migrate_add_agent_id(self):
        """迁移：添加 agent_id 列"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT agent_id FROM memories LIMIT 1")
            print("agent_id 列已存在")
        except:
            print("添加 agent_id 列...")
            cursor.execute("ALTER TABLE memories ADD COLUMN agent_id TEXT DEFAULT 'main'")
            self.conn.commit()
            print("✅ 迁移完成")


def bm25_search(db: MemoryDatabase, query: str, 
                 tags: List[str] = None,
                 time_range: Tuple[str, str] = None,
                 limit: int = 10) -> List[Tuple[Memory, float]]:
    """
    BM25 搜索
    
    Returns: List of (Memory, bm25_score) sorted by score descending
    """
    cursor = db.conn.cursor()
    
    # 构建 WHERE 条件
    where_clauses = ["memories_fts MATCH ?"]
    params = [_build_fts_query(query)]
    
    if tags:
        tag_fts = " OR ".join([f'"{t}"' for t in tags])
        where_clauses.append(f"memories.tags LIKE '%' || ? || '%'")
        params.append(tags[0])  # SQLite FTS5 不直接支持数组，这里简化
    
    if time_range:
        where_clauses.append("time_label >= ? AND time_label <= ?")
        params.extend(time_range)
    
    where_sql = " AND ".join(where_clauses)
    
    # BM25 搜索
    sql = f"""
        SELECT memories.*, 
               bm25(memories_fts) as bm25_score
        FROM memories_fts
        JOIN memories ON memories.rowid = memories_fts.rowid
        WHERE {where_sql}
        ORDER BY bm25_score
        LIMIT ?
    """
    params.append(limit)
    
    cursor.execute(sql, params)
    
    results = []
    for row in cursor.fetchall():
        memory = db._row_to_memory(row)
        bm25_score = row['bm25_score']
        results.append((memory, bm25_score))
    
    return results


def _build_fts_query(query: str) -> str:
    """构建 FTS5 查询字符串"""
    import re
    
    # 预处理：移除或转义 FTS5 特殊字符
    # FTS5 特殊字符: " * ^ - + ( ) : AND OR NOT NEAR
    # 简单策略：用双引号包裹整个查询词，对特殊字符进行转义
    special_chars = re.compile(r'["\*\^\-\+\(\)\:\s]+')
    
    # 分词
    words = query.split()
    if not words:
        return '""'
    
    # 清理每个词，移除 FTS5 特殊字符
    cleaned_parts = []
    for word in words:
        # 移除首尾的特殊字符
        cleaned = word.strip('"*-^+():')
        # 跳过纯特殊字符的词
        if cleaned and not cleaned.isspace():
            cleaned_parts.append(cleaned)
    
    if not cleaned_parts:
        return '""'
    
    # 用双引号包裹每个词，然后 OR 组合
    quoted_parts = [f'"{p}"' for p in cleaned_parts]
    return " OR ".join(quoted_parts)


# 命令行工具
if __name__ == "__main__":
    import sys
    
    db = MemoryDatabase()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--init":
        print("✅ 数据库初始化完成")
        print(f"📁 数据库路径: {db.db_path}")
        
        # 插入一条测试数据
        test_memory = Memory(
            id=str(uuid.uuid4()),
            content="测试记忆：用户偏好 tabs 缩进",
            tags=["#偏好", "#编程"],
            time_label="2026-03"
        )
        db.insert(test_memory)
        print("✅ 测试数据已插入")
        
        # 测试搜索
        results = bm25_search(db, "tabs 缩进", limit=5)
        print(f"\n🔍 搜索 'tabs 缩进' 结果:")
        for memory, score in results:
            print(f"  - [{score:.2f}] {memory.content[:50]}...")
        
    elif len(sys.argv) > 1 and sys.argv[1] == "--stats":
        print(f"📊 记忆统计:")
        print(f"  - 总数: {db.count()}")
        print(f"  - 已确认: {db.count(verified_only=True)}")
    else:
        print("用法:")
        print("  python database.py --init   # 初始化数据库")
        print("  python database.py --stats  # 查看统计")
