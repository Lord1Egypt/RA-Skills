"""
加密工具模块
使用 AES 对称加密算法保护敏感数据
"""

import base64
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoUtils:
    """加密工具类"""
    
    def __init__(self, password: str = None):
        """
        初始化加密工具
        
        Args:
            password: 加密密码，如果不提供则使用默认机器标识
        """
        if password is None:
            # 使用机器标识生成密码（不同机器不同）
            password = self._get_machine_key()
        
        self._key = self._derive_key(password)
        self._fernet = Fernet(self._key)
    
    def _get_machine_key(self) -> str:
        """获取机器唯一标识作为加密密码"""
        # 组合多个机器特征
        machine_id = f"{os.environ.get('COMPUTERNAME', 'default')}{os.environ.get('USERNAME', 'user')}"
        return hashlib.sha256(machine_id.encode()).hexdigest()[:32]
    
    def _derive_key(self, password: str) -> bytes:
        """
        从密码派生加密密钥
        
        Args:
            password: 用户密码
            
        Returns:
            Fernet 可用的密钥
        """
        # 使用固定的 salt（简化处理，实际应用中应该随机生成并存储）
        salt = b'equipment_analyzer_salt_2024'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt(self, plaintext: str) -> str:
        """
        加密字符串
        
        Args:
            plaintext: 明文字符串
            
        Returns:
            加密后的 Base64 字符串
        """
        if not plaintext:
            return ""
        
        encrypted = self._fernet.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """
        解密字符串
        
        Args:
            ciphertext: 加密的 Base64 字符串
            
        Returns:
            解密后的明文字符串
        """
        if not ciphertext:
            return ""
        
        try:
            encrypted = base64.urlsafe_b64decode(ciphertext.encode())
            decrypted = self._fernet.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"解密失败: {e}")
    
    @staticmethod
    def is_encrypted(value: str) -> bool:
        """
        判断字符串是否已加密
        
        Args:
            value: 待判断的字符串
            
        Returns:
            是否为加密字符串
        """
        if not value:
            return False
        
        # 加密后的字符串特征：以 gAAAAA 开头（Fernet 特征）
        try:
            decoded = base64.urlsafe_b64decode(value.encode())
            return decoded[:10] == b'gAAAAA'
        except:
            return False


# 全局加密工具实例
_crypto_instance = None

def get_crypto() -> CryptoUtils:
    """获取全局加密工具实例"""
    global _crypto_instance
    if _crypto_instance is None:
        _crypto_instance = CryptoUtils()
    return _crypto_instance


def encrypt_value(plaintext: str) -> str:
    """便捷加密函数"""
    return get_crypto().encrypt(plaintext)


def decrypt_value(ciphertext: str) -> str:
    """便捷解密函数"""
    return get_crypto().decrypt(ciphertext)
