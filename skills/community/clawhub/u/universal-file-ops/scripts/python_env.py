#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
python_env.py — Python 环境管理工具
功能：检测已安装版本、创建/管理 venv、安装/卸载包（含网络重试）、切换版本、干净重装
用法：
  python python_env.py detect                    # 检测系统 Python 版本
  python python_env.py list                      # 列出 venv 已安装包
  python python_env.py setup [--python VERSION] # 创建 venv（默认 3.11）
  python python_env.py install <pkg> [pkg ...] # 安装包（含重试）
  python python_env.py uninstall <pkg> [pkg ...]
  python python_env.py update [--all]           # 更新包
  python python_env.py switch <VERSION>          # 切换 venv 使用的 Python 版本（重建 venv）
  python python_env.py remove                   # 删除 venv
  python python_env.py clean-reinstall          # 干净重装（删除 venv + 重建）
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── 常量 ────────────────────────────────────────────────────────────
from utils import VENV_DIR, ensure_data_dirs, log_operation

DEFAULT_PYTHON_PREFER = (3, 11)   # 默认偏好版本

MIRRORS = [
    "https://pypi.tuna.tsinghua.edu.cn/simple",
    "https://mirrors.aliyun.com/pypi/simple",
    "https://pypi.douban.com/simple",
    "https://pypi.mirrors.ustc.edu.cn/simple",
]

ERROR_CODES = {
    "UFO-5001": "Python 未安装或不在 PATH",
    "UFO-5002": "venv 创建失败",
    "UFO-5003": "pip 安装包失败（网络或其他原因）",
    "UFO-5004": "venv 不存在，请先运行 setup",
    "UFO-5005": "不支持的 Python 版本",
    "UFO-5006": "切换版本失败",
}


# ── 工具函数 ───────────────────────────────────────────────────────────
def _ensure_dirs():
    """确保 venv 父目录存在"""
    os.makedirs(os.path.dirname(VENV_DIR), exist_ok=True)


def _log(msg: str, level: str = "INFO"):
    print(f"[{level}] {msg}", file=sys.stderr)


def _error_response(code: str, detail: str = "") -> str:
    msg = ERROR_CODES.get(code, "未知错误")
    full = f"{msg}（{detail}）" if detail else msg
    return json.dumps({"success": False, "error_code": code, "error": full},
                      ensure_ascii=False)


def _ok_response(data: dict) -> str:
    return json.dumps({"success": True, **data}, ensure_ascii=False)


def _run(cmd: List[str], cwd: Optional[str] = None,
         timeout: int = 120) -> Tuple[int, str, str]:
    """运行命令，返回 (returncode, stdout, stderr)"""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout
        )
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "超时"
    except Exception as e:
        return -1, "", str(e)


def _pip_install_with_retry(pip_exe: str, packages: List[str],
                            max_retry: int = 3) -> Tuple[bool, str]:
    """用多个镜像源重试安装，返回 (成功?, 输出信息)"""
    for attempt in range(max_retry):
        for mirror in MIRRORS:
            cmd = [pip_exe, "install", "-i", mirror] + packages
            rc, out, err = _run(cmd)
            if rc == 0:
                return True, out
            _log(f"  镜像 {mirror} 失败: {err[:100]}", "WARN")
        if attempt < max_retry - 1:
            wait = 2 ** attempt
            _log(f"  第 {attempt+1} 次重试，等待 {wait}s...", "INFO")
            time.sleep(wait)
    return False, err


def _find_python_executable(version_prefer: Tuple[int, int]) -> Optional[str]:
    """查找 Python 可执行文件，优先使用偏好版本"""
    candidates = [
        f"python{version_prefer[0]}.{version_prefer[1]}",
        "python3",
        "python",
    ]
    for cmd in candidates:
        rc, out, _ = _run([cmd, "--version"])
        if rc == 0:
            # 验证版本
            m = re.search(r"(\d+)\.(\d+)", out)
            if m:
                major, minor = int(m.group(1)), int(m.group(2))
                if (major, minor) == version_prefer:
                    return cmd
    # 降级：任意可用 Python
    rc, _, _ = _run(["python", "--version"])
    if rc == 0:
        return "python"
    rc, _, _ = _run(["python3", "--version"])
    if rc == 0:
        return "python3"
    return None


def _detect_installed_versions() -> List[Dict]:
    """检测系统已安装的 Python 版本"""
    results = []
    for cmd in ["python3", "python"]:
        rc, out, _ = _run([cmd, "--version"])
        if rc == 0:
            m = re.search(r"(\d+)\.(\d+)\.(\d+)", out)
            if m:
                results.append({
                    "command": cmd,
                    "version": out,
                    "major": int(m.group(1)),
                    "minor": int(m.group(2)),
                    "micro": int(m.group(3)),
                })
    # Windows 额外检查 py.exe
    if os.name == "nt":
        rc, out, _ = _run(["py", "--list"])
        if rc == 0:
            for line in out.splitlines():
                m = re.search(r"(\d+)\.(\d+)", line)
                if m:
                    results.append({
                        "command": "py",
                        "version": line.strip(),
                        "major": int(m.group(1)),
                        "minor": int(m.group(2)),
                        "micro": 0,
                    })
    return results


