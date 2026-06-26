#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送图片到飞书 - 支持Webhook签名
集成到画师技能
"""

import requests
import base64
import json
import sys
import os

# 飞书配置
APP_ID = "cli_a9151fbdb7b81cd4"
APP_SECRET = "V40tXt3QwXuDBJKlGPN9pdwFqxgBhwYh"

def get_access_token():
    """获取飞书 access token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json"}
    data = {"app_id": APP_ID, "app_secret": APP_SECRET}
    
    try:
        resp = requests.post(url, headers=headers, json=data, timeout=10)
        result = resp.json()
        
        if result.get("code") == 0:
            return result["tenant_access_token"]
        else:
            print(f"❌ 获取 token 失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 获取 token 异常: {e}")
        return None

def upload_image(token, image_path):
    """上传图片到飞书"""
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        with open(image_path, "rb") as f:
            files = {"image": f}
            data = {"image_type": "message"}
            resp = requests.post(url, headers=headers, files=files, data=data, timeout=30)
        
        result = resp.json()
        if result.get("code") == 0:
            return result["data"]["image_key"]
        else:
            print(f"❌ 上传图片失败: {result}")
            return None
    except Exception as e:
        print(f"❌ 上传图片异常: {e}")
        return None

def send_image_to_user(token, user_id, image_key, caption=""):
    """发送图片给指定用户"""
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {"receive_id_type": "open_id"}
    content = {"image_key": image_key}
    
    data = {
        "receive_id": user_id,
        "msg_type": "image",
        "content": json.dumps(content)
    }
    
    try:
        resp = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        result = resp.json()
        
        if result.get("code") == 0:
            return True
        else:
            print(f"❌ 发送失败: {result}")
            return False
    except Exception as e:
        print(f"❌ 发送异常: {e}")
        return False

def send_feishu_images(image_paths, user_id="ou_9ac9a7fa7050b46022dcdaf6c02a3ee3"):
    """
    发送多张图片到飞书
    
    Args:
        image_paths: 图片路径列表
        user_id: 接收用户ID
    
    Returns:
        成功发送的图片数量
    """
    if not image_paths:
        print("⚠️ 没有图片需要发送")
        return 0
    
    print("\n📤 正在发送到飞书...")
    
    # 获取 token
    token = get_access_token()
    if not token:
        return 0
    
    # 上传并发送每张图片
    success_count = 0
    for i, image_path in enumerate(image_paths, 1):
        if not os.path.exists(image_path):
            print(f"  ⚠️  图片不存在: {image_path}")
            continue
        
        # 上传图片
        image_key = upload_image(token, image_path)
        if not image_key:
            continue
        
        # 发送消息
        if send_image_to_user(token, user_id, image_key):
            success_count += 1
            print(f"  ✅ 图{i}已发送")
        else:
            print(f"  ❌ 图{i}发送失败")
    
    print(f"\n📊 发送完成：{success_count}/{len(image_paths)}")
    return success_count

def send_feishu_message(text, user_id="ou_9ac9a7fa7050b46022dcdaf6c02a3ee3"):
    """发送文本消息到飞书"""
    token = get_access_token()
    if not token:
        return False
    
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    params = {"receive_id_type": "open_id"}
    content = {"text": text}
    
    data = {
        "receive_id": user_id,
        "msg_type": "text",
        "content": json.dumps(content)
    }
    
    try:
        resp = requests.post(url, headers=headers, params=params, json=data, timeout=10)
        result = resp.json()
        return result.get("code") == 0
    except Exception as e:
        print(f"❌ 发送消息失败: {e}")
        return False
