#!/usr/bin/env python3
"""
memory_compress.py - 智能压缩记忆文件，防止上下文过长

用法:
  python scripts/memory_compress.py --uid pupper --level ALL      # 压缩所有层级
  python scripts/memory_compress.py --uid pupper --dry-run       # 仅分析，不实际压缩
  python scripts/memory_compress.py --uid pupper --upgrade        # 主题重复性升级（L1→L2）
  python scripts/memory_compress.py --uid pupper --undo          # 回滚到最近一次操作

选项:
  --uid               用户ID（默认 MEMORY_USER_ID 环境变量或 "default"）
  --level             压缩层级（默认: ALL，检查所有层级）
  --dry-run           仅分析，不实际压缩
  --threshold-l1      L1 压缩触发行数（默认: 150）
  --threshold-l2      L2 压缩触发行数（默认: 200）
  --archive-days      超过 N 天归档 L1 文件（默认: 30）
  --upgrade           执行 L1→L2→L3 主题升级
  --rebase-threshold  同一主题出现 N 次触发升级（默认: 3）
  --undo              回滚最近一次压缩/归档/升级操作（从快照恢复）
  --undo-id           回滚指定快照 ID（默认: 最近一次）
  --list-snapshots    列出所有可用的快照
  --keep-snapshots N  快照保留天数（默认: 7）
"""

import os
import re
import sys
import json
import shutil
import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List, Dict, Optional, Union, Any, Tuple


COMPRESS_HEADER = (
    "<!-- [已压缩] {date} | 原始: {original}行/{orig_entries}条 "
    "→ 压缩后: {compressed}行/{comp_entries}条 | 压缩率: {ratio:.0%} -->\n\n"
)

UPGRADE_L2_RE = re.compile(r"\[IMPORTANT\]|\[重要\]|\[WEEKLY\]|\[升级L2\]", re.IGNORECASE)
UPGRADE_L3_RE = re.compile(r"\[IMPORTANT\]|\[重要\]|\[升级L3\]|\[PERMANENT\]", re.IGNORECASE)
HABIT_RE = re.compile(r"\[HABIT\]|\[习惯\]", re.IGNORECASE)
TODO_RE = re.compile(r"^- \[ \] .+$", re.MULTILINE)


# ══════════════════════════════════════════════════════════════
#  快照系统
# ══════════════════════════════════════════════════════════════

def get_snapshots_dir(base_dir):
    return os.path.join(os.path.abspath(base_dir), ".snapshots")


def create_snapshot(base_dir, uid, operation_type, description="", files_changed=None):
    """
    创建操作前快照，返回 snapshot_id。
    files_changed: [{"path": str, "content": str, "mtime": float}]
    """
    snap_dir = get_snapshots_dir(base_dir)
    date_str = datetime.now().strftime("%Y-%m-%d")
    snap_subdir = os.path.join(snap_dir, date_str)
    os.makedirs(snap_subdir, exist_ok=True)

    snapshot_id = datetime.now().strftime("%H%M%S")  # HHMMSS 作为 ID
    snap_data = {
        "snapshot_id": snapshot_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "uid": uid,
        "operation_type": operation_type,
        "description": description,
        "files": files_changed or [],
    }

    snap_path = os.path.join(snap_subdir, f"{snapshot_id}.json")
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snap_data, f, ensure_ascii=False, indent=2)

    print(f"  💾 快照已创建: .snapshots/{date_str}/{snapshot_id}.json "
          f"({len(files_changed or [])} 个文件)")
    return snapshot_id


