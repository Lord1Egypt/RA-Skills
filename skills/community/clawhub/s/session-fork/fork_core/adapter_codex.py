# role: adapter:codex — 产品适配器，不含引擎逻辑
"""fork_core.adapter_codex — Codex（codex-cli / ChatGPT 桌面版内嵌）适配器。

一手依据（2026-09-14 真机取证 + 原生分叉对照；每条结论的命令与原始输出
均可复跑核对）：

真机环境
  - 二进制 `/Applications/ChatGPT.app/Contents/Resources/codex`，`codex-cli 0.150.0-alpha.8`，
    **不在 PATH**（ChatGPT 桌面应用内嵌，非 npm 全局安装）。
  - 隔离靠环境变量 **`CODEX_HOME`**（**没有** `--home` 参数）。
  - 零密钥造会话：`codex exec --oss --local-provider ollama -m <model> …`。

存储契约（三层，缺一即不可见）

  | 层 | 位置 | 分支侧要写什么 |
  |---|---|---|
  | 转录 | `$CODEX_HOME/sessions/YYYY/MM/DD/rollout-<本地ISO>-<uuid>.jsonl` | 自包含截断前缀（本适配器） |
  | 线程索引 | `state_5.sqlite` → `threads`（38 列，`rollout_path` NOT NULL） | 新行，**显式列名** INSERT |
  | 投影游标 | `thread_history_1.sqlite` → `thread_history_projection_state` | 新行 `(id, 0, 0)` = 尚未消费 |

关键实测事实（逐条都有对照实验）

  1. **文件名尾缀 = 会话 id**（5/5 吻合）。故 `list_all_sessions` 不能用 `fn[:-6]`：
     要 `fn.endswith("<sid>.jsonl")`。
  2. **`ordinal` 是「顶层键」**（`{type, ordinal, timestamp, payload}`），`session_meta` = 0、
     逐行 +1。原始取证曾误记为 `payload.ordinal`，已订正。
  3. **`role="user"` 不全是用户输入**：`<environment_context>` / `<recommended_plugins>` /
     `<permissions instructions>` / `<model_switch>` / 审批审查提示都会以 `role=user` 出现。
     只按 role 判定会把截断点落错位置 → 本适配器用前缀白名单排除（见 `_INJECTION_PREFIXES`）。
     ⚠️ 该白名单是**归纳**而非官方定义，随版本可能新增；已列入"待复测"。
  4. **新旧版本存在镜像重复**：新版会把同一条消息同时写成
     `response_item/message` 与 `event_msg/{user,agent}_message`。两者都计入会让
     **轮次翻倍**。设计决定：**只取 `response_item/message` 一族为权威**，
     `event_msg` 只用于读取 `thread_id` 等元信息。
  5. **会话 id 出现在三类位置**（实测 124 处）：
     `payload.thread_id`（59，最多）、沙箱可写根目录路径/权限条目/`workspace_roots`
     （配置渲染）、`payload.content[].text`（4 处，**全部是环境/权限注入的渲染文本**）。
     逐条核对后确认：`content` 里的 id 命中**没有一处在真实对话正文**里，
     因此本适配器**不把 `content` 列入 `_RAW_KEYS`**（与 pi / OpenClaw 的做法相反）。
     ⚠️ 代价：若真实用户消息正文里恰好出现源会话 id，会被改写。已知并接受
     （若将来出现误报，应改为"仅对注入型 role=user 消息改写 content"的精确规则）。
  6. **`context_window.window_id` 派生自会话 id 前缀**（实测
     `01a04c4a-fbb3-77c2-9809-` + 12 位随机 hex）→ 通用子串替换**命不中**它，
     必须单独重算，否则分支会继承源的上下文窗口身份。
  7. **`threads.rollout_path` 必须是 `$CODEX_HOME` 内的绝对路径**。实测：把库复制到
     隔离 home 后不改该列，`codex exec fork` 直接失败——
     `rollout path '…/.codex/…' must be in Codex home directory (code -32600)`。
     故新行必须写绝对路径，且指向 `$CODEX_HOME` 之内。
  8. **原生分叉是「零拷贝引用式」**（`codex exec fork` 实测）：
     新 rollout 只含 `session_meta` + 本回合条目，历史通过
     `payload.history_base = {thread_id, end_ordinal_exclusive, end_byte_offset}`
     **指针**引用源线程，血缘写在 `payload.forked_from_id`。
     在一个含 66 处 `visualizations/<日期>/<会话id>` 路径的桌面会话上对照：
     分叉产物里 `visualizations` 出现 **0** 次、源 id 仅 **2** 处（两个血缘指针）。
     **本适配器当前采用「自包含拷贝」而非指针式**（理由见文末"设计取舍"），
     但把指针式契约完整记录在案，供引擎未来升级为通用"引用式分叉"。
  9. **原生分叉不写** `thread_spawn_edges`（实测恒 0 行）与 `session_index.jsonl`
     （实测分叉前后 4 行不变）。本适配器同样不写。
 10. **原生分叉不改源文件**（实测源 rollout 字节/行数完全不变）——与本引擎
     "源只读"铁律一致。
 11. `threads` 列集随版本漂移（38 列，社区警告列集会变）→ **显式列名 INSERT，禁 SELECT ***。

设计取舍：为什么用「自包含拷贝」而不是产品原生的「指针式」

  - 引擎契约（`verify_branch`）要求产物行数 == 截断点，且能对产物做残留校验；
    指针式产物不含历史，行数天然对不上，需要引擎层新增"引用式"抽象 —— 属
    下一步契约演进，不在本轮适配器范围内。
  - 自包含产物**不依赖源文件存续**（源被删/被归档/字节偏移漂移都不影响），
    也与其余四个产品的分支语义一致（分支=独立可携带的会话）。
  - 代价：桌面会话的 rollout 可达数 MB，拷贝是 O(源大小)。已知并接受。
  - 为使自包含产物正确，`session_meta` 需要两处**归一化**（见 `write_branch`）：
    ① 丢弃源的 `history_base`（否则产品会把祖父会话历史再拼一遍 → 重复）；
    ② `history_mode` 归一为 `paginated`。
"""

