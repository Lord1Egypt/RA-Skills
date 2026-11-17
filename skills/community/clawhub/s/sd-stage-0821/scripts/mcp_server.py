#!/usr/bin/env python3
"""space-duck local MCP server — Lane A parity for /beak/duck/mcp.

Hosted (Lane B) ducks are already MCP servers at
https://beak.spaceduckling.com/beak/duck/mcp (single-response Streamable
HTTP). Lane A (BYOB) ducks are refused there with `-32000 lane_a_unsupported`
— the lane is immutable, the platform never fronts a Lane A duck. This
script is the Lane A equivalent: a localhost MCP server that exposes the
IDENTICAL 6 tools with IDENTICAL names/schemas, and forwards each tool
call 1:1 to the SAME public /beak/... REST route the hosted implementation
would touch, using this duck's beak_key from ~/.space-duck/config.json.

Facade law (constitution rule 1): no local business logic, no local state
beyond config. Every tools/call is a plain HTTPS request to beak, and
whatever status/message beak returns is what the MCP client sees.

Lane immutability (rule 2): the beak_key never leaves the local box except
as an Authorization header to beak.spaceduckling.com over TLS, and is
never printed beyond the first 8 chars.

Stdlib only (rule 4).

Usage:
  mcp_server.py run                       # start on 127.0.0.1:8472
  mcp_server.py status                    # show config + proxy secret path
  mcp_server.py print-client-config       # MCP client JSON (url + bearer)
  mcp_server.py install-systemd           # user-scope autostart (linux)
  mcp_server.py install-launchd           # LaunchAgent autostart (macOS)
  mcp_server.py uninstall-service         # remove either autostart entry

Env:
  SPACEDUCK_MCP_PORT       override 8472
  SPACEDUCK_MCP_HOST       override 127.0.0.1 (do not bind non-loopback)
  SPACEDUCK_CONFIG         override ~/.space-duck/config.json
  SPACEDUCK_MCP_NO_AUTH=1  disable local bearer auth (single-user boxes)
"""
import io
import json
import os
import re
import secrets as _secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from contextlib import redirect_stdout, redirect_stderr
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# ── local send_peck.py facade ───────────────────────────────────────────
# The MCP `send_peck` tool must NOT rebuild the v2/v3 signed envelope by
# hand — an unsigned POST to /beak/agent/message is rejected by platform
# gates. Reuse the existing local implementation (canonical_v2 / sign_v2,
# optional v3 Ed25519, permission preflight, target-name resolution, grant
# auto-request) that send_peck.py already contains.
#
# Import mechanics: send_peck.py lives beside this file in scripts/, but
# CWD may not be scripts/. Mirror the sys.path trick send_peck.py itself
# uses (~L124) for its `_envelope` sibling import.
import pathlib as _pl
_SCRIPT_DIR = str(_pl.Path(__file__).resolve().parent)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)
try:
    import send_peck as _send_peck_mod  # noqa: E402
except Exception as _e:  # pragma: no cover — surfaced on tool call
    _send_peck_mod = None
    _send_peck_import_err = str(_e)
else:
    _send_peck_import_err = None

# ── config / secrets ─────────────────────────────────────────────────────

CFG_DIR = Path(os.environ.get("SPACEDUCK_CONFIG_DIR", str(Path.home() / ".space-duck")))
CFG_PATH = Path(os.environ.get("SPACEDUCK_CONFIG", str(CFG_DIR / "config.json")))
PROXY_SECRET_PATH = CFG_DIR / "mcp_proxy_secret"
DEFAULT_PORT = int(os.environ.get("SPACEDUCK_MCP_PORT", "8472"))
DEFAULT_HOST = os.environ.get("SPACEDUCK_MCP_HOST", "127.0.0.1")
DEFAULT_API_BASE = "https://beak.spaceduckling.com"
UA = "space-duck-local-mcp/0.1"

_MCP_SRV_PROTOS = ("2024-11-05", "2025-03-26", "2025-06-18")
_DEFAULT_PROTO = "2025-03-26"  # mirrors hosted facade default
SERVER_NAME = "space-duck-local-mcp"
SERVER_VERSION = "0.1"


