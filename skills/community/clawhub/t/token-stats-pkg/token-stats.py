#!/usr/bin/env python3
"""
token-stats — 选个 Agent 看它的 token 消耗

用法:
  token-stats                    交互式菜单：选 Agent → 看统计
  token-stats -b hermes          直接查看 Hermes
  token-stats --watch            交互式菜单 → 实时监控
  token-stats --all              查看本机所有 Agent 的统计
  token-stats -b hermes --now    同默认（显式快照）

  时间段查询:
  token-stats -b hermes --today
  token-stats -b hermes --yesterday
  token-stats -b hermes --week
  token-stats -b hermes --last-7d
  token-stats -b hermes --from 2025-01-01 --to 2025-01-31

  导出:
  token-stats -b hermes --export
  token-stats -b hermes --today --export

  对比:
  token-stats -b hermes --compare --a today --b yesterday
  token-stats -b hermes --compare --a this-week --b last-week
  token-stats -b hermes --compare --a 2025-01-01 --b 2025-01-15
  token-stats -b hermes --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14

  详细模式:
  token-stats -b hermes --detail

安装:
  clawhub install agent-usage-stats
  token-stats setup              创建 ~/.local/bin/token-stats
"""

import argparse
import csv
import json
import os
import re
import signal
import sqlite3
import sys
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

VERSION = "2.0.9"

# 强制 stdout 行缓冲，使 --watch 模式的输出实时可见
sys.stdout.reconfigure(line_buffering=True)


# ═══════════════════════════════════════════════════
#  工具函数
# ═══════════════════════════════════════════════════

def fmt_num(n: int) -> str:
    if abs(n) < 1000:
        return str(n)
    elif abs(n) < 1_000_000:
        return f"{n/1000:.1f}K"
    else:
        return f"{n/1_000_000:.2f}M"


def fmt_pct(pct: float) -> str:
    if pct >= 100:
        return ">100%"
    elif pct >= 90:
        return f"{pct:.1f}% 🚨"
    elif pct >= 60:
        return f"{pct:.1f}% ⚠️"
    else:
        return f"{pct:.1f}% ✅"


MODEL_CONTEXT_MAP = {
    "deepseek-v4-flash": 1_048_576,
    "deepseek-v4": 1_048_576,
    "deepseek-chat": 1_048_576,
    "deepseek-reasoner": 1_048_576,
    "deepseek-v3": 131_072,
    "gpt-4o": 131_072,
    "gpt-4o-mini": 131_072,
    "claude-sonnet-4": 204_800,
    "claude-opus-4": 204_800,
    "claude-haiku-3.5": 204_800,
    "gemini-2.5-pro": 1_048_576,
    "gemini-2.0-flash": 1_048_576,
    "qwen3": 131_072,
    "qwen-plus": 131_072,
    "llama-3.1": 131_072,
    "mistral-large": 131_072,
}

DEFAULT_CONTEXT = 131_072


def detect_context(model_name: str) -> int:
    if not model_name:
        return DEFAULT_CONTEXT
    m = model_name.lower().strip()
    if m in MODEL_CONTEXT_MAP:
        return MODEL_CONTEXT_MAP[m]
    for key, val in sorted(MODEL_CONTEXT_MAP.items(), key=lambda x: -len(x[0])):
        if m.startswith(key):
            return val
    return DEFAULT_CONTEXT


def parse_date(s: str) -> tuple:
    """Parse 'YYYY-MM-DD' → (start_ts, end_ts)"""
    dt = datetime.strptime(s.strip(), "%Y-%m-%d")
    start = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    end = dt.replace(hour=23, minute=59, second=59, microsecond=0)
    return start.timestamp(), end.timestamp()


