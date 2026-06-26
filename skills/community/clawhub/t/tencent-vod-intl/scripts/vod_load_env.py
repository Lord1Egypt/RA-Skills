#!/usr/bin/env python3
"""
vod_load_env.py — Tencent Cloud VOD Skill Environment Variable Auto-Loader

Implementation:
  Uses the python-dotenv library's load_dotenv function to load dotenv-style
  configuration files. Loaded in the following order (existing environment
  variables will not be overwritten; the first to load wins):
    1. Default behavior: find_dotenv(usecwd=True) recursively searches upward
       from the current directory for the nearest .env file and loads it.
    2. ~/.env                (user-level dotenv, highest priority)
    3. ./.env                (current working directory dotenv)

  Target variables:
    TENCENTCLOUD_SECRET_ID       (required)
    TENCENTCLOUD_SECRET_KEY      (required)
    TENCENTCLOUD_VOD_AIGC_TOKEN  (optional, dedicated to AIGC LLM Chat)
    TENCENTCLOUD_VOD_SUB_APP_ID  (optional, sub-application ID)

Usage (calling from other scripts):
    from vod_load_env import ensure_env_loaded
    ensure_env_loaded()
"""

import os
import sys

try:
    from dotenv import load_dotenv
    _DOTENV_AVAILABLE = True
except ImportError:
    _DOTENV_AVAILABLE = False

# Target variables to detect
_TARGET_VARS = {
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
    "TENCENTCLOUD_VOD_AIGC_TOKEN",
    "TENCENTCLOUD_VOD_SUB_APP_ID",
}

# Required variables (error if missing)
_REQUIRED_VARS = [
    "TENCENTCLOUD_SECRET_ID",
    "TENCENTCLOUD_SECRET_KEY",
]

# Optional variables (only needed in specific scenarios)
_OPTIONAL_VARS = {
    "TENCENTCLOUD_VOD_AIGC_TOKEN": "Dedicated to AIGC LLM Chat (vod_aigc_chat.py)",
    "TENCENTCLOUD_VOD_SUB_APP_ID": "Used for sub-application operations (can be overridden via --sub-app-id parameter)",
}

# Candidate dotenv files (loaded in order; load_dotenv defaults to override=False)
# In addition, load_env_files() first calls load_dotenv() with no arguments,
# which uses find_dotenv(usecwd=True) to recursively search upward from the
# current working directory for the nearest .env file and load it.
_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.join(os.getcwd(), ".env"),
]


def load_env_files(verbose: bool = False) -> dict:
    """
    Load environment variables from candidate files into os.environ via load_dotenv.
    Existing environment variables will not be overwritten (override=False).

    Returns: dict of newly loaded variables {key: value} (includes target
    variables and any other variables in the files).
    """
    if not _DOTENV_AVAILABLE:
        if verbose:
            print(
                "[load_env] python-dotenv is not installed; cannot load .env files. "
                "Please run: pip install -r scripts/requirements.txt",
                file=sys.stderr,
            )
        return {}

    newly_loaded = {}
    seen_paths = set()

    # First try the default behavior of load_dotenv: search upward from the
    # current working directory for a .env file. This covers common scenarios
    # like "user puts .env in the project root, but the script runs from a
    # subdirectory".
    before_default = dict(os.environ)
    try:
        from dotenv import find_dotenv
        default_path = find_dotenv(usecwd=True)
    except (ImportError, Exception):
        default_path = ""

    if default_path and os.path.isfile(default_path):
        try:
            ok = load_dotenv(override=False)
            seen_paths.add(os.path.abspath(default_path))
            if verbose:
                print(
                    f"[load_env] Loaded default .env: {default_path} "
                    f"({'success' if ok else 'no change'})",
                    file=sys.stderr,
                )
            for key, value in os.environ.items():
                if key not in before_default:
                    newly_loaded[key] = value
                    if verbose:
                        display = value[:4] + "****" if len(value) > 4 else "****"
                        print(f"[load_env]   Set {key}={display}", file=sys.stderr)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] Failed to read default .env: {e}", file=sys.stderr)
    else:
        if verbose:
            print(
                "[load_env] No default .env found in current or parent directories",
                file=sys.stderr,
            )

    for filepath in _ENV_FILES:
        if not filepath:
            continue
        abs_path = os.path.abspath(filepath)
        if abs_path in seen_paths:
            if verbose:
                print(
                    f"[load_env] Skipping (already loaded by default search): {filepath}",
                    file=sys.stderr,
                )
            continue
        seen_paths.add(abs_path)

        if not os.path.isfile(filepath):
            if verbose:
                print(f"[load_env] Skipping (not found): {filepath}", file=sys.stderr)
            continue

        # Snapshot before loading, used to infer which KEYs were newly loaded
        before = dict(os.environ)

        try:
            ok = load_dotenv(dotenv_path=filepath, override=False)
        except (OSError, IOError) as e:
            if verbose:
                print(f"[load_env] Failed to read: {filepath} ({e})", file=sys.stderr)
            continue

        if verbose:
            print(
                f"[load_env] Loaded file: {filepath} ({'success' if ok else 'no change'})",
                file=sys.stderr,
            )

        # Collect variables newly loaded in this round
        for key, value in os.environ.items():
            if key not in before:
                newly_loaded[key] = value
                if verbose:
                    display = value[:4] + "****" if len(value) > 4 else "****"
                    print(f"[load_env]   Set {key}={display}", file=sys.stderr)

    return newly_loaded


