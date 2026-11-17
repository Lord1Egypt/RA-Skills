"""Snapshot storage plus snapshot and diff rendering."""

import json
import os
import sys
import time
from pathlib import Path

from .lifecycle import ZOMBIE_MIN_AGE_DAYS
from .overlap import overlap_pairs
from .diff import _overlap_keys, compare_reports


def diff_against(previous_path, now):
    """Load a baseline snapshot and compare it with the current report."""
    try:
        previous = json.loads(Path(previous_path).read_text(
            encoding="utf-8", errors="replace"))
    except (OSError, json.JSONDecodeError) as error:
        return {"error": f"Cannot read baseline file {previous_path}: {error}"}
    return compare_reports(previous, now, baseline_file=previous_path)

# ── 快照与 diff（PRODUCT §5.5、ARCHITECTURE §8.3）──────────
#
# 快照存在的唯一理由：本工具自己规定「装不够 N 天的不算僵尸，2–3 周后复查」，
# 而复查时没人记得基线。没有快照，那条建议就是空头支票。
#
# **快照只落在本机。**它含绝对路径、用户名、skill 名与完整 description ——
# 一个审计供应链风险的工具不能自己回传数据（PRODUCT §8.3、§615）。

SNAPSHOT_DIR_MODE = 0o700
SNAPSHOT_FILE_MODE = 0o600
SNAPSHOT_KEEP = 30


def snapshot_dir():
    """快照目录。可用 SKILL_VITALS_SNAPSHOT_DIR 覆盖（测试与多配置用）。"""
    env = os.environ.get("SKILL_VITALS_SNAPSHOT_DIR")
    if env:
        return Path(env)
    return Path(os.path.expanduser("~/.skill-vitals/snapshots"))


def list_snapshots():
    """已有快照，**旧→新**。文件名是 UTC 紧凑时间戳，字典序即时间序。"""
    d = snapshot_dir()
    try:
        return sorted(p for p in d.glob("*.json") if p.is_file())
    except OSError:
        return []


def latest_snapshot():
    snaps = list_snapshots()
    return snaps[-1] if snaps else None


def save_snapshot(out, keep=SNAPSHOT_KEEP, stamp=None):
    """写一份快照并轮换。返回写入的路径。

    **存进去的是一份干净的扫描记录，不带 diff_vs_baseline。**否则第二次
    快照里会嵌着「相对第一次的差异」，第三次又嵌着第二次的 —— 快照就从
    「某一时刻的事实」变成了一条越滚越大的历史链，而 diff 本来就该由两份
    事实现算。
    """
    d = snapshot_dir()
    # 目录 0700、文件 0600（ARCHITECTURE §8.3）。Windows 上 chmod 基本是
    # 空操作，但**不能因此就不调** —— POSIX 上这是唯一的防线。
    d.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(d, SNAPSHOT_DIR_MODE)
    except OSError:
        pass
    body = {k: v for k, v in out.items() if k != "diff_vs_baseline"}
    ts = stamp or time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    path = d / ("%s.json" % ts)
    # 同一秒内跑两次不能互相覆盖：加序号，别让第二次静默吃掉第一次
    n = 1
    while path.exists():
        n += 1
        path = d / ("%s-%d.json" % (ts, n))
    path.write_text(json.dumps(body, ensure_ascii=False, indent=2), encoding="utf-8")
    try:
        os.chmod(path, SNAPSHOT_FILE_MODE)
    except OSError:
        pass

    # 轮换。keep=0 表示不限制 —— 不是「一份都不留」，那会让刚写的这份
    # 立刻被删掉，用户看到「已保存」却什么都没有。
    if keep > 0:
        for old in list_snapshots()[:-keep]:
            try:
                old.unlink()
            except OSError:
                pass
    return path


def _diff_name(entry):
    """兼容旧快照：老的基线里 added_skills 是裸数组。"""
    if isinstance(entry, dict):
        ns = entry.get("namespace")
        return "%s:%s" % (ns, entry["name"]) if ns else entry["name"]
    if isinstance(entry, list):
        return entry[-1]
    return entry


