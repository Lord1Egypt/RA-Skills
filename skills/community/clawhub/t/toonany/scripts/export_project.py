#!/usr/bin/env python3
"""Export complete project to a timestamped directory."""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path

from utils.logger import setup_logger


def export_project(project_dir: Path, logger) -> Path:
    """Export project to timestamped directory.

    Returns:
        Path to export directory.
    """
    project_name = project_dir.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_name = f"{project_name}_export_{timestamp}"
    export_dir = Path("exports") / export_name

    export_dir.mkdir(parents=True, exist_ok=True)

    logger.info(f"Exporting to: {export_dir}")

    # Copy all files
    for item in project_dir.iterdir():
        if item.is_dir():
            shutil.copytree(item, export_dir / item.name, dirs_exist_ok=True)
        else:
            shutil.copy2(item, export_dir / item.name)

    # Create manifest
    manifest = export_dir / "MANIFEST.md"
    manifest.write_text(
        f"# 项目导出清单\n\n"
        f"## 项目信息\n"
        f"- 名称: {project_name}\n"
        f"- 导出时间: {datetime.now().isoformat()}\n"
        f"- 导出版本: 1.0\n\n"
        f"## 文件统计\n"
        f"- Markdown 文件: {len(list(export_dir.rglob('*.md')))}\n"
        f"- JSON 文件: {len(list(export_dir.rglob('*.json')))}\n"
        f"- 图片文件: {len(list(export_dir.rglob('*.jpg'))) + len(list(export_dir.rglob('*.png')))}\n"
        f"- 视频文件: {len(list(export_dir.rglob('*.mp4')))}\n"
        f"- 音频文件: {len(list(export_dir.rglob('*.mp3')))}\n",
        encoding="utf-8"
    )

    logger.info(f"Export complete: {export_dir}")
    return export_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Toonany project")
    parser.add_argument("--project", "-p", type=str, default=".", help="Project directory")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    logger = setup_logger("export", verbose=args.verbose)
    project_dir = Path(args.project)

    if not project_dir.exists():
        logger.error(f"Project not found: {project_dir}")
        return 1

    export_dir = export_project(project_dir, logger)
    print(f"\n导出完成: {export_dir.absolute()}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
