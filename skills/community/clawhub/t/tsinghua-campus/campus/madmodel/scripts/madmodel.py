"""madmodel.py — 清华 MAD 大模型服务（madmodel.cs.tsinghua.edu.cn）独立子模块。

解耦说明（本模块只依赖 campus 共享底座，不依赖任何外部中转/服务）：
  - 复用 base-cas 的 CDP 浏览器 + 共享 profile（已受信指纹、免短信 2FA）
  - 复用 creds 保险箱的 cas_username / cas_password
  - 复用 shared.common 的 runtime 目录（token 落 campus/runtime/madmodel/，.gitignore 已忽略）
  - 不 import 任何 campus 之外的东西；token/ticket 只存本机 runtime

机制（实测）：
  MAD 校外必须经清华 WebVPN。**WebVPN 会直接放行 MAD 的 SPA 页面**（不触发登录），
  因此必须先访问 webvpn 根触发 CAS，再进 MAD 触发 app CAS，最后用 ticket 换 JWT：
    校园统一认证(账号+密码) → CAS ?ticket= → GET /model-api/auth-login/check?ticket= → JWT
  调用：POST https://webvpn.tsinghua.edu.cn/https/<编码>/v1/chat/completions
        header: Authorization: Bearer <JWT>，cookie: wengine_vpn_ticket=<ticket>

CLI（stdout 一律 JSON；进度写 runtime/logs/campus.log）：
  madmodel.py token [--force]         # 取/刷新 JWT（必要时登录）
  madmodel.py status                  # 看缓存 token/ticket 是否有效
  madmodel.py models                  # 可用模型
  madmodel.py chat --prompt P [--model M] [--stream] [--thinking/--no-thinking] [--effort low|high|max]
  madmodel.py serve [--port 18720]    # 起本地 OpenAI 兼容代理（独立可用，供任意客户端）
"""
import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
CAMPUS = HERE.parents[2]                     # .../campus  (scripts -> madmodel -> campus)
for _p in ("base-cas", "shared", "creds"):
    sys.path.insert(0, str(CAMPUS / _p / "scripts"))
import common        # noqa: E402
import session       # noqa: E402
import browser       # noqa: E402
try:
    import vault     # noqa: E402
except Exception:
    vault = None

# 清华 MAD（Deepseek 服务）：webvpn 编码 = Wengine(wrdvpnisthebest!) + 加密后的域名
MAD_HOST = "madmodel.cs.tsinghua.edu.cn"
MAD_CODE = os.environ.get(
    "MADMODEL_WEBVPN_CODE",
    "77726476706e69737468656265737421fdf6459128346d5c300b9ae28c462a3b27469fc32211fa26a3e464",
)
WV = "https://webvpn.tsinghua.edu.cn"
MAD_URL = f"{WV}/https/{MAD_CODE}/"
API_URL = MAD_URL.rstrip("/") + "/v1/chat/completions"
CHECK_URL = MAD_URL.rstrip("/") + "/model-api/auth-login/check"

MODELS = [
    {"id": "DeepSeek-V4.1-Flash", "thinking_param": "thinking", "reasoning_field": "reasoning_content",
     "efforts": ["low", "high", "max"], "vision": False, "context": 1000000},
    {"id": "qwen3.8-27b", "thinking_param": "enable_thinking", "reasoning_field": "reasoning",
     "efforts": ["low", "medium", "xhigh"], "vision": True, "context": 262144},
    {"id": "DeepSeek-R1-W8A8", "thinking_param": None, "reasoning_field": "content",
     "efforts": ["low", "medium", "high"], "vision": False, "context": 262144},
]


# ---------- 状态（token/ticket 只落本机 runtime，.gitignore 已忽略 campus/runtime/） ----------
def _state_path():
    return common.runtime_dir("madmodel", "state.json")


def load_state():
    p = _state_path()
    try:
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def save_state(d):
    p = _state_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    try:
        os.chmod(p, 0o600)
    except Exception:
        pass


def _jwt_exp(tok):
    try:
        p = tok.split(".")[1]
        p += "=" * (-len(p) % 4)
        return int(json.loads(base64.urlsafe_b64decode(p)).get("exp", 0))
    except Exception:
        return 0


# ---------- 浏览器登录（复用 base-cas） ----------
def _cred(k):
    if vault is None:
        return ""
    try:
        return vault.vault_get(k) or ""
    except Exception:
        return ""


