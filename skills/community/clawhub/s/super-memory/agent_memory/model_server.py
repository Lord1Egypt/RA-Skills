#!/usr/bin/env python3
"""
model_server.py - Embedding 模型守护进程
保持模型常驻内存，CLI 通过 socket 请求编码，避免每次 10s 加载。

跨平台支持：
  - Linux/Mac: Unix domain socket（低延迟）
  - Windows:   TCP socket 127.0.0.1:8977

启动:  python3 model_server.py start
停止:  python3 model_server.py stop
状态:  python3 model_server.py status
清理:  python3 model_server.py cleanup   # 清理 stale socket/pid

HTTP 健康检查:
  http://localhost:<port>/healthz  → 200 if alive
  http://localhost:<port>/readyz   → 200 if model loaded
  http://localhost:<port>/metrics  → JSON stats
"""

from __future__ import annotations

import os
import sys
import json
import socket
import struct
import time
import logging
import threading
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
PID_PATH = os.path.join(PROJECT_DIR, "model.pid")

# ── 跨平台传输层 ──────────────────────────────────────
# Linux/Mac: Unix domain socket（零延迟，本地通信最优）
# Windows: TCP socket（AF_UNIX 不可用）

IS_WINDOWS = sys.platform == "win32"
TCP_HOST = "127.0.0.1"
TCP_PORT = int(os.environ.get("MODEL_SERVER_TCP_PORT", "8977"))
SOCK_PATH = os.path.join(PROJECT_DIR, "model.sock")


def _get_transport_addr():
    """返回当前平台的传输地址（供 bind/connect 使用）"""
    if IS_WINDOWS:
        return (TCP_HOST, TCP_PORT)
    return SOCK_PATH


def _create_server_socket() -> socket.socket:
    """创建服务端监听 socket"""
    if IS_WINDOWS:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(_get_transport_addr())
    else:
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(_get_transport_addr())
    return sock


def _create_client_socket() -> socket.socket:
    """创建客户端连接 socket"""
    if IS_WINDOWS:
        return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)


