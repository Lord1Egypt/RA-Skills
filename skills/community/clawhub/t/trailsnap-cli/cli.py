#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

# 将当前目录加入 sys.path 以便导入同级模块
sys.path.insert(0, str(Path(__file__).parent))

from commands import config, photos, tags, albums, locations, people, folders, medias

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(errors="replace")

    parser = argparse.ArgumentParser(description="TrailSnap CLI 命令行工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    subparsers.required = True

    # 注册各个子命令
    config.setup_parser(subparsers)
    photos.setup_parser(subparsers)
    tags.setup_parser(subparsers)
    albums.setup_parser(subparsers)
    locations.setup_parser(subparsers)
    people.setup_parser(subparsers)
    folders.setup_parser(subparsers)
    medias.setup_parser(subparsers)

    args = parser.parse_args()

    # 执行对应的命令处理函数
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
