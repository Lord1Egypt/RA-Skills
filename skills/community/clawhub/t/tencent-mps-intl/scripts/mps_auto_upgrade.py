#!/usr/bin/env python3
"""MPS scripts runtime dependency check and auto-upgrade.

All MPS scripts import this module before execution to trigger a dependency check:
    from mps_auto_upgrade import check_sdk_version

The **single source of truth** for the dependency list is `requirements.txt` in the
same directory:
  - Both package names and minimum version constraints (e.g., `pkg>=X.Y.Z`) are
    parsed from requirements.txt at runtime
  - When bumping a dependency version, **only requirements.txt needs to change**
  - This module parses that file at import time and exposes `_DEPENDENCIES` for
    check_sdk_version() to use

If any dependency is missing or below the minimum version, python3 -m pip install
is automatically invoked to upgrade.
"""

# Suppress the NotOpenSSLWarning from macOS system Python (LibreSSL) + urllib3 v2.
# This warning is unrelated to MPS functionality; it is only an environment hint,
# and users cannot easily fix it. Suppress it precisely without affecting other warnings.
#
# Note: The filter MUST be registered before urllib3 is first imported, because
# urllib3 v2 emits warnings.warn(...) at top-level as a "one-shot" call — once
# triggered, it cannot be undone. Therefore:
#   1) First register the filter by message-string regex (do not import any urllib3 module)
#   2) Then try to import the exception class as a secondary safeguard
#      (urllib3's first load will be intercepted by the filter above)
import warnings
warnings.filterwarnings(
    "ignore",
    message=r".*urllib3 v2 only supports OpenSSL.*",
)
try:
    from urllib3.exceptions import NotOpenSSLWarning
    warnings.filterwarnings("ignore", category=NotOpenSSLWarning)
except ImportError:
    # urllib3 not installed / version too old to have this class: rely on message filter
    pass

import re
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version as _pkg_version
from pathlib import Path


def _load_dependencies_from_requirements():
    """Parse the dependency list from the requirements.txt in the same directory.

    Supported line formats:
        pkg>=X.Y.Z   → ('pkg', (X, Y, Z))
        pkg==X.Y.Z   → ('pkg', (X, Y, Z))  also treated as minimum version
        pkg          → ('pkg', None)       presence check only

    Empty lines, comment lines (starting with #), and unrecognized complex
    constraints are skipped.
    Returns [(pkg_name, min_ver_tuple_or_None), ...] preserving file order.
    """
    req_path = Path(__file__).parent / "requirements.txt"
    if not req_path.exists():
        # Fallback: at least check the core SDK when the file is missing
        return [("tencentcloud-sdk-python", None)]

    deps = []
    line_pat = re.compile(
        r"^\s*"
        r"([A-Za-z][A-Za-z0-9_.\-]*)"       # package name
        r"\s*(?:(?:>=|==)\s*"                # >= or ==
        r"(\d+)\.(\d+)\.(\d+))?\s*$"          # X.Y.Z (optional)
    )
    for raw in req_path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()   # strip inline comments
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


# Dependency list (single source of truth: requirements.txt; this module just parses it at runtime)
_DEPENDENCIES = _load_dependencies_from_requirements()

# Backward compatibility: legacy code may reference MIN_SDK_VERSION constant (= first entry's min ver)
MIN_SDK_VERSION = _DEPENDENCIES[0][1] if _DEPENDENCIES else None


def _ver_tuple(ver_str):
    """Parse a version string into a 3-tuple; missing parts default to 0; parse failures return (0, 0, 0)."""
    try:
        parts = (ver_str or "0").split(".")[:3]
        return tuple(int(x) for x in parts) + (0,) * (3 - len(parts))
    except (ValueError, AttributeError):
        return (0, 0, 0)


def _pip_install(specs):
    """Run python3 -m pip install to install/upgrade a batch of dependencies at once.

    specs: list[str], e.g., ["tencentcloud-sdk-python>=X.Y.Z", "cos-python-sdk-v5>=X.Y.Z"]
    """
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "--quiet"] + specs
    print(f"⏳ Auto-installing/upgrading missing dependencies: {', '.join(specs)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"❌ Auto-install failed. Please run manually:\n"
            f"   python3 -m pip install --upgrade {' '.join(repr(s) for s in specs)}\n"
            f"   Error: {result.stderr.strip()}",
            file=sys.stderr,
        )
        sys.exit(1)
    print("✅ Install completed", file=sys.stderr)


def check_sdk_version():
    """Check all dependencies from requirements.txt; auto-install/upgrade if missing or too old.

    The legacy function name is preserved for compatibility with existing script imports;
    semantics have been extended to "check all dependencies".
    Uses importlib.metadata to read exact pip package versions (does not rely on each
    package exposing __version__).
    """
    to_install = []   # list[str]: pip specs to install

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
                f"⚠️  {pkg_name} version too low: {installed_ver}, requires >= {min_ver_str}",
                file=sys.stderr,
            )
            to_install.append(spec)

    if to_install:
        _pip_install(to_install)
        # After upgrade, clear possibly loaded stale module caches (so subsequent imports load new versions)
        for prefix in ("tencentcloud", "qcloud_cos", "dotenv"):
            for key in list(sys.modules.keys()):
                if key == prefix or key.startswith(prefix + "."):
                    del sys.modules[key]