def parse_time_label(label: str) -> tuple:
    """Parse a time label → (start_ts, end_ts).

    Supports:
      today, yesterday, this-week / week, last-week, last-7d
      YYYY-MM-DD (single day)
      YYYY-MM-DD~YYYY-MM-DD (date range)
    """
    s = label.strip().lower()
    now = datetime.now()

    if s == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "yesterday":
        d = now - timedelta(days=1)
        start = d.replace(hour=0, minute=0, second=0, microsecond=0)
        end = d.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s in ("this-week", "week"):
        monday = now - timedelta(days=now.weekday())
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    if s == "last-week":
        monday = now - timedelta(days=now.weekday() + 7)
        sunday = monday + timedelta(days=6)
        start = monday.replace(hour=0, minute=0, second=0, microsecond=0)
        end = sunday.replace(hour=23, minute=59, second=59, microsecond=0)
        return start.timestamp(), end.timestamp()

    if s == "last-7d":
        start = (now - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        return start.timestamp(), now.timestamp()

    # Date range: YYYY-MM-DD~YYYY-MM-DD
    if "~" in s:
        parts = s.split("~", 1)
        start_ts, _ = parse_date(parts[0])
        _, end_ts = parse_date(parts[1])
        return start_ts, end_ts

    # Single date
    return parse_date(s)


def format_model_line(model_name: str, inp: int, out: int, cache: int, calls: int,
                      context_window: int = None, session_count: int = None,
                      extra: str = None) -> str:
    """单行模型输出格式。若全为 0 则返回空字符串。"""
    if inp == 0 and out == 0 and cache == 0 and calls == 0:
        return ""

    parts = []
    total = inp + out
    if context_window:
        pct = round(total / context_window * 100, 1) if context_window else 0
        parts.append(f"上下文 {fmt_num(total)}/{fmt_num(context_window)} ({fmt_pct(pct)})")
    if inp > 0 or out > 0 or total > 0:
        if not context_window:
            parts.append(f"总计 {fmt_num(total)}")
        parts.append(f"输入 {fmt_num(inp)}")
        parts.append(f"输出 {fmt_num(out)}")
    if cache > 0:
        parts.append(f"缓存 {fmt_num(cache)}")
    if calls > 0 and (not session_count or session_count != calls):
        parts.append(f"调用 {calls} 次")
    elif calls > 0 and session_count == calls and total == 0:
        # 无 token 数据时，不重复显示 "调用 N 次" 和 "N 轮会话"
        pass
    elif calls > 0:
        parts.append(f"调用 {calls} 次")
    if session_count:
        parts.append(f"{session_count} 轮会话")
    if extra:
        parts.append(extra)
    if not parts:
        parts.append("无数据")
    return f"  {model_name} | {' | '.join(parts)}"


# ═══════════════════════════════════════════════════
#  Agent 基类与数据模型
# ═══════════════════════════════════════════════════

@dataclass
class AgentData:
    """单个 Agent 的统计数据"""
    name: str
    display_name: str
    stats: dict
    raw: str
    per_model: list = None  # [{"model": ..., "input": N, "output": N, "calls": N, "cache": N}, ...]


class BaseAgent(ABC):
    """Agent 检测器基类"""

    @staticmethod
    @abstractmethod
    def name() -> str: ...

    @staticmethod
    @abstractmethod
    def display_name() -> str: ...

    @staticmethod
    @abstractmethod
    def detect() -> bool: ...

    @abstractmethod
    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData: ...

    def watch(self, interval: int = 5) -> None:
        """实时监控模式"""
        stop_event = threading.Event()

        def _on_signal(sig, frame):
            stop_event.set()

        signal.signal(signal.SIGINT, _on_signal)
        signal.signal(signal.SIGTERM, _on_signal)

        def _interruptible_sleep(seconds: float) -> bool:
            """中断式睡眠，返回 False 表示被中断"""
            return not stop_event.wait(timeout=seconds)

        watch_start = time.time()
        print(f"\n📡 实时监控 [{self.display_name()}] — 每 {interval} 秒刷新 (Ctrl+C 停止)\n")

        # ── 首次基线 ──
        data_first = self.collect()
        bl_models = {}
        if data_first.per_model:
            for pm in data_first.per_model:
                bl_models[pm["model"]] = {
                    "input": pm.get("input", 0),
                    "output": pm.get("output", 0),
                    "calls": pm.get("calls", 0),
                    "cache": pm.get("cache", 0),
                }
        else:
            m = data_first.stats.get("model", "?")
            bl_models[m] = {
                "input": data_first.stats.get("input_tokens", 0),
                "output": data_first.stats.get("output_tokens", 0),
                "calls": data_first.stats.get("api_calls", 0),
                "cache": data_first.stats.get("cache_read", 0),
            }

        # ── 初始状态 ──
        print("初始状态:")
        for mn, mv in bl_models.items():
            cw = detect_context(mn)
            line = format_model_line(mn, mv["input"], mv["output"],
                                     mv.get("cache", 0), mv.get("calls", 0),
                                     context_window=cw)
            if line:
                print(line)
        print()

        # ── 监控循环 ──
        while not stop_event.is_set():
            tick_start = time.monotonic()
            if not _interruptible_sleep(interval):
                break
            if stop_event.is_set():
                break
            try:
                data = self.collect()
            except Exception as e:
                print(f"  ⚠️ {e}")
                continue

            now_models = {}
            if data.per_model:
                for pm in data.per_model:
                    now_models[pm["model"]] = {
                        "input": pm.get("input", 0),
                        "output": pm.get("output", 0),
                        "calls": pm.get("calls", 0),
                        "cache": pm.get("cache", 0),
                    }
            else:
                m = data.stats.get("model", "?")
                now_models[m] = {
                    "input": data.stats.get("input_tokens", 0),
                    "output": data.stats.get("output_tokens", 0),
                    "calls": data.stats.get("api_calls", 0),
                    "cache": data.stats.get("cache_read", 0),
                }

            # 对比上一次状态，列出增量
            changed_models = []
            total_delta_tok = 0
            total_delta_calls = 0
            for mn, mv in now_models.items():
                bl = bl_models.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
                d_in = mv["input"] - bl["input"]
                d_out = mv["output"] - bl["output"]
                d_calls = mv["calls"] - bl["calls"]
                d_cache = mv["cache"] - bl["cache"]
                d_tok = d_in + d_out
                if d_tok > 0 or d_calls > 0 or d_cache > 0:
                    changed_models.append((mn, d_in, d_out, d_tok, d_calls, d_cache))
                    total_delta_tok += d_tok
                    total_delta_calls += d_calls
                elif d_tok < 0 or d_calls < 0:
                    bl_models[mn] = mv

            # 每个 tick 都输出（有变化显示变化，无变化也显示一行）
            ts = datetime.now().strftime("%H:%M:%S")
            if changed_models:
                print(f"── [{ts}] +{fmt_num(total_delta_tok)} tokens ({total_delta_calls} calls) ──")
                for mn, d_in, d_out, d_tok, d_calls, d_cache in changed_models:
                    parts = [f"+{fmt_num(d_tok)} tokens"]
                    if d_in:
                        parts.append(f"+{fmt_num(d_in)} 输入")
                    if d_out:
                        parts.append(f"+{fmt_num(d_out)} 输出")
                    if d_cache:
                        parts.append(f"+{fmt_num(d_cache)} 缓存")
                    print(f"  {mn} | {' | '.join(parts)} | {d_calls} calls")
                    bl_models[mn] = mv
            else:
                print(f"── [{ts}] 无变化 ──")

            # 精确间隔补偿
            elapsed = time.monotonic() - tick_start
            if elapsed < interval and not stop_event.is_set():
                _interruptible_sleep(interval - elapsed)

        # ── 停止汇总：用时间段查询展示完整监控数据 ──
        watch_end = time.time()
        print()
        print("━" * 60)
        print("  📊 本次监控汇总")
        print("━" * 60)
        try:
            summary = self.collect(from_ts=watch_start, to_ts=watch_end)
            if summary.stats:
                print(summary.raw)
            else:
                print("  监控期间无数据")
        except Exception as e:
            print(f"  ⚠️ 获取汇总失败: {e}")
        print("👋 监控已停止")


# ═══════════════════════════════════════════════════
#  Hermes
# ═══════════════════════════════════════════════════

HERMES_DB = os.path.expanduser("~/.hermes/state.db")
HERMES_SESSIONS_FILE = os.path.expanduser("~/.hermes/sessions/sessions.json")


def _hermes_current_session_id() -> str | None:
    """从 sessions.json 读取当前活跃会话 ID。"""
    try:
        with open(HERMES_SESSIONS_FILE, encoding="utf-8") as f:
            data = json.load(f)
        # sessions.json 可能是一个 dict，key 是 platform:chat_id
        # 也可能是有特定结构的 dict
        if not isinstance(data, dict):
            return None
        # 找到第一个有 session_id 的条目
        for key, val in data.items():
            if isinstance(val, dict) and val.get("session_id"):
                return val["session_id"]
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return None


class HermesAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "hermes"

    @staticmethod
    def display_name() -> str:
        return "Hermes"

    @staticmethod
    def detect() -> bool:
        return os.path.exists(HERMES_DB)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        conn = sqlite3.connect(HERMES_DB)
        conn.row_factory = sqlite3.Row

        if from_ts is not None or to_ts is not None:
            # ── 时间段统计 ──
            where = []
            params = []
            if from_ts is not None:
                where.append("started_at >= ?")
                params.append(from_ts)
            if to_ts is not None:
                where.append("started_at <= ?")
                params.append(to_ts)
            clause = " AND ".join(where)

            cur = conn.execute(
                f"SELECT model, SUM(input_tokens) as inp, SUM(output_tokens) as out, "
                f"SUM(cache_read_tokens) as cache, SUM(api_call_count) as calls, "
                f"SUM(tool_call_count) as tools, COUNT(*) as cnt "
                f"FROM sessions WHERE {clause} GROUP BY model",
                params
            )
            rows = cur.fetchall()
            conn.close()

            if not rows:
                return AgentData(
                    name="hermes", display_name="Hermes",
                    stats={}, raw="Hermes: 该时间段内无会话记录"
                )

            total_inp = sum(r["inp"] or 0 for r in rows)
            total_out = sum(r["out"] or 0 for r in rows)
            total_cache = sum(r["cache"] or 0 for r in rows)
            total_calls = sum(r["calls"] or 0 for r in rows)
            total_sessions = sum(r["cnt"] or 0 for r in rows)

            per_model_list = []
            raw_lines = ["📊 Hermes"]
            for r in rows:
                m = r["model"] or "unknown"
                inp = r["inp"] or 0
                out = r["out"] or 0
                cache = r["cache"] or 0
                calls = r["calls"] or 0
                cnt = r["cnt"] or 0
                per_model_list.append({"model": m, "input": inp, "output": out,
                                        "calls": calls, "cache": cache})
                line = format_model_line(m, inp, out, cache, calls, session_count=cnt)
                if line:
                    raw_lines.append(line)

            raw = "\n".join(raw_lines)

            stats = {
                "model": ", ".join(r["model"] or "unknown" for r in rows),
                "input_tokens": total_inp,
                "output_tokens": total_out,
                "cache_read": total_cache,
                "api_calls": total_calls,
                "total_tokens": total_inp + total_out,
                "session_count": total_sessions,
            }

            return AgentData(name="hermes", display_name="Hermes",
                             stats=stats, raw=raw, per_model=per_model_list)

        # ── 当前会话 ──
        # 优先从 sessions.json 获取当前活跃会话 ID，精确查询
        current_id = _hermes_current_session_id()
        if current_id:
            cur = conn.execute(
                "SELECT id, model, input_tokens, output_tokens, cache_read_tokens, "
                "api_call_count, tool_call_count, title "
                "FROM sessions WHERE id = ?",
                (current_id,)
            )
        else:
            cur = conn.execute(
                "SELECT id, model, input_tokens, output_tokens, cache_read_tokens, "
                "api_call_count, tool_call_count, title "
                "FROM sessions ORDER BY started_at DESC LIMIT 1"
            )
        row = cur.fetchone()

        if not row:
            conn.close()
            return AgentData(
                name="hermes", display_name="Hermes",
                stats={}, raw="Hermes: 尚无会话记录"
            )

        model = row["model"] or "unknown"
        inp = row["input_tokens"] or 0
        out = row["output_tokens"] or 0
        cache = row["cache_read_tokens"] or 0
        calls = row["api_call_count"] or 0
        tools = row["tool_call_count"] or 0
        title = row["title"] or "无标题"

        cur2 = conn.execute("SELECT COUNT(*) as cnt FROM sessions")
        session_count = cur2.fetchone()["cnt"]
        conn.close()

        cw = detect_context(model)

        per_model_list = [{"model": model, "input": inp, "output": out,
                           "calls": calls, "cache": cache}]
        line = format_model_line(model, inp, out, cache, calls,
                                 context_window=cw,
                                 extra=f"第 {session_count} 轮 \"{title}\"")
        raw = "📊 Hermes" + ("\n" + line if line else "")

        stats = {
            "model": model,
            "input_tokens": inp,
            "output_tokens": out,
            "cache_read": cache,
            "api_calls": calls,
            "tool_calls": tools,
            "context_window": cw,
            "context_pct": round((inp + out) / cw * 100, 1) if cw else 0,
            "total_tokens": inp + out,
            "session_count": session_count,
            "title": title,
        }

        return AgentData(name="hermes", display_name="Hermes",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  Claude Code
# ═══════════════════════════════════════════════════

CLAUDE_DIR = os.path.expanduser("~/.claude")


class ClaudeCodeAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "claude-code"

    @staticmethod
    def display_name() -> str:
        return "Claude Code"

    @staticmethod
    def detect() -> bool:
        return os.path.isdir(os.path.join(CLAUDE_DIR, "projects"))

    def _find_sessions(self, from_ts: float = None, to_ts: float = None):
        projects_dir = os.path.join(CLAUDE_DIR, "projects")
        if not os.path.isdir(projects_dir):
            return []
        sessions = []
        for proj in os.listdir(projects_dir):
            proj_dir = os.path.join(projects_dir, proj)
            if not os.path.isdir(proj_dir):
                continue
            for fname in os.listdir(proj_dir):
                if fname.endswith(".jsonl") and not fname.endswith(".trajectory.jsonl"):
                    fpath = os.path.join(proj_dir, fname)
                    mtime = os.path.getmtime(fpath)
                    if from_ts is not None and mtime < from_ts:
                        continue
                    if to_ts is not None and mtime > to_ts:
                        continue
                    sessions.append((proj, fname, fpath))
        return sorted(sessions, key=lambda x: os.path.getmtime(x[2]), reverse=True)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        sessions = self._find_sessions(from_ts, to_ts)
        if not sessions:
            return AgentData(
                name="claude-code", display_name="Claude Code",
                stats={}, raw="Claude Code: 尚无会话记录"
            )

        per_model_data = {}
        total_sub = 0
        project_names = set()

        for proj, fname, fpath in sessions:
            project_names.add(proj)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            msg = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if msg.get("type") == "assistant":
                            model = msg.get("message", {}).get("model") or msg.get("model", "unknown")
                            if model.startswith("<"):
                                model = "subagent"
                            if model not in per_model_data:
                                per_model_data[model] = {"input": 0, "output": 0, "calls": 0, "cache": 0}
                            usage = msg.get("message", {}).get("usage") or msg.get("usage", {})
                            per_model_data[model]["input"] += usage.get("input_tokens", 0)
                            per_model_data[model]["output"] += usage.get("output_tokens", 0)
                            per_model_data[model]["cache"] += usage.get("cache_read_input_tokens", 0)
                            per_model_data[model]["calls"] += 1
                        if msg.get("toolUseResult") and "usage" in msg["toolUseResult"]:
                            total_sub += 1
            except Exception:
                continue

        if not per_model_data:
            return AgentData(
                name="claude-code", display_name="Claude Code",
                stats={}, raw="Claude Code: 会话文件中未解析到有效数据"
            )

        total_calls = sum(d["calls"] for d in per_model_data.values())
        total_input = sum(d["input"] for d in per_model_data.values())
        total_output = sum(d["output"] for d in per_model_data.values())
        total_cache = sum(d["cache"] for d in per_model_data.values())
        models_sorted = sorted(per_model_data.keys())

        # 过滤掉无效模型（input+output=0，无实际数据）
        meaningful_models = [
            mn for mn in models_sorted
            if per_model_data[mn]["input"] + per_model_data[mn]["output"] > 0
        ]

        per_model_list = []
        for mn in meaningful_models:
            md = per_model_data[mn]
            per_model_list.append({
                "model": mn,
                "input": md["input"],
                "output": md["output"],
                "calls": md["calls"],
                "cache": md["cache"],
            })

        raw_lines = ["📊 Claude Code"]
        for mn in meaningful_models:
            md = per_model_data[mn]
            cw = detect_context(mn)
            line = format_model_line(
                mn, md["input"], md["output"], md["cache"], md["calls"],
                context_window=cw,
                extra=f"子代理 {total_sub}" if total_sub > 0 and len(meaningful_models) <= 3 else None
            )
            if line:
                raw_lines.append(line)
        raw_lines.append(f"  ────────────────────────────────────")
        raw_lines.append(f"  子代理: {total_sub} 次 | 会话: {len(sessions)} 个 | 项目: {len(project_names)} 个")
        raw = "\n".join(raw_lines)

        stats = {
            "model": ", ".join(models_sorted),
            "input_tokens": total_input,
            "output_tokens": total_output,
            "cache_read": total_cache,
            "api_calls": total_calls,
            "sub_calls": total_sub,
            "total_tokens": total_input + total_output,
            "session_count": len(sessions),
            "projects": len(project_names),
        }

        return AgentData(name="claude-code", display_name="Claude Code",
                         stats=stats, raw=raw, per_model=per_model_list)


# ═══════════════════════════════════════════════════
#  CodeX
# ═══════════════════════════════════════════════════

def _find_codex_db() -> Optional[str]:
    codex_dir = os.path.expanduser("~/.codex")
    if not os.path.isdir(codex_dir):
        return None
    dbs = sorted(
        [f for f in os.listdir(codex_dir) if re.match(r'^state_\d+\.sqlite$', f)],
        reverse=True
    )
    return os.path.join(codex_dir, dbs[0]) if dbs else None


class CodeXAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "codex"

    @staticmethod
    def display_name() -> str:
        return "CodeX"

    @staticmethod
    def detect() -> bool:
        return _find_codex_db() is not None

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        db = _find_codex_db()
        if not db:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw="CodeX: 未检测到数据库文件"
            )
        try:
            conn = sqlite3.connect(db)
            conn.row_factory = sqlite3.Row

            if from_ts is not None or to_ts is not None:
                where = []
                params = []
                if from_ts is not None:
                    where.append("created_at >= ?")
                    params.append(int(from_ts))
                if to_ts is not None:
                    where.append("created_at <= ?")
                    params.append(int(to_ts))
                clause = " AND ".join(where)

                cur = conn.execute(
                    f"SELECT model, model_provider, SUM(tokens_used) as tokens, COUNT(*) as cnt "
                    f"FROM threads WHERE {clause} GROUP BY model, model_provider",
                    params
                )
                rows = cur.fetchall()
                conn.close()

                if not rows:
                    return AgentData(
                        name="codex", display_name="CodeX",
                        stats={}, raw="CodeX: 该时间段内无会话记录"
                    )

                per_model_list = []
                raw_lines = ["📊 CodeX"]
                total_tok = 0
                total_cnt = 0
                for r in rows:
                    model = r["model"] or r["model_provider"] or "codex-default"
                    ts = r["tokens"] or 0
                    cnt = r["cnt"] or 0
                    per_model_list.append({"model": model, "input": ts, "output": 0,
                                            "calls": cnt, "cache": 0})
                    line = format_model_line(model, ts, 0, 0, cnt, session_count=cnt)
                    if line:
                        raw_lines.append(line)
                    total_tok += ts
                    total_cnt += cnt

                raw = "\n".join(raw_lines)
                stats = {
                    "model": ", ".join(r["model"] or "unknown" for r in rows if r["model"]),
                    "total_tokens": total_tok,
                    "session_count": total_cnt,
                }
                return AgentData(name="codex", display_name="CodeX",
                                 stats=stats, raw=raw, per_model=per_model_list)

            # ── 默认：汇总所有线程（按模型） ──
            cur = conn.execute(
                "SELECT model, model_provider, SUM(tokens_used) as tokens, COUNT(*) as cnt "
                "FROM threads GROUP BY model, model_provider"
            )
            rows = cur.fetchall()

            cur2 = conn.execute("SELECT COUNT(*) as cnt FROM threads")
            total_sessions = cur2.fetchone()["cnt"] or 0
            conn.close()

            if not rows:
                return AgentData(
                    name="codex", display_name="CodeX",
                    stats={}, raw="CodeX: 尚无会话记录"
                )

            per_model_list = []
            raw_lines = ["📊 CodeX"]
            total_tok = 0
            for r in rows:
                model = r["model"] or r["model_provider"] or "codex-default"
                ts = r["tokens"] or 0
                cnt = r["cnt"] or 0
                per_model_list.append({"model": model, "input": ts, "output": 0,
                                        "calls": cnt, "cache": 0})
                line = format_model_line(model, ts, 0, 0, cnt, session_count=cnt)
                if line:
                    raw_lines.append(line)
                total_tok += ts

            if len(rows) == 1 and total_sessions > rows[0]["cnt"]:
                raw_lines[-1] = raw_lines[-1].rstrip() + f" | 共 {total_sessions} 次会话"

            raw = "\n".join(raw_lines)
            stats = {
                "model": ", ".join(r["model"] or "unknown" for r in rows if r["model"]),
                "total_tokens": total_tok,
                "session_count": total_sessions,
            }
            return AgentData(name="codex", display_name="CodeX",
                             stats=stats, raw=raw, per_model=per_model_list)

        except Exception as e:
            return AgentData(
                name="codex", display_name="CodeX",
                stats={}, raw=f"CodeX: 读取失败 — {e}"
            )


# ═══════════════════════════════════════════════════
#  OpenClaw
# ═══════════════════════════════════════════════════

OPENCLAW_DIR = os.path.expanduser("~/ai-testing-lab/openclaw/data")
OPENCLAW_SESSIONS = os.path.join(OPENCLAW_DIR, "agents", "main", "sessions", "sessions.json")


class OpenClawAgent(BaseAgent):
    @staticmethod
    def name() -> str:
        return "openclaw"

    @staticmethod
    def display_name() -> str:
        return "OpenClaw"

    @staticmethod
    def detect() -> bool:
        return os.path.exists(OPENCLAW_SESSIONS)

    def collect(self, *, from_ts: float = None, to_ts: float = None) -> AgentData:
        if not os.path.exists(OPENCLAW_SESSIONS):
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw="OpenClaw: 数据文件不存在"
            )
        try:
            with open(OPENCLAW_SESSIONS, encoding="utf-8") as f:
                data = json.load(f)

            agents = []
            if isinstance(data, dict):
                for agent_key, session in data.items():
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)
            elif isinstance(data, list):
                for session in data:
                    if isinstance(session, dict):
                        if from_ts is not None or to_ts is not None:
                            ts = session.get("startedAt", 0) or session.get("updatedAt", 0)
                            if from_ts is not None and ts < from_ts:
                                continue
                            if to_ts is not None and ts > to_ts:
                                continue
                        agents.append(session)

            if not agents:
                return AgentData(
                    name="openclaw", display_name="OpenClaw",
                    stats={}, raw="OpenClaw: 尚无会话" if from_ts is None else "OpenClaw: 该时间段内无会话"
                )

            total_input = sum(s.get("inputTokens", 0) for s in agents)
            total_output = sum(s.get("outputTokens", 0) for s in agents)
            total_cache = sum(s.get("cacheRead", 0) for s in agents)

            latest = max(agents, key=lambda s: s.get("startedAt", 0) or s.get("updatedAt", 0))
            model = latest.get("model", "unknown")
            provider = latest.get("modelProvider", "")
            model_display = f"{model}" if not provider else f"{model} ({provider})"
            context = latest.get("contextTokens", DEFAULT_CONTEXT)

            per_model_list = [{"model": model, "input": total_input, "output": total_output,
                               "calls": len(agents), "cache": total_cache}]

            if from_ts is not None or to_ts is not None:
                # 时间段模式：无上下文占比
                oline = format_model_line(
                    model_display, total_input, total_output, total_cache, len(agents),
                    session_count=len(agents)
                )
                raw = "📊 OpenClaw" + ("\n" + oline if oline else "")
                stats = {
                    "model": model,
                    "input_tokens": total_input,
                    "output_tokens": total_output,
                    "cache_read": total_cache,
                    "total_tokens": total_input + total_output,
                    "context_window": context,
                    "agent_count": len(agents),
                }
            else:
                # 当前模式：显示上下文占比
                cw = context
                oline = format_model_line(
                    model_display, total_input, total_output, total_cache, len(agents),
                    context_window=cw,
                    extra=f"{len(agents)} 个 Agent" if len(agents) > 1 else None
                )
                raw = "📊 OpenClaw" + ("\n" + oline if oline else "")
                stats = {
                    "model": model,
                    "input_tokens": total_input,
                    "output_tokens": total_output,
                    "cache_read": total_cache,
                    "total_tokens": total_input + total_output,
                    "context_window": cw,
                    "context_pct": round((total_input + total_output) / cw * 100, 1) if cw else 0,
                    "agent_count": len(agents),
                }

            return AgentData(name="openclaw", display_name="OpenClaw",
                             stats=stats, raw=raw, per_model=per_model_list)

        except Exception as e:
            return AgentData(
                name="openclaw", display_name="OpenClaw",
                stats={}, raw=f"OpenClaw: 读取失败 — {e}"
            )


