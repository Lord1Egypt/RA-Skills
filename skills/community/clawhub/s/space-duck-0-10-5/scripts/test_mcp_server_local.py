#!/usr/bin/env python3
"""Local unit + integration test for mcp_server.py — stdlib only.

Runs the server on an ephemeral loopback port with a stubbed upstream
(urllib.request.urlopen monkey-patched to a fake /beak router), and
proves:
  - 401 without local bearer
  - 405 on GET (single-response mode)
  - initialize / ping / tools/list shapes match hosted
  - tools/call forwards 1:1 to fake /beak and returns the upstream body
  - unknown method → -32601
  - upstream 429 passes through as JSON-RPC -32003 with retry_after_s
"""
import json
import os
import socket
import sys
import tempfile
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


# ── set env BEFORE importing mcp_server so paths/secret land in tmp ─────
_TMP = tempfile.mkdtemp(prefix="sd-mcp-test-")
os.environ["SPACEDUCK_CONFIG_DIR"] = _TMP
os.environ["SPACEDUCK_CONFIG"] = os.path.join(_TMP, "config.json")
os.environ["SPACEDUCK_ALLOW_CUSTOM_API"] = "1"  # [HARDEN-071] fake api_base below

# minimal config the server can read
_FAKE_API_BASE = "http://fake-beak.local"  # never actually contacted
with open(os.environ["SPACEDUCK_CONFIG"], "w") as f:
    json.dump({"beak_key": "bk_TEST_abcdefgh",
               "spaceduck_id": "sd_test_12345678901234567890",
               "duckling_id": "d_test_1",
               "api_base": _FAKE_API_BASE}, f)

import mcp_server  # noqa: E402


# ── fake upstream — records each request; returns canned responses ─────

_upstream_log = []
_upstream_next = {"status": 200, "body": {"ok": True}, "headers": {}}


class _FakeResp:
    def __init__(self, status, body, headers=None):
        self.status = status
        self._body = body if isinstance(body, (bytes, bytearray)) \
            else json.dumps(body).encode()
        self.headers = headers or {}

    def read(self):
        return self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def _fake_urlopen(req, timeout=None):
    url = req.full_url if hasattr(req, "full_url") else req.get_full_url()
    body_raw = req.data or b""
    try:
        body = json.loads(body_raw) if body_raw else None
    except Exception:
        body = body_raw
    _upstream_log.append({"method": req.get_method(), "url": url,
                          "body": body,
                          "auth": req.headers.get("X-beak-key")
                          or req.headers.get("X-Beak-Key")})
    st = _upstream_next["status"]
    bd = _upstream_next["body"]
    hd = _upstream_next["headers"]
    if 200 <= st < 300:
        return _FakeResp(st, bd, hd)
    raise urllib.error.HTTPError(url, st, "err", hd,
                                 __wrap_body(bd))


def __wrap_body(bd):
    import io
    raw = bd if isinstance(bd, (bytes, bytearray)) else json.dumps(bd).encode()
    return io.BytesIO(raw)


mcp_server._URLOPEN = _fake_urlopen


# ── boot the server on an ephemeral port ────────────────────────────────

def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


PORT = _free_port()
CFG = mcp_server.load_config()
SECRET = mcp_server.proxy_secret()
H = mcp_server._make_handler(CFG, SECRET)
srv = HTTPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
time.sleep(0.05)


# ── helpers ─────────────────────────────────────────────────────────────

URL = f"http://127.0.0.1:{PORT}/"


def _rpc(method, params=None, rpc_id=1, auth=True):
    body = {"jsonrpc": "2.0", "id": rpc_id, "method": method}
    if params is not None:
        body["params"] = params
    headers = {"Content-Type": "application/json"}
    if auth:
        headers["Authorization"] = "Bearer " + SECRET
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
                                 headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            j = json.loads(raw)
        except Exception:
            j = {"_raw": raw.decode("utf-8", "replace")}
        return e.code, j


def _set_upstream(status, body, headers=None):
    _upstream_next["status"] = status
    _upstream_next["body"] = body
    _upstream_next["headers"] = headers or {}
    _upstream_log.clear()


