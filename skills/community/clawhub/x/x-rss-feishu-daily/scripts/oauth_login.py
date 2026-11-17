"""一次性 OAuth 授权：起本地回调服务器，等用户在浏览器点同意，换取并保存 user token。

产出：同目录 user_token.json（access_token / refresh_token / 过期时间戳）。
用法：python oauth_login.py   （然后打开打印出的授权链接，点同意）
"""
import http.server
import json
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

BASE = Path(__file__).parent
CONF = {}
for line in (BASE / "feishu.env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        CONF[k.strip()] = v.strip()

REDIRECT = CONF.get("OAUTH_REDIRECT_URI", "http://127.0.0.1:8899/callback")
PORT = 8899
_opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
result = {"code": None}


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        if q.get("code"):
            result["code"] = q["code"][0]
            self.wfile.write("✅ 授权成功，可以关闭此页面回到 ZCode。".encode("utf-8"))
            threading.Thread(target=httpd.shutdown, daemon=True).start()
        else:
            self.wfile.write(("❌ 授权失败：" + json.dumps(q, ensure_ascii=False)).encode("utf-8"))

    def log_message(self, *a):
        pass


params = {
    "app_id": CONF["FEISHU_APP_ID"],
    "redirect_uri": REDIRECT,
    "response_type": "code",
    "state": "rss-stack-oauth3",
    "scope": "im:message im:chat:readonly",
}
auth_url = "https://accounts.feishu.cn/open-apis/authen/v1/authorize?" + urllib.parse.urlencode(params)

httpd = http.server.HTTPServer(("127.0.0.1", PORT), Handler)
print("AUTH_URL:", auth_url, flush=True)
print(f"等待回调 http://127.0.0.1:{PORT}/callback …", flush=True)
server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
server_thread.start()
server_thread.join(timeout=600)
if not result["code"]:
    print("超时：600 秒内未收到授权回调", flush=True)
    raise SystemExit(1)

print("收到 code，换取 token …", flush=True)
r1 = urllib.request.Request(
    "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal",
    data=json.dumps({"app_id": CONF["FEISHU_APP_ID"], "app_secret": CONF["FEISHU_APP_SECRET"]}).encode(),
    headers={"Content-Type": "application/json"})
app_at = json.load(_opener.open(r1, timeout=20))["app_access_token"]
r2 = urllib.request.Request(
    "https://open.feishu.cn/open-apis/authen/v1/oidc/access_token",
    data=json.dumps({"grant_type": "authorization_code", "code": result["code"]}).encode(),
    headers={"Content-Type": "application/json", "Authorization": "Bearer " + app_at})
d = json.load(_opener.open(r2, timeout=20))
print("完整响应 keys:", list(d.keys()), "| code:", d.get("code"), flush=True)
if d.get("code") != 0:
    print("换取失败:", json.dumps(d, ensure_ascii=False)[:400], flush=True)
    raise SystemExit(1)
d = d.get("data") or d

print("✅ user token 已保存到 user_token.json", flush=True)
print("   access_token 过期时间:", time.strftime("%m-%d %H:%M", time.localtime(data["access_expire_at"])), flush=True)
print("   refresh_token 过期时间:", time.strftime("%m-%d %H:%M", time.localtime(data["refresh_expire_at"])), flush=True)