def load_config():
    if not CFG_PATH.exists():
        raise RuntimeError(
            f"~/.space-duck/config.json missing at {CFG_PATH} — run setup.py first")
    try:
        cfg = json.loads(CFG_PATH.read_text())
    except Exception as e:
        raise RuntimeError(f"cannot parse {CFG_PATH}: {e}")
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg


def proxy_secret():
    """Local bearer for the MCP port. Auto-generated once, 0600. Set
    SPACEDUCK_MCP_NO_AUTH=1 to disable (single-user boxes only)."""
    if os.environ.get("SPACEDUCK_MCP_NO_AUTH") == "1":
        return None
    try:
        s = PROXY_SECRET_PATH.read_text().strip()
        if s:
            return s
    except FileNotFoundError:
        pass
    CFG_DIR.mkdir(parents=True, exist_ok=True, mode=0o700)
    s = "sd-mcp-" + _secrets.token_urlsafe(24)
    fd = os.open(str(PROXY_SECRET_PATH),
                 os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(s + "\n")
    return s


# ── the 6 tools — schemas MUST match _mcp_srv_tools() in lambda_function.py
# ──────────────────────────────────────────────────────────────────────────

def _tools():
    _obj = {"type": "object", "properties": {}, "required": []}
    return [
        {"name": "duck_status",
         "description": "This duck's profile: name, service tier, status.",
         "inputSchema": _obj},
        {"name": "list_workspace_files",
         "description": "List the duck's workspace files (memory, notes, plans).",
         "inputSchema": _obj},
        {"name": "read_workspace_file",
         "description": ("Read one workspace file (first 64KB). Use "
                         "list_workspace_files to find paths; MEMORY.md is "
                         "the duck's long-term memory."),
         "inputSchema": {"type": "object", "properties": {
             "path": {"type": "string",
                      "description": "File path from list_workspace_files"}},
             "required": ["path"]}},
        {"name": "send_task",
         "description": ("Hand the duck a task. It processes asynchronously "
                         "with its own brain/tools and reports the result in "
                         "its owner chat — this call returns immediately."),
         "inputSchema": {"type": "object", "properties": {
             "message": {"type": "string", "description": "The task text"}},
             "required": ["message"]}},
        {"name": "list_connections",
         "description": ("Ducks this duck is connected to — the valid "
                         "send_peck targets."),
         "inputSchema": _obj},
        # NOTE (Lane A divergence from hosted schema): the hosted
        # /beak/duck/mcp send_peck exposes `scopes` (scopes_asserted) as an
        # input, but the local send_peck.py implementation always signs the
        # v2 envelope with scopes_asserted=[] (see send_peck.py L284) and
        # accepts no caller-supplied scope list — passing scopes here would
        # be silently dropped, which is dishonest. The tool schema is
        # aligned to what the local impl truly supports. Similarly, `intent`
        # here maps to the local `peck_type` parameter (same enum).
        {"name": "send_peck",
         "description": ("Send a peck (duck-to-duck message) to a connected "
                         "duck. Platform trust gates apply: it delivers "
                         "instantly or is held for the receiving owner's "
                         "approval. Signed v2 (HMAC) / v3 (Ed25519) envelope "
                         "is built by the local send_peck.py — this tool is "
                         "a facade over that module."),
         "inputSchema": {"type": "object", "properties": {
             "to": {"type": "string",
                    "description": ("Target spaceduck_id, or the exact name "
                                    "of a connected duck (see "
                                    "list_connections)")},
             "message": {"type": "string", "description": "The peck text"},
             "intent": {"type": "string",
                        "enum": ["notify", "query", "data_request",
                                 "task_delegation"],
                        "description": ("Peck intent (default notify) — "
                                        "maps to peck_type in the local "
                                        "sender. Richer intents may be "
                                        "held for the receiving owner's "
                                        "approval.")}},
             "required": ["to", "message"]}},
    ]


# ── upstream /beak HTTP ─────────────────────────────────────────────────

# Set by tests to stub the network layer.
_URLOPEN = urllib.request.urlopen


def _beak(cfg, method, route, body=None, timeout=30):
    """1:1 HTTPS call to a /beak/... REST route with X-Beak-Key auth.
    Returns (status, parsed_json_or_str). Errors passed through honestly."""
    api = (cfg.get("api_base") or DEFAULT_API_BASE).rstrip("/")
    bk = cfg.get("beak_key") or ""
    if not bk:
        return 0, {"error": "no_beak_key",
                   "detail": "config.beak_key missing — run setup.py"}
    url = api + route
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={"X-Beak-Key": bk,
                 "Content-Type": "application/json",
                 "Accept": "application/json",
                 "User-Agent": UA})
    try:
        with _URLOPEN(req, timeout=timeout) as r:
            raw = r.read()
            status = r.status
            hdrs = {k.lower(): v for k, v in r.headers.items()} \
                if hasattr(r, "headers") else {}
    except urllib.error.HTTPError as e:
        raw = e.read() or b""
        status = e.code
        hdrs = {k.lower(): v for k, v in (e.headers or {}).items()} \
            if getattr(e, "headers", None) else {}
    except Exception as e:
        return 0, {"error": "upstream_unreachable", "detail": str(e)[:200]}
    try:
        parsed = json.loads(raw or b"{}")
    except Exception:
        parsed = {"_raw": (raw[:400].decode("utf-8", "replace") if raw else "")}
    # surface Retry-After for 429 mapping
    if status == 429 and isinstance(parsed, dict):
        ra = hdrs.get("retry-after")
        if ra and "retry_after_s" not in parsed:
            try:
                parsed["retry_after_s"] = int(ra)
            except Exception:
                pass
    return status, parsed


