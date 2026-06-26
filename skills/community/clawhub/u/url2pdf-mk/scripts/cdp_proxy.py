#!/usr/bin/env python3
"""
CDP Proxy — 常驻进程，复用单一 WebSocket 连接到 Chrome。

**解决的核心问题**：Chrome 136+ 的 ``chrome://inspect`` WS-only 模式下，
每个新的 WebSocket 连接都会触发一次 "要允许远程调试吗？" 弹窗。
CDP Proxy 保持**唯一一个** WS 连接到 Chrome，并向下游脚本暴露
标准的 HTTP + WS CDP 接口，从而让用户只需点击**一次** "允许"。
"""
from __future__ import annotations

import os, sys, argparse, atexit, base64, hashlib, json, secrets, signal, socket
import struct, tempfile, threading, time, getpass
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import URLError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _encoding_fix  # noqa: F401

DEFAULT_CHROME_PORT = 9222
DEFAULT_PROXY_PORT  = 9223

PROXY_STATE_DIR  = os.path.join(tempfile.gettempdir(), f'cdp-proxy-{getpass.getuser()}')
PROXY_PID_FILE   = os.path.join(PROXY_STATE_DIR, 'proxy.pid')
PROXY_STATE_FILE = os.path.join(PROXY_STATE_DIR, 'proxy.json')
RECONNECT_INTERVAL_S  = 2.0
RECONNECT_MAX_RETRIES = 30

WS_FIN_TEXT  = 0x81
WS_FIN_CLOSE = 0x88
WS_FIN_PING  = 0x89
WS_FIN_PONG  = 0x8A


def _log(msg: str):
    ts = time.strftime('%H:%M:%S')
    print(f"[cdp-proxy {ts}] {msg}", file=sys.stderr, flush=True)


