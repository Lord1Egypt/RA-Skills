#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
ensure_python_env.py  【OpenClaw 内部工具脚本】

检查并确保指定 Python 版本的虚拟环境存在于 ~/.python_env/<python_version>。
该环境按版本号命名，可被多个 skill 共享复用。
若 uv 未安装则自动安装；若环境不存在则用 uv venv 创建。

用法（供其他 skill 脚本调用，或 OpenClaw 直接 uv run）：
    uv run ensure_python_env.py <python_version> [--packages pkg1 pkg2 ...]

参数:
    python_version   必填，如 3.11、3.12
    --packages       可选，追加安装到该环境的包（幂等）

示例：
    uv run ensure_python_env.py 3.11
    uv run ensure_python_env.py 3.11 --packages requests httpx
    uv run ensure_python_env.py 3.12 --packages requests pillow numpy

返回（stdout 末尾机器可读行，供调用方 grep 解析）：
    PYTHON_ENV_ACTIVATE:/path/to/activate
    PYTHON_ENV_DIR:/path/to/env
    PYTHON_ENV_VERSION:3.11
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path


def log_info(msg: str) -> None:
    print(f"[skill-python-env] {msg}")


def log_ok(msg: str) -> None:
    print(f"[skill-python-env] ✓ {msg}")


def log_warn(msg: str) -> None:
    print(f"[skill-python-env] ⚠ {msg}", file=sys.stderr)


def log_error(msg: str) -> None:
    print(f"[skill-python-env] ✗ {msg}", file=sys.stderr)


def is_windows() -> bool:
    return platform.system() == "Windows"


def get_activate_path(env_dir: Path) -> Path:
    if is_windows():
        return env_dir / "Scripts" / "activate"
    return env_dir / "bin" / "activate"


# ── 1. 检查/安装 uv ───────────────────────────────────────

def find_uv() -> str | None:
    """返回 uv 可执行路径，找不到返回 None。"""
    if shutil.which("uv"):
        return "uv"
    candidates: list[Path] = [
        Path.home() / ".local" / "bin" / "uv",
        Path.home() / ".cargo" / "bin" / "uv",
    ]
    if is_windows():
        up = os.environ.get("USERPROFILE", "")
        la = os.environ.get("LOCALAPPDATA", "")
        candidates += [
            Path(up) / ".local" / "bin" / "uv.exe",
            Path(la) / "uv" / "uv.exe",
        ]
    for c in candidates:
        if c.exists():
            # 将其目录加入 PATH，让后续子进程也能直接调用 uv
            extra = str(c.parent)
            os.environ["PATH"] = extra + os.pathsep + os.environ.get("PATH", "")
            return str(c)
    return None


