# -*- coding: utf-8 -*-
"""
Memory Graph Core — SQLite 实体的关系图谱存储
供 skill-compounding 调用：add_entity / add_relation / query / traverse
"""
import sqlite3, hashlib, json, os
from datetime import datetime

GRAPH_DIR = r"C:\Users\37845\.qclaw\workspace\knowledge"
DB_PATH = os.path.join(GRAPH_DIR, "graph.db")

def _get_conn():
    os.makedirs(GRAPH_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化图数据库（幂等）"""
    with _get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS nodes (
                id       TEXT PRIMARY KEY,   -- SHA-256(name + type)
                type_    TEXT,              -- 项目/技术/决策/日期/人物/技能/工具
                name     TEXT,
                meta     TEXT DEFAULT '{}',  -- JSON 扩展属性
                updated_at INTEGER
            );
            CREATE TABLE IF NOT EXISTS edges (
                id       TEXT PRIMARY KEY,   -- SHA-256(source + rel + target)
                source   TEXT,
                rel      TEXT,              -- 因果/包含/依赖/触发/使用/产生
                target   TEXT,
                weight   REAL DEFAULT 1.0,
                meta     TEXT DEFAULT '{}',
                updated_at INTEGER,
                FOREIGN KEY (source) REFERENCES nodes(id),
                FOREIGN KEY (target) REFERENCES nodes(id)
            );
            CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type_);
            CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source);
            CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target);
            CREATE INDEX IF NOT EXISTS idx_edges_rel ON edges(rel);
        """)

def _node_id(name: str, type_: str) -> str:
    return hashlib.sha256(f"{type_}:{name}".encode()).hexdigest()[:16]

def _edge_id(source: str, rel: str, target: str) -> str:
    return hashlib.sha256(f"{source}|{rel}|{target}".encode()).hexdigest()[:16]

