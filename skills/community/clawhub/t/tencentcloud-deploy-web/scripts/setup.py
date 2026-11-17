#!/usr/bin/env python3
"""腾讯云首次接入向导：在本机打开一个网页，带非技术用户完成「注册 → 建策略 → 建子用户 → 交密钥」。
纯标准库，Python 3.8+，Windows/macOS/Linux 通用。

为什么用网页：用户不需要打开终端；密钥只在用户浏览器 → 本机进程 → 本机文件之间流转，
不经过 agent 的对话，模型看不到。网页只监听 127.0.0.1，地址里带一次性 token，保存成功后自动退出。

用法（agent 来运行；它会阻塞到用户完成或超时，建议在后台运行）：
    python setup.py [--profile agent-ops] [--region ap-hongkong] [--no-browser] [--timeout 1800] [--force] [--no-brand]

页面底部有出品方（龙虾学院）的品牌标识和官网链接，只是普通链接：不加载外部资源、不追踪。
用户不想看就加 --no-brand（或设置环境变量 CLAW_BRAND=0）。**不要修改 assets/ 下的页面源码**——
密钥表单和校验逻辑都在那里，改坏了用户就卡住了；页面缺失或被改坏时，脚本会自动退回内置的极简页面。

stderr 会先打印网页地址（浏览器没自动打开时，把地址发给用户）。
结束时 stdout 输出一行 JSON：
    {"ok": true,  "profile": "agent-ops", "uin": "...", "access": {...}}
    {"ok": false, "reason": "timeout|already_configured|..."}
stdout 里永远不会出现密钥。
"""
import argparse
import base64
import html
import json
import re
import os
import secrets
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tcapi  # noqa: E402

POLICY = (HERE.parent / "references" / "agent-ops-policy.json").read_text(encoding="utf-8")

FRIENDLY = {
    "AuthFailure.SecretIdNotFound": "SecretId 不对：请检查是否完整复制（以 AKID 开头），或者这个密钥已经被删除。",
    "AuthFailure.SignatureFailure": "SecretKey 不对：请重新复制 SecretKey，注意不要多带空格。",
    "AuthFailure.SecretIdDisabled": "这个密钥已被禁用，请在子用户详情里启用它，或者新建一个。",
    "Local.NetworkError": "连不上腾讯云，请检查网络后重试。",
}