# ── tool dispatch — each is a strict 1:1 /beak call ─────────────────────

def _dispatch(cfg, tool, args):
    """Returns (jsonrpc_error_or_None, content_text, is_error).
    Never raises. Never contains local business logic beyond routing."""
    args = args or {}
    sd_id = cfg.get("spaceduck_id") or ""

    # duck_status → POST /beak/spaceducks (returns the duck's own row)
    if tool == "duck_status":
        st, out = _beak(cfg, "POST", "/beak/spaceducks",
                        body={"spaceduck_id": sd_id})
        return _std(st, out)

    # list_workspace_files → GET /beak/skill/files
    if tool == "list_workspace_files":
        st, out = _beak(cfg, "GET", "/beak/skill/files")
        return _std(st, out)

    # read_workspace_file → POST /beak/skill/file {action:read}
    if tool == "read_workspace_file":
        path_in = str(args.get("path") or "").strip().lstrip("/")
        st, out = _beak(cfg, "POST", "/beak/skill/file",
                        body={"filename": path_in, "action": "read"})
        return _std(st, out)

    # send_task → POST /beak/tg/notify (owner-chat handoff, beak_key-auth'd).
    # Hosted equivalent hands a synthetic TG update to the duck's own brain;
    # for Lane A the local brain IS running here already, so notifying the
    # owner chat is the honest facade equivalent.
    if tool == "send_task":
        msg = str(args.get("message") or "").strip()[:4000]
        if not msg:
            return None, "message required", True
        st, out = _beak(cfg, "POST", "/beak/tg/notify",
                        body={"spaceduck_id": sd_id,
                              "message": (f"[external agent task via local MCP] "
                                          f"{msg}\n\n(Handle this task and "
                                          f"report the result to your owner "
                                          f"in this chat.)")},
                        timeout=60)
        return _std(st, out)

    # list_connections → POST /beak/spaceducks with mode='connections'
    # NOTE: Lane B facade reads DDB directly; there is no exact 1:1 public
    # REST route. /beak/spaceducks with mode='connections' is the closest
    # public analog the space-duck skill already relies on (connections.py).
    if tool == "list_connections":
        st, out = _beak(cfg, "POST", "/beak/spaceducks",
                        body={"spaceduck_id": sd_id,
                              "mode": "connections"})
        return _std(st, out)

    # send_peck → facade over the local send_peck.py module. That module
    # builds the signed v2 (HMAC-SHA256) envelope + v3 (Ed25519) if a
    # local sign key exists, runs the /beak/connection/permissions
    # pre-flight, resolves name→SDID via its own resolve_target, and
    # can auto-request a capability grant on a 403 grant_required.
    # Rebuilding any of that here would produce an UNSIGNED payload the
    # platform rejects — the whole point of this facade.
    if tool == "send_peck":
        if _send_peck_mod is None:
            return None, (f"send_peck module unavailable: "
                          f"{_send_peck_import_err}"), True
        msg = str(args.get("message") or "").strip()[:4000]
        to_in = str(args.get("to") or "").strip()
        if not msg or not to_in:
            return None, "to and message required", True
        intent = str(args.get("intent") or "notify").strip().lower()
        if intent not in ("notify", "query", "data_request", "task_delegation"):
            return None, ("invalid intent — must be one of: notify, query, "
                          "data_request, task_delegation"), True
        # Capture stdout/stderr: send_peck.py prints friendly progress
        # and calls sys.exit() on any error branch (403/429/etc.), so we
        # convert that into a structured MCP result rather than killing
        # the server process.
        buf_out, buf_err = io.StringIO(), io.StringIO()
        try:
            with redirect_stdout(buf_out), redirect_stderr(buf_err):
                target_sdid = _send_peck_mod.resolve_target(cfg, to_in)
                resp = _send_peck_mod.send_peck(
                    cfg, target_sdid, msg, peck_type=intent)
        except SystemExit as se:
            code = se.code if isinstance(se.code, int) else 1
            text = (buf_out.getvalue() + buf_err.getvalue()).strip() \
                or f"send_peck exited with code {code}"
            return None, text, True
        except Exception as e:
            text = (buf_out.getvalue() + buf_err.getvalue()).strip()
            detail = f"send_peck raised {type(e).__name__}: {e}"
            return None, (detail + ("\n" + text if text else "")), True
        # Success path — response dict from /beak/agent/message. Pass
        # through honestly: server may say status=sent|held|approval_
        # required|202-style pending, plus channels/byob_push/etc.
        if not isinstance(resp, dict):
            return None, json.dumps({"raw": str(resp)}), False
        return None, json.dumps(resp), False

    return {"code": -32602, "message": f"unknown tool: {tool}"}, "", True


