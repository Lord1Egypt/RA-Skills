#!/usr/bin/env python3
"""
semantic-split 环境检测与依赖安装脚本 v0.1.0

安装 Pipeline A(语义匹配) + Pipeline B(结构分析) 所需依赖。
支持多种 PyPI 镜像源，国内用户推荐 aliyun/tsinghua。

用法:
  python scripts/setup_env.py --auto-install --mirror aliyun    # 国内推荐
  python scripts/setup_env.py --auto-install                    # 默认源
  python scripts/setup_env.py --check-only                      # 仅检测不安装
"""

import os
import sys
import subprocess
import platform
import time
import datetime

REQUIRED_PACKAGES = [
    "sentence-transformers",   # Pipeline A embedding + CrossEncoder
]

# Pipeline B 为纯正则实现，无需额外依赖。
    "huggingface-hub",         # 模型下载
]

OPTIONAL_PACKAGES = {
    "torch": "torch",
    "modelscope": "modelscope",  # 国内模型下载源
}

MIRRORS = {
    "default": "https://pypi.org/simple/",
    "aliyun": "https://mirrors.aliyun.com/pypi/simple/",
    "tencent": "https://mirrors.cloud.tencent.com/pypi/simple/",
    "tsinghua": "https://pypi.tuna.tsinghua.edu.cn/simple/",
}

LOG_DIR = None


def _log(msg: str):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}")


def _check_python():
    """检查 Python 版本（3.8-3.12 推荐）"""
    v = sys.version_info
    _log(f"Python {v.major}.{v.minor}.{v.micro}")
    if v.major < 3 or (v.major == 3 and v.minor < 8):
        _log("[!] Python >= 3.8 是必需的")
        return False
    if v.minor >= 14:
        _log("[~] Python 3.14+ 可能需更新 pip 版本")
    return True


def _check_package(pkg_name: str) -> bool:
    """检测单个包是否已安装"""
    # 尝试 importlib.metadata（Python 3.8+）
    try:
        import importlib.metadata as ilm
        try:
            ilm.distribution(pkg_name)
            return True
        except ilm.PackageNotFoundError:
            pass
        except StopIteration:
            pass  # Python 3.14+ 兼容问题
    except (ImportError, Exception):
        pass
    # 回退：直接 import
    try:
        __import__(pkg_name.replace("-", "_"))
        return True
    except ImportError:
        pass
    return False


def _check_packages(packages: list) -> dict:
    """检查所有必需包的状态"""
    results = {}
    for pkg in packages:
        installed = _check_package(pkg)
        results[pkg] = installed
        status = "OK" if installed else "MISSING"
        _log(f"  {pkg:<30} [{status}]")
    return results


def _get_pip_cmd():
    """获取正确的 pip 命令"""
    for cmd in [sys.executable + " -m pip", "pip", "pip3"]:
        try:
            r = subprocess.run(cmd.split()[0] if isinstance(cmd, str) else cmd,
                               capture_output=True, shell=False, timeout=5)
            if r.returncode == 0:
                return cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    # fallback
    return sys.executable + " -m pip"


