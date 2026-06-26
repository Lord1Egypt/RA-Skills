#!/usr/bin/env python3
"""
OAuth 2.0 处理器 - 支持 Gmail 和 Outlook
包含自动刷新机制
"""

import json
import requests
import webbrowser
import time
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, parse_qs, urlparse
import threading
from datetime import datetime, timedelta

CREDENTIALS_DIR = Path.home() / '.openclaw' / 'credentials'
OAUTH_TOKENS_FILE = CREDENTIALS_DIR / 'oauth_tokens.json'

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """OAuth 回调处理器"""
    auth_code = None
    
    def do_GET(self):
        query = urlparse(self.path).query
        params = parse_qs(query)
        
        if 'code' in params:
            OAuthCallbackHandler.auth_code = params['code'][0]
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization Success!</h1><p>You can close this window now.</p></body></html>')
        else:
            self.send_response(400)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # 禁用日志

class GmailOAuth:
    """Gmail OAuth 处理"""
    
    def __init__(self, client_id, client_secret, redirect_uri='http://localhost:8080'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_uri = 'https://accounts.google.com/o/oauth2/v2/auth'
        self.token_uri = 'https://oauth2.googleapis.com/token'
    
    def get_authorization_url(self):
        """获取授权 URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/gmail.modify',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        return f"{self.auth_uri}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code):
        """用授权码换取令牌"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(self.token_uri, data=data)
        return response.json()
    
    def refresh_access_token(self, refresh_token):
        """刷新访问令牌"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        
        response = requests.post(self.token_uri, data=data)
        return response.json()

class OutlookOAuth:
    """Outlook OAuth 处理"""
    
    def __init__(self, client_id, client_secret, tenant_id, redirect_uri='http://localhost:8080'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.redirect_uri = redirect_uri
        self.auth_uri = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/authorize'
        self.token_uri = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    
    def get_authorization_url(self):
        """获取授权 URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': 'https://graph.microsoft.com/.default',
            'access_type': 'offline'
        }
        return f"{self.auth_uri}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code):
        """用授权码换取令牌"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri,
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        response = requests.post(self.token_uri, data=data)
        return response.json()
    
    def refresh_access_token(self, refresh_token):
        """刷新访问令牌"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token',
            'scope': 'https://graph.microsoft.com/.default'
        }
        
        response = requests.post(self.token_uri, data=data)
        return response.json()

def authorize_gmail(client_id, client_secret, account_name='gmail'):
    """授权 Gmail 账户"""
    print(f"\n🔐 正在授权 Gmail 账户 '{account_name}'...")
    
    oauth = GmailOAuth(client_id, client_secret)
    auth_url = oauth.get_authorization_url()
    
    print(f"\n📱 请在浏览器中打开以下链接进行授权：")
    print(f"{auth_url}\n")
    
    # 启动本地服务器接收回调
    server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()
    
    # 尝试打开浏览器
    try:
        webbrowser.open(auth_url)
    except:
        pass
    
    print("⏳ 等待授权...")
    server_thread.join(timeout=300)
    
    if OAuthCallbackHandler.auth_code:
        print("✅ 授权成功！正在获取令牌...")
        token_response = oauth.exchange_code_for_token(OAuthCallbackHandler.auth_code)
        
        # 保存令牌
        _save_oauth_token(account_name, 'gmail', token_response)
        print(f"✅ Gmail 账户 '{account_name}' 已授权并保存")
        return token_response
    else:
        print("❌ 授权失败或超时")
        return None

def authorize_outlook(client_id, client_secret, tenant_id, account_name='outlook'):
    """授权 Outlook 账户"""
    print(f"\n🔐 正在授权 Outlook 账户 '{account_name}'...")
    
    oauth = OutlookOAuth(client_id, client_secret, tenant_id)
    auth_url = oauth.get_authorization_url()
    
    print(f"\n📱 请在浏览器中打开以下链接进行授权：")
    print(f"{auth_url}\n")
    
    # 启动本地服务器接收回调
    server = HTTPServer(('localhost', 8080), OAuthCallbackHandler)
    server_thread = threading.Thread(target=server.handle_request)
    server_thread.daemon = True
    server_thread.start()
    
    # 尝试打开浏览器
    try:
        webbrowser.open(auth_url)
    except:
        pass
    
    print("⏳ 等待授权...")
    server_thread.join(timeout=300)
    
    if OAuthCallbackHandler.auth_code:
        print("✅ 授权成功！正在获取令牌...")
        token_response = oauth.exchange_code_for_token(OAuthCallbackHandler.auth_code)
        
        # 保存令牌
        _save_oauth_token(account_name, 'outlook', token_response)
        print(f"✅ Outlook 账户 '{account_name}' 已授权并保存")
        return token_response
    else:
        print("❌ 授权失败或超时")
        return None

