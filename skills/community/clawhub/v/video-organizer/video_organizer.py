#!/usr/bin/env python3
"""
Video Organizer - 视频文件批量重命名和整理工具
"""

import os
import json
import argparse
from datetime import datetime
from pathlib import Path
from shutil import copy2


class VideoOrganizer:
    def __init__(self, input_dir, output_dir=None):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir) if output_dir else self.input_dir / "organized"
        self.backup_file = self.output_dir / ".video-organizer-backup.json"
        self.backup_data = {}

        self.video_extensions = {
            ".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".webm",
            ".m4v", ".mpg", ".mpeg", ".3gp", ".ogv", ".ts"
        }

    def load_backup(self):
        if self.backup_file.exists():
            with open(self.backup_file, 'r', encoding='utf-8') as f:
                self.backup_data = json.load(f)
        return self.backup_data

    def save_backup(self, mappings):
        self.output_dir.mkdir(parents=True, exist_ok=True)
        with open(self.backup_file, 'w', encoding='utf-8') as f:
            json.dump(mappings, f, indent=2, ensure_ascii=False)

    def get_video_files(self):
        videos = []
        for item in self.input_dir.iterdir():
            if item.is_file() and item.suffix.lower() in self.video_extensions:
                videos.append(item)
        return sorted(videos)

    def get_date_components(self, file_path):
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
        return mtime.strftime('%Y'), mtime.strftime('%m'), mtime.strftime('%d')

    def get_folder_path(self, file_path, organize_by='date'):
        if organize_by == 'date':
            year, month, day = self.get_date_components(file_path)
            return self.output_dir / year / month
        elif organize_by == 'format':
            ext = file_path.suffix.lstrip('.').lower()
            return self.output_dir / ext
        else:
            return self.output_dir

    def generate_name(self, file_path, pattern, index):
        name = pattern
        stem = file_path.stem
        ext = file_path.suffix.lstrip('.')
        year, month, day = self.get_date_components(file_path)

        name = name.replace('{001}', f'{index+1:03d}')
        name = name.replace('{01}', f'{index+1:02d}')
        name = name.replace('{1}', f'{index+1}')
        name = name.replace('{YYYY}', year)
        name = name.replace('{MM}', month)
        name = name.replace('{DD}', day)
        name = name.replace('{original}', stem)
        name = name.replace('{ext}', ext)

        return name

    def organize(self, organize_by='date', preview=False):
        videos = self.get_video_files()
        mappings = {}

        for video_path in videos:
            target_folder = self.get_folder_path(video_path, organize_by)
            target_path = target_folder / video_path.name

            mappings[str(video_path)] = str(target_path)

            if preview:
                if organize_by == 'date':
                    year, month, day = self.get_date_components(video_path)
                    print(f"预览: {video_path.name} -> {year}/{month}/{video_path.name}")
                elif organize_by == 'format':
                    ext = video_path.suffix.lstrip('.').lower()
                    print(f"预览: {video_path.name} -> {ext}/{video_path.name}")
                else:
                    print(f"预览: {video_path.name} -> {video_path.name}")

        if preview:
            return mappings

        confirm = input(f"即将整理 {len(mappings)} 个视频，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        # 保存备份
        self.save_backup(mappings)

        # 执行整理
        for old_str, new_str in mappings.items():
            old_path = Path(old_str)
            new_path = Path(new_str)
            new_path.parent.mkdir(parents=True, exist_ok=True)
            if old_path.exists() and not new_path.exists():
                copy2(old_path, new_path)
                print(f"整理: {old_path.name} -> {new_path.parent.name}/{new_path.name}")

        return mappings

    def rename(self, pattern=None, regex=None, preview=False):
        videos = self.get_video_files()
        mappings = {}

        for i, video_path in enumerate(videos):
            if pattern:
                new_name = self.generate_name(video_path, pattern, i)
                target_path = self.input_dir / new_name
            elif regex:
                new_name = self.apply_regex(video_path.name, regex)
                target_path = self.input_dir / new_name
            else:
                continue

            mappings[str(video_path)] = str(target_path)

            if preview:
                print(f"预览: {video_path.name} -> {target_path.name}")

        if preview:
            return mappings

        confirm = input(f"即将重命名 {len(mappings)} 个视频，确认吗？(y/N): ")
        if confirm.lower() != 'y':
            print("操作已取消")
            return {}

        # 保存备份
        self.save_backup(mappings)

        # 执行重命名
        for old_str, new_str in mappings.items():
            old_path = Path(old_str)
            new_path = Path(new_str)
            if old_path.exists() and not new_path.exists():
                old_path.rename(new_path)
                print(f"重命名: {old_path.name} -> {new_path.name}")

        return mappings

    def apply_regex(self, filename, pattern):
        if pattern.startswith('s/'):
            parts = pattern.split('/')
            if len(parts) >= 3:
                search = parts[1]
                replace = parts[2]
                return __import__('re').sub(search, replace, filename)
        return filename

    def undo(self):
        backup = self.load_backup()
        if not backup:
            print("没有找到备份文件，无法撤销")
            return False

        reverse_mappings = {v: k for k, v in backup.items()}
        count = 0

        for new_str, old_str in reverse_mappings.items():
            new_path = Path(new_str)
            old_path = Path(old_str)
            if new_path.exists() and not old_path.exists():
                new_path.rename(old_path)
                print(f"撤销: {new_path.name} -> {old_path.name}")
                count += 1

        if count > 0:
            self.backup_file.unlink(missing_ok=True)
            print(f"已撤销 {count} 个视频的操作")
            return True
        else:
            print("没有需要撤销的视频")
            return False


def main():
    parser = argparse.ArgumentParser(description="视频文件批量重命名和整理工具")
    subparsers = parser.add_subparsers(title="命令", dest="command")

    # organize 命令
    organize_parser = subparsers.add_parser("organize", help="整理视频")
    organize_parser.add_argument("directory", help="视频目录")
    organize_parser.add_argument("--by", choices=["date", "format"], default="date", help="整理方式（默认按时间）")
    organize_parser.add_argument("--output", help="输出目录")
    organize_parser.add_argument("--preview", action="store_true", help="预览模式")

    # rename 命令
    rename_parser = subparsers.add_parser("rename", help="重命名视频")
    rename_parser.add_argument("directory", help="视频目录")
    rename_parser.add_argument("--pattern", help="命名模式")
    rename_parser.add_argument("--regex", help="正则表达式替换")
    rename_parser.add_argument("--preview", action="store_true", help="预览模式")

    # undo 命令
    undo_parser = subparsers.add_parser("undo", help="撤销操作")
    undo_parser.add_argument("directory", help="输出目录")

    args = parser.parse_args()

    if args.command == "organize":
        organizer = VideoOrganizer(args.directory, args.output)
        organizer.organize(organize_by=args.by, preview=args.preview)
    elif args.command == "rename":
        organizer = VideoOrganizer(args.directory, args.directory)
        organizer.rename(pattern=args.pattern, regex=args.regex, preview=args.preview)
    elif args.command == "undo":
        organizer = VideoOrganizer(args.directory, args.directory)
        organizer.undo()


if __name__ == "__main__":
    main()
