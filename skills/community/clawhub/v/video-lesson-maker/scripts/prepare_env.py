#!/usr/bin/env python3
"""
SRT 白板动画 - 环境引导脚本

职责：
  1. 在技能目录下建立隔离的 Python 虚拟环境（已存在则复用）
  2. 核对运行所需的第三方库是否可导入
  3. 自动补齐缺失的库
  4. 末行打印 ENV_PY=<解释器路径>，供上层调用方捕获

用法：
  python prepare_env.py          # 建环境 + 补依赖，输出 ENV_PY
  python prepare_env.py --check  # 仅探测，缺东西就以非零码退出
"""
from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path

# 技能根目录 = 本脚本向上两级
SKILL_ROOT = Path(__file__).resolve().parent.parent
VENV_ROOT = SKILL_ROOT / ".venv"

# 解释器导入名 -> pip 安装名
DEPS: dict[str, str] = {
    "cv2": "opencv-python",
    "numpy": "numpy",
    "av": "av",        # PyAV：纯 pip 安装的 H.264 编码，无需系统 ffmpeg
    "PIL": "Pillow",   # render_annotation_preview.py 画区域编号预览图（含中文标签）
    "soundfile": "soundfile",  # 配音 / 字幕 时间轴测量
    "edge_tts": "edge-tts",    # 云端中文配音合成
}


def interpreter_path() -> Path:
    """虚拟环境里的 python 可执行文件位置（跨平台）。"""
    if sys.platform.startswith("win"):
        return VENV_ROOT / "Scripts" / "python.exe"
    return VENV_ROOT / "bin" / "python"


def child_env() -> dict:
    """给子进程一个干净、可复现的环境（避免继承外部 PYTHONPATH/PYTHONHOME）。"""
    env = os.environ.copy()
    for key in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"):
        env.pop(key, None)
    return env


def ensure_venv(check_only: bool) -> Path:
    py = interpreter_path()
    if py.exists():
        print(f"[ok] 复用现有虚拟环境: {VENV_ROOT}")
        return py

    if check_only:
        print(f"[err] 虚拟环境尚未建立: {VENV_ROOT}")
        sys.exit(1)

    print(f"[..] 建立虚拟环境: {VENV_ROOT}")
    venv.create(str(VENV_ROOT), with_pip=True)
    # venv 建立后补一次 ensurepip，规避部分 Windows 环境 ensurepip 未落盘的问题
    subprocess.run([str(py), "-m", "ensurepip", "--upgrade"], capture_output=True, env=child_env())
    print("[ok] 虚拟环境就绪")
    return py


def can_import(py: Path, import_name: str) -> bool:
    probe = subprocess.run(
        [str(py), "-c", f"import {import_name}"],
        capture_output=True,
        env=child_env(),
    )
    return probe.returncode == 0


def install(py: Path, packages: list[str]) -> bool:
    if not packages:
        return True
    print(f"[..] 安装依赖: {', '.join(packages)}")
    res = subprocess.run(
        [str(py), "-m", "pip", "install", "--quiet", *packages],
        capture_output=True,
        text=True,
        env=child_env(),
    )
    if res.returncode != 0:
        print(f"[err] 安装失败:\n{res.stderr}")
        return False
    print("[ok] 依赖安装完成")
    return True


def main() -> None:
    check_only = "--check" in sys.argv

    py = ensure_venv(check_only)

    missing: list[str] = []
    for import_name, pip_name in DEPS.items():
        if can_import(py, import_name):
            print(f"[ok] {pip_name}")
        else:
            print(f"[miss] {pip_name}")
            missing.append(pip_name)

    if missing:
        if check_only:
            print(f"\n缺 {len(missing)} 个依赖: {', '.join(missing)}")
            sys.exit(1)
        if not install(py, missing):
            sys.exit(1)

    # 末行：供调用方捕获的约定输出
    print(f"\nENV_PY={py}")


if __name__ == "__main__":
    main()
