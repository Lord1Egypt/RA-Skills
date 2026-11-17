#!/usr/bin/env python3
"""MPS 脚本运行时依赖检查与自动升级。

用法（两步，缺一不可）：
    from mps_auto_upgrade import check_sdk_version
    check_sdk_version()          # ← 必须显式调用，import 本身不做依赖检查

  · 仅 import 只会注册 urllib3 NotOpenSSLWarning 过滤器（模块级副作用）；
  · 依赖检查与自动安装发生在 check_sdk_version() 内部，不调用则不生效；
  · 调用点应放在第三方包（tencentcloud / qcloud_cos / dotenv）首次 import 之前。

依赖清单的**唯一真源**是同目录下的 `requirements.txt`：
  - 包名 + 最低版本约束（如 `pkg>=X.Y.Z`）都从 requirements.txt 解析
  - 修改依赖版本时，**只需要改 requirements.txt 一处**
  - 本模块运行时读取，构造出 `_DEPENDENCIES` 供 check_sdk_version() 使用

任何依赖缺失或版本过低时，自动执行 python3 -m pip install 升级。
"""

# 抑制 macOS 系统 Python (LibreSSL) + urllib3 v2 的 NotOpenSSLWarning。
# 该告警与 MPS 功能无关，仅是环境提示，用户无法便捷修复；
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

import re
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from pathlib import Path


def _load_dependencies_from_requirements():
    """从同目录 requirements.txt 解析依赖清单。

    支持行格式：
        pkg>=X.Y.Z   → ('pkg', (X, Y, Z))
        pkg==X.Y.Z   → ('pkg', (X, Y, Z))  同样按最低版本处理
        pkg          → ('pkg', None)       仅检查是否安装

    自动跳过空行、注释行（以 # 开头）与不识别的复杂约束。
    返回 [(pkg_name, min_ver_tuple_or_None), ...]，保持文件中的顺序。
    """
    req_path = Path(__file__).parent / "requirements.txt"
    if not req_path.exists():
        # 兜底：文件缺失时至少检查最核心的 SDK
        return [("tencentcloud-sdk-python", None)]

    deps = []
    line_pat = re.compile(
        r"^\s*"
        r"([A-Za-z][A-Za-z0-9_.\-]*)"       # 包名
        r"\s*(?:(?:>=|==)\s*"                # >= 或 ==
        r"(\d+)\.(\d+)\.(\d+))?\s*$"          # X.Y.Z（可选）
    )
    for raw in req_path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()   # 去掉行内注释
        if not line:
            continue
        m = line_pat.match(line)
        if not m:
            continue
        pkg = m.group(1)
        if m.group(2) is None:
            deps.append((pkg, None))
        else:
            deps.append((pkg, (int(m.group(2)), int(m.group(3)), int(m.group(4)))))
    return deps


# 依赖清单（唯一真源：requirements.txt；本模块只是运行时解析）
_DEPENDENCIES = _load_dependencies_from_requirements()

# 兼容保留：老代码可能引用 MIN_SDK_VERSION 常量
# 按包名精确查找，不依赖 requirements.txt 中的行序
MIN_SDK_VERSION = next(
    (ver for pkg, ver in _DEPENDENCIES if pkg == "tencentcloud-sdk-python"),
    None,
)


def _ver_tuple(ver_str):
    """把版本字符串解析为 3 元组，缺位补 0；解析失败返回 (0, 0, 0)。"""
    try:
        parts = (ver_str or "0").split(".")[:3]
        return tuple(int(x) for x in parts) + (0,) * (3 - len(parts))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _pip_install(specs):
    """执行 python3 -m pip install 一次性安装/升级一组依赖。

    specs: list[str]，例如 ["tencentcloud-sdk-python>=X.Y.Z", "cos-python-sdk-v5>=X.Y.Z"]
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

    保留旧函数名以兼容各脚本的 import；语义已扩展为"全依赖检查"。
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
        for prefix in ("tencentcloud", "qcloud_cos", "dotenv"):
            for key in list(sys.modules.keys()):
                if key == prefix or key.startswith(prefix + "."):
                    del sys.modules[key]
