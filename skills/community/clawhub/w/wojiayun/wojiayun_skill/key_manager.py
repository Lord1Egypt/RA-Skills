"""
密钥管理器模块
安全存储和管理 API 密钥
"""

import json
import os
from datetime import datetime
from typing import Optional

try:
    from .crypto_utils import encrypt_value, decrypt_value, get_crypto
except ImportError:
    from crypto_utils import encrypt_value, decrypt_value, get_crypto


class KeyManager:
    """密钥管理器"""
    
    # 密钥存储文件路径
    STORAGE_FILE = "e:\\workbuddy\\wy\\.secure_keys"
    
    # 密钥配置文件（存储加密后的密钥）
    CONFIG_FILE = "e:\\workbuddy\\wy\\.key_config"
    
    def __init__(self):
        """初始化密钥管理器"""
        self._keys = {}
        self._load_keys()
    
    def _load_keys(self):
        """从文件加载密钥"""
        if os.path.exists(self.STORAGE_FILE):
            try:
                with open(self.STORAGE_FILE, 'r', encoding='utf-8') as f:
                    self._keys = json.load(f)
            except:
                self._keys = {}
    
    def _save_keys(self):
        """保存密钥到文件"""
        with open(self.STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(self._keys, f, ensure_ascii=False, indent=2)
    
    def store_key(self, key_name: str, key_value: str, description: str = "") -> bool:
        """存储密钥（加密后存储）"""
        try:
            encrypted = encrypt_value(key_value)
            
            self._keys[key_name] = {
                "encrypted": encrypted,
                "description": description,
                "created_at": datetime.now().isoformat()
            }
            
            self._save_keys()
            return True
        except Exception as e:
            print(f"存储密钥失败: {e}")
            return False
    
    def get_key(self, key_name: str) -> Optional[str]:
        """获取密钥（自动解密）"""
        if key_name not in self._keys:
            return None
        
        try:
            encrypted = self._keys[key_name]["encrypted"]
            return decrypt_value(encrypted)
        except Exception as e:
            print(f"解密密钥失败: {e}")
            return None
    
    def list_keys(self) -> list:
        """列出所有密钥名称"""
        return list(self._keys.keys())
    
    def delete_key(self, key_name: str) -> bool:
        """删除密钥"""
        if key_name in self._keys:
            del self._keys[key_name]
            self._save_keys()
            return True
        return False


# 全局实例
_key_manager = None


def get_key_manager() -> KeyManager:
    """获取全局密钥管理器实例"""
    global _key_manager
    if _key_manager is None:
        _key_manager = KeyManager()
    return _key_manager


def store_api_key(key_value: str, key_name: str = "default_api_key") -> bool:
    """便捷函数：存储 API Key"""
    km = get_key_manager()
    return km.store_key(key_name, key_value, "API Key")


def get_api_key(key_name: str = "default_api_key") -> Optional[str]:
    """便捷函数：获取 API Key"""
    km = get_key_manager()
    return km.get_key(key_name)


def init_default_key():
    """初始化默认密钥（用于测试）"""
    store_api_key("sk-kdwjy-4ee6de0b5a8f4b92b8e0c8b8b8b8b8b8")
