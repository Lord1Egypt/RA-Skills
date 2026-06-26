"""
Videoinu Skill - Common utilities.

Provides authentication, HTTP helpers, and a minimal WebSocket client
using only Python standard library.
"""

import json
import os
import sys
import ssl
import socket
import hashlib
import base64
import struct
import urllib.request
import urllib.error
import urllib.parse
from uuid import uuid4

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = os.environ.get("VIDEOINU_API_BASE", "https://videoinu.com").rstrip("/")

# Token resolution order: env var > credentials file
_CREDENTIALS_PATH = os.path.join(os.path.expanduser("~"), ".videoinu", "credentials.json")

def _load_access_key() -> str:
    # 1. Environment variable (highest priority)
    env_key = os.environ.get("VIDEOINU_ACCESS_KEY", "")
    if env_key:
        return env_key
    # 2. Credentials file
    if os.path.isfile(_CREDENTIALS_PATH):
        try:
            with open(_CREDENTIALS_PATH) as f:
                return json.load(f).get("access_key", "")
        except (json.JSONDecodeError, OSError):
            pass
    return ""

ACCESS_KEY = _load_access_key()

# Derived
GO_API_PREFIX = f"{BASE_URL}/api/backend"
AGENT_API_PREFIX = f"{BASE_URL}/api/agent"

def require_access_key():
    if not ACCESS_KEY:
        print(
            json.dumps(
                {
                    "error": "VIDEOINU_ACCESS_KEY is not set. "
                    "Run: export VIDEOINU_ACCESS_KEY=\"your-access-key\" "
                    "(get it from Profile -> Copy Access Key on videoinu.com)"
                }
            )
        )
        sys.exit(1)


def build_graph_url(graph_id: str) -> str:
    return f"{BASE_URL}/nova/project/{graph_id}"


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def _cookie_header() -> str:
    return f"token={ACCESS_KEY}"


def _base_headers() -> dict:
    return {
        "Cookie": _cookie_header(),
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }


def api_get(path: str, base: str | None = None, params: dict | None = None) -> dict:
    """GET request. Returns the `data` field from the standard response envelope."""
    url = f"{base or GO_API_PREFIX}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_base_headers(), method="GET")
    return _do_request(req)


def api_post(path: str, body: dict | None = None, base: str | None = None) -> dict:
    """POST request. Returns the `data` field from the standard response envelope."""
    url = f"{base or GO_API_PREFIX}{path}"
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(url, data=data, headers=_base_headers(), method="POST")
    return _do_request(req)


def api_put(path: str, body: dict | None = None, base: str | None = None) -> dict:
    url = f"{base or GO_API_PREFIX}{path}"
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(url, data=data, headers=_base_headers(), method="PUT")
    return _do_request(req)


def api_delete(path: str, base: str | None = None) -> dict:
    url = f"{base or GO_API_PREFIX}{path}"
    req = urllib.request.Request(url, headers=_base_headers(), method="DELETE")
    return _do_request(req)


def _do_request(req: urllib.request.Request, timeout: int = 30) -> dict:
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(json.dumps({"error": f"HTTP {e.code}: {error_body}"}))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"error": f"Connection error: {e.reason}"}))
        sys.exit(1)

    if body.get("err_code", 0) != 0:
        print(
            json.dumps(
                {"error": f"API error {body.get('err_code')}: {body.get('err_msg', 'Unknown')}"}
            )
        )
        sys.exit(1)

    return body.get("data")


