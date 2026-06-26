#!/usr/bin/env python3
"""飞书发送助手 - 上传并发送文件、图片、文字消息"""

import sys
import json
import time
import urllib.request
import urllib.error

import os

APP_ID = os.environ.get('FEISHU_APP_ID', '')
APP_SECRET = os.environ.get('FEISHU_APP_SECRET', '')
USER_OPEN_ID = os.environ.get('FEISHU_USER_OPEN_ID', '')

def get_token():
    """获取飞书 access token"""
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    return resp.get("tenant_access_token", "")

def send_text(token, text):
    """发送文字消息"""
    data = json.dumps({
        "receive_id": USER_OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text})
    }).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    return resp.get("code") == 0

def upload_file(token, file_path, file_name, file_type="stream"):
    """上传文件，返回 file_key"""
    with open(file_path, "rb") as f:
        file_data = f.read()
    
    boundary = "----FeishuBoundary" + str(int(time.time()))
    body = f"--{boundary}\r\n"
    body += f'Content-Disposition: form-data; name="file_type"\r\n\r\n{file_type}\r\n'
    body += f"--{boundary}\r\n"
    body += f'Content-Disposition: form-data; name="file_name"\r\n\r\n{file_name}\r\n'
    body += f"--{boundary}\r\n"
    body += 'Content-Disposition: form-data; name="file"; filename="{}"\r\n'.format(file_name)
    body += "Content-Type: application/octet-stream\r\n\r\n"
    
    body = body.encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
    
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/files",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    if resp.get("code") == 0:
        return resp.get("data", {}).get("file_key", "")
    print(f"Upload error: {resp}", file=sys.stderr)
    return ""

def send_file(token, file_key):
    """发送文件消息"""
    data = json.dumps({
        "receive_id": USER_OPEN_ID,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    return resp.get("code") == 0

def upload_image(token, image_path):
    """上传图片，返回 image_key"""
    with open(image_path, "rb") as f:
        file_data = f.read()
    
    boundary = "----FeishuBoundary" + str(int(time.time()))
    body = f"--{boundary}\r\n"
    body += 'Content-Disposition: form-data; name="image_type"\r\n\r\nmessage\r\n'
    body += f"--{boundary}\r\n"
    body += 'Content-Disposition: form-data; name="image"; filename="image.png"\r\n'
    body += "Content-Type: image/png\r\n\r\n"
    
    body = body.encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
    
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/images",
        data=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    if resp.get("code") == 0:
        return resp.get("data", {}).get("image_key", "")
    print(f"Image upload error: {resp}", file=sys.stderr)
    return ""

def send_image(token, image_key):
    """发送图片消息"""
    data = json.dumps({
        "receive_id": USER_OPEN_ID,
        "msg_type": "image",
        "content": json.dumps({"image_key": image_key})
    }).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=data,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read().decode())
    return resp.get("code") == 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 feishu_sender.py <action> [args]")
        print("Actions:")
        print("  text <message>")
        print("  file <file_path> <file_name>")
        print("  image <image_path>")
        print("  all <title> <summary> <docx_path> <cover_path> <topics>")
        sys.exit(1)
    
    action = sys.argv[1]
    token = get_token()
    
    if action == "text":
        msg = sys.argv[2] if len(sys.argv) > 2 else ""
        ok = send_text(token, msg)
        print("OK" if ok else "FAILED")
    
    elif action == "file":
        file_path = sys.argv[2]
        file_name = sys.argv[3] if len(sys.argv) > 3 else "file"
        file_key = upload_file(token, file_path, file_name)
        if file_key:
            ok = send_file(token, file_key)
            print(f"file_key: {file_key}, sent: {ok}")
        else:
            print("FAILED")
    
    elif action == "image":
        image_path = sys.argv[2]
        image_key = upload_image(token, image_path)
        if image_key:
            ok = send_image(token, image_key)
            print(f"image_key: {image_key}, sent: {ok}")
        else:
            print("FAILED")
    
    elif action == "all":
        # args: title summary docx_path cover_path topics
        title = sys.argv[2]
        summary = sys.argv[3]
        docx_path = sys.argv[4]
        cover_path = sys.argv[5]
        topics = sys.argv[6] if len(sys.argv) > 6 else ""
        
        # 1. Send text with topics, title, summary
        text_msg = f"{topics}\n\n📌 标题：{title}\n\n📝 摘要：{summary}"
        send_text(token, text_msg)
        time.sleep(1)
        
        # 2. Upload and send docx
        file_key = upload_file(token, docx_path, "抖音图文_文档.docx")
        if file_key:
            send_file(token, file_key)
        time.sleep(1)
        
        # 3. Upload and send cover image
        image_key = upload_image(token, cover_path)
        if image_key:
            send_image(token, image_key)
        
        print("All sent successfully")

if __name__ == "__main__":
    main()
