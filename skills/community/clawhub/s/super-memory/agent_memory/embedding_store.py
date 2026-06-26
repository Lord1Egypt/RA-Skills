"""
embedding_store.py - SQLite + sqlite-vec 向量存储 + 语义搜索

v6.0: 从 Chroma 迁移到 sqlite-vec，消灭双写架构。
向量和结构化数据在同一 SQLite 文件中，事务级一致性。

支持多种 embedding 后端（通过环境变量配置）:
  AGENT_MEMORY_EMBEDDING_BACKEND=local     — SentenceTransformer 本地模型 (默认)
  AGENT_MEMORY_EMBEDDING_BACKEND=openai    — OpenAI text-embedding-3-*
  AGENT_MEMORY_EMBEDDING_BACKEND=cohere    — Cohere embed-v3
  AGENT_MEMORY_EMBEDDING_BACKEND=voyage    — Voyage AI
  AGENT_MEMORY_EMBEDDING_BACKEND=hash      — SimHash 降级 (无语义能力)

模型配置:
  AGENT_MEMORY_EMBEDDING_MODEL=model_name  — 覆盖默认模型
  AGENT_MEMORY_EMBEDDING_DIM=512           — 覆盖向量维度
"""

from __future__ import annotations

import os
import math
import hashlib
import logging
import sqlite3
import threading
import warnings

from .utils import _validate_url

logger = logging.getLogger(__name__)

try:
    import sqlite_vec
    _HAS_SQLITE_VEC = True
except ImportError:
    _HAS_SQLITE_VEC = False

# 全局抑制 embedding 相关的非关键警告
warnings.filterwarnings("ignore", message=".*position_ids.*")
warnings.filterwarnings("ignore", message=".*safetensors.*")
warnings.filterwarnings("ignore", message=".*PyTorch.*")

# HuggingFace 镜像 — 需用户手动设置 HF_ENDPOINT 环境变量切换
_HF_MIRROR = "https://hf-mirror.com"

# 各后端默认模型和维度
_BACKEND_DEFAULTS = {
    "local":   {"model": "BAAI/bge-small-zh-v1.5", "dim": 512},
    "openai":  {"model": "text-embedding-3-small",  "dim": 1536},
    "cohere":  {"model": "embed-multilingual-v3.0", "dim": 1024},
    "voyage":  {"model": "voyage-3",                "dim": 1024},
    "hash":    {"model": "simhash",                  "dim": 512},
}


def _is_local_model_path(path: str) -> bool:
    """判断 model_name 是否为本地路径（目录或文件）"""
    if not path:
        return False
    # 绝对路径或含路径分隔符的相对路径
    if os.path.isabs(path) or ("/" in path and not path.startswith("/")):
        return os.path.isdir(path)
    # Windows 路径
    if "\\" in path:
        return os.path.isdir(path)
    return False


def _ensure_hf_endpoint():
    """检查 HF_ENDPOINT 配置，确保 HuggingFace 镜像可用。

    处理策略：
    1. HF_ENDPOINT 已设置 → 直接使用
    2. huggingface.co 可达 → 无需镜像
    3. 不可达 → 自动设置 HF_ENDPOINT 为 hf-mirror.com

    注意：huggingface_hub 1.16+ 的 hf_hub_download 在某些版本
    不正确读取 HF_ENDPOINT，此时需要用 HfApi(endpoint=...) 方式
    或直接使用本地模型路径绕开。
    """
    if os.environ.get("HF_ENDPOINT"):
        logger.info(f"Using custom HF_ENDPOINT: {os.environ['HF_ENDPOINT']}")
        return
    import socket
    try:
        socket.create_connection(("huggingface.co", 443), timeout=2).close()
    except (socket.timeout, OSError):
        os.environ["HF_ENDPOINT"] = _HF_MIRROR
        logger.info(f"HuggingFace unreachable, auto-set HF_ENDPOINT={_HF_MIRROR}")


def _download_model_via_api(model_name: str, endpoint: str = None) -> str | None:
    """通过 HfApi 从镜像下载模型，返回本地缓存路径；失败返回 None。

    解决 huggingface_hub 1.16+ 的 hf_hub_download 不读 HF_ENDPOINT 的问题：
    直接用 snapshot_download(endpoint=...) 来指定镜像源。
    """
    try:
        from huggingface_hub import snapshot_download
        ep = endpoint or os.environ.get("HF_ENDPOINT")
        local_path = snapshot_download(
            repo_id=model_name,
            endpoint=ep,
            max_workers=2,       # 限制并发，避免大模型下载卡死
        )
        logger.info(f"Model downloaded via HfApi: {model_name} -> {local_path}")
        return local_path
    except Exception as e:
        logger.warning(f"HfApi download failed: {e}")
        return None


