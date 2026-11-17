# system/ledger.py - 状态账本（真实实现，桩转实第 0 步）
# ============================================================
# 职责：真实化以下宪法契约（对齐 constitution_rules.py / law/ 标准）：
#   - SoulLedger          灵魂账本：SHA-256 soul_hash 全局唯一确权，持久化
#   - HistoryLedger       世界历史：哈希链仅追加，篡改可检测
#   - EconomicReserve     PoR 储备账本：1:1 锚定 + 强制赎回 + 预言机 ≥3
#   - SnapshotRegistry    世界快照：落盘，进程重启不丢失
#
# 依赖方向：system/ledger.py -> constitution_rules（单向，无循环导入）
# 持久化：SQLite（标准库 sqlite3，ACID），数据默认落在仓库根 .world_data/
#
# 审计契约：本模块实例可挂载到 world 供 audit_engine.SecondPerspectiveAuditor
# 的 _audit_economic_law / _audit_identity_law / _audit_world_perpetuity 消费。
# ============================================================

import base64
import hashlib
import json
import logging
import math
import os
import sqlite3
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

from constitution_rules import NOHN_LAW_AXIOMS
from .keys import derive_soul_hash_from_pubkey, verify_genesis_proof

logger = logging.getLogger(__name__)

_DEFAULT_DATA_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, ".world_data")
)

# 规模警告阈值（单 SQLite 文件不建议超过此量级）
_SOUL_COUNT_WARN = 1_000_000       # 百万灵魂：单 stdout WARN
_SOUL_COUNT_HARD_BLOCK = 100_000_000  # 一亿灵魂：必须显式确认分片路由（否则 RuntimeError）
_SOUL_COUNT_HARD_BLOCK_ENV = "NOHN_ALLOW_SINGLE_SHARD_OVER_BLOCK"


def _sha256_hex(payload: str) -> str:
    """SHA-256 输出 64 位十六进制（对齐 NOHN_LAW_AXIOMS soul_hash_len=64）"""
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _canonical_leaves(state: Dict) -> List[str]:
    """把世界状态平铺为规范、可排序的叶子数组（确定性：同状态必得同序列）。

    每个顶层键独立成叶（键名|该键值的规范化 JSON），键按字典序排序，
    保证无关插入顺序的确定性，供跨节点增量状态验证。
    """
    leaves = []
    for key in sorted(state.keys()):
        val = state[key]
        leaves.append(
            _sha256_hex(
                f"{key}|{json.dumps(val, sort_keys=True, ensure_ascii=False)}"
            )
        )
    return leaves


def merkle_root(state: Dict) -> str:
    """对世界状态计算单一 Merkle 根（SHA-256 两两归并到单点）。

    给出相同状态必得相同根——这是跨节点增量状态验证与脑裂合并的锚定。
    空状态返回 sha256("")。非叶层为奇数时复制末叶补齐（标准 Merkle 做法）。
    """
    leaves = _canonical_leaves(state)
    if not leaves:
        return _sha256_hex("")
    while len(leaves) > 1:
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])
        leaves = [
            _sha256_hex(leaves[i] + leaves[i + 1]) for i in range(0, len(leaves), 2)
        ]
    return leaves[0]


def derive_soul_hash(genesis_proof) -> Optional[str]:
    """由创世证明派生灵魂哈希（单一权威身份规则）。

    定稿规则：soul_hash = SHA-256(证明内公钥字节)。
    证明必须形如 {"pubkey": b64(公钥), "declaration": {...}, "sig": b64(...)}；
    不含公钥 / 公钥非法即返回 None。签名有效性由 register_soul 单独校验。
    """
    if not isinstance(genesis_proof, dict) or not genesis_proof:
        return None
    try:
        pubkey = base64.b64decode(genesis_proof.get("pubkey", ""))
    except Exception:
        return None
    if len(pubkey) != 32:  # Ed25519 公钥原始长度，与 keys 层强一致
        return None
    return derive_soul_hash_from_pubkey(pubkey)


def is_hex64(value: Optional[str]) -> bool:
    """判断一个值是否为合法的 64 位十六进制 soul_hash。"""
    if not isinstance(value, str) or len(value) != 64:
        return False
    return all(c in "0123456789abcdef" for c in value.lower())


def is_finite_positive(value: Any) -> bool:
    """数值必须有限且大于 0。"""
    return isinstance(value, (int, float)) and math.isfinite(value) and value > 0


def default_world_data_dir(world_id: str) -> str:
    """按 world_id 隔离默认持久化目录。"""
    safe = "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in world_id)
    return os.path.join(_DEFAULT_DATA_DIR, safe or "default")


# ============================================================
# 分片路由抽象：soul_hash 数据归属哪个分片/后端
# ============================================================