def check_required_vars(required: list = None) -> list:
    """
    Check whether the required environment variables are set.
    Returns a list of missing variable names (empty list means all are set).
    """
    if required is None:
        required = _REQUIRED_VARS
    return [k for k in required if not os.environ.get(k)]


def _print_setup_hint(missing_vars: list) -> None:
    """Print detailed configuration guidance to the user when environment variable loading fails."""
    env_files_str = "\n".join(f"    • {f}" for f in _ENV_FILES)
    missing_str = "\n".join(f"    {k}=<your_value>" for k in missing_vars)
    hint = f"""
╔══════════════════════════════════════════════════════════════════╗
║       Tencent Cloud VOD Environment Variables Not Configured     ║
╚══════════════════════════════════════════════════════════════════╝

The following environment variables are missing:
{missing_str}

Credentials can be obtained from the Tencent Cloud Console: https://console.cloud.tencent.com/cam/capi
VOD Console: https://console.cloud.tencent.com/vod

[Configuration] Write to a dotenv file (recommended, auto-loaded, no source needed):
  At startup, the script loads variables from the following files (in order)
  into the current process:
{env_files_str}

  Example (using ~/.env):
    TENCENTCLOUD_SECRET_ID=<your SecretId>
    TENCENTCLOUD_SECRET_KEY=<your SecretKey>
    # Optional
    TENCENTCLOUD_VOD_AIGC_TOKEN=<your AIGC Token>
    TENCENTCLOUD_VOD_SUB_APP_ID=<your sub-application ID>

⚠️  Security Notice: Configure credentials through a secure channel; avoid committing them to a code repository.

After configuration, please restart the conversation.
"""
    print(hint, file=sys.stderr)


def ensure_env_loaded(
    required: list = None,
    verbose: bool = False,
) -> bool:
    """
    Ensure that the required environment variables are loaded.

    Execution flow:
      1. Check whether required variables are already in os.environ
      2. If any are missing, call load_dotenv to load candidate files
      3. Check again and return whether all are ready

    Parameters:
      required  — list of variables that must be present; defaults to checking SECRET_ID / SECRET_KEY
      verbose   — whether to print loading logs to stderr

    Returns: True if all required variables are ready, False if any are still missing
    """
    if required is None:
        required = _REQUIRED_VARS

    missing_before = check_required_vars(required)
    if not missing_before:
        return True

    if verbose:
        print(
            f"[load_env] Missing variables detected: {missing_before}, starting to load dotenv files...",
            file=sys.stderr,
        )

    load_env_files(verbose=verbose)

    missing_after = check_required_vars(required)
    if missing_after:
        return False

    if verbose:
        print("[load_env] All required variables have been loaded.", file=sys.stderr)
    return True


def _format_var_status(var: str, val: str) -> str:
    """Format the display status of a single variable."""
    if val:
        display = val[:4] + "****" if len(val) > 4 else "****"
        return f"✅ Set ({display})"
    return "❌ Not set"


