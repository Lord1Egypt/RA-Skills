#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta_logs.py — YottaMeta 元史（yotta-logs）：跨智能体历史会话 / 记忆日志检索引擎。

v0.2.0 通用化：不再只认 JSONL，按「格式族 × 字段别名归一 + 配置兜底」适配
JSONL / 单文件 JSON / SQLite / Markdown / 二进制 五大格式族；discover 全源登记；
新增 --source / --kind / --format 过滤；默认检索范围 = 会话源 + 结构化记忆源开、
自由笔记 / 二进制日志默认关（可显式开）。格式普查见 references/agent-formats.md。

零依赖（Python 3.8+ 标准库），只读检索 / 分析，不修改、不删除、不联网上传。
与元忆（yotta-memory，语义记忆）互补：本技能只管原始日志 / 记忆文件的定位、
检索、提取与统计。

子命令（7 个语义不变）：
  locate                 全源登记（来源 / 格式 / 类型 / 路径 / 默认范围）
  scan   [--dir D]       列出所有会话（来源 / ID / 日期 / 消息数 / 大小）
  search <query> [--dir D]  跨源关键词 / 正则检索，输出时间线命中
  session <sid> [--dir D]   提取单个会话原文（时间线 + 角色 + 文本）
  stats  [--dir D]       统计（消息 / token / 成本 / 每日汇总 / 分源）
  tools  [--dir D]       工具调用次数排行
  version                打印版本

通用选项：
  --dir PATH      日志 / 记忆目录或文件（目录自动嗅探格式族；缺省读
                  YOTTA_LOGS_DIR，再 discover 全源登记）
  --source NAME   只检索指定来源（可多次；名称见 locate 登记）
  --kind KIND     只检索指定类型：session / memory / note / log
  --format FMT    只检索指定格式：jsonl / json / sqlite / markdown / binary
  --json          输出纯 JSON（stdout 无其它噪音）
  --no-redact     关闭默认脱敏
  --limit N       最多返回 N 条（默认 50）

退出码（与元安 / 元审 / 元盾 / 元真家族一致）：
  0 = 成功（检索到结果 / 操作完成）
  1 = 无匹配 / 空结果集（search 未命中、scan / stats 无会话）
  4 = 用法错误 / 路径不存在 / 致命异常

用法示例：
  python3 yotta_logs.py locate
  python3 yotta_logs.py scan --dir ~/.clawdbot/agents/dashu/sessions
  python3 yotta_logs.py search "部署方案"
  python3 yotta_logs.py search "CI 失败" --regex --date 2026-08-26 --source opencode-db
  python3 yotta_logs.py search "记住" --kind memory
  python3 yotta_logs.py session abc123 --role assistant
  python3 yotta_logs.py stats --dir /path/to/sessions --daily
  python3 yotta_logs.py tools --dir /path/to/logs --format sqlite
