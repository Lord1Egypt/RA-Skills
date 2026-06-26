#!/usr/bin/env python3
"""skills-audit/scripts/skills_watch_and_notify.py  (v2.0.0)

Incremental skills directory monitor with tiered notification display.

Strategy:
- Reuse skills_audit.py scan for diff detection.
- No changes = no output (for cron noOutputNoDelivery).
- Load notification template from templates/notify.txt.
- Show file-level diff details with tiered display rules.
- Skip baseline-approved skills that haven't changed.

Output:
- Changes found: formatted notification text to stdout.
- No changes: no output.

Dependencies:
- skills_audit.py (same directory)
- templates/notify.txt (skill root)

Usage:
  python3 skills/skills-audit/scripts/skills_watch_and_notify.py \
    --workspace /root/.openclaw/workspace
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


AUDIT_DIR = Path.home() / ".openclaw" / "skills-audit"
SNAPSHOTS_DIR = AUDIT_DIR / "snapshots"


def run(argv: list[str]) -> tuple[int, str, str]:
    p = subprocess.run(argv, capture_output=True, text=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def load_template(workspace: Path) -> str:
    """Load notification template from templates/notify.txt."""
    tpl_path = workspace / "skills" / "skills-audit" / "templates" / "notify.txt"
    try:
        return tpl_path.read_text("utf-8")
    except Exception:
        return (
            "【Skills 监控提醒】\n"
            "检测到 skills 目录发生变更\n\n"
            "{sections}\n"
            "📁 路径：{skills_dir}\n"
            "🕒 时间：{timestamp} ({timezone})\n"
            "🧾 审计日志：{logs_path}\n"
            "🔍 完整 diff：git -C {snapshots_dir} diff HEAD~1 HEAD\n"
        )


def load_baseline() -> dict:
    baseline_path = AUDIT_DIR / "baseline.json"
    if not baseline_path.exists():
        return {"approved": {}}
    try:
        return json.loads(baseline_path.read_text("utf-8"))
    except Exception:
        return {"approved": {}}


def load_recent_risks(logs_path: Path, *, window_minutes: int = 15) -> dict[str, dict]:
    """Load recent risk info per slug and keep the highest risk seen in a recent window."""
    risk_by_slug: dict[str, dict] = {}
    if not logs_path.exists():
        return risk_by_slug

    try:
        lines = logs_path.read_text("utf-8").splitlines()
    except Exception:
        return risk_by_slug

    level_rank = {"unknown": 0, "low": 1, "medium": 2, "high": 3, "extreme": 4}
    window_start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=window_minutes)

    for line in reversed(lines[-2000:]):
        try:
            rec: dict[str, Any] = json.loads(line)
        except Exception:
            continue

        slug = str(rec.get("slug") or "").strip()
        if not slug:
            continue

        rec_time = str(rec.get("time") or "").strip()
        if rec_time:
            try:
                t = dt.datetime.fromisoformat(rec_time.replace("Z", "+00:00"))
                if t < window_start:
                    continue
            except Exception:
                pass

        risk = rec.get("risk") or {}
        level = str((risk or {}).get("level") or "unknown").strip().lower() or "unknown"
        source = str((risk or {}).get("source") or "local").strip().lower()

        prev = risk_by_slug.get(slug)
        if prev is None or level_rank.get(level, 0) > level_rank.get(prev.get("level", "unknown"), 0):
            risk_by_slug[slug] = {"level": level, "source": source}

    return risk_by_slug


def load_state() -> dict:
    state_path = AUDIT_DIR / "state.json"
    if not state_path.exists():
        return {"skills": {}}
    try:
        return json.loads(state_path.read_text("utf-8"))
    except Exception:
        return {"skills": {}}


def risk_label(level: str, source: str = "") -> str:
    mapping = {
        "low": "🟢 低",
        "medium": "🟢 中",
        "high": "🟡 高",
        "extreme": "🔴 极高",
        "unknown": "⚪ 未知",
    }
    label = mapping.get(level, f"⚪ {level or '未知'}")
    if source == "qianxin":
        label += " (情报)"
    return label


def get_git_diff_stat_for_skill(skill_name: str) -> list[dict]:
    if not (SNAPSHOTS_DIR / ".git").exists():
        return []
    rc, numstat, _ = run([
        "git", "-C", str(SNAPSHOTS_DIR),
        "diff", "--numstat", "HEAD~1", "HEAD",
        "--", f"skills/{skill_name}/",
    ])
    if rc != 0 or not numstat:
        return []

    result = []
    for line in numstat.splitlines():
        parts = line.split("\t", 2)
        if len(parts) != 3:
            continue
        a_str, d_str, filepath = parts
        a = int(a_str) if a_str != "-" else 0
        d = int(d_str) if d_str != "-" else 0
        prefix = f"skills/{skill_name}/"
        display_path = filepath[len(prefix):] if filepath.startswith(prefix) else filepath
        result.append({"file": display_path, "added": a, "deleted": d})
    return result


def format_file_changes(file_diff: dict | None, git_stats: list[dict], skill_name: str) -> list[str]:
    lines: list[str] = []

    if git_stats:
        total = len(git_stats)
        if total <= 5:
            for s in git_stats:
                lines.append(f"  ↳ {s['file']} (+{s['added']} -{s['deleted']})")
        elif total <= 20:
            for s in git_stats[:3]:
                lines.append(f"  ↳ {s['file']} (+{s['added']} -{s['deleted']})")
            lines.append(f"  ↳ ... 另外 {total - 3} 个文件省略")
        else:
            for s in git_stats[:3]:
                lines.append(f"  ↳ {s['file']} (+{s['added']} -{s['deleted']})")
            lines.append(f"  ↳ ... 另外 {total - 3} 个文件省略")
            total_added = sum(s["added"] for s in git_stats)
            total_deleted = sum(s["deleted"] for s in git_stats)
            lines.append(
                f"  ⚠️ {skill_name} 发生大规模变更（{total} 个文件 / +{total_added} -{total_deleted} 行），建议人工复核"
            )
    elif file_diff:
        if file_diff.get("files_changed"):
            lines.append(f"  ↳ 变更文件：{', '.join(file_diff['files_changed'][:5])}")
            if len(file_diff["files_changed"]) > 5:
                lines.append(f"  ↳ ... 另外 {len(file_diff['files_changed']) - 5} 个变更文件省略")
        if file_diff.get("files_added"):
            lines.append(f"  ↳ 新增文件：{', '.join(file_diff['files_added'][:5])}")
        if file_diff.get("files_removed"):
            lines.append(f"  ↳ 删除文件：{', '.join(file_diff['files_removed'][:5])}")

    return lines


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workspace", default="/root/.openclaw/workspace")
    ap.add_argument("--who", default="cron")
    ap.add_argument("--channel", default="local")
    args = ap.parse_args()

    workspace = Path(args.workspace).resolve()
    audit_py = workspace / "skills" / "skills-audit" / "scripts" / "skills_audit.py"

    rc, out, err = run([
        sys.executable,
        str(audit_py),
        "scan",
        "--workspace",
        str(workspace),
        "--who",
        args.who,
        "--channel",
        args.channel,
    ])
    if rc != 0:
        print(err or out, file=sys.stderr)
        return rc

    try:
        summary = json.loads(out.splitlines()[-1]) if out else {}
    except Exception:
        summary = {}

    if not ((summary.get("added") or []) or (summary.get("changed") or []) or (summary.get("removed") or [])):
        return 0

    skills_dir = workspace / "skills"

    def is_real_skill(name: str) -> bool:
        d = skills_dir / name
        try:
            return (d / "_meta.json").is_file() or (d / "SKILL.md").is_file()
        except Exception:
            return False

    added = [x for x in (summary.get("added") or []) if is_real_skill(x)]
    changed_raw = summary.get("changed") or []
    removed_raw = summary.get("removed") or []
    removed = [x for x in removed_raw if x not in {"skills"}]
    file_diffs = summary.get("file_diffs") or {}

    baseline = load_baseline()
    state = load_state()
    changed = [x for x in changed_raw if is_real_skill(x)]

    added_filtered = []
    for x in added:
        skill_state = state.get("skills", {}).get(x, {})
        tree = skill_state.get("tree_sha256", "")
        approved_entry = baseline.get("approved", {}).get(x, {})
        if approved_entry.get("tree_sha256") == tree and tree:
            continue
        added_filtered.append(x)
    added = added_filtered

    if not (added or changed or removed):
        return 0

    logs_path = AUDIT_DIR / "logs.ndjson"
    now_bj = dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).replace(microsecond=0)
    recent_risks = load_recent_risks(logs_path)

    total_skills = len(added) + len(changed) + len(removed)
    compact_mode = total_skills > 8
    sections_lines: list[str] = []

    def skill_is_high_risk(name: str) -> bool:
        info = recent_risks.get(name, {"level": "unknown", "source": "local"})
        return info["level"] in ("high", "extreme")

    def append_section(title: str, items: list[str], show_diff: bool = False) -> None:
        if not items:
            return

        if compact_mode:
            high_risk = [x for x in items if skill_is_high_risk(x)]
            low_risk = [x for x in items if not skill_is_high_risk(x)]

            if high_risk:
                sections_lines.append(f"【{title} - 高风险（需关注）】")
                for x in high_risk:
                    info = recent_risks.get(x, {"level": "unknown", "source": "local"})
                    sections_lines.append(f"• {x}｜风险等级：{risk_label(info['level'], info['source'])}")
                    if show_diff:
                        git_stats = get_git_diff_stat_for_skill(x)
                        sections_lines.extend(format_file_changes(file_diffs.get(x), git_stats, x))
                sections_lines.append("")

            if low_risk:
                sections_lines.append(f"【{title} - 低风险（共 {len(low_risk)} 个）】")
                compact_items = []
                for x in low_risk:
                    total_a = 0
                    total_d = 0
                    if show_diff:
                        git_stats = get_git_diff_stat_for_skill(x)
                        total_a = sum(s["added"] for s in git_stats)
                        total_d = sum(s["deleted"] for s in git_stats)
                    compact_items.append(f"{x} (+{total_a} -{total_d})" if (total_a or total_d) else x)
                for i in range(0, len(compact_items), 4):
                    sections_lines.append("• " + "  • ".join(compact_items[i:i+4]))
                sections_lines.append("")
        else:
            sections_lines.append(f"【{title}】")
            for x in items:
                info = recent_risks.get(x, {"level": "unknown", "source": "local"})
                if show_diff:
                    git_stats = get_git_diff_stat_for_skill(x)
                    n_files = len(git_stats)
                    if n_files > 0:
                        sections_lines.append(
                            f"• {x}｜风险等级：{risk_label(info['level'], info['source'])}｜{n_files} 个文件"
                        )
                        sections_lines.extend(format_file_changes(file_diffs.get(x), git_stats, x))
                    else:
                        sections_lines.append(f"• {x}｜风险等级：{risk_label(info['level'], info['source'])}")
                else:
                    sections_lines.append(f"• {x}｜风险等级：{risk_label(info['level'], info['source'])}")
            sections_lines.append("")

    append_section("新增", added, show_diff=True)
    append_section("变更", changed, show_diff=True)
    append_section("删除", removed, show_diff=True)

    if total_skills > 8:
        sections_lines.insert(0, f"⚠️ 本次检测到 {total_skills} 个 skill 变更，可能为批量更新\n")

    template = load_template(workspace)
    output = template.format(
        sections="\n".join(sections_lines),
        skills_dir=str(skills_dir),
        timestamp=now_bj.strftime("%Y-%m-%d %H:%M:%S"),
        timezone="Asia/Shanghai",
        logs_path=str(logs_path),
        snapshots_dir=str(SNAPSHOTS_DIR),
    ).rstrip("\n")

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