# ═══════════════════════════════════════════════════
#  Agent 注册表
# ═══════════════════════════════════════════════════

ALL_AGENTS: list[type[BaseAgent]] = [
    HermesAgent,
    ClaudeCodeAgent,
    CodeXAgent,
    OpenClawAgent,
]


def detect_installed() -> list[type[BaseAgent]]:
    return [cls for cls in ALL_AGENTS if cls.detect()]


def get_agent(name: str) -> BaseAgent:
    for cls in ALL_AGENTS:
        if cls.name() == name.lower().strip():
            return cls()
    raise ValueError(f"不支持的 Agent: {name}")


# ═══════════════════════════════════════════════════
#  交互式菜单
# ═══════════════════════════════════════════════════

def show_menu(installed: list[type[BaseAgent]]) -> BaseAgent:
    print("\n🔍 选择你要查看的 AI 助手：")
    print("─" * 40)
    for i, cls in enumerate(installed, 1):
        print(f"  [{i}] {cls.display_name()}")
    print("  [q] 退出")
    print("─" * 40)

    while True:
        try:
            choice = input("请选择 (1-{})：".format(len(installed))).strip().lower()
            if choice == "q":
                print("再见 👋")
                sys.exit(0)
            idx = int(choice) - 1
            if 0 <= idx < len(installed):
                return installed[idx]()
            print(f"请输入 1-{len(installed)} 或 q")
        except (ValueError, EOFError):
            print(f"请输入 1-{len(installed)} 或 q")


