# -*- coding: utf-8 -*-
"""
Buddy 应用 OAuth 回调 · 腾讯云函数（SCF）版
=============================================
形态：事件函数 + API 网关触发器（即"HTTP 触发器"）。
业务逻辑与 buddy_oauth_callback_local.py 完全一致（标准 OAuth 2.x 授权码流程），
仅入口壳从"本地 HTTP 服务器"换成"main_handler(event, context)"。

部署：
  1. 腾讯云控制台 -> 云函数 SCF -> 新建 -> 从头开始 -> 事件函数 -> Python 3.x
  2. 把本文件全部内容粘贴到在线编辑器（入口函数名保持 main_handler）
  3. 函数配置 -> 环境变量：WB_CLIENT_ID / WB_CLIENT_SECRET /
     WB_TOKEN_ENDPOINT / WB_REDIRECT_URI（/ WB_AUTH_ENDPOINT 可选）
  4. 触发管理 -> 创建触发器 -> API 网关触发器 -> 保存，获得 https 访问路径
  5. 将该路径填到开放平台模块 1「授权回调 URL」，域名填入「可信 Origin」

费用：SCF 有每月免费额度，本端点仅在用户绑定时被调用，实际成本趋近于零。
"""

import hashlib
import hmac
import json
import os
import secrets
import time
import urllib.parse
import urllib.request

# ---------------------------------------------------------------- 配置（函数环境变量）

CLIENT_ID = os.environ.get("WB_CLIENT_ID", "")
CLIENT_SECRET = os.environ.get("WB_CLIENT_SECRET", "")
AUTH_ENDPOINT = os.environ.get("WB_AUTH_ENDPOINT", "")
TOKEN_ENDPOINT = os.environ.get("WB_TOKEN_ENDPOINT", "")
REDIRECT_URI = os.environ.get("WB_REDIRECT_URI", "")
STATE_SECRET = os.environ.get("WB_STATE_SECRET", "") or secrets.token_hex(16)

# 演示用内存令牌库（同一函数实例复用期间有效，冷启动后清空）。
# 生产环境请改用加密数据库 / KMS，按用户维度隔离，禁止明文落盘。
TOKENS = {}

# ---------------------------------------------------------------- state（防 CSRF）

def make_state() -> str:
    """生成带 HMAC 签名的 state：timestamp.nonce.signature"""
    payload = "%d.%s" % (int(time.time()), secrets.token_hex(8))
    sig = hmac.new(STATE_SECRET.encode(), payload.encode(), hashlib.sha256).hexdigest()[:24]
    return "%s.%s" % (payload, sig)


def check_state(state: str, max_age_sec: int = 600) -> bool:
    """校验 state：签名正确且未过期（默认 10 分钟）。"""
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
    令牌交换地址与返回字段名以开放平台官方文档为准。"""
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

# ---------------------------------------------------------------- 页面与响应

PAGE = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>
body{{font-family:system-ui,sans-serif;display:flex;justify-content:center;align-items:center;min-height:90vh;margin:0;background:#f6f7f9}}
.card{{background:#fff;border-radius:12px;padding:32px 40px;max-width:520px;box-shadow:0 4px 24px rgba(0,0,0,.08)}}
h1{{font-size:20px;margin:0 0 12px}} p{{color:#444;line-height:1.7}} code{{background:#f0f1f3;padding:2px 6px;border-radius:4px}}
</style></head><body><div class="card"><h1>{title}</h1>{body}</div></body></html>"""


def _resp(status: int, title: str, body_html: str) -> dict:
    """API 网关触发器要求的集成响应格式。"""
    return {
        "isBase64Encoded": False,
        "statusCode": status,
        "headers": {"Content-Type": "text/html; charset=utf-8"},
        "body": PAGE.format(title=title, body=body_html),
    }

# ---------------------------------------------------------------- 回调主逻辑

def handle_callback(q: dict) -> dict:
    # 0) 用户在授权页拒绝/取消
    if q.get("error"):
        desc = q.get("error_description", "")
        return _resp(400, "授权未完成", "<p>授权方返回错误：<code>%s</code> %s</p><p>请返回 WorkBuddy 重试。</p>" % (q["error"], desc))

    code = q.get("code")
    state = q.get("state", "")

    # 1) 参数完整性
    if not code:
        return _resp(400, "回调参数缺失", "<p>缺少 <code>code</code> 参数。</p>")

    # 2) state 校验（防 CSRF，必做）
    if not check_state(state):
        return _resp(400, "安全校验失败", "<p><code>state</code> 校验未通过（伪造或已过期），本次回调已拒绝。</p>")

    # 3) 授权码换令牌
    try:
        token = exchange_code(code)
    except Exception as exc:
        return _resp(502, "令牌交换失败", "<p>%s</p><p>请检查函数环境变量 WB_TOKEN_ENDPOINT / WB_CLIENT_SECRET 后重试。</p>" % type(exc).__name__)

    # 4) 令牌存储（演示：内存 + 掩码日志；生产：加密存储，按用户维度隔离）
    access = str(token.get("access_token", ""))
    TOKENS[hashlib.sha256(access.encode()).hexdigest()[:12]] = {
        "stored_at": int(time.time()),
        "expires_in": token.get("expires_in"),
        "scope": token.get("scope"),
    }
    masked = ("***" + access[-4:]) if len(access) >= 4 else "***"
    print("[callback] token stored, access_token=%s expires_in=%s" % (masked, token.get("expires_in")))

    # 5) 给用户的人机回执
    return _resp(200, "绑定成功", "<p>授权已完成，你可以关闭本页面，返回 WorkBuddy 继续使用。</p>")

# ---------------------------------------------------------------- 入口

def main_handler(event, context):
    """SCF 事件函数入口。API 网关触发器把 HTTP 请求封装进 event。"""
    path = (event.get("path") or "/").rstrip("/")
    query = event.get("queryString") or {}

    if path.endswith("oauth/callback"):
        return handle_callback(query)

    # 健康检查 / 说明页
    demo = ""
    if AUTH_ENDPOINT and CLIENT_ID and REDIRECT_URI:
        link_query = urllib.parse.urlencode({
            "response_type": "code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "state": make_state(),
            # "scope": "..."  # 按官方文档填入授权列表声明的项
        })
        demo = '<p>演示授权链接（真实环境由平台"绑定应用"弹窗触发）：<br><code>%s?%s</code></p>' % (AUTH_ENDPOINT, link_query)
    return _resp(200, "Buddy 应用 OAuth 回调端点",
                 "<p>云函数运行中。回调路径：<code>/oauth/callback</code></p>%s" % demo)
