import argparse
import ctypes
import json
import os
import secrets
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import uiautomation as auto

import wechat_send as ws


HOST = "127.0.0.1"
STATE_PATH = Path(__file__).with_name("wechat_assistant_state.json")
LOG_PATH = Path(__file__).with_name("wechat_assistant_daemon.log")
DEFAULT_TIMEOUT = 20.0


def now_ts() -> float:
    return time.time()


def log_event(message: str):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    LOG_PATH.write_text("", encoding="utf-8") if not LOG_PATH.exists() else None
    with LOG_PATH.open("a", encoding="utf-8") as handle:
        handle.write(f"[{timestamp}] {message}\n")


def reserve_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, 0))
        return sock.getsockname()[1]


def load_state():
    if not STATE_PATH.exists():
        return None
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def save_state(state):
    STATE_PATH.write_text(
        json.dumps(state, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def clear_state():
    if STATE_PATH.exists():
        STATE_PATH.unlink(missing_ok=True)


def build_url(state, path: str) -> str:
    return f"http://{state['host']}:{state['port']}{path}"


def is_process_alive(pid: int | None) -> bool:
    if not pid:
        return False
    try:
        handle = ctypes.windll.kernel32.OpenProcess(0x1000, False, int(pid))
    except Exception:
        return False
    if not handle:
        return False
    ctypes.windll.kernel32.CloseHandle(handle)
    return True


def daemon_request(state, operation: str, payload=None, timeout: float = DEFAULT_TIMEOUT):
    body = {
        "token": state["token"],
        "operation": operation,
        "payload": payload or {},
    }
    request = urllib.request.Request(
        build_url(state, "/rpc"),
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def is_daemon_alive(state, require_rpc: bool = False) -> bool:
    if is_process_alive(state.get("pid")) and not require_rpc:
        return True
    try:
        response = daemon_request(state, "status", timeout=2.0)
    except Exception:
        return False
    return bool(response.get("ok"))


class AssistantService:
    def __init__(self, exe_path: str | None):
        self.exe_path = exe_path
        self.lock = threading.RLock()
        self.current_contact = None
        self.last_window_handle = None
        log_event("service init start")
        ws.configure_stdio()
        auto.SetGlobalSearchTimeout(3)
        ws.get_ocr_engine()
        log_event("service init done")

    def ensure_window(self):
        log_event("ensure_window start")
        try:
            window = ws.find_wechat_window(timeout=2.0)
        except Exception:
            log_event("ensure_window find failed; launching exe")
            if not self.exe_path:
                raise
            ws.launch_wechat(self.exe_path)
            ws.sleep_with_abort(2.0)
            window = ws.find_wechat_window(timeout=12.0)

        self.last_window_handle = getattr(window, "NativeWindowHandle", None) or getattr(window, "Handle", None) or self.last_window_handle
        log_event(f"ensure_window got handle={self.last_window_handle}")
        window.SetActive()
        ws.sleep_with_abort(0.2)
        return window

    def ensure_chat(self, contact: str):
        log_event(f"ensure_chat start contact={contact}")
        window = self.ensure_window()
        if self.current_contact == contact and ws.is_current_chat(window, contact):
            log_event(f"ensure_chat reused contact={contact}")
            return window
        ws.open_chat(window, contact)
        self.current_contact = contact
        log_event(f"ensure_chat opened contact={contact}")
        return window

    def status(self):
        return {
            "current_contact": self.current_contact,
            "exe_path": self.exe_path,
            "window_handle": self.last_window_handle,
        }

    def read_latest_incoming(self, contact: str):
        with self.lock:
            log_event(f"read_latest_incoming start contact={contact}")
            window = self.ensure_chat(contact)
            text = ws.read_latest_incoming_message(window)
            log_event(f"read_latest_incoming done contact={contact} len={len(text)}")
            return {"contact": contact, "text": text}

    def read_latest(self, contact: str, history_lines: int = 12):
        with self.lock:
            log_event(f"read_latest start contact={contact}")
            window = self.ensure_chat(contact)
            text = ws.read_recent_chat(window, max_lines=history_lines)
            latest = ws.extract_latest_message(text)
            log_event(f"read_latest done contact={contact} len={len(latest)}")
            return {"contact": contact, "text": latest}

    def send_message(self, contact: str, message: str):
        with self.lock:
            log_event(f"send_message start contact={contact} len={len(message)}")
            window = self.ensure_chat(contact)
            ws.send_message(window, message)
            log_event(f"send_message done contact={contact}")
            return {"contact": contact, "message": message}


class RPCHandler(BaseHTTPRequestHandler):
    service = None
    token = None
    server_ref = None

    def _send(self, status_code: int, payload):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_POST(self):
        if self.path != "/rpc":
            self._send(404, {"ok": False, "error": "not_found"})
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        try:
            request = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, {"ok": False, "error": "invalid_json"})
            return

        if request.get("token") != self.token:
            self._send(403, {"ok": False, "error": "forbidden"})
            return

        operation = request.get("operation")
        payload = request.get("payload") or {}
        log_event(f"rpc start operation={operation}")

        try:
            if operation == "status":
                result = self.service.status()
            elif operation == "read_latest_incoming":
                result = self.service.read_latest_incoming(payload["contact"])
            elif operation == "read_latest":
                result = self.service.read_latest(
                    payload["contact"],
                    int(payload.get("history_lines", 12)),
                )
            elif operation == "send_message":
                result = self.service.send_message(
                    payload["contact"],
                    payload["message"],
                )
            elif operation == "stop":
                result = {"stopping": True}
                threading.Thread(target=self.server_ref.shutdown, daemon=True).start()
            else:
                self._send(400, {"ok": False, "error": "unknown_operation"})
                return
        except KeyboardInterrupt:
            log_event(f"rpc aborted operation={operation}")
            self._send(200, {"ok": False, "error": "aborted"})
            return
        except Exception as exc:
            log_event(f"rpc error operation={operation} error={exc}")
            self._send(200, {"ok": False, "error": str(exc)})
            return

        log_event(f"rpc done operation={operation}")
        self._send(200, {"ok": True, "result": result})

    def log_message(self, format, *args):
        return


def run_server(port: int, token: str, exe_path: str | None):
    state = load_state()
    if state and state.get("port") == port and state.get("token") == token:
        state["pid"] = os.getpid()
        save_state(state)

    service = AssistantService(exe_path)
    RPCHandler.service = service
    RPCHandler.token = token
    server = HTTPServer((HOST, port), RPCHandler)
    RPCHandler.server_ref = server
    try:
        server.serve_forever(poll_interval=0.2)
    finally:
        server.server_close()
        clear_state()


def start_daemon(exe_path: str | None):
    existing = load_state()
    if existing and is_daemon_alive(existing):
        return existing

    port = reserve_port()
    token = secrets.token_urlsafe(18)
    state = {
        "host": HOST,
        "port": port,
        "token": token,
        "started_at": now_ts(),
        "exe_path": exe_path or "",
    }
    save_state(state)
    cmd = [
        sys.executable,
        str(Path(__file__).resolve()),
        "--serve",
        "--port",
        str(port),
        "--token",
        token,
    ]
    if exe_path:
        cmd.extend(["--exe", exe_path])

    quoted_args = ", ".join("'" + part.replace("'", "''") + "'" for part in cmd[1:])
    ps_command = (
        f"Start-Process -FilePath '{cmd[0]}' "
        f"-ArgumentList @({quoted_args}) "
        f"-WorkingDirectory '{Path(__file__).resolve().parent}' "
        "-WindowStyle Hidden"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_command],
        check=True,
        cwd=str(Path(__file__).resolve().parent),
    )

    deadline = time.time() + 15.0
    while time.time() < deadline:
        if is_daemon_alive(state, require_rpc=True):
            return state
        time.sleep(0.25)

    raise RuntimeError("Assistant daemon failed to start.")


def stop_daemon():
    state = load_state()
    if not state:
        return {"stopped": False, "reason": "not_running"}
    try:
        daemon_request(state, "stop", timeout=3.0)
    except Exception:
        pass
    clear_state()
    return {"stopped": True}


def print_json(payload):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_parser():
    parser = argparse.ArgumentParser(description="Persistent local assistant for WeChat OCR/reply.")
    parser.add_argument("--serve", action="store_true", help="Internal: run the HTTP server.")
    parser.add_argument("--start", action="store_true", help="Start the local assistant daemon.")
    parser.add_argument("--stop", action="store_true", help="Stop the local assistant daemon.")
    parser.add_argument("--status", action="store_true", help="Show daemon status.")
    parser.add_argument("--read-latest-incoming", action="store_true", help="Read the latest incoming message.")
    parser.add_argument("--read-latest", action="store_true", help="Read the latest message block.")
    parser.add_argument("--send-message", help="Send a text message.")
    parser.add_argument("--contact", help="Target contact.")
    parser.add_argument("--exe", help="Path to Weixin.exe for auto-launch.")
    parser.add_argument("--history-lines", type=int, default=12, help="History lines for --read-latest.")
    parser.add_argument("--port", type=int, help="Internal: listen port.")
    parser.add_argument("--token", help="Internal: auth token.")
    return parser


def main():
    ws.configure_stdio()
    parser = build_parser()
    args = parser.parse_args()

    if args.serve:
        if not args.port or not args.token:
            raise SystemExit("Missing --port/--token for --serve.")
        run_server(args.port, args.token, args.exe)
        return 0

    if args.start:
        state = start_daemon(args.exe)
        print_json({"ok": True, "state": state})
        return 0

    if args.stop:
        print_json(stop_daemon())
        return 0

    state = load_state()
    if not state or not is_daemon_alive(state):
        state = start_daemon(args.exe)

    if args.status:
        print_json(daemon_request(state, "status"))
        return 0

    if args.read_latest_incoming:
        print_json(
            daemon_request(
                state,
                "read_latest_incoming",
                {"contact": args.contact},
            )
        )
        return 0

    if args.read_latest:
        print_json(
            daemon_request(
                state,
                "read_latest",
                {"contact": args.contact, "history_lines": args.history_lines},
            )
        )
        return 0

    if args.send_message is not None:
        print_json(
            daemon_request(
                state,
                "send_message",
                {"contact": args.contact, "message": args.send_message},
            )
        )
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