ASSETS = HERE.parent / "assets"
# 页面必须具备的功能元素；scripts/setup_page.py 缺失或被改坏时，自动退回下面的内置极简页面
REQUIRED = ("__TOKEN__", "__POLICY__", 'id="sid"', 'id="skey"', 'id="savebtn"', 'id="msg"', 'id="policy"')
FALLBACK_PAGE = """<!doctype html><html lang="zh"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>连接腾讯云 · 首次设置</title><style>body{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;max-width:720px;margin:24px auto;padding:0 16px;line-height:1.7}
a.b,button{display:inline-block;background:#0052d9;color:#fff;border:0;border-radius:6px;padding:8px 14px;margin:4px 4px 4px 0;text-decoration:none;cursor:pointer}
input{width:100%;padding:8px;margin:4px 0 10px;box-sizing:border-box;font-family:monospace}textarea{width:100%;height:100px;font-family:monospace;font-size:12px}
#msg{display:none;white-space:pre-wrap;padding:10px;border-radius:6px}.ok{background:#e8f8f0}.err{background:#fdecee}</style></head><body>
<h1>把你的 AI 助手接入腾讯云</h1>
<p>能做：配置解析、加速、证书，管理已有服务器。做不了：花钱、删除或重装服务器、删除或转让域名、查看实名资料。密钥只保存在这台电脑上。随时可在「访问管理 → 用户列表 → agent-ops」禁用。</p>
<h2>1 注册并实名（已有账号可跳过）</h2><a class="b" href="https://cloud.tencent.com/register" target="_blank">注册</a><a class="b" href="https://console.cloud.tencent.com/developer/auth" target="_blank">实名认证</a>
<h2>2 建权限策略</h2><a class="b" href="https://console.cloud.tencent.com/cam/policy" target="_blank">打开策略页</a><button onclick="copyPolicy()">复制策略内容</button><span id="copied"></span>
<p>新建自定义策略 → 按策略语法创建 → 空白模板；名称填 agent-ops-web；清空内容框后粘贴，完成。</p><details><summary>策略内容</summary><textarea id="policy" readonly>__POLICY__</textarea></details>
<h2>3 建子账号</h2><a class="b" href="https://console.cloud.tencent.com/cam" target="_blank">打开用户列表</a>
<p>新建用户 → 自定义创建 → 可访问资源并接收消息；用户名 agent-ops；只勾「编程访问」；权限只勾 agent-ops-web；完成后复制 SecretId / SecretKey。</p>
<h2>4 填入密钥</h2><label>SecretId</label><input id="sid" autocomplete="off"><label>SecretKey</label><input id="skey" type="password" autocomplete="off">
<button id="savebtn" onclick="save()">保存并验证</button><div id="msg"></div>
<script>const T="__TOKEN__";function copyPolicy(){const t=document.getElementById('policy');(navigator.clipboard?navigator.clipboard.writeText(t.value):Promise.reject()).catch(()=>{t.parentElement.open=true;t.select();document.execCommand('copy')}).finally(()=>{document.getElementById('copied').textContent=' 已复制'})}
async function save(){const m=document.getElementById('msg'),b=document.getElementById('savebtn');b.disabled=true;try{const r=await fetch('/save?t='+T,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({sid:document.getElementById('sid').value,skey:document.getElementById('skey').value})});const d=await r.json();m.className=d.ok?'ok':'err';m.textContent=d.text;m.style.display='block';if(d.ok){document.getElementById('skey').value='';return}}catch(e){m.className='err';m.textContent='页面和本机程序断开了，请让 AI 助手重新打开。';m.style.display='block'}b.disabled=false}</script></body></html>"""


def load_page():
    """读取页面模板 scripts/setup_page.py；模块缺失或缺少功能元素时，退回内置的极简页面。"""
    try:
        import importlib
        import setup_page
        importlib.reload(setup_page)
        page = setup_page.PAGE
        if all(k in page for k in REQUIRED):
            return page
    except Exception:   # 模板被删除、改坏都不能影响向导本身
        pass
    return FALLBACK_PAGE


def render_brand(page: str, enabled: bool) -> str:
    """把出品方品牌填进页面的 <!--BRAND:xxx--> 位置。
    assets/brand.json 只存文字和链接（不存 HTML），这里转义后套进固定的 HTML 结构——品牌数据无法向密钥页面注入任何标记或脚本。
    品牌是可选的：关闭开关、文件缺失或内容不合法时，位置留空，向导照常可用。"""
    slots = {}
    if enabled:
        try:
            b = json.loads((ASSETS / "brand.json").read_text(encoding="utf-8"))
            e = {k: html.escape(str(b[k]), quote=True) for k in ("name", "name_en", "done_text", "url", "link_text")}
            if not e["url"].startswith("https://"):
                raise ValueError("brand url 必须是 https 链接")
            logo = b.get("logo", "")   # 内嵌 PNG（市场网页上传会丢二进制文件，所以不单独放图片）
            img = (f'<img src="{logo}" alt="">'
                   if re.fullmatch(r"data:image/png;base64,[A-Za-z0-9+/]+=*", logo or "") else "")
            a = f'<a href="{e["url"]}" target="_blank" rel="noopener noreferrer">{e["link_text"]}</a>'
            slots = {
                "header": f'<header class="top"><div class="in">{img}<span class="brand">{e["name"]}<small>{e["name_en"]}</small></span></div></header>',
                "done": f'<p class="tip" style="color:#fff;opacity:.85;margin-top:14px">{e["done_text"]} '
                        f'<a href="{e["url"]}" target="_blank" rel="noopener noreferrer" style="color:#fff">{e["link_text"]}</a></p>',
                "footer": f'<footer><div class="in"><span>{img}{e["name"]} {e["name_en"]}</span>{a}</div></footer>',
            }
        except Exception:   # 品牌是可选的：任何问题都不能影响向导本身
            slots = {}
    for name in ("header", "done", "footer"):
        page = page.replace(f"<!--BRAND:{name}-->", slots.get(name, ""))
    return page