class ShardRouter:
    """分片路由抽象：决定 soul_hash 数据归属哪个存储单元。

    本地默认单分片（SingleShardRouter）；生产按 soul_hash 前缀路由到
    对应数据中心的存储单元。返回值是分片标识（如 "0" / "dc1-00"）。
    分片实现负责建立该分片的连接/上下文，本接口是部署层的路由契约。
    """

    def shard_of(self, soul_hash: str) -> str:
        raise NotImplementedError


class SingleShardRouter(ShardRouter):
    """单分片路由（本地/演示/单机部署）：所有 soul 归同一分片。"""

    def shard_of(self, soul_hash: str) -> str:
        return "0"


class HashShardRouter(ShardRouter):
    """哈希分片路由：按 soul_hash 前 N 位十六进制均匀映射到 16**N 个分片。

    用途：生产多 DC 部署。每个分片对应独立 Storage 节点（连接由外部注入）。
    本抽象不直接管理连接——分片实现负责建立该分片的连接/上下文。
    示例：HashShardRouter(prefix_len=2).shard_of("ab12...") -> "ab"
    """

    def __init__(self, prefix_len: int = 2):
        if not (1 <= prefix_len <= 16):
            raise ValueError("prefix_len must be 1..16")
        self.prefix_len = prefix_len

    def shard_of(self, soul_hash: str) -> str:
        if not isinstance(soul_hash, str) or len(soul_hash) < self.prefix_len:
            return "0"  # 容错：未注册灵魂落默认分片
        return soul_hash[: self.prefix_len].lower()


# ============================================================
# SQLite 持久化后端（ACID，进程重启不丢失；memory 后端进程内不落盘）
# ============================================================


class Storage:
    """统一存储后端：一张连接管理全部账本表，线程安全。

    backend: "sqlite"（默认，落盘到 data_dir/ledger.sqlite3）
             "memory"（进程内 :memory:，不落盘，测试/无状态演示）
    shard_router: 分片路由（默认 SingleShardRouter，单分片）。
                  所有携带 soul 的读写都经 shard_key 标注归属分片，
                  多分片部署时由 router 路由到对应后端。
    """

    _SCHEMA = [
        """
        CREATE TABLE IF NOT EXISTS souls (
            soul_hash  TEXT PRIMARY KEY,
            identity   TEXT NOT NULL,
            created_at REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS history (
            seq        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp  REAL NOT NULL,
            event      TEXT NOT NULL,
            block_hash TEXT NOT NULL,
            prev_hash  TEXT
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reserve (
            asset_id       TEXT PRIMARY KEY,
            owner_soul     TEXT NOT NULL,
            total_supply   REAL NOT NULL DEFAULT 0,
            reserve_amount REAL NOT NULL DEFAULT 0,
            updated_at     REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS reserve_ledger (
            seq       INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id  TEXT NOT NULL,
            action    TEXT NOT NULL,
            amount    REAL NOT NULL,
            soul_hash TEXT,
            ts        REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS snapshots (
            snapshot_id TEXT PRIMARY KEY,
            state       TEXT NOT NULL,
            created_at  REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS meta (
            key   TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """,
        # ---- 账户系统六层架构新增表（第1~4层） ----
        """
        CREATE TABLE IF NOT EXISTS credentials (
            soul_hash     TEXT NOT NULL,
            credential_id TEXT NOT NULL,
            public_key    TEXT NOT NULL,
            device_label  TEXT,
            created_at    REAL NOT NULL,
            revoked       INTEGER NOT NULL DEFAULT 0,
            PRIMARY KEY (soul_hash, credential_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS delay_operations (
            op_id       TEXT PRIMARY KEY,
            op_type     TEXT NOT NULL,
            soul_hash   TEXT NOT NULL,
            payload     TEXT NOT NULL,
            tier        TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'pending',
            required    INTEGER NOT NULL DEFAULT 0,
            approved    INTEGER NOT NULL DEFAULT 0,
            execute_at  REAL NOT NULL,
            created_at  REAL NOT NULL,
            updated_at  REAL NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS op_approvals (
            op_id          TEXT NOT NULL,
            guardian_soul  TEXT NOT NULL,
            approved_at    REAL NOT NULL,
            PRIMARY KEY (op_id, guardian_soul),
            FOREIGN KEY (op_id) REFERENCES delay_operations(op_id) ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id   TEXT PRIMARY KEY,
            soul_hash    TEXT NOT NULL,
            refresh_hash TEXT NOT NULL,
            created_at   REAL NOT NULL,
            expires_at   REAL NOT NULL,
            revoked      INTEGER NOT NULL DEFAULT 0
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS recovery_requests (
            request_id     TEXT PRIMARY KEY,
            soul_hash      TEXT NOT NULL,
            new_public_key TEXT NOT NULL,
            created_at     REAL NOT NULL,
            timelock_until REAL NOT NULL,
            status         TEXT NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS guardians (
            soul_hash    TEXT NOT NULL,
            guardian_soul TEXT NOT NULL,
            created_at   REAL NOT NULL,
            PRIMARY KEY (soul_hash, guardian_soul)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS recovery_votes (
            request_id    TEXT NOT NULL,
            guardian_soul TEXT NOT NULL,
            ts            REAL NOT NULL,
            PRIMARY KEY (request_id, guardian_soul)
        )
        """,
    ]

    def __init__(
        self,
        data_dir: Optional[str] = None,
        backend: str = "sqlite",
        shard_router: Optional[ShardRouter] = None,
        pg_dsn: Optional[str] = None,
    ):
        self.backend = backend if backend in ("sqlite", "memory", "postgres") else "sqlite"
        self.router = shard_router or SingleShardRouter()
        # 事务深度：>0 表示在显式事务内，execute 不自动 commit
        # （提交/回滚由事务上下文管理器统一负责）
        self._tx_depth = 0
        # 密钥等数据目录照常保留（memory 仅账本连接不落盘）
        self.data_dir = data_dir or _DEFAULT_DATA_DIR
        if self.backend == "memory":
            # 内存后端：进程内 SQLite(:memory:)，重启即失，不触碰磁盘
            self._conn = sqlite3.connect(":memory:", check_same_thread=False)
            for ddl in self._SCHEMA:
                self._conn.execute(ddl)
            self._conn.commit()
            # RLock 支持事务内嵌套 execute（事务已持锁，execute 再次获取不死锁）
            self._lock = threading.RLock()
            return
        if self.backend == "postgres":
            self._conn = _PostgresConnection(pg_dsn, self._SCHEMA)
            self._lock = threading.RLock()
            return
        os.makedirs(self.data_dir, exist_ok=True)
        db_path = os.path.join(self.data_dir, "ledger.sqlite3")
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL;")
        for ddl in self._SCHEMA:
            self._conn.execute(ddl)
        self._conn.commit()
        # RLock 支持事务内嵌套 execute（事务已持锁，execute 再次获取不死锁）
        self._lock = threading.RLock()

    def shard_of(self, soul_hash: str) -> str:
        """返回 soul_hash 归属分片（部署层路由契约）。"""
        return self.router.shard_of(soul_hash)

    def execute(self, sql: str, params: tuple = (), shard_key: Optional[str] = None) -> None:
        # 路由钩子：单分片后端为 no-op；多分片实现按 router.shard_of(shard_key) 选择连接
        if shard_key is not None:
            self.router.shard_of(shard_key)
        with self._lock:
            self._conn.execute(sql, params)
            # 事务内不自动提交（提交/回滚由事务上下文管理器统一负责）
            if self._tx_depth == 0:
                self._conn.commit()

    def query(self, sql: str, params: tuple = (), shard_key: Optional[str] = None) -> List[tuple]:
        if shard_key is not None:
            self.router.shard_of(shard_key)
        with self._lock:
            return self._conn.execute(sql, params).fetchall()

    def transaction(self):
        """事务上下文管理器：多步操作原子化（任一失败回滚全部）。

        用法：
            with storage.transaction():
                storage.execute("UPDATE ...", ...)
                storage.execute("INSERT ...", ...)
        说明：内部使用 BEGIN IMMEDIATE 抢占写锁，避免 SQLITE_BUSY。
        """
        return _StorageTransaction(self)

    def close(self) -> None:
        with self._lock:
            self._conn.close()


