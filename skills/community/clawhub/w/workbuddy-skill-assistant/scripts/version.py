#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
version.py — 本 skill 的单一版本源。

版本号只在 `SKILL.md` frontmatter 的 `version:` 定义一次，所有脚本从这里取，
杜绝多处硬编码漂移（历史缺陷：publish_build=6.4.1 而其余脚本=6.3.0）。

兜底也不写死版本号：SKILL.md 不可读时（脱离 skill 目录单独运行），改从同目录
`manifest.json` 的 version 兜底，仍取不到才返回 "unknown"。硬编码兜底会伪装成
一个"可信版本号"，目录结构一变便静默漂移——静默错误比崩溃更危险。

用法：
  from version import VERSION
改版本号：只改 `SKILL.md` 的 `version:`，无需再动任何脚本。
"""
import json
import re
from pathlib import Path

_SKILL_MD = Path(__file__).resolve().parent.parent / "SKILL.md"

# 兜底返回的显式异常标记（不是版本号）；正常路径永远取不到它
UNKNOWN = "unknown"


def _read_skill_version():
    try:
        text = _SKILL_MD.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(r"^version:\s*(\S+)\s*$", text, re.MULTILINE)
    return m.group(1) if m else None


def _read_manifest_version():
    """从 SKILL.md 同目录的 manifest.json 兜底取版本（不硬编码）。"""
    try:
        data = json.loads(
            (_SKILL_MD.parent / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    v = data.get("version")
    return str(v) if v else None


VERSION = _read_skill_version() or _read_manifest_version() or UNKNOWN

if __name__ == "__main__":
    print(VERSION)
