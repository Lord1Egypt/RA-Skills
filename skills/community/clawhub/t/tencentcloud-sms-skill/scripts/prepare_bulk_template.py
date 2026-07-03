#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
prepare_bulk_template.py

从 Skill 内置 assets 复制一份**全新空白**的群发 Excel 模板到目标目录，
文件名带时间戳避免覆盖。

目标目录策略（重要——适配多 channel）：
- 默认落到**当前工作目录**（cwd，即用户/Agent 的工作区），而非桌面。
  因为用户可能通过各类聊天 channel 使用 Agent，这些环境并没有
  「桌面」概念，文件应放在工作区内，再由宿主作为附件下发给用户。
- 仅当用户**显式**通过 --dest-dir 指定目录时，才使用该目录。

自动打开策略（默认关闭——仅桌面端可用）：
- 默认**不**自动打开文件（opened=false），适配聊天 channel：此时应由宿主
  将文件作为**附件发送**给用户，而不是在服务端「打开」文件。
- 仅当**显式**传入 --open 且当前确为本地桌面 GUI 环境时，才尝试用系统默认
  程序打开（macOS `open` / Windows `os.startfile` / Linux 有 DISPLAY 时 `xdg-open`）。

设计目的：
- 解决「直接使用 assets 下模板会被反复填写、残留旧数据」的问题。
- 跨 channel 一致：默认把新副本生成到工作区并以附件下发，桌面端可选自动打开。

输出 JSON：
    {
      "source": "<SKILL_DIR>/assets/国内短信群发模板.xlsx",
      "destination": "/path/to/workspace/国内短信群发模板_20260610_111200.xlsx",
      "opened": false,
      "platform": "darwin",
      "international": 0
    }
"""

import argparse
import datetime as _dt
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ASSET_MAP = {
    0: "国内短信群发模板.xlsx",
    1: "国际港澳台短信群发模板.xlsx",
}


def _err(message: str, code: str = "PREPARE_TEMPLATE_ERROR") -> None:
    """以结构化 JSON 输出错误并退出。"""
    print(
        json.dumps({"error": code, "message": message}, ensure_ascii=False),
        file=sys.stderr,
    )
    sys.exit(1)


def _default_dest_dir() -> Path:
    """返回当前工作目录（工作区）作为默认目标目录。"""
    return Path.cwd()


def _is_headless_linux() -> bool:
    """Linux 下若没有 DISPLAY/WAYLAND_DISPLAY 视为无 GUI。"""
    return not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY"))


def _try_open(path: Path) -> bool:
    """尝试用系统默认程序打开文件，成功返回 True，失败/无 GUI 返回 False。"""
    system = platform.system().lower()
    try:
        if system == "darwin":
            subprocess.Popen(
                ["open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        if system == "windows":
            os.startfile(str(path))  # type: ignore[attr-defined]
            return True
        if system == "linux":
            if _is_headless_linux():
                return False
            subprocess.Popen(
                ["xdg-open", str(path)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
    except Exception:  # pylint: disable=broad-except
        return False
    return False


def main() -> None:
    parser = argparse.ArgumentParser(
        description="复制群发 Excel 模板到目标目录（默认当前工作区），默认不自动打开",
    )
    parser.add_argument(
        "--international",
        type=int,
        choices=[0, 1],
        default=0,
        help="0=国内短信（默认），1=国际/港澳台短信",
    )
    parser.add_argument(
        "--dest-dir",
        type=str,
        default=None,
        help="目标目录，默认当前工作目录（工作区）；仅在显式需要时指定（如 ~/Desktop）",
    )
    parser.add_argument(
        "--open",
        dest="open_file",
        action="store_true",
        help="仅本地桌面端使用：复制后尝试用系统默认程序打开文件。"
             "默认不打开（聊天 channel 下应由宿主以附件下发）",
    )
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parent.parent
    src = skill_root / "assets" / ASSET_MAP[args.international]
    if not src.is_file():
        _err(f"内置模板文件不存在: {src}", code="ASSET_NOT_FOUND")

    if args.dest_dir:
        dest_dir = Path(args.dest_dir).expanduser().resolve()
    else:
        dest_dir = _default_dest_dir()

    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        _err(f"创建目标目录失败: {dest_dir} ({exc})", code="DEST_DIR_CREATE_FAILED")

    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = dest_dir / f"{src.stem}_{timestamp}{src.suffix}"

    try:
        shutil.copy2(src, dest)
    except OSError as exc:
        _err(f"复制模板失败: {exc}", code="COPY_FAILED")

    opened = _try_open(dest) if args.open_file else False

    print(json.dumps(
        {
            "source": str(src),
            "destination": str(dest),
            "opened": opened,
            "platform": platform.system().lower(),
            "international": args.international,
        },
        ensure_ascii=False,
        indent=2,
    ))


if __name__ == "__main__":
    main()
