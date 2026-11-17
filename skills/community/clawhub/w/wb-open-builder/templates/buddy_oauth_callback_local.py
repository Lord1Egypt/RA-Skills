#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Buddy 应用 OAuth 授权回调端点 · 参考实现
=========================================
职责（标准 OAuth 2.x 授权码流程的接收方）：
  输入  : GET /oauth/callback?code=...&state=...  （授权方重定向过来的授权码）
  处理  : 校验 state 防 CSRF -> 用授权码 + Client Secret 换取访问令牌
  输出  : 令牌安全存储 -> 给用户返回"绑定成功"页面

依赖：仅 Python 标准库，无需 pip install。
运行：python oauth-callback-demo.py  （默认监听 8080）

环境变量配置（严禁把 Secret 写进代码或任何提交入库的文件）：
  WB_CLIENT_ID       应用创建后平台颁发的 Client ID
  WB_CLIENT_SECRET   应用创建后平台颁发的 Client Secret（仅展示一次）
  WB_AUTH_ENDPOINT   授权页地址（拼"发起授权"链接用，以开放平台官方文档为准）
  WB_TOKEN_ENDPOINT  令牌交换地址（以开放平台官方文档为准）
  WB_REDIRECT_URI    与模块 1 填写的"授权回调 URL"完全一致
  WB_STATE_SECRET    state 签名密钥，不设置则每次启动随机生成（重启后旧 state 失效）
  PORT               监听端口，默认 8080

注意：授权页地址、令牌交换地址、scope 枚举值等平台特定参数，
      本文件一律走环境变量占位，请按开放平台官方文档填入真实值。
"""

import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# ---------------------------------------------------------------- 配置

CLIENT_ID = os.environ.get("WB_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("WB_CLIENT_SECRET", "")
AUTH_ENDPOINT = os.environ.get("WB_AUTH_ENDPOINT", "")
TOKEN_ENDPOINT = os.environ.get("WB_TOKEN_ENDPOINT", "")
REDIRECT_URI = os.environ.get("WB_REDIRECT_URI", "http://localhost:8080/oauth/callback")
STATE_SECRET = os.environ.get("WB_STATE_SECRET", "") or secrets.token_hex(16)
PORT = int(os.environ.get("PORT", "8080"))

# 演示用内存令牌库。生产环境禁止明文落盘：
# 应存入加密数据库 / 密钥管理系统（KMS），并按用户维度隔离。
TOKENS = {}

# ---------------------------------------------------------------- state（防 CSRF）

def make_state() -> str:
    """生成带 HMAC 签名的 state：timestamp.nonce.signature

    发起授权时把 state 拼进授权链接；回调时必须原样带回。
    攻击者无法伪造签名，因此回调可以被信任。
    """
    payload = "%d.%s" % (int(time.time()), secrets.token_hex(8))
    sig = hmac.new(STATE_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    return "%s.%s" % (payload, sig)


def check_state(state: str, max_age_sec: int = 600) -> bool:
    """校验回调带回的 state：签名正确且未过期（默认 10 分钟）。"""
    try:
        ts, nonce, sig = state.split(".")
        payload = "%s.%s" % (ts, nonce)
    except ValueError:
        return False
    expect = hmac.new(STATE_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    if not hmac.compare_digest(expect, sig):
        return False
    try:
        return (time.time() - int(ts)) < max_age_sec
    except ValueError:
        return False

# ---------------------------------------------------------------- 令牌交换

def exchange_code(code: str) -> dict:
    """授权码换访问令牌（application/x-www-form-urlencoded，标准授权码流程）。

    返回示例（字段名以官方文档为准）：access_token / refresh_token / expires_in / scope
    """
    if not TOKEN_ENDPOINT:
        raise RuntimeError("WB_TOKEN_ENDPOINT 未配置（请按官方文档填入令牌交换地址）")
    form = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    req = urllib.request.Request(
        TOKEN_ENDPOINT,
        data=urllib.parse.urlencode(form).encode("utf-8"),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))

# ---------------------------------------------------------------- 页面模板

PAGE = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
body{{font-family:system-ui,sans-serif;display:flex;justify-content:center;align-items:center;min-height:90vh;margin:0;background:#f6f7f9}}
.card{{background:#fff;border-radius:12px;padding:32px 40px;max-width:520px;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
h1{{font-size:20px;margin:0 0 12px}} p{{color:#444;line-height:1.7}} code{{background:#f0f1f3;padding:2px 6px;border-radius:4px}}
</style></head><body><div class="card"><h1>{title}</h1>{body}</div></body></html>"""

