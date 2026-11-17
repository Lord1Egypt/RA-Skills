#!/usr/bin/env python3
"""WorkBuddy ↔ lobster-memory 桥接 runner。

把 lobster-memory 的 MemorySession 包成命令行，供 WorkBuddy 在对话中调用。
注意：抽取 JSON 由 WorkBuddy（兼任 LLM）自己生成，本脚本只负责落盘/回忆/巩固。

依赖：自带 axolotl_rs 的 lobster-memory venv 的 python（路径经 LOBSTER_MEMORY_ENGINE 等环境变量配置）
"""
import sys
import os
import json
import argparse

# 所有路径均可经环境变量覆盖；默认值指向作者本机布局。
# 他人使用前设置对应环境变量即可，无需改代码。
SKILL_ENGINE = os.environ.get(
    "LOBSTER_MEMORY_ENGINE", "/Users/sai/.workbuddy/skills/lobster-memory"
)
MEMORY_DIR = os.environ.get(
    "LOBSTER_MEMORY_DIR", os.path.expanduser("~/.workbuddy/lobster-memory")
)
MEMORY_PATH = os.path.join(MEMORY_DIR, "memory.axeb")
CONSOLIDATE_EVERY = int(os.environ.get("LOBSTER_MEMORY_CONSOLIDATE_EVERY", "20"))

sys.path.insert(0, SKILL_ENGINE)

try:
    from engine.integration import MemorySession  # noqa: E402
except ImportError as e:
    sys.stderr.write(
        "[wb-lobster-memory] 无法导入 lobster-memory 的 engine。\n"
        "  请确认 LOBSTER_MEMORY_ENGINE 指向含 engine/ 的目录，\n"
        "  且当前 python 所在 venv 已安装 axolotl_rs。\n"
        f"原始错误: {e}\n"
    )
    sys.exit(2)


def _session():
    os.makedirs(MEMORY_DIR, exist_ok=True)
    return MemorySession(MEMORY_PATH, consolidate_every=CONSOLIDATE_EVERY)


def cmd_status(_):
    s = _session()
    try:
        out = s.start()
        s.close()  # 先落盘/解锁，失败则抛错，不打印假成功
    except Exception as e:
        sys.stderr.write(f"[wb-lobster-memory] status 失败: {e}\n")
        sys.exit(1)
    print(out)


def cmd_remember(args):
    raw = args.json if args.json else sys.stdin.read()
    raw = raw.strip()
    if not raw:
        print(json.dumps({"nodes_added": 0, "edges_added": 0, "error": "empty input"}, ensure_ascii=False))
        return
    s = _session()
    try:
        res = s.after_turn(raw)
        s.close()  # 先落盘，确保真正写入后再输出；失败则抛错、不打印假成功
    except Exception as e:
        sys.stderr.write(f"[wb-lobster-memory] 写入记忆失败（未落盘）: {e}\n")
        sys.exit(1)
    print(json.dumps(res, ensure_ascii=False))


def cmd_recall(args):
    s = _session()
    kws = args.keywords if args.keywords else None
    rows = s.recall(keywords=kws, domain=args.domain, limit=args.limit)
    s.close()
    if args.raw:
        print(json.dumps(rows, ensure_ascii=False, default=str))
    else:
        for m in rows:
            print(f"- {m.get('label')} | {m.get('content')} | domain={m.get('domain')} type={m.get('type')}")


def cmd_feedback(args):
    s = _session()
    rows = s.recall_feedback(valence=args.valence, limit=args.limit)
    s.close()
    if args.raw:
        print(json.dumps(rows, ensure_ascii=False, default=str))
    else:
        for m in rows:
            print(f"- {m.get('label')} | {m.get('content')} | valence={m.get('valence')}")


def cmd_should(args):
    s = _session()
    r = s.should_consolidate(args.round)
    s.close()
    print(r)


def cmd_consolidate(args):
    s = _session()
    if args.dry_run:
        report = s.consolidate(dry_run=True)
        s.close()
        # Render the plan as a readable table
        lines = ["[巩固预览 dry-run · 不改图]"]
        lines.append(f"  当前: 节点 {report['before']['vertices']} | 边 {report['before']['edges']}")
        lines.append(f"  类型化保护(不删): {report['protected']}")
        lines.append(f"  合并簇: {report['merged']['communities_found']} 个 → 将合并 {report['merged']['merged']} 个节点")
        lines.append(f"  将被软删除: {report['trashed']}")
        lines.append("")
        if report.get("merge_groups"):
            lines.append("合并计划(合并到 canonical):")
            for g in report["merge_groups"]:
                can = g["canonical"]
                mem = ", ".join(g["members"]) if g["members"] else "(无)"
                lines.append(f"  - {can}  ←  {mem}")
        if report.get("abstraction_clusters"):
            lines.append("")
            lines.append(f"归纳候选簇(被动抽象层, 仅提示不自动合并): {report['abstraction_candidates']} 个")
            for c in report["abstraction_clusters"]:
                lines.append(f"  - {' / '.join(c[:8])}{' …' if len(c) > 8 else ''}")
        if report.get("dry_trash_ids"):
            lines.append("")
            lines.append("将被软删除的节点:")
            lines.append("  - " + ", ".join(report["dry_trash_ids"]))
        print("\n".join(lines))
        return
    if s.should_consolidate(args.round):
        s.consolidate()
        summary = s.consolidate_summary()
    else:
        summary = "巩固未到期（容量未超且未到周期）"
    s.close()
    print(summary)


def main():
    p = argparse.ArgumentParser(description="WorkBuddy lobster-memory bridge")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="打印当前记忆统计（注入会话上下文用）")

    pr = sub.add_parser("remember", help="写入一轮抽取结果")
    pr.add_argument("--json", help="抽取 JSON 字符串；缺省读 stdin")

    pc = sub.add_parser("recall", help="按需回忆")
    pc.add_argument("keywords", nargs="*", help="关键词")
    pc.add_argument("--domain", default=None, choices=["emotion", "knowledge", "task"])
    pc.add_argument("--limit", type=int, default=20)
    pc.add_argument("--raw", action="store_true", help="输出原始 JSON")

    pf = sub.add_parser("feedback", help="回忆历史反馈")
    pf.add_argument("--valence", default=None, choices=["positive", "negative"])
    pf.add_argument("--limit", type=int, default=20)
    pf.add_argument("--raw", action="store_true")

    ps = sub.add_parser("should", help="是否该巩固")
    ps.add_argument("--round", type=int, default=0)

    pcon = sub.add_parser("consolidate", help="执行巩固流水线")
    pcon.add_argument("--round", type=int, default=0)
    pcon.add_argument("--dry-run", action="store_true", help="仅预览合并/删除计划, 不改图")

    args = p.parse_args()
    {
        "status": cmd_status,
        "remember": cmd_remember,
        "recall": cmd_recall,
        "feedback": cmd_feedback,
        "should": cmd_should,
        "consolidate": cmd_consolidate,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
