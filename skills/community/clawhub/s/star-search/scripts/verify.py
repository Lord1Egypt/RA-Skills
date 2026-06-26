#!/usr/bin/env python3
"""实战 60 验证码 (2026-06-16) - Turnstile 图形验证码版
- Cloudflare Turnstile (0 认证 0 费用)
- 后期换短信验证/邮箱验证只换 verify_token 实现
- 测试 site_key: 1x00000000000000000000AA (始终通过)
- 测试 secret_key: 1x0000000000000000000000000000000AA (始终通过)
- 真接: https://www.cloudflare.com/products/turnstile/ 注册拿自己的 key
"""
import os
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict

# Turnstile 配置 (测试 key, 真接需替换)
TURNSTILE_SITE_KEY = os.environ.get('TURNSTILE_SITE_KEY', '1x00000000000000000000AA')
TURNSTILE_SECRET_KEY = os.environ.get('TURNSTILE_SECRET_KEY', '1x0000000000000000000000000000000AA')
TURNSTILE_VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'

# 内存验证池 (同 IP 1 小时内只验证 1 次成功)
# 真接: 应存 Redis/MySQL 跨进程
VERIFY_POOL_FILE = Path('/home/ubuntu/star-search/verify_pool.json')


def _load_pool() -> Dict:
    if not VERIFY_POOL_FILE.exists():
        return {'tokens': {}}
    try:
        with open(VERIFY_POOL_FILE) as f:
            return json.load(f)
    except Exception:
        return {'tokens': {}}


def _save_pool(data: Dict):
    with open(VERIFY_POOL_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def verify_turnstile_token(token: str, remote_ip: str = '') -> Dict:
    """实战 60: 验证 Turnstile token
    调用 Cloudflare siteverify API
    """
    if not token:
        return {'success': False, 'error': 'no_token', 'message': '验证码 token 缺失'}

    # 调 Cloudflare siteverify
    body = urllib.parse.urlencode({
        'secret': TURNSTILE_SECRET_KEY,
        'response': token,
        'remoteip': remote_ip,
    }).encode()
    try:
        req = urllib.request.Request(
            TURNSTILE_VERIFY_URL,
            data=body,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        return {
            'success': data.get('success', False),
            'error': data.get('error-codes', [None])[0] if not data.get('success') else None,
            'action': data.get('action'),
            'hostname': data.get('hostname'),
            'challenge_ts': data.get('challenge_ts'),
        }
    except Exception as e:
        return {'success': False, 'error': 'network', 'message': f'验证服务异常: {e}'}


def verify_captcha(token: str, remote_ip: str = '', method: str = 'turnstile') -> Dict:
    """统一验证码接口 (后期可扩展 SMS/Email)
    - method: turnstile / sms / email
    """
    if method == 'turnstile':
        return verify_turnstile_token(token, remote_ip)
    # 后期扩展:
    # elif method == 'sms':
    #     return verify_sms_code(token, remote_ip)
    # elif method == 'email':
    #     return verify_email_code(token, remote_ip)
    return {'success': False, 'error': 'unknown_method', 'message': f'未知验证方式: {method}'}


def get_site_key() -> str:
    """实战 60: 前端获取 site_key
    (site_key 公开放, 不算秘密)
    """
    return TURNSTILE_SITE_KEY