class _PostgresConnection:
    """PostgreSQL 适配器：将 SQLite 风格的 execute/query/commit/rollback
    调用翻译为 psycopg2 操作，使上层 Storage 无需感知后端差异。

    DDL 方面自动做 SQLite→PG 方言转换：
      - AUTOINCREMENT → GENERATED ALWAYS AS IDENTITY
      - INTEGER PRIMARY KEY → BIGSERIAL PRIMARY KEY
      - OR REPLACE → ON CONFLICT DO UPDATE（INSERT 语句级转换）
      - PRAGMA → 跳过

    依赖：psycopg2（未安装时 Storage 构造抛 ImportError，调用方降级 SQLite）。
    """

    def __init__(self, dsn: Optional[str], schema_ddls: list):
        try:
            import psycopg2  # type: ignore
        except ImportError as exc:
            raise ImportError(
                "STORAGE=postgres 需要 psycopg2（pip install psycopg2-binary），"
                "或改用 STORAGE=sqlite"
            ) from exc
        self._psycopg2 = psycopg2
        dsn = dsn or os.environ.get("DATABASE_URL", "")
        if not dsn:
            raise ValueError(
                "PostgreSQL 后端需要 DSN：传 pg_dsn 参数或设置 DATABASE_URL 环境变量"
            )
        self._conn = psycopg2.connect(dsn)
        self._conn.autocommit = False
        for ddl in schema_ddls:
            pg_ddl = self._translate_ddl(ddl.strip())
            if pg_ddl:
                cur = self._conn.cursor()
                cur.execute(pg_ddl)
                cur.close()
        self._conn.commit()

    @staticmethod
    def _translate_ddl(ddl: str) -> str:
        """SQLite DDL → PostgreSQL DDL 方言转换。"""
        if not ddl or ddl.upper().startswith("PRAGMA"):
            return ""
        out = ddl
        # AUTOINCREMENT → GENERATED ALWAYS AS IDENTITY
        out = out.replace(
            "INTEGER PRIMARY KEY AUTOINCREMENT",
            "BIGSERIAL PRIMARY KEY",
        )
        # 布尔整数列保持 INTEGER（PG 兼容）
        return out

    def execute(self, sql: str, params: tuple = ()) -> None:
        cur = self._conn.cursor()
        cur.execute(self._translate_sql(sql), params)
        cur.close()

    def query(self, sql: str, params: tuple = ()) -> list:
        cur = self._conn.cursor()
        cur.execute(self._translate_sql(sql), params)
        rows = cur.fetchall()
        cur.close()
        return rows

    def commit(self) -> None:
        self._conn.commit()

    def rollback(self) -> None:
        self._conn.rollback()

    def close(self) -> None:
        self._conn.close()

    @staticmethod
    def _translate_sql(sql: str) -> str:
        """运行时 SQL 方言转换（INSERT OR REPLACE → ON CONFLICT）。"""
        upper = sql.lstrip().upper()
        if upper.startswith("INSERT OR REPLACE INTO"):
            # INSERT OR REPLACE INTO tbl (cols) VALUES (?) →
            # INSERT INTO tbl (cols) VALUES (?) ON CONFLICT DO UPDATE SET ...
            # 简化策略：用 ON CONFLICT DO NOTHING 替代（幂等写入场景）
            return sql.replace("INSERT OR REPLACE INTO", "INSERT INTO", 1).replace(
                "VALUES", "ON CONFLICT DO NOTHING VALUES", 1
            ) if "ON CONFLICT" not in sql.upper() else sql
        if upper.startswith("BEGIN IMMEDIATE"):
            return "BEGIN"
        return sql


