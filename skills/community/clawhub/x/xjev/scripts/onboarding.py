"""One-time localhost key form. No credentials in tool output or request logs."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import secrets
import sys
import time
import urllib.parse
import webbrowser

from common import XjevError, dump, home, probe, save_key, status

PAGE = """<!doctype html><html lang="zh-CN"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>配置 xjev</title>
<style>body{font:17px/1.7 system-ui;background:#f6f5f1;color:#202720;margin:0}main{max-width:540px;margin:12vh auto;padding:32px}h1{font-size:40px}label{display:block;margin-top:24px}input{box-sizing:border-box;width:100%;padding:14px;border:1px solid #9aab9b;border-radius:6px;font-size:18px}button{background:#234d3b;color:white;border:0;border-radius:6px;padding:13px 23px;margin-top:20px;font-size:17px}a{color:#234d3b}#result{white-space:pre-wrap}small{color:#536257}</style>
<main><h1>xjev</h1><p>连接 Jev，让 Agent 帮你比较、选择并从纠正中改进。</p>
<p>在 <a href="https://console.typesafe.ai/keys" target="_blank" rel="noreferrer">TypeSafe 控制台</a> 获取 API key，然后填在这里。</p>
<form id="form"><label for="key">Jev API key</label><input id="key" type="password" required autocomplete="off" maxlength="4096">
<button id="save">验证并保存</button></form><p id="result" role="status"></p>
<small>Key 仅保存在本机专用目录，并只发送给 TypeSafe 验证。验证会发起一次很小的 API 请求；后续决策按账户计费。不要把 key 发送到聊天中。</small></main>
<script>
const f=document.getElementById('form'), out=document.getElementById('result'), btn=document.getElementById('save');
f.onsubmit=async e=>{e.preventDefault();btn.disabled=true;out.textContent='正在验证…';
try{const r=await fetch('/configure',{method:'POST',headers:{'Content-Type':'application/json','X-Xjev-Setup':'__TOKEN__'},body:JSON.stringify({key:document.getElementById('key').value.trim()})});const d=await r.json();out.textContent=d.message;if(r.ok){document.getElementById('key').value='';f.hidden=true;}}
catch(e){out.textContent='无法连接配置服务，请重新打开配置入口。';}finally{btn.disabled=false;}};
</script></html>"""


def setup_server(timeout=600, open_browser=True):
    token = secrets.token_urlsafe(32)
    done = {"saved":False}
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def send(self, code, body, content_type="application/json"):
            raw = body.encode()
            self.send_response(code)
            self.send_header("Content-Type",content_type+"; charset=utf-8")
            self.send_header("Content-Length",str(len(raw)))
            self.send_header("Cache-Control","no-store")
            self.send_header("X-Content-Type-Options","nosniff")
            self.send_header("Referrer-Policy","no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(raw)

        def local_host(self):
            return self.headers.get("Host") == "127.0.0.1:"+str(self.server.server_port)

        def do_GET(self):
            url = urllib.parse.urlsplit(self.path)
            if not self.local_host() or url.path != "/" or urllib.parse.parse_qs(url.query).get("token") != [token]:
                return self.send(403,dump({"message":"无效的配置入口。"}))
            self.send(200,PAGE.replace("__TOKEN__",token),"text/html")

        def do_POST(self):
            origin = "http://127.0.0.1:"+str(self.server.server_port)
            if not self.local_host() or self.path != "/configure" or self.headers.get("Origin") != origin or self.headers.get("X-Xjev-Setup") != token:
                return self.send(403,dump({"message":"无效的配置请求。"}))
            try:
                length = int(self.headers.get("Content-Length","0"))
                if not 1 <= length <= 8192:
                    return self.send(400,dump({"message":"输入长度无效。"}))
                data = json.loads(self.rfile.read(length))
                value = data.get("key")
                if not isinstance(value,str) or not 1 <= len(value) <= 4096 or any(c.isspace() for c in value):
                    return self.send(400,dump({"message":"请输入有效 API key。"}))
                probe(value)
                save_key(value)
                done["saved"] = True
                self.send(200,dump({"message":"配置完成。回到 Agent 继续提出决策问题，xjev 会在相关任务中自动选用。"}))
            except XjevError as e:
                self.send(400,dump({"message":e.message}))
            except (ValueError,AttributeError,TypeError):
                self.send(400,dump({"message":"输入格式无效。"}))
            except OSError:
                self.send(500,dump({"message":"本机配置无法保存，请检查目录权限。"}))

    with HTTPServer(("127.0.0.1",0),Handler) as server:
        server.timeout = 1
        url = "http://127.0.0.1:%s/?token=%s" % (server.server_port,token)
        print(dump({"setup_url":url,"expires_in_seconds":timeout,"message":"请在本机页面填写 key；此链接不包含 API key。"}),flush=True)
        if open_browser:
            webbrowser.open(url)
        deadline = time.monotonic()+timeout
        while time.monotonic() < deadline and not done["saved"]:
            server.handle_request()
    print(dump({"configured":done["saved"],"message":"配置已保存。" if done["saved"] else "配置入口已过期；可重新运行 setup。"}),flush=True)
    return 0 if done["saved"] else 2