def render_diff(out, args):
    """`diff` 的呈现（PRODUCT §5.5）。"""
    d = out.get("diff_vs_baseline")
    if d is None:
        # **「没有基线」与「没有变化」必须区分。**返回 0 加一句空输出会被
        # 读成「查过了，没变化」—— 同 §3.1 的 null ≠ 0，只是换到了退出码上。
        print("No snapshot is available for comparison.", file=sys.stderr)
        print("Run `skill-vitals doctor` (saves one automatically) or "
              "`skill-vitals snapshot` first.", file=sys.stderr)
        return 1
    if d.get("error"):
        print(d["error"], file=sys.stderr)
        return 1

    if args.json:
        Path(args.json).write_text(json.dumps(d, ensure_ascii=False, indent=2),
                                   encoding="utf-8")
        print("Wrote %s" % args.json)
        return 0

    base = d.get("baseline_file", "")
    # 标题行只放文件名（路径可能很长），完整路径在末行给出 —— 既可读又可复现
    print("Changes since %s" % (Path(base).name or base))
    print("─" * 42)

    added, removed = d.get("added_skills", []), d.get("removed_skills", [])
    if added or removed:
        print()
        print("Skills")
        for k in added:
            print("  + %s" % _diff_name(k))
        for k in removed:
            print("  - %s" % _diff_name(k))

    # **没变就不出现这一小节。**打一句「无变化 (+0.0%)」既占地方又自相矛盾，
    # 而 diff 只该回答「这次多出/少了什么」。
    pt, pn = d.get("budget_pct_then_now", [None, None])
    delta = d.get("budget_delta_chars") or 0
    budget_changed = delta != 0 and pt is not None and pn is not None
    if budget_changed:
        print()
        print("Description budget")
        print("  %+d chars   %.1f%% → %.1f%%%s" % (
            delta, pt, pn,
            "   ⚠ overflow" if (out.get("description_budget", {}) or {}).get("over_by_chars") else ""))

    new_pairs = d.get("new_overlap_candidates", [])
    if new_pairs:
        print()
        print("New overlap candidates          [Lexical, review required]")
        for p in new_pairs:
            print("  %s ↔ %s" % (p[0], p[1]))

    ud = d.get("usage_delta", [])
    if ud:
        print()
        print("Trigger deltas")
        w = max(len(x["name"]) for x in ud)
        for x in ud:
            print("  %-*s  %+d   (total %d)" % (w, x["name"], x["delta"], x["now"]))

    ns = d.get("new_security_findings", [])
    if ns:
        print()
        print("New security findings")
        for x in ns:
            print("  %s  %s  %s:%s" % (x["skill"], x["rule"], x["where"], x["line"]))

    nj = d.get("newly_judgeable", [])
    if nj:
        # **只报这一批。**老结论重报一遍会把「本次新增的判定对象」淹掉，
        # 而那恰恰是复查唯一要看的东西（PRODUCT §5.5）。
        gate = (out.get("trigger_data", {}) or {}).get("zombie_min_age_days", ZOMBIE_MIN_AGE_DAYS)
        print()
        print("Newly judgeable (previously too new; now at least %d days old)" % gate)
        w = max(len(x["name"]) for x in nj)
        for x in nj:
            print("  %-*s  %d triggers → %s" % (w, x["name"], x["usage_count"], x["verdict"]))

    if not (added or removed or budget_changed or new_pairs or ud or ns or nj):
        print()
        print("  No changes from the baseline.")
    print()
    print("  Baseline: %s" % base)
    return 0


def render_snapshot(out, args):
    path = save_snapshot(out, keep=args.keep)
    kept = len(list_snapshots())
    print("Snapshot saved → %s" % path)
    print("  Retained %d snapshots (--keep %d)" % (kept, args.keep))
    print("  Directory mode 0700, file mode 0600; local only, never uploaded")
    if not (args.redact or args.redact_names):
        # 落盘的是未脱敏的原始记录 —— 说清楚，别让用户以为它可以随手外发
        print("  ! Not redacted: contains absolute paths, user names, skill names, and full descriptions. "
              "Use --redact --redact-names before sharing.")
    return 0
