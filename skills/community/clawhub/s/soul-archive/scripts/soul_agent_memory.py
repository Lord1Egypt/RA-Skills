#!/usr/bin/env python3
"""
🧬 Soul Agent Memory

主动智能体记忆引擎。soul_reflect.py 是写入侧；本模块是「主动召回 + 主动预警 + 主动蒸馏」侧。

核心能力：
  1. 跨会话记忆检索（recall）
     - 给定当前任务文本，召回相关 patterns / corrections / reflections
     - 用关键词命中 + Jaccard 字符 n-gram 相似度做轻量级排序

  2. 失败模式预警（warn-on-match）
     - 检测当前任务是否匹配过去某个 correction（用户纠正过的行为）
     - 命中时输出"你上次在这里踩过坑"提醒

  3. 行为模式蒸馏（distill）
     - 当 reflections 累积到阈值（默认 5 条且尚未蒸馏）时
     - 输出待蒸馏内容供调用方喂给 LLM，再回写为新 pattern

用法：
  python3 soul_agent_memory.py recall --task "执行 git rebase 操作"
  python3 soul_agent_memory.py warn  --task "批量删除 Desktop 文件"
  python3 soul_agent_memory.py distill --pretend            # 预览待蒸馏内容
  python3 soul_agent_memory.py distill --commit "<新 pattern JSON>"  # 写回蒸馏结果
  python3 soul_agent_memory.py session-start --task "..."   # 一次性输出 recall+warn 综合简报
"""


# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from soul_reflect import AgentMemory, ReflectionBuilder, read_jsonl, append_jsonl  # noqa: E402


# ---------- 文本相似度 ----------

def _bigrams(s: str) -> set:
    s = (s or "").lower().strip()
    if len(s) < 2:
        return {s} if s else set()
    return {s[i:i + 2] for i in range(len(s) - 1)}


def _similarity(a: str, b: str) -> float:
    sa, sb = _bigrams(a), _bigrams(b)
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union > 0 else 0.0


def _score_entry(query: str, text: str, tags: list = None) -> float:
    """命中分 = 文本相似度 + 标签命中加成"""
    base = _similarity(query, text)
    bonus = 0.0
    if tags:
        q_lower = query.lower()
        for t in tags:
            if t and t.lower() in q_lower:
                bonus += 0.1
    return min(1.0, base + bonus)


# ---------- 主功能 ----------

def recall(soul_dir: Path, task: str, limit: int = 5,
           min_score: float = 0.15) -> dict:
    """对当前任务做跨会话召回。返回 patterns / corrections / reflections 三类相关条目。"""
    agent = AgentMemory(soul_dir)
    patterns = list(agent.load_patterns().values())
    corrections = read_jsonl(agent.agent_dir / "corrections.jsonl")
    reflections = read_jsonl(agent.agent_dir / "reflections.jsonl")

    pat_scored = []
    for p in patterns:
        text = " ".join(filter(None, [p.get("name"), p.get("pattern"),
                                       p.get("category")]))
        s = _score_entry(task, text, p.get("tags"))
        if s >= min_score:
            pat_scored.append((s, p))
    pat_scored.sort(key=lambda x: x[0], reverse=True)

    corr_scored = []
    for c in corrections:
        text = " ".join(filter(None, [c.get("trigger"), c.get("user_said"),
                                       c.get("what_i_did_wrong"),
                                       c.get("root_cause")]))
        s = _score_entry(task, text)
        if s >= min_score:
            corr_scored.append((s, c))
    corr_scored.sort(key=lambda x: x[0], reverse=True)

    refl_scored = []
    for r in reflections:
        text = " ".join(filter(None, [r.get("task"), r.get("lesson"),
                                       " ".join(r.get("what_went_wrong") or []),
                                       " ".join(r.get("what_went_well") or [])]))
        s = _score_entry(task, text)
        if s >= min_score:
            refl_scored.append((s, r))
    refl_scored.sort(key=lambda x: x[0], reverse=True)

    return {
        "task": task,
        "patterns": [{"score": round(s, 2), **p} for s, p in pat_scored[:limit]],
        "corrections": [{"score": round(s, 2), **c} for s, c in corr_scored[:limit]],
        "reflections": [{"score": round(s, 2), **r} for s, r in refl_scored[:limit]],
    }


def warn(soul_dir: Path, task: str, threshold: float = 0.4) -> dict:
    """检查当前任务是否高度匹配过去的 correction，命中则返回预警。"""
    agent = AgentMemory(soul_dir)
    corrections = read_jsonl(agent.agent_dir / "corrections.jsonl")
    hits = []
    for c in corrections:
        text = " ".join(filter(None, [c.get("trigger"),
                                       c.get("what_i_did_wrong"),
                                       c.get("root_cause")]))
        s = _similarity(task, text)
        if s >= threshold:
            hits.append({
                "score": round(s, 2),
                "what_i_did_wrong": c.get("what_i_did_wrong"),
                "correction": c.get("correction"),
                "user_said": c.get("user_said"),
                "severity": c.get("severity", "medium"),
                "timestamp": c.get("timestamp"),
            })
    hits.sort(key=lambda x: x["score"], reverse=True)
    return {
        "task": task,
        "warnings": hits[:5],
        "has_warnings": bool(hits),
    }


# ---------- 蒸馏 ----------

DISTILL_LOG = "distill_log.jsonl"


