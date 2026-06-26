# -*- coding: utf-8 -*-
"""
加密管理模块
提供凭证加密、解密和密钥管理功能
"""

import os
import base64
import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class EncryptionManager:
    """加密管理器"""
    
    def __init__(self, key_file: str = ".secret_key"):
        """
        初始化加密管理器
        
        Args:
            key_file: 密钥文件路径
        """
        self.key_file = Path(key_file)
        self._fernet: Optional[Fernet] = None
        self._key: Optional[bytes] = None
    
    def generate_key(self, password: Optional[str] = None) -> bytes:
        """
        生成加密密钥
        
        Args:
            password: 可选的密码，用于派生密钥
        
        Returns:
            生成的密钥
        """
        if password:
            # 使用密码派生密钥
            salt = os.urandom(16)
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            # 保存 salt 以便后续使用
            self._save_salt(salt)
        else:
            # 生成随机密钥
            key = Fernet.generate_key()
        
        return key
    
    def _save_salt(self, salt: bytes):
        """保存 salt"""
        salt_file = self.key_file.parent / f"{self.key_file.stem}.salt"
        with open(salt_file, 'wb') as f:
            f.write(salt)
    
    def _load_salt(self) -> Optional[bytes]:
        """加载 salt"""
        salt_file = self.key_file.parent / f"{self.key_file.stem}.salt"
        if salt_file.exists():
            with open(salt_file, 'rb') as f:
                return f.read()
        return None
    
    def save_key(self, key: bytes):
        """
        保存密钥到文件
        
        Args:
            key: 要保存的密钥
        """
        # 确保目录存在
        self.key_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 保存密钥
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # 设置文件权限（仅 Unix）
        if os.name != 'nt':
            os.chmod(self.key_file, 0o600)
    
    def load_key(self) -> Optional[bytes]:
        """
        从文件加载密钥
        
        Returns:
            加载的密钥，如果文件不存在则返回 None
        """
        if not self.key_file.exists():
            return None
        
        with open(self.key_file, 'rb') as f:
            return f.read()
    
    def get_or_create_key(self, password: Optional[str] = None) -> bytes:
        """
        获取或创建密钥
        
        Args:
            password: 可选的密码
        
        Returns:
            密钥
        """
        # 尝试加载现有密钥
        key = self.load_key()
        if key:
            return key
        
        # 生成新密钥
        key = self.generate_key(password)
        self.save_key(key)
        return key
    
    def get_fernet(self, password: Optional[str] = None) -> Fernet:
        """
        获取 Fernet 实例
        
        Args:
            password: 可选的密码
        
        Returns:
            Fernet 实例
        """
        if self._fernet is None:
            key = self.get_or_create_key(password)
            self._fernet = Fernet(key)
        return self._fernet
    
    def encrypt(self, data: str, password: Optional[str] = None) -> str:
        """
        加密字符串
        
        Args:
            data: 要加密的字符串
            password: 可选的密码
        
        Returns:
            加密后的字符串（Base64 编码）
        """
        fernet = self.get_fernet(password)
        encrypted = fernet.encrypt(data.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, encrypted_data: str, password: Optional[str] = None) -> str:
        """
        解密字符串
        
        Args:
            encrypted_data: 加密的字符串（Base64 编码）
            password: 可选的密码
        
        Returns:
            解密后的字符串
        """
        fernet = self.get_fernet(password)
        encrypted = base64.urlsafe_b64decode(encrypted_data.encode())
        decrypted = fernet.decrypt(encrypted)
        return decrypted.decode()
    
    def encrypt_dict(self, data: Dict[str, Any], password: Optional[str] = None) -> str:
        """
        加密字典
        
        Args:
            data: 要加密的字典
            password: 可选的密码
        
        Returns:
            加密后的字符串
        """
        json_str = json.dumps(data, ensure_ascii=False)
        return self.encrypt(json_str, password)
    
    def decrypt_dict(self, encrypted_data: str, password: Optional[str] = None) -> Dict[str, Any]:
        """
        解密字典
        
        Args:
            encrypted_data: 加密的字符串
            password: 可选的密码
        
        Returns:
            解密后的字典
        """
        json_str = self.decrypt(encrypted_data, password)
        return json.loads(json_str)


class CredentialManager:
    """凭证管理器"""
    
    def __init__(self, config_file: str = "config.json", key_file: str = ".secret_key"):
        """
        初始化凭证管理器
        
        Args:
            config_file: 配置文件路径
            key_file: 密钥文件路径
        """
        self.config_file = Path(config_file)
        self.encryption_manager = EncryptionManager(key_file)
    
    def encrypt_credentials(self, app_id: str, app_secret: str, password: Optional[str] = None) -> Dict[str, str]:
        """
        加密凭证
        
        Args:
            app_id: App ID
            app_secret: App Secret
            password: 可选的密码
        
        Returns:
            加密后的凭证字典
        """
        return {
            "app_id_encrypted": self.encryption_manager.encrypt(app_id, password),
            "app_secret_encrypted": self.encryption_manager.encrypt(app_secret, password),
            "encrypted": True
        }
    
    def decrypt_credentials(self, encrypted_config: Dict[str, str], password: Optional[str] = None) -> Dict[str, str]:
        """
        解密凭证
        
        Args:
            encrypted_config: 加密的配置
            password: 可选的密码
        
        Returns:
            解密后的凭证字典
        """
        return {
            "app_id": self.encryption_manager.decrypt(encrypted_config["app_id_encrypted"], password),
            "app_secret": self.encryption_manager.decrypt(encrypted_config["app_secret_encrypted"], password)
        }
    
    def save_encrypted_config(self, app_id: str, app_secret: str, base_dir: str = "", password: Optional[str] = None):
        """
        保存加密的配置
        
        Args:
            app_id: App ID
            app_secret: App Secret
            base_dir: 基础目录
            password: 可选的密码
        """
        encrypted_creds = self.encrypt_credentials(app_id, app_secret, password)
        
        config = {
            **encrypted_creds,
            "base_dir": base_dir
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 设置文件权限
        if os.name != 'nt':
            os.chmod(self.config_file, 0o600)
    
    def load_config(self, password: Optional[str] = None) -> Dict[str, str]:
        """
        加载配置（自动处理加密/未加密）
        
        Args:
            password: 可选的密码
        
        Returns:
            配置字典
        """
        if not self.config_file.exists():
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # 检查是否加密
        if config.get("encrypted"):
            return self.decrypt_credentials(config, password)
        else:
            # 未加密，返回原始配置
            return {
                "app_id": config.get("app_id", ""),
                "app_secret": config.get("app_secret", ""),
                "base_dir": config.get("base_dir", "")
            }
    
    def is_encrypted(self) -> bool:
        """
        检查配置是否已加密
        
        Returns:
            是否已加密
        """
        if not self.config_file.exists():
            return False
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return config.get("encrypted", False)


# 便捷函数
def encrypt_value(value: str, key_file: str = ".secret_key", password: Optional[str] = None) -> str:
    """
    加密单个值
    
    Args:
        value: 要加密的值
        key_file: 密钥文件路径
        password: 可选的密码
    
    Returns:
        加密后的值
    """
    manager = EncryptionManager(key_file)
    return manager.encrypt(value, password)


def decrypt_value(encrypted_value: str, key_file: str = ".secret_key", password: Optional[str] = None) -> str:
    """
    解密单个值
    
    Args:
        encrypted_value: 加密的值
        key_file: 密钥文件路径
        password: 可选的密码
    
    Returns:
        解密后的值
    """
    manager = EncryptionManager(key_file)
    return manager.decrypt(encrypted_value, password)
