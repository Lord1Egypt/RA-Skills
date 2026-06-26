#!/usr/bin/env python3
"""
小米米家登录卡片 - 飞书 Interactive Card 实现
提供内置的登录界面，无需跳转
"""

import requests
import hashlib
import json
import os

# 飞书 API 配置
# 请在环境变量中设置：
# FEISHU_APP_ID - 飞书应用 ID
# FEISHU_APP_SECRET - 飞书应用密钥
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

def get_tenant_token():
    """获取飞书 tenant token"""
    resp = requests.post(
        'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal',
        json={'app_id': APP_ID, 'app_secret': APP_SECRET},
        timeout=10
    )
    return resp.json().get('tenant_access_token')

def create_login_card():
    """创建登录卡片"""
    return {
        "config": {"wide_screen_mode": True},
        "elements": [
            {"tag": "markdown", "content": "## 🔐 小米账号登录\n请输入你的小米账号信息\n\n*首次使用需要验证，之后 30 天内自动续期*"},
            {"tag": "hr"},
            {
                "tag": "input",
                "name": "username",
                "label": {"tag": "plain_text", "content": "📱 手机号"},
                "placeholder": {"tag": "plain_text", "content": "请输入小米账号手机号"}
            },
            {
                "tag": "input", 
                "name": "password",
                "label": {"tag": "plain_text", "content": "🔒 密码"},
                "placeholder": {"tag": "plain_text", "content": "请输入密码"}
            },
            {"tag": "hr"},
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "登录 🔑"},
                "type": "primary"
            }
        ]
    }

def create_captcha_card(captcha_image_key):
    """创建验证码卡片"""
    return {
        "config": {"wide_screen_mode": True},
        "elements": [
            {"tag": "markdown", "content": "## 🔐 身份验证\n请输入图中验证码完成登录"},
            {"tag": "hr"},
            {
                "tag": "img",
                "img_key": captcha_image_key,
                "alt": {"tag": "plain_text", "content": "验证码"}
            },
            {
                "tag": "input",
                "name": "captcha_code",
                "label": {"tag": "plain_text", "content": "🔢 验证码"},
                "placeholder": {"tag": "plain_text", "content": "请输入上图中的字符"}
            },
            {"tag": "hr"},
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "确认 ✓"},
                "type": "primary"
            }
        ]
    }

def create_success_card(username, devices):
    """创建登录成功卡片"""
    device_list = "\n".join([f"- {d['name']} ({'🟢在线' if d.get('online')==1 else '🔴离线'})" for d in devices])
    
    return {
        "config": {"wide_screen_mode": True},
        "elements": [
            {"tag": "markdown", "content": f"## ✅ 登录成功！\n\n**账号**: {username}\n\n**已发现 {len(devices)} 个设备**:\n{device_list}"},
            {"tag": "hr"},
            {"tag": "markdown", "content": "🎉 你现在可以让小蓝帮你控制这些设备了！\n\n比如：\n• \"帮我重启路由器\"\n• \"开灯\""},
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "知道了 ✨"},
                "type": "default"
            }
        ]
    }

def create_error_card(error_msg):
    """创建错误卡片"""
    return {
        "config": {"wide_screen_mode": True},
        "elements": [
            {"tag": "markdown", "content": f"## ❌ 登录失败\n\n**原因**: {error_msg}\n\n请重新尝试登录"},
            {"tag": "hr"},
            {
                "tag": "button",
                "text": {"tag": "plain_text", "content": "重新登录 🔄"},
                "type": "primary"
            }
        ]
    }

def upload_image(image_path):
    """上传图片到飞书，返回 image_key"""
    token = get_tenant_token()
    
    with open(image_path, 'rb') as f:
        resp = requests.post(
            'https://open.feishu.cn/open-apis/im/v1/images',
            headers={'Authorization': f'Bearer {token}'},
            files={'image': ('captcha.png', f, 'image/png')},
            data={'image_type': 'message'},
            timeout=10
        )
    
    if resp.json().get('code') == 0:
        return resp.json()['data']['image_key']
    return None

def send_card(token, open_id, card):
    """发送卡片消息"""
    resp = requests.post(
        'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'receive_id': open_id,
            'msg_type': 'interactive',
            'content': json.dumps(card)
        },
        timeout=10
    )
    return resp.json()

def update_card(token, message_id, card):
    """更新卡片消息"""
    resp = requests.patch(
        f'https://open.feishu.cn/open-apis/im/v1/messages/{message_id}',
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        },
        json={
            'content': json.dumps(card)
        },
        timeout=10
    )
    return resp.json()

# ============ 小米登录核心 ============

