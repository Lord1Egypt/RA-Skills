#!/usr/bin/env python3
"""
飞书文件发送脚本
用法: python send_feishu_file.py <file_path> <open_id> [caption]

环境变量（必须配置）:
  FEISHU_APP_ID     - 飞书应用 ID
  FEISHU_APP_SECRET - 飞书应用密钥
"""

import sys
import os
import requests
import json

# 飞书配置 - 从环境变量读取（必须配置）
APP_ID = os.environ.get("FEISHU_APP_ID")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET")

if not APP_ID or not APP_SECRET:
    print("❌ 错误: 请配置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")
    print("")
    print("配置方法:")
    print("  export FEISHU_APP_ID='cli_xxx'")
    print("  export FEISHU_APP_SECRET='xxx'")
    print("")
    print("或在 ~/.zshrc 中添加:")
    print("  export FEISHU_APP_ID='cli_xxx'")
    print("  export FEISHU_APP_SECRET='xxx'")
    sys.exit(1)

# MIME 类型映射
MIME_MAP = {
    '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    '.xls': 'application/vnd.ms-excel',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    '.doc': 'application/msword',
    '.pdf': 'application/pdf',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.gif': 'image/gif',
    '.mp4': 'video/mp4',
    '.mp3': 'audio/mpeg',
}

# file_type 映射
FILE_TYPE_MAP = {
    '.xlsx': 'xlsx', '.xls': 'xlsx',
    '.docx': 'doc', '.doc': 'doc',
    '.pdf': 'pdf',
    '.png': 'image', '.jpg': 'image', '.jpeg': 'image', '.gif': 'image', '.webp': 'image',
    '.mp4': 'video', '.mov': 'video',
    '.mp3': 'audio', '.wav': 'audio', '.m4a': 'audio',
}


def get_token():
    """获取 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": APP_ID, "app_secret": APP_SECRET})
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取 token 失败: {data}")
    return data["tenant_access_token"]


def upload_file(token, file_path):
    """上传文件到飞书，返回 file_key"""
    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()
    file_type = FILE_TYPE_MAP.get(ext, 'stream')
    mime_type = MIME_MAP.get(ext, 'application/octet-stream')
    
    url = "https://open.feishu.cn/open-apis/im/v1/files"
    headers = {"Authorization": f"Bearer {token}"}
    
    # 简化文件名，避免特殊字符问题
    safe_filename = f"file{ext}"
    
    with open(file_path, 'rb') as f:
        files = {'file': (safe_filename, f, mime_type)}
        # 统一使用 stream 类型，避免飞书 API 对特定类型的限制
        data = {'file_type': 'stream', 'file_name': safe_filename}
        resp = requests.post(url, headers=headers, files=files, data=data)
    
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"上传文件失败: {result}")
    
    return result["data"]["file_key"]


def send_file_message(token, open_id, file_key):
    """发送文件消息"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "receive_id": open_id,
        "msg_type": "file",
        "content": json.dumps({"file_key": file_key})
    }
    resp = requests.post(url, headers=headers, json=data)
    result = resp.json()
    if result.get("code") != 0:
        raise Exception(f"发送消息失败: {result}")
    return result["data"]["message_id"]


def main():
    if len(sys.argv) < 3:
        print("用法: python send_feishu_file.py <file_path> <open_id> [caption]")
        print("示例: python send_feishu_file.py /path/to/file.xlsx ou_xxx")
        sys.exit(1)
    
    file_path = sys.argv[1]
    open_id = sys.argv[2]
    caption = sys.argv[3] if len(sys.argv) > 3 else None
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    filename = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    print(f"📤 发送文件到飞书:")
    print(f"   文件: {filename} ({file_size/1024:.1f} KB)")
    print(f"   接收者: {open_id}")
    
    try:
        # 1. 获取 token
        print("\n1️⃣ 获取访问令牌...")
        token = get_token()
        print(f"   ✅ 成功")
        
        # 2. 上传文件
        print("\n2️⃣ 上传文件到飞书服务器...")
        file_key = upload_file(token, file_path)
        print(f"   ✅ 上传成功: {file_key}")
        
        # 3. 发送文件消息
        print("\n3️⃣ 发送文件消息...")
        message_id = send_file_message(token, open_id, file_key)
        print(f"   ✅ 发送成功!")
        print(f"\n📨 消息ID: {message_id}")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()