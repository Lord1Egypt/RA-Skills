# role: adapter:openclaw（SQLite 后端）— 产品适配器，不含引擎逻辑
"""fork_core.adapter_openclaw_sqlite — OpenClaw ≥2026.9.x 的 SQLite 后端。

一手依据（2026-09-14 真机取证，可复跑核对）：

  1. 真机安装 `openclaw@2026.9.4`（latest，要求 Node >=24.16 <25），
     用 ollama 本地模型跑出真实会话。
  2. 落盘判据：`agents/<id>/agent/openclaw-agent.sqlite` 里
     **`transcript_events` 有 31 行、`session_transcript_active_events` 30 行，
     且 sessions/ 下没有任何 .jsonl** —— 转录确实在 SQLite。
  3. 引擎要的唯一契约 —— `(session_id, seq) → event_json` —— 与 JSONL 的
     「行序 → 条目」**完全同构**：seq=0 同样是 `{"type":"session",...}` header，
     后续是同样词汇的 `model_change` / `message` / `custom` 条目，
     同样带 `id` / `parentId` 树。所以抽象层可以做到零语义损失。

存储契约（**一个会话需要 7 张表**，缺一即不可用 —— 全部由实测确定）：

  | 表 | 作用 | 分支侧要写什么 |
  |---|---|---|
  | session_windows | 会话窗口（PRIMARY KEY session_id） | 复制源行，换 session_id / session_key |
  | transcript_events | **转录本体** (session_id,seq)→event_json | 复制 seq < cut，header.id 换新 |
  | transcript_event_identities | seq → event_id / parent_id 反规范化索引 | 随事件复制 |
  | session_transcript_active_events | **投影**：(active_position)→event_seq | 复制 event_seq < cut |
  | transcript_rewrite_watermarks | 代际水印 | 新 generation |
  | session_transcript_index_state | **投影进度**（indexed_seq / leaf_event_id / needs_rebuild） | 见下 |
  | session_nodes | session_key → current_session_id + entry_json | 新行 |

  ⚠️ 两条实测踩出来的坑（都是"少一张表就卡住"）：

  ① **`session_transcript_index_state` 不能省**。漏掉它，会话**能被列出**，但运行时
     会报 `Session transcript projection is rebuilding: <id>` 并拒绝执行 ——
     因为没有投影进度，系统认为需要重建。补齐（indexed_seq = 已投影最大 seq、
     leaf_event_id、active_event_count / active_message_count 与实际行数一致）后即正常。

  ② **`session_nodes.entry_valid` 必须由官方置 1**。表上有 AFTER INSERT 触发器
     `UPDATE session_nodes SET entry_valid = 0`，即**任何直接写入的节点都标记为
     "待校验"**。此时 CLI 会拒绝：`invalid persisted session row requires repair`。
     解法：写入后跑一次官方 `openclaw doctor --fix`（它会校验 entry_json 并把
     entry_valid 置回 1）。本适配器不自行伪造该标志 —— 校验权归产品。

  **产物是活的**：真机实测，Python 造出的分支被 `openclaw sessions` 列出、
  `openclaw agent --session-key` 正常续跑（事件数 20 → 35），且 OpenClaw 自己
  把该分支的 indexed_seq 维护到 34 —— 说明它已完全接管这个分支。

已知边界（如实记录）：
  - 依赖**未公开的内部表结构**，随 OpenClaw 版本变化可能失效；写入失败时应
    回退到 JSONL 后端或提示用户升级适配器。
  - 需要用户在写入后执行一次 `openclaw doctor --fix`（entry_valid 由产品校验）。
  - 不维护 `session_transcript_fts*`（全文检索索引）：该表无触发器，
    缺失只影响会话内搜索，不影响会话加载与会话续跑（实测未触发问题）。
  - 不做"树路径抽取"：与 JSONL 后端一致，截断是 `seq < cut` 前缀。
"""

from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid

