# role: adapter:openclaw（JSONL 后端）— 产品适配器，不含引擎逻辑
"""fork_core.adapter_openclaw — OpenClaw 适配器（pi 血缘 + 产品索引）。

一手依据（2026-09-14 真机取证，非推测，可复跑核对）：

  1. 真机安装 `openclaw@2026.6.35`（dist-tag `extended-stable`），
     `OPENCLAW_STATE_DIR=<隔离目录> openclaw onboard --non-interactive
     --auth-choice ollama --custom-base-url http://127.0.0.1:11434
     --custom-model-id qwen2.5:3b --accept-risk`
     → `openclaw agent --local --session-key agent:main:<k> --message ...`
     产出真实会话（含 model_change / thinking_level_change / compaction 条目）。
  2. 官方解析器回验：`dist/session-manager-*.js` 导出的
     `loadEntriesFromFile` / `buildSessionContext` / `parseSessionEntries`
     （打包后导出名为单字母，需按键位对齐）能正确解析本适配器产物。
  3. 官方 CLI 回验：`openclaw sessions --json` 能列出分支。

存储契约（= pi 的文件格式 + OpenClaw 的目录布局与索引）：

  目录     <state_dir>/agents/<agent_id>/sessions/     ← 平铺，无 --cwd-- 子目录
           state_dir 默认 ~/.openclaw（OPENCLAW_STATE_DIR 可覆盖；--dev profile 是 ~/.openclaw-dev）
           agent_id 默认 main（OPENCLAW_AGENT_ID 可覆盖）
  文件名   <header.id>.jsonl        ← 与 pi 不同：无时间戳前缀，文件名 = 会话 id
  首行     {"type":"session","version":3,"id":<uuid>,"timestamp":ISO,
            "cwd":...,"parentSession"?:<上游会话文件绝对路径>}
  条目     {"type":...,"id":<8 位 hex>,"parentId":...} → append-only 树（与 pi 同契约）
  索引     <sessions_dir>/sessions.json
           { "<session_key>": {sessionId, sessionFile, updatedAt, sessionStartedAt,
             lastInteractionAt, contextTokens, modelProvider, model, agentHarnessId,
             abortedLastRun, compactionCount, ...} }
           session_key 形如 "agent:<agent_id>:<key>"

⚠️ 与 pi 的两处硬差异（勿"顺手统一"）：

  ① **必须有产品索引才可见**。实测：只把合法 `<new_id>.jsonl` 放进 sessions/，
     `openclaw sessions --json` **只列出 1 条**（源会话）——OpenClaw 不靠文件发现会话，
     `sessions.json` 才是权威索引。写入索引后立刻变为 2 条。
     故本适配器在登记时**同时**写旁路谱系索引与 OpenClaw 的 sessions.json
     （与 pi 只写旁路索引不同）。这是"产物必须被产品认"的硬要求，不是可选装饰。

  ② **trajectory.jsonl 干扰**。同目录还有 `<id>.trajectory.jsonl`（另一套 schema：
     首行 traceSchema="openclaw-trajectory"、type="session.started"），
     它不是会话转录。虽然其首行 `type != "session"` 恰好被 header 判据挡掉，
     仍显式排除 `*.trajectory.jsonl`——不依赖"恰好"。

已知能力边界（如实记录，未实现）：
  - 不覆盖 ≥2026.9.x 的 SQLite 运行时（转录迁入
    `agents/<id>/agent/openclaw-agent.sqlite` 的 transcript_events 表）。
    本适配器覆盖的是 ≤2026.6.x（实测 2026.6.35，该版 SQLite 只有 auth/memory
    等 9 张表，无 transcript_events）。
  - 不回写 header.parentSession：引擎没有"产物 header 定制"钩子，
    而 register_branch 发生在 verify 之后（回写会改动已校验文件）。
    OpenClaw 原生 fork 用 parentSession 记谱系，本适配器的谱系记在旁路索引 +
    sessions.json 的 sessionFile 指针上，原生字段保持原值。
  - 若 Gateway 正在运行，它可能持有 sessions.json 的内存副本；
    写入后需重启 Gateway 才可见（见 activation_hint）。
"""

from __future__ import annotations

import json
import os
import shutil
import time
import uuid

from .adapter_base import dumps_safe
from .adapter_pi import PiAdapter, LINEAGE_NAME
from .models import SessionMeta, VerifyItem