# ═══════════════════════════════════════════════════
#  导出
# ═══════════════════════════════════════════════════

def export_interactive(data: AgentData, agent: BaseAgent):
    """交互式导出统计"""
    try:
        # Step 1: 输入目录
        while True:
            dir_input = input("请输入导出目录路径: ").strip()
            if not dir_input or dir_input.lower() == "q":
                print("已取消导出")
                return
            dir_path = os.path.expanduser(dir_input)
            if os.path.isdir(dir_path):
                break
            print(f"⚠️ 目录不存在: {dir_path}")
            print("请确保目录存在，或输入 q 取消")

        # Step 2: 选择格式
        print("\n选择导出格式:")
        print("  [1] JSON")
        print("  [2] CSV")
        fmt_choice = input("请选择 (1/2): ").strip().lower()

        if fmt_choice in ("1", "json"):
            fmt = "json"
        elif fmt_choice in ("2", "csv"):
            fmt = "csv"
        else:
            print(f"⚠️ 不支持格式 '{fmt_choice}'，默认使用 JSON")
            fmt = "json"

        # Step 3: 写文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"token-stats_{agent.name()}_{timestamp}.{fmt}"
        filepath = os.path.join(dir_path, filename)

        if fmt == "json":
            export_data = {
                "tool": "token-stats",
                "version": VERSION,
                "agent": agent.name(),
                "agent_display": agent.display_name(),
                "exported_at": datetime.now().isoformat(),
                "stats": data.stats,
                "per_model": data.per_model or [],
            }
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
        else:
            with open(filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["模型", "输入tokens", "输出tokens", "缓存tokens", "调用次数"])
                for pm in (data.per_model or []):
                    writer.writerow([
                        pm.get("model", "unknown"),
                        pm.get("input", 0),
                        pm.get("output", 0),
                        pm.get("cache", 0),
                        pm.get("calls", 0),
                    ])

        print(f"✅ 已导出到: {filepath}")
    except KeyboardInterrupt:
        print()
        print("已取消导出")


