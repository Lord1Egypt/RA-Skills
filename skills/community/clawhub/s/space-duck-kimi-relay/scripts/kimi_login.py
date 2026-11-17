#!/usr/bin/env python3
"""space-duck-kimi-relay — local Kimi membership sign-in + proxy (Lane A).

Runs the RFC 8628 device-code flow against auth.kimi.com and stores the
resulting tokens LOCALLY at ~/.kimi-code/credentials/kimi.json. Nothing is
sent to Spaceduckling or any other third party — the only hosts contacted
are Kimi's own auth/API domain (and openrouter.ai, only if you configure
the optional fallback).

Usage:
  kimi_login.py login          # interactive device sign-in
  kimi_login.py token          # print a fresh access token (auto-refresh)
  kimi_login.py probe          # one-line inference smoke on membership quota
  kimi_login.py serve [port]   # local proxy: point your runtime's OpenAI-
                               # compatible base URL at http://127.0.0.1:PORT/v1
                               # (default 8471); injects a fresh membership
                               # token per request. Optional fallback: set
                               # OPENROUTER_API_KEY to retry failed calls on
                               # OpenRouter's kimi lane (pay-per-token).
  kimi_login.py logout         # delete local credentials
  kimi_login.py install-service [port]   # autostart proxy (systemd user / launchd)
  kimi_login.py uninstall-service        # remove the autostart service
  kimi_login.py status [port]            # creds + proxy + fallback meter

Env overrides: KIMI_CLIENT_ID, KIMI_AUTH_HOST, KIMI_CODING_BASE.
"""
import fcntl
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AUTH_HOST = os.environ.get("KIMI_AUTH_HOST", "https://auth.kimi.com")
# kimi-cli public client (override if Moonshot rotates it)
CLIENT_ID = os.environ.get("KIMI_CLIENT_ID",
                           "17e5f671-d194-4dfb-9706-5516cb48c098")
CODING_BASE = os.environ.get("KIMI_CODING_BASE", "https://api.kimi.com/coding/v1")
CRED_DIR = os.path.expanduser("~/.kimi-code/credentials")
CRED_PATH = os.path.join(CRED_DIR, "kimi.json")
LOCK_PATH = os.path.join(CRED_DIR, "kimi.lock")
OR_SLUGS = {"k3": "moonshotai/kimi-k3", "kimi-k3": "moonshotai/kimi-k3",
            "kimi-for-coding": "moonshotai/kimi-k2.5",
            "kimi-k2.5": "moonshotai/kimi-k2.5"}


def _post(url, form):
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "space-duck-kimi-relay/0.2"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except Exception:
            return e.code, {}


def _save(tok):
    os.makedirs(CRED_DIR, mode=0o700, exist_ok=True)
    rec = {
        "access_token": tok["access_token"],
        "refresh_token": tok.get("refresh_token", ""),
        "expires_at": int(time.time()) + int(tok.get("expires_in") or 900),
        "saved_at": int(time.time()),
    }
    tmp = CRED_PATH + ".tmp"
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(rec, f)
    os.replace(tmp, CRED_PATH)
    return rec


def _load():
    try:
        with open(CRED_PATH) as f:
            return json.load(f)
    except Exception:
        return None


def login():
    st, d = _post(AUTH_HOST + "/api/oauth/device_authorization",
                  {"client_id": CLIENT_ID})
    if st != 200 or not d.get("device_code"):
        print(f"device authorization failed (http {st}): {d}", file=sys.stderr)
        return 1
    uri = d.get("verification_uri_complete") or (
        "https://www.kimi.com/code/authorize_device?user_code=" + d.get("user_code", ""))
    print("1. Open:  " + uri, flush=True)
    print("2. Code:  " + d.get("user_code", ""), flush=True)
    print("Waiting for approval…", flush=True)
    interval = int(d.get("interval") or 5)
    deadline = time.time() + int(d.get("expires_in") or 1800)
    while time.time() < deadline:
        time.sleep(interval)
        st, tok = _post(AUTH_HOST + "/api/oauth/token", {
            "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
            "device_code": d["device_code"], "client_id": CLIENT_ID})
        if tok.get("access_token"):
            _save(tok)
            print("✅ Signed in. Credentials stored at " + CRED_PATH)
            return 0
        err = tok.get("error", "")
        if err == "slow_down":
            interval += 5
        elif err == "authorization_pending":
            continue
        elif err == "expired_token":
            break
        else:
            print(f"token exchange failed (http {st}): {tok}", file=sys.stderr)
            return 1
    print("Sign-in expired — run login again.", file=sys.stderr)
    return 1