def _last_distill_index(soul_dir: Path) -> int:
    log_path = soul_dir / "agent" / DISTILL_LOG
    if not log_path.exists():
        return 0
    last = 0
    for entry in read_jsonl(log_path):
        last = max(last, entry.get("up_to_reflection_index", 0))
    return last


def _record_distill(soul_dir: Path, up_to: int, pattern_id: str = None):
    log_path = soul_dir / "agent" / DISTILL_LOG
    append_jsonl(log_path, {
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00"),
        "up_to_reflection_index": up_to,
        "produced_pattern": pattern_id,
    })


def distill_pending(soul_dir: Path, threshold: int = 5) -> dict:
    """检查是否有未蒸馏的 reflections 达到阈值，是则返回待蒸馏数据包。
    调用方可以把 pending 喂给 LLM，让它产出一条新的 pattern。
    """
    agent = AgentMemory(soul_dir)
    reflections = read_jsonl(agent.agent_dir / "reflections.jsonl")
    last_idx = _last_distill_index(soul_dir)
    new_count = len(reflections) - last_idx
    if new_count < threshold:
        return {
            "needs_distill": False,
            "new_reflection_count": max(0, new_count),
            "threshold": threshold,
            "message": f"暂不需要蒸馏（{new_count}/{threshold} 条新反思）",
        }
    pending = reflections[last_idx:]
    return {
        "needs_distill": True,
        "new_reflection_count": new_count,
        "threshold": threshold,
        "pending_reflections": pending,
        "up_to_reflection_index": len(reflections),
        "instruction": (
            "把 pending_reflections 喂给 LLM，让它输出一条 pattern：\n"
            "  {id, name, pattern, source='distilled', confidence(0~1), category, tags}\n"
            "再用 distill --commit '<json>' 写回。"
        )
    }


def distill_commit(soul_dir: Path, pattern_json: str, up_to: int = None) -> dict:
    """把 LLM 蒸馏出的 pattern 写回 agent/patterns.json，并记录蒸馏日志。"""
    agent = AgentMemory(soul_dir)
    try:
        pattern = json.loads(pattern_json)
    except json.JSONDecodeError as e:
        raise SystemExit(f"❌ pattern JSON 解析失败：{e}")
    pid = pattern.get("id")
    if not pid:
        raise SystemExit("❌ pattern 必须包含 id 字段")

    builder = ReflectionBuilder()
    builder.add_pattern(
        pid,
        pattern.get("name", pid),
        pattern.get("pattern", ""),
        source=pattern.get("source", "distilled"),
        confidence=float(pattern.get("confidence", 0.8)),
        category=pattern.get("category", "general"),
        tags=pattern.get("tags") or [],
    )
    agent.save_extraction(builder.build())

    if up_to is None:
        # 默认：把当前所有 reflections 标记为已蒸馏
        reflections = read_jsonl(agent.agent_dir / "reflections.jsonl")
        up_to = len(reflections)
    _record_distill(soul_dir, up_to, pid)

    return {"committed": True, "pattern_id": pid, "up_to_reflection_index": up_to}


# ---------- session-start 综合简报 ----------

def session_start_briefing(soul_dir: Path, task: str) -> dict:
    """会话开始时一次性输出：召回 + 预警 + 蒸馏待办。"""
    return {
        "recall": recall(soul_dir, task),
        "warn": warn(soul_dir, task),
        "distill": distill_pending(soul_dir),
    }


# ---------- CLI ----------

def main():
    from soul_paths import resolve_soul_dir
    default_soul_dir = resolve_soul_dir()
    parser = argparse.ArgumentParser(description="🧬 Soul Agent Memory — 主动智能体记忆")
    parser.add_argument("--soul-dir", type=Path, default=default_soul_dir)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_recall = sub.add_parser("recall", help="按当前任务召回相关模式/批评/反思")
    p_recall.add_argument("--task", required=True)
    p_recall.add_argument("--limit", type=int, default=5)
    p_recall.add_argument("--min-score", type=float, default=0.15)

    p_warn = sub.add_parser("warn", help="检测当前任务是否匹配过去的失败模式")
    p_warn.add_argument("--task", required=True)
    p_warn.add_argument("--threshold", type=float, default=0.4)

    p_dist = sub.add_parser("distill", help="蒸馏新的行为模式（先 --pretend 预览，再 --commit 提交）")
    p_dist.add_argument("--pretend", action="store_true", help="只输出待蒸馏内容，不修改文件")
    p_dist.add_argument("--commit", help="提交一个 pattern JSON（字符串）")
    p_dist.add_argument("--threshold", type=int, default=5)

    p_sess = sub.add_parser("session-start", help="会话开始：一次性输出召回+预警+蒸馏简报")
    p_sess.add_argument("--task", required=True)

    args = parser.parse_args()

    if args.cmd == "recall":
        out = recall(args.soul_dir, args.task,
                     limit=args.limit, min_score=args.min_score)
    elif args.cmd == "warn":
        out = warn(args.soul_dir, args.task, threshold=args.threshold)
    elif args.cmd == "distill":
        if args.commit:
            out = distill_commit(args.soul_dir, args.commit)
        else:
            out = distill_pending(args.soul_dir, threshold=args.threshold)
    elif args.cmd == "session-start":
        out = session_start_briefing(args.soul_dir, args.task)
    else:
        parser.print_help()
        sys.exit(1)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
