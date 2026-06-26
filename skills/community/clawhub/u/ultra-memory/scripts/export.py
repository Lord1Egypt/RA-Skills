#!/usr/bin/env python3
"""
ultra-memory: 记忆导出脚本
将所有记忆（会话日志、摘要、语义层）打包为 zip 备份文件
"""

import os
import sys
import json
import shutil
import argparse
import zipfile
from datetime import datetime, timezone
from pathlib import Path

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8")

ULTRA_MEMORY_HOME = Path(os.environ.get("ULTRA_MEMORY_HOME", Path.home() / ".ultra-memory"))


def export_memory(
    output_path: str = None,
    project: str = None,
    include_archive: bool = False,
    days: int = None,
):
    """
    导出 ultra-memory 数据为 zip 备份。

    Args:
        output_path: 输出 zip 文件路径（默认 ~/ultra-memory-backup-<date>.zip）
        project: 只导出指定项目（None 表示全部）
        include_archive: 是否包含 archive/ 目录中的归档会话
        days: 只导出最近 N 天的会话（None 表示全部）
    """
    if not ULTRA_MEMORY_HOME.exists():
        print(f"[ultra-memory] 记忆目录不存在: {ULTRA_MEMORY_HOME}")
        return

    # 默认输出路径
    if not output_path:
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = str(Path.home() / f"ultra-memory-backup-{date_str}.zip")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc)
    cutoff = None
    if days is not None:
        from datetime import timedelta
        cutoff = now - timedelta(days=days)

    added_files = 0
    skipped_files = 0

    print(f"[ultra-memory] 开始导出到: {output_path}")
    if project:
        print(f"[ultra-memory] 过滤项目: {project}")
    if cutoff:
        print(f"[ultra-memory] 只导出 {cutoff.strftime('%Y-%m-%d')} 之后的数据")

    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 1. 导出 semantic 目录（用户画像、知识库、会话索引）
        semantic_dir = ULTRA_MEMORY_HOME / "semantic"
        if semantic_dir.exists():
            for file in semantic_dir.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(ULTRA_MEMORY_HOME)
                    zf.write(file, arcname)
                    added_files += 1
            print(f"[ultra-memory] ✅ 导出语义层: {semantic_dir}")

        # 2. 导出 sessions 目录
        sessions_dir = ULTRA_MEMORY_HOME / "sessions"
        if sessions_dir.exists():
            for session_dir in sessions_dir.iterdir():
                if not session_dir.is_dir():
                    continue

                meta_file = session_dir / "meta.json"
                if not meta_file.exists():
                    continue

                with open(meta_file) as f:
                    meta = json.load(f)

                # 过滤项目
                if project and meta.get("project") != project:
                    skipped_files += 1
                    continue

                # 过滤时间
                if cutoff:
                    ts_str = meta.get("started_at", "")
                    try:
                        ts = datetime.fromisoformat(ts_str.rstrip("Z")).replace(tzinfo=timezone.utc)
                        if ts < cutoff:
                            skipped_files += 1
                            continue
                    except Exception:
                        pass

                # 将整个会话目录打包
                for file in session_dir.rglob("*"):
                    if file.is_file():
                        arcname = file.relative_to(ULTRA_MEMORY_HOME)
                        zf.write(file, arcname)
                        added_files += 1

                print(f"  + {session_dir.name} (项目: {meta.get('project', '?')}, "
                      f"操作数: {meta.get('op_count', 0)})")

        # 3. 可选：导出 archive 目录
        if include_archive:
            archive_dir = ULTRA_MEMORY_HOME / "archive"
            if archive_dir.exists():
                for file in archive_dir.rglob("*"):
                    if file.is_file():
                        arcname = file.relative_to(ULTRA_MEMORY_HOME)
                        zf.write(file, arcname)
                        added_files += 1
                print(f"[ultra-memory] ✅ 导出归档层: {archive_dir}")

        # 4. 写入导出元信息
        export_meta = {
            "exported_at": now.isoformat(),
            "ultra_memory_home": str(ULTRA_MEMORY_HOME),
            "filter_project": project,
            "filter_days": days,
            "include_archive": include_archive,
            "total_files": added_files,
        }
        zf.writestr("export_meta.json", json.dumps(export_meta, ensure_ascii=False, indent=2))

    # 统计 zip 大小
    zip_size_kb = output_path.stat().st_size / 1024

    print(f"\n[ultra-memory] ✅ 导出完成")
    print(f"  输出文件: {output_path}")
    print(f"  文件大小: {zip_size_kb:.1f} KB")
    print(f"  已打包: {added_files} 个文件")
    if skipped_files:
        print(f"  已跳过: {skipped_files} 个会话（不符合过滤条件）")
    print(f"\n  恢复方式: unzip {output_path} -d ~/.ultra-memory/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="导出 ultra-memory 数据为 zip 备份")
    parser.add_argument("--output", default=None, help="输出 zip 路径（默认 ~/ultra-memory-backup-<date>.zip）")
    parser.add_argument("--project", default=None, help="只导出指定项目（默认全部）")
    parser.add_argument("--include-archive", action="store_true", help="同时导出归档会话")
    parser.add_argument("--days", type=int, default=None, help="只导出最近 N 天的会话")
    args = parser.parse_args()
    export_memory(args.output, args.project, args.include_archive, args.days)