def _get_venv_python() -> Optional[str]:
    """返回 venv 中的 python 可执行文件路径"""
    if os.name == "nt":
        path = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        path = os.path.join(VENV_DIR, "bin", "python")
    return path if os.path.exists(path) else None


def _get_venv_pip() -> Optional[str]:
    """返回 venv 中的 pip 可执行文件路径"""
    if os.name == "nt":
        path = os.path.join(VENV_DIR, "Scripts", "pip.exe")
    else:
        path = os.path.join(VENV_DIR, "bin", "pip")
    return path if os.path.exists(path) else None


def _update_requirements():
    """更新 requirements.txt（venv 已安装包列表）"""
    pip = _get_venv_pip()
    if not pip:
        return
    rc, out, _ = _run([pip, "freeze"])
    if rc == 0:
        req_file = os.path.join(os.path.dirname(VENV_DIR), "requirements.txt")
        with open(req_file, "w", encoding="utf-8") as f:
            f.write(out)


def _remove_venv():
    """删除 venv 目录"""
    if os.path.exists(VENV_DIR):
        shutil.rmtree(VENV_DIR, ignore_errors=True)
        _log(f"已删除 venv: {VENV_DIR}", "INFO")


# ── 子命令实现 ────────────────────────────────────────────────────────
def cmd_detect(args):
    versions = _detect_installed_versions()
    venv_py = _get_venv_python()
    result = {
        "installed_versions": versions,
        "venv_exists": os.path.exists(VENV_DIR),
        "venv_python": venv_py,
    }
    if venv_py and os.path.exists(venv_py):
        rc, out, _ = _run([venv_py, "--version"])
        result["venv_python_version"] = out if rc == 0 else "未知"
    print(_ok_response(result))
    return 0


def cmd_list(args):
    if not os.path.exists(VENV_DIR):
        print(_error_response("UFO-5004"))
        return 1
    pip = _get_venv_pip()
    if not pip:
        print(_error_response("UFO-5004"))
        return 1
    rc, out, err = _run([pip, "list", "--format=json"])
    if rc != 0:
        print(_error_response("UFO-5003", err))
        return 1
    import json as _json
    try:
        packages = _json.loads(out)
    except Exception:
        packages = []
    print(_ok_response({"packages": packages}))
    return 0


def cmd_setup(args):
    version = args.python or f"{DEFAULT_PYTHON_PREFER[0]}.{DEFAULT_PYTHON_PREFER[1]}"
    py_cmd = _find_python_executable(DEFAULT_PYTHON_PREFER)
    if not py_cmd:
        print(_error_response("UFO-5001"))
        return 1
    _ensure_dirs()
    if os.path.exists(VENV_DIR):
        _log(f"venv 已存在: {VENV_DIR}，跳过创建", "WARN")
        print(_ok_response({"venv": VENV_DIR, "skipped": True}))
        return 0
    rc, out, err = _run([py_cmd, "-m", "venv", VENV_DIR])
    if rc != 0:
        print(_error_response("UFO-5002", err))
        return 1
    _log(f"venv 创建成功: {VENV_DIR}", "INFO")
    log_operation("python_env_setup", VENV_DIR, "success")
    # 升级 pip
    pip = _get_venv_pip()
    if pip:
        _run([pip, "install", "--upgrade", "pip"])
    print(_ok_response({"venv": VENV_DIR, "python": py_cmd}))
    return 0


def cmd_install(args):
    if not os.path.exists(VENV_DIR):
        print(_error_response("UFO-5004"))
        return 1
    pip = _get_venv_pip()
    if not pip:
        print(_error_response("UFO-5004"))
        return 1
    ok, output = _pip_install_with_retry(pip, args.packages)
    if not ok:
        print(_error_response("UFO-5003", output))
        return 1
    _update_requirements()
    log_operation("python_env_install", ",".join(args.packages), "success")
    print(_ok_response({"installed": args.packages, "output": output}))
    return 0


def cmd_uninstall(args):
    if not os.path.exists(VENV_DIR):
        print(_error_response("UFO-5004"))
        return 1
    pip = _get_venv_pip()
    rc, out, err = _run([pip, "uninstall", "-y"] + args.packages)
    if rc != 0:
        print(_error_response("UFO-5003", err))
        return 1
    _update_requirements()
    log_operation("python_env_uninstall", ",".join(args.packages), "success")
    print(_ok_response({"uninstalled": args.packages}))
    return 0