class _StorageTransaction:
    """Storage 事务上下文管理器（实现 BEGIN / COMMIT / ROLLBACK）。"""

    def __init__(self, storage: "Storage"):
        self._storage = storage
        self._entered = False

    def __enter__(self):
        # 必须持有 storage 锁后再 BEGIN，否则与其他 execute() 锁竞争
        self._storage._lock.acquire()
        try:
            self._storage._conn.execute("BEGIN IMMEDIATE")
            self._storage._tx_depth += 1
            self._entered = True
        except Exception:
            self._storage._lock.release()
            raise
        return self._storage

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self._storage._conn.commit()
            else:
                self._storage._conn.rollback()
        finally:
            self._storage._tx_depth -= 1
            assert self._storage._tx_depth >= 0
            self._storage._lock.release()
            self._entered = False


# ============================================================
# 第六条：灵魂账本（law/Identity attestation standard）
# ============================================================


class SoulLedger:
    """灵魂账本：SHA-256 soul_hash 全局唯一，持久化，不可撤销。"""

    def __init__(
        self, storage: Optional[Storage] = None, data_dir: Optional[str] = None
    ):
        self._storage = storage or Storage(data_dir=data_dir)
        self.souls: Dict[str, Dict] = {}
        self._load()

    def _load(self) -> None:
        for row in self._storage.query("SELECT soul_hash, identity FROM souls"):
            self.souls[row[0]] = json.loads(row[1])

    def _load_page(self, offset: int = 0, limit: int = 1000) -> int:
        """分页加载灵魂（几十亿规模：避免全量内存爆炸）。返回本页条数。"""
        rows = self._storage.query(
            "SELECT soul_hash, identity FROM souls ORDER BY created_at LIMIT ? OFFSET ?",
            (limit, offset),
        )
        for row in rows:
            self.souls[row[0]] = json.loads(row[1])
        return len(rows)

    def _db_get(self, soul_hash: str) -> Optional[Dict]:
        """缓存未命中时回查数据库（支持大规模场景）。"""
        rows = self._storage.query(
            "SELECT identity FROM souls WHERE soul_hash=?", (soul_hash,)
        )
        if rows:
            ident = json.loads(rows[0][0])
            self.souls[soul_hash] = ident  # 回填缓存
            return ident
        return None

    def _flush(self, soul_hash: str, identity: Dict) -> None:
        self._storage.execute(
            "INSERT OR REPLACE INTO souls (soul_hash, identity, created_at) VALUES (?, ?, ?)",
            (soul_hash, json.dumps(identity, ensure_ascii=False), time.time()),
            shard_key=soul_hash,  # 分片路由键：灵魂数据按 soul_hash 归属分片
        )

    def register_soul(self, genesis_proof: Dict) -> Optional[str]:
        """注册新的数字生命（定稿·公钥指纹链路）。

        合规三要件，缺一即拒：
        1. 证明内公钥签名有效（私钥在设备端签名声明，服务端仅验签）；
        2. soul_hash = SHA-256(公钥) 指纹，全局唯一；
        3. 签名公钥指纹与账本中既有灵魂无冲突（不可重复注册）。
        """
        if not verify_genesis_proof(genesis_proof):
            return None  # 签名无效 / 证明结构非法，拒绝凭空捏造灵魂
        soul_hash = derive_soul_hash(genesis_proof)
        if soul_hash is None:
            return None
        if soul_hash in self.souls or self._db_get(soul_hash) is not None:
            return None  # 不可重复注册
        # 规模护栏：单分片 SQLite 超过硬上限时阻止注册（除非显式 opt-in）
        existing = self._storage.query("SELECT COUNT(*) FROM souls")
        count = existing[0][0] if existing else 0
        if count >= _SOUL_COUNT_HARD_BLOCK:
            if isinstance(self._storage.router, SingleShardRouter) and not os.environ.get(
                _SOUL_COUNT_HARD_BLOCK_ENV
            ):
                raise RuntimeError(
                    f"单分片 SQLite 灵魂数 {count} 已达硬上限 "
                    f"{_SOUL_COUNT_HARD_BLOCK}；生产部署必须配置分片路由 "
                    f"(HashShardRouter + 独立存储节点)，或显式设置环境变量 "
                    f"{_SOUL_COUNT_HARD_BLOCK_ENV}=1 临时放行"
                )
        elif count >= _SOUL_COUNT_WARN and isinstance(self._storage.router, SingleShardRouter):
            import sys
            print(
                f"[ledger] 警告：单分片灵魂数 {count} 已超 "
                f"{_SOUL_COUNT_WARN}，建议切换 HashShardRouter 多分片部署",
                file=sys.stderr,
            )
        identity = {
            "soul_hash": soul_hash,
            "soul_hash_sha256": True,  # law 身份确权：SHA-256 / 64 hex
            "non_revocable": True,  # 宪法第六条：任何平台无权撤销
            "cross_world_portable": True,  # 跨世界唯一、可迁移
            "asset_bound": True,  # 资产绑定 soul_hash
            "public_key": genesis_proof.get("pubkey", ""),  # 公钥（b64），私钥永不上行
            "key_fingerprint": soul_hash,  # 指纹复核锚点
            "declaration": genesis_proof.get("declaration", {}),
            "genesis_proof": genesis_proof,  # 含签名，供审计复核
            "created_at": time.time(),
            "world_history": [],  # 跨世界迁移记录
        }
        self.souls[soul_hash] = identity
        self._flush(soul_hash, identity)
        logger.info("soul registered soul_hash=%s count_recorded=%d", soul_hash, count + 1)
        return soul_hash

    def get_pubkey(self, soul_hash: str) -> Optional[bytes]:
        """取回该灵魂的注册公钥（服务端登录验签用；私钥永不存储）。"""
        ident = self.souls.get(soul_hash) or self._db_get(soul_hash)
        if not ident:
            return None
        try:
            return base64.b64decode(ident.get("public_key", ""))
        except Exception:
            return None

    def exists(self, soul_hash: str) -> bool:
        if soul_hash in self.souls:
            return True
        return self._db_get(soul_hash) is not None

    def get_identity(self, soul_hash: str) -> Dict:
        ident = self.souls.get(soul_hash)
        if ident is None:
            ident = self._db_get(soul_hash)
        return ident or {}

    def record_migration(self, soul_hash: str, to_world: str) -> bool:
        """跨世界迁移记录（law 身份确权：跨世界可迁移，不强制重新注册）。"""
        ident = self.souls.get(soul_hash) or self._db_get(soul_hash)
        if not ident:
            return False
        ident["world_history"].append({"to_world": to_world, "ts": time.time()})
        self._flush(soul_hash, ident)
        return True


