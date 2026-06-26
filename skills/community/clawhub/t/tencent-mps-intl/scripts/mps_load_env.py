#!/usr/bin/env python3
"""
mps_load_env.py — Tencent Cloud MPS Skill Environment Variable Auto-Loader

Implementation:
  Uses python-dotenv load_dotenv to load dotenv-style config files.
  Loads in the following order (existing env vars are not overwritten, first-loaded wins):
    1. Default: find_dotenv(usecwd=True) searches upward from cwd for nearest .env
    2. ~/.env                (user-level dotenv)
    3. ~/.bashrc             (shell startup file, compatible with export VAR=... syntax)
    4. ~/.profile            (login shell startup file)
    5. <SKILL_DIR>/.env      (dotenv in the skill directory containing this script)

  Target variables (all required):
    TENCENTCLOUD_SECRET_ID       (required)
    TENCENTCLOUD_SECRET_KEY      (required)
    TENCENTCLOUD_COS_BUCKET      (required, input/output COS bucket)
    TENCENTCLOUD_COS_REGION      (required, COS bucket region)
    TENCENTCLOUD_API_REGION      (required, MPS API region)

  Optional variables:
    TENCENTCLOUD_MPS_ENDPOINT    (optional, MPS API endpoint; default mps.tencentcloudapi.com,
                                  set to mps.intl.tencentcloudapi.com for international site)

Usage (called from other scripts):
    from mps_load_env import ensure_env_loaded
    ensure_env_loaded()

Diagnostic mode (standalone):
    python mps_load_env.py                   # Load and print results
    python mps_load_env.py --check-only      # Check current env var status only
    python mps_load_env.py --dry-run         # Dry run (no actual loading)
    python mps_load_env.py --verbose         # Show verbose loading logs
"""

import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# Required variables (error if missing)
_REQUIRED_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_COS_BUCKET",
    "TENCENTCLOUD_COS_REGION",
    "TENCENTCLOUD_API_REGION",
]

# Optional variables (use default if unset, no error)
_OPTIONAL_VARS = [
    "TENCENTCLOUD_MPS_ENDPOINT",
]

# Candidate dotenv file list (load order, first wins; load_dotenv default override=False)
# Additionally, load_env_files() first calls load_dotenv() without args,
# using find_dotenv(usecwd=True) to search upward from cwd for the nearest .env file.
_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.expanduser("~/.bashrc"),
    os.path.expanduser("~/.profile"),
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
]

def load_env_files(verbose: bool = False) -> dict:
    """
    Uses load_dotenv to load env vars from candidate files into os.environ.
    Existing env vars are not overwritten (override=False).

    Returns: dict of newly loaded variables {key: value}
    """
    if not _DOTENV_AVAILABLE:
        if verbose:
            print(
                "[load_env] python-dotenv not installed, cannot load .env files."
                "Run: pip install -r scripts/requirements.txt",
                file=sys.stderr,
            )
        return {}

    newly_loaded = {}
    seen_paths = set()

    def _load_and_collect(path_label, dotenv_path=None):
        """Load a dotenv file and collect newly added variables."""
        before = dict(os.environ)
        try:
            ok = load_dotenv(dotenv_path=dotenv_path, override=False) if dotenv_path else load_dotenv(override=False)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] Read failed: {path_label} ({e})", file=sys.stderr)
            return
        if verbose:
            print(f"[load_env] Loading file: {path_label} ({'success' if ok else 'no change'})", file=sys.stderr)
        for key, value in os.environ.items():
            if key not in before:
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[load_env]   Set {key}={display}", file=sys.stderr)

    # Try find_dotenv default: search upward from cwd for .env file
    try:
        from dotenv import find_dotenv
        default_path = find_dotenv(usecwd=True)
    except (ImportError, Exception):
        default_path = ""

    if default_path and os.path.isfile(default_path):
        _load_and_collect(f"Default .env: {default_path}")
        seen_paths.add(os.path.abspath(default_path))
    elif verbose:
        print("[load_env] No default .env found in cwd or parent directories", file=sys.stderr)

    for filepath in _ENV_FILES:
        if not filepath:
            continue
        abs_path = os.path.abspath(filepath)
        if abs_path in seen_paths:
            if verbose:
                print(f"[load_env] Skipped (already loaded): {filepath}", file=sys.stderr)
            continue
        seen_paths.add(abs_path)

        if not os.path.isfile(filepath):
            if verbose:
                print(f"[load_env] Skipped (not found): {filepath}", file=sys.stderr)
            continue

        _load_and_collect(filepath, dotenv_path=filepath)

    return newly_loaded


def check_required_vars(required: list = None) -> list:
    """
    Check if required environment variables are set.
    Returns list of missing var names (empty = all set).
    """
    if required is None:
        required = _REQUIRED_VARS
    return [k for k in required if not os.environ.get(k)]