# ---------------------------------------------------------------- HTTP 处理

class Handler(BaseHTTPRequestHandler):
    server_version = "BuddyOAuthCallback/1.0"

    def _send_html(self, title: str, body: str, status: int = 200):
        data = PAGE.format(title=title, body=body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/oauth/callback":
            self._handle_callback(urllib.parse.parse_qs(parsed.query))
        elif parsed.path == "/":
            self._handle_index()
        else:
            self._send_html("404", "<p>Not Found</p>", status=404)

    def log_message(self, fmt, *args):  # 日志脱敏：不打 query string（含 code/state）
        print("%s - %s" % (self.address_string(), fmt % (args[0].split(" ")[0],) if args else fmt))

    # ---- 首页：说明 + 演示"发起授权"链接的构造方式
    def _handle_index(self):
        demo_link = ""
        if AUTH_ENDPOINT and CLIENT_ID:
            query = urllib.parse.urlencode({
                "response_type": "code",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "state": make_state(),
                # "scope": "..."   # 按官方文档填入授权列表声明的项
            })
            demo_link = '<p>演示授权链接（真实环境由平台"绑定应用"弹窗触发）：<br><code>%s?%s</code></p>' % (AUTH_ENDPOINT, query)
        self._send_html(
            "Buddy 应用 OAuth 回调端点",
            "<p>服务运行中。回调地址：<code>%s</code></p>"
            "<p>用户授权完成后，授权方会重定向到该地址并携带 <code>code</code> 与 <code>state</code>。</p>%s" % (REDIRECT_URI, demo_link),
        )

    # ---- 回调主逻辑
    def _handle_callback(self, q):
        # 0) 用户在授权页拒绝/取消：标准错误参数 error / error_description
        if "error" in q:
            desc = q.get("error_description", [""])[0]
            self._send_html("授权未完成", "<p>授权方返回错误：<code>%s</code> %s</p><p>请返回 WorkBuddy 重试。</p>" % (q["error"][0], desc), status=400)
            return

        code = q.get("code", [None])[0]
        state = q.get("state", [""])[0]

        # 1) 参数完整性
        if not code:
            self._send_html("回调参数缺失", "<p>缺少 <code>code</code> 参数。</p>", status=400)
            return

        # 2) state 校验（防 CSRF，必做）
        if not check_state(state):
            self._send_html("安全校验失败", "<p><code>state</code> 校验未通过（伪造或已过期），本次回调已拒绝。</p>", status=400)
            return

        # 3) 授权码换令牌
        try:
            token = exchange_code(code)
        except Exception as exc:
            self._send_html("令牌交换失败", "<p>%s</p><p>请检查 WB_TOKEN_ENDPOINT / Client Secret 配置后重试。</p>" % type(exc).__name__, status=502)
            return

        # 4) 令牌存储（演示：内存；生产：加密数据库/KMS，按用户维度隔离）
        access = str(token.get("access_token", ""))
        TOKENS[hashlib.sha256(access.encode()).hexdigest()[:12]] = {
            "stored_at": int(time.time()),
            "expires_in": token.get("expires_in"),
            "scope": token.get("scope"),
            # refresh_token 如需离线续期，单独加密保存，有效期以官方文档为准
        }
        masked = ("***" + access[-4:]) if len(access) >= 4 else "***"
        print("[callback] token stored, access_token=%s expires_in=%s" % (masked, token.get("expires_in")))

        # 5) 给用户的人机回执
        self._send_html("绑定成功", "<p>授权已完成，你可以关闭本页面，返回 WorkBuddy 继续使用。</p>")

# ---------------------------------------------------------------- 启动

def main():
    missing = [k for k, v in {
        "WB_CLIENT_ID": CLIENT_ID,
        "WB_CLIENT_SECRET": CLIENT_SECRET,
    }.items() if not v]
    if missing:
        print("[warn] 缺少环境变量: %s（换令牌会失败，请先按官方文档配置）" % ", ".join(missing))
    print("OAuth 回调端点已启动: http://0.0.0.0:%d" % PORT)
    print("回调路径: /oauth/callback   生产环境必须通过 HTTPS 暴露，并与模块 1 填写的授权回调 URL 一致")
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
