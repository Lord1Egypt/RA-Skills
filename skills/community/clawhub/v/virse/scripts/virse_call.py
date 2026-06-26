#!/usr/bin/env python3
"""Lightweight MCP client for Virse — zero external dependencies.

Usage:
    python3 virse_call.py call <tool_name> '<json_args>'
    python3 virse_call.py batch '<json_array_of_calls>'
    python3 virse_call.py list-tools
    python3 virse_call.py save-key <api_key>
    python3 virse_call.py login
    python3 virse_call.py login-poll <device_code>
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_BASE_URL = "https://dev.virse.ai"
TOKEN_PATH = os.path.expanduser("~/.virse/token")
PROTOCOL_VERSION = "2025-03-26"


def _read_token():
    """Read token: VIRSE_API_KEY env > ~/.virse/token file."""
    token = os.environ.get("VIRSE_API_KEY", "").strip()
    if token:
        return token
    try:
        with open(TOKEN_PATH, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def _base_url():
    return os.environ.get("VIRSE_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


def _extract_error_message(error_value):
    """Safely extract message from a JSON-RPC error (dict or string)."""
    if isinstance(error_value, dict):
        return error_value.get("message", json.dumps(error_value))
    return str(error_value)


def _parse_sse(raw):
    """Parse SSE text and return the last JSON-RPC message found."""
    result = {}
    for line in raw.splitlines():
        if line.startswith("data:"):
            data_str = line[len("data:"):].strip()
            if data_str:
                try:
                    result = json.loads(data_str)
                except (json.JSONDecodeError, ValueError):
                    pass
    return result


class MCPError(Exception):
    """Raised when an HTTP request to the MCP server fails."""
    pass


def _http_post(url, headers, body):
    """POST JSON, return (response_headers, parsed_json). Raises MCPError on failure."""
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=60)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        raise MCPError(f"HTTP {e.code}: {err_body}")
    except urllib.error.URLError as e:
        raise MCPError(f"Connection error: {e.reason}")
    resp_body = resp.read().decode("utf-8")
    content_type = resp.headers.get("Content-Type", "")
    if "text/event-stream" in content_type:
        return resp.headers, _parse_sse(resp_body)
    return resp.headers, json.loads(resp_body) if resp_body else {}


def _init_session(endpoint, headers):
    """Run MCP initialize + notification handshake. Returns session_id.

    Raises MCPError on connection/protocol failure.
    """
    init_body = {
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "virse-skill", "version": "0.1.0"},
        },
    }
    resp_headers, init_result = _http_post(endpoint, headers, init_body)

    if init_result.get("error"):
        msg = _extract_error_message(init_result["error"])
        raise MCPError(f"MCP init error: {msg}")

    session_id = resp_headers.get("mcp-session-id") or ""

    # Send initialized notification
    notify_headers = dict(headers)
    if session_id:
        notify_headers["mcp-session-id"] = session_id
    _http_post(endpoint, notify_headers, {
        "jsonrpc": "2.0", "method": "notifications/initialized", "params": {},
    })

    return session_id


def call_tool(name, args_json):
    base = _base_url()
    token = _read_token()
    endpoint = f"{base}/mcp"

    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream;q=0.9"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        session_id = _init_session(endpoint, headers)
    except MCPError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    # Call tool
    call_headers = dict(headers)
    if session_id:
        call_headers["mcp-session-id"] = session_id

    args = json.loads(args_json) if isinstance(args_json, str) else args_json
    call_body = {
        "jsonrpc": "2.0", "id": 2, "method": "tools/call",
        "params": {"name": name, "arguments": args},
    }
    try:
        _, result = _http_post(endpoint, call_headers, call_body)
    except MCPError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if result.get("error"):
        msg = _extract_error_message(result["error"])
        print(f"Tool error: {msg}", file=sys.stderr)
        sys.exit(1)

    # Extract text content
    content = result.get("result", {}).get("content", [])
    for part in content:
        if part.get("type") == "text":
            print(part["text"])


def batch_call(calls_json):
    """Execute multiple tool calls in a single MCP session.

    calls_json: JSON array like [{"name": "tool_name", "args": {...}}, ...]
    Reuses one session for all calls, with 0.5s throttle between each.
    """
    calls = json.loads(calls_json) if isinstance(calls_json, str) else calls_json
    if not isinstance(calls, list) or not calls:
        print("batch expects a non-empty JSON array of {name, args} objects", file=sys.stderr)
        sys.exit(1)

    base = _base_url()
    token = _read_token()
    endpoint = f"{base}/mcp"

    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream;q=0.9"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        session_id = _init_session(endpoint, headers)
    except MCPError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    call_headers = dict(headers)
    if session_id:
        call_headers["mcp-session-id"] = session_id

    results = []
    for i, call in enumerate(calls):
        name = call.get("name", "")
        args = call.get("args", {})
        if not name:
            print(f"[{i}] Skipped: missing 'name'", file=sys.stderr)
            results.append({"index": i, "error": "missing name"})
            continue

        call_body = {
            "jsonrpc": "2.0", "id": i + 2, "method": "tools/call",
            "params": {"name": name, "arguments": args},
        }

        try:
            _, result = _http_post(endpoint, call_headers, call_body)
        except MCPError as e:
            print(f"[{i}] {name}: {e}", file=sys.stderr)
            results.append({"index": i, "name": name, "error": str(e)})
            if i < len(calls) - 1:
                time.sleep(0.5)
            continue

        if result.get("error"):
            msg = _extract_error_message(result["error"])
            print(f"[{i}] {name}: error — {msg}", file=sys.stderr)
            results.append({"index": i, "name": name, "error": msg})
        else:
            content = result.get("result", {}).get("content", [])
            texts = [p["text"] for p in content if p.get("type") == "text"]
            output = "\n".join(texts)
            print(f"[{i}] {name}: OK")
            print(output)
            results.append({"index": i, "name": name, "ok": True})

        # Throttle between calls
        if i < len(calls) - 1:
            time.sleep(0.5)

    # Summary
    ok_count = sum(1 for r in results if r.get("ok"))
    fail_count = len(results) - ok_count
    print(f"\n--- batch complete: {ok_count} succeeded, {fail_count} failed ---", file=sys.stderr)


def list_tools():
    base = _base_url()
    token = _read_token()
    endpoint = f"{base}/mcp"

    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream;q=0.9"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        session_id = _init_session(endpoint, headers)
    except MCPError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    # List tools
    list_headers = dict(headers)
    if session_id:
        list_headers["mcp-session-id"] = session_id
    try:
        _, result = _http_post(endpoint, list_headers, {
            "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
        })
    except MCPError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    if result.get("error"):
        msg = _extract_error_message(result["error"])
        print(f"Error: {msg}", file=sys.stderr)
        sys.exit(1)

    tools = result.get("result", {}).get("tools", [])
    for t in tools:
        print(f"  {t['name']:30s} {t.get('description', '')}")


def _http_post_form(url, data):
    """POST form-urlencoded (for OAuth endpoints, not JSON).
    Returns (status_code, parsed_json_body).
    """
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(
        url, data=encoded, method="POST",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        body = resp.read().decode("utf-8")
        return resp.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            return e.code, json.loads(body)
        except (json.JSONDecodeError, ValueError):
            return e.code, {"error": "http_error", "error_description": body}
    except urllib.error.URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def login():
    """Start Device Flow: POST /device/code, print JSON, exit immediately."""
    base = _base_url()
    status, result = _http_post_form(f"{base}/device/code", {"client_id": "virse-skill"})
    if status >= 400 or "error" in result:
        desc = result.get("error_description", result.get("error", f"HTTP {status}"))
        print(f"Device code request failed: {desc}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps({
        "verification_url": result.get("verification_uri_complete", result.get("verification_uri", "")),
        "user_code": result.get("user_code", ""),
        "device_code": result.get("device_code", ""),
        "expires_in": result.get("expires_in", 300),
    }))


def login_poll(device_code):
    """Poll /device/token until user completes login, then save token."""
    base = _base_url()
    interval = 5
    for _ in range(24):  # up to 2 minutes
        status, result = _http_post_form(f"{base}/device/token", {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": device_code,
            "client_id": "virse-skill",
        })
        if "access_token" in result:
            save_key(result["access_token"])
            print("Login successful!")
            return
        error = result.get("error", "")
        if error == "authorization_pending":
            time.sleep(interval)
            continue
        if error == "slow_down":
            interval += 5
            time.sleep(interval)
            continue
        # Any other error is fatal
        desc = result.get("error_description", error or f"HTTP {status}")
        print(f"Login failed: {desc}", file=sys.stderr)
        sys.exit(1)
    print("Login timed out (2 min)", file=sys.stderr)
    sys.exit(1)


def save_key(key):
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        f.write(key)
    os.chmod(TOKEN_PATH, 0o600)
    print(f"Token saved to {TOKEN_PATH}")


def main():
    if len(sys.argv) < 2:
        print((__doc__ or "").strip())
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "call":
        if len(sys.argv) < 4:
            print("Usage: virse_call.py call <tool_name> '<json_args>'", file=sys.stderr)
            sys.exit(1)
        call_tool(sys.argv[2], sys.argv[3])
    elif cmd == "batch":
        if len(sys.argv) < 3:
            print("Usage: virse_call.py batch '<json_array>'", file=sys.stderr)
            sys.exit(1)
        batch_call(sys.argv[2])
    elif cmd == "list-tools":
        list_tools()
    elif cmd == "login":
        login()
    elif cmd == "login-poll":
        if len(sys.argv) < 3:
            print("Usage: virse_call.py login-poll <device_code>", file=sys.stderr)
            sys.exit(1)
        login_poll(sys.argv[2])
    elif cmd == "save-key":
        if len(sys.argv) < 3:
            print("Usage: virse_call.py save-key <api_key>", file=sys.stderr)
            sys.exit(1)
        save_key(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
