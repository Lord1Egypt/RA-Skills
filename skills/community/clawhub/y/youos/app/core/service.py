"""Run the YouOS server reliably as a macOS launchd LaunchAgent.

`youos serve` is foreground-only — it dies when the terminal closes, on
reboot, or if it crashes. A LaunchAgent fixes all three: it runs at login,
restarts on crash (``KeepAlive``), and survives reboot, with no root needed.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

LABEL = "com.youos.server"
ROOT_DIR = Path(__file__).resolve().parents[2]


def plist_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"


def build_plist(
    *,
    python: str | None = None,
    root: Path | None = None,
    host: str | None = None,
    port: int | None = None,
    log_path: Path | None = None,
    data_dir: str | None = None,
) -> str:
    """Render the LaunchAgent plist for the YouOS server.

    Mirrors `youos serve` (venv python -m uvicorn app.main:app), at the
    configured host/port, working dir = repo root, output to a log file. Passes
    YOUOS_DATA_DIR through so the agent serves the same instance the installer
    was pointed at (instance-awareness).
    """
    python = python or sys.executable
    root = root or ROOT_DIR
    if host is None or port is None:
        from app.core.config import get_server_host, get_server_port

        host = host or get_server_host()
        port = port or get_server_port()
    log_path = log_path or (root / "var" / "server.log")
    if data_dir is None:
        data_dir = os.environ.get("YOUOS_DATA_DIR")

    env_entries = ""
    if data_dir:
        env_entries = f"  <key>EnvironmentVariables</key>\n  <dict>\n    <key>YOUOS_DATA_DIR</key><string>{escape(data_dir)}</string>\n  </dict>\n"

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>{LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>{escape(python)}</string>
    <string>-m</string>
    <string>uvicorn</string>
    <string>app.main:app</string>
    <string>--host</string><string>{escape(str(host))}</string>
    <string>--port</string><string>{escape(str(port))}</string>
  </array>
  <key>WorkingDirectory</key><string>{escape(str(root))}</string>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>StandardOutPath</key><string>{escape(str(log_path))}</string>
  <key>StandardErrorPath</key><string>{escape(str(log_path))}</string>
{env_entries}</dict>
</plist>
"""


def install() -> tuple[bool, str]:
    """Write the plist and (re)load it. Returns (ok, message)."""
    path = plist_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    (ROOT_DIR / "var").mkdir(parents=True, exist_ok=True)
    path.write_text(build_plist(), encoding="utf-8")
    # Reload cleanly: unload first (ignore failure if not loaded), then load -w.
    subprocess.run(["launchctl", "unload", str(path)], capture_output=True, check=False)
    result = subprocess.run(["launchctl", "load", "-w", str(path)], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return False, f"Wrote {path} but `launchctl load` failed: {result.stderr.strip()}"
    from app.core.config import get_server_host, get_server_port

    return True, f"Installed and started. YouOS will run at http://{get_server_host()}:{get_server_port()} on every login."


def uninstall() -> tuple[bool, str]:
    path = plist_path()
    if path.exists():
        subprocess.run(["launchctl", "unload", str(path)], capture_output=True, check=False)
        path.unlink()
        return True, f"Stopped and removed {path}."
    return True, "Not installed (nothing to remove)."


def is_loaded() -> bool:
    result = subprocess.run(["launchctl", "list", LABEL], capture_output=True, check=False)
    return result.returncode == 0


def status() -> str:
    installed = plist_path().exists()
    loaded = is_loaded()
    if loaded:
        return "running (LaunchAgent loaded)"
    if installed:
        return "installed but not loaded"
    return "not installed"
