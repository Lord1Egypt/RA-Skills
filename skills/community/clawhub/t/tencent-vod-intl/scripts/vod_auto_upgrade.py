#!/usr/bin/env python3
"""VOD SDK runtime version check and auto-upgrade.

All VOD scripts import this module before execution to trigger version check:
    from vod_auto_upgrade import check_sdk_version

If tencentcloud-sdk-python version is below requirement or not installed,
pip upgrade will be executed automatically.
"""

import subprocess
import sys

# Minimum version requirement (keep in sync with requirements.txt)
MIN_SDK_VERSION = (3, 1, 107)


def _pip_install(min_ver_str):
    """Execute pip install to upgrade SDK."""
    cmd = [
        sys.executable, "-m", "pip", "install",
        f"tencentcloud-sdk-python>={min_ver_str}",
        "--upgrade", "--quiet",
    ]
    print(f"⏳ Auto-upgrading tencentcloud-sdk-python >= {min_ver_str} ...", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"❌ Auto-upgrade failed, please run manually:\n"
            f"   pip install 'tencentcloud-sdk-python>={min_ver_str}' --upgrade\n"
            f"   Error: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"✅ Upgrade complete", file=sys.stderr)


def check_sdk_version():
    """Check tencentcloud-sdk-python version, auto-upgrade if insufficient."""
    min_ver_str = ".".join(map(str, MIN_SDK_VERSION))
    need_upgrade = False

    try:
        import tencentcloud
        ver_str = getattr(tencentcloud, "__version__", "0.0.0")
        ver_tuple = tuple(int(x) for x in ver_str.split(".")[:3])
        if ver_tuple < MIN_SDK_VERSION:
            print(
                f"⚠️  tencentcloud-sdk-python version too low: {ver_str}, need >= {min_ver_str}",
                file=sys.stderr,
            )
            need_upgrade = True
    except ImportError:
        print(f"⚠️  tencentcloud-sdk-python not installed, need >= {min_ver_str}", file=sys.stderr)
        need_upgrade = True

    if need_upgrade:
        _pip_install(min_ver_str)
        # Clear module cache after upgrade so subsequent imports load new version
        for key in list(sys.modules.keys()):
            if key == "tencentcloud" or key.startswith("tencentcloud."):
                del sys.modules[key]