def fresh_token():
    """Return a valid access token, refreshing under an exclusive file lock.

    Kimi refresh tokens ROTATE on every grant: two concurrent refreshes
    race and the loser strands the whole lineage. The lock serialises
    refreshes across every duck/process sharing this credential file
    (Lane A mirror of the Lambda-side fenced DDB write).
    """
    rec = _load()
    if not rec:
        print("not signed in — run: kimi_login.py login", file=sys.stderr)
        return None
    if rec["expires_at"] - 60 > time.time():
        return rec["access_token"]
    os.makedirs(CRED_DIR, mode=0o700, exist_ok=True)
    lock_fd = os.open(LOCK_PATH, os.O_WRONLY | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        rec = _load() or rec  # another holder may have refreshed while we waited
        if rec["expires_at"] - 60 > time.time():
            return rec["access_token"]
        st, tok = _post(AUTH_HOST + "/api/oauth/token", {
            "grant_type": "refresh_token",
            "refresh_token": rec.get("refresh_token", ""),
            "client_id": CLIENT_ID})
        if tok.get("access_token"):
            return _save(tok)["access_token"]
        print(f"refresh failed (http {st}): {tok} — run login again", file=sys.stderr)
        return None
    finally:
        os.close(lock_fd)


def _chat(base, key, body_bytes, extra_path="/chat/completions", model_map=None):
    if model_map:
        body = json.loads(body_bytes)
        body["model"] = model_map.get(body.get("model", ""), body.get("model"))
        body_bytes = json.dumps(body).encode()
    req = urllib.request.Request(base + extra_path, data=body_bytes,
                                 headers={"Content-Type": "application/json",
                                          "Authorization": "Bearer " + key,
                                          "User-Agent": "space-duck-kimi-relay/0.2"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.read()


def probe():
    at = fresh_token()
    if not at:
        return 1
    # k3 spends budget on reasoning_content first — keep max_tokens roomy
    payload = json.dumps({"model": "k3", "max_tokens": 512, "messages": [
        {"role": "user", "content": "Reply with exactly: KIMI_RELAY_OK"}]}).encode()
    try:
        _, raw = _chat(CODING_BASE, at, payload)
        data = json.loads(raw)
        print(data["choices"][0]["message"].get("content", "") or "(empty content)")
        return 0
    except urllib.error.HTTPError as e:
        print(f"probe failed (http {e.code}): {e.read()[:200]}", file=sys.stderr)
        return 1


STATS_PATH = os.path.join(CRED_DIR, "fallback_stats.json")
PROXY_SECRET_PATH = os.path.join(CRED_DIR, "proxy_secret")


def proxy_secret():
    """Local bearer secret for the proxy. Auto-generated once, 0600.
    Set KIMI_RELAY_NO_AUTH=1 to disable (single-user boxes only)."""
    if os.environ.get("KIMI_RELAY_NO_AUTH") == "1":
        return None
    try:
        with open(PROXY_SECRET_PATH) as f:
            s = f.read().strip()
            if s:
                return s
    except FileNotFoundError:
        pass
    import secrets as _secrets
    s = "kimi-relay-" + _secrets.token_urlsafe(24)
    os.makedirs(CRED_DIR, exist_ok=True)
    fd = os.open(PROXY_SECRET_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        f.write(s + "\n")
    return s
FALLBACK_DAILY_CAP = int(os.environ.get("KIMI_RELAY_FALLBACK_DAILY_CAP", "200"))


def _fallback_allowed():
    """Daily-capped fallback meter. Returns (allowed, count_today)."""
    day = time.strftime("%Y-%m-%d")
    try:
        with open(STATS_PATH) as f:
            st = json.load(f)
    except Exception:
        st = {}
    n = st.get(day, 0)
    return n < FALLBACK_DAILY_CAP, n


def _fallback_record():
    day = time.strftime("%Y-%m-%d")
    lock_fd = os.open(LOCK_PATH, os.O_WRONLY | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        try:
            with open(STATS_PATH) as f:
                st = json.load(f)
        except Exception:
            st = {}
        st = {day: st.get(day, 0) + 1}  # keep only today
        with open(STATS_PATH, "w") as f:
            json.dump(st, f)
        n = st[day]
    finally:
        os.close(lock_fd)
    if n % 10 == 1:
        sys.stderr.write(f"[kimi-relay] fallback spend meter: {n} OpenRouter "
                         f"call(s) today (cap {FALLBACK_DAILY_CAP})\n")
    return n


def _sse_wrap(raw):
    """Wrap a whole (fallback) chat.completion JSON as a single SSE chunk +
    [DONE] terminator, preserving `usage` on the final chunk per OpenAI's
    streaming convention (spend-metering clients read it there). Pure
    function — safe to unit-test without a live handler."""
    try:
        c = json.loads(raw)
        msg = (c.get("choices") or [{}])[0].get("message", {})
        chunk = {"id": c.get("id", "kimi-relay-fallback"),
                 "object": "chat.completion.chunk",
                 "created": c.get("created", int(time.time())),
                 "model": c.get("model", ""),
                 "choices": [{"index": 0,
                              "delta": {"role": msg.get("role", "assistant"),
                                        "content": msg.get("content", "")},
                              "finish_reason": (c.get("choices") or [{}])[0].get("finish_reason", "stop")}]}
        if c.get("usage") is not None:
            chunk["usage"] = c["usage"]
        return b"data: " + json.dumps(chunk).encode() + b"\n\ndata: [DONE]\n\n"
    except Exception:
        return b"data: [DONE]\n\n"


def serve(port):
    """Local OpenAI-compatible proxy: fresh-token injection, SSE streaming
    passthrough, metered OR fallback."""
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class H(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, fmt, *a):
            sys.stderr.write("[kimi-relay] " + fmt % a + "\n")

        def do_GET(self):
            if self.path.rstrip("/") in ("", "/health", "/v1"):
                self._reply(200, b'{"ok":true,"service":"kimi-relay"}')
            else:
                self.send_error(404)

        def do_POST(self):
            if not self.path.rstrip("/").endswith("/chat/completions"):
                self.send_error(404)
                return
            if secret:
                auth = self.headers.get("Authorization", "")
                if auth != "Bearer " + secret:
                    self._reply(401, json.dumps({"error": {"message":
                        "kimi-relay: bad or missing api key — use the proxy secret from `kimi_login.py status` as your runtime's api key"}}).encode())
                    return
            length = int(self.headers.get("Content-Length", 0))
            if length > 10 * 1024 * 1024:
                self._reply(413, b'{"error":{"message":"request too large"}}')
                return
            body = self.rfile.read(length)
            try:
                wants_stream = bool(json.loads(body or b"{}").get("stream"))
            except Exception:
                wants_stream = False
            at = fresh_token()
            if at:
                try:
                    if wants_stream:
                        self._stream(CODING_BASE, at, body)
                    else:
                        _, raw = _chat(CODING_BASE, at, body)
                        self._reply(200, raw)
                    return
                except urllib.error.HTTPError as e:
                    sys.stderr.write(f"[kimi-relay] membership call failed http {e.code} — trying fallback\n")
                except (BrokenPipeError, ConnectionResetError):
                    return
            or_key = os.environ.get("OPENROUTER_API_KEY", "")
            if or_key:
                ok, n = _fallback_allowed()
                if not ok:
                    self._reply(429, json.dumps({"error": {"message":
                        f"kimi-relay fallback daily cap reached ({n}) — raise KIMI_RELAY_FALLBACK_DAILY_CAP or wait for reset"}}).encode())
                    return
                try:
                    # fallback is always non-streamed: whole degraded reply
                    body_ns = body
                    if wants_stream:
                        b = json.loads(body)
                        b["stream"] = False
                        body_ns = json.dumps(b).encode()
                    _, raw = _chat("https://openrouter.ai/api/v1", or_key,
                                   body_ns, model_map=OR_SLUGS)
                    _fallback_record()
                    if wants_stream:
                        self._reply_as_sse(raw)
                    else:
                        self._reply(200, raw)
                    return
                except urllib.error.HTTPError as e:
                    self._reply(e.code, e.read())
                    return
            self._reply(502, json.dumps({"error": {
                "message": "kimi membership call failed and no OPENROUTER_API_KEY fallback configured"}}).encode())

        def _stream(self, base, key, body):
            req = urllib.request.Request(base + "/chat/completions", data=body,
                                         headers={"Content-Type": "application/json",
                                                  "Authorization": "Bearer " + key,
                                                  "Accept": "text/event-stream",
                                                  "User-Agent": "space-duck-kimi-relay/0.3"})
            with urllib.request.urlopen(req, timeout=300) as r:
                self.send_response(200)
                self.send_header("Content-Type",
                                 r.headers.get("Content-Type", "text/event-stream"))
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                while True:
                    chunk = r.read(4096)
                    if not chunk:
                        break
                    self.wfile.write(f"{len(chunk):X}\r\n".encode())
                    self.wfile.write(chunk + b"\r\n")
                    self.wfile.flush()
                self.wfile.write(b"0\r\n\r\n")

        def _reply_as_sse(self, raw):
            payload = _sse_wrap(raw)
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _reply(self, code, raw):
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

    secret = proxy_secret()
    H.timeout = 120
    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    srv.daemon_threads = True
    print(f"kimi-relay proxy on http://127.0.0.1:{port}/v1/chat/completions")
    if secret:
        print(f"api key (required): {secret}")
        print(f"(also at {PROXY_SECRET_PATH}; disable with KIMI_RELAY_NO_AUTH=1)")
    else:
        print("⚠️ auth disabled (KIMI_RELAY_NO_AUTH=1) — any local process can spend your quota")
    srv.serve_forever()


SERVICE_NAME = "kimi-relay"


def _script_path():
    return os.path.abspath(__file__)


SERVICE_ENV_VARS = ("OPENROUTER_API_KEY", "KIMI_RELAY_FALLBACK_DAILY_CAP",
                    "KIMI_CLIENT_ID", "KIMI_AUTH_HOST", "KIMI_CODING_BASE")
SERVICE_ENV_FILE = os.path.join(CRED_DIR, "relay.env")


def _service_env():
    return {k: os.environ[k] for k in SERVICE_ENV_VARS if os.environ.get(k)}


def _plist_env(env):
    if not env:
        return ""
    kv = "".join(f"\n    <key>{k}</key><string>{v}</string>" for k, v in env.items())
    return f"\n  <key>EnvironmentVariables</key><dict>{kv}\n  </dict>"


def install_service(port):
    import subprocess
    py = sys.executable or "python3"
    env = _service_env()
    if env:
        print("capturing into service env: " + ", ".join(env))
    if sys.platform == "darwin":
        plist_dir = os.path.expanduser("~/Library/LaunchAgents")
        os.makedirs(plist_dir, exist_ok=True)
        plist = os.path.join(plist_dir, "com.spaceduckling.kimi-relay.plist")
        with open(plist, "w") as f:
            f.write(f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>com.spaceduckling.kimi-relay</string>
  <key>ProgramArguments</key><array>
    <string>{py}</string><string>{_script_path()}</string>
    <string>serve</string><string>{port}</string>
  </array>
  <key>RunAtLoad</key><true/>
  <key>KeepAlive</key><true/>{_plist_env(env)}
</dict></plist>
""")
        os.chmod(plist, 0o600)
        subprocess.run(["launchctl", "unload", plist], capture_output=True)
        r = subprocess.run(["launchctl", "load", plist], capture_output=True, text=True)
        if r.returncode != 0:
            print("launchctl load failed: " + (r.stderr or r.stdout), file=sys.stderr)
            return 1
        print(f"✅ launchd agent installed + started ({plist}), proxy on 127.0.0.1:{port}")
        return 0
    unit_dir = os.path.expanduser("~/.config/systemd/user")
    os.makedirs(unit_dir, exist_ok=True)
    unit = os.path.join(unit_dir, SERVICE_NAME + ".service")
    # Secrets go in a 0600 EnvironmentFile, NOT inlined into the unit — a unit
    # is world-readable by convention, so an inline OPENROUTER_API_KEY would
    # leak. The proxy reads them from this file via systemd's EnvironmentFile.
    env_line = ""
    if env:
        os.makedirs(CRED_DIR, mode=0o700, exist_ok=True)
        fd = os.open(SERVICE_ENV_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            for k, v in env.items():
                f.write(f"{k}={v}\n")
        env_line = f"EnvironmentFile={SERVICE_ENV_FILE}\n"
    with open(unit, "w") as f:
        f.write(f"""[Unit]
Description=space-duck-kimi-relay local membership proxy
After=network-online.target

[Service]
ExecStart={py} {_script_path()} serve {port}
{env_line}Restart=always
RestartSec=3

[Install]
WantedBy=default.target
""")
    os.chmod(unit, 0o600)
    for args in (["daemon-reload"], ["enable", "--now", SERVICE_NAME]):
        r = subprocess.run(["systemctl", "--user"] + args, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"systemctl --user {' '.join(args)} failed: {r.stderr or r.stdout}",
                  file=sys.stderr)
            print("(headless box? enable lingering: loginctl enable-linger $USER)",
                  file=sys.stderr)
            return 1
    print(f"✅ systemd user service installed + started ({unit}), proxy on 127.0.0.1:{port}")
    print("tip: sudo loginctl enable-linger $USER  # keeps it running after logout/reboot")
    return 0


def uninstall_service():
    import subprocess
    if sys.platform == "darwin":
        plist = os.path.expanduser("~/Library/LaunchAgents/com.spaceduckling.kimi-relay.plist")
        subprocess.run(["launchctl", "unload", plist], capture_output=True)
        try:
            os.remove(plist)
            print("launchd agent removed")
        except FileNotFoundError:
            print("no launchd agent installed")
        return 0
    subprocess.run(["systemctl", "--user", "disable", "--now", SERVICE_NAME],
                   capture_output=True)
    unit = os.path.expanduser("~/.config/systemd/user/" + SERVICE_NAME + ".service")
    try:
        os.remove(unit)
        subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
        print("systemd user service removed")
    except FileNotFoundError:
        print("no service installed")
    try:
        os.remove(SERVICE_ENV_FILE)
    except FileNotFoundError:
        pass
    return 0


def status(port):
    rec = _load()
    if not rec:
        print("credentials : ❌ not signed in")
    else:
        alive = rec.get("expires_at", 0) - 60 > time.time()
        print(f"credentials : ✅ present ({'access token fresh' if alive else 'will refresh on next use'})")
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=3) as r:
            ok = r.status == 200
    except Exception:
        ok = False
    print(f"proxy :{port} : {'✅ up' if ok else '❌ down'}")
    s = proxy_secret()
    print(f"proxy auth  : {'✅ api key = ' + s if s else '⚠️ disabled (KIMI_RELAY_NO_AUTH=1)'}")
    _, n = _fallback_allowed()
    print(f"fallback    : {n}/{FALLBACK_DAILY_CAP} OpenRouter calls today"
          + ("" if os.environ.get("OPENROUTER_API_KEY") else " (no OPENROUTER_API_KEY set)"))
    _print_service_env_drift()
    return 0 if (rec and ok) else 1


def _print_service_env_drift():
    """Compare env vars captured into the installed service unit against the
    current process env; warn on drift by NAME only (never values)."""
    if sys.platform == "darwin":
        plist = os.path.expanduser("~/Library/LaunchAgents/com.spaceduckling.kimi-relay.plist")
        if os.path.exists(plist):
            print("service env : (not checked on macOS — inspect plist manually)")
        return
    try:
        with open(SERVICE_ENV_FILE) as f:
            text = f.read()
    except FileNotFoundError:
        return
    captured = {}
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#") or "=" not in s:
            continue
        k, v = s.split("=", 1)
        captured[k] = v
    if not captured:
        print("service env : (no vars in relay.env)")
        return
    drifted = [k for k, v in captured.items() if os.environ.get(k) != v]
    missing = [k for k in captured if os.environ.get(k) is None]
    if drifted:
        print("service env : ⚠️ drift vs current env: " + ", ".join(sorted(drifted))
              + " — reinstall service to refresh, or restart the service after exporting new values")
    else:
        print("service env : ✅ " + str(len(captured)) + " captured var(s) match current env")
    if missing and not drifted:
        # missing is already a subset of drifted if any values disagree; keep quiet otherwise
        pass


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "login"
    if cmd == "login":
        return login()
    if cmd == "token":
        at = fresh_token()
        if at:
            print(at)
            return 0
        return 1
    if cmd == "probe":
        return probe()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8471
    if cmd == "serve":
        return serve(port)
    if cmd == "install-service":
        return install_service(port)
    if cmd == "uninstall-service":
        return uninstall_service()
    if cmd == "status":
        return status(port)
    if cmd == "logout":
        try:
            os.remove(CRED_PATH)
            print("credentials deleted")
        except FileNotFoundError:
            print("not signed in")
        return 0
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
