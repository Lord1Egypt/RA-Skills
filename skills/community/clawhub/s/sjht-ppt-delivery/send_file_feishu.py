#!/usr/bin/env python3
"""
send_file_feishu.py — Send a file to a Feishu user via bot API.

Usage: python3 send_file_feishu.py <file_path> <receive_open_id> [--file-type pdf]

Uses the OpenClaw Feishu bot credentials from config.
"""
import requests, json, sys, os

# Read Feishu credentials from OpenClaw config
OPENCLAW_JSON = os.path.expanduser("~/.openclaw/openclaw.json")
with open(OPENCLAW_JSON) as f:
    cfg = json.load(f)

# Navigate to find APP_ID and APP_SECRET
def find_val(obj, keys):
    for k in keys:
        v = obj.get(k)
        if v: return v
    return None

channels = cfg.get("channels", {})
feishu_cfg = channels.get("feishu", {})
accounts = feishu_cfg.get("accounts", {})
main_account = accounts.get("main", {})
env = cfg.get("env", {})

APP_ID = main_account.get("appId") or env.get("FEISHU_APP_ID")
APP_SECRET = main_account.get("appSecret") or env.get("FEISHU_APP_SECRET")

if not APP_ID or not APP_SECRET:
    print("ERROR: Feishu APP_ID or APP_SECRET not found in openclaw.json")
    sys.exit(1)

# Parse arguments
args = sys.argv[1:]
file_path = None
receive_id = None
file_type = "pdf"

i = 0
while i < len(args):
    if args[i] == "--file-type" and i + 1 < len(args):
        file_type = args[i + 1]
        i += 2
    elif not file_path:
        file_path = args[i]
        i += 1
    elif not receive_id:
        receive_id = args[i]
        i += 1
    else:
        i += 1

if not file_path or not receive_id:
    print("Usage: python3 send_file_feishu.py <file_path> <receive_open_id> [--file-type pdf]")
    sys.exit(1)

file_name = os.path.basename(file_path)
ext_map = {
    ".pdf": "pdf", ".doc": "doc", ".docx": "doc",
    ".xls": "xls", ".xlsx": "xls", ".ppt": "ppt", ".pptx": "ppt",
    ".mp4": "mp4", ".opus": "opus", ".mp3": "opus"
}
ext = os.path.splitext(file_name)[1].lower()
mime_type = ext_map.get(ext, file_type)

# 1. Get tenant_access_token
r = requests.post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    json={"app_id": APP_ID, "app_secret": APP_SECRET})
token = r.json().get("tenant_access_token")
if not token:
    print("ERROR: Failed to get token:", r.json())
    sys.exit(1)

# 2. Upload file
headers = {"Authorization": f"Bearer {token}"}
mime_types = {"pdf": "application/pdf", "doc": "application/msword", "xls": "application/vnd.ms-excel", "ppt": "application/vnd.ms-powerpoint"}
content_type = mime_types.get(mime_type, "application/octet-stream")

with open(file_path, "rb") as f:
    r = requests.post("https://open.feishu.cn/open-apis/im/v1/files",
        headers=headers,
        data={"file_type": mime_type, "file_name": file_name},
        files={"file": (file_name, f, content_type)})
resp = r.json()
if resp.get("code") != 0:
    print("ERROR: Upload failed:", resp)
    sys.exit(1)
file_key = resp["data"]["file_key"]
print(f"File uploaded: {file_key}")

# 3. Send file message
r = requests.post(
    "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
    headers={**headers, "Content-Type": "application/json"},
    json={
        "receive_id": receive_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    })
result = r.json()
if result.get("code") == 0:
    print(f"File sent to {receive_id}: {file_name}")
else:
    print("ERROR: Send failed:", result)
    sys.exit(1)