def _pip_run(cmd_parts: list, timeout=300):
    """运行 pip 命令，实时输出"""
    try:
        proc = subprocess.Popen(
            cmd_parts,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        output_lines = []
        for line in iter(proc.stdout.readline, ""):
            if not line:
                break
            line = line.rstrip()
            if line:
                print(f"  {line}")
                output_lines.append(line)
        proc.wait(timeout=timeout)
        return proc.returncode, "\n".join(output_lines)
    except subprocess.TimeoutExpired:
        proc.kill()
        return -1, "TIMEOUT"
    except Exception as e:
        return -1, str(e)


def _install_missing(missing: list, mirror: str, no_deps=False):
    """安装缺失的包"""
    if not missing:
        return True

    pip_cmd = _get_pip_cmd()
    mirror_url = MIRRORS.get(mirror, MIRRORS["default"])

    _log(f"安装 {len(missing)} 个缺失包 (mirror: {mirror})...")

    for pkg in missing:
        _log(f"  安装 {pkg}...")
        cmd = pip_cmd.split()
        cmd += ["install"]
        if no_deps:
            cmd.append("--no-deps")
        cmd.append(pkg)
        if mirror != "default":
            cmd += ["-i", mirror_url]

        rc, output = _pip_run(cmd)
        if rc != 0:
            _log(f"  [!] {pkg} 安装失败 (rc={rc})")
            return False

        # 验证安装
        if not _check_package(pkg):
            _log(f"  [!] {pkg} 安装后验证失败")
            return False
        _log(f"  [OK] {pkg} 安装成功")

    return True


def _install_pytorch(mirror: str):
    """安装 PyTorch CPU 版本"""
    if _check_package("torch"):
        _log("  torch 已安装，跳过")
        return True

    _log("安装 PyTorch (CPU only)...")
    pip_cmd = _get_pip_cmd()
    mirror_url = MIRRORS.get(mirror, MIRRORS["default"])

    cmd = pip_cmd.split() + [
        "install", "torch",
        "--index-url", "https://download.pytorch.org/whl/cpu",
    ]
    if mirror != "default":
        cmd += ["-i", mirror_url]

    rc, output = _pip_run(cmd, timeout=600)
    if rc != 0:
        _log("[!] PyTorch 安装失败")
        return False
    if not _check_package("torch"):
        _log("[!] PyTorch 安装后验证失败")
        return False
    _log("  [OK] PyTorch 安装成功")
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="semantic-split 环境检测与安装")
    parser.add_argument("--auto-install", action="store_true", help="自动安装缺失依赖")
    parser.add_argument("--check-only", action="store_true", help="仅检测，不安装")
    parser.add_argument("--mirror", choices=list(MIRRORS.keys()), default="aliyun",
                        help="PyPI 镜像源 (default: aliyun)")
    # 兼容 --mirror 直接传值
    args, unknown = parser.parse_known_args()

    print("=" * 55)
    print("  semantic-split 环境检测 v0.1.0")
    print("=" * 55)

    # --- Python 版本 ---
    print("\n[1/3] Python 版本检测")
    if not _check_python():
        sys.exit(1)

    # --- 依赖包检测 ---
    print("\n[2/3] 依赖包检测")
    all_packages = list(REQUIRED_PACKAGES)
    all_packages += [k for k in OPTIONAL_PACKAGES if not _check_package(k)]

    status = _check_packages(REQUIRED_PACKAGES)
    missing = [pkg for pkg, installed in status.items() if not installed]

    # 可选包检测
    for name, pkg_name in OPTIONAL_PACKAGES.items():
        if not _check_package(pkg_name):
            _log(f"  {name:<30} [OPTIONAL - 未安装]")

    if not missing:
        print("\n[3/3] 全部依赖已就绪")
        print("=" * 55)
        return

    if args.check_only:
        print(f"\n[!] 缺失 {len(missing)} 个包 (--check-only 模式)")
        print(f"  运行: python scripts/setup_env.py --auto-install")
        sys.exit(1)

    # --- 安装缺失包 ---
    print(f"\n[3/3] 安装 {len(missing)} 个缺失包")
    ok = _install_missing(missing, args.mirror)
    if not ok:
        print("\n[!] 部分包安装失败，尝试 --no-deps 模式...")
        ok = _install_missing(missing, args.mirror, no_deps=True)

    # 安装 PyTorch（如果缺失）
    if not _check_package("torch"):
        print("\n安装 PyTorch CPU 版本...")
        _install_pytorch(args.mirror)

    print("\n" + "=" * 55)
    if ok:
        print("  环境就绪，可以运行 model_manager.py 下载模型")
        print("  python scripts/model_manager.py --download-all")
    else:
        print("  [!] 部分安装失败，请检查错误信息重试")
        print("  建议: python scripts/setup_env.py --mirror tsinghua")
    print("=" * 55)


if __name__ == "__main__":
    main()
