# -*- coding: utf-8 -*-
"""
哈希计算工具
"""

import hashlib

# simhash是可选依赖
try:
    import simhash
    HAS_SIMHASH = True
except ImportError:
    HAS_SIMHASH = False


def compute_text_hash(text: str, algorithm: str = 'sha256') -> str:
    """
    计算文本的哈希值
    
    @param text: 输入文本
    @param algorithm: 哈希算法 (md5/sha1/sha256/sha512)
    @return: 哈希值（十六进制）
    """
    hash_func = getattr(hashlib, algorithm)()
    hash_func.update(text.encode('utf-8'))
    return hash_func.hexdigest()
    
    
def compute_text_simhash(text: str) -> int:
    """
    计算文本的SimHash值
    
    @param text: 输入文本
    @return: SimHash值
    """
    if not HAS_SIMHASH:
        raise ImportError("simhash模块未安装，请执行: pip install simhash")
    return simhash.compute(text)
    
    
def compute_text_simhash_with_features(text: str) -> tuple:
    """
    计算文本的SimHash值和特征
    
    @param text: 输入文本
    @return: (simhash值, 特征列表)
    """
    if not HAS_SIMHASH:
        raise ImportError("simhash模块未安装，请执行: pip install simhash")
    return simhash.compute_with_features(text)
    
    
def hamming_distance(hash1: int, hash2: int) -> int:
    """
    计算两个SimHash之间的汉明距离
    
    @param hash1: SimHash值1
    @param hash2: SimHash值2
    @return: 汉明距离
    """
    xor = hash1 ^ hash2
    return bin(xor).count('1')
    
    
def similarity_by_simhash(hash1: int, hash2: int, bits: int = 64) -> float:
    """
    根据SimHash计算相似度
    
    @param hash1: SimHash值1
    @param hash2: SimHash值2
    @param bits: SimHash位数
    @return: 相似度 [0, 1]
    """
    distance = hamming_distance(hash1, hash2)
    return 1 - (distance / bits)
    
    
def compute_md5(text: str) -> str:
    """计算MD5"""
    return compute_text_hash(text, 'md5')
    
    
def compute_sha256(text: str) -> str:
    """计算SHA256"""
    return compute_text_hash(text, 'sha256')
    
    
def compute_sha1(text: str) -> str:
    """计算SHA1"""
    return compute_text_hash(text, 'sha1')