def _print_setup_hint(missing_vars: list) -> None:
    """Print detailed setup hint when env vars fail to load."""
    env_files_str = "\n".join(f"    • {f}" for f in _ENV_FILES)
    missing_str = "\n".join(f"    {k}=<your_value>" for k in missing_vars)
    hint = f"""
╔══════════════════════════════════════════════════════════════════╗
║       Tencent Cloud MPS Env Vars Not Configured                ║
╚══════════════════════════════════════════════════════════════════╝

The following environment variables are missing:
{missing_str}

Enable MPS service:https://console.cloud.tencent.com/mps
Get credentials:     https://console.cloud.tencent.com/cam/capi
COS bucket management:   https://console.cloud.tencent.com/mps/workflows/buckets

[Method 1] Write to dotenv file (recommended, auto-loaded, no source needed):
  The script loads variables from the following files in order:
{env_files_str}
  Additionally, find_dotenv(usecwd=True) searches upward from cwd for the nearest .env.

  Example (~/.env):
    TENCENTCLOUD_SECRET_ID=<Your SecretId>
    TENCENTCLOUD_SECRET_KEY=<Your SecretKey>
    TENCENTCLOUD_COS_BUCKET=<Your Bucket name>
    TENCENTCLOUD_COS_REGION=<Bucket region, e.g. ap-guangzhou>
    TENCENTCLOUD_API_REGION=<MPS API region, e.g. ap-guangzhou>

[Method 2] Traditional shell env vars (requires restart or source):
    export TENCENTCLOUD_SECRET_ID=<Your SecretId>
    export TENCENTCLOUD_SECRET_KEY=<Your SecretKey>

⚠️  Security: configure credentials securely. Do not commit to repositories.
   To install python-dotenv:pip install -r scripts/requirements.txt

After configuration, restart the conversation.
"""
    print(hint, file=sys.stderr)


def ensure_env_loaded(
    required: list = None,
    verbose: bool = False,
) -> bool:
    """
    Ensure required environment variables are loaded.

    Flow:
      1. Check if required vars exist in os.environ
      2. If missing, call load_dotenv to load candidate files
      3. Re-check, return whether all ready
    Parameters:
      required  — Required var list, default _REQUIRED_VARS (5 items)
      verbose   — Whether to print loading logs to stderr

    Returns: True if all required vars are ready, False if some are still missing
    """
    if required is None:
        required = _REQUIRED_VARS

    missing_before = check_required_vars(required)
    if not missing_before:
        return True

    if verbose:
        print(
            f"[load_env] Missing variables detected: {missing_before}, Loading dotenv files...",
            file=sys.stderr,
        )

    load_env_files(verbose=verbose)

    missing_after = check_required_vars(required)
    if missing_after:
        return False

    if verbose:
        print("[load_env] All required variables loaded successfully.", file=sys.stderr)
    return True


def _format_var_status(var: str, val: str) -> str:
    """Format display status of a single variable."""
    if val:
        display = val[:4] + "****" if len(val) > 4 else "****"
        return f"✅ Set ({display})"
    return "❌ Not set"


def _format_optional_var_status(var: str, val: str) -> str:
    """Format display status of an optional variable (non-sensitive, shown in plain text)."""
    if val:
        return f"✅ Set ({val})"
    if var == "TENCENTCLOUD_MPS_ENDPOINT":
        return "⚪ Not set (default domestic site mps.tencentcloudapi.com)"
    return "⚪ Not set (using default)"


# ─── Standalone: Diagnostic Mode ───────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Load dotenv files and check Tencent Cloud MPS env vars (diagnostic mode)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show verbose loading logs"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Check current env var status only, do not load"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Dry run: show planned actions without loading"
    )
    args = parser.parse_args()

    if args.check_only:
        print("=== Tencent Cloud MPS Environment Variable Status ===\n")
        print("[Required Variables]")
        all_ok = True
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            status = _format_var_status(var, val)
            if not val:
                all_ok = False
            print(f"  {var}: {status}")

        print()
        print("[Optional Variables]")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            print(f"  {var}: {_format_optional_var_status(var, val)}")

        print()
        if all_ok:
            print("✅ All required variables configured. MPS Skill ready.")
            sys.exit(0)
        else:
            print("❌ Required variables incomplete. Please configure and retry.")
            sys.exit(1)

    if args.dry_run:
        print("=== Dry Run ===\n")
        print("Action: load Tencent Cloud MPS env vars via load_dotenv")
        print(f"\npython-dotenv status: {'✅ Available' if _DOTENV_AVAILABLE else '❌ Not installed'}")
        print("\nDotenv files to load (in order):")
        print("  - 0) find_dotenv(usecwd=True) Auto-search upward from cwd for nearest .env")
        for filepath in _ENV_FILES:
            exists = "✅ Exists" if os.path.isfile(filepath) else "⚪ Not found"
            print(f"  - {filepath}  [{exists}]")

        print("\nEnvironment variables to find:")
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            print(f"  - {var}: {_format_var_status(var, val)}  [required]")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            print(f"  - {var}: {_format_optional_var_status(var, val)}  [optional]")

        print("\nNo env vars loaded. Remove --dry-run to execute.")
        sys.exit(0)

    print("=== Loading dotenv files ===", flush=True)
    if not _DOTENV_AVAILABLE:
        print(
            "❌ python-dotenv not installed. Run: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    newly = load_env_files(verbose=True)
    sys.stderr.flush()

    print("\n=== Load Results ===")
    print("[Required Variables]")
    all_ok = True
    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        status = _format_var_status(var, val)
        if not val:
            all_ok = False
        print(f"  {var}: {status}")

    print()
    print("[Optional Variables]")
    for var in _OPTIONAL_VARS:
        val = os.environ.get(var, "")
        print(f"  {var}: {_format_optional_var_status(var, val)}")

    if newly:
        target_hits = [k for k in newly if k in set(_REQUIRED_VARS)]
        print(f"\nNewly loaded {len(newly)} variables"
              f" (of which {len(target_hits)} target vars: {target_hits})")
    else:
        print("\nNo new variables loaded (all set or files not found)")

    if not all_ok:
        _print_setup_hint([v for v in _REQUIRED_VARS if not os.environ.get(v)])
        sys.exit(1)
    else:
        print("\n✅ All required variables configured. MPS Skill ready.")
