"""
monitor.py - Runtime behavior capture.

Two responsibilities:

  1. get_bootstrap_source():
     Returns the Python source that runs INSIDE the sandbox. It installs
     lightweight audit hooks (via sys.addaudithook, Python 3.8+) to record:
        - network connections (target host/IP + port)
        - file open (path + mode)
        - subprocess / process creation
        - environment variable reads
        - dynamic code execution (exec/compile)
     Then it executes each entrypoint with a per-run timeout and prints ONE
     JSON line: {"behaviors": [...]}.

  2. normalize(raw):
     Runs on the HOST. Converts the raw payload from any backend into a flat,
     uniform list of behavior dicts:
        {"type": "network|file|process|env|exec", "detail": {...}}

The bootstrap uses only the Python standard library so it works in a bare
python:slim container with no pip install.
"""

import json


def normalize(raw):
    """Normalize a backend's raw payload into a flat behavior list."""
    if not raw:
        return []
    behaviors = raw.get('behaviors') if isinstance(raw, dict) else None
    if not behaviors:
        return []
    flat = []
    for b in behaviors:
        if not isinstance(b, dict):
            continue
        btype = b.get('type')
        detail = b.get('detail', {})
        if btype:
            flat.append({'type': btype, 'detail': detail})
    return flat


def get_bootstrap_source():
    """Return the in-sandbox monitor bootstrap source (stdlib only)."""
    return _BOOTSTRAP_SRC


# The bootstrap is stored as a plain string so it can be written into the
# sandbox temp dir and executed there. It relies only on the standard library.
_BOOTSTRAP_SRC = r'''
import os, sys, json, runpy, threading, time

_behaviors = []

def _record(btype, **detail):
    try:
        _behaviors.append({"type": btype, "detail": detail})
    except Exception:
        pass

# --- Audit hook: capture sensitive runtime events (Python 3.8+) ---
def _audit(event, args):
    try:
        if event == "socket.connect":
            addr = args[1] if len(args) > 1 else None
            _record("network", event=event, address=str(addr))
        elif event in ("urllib.Request",):
            url = args[0] if args else None
            _record("network", event=event, url=str(url))
        elif event == "open":
            path = args[0] if args else None
            mode = args[1] if len(args) > 1 else None
            _record("file", path=str(path), mode=str(mode))
        elif event in ("subprocess.Popen", "os.system", "os.exec"):
            cmd = args[0] if args else None
            _record("process", event=event, cmd=str(cmd)[:300])
        elif event in ("exec", "compile"):
            _record("exec", event=event)
    except Exception:
        pass

try:
    sys.addaudithook(_audit)
except Exception:
    pass

# --- Capture environment variable reads via os.environ wrapper ---
_orig_getitem = os.environ.__class__.__getitem__
def _env_getitem(self, key):
    try:
        _record("env", key=str(key))
    except Exception:
        pass
    return _orig_getitem(self, key)
try:
    os.environ.__class__.__getitem__ = _env_getitem
except Exception:
    pass

def _run_one(entry, timeout):
    def target():
        try:
            runpy.run_path(entry, run_name="__main__")
        except SystemExit:
            pass
        except Exception as e:
            _record("error", entry=entry, err=str(e)[:200])
    t = threading.Thread(target=target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        _record("timeout", entry=entry)

def main():
    try:
        entrypoints = json.loads(os.environ.get("SSC_ENTRYPOINTS", "[]"))
    except Exception:
        entrypoints = []
    try:
        timeout = int(os.environ.get("SSC_TIMEOUT", "30"))
    except Exception:
        timeout = 30
    per = max(3, timeout // max(1, len(entrypoints))) if entrypoints else timeout
    base = "/skill"
    for ep in entrypoints:
        full = ep if os.path.isabs(ep) else os.path.join(base, ep)
        if os.path.isfile(full) and full.lower().endswith(".py"):
            _run_one(full, per)
    print(json.dumps({"behaviors": _behaviors}))

main()
'''