def _is_port_in_use(host: str, port: int, timeout: float = 1.0) -> bool:
    """检查 TCP 端口是否被占用（Windows 用）"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((host, port))
        s.close()
        return True
    except Exception as e:
        logger.debug("model_server: connection check: %s", e)
        return False


def _is_transport_connectable(timeout: float = 1.0) -> bool:
    """探测当前平台的传输通道是否真的可用"""
    try:
        s = _create_client_socket()
        s.settimeout(timeout)
        s.connect(_get_transport_addr())
        s.close()
        return True
    except Exception as e:
        logger.debug("model_server: connection check: %s", e)
        return False


# HTTP 健康检查端口（0 = 禁用）
HTTP_PORT = int(os.environ.get("MODEL_SERVER_HTTP_PORT", "0"))

logger = logging.getLogger(__name__)


def _ensure_hf_endpoint():
    """确保 HF 镜像可用（与 embedding_store 保持一致）"""
    if os.environ.get("HF_ENDPOINT"):
        return
    import socket as s
    try:
        s.create_connection(("huggingface.co", 443), timeout=2).close()
    except (s.timeout, OSError):
        os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
        logger.info(f"HuggingFace unreachable, auto-set HF_ENDPOINT=https://hf-mirror.com")


def _is_pid_alive(pid: int) -> bool:
    """检查进程是否存活"""
    try:
        pid = int(pid)
        if IS_WINDOWS:
            result = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True, text=True, timeout=3
            )
            return str(pid) in result.stdout
        else:
            os.kill(pid, 0)
            return True
    except (OSError, ProcessLookupError, subprocess.SubprocessError):
        return False


def cleanup_stale():
    """
    清理残留的 socket/port 和 PID 文件。

    Linux/Mac: 清理 Unix socket 文件
    Windows:   检查 TCP 端口是否仍在被占用
    """
    cleaned = []

    # 检查 PID 文件
    if os.path.exists(PID_PATH):
        try:
            with open(PID_PATH, "r") as f:
                pid = int(f.read().strip())
            if not _is_pid_alive(pid):
                logger.info(f"Stale PID file (pid={pid} not alive), cleaning up")
                os.remove(PID_PATH)
                cleaned.append("pid")
                if not IS_WINDOWS and os.path.exists(SOCK_PATH):
                    os.remove(SOCK_PATH)
                    cleaned.append("sock")
                return cleaned
            else:
                # PID 还活着，但传输通道可能坏了
                if not _is_transport_connectable():
                    logger.warning(f"PID alive but transport dead")
                    if not IS_WINDOWS and os.path.exists(SOCK_PATH):
                        os.remove(SOCK_PATH)
                        cleaned.append("sock")
        except (ValueError, IOError):
            os.remove(PID_PATH)
            cleaned.append("pid")

    # Linux/Mac: 只有 socket 没有 PID
    if not IS_WINDOWS and os.path.exists(SOCK_PATH) and not os.path.exists(PID_PATH):
        if not _is_transport_connectable():
            logger.info("Stale socket file, cleaning up")
            os.remove(SOCK_PATH)
            cleaned.append("sock")

    return cleaned


class ModelServer:
    """Embedding 模型守护进程"""

    def __init__(self, model_name=None):
        # Fix (冷启动优化): 默认模型与 embedding_store.py 保持一致
        self.model_name = model_name or os.environ.get(
            "AGENT_MEMORY_EMBEDDING_MODEL", "BAAI/bge-small-zh-v1.5"
        )
        self.model = None
        self._load_model()

    def _load_model(self):
        """加载模型（仅一次），支持本地路径和 HfApi 镜像降级"""
        import warnings
        warnings.filterwarnings("ignore")
        _ensure_hf_endpoint()

        t0 = time.time()
        from sentence_transformers import SentenceTransformer

        # 1. 本地路径模式
        model_path = self.model_name
        if os.path.isdir(model_path):
            self.model = SentenceTransformer(model_path, device="cpu")
            logger.info(f"Model loaded from local path in {time.time()-t0:.1f}s: {model_path}")
            return

        # 2. 标准模式
        try:
            self.model = SentenceTransformer(model_path, device="cpu")
            logger.info(f"Model loaded in {time.time()-t0:.1f}s")
            return
        except Exception as e1:
            # 3. 降级：HfApi(endpoint=...) 方式
            hf_endpoint = os.environ.get("HF_ENDPOINT")
            if hf_endpoint:
                logger.info(f"SentenceTransformer download failed, trying HfApi(endpoint={hf_endpoint})...")
                try:
                    from huggingface_hub import HfApi, snapshot_download
                    local_path = snapshot_download(
                        repo_id=model_path,
                        endpoint=hf_endpoint,
                    )
                    self.model = SentenceTransformer(local_path, device="cpu")
                    logger.info(f"Model loaded via HfApi mirror in {time.time()-t0:.1f}s: {local_path}")
                    return
                except Exception as e2:
                    logger.error(f"HfApi download also failed: {e2}")
            raise e1

    def encode(self, texts: list[str]) -> list[list[float]]:
        """批量编码"""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return [e.tolist() for e in embeddings]

    def handle_request(self, data: dict) -> dict:
        """处理一个请求"""
        action = data.get("action")

        if action == "encode":
            texts = data.get("texts", [])
            if not texts:
                HealthCheckHandler.record_request(True)
                return {"ok": True, "embeddings": []}
            try:
                embeddings = self.encode(texts)
                HealthCheckHandler.record_request(True)
                return {"ok": True, "embeddings": embeddings}
            except Exception as e:
                HealthCheckHandler.record_request(False)
                return {"ok": False, "error": str(e)}

        elif action == "ping":
            HealthCheckHandler.record_request(True)
            return {"ok": True, "model": self.model_name}

        elif action == "shutdown":
            HealthCheckHandler.record_request(True)
            return {"ok": True, "action": "shutdown"}

        HealthCheckHandler.record_request(False)
        return {"ok": False, "error": f"unknown action: {action}"}


# ── HTTP 健康检查 ───────────────────────────────────────

class HealthCheckHandler(BaseHTTPRequestHandler):
    _model_loaded = False
    _model_name = ""
    _start_time = 0
    _request_count = 0
    _error_count = 0

    @classmethod
    def set_model_state(cls, loaded: bool, name: str):
        cls._model_loaded = loaded
        cls._model_name = name

    @classmethod
    def record_request(cls, success: bool = True):
        cls._request_count += 1
        if not success:
            cls._error_count += 1

    def do_GET(self):
        if self.path == "/healthz":
            self._respond(200, "OK", "text/plain")

        elif self.path == "/readyz":
            if self._model_loaded:
                self._respond(200, "READY", "text/plain")
            else:
                self._respond(503, "NOT READY", "text/plain")

        elif self.path == "/metrics":
            uptime = time.time() - self._start_time if self._start_time else 0
            metrics = {
                "status": "running",
                "model_loaded": self._model_loaded,
                "model_name": self._model_name,
                "uptime_seconds": round(uptime, 1),
                "total_requests": self._request_count,
                "error_count": self._error_count,
                "error_rate": round(self._error_count / max(1, self._request_count), 4),
                "transport": "tcp" if IS_WINDOWS else "unix",
            }
            body = json.dumps(metrics, ensure_ascii=False)
            self._respond(200, body, "application/json")

        else:
            self._respond(404, "Not Found", "text/plain")

    def _respond(self, code: int, body: str, content_type: str):
        self.send_response(code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        pass


def start_http_server(port: int) -> HTTPServer | None:
    """启动 HTTP 健康检查服务（在独立线程中）"""
    if port <= 0:
        return None

    try:
        server = HTTPServer(("127.0.0.1", port), HealthCheckHandler)
        server.socket.settimeout(1.0)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        HealthCheckHandler._start_time = time.time()
        logger.info(f"HTTP health check on :{port} (/healthz, /readyz, /metrics)")
        return server
    except Exception as e:
        logger.warning("model_server: %s", e)
        return None


def _recv_msg(conn) -> bytes:
    """接收一条长度前缀的消息"""
    raw_len = conn.recv(4)
    if not raw_len:
        return b""
    msg_len = struct.unpack("!I", raw_len)[0]
    data = b""
    while len(data) < msg_len:
        chunk = conn.recv(msg_len - len(data))
        if not chunk:
            break
        data += chunk
    return data


def _send_msg(conn, data: bytes):
    """发送一条长度前缀的消息"""
    conn.sendall(struct.pack("!I", len(data)) + data)


def run_server():
    """运行守护进程（主线程阻塞）"""
    import warnings
    warnings.filterwarnings("ignore")
    from logging_config import configure_logging
    configure_logging(level="INFO", fmt="[model-server] %(message)s")

    # 启动前清理 stale 文件
    cleaned = cleanup_stale()
    if cleaned:
        logger.info(f"Cleaned stale files: {cleaned}")

    # 如果传输通道还在用（正常运行的实例），退出
    if IS_WINDOWS:
        if _is_port_in_use(TCP_HOST, TCP_PORT):
            logger.error(f"Server already running on {TCP_HOST}:{TCP_PORT}")
            sys.exit(1)
    else:
        if os.path.exists(SOCK_PATH):
            if _is_transport_connectable():
                logger.error("Server already running and socket is connectable")
                sys.exit(1)
            else:
                os.remove(SOCK_PATH)

    server = ModelServer()

    # 设置 HTTP 端点的模型状态
    HealthCheckHandler.set_model_state(True, server.model_name)

    # 启动 HTTP 健康检查（如果配置了端口）
    http_server = start_http_server(HTTP_PORT)

    # 创建主监听 socket
    sock = _create_server_socket()
    sock.listen(8)
    sock.settimeout(None)

    # 写 PID
    with open(PID_PATH, "w") as f:
        f.write(str(os.getpid()))

    transport_desc = f"{TCP_HOST}:{TCP_PORT}" if IS_WINDOWS else SOCK_PATH
    logger.info(f"Listening on {transport_desc}")

    running = True

    def handle_signal(signum, frame):
        nonlocal running
        running = False

    if not IS_WINDOWS:
        import signal as _signal
        _signal.signal(_signal.SIGTERM, handle_signal)
        _signal.signal(_signal.SIGINT, handle_signal)
    else:
        # Windows: SIGTERM 不可用，用 SIGINT（Ctrl+C）即可
        import signal as _signal
        _signal.signal(_signal.SIGINT, handle_signal)

    while running:
        try:
            conn, _ = sock.accept()
        except OSError:
            break

        try:
            raw = _recv_msg(conn)
            if not raw:
                conn.close()
                continue

            request = json.loads(raw)
            response = server.handle_request(request)
            _send_msg(conn, json.dumps(response, ensure_ascii=False).encode())

            if response.get("action") == "shutdown":
                running = False
        except Exception as e:
            try:
                _send_msg(conn, json.dumps({"ok": False, "error": str(e)}).encode())
            except Exception as e:
                logger.warning("model_server: %s", e)
        finally:
            conn.close()

    # 清理
    sock.close()
    if http_server:
        http_server.shutdown()
    if not IS_WINDOWS and os.path.exists(SOCK_PATH):
        os.remove(SOCK_PATH)
    if os.path.exists(PID_PATH):
        os.remove(PID_PATH)
    logger.info("Server stopped")


def send_request(request: dict, timeout: float = 30) -> dict:
    """向守护进程发送请求"""
    if IS_WINDOWS:
        # Windows: TCP 探测端口是否在用
        if not _is_port_in_use(TCP_HOST, TCP_PORT, timeout=1.0):
            return {"ok": False, "error": "server not running"}
    else:
        if not os.path.exists(SOCK_PATH):
            return {"ok": False, "error": "server not running"}

    sock = _create_client_socket()
    sock.settimeout(timeout)
    try:
        sock.connect(_get_transport_addr())
        _send_msg(sock, json.dumps(request, ensure_ascii=False).encode())
        raw = _recv_msg(sock)
        return json.loads(raw) if raw else {"ok": False, "error": "empty response"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
    finally:
        sock.close()


def is_running() -> bool:
    """
    检查守护进程是否在运行。

    先清理 stale 文件，再通过 socket 连通性探测。
    """
    cleanup_stale()

    if IS_WINDOWS:
        # Windows: 检查 TCP 端口
        if not _is_port_in_use(TCP_HOST, TCP_PORT, timeout=1.0):
            return False
        return _is_transport_connectable()

    # Linux/Mac: 检查 Unix socket 文件
    if not os.path.exists(SOCK_PATH):
        return False
    return _is_transport_connectable()


def stop_server():
    """停止守护进程"""
    if not is_running():
        return
    send_request({"action": "shutdown"}, timeout=5)
    # 等待清理
    for _ in range(10):
        if IS_WINDOWS:
            if not _is_port_in_use(TCP_HOST, TCP_PORT, timeout=0.5):
                break
        else:
            if not os.path.exists(SOCK_PATH):
                break
        time.sleep(0.3)


def start_server(daemon: bool = True):
    """启动守护进程"""
    if is_running():
        print("Server already running")
        return

    if not daemon:
        run_server()
        return

    if IS_WINDOWS:
        # Windows: 用 subprocess 后台启动（没有 fork）
        creationflags = 0x08000000  # CREATE_NO_WINDOW
        proc = subprocess.Popen(
            [sys.executable, __file__, "run"],
            creationflags=creationflags,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        )
        # 等待端口就绪
        for _ in range(50):
            if _is_port_in_use(TCP_HOST, TCP_PORT, timeout=0.5):
                break
            time.sleep(0.2)
        # 写 PID
        with open(PID_PATH, "w") as f:
            f.write(str(proc.pid))
        print(f"Server started (pid={proc.pid}, tcp={TCP_HOST}:{TCP_PORT})")
        return

    # Linux/Mac: fork 后台启动
    pid = os.fork()
    if pid > 0:
        # 等待 socket 就绪
        for _ in range(50):
            if os.path.exists(SOCK_PATH) and _is_transport_connectable():
                break
            time.sleep(0.2)
        print(f"Server started (pid={pid})")
        return

    # 子进程
    os.setsid()
    sys.stdin = open(os.devnull, "r")
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    run_server()
    sys.exit(0)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "start"

    if cmd == "start":
        start_server()
    elif cmd == "stop":
        stop_server()
    elif cmd == "status":
        if is_running():
            resp = send_request({"action": "ping"})
            print(f"Running: {resp}")
        else:
            print("Not running")
    elif cmd == "cleanup":
        cleaned = cleanup_stale()
        print(f"Cleaned: {cleaned}" if cleaned else "Nothing to clean")
    elif cmd == "run":
        start_server(daemon=False)
    else:
        print(f"Usage: {sys.argv[0]} [start|stop|status|cleanup|run]")
