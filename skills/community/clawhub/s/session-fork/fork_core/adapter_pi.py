# role: adapter:pi — 产品适配器，不含引擎逻辑
"""fork_core.adapter_pi — pi / OpenClaw 谱系适配器。

一手依据（2026-09-14 取证，非推测）：
  1. pi 官方格式文档  @mariozechner/pi-coding-agent@0.73.1  docs/session-format.md
  2. pi 官方实现     同包 dist/core/session-manager.js（0.73.1，1108 行）
  3. 上游产品文档    OpenClaw  docs.openclaw.ai/reference/session-management-compaction

存储契约（与 WorkBuddy 的关键差异见下）：

  目录     <agent_dir>/sessions/--<cwd 转义>--/
           cwd 转义 = 去掉前导 /，再把 / \\ : 换成 -
           agent_dir 默认 ~/.pi/agent（可用环境变量 PI_AGENT_DIR 覆盖）
  文件名   <ISO 时间戳，: 和 . 换成 ->_<header.id>.jsonl
           ⚠️ 文件名 ≠ 会话 id（WorkBuddy 是 <session-id>.jsonl，这点不同）
  首行     {"type":"session","version":3,"id":<uuid>,"timestamp":ISO,
            "cwd":..., "parentSession"?:<上游会话文件绝对路径>}
           官方校验只有两条（loadEntriesFromFile / isValidSessionFile）：
             ① 文件扩展名 .jsonl；② 首行 type=="session" 且 id 是 string
           ——发现会话**不看文件名格式**，所以引擎产出的 <uuid>.jsonl 能被官方列出。
  条目     {"type":<...>,"id":<8 位 hex>,"parentId":<父条目 id|null>,
            "timestamp":ISO, ...}  → 构成一棵 append-only 树
           条目类型：message / model_change / thinking_level_change / compaction /
                    branch_summary / custom / custom_message / label / session_info
  消息行   entry.type=="message"，正文在 entry.message：
             {role:user|assistant|toolResult|bashExecution|custom|...,
              content: string | [{type:text|thinking|image|toolCall,...}]}

本适配器相对 WorkBuddy 适配器的三处关键差异（都是硬约束，勿"顺手统一"）：

  ① 会话 id 不按文件名找：必须读首行 header 的 id 字段。
  ② **不改写条目 id**：条目 id 是树结构的边（parentId 指向它），
     替换会直接剪断整棵树。源会话 id（完整 UUID）在 pi 里只出现在
     header.id 上，所以只改 header 一行即可，天然零残留。
     官方 createBranchedSession() 同样保留条目 id 原样
     （session-manager.js:`const pathWithoutLabels = path.filter(...)` 后直接
      `this.fileEntries = [header, ...pathWithoutLabels, ...labelEntries]`）。
  ③ **parentSession 是谱系指针，不是待替换的 id**：它是源会话文件的绝对路径
     （可能含源 session id）。若不保护，引擎的残留检查会判它"源 id 残留"，
     而更糟的是把谱系指向一个不存在的路径。故列入 _RAW_KEYS。

已知能力边界（如实记录，未实现）：
  - 不做"树路径抽取"：引擎的截断是 `lines[:cut]`（前缀），而官方
    createBranchedSession 走的是 root→leaf 路径。对线性会话两者等价；
    对已分叉过的会话，前缀会带上被放弃的旁路条目（详见验证报告）。
  - 不回写原生 parentSession：引擎没有"产物 header 定制"钩子，
    register_branch 又发生在 verify 之后（回写会改动已校验的文件）。
    故谱系记在旁路索引（与 Claude adapter 同构），原生字段保持原值。
  - OpenClaw 现代版把转录迁进了 SQLite（每 Agent 一个
    openclaw-agent.sqlite），JSONL 降级为导出格式。本适配器覆盖的是
    pi 原生文件后端与 OpenClaw 的 legacy/export 通道，不覆盖 SQLite 运行时。
"""

from __future__ import annotations

import json
import os

from .models import SessionMeta, VerifyItem
from .adapter_base import TranscriptionAdapter, dumps_safe, read_jsonl_file

HOME = os.path.expanduser("~")
# 默认 ~/.pi/agent；OpenClaw 的 legacy 转录在 ~/.openclaw/agents/<agentId>/sessions/，
# 可用 PI_AGENT_DIR 指过去做离线维护（但那不是官方支持的运行时路径）。
AGENT_DIR = os.environ.get("PI_AGENT_DIR") or os.path.join(HOME, ".pi", "agent")
SESSIONS_DIR_NAME = "sessions"
LINEAGE_NAME = "fork.branches.json"