# ── tests ───────────────────────────────────────────────────────────────

results = []


def check(name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    results.append((tag, name, detail))
    print(f"  {tag}  {name}" + (f"  — {detail}" if detail and not cond else ""))


# 1) 401 without bearer
st, j = _rpc("ping", auth=False)
check("401 without bearer", st == 401 and j.get("error") == "unauthorized",
      f"got {st} {j}")

# 2) 405 on GET
try:
    req = urllib.request.Request(URL, method="GET")
    with urllib.request.urlopen(req, timeout=5) as r:
        st = r.status
        j = json.loads(r.read() or b"{}")
except urllib.error.HTTPError as e:
    st = e.code
    j = json.loads(e.read() or b"{}")
check("405 on GET", st == 405 and j.get("error") == "method_not_allowed",
      f"got {st} {j}")

# 3) initialize
st, j = _rpc("initialize", {"protocolVersion": "2025-03-26"})
res = j.get("result", {})
check("initialize protocolVersion echoed",
      st == 200 and res.get("protocolVersion") == "2025-03-26",
      f"got {j}")
check("initialize serverInfo.name = space-duck-local-mcp",
      res.get("serverInfo", {}).get("name") == "space-duck-local-mcp",
      f"got {res.get('serverInfo')}")
check("initialize serverInfo.laneA hint = true",
      res.get("serverInfo", {}).get("laneA") is True)
check("initialize capabilities.tools present",
      "tools" in (res.get("capabilities") or {}))

# initialize with unknown protocolVersion → default
st, j = _rpc("initialize", {"protocolVersion": "9999-99-99"})
check("initialize unknown proto → default 2025-03-26",
      j.get("result", {}).get("protocolVersion") == "2025-03-26")

# 4) ping
st, j = _rpc("ping")
check("ping returns empty result", st == 200 and j.get("result") == {},
      f"got {j}")

# 5) tools/list — must have 6 tools with hosted names
st, j = _rpc("tools/list")
tools = j.get("result", {}).get("tools", [])
names = [t["name"] for t in tools]
expected = ["duck_status", "list_workspace_files", "read_workspace_file",
            "send_task", "list_connections", "send_peck"]
check("tools/list returns 6 tools", len(tools) == 6, f"got {names}")
check("tools/list names match hosted", names == expected,
      f"got {names}")
check("send_peck schema has to/message required",
      any(t["name"] == "send_peck"
          and set(t["inputSchema"].get("required", [])) == {"to", "message"}
          for t in tools))

# 6) tools/call → forwards 1:1 to fake upstream, returns result
_set_upstream(200, {"spaceduck_id": "sd_test_12345678901234567890",
                    "name": "Test Duck", "status": "active"})
st, j = _rpc("tools/call", {"name": "duck_status", "arguments": {}})
res = j.get("result", {})
check("tools/call duck_status → success",
      st == 200 and res.get("isError") is False,
      f"got {j}")
check("tools/call proxied to /beak/spaceducks with POST",
      len(_upstream_log) == 1
      and _upstream_log[0]["method"] == "POST"
      and _upstream_log[0]["url"].endswith("/beak/spaceducks"),
      f"log={_upstream_log}")
check("tools/call forwards beak_key",
      _upstream_log[0]["auth"] == "bk_TEST_abcdefgh")
check("tools/call content is JSON text from upstream",
      "Test Duck" in res.get("content", [{}])[0].get("text", ""))

# read_workspace_file → POST /beak/skill/file with filename+action
_set_upstream(200, {"filename": "MEMORY.md", "content": "hello memory"})
st, j = _rpc("tools/call",
             {"name": "read_workspace_file", "arguments": {"path": "MEMORY.md"}})
check("read_workspace_file → /beak/skill/file",
      _upstream_log[-1]["url"].endswith("/beak/skill/file")
      and _upstream_log[-1]["body"] == {"filename": "MEMORY.md",
                                        "action": "read"})

# list_workspace_files → GET /beak/skill/files
_set_upstream(200, {"files": []})
st, j = _rpc("tools/call",
             {"name": "list_workspace_files", "arguments": {}})
check("list_workspace_files → GET /beak/skill/files",
      _upstream_log[-1]["method"] == "GET"
      and _upstream_log[-1]["url"].endswith("/beak/skill/files"))

# send_task → POST /beak/tg/notify with beak_key+spaceduck_id
_set_upstream(200, {"dispatched": True})
st, j = _rpc("tools/call",
             {"name": "send_task", "arguments": {"message": "audit inbox"}})
check("send_task → /beak/tg/notify",
      _upstream_log[-1]["url"].endswith("/beak/tg/notify")
      and _upstream_log[-1]["body"]["spaceduck_id"]
          == "sd_test_12345678901234567890"
      and "audit inbox" in _upstream_log[-1]["body"]["message"])

# send_peck facade over send_peck.py — stub the module functions so we can
# assert the MCP tool (a) resolves the target via resolve_target, (b) calls
# send_peck.send_peck with the resolved SDID + message + intent-as-peck_type,
# and (c) maps success / SystemExit-error / 202-pending responses honestly.
_sp_calls = []


def _fake_resolve_target(cfg, name_or_sdid):
    _sp_calls.append(("resolve_target", name_or_sdid))
    # simulate name→SDID resolution
    if name_or_sdid == "PeerDuck":
        return "ABCDEF0123456789"
    return name_or_sdid.upper()


def _make_fake_send_peck(mode):
    """mode: 'ok' | 'pending' | 'exit403' | 'exception'."""
    def _fake(cfg, target_id, message, purpose='connect', peck_type='notify',
              skip_preflight=False, tool_use=None, peck_meta=None,
              no_auto_grant=False):
        _sp_calls.append(("send_peck", target_id, message, peck_type))
        if mode == "ok":
            return {"status": "sent", "peck_id": "peck_test",
                    "channels": ["tg"], "byob_push": "ok"}
        if mode == "pending":
            return {"status": "approval_required",
                    "peck_id": "peck_test",
                    "message": "held for owner approval"}
        if mode == "exit403":
            print("ERROR: HTTP 403 — grant_required")
            raise SystemExit(1)
        if mode == "exception":
            raise RuntimeError("kaboom")
        return None
    return _fake


# Invalid intent → structured error (schema validation, no call to module)
_sp_calls.clear()
mcp_server._send_peck_mod.resolve_target = _fake_resolve_target
mcp_server._send_peck_mod.send_peck = _make_fake_send_peck("ok")
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "sd_other_id_1234567890abcd",
                            "message": "hi", "intent": "wat"}})