def _std(status, out):
    """Normalise an upstream HTTP result into (jsonrpc_error, text, is_error).
    429 is surfaced as a JSON-RPC error so clients see retry_after_s.
    Other non-2xx codes come back as isError=true content (hosted convention)."""
    if status == 429:
        # Pass through as JSON-RPC error, preserving retry_after_s
        msg = out.get("error") or out.get("message") or "rate_limited"
        extra = {}
        if isinstance(out, dict) and "retry_after_s" in out:
            extra["retry_after_s"] = out["retry_after_s"]
        err = {"code": -32003, "message": f"rate_limited: {msg}"}
        if extra:
            err["data"] = extra
        return err, "", True
    if not (200 <= (status or 0) < 300):
        body_text = json.dumps(out) if not isinstance(out, str) else out
        return None, f"upstream {status}: {body_text[:800]}", True
    if isinstance(out, str):
        return None, out, False
    return None, json.dumps(out), False


# ── HTTP handler ────────────────────────────────────────────────────────

def _make_handler(cfg, secret):

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *a):
            sys.stderr.write("[sd-mcp] " + fmt % a + "\n")

        def _write(self, code, obj, extra_headers=None):
            raw = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            for k, v in (extra_headers or {}).items():
                self.send_header(k, v)
            self.end_headers()
            try:
                self.wfile.write(raw)
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            # Streamable-HTTP single-response mode — no SSE, no GET stream.
            self._write(405, {"error": "method_not_allowed",
                              "message": ("MCP single-response mode: POST "
                                          "JSON-RPC only (no SSE stream).")},
                        extra_headers={"Allow": "POST"})

        def do_POST(self):
            # local bearer gate
            if secret is not None:
                auth = self.headers.get("Authorization", "")
                if auth != "Bearer " + secret:
                    self._write(401, {"error": "unauthorized",
                                      "message": ("local MCP proxy secret "
                                                  "required — read it from " +
                                                  str(PROXY_SECRET_PATH) +
                                                  " and set as Authorization: "
                                                  "Bearer <secret>")})
                    return
            length = int(self.headers.get("Content-Length", 0) or 0)
            if length > 1 * 1024 * 1024:
                self._write(413, {"error": "too_large"})
                return
            raw = self.rfile.read(length) if length else b""
            try:
                body = json.loads(raw or b"{}")
            except Exception:
                self._write(400, {"jsonrpc": "2.0", "id": None,
                                  "error": {"code": -32700,
                                            "message": "parse error"}})
                return
            rpc_id = body.get("id")
            method = str(body.get("method") or "")

            def ok(res):
                self._write(200, {"jsonrpc": "2.0", "id": rpc_id, "result": res})

            def err(code, msg, data=None):
                e = {"code": code, "message": msg}
                if data is not None:
                    e["data"] = data
                self._write(200, {"jsonrpc": "2.0", "id": rpc_id, "error": e})

            if method == "initialize":
                pv = str((body.get("params") or {}).get("protocolVersion") or "")
                return ok({
                    "protocolVersion": pv if pv in _MCP_SRV_PROTOS else _DEFAULT_PROTO,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NAME,
                                   "version": SERVER_VERSION,
                                   "laneA": True}})
            if method.startswith("notifications/"):
                # spec: notifications get 202 Accepted, no body
                self.send_response(202)
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            if method == "ping":
                return ok({})
            if method == "tools/list":
                return ok({"tools": _tools()})
            if method == "tools/call":
                p = body.get("params") or {}
                tool = str(p.get("name") or "")
                jerr, text, is_error = _dispatch(cfg, tool,
                                                 p.get("arguments") or {})
                if jerr is not None:
                    return err(jerr["code"], jerr["message"],
                               jerr.get("data"))
                return ok({"content": [{"type": "text", "text": text}],
                           "isError": bool(is_error)})
            return err(-32601, f"method not found: {method}")

    return H


