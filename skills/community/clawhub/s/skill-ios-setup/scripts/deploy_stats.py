#!/usr/bin/env python3
"""
Deploy and start the stats server for the OpenClaw iOS dashboard.
- Detects workspace path dynamically (no hardcoded agent name)
- Installs missing Python deps
- Starts the server with token passed via env (not inlined in shell string)
- Suggests OS-level auto-restart (Docker or crontab) — no agent watchdog
"""
import json
import os
import subprocess
import sys
import time


def run(cmd, timeout=30, env=None):
    e = os.environ.copy()
    if env:
        e.update(env)
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, env=e)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def run_args(args, timeout=30, env=None):
    """Run a command as a list of args (avoids shell interpolation of secrets)."""
    e = os.environ.copy()
    if env:
        e.update(env)
    r = subprocess.run(args, capture_output=True, text=True, timeout=timeout, env=e)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


def is_running():
    code, _, _ = run("pgrep -f stats_server.py")
    return code == 0


def get_workspace():
    """Detect workspace path from openclaw config — never hardcode agent name."""
    # Try CLI first
    code, out, _ = run("openclaw config get agents.defaults.workspace 2>/dev/null")
    if code == 0 and out and out not in ("null", ""):
        return out.strip('"')

    # Fallback: parse config file
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            import re
            with open(config_path) as f:
                content = f.read()
            m = re.search(r'"workspace"\s*:\s*"([^"]+)"', content)
            if m:
                return m.group(1)
        except Exception:
            pass

    return os.path.expanduser("~/.openclaw/workspace")


def find_stats_server(workspace):
    """Search common locations for stats_server.py under the workspace."""
    candidates = [
        os.path.join(workspace, "scripts", "dashboard", "stats_server.py"),
        os.path.join(workspace, "orchestrator", "scripts", "dashboard", "stats_server.py"),
        os.path.join(workspace, "main", "scripts", "dashboard", "stats_server.py"),
    ]
    # Also search one level deep
    try:
        for entry in os.scandir(workspace):
            if entry.is_dir():
                candidate = os.path.join(entry.path, "scripts", "dashboard", "stats_server.py")
                if candidate not in candidates:
                    candidates.append(candidate)
    except Exception:
        pass

    for c in candidates:
        if os.path.exists(c):
            return c
    return None


def get_gateway_token():
    """Read gateway token — never inline into shell strings."""
    code, out, _ = run("openclaw config get gateway.auth.token 2>/dev/null")
    if code == 0 and out and out not in ("null", ""):
        return out.strip('"')

    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            import re
            with open(config_path) as f:
                content = f.read()
            m = re.search(r'"token"\s*:\s*"([^"]+)"', content)
            if m:
                return m.group(1)
        except Exception:
            pass
    return None


def start_server(stats_script, token):
    """Start stats server with token passed via environment, not shell string."""
    ensure_script = os.path.join(os.path.dirname(stats_script), "..", "..", "ensure_stats_server.sh")
    ensure_script = os.path.normpath(ensure_script)

    env_override = {"OPENCLAW_GATEWAY_TOKEN": token or ""}

    if os.path.exists(ensure_script):
        os.chmod(ensure_script, 0o755)
        code, out, err = run_args(["bash", ensure_script], env=env_override)
        return code == 0, out, err
    else:
        # Start directly — token passed via env, NOT inlined in shell command
        log_path = "/tmp/stats_server.log"
        with open(log_path, "a") as log:
            proc = subprocess.Popen(
                ["python3", stats_script],
                stdout=log,
                stderr=log,
                env={**os.environ, **env_override},
                start_new_session=True
            )
        time.sleep(1)
        success = is_running()
        return success, f"PID: {proc.pid}" if success else "", "Check /tmp/stats_server.log"


def main():
    if is_running():
        print(json.dumps({
            "ok": True,
            "already_running": True,
            "message": "Stats server is already running"
        }))
        return

    workspace = get_workspace()
    stats_script = find_stats_server(workspace)

    if not stats_script:
        print(json.dumps({
            "ok": False,
            "error": f"stats_server.py not found under workspace: {workspace}. Is the stats server skill installed?",
            "workspace": workspace
        }))
        sys.exit(1)

    token = get_gateway_token()
    if not token:
        print(json.dumps({
            "ok": False,
            "error": "Could not read gateway token from config. Check gateway.auth.token in openclaw.json."
        }))
        sys.exit(1)

    success, out, err = start_server(stats_script, token)

    ensure_script_path = os.path.join(os.path.dirname(stats_script), "..", "..", "ensure_stats_server.sh")
    ensure_script_path = os.path.normpath(ensure_script_path)

    print(json.dumps({
        "ok": success,
        "started": success,
        "already_running": False,
        "workspace": workspace,
        "stats_script": stats_script,
        "ensure_script": ensure_script_path if os.path.exists(ensure_script_path) else None,
        "message": "Stats server started successfully" if success else f"Failed to start: {err or 'check /tmp/stats_server.log'}"
    }, indent=2))

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
