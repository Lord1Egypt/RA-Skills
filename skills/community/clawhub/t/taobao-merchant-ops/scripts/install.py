#!/usr/bin/env python3
"""
Taobao Merchant Ops (Customer) - 依赖安装脚本
自动安装所有必需的 Python 包和 Playwright 浏览器
支持 Python 3.9+ (Windows)
"""
from __future__ import annotations

import subprocess
import sys
import os
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ─────────────────────────────────────────────
# 依赖清单
# ─────────────────────────────────────────────
SYSTEM_PACKAGES = [
    "openpyxl>=3.1.0",
    "pyyaml>=6.0",
    "playwright>=1.40.0",
]

REQUIREMENTS_FILE = Path(__file__).resolve().parents[1] / "requirements.txt"

# ─────────────────────────────────────────────
# 全局解释器
# ─────────────────────────────────────────────
_SELF_PY = Path(sys.executable)


def _has_pip(py: Path) -> bool:
    result = subprocess.run(
        [str(py), "-m", "pip", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode == 0


def find_python_with_pip() -> Path:
    """找一个有 pip 的 Python 解释器"""
    if _has_pip(_SELF_PY):
        return _SELF_PY
    candidates = [
        Path("C:/Python312/python.exe"),
        Path("C:/Python311/python.exe"),
        Path("C:/Python310/python.exe"),
        Path("C:/Program Files/Python312/python.exe"),
        Path("C:/Program Files/Python311/python.exe"),
        Path("C:/Program Files/Python310/python.exe"),
    ]
    for candidate in candidates:
        if candidate.exists() and _has_pip(candidate):
            return candidate
    return _SELF_PY


PY = find_python_with_pip()


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────
def run(
    cmd: list[str],
    *,
    check: bool = True,
    env: dict | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[bytes]:
    print(f"\n>>> {' '.join(cmd)}")
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)
    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=merged_env,
        cwd=cwd,
    )
    if check and result.returncode != 0:
        print(result.stdout.decode("utf-8", errors="replace"))
        raise SystemExit(f"命令失败 (code={result.returncode}): {' '.join(cmd)}")
    return result


def ensure_pip() -> None:
    """确保 pip 可用"""
    try:
        run([str(PY), "-m", "pip", "--version"], check=True)
    except SystemExit:
        print("[*] pip 不可用，尝试安装 pip...")
        try:
            run([str(PY), "ensurepip", "--upgrade"], check=True)
        except SystemExit:
            print("[*] ensurepip 失败，下载 get-pip.py...")
            run(
                [
                    str(PY),
                    "-c",
                    "import urllib.request; urllib.request.urlretrieve('https://bootstrap.pypa.io/get-pip.py', 'get-pip.py')",
                ],
                check=True,
            )
            run([str(PY), "get-pip.py"], check=True)


def install_packages(packages: list[str]) -> None:
    """安装 Python 包"""
    print(f"\n[*] 安装 Python 包: {', '.join(packages)}")
    for pkg in packages:
        run(
            [
                str(PY), "-m", "pip", "install",
                "--quiet",
                "--upgrade",
                pkg,
            ],
            check=True,
        )


def load_packages() -> list[str]:
    if not REQUIREMENTS_FILE.exists():
        return SYSTEM_PACKAGES
    packages = []
    for line in REQUIREMENTS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        packages.append(line)
    return packages or SYSTEM_PACKAGES


def install_playwright_browsers() -> None:
    """安装 Playwright 浏览器"""
    print("\n[*] 安装 Playwright Chromium 浏览器 (约 150MB)...")
    run(
        [
            str(PY), "-m", "playwright",
            "install",
            "--with-deps",
            "chromium",
        ],
        check=True,
    )


def check_python_version() -> None:
    """检查 Python 版本"""
    info = subprocess.run(
        [str(PY), "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    version_str = info.stdout.decode("utf-8", errors="replace").strip()
    import re
    m = re.search(r"Python (\d+)\.(\d+)\.(\d+)", version_str)
    if m:
        major, minor = int(m.group(1)), int(m.group(2))
        if (major, minor) < (3, 9):
            raise SystemExit(
                f"[ERROR] 需要 Python 3.9+，当前版本: {version_str}\n"
                f"   下载地址: https://www.python.org/downloads/"
            )
    print(f"[OK] {version_str}")


def verify_install() -> None:
    """验证安装结果"""
    print("\n[*] 验证安装...")
    errors: list[str] = []

    env = os.environ.copy()
    env["PATH"] = str(PY.parent) + ";" + env.get("PATH", "")

    checks = [
        ("openpyxl", "import openpyxl; print(openpyxl.__version__)"),
        ("pyyaml", "import yaml; print(yaml.__version__)"),
        ("playwright", "import playwright; print(playwright.__version__)"),
    ]

    for name, check in checks:
        result = subprocess.run(
            [str(PY), "-c", check],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
        if result.returncode == 0:
            ver = result.stdout.decode("utf-8", errors="replace").strip()
            print(f"[OK] {name} {ver}")
        else:
            errors.append(name)

    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            browser.close()
        print("[OK] Playwright Chromium (可执行)")
    except Exception:
        errors.append("Playwright Chromium")

    if errors:
        print(f"\n[WARNING] 以下项目未就绪: {', '.join(errors)}")
        print("\n请运行: python install.py --fix")
    else:
        print("\n[SUCCESS] 所有依赖安装成功!")


# ─────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────
def main() -> int:
    print("=" * 50)
    print("Taobao Merchant Ops - 依赖安装")
    print("=" * 50)

    if str(PY) != str(_SELF_PY):
        print(f"[*] 使用 Python: {PY}")

    check_python_version()
    ensure_pip()

    fix_mode = "--fix" in sys.argv or "--repair" in sys.argv
    if fix_mode:
        print("\n[*] 修复模式")

    install_packages(load_packages())
    install_playwright_browsers()
    verify_install()

    print("\n" + "=" * 50)
    print("下一步:")
    print("  1. 运行: python scripts/run_taobao_merchant_ops.py")
    print("  2. 首次运行会提示输入卡密")
    print("=" * 50)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\n\n[ABORT] 安装已取消")
        raise SystemExit(1)
    except Exception as exc:
        print(f"\n[ERROR] 安装失败: {exc}")
        raise SystemExit(1)