HOME = os.path.expanduser("~")
DEFAULT_STATE_DIR = os.path.join(HOME, ".openclaw")
DEFAULT_AGENT_ID = "main"
SESSIONS_DIR_NAME = "sessions"
SESSIONS_INDEX_NAME = "sessions.json"

# 非转录文件（同目录干扰项），显式排除
_IGNORED_SUFFIXES = (".trajectory.jsonl",)

# 分支在 OpenClaw 索引里的 key 前缀（生成 "agent:<agent_id>:fork-<8位>"）
BRANCH_KEY_PREFIX = "fork-"


class OpenClawJsonlAdapter(PiAdapter):
    """OpenClaw ≤2026.6.x（JSONL 运行时）适配器。

    格式层完全复用 PiAdapter（同一 append-only 树契约），
    只覆盖：路径布局 / 会话枚举 / 产品索引注册 / 文案 / 体检。
    """

    name = "openclaw"

    def __init__(self):
        self.STATE_DIR = os.environ.get("OPENCLAW_STATE_DIR") or DEFAULT_STATE_DIR
        self.AGENT_ID = os.environ.get("OPENCLAW_AGENT_ID") or DEFAULT_AGENT_ID
        # pi 侧字段（供继承来的方法使用）
        self.AGENT_DIR = os.path.join(self.STATE_DIR, "agents", self.AGENT_ID)
        self.SESSIONS_DIR = os.path.join(self.AGENT_DIR, SESSIONS_DIR_NAME)
        self.LINEAGE_PATH = os.path.join(self.AGENT_DIR, LINEAGE_NAME)
        self.SESSIONS_INDEX = os.path.join(self.SESSIONS_DIR, SESSIONS_INDEX_NAME)

    # ------------------------------------------------------------------
    # 内部：会话枚举（平铺 + 排除 trajectory）
    # ------------------------------------------------------------------
    def _iter_session_files(self):
        root = self.SESSIONS_DIR
        if not os.path.isdir(root):
            return
        for fn in sorted(os.listdir(root)):
            if not fn.endswith(".jsonl"):
                continue
            if fn.endswith(_IGNORED_SUFFIXES):
                continue
            yield os.path.join(root, fn)

    def _session_key_for(self, new_id: str) -> str:
        return f"fork-{new_id[:8]}"

    def _full_key(self, new_id: str) -> str:
        return f"agent:{self.AGENT_ID}:{self._session_key_for(new_id)}"

    # ------------------------------------------------------------------
    # D. 注册与查询（旁路谱系索引 + OpenClaw 原生 sessions.json）
    # ------------------------------------------------------------------
    def _read_sessions_index(self) -> dict:
        if not os.path.exists(self.SESSIONS_INDEX):
            return {}
        try:
            with open(self.SESSIONS_INDEX, encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _write_sessions_index(self, data: dict) -> None:
        """原子写：tmp + replace。先备份到 backups_dir。"""
        os.makedirs(self.SESSIONS_DIR, exist_ok=True)
        if os.path.exists(self.SESSIONS_INDEX):
            try:
                os.makedirs(self.backups_dir(), exist_ok=True)
                shutil.copy2(
                    self.SESSIONS_INDEX,
                    os.path.join(
                        self.backups_dir(),
                        f"sessions.json.bak.{time.strftime('%Y%m%d-%H%M%S')}",
                    ),
                )
            except Exception:
                pass
        tmp = f"{self.SESSIONS_INDEX}.{os.getpid()}.{uuid.uuid4().hex[:6]}.tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(dumps_safe(data, indent=2))
        os.replace(tmp, self.SESSIONS_INDEX)

    def _src_index_entry(self, src_id: str) -> dict | None:
        """从 sessions.json 里找出指向源会话的条目（作为分支条目的字段模板）。"""
        for v in self._read_sessions_index().values():
            if isinstance(v, dict) and v.get("sessionId") == src_id:
                return v
        return None

    def register_branch(self, src, new_id, dst_path, name, parent_id=None, at_seq=None,
                        prefix_fp=None) -> None:
        """写两处索引，顺序：OpenClaw 原生索引 → 旁路谱系索引。

        先写产品索引：万一失败，旁路索引尚未写入，引擎的 unregister 兜底更干净；
        反之若先写旁路再写产品失败，旁路里会留下一个"产品看不见"的分支。
        """
        key = self._full_key(new_id)
        now_ms = int(time.time() * 1000)
        index = self._read_sessions_index()
        template = self._src_index_entry(src.id) or {}
        entry = dict(template)
        # 与源会话绑定的运行期报告不含分支语义，且内嵌源 sessionId —— 丢弃
        entry.pop("systemPromptReport", None)
        entry.pop("contextBudgetStatus", None)
        entry.update(
            {
                "sessionId": new_id,
                "sessionFile": dst_path,
                "updatedAt": now_ms,
                "sessionStartedAt": now_ms,
                "lastInteractionAt": now_ms,
                "agentHarnessId": entry.get("agentHarnessId") or "openclaw",
                "abortedLastRun": False,
                "compactionCount": 0,
            }
        )
        index[key] = entry
        self._write_sessions_index(index)
        # 旁路谱系索引（继承 pi 的实现）
        super().register_branch(src, new_id, dst_path, name, parent_id=parent_id,
                                at_seq=at_seq, prefix_fp=prefix_fp)

    def unregister_branch(self, new_id: str) -> None:
        # 先清旁路，再清产品索引
        super().unregister_branch(new_id)
        try:
            index = self._read_sessions_index()
            key = self._full_key(new_id)
            if key in index:
                index.pop(key)
                self._write_sessions_index(index)
                return
            # 兜底：按 sessionId 匹配（key 可能被用户改过）
            hit = [k for k, v in index.items() if isinstance(v, dict) and v.get("sessionId") == new_id]
            if hit:
                for k in hit:
                    index.pop(k)
                self._write_sessions_index(index)
        except Exception:
            pass

    def load_session_meta(self, session_id: str) -> SessionMeta | None:
        meta = super().load_session_meta(session_id)
        if meta is None:
            return None
        return meta

    # ------------------------------------------------------------------
    # E. 体检（路径与判据按 OpenClaw 口径）
    # ------------------------------------------------------------------
    def storage_root(self) -> str:
        return self.SESSIONS_DIR

    def verify_storage(self) -> list[VerifyItem]:
        n = 0
        ok = os.path.isdir(self.SESSIONS_DIR)
        if ok:
            for p in self._iter_session_files():
                if self._read_header(p):
                    n += 1
        index_ok = os.path.exists(self.SESSIONS_INDEX)
        indexed = len(self._read_sessions_index()) if index_ok else 0
        level = "L2" if n else "L1"
        return [
            VerifyItem(
                "OpenClaw transcript 目录",
                level,
                ok,
                f"{self.SESSIONS_DIR}（{n} 个合法会话）"
                if ok
                else f"缺失：{self.SESSIONS_DIR}（先跑 `openclaw agent` 产生会话，或设 OPENCLAW_STATE_DIR）",
            ),
            VerifyItem(
                "OpenClaw 会话索引 sessions.json",
                "L2" if indexed else "L1",
                index_ok,
                f"{self.SESSIONS_INDEX}（{indexed} 条登记）"
                if index_ok
                else f"缺失：{self.SESSIONS_INDEX}（分支不会被 OpenClaw 列出）",
            ),
            VerifyItem(
                "原生谱系字段",
                "L1",
                True,
                "header.parentSession 由 OpenClaw 原生维护，本适配器只读不写（_RAW_KEYS 保护）；"
                "本适配器的谱系落在 sessions.json 的 sessionFile 指针 + 旁路索引",
            ),
        ]

    # ------------------------------------------------------------------
    # G. 面向用户的文案与路径
    # ------------------------------------------------------------------
    def activation_hint(self) -> str:
        return (
            "OpenClaw 分支已写入 sessions.json：`openclaw sessions --json` 立即可列出"
            "（session key 形如 agent:%s:fork-xxxxxxxx）。"
            "若 Gateway 正在运行，重启一次以加载新会话。" % self.AGENT_ID
        )

    def produce_hint(self) -> str:
        return (
            "跑一次 OpenClaw（如 `openclaw agent --local --session-key agent:%s:demo "
            "--message 'hi'`），转录会存到 %s" % (self.AGENT_ID, self.SESSIONS_DIR)
        )

    def backups_dir(self) -> str:
        return self._backups_root(os.path.join(self.AGENT_DIR, "fork-backups"))


# 兼容别名：旧代码/测试里用的名字。
# 实际选择后端请用 adapters.get_adapter("openclaw")（自动探测介质）。
OpenClawAdapter = OpenClawJsonlAdapter
