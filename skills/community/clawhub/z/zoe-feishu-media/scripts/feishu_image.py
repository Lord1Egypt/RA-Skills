# -*- coding: utf-8 -*-
"""
飞书图片发送模块
注意：此模块需要用户自行配置app_id和app_secret，切勿提交包含真实凭证的代码！
"""

import os
import json


def get_feishu_config():
    """
    从环境变量或配置文件获取飞书凭证
    建议使用环境变量，不要硬编码！
    
    环境变量:
        FEISHU_APP_ID: 飞书应用ID
        FEISHU_APP_SECRET: 飞书应用密钥
    """
    app_id = os.environ.get("FEISHU_APP_ID")
    app_secret = os.environ.get("FEISHU_APP_SECRET")
    
    if not app_id or not app_secret:
        raise Exception("请配置FEISHU_APP_ID和FEISHU_APP_SECRET环境变量")
    
    return app_id, app_secret


def send_image(image_path: str, chat_id: str, app_id: str = None, app_secret: str = None):
    """
    发送图片到飞书群或个人
    
    Args:
        image_path: 图片本地路径
        chat_id: 飞书群ID或个人ID
        app_id: 飞书应用ID (可选，从环境变量读取)
        app_secret: 飞书应用密钥 (可选，从环境变量读取)
    """
    # 从参数或环境变量获取凭证
    if not app_id or not app_secret:
        app_id, app_secret = get_feishu_config()
    
    # 动态导入，避免全局依赖
    import requests
    
    BASE_URL = "https://open.feishu.cn/open-apis"
    access_token = None
    
    def get_access_token():
        nonlocal access_token
        if access_token:
            return access_token
            
        url = f"{BASE_URL}/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": app_id,
            "app_secret": app_secret
        }
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        if result.get("code") != 0:
            raise Exception(f"获取access_token失败: {result}")
            
        access_token = result["tenant_access_token"]
        return access_token
    
    def get_headers():
        token = get_access_token()
        return {"Authorization": f"Bearer {token}"}
    
    # 1. 上传图片
    print(f"[INFO] 上传图片: {image_path}")
    
    with open(image_path, "rb") as f:
        files = {
            "image": (os.path.basename(image_path), f, "application/octet-stream")
        }
        data = {"image_type": "message"}
        
        upload_url = f"{BASE_URL}/im/v1/images"
        response = requests.post(upload_url, files=files, data=data, headers=get_headers())
    
    result = response.json()
    print(f"[DEBUG] Upload image response: {result}")
    
    if result.get("code") != 0:
        raise Exception(f"上传图片失败: {result}")
    
    image_key = result.get("data", {}).get("image_key")
    print(f"[INFO] 图片key: {image_key}")
    
    # 2. 发送图片
    print(f"[INFO] 发送图片到: {chat_id}")
    
    send_url = f"{BASE_URL}/im/v1/messages"
    params = {"receive_id_type": "chat_id"}
    
    content = json.dumps({"image_key": image_key})
    data = {
        "receive_id": chat_id,
        "msg_type": "image",
        "content": content
    }
    
    response = requests.post(send_url, headers=get_headers(), params=params, json=data)
    result = response.json()
    print(f"[DEBUG] Send image response: {result}")
    
    if result.get("code") != 0:
        raise Exception(f"发送图片失败: {result}")
    
    print(f"[INFO] 发送成功!")
    return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python feishu_image.py <图片路径> <chat_id>")
        print("环境变量: FEISHU_APP_ID, FEISHU_APP_SECRET")
        sys.exit(1)
    
    image_path = sys.argv[1]
    chat_id = sys.argv[2]
    
    # 可以从命令行传参，也可以设置环境变量
    cmd_app_id = sys.argv[3] if len(sys.argv) > 3 else None
    cmd_secret = sys.argv[4] if len(sys.argv) > 4 else None
    
    send_image(image_path, chat_id, cmd_app_id, cmd_secret)