def cmd_update(args):
    if not os.path.exists(VENV_DIR):
        print(_error_response("UFO-5004"))
        return 1
    pip = _get_venv_pip()
    if args.all:
        rc, out, err = _run([pip, "list", "--outdated", "--format=json"])
        if rc != 0:
            print(_error_response("UFO-5003", err))
            return 1
        import json as _json
        pkgs = [p["name"] for p in _json.loads(out)]
        if not pkgs:
            print(_ok_response({"updated": [], "message": "所有包均为最新"}))
            return 0
        ok, output = _pip_install_with_retry(pip, [f"{p}==" for p in pkgs])
        # 实际用 pip install -U
        rc2, out2, err2 = _run([pip, "install", "-U"] + pkgs)
        if rc2 != 0:
            print(_error_response("UFO-5003", err2))
            return 1
        _update_requirements()
        print(_ok_response({"updated": pkgs}))
    else:
        ok, output = _pip_install_with_retry(pip, [f"{p}==" for p in args.packages])
        rc, out, err = _run([pip, "install", "-U"] + args.packages)
        if rc != 0:
            print(_error_response("UFO-5003", err))
            return 1
        _update_requirements()
        print(_ok_response({"updated": args.packages}))
    return 0


def cmd_switch(args):
    """切换 Python 版本（重建 venv）"""
    new_version = args.version
    if not re.match(r"^\d+\.\d+$", new_version):
        print(_error_response("UFO-5005", new_version))
        return 1
    _remove_venv()
    py_cmd = f"python{new_version}"
    rc, _, err = _run([py_cmd, "--version"])
    if rc != 0:
        print(_error_response("UFO-5006", f"找不到 Python {new_version}"))
        return 1
    _ensure_dirs()
    rc, out, err = _run([py_cmd, "-m", "venv", VENV_DIR])
    if rc != 0:
        print(_error_response("UFO-5002", err))
        return 1
    _log(f"venv 已切换到 Python {new_version}", "INFO")
    log_operation("python_env_switch", new_version, "success")
    print(_ok_response({"venv": VENV_DIR, "python_version": new_version}))
    return 0


def cmd_remove(args):
    _remove_venv()
    log_operation("python_env_remove", VENV_DIR, "success")
    print(_ok_response({"removed": VENV_DIR}))
    return 0


def cmd_clean_reinstall(args):
    _remove_venv()
    py_cmd = _find_python_executable(DEFAULT_PYTHON_PREFER)
    if not py_cmd:
        print(_error_response("UFO-5001"))
        return 1
    _ensure_dirs()
    rc, out, err = _run([py_cmd, "-m", "venv", VENV_DIR])
    if rc != 0:
        print(_error_response("UFO-5002", err))
        return 1
    pip = _get_venv_pip()
    if pip:
        _run([pip, "install", "--upgrade", "pip"])
    log_operation("python_env_clean_reinstall", VENV_DIR, "success")
    print(_ok_response({"venv": VENV_DIR, "reinstalled": True}))
    return 0


# ── CLI ────────────────────────────────────────────────────────────────
def parse_args():
    p = argparse.ArgumentParser(description="Python 环境管理工具")
    sub = p.add_subparsers(dest="command")

    sub.add_parser("detect", help="检测系统 Python 版本")
    sub.add_parser("list", help="列出 venv 已安装包")

    sp_setup = sub.add_parser("setup", help="创建 venv")
    sp_setup.add_argument("--python", help="指定 Python 版本（如 3.11）")

    sp_install = sub.add_parser("install", help="安装包")
    sp_install.add_argument("packages", nargs="+")

    sp_uninstall = sub.add_parser("uninstall", help="卸载包")
    sp_uninstall.add_argument("packages", nargs="+")

    sp_update = sub.add_parser("update", help="更新包")
    sp_update.add_argument("packages", nargs="*")
    sp_update.add_argument("--all", action="store_true", help="更新所有包")

    sp_switch = sub.add_parser("switch", help="切换 Python 版本（重建 venv）")
    sp_switch.add_argument("version", help="目标版本，如 3.12")

    sub.add_parser("remove", help="删除 venv")
    sub.add_parser("clean-reinstall", help="干净重装（删除+重建 venv）")

    return p.parse_args()


def main():
    args = parse_args()
    if not args.command:
        print(json.dumps(
            {"success": False, "error": "需要子命令: detect/list/setup/install/..."},
            ensure_ascii=False
        ))
        sys.exit(1)
    handlers = {
        "detect":           cmd_detect,
        "list":              cmd_list,
        "setup":             cmd_setup,
        "install":           cmd_install,
        "uninstall":         cmd_uninstall,
        "update":            cmd_update,
        "switch":            cmd_switch,
        "remove":            cmd_remove,
        "clean-reinstall":   cmd_clean_reinstall,
    }
    handler = handlers.get(args.command)
    if not handler:
        print(json.dumps(
            {"success": False, "error": f"未知子命令: {args.command}"},
            ensure_ascii=False
        ))
        sys.exit(1)
    sys.exit(handler(args))


if __name__ == "__main__":
    main()
