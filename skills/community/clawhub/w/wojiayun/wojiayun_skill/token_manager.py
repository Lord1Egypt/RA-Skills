"""
Access Token 管理模块
实现 token 失效检测和自动刷新
"""

import json
import os
from datetime import datetime, timedelta
from typing import Optional, Tuple

try:
    from .crypto_utils import encrypt_value, decrypt_value
    from .key_manager import get_key_manager
except ImportError:
    from crypto_utils import encrypt_value, decrypt_value
    from key_manager import get_key_manager


class TokenManager:
    """Access Token 管理器"""
    
    # Token 存储文件
    TOKEN_FILE = "e:\\workbuddy\\wy\\.secure_tokens"
    
    # Token 失效错误码前缀
    TOKEN_EXPIRED_CODES = ["9001", "9002", "9003", "9004"]
    
    def __init__(self):
        """初始化 Token 管理器"""
        self._tokens = {}
        self._load_tokens()
    
    def _load_tokens(self):
        """从文件加载 token"""
        if os.path.exists(self.TOKEN_FILE):
            try:
                with open(self.TOKEN_FILE, 'r', encoding='utf-8') as f:
                    self._tokens = json.load(f)
            except:
                self._tokens = {}
    
    def _save_tokens(self):
        """保存 token 到文件"""
        with open(self.TOKEN_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._tokens, f, ensure_ascii=False, indent=2)
    
    def is_token_expired_error(self, response: dict) -> bool:
        """检测是否为 token 失效错误"""
        code = str(response.get("code", ""))
        
        if code.startswith("900"):
            return True
        
        msg = response.get("msg", "").lower()
        token_expired_keywords = [
            "token", "access_token", "失效", "过期", 
            "无效", "认证", "权限", "context"
        ]
        
        for keyword in token_expired_keywords:
            if keyword in msg:
                return True
        
        return False
    
    def store_access_token(self, token: str, expires_in: int = 7200):
        """存储 access_token（加密）"""
        encrypted_token = encrypt_value(token)
        
        self._tokens["access_token"] = {
            "encrypted": encrypted_token,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=expires_in)).isoformat(),
            "expires_in": expires_in
        }
        
        self._save_tokens()
    
    def get_access_token(self) -> Optional[str]:
        """获取 access_token（自动解密，解密失败则清除缓存）"""
        if "access_token" not in self._tokens:
            return None
        
        try:
            encrypted = self._tokens["access_token"]["encrypted"]
            token = decrypt_value(encrypted)
            if not token:
                self.clear_token()
                return None
            return token
        except Exception:
            # 解密失败，清除旧缓存（可能是密钥变更导致）
            self.clear_token()
            return None
    
    def is_token_valid(self) -> bool:
        """检查 token 是否有效（未过期）"""
        if "access_token" not in self._tokens:
            return False
        
        try:
            expires_at = datetime.fromisoformat(self._tokens["access_token"]["expires_at"])
            return datetime.now() < (expires_at - timedelta(minutes=5))
        except:
            return False
    
    def refresh_access_token(self, api_key: str, base_url: str) -> Tuple[bool, str]:
        """刷新 access_token"""
        import requests
        
        try:
            # 直接使用完整URL
            url = f"{base_url}/thirdUser/apiKeyAuth"
            
            response = requests.get(
                url,
                params={"apiKey": api_key},
                timeout=30
            )
            
            # 检查响应是否为空或非 JSON
            if not response.text or not response.text.strip().startswith("{"):
                return False, f"响应格式异常: HTTP {response.status_code}"
            
            data = response.json()
            
            if data.get("success") and data.get("result") == "success":
                token_data = data.get("data", {})
                new_token = token_data.get("access_token")
                expires_in = token_data.get("expires_time", 7200)
                
                if new_token:
                    self.store_access_token(new_token, expires_in)
                    return True, "Access Token 刷新成功"
                else:
                    return False, "响应中未找到 access_token"
            else:
                return False, f"刷新失败: {data.get('msg', '未知错误')}"
                
        except Exception as e:
            return False, f"刷新异常: {str(e)}"
    
    def get_token_info(self) -> dict:
        """获取 token 信息（不含实际值）"""
        if "access_token" not in self._tokens:
            return {"status": "未设置"}
        
        info = self._tokens["access_token"].copy()
        info["encrypted"] = "***已加密***"
        info["status"] = "有效" if self.is_token_valid() else "已过期"
        return info
    
    def clear_token(self):
        """清除 token"""
        self._tokens = {}
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)


# 全局实例
_token_manager = None


def get_token_manager() -> TokenManager:
    """获取全局 Token 管理器实例"""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


def handle_token_expired(api_key: str, base_url: str) -> bool:
    """处理 token 失效，自动刷新"""
    tm = get_token_manager()
    success, message = tm.refresh_access_token(api_key, base_url)
    
    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
    
    return success