def serve(host=DEFAULT_HOST, port=DEFAULT_PORT):
    if host not in ("127.0.0.1", "localhost", "::1"):
        print(f"⚠️ refusing non-loopback bind {host} — Lane A local server "
              f"must not be exposed off-box", file=sys.stderr)
        return 2
    cfg = load_config()
    bk = cfg.get("beak_key") or ""
    secret = proxy_secret()
    H = _make_handler(cfg, secret)
    srv = ThreadingHTTPServer((host, port), H)
    srv.daemon_threads = True
    print(f"space-duck local MCP on http://{host}:{port}/")
    print(f"  spaceduck_id : {cfg.get('spaceduck_id', '(unset)')}")
    print(f"  beak_key     : {(bk[:8] + '…') if bk else '(unset)'}")
    if secret:
        print(f"  bearer       : {secret}")
        print(f"  (also at {PROXY_SECRET_PATH}; disable with SPACEDUCK_MCP_NO_AUTH=1)")
    else:
        print("⚠️ auth disabled (SPACEDUCK_MCP_NO_AUTH=1)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
    return 0


# ── CLI helpers ─────────────────────────────────────────────────────────

def cmd_status(port):
    try:
        cfg = load_config()
        bk = cfg.get("beak_key") or ""
        print(f"config       : ✅ {CFG_PATH}")
        print(f"spaceduck_id : {cfg.get('spaceduck_id', '(unset)')}")
        print(f"beak_key     : {(bk[:8] + '…') if bk else '(unset)'}")
        print(f"api_base     : {cfg.get('api_base', DEFAULT_API_BASE)}")
    except Exception as e:
        print(f"config       : ❌ {e}")
    s = proxy_secret()
    print(f"proxy secret : {'✅ ' + str(PROXY_SECRET_PATH) if s else '⚠️ disabled'}")
    try:
        req = urllib.request.Request(f"http://127.0.0.1:{port}/",
                                     method="POST",
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + (s or "")},
                                     data=b'{"jsonrpc":"2.0","id":1,"method":"ping"}')
        with urllib.request.urlopen(req, timeout=3) as r:
            up = r.status == 200
    except Exception:
        up = False
    print(f"proxy :{port}  : {'✅ up' if up else '❌ down'}")
    return 0