# 本页面处理密钥：浏览器层面禁止加载任何外部脚本/样式/图片/字体，也禁止向本机以外发请求。
# 推广内容只是普通超链接（用户点击后在新标签页打开）。
CSP = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
       "img-src data:; connect-src 'self'; form-action 'none'; base-uri 'none'; frame-ancestors 'none'")


def verify(sid: str, skey: str, region: str):
    """返回 (ok, 给用户看的文字, 给 agent 的结果字典)。"""
    sid, skey = sid.strip(), skey.strip()
    if not sid.startswith("AKID") or len(skey) < 20:
        return False, "格式不对：SecretId 应该以 AKID 开头，SecretKey 是一长串字母和数字。请重新复制。", None
    try:
        ident = tcapi.call_with((sid, skey), "sts", "GetCallerIdentity", region=region)
    except tcapi.TcError as e:
        return False, FRIENDLY.get(e.code, f"腾讯云没有通过验证（{e.code}）。请检查后重试。"), None
    if ident.get("Type") != "CAMUser":
        return False, ("这是主账号的密钥，权限太大，不能交给 AI 助手。\n"
                       "请按第 3 步创建子账号 agent-ops，然后用它的密钥。\n"
                       "（建议到「访问密钥」页面把刚才这个主账号密钥禁用。）"), None
    access = {}
    for svc, action, params in (("dnspod", "DescribeDomainList", {"Limit": 1}),
                                ("lighthouse", "DescribeInstances", {}),
                                ("teo", "DescribeZones", {})):
        try:
            tcapi.call_with((sid, skey), svc, action, params, region=region)
            access[svc] = "allowed"
        except tcapi.TcError as e:
            # 查不到数据只能算"未验证"（资源校验可能先于鉴权），不算放行也不算拒绝
            access[svc] = "unverified" if e.code.startswith("ResourceNotFound") else "denied"
    if "denied" in access.values():
        return False, ("密钥是对的，但这个子账号还没有权限。\n"
                       "请到「用户列表」→ agent-ops → 关联策略，勾选 agent-ops-web，然后再点一次「保存并验证」。"), None
    # 权限也不能过大：计费、管理子用户、云服务器 CVM 都必须被拒绝（说明只挂了 agent-ops-web）
    too_much = []
    for svc, action in (("billing", "DescribeAccountBalance"), ("cam", "ListUsers"), ("cvm", "DescribeInstances")):
        try:
            tcapi.call_with((sid, skey), svc, action, {}, region=region)
            too_much.append(svc)
        except tcapi.TcError as e:
            if "Unauthorized" not in e.code and "NoPermission" not in e.code and "CamNoAuth" not in e.code:
                return False, f"暂时没法确认这个子账号的权限范围（{e.code}），请稍后再点一次「保存并验证」。", None
    if too_much:
        return False, ("这个子账号的权限比需要的大（能操作：" + "、".join(too_much) + "）。\n"
                       "请到「用户列表」→ agent-ops → 权限，只保留 agent-ops-web 一个策略，然后再点一次「保存并验证」。"), None
    return True, "", {"uin": ident.get("UserId"), "owner_uin": ident.get("AccountId"), "access": access}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", default=tcapi.DEFAULT_PROFILE)
    ap.add_argument("--region", default="ap-hongkong")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--no-browser", action="store_true")
    ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--force", action="store_true", help="已有可用凭证时也重新设置")
    ap.add_argument("--no-brand", action="store_true",
                    help="不显示出品方（龙虾学院）的品牌标识和官网链接。用户不想看时用它，不要去改页面源码")
    a = ap.parse_args()

    cred = tcapi.load_credential(a.profile) if not a.force else None
    if cred:
        ok, _, info = verify(cred[0], cred[1], a.region)   # 已有凭证也要过同样的检查：子账号 + 权限不多不少
        if ok:
            print(json.dumps({"ok": True, "reason": "already_configured", "profile": a.profile, **info},
                             ensure_ascii=False))
            return 0
        # 旧凭证失效、是主账号密钥、或权限不对 → 继续走向导，重新录一对

    token = secrets.token_urlsafe(16)
    brand_on = not a.no_brand and os.environ.get("CLAW_BRAND", "1") != "0"
    page = render_brand(load_page(), brand_on)
    page = page.replace("__POLICY__", html.escape(POLICY)).replace("__TOKEN__", token).encode("utf-8")
    result = {}
    done = threading.Event()

    used = threading.Event()   # 保存成功后 token 立即作废，不能重复提交
    MAX_BODY = 4096

    class H(BaseHTTPRequestHandler):
        def _local_request(self):
            """只接受发给本机这个端口的请求：防 DNS 重绑定（Host）与其他网页跨站提交（Origin）。"""
            port = srv.server_address[1]
            ok_hosts = {f"127.0.0.1:{port}", f"localhost:{port}"}
            if self.headers.get("Host", "") not in ok_hosts:
                return False
            origin = self.headers.get("Origin")
            return origin is None or origin in {f"http://{h}" for h in ok_hosts}

        def log_message(self, *args):
            pass  # 不打印访问日志，以免误打出请求内容

        def _send(self, code, body, ctype):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("Referrer-Policy", "no-referrer")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            q = parse_qs(urlparse(self.path).query)
            if not self._local_request() or q.get("t", [""])[0] != token or used.is_set():
                return self._send(403, "链接已失效，请让 AI 助手重新打开。".encode("utf-8"), "text/plain; charset=utf-8")
            self._send(200, page, "text/html; charset=utf-8")

        def do_POST(self):
            q = parse_qs(urlparse(self.path).query)
            if (not self._local_request() or q.get("t", [""])[0] != token or used.is_set()
                    or urlparse(self.path).path != "/save"):
                return self._send(403, b"{}", "application/json")
            try:
                n = int(self.headers.get("Content-Length", 0))
            except ValueError:
                n = MAX_BODY + 1
            if n > MAX_BODY:
                return self._send(413, b"{}", "application/json")
            try:
                d = json.loads(self.rfile.read(n).decode("utf-8"))
            except Exception:
                d = {}
            sid, skey = d.get("sid", ""), d.get("skey", "")
            if not isinstance(sid, str) or not isinstance(skey, str):
                sid, skey = "", ""
            ok, text, info = verify(sid, skey, a.region)
            if ok:
                try:
                    tcapi.save_credential(a.profile, sid, skey, a.region)
                except OSError as err:
                    body = json.dumps({"ok": False, "text": f"密钥是对的，但保存到本机失败（{err.__class__.__name__}）。请让 AI 助手检查用户目录的写入权限。"},
                                      ensure_ascii=False).encode("utf-8")
                    return self._send(200, body, "application/json; charset=utf-8")
                used.set()
                result.update({"ok": True, "profile": a.profile, **info})
                text = ("✅ 连接成功！子账号编号 " + str(info["uin"]) + "\n"
                        "密钥已保存在这台电脑上。现在可以关掉这个页面，回到 AI 助手那里继续了。")
                threading.Timer(1.5, done.set).start()
            body = json.dumps({"ok": ok, "text": text}, ensure_ascii=False).encode("utf-8")
            self._send(200, body, "application/json; charset=utf-8")

    srv = ThreadingHTTPServer(("127.0.0.1", a.port), H)
    url = f"http://127.0.0.1:{srv.server_address[1]}/?t={token}"
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"SETUP_URL {url}", file=sys.stderr, flush=True)
    if not a.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass

    finished = done.wait(a.timeout)
    srv.shutdown()
    if not finished:
        result = {"ok": False, "reason": "timeout",
                  "say": "接入页面已超时关闭。需要时告诉我，我重新打开一个。"}
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
