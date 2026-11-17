"""install.py — 技能包全自动安装（面向 AI，无阻塞）

前提: 用户机器已有 Python 3.10+（产品假设）。

流程:
  1. 平台检测 + Python 版本校验
  2. 建 runtime 目录结构
  3. 下载浏览器（腾讯云镜像优先，双轨 fallback）→ fetch_artifacts.py
  4. 装 pip 依赖 → fetch_artifacts.py
  5. 自检 → selfcheck.py

CLI:
  install.py --full     → 完整安装（默认）
  install.py --browsers → 只装浏览器
  install.py --pip      → 只装依赖
  install.py --check    → 只检查现状（不动）

每次操作输出 JSON，AI 据输出决定下一步。错误即退出（sys.exit(1)）。
"""
import sys
import os
import json
import argparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "shared", "scripts"))
import common
import fetch_artifacts

MIN_PYTHON = (3, 10)


def _mkdirs():
    for sub in [("profiles",), ("sessions", "pending"), ("screenshots",), ("vault",)]:
        common.runtime_dir(*sub)


def check_python():
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PYTHON
    return {"ok": ok, "version": f"{v.major}.{v.minor}.{v.micro}", "required": f"{MIN_PYTHON[0]}.{MIN_PYTHON[1]}+"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--full", action="store_true", help="完整安装（默认）")
    ap.add_argument("--browsers", action="store_true")
    ap.add_argument("--pip", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    py = check_python()
    if args.check:
        import selfcheck
        selfcheck.main()
        return
    if not py["ok"]:
        common.output_json({"status": "error", "message": f"需要 Python {py['required']}，当前 {py['version']}"})
        sys.exit(1)

    _mkdirs()
    common.log(f"[install] Python {py['version']} 通过，目录已建")

    do_all = args.full or (not args.browsers and not args.pip)
    if do_all or args.browsers:
        common.log("[install] 下载浏览器（镜像优先）")
        fetch_artifacts.download_browsers()
    if do_all or args.pip:
        common.log("[install] 安装 pip 依赖")
        fetch_artifacts.install_pip()

    common.output_json({"status": "ok", "message": "安装完成", "next": "creds.py status 配置凭据 → base-cas login --ensure 验证"})


if __name__ == "__main__":
    main()