# ─── When run standalone: diagnostic mode ──────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Load dotenv files and check Tencent Cloud VOD required environment variables (diagnostic mode)"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed loading logs"
    )
    parser.add_argument(
        "--check-only", action="store_true", help="Only check current environment variable status, do not load"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulate execution, show operations that would be performed without actually loading"
    )
    args = parser.parse_args()

    if args.check_only:
        print("=== Tencent Cloud VOD Environment Variable Status ===\n")
        print("[Required Variables]")
        all_required_ok = True  # NOCA:invalid-name(naming follows SDK convention)
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            status = _format_var_status(var, val)
            if not val:
                all_required_ok = False  # NOCA:invalid-name(naming follows SDK convention)
            print(f"  {var}: {status}")

        print("\n[Optional Variables]")
        for var, desc in _OPTIONAL_VARS.items():
            val = os.environ.get(var, "")
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                status = f"✅ Set ({display})"
            else:
                status = f"⚪ Not set ({desc})"
            print(f"  {var}: {status}")

        print()
        if all_required_ok:
            print("✅ All required variables are configured. VOD Skill is ready to use.")
            sys.exit(0)
        else:
            print("❌ Required variables are not fully configured. Please configure them as instructed and retry.")
            sys.exit(1)

    if args.dry_run:
        print("=== Dry-run ===\n")
        print("Operation: Use load_dotenv to load Tencent Cloud VOD environment variables")
        print(f"\npython-dotenv status: {'✅ Available' if _DOTENV_AVAILABLE else '❌ Not installed'}")
        print("\nDotenv files to be loaded (in order):")
        for filepath in _ENV_FILES:
            exists = "✅ exists" if os.path.isfile(filepath) else "⚪ does not exist"
            print(f"  - {filepath}  [{exists}]")

        print("\nEnvironment variables to be looked up:")
        for var in _REQUIRED_VARS:
            val = os.environ.get(var, "")
            tag = "[required]"
            print(f"  - {var}: {_format_var_status(var, val)}  {tag}")
        for var in _OPTIONAL_VARS:
            val = os.environ.get(var, "")
            tag = "[optional]"
            if val:
                display = val[:4] + "****" if len(val) > 4 else "****"
                print(f"  - {var}: ✅ Set ({display})  {tag}")
            else:
                print(f"  - {var}: ⚪ Not set  {tag}")

        print("\nNo environment variables will actually be loaded. Remove the --dry-run flag to perform the actual operation.")
        sys.exit(0)

    print("=== Loading dotenv files ===", flush=True)
    if not _DOTENV_AVAILABLE:
        print(
            "❌ python-dotenv is not installed. Please run: pip install -r scripts/requirements.txt",
            file=sys.stderr,
        )
        sys.exit(1)

    newly = load_env_files(verbose=True)
    sys.stderr.flush()

    print("\n=== Load Results ===")
    print("[Required Variables]")
    all_required_ok = True  # NOCA:invalid-name(naming follows SDK convention)
    for var in _REQUIRED_VARS:
        val = os.environ.get(var, "")
        status = _format_var_status(var, val)
        if not val:
            all_required_ok = False  # NOCA:invalid-name(naming follows SDK convention)
        print(f"  {var}: {status}")

    print("[Optional Variables]")
    for var, desc in _OPTIONAL_VARS.items():
        val = os.environ.get(var, "")
        if val:
            display = val[:4] + "****" if len(val) > 4 else "****"
            status = f"✅ Set ({display})"
        else:
            status = f"⚪ Not set ({desc})"
        print(f"  {var}: {status}")

    if newly:
        target_hits = [k for k in newly if k in _TARGET_VARS]
        print(f"\n{len(newly)} new variable(s) loaded this time"
              f" (including {len(target_hits)} target variable(s): {target_hits})")
    else:
        print("\nNo new variables loaded (all already set or files do not exist)")

    if not all_required_ok:
        _print_setup_hint([v for v in _REQUIRED_VARS if not os.environ.get(v)])
        sys.exit(1)
    else:
        print("\n✅ All required variables are configured. VOD Skill is ready to use.")