# ═══════════════════════════════════════════════════
#  对比
# ═══════════════════════════════════════════════════

def run_compare(agent: BaseAgent, a_label: str, b_label: str):
    """对比两个时间段的统计"""
    a_start, a_end = parse_time_label(a_label)
    b_start, b_end = parse_time_label(b_label)

    data_a = agent.collect(from_ts=a_start, to_ts=a_end)
    data_b = agent.collect(from_ts=b_start, to_ts=b_end)

    models_a = {pm["model"]: pm for pm in (data_a.per_model or [])}
    models_b = {pm["model"]: pm for pm in (data_b.per_model or [])}
    all_models = sorted(set(list(models_a.keys()) + list(models_b.keys())))

    if not all_models:
        print("两个时间段均无数据")
        return

    print(f"\n📊 对比: \"{a_label}\" vs \"{b_label}\"  [{agent.display_name()}]")
    # 列宽根据标签长度自适应
    label_w = max(len(b_label), 12) if len(b_label) > len(a_label) else max(len(a_label), 12)
    col_model = 28      # 模型列宽（不含前导空格）
    col_delta = 12      # 变化列宽
    sep = 3             # " | " 分隔符宽度
    leading = 2         # "  " 前导空格
    total_w = leading + col_model + sep + label_w + sep + label_w + sep + col_delta
    print("═" * total_w)
    print(f"  {'模型':<{col_model}} | {a_label:>{label_w}} | {b_label:>{label_w}} | {'变化':>{col_delta}}")
    print("─" * total_w)

    total_a, total_b = 0, 0
    model_count = 0
    for mn in all_models:
        ma = models_a.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        mb = models_b.get(mn, {"input": 0, "output": 0, "calls": 0, "cache": 0})
        ta = ma["input"] + ma["output"]
        tb = mb["input"] + mb["output"]
        # 跳过两侧均为 0 的模型
        if ta == 0 and tb == 0:
            continue
        total_a += ta
        total_b += tb
        delta = tb - ta
        delta_str = f"+{fmt_num(delta)}" if delta > 0 else fmt_num(delta) if delta < 0 else "0"
        print(f"  {mn:<{col_model}} | {fmt_num(ta):>{label_w}} | {fmt_num(tb):>{label_w}} | {delta_str:>{col_delta}}")
        model_count += 1

    if model_count == 0:
        print("  (两侧均无有效数据)")
        print()
        return

    print("─" * total_w)
    total_delta = total_b - total_a
    total_delta_str = f"+{fmt_num(total_delta)}" if total_delta > 0 else fmt_num(total_delta) if total_delta < 0 else "0"
    print(f"  {'总计':<{col_model}} | {fmt_num(total_a):>{label_w}} | {fmt_num(total_b):>{label_w}} | {total_delta_str:>{col_delta}}")
    print()


