
#!/usr/bin/env python3
"""
扫描本机各 Agent 宿主的 skill 安装目录，输出成本清单（JSON）。

只做确定性统计，不做判断。判断交给调用它的 Agent。

关键设计：**按宿主隔离「装在磁盘上」和「真的进了上下文」**。
不同宿主的 skill 绝不能合并计算上下文预算或覆盖冲突。

用法:
    python3 scan.py                    # 扫描默认路径
    python3 scan.py --path <dir> ...   # 追加自定义路径
    python3 scan.py --json out.json    # 写入文件
    python3 scan.py --all              # 预算按磁盘上所有 skill 算（诊断用，默认只算已加载）
"""

import argparse
import json
import os
import sys
from pathlib import Path

from skill_vitals import __version__
from skill_vitals.doctor import _doctor_snapshot, render_doctor
from skill_vitals.explain import render_explain
from skill_vitals.inventory import build_inventory
from skill_vitals.lifecycle import render_list
from skill_vitals.overlap import DEFAULT_OVERLAP_MIN, render_overlap
import skill_vitals.redact as redact_module
from skill_vitals.report import build_report
import skill_vitals.security as security_module
from skill_vitals.snapshots import SNAPSHOT_KEEP, diff_against, latest_snapshot, render_diff, render_snapshot

# Windows services and CI runners may expose cp1252 consoles. Reports and
# diagnostics are bilingual, so make redirected and interactive output stable.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

# 输出 JSON 的 schema 版本。**与工具版本无关**：工具可以升版而 schema 不变，
# schema 也可以在工具小版本里升主版本。
#
# 兼容性策略见 ARCHITECTURE §2.3：字段只增不删不改语义，破坏性变更升主版本。
#
# 「1.0」是**第一个带版本号的版本**。在它之前的输出没有版本字段 —— 那段时间
# schema 改过好几次（新增 unreadable_skills、runtime_verified_* 由 0 改为 null、
# WorkBuddy 口径变更），下游无法区分自己拿到的是哪一版。**没有版本号的
# schema 等于没有契约**，这笔账早该还。
SCHEMA_VERSION = "1.0"

# Claude Code 的 skill/命令描述总预算。默认约 15000 字符（≈4000 token）。
# 超出后描述被静默丢弃，无任何告警。可用 SLASH_COMMAND_TOOL_CHAR_BUDGET 调大。
# 不同版本口径不一（另有"上下文窗口 1%"的说法），故做成可配置。
DEFAULT_DESC_BUDGET = int(os.environ.get("SLASH_COMMAND_TOOL_CHAR_BUDGET", 15000))
CODEX_FALLBACK_DESC_BUDGET = 8000

# 判定「僵尸」前至少要装够这么多天。装了一天就说零触发没有意义。
ZOMBIE_MIN_AGE_DAYS = 14

# 各宿主的常见 skill 目录。找不到的会被静默跳过。
# 同一个 host 的多个根目录按该宿主的优先级归类，绝不跨宿主比较。
DEFAULT_ROOTS = [
    ("claude-code", "./.claude/skills"),
    ("claude-code", "~/.claude/skills"),
    ("claude-code-plugins", "~/.claude/plugins"),
    ("codex", "~/.codex/skills"),
    ("openclaw", "./skills"),
    ("openclaw", "./.agents/skills"),
    ("hermes", "~/.hermes/skills"),
    ("workbuddy", "./.codebuddy/skills"),
    ("workbuddy", "./.workbuddy/skills"),
    ("workbuddy", "~/.workbuddy/skills"),
    ("cc-switch", "~/.cc-switch/skills"),
    ("cursor", "~/.cursor/skills"),
    ("gemini-cli", "~/.gemini/skills"),
    ("opencode", "~/.opencode/skills"),
]

