#!/usr/bin/env python3
"""
ultra-memory: 会话清理脚本
清理 N 天前的历史会话，支持 --archive-only 模式（只归档不删除）
"""

import os
import sys
import json
import shutil
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


def parse_session_date(meta: dict) -> datetime:
    """从 meta 中解析会话开始时间"""
    ts_str = meta.get("started_at", "")
    try:
        return datetime.fromisoformat(ts_str.rstrip("Z")).replace(tzinfo=timezone.utc)
    except Exception:
        return datetime.min.replace(tzinfo=timezone.utc)


def cleanup(days: int = 30, archive_only: bool = False, dry_run: bool = False, project: str = None):
    """
    清理或归档 N 天前的会话。

    Args:
        days: 清理多少天前的会话（默认 30 天）
        archive_only: True 时只将旧会话移动到 archive/，不删除
        dry_run: True 时只打印将要操作的会话，不实际执行
        project: 只清理指定项目的会话（None 表示所有项目）
    """
    sessions_dir = ULTRA_MEMORY_HOME / "sessions"
    archive_dir = ULTRA_MEMORY_HOME / "archive"

    if not sessions_dir.exists():
        print("[ultra-memory] 会话目录不存在，无需清理")
        return

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    print(f"[ultra-memory] 清理 {cutoff.strftime('%Y-%m-%d')} 之前的会话")
    if archive_only:
        print(f"[ultra-memory] 模式: 归档（不删除）")
    if dry_run:
        print(f"[ultra-memory] 模式: 演习（dry-run，不实际执行）")

    removed = 0
    archived = 0
    skipped = 0

    for session_dir in sessions_dir.iterdir():
        if not session_dir.is_dir():
            continue

        meta_file = session_dir / "meta.json"
        if not meta_file.exists():
            continue

        with open(meta_file, encoding="utf-8") as f:
            meta = json.load(f)

        # 过滤项目
        if project and meta.get("project") != project:
            skipped += 1
            continue

        session_date = parse_session_date(meta)
        session_id = meta.get("session_id", session_dir.name)

        if session_date >= cutoff:
            skipped += 1
            continue

        age_days = (datetime.now(timezone.utc) - session_date).days
        print(f"  {'[DRY]' if dry_run else ''} 处理: {session_id} ({age_days} 天前, 项目: {meta.get('project', '?')})")

        if dry_run:
            continue

        if archive_only:
            # 移动到 archive 目录
            archive_dir.mkdir(parents=True, exist_ok=True)
            dest = archive_dir / session_dir.name
            if not dest.exists():
                shutil.move(str(session_dir), str(dest))
                archived += 1
                print(f"    → 已归档到 {dest}")
            else:
                print(f"    ⚠️  归档目标已存在，跳过: {dest}")
        else:
            # 直接删除
            shutil.rmtree(session_dir)
            removed += 1
            print(f"    → 已删除")

    # 同步更新 session_index.json（移除已清理的条目）
    if not dry_run and (removed > 0 or archived > 0):
        _update_session_index(cutoff, project, archive_only)

    print(f"\n[ultra-memory] 清理完成：")
    print(f"  删除: {removed} 个会话")
    print(f"  归档: {archived} 个会话")
    print(f"  跳过: {skipped} 个会话（未到期或不匹配项目）")


def _update_session_index(cutoff: datetime, project: str, archive_only: bool):
    """从 session_index.json 中移除已清理的会话条目"""
    index_file = ULTRA_MEMORY_HOME / "semantic" / "session_index.json"
    if not index_file.exists():
        return

    with open(index_file, encoding="utf-8") as f:
        index = json.load(f)

    original_count = len(index.get("sessions", []))
    kept = []
    for s in index.get("sessions", []):
        ts_str = s.get("started_at", "")
        try:
            ts = datetime.fromisoformat(ts_str.rstrip("Z")).replace(tzinfo=timezone.utc)
        except Exception:
            kept.append(s)
            continue
        if ts >= cutoff:
            kept.append(s)
        elif project and s.get("project") != project:
            kept.append(s)
        elif archive_only:
            # 归档模式：标记为 archived，保留索引条目
            s["archived"] = True
            kept.append(s)

    index["sessions"] = kept
    with open(index_file, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"[ultra-memory] session_index.json: {original_count} → {len(kept)} 条记录")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="清理历史会话")
    parser.add_argument("--days", type=int, default=30, help="清理多少天前的会话（默认 30 天）")
    parser.add_argument("--archive-only", action="store_true", help="只归档到 archive/ 目录，不删除")
    parser.add_argument("--dry-run", action="store_true", help="演习模式，只打印不执行")
    parser.add_argument("--project", default=None, help="只清理指定项目（默认所有项目）")
    parser.add_argument(
        "--run-decay", action="store_true",
        help="执行事实衰减扫描（auto_decay.py），在清理前运行"
    )
    args = parser.parse_args()

    if args.run_decay:
        import subprocess
        scripts_dir = Path(__file__).parent
        python = sys.executable
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        print("[ultra-memory] 运行事实衰减扫描...")
        result = subprocess.run(
            [python, str(scripts_dir / "auto_decay.py"), "--session", args.project or ""],
            capture_output=True, text=True, startupinfo=startupinfo,
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)

    cleanup(args.days, args.archive_only, args.dry_run, args.project)