def install_uv() -> str:
    """安装 uv，返回可用路径，失败则 sys.exit(1)。"""
    log_warn("未检测到 uv，正在安装...")

    if is_windows():
        ps = shutil.which("powershell.exe") or shutil.which("powershell")
        if not ps:
            log_error("未找到 PowerShell，请手动安装 uv：")
            log_error("  https://docs.astral.sh/uv/getting-started/installation/")
            sys.exit(1)
        log_info("使用 PowerShell 安装 uv...")
        result = subprocess.run(
            [ps, "-ExecutionPolicy", "ByPass", "-Command",
             "irm https://astral.sh/uv/install.ps1 | iex"],
            check=False,
        )
        if result.returncode != 0:
            log_error("PowerShell 安装 uv 失败，请手动安装：")
            log_error("  https://docs.astral.sh/uv/getting-started/installation/")
            sys.exit(1)
    else:
        curl = shutil.which("curl")
        wget = shutil.which("wget")
        if curl:
            log_info("使用 curl 安装 uv...")
            proc = subprocess.run([curl, "-LsSf", "https://astral.sh/uv/install.sh"],
                                  stdout=subprocess.PIPE, check=True)
            subprocess.run(["sh"], input=proc.stdout, check=True)
        elif wget:
            log_info("使用 wget 安装 uv...")
            proc = subprocess.run([wget, "-qO-", "https://astral.sh/uv/install.sh"],
                                  stdout=subprocess.PIPE, check=True)
            subprocess.run(["sh"], input=proc.stdout, check=True)
        else:
            log_error("未找到 curl 或 wget，请手动安装 uv：")
            log_error("  https://docs.astral.sh/uv/getting-started/installation/")
            sys.exit(1)

    # 将常见安装目录加入当前进程 PATH
    for extra in [
        str(Path.home() / ".local" / "bin"),
        str(Path.home() / ".cargo" / "bin"),
    ]:
        os.environ["PATH"] = extra + os.pathsep + os.environ.get("PATH", "")

    uv_path = find_uv()
    if not uv_path:
        log_error("uv 安装后仍未找到，请重启终端后重试，或手动安装：")
        log_error("  https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)

    version = subprocess.check_output([uv_path, "--version"], text=True).strip()
    log_ok(f"uv 安装成功：{version}")
    if is_windows():
        log_warn(r"请将 %USERPROFILE%\.local\bin 加入系统 PATH 以永久生效")
    else:
        log_warn("请将以下行加入 ~/.bashrc 或 ~/.zshrc 以永久生效：")
        log_warn('  export PATH="$HOME/.local/bin:$PATH"')
    return uv_path


def check_or_install_uv() -> str:
    uv_path = find_uv()
    if uv_path:
        version = subprocess.check_output([uv_path, "--version"], text=True).strip()
        log_ok(f"uv 已安装：{version}")
        return uv_path
    return install_uv()


# ── 2. 检查/创建虚拟环境 ──────────────────────────────────

def ensure_env(uv_path: str, env_dir: Path, python_version: str) -> None:
    activate = get_activate_path(env_dir)

    if env_dir.exists() and activate.exists():
        log_ok(f"Python {python_version} 环境已存在：{env_dir}")
        return

    if env_dir.exists() and not activate.exists():
        log_warn(f"目录 {env_dir} 存在但环境不完整，重新创建...")
        shutil.rmtree(env_dir)

    log_info(f"创建 Python {python_version} 虚拟环境：{env_dir}")
    env_dir.parent.mkdir(parents=True, exist_ok=True)

    result = subprocess.run(
        [uv_path, "venv", str(env_dir), "--python", python_version],
        check=False,
    )
    if result.returncode != 0:
        log_error(f"虚拟环境创建失败（Python {python_version}）")
        sys.exit(1)
    log_ok("虚拟环境创建成功")


# ── 3. 安装依赖包（幂等，已安装的包会被跳过） ────────────

def install_packages(uv_path: str, env_dir: Path, packages: list[str]) -> None:
    if not packages:
        return
    log_info(f"安装依赖包：{' '.join(packages)}")
    result = subprocess.run(
        [uv_path, "pip", "install", "--python", str(env_dir), *packages],
        check=False,
    )
    if result.returncode != 0:
        log_error(f"依赖包安装失败：{' '.join(packages)}")
        sys.exit(1)
    log_ok("依赖包安装成功")


# ── 4. 输出机器可读结果 ───────────────────────────────────

def print_result(env_dir: Path, python_version: str) -> None:
    activate = get_activate_path(env_dir)
    print()
    print("[skill-python-env] ── 环境就绪 ──────────────────────────────")
    print(f"[skill-python-env] Python 版本：{python_version}")
    print(f"[skill-python-env] 环境路径：{env_dir}")
    if is_windows():
        ps1 = env_dir / "Scripts" / "Activate.ps1"
        print(f"[skill-python-env] 激活（bash）：source \"{activate}\"")
        print(f"[skill-python-env] 激活（PS）  ：& \"{ps1}\"")
    else:
        print(f"[skill-python-env] 激活命令：source \"{activate}\"")
    print("[skill-python-env] ─────────────────────────────────────────")
    # 机器可读行，供调用方 grep 解析
    print(f"PYTHON_ENV_ACTIVATE:{activate}")
    print(f"PYTHON_ENV_DIR:{env_dir}")
    print(f"PYTHON_ENV_VERSION:{python_version}")


# ── 主程序 ────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="[OpenClaw 内部工具] 确保 ~/.python_env/<version> 共享虚拟环境存在"
    )
    parser.add_argument(
        "python_version",
        help="Python 版本，如 3.11、3.12（环境存于 ~/.python_env/<version>）",
    )
    parser.add_argument(
        "--packages", nargs="*", default=[],
        help="需要安装到该环境的包（可选，幂等）",
    )
    args = parser.parse_args()

    python_version: str = args.python_version
    env_dir = Path.home() / ".python_env" / python_version

    log_info(f"检查 Python {python_version} 共享环境")

    uv_path = check_or_install_uv()
    ensure_env(uv_path, env_dir, python_version)
    install_packages(uv_path, env_dir, args.packages or [])
    print_result(env_dir, python_version)


if __name__ == "__main__":
    main()