def _ws_handshake_request(host: str, port: int, path: str):
    ws_key = base64.b64encode(os.urandom(16)).decode()
    req = (
        f'GET {path} HTTP/1.1\r\n'
        f'Host: {host}:{port}\r\n'
        'Upgrade: websocket\r\n'
        'Connection: Upgrade\r\n'
        f'Sec-WebSocket-Key: {ws_key}\r\n'
        'Sec-WebSocket-Version: 13\r\n'
        '\r\n'
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(120)
    sock.connect((host, port))
    sock.sendall(req.encode())
    buf = b''
    while b'\r\n\r\n' not in buf:
        chunk = sock.recv(4096)
        if not chunk:
            sock.close()
            raise ConnectionError("Connection closed during handshake")
        buf += chunk
    header_text = buf.split(b'\r\n\r\n')[0].decode('utf-8', errors='replace')
    if '101' not in header_text:
        sock.close()
        raise ConnectionError(f"WS handshake failed: {header_text[:200]}")
    remainder = buf.split(b'\r\n\r\n', 1)[1]
    return sock, remainder


def _ws_send_frame(sock, payload, opcode=0x01, masked=True):
    frame = bytearray()
    frame.append(0x80 | opcode)
    mask_bit = 0x80 if masked else 0x00
    length = len(payload)
    if length < 126:
        frame.append(mask_bit | length)
    elif length < 65536:
        frame.append(mask_bit | 126)
        frame.extend(struct.pack('>H', length))
    else:
        frame.append(mask_bit | 127)
        frame.extend(struct.pack('>Q', length))
    if masked:
        mask_key = os.urandom(4)
        frame.extend(mask_key)
        frame.extend(bytearray(b ^ mask_key[i % 4] for i, b in enumerate(payload)))
    else:
        frame.extend(payload)
    sock.sendall(bytes(frame))


def _ws_recv_frame(sock, buf):
    def _ensure(n):
        nonlocal buf
        while len(buf) < n:
            chunk = sock.recv(65536)
            if not chunk:
                raise ConnectionError("WS connection closed")
            buf.extend(chunk)
    _ensure(2)
    b0, b1 = buf[0], buf[1]
    opcode  = b0 & 0x0F
    is_masked = (b1 & 0x80) != 0
    length  = b1 & 0x7F
    offset  = 2
    if length == 126:
        _ensure(offset + 2)
        length = struct.unpack('>H', bytes(buf[offset:offset+2]))[0]; offset += 2
    elif length == 127:
        _ensure(offset + 8)
        length = struct.unpack('>Q', bytes(buf[offset:offset+8]))[0]; offset += 8
    if is_masked:
        _ensure(offset + 4)
        mask = bytes(buf[offset:offset+4]); offset += 4
    _ensure(offset + length)
    data = bytes(buf[offset:offset+length])
    if is_masked:
        data = bytes(b ^ mask[i % 4] for i, b in enumerate(data))
    remaining = bytearray(buf[offset+length:])
    return opcode, data, remaining


class ChromeUpstream:
    def __init__(self, host, port):
        self.host = host; self.port = port
        self._sock = None; self._send_lock = threading.Lock()
        self._state_lock = threading.Lock(); self._recv_buf = bytearray()
        self._closed = False; self._recv_thread = None
        self._on_message = None; self._on_disconnect = None
        self._version_info = None
        self._pending_lock = threading.Lock(); self._pending = {}

    def connect(self, timeout=120.0):
        with self._state_lock:
            if self._sock:
                try: self._sock.close()
                except OSError: pass
                self._sock = None
        try:
            sock, remainder = _ws_handshake_request(self.host, self.port, '/devtools/browser')
            with self._state_lock:
                self._sock = sock; self._recv_buf = bytearray(remainder); self._closed = False
            self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True, name='chrome-upstream-recv')
            self._recv_thread.start()
            self._fetch_version_info()
            return True
        except (OSError, ConnectionError) as e:
            _log(f"Failed to connect to Chrome at {self.host}:{self.port}: {e}")
            return False

    def adopt_socket(self, sock):
        with self._state_lock:
            if self._sock:
                try: self._sock.close()
                except OSError: pass
            self._sock = sock; self._recv_buf = bytearray(); self._closed = False
        self._recv_thread = threading.Thread(target=self._recv_loop, daemon=True, name='chrome-upstream-recv')
        self._recv_thread.start()
        self._fetch_version_info()
        return self._version_info is not None

    def _fetch_version_info(self):
        try:
            result = self.send_and_wait({'id': -1, 'method': 'Browser.getVersion'}, timeout=5.0)
            if result and 'result' in result:
                self._version_info = result['result']
        except Exception: pass

    @property
    def connected(self): return self._sock is not None and not self._closed
    @property
    def version_info(self): return self._version_info or {}

    def send(self, data):
        with self._send_lock:
            with self._state_lock:
                sock = self._sock; closed = self._closed
            if not sock or closed: raise ConnectionError("Not connected to Chrome")
            _ws_send_frame(sock, data, opcode=0x01, masked=True)

    def send_and_wait(self, msg, timeout=30.0):
        msg_id = msg.get('id', -1)
        event = threading.Event(); result_holder = [None]
        with self._pending_lock: self._pending[msg_id] = (event, result_holder)
        try:
            self.send(json.dumps(msg).encode())
            event.wait(timeout=timeout)
            return result_holder[0]
        finally:
            with self._pending_lock: self._pending.pop(msg_id, None)

    def set_on_message(self, cb): self._on_message = cb
    def set_on_disconnect(self, cb): self._on_disconnect = cb

    def close(self):
        self._closed = True
        with self._state_lock:
            if self._sock:
                try: self._sock.close()
                except OSError: pass
                self._sock = None

    def _dispatch_message(self, text):
        try: data = json.loads(text)
        except: self._on_message and self._on_message(text); return
        msg_id = data.get('id')
        if msg_id is not None:
            with self._pending_lock:
                pending = self._pending.get(msg_id)
            if pending:
                event, result_holder = pending
                result_holder[0] = data; event.set(); return
        if self._on_message: self._on_message(text)

    def _recv_loop(self):
        while not self._closed:
            try:
                with self._state_lock: sock = self._sock; buf = self._recv_buf
                if not sock: break
                sock.settimeout(1.0)
                try: chunk = sock.recv(65536)
                except socket.timeout: continue
                if not chunk: break
                buf.extend(chunk)
                while True:
                    try:
                        opcode, payload, remaining = _ws_recv_frame(sock, buf)
                        with self._state_lock: self._recv_buf = remaining
                        buf = remaining
                        if opcode == 0x01:
                            text = payload.decode('utf-8', errors='replace')
                            try: self._dispatch_message(text)
                            except Exception: pass
                        elif opcode == 0x08:
                            self._closed = True; return
                        elif opcode == 0x09:
                            with self._send_lock:
                                with self._state_lock: s = self._sock
                                if s: _ws_send_frame(s, payload, opcode=0x0A, masked=True)
                    except (ConnectionError, struct.error): break
                    except (TimeoutError, socket.timeout): break
            except (OSError, ConnectionError): break
        self._closed = True
        if self._on_disconnect:
            try: self._on_disconnect()
            except Exception: pass