def upload_raw(upload_url: str, file_bytes: bytes, content_type: str, timeout: int = 120):
    """PUT raw bytes to a pre-signed URL."""
    req = urllib.request.Request(
        upload_url,
        data=file_bytes,
        headers={
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        },
        method="PUT",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status >= 400:
            raise RuntimeError(f"Upload failed with status {resp.status}")


# ---------------------------------------------------------------------------
# Minimal WebSocket client (RFC 6455, text frames only, standard library)
# ---------------------------------------------------------------------------

class SimpleWebSocket:
    """
    Minimal blocking WebSocket client for agent chat.
    Supports text frames, ping/pong, close. No extensions or compression.
    """

    def __init__(self, url: str, extra_headers: dict | None = None):
        self.url = url
        self.extra_headers = extra_headers or {}
        self._sock: socket.socket | None = None
        self._closed = False

    def connect(self):
        parsed = urllib.parse.urlparse(self.url)
        is_ssl = parsed.scheme == "wss"
        host = parsed.hostname
        port = parsed.port or (443 if is_ssl else 80)
        path = parsed.path
        if parsed.query:
            path += "?" + parsed.query

        # TCP connect
        sock = socket.create_connection((host, port), timeout=30)
        if is_ssl:
            ctx = ssl.create_default_context()
            sock = ctx.wrap_socket(sock, server_hostname=host)
        self._sock = sock

        # WebSocket handshake
        ws_key = base64.b64encode(os.urandom(16)).decode()
        lines = [
            f"GET {path} HTTP/1.1",
            f"Host: {host}",
            "Upgrade: websocket",
            "Connection: Upgrade",
            f"Sec-WebSocket-Key: {ws_key}",
            "Sec-WebSocket-Version: 13",
        ]
        # Auth via cookie
        lines.append(f"Cookie: {_cookie_header()}")
        lines.append("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        for k, v in self.extra_headers.items():
            lines.append(f"{k}: {v}")
        lines.append("")
        lines.append("")
        sock.sendall("\r\n".join(lines).encode())

        # Read response
        resp = b""
        while b"\r\n\r\n" not in resp:
            chunk = sock.recv(4096)
            if not chunk:
                raise ConnectionError("Connection closed during handshake")
            resp += chunk

        status_line = resp.split(b"\r\n")[0].decode()
        if "101" not in status_line:
            raise ConnectionError(f"WebSocket handshake failed: {status_line}")

    def send(self, text: str):
        """Send a text frame."""
        payload = text.encode("utf-8")
        self._send_frame(0x1, payload)

    def recv(self, timeout: float | None = None) -> str | None:
        """
        Receive one text frame. Returns None on close.
        Automatically responds to ping with pong.
        """
        if self._closed:
            return None
        if timeout is not None:
            self._sock.settimeout(timeout)
        try:
            while True:
                opcode, data = self._read_frame()
                if opcode == 0x1:  # text
                    return data.decode("utf-8")
                elif opcode == 0x9:  # ping
                    self._send_frame(0xA, data)  # pong
                elif opcode == 0x8:  # close
                    self._closed = True
                    try:
                        self._send_frame(0x8, data)
                    except Exception:
                        pass
                    return None
                # ignore other opcodes (binary, continuation)
        except socket.timeout:
            return None
        except (ConnectionError, OSError):
            self._closed = True
            return None

    def close(self):
        if self._sock and not self._closed:
            try:
                self._send_frame(0x8, b"")
            except Exception:
                pass
            self._closed = True
            self._sock.close()

    # --- internal ---

    def _send_frame(self, opcode: int, payload: bytes):
        header = bytearray()
        header.append(0x80 | opcode)  # FIN + opcode
        mask_key = os.urandom(4)
        length = len(payload)
        if length < 126:
            header.append(0x80 | length)  # MASK bit set
        elif length < 65536:
            header.append(0x80 | 126)
            header += struct.pack("!H", length)
        else:
            header.append(0x80 | 127)
            header += struct.pack("!Q", length)
        header += mask_key
        # mask payload
        masked = bytearray(length)
        for i in range(length):
            masked[i] = payload[i] ^ mask_key[i % 4]
        self._sock.sendall(bytes(header) + bytes(masked))

    def _read_frame(self) -> tuple:
        def _recv_exact(n):
            buf = b""
            while len(buf) < n:
                chunk = self._sock.recv(n - len(buf))
                if not chunk:
                    raise ConnectionError("Connection closed")
                buf += chunk
            return buf

        head = _recv_exact(2)
        opcode = head[0] & 0x0F
        masked = bool(head[1] & 0x80)
        length = head[1] & 0x7F

        if length == 126:
            length = struct.unpack("!H", _recv_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", _recv_exact(8))[0]

        if masked:
            mask_key = _recv_exact(4)
            data = bytearray(_recv_exact(length))
            for i in range(length):
                data[i] ^= mask_key[i % 4]
            data = bytes(data)
        else:
            data = _recv_exact(length)

        return opcode, data


def create_ws(session_id: str) -> SimpleWebSocket:
    """Create a WebSocket connection for an agent session."""
    parsed = urllib.parse.urlparse(BASE_URL)
    scheme = "wss" if parsed.scheme == "https" else "ws"
    host = parsed.netloc
    trace_id = str(uuid4())
    ws_url = f"{scheme}://{host}/api/agent/sessions/{session_id}/stream?trace_id={trace_id}"
    ws = SimpleWebSocket(ws_url)
    ws.connect()
    return ws
