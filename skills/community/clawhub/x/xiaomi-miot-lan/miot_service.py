#!/usr/bin/env python3
"""
小米米家 MCP 服务
全平台兼容版 - 纯文字交互
"""

import os
import sys
import json
import time
import hashlib
import requests
from pathlib import Path

# ============ 配置 ============
# 请在环境变量中设置以下值：
# XIAOMI_CLIENT_ID - 小米 OAuth2 客户端 ID
# XIAOMI_CLIENT_SECRET - 小米 OAuth2 客户端密钥
CLIENT_ID = os.environ.get("XIAOMI_CLIENT_ID", "2882303761517424859")
CLIENT_SECRET = os.environ.get("XIAOMI_CLIENT_SECRET", "")
CACHE_DIR = os.path.expanduser("~/.openclaw/skills/xiaomi-miot/data")
TOKEN_CACHE_FILE = os.path.join(CACHE_DIR, "token_cache.json")

# ============ Token 缓存 ============

def load_token_cache():
    """加载缓存的 token"""
    if os.path.exists(TOKEN_CACHE_FILE):
        with open(TOKEN_CACHE_FILE, 'r') as f:
            return json.load(f)
    return None

def save_token_cache(token_data):
    """保存 token 到缓存"""
    os.makedirs(CACHE_DIR, exist_ok=True)
    with open(TOKEN_CACHE_FILE, 'w') as f:
        json.dump(token_data, f, indent=2)

def is_token_valid(cache):
    """检查 token 是否有效（提前5分钟检查）"""
    if not cache:
        return False
    expires_at = cache.get('expires_at', 0)
    return time.time() < (expires_at - 300)

def clear_token_cache():
    """清除过期的 token"""
    if os.path.exists(TOKEN_CACHE_FILE):
        os.remove(TOKEN_CACHE_FILE)

# ============ 验证码获取 ============

def get_captcha():
    """获取验证码图片路径，返回 (success, session, sign, captcha_path)"""
    try:
        session = requests.Session()
        
        resp = session.get(
            "https://account.xiaomi.com/pass/serviceLogin?sid=xiaomiio&_json=true",
            timeout=10
        )
        text = resp.text
        if text.startswith("&&&START&&&"):
            text = text.replace("&&&START&&&", "")
        data = json.loads(text)
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
    except Exception as e:
        return False, None, "", None

# ============ 登录核心 ============