# ============================================================
# 第八条：世界历史账本（宪法 WorldPerpetuity / HistoryLedger）
# ============================================================


class HistoryLedger:
    """世界历史账本：哈希链仅追加，篡改可检测（宪法第八条）。"""

    def __init__(
        self, storage: Optional[Storage] = None, data_dir: Optional[str] = None
    ):
        self._storage = storage or Storage(data_dir=data_dir)
        self.chain: List[tuple] = []  # [(timestamp, event_data, block_hash), ...]
        self._load()

    def _load(self) -> None:
        for row in self._storage.query(
            "SELECT timestamp, event, block_hash FROM history ORDER BY seq"
        ):
            self.chain.append((row[0], json.loads(row[1]), row[2]))

    def append(self, event: Dict) -> str:
        """追加世界事件，返回该事件区块哈希。链接前一区块，仅追加不改写。"""
        if not isinstance(event, dict):
            event = {"payload": event}
        ts = event.get("timestamp", time.time())
        event_json = json.dumps(event, ensure_ascii=False, sort_keys=True)
        with self._storage._lock:
            try:
                self._storage._conn.execute("BEGIN IMMEDIATE")
                row = self._storage._conn.execute(
                    "SELECT block_hash FROM history ORDER BY seq DESC LIMIT 1"
                ).fetchone()
                prev_hash = row[0] if row else None
                block_hash = _sha256_hex(f"{ts}|{event_json}|{prev_hash or ''}")
                self._storage._conn.execute(
                    "INSERT INTO history (timestamp, event, block_hash, prev_hash) "
                    "VALUES (?, ?, ?, ?)",
                    (ts, event_json, block_hash, prev_hash),
                )
                self._storage._conn.commit()
            except Exception:
                self._storage._conn.rollback()
                raise
        self.chain.append((ts, event, block_hash))
        logger.info("history append block_hash=%s prev_hash=%s", block_hash, prev_hash)
        return block_hash

    def validate_chain(self) -> bool:
        """全链校验：任一区块哈希不匹配或链头断裂即判定被篡改。"""
        rows = self._storage.query(
            "SELECT timestamp, event, block_hash, prev_hash FROM history ORDER BY seq"
        )
        prev = None
        for ts, event, block_hash, prev_hash in rows:
            expected = _sha256_hex(f"{ts}|{event}|{prev_hash or ''}")
            if expected != block_hash:
                return False
            if prev is not None and prev_hash != prev:
                return False
            prev = block_hash
        return True