# 原始内容键：这些字段保留源 id 是合法设计，不参与替换、不报残留
#
#  - parentSession：谱系指针（上游会话文件路径，可能含源 id）。必须保持原值，
#    否则谱系会指向不存在的路径。
#  - content：**对话正文**。pi 的会话 id 不在条目里，正文中出现源 id 只是对话内容
#    （用户可能贴了会话 id、工具输出里可能回显）。官方 createBranchedSession 同样
#    原样保留正文。若不列入黑名单，`verify_branch` 的残留检查会把正文命中判成
#    "分支污染"而**误拒分支**（2026-09-14 复核实测复现：errs=['L2.message.content']）。
#    真正的会话关联字段仍由引擎的结构性硬查兜底（`_find_structural_residue` 查
#    `sessionId`/`session_id`，不受本黑名单影响）。
_RAW_KEYS = {"parentSession", "content"}


class PiAdapter(TranscriptionAdapter):
    name = "pi"

    def __init__(self):
        # 实例化时快照模块级路径（引擎用 getattr 取实例属性；测试可隔离）
        self.AGENT_DIR = AGENT_DIR
        self.SESSIONS_DIR = os.path.join(AGENT_DIR, SESSIONS_DIR_NAME)
        self.LINEAGE_PATH = os.path.join(AGENT_DIR, LINEAGE_NAME)

    _RAW_KEYS = _RAW_KEYS

    # ------------------------------------------------------------------
    # 内部：会话发现（官方判据：.jsonl 扩展名 + 首行 type/id）
    # ------------------------------------------------------------------
    def _iter_session_files(self):
        """遍历所有 <agent_dir>/sessions/<--cwd-->/<timestamp>_<id>.jsonl。"""
        root = self.SESSIONS_DIR
        if not os.path.isdir(root):
            return
        for slug in sorted(os.listdir(root)):
            d = os.path.join(root, slug)
            if not os.path.isdir(d):
                continue
            for fn in sorted(os.listdir(d)):
                if fn.endswith(".jsonl"):
                    yield os.path.join(d, fn)

    @staticmethod
    def _read_header(path: str) -> dict | None:
        """读首行 header；官方 is_valid_session_file 判据（type=="session" 且 id 为 str）。"""
        try:
            with open(path, encoding="utf-8") as f:
                first = f.readline()
            if not first.strip():
                return None
            h = json.loads(first)
        except Exception:
            return None
        if not isinstance(h, dict) or h.get("type") != "session":
            return None
        if not isinstance(h.get("id"), str) or not h["id"]:
            return None
        return h

    def _find_by_header_id(self, session_id: str) -> str | None:
        for path in self._iter_session_files():
            h = self._read_header(path)
            if h and h.get("id") == session_id:
                return path
        return None

    # ------------------------------------------------------------------
    # A. 定位
    # ------------------------------------------------------------------
    def resolve_session(self, session_ref: str) -> str:
        if session_ref != "current":
            return session_ref
        # pi 无全局 "working" 概念：取最近修改的合法会话（官方 findMostRecentSession 同策略）
        newest, newest_ts = None, -1.0
        for path in self._iter_session_files():
            if not self._read_header(path):
                continue
            ts = os.path.getmtime(path)
            if ts > newest_ts:
                h = self._read_header(path)
                newest, newest_ts = h["id"], ts
        if not newest:
            raise SystemExit(
                "No pi session found under %s（先跑 `pi` 产生会话，或用 PI_AGENT_DIR 指向别处）"
                % self.SESSIONS_DIR
            )
        return newest

    def find_transcript(self, session_id: str) -> tuple[str | None, str | None]:
        # 安全校验：session id 只允许文件名字符（虽不直接拼路径，仍拒绝穿越意图）
        if not session_id or "/" in session_id or "\\" in session_id or session_id in (".", ".."):
            return None, None
        path = self._find_by_header_id(session_id)
        if not path:
            return None, None
        # 兜底：realpath 必须仍在 SESSIONS_DIR 内
        try:
            if os.path.realpath(path).startswith(os.path.realpath(self.SESSIONS_DIR) + os.sep):
                return path, os.path.basename(os.path.dirname(path))
        except Exception:
            pass
        return None, None

    def find_session_by_request_id(self, request_id: str) -> str | None:
        """按**条目 id** 反查所属会话（pi 里最接近"UI 请求标识"的是 /tree 的条目 id）。

        收集全部命中，优先返回**非分支**（源会话），理由与 WorkBuddy adapter 一致：
        分支会继承被复制的条目 id，否则会把定位解析到后代分支。
        """
        hits = []
        for path in self._iter_session_files():
            h = self._read_header(path)
            if not h:
                continue
            try:
                with open(path, encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or request_id not in line:
                            continue
                        try:
                            o = json.loads(line)
                        except Exception:
                            continue
                        if o.get("type") == "message" and o.get("id") == request_id:
                            hits.append((h["id"], path, os.path.getmtime(path)))
                            break
            except Exception:
                continue
        if not hits:
            return None
        branched = {b.get("id") for b in self._read_index().get("branches", [])}
        hits.sort(key=lambda t: (t[0] in branched, -t[2]))  # 非分支优先，其次最新
        return hits[0][0]

    # ------------------------------------------------------------------
    # B. 消息判定
    # ------------------------------------------------------------------
    @staticmethod
    def _msg(o: dict) -> dict:
        m = o.get("message")
        return m if isinstance(m, dict) else {}

    def is_user_message(self, obj: dict) -> bool:
        return obj.get("type") == "message" and self._msg(obj).get("role") == "user"

    def is_assistant_message(self, obj: dict) -> bool:
        return obj.get("type") == "message" and self._msg(obj).get("role") == "assistant"

    def get_text(self, obj: dict) -> str:
        """提取文本块。content 可为 str（用户消息）或块数组（助手消息含 thinking/toolCall）。"""
        if obj.get("type") != "message":
            return ""
        role = self._msg(obj).get("role")
        if role not in ("user", "assistant", "toolResult", "custom"):
            return ""
        content = self._msg(obj).get("content")
        if isinstance(content, str):
            return content
        if not isinstance(content, list):
            return ""
        parts = []
        for c in content:
            if isinstance(c, dict) and c.get("type") == "text" and isinstance(c.get("text"), str):
                parts.append(c["text"])
        return "\n".join(parts)

    def get_request_id(self, obj: dict) -> str | None:
        # pi 无 conversationRequestId；**消息条目**的 id 是等价的精确锚点。
        # ⚠️ 必须限定 type=="message"：header 也有 id 字段，但那是会话 id，
        # 不是可定位的条目锚点（2026-09-14 测试抓出）。
        if obj.get("type") != "message":
            return None
        rid = obj.get("id")
        return rid if isinstance(rid, str) else None

    # ------------------------------------------------------------------
    # C. 读写
    # ------------------------------------------------------------------
    def read_lines(self, path: str) -> list[dict]:
        # 坏行跳过（不抛）：读取方不该因为一行坏掉就整轮崩；
        # 需要坏行行号时走 read_lines_checked（见 adapter_base.parse_jsonl 的说明）。
        return read_jsonl_file(path).objs

    def write_branch(self, path: str, lines: list[dict]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(dumps_safe(o) for o in lines) + "\n")

    def rewrite_ids(self, lines: list[dict], old_id: str, new_id: str) -> tuple[list[dict], int]:
        """只改 header.id；条目 id 原样保留（改动它会剪断 parentId 树）。

        - 源会话 id 在 pi 里只出现在首行 header.id（条目 id 是 8 位 hex，与 UUID 不同形），
          因此"只改 header"即等价于全量替换，且零误伤。
        - parentSession 列入 _RAW_KEYS，不替换（它是谱系指针，必须保持指向真实上游）。
        - 若 header 缺失（异常文件），退化为全量递归替换以兜底，但条目 id 仍受保护。
        """
        replacements = 0
        header_seen = False

        def walk(node):
            nonlocal replacements
            if isinstance(node, str):
                if old_id in node:
                    replacements += 1
                    return node.replace(old_id, new_id)
                return node
            if isinstance(node, dict):
                out = {}
                for k, v in node.items():
                    out[k] = v if k in _RAW_KEYS else walk(v)
                return out
            if isinstance(node, list):
                return [walk(v) for v in node]
            return node

        out_lines = []
        for o in lines:
            if isinstance(o, dict) and o.get("type") == "session":
                header_seen = True
                new_o = dict(o)
                if new_o.get("id") == old_id:
                    new_o["id"] = new_id
                    replacements += 1
                elif isinstance(new_o.get("id"), str) and old_id in new_o["id"]:
                    new_o["id"] = new_o["id"].replace(old_id, new_id)
                    replacements += 1
                # 其余 header 字段保持（version / cwd / parentSession / timestamp）
                out_lines.append(new_o)
            else:
                out_lines.append(o)

        if not header_seen:
            # 异常文件（无 header）：条目 id 仍是树边，不动；仅递归处理其余字段
            out_lines, replacements = [walk(o) for o in lines], replacements
        return out_lines, replacements

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

    # ------------------------------------------------------------------
    # D. 注册与查询（旁路索引；不污染 pi 官方存储）
    # ------------------------------------------------------------------
    def load_session_meta(self, session_id: str) -> SessionMeta | None:
        path = self._find_by_header_id(session_id)
        if not path:
            return None
        h = self._read_header(path) or {}
        meta = SessionMeta(
            id=session_id,
            title="",
            status="",
            created_at=os.path.getmtime(path),
            cwd=h.get("cwd") or "",
        )
        parent = h.get("parentSession")
        if isinstance(parent, str) and parent:
            # 原生谱系：上游会话文件路径 → 反查其 id，供 --list --tree 展示
            ph = self._read_header(parent)
            if ph and isinstance(ph.get("id"), str):
                meta.parent_id = ph["id"]
        return meta

    def _read_index(self) -> dict:
        if os.path.exists(self.LINEAGE_PATH):
            try:
                with open(self.LINEAGE_PATH, encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"branches": []}

    def _write_index(self, data: dict) -> None:
        os.makedirs(self.AGENT_DIR, exist_ok=True)
        with open(self.LINEAGE_PATH, "w", encoding="utf-8") as f:
            f.write(dumps_safe(data, indent=2))

    def register_branch(self, src, new_id, dst_path, name, parent_id=None, at_seq=None,
                        prefix_fp=None) -> None:
        data = self._read_index()
        data.setdefault("branches", []).append(
            {
                "id": new_id,
                "name": name,
                "parent_id": parent_id or src.id,
                "source_id": src.id,
                "path": dst_path,
                "at_seq": at_seq,
                # 前缀指纹（v2.4.15）：体检据此核对"前 at_seq 行是否仍是 fork 当时的产物"
                "prefix_fp": prefix_fp,
                "created_at": src.created_at,
            }
        )
        self._write_index(data)

    def unregister_branch(self, new_id: str) -> None:
        try:
            data = self._read_index()
            branches = [b for b in data.get("branches", []) if b.get("id") != new_id]
            if len(branches) != len(data.get("branches", [])):
                data["branches"] = branches
                self._write_index(data)
        except Exception:
            pass

    def list_branches(self, cwd: str | None = None) -> list[SessionMeta]:
        out = []
        for b in self._read_index().get("branches", []):
            out.append(
                SessionMeta(
                    id=b.get("id", ""),
                    title=b.get("name", ""),
                    status="",
                    created_at=b.get("created_at"),
                    cwd=cwd or "",
                    parent_id=b.get("parent_id", ""),
                )
            )
        return out

    def is_branch_name(self, title: str) -> bool:
        return True  # 分支在旁路索引里显式记录，不需标题启发式

    # ------------------------------------------------------------------
    # E. 体检与枚举
    # ------------------------------------------------------------------
    def storage_root(self) -> str:
        """存储根目录（sessions 下按 --cwd-- 分子目录）。"""
        return self.SESSIONS_DIR

    def list_all_sessions(self) -> list[tuple[str, str]]:
        """枚举全部会话 → [(path, header.id)]。

        必须覆盖基类默认实现：pi 的文件名含时间戳前缀，会话 id 在首行 header 里
        （`<ISO 时间戳>_<header.id>.jsonl`）。
        """
        out = []
        for path in self._iter_session_files():
            h = self._read_header(path)
            if h:
                out.append((path, h["id"]))
        return out

    # ------------------------------------------------------------------
    # G. 面向用户的文案与路径（覆盖基类的 WorkBuddy 默认口径）
    # ------------------------------------------------------------------
    def activation_hint(self) -> str:
        return "pi 无需重启：在会话选择器（/resume）或 /tree 里刷新即可看到新会话"

    def produce_hint(self) -> str:
        return "在本机跑一次 pi（pi 会把会话自动存到 ~/.pi/agent/sessions/）"

    def backups_dir(self) -> str:
        return self._backups_root(os.path.join(self.AGENT_DIR, "fork-backups"))

    def verify_storage(self) -> list[VerifyItem]:
        n = 0
        ok = os.path.isdir(self.SESSIONS_DIR)
        if ok:
            for p in self._iter_session_files():
                if self._read_header(p):
                    n += 1
        level = "L2" if n else "L1"
        return [
            VerifyItem(
                "pi transcript 目录",
                level,
                ok,
                f"{self.SESSIONS_DIR}（{n} 个合法会话）"
                if ok
                else f"缺失：{self.SESSIONS_DIR}（先跑 pi 产生会话，或设 PI_AGENT_DIR）",
            ),
            VerifyItem(
                "原生谱系字段",
                "L1",
                True,
                "header.parentSession 由 pi 官方维护，本适配器只读不写（_RAW_KEYS 保护）",
            ),
        ]
