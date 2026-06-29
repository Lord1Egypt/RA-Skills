#!/usr/bin/env python3
"""skill-sub settings manager (v1.2.0)

HTML settings UI + CLI config management + conversational fallback.

Usage:
    python settings.py                     # Interactive: start server + open browser
    python settings.py --serve-only        # Agent mode: print SERVER_STARTED:<port>, wait for .settings_done
    python settings.py --save-config '<json>'  # Save config from JSON string
    python settings.py --get-config        # Print current config as JSON
"""

import json
import os
import sys
import time
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# R-12 审计锚点：数据目录字面量声明
DEFAULT_DATA_DIR_RAW = "skills/.standardization/skill-sub/data/"

SKILL_DIR = Path(__file__).resolve().parent.parent
# 运行时绝对路径
DATA_DIR = SKILL_DIR.parent / ".standardization" / "skill-sub" / "data"


# ─── Paths ────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSETS_DIR = SKILL_DIR / "scripts"

# Pre-compute skill_dir for HTTP handler (before forking / chdir)
_SCRIPT_DIR_STR = str(SCRIPT_DIR)
_SKILL_DIR_STR = str(SKILL_DIR)
_ASSETS_DIR_STR = str(ASSETS_DIR)

def get_home_dir():
    """Resolve SKILL_SUB_HOME with fallback."""
    home = (
        os.environ.get("SKILL_SUB_HOME")
        or os.environ.get("SKILL_CHAIN_HOME")
        or str(Path.home() / ".workbuddy" / "skills" / ".standardization" / "skill-sub")
    )
    return Path(home).expanduser()

    def get_default_config_path():
        return SCRIPT_DIR / "default_config.json"

def get_user_config_path():
    return get_home_dir() / "config.json"

def get_settings_done_path():
    return SKILL_DIR / ".settings_done"

def load_config():
    """Load merged config: default_config.json + config.json (user overrides)."""
    defaults = {}
    defaults_path = get_default_config_path()
    if defaults_path.exists():
        defaults = json.loads(defaults_path.read_text(encoding="utf-8"))

    user_cfg = {}
    user_path = get_user_config_path()
    if user_path.exists():
        user_cfg = json.loads(user_path.read_text(encoding="utf-8"))

    defaults.update(user_cfg)
    return defaults

def save_config_from_dict(cfg_dict):
    """Save config dict to user config.json, creating parent dirs if needed."""
    user_path = get_user_config_path()
    user_path.parent.mkdir(parents=True, exist_ok=True)

    # Remove internal tracking key if present
    cfg_dict.pop("_saved", None)

    with open(user_path, "w", encoding="utf-8") as f:
        json.dump(cfg_dict, f, indent=2, ensure_ascii=False)
    return user_path

def save_config_from_json(json_str):
    """Parse JSON string and save. Returns (success: bool, message: str)."""
    try:
        cfg = json.loads(json_str)
    except json.JSONDecodeError as e:
        return False, f"JSON parse error: {e}"

    required_keys = {"use_memory_reference", "naming_mode", "default_max_retries"}
    if not required_keys.issubset(cfg.keys()):
        missing = required_keys - cfg.keys()
        return False, f"Missing keys: {missing}"

    # Validate values
    if cfg.get("use_memory_reference") not in (True, False):
        return False, "use_memory_reference must be true or false"
    if cfg.get("naming_mode") not in ("auto", "manual"):
        return False, 'naming_mode must be "auto" or "manual"'
    if not isinstance(cfg.get("default_max_retries"), int) or cfg["default_max_retries"] < 1:
        return False, "default_max_retries must be a positive integer"

    try:
        path = save_config_from_dict(cfg)
        return True, f"Config saved to {path}"
    except Exception as e:
        return False, f"Save error: {e}"

# ─── HTTP Server ─────────────────────────────────────────────────────

def find_available_port(start=8080, end=8999):
    for port in range(start, end + 1):
        try:
            s = HTTPServer(("localhost", port), _make_handler)
            s.server_close()
            return port
        except OSError:
            continue
    return start

