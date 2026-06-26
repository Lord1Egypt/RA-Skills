#!/usr/bin/env python3
"""安全存储模块 - 加密存储敏感数据"""

import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class SecureStorage:
    """加密存储类"""
    
    def __init__(self, app_name: str = "logistics"):
        self.app_name = app_name
        self.base_dir = Path.home() / ".openclaw" / "data" / app_name / "secure"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        # 密钥文件
        self.key_file = self.base_dir / ".key"
        self._key = self._get_or_create_key()
        self._cipher = Fernet(self._key)
    
    def _get_or_create_key(self) -> bytes:
        """获取或创建加密密钥"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                return base64.urlsafe_b64decode(f.read())
        
        # 生成新密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=os.urandom(16),
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(os.urandom(32)))
        
        # 保存密钥 (权限 600)
        with open(self.key_file, 'wb') as f:
            f.write(key)
        os.chmod(self.key_file, 0o600)
        
        return base64.urlsafe_b64decode(key)
    
    def encrypt(self, data: str) -> str:
        """加密字符串"""
        return self._cipher.encrypt(data.encode()).decode()
    
    def decrypt(self, token: str) -> str:
        """解密字符串"""
        return self._cipher.decrypt(token.encode()).decode()
    
    def save_json(self, filename: str, data: dict):
        """保存加密JSON文件"""
        filepath = self.base_dir / filename
        json_str = json.dumps(data, ensure_ascii=False)
        encrypted = self.encrypt(json_str)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        os.chmod(filepath, 0o600)
    
    def load_json(self, filename: str) -> dict:
        """加载加密JSON文件"""
        filepath = self.base_dir / filename
        if not filepath.exists():
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            encrypted = f.read()
        json_str = self.decrypt(encrypted)
        return json.loads(json_str)
    
    def save_file(self, filename: str, content: str):
        """保存加密文件"""
        filepath = self.base_dir / filename
        encrypted = self.encrypt(content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        os.chmod(filepath, 0o600)
    
    def load_file(self, filename: str) -> str:
        """加载加密文件"""
        filepath = self.base_dir / filename
        if not filepath.exists():
            return ""
        with open(filepath, 'r', encoding='utf-8') as f:
            encrypted = f.read()
        return self.decrypt(encrypted)
    
    def delete(self, filename: str):
        """删除文件"""
        filepath = self.base_dir / filename
        if filepath.exists():
            filepath.unlink()
    
    def list_files(self) -> list:
        """列出所有存储的文件"""
        return [f.name for f in self.base_dir.iterdir() if f.is_file()]
    
    def clear_all(self):
        """清除所有数据"""
        for f in self.base_dir.iterdir():
            if f.is_file():
                f.unlink()
    
    def get_storage_info(self) -> dict:
        """获取存储信息"""
        files = []
        for f in self.base_dir.iterdir():
            if f.is_file():
                stat = f.stat()
                files.append({
                    'name': f.name,
                    'size': stat.st_size,
                    'permissions': oct(stat.st_mode)[-3:],
                    'modified': stat.st_mtime
                })
        return {
            'base_dir': str(self.base_dir),
            'files': files,
            'total_files': len(files)
        }