def list_snapshots(base_dir, uid=None, keep_days=7):
    """列出所有快照，删除过期快照"""
    snap_dir = get_snapshots_dir(base_dir)
    if not os.path.exists(snap_dir):
        return []

    # 清理过期快照
    cutoff = datetime.now() - timedelta(days=keep_days)
    all_snapshots = []

    for date_dir in os.listdir(snap_dir):
        date_path = os.path.join(snap_dir, date_dir)
        if not os.path.isdir(date_path):
            continue

        try:
            dir_date = datetime.strptime(date_dir, "%Y-%m-%d")
        except ValueError:
            continue

        if dir_date < cutoff:
            shutil.rmtree(date_path)
            continue

        for fname in os.listdir(date_path):
            if not fname.endswith(".json"):
                continue
            fpath = os.path.join(date_path, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            if uid and data.get("uid") != uid:
                continue
            data["_file_path"] = fpath
            all_snapshots.append(data)

    all_snapshots.sort(key=lambda x: x["created_at"], reverse=True)
    return all_snapshots


def undo_snapshot(base_dir, snapshot_id=None):
    """从快照恢复文件"""
    snapshots = list_snapshots(base_dir)
    if not snapshots:
        print("❌ 无可用快照")
        return False

    if snapshot_id:
        target = next((s for s in snapshots if s["snapshot_id"] == snapshot_id), None)
        if not target:
            print(f"❌ 未找到快照: {snapshot_id}")
            return False
    else:
        target = snapshots[0]

    print(f"\n↩️  回滚操作")
    print(f"   快照 ID: {target['snapshot_id']}")
    print(f"   创建时间: {target['created_at']}")
    print(f"   操作类型: {target['operation_type']}")
    print(f"   描述: {target['description'] or '(无)'}")
    print(f"   包含文件: {len(target['files'])} 个")

    restored = 0
    for file_entry in target["files"]:
        fpath = file_entry["path"]
        if not os.path.exists(fpath):
            print(f"  ⚠️  文件已不存在，跳过: {fpath}")
            continue

        with open(fpath, "w", encoding="utf-8") as f:
            f.write(file_entry["content"])

        # 恢复 mtime
        if "mtime" in file_entry:
            try:
                os.utime(fpath, (file_entry["mtime"], file_entry["mtime"]))
            except OSError:
                pass

        print(f"  ✅ 已恢复: {os.path.relpath(fpath, base_dir)}")
        restored += 1

    print(f"\n✅ 回滚完成，恢复了 {restored} 个文件")
    print(f"   快照文件: {target['_file_path']}（保留，可手动删除）")
    return True


# ══════════════════════════════════════════════════════════════
#  核心压缩逻辑
# ══════════════════════════════════════════════════════════════

def backup_file(filepath):
    """创建文件备份到 .compress_backup/"""
    backup_dir = os.path.join(os.path.dirname(filepath), ".compress_backup")
    os.makedirs(backup_dir, exist_ok=True)
    fname = os.path.basename(filepath)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"{fname}.{ts}.bak")
    shutil.copy2(filepath, backup_path)
    return backup_path


def parse_sections(content):
    sections = []
    parts = re.split(r"(?=^## )", content, flags=re.MULTILINE)

    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n")
        title = lines[0].lstrip("#").strip() if lines else ""
        body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

        sections.append({
            "title": title,
            "body": body,
            "raw": part,
            "has_todo": bool(TODO_RE.search(part)),
            "is_important_l2": bool(UPGRADE_L2_RE.search(part)),
            "is_important_l3": bool(UPGRADE_L3_RE.search(part)),
            "is_habit": bool(HABIT_RE.search(part)),
            "line_count": len(part.split("\n")),
        })
    return sections


def compress_l1_section(section):
    body = section["body"]
    todos = TODO_RE.findall(body)
    key_lines = []
    for line in body.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        if (
            stripped.startswith("**")
            or stripped.startswith("- ")
            or stripped.startswith("- [")
            or stripped.startswith("#")
            or re.match(r"^\*\*[^\*]*\*\*(?:$|:)", stripped)
        ):
            key_lines.append(line)
    compressed_body = "\n".join(key_lines)
    if todos and "**待办" not in compressed_body:
        compressed_body += "\n**待办（保留）**:\n" + "\n".join(todos)
    return compressed_body


def compress_l2_section(section):
    body = section["body"]
    title = section["title"]
    todos = TODO_RE.findall(body)
    preserve_full = any(k in title for k in ["决策", "里程碑", "决定", "decision", "milestone"])
    if preserve_full or todos:
        return body
    key_lines = [
        line for line in body.split("\n")
        if line.strip() and (line.strip().startswith("**")
                               or line.strip().startswith("- ")
                               or line.strip().startswith("- ["))
    ]
    compressed_body = "\n".join(key_lines)
    if key_lines:
        compressed_body += "\n_(已压缩详情)_"
    return compressed_body


