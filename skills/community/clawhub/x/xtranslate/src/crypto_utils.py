import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoUtils:
    def __init__(self, password="Xtranslate_Secret_Key"):
        # 生成基于密码的固定密钥（也可以生成一个文件保存，但由于是本地工具，固定算法比较方便）
        salt = b'xtranslate_salt'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.fernet = Fernet(key)

    def encrypt(self, text):
        if not text:
            return ""
        return self.fernet.encrypt(text.encode()).decode()

    def decrypt(self, encrypted_text):
        if not encrypted_text or not encrypted_text.startswith("gAAAA"): # Fernet 密文特征
            return encrypted_text # 如果不是加密文本，直接返回原文（兼容未加密的旧配置）
        try:
            return self.fernet.decrypt(encrypted_text.encode()).decode()
        except:
            return encrypted_text # 解密失败则返回原样

# 快捷工具实例
crypto = CryptoUtils()
