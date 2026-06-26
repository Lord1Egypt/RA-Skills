from pathlib import Path
#!/usr/bin/env python3
"""feishu_handler — 私聊命令 → 直接发飞书卡片"""
import json, subprocess, os, urllib.request, urllib.error, sys

SKILL_DIR = Path(__file__).parent
TOKEN_FILE = Path("/tmp/feishu_card_token.json")

def get_token():
    """获取飞书 tenant_access_token（缓存5分钟）"""
    if TOKEN_FILE.exists():
        try:
            data = json.loads(TOKEN_FILE.read_text())
            if data.get("expire", 0) > __import__("time").time() + 60:
                return data["token"]
        except: pass
    cfg = json.loads(open(os.path.expanduser("~/.openclaw/openclaw.json")).read())
    feishu = cfg.get("channels", {}).get("feishu", {})
    app_id = feishu.get("appId", ""); app_secret = feishu.get("appSecret", "")
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({"app_id": app_id, "app_secret": app_secret}).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read())
    token = result.get("tenant_access_token", "")
    TOKEN_FILE.write_text(json.dumps({"token": token, "expire": __import__("time").time() + 1900}))
    return token

def send_card(user_open_id, card_content):
    """发送飞书互动卡片"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    payload = {"receive_id": user_open_id, "msg_type": "interactive", "content": card_content}
    req = urllib.request.Request(url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {get_token()}"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read()).get("code") == 0
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()[:100]}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"发送失败: {e}", file=sys.stderr)
        return False

def handle(text):
    text = text.strip()
    if not text.startswith("/"):
        return None
    r = subprocess.run(["python3", str(SKILL_DIR / "skill.py"), text],
        capture_output=True, text=True, timeout=20, cwd=str(SKILL_DIR))
    output = r.stdout.strip()
    if not output:
        return None
    # 判断是 JSON（卡片）还是纯文本
    try:
        card_content = json.loads(output)
        return ("card", card_content)
    except:
        return ("text", output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: feishu_handler.py '<命令>' '<user_open_id>'", file=sys.stderr)
        sys.exit(1)
    result = handle(sys.argv[1])
    if result is None:
        sys.exit(0)
    msg_type, content = result
    if msg_type == "card":
        ok = send_card(sys.argv[2], json.dumps(content))
        print("卡片发送成功" if ok else "卡片发送失败")
    else:
        print(content)