def compress_file(filepath, threshold=150, dry_run=False, level="L1",
                  snapshot_context=None):
    """
    压缩单个记忆文件。
    snapshot_context: [files_changed_list] — append file info here for snapshot
    返回 (是否压缩了, 升级条目列表)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original_lines = len(content.split("\n"))
    if original_lines <= threshold:
        return False, []

    sections = parse_sections(content)
    orig_entries = len(sections)

    preserved = []
    compressed = []
    upgraded_l2 = []
    upgraded_l3 = []
    habit_entries = []

    for s in sections:
        if s["has_todo"] or s["is_important_l3"]:
            preserved.append(s["raw"])
        elif s["is_important_l2"]:
            compressed.append(f"## {s['title']}\n{compress_l1_section(s)}")
            upgraded_l2.append(s)
        elif s["is_habit"]:
            habit_entries.append(s)
            compressed.append(f"## {s['title']}\n_(已提取到习惯追踪)_")
        else:
            comp = compress_l2_section(s) if level == "L2" else compress_l1_section(s)
            compressed.append(f"## {s['title']}\n{comp}")

    all_sections = preserved + compressed
    new_content = "\n\n---\n\n".join(all_sections)
    compressed_lines = len(new_content.split("\n"))
    ratio = (original_lines - compressed_lines) / original_lines if original_lines > 0 else 0
    comp_entries = len(all_sections)

    header = COMPRESS_HEADER.format(
        date=datetime.now().strftime("%Y-%m-%d %H:%M"),
        original=original_lines,
        orig_entries=orig_entries,
        compressed=compressed_lines,
        comp_entries=comp_entries,
        ratio=ratio,
    )
    final_content = header + new_content

    if not dry_run:
        # 记录快照
        if snapshot_context is not None:
            import os as _os
            stat = _os.stat(filepath)
            snapshot_context.append({
                "path": filepath,
                "content": content,
                "mtime": stat.st_mtime,
            })
        backup = backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"  ✅ {Path(filepath).name}: {original_lines}行/{orig_entries}条 "
              f"→ {compressed_lines}行/{comp_entries}条 ({ratio:.0%})")
        print(f"     💾 备份: {Path(backup).name}")
    else:
        print(f"  [DRY-RUN] {Path(filepath).name}: {original_lines}行 "
              f"→ {compressed_lines}行 ({ratio:.0%})")

    return True, upgraded_l2 + upgraded_l3


def upgrade_repeated_themes(base_dir, uid, threshold=3, dry_run=False,
                             snapshot_context=None):
    """发现同一主题在多个 L1 文件中重复出现 → 升级到 L2"""
    print(f"\n🔍 主题重复性检查（阈值: {threshold} 次）...")

    daily_dir = os.path.join(base_dir, "users", uid, "daily")
    if not os.path.exists(daily_dir):
        print("  (无 L1 文件)")
        return

    theme_counts = {}
    theme_examples = {}

    for fname in os.listdir(daily_dir):
        if not fname.endswith(".md"):
            continue
        with open(os.path.join(daily_dir, fname), "r", encoding="utf-8") as f:
            content = f.read()
        titles = re.findall(r"^## (.+)$", content, re.MULTILINE)
        for t in titles:
            clean = re.sub(r"^\[\d{2}:\d{2}\]\s*", "", t).strip().lower()
            if len(clean) < 3:
                continue
            theme_counts[clean] = theme_counts.get(clean, 0) + 1
            theme_examples.setdefault(clean, []).append(t)

    upgrades = {k: v for k, v in theme_counts.items() if v >= threshold}

    if not upgrades:
        print("  ✅ 无重复主题，无需升级")
        return

    print(f"  📋 发现 {len(upgrades)} 个重复主题:")
    for theme, count in sorted(upgrades.items(), key=lambda x: -x[1]):
        print(f"     [{count}次] {theme}")

    if dry_run:
        print("  [DRY-RUN] 跳过实际升级")
        return

    weekly_dir = os.path.join(base_dir, "users", uid, "weekly")
    this_week = datetime.now().strftime("%Y-W%V") + ".md"
    weekly_path = os.path.join(weekly_dir, this_week)

    # 快照：记录原周报内容
    original_weekly_content = ""
    weekly_existed = os.path.exists(weekly_path)
    if weekly_existed:
        with open(weekly_path, "r", encoding="utf-8") as f:
            original_weekly_content = f.read()

    upgrade_block = f"\n---\n\n## 主题升级（{datetime.now().strftime('%Y-%m-%d')}）\n\n"
    for theme, count in sorted(upgrades.items(), key=lambda x: -x[1]):
        examples = theme_examples[theme][:5]
        upgrade_block += f"### [{theme.title()}] 出现 {count} 次\n"
        upgrade_block += f"- **主题**: {theme}\n"
        upgrade_block += f"- **出现次数**: {count} 次\n"
        upgrade_block += f"- **示例**: {' | '.join(examples[:3])}\n\n"

    if weekly_existed:
        new_weekly_content = original_weekly_content + upgrade_block
    else:
        os.makedirs(weekly_dir, exist_ok=True)
        new_weekly_content = f"# Weekly Memory — {this_week.replace('.md', '')}\n\n{upgrade_block}"

    # 记录快照
    if snapshot_context is not None and weekly_existed:
        import os as _os
        stat = _os.stat(weekly_path)
        snapshot_context.append({
            "path": weekly_path,
            "content": original_weekly_content,
            "mtime": stat.st_mtime,
        })

    with open(weekly_path, "w", encoding="utf-8") as f:
        f.write(new_weekly_content)

    print(f"  ✅ 主题升级写入: users/{uid}/weekly/{this_week}")


def archive_old_l1(base_dir, uid, days=30, dry_run=False, snapshot_context=None):
    """归档超过 N 天的 L1 文件到 archive/daily/"""
    daily_dir = os.path.join(base_dir, "users", uid, "daily")
    archive_dir = os.path.join(base_dir, "users", uid, "archive", "daily")
    cutoff = datetime.now() - timedelta(days=days)

    if not os.path.exists(daily_dir):
        return 0

    archived = 0
    for fname in os.listdir(daily_dir):
        if not fname.endswith(".md"):
            continue
        try:
            file_date = datetime.strptime(fname.replace(".md", ""), "%Y-%m-%d")
            if file_date < cutoff:
                src = os.path.join(daily_dir, fname)
                if not dry_run:
                    # 记录快照（保存原位置的内容）
                    if snapshot_context is not None:
                        with open(src, "r", encoding="utf-8") as f:
                            content = f.read()
                        snapshot_context.append({
                            "path": src,
                            "content": content,
                            "mtime": os.path.getmtime(src),
                            "_archive_dest": os.path.join(archive_dir, fname),
                        })
                    os.makedirs(archive_dir, exist_ok=True)
                    shutil.move(src, os.path.join(archive_dir, fname))
                    print(f"  📦 归档: {fname} → archive/daily/")
                else:
                    print(f"  [DRY-RUN] 将归档: {fname}")
                archived += 1
        except ValueError:
            pass

    return archived


def main():
    parser = argparse.ArgumentParser(description="智能压缩记忆文件（支持快照+回滚）")
    parser.add_argument("--base-dir", default=".", help="记忆仓库根目录")
    parser.add_argument("--uid", help="用户ID（默认: MEMORY_USER_ID 或 'default'）")
    parser.add_argument("--level", default="ALL", choices=["L1", "L2", "L3", "ALL"],
                        help="压缩层级")
    parser.add_argument("--dry-run", action="store_true", help="仅分析，不实际压缩")
    parser.add_argument("--threshold-l1", type=int, default=150, help="L1 压缩触发行数")
    parser.add_argument("--threshold-l2", type=int, default=200, help="L2 压缩触发行数")
    parser.add_argument("--archive-days", type=int, default=30, help="归档超过N天的L1文件")
    parser.add_argument("--upgrade", action="store_true",
                        help="执行主题重复性升级（L1→L2）")
    parser.add_argument("--rebase-threshold", type=int, default=3,
                        help="同一主题出现N次触发升级")
    parser.add_argument("--undo", action="store_true", help="回滚到最近一次操作")
    parser.add_argument("--undo-id", help="回滚指定快照 ID")
    parser.add_argument("--list-snapshots", action="store_true", help="列出所有快照")
    parser.add_argument("--keep-snapshots", type=int, default=7, help="快照保留天数")
    args = parser.parse_args()

    base_dir = os.path.abspath(args.base_dir)
    uid = args.uid or os.environ.get("MEMORY_USER_ID", "default")

    # ── 快照列表 ──
    if args.list_snapshots:
        snapshots = list_snapshots(base_dir, uid, args.keep_snapshots)
        if not snapshots:
            print("📦 暂无快照")
            return
        print(f"📦 可用快照（共 {len(snapshots)} 个，保留 {args.keep_snapshots} 天）:\n")
        for s in snapshots[:20]:
            ts = s["created_at"][:19].replace("T", " ")
            print(f"  [{s['snapshot_id']}] {ts} | {s['operation_type']} | "
                  f"{len(s['files'])} 文件 | {s.get('description', '') or '无描述'}")
        return

    # ── 回滚 ──
    if args.undo:
        undo_snapshot(base_dir, args.undo_id)
        return

    # ── 普通压缩 ──
    user_dir = os.path.join(base_dir, "users", uid)
    if not os.path.exists(user_dir):
        print(f"❌ 用户目录不存在: users/{uid}/")
        print("   请先运行: python scripts/memory_init.py --uid " + uid)
        sys.exit(1)

    print(f"\n🗜️  记忆压缩工具（用户: {uid}）")
    print(f"📁 仓库根目录: {base_dir}")
    print(f"📅 快照保留: {args.keep_snapshots} 天")
    if args.dry_run:
        print("🔍 模式: DRY-RUN（仅分析）\n")
    else:
        print("⚡ 模式: 实际压缩\n")

    # 创建操作快照上下文
    snapshot_context = [] if not args.dry_run else None

    compressed_count = 0

    if args.level in ("L1", "ALL"):
        daily_dir = os.path.join(user_dir, "daily")
        print(f"📋 检查 L1 临时记忆（阈值: {args.threshold_l1}行）...")
        if os.path.exists(daily_dir):
            files = sorted([f for f in os.listdir(daily_dir) if f.endswith(".md")], reverse=True)
            if files:
                for fname in files:
                    fpath = os.path.join(daily_dir, fname)
                    if compress_file(fpath, args.threshold_l1, args.dry_run, "L1",
                                     snapshot_context):
                        compressed_count += 1
            else:
                print("  (无文件)")
        else:
            print("  (目录不存在)")

        if not args.dry_run:
            print(f"\n📦 归档超过 {args.archive_days} 天的 L1 文件...")
            archived = archive_old_l1(base_dir, uid, args.archive_days, args.dry_run,
                                      snapshot_context)
            if archived == 0:
                print("  (无需归档)")

    if args.level in ("L2", "ALL"):
        weekly_dir = os.path.join(user_dir, "weekly")
        print(f"\n📋 检查 L2 长期记忆（阈值: {args.threshold_l2}行）...")
        if os.path.exists(weekly_dir):
            files = sorted([f for f in os.listdir(weekly_dir) if f.endswith(".md")], reverse=True)
            if files:
                for fname in files:
                    fpath = os.path.join(weekly_dir, fname)
                    if compress_file(fpath, args.threshold_l2, args.dry_run, "L2",
                                     snapshot_context):
                        compressed_count += 1
            else:
                print("  (无文件)")
        else:
            print("  (目录不存在)")

    if args.upgrade:
        upgrade_repeated_themes(base_dir, uid, args.rebase_threshold, args.dry_run,
                               snapshot_context)

    # 创建快照（仅在实际操作且有文件变更时）
    if compressed_count > 0 and not args.dry_run and snapshot_context:
        create_snapshot(base_dir, uid, "compress",
                       f"压缩 {compressed_count} 个文件",
                       snapshot_context)

    print(f"\n{'✅' if compressed_count > 0 else '📊'} 完成！共压缩 {compressed_count} 个文件。")

    if compressed_count > 0 and not args.dry_run:
        print("\n💡 如需回滚: python scripts/memory_compress.py --uid " + uid + " --undo")
        print("💡 查看快照: python scripts/memory_compress.py --uid " + uid + " --list-snapshots")


if __name__ == "__main__":
    main()