class DownstreamClient:
    def __init__(self, sock, addr, client_id):
        self.sock = sock; self.addr = addr; self.client_id = client_id
        self._recv_buf = bytearray(); self._closed = False; self._lock = threading.Lock()

    def send_text(self, text):
        with self._lock:
            if self._closed: return
            try: _ws_send_frame(self.sock, text.encode(), opcode=0x01, masked=False)
            except (OSError, BrokenPipeError): self._closed = True

    def close(self):
        self._closed = True
        try: self.sock.close()
        except OSError: pass


class CDPProxy:
    def __init__(self, chrome_host='127.0.0.1', chrome_port=DEFAULT_CHROME_PORT, proxy_port=DEFAULT_PROXY_PORT):
        self._auth_token = secrets.token_urlsafe(32)
        self.chrome_host = chrome_host; self.chrome_port = chrome_port; self.proxy_port = proxy_port
        self._upstream = ChromeUpstream(chrome_host, chrome_port)
        self._downstream_clients = {}; self._client_counter = 0; self._lock = threading.Lock(); self._running = False
        self._id_offset = 0; self._id_map = {}
        self._session_map = {}; self._http_server = None
        self._disconnect_timer = None; self._disconnect_timeout_s = 60

    def start(self, block=True, auth_sock=None):
        _log(f"Starting CDP Proxy: Chrome={self.chrome_host}:{self.chrome_port}, Proxy=127.0.0.1:{self.proxy_port}")
        self._running = True
        if not self._connect_upstream(auth_sock=auth_sock):
            _log("Failed to connect to Chrome. Will retry in background.")
        ws_thread = threading.Thread(target=self._ws_accept_loop, daemon=True, name='proxy-ws-accept')
        ws_thread.start()
        self._write_state()
        _log(f"CDP Proxy ready on port {self.proxy_port}")
        if block:
            try:
                while self._running: time.sleep(1)
            except KeyboardInterrupt:
                _log("Interrupted, stopping...")
            finally: self.stop()

    def stop(self):
        self._running = False
        self._cancel_disconnect_timer()
        with self._lock:
            for c in self._downstream_clients.values(): c.close()
            self._downstream_clients.clear()
        self._upstream.close()
        if self._http_server:
            try: self._http_server.shutdown()
            except Exception: pass
        self._cleanup_state()
        _log("CDP Proxy stopped.")

    def _connect_upstream(self, auth_sock=None):
        if auth_sock:
            if self._upstream.adopt_socket(auth_sock):
                self._upstream.set_on_message(self._on_upstream_message)
                self._upstream.set_on_disconnect(self._on_upstream_disconnect)
                self._cancel_disconnect_timer()
                _log("Adopted authenticated socket to Chrome CDP (no new dialog).")
                return True
            else:
                _log("Failed to adopt authenticated socket, falling back to new connection.")
        for attempt in range(RECONNECT_MAX_RETRIES):
            if not self._running: return False
            if self._upstream.connect():
                self._upstream.set_on_message(self._on_upstream_message)
                self._upstream.set_on_disconnect(self._on_upstream_disconnect)
                self._cancel_disconnect_timer()
                _log("Connected to Chrome CDP.")
                return True
            if attempt < RECONNECT_MAX_RETRIES - 1: time.sleep(RECONNECT_INTERVAL_S)
        return False

    def _on_upstream_message(self, text):
        try: msg = json.loads(text)
        except: return
        if 'id' in msg:
            global_id = msg['id']
            with self._lock: mapping = self._id_map.pop(global_id, None)
            if mapping:
                client_id, original_id = mapping; msg['id'] = original_id
                with self._lock: client = self._downstream_clients.get(client_id)
                if client:
                    client.send_text(json.dumps(msg))
                    result = msg.get('result', {})
                    if 'sessionId' in result:
                        with self._lock: self._session_map[result['sessionId']] = client_id
        elif 'method' in msg:
            session_id = msg.get('sessionId')
            if session_id:
                with self._lock: client_id = self._session_map.get(session_id); client = self._downstream_clients.get(client_id) if client_id else None
                if client: client.send_text(text)
            else:
                with self._lock: clients = list(self._downstream_clients.values())
                for c in clients: c.send_text(text)

    def _ws_accept_loop(self):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.settimeout(1.0)
        server_sock.bind(('127.0.0.1', self.proxy_port))
        server_sock.listen(16)
        while self._running:
            try: client_sock, addr = server_sock.accept()
            except socket.timeout: continue
            except OSError: break
            threading.Thread(target=self._handle_ws_upgrade, args=(client_sock, addr), daemon=True).start()
        server_sock.close()

    def _handle_ws_upgrade(self, sock, addr):
        client_id = -1
        try:
            sock.settimeout(10); buf = b''
            while b'\r\n\r\n' not in buf:
                chunk = sock.recv(4096)
                if not chunk: sock.close(); return
                buf += chunk
            header_text = buf.decode('utf-8', errors='replace')
            if 'upgrade: websocket' not in header_text.lower():
                self._handle_http_on_ws_port(sock, header_text); return
            for line in header_text.split('\r\n'):
                if line.lower().startswith('origin:'):
                    origin = line.split(':', 1)[1].strip().lower()
                    allowed = {'http://127.0.0.1', 'http://localhost', 'https://127.0.0.1', 'https://localhost'}
                    if origin and not any(origin.startswith(ao) for ao in allowed):
                        _log(f"Rejected WS from non-localhost origin: {origin}"); sock.close(); return
                    break
            first_line = header_text.split('\r\n')[0]
            request_path = first_line.split()[1] if len(first_line.split()) >= 2 else ''
            token_valid = False
            if '?token=' in request_path:
                from urllib.parse import urlparse, parse_qs
                parsed = urlparse(request_path)
                token_param = parse_qs(parsed.query).get('token', [None])[0]
                if token_param == self._auth_token: token_valid = True
            if not token_valid:
                _log(f"Rejected WS from {addr}: invalid or missing token")
                try: sock.sendall(b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
                except OSError: pass
                sock.close(); return
            ws_key = None
            for line in header_text.split('\r\n'):
                if line.lower().startswith('sec-websocket-key:'):
                    ws_key = line.split(':', 1)[1].strip(); break
            if not ws_key: sock.close(); return
            accept_key = base64.b64encode(
                hashlib.sha1((ws_key + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()
            ).decode()
            response = (f'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: {accept_key}\r\n\r\n')
            sock.sendall(response.encode())
            with self._lock: self._client_counter += 1; client_id = self._client_counter
            client = DownstreamClient(sock, addr, client_id)
            with self._lock: self._downstream_clients[client_id] = client
            _log(f"Downstream client #{client_id} connected from {addr}")
            recv_buf = bytearray(buf.split(b'\r\n\r\n', 1)[1])
            sock.settimeout(1.0)
            while self._running and not client._closed:
                try: chunk = sock.recv(65536)
                except socket.timeout: continue
                except OSError: break
                if not chunk: break
                recv_buf.extend(chunk)
                while True:
                    try:
                        opcode, payload, recv_buf = _ws_recv_frame(sock, recv_buf)
                        if opcode == 0x01: self._forward_downstream_to_upstream(client_id, payload)
                        elif opcode == 0x08: break
                        elif opcode == 0x09: _ws_send_frame(sock, payload, opcode=0x0A, masked=False)
                    except (ConnectionError, struct.error): break
                    except (TimeoutError, socket.timeout): break
        except (OSError, ConnectionError): pass
        finally:
            with self._lock:
                removed = self._downstream_clients.pop(client_id, None)
                if removed:
                    to_remove = [sid for sid, cid in self._session_map.items() if cid == client_id]
                    for sid in to_remove: self._session_map.pop(sid, None)
            if removed: _log(f"Downstream client #{removed.client_id} disconnected")
            try: sock.close()
            except OSError: pass

    def _forward_downstream_to_upstream(self, client_id, payload):
        try: text = payload.decode('utf-8', errors='replace'); msg = json.loads(text)
        except: return
        if 'id' in msg:
            original_id = msg['id']
            with self._lock: self._id_offset += 1; global_id = self._id_offset; self._id_map[global_id] = (client_id, original_id)
            msg['id'] = global_id
        session_id = msg.get('sessionId')
        if session_id:
            with self._lock: self._session_map[session_id] = client_id
        try: self._upstream.send(json.dumps(msg).encode())
        except ConnectionError:
            _log("Upstream disconnected, attempting reconnect...")
            threading.Thread(target=self._reconnect_upstream, daemon=True).start()

    def _reconnect_upstream(self):
        if self._connect_upstream(): _log("Reconnected to Chrome.")
        else:
            _log("Failed to reconnect to Chrome after retries.")
            self._start_disconnect_timer()

    def _on_upstream_disconnect(self):
        if not self._running: return
        _log(f"Upstream WS disconnected. Will auto-exit in {self._disconnect_timeout_s}s unless reconnected.")
        self._start_disconnect_timer()

    def _start_disconnect_timer(self):
        self._cancel_disconnect_timer()
        timer = threading.Timer(self._disconnect_timeout_s, self._auto_exit_on_disconnect)
        timer.daemon = True; timer.name = 'proxy-disconnect-timer'
        self._disconnect_timer = timer; timer.start()

    def _cancel_disconnect_timer(self):
        t = self._disconnect_timer
        if t is not None: t.cancel(); self._disconnect_timer = None

    def _auto_exit_on_disconnect(self):
        if not self._running: return
        if self._upstream.connected:
            _log("Upstream reconnected before auto-exit timer fired. Staying alive."); return
        _log(f"Upstream WS disconnected for {self._disconnect_timeout_s}s. Auto-stopping proxy."); self.stop()

    def _handle_http_on_ws_port(self, sock, header_text):
        try:
            first_line = header_text.split('\r\n')[0]
            parts = first_line.split()
            if len(parts) < 2: sock.close(); return
            method, path = parts[0], parts[1]
            response_body = self._handle_json_endpoint(path)
            if response_body is not None:
                body_bytes = response_body.encode('utf-8')
                response = (f'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\nContent-Length: {len(body_bytes)}\r\nConnection: close\r\n\r\n')
                sock.sendall(response.encode() + body_bytes)
            else:
                sock.sendall(b'HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n')
        except (OSError, BrokenPipeError): pass
        finally:
            try: sock.close()
            except OSError: pass

    def _handle_json_endpoint(self, path):
        if path == '/json/version':
            info = dict(self._upstream.version_info)
            info['webSocketDebuggerUrl'] = f'ws://127.0.0.1:{self.proxy_port}/devtools/browser?token={self._auth_token}'
            info['_proxy'] = True; info['_proxy_port'] = self.proxy_port
            info['_chrome_port'] = self.chrome_port
            info['_upstream_connected'] = self._upstream.connected
            return json.dumps(info)
        elif path == '/json/list' or path == '/json':
            try:
                result = self._upstream.send_and_wait({'id': -2, 'method': 'Target.getTargets'}, timeout=5.0)
                if result and 'result' in result:
                    targets = result['result'].get('targetInfos', [])
                    tab_list = []
                    for t in targets:
                        if t.get('type') == 'page':
                            tid = t.get('targetId', '')
                            tab_list.append({
                                'id': tid, 'type': 'page', 'title': t.get('title', ''),
                                'url': t.get('url', ''),
                                'webSocketDebuggerUrl': f'ws://127.0.0.1:{self.proxy_port}/devtools/page/{tid}',
                            })
                    return json.dumps(tab_list)
            except Exception: pass
            return '[]'
        elif path.startswith('/json/new'):
            url = 'about:blank'
            if '?' in path:
                from urllib.parse import unquote; url = unquote(path.split('?', 1)[1])
            try:
                result = self._upstream.send_and_wait({'id': -3, 'method': 'Target.createTarget', 'params': {'url': url}}, timeout=10.0)
                if result and 'result' in result:
                    tid = result['result'].get('targetId', '')
                    return json.dumps({'id': tid, 'type': 'page', 'title': '', 'url': url,
                                       'webSocketDebuggerUrl': f'ws://127.0.0.1:{self.proxy_port}/devtools/page/{tid}'})
            except Exception: pass
            return None
        elif path.startswith('/json/close/'):
            tid = path.split('/json/close/', 1)[1]
            try:
                self._upstream.send_and_wait({'id': -4, 'method': 'Target.closeTarget', 'params': {'targetId': tid}}, timeout=5.0)
                return '"Target is closing"'
            except Exception: return None
        elif path.startswith('/json/activate/'):
            tid = path.split('/json/activate/', 1)[1]
            try:
                self._upstream.send_and_wait({'id': -5, 'method': 'Target.activateTarget', 'params': {'targetId': tid}}, timeout=5.0)
                return '"Target activated"'
            except Exception: return None
        return None

    def _write_state(self):
        os.makedirs(PROXY_STATE_DIR, exist_ok=True)
        os.chmod(PROXY_STATE_DIR, 0o700)
        with open(PROXY_PID_FILE, 'w') as f: f.write(str(os.getpid()))
        state = {'pid': os.getpid(), 'proxy_port': self.proxy_port,
                 'chrome_port': self.chrome_port, 'chrome_host': self.chrome_host,
                 'started_at': time.time(),
                 'proxy_url': f'http://127.0.0.1:{self.proxy_port}', 'auth_token': self._auth_token}
        with open(PROXY_STATE_FILE, 'w') as f: json.dump(state, f)

    def _cleanup_state(self):
        for f in (PROXY_PID_FILE, PROXY_STATE_FILE):
            try: os.remove(f)
            except OSError: pass


def get_proxy_state():
    if not os.path.isfile(PROXY_STATE_FILE): return None
    try:
        with open(PROXY_STATE_FILE, 'r') as f: state = json.load(f)
        pid = state.get('pid')
        if pid:
            try:
                os.kill(pid, 0)
                return state
            except (OSError, ProcessLookupError):
                _cleanup_stale_state(); return None
        return None
    except (json.JSONDecodeError, OSError):
        return None


def _cleanup_stale_state():
    for f in (PROXY_PID_FILE, PROXY_STATE_FILE):
        try: os.remove(f)
        except OSError: pass


def is_proxy_running(): return get_proxy_state() is not None

def get_proxy_url():
    state = get_proxy_state()
    return state.get('proxy_url') if state else None


def stop_proxy():
    state = get_proxy_state()
    if not state: _log("No proxy is running."); return False
    pid = state.get('pid')
    if pid:
        try:
            os.kill(pid, signal.SIGTERM)
            _log(f"Sent SIGTERM to proxy (PID {pid}).")
            for _ in range(10):
                try: os.kill(pid, 0); time.sleep(0.3)
                except (OSError, ProcessLookupError): break
            _cleanup_stale_state(); return True
        except (OSError, ProcessLookupError):
            _log(f"Proxy (PID {pid}) is not running. Cleaning up state.")
            _cleanup_stale_state(); return False
    return False


def _is_port_listening(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1); return s.connect_ex(('127.0.0.1', port)) == 0


def ensure_proxy_running(chrome_port=DEFAULT_CHROME_PORT, proxy_port=DEFAULT_PROXY_PORT,
                          timeout=30.0, auth_sock=None):
    state = get_proxy_state()
    if state:
        existing_port = state.get('proxy_port')
        if existing_port and _is_port_listening(existing_port):
            upstream_ok = False
            try:
                req = Request(f'http://127.0.0.1:{existing_port}/json/version', headers={'Accept': 'application/json'})
                with urlopen(req, timeout=3) as resp:
                    info = json.loads(resp.read().decode('utf-8'))
                    upstream_ok = info.get('_upstream_connected', False)
            except Exception: pass
            if upstream_ok:
                if auth_sock:
                    try: auth_sock.close()
                    except OSError: pass
                return state.get('proxy_url')
            else:
                _log("Existing proxy has no upstream connection. Stopping it.")
                stop_proxy(); time.sleep(0.5)
        else:
            _cleanup_stale_state()

    if auth_sock:
        if sys.platform == 'win32':
            proxy = CDPProxy(chrome_port=chrome_port, proxy_port=proxy_port)
            proxy_thread = threading.Thread(target=proxy.start, kwargs={'block': True, 'auth_sock': auth_sock},
                                            daemon=True, name='cdp-proxy-inprocess')
            proxy_thread.start()
            proxy_url = f'http://127.0.0.1:{proxy_port}'
            deadline = time.time() + timeout
            while time.time() < deadline:
                if _is_port_listening(proxy_port): time.sleep(0.3); return proxy_url
                time.sleep(0.5)
            raise RuntimeError(f"In-process CDP Proxy did not become ready within {timeout}s")
        pid = os.fork()
        if pid == 0:
            try:
                os.setsid()
                os.makedirs(PROXY_STATE_DIR, exist_ok=True)
                log_path = os.path.join(PROXY_STATE_DIR, 'proxy.log')
                log_fd = os.open(log_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o644)
                os.dup2(log_fd, 1); os.dup2(log_fd, 2); os.close(log_fd)
                devnull = os.open(os.devnull, os.O_RDONLY); os.dup2(devnull, 0); os.close(devnull)
                def _sig_handler(sig, frame): proxy.stop(); sys.exit(0)
                signal.signal(signal.SIGTERM, _sig_handler); signal.signal(signal.SIGINT, _sig_handler)
                proxy = CDPProxy(chrome_port=chrome_port, proxy_port=proxy_port)
                proxy.start(block=True, auth_sock=auth_sock)
            except Exception: pass
            finally: os._exit(0)
        else:
            try: auth_sock.close()
            except OSError: pass
            proxy_url = f'http://127.0.0.1:{proxy_port}'
            deadline = time.time() + timeout
            while time.time() < deadline:
                if _is_port_listening(proxy_port): time.sleep(0.3); return proxy_url
                try:
                    wpid, status = os.waitpid(pid, os.WNOHANG)
                    if wpid != 0: raise RuntimeError(f"CDP Proxy child (PID {pid}) exited with status {status}")
                except ChildProcessError: break
                time.sleep(0.5)
            raise RuntimeError(f"Forked CDP Proxy did not become ready within {timeout}s")

    script_path = os.path.abspath(__file__)
    cmd = [sys.executable, script_path, 'start', '--chrome-port', str(chrome_port), '--proxy-port', str(proxy_port), '--daemon']
    import subprocess
    log_path = os.path.join(PROXY_STATE_DIR, 'proxy.log')
    os.makedirs(PROXY_STATE_DIR, exist_ok=True)
    log_file = open(log_path, 'a')
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=log_file, start_new_session=True)
    proxy_url = f'http://127.0.0.1:{proxy_port}'
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _is_port_listening(proxy_port): time.sleep(0.3); return proxy_url
        if proc.poll() is not None:
            try:
                log_file.flush()
                with open(log_path, 'r') as lf: log_content = lf.read()[-500:]
            except Exception: log_content = ''
            raise RuntimeError(f"CDP Proxy failed to start (exit code {proc.returncode}): {log_content}")
        time.sleep(0.5)
    raise RuntimeError(f"CDP Proxy did not become ready within {timeout}s")


def main():
    parser = argparse.ArgumentParser(description='CDP Proxy')
    sub = parser.add_subparsers(dest='command')
    start_p = sub.add_parser('start', help='Start proxy')
    start_p.add_argument('--chrome-port', type=int, default=DEFAULT_CHROME_PORT)
    start_p.add_argument('--proxy-port', type=int, default=DEFAULT_PROXY_PORT)
    start_p.add_argument('--daemon', action='store_true')
    sub.add_parser('status', help='Show proxy status')
    sub.add_parser('stop', help='Stop proxy')
    args = parser.parse_args()
    if not args.command: parser.print_help(); sys.exit(0)
    if args.command == 'start':
        existing = get_proxy_state()
        if existing:
            print(f"CDP Proxy already running (PID {existing['pid']}, port {existing['proxy_port']})"); sys.exit(0)
        proxy = CDPProxy(chrome_port=args.chrome_port, proxy_port=args.proxy_port)
        if args.daemon:
            def _sig_handler(sig, frame): proxy.stop(); sys.exit(0)
            signal.signal(signal.SIGTERM, _sig_handler); signal.signal(signal.SIGINT, _sig_handler)
        proxy.start(block=True)
    elif args.command == 'status':
        state = get_proxy_state()
        if state:
            age = time.time() - state.get('started_at', 0)
            print(f"CDP Proxy is running")
            print(f"   PID:       {state['pid']}")
            print(f"   Proxy URL: {state['proxy_url']}")
            print(f"   Chrome:    {state['chrome_host']}:{state['chrome_port']}")
            print(f"   Uptime:    {int(age)}s")
        else:
            print("CDP Proxy is not running"); sys.exit(1)
    elif args.command == 'stop':
        if stop_proxy(): print("CDP Proxy stopped.")
        else: print("No proxy to stop."); sys.exit(1)


if __name__ == '__main__': main()