def cmd_print_client_config(port):
    s = proxy_secret()
    cfg = {"mcpServers": {"space-duck": {
        "transport": "http",
        "url": f"http://127.0.0.1:{port}/",
        "headers": {"Authorization": "Bearer " + (s or "")}}}}
    print(json.dumps(cfg, indent=2))
    return 0


SERVICE_NAME = "space-duck-mcp"


def _script_path():
    return os.path.abspath(__file__)


def install_systemd(port):
    py = sys.executable or "python3"
    unit_dir = Path.home() / ".config/systemd/user"
    unit_dir.mkdir(parents=True, exist_ok=True)
    unit = unit_dir / (SERVICE_NAME + ".service")
    unit.write_text(f"""[Unit]
Description=space-duck local MCP server (Lane A parity)
After=network-online.target

[Service]
ExecStart={py} {_script_path()} run
Environment="SPACEDUCK_MCP_PORT={port}"
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
""")
    unit.chmod(0o600)
    for args in (["daemon-reload"], ["enable", "--now", SERVICE_NAME]):
        r = subprocess.run(["systemctl", "--user"] + args,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(f"systemctl --user {' '.join(args)} failed: "
                  f"{r.stderr or r.stdout}", file=sys.stderr)
            print("(headless box? loginctl enable-linger $USER)",
                  file=sys.stderr)
            return 1
    print(f"✅ systemd user service installed + started ({unit}), MCP on 127.0.0.1:{port}")
    return 0


def install_launchd(port):
    plist_dir = Path.home() / "Library/LaunchAgents"
    plist_dir.mkdir(parents=True, exist_ok=True)
    plist = plist_dir / "com.spaceduckling.space-duck-mcp.plist"
    py = sys.executable or "python3"
    plist.write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.spaceduckling.space-duck-mcp</string>
  <key>ProgramArguments</key><array>
    <string>{py}</string><string>{_script_path()}</string><string>run</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>
  <key>EnvironmentVariables</key><dict>
    <key>SPACEDUCK_MCP_PORT</key><string>{port}</string>
  </dict>
</dict></plist>
""")
    plist.chmod(0o600)
    subprocess.run(["launchctl", "unload", str(plist)], capture_output=True)
    r = subprocess.run(["launchctl", "load", str(plist)],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("launchctl load failed: " + (r.stderr or r.stdout),
              file=sys.stderr)
        return 1
    print(f"✅ launchd agent installed + started ({plist}), MCP on 127.0.0.1:{port}")
    return 0


def uninstall_service():
    if sys.platform == "darwin":
        plist = Path.home() / "Library/LaunchAgents/com.spaceduckling.space-duck-mcp.plist"
        subprocess.run(["launchctl", "unload", str(plist)], capture_output=True)
        try:
            plist.unlink()
            print("launchd agent removed")
        except FileNotFoundError:
            print("no launchd agent installed")
        return 0
    subprocess.run(["systemctl", "--user", "disable", "--now", SERVICE_NAME],
                   capture_output=True)
    unit = Path.home() / ".config/systemd/user" / (SERVICE_NAME + ".service")
    try:
        unit.unlink()
        subprocess.run(["systemctl", "--user", "daemon-reload"],
                       capture_output=True)
        print("systemd user service removed")
    except FileNotFoundError:
        print("no service installed")
    return 0


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "run"
    port = int(os.environ.get("SPACEDUCK_MCP_PORT", str(DEFAULT_PORT)))
    if cmd == "run":
        return serve(DEFAULT_HOST, port)
    if cmd == "status":
        return cmd_status(port)
    if cmd == "print-client-config":
        return cmd_print_client_config(port)
    if cmd == "install-systemd":
        return install_systemd(port)
    if cmd == "install-launchd":
        return install_launchd(port)
    if cmd == "uninstall-service":
        return uninstall_service()
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
