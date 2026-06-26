"""
SM4 加密解密工具类（使用 cryptography 库）
参考 Java Hutool SM4 加密实现
"""

import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib


def sm4_encrypt(plaintext: str, key: bytes) -> str:
    """
    SM4 加密（ECB 模式，PKCS7 填充）
    参考 Java Hutool: SM4.encryptBase64(plainText)
    
    @param plainText 待加密的明文
    @param keyBytes 密钥（16字节）
    @return Base64编码的加密结果
    """
    if not plaintext:
        raise ValueError("明文不能为空")
    
    if len(key) != 16:
        raise ValueError("密钥必须为 16 字节")
    
    # PKCS7 填充
    padding_len = 16 - (len(plaintext.encode('utf-8')) % 16)
    padded = plaintext.encode('utf-8') + bytes([padding_len] * padding_len)
    
    # SM4 ECB 模式加密
    cipher = Cipher(algorithms.SM4(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    
    # 返回 Base64 编码
    return base64.b64encode(ciphertext).decode('utf-8')


def sm4_decrypt(encrypted_text: str, key: bytes) -> str:
    """
    SM4 解密（ECB 模式，PKCS7 填充）
    参考 Java Hutool: SM4.decryptStr(encryptedText)
    
    @param encryptedText Base64编码的密文
    @param keyBytes 密钥（16字节）
    @return 解密后的明文
    """
    if not encrypted_text:
        raise ValueError("密文不能为空")
    
    if len(key) != 16:
        raise ValueError("密钥必须为 16 字节")
    
    # Base64 解码
    ciphertext = base64.b64decode(encrypted_text.encode('utf-8'))
    
    # SM4 ECB 模式解密
    cipher = Cipher(algorithms.SM4(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # 去除 PKCS7 填充
    padding_len = plaintext[-1]
    plaintext = plaintext[:-padding_len]
    
    return plaintext.decode('utf-8')


def is_valid_key(key_bytes: bytes) -> bool:
    """
    验证密钥是否有效（SM4 密钥必须为 128 bit，即 16 字节）
    参考 Java: isValidKey(keyBytes)
    """
    return len(key_bytes) == 16


def generate_key() -> str:
    """
    生成新的 SM4 密钥并返回 Base64 编码格式
    参考 Java: generateKey()
    """
    import os
    key = os.urandom(16)
    return base64.b64encode(key).decode('utf-8')


if __name__ == "__main__":
    # 测试
    key_b64 = "k3qWnsp+ZzFS+Old/VDtcw=="
    key = base64.b64decode(key_b64)
    
    plaintext = '{"orderNo":"123456","amount":1,"payTo":"test"}'
    
    encrypted = sm4_encrypt(plaintext, key)
    print(f"加密: {encrypted}")
    
    decrypted = sm4_decrypt(encrypted, key)
    print(f"解密: {decrypted}")
    
    print(f"密钥验证: {is_valid_key(key)}")
    print(f"生成新密钥: {generate_key()}")
