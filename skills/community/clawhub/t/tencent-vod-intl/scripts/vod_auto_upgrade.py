#!/usr/bin/env python3
"""VOD scripts runtime dependency check and auto-upgrade.

All VOD scripts import this module before execution to trigger checks:
    from vod_auto_upgrade import check_sdk_version

Scope (kept in sync with requirements.txt):
  - tencentcloud-sdk-python : check minimum version
  - python-dotenv           : only check installation
  - requests                : check minimum version

If any dependency is missing or too old, python3 -m pip install is run automatically.
"""

# Suppress urllib3 v2 NotOpenSSLWarning on macOS system Python (LibreSSL).
# This warning is unrelated to VOD functionality — it's just an environment notice
# that users cannot easily fix. Suppressed narrowly to avoid muting other warnings.
#
# IMPORTANT: The filter must be registered BEFORE urllib3 is first imported,
# because urllib3 v2's top-level `warnings.warn(...)` fires only once at import
# time and cannot be replayed. Therefore:
#   1) First register the filter by message-regex (does NOT import urllib3).
#   2) Then attempt to import the exception class as a secondary safety net
#      (urllib3's first-time load will be intercepted by the message filter above).
import warnings
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 v2 only supports OpenSSL.*",
)
try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except ImportError:
    # urllib3 not installed yet, or too old to have the class: message filter suffices.
    pass

import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version

# Dependency list (keep in sync with requirements.txt)
# Format: (pip package name, min version tuple or None to skip version check)
_DEPENDENCIES = [
    ("tencentcloud-sdk-python", (3, 1, 107)),
    ("python-dotenv",           (1, 0, 0)),
    ("requests",                (2, 31, 0)),
]


def _ver_tuple(ver_str):
    """Parse version string into a 3-tuple, padded with 0; on failure returns (0, 0, 0)."""
    try:
        parts = (ver_str or "0").split(".")[:3]
        return tuple(int(x) for x in parts) + (0,) * (3 - len(parts))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _pip_install(specs):
    """Run python3 -m pip install to install/upgrade a batch of dependencies.

    specs: list[str], e.g. ["tencentcloud-sdk-python>=3.1.107", "requests>=2.31.0"]
    """
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet"] + specs
    print(f"⏳ Auto-installing/upgrading missing dependencies: {', '.join(specs)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"❌ Auto-install failed, please run manually:\n"
            f"   python3 -m pip install --upgrade {' '.join(repr(s) for s in specs)}\n"
            f"   Error: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    print("✅ Install complete", file=sys.stderr)


def check_sdk_version():
    """Check all dependencies in requirements.txt; auto-install/upgrade if missing or too old.

    Keeps the original function name for compatibility with the 16 scripts that import it;
    semantics has been extended to cover the full dependency list. Uses importlib.metadata
    to read each pip package's exact version (does not depend on the module exposing __version__).
    """
    to_install = []   # list[str]: pip specs

    for pkg_name, min_ver in _DEPENDENCIES:
        min_ver_str = ".".join(map(str, min_ver)) if min_ver else None
        spec = f"{pkg_name}>={min_ver_str}" if min_ver_str else pkg_name

        try:
            installed_ver = _pkg_version(pkg_name)
        except PackageNotFoundError:
            print(f"⚠️  {pkg_name} not installed", file=sys.stderr)
            to_install.append(spec)
            continue

        if min_ver and _ver_tuple(installed_ver) < min_ver:
            print(
                f"⚠️  {pkg_name} version too low: {installed_ver}, need >= {min_ver_str}",
                file=sys.stderr,
            )
            to_install.append(spec)

    if to_install:
        _pip_install(to_install)
        # Clear any already-loaded stale modules so subsequent imports load new version
        for prefix in ("tencentcloud", "dotenv", "requests"):
            for key in list(sys.modules.keys()):
                if key == prefix or key.startswith(prefix + "."):
                    del sys.modules[key]
