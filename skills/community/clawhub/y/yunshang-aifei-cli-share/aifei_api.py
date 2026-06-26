#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
云上艾飞 API 客户端（分享版）
SM4 加解密 + Cookie Token 认证
账号密码从 .env 文件读取，不含任何硬编码敏感信息
"""

import sys
import io
import os
import json
import time
import requests
from pathlib import Path
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from dotenv import load_dotenv

# 加载 .env
load_dotenv(Path(__file__).parent / '.env')

# 确保 UTF-8 输出
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ============ SM4 加解密 ============

SM4_KEY = '1097659710ff550f7da111309f64386b'
_KEY_BYTES = bytes.fromhex(SM4_KEY)


def sm4_encrypt(plaintext: str) -> str:
    """SM4/ECB/PKCS5Padding 加密 → hex 字符串"""
    crypt = CryptSM4()
    crypt.set_key(_KEY_BYTES, SM4_ENCRYPT)
    return crypt.crypt_ecb(plaintext.encode('utf-8')).hex()


def sm4_decrypt(cipher_hex: str) -> str:
    """hex 字符串 → SM4/ECB/PKCS5Padding 解密"""
    crypt = CryptSM4()
    crypt.set_key(_KEY_BYTES, SM4_DECRYPT)
    decrypted = crypt.crypt_ecb(bytes.fromhex(cipher_hex))
    pad_len = decrypted[-1]
    if 0 < pad_len <= 16:
        decrypted = decrypted[:-pad_len]
    return decrypted.decode('utf-8')


def parse_response(text: str):
    """解析 API 响应（自动解密）"""
    text = text.strip()
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    if all(c in '0123456789abcdefABCDEF' for c in text):
        try:
            return json.loads(sm4_decrypt(text))
        except Exception:
            pass
    return {'_raw': text[:500]}


# ============ 环境配置 ============

def _get_envs():
    """从 .env 读取账号密码构建环境配置"""
    username = os.getenv('AIFEI_USERNAME', '')
    password = os.getenv('AIFEI_PASSWORD', '')
    if not username or not password:
        raise RuntimeError(
            '请先配置 .env 文件！\n'
            '  1. 复制 .env.example 为 .env\n'
            '  2. 填入 AIFEI_USERNAME 和 AIFEI_PASSWORD\n'
            '  3. 填入 DASHSCOPE_API_KEY'
        )
    return {
        'test': {
            'base_url': 'http://192.168.24.25',
            'api_prefix': '/dev-api',
            'username': username,
            'password': password,
            'domain': '192.168.24.25',
            'login_mode': 'api',
        },
        'prod': {
            'base_url': 'http://192.168.24.208:20080',
            'api_prefix': '/dev-api',
            'api_prefix_biz': '/prod-api',
            'username': username,
            'password': password,
            'domain': '192.168.24.208',
            'login_mode': 'api',
        },
    }


# ============ API 客户端 ============

class AifeiClient:
    """云上艾飞 API 客户端"""

    def __init__(self, env='prod'):
        self.env_name = env
        envs = _get_envs()
        self.config = envs[env].copy()
        self.base_url = self.config['base_url']
        self.session = requests.Session()
        self.token = None
        self._token_file = Path(__file__).parent / f'.token-{env}.json'

    def _url(self, path, use_biz_prefix=False):
        if path.startswith('http'):
            return path
        if path.startswith('/dev-api') or path.startswith('/prod-api'):
            return f'{self.base_url}{path}'
        prefix = self.config.get('api_prefix_biz', self.config['api_prefix']) if use_biz_prefix else self.config['api_prefix']
        return f'{self.base_url}{prefix}/{path.lstrip("/")}'

    def _headers(self):
        h = {'Content-Type': 'application/json;charset=UTF-8'}
        if self.token:
            h['Authorization'] = f'Bearer {self.token}'
        return h

    def get(self, path, params=None, biz=False):
        url = self._url(path, use_biz_prefix=biz)
        resp = self.session.get(url, params=params, headers=self._headers(), timeout=30)
        return parse_response(resp.text)

    def post(self, path, data=None, biz=False, encrypt=True):
        url = self._url(path, use_biz_prefix=biz)
        body = None
        if data is not None and encrypt:
            body = sm4_encrypt(json.dumps(data, ensure_ascii=False))
        elif data is not None:
            body = json.dumps(data, ensure_ascii=False)
        resp = self.session.post(url, data=body, headers=self._headers(), timeout=30)
        return parse_response(resp.text)

    def put(self, path, data=None, biz=False, encrypt=True):
        url = self._url(path, use_biz_prefix=biz)
        body = None
        if data is not None and encrypt:
            body = sm4_encrypt(json.dumps(data, ensure_ascii=False))
        elif data is not None:
            body = json.dumps(data, ensure_ascii=False)
        resp = self.session.put(url, data=body, headers=self._headers(), timeout=30)
        return parse_response(resp.text)

    # ---------- 登录 ----------

    def _set_token(self, token):
        self.token = token
        self.session.cookies.set('Admin-Token', token, domain=self.config['domain'], path='/')
        self._token_file.write_text(json.dumps({
            'token': token, 'time': time.time(), 'env': self.env_name
        }))

    def _load_cached_token(self):
        if self._token_file.exists():
            try:
                data = json.loads(self._token_file.read_text())
                if time.time() - data.get('time', 0) < 14400:
                    self._set_token(data['token'])
                    info = self.get('system/user/getInfo')
                    if isinstance(info, dict) and info.get('code') == 200:
                        return True
            except Exception:
                pass
        return False

    def login(self):
        print(f'🔐 登录 [{self.env_name}] {self.base_url}...')
        if self._load_cached_token():
            print(f'  ✅ 缓存 token 有效')
            return True

        sys.path.insert(0, str(Path(__file__).parent))
        from modules.captcha_solver import solve_captcha

        for attempt in range(5):
            code_resp = self.get(f'{self.config["api_prefix"]}/code')
            if not isinstance(code_resp, dict) or 'uuid' not in code_resp:
                continue
            captcha = solve_captcha(code_resp['img'])
            login_data = {
                'username': self.config['username'],
                'password': sm4_encrypt(self.config['password']),
                'code': captcha,
                'uuid': code_resp['uuid'],
                'forceLogin': '1'
            }
            result = self.post(f'{self.config["api_prefix"]}/auth/login', login_data)
            if isinstance(result, dict) and result.get('code') == 200:
                token = result.get('data', {}).get('access_token', '')
                if token:
                    self._set_token(token)
                    print(f'  ✅ 登录成功')
                    return True
            msg = result.get('msg', '') if isinstance(result, dict) else ''
            if '锁定' in str(msg):
                print(f'  ❌ 账号被锁定')
                return False
        return False

    # ---------- 业务 API ----------

    def get_user_info(self):
        return self.get('system/user/getInfo')

    def get_todos(self, page_num=1, page_size=20):
        return self.post('public/pendingTask/processingList',
                         {'pageNum': page_num, 'pageSize': page_size}, biz=True)

    def get_projects(self, name=None, page_num=1, page_size=10):
        data = {'pageNum': page_num, 'pageSize': page_size}
        if name:
            data['projectName'] = name
        result = self.post('ef-project/project/info/list', data)
        if isinstance(result, dict) and isinstance(result.get('data'), dict):
            return result['data']
        return result

    def get_reimbursements(self, page_num=1, page_size=20):
        return self.post('ef-finance/expense/list',
                         {'pageNum': page_num, 'pageSize': page_size})

    def get_employee_costs(self, page_num=1, page_size=200):
        return self.post('ef-human/employeeCost/listPage',
                         {'pageNum': page_num, 'pageSize': page_size})

    def get_clues(self, page_num=1, page_size=500):
        return self.post('ef-market/clue/selectList',
                         {'pageNum': page_num, 'pageSize': page_size})

    def get_clue_follows(self, clue_id, page_num=1, page_size=200):
        return self.post('ef-market/clueFollow/list',
                         {'pageNum': page_num, 'pageSize': page_size, 'clueId': clue_id})

    def get_weekly_reports(self, project_id, page_num=1, page_size=20):
        return self.post('ef-project/project/weekly/list',
                         {'pageNum': page_num, 'pageSize': page_size, 'projectId': project_id})

    def get_weekly_detail(self, weekly_id):
        return self.post(f'ef-project/project/weekly/getInfo/{weekly_id}', {})

    def create_task(self, task_data):
        return self.post('ef-public/public/task/add', task_data)

    def add_weekly_comment(self, weekly_id, project_id, description):
        return self.post('ef-project/project/weekly/insertComment', {
            'weeklyId': weekly_id,
            'projectId': project_id,
            'description': description
        })


def create_client(env='prod') -> AifeiClient:
    client = AifeiClient(env=env)
    if not client.login():
        raise RuntimeError(f'登录失败 [{env}]')
    return client
