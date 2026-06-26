#!/usr/bin/env python3
"""
ultra-memory 管理命令行工具
提供 list / search / stats / export / gc / tier 六个子命令。

用法示例：
  python3 scripts/manage.py list
  python3 scripts/manage.py search "pandas 数据清洗"
  python3 scripts/manage.py stats
  python3 scripts/manage.py export --format json --output backup.json
  python3 scripts/manage.py gc --dry-run
  python3 scripts/manage.py tier --session sess_xxx
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))
SCRIPTS_DIR       = Path(__file__).parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))


# ── 公共工具 ────────────────────────────────────────────────────────────────

def _load_meta(session_dir: Path) -> dict:
    meta_file = session_dir / "meta.json"
    if not meta_file.exists():
        return {}
    try:
        return json.loads(meta_file.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _load_ops(session_dir: Path) -> list[dict]:
    ops_file = session_dir / "ops.jsonl"
    if not ops_file.exists():
        return []
    ops = []
    for line in ops_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                ops.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return ops


def _all_sessions() -> list[tuple[Path, dict]]:
    """返回 [(session_dir, meta), ...] 按最后活跃时间倒序"""
    sessions_dir = ULTRA_MEMORY_HOME / "sessions"
    if not sessions_dir.exists():
        return []
    result = []
    for d in sessions_dir.iterdir():
        if d.is_dir():
            meta = _load_meta(d)
            if meta:
                result.append((d, meta))
    result.sort(key=lambda x: x[1].get("last_op_at", ""), reverse=True)
    return result


# ── list 子命令 ──────────────────────────────────────────────────────────────

def cmd_list(args):
    """列出所有会话，显示项目名、操作数、最后活跃时间"""
    sessions = _all_sessions()
    if not sessions:
        print("无会话记录。运行 init.py 创建第一个会话。")
        return

    project_filter = getattr(args, "project", None)
    print(f"{'会话 ID':<28} {'项目':<20} {'操作数':>6} {'最后里程碑':<35} {'最后活跃'}")
    print("-" * 110)
    for d, meta in sessions:
        proj = meta.get("project", "default")
        if project_filter and project_filter not in proj:
            continue
        sid       = meta.get("session_id", d.name)
        op_count  = meta.get("op_count", 0)
        last_ms   = (meta.get("last_milestone") or "—")[:34]
        last_op   = (meta.get("last_op_at") or "")[:16].replace("T", " ")
        print(f"{sid:<28} {proj:<20} {op_count:>6} {last_ms:<35} {last_op}")


# ── search 子命令 ──────────────────────────────────────────────────────────

def cmd_search(args):
    """跨所有会话全文搜索操作日志（关键词匹配）"""
    query    = args.query.lower()
    limit    = getattr(args, "limit", 20)
    sessions = _all_sessions()

    hits = []
    for d, meta in sessions:
        for op in _load_ops(d):
            text = op.get("summary", "") + " " + json.dumps(op.get("detail", {}), ensure_ascii=False)
            if query in text.lower():
                hits.append({
                    "session":  meta.get("session_id", d.name),
                    "project":  meta.get("project", ""),
                    "seq":      op.get("seq", 0),
                    "ts":       op.get("ts", "")[:16].replace("T", " "),
                    "type":     op.get("type", ""),
                    "summary":  op.get("summary", ""),
                    "tier":     op.get("tier", ""),
                })

    if not hits:
        print(f"未找到包含「{args.query}」的记录")
        return

    print(f"找到 {len(hits)} 条记录（显示前 {limit} 条）：\n")
    for h in hits[:limit]:
        tier_tag = f" [{h['tier']}]" if h["tier"] else ""
        print(f"  [{h['ts']}] {h['project']}/{h['session']} #{h['seq']} {h['type']}{tier_tag}")
        print(f"  {h['summary'][:100]}\n")


# ── stats 子命令 ──────────────────────────────────────────────────────────

def cmd_stats(args):
    """显示记忆库全局统计信息"""
    sessions  = _all_sessions()
    total_ops = 0
    type_dist: Counter = Counter()
    tier_dist: Counter = Counter()
    proj_dist: Counter = Counter()
    kb_count  = 0
    ent_count = 0

    for d, meta in sessions:
        ops = _load_ops(d)
        total_ops += len(ops)
        for op in ops:
            type_dist[op.get("type", "unknown")] += 1
            tier_dist[op.get("tier", "unclassified")] += 1
        proj_dist[meta.get("project", "default")] += 1

    kb_file  = ULTRA_MEMORY_HOME / "semantic" / "knowledge_base.jsonl"
    ent_file = ULTRA_MEMORY_HOME / "semantic" / "entities.jsonl"
    if kb_file.exists():
        kb_count = sum(1 for l in kb_file.read_text(encoding="utf-8").splitlines() if l.strip())
    if ent_file.exists():
        ent_count = sum(1 for l in ent_file.read_text(encoding="utf-8").splitlines() if l.strip())

    profile_file = ULTRA_MEMORY_HOME / "semantic" / "user_profile.json"
    has_profile  = profile_file.exists()

    print(f"\n{'='*50}")
    print(f"  ultra-memory 记忆库统计")
    print(f"{'='*50}")
    print(f"  会话总数    : {len(sessions)}")
    print(f"  操作总数    : {total_ops}")
    print(f"  知识库条目  : {kb_count}")
    print(f"  实体索引    : {ent_count}")
    print(f"  用户画像    : {'已建立' if has_profile else '未建立'}")
    print(f"  存储路径    : {ULTRA_MEMORY_HOME}")
    print()

    if proj_dist:
        print(f"  项目分布（操作数）：")
        for proj, cnt in proj_dist.most_common(10):
            print(f"    {proj:<25} {cnt} 个会话")
        print()

    if type_dist:
        print(f"  操作类型分布：")
        for t, c in type_dist.most_common():
            bar = "█" * min(c // max(1, total_ops // 30), 20)
            print(f"    {t:<20} {c:>5}  {bar}")
        print()

    if tier_dist:
        print(f"  记忆分层分布：")
        for tier in ("core", "working", "peripheral", "unclassified"):
            c = tier_dist[tier]
            if c:
                pct = c * 100 // max(total_ops, 1)
                print(f"    {tier:<15} {c:>5} ({pct}%)")
        print()


# ── export 子命令 ──────────────────────────────────────────────────────────

def cmd_export(args):
    """导出全部记忆为 JSON 或 Markdown"""
    fmt    = getattr(args, "format", "json")
    output = getattr(args, "output", None)
    sessions = _all_sessions()

    if fmt == "json":
        data = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "sessions":    [],
            "knowledge_base": [],
            "entities":    [],
            "user_profile": {},
        }
        for d, meta in sessions:
            data["sessions"].append({
                "meta": meta,
                "ops":  _load_ops(d),
                "summary": (d / "summary.md").read_text(encoding="utf-8")
                            if (d / "summary.md").exists() else "",
            })

        kb_file = ULTRA_MEMORY_HOME / "semantic" / "knowledge_base.jsonl"
        if kb_file.exists():
            for line in kb_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        data["knowledge_base"].append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        ent_file = ULTRA_MEMORY_HOME / "semantic" / "entities.jsonl"
        if ent_file.exists():
            for line in ent_file.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        data["entities"].append(json.loads(line))
                    except json.JSONDecodeError:
                        pass

        profile_file = ULTRA_MEMORY_HOME / "semantic" / "user_profile.json"
        if profile_file.exists():
            try:
                data["user_profile"] = json.loads(profile_file.read_text(encoding="utf-8"))
            except Exception:
                pass

        content = json.dumps(data, ensure_ascii=False, indent=2)

    else:  # markdown
        lines = [f"# ultra-memory 导出\n导出时间: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')} UTC\n"]
        for d, meta in sessions:
            sid = meta.get("session_id", d.name)
            lines.append(f"\n## 会话: {sid}（{meta.get('project', 'default')}）\n")
            summary_file = d / "summary.md"
            if summary_file.exists():
                lines.append(summary_file.read_text(encoding="utf-8"))
        content = "\n".join(lines)

    if output:
        Path(output).write_text(content, encoding="utf-8")
        print(f"✅ 已导出到 {output}（{len(content)} 字符）")
    else:
        print(content)


# ── gc 子命令 ──────────────────────────────────────────────────────────────

def cmd_gc(args):
    """垃圾回收：清理超过 N 天且无核心操作的外围记忆会话"""
    days     = getattr(args, "days", 90)
    dry_run  = getattr(args, "dry_run", True)
    cutoff   = datetime.now(timezone.utc) - timedelta(days=days)
    sessions = _all_sessions()

    candidates = []
    for d, meta in sessions:
        last_op_str = meta.get("last_op_at", "")
        if not last_op_str:
            continue
        try:
            last_op = datetime.fromisoformat(last_op_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        if last_op >= cutoff:
            continue
        # 只清理无核心操作的会话
        ops  = _load_ops(d)
        core = sum(1 for op in ops if op.get("tier") == "core"
                   or op.get("type") in ("milestone", "decision"))
        if core == 0:
            candidates.append((d, meta, last_op))

    if not candidates:
        print(f"✅ 无符合清理条件的会话（{days}天未活跃 且 无核心操作）")
        return

    mode = "（预演，未实际删除）" if dry_run else ""
    print(f"发现 {len(candidates)} 个可清理会话 {mode}：\n")
    freed = 0
    for d, meta, last_op in candidates:
        size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file())
        freed += size
        print(f"  {meta.get('session_id', d.name):<30} {meta.get('project', ''):<20}"
              f" 最后活跃: {str(last_op)[:10]}  大小: {size//1024}KB")
        if not dry_run:
            import shutil
            shutil.rmtree(d)

    print(f"\n{'预计' if dry_run else ''}释放空间: {freed//1024}KB")
    if dry_run:
        print("加 --no-dry-run 参数执行实际清理")


# ── tier 子命令 ──────────────────────────────────────────────────────────────

def cmd_tier(args):
    """对指定会话（或所有会话）的 ops 补写 tier 分级字段"""
    from summarize import classify_tier

    session_id = getattr(args, "session", None)
    sessions   = _all_sessions()

    if session_id:
        sessions = [(d, m) for d, m in sessions if m.get("session_id") == session_id]
        if not sessions:
            print(f"❌ 会话不存在: {session_id}")
            return

    total_updated = 0
    for d, meta in sessions:
        ops_file = d / "ops.jsonl"
        if not ops_file.exists():
            continue

        ops     = _load_ops(d)
        updated = 0
        tmp     = ops_file.with_suffix(".tmp")

        with open(tmp, "w", encoding="utf-8") as fout:
            for op in ops:
                if "tier" not in op:
                    op["tier"] = classify_tier(op)
                    updated += 1
                fout.write(json.dumps(op, ensure_ascii=False) + "\n")

        if updated > 0:
            tmp.replace(ops_file)
            print(f"  {meta.get('session_id', d.name)}: 已补写 {updated} 条 tier 标记")
            total_updated += updated
        else:
            tmp.unlink(missing_ok=True)

    print(f"\n✅ 共更新 {total_updated} 条操作的 tier 分级")


# ── scopes 子命令 ─────────────────────────────────────────────────────────────

def cmd_scopes(args):
    """列出所有隔离 scope 及其会话数、存储路径"""
    scopes_dir = ULTRA_MEMORY_HOME / "scopes"
    if not scopes_dir.exists():
        print("尚无隔离 scope（所有数据在默认空间）")
        print(f"默认空间: {ULTRA_MEMORY_HOME}")
        return

    entries = [d for d in scopes_dir.iterdir() if d.is_dir()]
    if not entries:
        print("尚无隔离 scope（所有数据在默认空间）")
        return

    # 默认空间统计
    default_sessions = ULTRA_MEMORY_HOME / "sessions"
    default_count = len(list(default_sessions.iterdir())) if default_sessions.exists() else 0

    print(f"\n{'Scope':<28} {'会话数':>6}  {'存储路径'}")
    print("-" * 80)
    print(f"{'（默认）':<28} {default_count:>6}  {ULTRA_MEMORY_HOME}")

    for d in sorted(entries):
        sess_dir = d / "sessions"
        sess_count = len(list(sess_dir.iterdir())) if sess_dir.exists() else 0
        # 还原显示名：user__alice → user:alice
        display = d.name.replace("__", ":", 1)
        print(f"{display:<28} {sess_count:>6}  {d}")

    print()
    print("用法：python3 scripts/init.py --scope user:alice --project myapp")
    print("      python3 scripts/manage.py list --storage <scope_path>")


# ── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ultra-memory 记忆库管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
子命令:
  list    列出所有会话
  search  跨会话全文搜索
  stats   显示全局统计
  export  导出为 JSON 或 Markdown
  gc      垃圾回收旧会话
  tier    补写记忆分层标记
        """,
    )
    parser.add_argument("--storage", default=None, help="覆盖 ULTRA_MEMORY_HOME 路径")

    sub = parser.add_subparsers(dest="command")

    # list
    p_list = sub.add_parser("list", help="列出所有会话")
    p_list.add_argument("--project", default=None, help="按项目名过滤")

    # search
    p_search = sub.add_parser("search", help="跨会话全文搜索")
    p_search.add_argument("query", help="搜索关键词")
    p_search.add_argument("--limit", type=int, default=20, help="最多返回条数（默认20）")

    # stats
    sub.add_parser("stats", help="全局统计信息")

    # export
    p_export = sub.add_parser("export", help="导出记忆为 JSON 或 Markdown")
    p_export.add_argument("--format", choices=["json", "markdown"], default="json")
    p_export.add_argument("--output", default=None, help="输出文件路径（默认标准输出）")

    # gc
    p_gc = sub.add_parser("gc", help="垃圾回收旧会话")
    p_gc.add_argument("--days",       type=int, default=90,  help="超过多少天未活跃（默认90）")
    p_gc.add_argument("--no-dry-run", dest="dry_run", action="store_false", help="实际执行删除")
    p_gc.set_defaults(dry_run=True)

    # tier
    p_tier = sub.add_parser("tier", help="补写记忆分层标记")
    p_tier.add_argument("--session", default=None, help="指定会话 ID（默认所有会话）")

    # scopes
    sub.add_parser("scopes", help="列出所有隔离 scope（多用户/多 Agent）")

    args = parser.parse_args()

    if args.storage:
        global ULTRA_MEMORY_HOME
        ULTRA_MEMORY_HOME = Path(args.storage)
        os.environ["ULTRA_MEMORY_HOME"] = str(ULTRA_MEMORY_HOME)

    dispatch = {
        "list":   cmd_list,
        "search": cmd_search,
        "stats":  cmd_stats,
        "export": cmd_export,
        "gc":     cmd_gc,
        "tier":   cmd_tier,
        "scopes": cmd_scopes,
    }

    if args.command not in dispatch:
        parser.print_help()
        return

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