res = j.get("result", {})
check("send_peck invalid intent → isError",
      res.get("isError") is True
      and "invalid intent" in res.get("content", [{}])[0].get("text", ""))
check("send_peck invalid intent did NOT call module",
      _sp_calls == [], f"got {_sp_calls}")

# Missing to/message → structured error
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "", "message": ""}})
res = j.get("result", {})
check("send_peck missing to/message → isError",
      res.get("isError") is True
      and "required" in res.get("content", [{}])[0].get("text", ""))

# Happy path: name-target resolved via resolve_target, forwarded to module
_sp_calls.clear()
mcp_server._send_peck_mod.send_peck = _make_fake_send_peck("ok")
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "PeerDuck",
                            "message": "hi there",
                            "intent": "notify"}})
res = j.get("result", {})
check("send_peck ok → not isError",
      st == 200 and res.get("isError") is False, f"got {j}")
check("send_peck resolved name via resolve_target",
      any(c[0] == "resolve_target" and c[1] == "PeerDuck"
          for c in _sp_calls), f"got {_sp_calls}")
check("send_peck called module with resolved SDID + peck_type=intent",
      any(c[0] == "send_peck" and c[1] == "ABCDEF0123456789"
          and c[2] == "hi there" and c[3] == "notify"
          for c in _sp_calls), f"got {_sp_calls}")
_txt = res.get("content", [{}])[0].get("text", "")
try:
    _pl_ok = json.loads(_txt)
except Exception:
    _pl_ok = {}
check("send_peck ok body passed through honestly",
      _pl_ok.get("status") == "sent"
      and _pl_ok.get("peck_id") == "peck_test"
      and _pl_ok.get("channels") == ["tg"], f"got {_txt}")

