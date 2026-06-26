#!/usr/bin/env python3
import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path


def read_content(args) -> str:
    if args.stdin:
        return sys.stdin.read()
    if args.file:
        return Path(args.file).read_text(encoding='utf-8')
    return ''


def backup_if_exists(target: Path) -> Path | None:
    if not target.exists():
        return None
    stamp = datetime.now().strftime('%Y-%m-%d-%H')
    backup = target.with_name(f'productdemand.backup.{stamp}.md')
    shutil.copy2(target, backup)
    return backup


def main() -> int:
    parser = argparse.ArgumentParser(description='Backup and write productdemand.md')
    parser.add_argument('--project-dir', required=True, help='Target project directory')
    parser.add_argument('--demand-file-name', default='productdemand.md', help='Demand file name inside project dir')
    parser.add_argument('--stdin', action='store_true', help='Read demand content from stdin')
    parser.add_argument('--file', help='Read demand content from a file')
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    demand_file = project_dir / args.demand_file_name

    content = read_content(args)
    if not content or not content.strip():
        print('Demand content is empty.', file=sys.stderr)
        return 2

    project_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_if_exists(demand_file)
    normalized = content.rstrip() + '\n'
    demand_file.write_text(normalized, encoding='utf-8')

    print(f'PROJECT_DIR={project_dir}')
    print(f'WROTE={demand_file}')
    if backup:
        print(f'BACKUP={backup}')
    else:
        print('BACKUP=')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
