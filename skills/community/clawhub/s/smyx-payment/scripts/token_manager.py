#!/usr/bin/env python3
"""
Token 管理模块 - Bearer Token 实现
提供 Token 生成、验证、刷新、撤销功能
"""

import secrets
import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

# 尝试导入 Redis（可选）
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False
    print("⚠️  Redis 未安装，使用内存存储 Token")


class TokenManager:
    """Token 管理器"""
    
    def __init__(self, secret_key: str = None, use_redis: bool = False, redis_host: str = 'localhost', redis_port: int = 6379):
        """
        初始化 Token 管理器
        
        Args:
            secret_key: 加密密钥（可选，用于增强安全性）
            use_redis: 是否使用 Redis 存储
            redis_host: Redis 主机
            redis_port: Redis 端口
        """
        self.secret_key = secret_key or secrets.token_urlsafe(32)
        self.use_redis = use_redis and REDIS_AVAILABLE
        self.redis_client = None
        
        # 初始化 Redis
        if self.use_redis:
            try:
                self.redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
                self.redis_client.ping()
                print("✅ Redis 连接成功")
            except Exception as e:
                print(f"⚠️  Redis 连接失败：{e}，使用内存存储")
                self.use_redis = False
        
        # 内存存储（测试用）
        self.memory_store = {}
    
    def generate_token(self, user_id: str, extra_data: Dict[str, Any] = None, expire_seconds: int = 86400) -> str:
        """
        生成 Bearer Token
        
        Args:
            user_id: 用户 ID（如手机号）
            extra_data: 额外数据（可选）
            expire_seconds: 过期时间（秒），默认 24 小时
        
        Returns:
            Token 字符串
        """
        # 生成随机字符串
        random_str = secrets.token_urlsafe(32)
        
        # 拼接用户 ID 和随机字符串
        token_raw = f"{user_id}:{random_str}:{time.time()}"
        
        # SHA256 哈希
        token = hashlib.sha256(token_raw.encode()).hexdigest()
        
        # 存储 Token 信息
        token_data = {
            'user_id': user_id,
            'token': token,
            'created_at': time.time(),
            'expires_at': time.time() + expire_seconds,
            'extra_data': extra_data or {}
        }
        
        self._save_token(token, token_data, expire_seconds)
        
        return token
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证 Token
        
        Args:
            token: Token 字符串
        
        Returns:
            Token 信息（验证失败返回 None）
        """
        token_data = self._get_token(token)
        
        if not token_data:
            return None
        
        # 检查是否过期
        if time.time() > token_data.get('expires_at', 0):
            self._delete_token(token)
            return None
        
        # 检查是否在黑名单中
        if self._is_blacklisted(token):
            return None
        
        return token_data
    
    def refresh_token(self, old_token: str) -> Optional[str]:
        """
        刷新 Token
        
        Args:
            old_token: 旧 Token
        
        Returns:
            新 Token（失败返回 None）
        """
        token_data = self.verify_token(old_token)
        
        if not token_data:
            return None
        
        # 生成新 Token
        new_token = self.generate_token(
            user_id=token_data['user_id'],
            extra_data=token_data.get('extra_data'),
            expire_seconds=86400
        )
        
        # 撤销旧 Token
        self._delete_token(old_token)
        
        return new_token
    
    def revoke_token(self, token: str) -> bool:
        """
        撤销 Token
        
        Args:
            token: Token 字符串
        
        Returns:
            是否成功撤销
        """
        # 加入黑名单
        self._add_to_blacklist(token)
        
        # 删除 Token
        self._delete_token(token)
        
        return True
    
    def _save_token(self, token: str, token_data: Dict[str, Any], expire_seconds: int):
        """保存 Token"""
        if self.use_redis and self.redis_client:
            key = f"token:{token}"
            self.redis_client.setex(key, expire_seconds, json.dumps(token_data))
        else:
            self.memory_store[f"token:{token}"] = {
                'data': token_data,
                'expires_at': token_data.get('expires_at', 0)
            }
    
    def _get_token(self, token: str) -> Optional[Dict[str, Any]]:
        """获取 Token 信息"""
        if self.use_redis and self.redis_client:
            key = f"token:{token}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        else:
            stored = self.memory_store.get(f"token:{token}")
            if stored and time.time() < stored.get('expires_at', 0):
                return stored['data']
            return None
    
    def _delete_token(self, token: str):
        """删除 Token"""
        if self.use_redis and self.redis_client:
            key = f"token:{token}"
            self.redis_client.delete(key)
        else:
            self.memory_store.pop(f"token:{token}", None)
    
    def _add_to_blacklist(self, token: str):
        """加入黑名单"""
        if self.use_redis and self.redis_client:
            key = f"token_blacklist:{token}"
            self.redis_client.setex(key, 86400, "revoked")
        else:
            self.memory_store[f"token_blacklist:{token}"] = {
                'revoked_at': time.time()
            }
    
    def _is_blacklisted(self, token: str) -> bool:
        """检查是否在黑名单中"""
        if self.use_redis and self.redis_client:
            key = f"token_blacklist:{token}"
            return self.redis_client.exists(key) > 0
        else:
            return f"token_blacklist:{token}" in self.memory_store
    
    def get_stats(self) -> Dict[str, Any]:
        """获取统计信息"""
        if self.use_redis and self.redis_client:
            # Redis 统计
            keys = self.redis_client.keys("token:*")
            blacklisted = self.redis_client.keys("token_blacklist:*")
            return {
                'storage': 'Redis',
                'active_tokens': len(keys),
                'blacklisted_tokens': len(blacklisted)
            }
        else:
            # 内存存储统计
            active = len([k for k in self.memory_store if k.startswith('token:') and not k.startswith('token_blacklist:')])
            blacklisted = len([k for k in self.memory_store if k.startswith('token_blacklist:')])
            return {
                'storage': 'Memory',
                'active_tokens': active,
                'blacklisted_tokens': blacklisted
            }


# 全局 Token 管理器实例
token_manager = None

def init_token_manager(secret_key: str = None, use_redis: bool = False):
    """初始化全局 Token 管理器"""
    global token_manager
    token_manager = TokenManager(secret_key=secret_key, use_redis=use_redis)
    return token_manager

def get_token_manager() -> TokenManager:
    """获取全局 Token 管理器"""
    global token_manager
    if not token_manager:
        token_manager = TokenManager()
    return token_manager


# Flask 中间件示例
def create_auth_middleware(app, token_manager: TokenManager):
    """
    创建 Flask 认证中间件
    
    Args:
        app: Flask 应用
        token_manager: Token 管理器
    """
    @app.before_request
    def check_auth():
        # 跳过不需要认证的路由
        if request.endpoint in ['login', 'register', 'health']:
            return
        
        # 获取 Token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return {'error': 'Missing or invalid Authorization header'}, 401
        
        token = auth_header.split(' ')[1]
        
        # 验证 Token
        token_data = token_manager.verify_token(token)
        if not token_data:
            return {'error': 'Invalid or expired token'}, 401
        
        # 将用户信息添加到请求上下文
        request.user = token_data


# 使用示例
if __name__ == "__main__":
    print("\n\n")
    print("=" * 80)
    print("Token 管理器测试")
    print("=" * 80)
    
    # 初始化 Token 管理器
    tm = TokenManager(use_redis=False)
    
    # 生成 Token
    print("\n【生成 Token】")
    user_id = "13829295599"
    token = tm.generate_token(user_id, extra_data={'phone': user_id, 'vip_level': 1})
    print(f"用户 ID: {user_id}")
    print(f"Token: {token}")
    
    # 验证 Token
    print("\n【验证 Token】")
    token_data = tm.verify_token(token)
    if token_data:
        print("✅ Token 有效")
        print(f"用户 ID: {token_data['user_id']}")
        print(f"额外数据：{token_data['extra_data']}")
    else:
        print("❌ Token 无效")
    
    # 刷新 Token
    print("\n【刷新 Token】")
    new_token = tm.refresh_token(token)
    if new_token:
        print(f"✅ Token 已刷新")
        print(f"新 Token: {new_token}")
    else:
        print("❌ 刷新失败")
    
    # 撤销 Token
    print("\n【撤销 Token】")
    success = tm.revoke_token(new_token)
    if success:
        print(f"✅ Token 已撤销")
    
    # 验证已撤销的 Token
    print("\n【验证已撤销的 Token】")
    token_data = tm.verify_token(new_token)
    if not token_data:
        print("✅ Token 已失效")
    else:
        print("❌ Token 仍然有效")
    
    # 统计信息
    print("\n【统计信息】")
    stats = tm.get_stats()
    print(f"存储方式：{stats['storage']}")
    print(f"活跃 Token 数：{stats['active_tokens']}")
    print(f"黑名单 Token 数：{stats['blacklisted_tokens']}")
    
    print("\n✅ 测试完成！")