def do_oauth_login(username, password):
    """执行 OAuth2 登录，返回 (success, result)"""
    try:
        password_hash = hashlib.md5(password.encode()).hexdigest().upper()
        
        resp = requests.post(
            "https://account.xiaomi.com/oauth2/token",
            data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
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
            
            expires_in = result.get('expires_in', 2592000)
            
            return True, {
                'macaroon': macaroon,
                'expires_at': time.time() + expires_in,
                'username': username
            }
        else:
            return False, f"登录失败: {result.get('error_description', 'Unknown')}"
    except Exception as e:
        return False, f"登录异常: {str(e)}"

def login_step1(username, password):
    """第一步：尝试直接 OAuth2 登录，返回 (success, need_captcha, session, result)"""
    # 先尝试 OAuth2（可能直接成功）
    success, result = do_oauth_login(username, password)
    
    if success:
        return True, False, None, result
    
    # 如果 OAuth2 失败，尝试带验证码的登录
    ok, session, sign, captcha_path = get_captcha()
    if not ok:
        return False, False, None, "无法连接小米服务器"
    
    # 检查是否需要验证码（通过传统登录接口判断）
    password_hash = hashlib.md5(password.encode()).hexdigest().upper()
    
    resp = session.post(
        "https://account.xiaomi.com/pass/serviceLoginAuth2",
        data={
            "user": username,
            "hash": password_hash,
            "sid": "xiaomiio",
            "_sign": sign,
            "_json": "true"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    data_text = resp.text
    if data_text.startswith("&&&START&&&"):
        data_text = data_text.replace("&&&START&&&", "")
    data = json.loads(data_text)
    code = data.get('code')
    
    if code == 0:
        # 传统登录成功，但需要用 OAuth2 获取 macaroon
        # 再次尝试 OAuth2
        success2, result2 = do_oauth_login(username, password)
        if success2:
            return True, False, None, result2
        return False, False, None, "OAuth2 获取失败"
    elif code == 87001:
        # 需要验证码
        return False, True, session, {"sign": sign, "captcha_path": captcha_path}
    else:
        return False, False, None, data.get('desc', '登录失败')

def login_step2_with_captcha(username, password, session, sign, captcha_code):
    """第二步：用验证码完成登录"""
    password_hash = hashlib.md5(password.encode()).hexdigest().upper()
    
    resp = session.post(
        "https://account.xiaomi.com/pass/serviceLoginAuth2",
        data={
            "user": username,
            "hash": password_hash,
            "sid": "xiaomiio",
            "_sign": sign,
            "icode": captcha_code,
            "_json": "true"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10
    )
    
    data_text = resp.text
    if data_text.startswith("&&&START&&&"):
        data_text = data_text.replace("&&&START&&&", "")
    data = json.loads(data_text)
    if data.get('code') == 0:
        # 登录成功，获取 macaroon
        success, result = do_oauth_login(username, password)
        return success, result if success else None, result
    return False, None, data.get('desc', '验证码错误')

def get_devices_with_token(macaroon):
    """用 macaroon token 获取设备列表"""
    try:
        resp = requests.get(
            "https://api.io.mi.com/app/home/device/list",
            headers={
                "Authorization": f"Bearer {macaroon}",
                "User-Agent": "Dalvik/2.1.0"
            },
            timeout=15
        )
        
        if resp.status_code == 200:
            return resp.json().get('result', {}).get('devices', [])
        elif resp.status_code == 401:
            return None  # Token 失效
        else:
            return []
    except:
        return []

# ============ 主类 ============

class XiaomiMiot:
    """小米米家控制客户端"""
    
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
        self.macaroon = None
        
    def ensure_token(self):
        """确保有有效 token"""
        # 1. 先尝试缓存
        cache = load_token_cache()
        if is_token_valid(cache):
            self.macaroon = cache['macaroon']
            return True, "cached"
        
        # 2. 缓存无效，尝试登录
        if not self.username or not self.password:
            return False, "need_credentials"
        
        success, need_captcha, session_or_result, data = login_step1(
            self.username, self.password
        )
        
        if success:
            self.macaroon = data['macaroon']
            save_token_cache(data)
            return True, "new_login"
        
        if need_captcha:
            return False, f"CAPTCHA|{data.get('sign')}|{data.get('captcha_path')}"
        
        return False, str(data)
    
    def get_devices(self):
        """获取设备列表"""
        # 确保有 token
        ok, status = self.ensure_token()
        
        if not ok:
            return None, status
        
        devices = get_devices_with_token(self.macaroon)
        
        if devices is None:
            # Token 失效，清除缓存并重试
            clear_token_cache()
            ok, status = self.ensure_token()
            if ok:
                devices = get_devices_with_token(self.macaroon)
            else:
                return None, status
        
        return devices, "success"
    
    def format_devices(self, devices):
        """格式化设备列表为文字"""
        if not devices:
            return "未找到设备"
        
        lines = [f"找到 {len(devices)} 个设备:\n"]
        for i, d in enumerate(devices, 1):
            name = d.get('name', '未知设备')
            did = d.get('did', '')
            model = d.get('model', '')
            online = "🟢" if d.get('online') == 1 else "🔴"
            lines.append(f"{i}. {online} {name}")
            if model:
                lines.append(f"   型号: {model}")
        
        return "\n".join(lines)

# ============ CLI 测试 ============

if __name__ == "__main__":
    print("=" * 50)
    print("小米米家控制 - 全平台兼容版")
    print("=" * 50)
    
    username = os.environ.get("XIAOMI_USERNAME")
    password = os.environ.get("XIAOMI_PASSWORD")
    
    if not username or not password:
        print("\n请设置环境变量：")
        print("  export XIAOMI_USERNAME='你的手机号'")
        print("  export XIAOMI_PASSWORD='你的密码'")
        sys.exit(1)
    
    client = XiaomiMiot(username, password)
    devices, status = client.get_devices()
    
    if status == "need_credentials":
        print("\n需要提供账号密码")
    elif status.startswith("CAPTCHA"):
        print(f"\n需要验证码，状态: {status}")
    elif status == "new_login":
        print(f"\n{client.format_devices(devices)}")
    elif status == "cached":
        print(f"\n{client.format_devices(devices)}")
    else:
        print(f"\n错误: {status}")