class SettingsHandler(BaseHTTPRequestHandler):
    """HTTP handler for settings UI."""

    skill_dir = _SKILL_DIR_STR
    home_dir = str(get_home_dir())

    def log_message(self, format, *args):
        # Suppress default request logging
        pass

    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-cache")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ("", "/", "/index.html"):
            html_path = Path(self.skill_dir) / "scripts" / "settings.html"
            if not html_path.exists():
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"settings.html not found")
                return
            content = html_path.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self._send_cors()
            self.end_headers()
            self.wfile.write(content)

        elif path == "/config":
            config = load_config()
            body = json.dumps(config, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors()
            self.end_headers()
            self.wfile.write(body)

        elif path == "/done":
            done_path = Path(self.skill_dir) / ".settings_done"
            done_path.touch()
            html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Settings Complete</title>
<style>body{font-family:system-ui;display:flex;justify-content:center;align-items:center;
min-height:100vh;margin:0;background:#1a1a2e;color:#eee}
.box{text-align:center;padding:40px;background:#16213e;border-radius:12px}
.ok{font-size:64px;margin-bottom:16px}h2{margin:0 0 8px}p{color:#8899aa}
</style></head><body><div class="box"><div class="ok">&#10004;</div>
<h2>Settings Complete</h2><p>You can close this window.</p></div></body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self._send_cors()
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/save":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)

            try:
                data = json.loads(body.decode("utf-8"))
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Invalid JSON"}).encode())
                return

            # Quick validation
            if "use_memory_reference" not in data:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": "Missing use_memory_reference"}).encode())
                return

            # Respond immediately, save in background
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self._send_cors()
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())

            # Background save
            t = threading.Thread(target=_background_save, args=(data,), daemon=True)
            t.start()
        else:
            self.send_response(404)
            self.end_headers()

def _make_handler(*args, **kwargs):
    return SettingsHandler(*args, **kwargs)

def _background_save(data):
    """Save config in background thread."""
    try:
        save_config_from_dict(data)

        # Write _saved flag so frontend can detect completion
        user_path = get_user_config_path()
        config = json.loads(user_path.read_text(encoding="utf-8"))
        config["_saved"] = True
        with open(user_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[settings] Background save error: {e}", file=sys.stderr)

def shutdown_server():
    """Create the done flag file to signal server shutdown."""
    get_settings_done_path().touch()

# ─── Server lifecycle ────────────────────────────────────────────────

def start_server(port, serve_only=False):
    """Start HTTP server. If serve_only, block until .settings_done; else open browser."""
    server = HTTPServer(("localhost", port), SettingsHandler)
    server.skill_dir = _SKILL_DIR_STR
    server.home_dir = str(get_home_dir())

    done_path = get_settings_done_path()
    # Clean up any stale flag
    if done_path.exists():
        done_path.unlink()

    if serve_only:
        print(f"SERVER_STARTED:{port}")
        sys.stdout.flush()

    # Block until done flag or keyboard interrupt
    try:
        while not done_path.exists():
            server.handle_request()  # Handle one request at a time (single-thread)
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        if done_path.exists():
            done_path.unlink()

# ─── CLI ─────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    if "--serve-only" in args:
        port = find_available_port()
        start_server(port, serve_only=True)

    elif "--save-config" in args:
        idx = args.index("--save-config")
        if idx + 1 >= len(args):
            print("Error: --save-config requires a JSON string argument", file=sys.stderr)
            sys.exit(1)
        json_str = args[idx + 1]
        ok, msg = save_config_from_json(json_str)
        if ok:
            print(msg)
            sys.exit(0)
        else:
            print(f"Error: {msg}", file=sys.stderr)
            sys.exit(1)

    elif "--get-config" in args:
        config = load_config()
        # Strip internal keys
        for k in ("_saved", "_skill_sub_home"):
            config.pop(k, None)
        print(json.dumps(config, ensure_ascii=False, indent=2))
        sys.exit(0)

    else:
        # Interactive mode: start server + open browser
        port = find_available_port()
        print(f"Starting settings server on port {port}...")

        # Open browser in background
        def open_browser():
            time.sleep(0.5)
            webbrowser.open(f"http://localhost:{port}/")

        t = threading.Thread(target=open_browser, daemon=True)
        t.start()

        start_server(port, serve_only=False)

if __name__ == "__main__":
    main()
