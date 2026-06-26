# -*- coding: utf-8 -*-
#!/usr/bin/env python3 -u
"""ZeeLin 任务监控脚本 - 子代理用"""
import os, sys, time, json, requests
from pathlib import Path

# 配置文件路径（脚本在 scripts/ 下，config.json 在 skill/ 下）
CONFIG_FILE = Path(__file__).resolve().parent.parent / "config.json"

def load_config():
    """从配置文件读取配置"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

config = load_config()

def load_api_key():
    """从配置文件读取 API Key"""
    key = config.get("api_key", "").strip()
    if key:
        return key
    print(f"ERROR: API Key not found in {CONFIG_FILE}")
    sys.exit(1)

API_KEY = load_api_key()
TARGET_USER = config.get("target_user", "")
CHANNEL = config.get("channel", "dingtalk")
BASE_URL = "https://desearch.zeelin.cn"
API_URL = f"{BASE_URL}/api/conversation/status"
SESSION_ID = os.environ.get("ZEELIN_SESSION_ID", "")
TITLE = os.environ.get("ZEELIN_CONTENT", "调研任务")

def check_status(session_id):
    resp = requests.get(
        f"{API_URL}?sessionId={session_id}",
        headers={"x-skill-key": API_KEY}
    )
    data = resp.json()
    return data.get("data", {}).get("status"), data.get("data", {})

def get_pdf(session_id):
    """获取 PDF 下载链接"""
    resp = requests.get(
        f"{BASE_URL}/api/conversation/to_report?sessionId={session_id}&reportType=pdf",
        headers={"x-skill-key": API_KEY}
    )
    data = resp.json()
    return data.get("data", "")

def notify_done(title):
    """任务完成后通知用户（发送 PDF 下载地址）"""
    # 获取 PDF 下载地址（接口返回的原始 URL）
    pdf_url = get_pdf(SESSION_ID)
    
    import subprocess
    # 直接发送 PDF 下载地址的原始链接
    cmd = [
        "openclaw", "message", "send",
        "--channel", CHANNEL,
        "--target", TARGET_USER,
        "--message", f"✅ 调研完成：{title}\n\n📥 PDF下载链接：{pdf_url}"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"NOTIFY_OUTPUT: {result.stdout}")
    if result.returncode != 0:
        print(f"NOTIFY_ERROR: {result.stderr}")

def main():
    if not SESSION_ID:
        print("ERROR: ZEELIN_SESSION_ID not set")
        sys.exit(1)
    if not API_KEY:
        print("ERROR: API_KEY not configured")
        sys.exit(1)

    print(f"Watching task: {SESSION_ID}")
    print(f"Title: {TITLE}")

    while True:
        time.sleep(30)
        status, data = check_status(SESSION_ID)
        print(f"Status: {status}")

        if status == 2:  # 完成
            title = data.get("title", TITLE)
            print(f"DONE: {title}")
            
            # 直接发送链接
            notify_done(title)
            print("NOTIFIED_USER")
            break
        elif status in [3, 4]:  # 终止/失败
            print(f"FAILED: status={status}")
            break

if __name__ == "__main__":
    main()