# 202-style approval-required response → still not isError, body passed through
_sp_calls.clear()
mcp_server._send_peck_mod.send_peck = _make_fake_send_peck("pending")
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "sd_other_id_1234567890abcd",
                            "message": "hi",
                            "intent": "query"}})
res = j.get("result", {})
_txt = res.get("content", [{}])[0].get("text", "")
try:
    _pl_pending = json.loads(_txt)
except Exception:
    _pl_pending = {}
check("send_peck approval_required → not isError, body passthrough",
      res.get("isError") is False
      and _pl_pending.get("status") == "approval_required",
      f"got {j}")

# SystemExit inside send_peck (e.g. 403) → mapped to isError with captured text
_sp_calls.clear()
mcp_server._send_peck_mod.send_peck = _make_fake_send_peck("exit403")
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "sd_other_id_1234567890abcd",
                            "message": "hi", "intent": "notify"}})
res = j.get("result", {})
check("send_peck SystemExit → isError=true with printed detail",
      res.get("isError") is True
      and "403" in res.get("content", [{}])[0].get("text", ""),
      f"got {j}")

# Unexpected exception → mapped to isError, server not killed
_sp_calls.clear()
mcp_server._send_peck_mod.send_peck = _make_fake_send_peck("exception")
st, j = _rpc("tools/call",
             {"name": "send_peck",
              "arguments": {"to": "sd_other_id_1234567890abcd",
                            "message": "hi", "intent": "notify"}})
res = j.get("result", {})
check("send_peck unexpected exception → isError with type name",
      res.get("isError") is True
      and "RuntimeError" in res.get("content", [{}])[0].get("text", ""),
      f"got {j}")

# Schema no longer advertises `scopes` (aligned to local impl, which
# always signs scopes_asserted=[] and cannot forward a caller list).
st, j = _rpc("tools/list")
_sp_tool = next(t for t in j["result"]["tools"] if t["name"] == "send_peck")
check("send_peck schema drops `scopes` (Lane A divergence noted in code)",
      "scopes" not in _sp_tool["inputSchema"].get("properties", {}),
      f"got {_sp_tool['inputSchema']}")

# 7) unknown method
st, j = _rpc("does/not/exist")
check("unknown method → -32601",
      j.get("error", {}).get("code") == -32601, f"got {j}")

# 8) upstream 429 passthrough → JSON-RPC -32003 + retry_after_s
_set_upstream(429, {"error": "rate_limited", "retry_after_s": 42})
st, j = _rpc("tools/call",
             {"name": "duck_status", "arguments": {}})
err = j.get("error") or {}
check("upstream 429 → JSON-RPC -32003",
      err.get("code") == -32003, f"got {j}")
check("429 preserves retry_after_s",
      (err.get("data") or {}).get("retry_after_s") == 42, f"got {j}")

# 9) upstream non-2xx (500) → tools/call isError with upstream body
_set_upstream(500, {"error": "boom"})
st, j = _rpc("tools/call", {"name": "duck_status", "arguments": {}})
res = j.get("result", {})
check("upstream 500 → tools/call isError=true",
      res.get("isError") is True
      and "500" in res.get("content", [{}])[0].get("text", ""),
      f"got {j}")

# 10) notifications/* → 202
req = urllib.request.Request(
    URL, data=json.dumps({"jsonrpc": "2.0",
                          "method": "notifications/initialized"}).encode(),
    headers={"Content-Type": "application/json",
             "Authorization": "Bearer " + SECRET}, method="POST")
try:
    with urllib.request.urlopen(req, timeout=5) as r:
        code = r.status
except urllib.error.HTTPError as e:
    code = e.code
check("notifications/* → 202", code == 202, f"got {code}")

# ── summary ─────────────────────────────────────────────────────────────

srv.shutdown()
n_pass = sum(1 for t, *_ in results if t == "PASS")
n_fail = sum(1 for t, *_ in results if t == "FAIL")
print(f"\n{n_pass} passed, {n_fail} failed, {len(results)} total")
sys.exit(0 if n_fail == 0 else 1)
