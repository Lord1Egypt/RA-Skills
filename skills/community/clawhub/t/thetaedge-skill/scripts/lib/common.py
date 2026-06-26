"""Shared utilities for thetaedge-skill scripts."""

import json
import os
import platform
import shutil
import stat
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_API_BASE = "https://api.thetaedge.ai"
DEFAULT_CLONE_URL = "https://github.com/thetaedge/thetaedge-skill.git"

TARGETS = ("claude-code", "openclaw", "generic")


def home() -> Path:
    return Path.home()


def is_windows() -> bool:
    return platform.system() == "Windows"


def detect_os() -> str:
    s = platform.system()
    if s == "Windows":
        return "windows"
    if s == "Darwin":
        return "macos"
    return "linux"


# ---------------------------------------------------------------------------
# Target / platform detection
# ---------------------------------------------------------------------------

def detect_targets() -> list:
    """Return list of agent platforms that appear to be installed."""
    found = []
    if (home() / ".claude").is_dir() or shutil.which("claude"):
        found.append("claude-code")
    if (home() / ".openclaw").is_dir() or shutil.which("openclaw"):
        found.append("openclaw")
    return found if found else ["generic"]


def skill_dir_for_target(target: str) -> Path:
    if target == "claude-code":
        return home() / ".claude" / "skills" / "thetaedge-skill"
    if target == "openclaw":
        return home() / ".openclaw" / "skills" / "thetix"
    return Path("")  # generic has no skill dir


def config_path_for_target(target: str) -> Path:
    if target == "claude-code":
        return home() / ".claude" / "settings.json"
    if target == "openclaw":
        return home() / ".openclaw" / "openclaw.json"
    # generic
    if is_windows():
        base = Path(os.environ.get("APPDATA", home() / "AppData" / "Roaming"))
    else:
        base = home() / ".config"
    return base / "thetaedge" / "credentials.json"


# ---------------------------------------------------------------------------
# JSON helpers
# ---------------------------------------------------------------------------

def read_json(path: Path) -> dict:
    """Read a JSON file, returning {} if missing or invalid."""
    if not path.is_file():
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def write_json(path: Path, data: dict) -> None:
    """Write dict as JSON, creating parent dirs. Sets 600 on Unix."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    if not is_windows():
        os.chmod(path, stat.S_IRUSR | stat.S_IWUSR)


def deep_merge(base: dict, overlay: dict) -> dict:
    """Recursively merge overlay into base (returns new dict)."""
    result = dict(base)
    for k, v in overlay.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


# ---------------------------------------------------------------------------
# Credential helpers
# ---------------------------------------------------------------------------

def set_credentials(target: str, api_key: str, api_base: str) -> Path:
    """Merge credentials into the config file for the given target. Returns config path."""
    path = config_path_for_target(target)
    existing = read_json(path)

    if target == "claude-code":
        overlay = {"env": {"THETAEDGE_API_KEY": api_key}}
        if api_base != DEFAULT_API_BASE:
            overlay["env"]["THETAEDGE_API_BASE"] = api_base
        merged = deep_merge(existing, overlay)

    elif target == "openclaw":
        overlay = {
            "skills": {
                "entries": {
                    "thetix": {
                        "enabled": True,
                        "env": {
                            "THETAEDGE_API_KEY": api_key,
                            "THETAEDGE_API_BASE": api_base,
                        },
                    }
                }
            }
        }
        merged = deep_merge(existing, overlay)

    else:  # generic
        overlay = {"api_key": api_key, "api_base": api_base}
        merged = deep_merge(existing, overlay)

    write_json(path, merged)
    return path


def get_credentials(target: str) -> tuple:
    """Read (api_key, api_base) from the config file for the given target."""
    data = read_json(config_path_for_target(target))

    if target == "claude-code":
        env = data.get("env", {})
        return env.get("THETAEDGE_API_KEY", ""), env.get("THETAEDGE_API_BASE", DEFAULT_API_BASE)

    if target == "openclaw":
        env = (data.get("skills", {}).get("entries", {}).get("thetix", {}).get("env", {}))
        return env.get("THETAEDGE_API_KEY", ""), env.get("THETAEDGE_API_BASE", DEFAULT_API_BASE)

    # generic
    return data.get("api_key", ""), data.get("api_base", DEFAULT_API_BASE)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_api_key(key: str) -> tuple:
    """Returns (ok: bool, message: str)."""
    if not key:
        return False, "API key is empty"
    if not key.startswith("te_"):
        return False, "API key should start with 'te_'"
    if len(key) < 10:
        return False, "API key is too short"
    return True, "API key format valid"


def test_api_connection(api_base: str, api_key: str, timeout: int = 5) -> tuple:
    """Make a test GET /api/accounts call. Returns (ok, message)."""
    url = f"{api_base.rstrip('/')}/api/accounts"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return True, "API key accepted"
            return False, f"Unexpected status {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return False, "API key is invalid or expired"
        return False, f"HTTP {e.code}: {e.reason}"
    except (urllib.error.URLError, OSError) as e:
        return False, f"Could not reach API: {e}"


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def run_git(*args, cwd=None) -> subprocess.CompletedProcess:
    """Run a git command, returning CompletedProcess."""
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )


def git_available() -> bool:
    return shutil.which("git") is not None


# ---------------------------------------------------------------------------
# Terminal output
# ---------------------------------------------------------------------------

_use_color = None


def _supports_color() -> bool:
    global _use_color
    if _use_color is not None:
        return _use_color
    if os.environ.get("NO_COLOR"):
        _use_color = False
    elif is_windows():
        _use_color = os.environ.get("WT_SESSION") or os.environ.get("TERM_PROGRAM")
        _use_color = bool(_use_color)
    else:
        _use_color = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
    return _use_color


def _color(code: str, text: str) -> str:
    if _supports_color():
        return f"\033[{code}m{text}\033[0m"
    return text


def info(msg: str) -> None:
    arrow = _color("1;34", "==>")
    print(f"\n{arrow} {_color('1', msg)}")


def warn(msg: str) -> None:
    label = _color("1;33", "WARN:")
    print(f"{label} {msg}")


def error(msg: str) -> None:
    label = _color("1;31", "ERROR:")
    print(f"{label} {msg}", file=sys.stderr)


def print_status(status: str, msg: str, detail: str = "") -> None:
    """Print a [PASS]/[WARN]/[FAIL] line."""
    colors = {"pass": "1;32", "warn": "1;33", "fail": "1;31"}
    tag = _color(colors.get(status, "0"), f"[{status.upper()}]")
    print(f"  {tag} {msg}")
    if detail:
        print(f"         {detail}")


def fatal(msg: str) -> None:
    error(msg)
    sys.exit(1)
