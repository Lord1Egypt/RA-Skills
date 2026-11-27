"""北向本地 mock 服务：用于离线验证 lib/north_client.py 与 .mjs。

启动：python tests/mock_north.py [port]
行为：首次不带 Authorization 的 /open/device/list 返回 401（验证自动重登）；
      /open/alarm/list?status=ratelimit 返回 code=429（验证限频错误）。
"""
import json
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs


class State:
    def __init__(self):
        self.requests = []
        self.token = "TKN-1"


def make_handler(state):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):
            pass

        def _body(self):
            n = int(self.headers.get("Content-Length") or 0)
            raw = self.rfile.read(n) if n else b""
            try:
                return json.loads(raw.decode("utf-8")) if raw else None
            except json.JSONDecodeError:
                return None

        def _send(self, obj, status=200):
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _record(self, method, path, body, query):
            state.requests.append({"method": method, "path": path, "body": body, "query": query,
                                   "auth": self.headers.get("Authorization"),
                                   "api_key": self.headers.get("X-API-Key")})

        def do_GET(self):
            u = urlparse(self.path)
            query = {k: v[0] for k, v in parse_qs(u.query).items()}
            self._record("GET", u.path, None, query)
            if u.path == "/auth/profile":
                return self._send({"code": 0, "data": {"id": "u1", "username": "tester"}, "msg": "ok"})
            if u.path == "/open/account":
                return self._send({"code": 0, "data": {"devices": 1}, "msg": "ok"})
            if u.path == "/open/device/list":
                if not self.headers.get("Authorization"):
                    return self._send({"code": 401, "msg": "unauthorized"}, 401)
                return self._send({"code": 0, "data": {"items": [
                    {"id": "DEV-1", "name": "阀", "password": "p", "bindCode": "b"}], "totalCount": 1}, "msg": "ok"})
            if u.path == "/open/device/DEV-1":
                return self._send({"code": 0, "data": {"id": "DEV-1", "password": "p", "bindCode": "b"}, "msg": "ok"})
            if u.path == "/open/device/DEV-1/telemetry":
                return self._send({"code": 0, "data": {"deviceId": "DEV-1", "online": True,
                                                       "values": {"wd": "25.3"}}, "msg": "ok"})
            if u.path == "/open/device/DEV-1/history":
                return self._send({"code": 0, "data": {"items": [{"ts": 1, "values": {"wd": "25.3"}}]}, "msg": "ok"})
            if u.path == "/open/device/DEV-1/aggregate":
                return self._send({"code": 0, "data": {"items": []}, "msg": "ok"})
            if u.path == "/open/device/DEV-1/backfill-logs":
                return self._send({"code": 0, "data": {"items": []}, "msg": "ok"})
            if u.path == "/open/device/stats":
                return self._send({"code": 0, "data": {"online": 1, "offline": 0}, "msg": "ok"})
            if u.path == "/open/command/list":
                return self._send({"code": 0, "data": {"items": [], "totalCount": 0}, "msg": "ok"})
            if u.path == "/open/command/CMD-1":
                return self._send({"code": 0, "data": {"id": "CMD-1", "status": "succeeded"}, "msg": "ok"})
            if u.path == "/open/alarm/list":
                if query.get("status") == "ratelimit":
                    return self._send({"code": 429, "msg": "too many requests"}, 429)
                return self._send({"code": 0, "data": {"items": [], "totalCount": 0}, "msg": "ok"})
            if u.path == "/open/product/list":
                return self._send({"code": 0, "data": {"items": [
                    {"id": "RSTICQ", "metrics": [{"key": "in1", "access": "none"}]}]}, "msg": "ok"})
            if u.path == "/open/gateway/ports":
                return self._send({"code": 0, "data": {"tcp": [41032], "udp": [40501], "mqtt": [1883]}, "msg": "ok"})
            return self._send({"code": 404, "msg": "not found"}, 404)

        def do_POST(self):
            u = urlparse(self.path)
            body = self._body()
            self._record("POST", u.path, body, {})
            if u.path == "/auth/login":
                if body and body.get("password") == "pw":
                    return self._send({"code": 0, "data": {"token": state.token,
                                                           "user": {"id": "u1", "username": body.get("account")}},
                                       "msg": "ok"})
                return self._send({"code": 401, "msg": "bad password"}, 401)
            if u.path == "/open/device/DEV-1/command":
                return self._send({"code": 0, "data": {"tra": "tra-1", "cmd": body.get("cmd")}, "msg": "ok"})
            if u.path == "/open/product/RSTICQ/clean-metrics":
                return self._send({"code": 0, "data": {"removed": 0}, "msg": "ok"})
            return self._send({"code": 404, "msg": "not found"}, 404)

        def do_PATCH(self):
            u = urlparse(self.path)
            body = self._body()
            self._record("PATCH", u.path, body, {})
            if u.path.startswith("/open/product/RSTICQ/metric/"):
                return self._send({"code": 0, "data": {"before": {"access": "none"},
                                                       "after": body}, "msg": "ok"})
            return self._send({"code": 404, "msg": "not found"}, 404)

        def do_PUT(self):
            u = urlparse(self.path)
            body = self._body()
            self._record("PUT", u.path, body, {})
            return self._send({"code": 0, "data": {"ok": True}, "msg": "ok"})

    return Handler


def start(port=18081):
    state = State()
    srv = ThreadingHTTPServer(("127.0.0.1", port), make_handler(state))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, state


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 18081
    srv, state = start(port)
    print("mock north on http://127.0.0.1:%d" % port)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        srv.shutdown()
