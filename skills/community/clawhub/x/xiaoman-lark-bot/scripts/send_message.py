#!/usr/bin/env python3
"""
飞书消息发送工具
用法: python3 send_message.py "消息内容"
"""
import os
import sys
import json
import urllib.request

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
CHAT_ID = os.environ.get("LARK_CHAT_ID", "")

def get_token():
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())['tenant_access_token']

def send_message(text):
    token = get_token()
    url = "https://open.larksuite.com/open-apis/im/v1/messages?receive_id_type=chat_id"
    data = {
        "receive_id": CHAT_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        method="POST",
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req).read())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 send_message.py \"消息内容\"")
        sys.exit(1)
    
    text = sys.argv[1]
    result = send_message(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
