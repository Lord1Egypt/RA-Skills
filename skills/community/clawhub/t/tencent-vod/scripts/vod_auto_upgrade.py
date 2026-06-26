#!/usr/bin/env python3
"""VOD SDK 运行时版本检查与自动升级。

所有 VOD 脚本在执行前导入此模块即可自动触发版本检查：
    from vod_auto_upgrade import check_sdk_version

若 tencentcloud-sdk-python 版本低于要求或未安装，会自动执行 pip 升级。
"""

import subprocess
import sys

# 最低版本要求（与 requirements.txt 保持同步）
MIN_SDK_VERSION = (3, 1, 107)


def _pip_install(min_ver_str):
    """执行 pip install 升级 SDK。"""
    cmd = [
        sys.executable, "-m", "pip", "install",
        f"tencentcloud-sdk-python>={min_ver_str}",
        "--upgrade", "--quiet",
    ]
    print(f"⏳ 正在自动升级 tencentcloud-sdk-python >= {min_ver_str} ...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"❌ 自动升级失败，请手动执行:\n"
            f"   pip install 'tencentcloud-sdk-python>={min_ver_str}' --upgrade\n"
            f"   错误信息: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"✅ 升级完成", file=sys.stderr)


def check_sdk_version():
    """检查 tencentcloud-sdk-python 版本，不足时自动升级。"""
    min_ver_str = ".".join(map(str, MIN_SDK_VERSION))
    need_upgrade = False

    try:
        import tencentcloud
        ver_str = getattr(tencentcloud, "__version__", "0.0.0")
        ver_tuple = tuple(int(x) for x in ver_str.split(".")[:3])
        if ver_tuple < MIN_SDK_VERSION:
            print(
                f"⚠️  tencentcloud-sdk-python 版本过低: {ver_str}，需要 >= {min_ver_str}",
                file=sys.stderr,
            )
            need_upgrade = True
    except ImportError:
        print(f"⚠️  tencentcloud-sdk-python 未安装，需要 >= {min_ver_str}", file=sys.stderr)
        need_upgrade = True

    if need_upgrade:
        _pip_install(min_ver_str)
        # 升级后清除模块缓存，让后续 import 加载新版本
        for key in list(sys.modules.keys()):
            if key == "tencentcloud" or key.startswith("tencentcloud."):
                del sys.modules[key]