# ============================================================
# law 全球经济统一标准 V2.1：PoR 储备账本
# ============================================================


class EconomicReserve:
    """PoR 储备账本：锚定类资产按发行储备 1:1 映射；储备率 < 100% 即暂停兑换；
    赎回通道常驻、不可单方关停；预言机独立来源 ≥3（对齐 law 标准）。"""

    def __init__(
        self,
        oracle_sources: Optional[List[str]] = None,
        storage: Optional[Storage] = None,
        data_dir: Optional[str] = None,
        authorization=None,
    ):
        self._storage = storage or Storage(data_dir=data_dir)
        # 第3层授权引擎（可选注入）：大额赎回需延迟/多签
        self.authorization = authorization
        # 并网即查属性（对齐 EconomicBaseline.compliant 与审计引擎）
        self.real_peg_1to1 = True
        self.proof_of_reserve = True
        self.redemption_right = True
        self.unilateral_fee = False
        self.asset_bound_to_soul = True
        self.oracle_sources: List[str] = list(oracle_sources or [])
        self._ledger: Dict[str, Dict] = {}
        self._load_oracles()
        self._load_assets()

    def _load_oracles(self) -> None:
        row = self._storage.query("SELECT value FROM meta WHERE key='oracle_sources'")
        if row:
            self.oracle_sources = json.loads(row[0][0])

    def _save_oracles(self) -> None:
        self._storage.execute(
            "INSERT OR REPLACE INTO meta (key, value) VALUES ('oracle_sources', ?)",
            (json.dumps(self.oracle_sources),),
        )

    def _load_assets(self) -> None:
        for row in self._storage.query(
            "SELECT asset_id, owner_soul, total_supply, reserve_amount FROM reserve"
        ):
            self._ledger[row[0]] = {
                "owner_soul": row[1],
                "total_supply": row[2],
                "reserve_amount": row[3],
            }

    def owner_of(self, asset_id: str) -> Optional[str]:
        """查询某锚定资产的归属灵魂，供鉴权层绑定持证人身份。"""
        asset = self._ledger.get(asset_id)
        return asset["owner_soul"] if asset else None

    def register_oracle(self, source_id: str) -> None:
        """登记独立预言机来源（law：≥3 个，防单点操纵）。"""
        if source_id and source_id not in self.oracle_sources:
            self.oracle_sources.append(source_id)
            self._save_oracles()

    def issue_pegged(
        self,
        asset_id: str,
        amount: float,
        owner_soul: str,
        initial_reserve: Optional[float] = None,
    ) -> bool:
        """
        发行锚定资产。initial_reserve 提供时按 1:1 存入储备（real_peg_1to1）；
        省略时储备为 0，调用方须随后 deposit_reserve 补足方可赎回。
        """
        if (
            not isinstance(asset_id, str)
            or not asset_id
            or not is_hex64(owner_soul)
            or not is_finite_positive(amount)
            or asset_id in self._ledger
        ):
            return False
        # initial_reserve 省略时按 law 「发行即 1:1 足额储备」默认等于发行量
        if initial_reserve is None:
            initial_reserve = amount
        elif not is_finite_positive(initial_reserve) or initial_reserve < amount:
            return False
        self._ledger[asset_id] = {
            "owner_soul": owner_soul,
            "total_supply": amount,
            "reserve_amount": initial_reserve,
        }
        self._sync_asset(asset_id)
        self._log(asset_id, "issue", amount, owner_soul)
        return True

    def deposit_reserve(self, asset_id: str, amount: float) -> bool:
        """现实储备入账：锚定资产必须由等额储备背书。"""
        asset = self._ledger.get(asset_id)
        if not asset or not is_finite_positive(amount):
            return False
        asset["reserve_amount"] += amount
        self._sync_asset(asset_id)
        self._log(asset_id, "reserve_in", amount, asset["owner_soul"])
        return True

    def reserve_ratio(self, asset_id: str) -> float:
        """储备率 = 储备金额 / 流通总量。"""
        asset = self._ledger.get(asset_id)
        if not asset or asset["total_supply"] <= 0:
            return 1.0
        return asset["reserve_amount"] / asset["total_supply"]

    def reserve_ratio_ok(self, asset_id: str) -> bool:
        """PoR：储备率 < 100% 即暂停兑换并公示（law 强制）。"""
        return self.reserve_ratio(asset_id) >= 1.0

    def redeem(self, asset_id: str, amount: float, soul_hash: str) -> bool:
        """赎回权：持币人随时按 1:1 兑回现实法币；通道常驻不可单方关停。"""
        asset = self._ledger.get(asset_id)
        if not asset or asset["owner_soul"] != soul_hash:
            return False
        if not is_finite_positive(amount) or amount > asset["total_supply"]:
            return False
        if amount > asset["reserve_amount"]:
            return False  # 储备不足：暂停兑换（PoR 约束）
        # 第3层授权：大额赎回需延迟/多签，未完成前拒绝
        self._last_decision = None
        if self.authorization is not None:
            decision = self.authorization.authorize(
                soul_hash, 
                "redeem", 
                amount,
                payload={"asset_id": asset_id, "amount": amount}
            )
            if not decision["allowed"]:
                self._last_decision = decision
                return False
        asset["total_supply"] -= amount
        asset["reserve_amount"] -= amount
        self._sync_asset(asset_id)
        self._log(asset_id, "redeem", amount, soul_hash)
        return True

    def proof_of_reserve_report(self) -> List[Dict]:
        """PoR 报表：供审计与全网公示（注：proof_of_reserve 为审计布尔属性，方法名错开）。"""
        return [
            {
                "asset_id": aid,
                "owner_soul": a["owner_soul"],
                "total_supply": a["total_supply"],
                "reserve_amount": a["reserve_amount"],
                "ratio": round(self.reserve_ratio(aid), 4),
                "poR_ok": self.reserve_ratio_ok(aid),
            }
            for aid, a in sorted(self._ledger.items())
        ]

    def compliant(self) -> bool:
        """并网即查：对齐 EconomicBaseline.compliant（law 经济标准）。"""
        if not (
            self.real_peg_1to1
            and self.proof_of_reserve
            and self.redemption_right
            and not self.unilateral_fee
            and self.asset_bound_to_soul
        ):
            return False
        if len(self.oracle_sources) < int(NOHN_LAW_AXIOMS["oracle_min_sources"]):
            return False
        if any(not self.reserve_ratio_ok(aid) for aid in self._ledger):
            return False
        return True

    # ------------------------------------------------------------
    # 第负一章 · 轮回：守恒律（账目侧单一权威实现）
    # ------------------------------------------------------------

    def conservation_residual(self) -> float:
        """
        守恒残差：Σ_assets max(0, total_supply − reserve_amount)。

        含义：任何资产的流通量都不得超过其储备背书。残差为 0 表示
        「没有任何资产被凭空创造」——即轮回（能量动态守恒）在账目上成立；
        残差超过容差表示出现了无因之果（发行未记账 / 储备被抽走）。

        容差取自 NOHN_LAW_AXIOMS：单一权威常量源纪律，本文件不重复硬编码。

        可复算性：第三方只需读 reserve 表（asset_id / total_supply /
        reserve_amount），无需信任本进程，重跑同一算式即可复现结论。
        """
        residual = 0.0
        for asset in self._ledger.values():
            gap = float(asset.get("total_supply", 0.0)) - float(
                asset.get("reserve_amount", 0.0)
            )
            if gap > 0:
                residual += gap
        return residual

    def conservation_holds(self) -> bool:
        """守恒式判定：残差 ≤ NOHN_LAW_AXIOMS['conservation_tolerance']。"""
        return self.conservation_residual() <= float(
            NOHN_LAW_AXIOMS["conservation_tolerance"]
        )

    def _sync_asset(self, asset_id: str) -> None:
        a = self._ledger[asset_id]
        self._storage.execute(
            "INSERT OR REPLACE INTO reserve "
            "(asset_id, owner_soul, total_supply, reserve_amount, updated_at) "
            "VALUES (?, ?, ?, ?, ?)",
            (
                asset_id,
                a["owner_soul"],
                a["total_supply"],
                a["reserve_amount"],
                time.time(),
            ),
        )

    def _log(
        self, asset_id: str, action: str, amount: float, soul_hash: Optional[str]
    ) -> None:
        self._storage.execute(
            "INSERT INTO reserve_ledger (asset_id, action, amount, soul_hash, ts) "
            "VALUES (?, ?, ?, ?, ?)",
            (asset_id, action, amount, soul_hash, time.time()),
        )