"""
import argparse
import datetime as _dt
import glob
import json
import os
import re
import sqlite3
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

VERSION = "0.3.5"
TOOL_NAME = "yotta-logs"
TOOL_CN = "元史"
DEFAULT_LIMIT = 50
DEFAULT_CONTEXT = 40  # 命中上下文半径（字符）
JSONL_SUFFIXES = (".jsonl", ".jsonlines", ".ndjson")
JSON_SUFFIXES = (".json",)
SQLITE_SUFFIXES = (".db", ".sqlite", ".sqlite3", ".vscdb")
MD_SUFFIXES = (".md", ".markdown", ".mdown")
BINARY_SUFFIXES = (".pbtxt", ".nitrite", ".cascade", ".bin", ".enc")
ROLE_TOOL = ("tool", "toolResult", "tool_result", "toolCall", "tool_call",
             "function", "functionCall", "function_call")
KIND_CHOICES = ("session", "memory", "note", "log")
FORMAT_CHOICES = ("jsonl", "json", "sqlite", "markdown", "binary")

# 字段别名（按序取首个命中）——适配一切关键字段
TIME_ALIASES = ("timestamp", "time_created", "created", "time", "ts", "date",
                "created_at", "mtime", "updated")
ROLE_ALIASES = ("role", "type", "kind")
TEXT_ALIASES = ("text", "content", "body", "message", "statement",
                "text_content")
SESSION_ALIASES = ("session_id", "thread_id", "sessionId", "session",
                   "conversation_id", "threadId")
TITLE_ALIASES = ("title", "subject", "name", "heading")

# ── 脱敏（默认开启）──────────────────────────────────────────────────────

_URL_RE = re.compile(r"(https?://[^\s\"'<>]+)", re.I)
# v0.3.2：URL 内嵌凭据脱敏覆盖所有协议（不只是 http/https），并遮蔽查询串里的
# 凭据参数 —— 旧行为只处理 http(s)://user:pass@，`postgres://` / `?token=...` 会漏。
_URL_USERPASS_RE = re.compile(
    r"([a-z][a-z0-9+.\-]*://)([^/\s:@]*):([^/\s@]+)@", re.I)
_URL_SECRET_QUERY_RE = re.compile(
    r"(?i)([?&](?:token|api[_-]?key|apikey|access[_-]?token|auth|authorization|"
    r"password|passwd|pwd|secret|client[_-]?secret|session|sig|signature)=)"
    r"[^&\s\"'<>]+")
_KNOWN_KEY_RE = re.compile(
    r"(?i)\b("
    r"sk-[a-z0-9_-]{8,}"           # OpenAI 类 API key
    r"|rk-[a-z0-9_-]{8,}"
    r"|pk-[a-z0-9_-]{8,}"
    r"|gh[pousr]_[a-z0-9]{20,}"    # GitHub token
    r"|xox[baprs]-[a-z0-9-]{10,}"  # Slack token
    r"|AKIA[0-9A-Z]{16}"           # AWS access key
    r"|ASIA[0-9A-Z]{16}"
    r")\b")
_JWT_RE = re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}")
_BEARER_RE = re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/-]+")
_PEM_RE = re.compile(
    r"-----BEGIN [A-Z0-9 ]+ PRIVATE KEY-----.*?-----END [A-Z0-9 ]+ PRIVATE KEY-----",
    re.S)
_ASSIGN_RE = re.compile(
    r"(?i)\b(token|password|passwd|secret|api[_-]?key|access[_-]?key|"
    r"client[_-]?secret)\b\s*[=:]\s*[\"']?[a-z0-9._~+/\-]{6,}")
_LONG_TOKEN_RE = re.compile(r"[a-z0-9+/_-]{40,}", re.I)


def redact(text):
    """把疑似密钥 / token / 口令打码（默认开启；--no-redact 关闭）。"""
    if not text:
        return text
    text = _PEM_RE.sub("[PRIVATE KEY REDACTED]", text)
    text = _URL_USERPASS_RE.sub(r"\1\2:***@", text)
    text = _URL_SECRET_QUERY_RE.sub(r"\1***", text)
    chunks = _URL_RE.split(text)  # 奇数下标为 URL，原文保留（路径不算密钥）
    out = []
    for i, chunk in enumerate(chunks):
        if i % 2 == 1:
            out.append(chunk)
            continue
        chunk = _KNOWN_KEY_RE.sub("***", chunk)
        chunk = _JWT_RE.sub("***", chunk)
        chunk = _BEARER_RE.sub("Bearer ***", chunk)
        chunk = _ASSIGN_RE.sub(lambda m: m.group(1) + "=***", chunk)
        chunk = _LONG_TOKEN_RE.sub("***", chunk)
        out.append(chunk)
    return "".join(out)

# ── JSONL 会话日志目录（兼容保留）───────────────────────────────────────


def discover_dirs():
    """自动发现本机常见 JSONL 会话日志目录（只返回存在且含 *.jsonl 的目录）。"""
    home = Path.home()
    patterns = [
        home / ".clawdbot" / "agents" / "*" / "sessions",
        home / ".codex" / "sessions",
        home / ".claude" / "projects" / "*",
        home / ".config" / "opencode" / "sessions",
        home / ".gemini" / "sessions",
        home / ".agents" / "sessions",
    ]
    if os.environ.get("CODEX_HOME"):
        patterns.append(Path(os.environ["CODEX_HOME"]) / "sessions")
    found = []
    for pat in patterns:
        for d in glob.glob(str(pat)):
            dp = Path(d)
            if not dp.is_dir():
                continue
            if any(p.is_file() and p.name.lower().endswith(JSONL_SUFFIXES)
                   for p in dp.iterdir()):
                found.append(str(dp))
    return sorted(set(found))


def list_sessions(dir_path):
    """返回目录下所有会话文件信息（只按文件名/大小，不解析内容）。"""
    d = Path(dir_path)
    out = []
    for p in sorted(d.iterdir()):
        if not p.is_file() or not p.name.lower().endswith(JSONL_SUFFIXES):
            continue
        st = p.stat()
        out.append({
            "session": p.stem,
            "path": str(p),
            "size": st.st_size,
            "mtime": _dt.datetime.fromtimestamp(st.st_mtime)
            .isoformat(timespec="seconds"),
        })
    return out


def parse_jsonl(path):
    """解析一个 JSONL 文件 → (records, invalid)。容错：坏行跳过并计数。"""
    records = []
    invalid = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:  # noqa: BLE001
                invalid += 1
                continue
            if isinstance(obj, dict):
                records.append(obj)
            else:
                invalid += 1
    return records, invalid


def load_index(dir_path):
    """读取 sessions.json（若有）：返回 {别名: 会话ID}。"""
    idx = {}
    p = Path(dir_path) / "sessions.json"
    if not p.exists():
        return idx
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    except Exception:  # noqa: BLE001
        return idx
    if isinstance(data, dict):
        for k, v in data.items():
            idx[str(k)] = str(v)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                sid = item.get("sessionId") or item.get("session_id") or item.get("id")
                key = item.get("key") or item.get("name")
                if sid and key:
                    idx[str(key)] = str(sid)
    return idx


def _resolve_session_ids(idx, key):
    """把别名 / 会话 ID 统一解析为候选会话 ID 集合。"""
    ids = {key}
    if key in idx:
        ids.add(idx[key])
    for alias, sid in idx.items():
        if sid == key:
            ids.add(alias)
            ids.add(sid)
    return ids


def _alias_for(idx, sid):
    for alias, value in idx.items():
        if value == sid:
            return alias
    return ""


def _ts_on_date(ts, date):
    if not ts:
        return False
    if len(date) == 10:
        return ts[:10] == date
    if len(date) == 7:
        return ts[:7] == date
    return date in ts


def _clock(ts):
    """从 ISO 时间戳取 HH:MM:SS 片段。"""
    if "T" in ts:
        return ts.split("T", 1)[1][:8]
    if " " in ts:
        return ts.split(" ", 1)[1][:8]
    return ts[:8]


def _human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "%d B" % n if unit == "B" else "%.1f %s" % (n, unit)
        n /= 1024.0
    return "%d B" % n


# ── 记录提取（JSONL 消息形态；兼容保留）─────────────────────────────────

def _rec_ts(rec):
    ts = rec.get("timestamp")
    if not ts and isinstance(rec.get("message"), dict):
        ts = rec["message"].get("timestamp")
    if not ts and isinstance(rec.get("payload"), dict):
        ts = rec["payload"].get("timestamp") or rec["payload"].get("started_at")
    return str(ts) if ts else ""


def _rec_role(rec):
    payload = rec.get("payload")
    if isinstance(payload, dict):
        ptype = payload.get("type")
        if ptype == "message":
            role = str(payload.get("role") or "")
        elif ptype in ("function_call", "function_call_output",
                       "local_shell_call", "shell_call", "web_search_call"):
            role = "tool"
        else:
            role = ""
        return _norm_role(role) if role else ""
    msg = rec.get("message")
    if isinstance(msg, dict) and msg.get("role"):
        role = str(msg["role"])
    else:
        role = rec.get("role")
        role = str(role) if role else ""
    if role in ROLE_TOOL:
        return "tool"
    return role


def _rec_content(rec):
    payload = rec.get("payload")
    if isinstance(payload, dict) and payload.get("content") is not None:
        return payload["content"]
    msg = rec.get("message")
    if isinstance(msg, dict):
        return msg.get("content")
    return rec.get("content")


def _rec_text(rec):
    """提取记录里的人类可读文本（content 列表只取 type=text，字符串直接取）。"""
    content = _rec_content(rec)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in ("text", "input_text", "output_text") \
                    and item.get("text"):
                parts.append(str(item["text"]))
        return "\n".join(parts)
    return ""


def _rec_tool_names(rec):
    """提取记录里的工具调用名（toolCall / toolResult / payload function_call）。"""
    payload = rec.get("payload")
    if isinstance(payload, dict):
        ptype = payload.get("type")
        if ptype in ("function_call", "function_call_output",
                     "local_shell_call", "shell_call"):
            nm = payload.get("name") or payload.get("tool_name") or ""
            return [str(nm)] if nm else []
        return []
    content = _rec_content(rec)
    names = []
    if isinstance(content, list):
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in ("tool_call", "toolCall", "toolResult"):
                nm = item.get("name") or item.get("toolName") or ""
                if nm:
                    names.append(str(nm))
    return names


def _rec_cost(rec):
    payload = rec.get("payload")
    usage = None
    if isinstance(payload, dict):
        usage = payload.get("usage")
    if not isinstance(usage, dict):
        msg = rec.get("message")
        if isinstance(msg, dict):
            usage = msg.get("usage")
    if not isinstance(usage, dict):
        usage = rec.get("usage")
    if not isinstance(usage, dict):
        return 0.0
    cost = usage.get("cost")
    if isinstance(cost, dict):
        return float(cost.get("total") or 0)
    try:
        return float(cost or 0)
    except (TypeError, ValueError):
        return 0.0


def _rec_tokens(rec):
    payload = rec.get("payload")
    usage = None
    if isinstance(payload, dict):
        usage = payload.get("usage")
    if not isinstance(usage, dict):
        msg = rec.get("message")
        if isinstance(msg, dict):
            usage = msg.get("usage")
    if not isinstance(usage, dict):
        usage = rec.get("usage")
    if not isinstance(usage, dict):
        return (0, 0)
    return (int(usage.get("input_tokens") or 0),
            int(usage.get("output_tokens") or 0))


def _is_message(rec):
    """是否为可计入统计的消息记录（排除 session 元数据 / 空角色）。"""
    role = _rec_role(rec)
    if role in ("", "session"):
        return False
    return True


# ── 统一记录模型 + 字段别名归一 ──────────────────────────────────────────

def _first_alias(rec, aliases):
    if not isinstance(rec, dict):
        return None
    for k in aliases:
        if k in rec and rec[k] is not None and rec[k] != "":
            return rec[k]
    return None


def _unpack(value):
    """JSON 字符串解包（一层）：content / data 可能是 JSON 编码的字符串。"""
    if isinstance(value, str):
        s = value.strip()
        if s[:1] in ("{", "[") and (s.endswith("}") or s.endswith("]")):
            try:
                return json.loads(s)
            except Exception:
                return value
    return value


def _norm_time(value):
    """时间戳归一为 ISO 字符串；秒 / 毫秒自动推断。"""
    if value is None:
        return ""
    s = str(value).strip()
    if not s:
        return ""
    if re.fullmatch(r"\d{9,13}(\.\d+)?", s):
        try:
            secs = float(s)
            if secs > 1e12:      # 毫秒
                secs /= 1000.0
            return _dt.datetime.fromtimestamp(
                secs, tz=_dt.timezone.utc).isoformat(timespec="seconds")
        except (ValueError, OSError, OverflowError):
            return s
    return s[:-1] + "+00:00" if s.endswith("Z") else s


def _norm_role(role):
    if role is None:
        return ""
    r = str(role).strip()
    low = r.lower().replace("_", "").replace("-", "")
    if low in ("toolresult", "toolcall", "tool", "function",
               "functioncall", "toolcallresult"):
        return "tool"
    return r


def _extract_text(rec):
    """从各种形态的记录里提取人类可读文本（含 content 列表 / 字符串 / 嵌套 message）。"""
    if not isinstance(rec, dict):
        return ""
    msg = rec.get("message")
    content = None
    if isinstance(msg, dict):
        content = msg.get("content")
    if content is None:
        content = rec.get("content")
    if content is None:
        for k in TEXT_ALIASES:
            if k in rec and isinstance(rec[k], (str, list, dict)):
                content = rec[k]
                break
    content = _unpack(content)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if not isinstance(item, dict):
                continue
            if item.get("type") in ("text", "input_text", "output_text") \
                    and item.get("text"):
                parts.append(str(item["text"]))
            elif item.get("type") == "text" and item.get("content"):
                parts.append(str(item["content"]))
        return "\n".join(parts)
    if isinstance(content, dict):
        return str(content.get("text") or content.get("content") or "")
    return ""


def _norm_record(rec, source, fmt, kind, session_default, path, line=0,
                 extra_meta=None):
    """把一个原始记录（dict）归一为统一 Record。"""
    msg = rec.get("message") if isinstance(rec, dict) else None
    payload = rec.get("payload") if isinstance(rec, dict) else None
    if isinstance(msg, dict) or isinstance(payload, dict):
        role = _rec_role(rec)
        ts = _rec_ts(rec) or _first_alias(rec, TIME_ALIASES)
        text = _rec_text(rec)
    else:
        role = _first_alias(rec, ROLE_ALIASES)
        role = _norm_role(role) if role is not None else ""
        ts = _first_alias(rec, TIME_ALIASES)
        text = _extract_text(rec)
    session_id = _first_alias(rec, SESSION_ALIASES) or session_default
    title = _first_alias(rec, TITLE_ALIASES)
    meta = dict(extra_meta or {})
    meta["line"] = line
    if title:
        meta["title"] = str(title)
    tools = _rec_tool_names(rec)
    if tools:
        meta["tools"] = tools
    cost = _rec_cost(rec)
    ti, to = _rec_tokens(rec)
    if cost:
        meta["cost"] = cost
    if ti or to:
        meta["tokens_in"] = ti
        meta["tokens_out"] = to
    return {
        "source": source, "format": fmt, "kind": kind,
        "session": str(session_id), "time": _norm_time(ts),
        "role": role, "text": text, "path": str(path), "meta": meta,
    }


def _mk_source(name, kind, fmt, path, default_on=True, extra=None):
    return {"name": name, "kind": kind, "format": fmt, "path": str(path),
            "default_on": default_on, "extra": extra or {}}


# ── Reader 层：格式族可插拔 ──────────────────────────────────────────────

class JSONLReader:
    FORMAT = "jsonl"
    KIND = "session"

    @classmethod
    def discover(cls, base=None):
        base = base or Path.home()
        patterns = [
            base / ".clawdbot" / "agents" / "*" / "sessions",
            base / ".codex" / "sessions",
            base / ".claude" / "projects" / "*",
            base / ".config" / "opencode" / "sessions",
            base / ".gemini" / "sessions",
            base / ".agents" / "sessions",
        ]
        if os.environ.get("CODEX_HOME"):
            patterns.append(Path(os.environ["CODEX_HOME"]) / "sessions")
        out = []
        for pat in patterns:
            for d in glob.glob(str(pat)):
                dp = Path(d)
                if not dp.is_dir():
                    continue
                if cls._has_jsonl(dp):
                    out.append(_mk_source(cls._name_for(dp), "session",
                                          "jsonl", dp))
        return out

    @staticmethod
    def _has_jsonl(dp, max_depth=3):
        """目录（含最多 3 层子目录）内是否存在 *.jsonl 会话文件。"""
        root = str(dp)
        for dirpath, dirnames, filenames in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth >= max_depth:
                dirnames[:] = []
            for f in filenames:
                if f.lower().endswith(JSONL_SUFFIXES):
                    return True
        return False

    @staticmethod
    def _name_for(dp):
        s = str(dp).replace("\\", "/")
        if ".clawdbot" in s:
            m = re.search(r"agents/([^/]+)/sessions", s)
            return "clawdbot-" + (m.group(1) if m else "sessions")
        if ".codex" in s:
            return "codex-sessions"
        if ".claude" in s:
            return "claude-projects"
        if "opencode" in s:
            return "opencode-sessions"
        if ".gemini" in s:
            return "gemini-sessions"
        if ".agents" in s:
            return "agents-sessions"
        return "jsonl-sessions"

    @staticmethod
    def _walk_jsonl(d, max_depth=5):
        """递归收集目录下（含子目录）的 *.jsonl 会话文件。"""
        out = []
        root = str(d)
        for dirpath, dirnames, filenames in os.walk(root):
            depth = dirpath[len(root):].count(os.sep)
            if depth >= max_depth:
                dirnames[:] = []
            for f in sorted(filenames):
                if f.lower().endswith(JSONL_SUFFIXES):
                    out.append(Path(dirpath) / f)
        return out

    def iter_sessions(self, source, limit=0):
        d = Path(source["path"])
        idx = load_index(d)
        rows = []
        total_messages = 0
        total_invalid = 0
        for path in self._walk_jsonl(d):
            st = path.stat()
            records, invalid = parse_jsonl(path)
            total_invalid += invalid
            first_ts = ""
            messages = 0
            for rec in records:
                if not _is_message(rec):
                    continue
                messages += 1
                ts = _rec_ts(rec)
                if not first_ts and ts:
                    first_ts = ts
            total_messages += messages
            rows.append({
                "source": source["name"], "format": "jsonl", "kind": "session",
                "session": path.stem, "alias": _alias_for(idx, path.stem),
                "path": str(path), "size": st.st_size,
                "date": first_ts[:10], "messages": messages,
                "invalid": invalid,
                "mtime": _dt.datetime.fromtimestamp(st.st_mtime)
                .isoformat(timespec="seconds"),
            })
        rows.sort(key=lambda r: (r["date"] or r["mtime"]), reverse=True)
        if limit > 0:
            rows = rows[:limit]
        return rows, total_messages, total_invalid

    def iter_records(self, source):
        d = Path(source["path"])
        for path in self._walk_jsonl(d):
            records, _ = parse_jsonl(path)
            for lineno, rec in enumerate(records, 1):
                if not _is_message(rec):
                    continue
                yield _norm_record(rec, source["name"], "jsonl", "session",
                                   path.stem, path, line=lineno)


class JSONReader:
    FORMAT = "json"
    KIND = "session"

    @classmethod
    def discover(cls, base=None):
        base = base or Path.home()
        out = []
        for cand in (base / ".continue" / "sessions",
                     base / ".config" / "continue" / "sessions"):
            if cand.is_dir() and any(
                    p.suffix.lower() in JSON_SUFFIXES for p in cand.iterdir()):
                out.append(_mk_source("continue-sessions", "session", "json", cand))
        return out

    def _files(self, source):
        p = Path(source["path"])
        if p.is_file():
            return [p]
        return sorted(x for x in p.iterdir()
                      if x.is_file() and x.suffix.lower() in JSON_SUFFIXES)

    def _iter_file_records(self, path, source):
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        except Exception:
            return
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    yield _norm_record(item, source["name"], "json", "session",
                                       path.stem, path, line=i)
        elif isinstance(data, dict):
            for sid, val in data.items():
                if isinstance(val, list):
                    for i, item in enumerate(val, 1):
                        if isinstance(item, dict):
                            yield _norm_record(item, source["name"], "json",
                                               "session", sid, path, line=i)
                elif isinstance(val, dict):
                    yield _norm_record(val, source["name"], "json", "session",
                                       sid, path, line=1)

    def iter_records(self, source):
        for p in self._files(source):
            for rec in self._iter_file_records(p, source):
                yield rec

    def iter_sessions(self, source, limit=0):
        rows = []
        total_messages = 0
        for p in self._files(source):
            recs = list(self._iter_file_records(p, source))
            grouped = {}
            for r in recs:
                grouped.setdefault(r["session"], []).append(r)
            for sid, rl in grouped.items():
                first_ts = next((r["time"] for r in rl if r["time"]), "")
                total_messages += len(rl)
                rows.append({
                    "source": source["name"], "format": "json", "kind": "session",
                    "session": sid, "alias": "", "path": str(p),
                    "size": p.stat().st_size, "date": first_ts[:10],
                    "messages": len(rl), "invalid": 0,
                    "mtime": _dt.datetime.fromtimestamp(p.stat().st_mtime)
                    .isoformat(timespec="seconds"),
                })
        rows.sort(key=lambda r: (r["date"] or r["mtime"]), reverse=True)
        if limit > 0:
            rows = rows[:limit]
        return rows, total_messages, 0


class SQLiteReader:
    FORMAT = "sqlite"
    KIND = "session"

    @classmethod
    def discover(cls, base=None):
        base = base or Path.home()
        out = []
        cands = []
        xdg = os.environ.get("XDG_DATA_HOME")
        if xdg:
            cands.append(("opencode-db",
                          Path(xdg) / "opencode" / "opencode.db"))
        env = os.environ.get("OPENCODE_DATA")
        if env:
            cands.append(("opencode-db", Path(env) / "data" / "opencode" / "opencode.db"))
            cands.append(("opencode-db", Path(env) / "opencode.db"))
        cands += [
            ("opencode-db", base / ".local" / "share" / "opencode" / "opencode.db"),
            ("opencode-db", base / ".config" / "opencode" / "opencode.db"),
        ]
        seen = set()
        for name, p in cands:
            key = str(p)
            if key in seen:
                continue
            seen.add(key)
            if p.exists():
                out.append(_mk_source(name, "session", "sqlite", p))
        # VS Code / Cursor state.vscdb（Windows / Linux / macOS）
        for app in ("Code", "Cursor"):
            for root in (base / "AppData" / "Roaming" / app / "User" / "globalStorage",
                         base / ".config" / app / "User" / "globalStorage",
                         base / "Library" / "Application Support" / app / "User" / "globalStorage"):
                for d in glob.glob(str(root / "*")):
                    p = Path(d) / "state.vscdb"
                    if p.exists():
                        out.append(_mk_source(app.lower() + "-state", "session",
                                              "sqlite", p))
        return out

    @staticmethod
    def _connect(path):
        return sqlite3.connect("file:%s?mode=ro" % str(path).replace("\\", "/"),
                               uri=True)

    def _is_opencode(self, con):
        tabs = {r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        return {"session", "message", "part"}.issubset(tabs)

    def _pick_generic(self, con, extra):
        if extra.get("table"):
            return extra["table"]
        tabs = [r[0] for r in con.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
        best = None
        for t in tabs:
            if t.startswith("sqlite_"):
                continue
            cols = [c[1].lower() for c in con.execute("PRAGMA table_info(%s)" % t)]
            if any(c in ("text", "content", "body", "message", "statement")
                   for c in cols):
                if "id" in cols or "session" in cols or "role" in cols:
                    return t
                if best is None:
                    best = t
        return best

    def _generic_cols(self, con, table, extra):
        real = [c[1] for c in con.execute("PRAGMA table_info(%s)" % table)]
        low = [c.lower() for c in real]

        def pick(aliases, explicit):
            if explicit and explicit in real:
                return explicit
            if explicit and explicit.lower() in low:
                return real[low.index(explicit.lower())]
            for a in aliases:
                if a in real:
                    return a
                if a.lower() in low:
                    return real[low.index(a.lower())]
            return None

        return (pick(TIME_ALIASES, extra.get("col_time")),
                pick(ROLE_ALIASES, extra.get("col_role")),
                pick(TEXT_ALIASES, extra.get("col_text")),
                pick(SESSION_ALIASES, extra.get("col_session")),
                pick(TITLE_ALIASES, extra.get("col_title")))

    def _opencode_records(self, con, source):
        sess_title = dict(con.execute("SELECT id, title FROM session").fetchall())
        parts = {}
        for mid, data in con.execute("SELECT message_id, data FROM part"):
            parts.setdefault(mid, []).append(data)
        for mid, sid, t_created, mdata in con.execute(
                "SELECT id, session_id, time_created, data FROM message"):
            try:
                m = json.loads(mdata) if isinstance(mdata, str) else (mdata or {})
                role = (m or {}).get("role", "")
            except Exception:
                role = ""
            texts = []
            tools = []
            for pdata in parts.get(mid, []):
                try:
                    p = json.loads(pdata) if isinstance(pdata, str) else (pdata or {})
                except Exception:
                    continue
                ptype = p.get("type", "")
                if ptype == "text" and p.get("text"):
                    texts.append(p["text"])
                elif ptype == "tool" and p.get("tool"):
                    tools.append(p["tool"])
            if not texts and not tools:
                continue
            meta = {"tools": tools}
            title = sess_title.get(sid)
            if title:
                meta["title"] = title
            yield {
                "source": source["name"], "format": "sqlite", "kind": "session",
                "session": sid, "time": _norm_time(t_created),
                "role": _norm_role(role), "text": "\n".join(texts),
                "path": str(source["path"]), "meta": meta,
            }

    def iter_records(self, source):
        con = self._connect(source["path"])
        try:
            if self._is_opencode(con):
                for r in self._opencode_records(con, source):
                    yield r
                return
            extra = source.get("extra") or {}
            table = self._pick_generic(con, extra)
            if not table:
                return
            col_time, col_role, col_text, col_session, col_title = \
                self._generic_cols(con, table, extra)
            if not col_text:
                return
            cols = [d[0] for d in con.execute("SELECT * FROM %s LIMIT 0" % table)
                    .description]
            for i, row in enumerate(con.execute("SELECT * FROM %s" % table), 1):
                rec = dict(zip(cols, row))
                text = rec.get(col_text)
                if isinstance(text, (dict, list)):
                    text = json.dumps(text, ensure_ascii=False)
                elif isinstance(text, str):
                    text = _unpack(text)
                text = str(text) if text is not None else ""
                sid = rec.get(col_session) if col_session else \
                    Path(source["path"]).stem
                meta = {}
                if col_title and rec.get(col_title) is not None:
                    meta["title"] = str(rec[col_title])
                yield {
                    "source": source["name"], "format": "sqlite",
                    "kind": source["kind"],
                    "session": str(sid),
                    "time": _norm_time(rec.get(col_time) if col_time else None),
                    "role": _norm_role(rec.get(col_role) if col_role else ""),
                    "text": text, "path": str(source["path"]), "meta": meta,
                }
        finally:
            con.close()

    def iter_sessions(self, source, limit=0):
        con = self._connect(source["path"])
        try:
            rows = []
            if self._is_opencode(con):
                cols = {c[1] for c in con.execute("PRAGMA table_info(session)")}
                use_metrics = {"cost", "tokens_input", "tokens_output"}.issubset(cols)
                if use_metrics:
                    q = ("SELECT id, title, time_created, cost, tokens_input, "
                         "tokens_output, (SELECT COUNT(*) FROM message m WHERE "
                         "m.session_id = s.id) FROM session s "
                         "ORDER BY time_created DESC")
                else:
                    q = ("SELECT id, title, time_created, 0, 0, 0, "
                         "(SELECT COUNT(*) FROM message m WHERE "
                         "m.session_id = s.id) FROM session s "
                         "ORDER BY time_created DESC")
                for sid, title, t_created, cost, ti, to, cnt in con.execute(q):
                    rows.append({
                        "source": source["name"], "format": "sqlite",
                        "kind": "session", "session": sid, "alias": "",
                        "path": str(source["path"]),
                        "size": os.path.getsize(source["path"]),
                        "date": _norm_time(t_created)[:10],
                        "messages": cnt, "invalid": 0,
                        "mtime": _norm_time(t_created)[:19].replace("T", " "),
                        "title": title or "",
                    })
                return rows, sum(r["messages"] for r in rows), 0
            extra = source.get("extra") or {}
            table = self._pick_generic(con, extra)
            if not table:
                return [], 0, 0
            col_time, col_role, col_text, col_session, col_title = \
                self._generic_cols(con, table, extra)
            if not col_session:
                cnt = con.execute("SELECT COUNT(*) FROM %s" % table).fetchone()[0]
                rows.append({
                    "source": source["name"], "format": "sqlite",
                    "kind": source["kind"], "session": Path(source["path"]).stem,
                    "alias": "", "path": str(source["path"]),
                    "size": os.path.getsize(source["path"]),
                    "date": "", "messages": cnt, "invalid": 0,
                    "mtime": _dt.datetime.fromtimestamp(
                        os.path.getmtime(source["path"])).isoformat(timespec="seconds"),
                    "title": "",
                })
                return rows, cnt, 0
            q = ("SELECT %s, COUNT(*) FROM %s GROUP BY %s"
                 % (col_session, table, col_session))
            for sid, cnt in con.execute(q):
                rows.append({
                    "source": source["name"], "format": "sqlite",
                    "kind": source["kind"], "session": str(sid), "alias": "",
                    "path": str(source["path"]),
                    "size": os.path.getsize(source["path"]),
                    "date": "", "messages": cnt, "invalid": 0,
                    "mtime": _dt.datetime.fromtimestamp(
                        os.path.getmtime(source["path"])).isoformat(timespec="seconds"),
                    "title": "",
                })
            rows.sort(key=lambda r: r["session"])
            if limit > 0:
                rows = rows[:limit]
            return rows, sum(r["messages"] for r in rows), 0
        finally:
            con.close()


class MarkdownReader:
    FORMAT = "markdown"
    KIND = "memory"

    @classmethod
    def discover(cls, base=None):
        base = base or Path.home()
        cwd = Path.cwd()
        out = []
        mem = cls._memory_home(base)
        for name, sub in (("yottamemory-facts", "facts"),
                          ("yottamemory-private", "private"),
                          ("yottamemory-archive", "archive")):
            p = mem / sub
            if p.is_dir() and any(x.suffix.lower() in MD_SUFFIXES
                                  for x in p.iterdir()):
                out.append(_mk_source(name, "memory", "markdown", p))
        codex_home = os.environ.get("CODEX_HOME") or str(base / ".codex")
        codex_notes = Path(codex_home) / "memories"
        if codex_notes.is_dir() and cls._has_md(codex_notes):
            out.append(_mk_source("codex-notes", "note", "markdown", codex_notes,
                                  default_on=False))
        # Aider 会话历史（当前目录浅扫）
        for p in sorted(cwd.glob("*.aider.*.md")) + \
                sorted(cwd.glob("*.aider.*.markdown")):
            out.append(_mk_source("aider-history", "session", "markdown", p))
        return out

    @staticmethod
    def _memory_home(base):
        """yotta-memory 记忆库位置：优先环境变量，再读引擎 config.json。"""
        env = os.environ.get("YOTTA_MEMORY_HOME")
        if env:
            return Path(env)
        try:
            cfg_p = base / ".yottamemory" / "config.json"
            cfg = json.loads(cfg_p.read_text(encoding="utf-8", errors="replace"))
            mh = cfg.get("memory_home")
            if mh:
                return Path(mh)
        except Exception:
            pass
        return base / ".yottamemory"

    @staticmethod
    def _has_md(p, depth=3):
        for x in p.rglob("*.md"):
            rel = x.relative_to(p)
            if len(rel.parts) <= depth:
                return True
        return False

    def _files(self, source):
        p = Path(source["path"])
        if p.is_file():
            return [p]
        if not p.is_dir():
            return []
        out = []
        for x in sorted(p.rglob("*.md")):
            rel = x.relative_to(p)
            if len(rel.parts) <= 4:
                out.append(x)
        return out

    @staticmethod
    def _split_frontmatter(text):
        """YAML frontmatter 子集解析：--- 块 → (dict, 正文)。零依赖。"""
        if not text.startswith("---"):
            return {}, text
        lines = text.split("\n")
        end = None
        for i in range(1, min(len(lines), 300)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            return {}, text
        fm = {}
        for line in lines[1:end]:
            s = line.strip()
            if not s or s.startswith("#") or ":" not in s:
                continue
            k, _, v = s.partition(":")
            k = k.strip().lower()
            v = v.strip()
            if not v:
                fm[k] = None
                continue
            if v.startswith("[") and v.endswith("]"):
                inner = v[1:-1].strip()
                fm[k] = [x.strip().strip("\"'")
                         for x in inner.split(",") if x.strip()]
            elif v[:1] in ("\"", "'") and v[-1:] == v[:1]:
                fm[k] = v[1:-1]
            else:
                fm[k] = v
        body = "\n".join(lines[end + 1:])
        return fm, body

    def _file_record(self, path, source):
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return None
        fm, body = self._split_frontmatter(text)
        st = path.stat()
        mtime = _dt.datetime.fromtimestamp(st.st_mtime) \
            .isoformat(timespec="seconds")
        kind = source["kind"]
        role = ""
        if fm:
            role = _norm_role(fm.get("type") or "")
            if not role and kind == "memory":
                role = "memory"
        title = fm.get("subject") or fm.get("title") or fm.get("name")
        content = fm.get("statement") or fm.get("content") or fm.get("text")
        if content is None:
            content = body.strip()
        else:
            content = str(content)
        if not title:
            m = re.search(r"^#\s+(.+)$", body, re.M)
            title = m.group(1).strip() if m else ""
        ts = fm.get("created") or fm.get("date") or fm.get("updated") or mtime
        meta = {}
        if title:
            meta["title"] = title
        for k in ("tags", "confidence", "scope", "owner", "immutable"):
            if fm.get(k) is not None:
                meta[k] = fm[k]
        return {
            "source": source["name"], "format": "markdown", "kind": kind,
            "session": path.stem, "time": _norm_time(ts),
            "role": role, "text": content, "path": str(path), "meta": meta,
        }

    def iter_records(self, source):
        for p in self._files(source):
            r = self._file_record(p, source)
            if r and (r["text"] or r["meta"].get("title")):
                yield r

    def iter_sessions(self, source, limit=0):
        rows = []
        total = 0
        for p in self._files(source):
            r = self._file_record(p, source)
            if not r:
                continue
            total += 1
            rows.append({
                "source": source["name"], "format": "markdown",
                "kind": r["kind"], "session": p.stem, "alias": "",
                "path": str(p), "size": p.stat().st_size,
                "date": r["time"][:10], "messages": 1, "invalid": 0,
                "mtime": _dt.datetime.fromtimestamp(p.stat().st_mtime)
                .isoformat(timespec="seconds"),
                "title": r["meta"].get("title", ""),
            })
        rows.sort(key=lambda r: (r["date"] or r["mtime"]), reverse=True)
        if limit > 0:
            rows = rows[:limit]
        return rows, total, 0


class BinaryReader:
    FORMAT = "binary"
    KIND = "log"

    @classmethod
    def discover(cls, base=None):
        base = base or Path.home()
        out = []
        for root in (base / ".codeium" / "windsurf", base / ".windsurf"):
            if root.is_dir():
                for p in list(root.glob("**/*.pbtxt"))[:200]:
                    out.append(_mk_source("windsurf-conv", "log", "binary",
                                          p, default_on=False))
        return out

    def iter_records(self, source):
        p = Path(source["path"])
        title = p.stem
        try:
            raw = p.read_bytes()[:512]
            s = raw.decode("utf-8", errors="replace")
            m = re.search(r"[A-Za-z0-9\u4e00-\u9fff][^\x00-\x1f]{2,80}", s)
            if m:
                title = m.group(0).strip()
        except Exception:
            pass
        st = p.stat()
        yield {
            "source": source["name"], "format": "binary", "kind": "log",
            "session": p.stem,
            "time": _dt.datetime.fromtimestamp(st.st_mtime)
            .isoformat(timespec="seconds"),
            "role": "", "text": title, "path": str(p),
            "meta": {"title": title},
        }

    def iter_sessions(self, source, limit=0):
        rows = []
        for rec in self.iter_records(source):
            p = Path(source["path"])
            st = p.stat()
            rows.append({
                "source": source["name"], "format": "binary", "kind": "log",
                "session": rec["session"], "alias": "", "path": str(p),
                "size": st.st_size, "date": rec["time"][:10],
                "messages": 1, "invalid": 0,
                "mtime": _dt.datetime.fromtimestamp(st.st_mtime)
                .isoformat(timespec="seconds"),
                "title": rec["meta"].get("title", ""),
            })
        return rows, len(rows), 0


READERS = (JSONLReader, JSONReader, SQLiteReader, MarkdownReader, BinaryReader)


def reader_for(fmt):
    for cls in READERS:
        if cls.FORMAT == fmt:
            return cls()
    raise SystemExit("不支持的格式：%s" % fmt)


# ── 嗅探（--dir 指向目录 / 文件时自动判定格式族）────────────────────────

def _sniff_file_format(p):
    name = p.name.lower()
    for suf in JSONL_SUFFIXES:
        if name.endswith(suf):
            return "jsonl"
    if name.endswith(JSON_SUFFIXES):
        return "json"
    if name.endswith(SQLITE_SUFFIXES):
        return "sqlite"
    if name.endswith(MD_SUFFIXES):
        return "markdown"
    if name.endswith(BINARY_SUFFIXES):
        return "binary"
    try:
        head = p.read_bytes()[:512]
    except Exception:
        return "binary"
    if head.startswith(b"SQLite format 3"):
        return "sqlite"
    try:
        s = head.decode("utf-8", errors="replace").lstrip()
    except Exception:
        return "binary"
    if s.startswith("---"):
        return "markdown"
    if s[:1] in ("{", "["):
        first_line = s.split("\n", 1)[0].strip()
        if first_line.startswith("["):
            return "json"
        try:
            obj = json.loads(first_line)
            return "jsonl" if isinstance(obj, dict) else "json"
        except Exception:
            return "json"
    if re.search(r"^#\s+\S", s, re.M):
        return "markdown"
    return "binary"


def _sniff_dir_format(p):
    names = [f.name.lower() for f in p.iterdir() if f.is_file()]
    if any(n.endswith(JSONL_SUFFIXES) for n in names):
        return "jsonl"
    if any(n.endswith(SQLITE_SUFFIXES) for n in names):
        return "sqlite"
    if any(n.endswith(JSON_SUFFIXES) for n in names):
        return "json"
    if any(n.endswith(MD_SUFFIXES) for n in names):
        return "markdown"
    return None


def _sniff_file_kind(p):
    fmt = _sniff_file_format(p)
    if fmt == "markdown":
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
            return "memory" if t.startswith("---") else "note"
        except Exception:
            return "note"
    if fmt == "binary":
        return "log"
    return "session"


def _sniff_dir_kind(p):
    low = p.name.lower()
    if any(k in low for k in ("fact", "private", "memory", "记忆")):
        return "memory"
    if any(k in low for k in ("note", "notes", "笔记", "memories")):
        return "note"
    return "session"


def sniff_source(path):
    """把 --dir / YOTTA_LOGS_DIR 指向的路径嗅探为一个单一来源。"""
    p = Path(path)
    if not p.exists():
        raise SystemExit("路径不存在：%s" % p)
    if p.is_file():
        return _mk_source(p.stem or "source", _sniff_file_kind(p),
                          _sniff_file_format(p), p)
    fmt = _sniff_dir_format(p)
    if fmt == "markdown":
        return _mk_source(p.name or "source", _sniff_dir_kind(p), fmt, p)
    if fmt:
        return _mk_source(p.name or "source", "session", fmt, p)
    raise SystemExit("无法识别 %s 的日志 / 记忆格式（支持 jsonl / json / "
                     "sqlite / markdown）" % p)


# ── 配置兜底 + discover 全源登记 ─────────────────────────────────────────

def default_config_path():
    """平台无关的默认配置路径；环境变量始终优先。"""
    env = os.environ.get("YOTTA_LOGS_CONFIG")
    if env:
        return Path(env)
    xdg = os.environ.get("XDG_CONFIG_HOME")
    if xdg:
        return Path(xdg) / "yotta-logs" / "config.json"
    if os.name == "nt":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata) / "yotta-logs" / "config.json"
    return Path.home() / ".config" / "yotta-logs" / "config.json"


def load_config():
    cfg_path = default_config_path()
    if not cfg_path.exists():
        return {}
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8", errors="replace"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def default_scope():
    cfg = load_config()
    return list(cfg.get("default_scope") or ["session", "memory"])


def _config_sources(cfg):
    out = []
    for s in (cfg.get("sources") or []):
        if not isinstance(s, dict) or not s.get("path"):
            continue
        extra = {k: v for k, v in s.items()
                 if k in ("table", "col_time", "col_role", "col_text",
                          "col_session", "col_title")}
        out.append(_mk_source(
            s.get("name") or Path(s["path"]).stem,
            s.get("kind") or "session",
            s.get("format") or "jsonl",
            s["path"],
            default_on=True,
            extra=extra,
        ))
    return out


def discover_sources(config=None):
    cfg = config if config is not None else load_config()
    sources = []
    for cls in READERS:
        for s in cls.discover():
            sources.append(s)
    sources += _config_sources(cfg)
    seen = set()
    dedup = []
    for s in sources:
        key = (s["format"], str(s["path"]).lower())
        if key in seen:
            continue
        seen.add(key)
        dedup.append(s)
    scope = set(cfg.get("default_scope") or ["session", "memory"])
    for s in dedup:
        s["default_on"] = s["default_on"] or s["kind"] in scope
    return dedup


def _candidate_ids(source, session_ids):
    """把会话 ID / 别名解析为候选会话 ID 集合（JSONL 源带 sessions.json 别名）。"""
    ids = set()
    for g in (session_ids if isinstance(session_ids, (list, tuple))
              else [session_ids]):
        ids.add(g)
        if source["format"] == "jsonl":
            idx = load_index(Path(source["path"]))
            ids |= _resolve_session_ids(idx, g)
    return ids


def filter_sources(sources, args):
    explicit = False
    if getattr(args, "source", None):
        names = set(args.source)
        sources = [s for s in sources if s["name"] in names]
        explicit = True
    if getattr(args, "format", None):
        sources = [s for s in sources if s["format"] == args.format]
        explicit = True
    if getattr(args, "kind", None):
        sources = [s for s in sources if s["kind"] == args.kind]
        explicit = True
    if not explicit:
        sources = [s for s in sources if s["default_on"]]
    return sources


def resolve_sources(args):
    if getattr(args, "dir", None):
        srcs = [sniff_source(args.dir)]
    else:
        env = os.environ.get("YOTTA_LOGS_DIR")
        if env:
            srcs = [sniff_source(env)]
        else:
            srcs = discover_sources()
            if not srcs:
                raise SystemExit(
                    "未找到已知日志 / 记忆源：用 --dir 指定，或设 YOTTA_LOGS_DIR / "
                    "YOTTA_LOGS_CONFIG；可用 locate 查看候选。")
    return filter_sources(srcs, args)


# ── 统一检索 / 提取 / 统计 / 工具排行 ───────────────────────────────────

def scan_all(sources, limit=0):
    rows = []
    total_messages = 0
    total_invalid = 0
    for src in sources:
        reader = reader_for(src["format"])
        r, tm, inv = reader.iter_sessions(src)
        rows.extend(r)
        total_messages += tm
        total_invalid += inv
    if limit > 0:
        rows = rows[:limit]
    return {"rows": rows, "total_sessions": len(rows),
            "total_messages": total_messages, "total_invalid": total_invalid}


def search_all(sources, query, regex=False, date=None, sessions=None, role=None,
               limit=DEFAULT_LIMIT, context=DEFAULT_CONTEXT, no_redact=False):
    if regex:
        try:
            pat = re.compile(query, re.I)
        except re.error as e:
            raise SystemExit("正则无效：%s" % e)
    matches = []
    hit = set()
    truncated = False
    for source in sources:
        reader = reader_for(source["format"])
        cands = _candidate_ids(source, sessions) if sessions else None
        for rec in reader.iter_records(source):
            text = rec["text"]
            if not text:
                continue
            if cands is not None and rec["session"] not in cands:
                continue
            ts = rec["time"]
            if date and not _ts_on_date(ts, date):
                continue
            rrole = rec["role"]
            if role and rrole != role:
                continue
            if regex:
                m = pat.search(text)
                if not m:
                    continue
                span = m.span()
                matched = m.group(0)
            else:
                idx_f = text.lower().find(query.lower())
                if idx_f < 0:
                    continue
                span = (idx_f, idx_f + len(query))
                matched = query
            snippet = _snippet(text, span, context)
            if not no_redact:
                snippet = redact(snippet)
                matched = redact(matched)
            matches.append({
                "source": source["name"], "format": source["format"],
                "kind": source["kind"], "session": rec["session"],
                "timestamp": ts, "role": rrole,
                "line": rec["meta"].get("line", 0),
                "match": matched, "text": snippet,
            })
            hit.add((source["name"], rec["session"]))
            if len(matches) >= limit:
                truncated = True
                return {"matches": matches, "sessions_hit": len(hit),
                        "truncated": truncated}
    return {"matches": matches, "sessions_hit": len(hit), "truncated": truncated}


def extract_all(sources, session_id, role=None, with_tools=False,
                no_redact=False):
    """跨源提取单个会话；多个源同名会话取第一个（--source 可消歧）。"""
    source_match = None
    for source in sources:
        reader = reader_for(source["format"])
        cands = _candidate_ids(source, session_id)
        for rec in reader.iter_records(source):
            if rec["session"] in cands:
                source_match = source
                break
        if source_match:
            break
    if source_match is None:
        raise SystemExit("未找到会话：%s（可用 scan 列出会话 ID）" % session_id)
    reader = reader_for(source_match["format"])
    cands = _candidate_ids(source_match, session_id)
    actual = None
    messages = []
    total_records = 0
    for rec in reader.iter_records(source_match):
        if rec["session"] not in cands:
            continue
        if actual is None:
            actual = rec["session"]
        total_records += 1
        rrole = rec["role"]
        if role and rrole != role:
            continue
        text = rec["text"]
        tools = rec["meta"].get("tools") or []
        if not text and not tools:
            continue
        if not no_redact:
            text = redact(text)
        messages.append({
            "line": rec["meta"].get("line", 0),
            "timestamp": rec["time"],
            "role": rrole,
            "text": text,
            "tools": tools,
        })
    return {
        "session": actual,
        "dir": str(source_match["path"]),
        "source": source_match["name"],
        "format": source_match["format"],
        "kind": source_match["kind"],
        "messages": messages,
        "invalid": 0,
        "total_records": total_records,
    }


def stats_all(sources, session_id=None, daily=False):
    agg = {
        "sessions": 0, "messages": 0, "invalid": 0,
        "roles": {}, "cost": 0.0, "tokens_in": 0, "tokens_out": 0,
        "first": "", "last": "", "days": {}, "by_source": {},
    }
    for source in sources:
        reader = reader_for(source["format"])
        rows, tm, inv = reader.iter_sessions(source)
        if session_id:
            cands = _candidate_ids(source, session_id)
            rows = [r for r in rows if r["session"] in cands]
        agg["sessions"] += len(rows)
        agg["invalid"] += inv
        bs = agg["by_source"].setdefault(source["name"], {
            "format": source["format"], "kind": source["kind"],
            "sessions": 0, "messages": 0, "cost": 0.0,
            "tokens_in": 0, "tokens_out": 0, "first": "", "last": "",
        })
        bs["sessions"] += len(rows)
        cands = _candidate_ids(source, session_id) if session_id else None
        for rec in reader.iter_records(source):
            if cands is not None and rec["session"] not in cands:
                continue
            role = rec["role"]
            agg["roles"][role] = agg["roles"].get(role, 0) + 1
            bs["messages"] += 1
            ts = rec["time"]
            cost = rec["meta"].get("cost", 0.0)
            ti = rec["meta"].get("tokens_in", 0)
            to = rec["meta"].get("tokens_out", 0)
            if ts:
                day = ts[:10]
                if day:
                    d = agg["days"].setdefault(day, {"messages": 0, "cost": 0.0})
                    d["messages"] += 1
                    d["cost"] += cost
                if not agg["first"] or ts < agg["first"]:
                    agg["first"] = ts
                if not agg["last"] or ts > agg["last"]:
                    agg["last"] = ts
                if not bs["first"] or ts < bs["first"]:
                    bs["first"] = ts
                if not bs["last"] or ts > bs["last"]:
                    bs["last"] = ts
            agg["cost"] += cost
            agg["tokens_in"] += ti
            agg["tokens_out"] += to
            bs["cost"] += cost
            bs["tokens_in"] += ti
            bs["tokens_out"] += to
        agg["messages"] += bs["messages"]
    return agg


def tools_all(sources, session_id=None):
    counts = {}
    for source in sources:
        reader = reader_for(source["format"])
        cands = _candidate_ids(source, session_id) if session_id else None
        for rec in reader.iter_records(source):
            if cands is not None and rec["session"] not in cands:
                continue
            for nm in rec["meta"].get("tools") or []:
                counts[nm] = counts.get(nm, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


# ── 兼容保留：单目录（JSONL）旧函数签名 ─────────────────────────────────

def scan_sessions(dir_path):
    source = sniff_source(dir_path)
    res = scan_all([source])
    res["dir"] = str(dir_path)
    return res


def search_sessions(dir_path, query, regex=False, date=None, sessions=None,
                    role=None, limit=DEFAULT_LIMIT, context=DEFAULT_CONTEXT,
                    no_redact=False):
    source = sniff_source(dir_path)
    return search_all([source], query, regex=regex, date=date,
                      sessions=sessions, role=role, limit=limit,
                      context=context, no_redact=no_redact)


def extract_session(dir_path, session_id, role=None, with_tools=False,
                    no_redact=False):
    source = sniff_source(dir_path)
    return extract_all([source], session_id, role=role, with_tools=with_tools,
                       no_redact=no_redact)


def session_stats(dir_path, session_id=None, daily=False):
    source = sniff_source(dir_path)
    res = stats_all([source], session_id=session_id, daily=daily)
    res["dir"] = str(dir_path)
    return res


def tool_breakdown(dir_path, session_id=None):
    source = sniff_source(dir_path)
    return tools_all([source], session_id=session_id)


# ── 文本格式化 ───────────────────────────────────────────────────────────

def fmt_locate(sources):
    lines = []
    scope = " + ".join(default_scope()) if default_scope() else "（无）"
    lines.append("发现的日志 / 记忆源 %d 个 ｜ 默认范围：%s"
                 % (len(sources), scope))
    lines.append("")
    lines.append("%-22s %-9s %-8s %-3s %s"
                 % ("来源", "格式", "类型", "默认", "路径"))
    for s in sorted(sources, key=lambda x: (x["name"], x["path"])):
        lines.append("%-22s %-9s %-8s %-3s %s"
                     % (s["name"][:22], s["format"], s["kind"],
                        "开" if s["default_on"] else "关", s["path"]))
    return "\n".join(lines)


def fmt_scan(res):
    lines = []
    lines.append("来源 %d 个 ｜ 会话 %d 个 ｜ 消息合计 %d ｜ 无效行 %d"
                 % (len(res.get("sources") or []), res["total_sessions"],
                    res["total_messages"], res["total_invalid"]))
    lines.append("")
    lines.append("%-14s %-8s %-8s %-24s %-10s %8s %10s  %s"
                 % ("来源", "格式", "类型", "会话 ID", "日期", "消息", "大小", "别名"))
    for r in res["rows"]:
        lines.append("%-14s %-8s %-8s %-24s %-10s %8d %10s  %s"
                     % (r["source"][:14], r["format"], r["kind"],
                        r["session"][:24], r["date"] or "-", r["messages"],
                        _human_size(r["size"]), r.get("alias", "")))
    return "\n".join(lines)


def fmt_search(res, query, sources, regex):
    lines = []
    if regex:
        desc = "正则：%s" % query
    else:
        desc = "检索词：%s" % query
    lines.append("匹配 %d 处 / %d 个会话（%s）"
                 % (len(res["matches"]), res["sessions_hit"], desc))
    if res["truncated"]:
        lines.append("（已达 --limit 上限，结果被截断）")
    lines.append("")
    cur = None
    for m in res["matches"]:
        key = (m["source"], m["session"])
        if key != cur:
            cur = key
            lines.append("── %s / 会话 %s ─────────────────" % (m["source"], m["session"]))
        lines.append("%s [%s] %s" % (_clock(m["timestamp"]), m["role"], m["text"]))
    if not res["matches"]:
        lines.append("未命中。")
    return "\n".join(lines)


def fmt_session(res):
    lines = []
    counts = {}
    for m in res["messages"]:
        counts[m["role"]] = counts.get(m["role"], 0) + 1
    parts = " ｜ ".join("%s %d" % (k, v) for k, v in sorted(counts.items()))
    lines.append("会话：%s ｜ 来源 %s（%s）｜ 消息 %d（%s）"
                 % (res["session"], res.get("source", "-"),
                    res.get("format", "-"), len(res["messages"]), parts))
    lines.append("")
    for m in res["messages"]:
        lines.append("── %s ─────────────────────────" % _clock(m["timestamp"]))
        tag = "[%s]" % m["role"]
        if m["tools"]:
            tag += " 工具:%s" % ",".join(m["tools"])
        lines.append("%s %s" % (tag, m["text"]))
        lines.append("")
    return "\n".join(lines)


def fmt_stats(res, daily):
    lines = []
    lines.append("会话统计")
    srcs = " ｜ ".join("%s %d" % (k, v["sessions"])
                      for k, v in sorted(res.get("by_source", {}).items()))
    if srcs:
        lines.append("分源会话：%s" % srcs)
    roles = " ｜ ".join("%s %d" % (k, v)
                        for k, v in sorted(res["roles"].items()))
    lines.append("会话 %d ｜ 消息 %d（%s）｜ 无效行 %d"
                 % (res["sessions"], res["messages"], roles, res["invalid"]))
    if res["first"]:
        lines.append("时间范围 %s → %s" % (res["first"][:19], res["last"][:19]))
    lines.append("token 输入 %s ｜ 输出 %s ｜ 成本 $%.2f"
                 % (_fmt_int(res["tokens_in"]), _fmt_int(res["tokens_out"]),
                    res["cost"]))
    if daily and res["days"]:
        lines.append("")
        lines.append("── 每日汇总 ──")
        for day in sorted(res["days"], reverse=True):
            d = res["days"][day]
            lines.append("%s  消息 %d ｜ 成本 $%.2f" % (day, d["messages"], d["cost"]))
    return "\n".join(lines)


def _fmt_int(n):
    return format(n, ",")


def fmt_tools(items):
    lines = []
    lines.append("工具调用排行（按次数降序）")
    for name, count in items:
        lines.append("%6d  %s" % (count, name))
    if not items:
        lines.append("（无工具调用记录）")
    return "\n".join(lines)


def _snippet(text, span, radius):
    start, end = span
    lo = max(0, start - radius)
    hi = min(len(text), end + radius)
    pre = "…" if lo > 0 else ""
    post = "…" if hi < len(text) else ""
    return pre + text[lo:hi].replace("\n", " ") + post


# ── CLI ──────────────────────────────────────────────────────────────────

class _Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self._print_message("%s: error: %s\n" % (self.prog, message), sys.stderr)
        raise SystemExit(4)


def _add_dir(ap):
    ap.add_argument("--dir", metavar="PATH",
                    help="日志 / 记忆目录或文件（缺省读 YOTTA_LOGS_DIR，"
                         "再 discover 全源登记）")


def _add_filters(ap):
    ap.add_argument("--source", action="append", metavar="NAME",
                    help="只检索指定来源（可多次；名称见 locate）")
    ap.add_argument("--kind", choices=KIND_CHOICES,
                    help="只检索指定类型：session / memory / note / log")
    ap.add_argument("--format", choices=FORMAT_CHOICES,
                    help="只检索指定格式：jsonl / json / sqlite / markdown / binary")


def _source_brief(sources):
    return [{"name": s["name"], "kind": s["kind"], "format": s["format"],
             "path": s["path"], "default_on": s["default_on"]} for s in sources]


def main(argv=None):
    ap = _Parser(
        prog=TOOL_NAME,
        description="%s（%s）：零依赖跨智能体会话 / 记忆日志检索引擎。"
                    % (TOOL_CN, TOOL_NAME))
    ap.add_argument("--version", action="version",
                    version="%s %s" % (TOOL_NAME, VERSION))
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("version", help="打印版本")

    p_locate = sub.add_parser("locate", help="全源登记：发现本机日志 / 记忆源")
    p_locate.add_argument("--json", action="store_true", help="输出 JSON")

    p_scan = sub.add_parser("scan", help="列出所有会话（跨源）")
    _add_dir(p_scan)
    _add_filters(p_scan)
    p_scan.add_argument("--json", action="store_true", help="输出 JSON")
    p_scan.add_argument("--limit", type=int, default=0,
                        help="最多列出 N 个会话（默认全部）")

    p_search = sub.add_parser("search", help="跨源检索关键词 / 正则")
    p_search.add_argument("query", help="检索词（默认不区分大小写）")
    _add_dir(p_search)
    _add_filters(p_search)
    p_search.add_argument("--regex", action="store_true", help="把 query 当正则")
    p_search.add_argument("--date", metavar="YYYY-MM-DD",
                          help="只检索指定日期（或 YYYY-MM）")
    p_search.add_argument("-s", "--session", action="append", metavar="SID",
                          help="只检索指定会话 ID / 别名（可多次）")
    p_search.add_argument("--role", choices=("user", "assistant", "tool", "system", "developer"),
                          help="只检索指定角色")
    p_search.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                          help="最多返回 N 条命中（默认 %d）" % DEFAULT_LIMIT)
    p_search.add_argument("--context", type=int, default=DEFAULT_CONTEXT,
                          help="命中上下文半径字符数（默认 %d）" % DEFAULT_CONTEXT)
    p_search.add_argument("--json", action="store_true", help="输出 JSON")
    p_search.add_argument("--no-redact", action="store_true",
                          help="关闭默认脱敏")

    p_session = sub.add_parser("session", help="提取单个会话原文")
    p_session.add_argument("sid", help="会话 ID / 别名")
    _add_dir(p_session)
    _add_filters(p_session)
    p_session.add_argument("--role", choices=("user", "assistant", "tool", "system", "developer"),
                           help="只提取指定角色")
    p_session.add_argument("--tools", action="store_true",
                           help="标注工具调用")
    p_session.add_argument("--limit", type=int, default=0,
                           help="最多输出 N 条消息（默认全部）")
    p_session.add_argument("--json", action="store_true", help="输出 JSON")
    p_session.add_argument("--no-redact", action="store_true",
                           help="关闭默认脱敏")

    p_stats = sub.add_parser("stats", help="会话统计汇总（跨源）")
    _add_dir(p_stats)
    _add_filters(p_stats)
    p_stats.add_argument("-s", "--session", metavar="SID",
                         help="只统计指定会话 ID / 别名")
    p_stats.add_argument("--daily", action="store_true", help="输出每日汇总")
    p_stats.add_argument("--json", action="store_true", help="输出 JSON")

    p_tools = sub.add_parser("tools", help="工具调用次数排行（跨源）")
    _add_dir(p_tools)
    _add_filters(p_tools)
    p_tools.add_argument("-s", "--session", metavar="SID",
                         help="只统计指定会话 ID / 别名")
    p_tools.add_argument("--json", action="store_true", help="输出 JSON")

    args = ap.parse_args(argv)
    try:
        if args.command == "version":
            print("%s %s" % (TOOL_NAME, VERSION))
            return 0

        if args.command == "locate":
            sources = discover_sources()
            if args.json:
                print(json.dumps({
                    "tool": TOOL_NAME, "version": VERSION,
                    "default_scope": default_scope(),
                    "sources": _source_brief(sources),
                }, ensure_ascii=False, indent=2))
            elif sources:
                print(fmt_locate(sources))
            else:
                print("未发现已知日志 / 记忆源。")
                return 1
            return 0

        if args.command == "scan":
            sources = resolve_sources(args)
            res = scan_all(sources, limit=args.limit)
            res["sources"] = _source_brief(sources)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(fmt_scan(res))
            return 0 if res["rows"] else 1

        if args.command == "search":
            sources = resolve_sources(args)
            res = search_all(
                sources, args.query, regex=args.regex, date=args.date,
                sessions=args.session, role=args.role, limit=args.limit,
                context=args.context, no_redact=args.no_redact)
            if args.json:
                print(json.dumps({
                    "command": "search",
                    "tool": TOOL_NAME,
                    "version": VERSION,
                    "query": args.query,
                    "regex": args.regex,
                    "sources": _source_brief(sources),
                    "total_matches": len(res["matches"]),
                    "sessions_hit": res["sessions_hit"],
                    "truncated": res["truncated"],
                    "matches": res["matches"],
                }, ensure_ascii=False, indent=2))
            else:
                print(fmt_search(res, args.query, sources, args.regex))
            return 0 if res["matches"] else 1

        if args.command == "session":
            sources = resolve_sources(args)
            res = extract_all(sources, args.sid, role=args.role,
                              with_tools=args.tools,
                              no_redact=args.no_redact)
            if args.limit > 0:
                res["messages"] = res["messages"][:args.limit]
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(fmt_session(res))
            return 0

        if args.command == "stats":
            sources = resolve_sources(args)
            res = stats_all(sources, session_id=args.session, daily=args.daily)
            if args.json:
                print(json.dumps(res, ensure_ascii=False, indent=2))
            else:
                print(fmt_stats(res, args.daily))
            return 0 if res["sessions"] else 1

        if args.command == "tools":
            sources = resolve_sources(args)
            items = tools_all(sources, session_id=args.session)
            if args.json:
                print(json.dumps({
                    "command": "tools",
                    "tool": TOOL_NAME,
                    "version": VERSION,
                    "sources": _source_brief(sources),
                    "tools": [{"name": n, "count": c} for n, c in items],
                }, ensure_ascii=False, indent=2))
            else:
                print(fmt_tools(items))
            return 0
    except BrokenPipeError:
        # 管道被提前关闭（如 scan | head）：静默收尾，不算错误
        try:
            sys.stdout.close()
        except Exception:
            pass
        return 0
    except SystemExit as e:
        code = e.code if isinstance(e.code, int) else 4
        msg = e.code if isinstance(e.code, str) else None
        if msg:
            print(msg, file=sys.stderr)
        return code if code in (0, 4) else 4
    except Exception as e:  # noqa: BLE001
        print("错误：%s" % e, file=sys.stderr)
        return 4
    return 4


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit:
        raise