class EmbeddingStore:
    """基于 sqlite-vec / ChromaDB 的语义向量存储

    v6.0: 向量存储在同一 SQLite 文件的 vec0 虚拟表中。
    消灭了 Chroma 双写、sync_flags、repair 线程。

    v6.1 Fix (Issue 1 - 原子性): 支持接受外部连接（来自 MemoryStore），
    确保结构化数据和向量在同一个事务内写入。

    v12: ChromaDB 回退 — sqlite-vec 不可用时自动尝试 ChromaDB，
    确保语义搜索在所有环境下可用。

    设计：
    - 首选: vec0 虚拟表存储归一化向量（L2 距离等价余弦距离）
    - 回退: ChromaDB 持久化集合（余弦相似度）
    - 辅助列存 metadata（memory_id, importance, nature_id）
    - 与 memories 表通过 rowid 关联
    """

    def __init__(
        self,
        db_path: str = None,
        model_name: str = None,
        external_conn: sqlite3.Connection = None,
        conn_provider=None,
    ):
        import os
        self._backend = os.environ.get("AGENT_MEMORY_EMBEDDING_BACKEND", "local").lower()

        # 从环境变量或参数推导模型名和维度
        defaults = _BACKEND_DEFAULTS.get(self._backend, _BACKEND_DEFAULTS["local"])
        self._model_name = model_name or os.environ.get("AGENT_MEMORY_EMBEDDING_MODEL", defaults["model"])
        self._dim = int(os.environ.get("AGENT_MEMORY_EMBEDDING_DIM", str(defaults["dim"])))

        self._project_dir = os.path.dirname(__file__)
        self.db_path = db_path or os.path.join(self._project_dir, "memory.db")

        # Fix (Issue 1): 支持外部连接注入，实现真正的单事务原子性
        # Fix (Issue 9 - P0): 新增 conn_provider 可调用对象，
        # 动态返回当前线程的连接（解决 ThreadingMixIn 下的线程安全问题）
        self._conn_provider = conn_provider
        self._external_conn = external_conn  # 向后兼容：固定连接引用

        # 线程本地连接（仅在没有外部连接/conn_provider 时使用）
        self._local = threading.local()

        # 追踪已初始化 vec0 的连接（用 id(conn) 去重，避免 WeakSet 对 Connection 的弱引用限制）
        self._initialized_conn_ids: set[int] = set()

        # 检测 sqlite-vec 是否可用
        self._vec_available: bool = self._check_vec_available()

        # v12: ChromaDB 回退 — sqlite-vec 不可用时尝试 ChromaDB
        self._chroma_client = None
        self._chroma_collection = None
        self._use_chroma = False
        if not self._vec_available:
            self._use_chroma = self._init_chroma_fallback()

        # 确保 vec0 虚拟表存在（仅在可用时）
        if self._vec_available:
            self._ensure_vec_table()

        # 模型状态：懒加载
        self.model = None
        self._use_model = False
        self._use_server = False
        self._model_loaded = False
        self._api_client = None
        self._model_load_lock = threading.Lock()  # Fix (Issue 4): 模型加载互斥锁

        # CLIP 多模态（懒加载）
        self._clip_model = None
        self._clip_processor = None
        self._clip_loaded = False

        # 兼容旧接口
        self._chroma_removed = True

        logger.info(f"EmbeddingStore: backend={self._backend}, model={self._model_name}, "
                    f"dim={self._dim}, vec_available={self._vec_available}, chroma_fallback={self._use_chroma}")

    def _check_vec_available(self) -> bool:
        if not _HAS_SQLITE_VEC:
            return False
        try:
            test_conn = sqlite3.connect(":memory:")
            test_conn.enable_load_extension(True)
            sqlite_vec.load(test_conn)
            test_conn.execute("CREATE VIRTUAL TABLE _vec_test USING vec0(v float[4])")
            test_conn.close()
            return True
        except Exception as e:
            logger.warning(f"sqlite-vec 不可用，向量搜索将降级: {e}")
            return False

    def _init_chroma_fallback(self) -> bool:
        """v12: sqlite-vec 不可用时，尝试 ChromaDB 作为向量存储回退。

        ChromaDB 是纯 Python 实现，无需编译 C 扩展，在所有平台可用。
        数据持久化到 db_path 同级目录下的 _chroma_data/ 子目录。

        Returns:
            True if ChromaDB initialized successfully, False otherwise.
        """
        try:
            import chromadb
            chroma_dir = os.path.join(os.path.dirname(self.db_path), "_chroma_data")
            self._chroma_client = chromadb.PersistentClient(path=chroma_dir)
            self._chroma_collection = self._chroma_client.get_or_create_collection(
                name="agent_memory_vectors",
                metadata={"hnsw:space": "cosine"},
            )
            logger.info(f"ChromaDB 回退初始化成功 (path={chroma_dir}, "
                       f"existing_count={self._chroma_collection.count()})")
            return True
        except ImportError:
            logger.info("chromadb 未安装，语义搜索不可用。安装: pip install chromadb")
            return False
        except Exception as e:
            logger.warning(f"ChromaDB 初始化失败: {e}")
            return False

    def set_connection(self, conn: sqlite3.Connection = None, conn_provider=None):
        """Fix (Issue 1/9): 注入外部连接或连接提供者，实现与 MemoryStore 共享同一事务。

        conn_provider: 可调用对象，每次调用返回当前线程的连接。
                       解决 ThreadingMixIn 下多线程共享固定连接的问题。
        conn: 固定连接引用（向后兼容，单线程场景使用）。
        """
        if not self._vec_available:
            # vec 不可用时仍接受连接（供结构化数据使用），但跳过 vec 初始化
            if conn_provider is not None:
                self._conn_provider = conn_provider
                self._external_conn = None
            elif conn is not None:
                self._external_conn = conn
                self._conn_provider = None
            return

        if conn_provider is not None:
            self._conn_provider = conn_provider
            self._external_conn = None
            # 用 provider 获取一次连接来初始化 vec 表
            sample_conn = conn_provider()
            self._ensure_vec_table_on_conn(sample_conn)
        elif conn is not None:
            self._external_conn = conn
            self._conn_provider = None
            if not _HAS_SQLITE_VEC:
                logger.error("sqlite-vec 未安装: pip install sqlite-vec")
                raise ImportError("sqlite-vec 未安装: pip install sqlite-vec")
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            self._ensure_vec_table_on_conn(conn)

    def _check_vec_dim(self, conn: sqlite3.Connection) -> bool:
        if not _HAS_SQLITE_VEC:
            return True
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
        except Exception:
            return True
        try:
            # 尝试插入一个测试向量来探测维度
            test_vec = [0.0] * self._dim
            c = conn.execute(
                "INSERT INTO memory_vectors(rowid, embedding, memory_id, importance, nature_id) "
                "VALUES ((SELECT COALESCE(MAX(rowid), 0) + 1 FROM memory_vectors), ?, '__dim_test__', 'low', '')",
                (sqlite_vec.serialize_float32(test_vec),)
            )
            # 插入成功，清理测试数据
            conn.execute("DELETE FROM memory_vectors WHERE memory_id = '__dim_test__'")
            return True
        except Exception as e:
            err_msg = str(e).lower()
            if "dimension" in err_msg or "mismatch" in err_msg or "expected" in err_msg:
                logger.warning(f"vec0 维度不匹配（现有表 != 当前 dim={self._dim}），需要重建")
                return False
            # 其他错误（如表不存在）视为正常
            return True

    def _ensure_vec_table_on_conn(self, conn: sqlite3.Connection):
        if not _HAS_SQLITE_VEC:
            logger.error("sqlite-vec 未安装: pip install sqlite-vec")
            raise ImportError("sqlite-vec 未安装: pip install sqlite-vec")
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        try:
            conn.execute(f"""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_vectors USING vec0(
                    embedding float[{self._dim}],
                    +memory_id TEXT,
                    +importance TEXT,
                    +nature_id TEXT
                )
            """)
        except Exception as e:
            logger.debug(f"vec0 表确认: {e}")

        # Fix (Bug 1): 检测维度不匹配，自动重建 vec0 表
        if not self._check_vec_dim(conn):
            logger.warning(f"重建 vec0 虚拟表：维度从旧值切换到 {self._dim}")
            try:
                conn.execute("DROP TABLE IF EXISTS memory_vectors")
                conn.execute(f"""
                    CREATE VIRTUAL TABLE memory_vectors USING vec0(
                        embedding float[{self._dim}],
                        +memory_id TEXT,
                        +importance TEXT,
                        +nature_id TEXT
                    )
                """)
                conn.commit()
                logger.info(f"vec0 虚拟表已重建 (dim={self._dim})，旧向量数据已清空，下次写入将重新生成")
            except Exception as e:
                logger.error(f"vec0 表重建失败: {e}，建议手动删除数据库文件重新初始化")

    def _ensure_vec_on_conn(self, conn: sqlite3.Connection):
        conn_id = id(conn)
        if conn_id in self._initialized_conn_ids:
            return
        if not _HAS_SQLITE_VEC:
            return
        try:
            conn.enable_load_extension(True)
            sqlite_vec.load(conn)
            self._initialized_conn_ids.add(conn_id)
        except Exception as e:
            logger.warning("embedding_store: %s", e)

    @property
    def conn(self) -> sqlite3.Connection:
        """连接获取：优先使用 conn_provider → external_conn → 线程本地创建

        Fix (Issue 9 - P0): conn_provider 是一个可调用对象（如 lambda），
        每次调用动态返回当前线程的连接。解决 ThreadingMixIn 下所有线程
        共享同一个固定连接的问题。

        优先级：conn_provider > external_conn > thread-local fallback
        """
        if self._conn_provider is not None:
            c = self._conn_provider()
            self._ensure_vec_on_conn(c)
            return c

        if self._external_conn is not None:
            return self._external_conn

        if not hasattr(self._local, 'conn') or self._local.conn is None:
            self._local.conn = sqlite3.connect(self.db_path)
            self._local.conn.row_factory = sqlite3.Row
            self._local.conn.execute("PRAGMA journal_mode=WAL")
            self._local.conn.execute("PRAGMA busy_timeout=30000")
            if _HAS_SQLITE_VEC:
                self._local.conn.enable_load_extension(True)
                sqlite_vec.load(self._local.conn)
            else:
                logger.error("sqlite-vec 未安装: pip install sqlite-vec")
                raise ImportError("sqlite-vec 未安装: pip install sqlite-vec")
        return self._local.conn

    def _ensure_vec_table(self):
        """创建 vec0 虚拟表（幂等，维度不匹配时自动重建）"""
        try:
            conn = self.conn  # 通过 property 获取（支持 provider 模式）
            conn.execute(f"""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_vectors USING vec0(
                    embedding float[{self._dim}],
                    +memory_id TEXT,
                    +importance TEXT,
                    +nature_id TEXT
                )
            """)
            conn.commit()
        except Exception as e:
            logger.warning("embedding_store: %s", e)

        # Fix (Bug 1): 维度不匹配检测（_ensure_vec_table_on_conn 已处理，此处兜底）
        try:
            if not self._check_vec_dim(self.conn):
                logger.warning(f"维度不匹配，重建 vec0 表 (dim={self._dim})")
                self.conn.execute("DROP TABLE IF EXISTS memory_vectors")
                self.conn.execute(f"""
                    CREATE VIRTUAL TABLE memory_vectors USING vec0(
                        embedding float[{self._dim}],
                        +memory_id TEXT,
                        +importance TEXT,
                        +nature_id TEXT
                    )
                """)
                self.conn.commit()
        except Exception as e:
            logger.warning("embedding_store: %s", e)

    # ── 核心读写 ─────────────────────────────────────

    def add(self, memory_id: str, content: str, metadata: dict = None, conn: sqlite3.Connection = None):
        """添加/更新一条记忆的向量

        Fix (Issue 1): 支持传入外部连接，使向量写入与结构化数据在同一事务内完成。
        当 conn 参数传入时，不自行 commit（由调用方管理事务）。

        v12: sqlite-vec 不可用时，回退到 ChromaDB 存储。
        """
        if not self._vec_available and not self._use_chroma:
            return  # 降级：跳过向量存储

        if self._use_chroma:
            self._add_chroma(memory_id, content, metadata)
            return

        embedding = self._normalize(self._encode(content))
        meta = metadata or {}

        c = conn or self.conn
        self._ensure_vec_on_conn(c)
        # 先删除旧向量（幂等 upsert）
        c.execute("DELETE FROM memory_vectors WHERE memory_id = ?", (memory_id,))
        c.execute(
            "INSERT INTO memory_vectors(rowid, embedding, memory_id, importance, nature_id) "
            "VALUES ((SELECT COALESCE(MAX(rowid), 0) + 1 FROM memory_vectors), ?, ?, ?, ?)",
            (
                sqlite_vec.serialize_float32(embedding),
                memory_id,
                meta.get("importance", "medium"),
                meta.get("nature_id", ""),
            ),
        )
        # 仅在使用线程本地 fallback 连接时自行 commit
        # 外部连接/conn_provider 由调用方管理事务
        if conn is None and self._external_conn is None and self._conn_provider is None:
            c.commit()

    def add_batch(self, items: list[dict]):
        """批量添加向量"""
        if not items:
            return
        if not self._vec_available and not self._use_chroma:
            return  # 降级：跳过向量存储

        if self._use_chroma:
            self._add_batch_chroma(items)
            return

        self._ensure_model()

        mids = [it["memory_id"] for it in items]
        self.delete_batch(mids)

        contents = [it["content"] for it in items]
        embeddings = self._encode_batch(contents)

        conn = self.conn
        data = [
            (
                sqlite_vec.serialize_float32(self._normalize(emb)),
                it["memory_id"],
                (it.get("metadata") or {}).get("importance", "medium"),
                (it.get("metadata") or {}).get("nature_id", ""),
            )
            for it, emb in zip(items, embeddings)
        ]
        conn.executemany(
            "INSERT INTO memory_vectors(rowid, embedding, memory_id, importance, nature_id) "
            "VALUES ((SELECT COALESCE(MAX(rowid), 0) + 1 FROM memory_vectors), ?, ?, ?, ?)",
            data,
        )
        conn.commit()

    def search(
        self,
        query: str,
        top_k: int = 10,
        filter_metadata: dict = None,
    ) -> list[dict]:
        """语义搜索（首次调用触发模型懒加载）

        返回: [{"memory_id": str, "score": float, "content": str, "metadata": dict}, ...]

        v12: sqlite-vec 不可用时，回退到 ChromaDB 搜索。
        """
        if not self._vec_available and not self._use_chroma:
            return []  # 降级：无向量搜索能力

        if self._use_chroma:
            return self._search_chroma(query, top_k, filter_metadata)

        self._ensure_model()
        query_embedding = self._normalize(self._encode(query))

        # KNN 查询（vec0 要求 LIMIT 在查询中）
        knn_limit = top_k * 3  # 多取一些用于 post-filter

        if filter_metadata:
            _ALLOWED_FILTER_KEYS = {"memory_id", "importance", "nature_id"}
            where_clauses = []
            params = [sqlite_vec.serialize_float32(query_embedding)]
            for key, val in filter_metadata.items():
                if key not in _ALLOWED_FILTER_KEYS:
                    continue
                where_clauses.append(f"v.{key} = ?")
                params.append(val)
            where_sql = " AND ".join(where_clauses)

            rows = conn_query(self.conn,
                f"SELECT v.rowid, v.memory_id, v.importance, v.nature_id, v.distance "
                f"FROM ("
                f"  SELECT rowid, memory_id, importance, nature_id, distance "
                f"  FROM memory_vectors WHERE embedding MATCH ? ORDER BY distance LIMIT ?"
                f") v WHERE {where_sql} LIMIT ?",
                params + [knn_limit, top_k],
            )
        else:
            rows = conn_query(self.conn,
                "SELECT rowid, memory_id, importance, nature_id, distance "
                "FROM memory_vectors WHERE embedding MATCH ? ORDER BY distance LIMIT ?",
                [sqlite_vec.serialize_float32(query_embedding), top_k],
            )

        output = []
        for r in rows:
            # L2 距离（归一化向量）→ 余弦相似度
            dist = r["distance"]
            score = max(0.0, 1.0 - (dist * dist) / 2.0)
            output.append({
                "memory_id": r["memory_id"],
                "score": round(score, 4),
                "content": "",  # vec0 不存完整内容，由 caller 从 memories 表补充
                "metadata": {
                    "importance": r["importance"],
                    "nature_id": r["nature_id"],
                },
            })

        return output

    def delete(self, memory_id: str, conn: sqlite3.Connection = None):
        """删除一条向量

        Fix (Issue 1/9): 支持传入外部连接实现事务一致性。

        v12: sqlite-vec 不可用时，回退到 ChromaDB 删除。
        """
        if not self._vec_available and not self._use_chroma:
            return  # 降级：无向量表可操作

        if self._use_chroma:
            self._delete_chroma(memory_id)
            return

        c = conn or self.conn
        self._ensure_vec_on_conn(c)
        c.execute("DELETE FROM memory_vectors WHERE memory_id = ?", (memory_id,))
        if conn is None and self._external_conn is None and self._conn_provider is None:
            c.commit()

    def delete_batch(self, memory_ids: list[str], conn: sqlite3.Connection = None):
        """批量删除向量（Fix: 解决 N+1 删除问题）

        Args:
            memory_ids: 要删除的 memory_id 列表
            conn: 可选的外部连接，用于事务一致性

        Note:
            SQLite 默认参数限制为 999，超过时会自动分批处理
        """
        if not memory_ids:
            return
        if not self._vec_available and not self._use_chroma:
            return 0  # 降级：无向量表可操作

        if self._use_chroma:
            self._delete_chroma_batch(memory_ids)
            return

        c = conn or self.conn
        self._ensure_vec_on_conn(c)

        # SQLite 默认参数限制为 999
        SQLITE_MAX_VARIABLES = 999

        total_deleted = 0
        for i in range(0, len(memory_ids), SQLITE_MAX_VARIABLES):
            batch = memory_ids[i:i + SQLITE_MAX_VARIABLES]
            placeholders = ",".join("?" * len(batch))
            cursor = c.execute(
                f"DELETE FROM memory_vectors WHERE memory_id IN ({placeholders})",
                batch
            )
            total_deleted += cursor.rowcount

        if conn is None and self._external_conn is None and self._conn_provider is None:
            c.commit()

        logger.debug(f"delete_batch: 删除 {total_deleted} 条向量")
        return total_deleted

    def count(self) -> int:
        """返回存储的向量数量"""
        if not self._vec_available:
            return 0
        row = self.conn.execute("SELECT count(*) FROM memory_vectors").fetchone()
        return row[0] if row else 0

    def list_all_ids(self, limit: int = 100000) -> list[str]:
        """List all memory IDs in the vector store."""
        if not self._vec_available:
            return []
        rows = self.conn.execute(
            "SELECT memory_id FROM memory_vectors LIMIT ?", (limit,)
        ).fetchall()
        return [r["memory_id"] for r in rows]

    # ── 编码器（复用原逻辑）────────────────────────────

    def _ensure_model(self):
        """懒加载：首次编码时才初始化对应后端

        Fix (Issue 4): 使用 threading.Lock 保护模型加载，
        防止多线程首次并发调用时重复加载模型到内存（~300MB bge-small）。
        """
        if self._model_loaded:
            return

        with self._model_load_lock:
            # Double-check locking: 拿到锁后再检查一次
            if self._model_loaded:
                return
            self._model_loaded = True

            if self._backend == "hash":
                self._use_model = False
                logger.info("Using SimHash embedding (no semantic capability)")
                return

            if self._backend == "local":
                try:
                    from model_server import send_request, is_running
                    if is_running():
                        resp = send_request({"action": "ping"}, timeout=2)
                        if resp.get("ok"):
                            self._use_server = True
                            self._use_model = True
                            logger.info("Using model server (zero-latency embedding)")
                            return
                except Exception as e:
                    logger.warning("embedding_store: %s", e)

            if self._backend in ("openai", "cohere", "voyage"):
                if self._init_api_backend():
                    self._use_model = True
                    return
                logger.warning(f"API backend '{self._backend}' init failed, falling back to local")

            _ensure_hf_endpoint()
            try:
                from sentence_transformers import SentenceTransformer

                # 1. 本地路径模式：直接加载，无需网络
                if _is_local_model_path(self._model_name):
                    self.model = SentenceTransformer(self._model_name, device="cpu")
                    self._use_model = True
                    logger.info(f"Embedding model loaded from local path: {self._model_name}")
                    return

                # 2. 检测网络：如果 HF 不可达且无镜像，直接跳过下载
                hf_endpoint = os.environ.get("HF_ENDPOINT")
                can_reach_hf = True
                if not hf_endpoint:
                    import socket
                    try:
                        socket.create_connection(("huggingface.co", 443), timeout=3).close()
                    except (socket.timeout, OSError):
                        can_reach_hf = False
                        logger.info("HuggingFace unreachable and no mirror configured, skip download")

                # 3. 标准模式：SentenceTransformer 自动从 HF 下载
                if can_reach_hf or hf_endpoint:
                    try:
                        self.model = SentenceTransformer(self._model_name, device="cpu")
                        self._use_model = True
                        logger.info(f"Embedding model '{self._model_name}' loaded (lazy, dim={self._dim})")
                        return
                    except Exception as e1:
                        # 4. 降级：HF_ENDPOINT 不生效时，用 HfApi(endpoint=...) 下载
                        if hf_endpoint:
                            logger.info(f"SentenceTransformer download failed, trying HfApi(endpoint={hf_endpoint})...")
                            local_path = _download_model_via_api(self._model_name, endpoint=hf_endpoint)
                            if local_path:
                                self.model = SentenceTransformer(local_path, device="cpu")
                                self._use_model = True
                                logger.info(f"Embedding model loaded via HfApi mirror: {local_path}")
                                return
                        raise e1

            except Exception as e:
                logger.warning("embedding_store: %s", e)
                logger.info(
                    "Hint: If network is unavailable, download model manually and set "
                    "AGENT_MEMORY_EMBEDDING_MODEL=/path/to/local/model"
                )
                self.model = None
                self._use_model = False

    def _init_api_backend(self) -> bool:
        """初始化 API embedding 后端"""
        try:
            if self._backend == "openai":
                _cred = os.environ.get("OPENAI_API_KEY")
                if not _cred:
                    return False
                self._api_client = {"backend": "openai", "_cred": _cred,
                                    "base_url": os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")}
                return True
            elif self._backend == "cohere":
                _cred = os.environ.get("COHERE_API_KEY")
                if not _cred:
                    return False
                self._api_client = {"backend": "cohere", "_cred": _cred}
                return True
            elif self._backend == "voyage":
                _cred = os.environ.get("VOYAGE_API_KEY")
                if not _cred:
                    return False
                self._api_client = {"backend": "voyage", "_cred": _cred}
                return True
        except Exception as e:
            logger.warning("embedding_store: %s", e)
        return False

    def _encode(self, text: str) -> list[float]:
        """编码文本为向量"""
        self._ensure_model()
        if self._use_server:
            return self._encode_via_server([text])[0]
        elif self._api_client:
            return self._encode_via_api([text])[0]
        elif self._use_model:
            return self.model.encode(text).tolist()
        else:
            return self._hash_embedding(text, dim=self._dim)

    def _encode_batch(self, texts: list[str]) -> list[list[float]]:
        """批量编码"""
        self._ensure_model()
        if self._use_server:
            return self._encode_via_server(texts)
        elif self._api_client:
            return self._encode_via_api(texts)
        elif self._use_model:
            raw = self.model.encode(texts, show_progress_bar=False)
            return [e.tolist() for e in raw]
        else:
            return [self._hash_embedding(t, dim=self._dim) for t in texts]

    def _encode_via_server(self, texts: list[str]) -> list[list[float]]:
        """通过守护进程编码"""
        from model_server import send_request
        resp = send_request({"action": "encode", "texts": texts}, timeout=30)
        if resp.get("ok"):
            return resp["embeddings"]
        logger.warning("Model server unavailable, falling back to hash")
        self._use_server = False
        self._use_model = False
        return [self._hash_embedding(t, dim=self._dim) for t in texts]

    def _encode_via_api(self, texts: list[str]) -> list[list[float]]:
        """通过 API 后端批量编码"""
        import json as _json
        import urllib.request

        backend = self._api_client["backend"]
        _cred = self._api_client["_cred"]

        if backend == "openai":
            url = f"{self._api_client['base_url']}/embeddings"
            _validate_url(url)
            payload = _json.dumps({"model": self._model_name, "input": texts}).encode()
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_cred}",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = _json.loads(resp.read())
            return [item["embedding"] for item in data["data"]]

        elif backend == "cohere":
            url = "https://api.cohere.ai/v1/embed"
            _validate_url(url)
            payload = _json.dumps({"model": self._model_name, "texts": texts, "input_type": "search_document"}).encode()
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_cred}",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = _json.loads(resp.read())
            return data["embeddings"]

        elif backend == "voyage":
            url = "https://api.voyageai.com/v1/embeddings"
            _validate_url(url)
            payload = _json.dumps({"model": self._model_name, "input": texts}).encode()
            req = urllib.request.Request(url, data=payload, headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {_cred}",
            })
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = _json.loads(resp.read())
            return [item["embedding"] for item in data["data"]]

        raise ValueError(f"Unknown API backend: {backend}")

    @staticmethod
    def _normalize(vec: list[float]) -> list[float]:
        """L2 归一化 — 使 L2 距离等价余弦距离排序"""
        norm = math.sqrt(sum(x * x for x in vec))
        if norm < 1e-10:
            return vec
        return [x / norm for x in vec]

    @staticmethod
    def _hash_embedding(text: str, dim: int = 512) -> list[float]:
        """SimHash 伪 embedding（降级模式）"""
        import re
        tokens = re.findall(r'[\w]|[\u4e00-\u9fff]+', text.lower())
        if not tokens:
            tokens = [text]

        votes = [0.0] * dim
        for token in tokens:
            h = hashlib.md5(token.encode("utf-8")).hexdigest()
            bit_str = bin(int(h, 16))[2:].zfill(128)
            for i in range(dim):
                bit = int(bit_str[i % len(bit_str)])
                votes[i] += 1.0 if bit else -1.0

        max_abs = max(abs(v) for v in votes) if votes else 1.0
        if max_abs > 0:
            return [v / max_abs for v in votes]
        return votes

    # ── CLIP 多模态（兼容保留）────────────────────────

    def _ensure_clip(self):
        """懒加载 CLIP 模型"""
        if self._clip_loaded:
            return
        self._clip_loaded = True
        try:
            from transformers import CLIPModel, CLIPProcessor
            import torch
            self._clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
            self._clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
            _set_eval = getattr(self._clip_model, "eval", None)
            if _set_eval and callable(_set_eval):
                _set_eval()
            logger.info("CLIP loaded (lazy)")
        except Exception as e:
            logger.debug(f"CLIP unavailable: {e}")

    def add_image(self, memory_id: str, image_path: str, text_description: str = "", metadata: dict = None):
        """添加图片向量（CLIP embedding，不可用时降级为文本）"""
        meta = metadata or {}
        meta["importance"] = meta.get("importance", "medium")
        meta["nature_id"] = meta.get("nature_id", "")

        embedding = self._encode_image_clip(image_path)
        if embedding is None:
            fallback_text = text_description or f"图片: {os.path.basename(image_path)}"
            embedding = self._encode(fallback_text)

        normalized = self._normalize(embedding)
        conn = self.conn
        conn.execute("DELETE FROM memory_vectors WHERE memory_id = ?", (memory_id,))
        conn.execute(
            "INSERT INTO memory_vectors(rowid, embedding, memory_id, importance, nature_id) "
            "VALUES ((SELECT COALESCE(MAX(rowid), 0) + 1 FROM memory_vectors), ?, ?, ?, ?)",
            (sqlite_vec.serialize_float32(normalized), memory_id, meta["importance"], meta["nature_id"]),
        )
        conn.commit()

    def search_image(self, query_text: str, top_k: int = 5) -> list[dict]:
        """用文字搜索图片（CLIP 跨模态检索，不可用时降级为普通搜索）"""
        return self.search(query_text, top_k=top_k)

    def _encode_image_clip(self, image_path: str) -> list[float] | None:
        """CLIP 图片编码"""
        self._ensure_clip()
        if not self._clip_model:
            return None
        try:
            from PIL import Image
            import torch
            img = Image.open(image_path).convert("RGB")
            inputs = self._clip_processor(images=[img], return_tensors="pt")
            with torch.no_grad():
                features = self._clip_model.get_image_features(**inputs)
                features = features / features.norm(dim=-1, keepdim=True)
            return features.squeeze().tolist()
        except Exception as e:
            logger.debug(f"CLIP encoding failed: {e}")
            return None

    # ── ChromaDB 回退操作 ───────────────────────────────

    def _add_chroma(self, memory_id: str, content: str, metadata: dict = None):
        """ChromaDB: 添加/更新一条向量"""
        if not self._chroma_collection:
            return
        try:
            self._ensure_model()
            embedding = self._encode(content)
            meta = metadata or {}
            # ChromaDB upsert
            self._chroma_collection.upsert(
                ids=[memory_id],
                embeddings=[embedding],
                metadatas=[{
                    "importance": meta.get("importance", "medium"),
                    "nature_id": meta.get("nature_id", ""),
                }],
                documents=[content],
            )
        except Exception as e:
            logger.debug("ChromaDB add failed: %s", e)

    def _add_batch_chroma(self, items: list[dict]):
        """ChromaDB: 批量添加向量"""
        if not self._chroma_collection or not items:
            return
        try:
            self._ensure_model()
            contents = [it["content"] for it in items]
            embeddings = self._encode_batch(contents)
            ids = [it["memory_id"] for it in items]
            metas = [
                {
                    "importance": (it.get("metadata") or {}).get("importance", "medium"),
                    "nature_id": (it.get("metadata") or {}).get("nature_id", ""),
                }
                for it in items
            ]
            self._chroma_collection.upsert(
                ids=ids,
                embeddings=embeddings,
                metadatas=metas,
                documents=contents,
            )
        except Exception as e:
            logger.debug("ChromaDB batch add failed: %s", e)

    def _search_chroma(self, query: str, top_k: int = 10,
                       filter_metadata: dict = None) -> list[dict]:
        """ChromaDB: 语义搜索"""
        if not self._chroma_collection:
            return []
        try:
            self._ensure_model()
            query_embedding = self._encode(query)

            where_filter = None
            if filter_metadata:
                conditions = []
                for k, v in filter_metadata.items():
                    if k in ("importance", "nature_id"):
                        conditions.append({k: v})
                if conditions:
                    where_filter = {"$and": conditions} if len(conditions) > 1 else conditions[0]

            results = self._chroma_collection.query(
                query_embeddings=[query_embedding],
                n_results=min(top_k, self._chroma_collection.count() or 1),
                where=where_filter,
                include=["metadatas", "distances", "documents"],
            )

            output = []
            if results and results["ids"] and results["ids"][0]:
                for i, mid in enumerate(results["ids"][0]):
                    dist = results["distances"][0][i] if results["distances"] else 0.0
                    # ChromaDB cosine distance → similarity
                    score = max(0.0, 1.0 - dist)
                    meta = results["metadatas"][0][i] if results["metadatas"] else {}
                    output.append({
                        "memory_id": mid,
                        "score": round(score, 4),
                        "content": results["documents"][0][i] if results["documents"] else "",
                        "metadata": meta,
                    })
            return output
        except Exception as e:
            logger.debug("ChromaDB search failed: %s", e)
            return []

    def _delete_chroma(self, memory_id: str):
        """ChromaDB: 删除一条向量"""
        if not self._chroma_collection:
            return
        try:
            self._chroma_collection.delete(ids=[memory_id])
        except Exception as e:
            logger.debug("ChromaDB delete failed: %s", e)

    def _delete_chroma_batch(self, memory_ids: list[str]):
        """ChromaDB: 批量删除向量"""
        if not self._chroma_collection:
            return
        try:
            self._chroma_collection.delete(ids=memory_ids)
        except Exception as e:
            logger.debug("ChromaDB batch delete failed: %s", e)

    def close(self):
        """关闭线程本地连接"""
        if hasattr(self._local, 'conn') and self._local.conn:
            try:
                self._local.conn.close()
                self._local.conn = None
            except Exception as e:
                logger.warning("embedding_store: %s", e)


def conn_query(conn: sqlite3.Connection, sql: str, params: list = None) -> list[sqlite3.Row]:
    """执行查询并返回结果列表（统一处理参数绑定）"""
    if params:
        return conn.execute(sql, params).fetchall()
    return conn.execute(sql).fetchall()
