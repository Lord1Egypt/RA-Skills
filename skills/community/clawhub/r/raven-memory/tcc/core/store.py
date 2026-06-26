from __future__ import annotations

import json
import sqlite3
import threading
import warnings
from collections import deque
from typing import Callable, Optional

from .node import TCCNode

VALID_STATUSES = {"running", "done", "failed"}


class TCCError(Exception):
    pass


class NodeNotFoundError(TCCError):
    pass


class DuplicateNodeError(TCCError):
    pass


class DAGError(TCCError):
    pass


class InvalidStatusError(TCCError):
    pass


NODE_COLUMNS = [
    "hash",
    "node_type",
    "timestamp",
    "actor",
    "session_key",
    "session_id",
    "event",
    "status",
    "branch_id",
    "transcript_ref",
    "tool_name",
    "tool_args_hash",
    "duration_ms",
    "result_summary",
    "file_path",
    "content",
    "trigger",
    "subtype",
    "summary",
    "open_threads",
    "token_count",
]


class TCCStore:
    def __init__(self, path: str = ":memory:", on_status_update: Optional[Callable] = None):
        self.path = path
        self._lock = threading.Lock()
        self._on_status_update = on_status_update
        self._conn = sqlite3.connect(path, check_same_thread=False)
        if path != ":memory:":
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.execute("PRAGMA cache_size=-64000")
            self._conn.execute("PRAGMA temp_store=MEMORY")
            self._conn.commit()
        self._vec_enabled = self._load_sqlite_vec(self._conn)
        self._init_schema()

    def _load_sqlite_vec(self, conn: sqlite3.Connection) -> bool:
        """Load sqlite-vec extension if available."""
        if self.path == ":memory:":
            return False
        try:
            import sqlite_vec

            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            conn.enable_load_extension(False)
            return True
        except Exception as exc:
            warnings.warn(
                f"sqlite-vec not available — semantic search disabled: {exc}",
                UserWarning,
            )
            return False

    def _init_schema(self):
        with self._lock:
            cur = self._conn.cursor()
            cur.executescript(
                """
                CREATE TABLE IF NOT EXISTS nodes (
                    hash            TEXT PRIMARY KEY,
                    node_type       TEXT NOT NULL,
                    timestamp       TEXT NOT NULL,
                    actor           TEXT NOT NULL,
                    session_key     TEXT NOT NULL,
                    session_id      TEXT NOT NULL,
                    event           TEXT NOT NULL,
                    status          TEXT NOT NULL,
                    branch_id       TEXT NOT NULL DEFAULT 'main',
                    transcript_ref  TEXT,
                    tool_name       TEXT,
                    tool_args_hash  TEXT,
                    duration_ms     INTEGER,
                    result_summary  TEXT,
                    file_path       TEXT,
                    content         TEXT,
                    trigger         TEXT,
                    subtype         TEXT,
                    summary         TEXT,
                    open_threads    TEXT,
                    token_count     INTEGER
                );
                CREATE TABLE IF NOT EXISTS node_parents (
                    child_hash  TEXT NOT NULL,
                    parent_hash TEXT NOT NULL,
                    PRIMARY KEY (child_hash, parent_hash)
                );
                CREATE INDEX IF NOT EXISTS idx_node_parents_child
                    ON node_parents(child_hash);
                CREATE INDEX IF NOT EXISTS idx_node_parents_parent
                    ON node_parents(parent_hash);
                CREATE TABLE IF NOT EXISTS tool_payloads (
                    args_hash   TEXT PRIMARY KEY,
                    args_json   TEXT NOT NULL,
                    output_json TEXT
                );
                CREATE TABLE IF NOT EXISTS meta (
                    key   TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_session   ON nodes(session_id);
                CREATE INDEX IF NOT EXISTS idx_branch    ON nodes(branch_id);
                CREATE INDEX IF NOT EXISTS idx_status    ON nodes(status);
                CREATE INDEX IF NOT EXISTS idx_timestamp ON nodes(timestamp);
            """
            )
            self._migrate_nodes_schema(cur)
            if self._vec_enabled:
                cur.executescript(
                    """
                    CREATE VIRTUAL TABLE IF NOT EXISTS node_embeddings
                    USING vec0(
                        hash        TEXT PRIMARY KEY,
                        embedding   FLOAT[384]
                    );
                """
                )
            self._conn.commit()

    def _migrate_nodes_schema(self, cur: sqlite3.Cursor) -> None:
        info_rows = cur.execute("PRAGMA table_info(nodes)").fetchall()
        if not info_rows:
            return
        existing_columns = {row[1] for row in info_rows}
        column_types = {
            "node_type": "TEXT",
            "session_key": "TEXT",
            "transcript_ref": "TEXT",
            "tool_name": "TEXT",
            "tool_args_hash": "TEXT",
            "duration_ms": "INTEGER",
            "result_summary": "TEXT",
            "file_path": "TEXT",
            "content": "TEXT",
            "trigger": "TEXT",
            "subtype": "TEXT",
            "summary": "TEXT",
            "open_threads": "TEXT",
            "token_count": "INTEGER",
            "branch_id": "TEXT",
            "event": "TEXT",
            "status": "TEXT",
            "session_id": "TEXT",
            "timestamp": "TEXT",
            "actor": "TEXT",
            "hash": "TEXT",
        }
        for col in NODE_COLUMNS:
            if col not in existing_columns:
                cur.execute(f"ALTER TABLE nodes ADD COLUMN {col} {column_types[col]}")

    def save_node(self, node: TCCNode, parent_hashes: list[str]) -> None:
        with self._lock:
            try:
                cur = self._conn.cursor()
                self._write_node_no_commit(cur, node, parent_hashes)
                # Set root_hash on first ever node
                existing_root = self._conn.execute(
                    "SELECT value FROM meta WHERE key='root_hash'"
                ).fetchone()
                if existing_root is None:
                    self._conn.execute(
                        "INSERT OR IGNORE INTO meta(key,value) VALUES(?,?)",
                        ("root_hash", node.hash),
                    )
                self._conn.commit()
            except sqlite3.IntegrityError:
                self._conn.rollback()
                raise DuplicateNodeError(f"Node {node.hash} already exists")

    def _write_node_no_commit(
        self,
        cur: sqlite3.Cursor,
        node: TCCNode,
        parent_hashes: list[str],
    ) -> None:
        """Write node + parents without committing. Caller owns the transaction."""
        values = tuple(getattr(node, col) for col in NODE_COLUMNS)
        cur.execute(
            f"INSERT OR IGNORE INTO nodes "
            f"({', '.join(NODE_COLUMNS)}) "
            f"VALUES ({', '.join(['?'] * len(NODE_COLUMNS))})",
            values,
        )
        if parent_hashes:
            cur.executemany(
                "INSERT OR IGNORE INTO node_parents"
                "(child_hash, parent_hash) VALUES (?, ?)",
                [(node.hash, ph) for ph in parent_hashes],
            )

    def save_nodes_batch(self, items: list[tuple[TCCNode, list[str]]]) -> None:
        """Write multiple nodes in a single transaction."""
        with self._lock:
            cur = self._conn.cursor()
            for node, parent_hashes in items:
                self._write_node_no_commit(cur, node, parent_hashes)
            if items:
                existing_root = self._conn.execute(
                    "SELECT value FROM meta WHERE key='root_hash'"
                ).fetchone()
                if existing_root is None:
                    self._conn.execute(
                        "INSERT OR IGNORE INTO meta(key,value) VALUES(?,?)",
                        ("root_hash", items[0][0].hash),
                    )
            self._conn.commit()

    def save(self, node: TCCNode) -> None:
        parent_hashes = list(getattr(node, "parent_hashes", ()))
        self.save_node(node, parent_hashes=parent_hashes)

    def save_tool_payload(self, args_hash: str, args_json: str, output_json: str | None) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR IGNORE INTO tool_payloads(args_hash, args_json, output_json) VALUES (?, ?, ?)",
                (args_hash, args_json, output_json),
            )
            self._conn.commit()

    def get_tool_payload(self, args_hash: str) -> dict | None:
        with self._lock:
            row = self._conn.execute(
                "SELECT args_json, output_json FROM tool_payloads WHERE args_hash=?",
                (args_hash,),
            ).fetchone()
        if not row:
            return None
        return {"args": row[0], "output": row[1]}

    def get_parents(self, hash: str) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT parent_hash FROM node_parents WHERE child_hash=?",
                (hash,),
            ).fetchall()
        return [row[0] for row in rows]

    def get_children(self, hash: str) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT child_hash FROM node_parents WHERE parent_hash=?",
                (hash,),
            ).fetchall()
        return [row[0] for row in rows]

    def ancestors(self, hash: str, max_depth: int = 50) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                """
                WITH RECURSIVE anc(hash, depth) AS (
                    SELECT parent_hash, 1
                    FROM node_parents
                    WHERE child_hash = ?
                    UNION ALL
                    SELECT np.parent_hash, anc.depth + 1
                    FROM node_parents np
                    JOIN anc ON np.child_hash = anc.hash
                    WHERE anc.depth < ?
                )
                SELECT hash, MIN(depth) AS d
                FROM anc
                GROUP BY hash
                ORDER BY d ASC;
                """,
                (hash, max_depth),
            ).fetchall()
        return [row[0] for row in rows]

    def descendants(self, hash: str, max_depth: int = 50) -> list[str]:
        with self._lock:
            rows = self._conn.execute(
                """
                WITH RECURSIVE des(hash, depth) AS (
                    SELECT child_hash, 1
                    FROM node_parents
                    WHERE parent_hash = ?
                    UNION ALL
                    SELECT np.child_hash, des.depth + 1
                    FROM node_parents np
                    JOIN des ON np.parent_hash = des.hash
                    WHERE des.depth < ?
                )
                SELECT hash, MIN(depth) AS d
                FROM des
                GROUP BY hash
                ORDER BY d ASC;
                """,
                (hash, max_depth),
            ).fetchall()
        return [row[0] for row in rows]

    def path_between(self, from_hash: str, to_hash: str) -> list[str]:
        if from_hash == to_hash:
            return [from_hash]
        queue: deque[str] = deque([from_hash])
        prev: dict[str, str | None] = {from_hash: None}

        while queue:
            current = queue.popleft()
            for child in self.get_children(current):
                if child in prev:
                    continue
                prev[child] = current
                if child == to_hash:
                    path = [to_hash]
                    node = to_hash
                    while prev[node] is not None:
                        node = prev[node]  # type: ignore[index]
                        path.append(node)
                    return list(reversed(path))
                queue.append(child)
        return []

    def get_node(self, hash: str) -> TCCNode:
        return self.load(hash)

    def load(self, hash: str) -> TCCNode:
        with self._lock:
            row = self._conn.execute(
                f"SELECT {', '.join(NODE_COLUMNS)} FROM nodes WHERE hash=?",
                (hash,),
            ).fetchone()
        if not row:
            raise NodeNotFoundError(f"Node {hash} not found")
        return self._row_to_node(row)

    def get_all_nodes(self) -> list[TCCNode]:
        return self.load_all()

    def load_all(self) -> list[TCCNode]:
        with self._lock:
            rows = self._conn.execute(
                f"SELECT {', '.join(NODE_COLUMNS)} FROM nodes ORDER BY timestamp ASC"
            ).fetchall()
        return [self._row_to_node(r) for r in rows]

    def nodes_for_session(self, session_id: str) -> list[TCCNode]:
        with self._lock:
            rows = self._conn.execute(
                f"SELECT {', '.join(NODE_COLUMNS)} FROM nodes WHERE session_id=? ORDER BY timestamp ASC",
                (session_id,),
            ).fetchall()
        return [self._row_to_node(row) for row in rows]

    def embed_all(
        self,
        show_progress: bool = False,
        batch_size: int = 32,
    ) -> int:
        if not self._vec_enabled:
            return 0

        try:
            from .embedder import get_embedder

            with self._lock:
                all_hashes = {r[0] for r in self._conn.execute("SELECT hash FROM nodes").fetchall()}
                embedded_hashes = {
                    r[0] for r in self._conn.execute("SELECT hash FROM node_embeddings").fetchall()
                }

            to_embed = list(all_hashes - embedded_hashes)
            if not to_embed:
                return 0

            nodes = [self.load(h) for h in to_embed]
            texts = [n.event for n in nodes]

            model = get_embedder()
            all_vecs = model.encode(
                texts,
                batch_size=batch_size,
                normalize_embeddings=True,
                show_progress_bar=show_progress,
            )

            with self._lock:
                for node, vec in zip(nodes, all_vecs):
                    self._conn.execute(
                        "INSERT OR REPLACE INTO node_embeddings(hash, embedding) VALUES (?, ?)",
                        (node.hash, json.dumps(vec.tolist())),
                    )
                self._conn.commit()

            return len(nodes)

        except Exception as exc:
            warnings.warn(f"embed_all failed: {exc}", UserWarning)
            return 0

    def update_status(self, hash: str, status: str) -> None:
        if status not in VALID_STATUSES:
            raise InvalidStatusError(f"Invalid status: {status}")
        with self._lock:
            affected = self._conn.execute(
                "UPDATE nodes SET status=? WHERE hash=?", (status, hash)
            ).rowcount
            self._conn.commit()
        if affected == 0:
            raise NodeNotFoundError(f"Node {hash} not found")
        if self._on_status_update:
            self._on_status_update(hash, status)

    def query_before(self, timestamp: str) -> list[TCCNode]:
        with self._lock:
            rows = self._conn.execute(
                f"SELECT {', '.join(NODE_COLUMNS)} FROM nodes WHERE timestamp < ? ORDER BY timestamp ASC",
                (timestamp,),
            ).fetchall()
        return [self._row_to_node(r) for r in rows]

    def delete(self, hashes: list[str]) -> None:
        with self._lock:
            self._conn.executemany("DELETE FROM nodes WHERE hash=?", [(h,) for h in hashes])
            self._conn.executemany("DELETE FROM node_parents WHERE child_hash=?", [(h,) for h in hashes])
            self._conn.executemany("DELETE FROM node_parents WHERE parent_hash=?", [(h,) for h in hashes])
            self._conn.commit()

    def get_meta(self, key: str) -> Optional[str]:
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key=?", (key,)).fetchone()
        return row[0] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._lock:
            self._conn.execute("INSERT OR REPLACE INTO meta(key,value) VALUES(?,?)", (key, value))
            self._conn.commit()

    def get_tip_hash(self) -> Optional[str]:
        return self.get_meta("tip_hash")

    def set_tip_hash(self, hash: str) -> None:
        self.set_meta("tip_hash", hash)

    def get_branch_tip(self, branch_id: str) -> Optional[str]:
        return self.get_meta(f"branch_{branch_id}_tip")

    def set_branch_tip(self, branch_id: str, hash: str) -> None:
        self.set_meta(f"branch_{branch_id}_tip", hash)

    def get_all_branches(self) -> dict[str, str]:
        with self._lock:
            rows = self._conn.execute(
                "SELECT key, value FROM meta WHERE key LIKE 'branch_%_tip'"
            ).fetchall()
        result = {}
        for key, value in rows:
            branch_id = key[len("branch_") : -len("_tip")]
            if branch_id == "main":
                continue
            merged = self.get_meta(f"branch_{branch_id}_merged")
            if not merged:
                result[branch_id] = value
        return result

    def mark_branch_merged(self, branch_id: str) -> None:
        self.set_meta(f"branch_{branch_id}_merged", "true")

    def search(
        self,
        query: str,
        n: int = 5,
        session_id: str | None = None,
    ) -> list[TCCNode]:
        if not self._vec_enabled:
            return []

        try:
            from .embedder import embed

            vec = embed(query)
            vec_json = json.dumps(vec)

            with self._lock:
                if session_id:
                    rows = self._conn.execute(
                        """
                        SELECT n.hash
                        FROM node_embeddings e
                        JOIN nodes n ON e.hash = n.hash
                        WHERE n.session_id = ?
                        ORDER BY vec_distance_cosine(e.embedding, ?) ASC
                        LIMIT ?
                        """,
                        (session_id, vec_json, n),
                    ).fetchall()
                else:
                    rows = self._conn.execute(
                        """
                        SELECT hash
                        FROM node_embeddings
                        ORDER BY vec_distance_cosine(embedding, ?) ASC
                        LIMIT ?
                        """,
                        (vec_json, n),
                    ).fetchall()

            return [self.load(row[0]) for row in rows]
        except Exception as exc:
            warnings.warn(f"Search failed: {exc}", UserWarning)
            return []

    @property
    def is_vec_enabled(self) -> bool:
        return self._vec_enabled

    def _row_to_node(self, row) -> TCCNode:
        return TCCNode(
            hash=row[0],
            node_type=row[1],
            timestamp=row[2],
            actor=row[3],
            session_key=row[4],
            session_id=row[5],
            event=row[6],
            status=row[7],
            branch_id=row[8],
            transcript_ref=row[9],
            tool_name=row[10],
            tool_args_hash=row[11],
            duration_ms=row[12],
            result_summary=row[13],
            file_path=row[14],
            content=row[15],
            trigger=row[16],
            subtype=row[17],
            summary=row[18],
            open_threads=row[19],
            token_count=row[20],
        )
