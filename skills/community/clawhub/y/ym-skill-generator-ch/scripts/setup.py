#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""环境自检 + 可选依赖安装。

    python scripts/setup.py                    # 只做环境自检，列出缺什么、怎么补
    python scripts/setup.py --install-pillow   # 装上 Pillow（生成技能图标时需要）

本技能的生成 / 体检 / 打包流程**只用标准库**，不装任何东西就能跑。
唯一的第三方依赖是 Pillow，仅在 `make_icon.py` 处理技能图标（裁切 / 缩放 / 压缩）时用到，
属于**可选**依赖：不装也能出 zip，只是图标得自己压到 512×512 / ≤500KB。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _friendly import explain_exit, pip_install, use_utf8_stdout  # noqa: E402
from _paths import PathResolutionError, SKILLS_HOME_ENV  # noqa: E402
from _paths import skills_dir as detect_skills_dir  # noqa: E402


def has(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def main() -> int:
    use_utf8_stdout()
    argv = sys.argv[1:]
    if argv and argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0

    print("ym-skill-generator 环境自检")
    print("─" * 52)

    ok = True

    major, minor = sys.version_info[:2]
    version_ok = (major, minor) >= (3, 8)
    print(f"{'[OK]' if version_ok else '[X] '} Python {major}.{minor}"
          f"{'' if version_ok else '（需要 3.8+）'}")
    ok &= version_ok

    try:
        installed_dir = detect_skills_dir()
        exists = installed_dir.is_dir()
        print(f"{'[OK]' if exists else '[!] '} 技能安装目录 {installed_dir}")
        if not exists:
            print("     · 目录不存在：平台首次启动会生成；打包安装时也会自动创建")
    except PathResolutionError as e:
        print(f"[!] 技能安装目录 自动定位失败：{e}")
        print(f"     · 设置环境变量 {SKILLS_HOME_ENV} 指向你的技能目录即可")

    pillow_ok = has("PIL")
    print(f"{'[OK]' if pillow_ok else '[i]'} Pillow {'已安装' if pillow_ok else '未安装（可选）'}")
    if not pillow_ok:
        print("     · 只有生成技能图标时才需要它：python scripts/setup.py --install-pillow")
        print("     · 不装也能生成 / 体检 / 打包，只是图标要自己压到 512×512 且 ≤500KB")

    code = 0 if ok else 1
    if "--install-pillow" in argv and not pillow_ok:
        print("\n正在安装 Pillow（失败会自动重试并改用国内镜像）…")
        ok_pip, log = pip_install(["Pillow"])
        for line in log:
            print("    · %s" % line)
        if ok_pip:
            print("[OK] Pillow 安装完成")
        else:
            print("[X] 自动安装失败。手动装任意一条即可：")
            print("    python -m pip install Pillow")
            print("    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple Pillow")
            code = 4
    elif "--install-pillow" in argv:
        print("\nPillow 已存在，无需安装。")

    print("─" * 52)
    print("环境就绪。" if ok else "请先解决上面的 [X] 项。")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
