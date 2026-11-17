#!/usr/bin/env python3
"""VOD 脚本运行时依赖检查与自动升级。

所有 VOD 脚本在执行前导入此模块即可自动触发依赖检查：
    from vod_auto_upgrade import check_sdk_version

检查范围（与 requirements.txt 保持同步）：
  - tencentcloud-sdk-python : 检查最低版本
  - python-dotenv           : 仅检查是否安装
  - requests                : 检查最低版本

任何依赖缺失或版本过低时，自动执行 python3 -m pip install 升级。
"""

# 抑制 macOS 系统 Python (LibreSSL) + urllib3 v2 的 NotOpenSSLWarning。
# 该告警与 VOD 功能无关，仅是环境提示，用户无法便捷修复；
# 精准定向抑制，不影响其他 warning 输出。
#
# 注意：必须在 urllib3 首次被 import 之前注册 filter，
# 因为 urllib3 v2 顶层代码执行 warnings.warn(...) 是"一次性"的，
# 一旦触发就无法回退。所以这里：
#   1) 先用"消息串正则"直接注册 filter（不 import 任何 urllib3 相关模块）
#   2) 再尝试 import 类做二次保险（此时 urllib3 首次加载会被前面的 filter 拦下）
import warnings
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 v2 only supports OpenSSL.*",
)
try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except ImportError:
    # urllib3 尚未装 / 版本过老没有该类：仅靠消息 filter 兜底
    pass

import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version

# 依赖清单（与 requirements.txt 保持同步）
# 格式：(pip 包名, 最低版本元组 or None 表示不查版本)
_DEPENDENCIES = [
    ("tencentcloud-sdk-python", (3, 1, 107)),
    ("python-dotenv",           (1, 0, 0)),
    ("requests",                (2, 31, 0)),
]


def _ver_tuple(ver_str):
    """把版本字符串解析为 3 元组，缺位补 0；解析失败返回 (0, 0, 0)。"""
    try:
        parts = (ver_str or "0").split(".")[:3]
        return tuple(int(x) for x in parts) + (0,) * (3 - len(parts))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _pip_install(specs):
    """执行 python3 -m pip install 一次性安装/升级一组依赖。

    specs: list[str]，例如 ["tencentcloud-sdk-python>=3.1.107", "requests>=2.31.0"]
    """
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet"] + specs
    print(f"⏳ 正在自动安装/升级缺失依赖：{', '.join(specs)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"❌ 自动安装失败，请手动执行:\n"
            f"   python3 -m pip install --upgrade {' '.join(repr(s) for s in specs)}\n"
            f"   错误信息: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    print("✅ 安装完成", file=sys.stderr)


def check_sdk_version():
    """检查 requirements.txt 全部依赖；缺失或版本过低时自动安装/升级。

    保留旧函数名以兼容 16 个脚本的 import；语义已扩展为"全依赖检查"。
    使用 importlib.metadata 读取 pip 包的精确版本（不依赖各包提供 __version__）。
    """
    to_install = []   # list[str]：传给 pip 的 spec

    for pkg_name, min_ver in _DEPENDENCIES:
        min_ver_str = ".".join(map(str, min_ver)) if min_ver else None
        spec = f"{pkg_name}>={min_ver_str}" if min_ver_str else pkg_name

        try:
            installed_ver = _pkg_version(pkg_name)
        except PackageNotFoundError:
            print(f"⚠️  {pkg_name} 未安装", file=sys.stderr)
            to_install.append(spec)
            continue

        if min_ver and _ver_tuple(installed_ver) < min_ver:
            print(
                f"⚠️  {pkg_name} 版本过低: {installed_ver}，需要 >= {min_ver_str}",
                file=sys.stderr,
            )
            to_install.append(spec)

    if to_install:
        _pip_install(to_install)
        # 升级后清除可能已加载的过旧模块缓存（让后续 import 加载新版本）
        for prefix in ("tencentcloud", "dotenv", "requests"):
            for key in list(sys.modules.keys()):
                if key == prefix or key.startswith(prefix + "."):
                    del sys.modules[key]