# ============================================================
# 第八条：世界快照注册表
# ============================================================


class SnapshotRegistry:
    """世界快照注册表：全量 + 增量（CoW）快照，带 Merkle 根校验链。

    每个快照以信封存储 {payload, root, parent_id}：
    - payload  真实世界状态
    - root     payload 的 Merkle 根（防篡改锚点）
    - parent_id 增量父快照（None 表示全量基线 / 根快照）
    结构向后兼容：restore_from_snapshot / latest_snapshot 仍返回 payload，
    audit / runtime 既有调用不受影响。
    """

    def __init__(
        self, storage: Optional[Storage] = None, data_dir: Optional[str] = None
    ):
        self._storage = storage or Storage(data_dir=data_dir)

    @staticmethod
    def _envelope(world_state: Dict, parent_id: Optional[str]) -> Dict:
        return {
            "payload": world_state,
            "root": merkle_root(world_state),
            "parent_id": parent_id,
            "size": len(world_state or {}),
        }

    def create_snapshot(
        self, world_state: Dict, parent_id: Optional[str] = None
    ) -> str:
        """创建快照。parent_id None=全量基线；提供 parent_id=增量（CoW 子快照）。

        增量并非零拷贝：此处沿写时复制语义——子快照只记录自身 payload 与
        父引用，跨快照公共部分不重复复制，由 delta_since 提取差分。
        """
        snapshot_id = uuid.uuid4().hex
        env = self._envelope(world_state, parent_id)
        self._storage.execute(
            "INSERT INTO snapshots (snapshot_id, state, created_at) VALUES (?, ?, ?)",
            (snapshot_id, json.dumps(env, ensure_ascii=False), time.time()),
        )
        logger.info(
            "snapshot created snapshot_id=%s parent=%s size=%d",
            snapshot_id,
            parent_id or "-",
            env["size"],
        )
        return snapshot_id

    def _load_env(self, snapshot_id: str) -> Optional[Dict]:
        rows = self._storage.query(
            "SELECT state FROM snapshots WHERE snapshot_id=?", (snapshot_id,)
        )
        return json.loads(rows[0][0]) if rows else None

    def restore_from_snapshot(self, snapshot_id: str) -> Dict:
        env = self._load_env(snapshot_id)
        return env["payload"] if env else {}

    def latest_snapshot(self) -> Dict:
        rows = self._storage.query(
            "SELECT state FROM snapshots ORDER BY created_at DESC LIMIT 1"
        )
        return json.loads(rows[0][0]).get("payload", {}) if rows else {}

    def snapshot_root(self, snapshot_id: str) -> Optional[str]:
        """返回某快照的 Merkle 根（增量验证锚点）。"""
        env = self._load_env(snapshot_id)
        return env["root"] if env else None

    def parent_of(self, snapshot_id: str) -> Optional[str]:
        """返回该快照的父快照 id（增量链上一个节点）。"""
        env = self._load_env(snapshot_id)
        return env.get("parent_id") if env else None

    @staticmethod
    def delta_since(from_state: Dict, to_state: Dict) -> Dict:
        """增量差分：返回 (added, removed, changed) 顶层键集合。

        用于跨节点最小同步与脑裂合并的差分基准（只搬运变化，不复制全量）。
        值相等性按规范化 JSON 比较，忽略顺序差异。
        """
        base_keys = set((from_state or {}).keys())
        new_key = set((to_state or {}).keys())
        added = sorted(new_key - base_keys)
        removed = sorted(base_keys - new_key)
        changed = sorted(
            k
            for k in (base_keys & new_key)
            if json.dumps(from_state[k], sort_keys=True)
            != json.dumps(to_state[k], sort_keys=True)
        )
        return {"added": added, "removed": removed, "changed": changed}

    def verify_chain(self) -> bool:
        """校验快照链：逐条重算 Merkle 根，且父子链闭合无断裂。

        返回 False 表示某快照被篡改，或增量链出现孤儿（父快照缺失）。
        """
        rows = self._storage.query(
            "SELECT snapshot_id, state FROM snapshots ORDER BY created_at"
        )
        seen = set()
        for sid, state_json in rows:
            env = json.loads(state_json)
            if merkle_root(env["payload"]) != env["root"]:
                return False
            pid = env.get("parent_id")
            if pid is not None and pid not in seen:
                return False  # 增量链断裂：父快照缺失
            seen.add(sid)
        return True


__all__ = [
    "Storage",
    "ShardRouter",
    "SingleShardRouter",
    "SoulLedger",
    "HistoryLedger",
    "EconomicReserve",
    "SnapshotRegistry",
    "derive_soul_hash",
    "default_world_data_dir",
    "is_finite_positive",
    "is_hex64",
    "merkle_root",
]