def xiaomi_get_captcha():
    """获取小米登录验证码"""
    session = requests.Session()
    
    resp = session.get(
        "https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true",
        timeout=10
    )
    data = resp.json()
    sign = data.get("_sign", "")
    
    img_resp = session.get(
        "https://account.xiaomi.com/pass/getCode?icodeType=login",
        timeout=10
    )
    
    if img_resp.status_code == 200:
        captcha_path = "/tmp/xiaomi_captcha.png"
        with open(captcha_path, 'wb') as f:
            f.write(img_resp.content)
        return True, session, sign, captcha_path
    
    return False, session, sign, None

def xiaomi_login_with_creds(username, password, session, sign, captcha_code=None):
    """使用账号密码（和验证码）登录小米"""
    password_hash = hashlib.md5(password.encode()).hexdigest().upper()
    
    data = {
        "user": username,
        "hash": password_hash,
        "sid": "xiaomiio",
        "_sign": sign,
        "_json": "true"
    }
    
    if captcha_code:
        data["icode"] = captcha_code
    
    resp = session.post(
        "https://account.xiaomi.com/pass/serviceLoginAuth2",
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    result = resp.json()
    code = result.get('code')
    
    if code == 0:
        return True, "success", session
    elif code == 87001:
        return False, "CAPTCHA_NEEDED", session
    else:
        return False, result.get('desc', 'Unknown error'), session

def xiaomi_oauth_get_devices(session, username, password):
    """通过 OAuth2 获取设备列表"""
    password_hash = hashlib.md5(password.encode()).hexdigest().upper()
    
    resp = session.post(
        "https://account.xiaomi.com/oauth2/token",
        data={
            "client_id": "2882303761517424859",
            "client_secret": "7u5bWIWiWiWiWiWiWiWiWiWg==",
            "grant_type": "password",
            "password": password_hash,
            "scope": "1,30000",
            "username": username
        },
        headers={"User-Agent": "Dalvik/2.1.0"},
        timeout=15
    )
    
    result = resp.json()
    
    if 'access_token' in result:
        access_token = result['access_token']
        if isinstance(access_token, dict):
            macaroon = access_token.get('macaroon', '')
        else:
            macaroon = access_token
        
        headers = {
            "Authorization": f"Bearer {macaroon}",
            "User-Agent": "Dalvik/2.1.0"
        }
        
        resp2 = session.get(
            "https://api.io.mi.com/app/home/device/list",
            headers=headers,
            timeout=15
        )
        
        if resp2.status_code == 200:
            return resp2.json().get('result', {}).get('devices', [])
    
    return None

# ============ 主流程 ============

def handle_login_message(open_id, username, password, captcha_code=None, session=None, sign=None, state="INIT"):
    """
    处理登录流程
    state: INIT -> CAPTCHA -> SUCCESS/ERROR
    """
    token = get_tenant_token()
    
    if state == "INIT":
        ok, _, captcha_sign, _ = xiaomi_get_captcha()
        if not ok:
            return "ERROR", "无法连接小米服务器"
        
        success, msg, session = xiaomi_login_with_creds(username, password, session, captcha_sign)
        
        if success:
            devices = xiaomi_oauth_get_devices(session, username, password)
            if devices:
                card = create_success_card(username, devices)
            else:
                card = create_success_card(username, [{"name": "（无法获取设备列表）", "online": 0}])
            send_card(token, open_id, card)
            return "SUCCESS", devices
        elif msg == "CAPTCHA_NEEDED":
            ok, session, sign, captcha_path = xiaomi_get_captcha()
            if ok:
                image_key = upload_image(captcha_path)
                if image_key:
                    card = create_captcha_card(image_key)
                    result = send_card(token, open_id, card)
                    return "CAPTCHA", None
            return "ERROR", "无法获取验证码"
        else:
            card = create_error_card(msg)
            send_card(token, open_id, card)
            return "ERROR", msg
    
    elif state == "CAPTCHA":
        ok, session, sign, _ = xiaomi_get_captcha()
        if not ok:
            return "ERROR", "会话已过期，请重新开始"
        
        success, msg, session = xiaomi_login_with_creds(
            username, password, session, sign, captcha_code
        )
        
        if success:
            devices = xiaomi_oauth_get_devices(session, username, password)
            if devices:
                card = create_success_card(username, devices)
            else:
                card = create_success_card(username, [{"name": "（无法获取设备列表）", "online": 0}])
            send_card(token, open_id, card)
            return "SUCCESS", devices
        else:
            card = create_error_card("验证码错误，请重试")
            send_card(token, open_id, card)
            return "ERROR", msg


if __name__ == "__main__":
    print("小米登录卡片服务")
    print("此模块由小蓝自动调用，不需要手动运行")