def _ls_token(page):
    try:
        ls = page.evaluate("() => { const o={}; for (let i=0;i<localStorage.length;i++){const k=localStorage.key(i);o[k]=localStorage.getItem(k);} return o; }")
    except Exception:
        return None
    for k, v in (ls or {}).items():
        if k == "token" and v:
            return v
        if k.endswith("_user") and v:
            try:
                j = json.loads(v)
                if isinstance(j, dict) and j.get("token"):
                    return j["token"]
            except Exception:
                pass
    return None


def _visible(page, sel):
    try:
        loc = page.locator(sel)
        return any(loc.nth(i).is_visible() for i in range(loc.count()))
    except Exception:
        return False


def _fill_cas(page, user, pwd):
    page.fill("#i_user", user)
    page.fill("#i_pass", pwd)
    page.evaluate("doLogin()")


def _fetch_token(page, user, pwd):
    """返回 (token, needs, ticket)。needs ∈ {None,'captcha','2fa','timeout'}。"""
    # 先用现有会话试一次 MAD
    try:
        page.goto(MAD_URL, wait_until="domcontentloaded", timeout=60000)
    except Exception:
        pass
    time.sleep(4)
    tok = _ls_token(page)
    if tok:
        return tok, None, None
    # 强制从 webvpn 根登录（webvpn 会直接放行 MAD SPA，不触发登录）
    try:
        page.goto(WV + "/", wait_until="domcontentloaded", timeout=60000)
    except Exception:
        pass
    time.sleep(3)
    entered = False
    deadline = time.time() + 150
    while time.time() < deadline:
        tok = _ls_token(page)
        if tok:
            break
        # CAS 登录成功页（"登录成功。正在重定向…直接跳转"）
        try:
            body = page.inner_text("body")
        except Exception:
            body = ""
        if ("登录成功" in body) or ("正在重定向" in body):
            for sel in ["a:has-text('直接跳转')", "a:has-text('跳转')"]:
                try:
                    if page.locator(sel).count() > 0:
                        page.click(sel, timeout=3000)
                        break
                except Exception:
                    pass
            time.sleep(3)
            continue
        if not entered and ("id.tsinghua" not in page.url) and ("oauth.tsinghua" not in page.url) and (MAD_CODE not in page.url):
            try:
                page.goto(MAD_URL, wait_until="domcontentloaded", timeout=60000)
            except Exception:
                pass
            entered = True
            time.sleep(3)
            continue
        if _visible(page, "#vericode") or _visible(page, "input[name=vericode]"):
            return None, "2fa", None
        if _visible(page, "#i_code") or _visible(page, "input[name=captcha]"):
            return None, "captcha", None
        if page.locator("#i_user").count() > 0:
            try:
                _fill_cas(page, user, pwd)
            except Exception:
                pass
            time.sleep(5)
            continue
        time.sleep(2)
    return tok, (None if tok else "timeout"), None


def _ticket_from(ctx):
    try:
        for c in ctx.cookies():
            if c.get("name") == "wengine_vpn_ticket":
                return c["value"]
    except Exception:
        pass
    return None


def cmd_token(force=False):
    st = load_state()
    if (not force) and st.get("token") and _jwt_exp(st["token"]) > time.time() + 2700 and st.get("ticket"):
        return {"status": "ok", "reused": True, "exp": _jwt_exp(st["token"]),
                "token_len": len(st["token"]), "ticket_len": len(st["ticket"])}
    user, pwd = _cred("cas_username"), _cred("cas_password")
    if not user or not pwd:
        return {"status": "error", "error": "no_cred", "run": "creds.py add cas_username/cas_password --value-stdin"}
    browser.start_cdp()
    pw, b, ctx, page = browser.connect_cdp()
    try:
        try:
            session.inject_cookies(ctx, "info")   # 复用既有 webvpn ticket
        except Exception:
            pass
        tok, needs, _ = _fetch_token(page, user, pwd)
        ticket = _ticket_from(ctx)
        if tok:
            save_state({"token": tok, "ticket": ticket, "ts": time.time(), "exp": _jwt_exp(tok)})
            return {"status": "ok", "reused": False, "exp": _jwt_exp(tok),
                    "token_len": len(tok), "ticket_len": len(ticket or "")}
        return {"status": "error", "error": needs or "no_token",
                "message": {"2fa": "登录触发短信二次验证，请人工完成后再试",
                            "captcha": "登录触发图形验证码，请人工完成后再试",
                            "timeout": "登录超时"}.get(needs, "未取到 token")}
    finally:
        try:
            pw.stop()
        except Exception:
            pass
        try:
            browser.stop_cdp()
        except Exception:
            pass