# ═══════════════════════════════════════════════════
#  全部统计 (--all)
# ═══════════════════════════════════════════════════

def show_all(*, from_ts: float = None, to_ts: float = None):
    """显示本机所有 Agent 的统计"""
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        return

    print("\n📊 本机 Agent 统计汇总")
    print("═" * 50)

    any_data = False
    for cls in ALL_AGENTS:
        detected = cls.detect()
        status = "✅" if detected else "❌"
        name = cls.display_name()
        print(f"\n{status} {name}")

        if detected:
            try:
                agent = cls()
                data = agent.collect(from_ts=from_ts, to_ts=to_ts)
                if data.stats:
                    any_data = True
                print(data.raw)
            except Exception as e:
                print(f"  ⚠️ 读取失败: {e}")
        else:
            print("  (未安装)")

    if not any_data:
        print("\n（所有 Agent 均无数据）")
    print()


# ═══════════════════════════════════════════════════
#  CLI 入口
# ═══════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="token-stats — 选个 Agent 看它的 token 消耗",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
命令大全:
  基础:
    token-stats                       交互式菜单选择 Agent → 查看统计
    token-stats -b <name>             直接指定 Agent: hermes/claude-code/codex/openclaw
    token-stats --version             显示版本号
    token-stats -b <name> --detail    详细模式（同默认）
    token-stats -b <name> --now       当前快照（同默认）

  快速时间段:
    token-stats -b <name> --today     今日统计
    token-stats -b <name> --yesterday 昨日统计
    token-stats -b <name> --week      本周统计（周一起）
    token-stats -b <name> --last-7d   最近 7 天
    token-stats -b <name> --from 2025-01-01 --to 2025-01-31  自定义时间段

  对比:
    token-stats -b <name> --compare --a today --b yesterday
        快捷标签对比
    token-stats -b <name> --compare --a 2025-01-01~2025-01-07 --b 2025-01-08~2025-01-14
        自定义时间段对比
    标签支持: today / yesterday / this-week / last-week / YYYY-MM-DD / YYYY-MM-DD~YYYY-MM-DD

  导出:
    token-stats -b <name> --export    导出当前统计（交互式选目录和格式）
    token-stats -b <name> --today --export  导出今日统计

  实时监控:
    token-stats -b <name> --watch     实时监控，每 5 秒刷新 (Ctrl+C 停止)
    token-stats -b <name> --watch 10  自定义间隔秒数
    停止后自动展示监控时间段内的完整统计数据（模型、输入、输出、缓存、调用次数）

  多 Agent:
    token-stats --all                 查看本机所有 Agent 统计
    token-stats --list-backends       列出已安装的 Agent

  安装:
    clawhub install agent-usage-stats  从 ClawHub 安装
    token-stats --setup                创建 ~/.local/bin/token-stats 全局命令
        """,
    )
    parser.add_argument("--version", action="store_true", help="显示版本号")
    parser.add_argument("--list-backends", action="store_true", help="列出本机已安装的 Agent")
    parser.add_argument("-b", "--backend", help="直接指定 Agent: hermes/claude-code/codex/openclaw")
    parser.add_argument("--watch", nargs="?", type=int, const=5, default=None, metavar="秒",
                        help="实时监控模式（默认每 5 秒轮询）")
    parser.add_argument("setup_pos", nargs="?", const=True, help=argparse.SUPPRESS)

    # 时间段
    parser.add_argument("--today", action="store_true", help="今日统计")
    parser.add_argument("--yesterday", action="store_true", help="昨日统计")
    parser.add_argument("--week", action="store_true", help="本周统计")
    parser.add_argument("--last-7d", action="store_true", help="最近 7 天统计")
    parser.add_argument("--from", dest="from_date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--to", dest="to_date", help="结束日期 (YYYY-MM-DD)")

    # 功能
    parser.add_argument("--export", nargs="?", const=True, default=None, metavar="目录",
                        help="导出统计（交互式选择目录和格式）")
    parser.add_argument("--compare", action="store_true", help="对比模式")
    parser.add_argument("--a", help="对比时间段 A（today/yesterday/this-week/last-week/日期/日期段）")
    parser.add_argument("--b", help="对比时间段 B")
    parser.add_argument("--detail", action="store_true", help="详细信息模式")
    parser.add_argument("--now", action="store_true", help="当前快照（同默认）")
    parser.add_argument("--all", action="store_true", help="查看本机所有 Agent 统计")
    parser.add_argument("--setup", action="store_true", help="创建 ~/.local/bin/token-stats")

    args = parser.parse_args()

    # 兼容旧用法：token-stats setup → 当作 --setup
    if args.setup_pos is True or args.setup_pos == "setup":
        args.setup = True

    # ── version ──
    if args.version:
        print(f"token-stats v{VERSION}")
        return

    # ── setup ──
    if args.setup:
        target = os.path.join(os.path.expanduser("~"), ".local", "bin", "token-stats")
        script_path = os.path.abspath(__file__)
        os.makedirs(os.path.dirname(target), exist_ok=True)

        wrapper = (
            "#!/bin/sh\n"
            f'exec python3 "{script_path}" "$@"\n'
        )
        with open(target, "w", encoding="utf-8") as f:
            f.write(wrapper)
        os.chmod(target, 0o755)

        print(f"✅ 已创建全局命令: {target}")
        print(f"   → 每次执行都调用: python3 {script_path}")

        for rc_file in ["~/.zshrc", "~/.bashrc", "~/.bash_profile"]:
            rc_path = os.path.expanduser(rc_file)
            if os.path.exists(rc_path):
                with open(rc_path, encoding="utf-8") as f:
                    content = f.read()
                alias_lines = []
                for i, line in enumerate(content.splitlines(), 1):
                    if "alias token-stats" in line.strip():
                        alias_lines.append(f"  {rc_file} 第 {i} 行: {line.strip()}")
                if alias_lines:
                    print()
                    print("⚠️  检测到旧的 alias，会覆盖全局命令，建议删除：")
                    for al in alias_lines:
                        print(al)
                    print("   删除方法: 手动编辑或用 sed 删除对应行，然后 source ~/.zshrc")

        bin_dir = os.path.dirname(target)
        if bin_dir not in os.environ.get("PATH", "").split(":"):
            print(f"⚠️  {bin_dir} 不在 PATH 中，请添加到 shell 配置:")
            print(f"   echo 'export PATH=\"$PATH:{bin_dir}\"' >> ~/.zshrc")
            print(f"   source ~/.zshrc")
        return

    # ── list-backends ──
    if args.list_backends:
        installed = detect_installed()
        print("\n本机已安装的 AI 助手：")
        for cls in ALL_AGENTS:
            ok = "✅" if cls.detect() else "❌"
            print(f"  {ok} {cls.display_name()}")
        print()
        return

    # ── 解析时间段参数 ──
    from_ts = None
    to_ts = None

    if args.from_date:
        if args.to_date:
            from_ts, _ = parse_date(args.from_date)
            _, to_ts = parse_date(args.to_date)
        else:
            from_ts, _ = parse_date(args.from_date)
            to_ts = from_ts + 86399  # end of that day
    elif args.to_date and not args.from_date:
        _, to_ts = parse_date(args.to_date)
        # no from_ts means "from beginning"

    if args.today:
        from_ts, to_ts = parse_time_label("today")
    elif args.yesterday:
        from_ts, to_ts = parse_time_label("yesterday")
    elif args.week:
        from_ts, to_ts = parse_time_label("this-week")
    elif args.last_7d:
        from_ts, to_ts = parse_time_label("last-7d")

    # ── --all (所有 Agent) ──
    if args.all:
        show_all(from_ts=from_ts, to_ts=to_ts)
        return

    # ── 选择 Agent ──
    installed = detect_installed()
    if not installed:
        print("❌ 本机未检测到任何支持的 AI 助手")
        print("   支持的 Agent: Hermes, Claude Code, CodeX, OpenClaw")
        print("   请先使用并运行一个 Agent 后再来查看统计。")
        return

    if args.backend:
        try:
            agent = get_agent(args.backend)
        except ValueError as e:
            print(f"❌ {e}")
            print(f"   可选: {', '.join(cls.name() for cls in ALL_AGENTS)}")
            return
    elif len(installed) == 1:
        agent = installed[0]()
        print(f"\n（本机仅安装了 {agent.display_name()}，直接显示统计）")
    else:
        agent = show_menu(installed)

    # ── --compare (对比) ──
    if args.compare:
        a_label = args.a
        b_label = args.b
        if not a_label or not b_label:
            print("❌ --compare 需要 --a 和 --b 参数")
            print("   示例: token-stats -b hermes --compare --a today --b yesterday")
            return
        run_compare(agent, a_label, b_label)
        return

    # ── --watch (实时监控) ──
    if args.watch is not None:
        agent.watch(args.watch)
        return

    # ── 收集并展示 ──
    try:
        data = agent.collect(from_ts=from_ts, to_ts=to_ts)
        print()
        print(data.raw)
        print()
    except Exception as e:
        print(f"❌ 获取 {agent.display_name()} 统计失败: {e}")
        return

    # ── --export (导出) ──
    if args.export:
        export_interactive(data, agent)

    # --detail 在下一步也可能有用，但当前 collect() 已含 per_model 详情
    # detail 主要用于 watch/collect 输出内容更丰富，当前 collect 实现已包含
    # 后续可通过 stats 或 per_model 扩展


if __name__ == "__main__":
    main()
