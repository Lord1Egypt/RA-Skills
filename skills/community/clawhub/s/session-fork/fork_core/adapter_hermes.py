# role: adapter:hermes — 产品适配器（SQLite 后端），不含引擎逻辑
"""fork_core.adapter_hermes — Hermes Agent 的 SQLite 后端（纯 SQL，不 import 产品包）。

一手依据（2026-09-14 真机取证 + 手工验收实验，可复跑核对）：
  - 2026-09-14 真机取证记录（含全部命令与原始输出，可复跑核对）
  - 决定本文件写法的**关键实验**：用纯 `sqlite3` 脚本手写分支，
    产品**完整接受**（`sessions list` 列出 + `chat --resume` 续跑并答对被复制的前缀），
    **无需任何"产品盖章"动作** —— 这与 OpenClaw 相反（OpenClaw 必须跑 `doctor --fix`
    让产品把 `entry_valid` 置 1）。故本适配器**不 import 产品代码**、**不要求用户跑修复命令**。

## v0.21.6（schema 31）兼容 —— 2026-10-09 实测新增

上游把 `schema_version` 从 **30 升到 31**，并新增列：`sessions` 58→**62**（`created_source` /
`compression_overload_streak` / `transport_profile` / `auto_archived`）、
`messages` 26→**30**（`message_uid` / `absorbed_message_uids` / `tool_call_uids` / `tool_call_uid`）；
索引：`sessions`+`messages` 两表合计 19→21（新增非唯一的 `idx_messages_session_uid … WHERE active = 1`、
`idx_sessions_tool_names`）；**全库口径** 24→26。
触发器：**全库 10→11**，v31 新增 `messages_message_uid_insert`（**是一个 AFTER INSERT 触发器**）。
FTS：`state_meta.fts_storage_version` 实测 **2 → 3**（`FTS_STORAGE_VERSION = 3`）。

> ⚠️ 口径说明（避免误读）：**触发器按全库统计**、**索引按 `sessions`+`messages` 两表统计** ——
> 两个口径的数字不同（全库索引 24→26），写在一起容易被当成同一个范围。

**验证方式（不是只看 diff）**：把 2026-09-14 的真库复制一份，
用 v0.21.6 自己的 `hermes_state.SessionDB` 打开（产品自行跑 30→31 迁移，25 张表、数据完整），
然后跑本适配器：放行白名单后**写入成功**；再用产品代码读回 —— `list_sessions_rich(include_children=True)`
**列出该分支**且 `parent_session_id` 指向源会话、消息内容与 `message_uid` 原样复制；
SQLite 官方 `FTS5 integrity-check` 通过，`messages_fts` 行数 = `messages` 行数（含分支新行）。

**为什么列数变了却不改写入逻辑**：本适配器用 `SELECT * … LIMIT 0` 取**实际列名**再拼
`INSERT INTO {table} ({cols}) VALUES (…)` ⇒ 新增列随行原样复制，不受列数变化影响。
（这条"动态取列"是刻意设计，改动它之前请先想清楚新增列的回填语义。）

## 介质契约

`$HERMES_HOME/state.db`（`journal_mode=wal`，`SCHEMA_VERSION` **30 或 31**）。一个会话横跨**两张表**：

| 表 | 列数（v30 → v31） | 作用 | 分支侧要写什么 |
|---|---|---|---|
| `sessions` | 58 → **62** | 会话元数据（`id` 主键、`model_config`、`parent_session_id`…） | 复制源行 + 覆写身份/血缘/时间/标题 |
| `messages` | 26 → **30** | 消息本体（`id` 自增主键、`session_id` 外键、`role`、`content`…） | 复制前缀，**排除自增 `id`**；其余列**按实际列名**复制 |

**与其它产品的三处关键差异**（全部实测确定）：

1. **血缘＝两列配合，缺一不可**：`sessions.parent_session_id`（外键 + `idx_sessions_parent`）
   **加上** `model_config._branched_from`。实测**只写前者、不写标记** ⇒ 会话**写进去了但
   `sessions list` 里看不见**（产品的 `_BRANCH_CHILD_SQL` 有一条时间戳兜底判据，
   注释自承"子体先创建"之后即失效）。⇒ **标记是必需项，不是可选装饰。**
2. **`title` 是全库唯一**（`CREATE UNIQUE INDEX idx_sessions_title_unique … WHERE title IS NOT NULL`）
   ⇒ 复制式 fork 撞名会**硬报** `IntegrityError`。本适配器在事务内做唯一化。
3. **FTS 不需要我们动**：`messages_fts*` 是 external-content + 触发器维护，
   插入消息时**自动补行**（实测：手写分支后 `fts base rows` 正确增长）。本适配器**不碰 FTS**。

## 行流（lines）的定义：**只有 messages，不含 header**

引擎的"行"＝可截断的有序条目。本产品把会话元数据与消息**分居两表**，故：

- `read_lines(ref)` → `messages` 行（`ORDER BY id`，即插入序＝对话序），每行一个 dict；
- **`sessions` 行不进行流** —— 它由 `finalize_branch` 从源行**复制 + 覆写**生成
  （与 OpenClaw 把 `session_windows` 单独复制的做法同构）。
  好处：行流里只有消息，`cut` 天然等于"复制多少条消息"，且**不需要任何残留豁免**
  （实测：`messages` 除 `session_id` 列外**没有任何列**含本会话 id ⇒ 改写 `session_id` 后零残留）。

## 已知边界（如实记录）

- 依赖**未公开的内部表结构**（已知 `SCHEMA_VERSION` = **30 / 31**）。故设**版本闸**：
  版本**不在白名单**（含比我们更新的版本、以及读不到版本）时 **拒绝写入**并提示升级适配器，
  而不是静默写坏库（产品无 schema 兼容承诺）。
  ⚠️ 代价要说清：白名单只是把"产品再升一版就整体停摆"推后，**下一次产品升版仍会停摆**——
  这是刻意取舍（宁可停摆也不写坏库）；根治要靠"未知高版本 ⇒ 只读/降级提示"这类策略。
- `title` 唯一化是**尽力而为**：事务内查重 + 冲突时退化为带随机尾缀；仍冲突则整体回滚，
  由引擎的注册失败路径处理。
- `--request-id` 语义映射到 `messages.platform_message_id`（本产品无 conversationRequestId）；
  该列为空时返回 None（此时请用 `--session`）。
- 斜杠命令也会被产品存成 `role='user'` 的消息（实测 `/branch fork-probe` 即一条 user 行）
  ⇒ 它会参与 "最后一条 user 消息" 的标题摘要，属**外观层面**的小噪音，不影响截断正确性。
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid

from .adapter_base import TranscriptionAdapter, dumps_safe
from .models import SessionMeta, VerifyItem

#: 本适配器**认得（可安全写入）**的 schema 版本白名单 —— 实测口径：
#:   · **30** = Hermes v0.21.2（2026-09-14 真机，原声明值）
#:   · **31** = Hermes **v0.21.6**（2026-10-09 实测：产品自己的 `SessionDB` 把 v30 真库
#:     迁移到 v31；白名单放开后写入成功，且产品代码 `list_sessions_rich(include_children=True)`
#:     能列出该分支、`parent_session_id` 指向源会话、消息内容与 `message_uid` 均原样复制、
#:     SQLite 官方 `FTS5 integrity-check` 通过、`messages_fts` 行数与 `messages` 一致）
#: 白名单**之外**（含更高版本、以及读不到版本）一律拒绝写 —— 版本闸宁可停摆，也不写坏用户的库。
#: ⚠️ 历史教训：此前是"等于单一值"的等值闸，产品升一个版本就整体停摆（v0.21.6 即如此）。
KNOWN_SCHEMA_VERSIONS: tuple[int, ...] = (30, 31)

#: 展示用（最新已知版本）；判定一律走上面的白名单。
KNOWN_SCHEMA_VERSION = KNOWN_SCHEMA_VERSIONS[-1]

DB_NAME = "state.db"
REF_SEP = "#"  # "<db 绝对路径>#<session_id>"
LINEAGE_NAME = "fork.lineage.json"

#: `model_config` 里指向源会话的标记键 —— 产品的分支可见性开关。
MARKER_KEY = "_branched_from"


def make_ref(db_path: str, session_id: str) -> str:
    return f"{db_path}{REF_SEP}{session_id}"


def parse_ref(ref: str) -> tuple[str, str]:
    db, _, sid = ref.rpartition(REF_SEP)
    if not db:
        raise ValueError(f"非法 Hermes 转录引用（应形如 <db>#<session_id>）：{ref!r}")
    return db, sid


def _json_default(o):
    """把 SQLite 取出的非 JSON 原生类型转成可序列化形式（**仅用于校验文本**）。"""
    if isinstance(o, (bytes, bytearray, memoryview)):
        return bytes(o).hex()
    return str(o)


class HermesAdapter(TranscriptionAdapter):
    """Hermes Agent（Nous Research）后端：纯 SQL 读写 `state.db`。"""

    name = "hermes"

    #: 允许保留源 id 的键。**本适配器为空** —— 行流里只有 `messages` 行，
    #: 而 `messages` 除 `session_id` 外没有任何列含会话 id（实测），
    #: `session_id` 一律改写成新 id。血缘指针（`parent_session_id` /
    #: `model_config._branched_from`）与源 id 同值，但它们**在 header 行里**，
    #: 而 header 不进行流 ⇒ 引擎的残留检查根本扫不到它们。
    _RAW_KEYS: set = frozenset()

    def __init__(self):
        # ⚠️ 必须在 __init__ 时读环境变量：HERMES_HOME 可能在本模块导入后才设置
        # （与 adapter_codex 同一条教训 —— 隔离根靠环境变量，产品无 --home 参数）。
        self.HERMES_HOME = os.environ.get("HERMES_HOME") or os.path.join(
            os.path.expanduser("~"), ".hermes")
        self.DB_PATH = os.path.join(self.HERMES_HOME, DB_NAME)
        self.LINEAGE_PATH = os.path.join(self.HERMES_HOME, LINEAGE_NAME)
        # write_branch → finalize 之间的暂存（key = 产物 ref）。
        # 与 JSONL 后端写 .tmp 同义：校验期内容**对外不可见**，但校验器读得到。
        self._pending: dict[str, list[dict]] = {}
        # 产物 ref → 源 ref（branch_target 记下，finalize 靠它复制源 header）
        self._src_of_dst: dict[str, str] = {}

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------
    def _connect(self, readonly: bool = False) -> sqlite3.Connection:
        if readonly:
            con = sqlite3.connect(f"file:{self.DB_PATH}?mode=ro", uri=True)
        else:
            con = sqlite3.connect(self.DB_PATH)
            # 与产品一致：写连接启用外键（hermes_state.py 在连接上执行此 PRAGMA）
            con.execute("PRAGMA foreign_keys=ON")
        con.row_factory = sqlite3.Row
        return con

    @staticmethod
    def _cols(cur, table: str) -> list[str]:
        return [d[0] for d in cur.execute(f"SELECT * FROM {table} LIMIT 0").description]

    def _schema_version(self, con: sqlite3.Connection) -> int | None:
        try:
            row = con.execute("SELECT version FROM schema_version LIMIT 1").fetchone()
            return int(row[0]) if row and row[0] is not None else None
        except Exception:
            return None

    def _gate(self, con: sqlite3.Connection) -> None:
        """版本闸：版本不明、或不在白名单 ⇒ 拒绝写（不静默写坏用户的库）。"""
        v = self._schema_version(con)
        known = "、".join(str(x) for x in KNOWN_SCHEMA_VERSIONS)
        if v is None:
            raise RuntimeError(
                f"Hermes schema_version 读不到（{self.DB_PATH}）；"
                f"拒绝写入。请确认这是 Hermes 的 state.db，或升级本适配器。")
        if v not in KNOWN_SCHEMA_VERSIONS:
            raise RuntimeError(
                f"Hermes schema_version = {v}，本适配器认得的是 {known}；"
                f"拒绝写入以免破坏你的会话库。请升级 session-fork 的 Hermes 适配器。")

    def _assert_writable_schema(self) -> None:
        """**fail-fast 版**闸门：在写路径的第一个调用点（`branch_target`）就跑。

        为什么必须前移（2026-09-15 实测教训）：只在 `finalize_branch` 里拦的话，
        引擎此时已经**做完备份、写过 tmp、跑完 verify**，才在最后一刻拒绝 ——
        用户白等一轮，还多出一份无用的备份目录。
        而 `branch_target` 在 `backup_transcript` / `write_branch` **之前**被调用，
        且只出现在写路径上 ⇒ 放这里既 fail-fast，又让 **`--dry-run` 同样被拦**
        （dry-run 的承诺是"预告真实行为"，真实行为会拒绝，dry-run 就不该假装能过）。
        """
        if not os.path.exists(self.DB_PATH):
            raise RuntimeError(f"Hermes 会话库不存在：{self.DB_PATH}")
        con = self._connect(readonly=True)
        try:
            self._gate(con)
        finally:
            con.close()

    def is_available(self) -> bool:
        if not os.path.exists(self.DB_PATH):
            return False
        try:
            con = self._connect(readonly=True)
            try:
                n = con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
            finally:
                con.close()
            return n > 0
        except Exception:
            return False

    # ------------------------------------------------------------------
    # A. 定位
    # ------------------------------------------------------------------
    def _sessions(self) -> list[tuple[str, str, float]]:
        """[(ref, session_id, 活动时间)]，按活动时间倒序。"""
        if not os.path.exists(self.DB_PATH):
            return []
        con = self._connect(readonly=True)
        try:
            rows = con.execute(
                "SELECT id, COALESCE(last_activity_at, started_at) AS act "
                "FROM sessions ORDER BY act DESC"
            ).fetchall()
        except Exception:
            rows = []
        finally:
            con.close()
        return [(make_ref(self.DB_PATH, r["id"]), r["id"], float(r["act"] or 0)) for r in rows]

    def resolve_session(self, session_ref: str) -> str:
        if session_ref != "current":
            return session_ref
        rows = self._sessions()
        if not rows:
            raise SystemExit(
                f"No Hermes session found in {self.DB_PATH}（先跑 `hermes chat` 产生会话）")
        return rows[0][1]

    def find_transcript(self, session_id: str) -> tuple[str | None, str | None]:
        if not session_id or "/" in session_id or "\\" in session_id or REF_SEP in session_id:
            return None, None
        con = None
        try:
            con = self._connect(readonly=True)
            row = con.execute(
                "SELECT cwd FROM sessions WHERE id = ? LIMIT 1", (session_id,)
            ).fetchone()
        except Exception:
            row = None
        finally:
            if con is not None:
                con.close()
        if row is None:
            return None, None
        return make_ref(self.DB_PATH, session_id), (row["cwd"] or "")

    def find_session_by_request_id(self, request_id: str) -> str | None:
        """本产品无 conversationRequestId；把 `--request-id` 映射到 `platform_message_id`。"""
        if not os.path.exists(self.DB_PATH) or not request_id:
            return None
        con = self._connect(readonly=True)
        try:
            rows = con.execute(
                "SELECT DISTINCT session_id FROM messages WHERE platform_message_id = ? LIMIT 2",
                (request_id,),
            ).fetchall()
        except Exception:
            rows = []
        finally:
            con.close()
        if not rows:
            return None
        branched = {b.get("id") for b in self._read_index().get("branches", [])}
        # 非分支优先（分支会继承被复制消息的 platform_message_id）
        return rows[0]["session_id"] if rows[0]["session_id"] not in branched else rows[-1]["session_id"]

    def list_all_sessions(self) -> list[tuple[str, str]]:
        return [(ref, sid) for ref, sid, _ in self._sessions()]

    def sort_key(self, ref: str) -> float:
        """最近使用排序键 = sessions 的活动时间（ref 不是文件路径，不能 getmtime）。"""
        db, sid = parse_ref(ref)
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            try:
                row = con.execute(
                    "SELECT COALESCE(last_activity_at, started_at) AS act FROM sessions WHERE id = ?",
                    (sid,),
                ).fetchone()
            finally:
                con.close()
            return float(row[0]) if row and row[0] else 0.0
        except Exception:
            return 0.0

    # ------------------------------------------------------------------
    # B. 消息判定
    # ------------------------------------------------------------------
    def is_user_message(self, obj: dict) -> bool:
        return obj.get("role") == "user"

    def is_assistant_message(self, obj: dict) -> bool:
        return obj.get("role") == "assistant"

    def get_text(self, obj: dict) -> str:
        return obj.get("content") or ""

    def get_request_id(self, obj: dict) -> str | None:
        v = obj.get("platform_message_id")
        return v if isinstance(v, str) and v else None

    # ------------------------------------------------------------------
    # C. 读写（行存储契约：messages 行序 → 条目）
    # ------------------------------------------------------------------
    def read_lines(self, ref: str) -> list[dict]:
        if ref in self._pending:
            return self._pending[ref]
        db, sid = parse_ref(ref)
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        try:
            rows = con.execute(
                "SELECT * FROM messages WHERE session_id = ? ORDER BY id", (sid,)
            ).fetchall()
        finally:
            con.close()
        return [dict(r) for r in rows]

    def read_raw(self, ref: str) -> str:
        """读出"每行一条 JSON"的等价文本，供引擎的行数/解析/残留校验复用。

        ⚠️ 必须给 `json.dumps` 兜一个 default：`messages.display_identity` 是 **BLOB**
        （实测有行带 bytes），否则 `Object of type bytes is not JSON serializable`
        会让 verify 直接异常（第一次真机跑就撞上了）。
        **这只影响校验用的文本**——真正的写入走 `read_lines` 的 dict，
        BLOB 仍是原始 bytes，不会被这里降级成字符串。
        """
        lines = self.read_lines(ref)
        return "\n".join(
            json.dumps(o, ensure_ascii=False, default=_json_default) for o in lines
        ) + ("\n" if lines else "")

    def write_branch(self, tmp_ref: str, lines: list[dict]) -> None:
        """只暂存；真正的库写入推迟到 finalize（＝引擎的"发布"动作）。"""
        self._pending[tmp_ref] = [dict(o) for o in lines]

    def branch_target(self, src_ref: str, new_id: str) -> str:
        """产物与源同库、不同 session_id —— 不是新文件。

        **写路径的第一个调用点**，版本闸在这里 fail-fast（详见 `_assert_writable_schema`）。
        """
        self._assert_writable_schema()
        db, _ = parse_ref(src_ref)
        dst_ref = make_ref(db, new_id)
        self._src_of_dst[dst_ref] = src_ref
        return dst_ref

    def rewrite_ids(self, lines: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
        """结构化替换：`messages.session_id` 是**外键**（会话关联字段），必须换新。

        实测 `messages` 其余 25 列**不含**会话 id，故只处理这一列即无残留
        （与 WorkBuddy/Codex 那种"文本里嵌 id"的形态不同）。
        """
        n = 0
        out = []
        for o in lines:
            o = dict(o)
            if o.get("session_id") == old_id:
                o["session_id"] = new_id
                n += 1
            out.append(o)
        return out, n

    def extract_title_hint(self, lines: list[dict]) -> str:
        for o in reversed(lines):
            if self.is_user_message(o):
                t = " ".join((self.get_text(o) or "").split())
                if t:
                    return t[:40]
        return ""

    # ------------------------------------------------------------------
    # D. 落位与注册
    # ------------------------------------------------------------------
    def _pending_of(self, tmp_ref: str) -> list[dict]:
        lines = self._pending.pop(tmp_ref, None)
        if lines is None:
            raise RuntimeError(f"finalize 找不到待落位内容：{tmp_ref}")
        return lines

    def finalize_branch(self, tmp_ref: str, dst_ref: str) -> None:
        """一个事务写完 `sessions` + `messages`（原子；任一步失败整体回滚）。"""
        lines = self._pending_of(tmp_ref)
        src_ref = self._src_of_dst.pop(dst_ref, None)
        if not src_ref:
            raise RuntimeError(f"finalize 缺少源会话引用（branch_target 未被调用？）：{dst_ref}")
        db, new_id = parse_ref(dst_ref)
        _, src_id = parse_ref(src_ref)

        now = time.time()
        con = self._connect()
        try:
            self._gate(con)
            con.execute("BEGIN")
            cur = con.cursor()
            self._insert_session(cur, src_id, new_id, lines, now)
            self._insert_messages(cur, new_id, lines, now)
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()

    def _insert_session(self, cur, src_id: str, new_id: str, lines: list[dict], now: float) -> None:
        cols = self._cols(cur, "sessions")
        src = cur.execute("SELECT * FROM sessions WHERE id = ?", (src_id,)).fetchone()
        if src is None:
            raise RuntimeError(f"源会话不在库中：{src_id}")
        row = {k: src[k] for k in cols}

        # 血缘标记：与产品自身的 fork 完全同形（实测产品写的就是只有这一个键）
        model_config = json.dumps({MARKER_KEY: src_id}, ensure_ascii=False)
        title = self._unique_title(cur, (src["title"] or "") and f"{src['title']} (分支)" or "分支")

        row.update({
            "id": new_id,
            # 源会话 id 出现在两处，且**都必须保留为源 id**（血缘指针，不是残留）：
            "parent_session_id": src_id,      # ← 血缘列（外键指向源会话）
            "model_config": model_config,     # ← 分支可见性标记（同上）
            "started_at": now,
            "ended_at": None,
            "end_reason": None,
            "message_count": len(lines),
            "title": title,
            "title_source": "user",
            # 新会话不该继承"已归档/已隐藏"状态，否则刚造的产物在默认列表里看不见
            "archived": 0,
            "hidden": 0,
            # v31 起新增的"自动归档"位：产品的语义是"只有它的清理扫描会置位、且只置在它归档的行上"。
            # 我们既然把 archived 归零，就必须把它一起归零 ——
            # 否则会产出 `archived=0 且 auto_archived=1` 这种产品语义下不该存在的组合
            # （当前不影响可见性过滤，但属隐性状态污染）。
            # v30 的 sessions 没有这一列，多出的键不会被 INSERT 使用（列清单取自实际表结构）。
            "auto_archived": 0,
            "last_activity_at": now,
        })
        cur.execute(
            f"INSERT INTO sessions ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
            [row[k] for k in cols],
        )

    def _insert_messages(self, cur, new_id: str, lines: list[dict], now: float) -> None:
        """复制前缀。**排除自增主键 `id`**（复制它会与既有行撞主键）。"""
        cols = [c for c in self._cols(cur, "messages") if c != "id"]
        for o in lines:
            d = {c: o.get(c) for c in cols}
            d["session_id"] = new_id
            if d.get("timestamp") is None:
                d["timestamp"] = now
            cur.execute(
                f"INSERT INTO messages ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                [d[c] for c in cols],
            )

    @staticmethod
    def _unique_title(cur, title: str, limit: int = 200) -> str:
        """`title` 上有全局唯一索引 ⇒ 撞名必须让路（否则 IntegrityError 让整个事务回滚）。"""
        base = " ".join((title or "").split())[:80] or "分支"
        cand = base
        n = 1
        while n <= limit:
            if cur.execute(
                "SELECT 1 FROM sessions WHERE title = ? LIMIT 1", (cand,)
            ).fetchone() is None:
                return cand
            n += 1
            cand = f"{base} ({n})"
        return f"{base} {uuid.uuid4().hex[:6]}"

    def register_branch(self, src, new_id, dst_path, name, parent_id=None, at_seq=None,
                        prefix_fp=None) -> None:
        # 产品的会话行随 finalize 落地；这里只写**旁路谱系索引**（引擎体检用）
        if name:
            self._set_title(new_id, name)
        data = self._read_index()
        data.setdefault("branches", []).append({
            "id": new_id,
            "name": name,
            "parent_id": parent_id or src.id,
            "source_id": src.id,
            "path": dst_path,
            "at_seq": at_seq,
            # 前缀指纹（v2.4.15）：体检据此核对"前 at_seq 行是否仍是 fork 当时的产物"
            "prefix_fp": prefix_fp,
            "created_at": src.created_at,
        })
        self._write_index(data)

    def _set_title(self, new_id: str, name: str) -> None:
        """把用户给的 `--name` 落成产品标题（**再次唯一化**：finalize 里那次用的是自动名）。"""
        try:
            con = self._connect()
            try:
                con.execute("BEGIN")
                cur = con.cursor()
                cur.execute(
                    "UPDATE sessions SET title = ?, title_source = 'user' WHERE id = ?",
                    (self._unique_title(cur, name), new_id),
                )
                con.commit()
            except Exception:
                con.rollback()
                raise
            finally:
                con.close()
        except Exception:
            # 标题更新失败不应让分支不可用（行已在库中、模型标记也写好了）
            pass

    def unregister_branch(self, new_id: str) -> None:
        # 撤销注册副作用：删掉库里的行 + 谱系条目（回滚路径，尽力而为）
        try:
            con = self._connect()
            try:
                con.execute("BEGIN")
                cur = con.cursor()
                cur.execute("DELETE FROM messages WHERE session_id = ?", (new_id,))
                cur.execute("DELETE FROM sessions WHERE id = ?", (new_id,))
                con.commit()
            except Exception:
                con.rollback()
            finally:
                con.close()
        except Exception:
            pass
        try:
            data = self._read_index()
            branches = [b for b in data.get("branches", []) if b.get("id") != new_id]
            if len(branches) != len(data.get("branches", [])):
                data["branches"] = branches
                self._write_index(data)
        except Exception:
            pass

    def load_session_meta(self, session_id: str) -> SessionMeta | None:
        if not os.path.exists(self.DB_PATH):
            return None
        con = self._connect(readonly=True)
        try:
            r = con.execute(
                "SELECT id, title, ended_at, end_reason, started_at, cwd, parent_session_id "
                "FROM sessions WHERE id = ?", (session_id,)
            ).fetchone()
        except Exception:
            r = None
        finally:
            con.close()
        if r is None:
            return None
        status = "terminated" if r["ended_at"] else "working"
        if r["end_reason"] in ("branched", "compression"):
            status = "branched"
        return SessionMeta(
            id=r["id"],
            title=r["title"] or "",
            status=status,
            created_at=r["started_at"],
            cwd=r["cwd"] or "",
            parent_id=r["parent_session_id"] or "",
            extra={"end_reason": r["end_reason"] or ""},
        )

    # ------------------------------------------------------------------
    # 旁路谱系索引（与 pi / codex 同格式：{branches:[…]}）
    # ------------------------------------------------------------------
    def _read_index(self) -> dict:
        if os.path.exists(self.LINEAGE_PATH):
            try:
                with open(self.LINEAGE_PATH, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"branches": []}

    def _write_index(self, data: dict) -> None:
        os.makedirs(os.path.dirname(self.LINEAGE_PATH) or ".", exist_ok=True)
        tmp = self.LINEAGE_PATH + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(dumps_safe(data, indent=2))
        os.replace(tmp, self.LINEAGE_PATH)

    def list_branches(self, cwd: str | None = None) -> list[SessionMeta]:
        out = []
        for b in self._read_index().get("branches", []):
            out.append(SessionMeta(
                id=b.get("id", ""),
                title=b.get("name", ""),
                status="",
                created_at=b.get("created_at"),
                cwd=cwd or "",
                parent_id=b.get("parent_id", ""),
            ))
        return out

    def is_branch_name(self, title: str) -> bool:
        return True  # 分支在旁路索引里显式登记，不依赖标题启发式

    # ------------------------------------------------------------------
    # E. 体检 / 备份 / 文案
    # ------------------------------------------------------------------
    def storage_root(self) -> str:
        return self.DB_PATH

    def backups_dir(self) -> str:
        # 与其它产品一致：备份进 Hermes 自己的 home（此前漏了覆盖，会落到 ~/.workbuddy/backups）
        return self._backups_root(os.path.join(self.HERMES_HOME, "fork-backups"))

    def verify_storage(self) -> list[VerifyItem]:
        exists = os.path.exists(self.DB_PATH)
        ver = sess = msgs = fts = None
        if exists:
            try:
                con = self._connect(readonly=True)
                try:
                    ver = self._schema_version(con)
                    sess = con.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
                    msgs = con.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
                    fts = con.execute("SELECT COUNT(*) FROM messages_fts").fetchone()[0]
                finally:
                    con.close()
            except Exception:
                pass
        gate_ok = ver in KNOWN_SCHEMA_VERSIONS
        return [
            VerifyItem(
                "Hermes 会话库 (state.db)", "L2" if msgs else "L1", bool(exists and msgs),
                f"{self.DB_PATH}（{sess} 个会话 / {msgs} 条消息）" if exists
                else f"缺失：{self.DB_PATH}（先跑 `hermes chat` 产生会话）",
            ),
            VerifyItem(
                "schema_version 版本闸", "L2" if ver is not None else "L1", gate_ok,
                f"schema_version = {ver}（本适配器认得 "
                f"{'、'.join(str(x) for x in KNOWN_SCHEMA_VERSIONS)}；白名单外一律拒绝写入）"
                if ver is not None else "读不到 schema_version 表",
            ),
            VerifyItem(
                "行存储契约 messages → 条目", "L2" if msgs else "L1", bool(msgs),
                "按 `id`（插入序）读取；写入时排除自增主键，其余列**按实际列名动态**原样复制"
                "（v0.21.6 新增的 message_uid / tool_call_uids / tool_call_uid / "
                "absorbed_message_uids 等一并随行复制）",
            ),
            VerifyItem(
                "FTS 索引", "L1", True,
                f"messages_fts 现有 {fts} 行；由触发器自维护，适配器不写（实测无需干预）"
                if fts is not None else "未读到 messages_fts",
            ),
            VerifyItem(
                "血缘标记 _branched_from", "L1", True,
                "写入时必须带 —— 实测缺它则分支被产品隐藏（无标记的子体从默认列表消失）",
            ),
            VerifyItem(
                "产品盖章动作", "L1", True,
                "无需 —— 本产品没有 OpenClaw 式 entry_valid；实测纯 SQL 写入即被接受",
            ),
        ]

    def backup_transcript(self, ref: str, backups_dir: str) -> str:
        """备份**整个数据库**（WAL 一致性快照，用官方 backup API）。

        裸 `cp state.db` 会丢掉仍在 `-wal` 里的事务（实测漏过刚创建的对象）。
        """
        db, _ = parse_ref(ref)
        ts = time.strftime("%Y%m%d-%H%M%S")
        backup_dir = os.path.join(backups_dir, ts)
        os.makedirs(backup_dir, exist_ok=True)
        dst = os.path.join(backup_dir, os.path.basename(db))
        src = sqlite3.connect(db)
        out = sqlite3.connect(dst)
        try:
            src.backup(out)
        finally:
            out.close()
            src.close()
        return backup_dir

    def activation_hint(self) -> str:
        return (
            "Hermes 无需重启、无需修复命令：\n"
            "            `hermes sessions list` 即可看到分支；"
            "`hermes chat --resume <分支 id>` 续跑"
        )

    def produce_hint(self) -> str:
        return f"跑一次 `hermes chat -q \"hi\"`（或 `hermes serve`），会话会写入 {self.DB_PATH}"

    def publish_hint(self) -> str:
        return ""  # 无需额外动作（实测：写入即被产品接受）

    def backup_note(self) -> str:
        return "整个 state.db（官方 backup API，含 WAL 的一致性快照）"

    def readonly_hint(self, dst_ref: str) -> str:
        return ""  # 分支是库里的行，不是文件 —— 没有可改权限位的对象