# ---------- 调用 API ----------
def _post(body, timeout=180):
    import urllib.request
    st = load_state()
    tok, ticket = st.get("token"), st.get("ticket")
    req = urllib.request.Request(API_URL, data=json.dumps(body).encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json",
                                          "Authorization": f"Bearer {tok}",
                                          "Cookie": f"wengine_vpn_ticket={ticket}"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def cmd_chat(a):
    # 确保 token 新鲜
    t = cmd_token(force=False)
    if t.get("status") != "ok":
        return t
    body = {"model": a.model, "messages": [{"role": "user", "content": a.prompt}],
            "stream": bool(a.stream), "max_tokens": a.max_tokens}
    if a.thinking is not None and a.model in ("DeepSeek-V4.1-Flash", "qwen3.8-27b"):
        kw = "thinking" if a.model == "DeepSeek-V4.1-Flash" else "enable_thinking"
        body["chat_template_kwargs"] = {kw: bool(a.thinking)}
    if a.effort:
        body["reasoning_effort"] = a.effort
    if a.stream:
        body["stream_options"] = {"include_usage": True}
    raw = _post(body, timeout=a.timeout)
    if a.stream:
        return {"status": "ok", "stream_raw": raw[:1500], "note": "stream 原始 SSE（截断）"}
    try:
        return {"status": "ok", "response": json.loads(raw)}
    except Exception:
        return {"status": "ok", "raw": raw[:1500]}


def cmd_models():
    return {"status": "ok", "models": MODELS}


# ---------- 本地 OpenAI 兼容代理（独立可用） ----------
def cmd_serve(port):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class H(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass

        def _send(self, code, obj):
            data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path.rstrip("/").endswith("/models"):
                self._send(200, {"object": "list", "data": [
                    {"id": m["id"], "object": "model", "owned_by": "tsinghua-madmodel"} for m in MODELS]})
            else:
                self._send(404, {"error": {"message": "not found"}})

        def do_POST(self):
            n = int(self.headers.get("Content-Length") or 0)
            try:
                body = json.loads(self.rfile.read(n) or b"{}")
            except Exception:
                return self._send(400, {"error": {"message": "invalid json"}})
            if cmd_token(force=False).get("status") != "ok":
                return self._send(503, {"error": {"message": "madmodel token unavailable"}})
            try:
                raw = _post(body, timeout=600)
            except Exception as e:
                return self._send(502, {"error": {"message": str(e)[:200]}})
            try:
                self._send(200, json.loads(raw))
            except Exception:
                self._send(200, {"error": {"message": raw[:300]}})

    srv = ThreadingHTTPServer(("127.0.0.1", port), H)
    common.log(f"[madmodel] serve on 127.0.0.1:{port} (OpenAI 兼容)")
    srv.serve_forever()


def cmd_status():
    st = load_state()
    tok = st.get("token") or ""
    return {"status": "ok", "has_token": bool(tok), "exp": _jwt_exp(tok), "valid": bool(tok) and _jwt_exp(tok) > time.time() + 60,
            "token_len": len(tok), "ticket_len": len(st.get("ticket") or ""), "ts": st.get("ts")}


def main():
    ap = argparse.ArgumentParser(prog="madmodel")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("token"); p.add_argument("--force", action="store_true")
    sub.add_parser("status")
    sub.add_parser("models")
    p = sub.add_parser("chat")
    p.add_argument("--prompt", required=True)
    p.add_argument("--model", default="DeepSeek-V4.1-Flash")
    p.add_argument("--stream", action="store_true")
    p.add_argument("--max-tokens", type=int, default=512)
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument("--effort", default=None, choices=[None, "low", "medium", "high", "xhigh", "max"])
    p.add_argument("--thinking", dest="thinking", action="store_true")
    p.add_argument("--no-thinking", dest="thinking", action="store_false")
    p.set_defaults(thinking=None)
    p = sub.add_parser("serve"); p.add_argument("--port", type=int, default=18720)
    a = ap.parse_args()

    if a.cmd == "token":
        out = cmd_token(force=a.force)
    elif a.cmd == "status":
        out = cmd_status()
    elif a.cmd == "models":
        out = cmd_models()
    elif a.cmd == "chat":
        out = cmd_chat(a)
    elif a.cmd == "serve":
        return cmd_serve(a.port)
    else:
        out = {"status": "error", "message": "unknown"}
    common.output_json(out)


if __name__ == "__main__":
    main()
