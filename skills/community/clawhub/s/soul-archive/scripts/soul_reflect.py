#!/usr/bin/env python3
"""
🧬 Soul Archive -- AI Self-Improvement Engine (soul_reflect.py)

AI 自我反思、自我批评、自我学习引擎（写入侧）。
查询/召回/预警/蒸馏 等"主动智能体记忆"能力请使用 soul_agent_memory.py。

条目生命周期（v3.2.0+，借鉴 self-improving-agent 实践）：
  每条 correction / reflection 自动获得稳定 ID（COR-YYYYMMDD-XXX /
  RFL-YYYYMMDD-XXX）+ status（pending → resolved / promoted / wont_fix）。
  新增 correction 时自动做复现检测：命中同 pattern 或高相似历史条目 →
  recurrence_count +1、see_also 链接、priority 自动升级。
  recurrence_count ≥ 3 的教训应晋升（promote）为行为模式 / agent 共享记忆。


默认数据目录：~/.agent-guild/skills_data/soul-archive/（agent/ 子目录）

Usage:
  python3 soul_reflect.py --mode reflect --input "<反思内容>"
  python3 soul_reflect.py --mode critique --input "<批评内容>"
  python3 soul_reflect.py --mode learn --input "<学习内容>"
  python3 soul_reflect.py --mode status
  python3 soul_reflect.py --mode patterns
  python3 soul_reflect.py --mode review                 # pending 概览 + 高优先级清单
  python3 soul_reflect.py --mode resolve --id COR-20260818-001 --notes "<修复说明>"

Works on: macOS, Linux, Windows
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


def load_json(path: Path, default=None):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            pass
    return default if default is not None else {}


def save_json(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, entry: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


def read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


# ============================================================
# Entry lifecycle helpers (v3.2.0+, borrowed from self-improving-agent)
# ============================================================

_SEVERITY_TO_PRIORITY = {"critical": "critical", "high": "high",
                         "medium": "medium", "low": "low"}
_PRIORITY_LADDER = ["low", "medium", "high", "critical"]


def _next_id(prefix: str, existing_entries: list) -> str:
    """Generate TYPE-YYYYMMDD-XXX, sequentially unique within one day."""
    day = datetime.now().strftime("%Y%m%d")
    same_day = 0
    for e in existing_entries:
        eid = e.get("id", "")
        if eid.startswith(f"{prefix}-{day}-"):
            try:
                same_day = max(same_day, int(eid.rsplit("-", 1)[1]))
            except (ValueError, IndexError):
                continue
    return f"{prefix}-{day}-{same_day + 1:03d}"


def _bigrams(s: str) -> set:
    s = "".join(s.split()).lower()
    return {s[i:i + 2] for i in range(len(s) - 1)} if len(s) > 1 else {s}


def _similarity(a: str, b: str) -> float:
    """Dice coefficient over character bigrams (0.0–1.0)."""
    if not a or not b:
        return 0.0
    ga, gb = _bigrams(a), _bigrams(b)
    if not ga or not gb:
        return 0.0
    return 2 * len(ga & gb) / (len(ga) + len(gb))


def _bump_priority(current: str) -> str:
    try:
        return _PRIORITY_LADDER[min(_PRIORITY_LADDER.index(current) + 1,
                                    len(_PRIORITY_LADDER) - 1)]
    except ValueError:
        return current or "medium"


# ============================================================
# ReflectionBuilder
# ============================================================

class ReflectionBuilder:
    """Builder for constructing AI self-improvement entries."""

    def __init__(self):
        self.result = {
            "reflections": [],
            "critiques": [],
            "patterns": {},
            "episodes": [],
            "summary": ""
        }

    def add_reflection(self, task: str, outcome: str = "success",
                       went_well: list = None, went_wrong: list = None,
                       lesson: str = None):
        entry = {"timestamp": now_iso(), "task": task, "outcome": outcome}
        if went_well:
            entry["what_went_well"] = went_well
        if went_wrong:
            entry["what_went_wrong"] = went_wrong
        if lesson:
            entry["lesson"] = lesson
        self.result["reflections"].append(entry)
        return self

    def add_critique(self, trigger: str, user_said: str,
                     what_i_did_wrong: str, root_cause: str,
                     correction: str, severity: str = "medium",
                     pattern_id: str = None):
        entry = {
            "timestamp": now_iso(),
            "trigger": trigger,
            "user_said": user_said,
            "what_i_did_wrong": what_i_did_wrong,
            "root_cause": root_cause,
            "correction": correction,
            "severity": severity,
        }
        if pattern_id:
            entry["pattern_id"] = pattern_id
        self.result["critiques"].append(entry)
        return self

    def add_pattern(self, pattern_id: str, name: str, pattern: str,
                    source: str = "self_reflection", confidence: float = 0.8,
                    category: str = "general", tags: list = None):
        entry = {
            "id": pattern_id,
            "name": name,
            "pattern": pattern,
            "source": source,
            "confidence": confidence,
            "category": category,
            "tags": tags or [],
            "applications": 0,
            "created": today_str(),
            "last_applied": today_str()
        }
        self.result["patterns"][pattern_id] = entry
        return self

    def add_episode(self, task: str, skill_used: str = None,
                    outcome: str = "success", key_insight: str = None,
                    user_feedback: str = None):
        entry = {
            "timestamp": now_iso(),
            "date": today_str(),
            "task": task,
            "outcome": outcome,
        }
        if skill_used:
            entry["skill_used"] = skill_used
        if key_insight:
            entry["key_insight"] = key_insight
        if user_feedback:
            entry["user_feedback"] = user_feedback
        self.result["episodes"].append(entry)
        return self

    def set_summary(self, summary: str):
        self.result["summary"] = summary
        return self

    def build(self) -> dict:
        return self.result


# ============================================================
# AgentMemory（写入与基础读取，主动召回能力见 soul_agent_memory.py）
# ============================================================

class AgentMemory:
    """Manages the agent/ directory for AI self-improvement."""

    def __init__(self, soul_dir):
        self.soul_dir = Path(soul_dir)
        self.agent_dir = self.soul_dir / "agent"
        (self.agent_dir / "episodes").mkdir(parents=True, exist_ok=True)

    # --- Patterns ---
    def load_patterns(self) -> dict:
        data = load_json(self.agent_dir / "patterns.json", {"patterns": {}})
        return data.get("patterns", {})

    def save_patterns(self, patterns: dict):
        save_json(self.agent_dir / "patterns.json", {
            "patterns": patterns,
            "_meta": {"last_updated": now_iso(), "total_patterns": len(patterns)}
        })

    def update_pattern(self, pattern_id: str, pattern_data: dict):
        patterns = self.load_patterns()
        if pattern_id in patterns:
            existing = patterns[pattern_id]
            existing["applications"] = existing.get("applications", 0) + 1
            existing["last_applied"] = today_str()
            if pattern_data.get("confidence", 0) > existing.get("confidence", 0):
                existing["confidence"] = pattern_data["confidence"]
            for k in ["name", "pattern", "category", "tags"]:
                if k in pattern_data:
                    existing[k] = pattern_data[k]
        else:
            patterns[pattern_id] = pattern_data
        self.save_patterns(patterns)

    # --- Reflections ---
    def add_reflection(self, entry: dict):
        # Lifecycle enrichment: stable ID + status (v3.2.0+)
        existing = read_jsonl(self.agent_dir / "reflections.jsonl")
        if "id" not in entry:
            entry = {"id": _next_id("RFL", existing),
                     "status": "pending", **entry}
        elif "status" not in entry:
            entry["status"] = "pending"
        append_jsonl(self.agent_dir / "reflections.jsonl", entry)

    def load_reflections(self, limit: int = 20) -> list:
        return read_jsonl(self.agent_dir / "reflections.jsonl")[-limit:]

    # --- Corrections ---
    def add_correction(self, entry: dict):
        """
        Append a correction with lifecycle enrichment:
          - stable ID:  COR-YYYYMMDD-XXX
          - status:     pending (until resolve/promote)
          - priority:   defaults from severity
          - recurrence: if the same pattern_id or a highly similar past
                        correction exists, link them (see_also), count
                        recurrences and bump priority — recurring mistakes
                        deserve more attention.
        """
        path = self.agent_dir / "corrections.jsonl"
        existing = read_jsonl(path)

        entry["priority"] = _SEVERITY_TO_PRIORITY.get(
            entry.get("severity", "medium"), "medium")

        # Recurrence detection: same pattern_id, or text similarity over the
        # "what went wrong" field (mirrors self-improving-agent's See-Also).
        related = []
        if entry.get("pattern_id"):
            related = [e for e in existing if e.get("pattern_id") == entry["pattern_id"]]
        if not related:
            wrong = entry.get("what_i_did_wrong", "") + " " + entry.get("root_cause", "")
            related = [e for e in existing
                       if _similarity(wrong,
                                      e.get("what_i_did_wrong", "") + " " + e.get("root_cause", "")) >= 0.6]
        recurrence = max((e.get("recurrence_count", 1) for e in related), default=0) + 1
        if related:
            entry["see_also"] = sorted({e["id"] for e in related if e.get("id")})
            if recurrence >= 2:
                entry["priority"] = _bump_priority(entry["priority"])
        entry["recurrence_count"] = recurrence

        if "id" not in entry:
            entry = {"id": _next_id("COR", existing), **entry}
        if "status" not in entry:
            entry["status"] = "pending"

        append_jsonl(path, entry)

    def load_corrections(self, limit: int = 20) -> list:
        return read_jsonl(self.agent_dir / "corrections.jsonl")[-limit:]

    # --- Entry lifecycle (resolve / promote) ---
    def resolve_entry(self, entry_id: str, notes: str = "",
                      status: str = "resolved") -> dict:
        """
        Mark a correction/reflection as resolved (or promoted / wont_fix).
        Rewrites the corresponding .jsonl in place — the only non-append
        write in this engine, and it only touches the matched entry.
        """
        for filename in ("corrections.jsonl", "reflections.jsonl"):
            path = self.agent_dir / filename
            entries = read_jsonl(path)
            hit = False
            for e in entries:
                if e.get("id") == entry_id:
                    e["status"] = status
                    e["resolution"] = {
                        "resolved": now_iso(),
                        "notes": notes,
                    }
                    hit = True
            if hit:
                with open(path, "w", encoding="utf-8") as f:
                    for e in entries:
                        f.write(json.dumps(e, ensure_ascii=False) + "\n")
                return {"ok": True, "id": entry_id, "status": status,
                        "file": filename}
        return {"ok": False, "id": entry_id,
                "error": "entry not found"}

    def review(self) -> dict:
        """
        Pending-focused overview (borrowed from self-improving-agent's
        Quick Status Check): pending counts, high/critical pending list,
        and recurrence ≥ 3 entries that are ripe for promotion.
        """
        corrections = read_jsonl(self.agent_dir / "corrections.jsonl")
        reflections = read_jsonl(self.agent_dir / "reflections.jsonl")

        def pending(entries):
            return [e for e in entries if e.get("status", "pending") == "pending"]

        pc, pr = pending(corrections), pending(reflections)
        hot = [e for e in pc if e.get("priority", "medium") in ("high", "critical")]
        ripe = [e for e in pc if e.get("recurrence_count", 1) >= 3]

        return {
            "pending_corrections": len(pc),
            "pending_reflections": len(pr),
            "resolved_total": sum(1 for e in corrections + reflections
                                  if e.get("status") == "resolved"),
            "high_priority_pending": [
                {"id": e.get("id"), "wrong": e.get("what_i_did_wrong", "?")[:60],
                 "priority": e.get("priority"), "recurrence": e.get("recurrence_count", 1)}
                for e in sorted(hot, key=lambda x: x.get("recurrence_count", 1),
                                reverse=True)[:8]
            ],
            "ripe_for_promotion": [
                {"id": e.get("id"), "recurrence": e.get("recurrence_count", 1),
                 "pattern_id": e.get("pattern_id"),
                 "correction": e.get("correction", "?")[:80]}
                for e in ripe[:8]
            ],
        }

    # --- Episodes ---
    def add_episode(self, entry: dict):
        date = entry.get("date", today_str())
        path = self.agent_dir / "episodes" / f"{date}.jsonl"
        append_jsonl(path, entry)

    def load_episodes(self, date: str = None, limit: int = 20) -> list:
        if date:
            path = self.agent_dir / "episodes" / f"{date}.jsonl"
            return read_jsonl(path)[-limit:]
        episode_dir = self.agent_dir / "episodes"
        if not episode_dir.exists():
            return []
        files = sorted(episode_dir.glob("*.jsonl"), reverse=True)
        entries = []
        for f in files:
            entries.extend(read_jsonl(f))
            if len(entries) >= limit:
                break
        return entries[-limit:]

    # --- Save extraction result ---
    def save_extraction(self, result: dict) -> list:
        changes = []
        for r in result.get("reflections", []):
            self.add_reflection(r)
            changes.append(f"reflection: {r.get('task', '?')}")
        for c in result.get("critiques", []):
            self.add_correction(c)
            changes.append(f"critique: {c.get('what_i_did_wrong', '?')[:50]}")
        for pid, pdata in result.get("patterns", {}).items():
            self.update_pattern(pid, pdata)
            changes.append(f"pattern: {pid}")
        for e in result.get("episodes", []):
            self.add_episode(e)
            changes.append(f"episode: {e.get('task', '?')[:50]}")
        return changes

    # --- Status ---
    def get_status(self) -> dict:
        patterns = self.load_patterns()
        reflections = read_jsonl(self.agent_dir / "reflections.jsonl")
        corrections = read_jsonl(self.agent_dir / "corrections.jsonl")

        episode_count = 0
        episode_dir = self.agent_dir / "episodes"
        if episode_dir.exists():
            for f in episode_dir.glob("*.jsonl"):
                episode_count += len(read_jsonl(f))

        return {
            "total_patterns": len(patterns),
            "total_reflections": len(reflections),
            "total_corrections": len(corrections),
            "total_episodes": episode_count,
            "pending_corrections": sum(1 for e in corrections
                                       if e.get("status", "pending") == "pending"),
            "pending_reflections": sum(1 for e in reflections
                                       if e.get("status", "pending") == "pending"),
            "top_patterns": sorted(
                patterns.values(),
                key=lambda p: p.get("applications", 0),
                reverse=True
            )[:5]
        }


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="🧬 灵魂存档 -- AI 自我改进引擎")
    parser.add_argument("--soul-dir", type=Path,
                        default=__import__("soul_paths", fromlist=["resolve_soul_dir"]).resolve_soul_dir(),
                        help="灵魂数据目录路径")
    parser.add_argument("--mode", choices=["reflect", "critique", "learn", "status", "patterns", "review", "resolve"],
                        default="status",
                        help="工作模式")
    parser.add_argument("--input", type=str, default=None,
                        help="输入内容（反思/批评/学习的文本）")
    parser.add_argument("--id", type=str, default=None,
                        help="resolve 模式：要标记的条目 ID（COR-.../RFL-...）")
    parser.add_argument("--notes", type=str, default="",
                        help="resolve 模式：修复说明")
    parser.add_argument("--to", type=str, default="resolved",
                        choices=["resolved", "promoted", "wont_fix"],
                        help="resolve 模式：目标状态（默认 resolved）")
    args = parser.parse_args()

    agent = AgentMemory(args.soul_dir)

    if args.mode == "status":
        status = agent.get_status()
        print("🧬 AI 自我改进状态")
        print("=" * 40)
        print(f"  行为模式：{status['total_patterns']} 个")
        print(f"  自我反思：{status['total_reflections']} 次（待处理 {status['pending_reflections']}）")
        print(f"  自我批评：{status['total_corrections']} 次（待处理 {status['pending_corrections']}）")
        print(f"  工作经历：{status['total_episodes']} 条")
        if status['top_patterns']:
            print()
            print("  📊 高频模式：")
            for p in status['top_patterns']:
                print(f"    [{p.get('applications', 0)}x] {p.get('name', '?')} (置信度 {p.get('confidence', 0):.0%})")

    elif args.mode == "review":
        r = agent.review()
        print("🧬 自我改进 Review — pending 概览")
        print("=" * 44)
        print(f"  待处理批评：{r['pending_corrections']}    待处理反思：{r['pending_reflections']}    已解决：{r['resolved_total']}")
        if r["high_priority_pending"]:
            print()
            print("  🔥 高优先级 pending：")
            for e in r["high_priority_pending"]:
                print(f"    [{e['priority']}/{e['recurrence']}x] {e['id'] or '(无ID)'} — {e['wrong']}")
        if r["ripe_for_promotion"]:
            print()
            print("  📚 复现 ≥3 次，应晋升为行为模式 / 共享记忆：")
            for e in r["ripe_for_promotion"]:
                print(f"    [{e['recurrence']}x] {e['id']} → {e['pattern_id'] or '新建 pattern'}：{e['correction']}")
        if not r["high_priority_pending"] and not r["ripe_for_promotion"]:
            print("  ✅ 无高优先级 pending，无待晋升条目")

    elif args.mode == "resolve":
        if not args.id:
            print("请提供 --id 参数（COR-YYYYMMDD-XXX 或 RFL-YYYYMMDD-XXX）")
            return
        result = agent.resolve_entry(args.id, notes=args.notes, status=args.to)
        if result["ok"]:
            print(f"✅ {result['id']} → {result['status']}（{result['file']}）")
            if args.notes:
                print(f"   notes: {args.notes}")
        else:
            print(f"❌ 未找到条目 {result['id']}")

    elif args.mode == "patterns":
        patterns = agent.load_patterns()
        if not patterns:
            print("暂无行为模式记录")
            return
        print(f"🧬 行为模式库 ({len(patterns)} 个)")
        print("=" * 50)
        for pid, p in patterns.items():
            print(f"\n  [{pid}]")
            print(f"    名称：{p.get('name', '?')}")
            print(f"    模式：{p.get('pattern', '?')}")
            print(f"    置信度：{p.get('confidence', 0):.0%}")
            print(f"    应用次数：{p.get('applications', 0)}")
            print(f"    来源：{p.get('source', '?')}")
            if p.get("tags"):
                print(f"    标签：{', '.join(p['tags'])}")

    elif args.mode in ("reflect", "critique", "learn"):
        if not args.input:
            print(f"请提供 --input 参数（{args.mode} 的内容）")
            return
        print(f"📖 收到{args.mode}内容（{len(args.input)} 字符）")
        print(f"📂 灵魂存档路径：{args.soul_dir}")
        print()
        print("请使用 ReflectionBuilder 构建结果，然后调用 AgentMemory.save_extraction() 保存。")
        print()
        print("示例代码：")
        print("```python")
        print("from soul_reflect import AgentMemory, ReflectionBuilder")
        print(f"agent = AgentMemory('{args.soul_dir}')")
        print("builder = ReflectionBuilder()")
        print("builder.add_reflection(task='完成数据迁移', outcome='success',")
        print("    went_well=['全面扫描了路径'], went_wrong=['遗漏了一个目录'],")
        print("    lesson='迁移前应全面扫描所有目录')")
        print("builder.add_pattern('pat-thorough-scan', '全面扫描',")
        print("    pattern='执行迁移/清理操作前全面扫描目标范围',")
        print("    tags=['migration', 'safety'])")
        print("changes = agent.save_extraction(builder.build())")
        print("```")
        print()
        print("💡 想要主动召回相关模式/失败预警，请使用 soul_agent_memory.py")


if __name__ == "__main__":
    main()