from .adapter_base import dumps_safe, parse_jsonl
from .adapter_openclaw import OpenClawJsonlAdapter, BRANCH_KEY_PREFIX
from .models import SessionMeta, VerifyItem

DB_NAME = "openclaw-agent.sqlite"
DB_REL = os.path.join("agent", DB_NAME)
REF_SEP = "#"  # "<db 绝对路径>#<session_id>"


def make_ref(db_path: str, session_id: str) -> str:
    return f"{db_path}{REF_SEP}{session_id}"


def parse_ref(ref: str) -> tuple[str, str]:
    db, _, sid = ref.rpartition(REF_SEP)
    if not db:
        raise ValueError(f"非法 SQLite 转录引用（应形如 <db>#<session_id>）：{ref!r}")
    return db, sid


class OpenClawSqliteAdapter(OpenClawJsonlAdapter):
    """OpenClaw ≥2026.9.x（SQLite 运行时）后端。

    复用 JSONL 后端的格式层（消息判定 / get_text / rewrite_ids / 标题提取 /
    旁路谱系索引），只替换介质相关部分：定位、读写、落位、注册、体检。
    """

    name = "openclaw"

    # 原始内容键（覆盖 JSONL 后端的 {"parentSession","content"}，再加 data）。
    #
    # data：**custom 条目的运行时原始记录**。真机实测，OpenClaw 会在会话中写入
    #   `customType: "openclaw:bootstrap-context:full"` 条目，其 `data` 形如
    #   `{"timestamp":…,"runId":…,"sessionId":<源会话 id>}` —— 它记录的是
    #   「这一次 run 发生在哪个会话上」，是**历史事实**。
    #   分支继承这段历史时，把 sessionId 改成新 id 等于篡改历史记录
    #   （而引擎首轮的残留检查会把它判成"源 id 残留"从而**误拒分支**，
    #   实测复现：errs=['old session id still present in 1 non-raw fields: [L25.data.sessionId]']）。
    #   与 pi 处理 parentSession / content 同一条逻辑：这些字段保留源 id 是合法设计。
    #   ⚠️ 已知风险（如实记录）：若未来某个 OpenClaw 版本改用该字段做**会话归属判断**
    #   而非历史记录，本豁免就需要收紧。当前无证据表明运行时读它定位会话
    #   （会话定位一律走 session_id 列）。
    _RAW_KEYS = {"parentSession", "content", "data"}

    def __init__(self):
        super().__init__()
        self.DB_PATH = os.path.join(self.AGENT_DIR, DB_REL)
        # write_branch → finalize_branch 之间的暂存：key 是产物 ref
        # 这样 verify 能读到"尚未对外可见"的内容，且**不留下悬挂事务**。
        self._pending: dict[str, list[dict]] = {}
        # 产物 ref → 源 ref（branch_target 时记下，finalize 时要靠它复制源行）
        self._src_of_dst: dict[str, str] = {}

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------
    def _connect(self, readonly: bool = False) -> sqlite3.Connection:
        if readonly:
            con = sqlite3.connect(f"file:{self.DB_PATH}?mode=ro", uri=True)
        else:
            con = sqlite3.connect(self.DB_PATH)
        con.row_factory = sqlite3.Row
        return con

    @staticmethod
    def _cols(cur, table: str) -> list[str]:
        return [d[0] for d in cur.execute(f"SELECT * FROM {table} LIMIT 0").description]

    def is_available(self) -> bool:
        if not os.path.exists(self.DB_PATH):
            return False
        try:
            con = self._connect(readonly=True)
            n = con.execute("SELECT COUNT(*) FROM transcript_events").fetchone()[0]
            con.close()
            return n > 0
        except Exception:
            return False

    # ------------------------------------------------------------------
    # A. 定位
    # ------------------------------------------------------------------
    def _sessions(self) -> list[tuple[str, str, int]]:
        """[(ref, session_id, updated_at)]，按更新时间倒序。"""
        if not os.path.exists(self.DB_PATH):
            return []
        con = self._connect(readonly=True)
        try:
            rows = con.execute(
                "SELECT session_id, updated_at FROM session_windows ORDER BY updated_at DESC"
            ).fetchall()
        except Exception:
            rows = []
        finally:
            con.close()
        return [(make_ref(self.DB_PATH, r["session_id"]), r["session_id"], r["updated_at"] or 0) for r in rows]

    def resolve_session(self, session_ref: str) -> str:
        if session_ref != "current":
            return session_ref
        rows = self._sessions()
        if not rows:
            raise SystemExit(f"No OpenClaw session found in {self.DB_PATH}（先跑 openclaw agent 产生会话）")
        return rows[0][1]

    def find_transcript(self, session_id: str) -> tuple[str | None, str | None]:
        if not session_id or "/" in session_id or "\\" in session_id:
            return None, None
        for ref, sid, _ in self._sessions():
            if sid == session_id:
                return ref, self.AGENT_ID
        return None, None

    def find_session_by_request_id(self, request_id: str) -> str | None:
        """按**事件 id** 反查会话（transcript_event_identities.event_id）。"""
        if not os.path.exists(self.DB_PATH) or not request_id:
            return None
        con = self._connect(readonly=True)
        try:
            rows = con.execute(
                "SELECT session_id FROM transcript_event_identities WHERE event_id = ? LIMIT 2",
                (request_id,),
            ).fetchall()
        except Exception:
            rows = []
        finally:
            con.close()
        if not rows:
            return None
        branched = {b.get("id") for b in self._read_index().get("branches", [])}
        # 非分支优先（分支会继承被复制的条目 id）
        return rows[0]["session_id"] if rows[0]["session_id"] not in branched else rows[-1]["session_id"]

    def list_all_sessions(self) -> list[tuple[str, str]]:
        return [(ref, sid) for ref, sid, _ in self._sessions()]

    def is_historical_id_path(self, path: str) -> bool:
        """豁免 custom 条目 `data` 子树里的会话关联字段。

        真机实测：OpenClaw 写入 `customType: "openclaw:bootstrap-context:full"` 条目，
        其 `data` 同时含 `runId` 与 `sessionId` —— 记录"这一次 run 发生在哪个会话"，
        是**历史事实**。分支继承这段历史时不该改写它（改写 = 篡改历史）。
        路径形如 `L25.data.sessionId`，故判定"路径里含 data 段"。
        """
        return ".data." in path or path.endswith(".data")

    def sort_key(self, ref: str) -> float:
        """最近使用排序键 = session_windows.updated_at（ref 不是文件路径）。"""
        db, sid = parse_ref(ref)
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
            try:
                row = con.execute(
                    "SELECT updated_at FROM session_windows WHERE session_id=?", (sid,)
                ).fetchone()
            finally:
                con.close()
            return float(row[0]) if row and row[0] else 0.0
        except Exception:
            return 0.0

    # ------------------------------------------------------------------
    # C. 读写（行存储契约：(session_id, seq) → event_json）
    # ------------------------------------------------------------------
    def read_lines(self, ref: str) -> list[dict]:
        if ref in self._pending:
            return self._pending[ref]
        db, sid = parse_ref(ref)
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            rows = con.execute(
                "SELECT event_json FROM transcript_events WHERE session_id=? ORDER BY seq",
                (sid,),
            ).fetchall()
        finally:
            con.close()
        # 逐个容错解析：DB 里也可能有坏行（半写/上游写坏），一个坏行不该让整轮体检崩
        # （防御性：本机真库实测 0 例，见 adapter_base.parse_jsonl 的证据等级说明）。
        # 坏行的**行号按"第几条事件"计**（seq 升序的序号）——与 at_seq 同一口径。
        out = []
        for r in rows:
            out.extend(parse_jsonl(r[0] if isinstance(r[0], str) else str(r[0])).objs)
        return out

    def read_lines_checked(self, ref: str):
        """坏行按"第几条事件"报出（本后端不走文件，故不能依赖基类的文件默认实现）。"""
        from .adapter_base import ParseResult

        if ref in self._pending:
            return ParseResult(objs=self._pending[ref], bad_lines=[])
        db, sid = parse_ref(ref)
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            rows = con.execute(
                "SELECT event_json FROM transcript_events WHERE session_id=? ORDER BY seq",
                (sid,),
            ).fetchall()
        finally:
            con.close()
        objs, bad = [], []
        for i, r in enumerate(rows, 1):
            res = parse_jsonl(r[0] if isinstance(r[0], str) else str(r[0]))
            objs.extend(res.objs)
            if res.bad_lines:
                bad.append(i)
        # bad_items 与 bad_lines 同为「第几条事件」：本后端没有"文件行号"这一层，
        # 显式给出以免引擎回退到 bad_files 而让尺度契约含糊（显式给出才不含糊）。
        return ParseResult(objs=objs, bad_lines=bad, bad_items=list(bad))

    def read_raw(self, ref: str) -> str:
        """读出「每行一条 JSON」的等价文本，**仅供引擎的行数 / 解析 / 残留校验复用**。

        ⚠️ 这是**读侧**：只在内存里比较，从不 `encode`、从不落盘 ⇒ 含孤立代理也不会崩，
        故**有意**不用 `dumps_safe`（那是**写出点**才需要的安全阀）。
        **不要**把本方法的返回值直接写盘——要写盘请改走 `dumps_safe`。
        """
        lines = self.read_lines(ref)
        return "\n".join(json.dumps(o, ensure_ascii=False) for o in lines) + ("\n" if lines else "")

    def branch_target(self, src_ref: str, new_id: str) -> str:
        """产物与源同库、不同 session_id —— 不是新文件。"""
        db, _ = parse_ref(src_ref)
        dst_ref = make_ref(db, new_id)
        self._src_of_dst[dst_ref] = src_ref
        return dst_ref

    def write_branch(self, tmp_ref: str, lines: list[dict]) -> None:
        """只暂存；真正的库写入推迟到 finalize（= 引擎的"发布"动作）。

        这与 JSONL 后端写 .tmp 是同一种语义：校验期内容**对外不可见**，
        但校验器能读到。区别只是介质不同。
        """
        self._pending[tmp_ref] = [dict(o) for o in lines]

    def finalize_branch(self, tmp_ref: str, dst_ref: str) -> None:
        """一次性把 7 张表写进同一个事务（原子；任一步失败则整体回滚）。"""
        lines = self._pending.pop(tmp_ref, None)
        if lines is None:
            raise RuntimeError(f"finalize 找不到待落位内容：{tmp_ref}")
        src_ref = self._src_of_dst.pop(dst_ref, None)
        if not src_ref:
            raise RuntimeError(f"finalize 缺少源会话引用（branch_target 未被调用？）：{dst_ref}")
        db, new_id = parse_ref(dst_ref)
        _, src_id = parse_ref(src_ref)

        cut = len(lines)
        new_key = f"agent:{self.AGENT_ID}:{BRANCH_KEY_PREFIX}{new_id[:8]}"
        now_ms = int(time.time() * 1000)
        con = self._connect()
        try:
            con.execute("BEGIN")
            self._copy_session_rows(con, src_id, new_id, new_key, lines, cut, now_ms)
            con.commit()
        except Exception:
            con.rollback()
            raise
        finally:
            con.close()
        # 分支的 header.id 已由引擎的 rewrite_ids 换过，库内 header 与之一致

    def _copy_session_rows(self, con, src_id, new_id, new_key, lines, cut, now_ms) -> None:
        cur = con.cursor()

        def dup(table, overrides, extra=None):
            cs = self._cols(cur, table)
            sql = f"SELECT * FROM {table} WHERE session_id=?"
            if extra:
                sql += " AND " + extra
            n = 0
            for r in cur.execute(sql, (src_id,)).fetchall():
                d = {k: r[k] for k in cs}
                d.update(overrides)
                cur.execute(
                    f"INSERT INTO {table} ({','.join(cs)}) VALUES ({','.join('?' * len(cs))})",
                    [d[k] for k in cs],
                )
                n += 1
            return n

        # 1. 会话窗口
        dup("session_windows", {
            "session_id": new_id, "session_key": new_key,
            "previous_session_id": src_id, "reason": "fork",
            "created_at": now_ms, "updated_at": now_ms,
            "transcript_updated_at": now_ms, "transcript_observed_at": now_ms,
        })
        # 2. 转录本体（引擎已截断 + 换 header.id，这里按 seq 顺序落库）
        for seq, obj in enumerate(lines):
            cur.execute(
                "INSERT INTO transcript_events (session_id,seq,event_json,created_at) VALUES (?,?,?,?)",
                (new_id, seq, dumps_safe(obj), now_ms),
            )
        # 3/4. 反规范化索引 + 投影行：随事件裁剪
        dup("transcript_event_identities", {"session_id": new_id}, extra=f"seq < {cut}")
        dup("session_transcript_active_events", {"session_id": new_id}, extra=f"event_seq < {cut}")
        # 5. 代际水印
        dup("transcript_rewrite_watermarks",
            {"session_id": new_id, "generation": uuid.uuid4().hex, "updated_at": now_ms})
        # 6. 投影进度（漏了它 → "projection is rebuilding"）
        msg_cnt = cur.execute(
            "SELECT COUNT(*) FROM session_transcript_active_events "
            "WHERE session_id=? AND message_position IS NOT NULL", (new_id,)).fetchone()[0]
        ev_cnt = cur.execute(
            "SELECT COUNT(*) FROM session_transcript_active_events WHERE session_id=?",
            (new_id,)).fetchone()[0]
        cur.execute(
            "INSERT INTO session_transcript_index_state "
            "(session_id,indexed_seq,leaf_event_id,needs_rebuild,"
            "active_event_count,active_message_count,updated_at) VALUES (?,?,?,0,?,?,?)",
            (new_id, cut - 1, lines[-1].get("id") if lines else None, ev_cnt, msg_cnt, now_ms),
        )
        # 7. 会话节点（entry_valid 交由产品校验：触发器会先置 0）
        sn_cs = self._cols(cur, "session_nodes")
        src_node = cur.execute(
            "SELECT * FROM session_nodes WHERE current_session_id=?", (src_id,)).fetchone()
        if src_node:
            d = {k: src_node[k] for k in sn_cs}
            entry = json.loads(d["entry_json"]) if d.get("entry_json") else {}
            entry.update({"sessionId": new_id, "updatedAt": now_ms, "sessionStartedAt": now_ms})
            d.update({
                "session_key": new_key, "current_session_id": new_id,
                "entry_json": dumps_safe(entry),
                "entry_valid": 0, "updated_at": now_ms, "created_at": now_ms,
                "fork_source_session_key": src_node["session_key"],
                "fork_source_session_id": src_id,
                "fork_source_entry_id": None,
                "parent_session_key": src_node["session_key"],
            })
            cur.execute(
                f"INSERT INTO session_nodes ({','.join(sn_cs)}) VALUES ({','.join('?' * len(sn_cs))})",
                [d[k] for k in sn_cs],
            )

    def backup_transcript(self, ref: str, backups_dir: str) -> str:
        """备份**整个数据库**（含 WAL）。用 SQLite 官方 backup API 保证一致性。"""
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

    # ------------------------------------------------------------------
    # D. 注册（OpenClaw 无 sessions.json；session_nodes 已在 finalize 写入）
    # ------------------------------------------------------------------
    def register_branch(self, src, new_id, dst_path, name, parent_id=None, at_seq=None,
                        prefix_fp=None) -> None:
        # 产品索引（session_nodes）随 finalize 落地；这里只写旁路谱系索引
        super(OpenClawJsonlAdapter, self).register_branch(
            src, new_id, dst_path, name, parent_id=parent_id, at_seq=at_seq,
            prefix_fp=prefix_fp)

    def unregister_branch(self, new_id: str) -> None:
        super(OpenClawJsonlAdapter, self).unregister_branch(new_id)
        try:
            con = self._connect()
            con.execute("PRAGMA foreign_keys=ON")
            con.execute("DELETE FROM session_nodes WHERE current_session_id=?", (new_id,))
            con.execute("DELETE FROM session_windows WHERE session_id=?", (new_id,))
            con.commit()
            con.close()
        except Exception:
            pass

    def load_session_meta(self, session_id: str) -> SessionMeta | None:
        for ref, sid, _ in self._sessions():
            if sid == session_id:
                cwd = ""
                try:
                    lines = self.read_lines(ref)
                    if lines:
                        cwd = lines[0].get("cwd") or ""
                except Exception:
                    pass
                return SessionMeta(id=session_id, title="", status="", created_at=os.path.getmtime(self.DB_PATH), cwd=cwd)
        return None

    # ------------------------------------------------------------------
    # E. 体检
    # ------------------------------------------------------------------
    def storage_root(self) -> str:
        return self.DB_PATH

    def verify_storage(self) -> list[VerifyItem]:
        ok = os.path.exists(self.DB_PATH)
        n = ev = 0
        if ok:
            try:
                con = self._connect(readonly=True)
                n = con.execute("SELECT COUNT(DISTINCT session_id) FROM transcript_events").fetchone()[0]
                ev = con.execute("SELECT COUNT(*) FROM transcript_events").fetchone()[0]
                con.close()
            except Exception:
                pass
        return [
            VerifyItem(
                "OpenClaw SQLite 转录库",
                "L2" if ev else "L1",
                ok and ev > 0,
                f"{self.DB_PATH}（{n} 个会话 / {ev} 条事件）" if ok
                else f"缺失：{self.DB_PATH}（先跑 `openclaw agent` 产生会话）",
            ),
            VerifyItem(
                "行存储契约 (session_id, seq) → event_json",
                "L2" if ev else "L1",
                ev > 0,
                "与 JSONL 的「行序 → 条目」同构；引擎按 seq 排序读取",
            ),
            VerifyItem(
                "会话节点 entry_valid",
                "L1",
                True,
                "由 OpenClaw 校验后置位；分支写入后需跑一次 `openclaw doctor --fix`",
            ),
        ]

    # ------------------------------------------------------------------
    # G. 文案
    # ------------------------------------------------------------------
    def activation_hint(self) -> str:
        return (
            "OpenClaw 分支已写入 %s（7 张表，事务提交）：\n"
            "            ① 跑一次 `openclaw doctor --fix`（让官方校验并置 entry_valid）\n"
            "            ② `openclaw sessions --json` 即可列出；用 "
            "`openclaw agent --session-key agent:%s:%s<8位>` 续跑"
            % (os.path.basename(self.DB_PATH), self.AGENT_ID, BRANCH_KEY_PREFIX)
        )

    def produce_hint(self) -> str:
        return (
            "跑一次 OpenClaw（如 `openclaw agent --local --session-key agent:%s:demo "
            "--message 'hi'`），转录会写入 %s" % (self.AGENT_ID, self.DB_PATH)
        )

    def publish_hint(self) -> str:
        return "openclaw doctor --fix"

    def backup_note(self) -> str:
        return "整个 SQLite 数据库（官方 backup API，一致性快照）"

    def readonly_hint(self, dst_ref: str) -> str:
        # 分支是库里的行，不是文件 —— 没有可改权限位的对象
        return ""
