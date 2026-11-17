#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""本地工具链（IndexTTS / 音色库）的路径解析。

整个 skill 只有这一个文件读 `SHADIAO_TOOLCHAIN`，其余脚本只拿现成的 Path。
这样「外部路径从哪来」只有一处、好审计，也方便在调用前做存在性检查。

工具链不在本仓库内：不装 clone 引擎的人完全可以忽略这里。
"""

import os
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[3]


def toolchain_root():
    """工具链根目录：$SHADIAO_TOOLCHAIN，缺省是 skill 的上一级。"""
    return Path(os.environ.get("SHADIAO_TOOLCHAIN", str(SKILL_ROOT.parent))).expanduser()


def resolve():
    root = toolchain_root()
    voice_lib = root / "23-视频制作" / "10-音色制作" / "voice-timbre-library"
    return {
        "root": root,
        "voice_lib": voice_lib,
        "make_emotion": voice_lib / "scripts" / "make_emotion.py",
        "douyin_dir": root / "23-视频制作" / "10-音色制作" / "抖音",
        "default_clone": voice_lib
        / "assets"
        / "source"
        / "音色音频"
        / "aishell3"
        / "SSB0623.wav",
    }


_PATHS = resolve()

TOOLCHAIN = _PATHS["root"]
VOICE_LIB = _PATHS["voice_lib"]
MAKE_EMOTION = _PATHS["make_emotion"]
DOUYIN_DIR = _PATHS["douyin_dir"]
DEFAULT_CLONE = _PATHS["default_clone"]