from __future__ import annotations

import json
import os
import shutil
import sqlite3
import time
import uuid

from .adapter_base import TranscriptionAdapter, dumps_safe, read_jsonl_file
from .models import SessionMeta, VerifyItem

#: 转录布局
SESSIONS_DIR_NAME = "sessions"
ARCHIVED_DIR_NAME = "archived_sessions"
STATE_DB_NAME = "state_5.sqlite"
HISTORY_DB_NAME = "thread_history_1.sqlite"
#: 旁路谱系索引（不污染 Codex 官方存储；token 与 pi 一致便于统一运维）
LINEAGE_NAME = "fork.lineage.json"
BACKUPS_DIR_NAME = "fork-backups"

#: `role=user` 但属**注入项**的文本前缀白名单（实测归纳，非官方定义）。
_INJECTION_PREFIXES = (
    "<environment_context>",
    "<recommended_plugins>",
    "<app-context>",
    "<permissions instructions>",
    "<skills_instructions>",
    "<model_switch>",
    "The following is the Codex agent history",
)

#: 消息正文的块类型（response_item/message.content[]）
_TEXT_PART_TYPES = ("input_text", "output_text", "text")


class CodexAdapter(TranscriptionAdapter):
    """Codex 适配器（JSONL 转录 + 两个 SQLite 索引层）。"""

    name = "codex"

    #: 允许保留源 id 的键 —— **血缘指针**，不是会话关联字段。
    #:
    #: `forked_from_id` / `history_base` 记录"本会话从哪个会话派生"，写源 id 是
    #: **正确语义**（与 pi 的 `parentSession`、OpenClaw 的 `data.sessionId` 同一条逻辑）。
    #: 列入黑名单后，引擎的残留检查不会把它们误判为污染。
    _RAW_KEYS = {"forked_from_id", "history_base"}

    #: 是否把分支血缘写进产品自己的字段（`payload.forked_from_id`）。
    #: 置 False 则产物完全不提血缘（只留旁路索引）。
    SET_FORKED_FROM = True

    #: 投影游标初值。产品在"会话刚建、尚未消费 rollout"时写 (0, 0)；
    #: 我们不伪造派生状态（thread_turns / thread_items 留空），
    #: 让产品自己从 rollout 重建投影 —— 与 OpenClaw "校验权归产品"同一条原则。
    PROJECTION_RESET = True

    def __init__(self):
        # ⚠️ 必须在 __init__ 时读环境变量：CODEX_HOME 可能在本模块导入后才设置
        self.CODEX_HOME = os.environ.get("CODEX_HOME") or os.path.join(
            os.path.expanduser("~"), ".codex")
        self.SESSIONS_DIR = os.path.join(self.CODEX_HOME, SESSIONS_DIR_NAME)
        self.ARCHIVED_DIR = os.path.join(self.CODEX_HOME, ARCHIVED_DIR_NAME)
        self.STATE_DB = os.path.join(self.CODEX_HOME, STATE_DB_NAME)
        self.HISTORY_DB = os.path.join(self.CODEX_HOME, HISTORY_DB_NAME)
        self.LINEAGE_PATH = os.path.join(self.CODEX_HOME, LINEAGE_NAME)
        self._src_of_dst: dict[str, str] = {}
        # engine 传入 write_branch 的是**暂存路径**（dst.<pid>.<hex>.tmp），
        # 与 branch_target 返回的 dst 不同名 → 不能用 _src_of_dst 反查，
        # 故在 branch_target 时把源 id 记在这里供 write_branch 用。
        self._cur_src_id: str | None = None

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------
    @staticmethod
    def _pl(o: dict) -> dict:
        p = o.get("payload")
        return p if isinstance(p, dict) else {}

    def _connect(self, db: str, readonly: bool = False) -> sqlite3.Connection:
        if readonly:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        else:
            con = sqlite3.connect(db)
        con.row_factory = sqlite3.Row
        return con

    @staticmethod
    def _cols(cur, table: str) -> list[str]:
        """取列名（用 SELECT * LIMIT 0，不写死列序 —— 列集会随版本漂移）。"""
        return [d[0] for d in cur.execute(f"SELECT * FROM {table} LIMIT 0").description]

    @staticmethod
    def _looks_injected(text: str) -> bool:
        t = (text or "").lstrip()
        return any(t.startswith(p) for p in _INJECTION_PREFIXES)

    def is_available(self) -> bool:
        return os.path.isdir(self.CODEX_HOME) and (
            os.path.isdir(self.SESSIONS_DIR) or os.path.exists(self.STATE_DB))

    # ------------------------------------------------------------------
    # A. 定位
    # ------------------------------------------------------------------
    def _thread_rows(self) -> list[sqlite3.Row]:
        if not os.path.exists(self.STATE_DB):
            return []
        try:
            con = self._connect(self.STATE_DB, readonly=True)
            try:
                return con.execute(
                    "SELECT * FROM threads ORDER BY recency_at DESC, updated_at DESC"
                ).fetchall()
            finally:
                con.close()
        except Exception:
            return []

    def _iter_rollouts(self, include_archived: bool = True):
        """(path, session_id) 由**文件名尾缀**解析 id（不能 fn[:-6]）。"""
        pats = [self.SESSIONS_DIR]
        if include_archived:
            pats.append(self.ARCHIVED_DIR)
        for root in pats:
            if not os.path.isdir(root):
                continue
            for dp, _dns, fns in os.walk(root):
                for fn in fns:
                    if not fn.startswith("rollout-") or not fn.endswith(".jsonl"):
                        continue
                    yield os.path.join(dp, fn), self._id_from_filename(fn)

    @staticmethod
    def _id_from_filename(fn: str) -> str:
        """`rollout-<本地ISO>-<uuid>.jsonl` → `<uuid>`。

        uuid 固定 36 字符（8-4-4-4-12），从尾部切最稳，不依赖 ISO 段的位数。
        """
        return fn[len("rollout-"):-len(".jsonl")][-36:]

    def resolve_session(self, session_ref: str) -> str:
        if session_ref != "current":
            return session_ref
        rows = self._thread_rows()
        for r in rows:
            if not r["archived"]:
                return r["id"]
        if rows:
            return rows[0]["id"]
        raise SystemExit(
            f"No Codex thread found in {self.STATE_DB}（先跑一次 codex 产生会话）")

    def find_transcript(self, session_id: str) -> tuple[str | None, str | None]:
        """按 `threads.rollout_path` 定位；库缺失/行缺失时退回文件名扫描。

        返回 (path, workspace_slug)。Codex 无 workspace 概念，slug 用 $CODEX_HOME。
        """
        if not session_id or "/" in session_id or "\\" in session_id:
            return None, None
        for r in self._thread_rows():
            if r["id"] == session_id:
                p = r["rollout_path"]
                if p and os.path.exists(p):
                    return p, self.CODEX_HOME
                break
        for path, sid in self._iter_rollouts():
            if sid == session_id:
                return path, self.CODEX_HOME
        return None, None

    def find_session_by_request_id(self, request_id: str) -> str | None:
        """按**条目 id**（`payload.id`，形如 `msg_…`）反查会话。

        Codex 没有 conversationRequestId；`response_item/message` 的 `payload.id`
        是等价的精确锚点（与 pi 同思路）。扫描有上限：只查最近 20 个 rollout。
        """
        if not request_id:
            return None
        branched = {b.get("id") for b in self._read_index().get("branches", [])}
        candidates = list(self._iter_rollouts())[:20]
        for path, sid in candidates:
            try:
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        if request_id in line:
                            if sid not in branched:
                                return sid
                            break
            except OSError:
                continue
        for path, sid in candidates:
            try:
                with open(path, encoding="utf-8") as f:
                    if any(request_id in l for l in f):
                        return sid
            except OSError:
                continue
        return None

    # ------------------------------------------------------------------
    # B. 消息判定
    # ------------------------------------------------------------------
    def is_user_message(self, obj: dict) -> bool:
        """**权威族** `response_item/message` + role=user + 非注入项。

        注入项过滤见 `_INJECTION_PREFIXES`（发现 3）。不过滤会让截断点落在
        环境注入上；`event_msg/user_message` 族**有意不计入**（发现 2 的镜像重复）。
        """
        p = self._pl(obj)
        if obj.get("type") != "response_item" or p.get("type") != "message":
            return False
        if p.get("role") != "user":
            return False
        return not self._looks_injected(self.get_text(obj))

    def is_assistant_message(self, obj: dict) -> bool:
        """`response_item/message` + role=assistant（**不含** developer / 审查判决 JSON）。

        审批审查会话里 assistant 文本是 `{"outcome":"allow"}` 这类判决 JSON ——
        它们是真 assistant 条目，但 `get_text` 不会把非文本块当正文；
        本方法只做角色判定，文本完整性由 `verify_branch` 的末行检查负责。
        """
        p = self._pl(obj)
        return (obj.get("type") == "response_item" and p.get("type") == "message"
                and p.get("role") == "assistant")

    def get_text(self, obj: dict) -> str:
        p = self._pl(obj)
        if p.get("type") != "message":
            return ""
        if p.get("role") not in ("user", "assistant", "developer", "system"):
            return ""
        parts = []
        for c in p.get("content") or []:
            if isinstance(c, dict) and c.get("type") in _TEXT_PART_TYPES \
                    and isinstance(c.get("text"), str):
                parts.append(c["text"])
        return "\n".join(parts)

    def get_request_id(self, obj: dict) -> str | None:
        """条目锚点 = `payload.id`（仅 message 条目；session_meta 的 id 是会话 id）。"""
        p = self._pl(obj)
        if p.get("type") != "message":
            return None
        rid = p.get("id")
        return rid if isinstance(rid, str) else None

    # ------------------------------------------------------------------
    # C. 读写
    # ------------------------------------------------------------------
    def read_lines(self, path: str) -> list[dict]:
        # 坏行跳过（不抛）：读取方不该因为一行坏掉就整轮崩；
        # 需要坏行行号时走 read_lines_checked（见 adapter_base.parse_jsonl 的说明）。
        return read_jsonl_file(path).objs

    def write_branch(self, path: str, lines: list[dict]) -> None:
        """写产物 + 两处 `session_meta` 归一化（自包含分支的成立条件）。

        ① 丢弃 `history_base`：源若本身是分支，它带着指向祖父的指针；照抄会让
           产品把祖父历史再拼一遍 → 历史重复。自包含产物必须自带完整历史。
        ② `history_mode` 归一为 `paginated`：与产品新建会话的取值一致，
           并配有 projection_state 新行（见 register_branch）。
        ③ 可选写入 `forked_from_id`（血缘，属 `_RAW_KEYS` 故不触发残留误报）。
        """
        out = []
        for o in lines:
            if isinstance(o, dict) and o.get("type") == "session_meta":
                o = dict(o)
                p = dict(o.get("payload") or {})
                p.pop("history_base", None)
                p["history_mode"] = "paginated"
                if self.SET_FORKED_FROM and self._cur_src_id:
                    p["forked_from_id"] = self._cur_src_id
                o["payload"] = p
            out.append(o)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(dumps_safe(o) for o in out) + "\n")

    def rewrite_ids(self, lines: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
        """会话 id 结构化替换。

        通用递归替换（排除 `_RAW_KEYS`）+ 两处**专项处理**：

        - `payload.session_id` / `payload.id` / `payload.thread_id` / 权限路径里的
          目录名 / `content[].text` 里的注入渲染 —— 都由通用替换覆盖。
        - `context_window.window_id`：**不包含完整会话 id**（只有前 24 字符 + 12 位随机），
          通用替换命不中 → 单独按 `new_id` 前 24 字符重算，避免分支继承源的上下文窗口身份。
        """
        replacements = 0
        win_new = self._derive_window_id(new_id)

        def walk(node, key=None):
            nonlocal replacements
            if isinstance(node, str):
                if old_id in node:
                    replacements += 1
                    return node.replace(old_id, new_id)
                return node
            if isinstance(node, dict):
                out = {}
                for k, v in node.items():
                    if k in self._RAW_KEYS:
                        out[k] = v
                        continue
                    if k == "context_window" and isinstance(v, dict) and v.get("window_id"):
                        nv = dict(v)
                        if nv["window_id"] != win_new:
                            nv["window_id"] = win_new
                            replacements += 1
                        out[k] = {kk: walk(vv, kk) for kk, vv in nv.items()}
                        continue
                    out[k] = walk(v, k)
                return out
            if isinstance(node, list):
                return [walk(v, key) for v in node]
            return node

        return [walk(o) for o in lines], replacements

    @staticmethod
    def _derive_window_id(session_id: str) -> str:
        """实测形态：会话 id 的**前 4 组**（23 字符，不含第 4 个连字符）+ '-' + 12 位随机 hex。

        例：`01a04c4a-fbb3-77c2-9809-89454417c73c` → `01a04c4a-fbb3-77c2-9809-8950dc628136`。
        切 24 字符会多带一个连字符，产出 `…9809--xxxxxxxxxxxx` 这种畸形值
        （2026-09-14 首次真机产物核对时抓出）。
        """
        return f"{session_id[:23]}-{uuid.uuid4().hex[:12]}"

    def extract_title_hint(self, lines: list[dict]) -> str:
        for o in reversed(lines):
            if not self.is_user_message(o):
                continue
            text = self.get_text(o).strip()
            if not text or text.startswith(("<", "<!--")):
                continue
            first = text.split("\n")[0].strip()
            if len(first) < 2 or first.startswith(("!", "/", "#", "```")):
                continue
            return first[:15] + "…" if len(first) > 15 else first
        return ""

    def branch_target(self, src_ref: str, new_id: str) -> str:
        """产物路径：**今天**的日期目录 + `rollout-<本地ISO>-<new_id>.jsonl`。

        实测原生分叉即落在"分叉当天"的 `sessions/YYYY/MM/DD/` 下，
        文件名时间戳用**本地时间**（`2026-09-14T15-22-54` ↔ meta 里的 `07:22:54Z`）。
        """
        t = time.localtime()
        day = os.path.join(self.SESSIONS_DIR, time.strftime("%Y", t),
                           time.strftime("%m", t), time.strftime("%d", t))
        fn = f"rollout-{time.strftime('%Y-%m-%dT%H-%M-%S', t)}-{new_id}.jsonl"
        dst = os.path.join(day, fn)
        self._src_of_dst[dst] = src_ref
        self._cur_src_id = self._split_ref(src_ref)[1]
        return dst

    @staticmethod
    def _split_ref(ref: str) -> tuple[str, str]:
        """ref 对 Codex 就是 rollout 文件路径；返回 (ref, 会话id)。"""
        return ref, CodexAdapter._id_from_filename(os.path.basename(ref))

    def backup_transcript(self, ref: str, backups_dir: str) -> str:
        """备份 rollout 文件 **+ 两个索引库**（分叉会同时改两侧，缺一不可回滚）。"""
        ts = time.strftime("%Y%m%d-%H%M%S")
        backup_dir = os.path.join(backups_dir, ts)
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy2(ref, os.path.join(backup_dir, os.path.basename(ref)))
        for db in (self.STATE_DB, self.HISTORY_DB):
            if os.path.exists(db):
                try:
                    s = sqlite3.connect(db)
                    d = sqlite3.connect(os.path.join(backup_dir, os.path.basename(db)))
                    try:
                        s.backup(d)
                    finally:
                        d.close()
                        s.close()
                except Exception:
                    pass
        return backup_dir

    # ------------------------------------------------------------------
    # D. 注册与查询
    # ------------------------------------------------------------------
    def load_session_meta(self, session_id: str) -> SessionMeta | None:
        for r in self._thread_rows():
            if r["id"] == session_id:
                return SessionMeta(
                    id=session_id,
                    title=r["title"] or "",
                    status="archived" if r["archived"] else "active",
                    created_at=r["created_at"],
                    cwd=r["cwd"] or "",
                    extra={"rollout_path": r["rollout_path"], "source": r["source"]},
                )
        return None

    def register_branch(self, src, new_id, dst_path, name, parent_id=None,
                        at_seq=None, prefix_fp=None) -> None:
        """写两层索引：`threads` 新行 + `thread_history_projection_state` 新行。

        时序：文件已由 finalize_branch 落位（引擎的发布动作），本方法再补索引。
        两个库分属不同文件、无法共用一个事务 —— 采用"先 state_5 后 history_1"，
        任一步失败即整体抛错，由引擎调用 `unregister_branch` 清干净。
        """
        src_id = parent_id or src.id
        if not os.path.exists(dst_path):
            raise RuntimeError(f"register_branch: 产物文件不存在：{dst_path}")
        with open(dst_path, "rb") as f:
            blob = f.read()
        n_bytes = len(blob)
        n_lines = sum(1 for l in blob.splitlines() if l.strip())

        src_row = None
        for r in self._thread_rows():
            if r["id"] == src_id:
                src_row = r
                break

        now = int(time.time())
        now_ms = int(time.time() * 1000)

        # ---- state_5.threads：显式列名 INSERT（列集会随版本漂移，禁 SELECT *） ----
        con = self._connect(self.STATE_DB)
        try:
            con.execute("BEGIN")
            cur = con.cursor()
            cols = self._cols(cur, "threads")
            vals = {c: None for c in cols}
            if src_row is not None:
                for c in cols:
                    vals[c] = src_row[c]
            vals.update({
                "id": new_id,
                "rollout_path": os.path.abspath(dst_path),
                "created_at": now,
                "updated_at": now,
                "created_at_ms": now_ms,
                "updated_at_ms": now_ms,
                "recency_at": now,
                "recency_at_ms": now_ms,
                # 分支名进 title/preview：列表里与源区分开
                "title": name,
                "preview": name,
                # 分支自包含完整历史 → history_mode 与产品新建会话一致
                "history_mode": "paginated",
                "archived": 0,
                "archived_at": None,
                "is_pinned": 0,
            })
            # 库列集可能多于/少于我们已知的字段：只 INSERT 库里真实存在的列
            use = [c for c in cols if c in vals]
            cur.execute(
                f"INSERT INTO threads ({','.join(use)}) VALUES ({','.join('?' * len(use))})",
                [vals[c] for c in use],
            )
            con.commit()
        except Exception:
            con.rollback()
            con.close()
            raise
        con.close()

        # ---- thread_history_1.thread_history_projection_state ----
        con = self._connect(self.HISTORY_DB)
        try:
            con.execute("BEGIN")
            if self.PROJECTION_RESET:
                # (0,0) = "尚未消费本 rollout"。让产品自己从 byte 0 重建投影，
                # 我们不伪造 thread_turns / thread_items 这类派生状态。
                con.execute(
                    "INSERT OR REPLACE INTO thread_history_projection_state "
                    "(thread_id, next_rollout_byte_offset, next_rollout_ordinal) "
                    "VALUES (?,?,?)", (new_id, 0, 0))
            else:
                con.execute(
                    "INSERT OR REPLACE INTO thread_history_projection_state "
                    "(thread_id, next_rollout_byte_offset, next_rollout_ordinal) "
                    "VALUES (?,?,?)", (new_id, n_bytes, n_lines))
            con.commit()
        except Exception:
            con.rollback()
            con.close()
            raise
        con.close()

        # ---- 旁路谱系索引 ----
        data = self._read_index()
        data.setdefault("branches", []).append({
            "id": new_id,
            "name": name,
            "parent_id": src_id,
            "source_id": src_id,
            "path": dst_path,
            "at_seq": at_seq,
            # 前缀指纹（v2.4.15）：体检据此核对"前 at_seq 行是否仍是 fork 当时的产物"
            "prefix_fp": prefix_fp,
            "created_at": src.created_at,
            "artifact_bytes": n_bytes,
            "artifact_lines": n_lines,
        })
        self._write_index(data)

    def unregister_branch(self, new_id: str) -> None:
        """撤销注册副作用：两个库的行 + 旁路索引条目。"""
        for db in (self.STATE_DB, self.HISTORY_DB):
            if not os.path.exists(db):
                continue
            try:
                con = self._connect(db)
                if os.path.basename(db) == STATE_DB_NAME:
                    con.execute("DELETE FROM threads WHERE id=?", (new_id,))
                else:
                    con.execute(
                        "DELETE FROM thread_history_projection_state WHERE thread_id=?",
                        (new_id,))
                con.commit()
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

    def _read_index(self) -> dict:
        if os.path.exists(self.LINEAGE_PATH):
            try:
                with open(self.LINEAGE_PATH, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"branches": []}

    def _write_index(self, data: dict) -> None:
        os.makedirs(os.path.dirname(self.LINEAGE_PATH), exist_ok=True)
        with open(self.LINEAGE_PATH, "w", encoding="utf-8") as f:
            f.write(dumps_safe(data, indent=2))

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
        return True  # 分支在旁路索引里显式记录，不靠标题启发式

    # ------------------------------------------------------------------
    # E/F. 体检与枚举
    # ------------------------------------------------------------------
    def storage_root(self) -> str:
        return self.SESSIONS_DIR

    def list_all_sessions(self) -> list[tuple[str, str]]:
        """必须覆盖基类默认实现：文件名是 `rollout-<ISO>-<uuid>.jsonl`。"""
        seen = {}
        for path, sid in self._iter_rollouts():
            seen.setdefault(sid, path)
        return [(p, s) for s, p in seen.items()]

    def sort_key(self, ref: str) -> float:
        try:
            return os.path.getmtime(ref)
        except OSError:
            return 0.0

    def verify_storage(self) -> list[VerifyItem]:
        items = []
        home_ok = os.path.isdir(self.CODEX_HOME)
        n_thr = 0
        n_roll = 0
        try:
            n_thr = len(self._thread_rows())
        except Exception:
            pass
        try:
            n_roll = len(list(self._iter_rollouts()))
        except Exception:
            pass
        items.append(VerifyItem(
            "Codex home", "L2" if n_roll else "L1", home_ok,
            f"{self.CODEX_HOME}（{n_roll} 个 rollout / {n_thr} 个 threads 行）" if home_ok
            else f"缺失：{self.CODEX_HOME}（设 CODEX_HOME 或先跑一次 codex）",
        ))
        items.append(VerifyItem(
            "转录布局 sessions/YYYY/MM/DD/rollout-<ISO>-<uuid>.jsonl",
            "L2" if n_roll else "L1", n_roll > 0,
            "三层日期嵌套；**文件名尾缀 == 会话 id**（故不能用 fn[:-6] 取 id）",
        ))
        items.append(VerifyItem(
            "线程索引 state_5.sqlite → threads.rollout_path",
            "L2" if n_thr else "L1", n_thr > 0,
            "NOT NULL 且必须指向 $CODEX_HOME 内的绝对路径"
            "（实测：指向外部时 codex 直接拒绝 fork，code -32600）",
        ))
        items.append(VerifyItem(
            "投影游标 thread_history_1.sqlite → thread_history_projection_state",
            "L1", os.path.exists(self.HISTORY_DB),
            "分支写入 (thread_id, 0, 0) = 尚未消费；派生状态交由产品重建",
        ))
        items.append(VerifyItem(
            "ordinal 顶层键契约",
            "L1", True,
            "session_meta=0 起逐行 +1；分叉时**续接源计数**（原生实测：源 12 行 → 分支 12..21）",
        ))
        items.append(VerifyItem(
            "thread_spawn_edges / session_index.jsonl",
            "L1", True,
            "原生分叉实测**都不写**（前者恒 0 行、后者行数不变）→ 本适配器同样不写",
        ))
        return items

    # ------------------------------------------------------------------
    # G. 面向用户的文案
    # ------------------------------------------------------------------
    def activation_hint(self) -> str:
        return (
            "Codex 侧已写 2 层索引 + 1 个转录：\n"
            "            ① `codex exec resume <新 id> \"…\"` 可直接续跑（非交互，按 UUID 精确定位）\n"
            "            ② 桌面版会话列表非实时刷新，重启可见（macOS ⌘Q / Windows 托盘退出）\n"
            "            ③ 想让它被 `codex fork --last` 选中：用 `codex exec resume` 跑一轮即可"
        )

    def produce_hint(self) -> str:
        return (
            "跑一次零密钥会话：`codex exec --oss --local-provider ollama "
            "-m qwen2.5:3b \"hi\"`（先 export CODEX_HOME=<隔离目录>）"
        )

    def backups_dir(self) -> str:
        # 备份进 Codex 自己的 home，不污染别家目录；FORK_BACKUP_DIR 可整体覆盖
        return self._backups_root(os.path.join(self.CODEX_HOME, BACKUPS_DIR_NAME))

    def publish_hint(self) -> str:
        return ""

    def backup_note(self) -> str:
        return "源 rollout 文件 + state_5.sqlite + thread_history_1.sqlite（三个文件的一致性快照）"

    def readonly_hint(self, dst_ref: str) -> str:
        return (
            "分支转录未锁定只读（**本技能不会替你修改文件权限**）。如需防止 Codex 继续追加消息，"
            f"可由你自己把该文件设为只读——（用你系统的方式把该文件设为只读）{dst_ref}"
        )