def _save_oauth_token(account_name, provider, token_data):
    """保存 OAuth 令牌"""
    CREDENTIALS_DIR.mkdir(parents=True, exist_ok=True)
    
    tokens = {}
    if OAUTH_TOKENS_FILE.exists():
        with open(OAUTH_TOKENS_FILE, 'r') as f:
            tokens = json.load(f)
    
    tokens[account_name] = {
        'provider': provider,
        'access_token': token_data.get('access_token'),
        'refresh_token': token_data.get('refresh_token'),
        'expires_at': time.time() + token_data.get('expires_in', 3600),
        'token_type': token_data.get('token_type', 'Bearer')
    }
    
    with open(OAUTH_TOKENS_FILE, 'w') as f:
        json.dump(tokens, f, indent=2)
    
    # 设置权限
    OAUTH_TOKENS_FILE.chmod(0o600)

def get_oauth_token(account_name):
    """获取 OAuth 令牌"""
    if not OAUTH_TOKENS_FILE.exists():
        return None
    
    with open(OAUTH_TOKENS_FILE, 'r') as f:
        tokens = json.load(f)
    
    return tokens.get(account_name)

def list_oauth_accounts():
    """列出所有 OAuth 账户"""
    if not OAUTH_TOKENS_FILE.exists():
        return {}
    
    with open(OAUTH_TOKENS_FILE, 'r') as f:
        return json.load(f)

def is_token_expired(expires_at, buffer_minutes=5):
    """检查 token 是否已过期（提前 buffer_minutes 分钟）"""
    expiry_time = datetime.fromtimestamp(expires_at)
    buffer_time = datetime.now() + timedelta(minutes=buffer_minutes)
    return buffer_time >= expiry_time

def _get_oauth_credentials(provider='gmail'):
    """从环境变量或配置文件获取 OAuth 凭证"""
    import os
    
    if provider == 'gmail':
        # 优先从环境变量读取
        client_id = os.getenv('GMAIL_CLIENT_ID')
        client_secret = os.getenv('GMAIL_CLIENT_SECRET')
        
        if client_id and client_secret:
            return client_id, client_secret
        
        # 从配置文件读取
        config_file = CREDENTIALS_DIR / 'oauth_config.json'
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('gmail', {}).get('client_id'), config.get('gmail', {}).get('client_secret')
    
    return None, None

def refresh_gmail_token_auto(account_name='gmail', client_id=None, client_secret=None):
    """自动刷新 Gmail token"""
    tokens = list_oauth_accounts()
    
    if account_name not in tokens:
        print(f"❌ 账户 '{account_name}' 不存在")
        return None
    
    token_data = tokens[account_name]
    
    # 检查是否需要刷新
    if not is_token_expired(token_data.get('expires_at', 0)):
        return token_data['access_token']
    
    # 需要刷新
    if not token_data.get('refresh_token'):
        print(f"❌ 账户 '{account_name}' 没有 refresh_token，无法自动刷新")
        return None
    
    print(f"🔄 刷新 {account_name} token...")
    
    try:
        # 获取 OAuth 凭证
        if client_id is None or client_secret is None:
            client_id, client_secret = _get_oauth_credentials('gmail')
        
        if not client_id or not client_secret:
            print(f"❌ 无法获取 Gmail OAuth 凭证")
            return None
        
        oauth = GmailOAuth(client_id, client_secret)
        result = oauth.refresh_access_token(token_data['refresh_token'])
        
        if 'access_token' in result:
            # 更新 token
            token_data['access_token'] = result['access_token']
            token_data['expires_at'] = time.time() + result.get('expires_in', 3600)
            
            # 保存更新
            tokens[account_name] = token_data
            with open(OAUTH_TOKENS_FILE, 'w') as f:
                json.dump(tokens, f, indent=2)
            OAUTH_TOKENS_FILE.chmod(0o600)
            
            print(f"✅ {account_name} token 刷新成功")
            return result['access_token']
        else:
            print(f"❌ 刷新失败: {result.get('error_description', result)}")
            return None
    except Exception as e:
        print(f"❌ 刷新异常: {e}")
        return None

def get_valid_token(account_name='gmail', client_id=None, client_secret=None):
    """获取有效的 token（自动刷新）"""
    token_data = get_oauth_token(account_name)
    
    if not token_data:
        print(f"❌ 账户 '{account_name}' 不存在")
        return None
    
    # 尝试自动刷新
    valid_token = refresh_gmail_token_auto(account_name, client_id, client_secret)
    
    if valid_token:
        return valid_token
    else:
        # 如果刷新失败，返回现有 token（可能已过期）
        return token_data.get('access_token')