def add_entity(type_: str, name: str, meta: dict = None) -> str:
    """
    添加或更新实体，返回 entity_id。
    如果实体已存在则更新 meta 和 updated_at，不重复创建。
    """
    nid = _node_id(name, type_)
    now = int(datetime.now().timestamp())
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO nodes (id, type_, name, meta, updated_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                meta = excluded.meta,
                updated_at = excluded.updated_at
        """, (nid, type_, name, meta_json, now))
    return nid

def add_relation(source: str, rel: str, target: str, weight: float = 1.0, meta: dict = None) -> str:
    """添加或更新边，返回 edge_id。source/target 支持 entity_id 或 name#type 格式。"""
    # 解析 source/target：如果包含 # 视为 name#type，否则视为 entity_id
    src_id = source if len(source) == 16 else _resolve_id(source)
    tgt_id = target if len(target) == 16 else _resolve_id(target)
    if not src_id or not tgt_id:
        return None  # 解析失败，不存在对应实体
    eid = _edge_id(src_id, rel, tgt_id)
    now = int(datetime.now().timestamp())
    meta_json = json.dumps(meta or {}, ensure_ascii=False)
    with _get_conn() as conn:
        conn.execute("""
            INSERT INTO edges (id, source, rel, target, weight, meta, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                weight = excluded.weight,
                meta = excluded.meta,
                updated_at = excluded.updated_at
        """, (eid, src_id, rel, tgt_id, weight, meta_json, now))
    return eid

def _resolve_id(key: str) -> str | None:
    """解析 name#type 或 entity_id。如果 key 不含 # 且非 entity_id，则尝试模糊匹配 name。"""
    if "#" in key:
        name, type_ = key.rsplit("#", 1)
        return _node_id(name.strip(), type_.strip())
    # 假设是 entity_id，直接查询存在性
    with _get_conn() as conn:
        row = conn.execute("SELECT id FROM nodes WHERE id = ?", (key,)).fetchone()
        if row:
            return row["id"]
        # entity_id 查不到，尝试 name 模糊匹配（取第一个）
        row = conn.execute("SELECT id FROM nodes WHERE name LIKE ? LIMIT 1",
                           (f"%{key}%",)).fetchone()
        return row["id"] if row else None

def query(keyword: str, type_: str = None, limit: int = 20) -> list[dict]:
    """模糊搜索实体：按 name 匹配 keyword，可选按 type_ 过滤。"""
    with _get_conn() as conn:
        if type_:
            rows = conn.execute("""
                SELECT * FROM nodes
                WHERE name LIKE ? AND type_ = ?
                ORDER BY updated_at DESC LIMIT ?
            """, (f"%{keyword}%", type_, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM nodes
                WHERE name LIKE ?
                ORDER BY updated_at DESC LIMIT ?
            """, (f"%{keyword}%", limit)).fetchall()
        return [dict(r) for r in rows]

def traverse(start: str, rel: str = None, direction: str = "out", limit: int = 20) -> list[dict]:
    """
    图遍历：从 start 实体出发沿边扩展。
    - direction=out：找 start 指向的节点（start → ?）
    - direction=in：找指向 start 的节点（? → start）
    - direction=both：双向
    - rel 可选，限制关系类型
    """
    src_id = start if len(start) == 16 else _resolve_id(start)
    if not src_id:
        return []
    with _get_conn() as conn:
        if direction == "out":
            sql = """SELECT e.*, n.name AS target_name, n.type_ AS target_type
                     FROM edges e JOIN nodes n ON e.target = n.id
                     WHERE e.source = ?"""
            params = [src_id]
        elif direction == "in":
            sql = """SELECT e.*, n.name AS source_name, n.type_ AS source_type
                     FROM edges e JOIN nodes n ON e.source = n.id
                     WHERE e.target = ?"""
            params = [src_id]
        else:  # both
            sql = """SELECT e.*,
                     sn.name AS source_name, sn.type_ AS source_type,
                     tn.name AS target_name, tn.type_ AS target_type
                     FROM edges e
                     JOIN nodes sn ON e.source = sn.id
                     JOIN nodes tn ON e.target = tn.id
                     WHERE e.source = ? OR e.target = ?"""
            params = [src_id, src_id]
        if rel:
            sql += " AND e.rel = ?"
            params.append(rel)
        sql += " ORDER BY e.weight DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(sql, params).fetchall()
        return [dict(r) for r in rows]

def get_path(from_: str, to: str, max_depth: int = 3) -> list[dict]:
    """
    找 from_ 到 to 的最短路径（BFS，限深 max_depth）。
    返回路径上的边列表，每条边含 source/rel/target。
    """
    src_id = from_ if len(from_) == 16 else _resolve_id(from_)
    tgt_id = to   if len(to)   == 16 else _resolve_id(to)
    if not src_id or not tgt_id:
        return []
    if src_id == tgt_id:
        return [{"source": src_id, "rel": "same", "target": tgt_id}]

    with _get_conn() as conn:
        visited = {src_id}
        queue = [(src_id, [])]
        while queue:
            current, path = queue.pop(0)
            if len(path) >= max_depth:
                continue
            rows = conn.execute("""
                SELECT source, rel, target FROM edges
                WHERE source = ? OR target = ?
            """, (current, current)).fetchall()
            for row in rows:
                neighbor = row["target"] if row["source"] == current else row["source"]
                if neighbor in visited:
                    continue
                edge = {"source": row["source"], "rel": row["rel"], "target": row["target"]}
                new_path = path + [edge]
                if neighbor == tgt_id:
                    return new_path
                visited.add(neighbor)
                queue.append((neighbor, new_path))
        return []

def stats() -> dict:
    """返回图谱统计信息"""
    with _get_conn() as conn:
        n_nodes = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        n_edges = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        types = conn.execute("SELECT type_, COUNT(*) FROM nodes GROUP BY type_").fetchall()
        rels = conn.execute("SELECT rel, COUNT(*) FROM edges GROUP BY rel ORDER BY COUNT(*) DESC").fetchall()
        return {
            "nodes": n_nodes,
            "edges": n_edges,
            "by_type": [dict(r) for r in types],
            "by_rel": [dict(r) for r in rels],
            "db_path": DB_PATH
        }

# 初始化
init_db()