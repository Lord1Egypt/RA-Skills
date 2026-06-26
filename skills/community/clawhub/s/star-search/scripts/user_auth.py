#!/usr/bin/env python3
"""实战 55 用户系统 (2026-06-15)
- phone + password 注册/登录
- HMAC token (12h 过期)
- 简单 quota tracking (100/天 免费 / 1000/月 基础 / 10000/年 Pro)
- JSON file 存储 /home/ubuntu/star-search/users.json
- 端点: POST /v1/auth/register, /v1/auth/login, /v1/auth/me, /v1/auth/quota
"""
import os
import json
import hmac
import hashlib
import time
import base64
import secrets
from typing import Optional, Dict, List
from pathlib import Path

USERS_FILE = Path('/home/ubuntu/star-search/users.json')
SECRET = b'star-search-stardust-2026'  # 实战 55: HMAC 密钥 (生产用 env)
TOKEN_TTL = 12 * 3600  # 12h

# 简单 bcrypt-like: sha256 多次 + salt (生产换 bcrypt/argon2)
def _hash_password(password: str, salt: str = None) -> str:
    if salt is None:
        salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    for _ in range(1000):
        h = hashlib.sha256((h + salt).encode()).hexdigest()
    return f"{salt}${h}"

def _verify_password(password: str, stored: str) -> bool:
    try:
        salt, _ = stored.split('$', 1)
        return _hash_password(password, salt) == stored
    except Exception:
        return False

def _make_token(user_id: str) -> str:
    payload = {
        'uid': user_id,
        'exp': int(time.time()) + TOKEN_TTL,
        'jti': secrets.token_hex(8),
    }
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    sig = hmac.new(SECRET, payload_b64.encode(), hashlib.sha256).hexdigest()[:32]
    return f"{payload_b64}.{sig}"

def _verify_token(token: str) -> Optional[Dict]:
    try:
        payload_b64, sig = token.split('.', 1)
        expected_sig = hmac.new(SECRET, payload_b64.encode(), hashlib.sha256).hexdigest()[:32]
        if not hmac.compare_digest(sig, expected_sig):
            return None
        payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())
        if payload.get('exp', 0) < time.time():
            return None
        return payload
    except Exception:
        return None

def _load_users() -> Dict:
    if not USERS_FILE.exists():
        return {'users': {}, 'quota_usage': {}}
    try:
        with open(USERS_FILE) as f:
            return json.load(f)
    except Exception:
        return {'users': {}, 'quota_usage': {}}

def _save_users(data: Dict):
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# === 业务函数 ===
def register(phone: str, password: str, email: str = '') -> Dict:
    """注册: 验证手机号 + 密码长度 + 唯一性"""
    phone = phone.strip()
    if not phone or len(phone) < 6 or len(phone) > 20:
        return {'error': '手机号格式不对 (6-20 位)'}
    if not password or len(password) < 6:
        return {'error': '密码至少 6 位'}
    data = _load_users()
    if phone in data['users']:
        return {'error': '该手机号已注册'}
    user_id = secrets.token_hex(8)
    data['users'][phone] = {
        'user_id': user_id,
        'phone': phone,
        'email': email,
        'password': _hash_password(password),
        'created_at': int(time.time()),
        'tier': 'free',  # free / basic / pro
    }
    _save_users(data)
    return {'user_id': user_id, 'token': _make_token(user_id), 'tier': 'free'}

def login(phone: str, password: str) -> Dict:
    """登录: 验证手机号 + 密码"""
    data = _load_users()
    user = data['users'].get(phone.strip())
    if not user:
        return {'error': '手机号未注册'}
    if not _verify_password(password, user['password']):
        return {'error': '密码错误'}
    return {
        'user_id': user['user_id'],
        'token': _make_token(user['user_id']),
        'tier': user.get('tier', 'free'),
    }

def get_user(token: str) -> Optional[Dict]:
    """验证 token + 返回用户信息"""
    payload = _verify_token(token)
    if not payload:
        return None
    data = _load_users()
    for phone, user in data['users'].items():
        if user['user_id'] == payload['uid']:
            return {**user, 'phone': phone}
    return None

# === Quota ===
QUOTA = {
    'free': 100,    # 100/天
    'basic': 1000,  # 1000/月
    'pro': 10000,   # 10000/年
}

def check_quota(user_id: str) -> Dict:
    """检查 + 累加 quota (UTC 天 / 月 / 年)"""
    data = _load_users()
    today = time.strftime('%Y-%m-%d')
    month = time.strftime('%Y-%m')
    year = time.strftime('%Y')

    user = None
    for u in data['users'].values():
        if u['user_id'] == user_id:
            user = u
            break
    if not user:
        return {'error': 'user not found'}

    tier = user.get('tier', 'free')
    limit = QUOTA.get(tier, 100)

    if tier == 'free':
        bucket = today
        cap = limit
    elif tier == 'basic':
        bucket = month
        cap = limit
    else:  # pro
        bucket = year
        cap = limit

    quota = data.setdefault('quota_usage', {})
    bucket_data = quota.setdefault(bucket, {})
    used = bucket_data.get(user_id, 0)

    if used >= cap:
        return {
            'error': f'quota exceeded ({tier}: {used}/{cap})',
            'tier': tier,
            'used': used,
            'limit': cap,
            'bucket': bucket,
        }
    # +1
    bucket_data[user_id] = used + 1
    _save_users(data)
    return {
        'ok': True,
        'tier': tier,
        'used': used + 1,
        'limit': cap,
        'bucket': bucket,
        'remaining': cap - used - 1,
    }