# ── 主流程 ───────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", action="version",
                    version="skill-vitals %s" % __version__)
    ap.add_argument("--host", choices=("all", "claude-code", "codex", "openclaw", "hermes", "workbuddy"),
                    default="all", help="Analyze one host; default: scan every supported host separately")
    ap.add_argument("--path", action="append", default=[],
                    help="Additional scan path; repeatable")
    ap.add_argument("--json", metavar="FILE",
                    help="Write scan JSON to FILE; use - for stdout. Without this option, run doctor.")
    ap.add_argument("--budget", type=int, default=DEFAULT_DESC_BUDGET,
                    help=f"Description character budget; default: {DEFAULT_DESC_BUDGET}")
    ap.add_argument("--all", action="store_true",
                    help="Calculate budget and conflicts over all on-disk skills (diagnostic; default: loaded only)")
    ap.add_argument("--zombie-age", type=int, default=ZOMBIE_MIN_AGE_DAYS,
                    help=f"Minimum installed age for zombie classification; default: {ZOMBIE_MIN_AGE_DAYS}")
    ap.add_argument("--split-threshold", type=int, default=6000,
                    help="Recommend splitting above this tier2_core_tokens value; default: 6000")
    ap.add_argument("--baseline", help="Previous scan JSON used for change comparison")
    ap.add_argument("--no-snapshot", action="store_true",
                    help="Disable doctor's automatic snapshot and comparison")
    ap.add_argument("--redact", action="store_true",
                    help="Redact home directories and user names in absolute paths for safe sharing")
    ap.add_argument("--self-root",
                    help="This tool's own skill directory, excluded from security scanning; inferred when omitted")
    ap.add_argument("--redact-names", action="store_true",
                    help="Also redact skill names to stable skill-001-style IDs and drop descriptions")
    # 子命令建在现有参数**之上**：不带子命令 = 原来的扫描行为。
    # 这条不是洁癖 —— SKILL.md 与全部集成测试都依赖裸调用 `--json`，
    # 把扫描降级成子命令会一次性打断所有调用方。
    sub = ap.add_subparsers(dest="cmd")
    p_list = sub.add_parser("list", help="List discovered skills and their effective state")
    p_list.add_argument("--unused", action="store_true", help="Show dormant / zombie only")
    p_list.add_argument("--shadowed", action="store_true", help="Show shadowed copies only")
    p_list.add_argument("--stale", type=int, help="Dormant threshold in days; default: 30")
    p_list.add_argument("--sort", choices=("usage", "cost", "name"), default="cost")
    p_list.add_argument("--top", type=int, help="Show only the first N rows")
    p_list.add_argument("--json", help="Write JSON instead of a table")
    p_over = sub.add_parser("overlap",
                            help="Lexical filter for skills that may compete for similar requests")
    p_over.add_argument("--min", type=float, default=DEFAULT_OVERLAP_MIN,
                        help="Jaccard threshold; default: %.2f" % DEFAULT_OVERLAP_MIN)
    p_over.add_argument("--top", type=int, help="Show only the first N pairs")
    p_over.add_argument("--json", help="Write JSON instead of a table")
    p_doc = sub.add_parser("doctor",
                           help="Turn scan facts into cause, impact, and action")
    p_doc.add_argument("--min", type=float, default=DEFAULT_OVERLAP_MIN,
                       help="Jaccard threshold for SV401; default: %.2f (shared with overlap)"
                            % DEFAULT_OVERLAP_MIN)
    p_doc.add_argument("--json", help="Write diagnostic JSON instead of a report")
    p_doc.add_argument("--no-snapshot", action="store_true",
                       help="Do not save a snapshot or compare automatically")
    p_exp = sub.add_parser("explain",
                           help="Explain why one skill is ineffective and how to fix it")
    p_exp.add_argument("name", help="Skill name or <plugin>:<name>")
    p_exp.add_argument("--min", type=float, default=DEFAULT_OVERLAP_MIN,
                       help="Jaccard threshold for neighbors; default: %.2f (shared with overlap)"
                            % DEFAULT_OVERLAP_MIN)
    p_exp.add_argument("--json", help="Write JSON instead of a report")
    p_snap = sub.add_parser("snapshot", help="Save a snapshot to ~/.skill-vitals/snapshots")
    p_snap.add_argument("--keep", type=int, default=SNAPSHOT_KEEP,
                        help="Retain the newest N snapshots; default: %d; 0 means unlimited" % SNAPSHOT_KEEP)
    p_diff = sub.add_parser("diff", help="Compare with the previous snapshot")
    p_diff.add_argument("file", nargs="?",
                        help="Snapshot file to compare; default: latest")
    p_diff.add_argument("--json", help="Write JSON instead of a report")
    # 子命令要复用扫描参数，故把它们也挂到子解析器上
    for pp in (p_list, p_over, p_doc, p_exp, p_snap, p_diff):
        pp.add_argument("--host", choices=("all", "claude-code", "codex", "openclaw",
                                           "hermes", "workbuddy"), default="all")
        pp.add_argument("--path", action="append", default=[])
        pp.add_argument("--all", action="store_true")
        pp.add_argument("--zombie-age", type=int, default=ZOMBIE_MIN_AGE_DAYS)
        pp.add_argument("--split-threshold", type=int, default=6000)
        pp.add_argument("--budget", type=int, default=DEFAULT_DESC_BUDGET)
        pp.add_argument("--self-root")
        pp.add_argument("--redact", action="store_true")
        pp.add_argument("--redact-names", action="store_true")
        pp.add_argument("--baseline")

    args = ap.parse_args()
    if getattr(args, "cmd", None):
        # 子命令下这些扫描期参数必须有默认值，下面的主流程要用
        args.baseline = getattr(args, "baseline", None)

    # 负数一律拒绝。**不能静默接受后产出垃圾** —— `--budget -1` 曾经算出
    # `pct_used: -6300.0` 并原样打进摘要行，一个负百分比被当成测量值输出。
    # 拒绝比编一个数好：这是本工具反复申明的那条底线。
    for flag, value in (("--budget", args.budget),
                        ("--zombie-age", args.zombie_age),
                        ("--split-threshold", args.split_threshold)):
        if value is not None and value < 0:
            ap.error("%s cannot be negative (received %d)" % (flag, value))

    # 显式指定「自己」在哪。Python 版本来能靠 __file__ 推断，二进制形态
    # 下那条线断了（二进制装在 npm/cargo 的 bin 目录，与 skill 目录无关），
    # 所以两个实现都提供这个开关，保持命令面一致。
    # **排除是可见的**：被排除的 skill 带着 self_excluded=true 出现在报告里。
    if args.self_root:
        security_module.SELF_SKILL_ROOT = Path(args.self_root).resolve()

    zombie_age = args.zombie_age
    budget = args.budget
    inventory = build_inventory(
        args.host, args.path, DEFAULT_ROOTS, env=os.environ,
        home=Path(os.path.expanduser("~")), cwd=Path.cwd())
    skills = inventory["skills"]
    scanned = inventory["scanned_roots"]
    unreadable = inventory["unreadable_skills"]
    roots = inventory["roots"]
    enabled_plugins = inventory["enabled_plugins"]
    usage = inventory["usage"]
    host_cfg = inventory["host_config"]
    plugins_known = inventory["plugins_known"]
    workbuddy_mode = inventory["workbuddy_mode"]
    workbuddy_roots = inventory["workbuddy_roots"]
    openclaw_runtime = inventory["openclaw_runtime"]
    codex_runtime = inventory["codex_runtime"]

    out = build_report(
        inventory,
        host=args.host,
        include_all=args.all,
        budget=budget,
        codex_fallback_budget=CODEX_FALLBACK_DESC_BUDGET,
        zombie_age=zombie_age,
        split_threshold=args.split_threshold,
        schema_version=SCHEMA_VERSION,
        home_n=str(Path(os.path.expanduser("~")).resolve()).replace("\\", "/"),
    )
    loaded = [skill for skill in skills if skill["loaded"]]
    budget_report = out["description_budget"]
    trigger_report = out["trigger_data"]
    structure_report = out["structure"]
    security_report = out["security"]
    tier1_total = out["tier1_total_tokens"]


    # 快照要在**算完 diff 之后**才写，否则这一次会拿自己当基线，
    # 变化段永远是空的 —— 一个看起来在工作、实际什么都没比的功能。
    cmd = getattr(args, "cmd", None)
    auto_snapshot = cmd in (None, "doctor") and not getattr(args, "no_snapshot", False) \
        and not args.json
    baseline = args.baseline
    if baseline is None and (auto_snapshot or cmd == "diff"):
        baseline = getattr(args, "file", None) or latest_snapshot()
    if baseline:
        out["diff_vs_baseline"] = diff_against(baseline, out)

    if args.redact or args.redact_names:
        out = redact_module.redact(
            out, names=args.redact_names, name_map={},
            home_n=str(Path(os.path.expanduser("~")).resolve()).replace("\\", "/"),
            cwd_n=str(Path.cwd()).replace("\\", "/"))
        out["redacted"] = {
            "paths": True,
            "names": bool(args.redact_names),
            "note": "This output is redacted for sharing. Run a new scan to obtain the original data.",
        }

    # `skill-vitals` 无参数等价于 `doctor`（PRODUCT §5 第一行、§183）。
    #
    # 第一次用的人想知道的是「我的 Agent 到底有没有问题」，不该先学 CLI。
    # 但 SKILL.md 与全部集成测试都靠 `--json <file>` 取原始 JSON，所以判据
    # 是**有没有给 --json**，不是「有没有子命令」—— 那条路径原样保留。
    # 想把 JSON 打到 stdout（原来的裸调用行为）用 `--json -`。
    if not getattr(args, "cmd", None) and not args.json:
        args.min = DEFAULT_OVERLAP_MIN
        render_doctor(out, args)
        _doctor_snapshot(out, auto_snapshot)
        return

    if getattr(args, "cmd", None) == "list":
        render_list(out, args)
        return
    if getattr(args, "cmd", None) == "overlap":
        render_overlap(out, args)
        return
    if getattr(args, "cmd", None) == "doctor":
        render_doctor(out, args)
        _doctor_snapshot(out, auto_snapshot and not args.json)
        return
    if getattr(args, "cmd", None) == "snapshot":
        sys.exit(render_snapshot(out, args))
    if getattr(args, "cmd", None) == "diff":
        sys.exit(render_diff(out, args))
    if getattr(args, "cmd", None) == "explain":
        # 找不到那个名字要以非零退出：脚本调用方靠退出码判断，
        # 打印一行「没找到」然后返回 0 会被当成「查过了，没问题」。
        sys.exit(render_explain(out, args))

    text = json.dumps(out, ensure_ascii=False, indent=2)
    if args.json == "-":
        print(text)
    elif args.json:
        Path(args.json).write_text(text, encoding="utf-8")
        budget_text = (f"{budget_report['pct_used']}% ({budget_report['scope']})"
                       if budget_report["available"] else
                       "configurable (not set for this instance)" if args.host == "openclaw" else "unavailable")
        active_text = (f"{len(loaded)} runtime-visible records"
                       if args.host == "openclaw" else f"{len(loaded)} loaded")
        print(f"Wrote {args.json}: {len(skills)} skills on disk, "
              f"{active_text}, "
              f"approximately {tier1_total} Tier1 tokens, "
              f"description budget {budget_text}, "
              f"trigger data {'available' if trigger_report['available'] else 'unavailable'}, "
              f"{len(structure_report['oversized'])} split candidates, "
              f"{security_report['flagged_count']} security findings "
              f"({security_report['all_cited_count']} contain only citation-like matches and still require review)")

    if unreadable:
        # 也写一份到 stderr：JSON 里那条字段只有解析输出的人会看到，
        # 而直接在终端跑的人同样需要知道清点数字是不完整的。
        print("\nWarning: %d SKILL.md files could not be read and were excluded "
              "(see unreadable_skills):" % len(unreadable), file=sys.stderr)
        for u in unreadable[:10]:
            print("  %s" % u["path"], file=sys.stderr)

    if not skills:
        print("\nNo skills were found. Use --path to specify an installation directory.",
              file=sys.stderr)


if __name__ == "__main__":
    main()
