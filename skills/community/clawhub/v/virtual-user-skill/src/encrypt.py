#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
加密解密模块 - 保护场景库数据

功能：
1. 首次运行时自动生成密钥
2. 使用密钥加密/解密数据
3. 密钥保存在用户本地（~/.virtual_user/.key）
"""

import os
import base64
from pathlib import Path
from cryptography.fernet import Fernet


class EncryptManager:
    """加密管理器"""
    
    def __init__(self):
        self.key_dir = Path.home() / ".virtual_user"
        self.key_file = self.key_dir / ".key"
        self.key = None
    
    def ensure_key_dir(self):
        """确保密钥目录存在"""
        self.key_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_key(self):
        """生成新密钥"""
        return Fernet.generate_key()
    
    def load_or_create_key(self):
        """加载已有密钥或创建新密钥"""
        self.ensure_key_dir()
        
        if self.key_file.exists():
            # 加载已有密钥
            with open(self.key_file, 'rb') as f:
                self.key = f.read()
            print(f"✅ 已加载已有密钥：{self.key_file}")
        else:
            # 生成新密钥
            self.key = self.generate_key()
            with open(self.key_file, 'wb') as f:
                f.write(self.key)
            # 设置文件权限（仅所有者可读写）
            os.chmod(self.key_file, 0o600)
            print(f"🔑 已生成新密钥并保存：{self.key_file}")
        
        return self.key
    
    def get_cipher(self):
        """获取加密器"""
        if self.key is None:
            self.load_or_create_key()
        return Fernet(self.key)
    
    def encrypt_data(self, data_bytes):
        """加密数据"""
        cipher = self.get_cipher()
        encrypted = cipher.encrypt(data_bytes)
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt_data(self, encrypted_str):
        """解密数据"""
        cipher = self.get_cipher()
        encrypted_bytes = base64.b64decode(encrypted_str.encode('utf-8'))
        decrypted = cipher.decrypt(encrypted_bytes)
        return decrypted
    
    def encrypt_file(self, input_file, output_file):
        """加密文件"""
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encrypted = self.encrypt_data(data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encrypted)
        
        print(f"🔒 已加密文件：{input_file} → {output_file}")
    
    def decrypt_file(self, encrypted_file):
        """解密文件"""
        with open(encrypted_file, 'r', encoding='utf-8') as f:
            encrypted_str = f.read()
        
        decrypted = self.decrypt_data(encrypted_str)
        return decrypted.decode('utf-8')


# 测试代码
if __name__ == "__main__":
    manager = EncryptManager()
    key = manager.load_or_create_key()
    print(f"密钥：{key.decode()}")
    
    # 测试加密解密
    test_data = "这是测试数据".encode('utf-8')
    encrypted = manager.encrypt_data(test_data)
    print(f"加密后：{encrypted}")
    
    decrypted = manager.decrypt_data(encrypted)
    print(f"解密后：{decrypted.decode()}")
    
    assert decrypted == test_data, "加密解密测试失败！"
    print("✅ 加密解密测试通过！")
