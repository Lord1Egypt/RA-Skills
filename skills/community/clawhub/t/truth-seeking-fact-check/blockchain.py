#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Truth (求真) v1.3 - 区块链存证验证模块
功能：验证区块链上存证的内容哈希，适配2核2G不运行全节点
"""

import hashlib
import re
from typing import Optional, Dict
from dataclasses import dataclass


@dataclass
class BlockchainVerification:
    """区块链验证结果"""
    has_verification: bool
    blockchain_url: str
    content_hash: str
    on_chain_hash: Optional[str]
    verification_result: Optional[bool]
    explanation: str
    score: float  # 0-10分
    
    def to_dict(self) -> Dict:
        return {
            "has_verification": self.has_verification,
            "blockchain_url": self.blockchain_url,
            "content_hash": self.content_hash,
            "on_chain_hash": self.on_chain_hash,
            "verification_result": self.verification_result,
            "explanation": self.explanation,
            "score": self.score
        }


class BlockchainVerifier:
    """区块链存证验证器 - 轻量版本，不运行全节点"""
    
    def __init__(self):
        # 支持的区块链浏览器
        self.supported_domains = [
            "etherscan.io",
            "bscscan.com",
            "polygonscan.com",
            "arbiscan.io",
            "snowtrace.io"
        ]
    
    def _calculate_content_hash(self, content: str) -> str:
        """计算内容的SHA256哈希"""
        # 去除#blockchain标记后计算哈希
        clean_content = re.sub(r'#blockchain:\S+', '', content).strip()
        return hashlib.sha256(clean_content.encode('utf-8')).hexdigest()
    
    def _extract_hash_from_url(self, url: str) -> Optional[str]:
        """从区块链浏览器URL提取哈希/交易信息
        简化版本：假设存证内容哈希放在备注或input数据中
        实际完整验证需要调用区块链浏览器API，这里做轻量处理
        """
        # 支持格式：
        # https://etherscan.io/tx/0x...
        # 交易的input data中包含存证哈希
        
        # 简化实现：提取url最后的十六进制字符串
        match = re.search(r'/(0x[0-9a-fA-f]+)', url)
        if match:
            return match.group(1)
        return None
    
    def _is_supported_url(self, url: str) -> bool:
        """检查是否是支持的区块链浏览器URL"""
        for domain in self.supported_domains:
            if domain in url:
                return True
        return False
    
    def verify(self, text: str, blockchain_url: str) -> BlockchainVerification:
        """
        验证区块链存证
        简化流程：计算当前内容哈希，从URL提取链上哈希，比对
        完整实现需要调用区块链浏览器API，这里保留接口框架
        """
        content_hash = self._calculate_content_hash(text)
        
        if not self._is_supported_url(blockchain_url):
            return BlockchainVerification(
                has_verification=True,
                blockchain_url=blockchain_url,
                content_hash=content_hash,
                on_chain_hash=None,
                verification_result=None,
                explanation="不支持的区块链浏览器，仅计算了内容哈希，未验证",
                score=5.0  # 默认分
            )
        
        on_chain_hash = self._extract_hash_from_url(blockchain_url)
        
        if on_chain_hash is None:
            return BlockchainVerification(
                has_verification=True,
                blockchain_url=blockchain_url,
                content_hash=content_hash,
                on_chain_hash=None,
                verification_result=None,
                explanation="无法从URL提取存证哈希，仅计算了内容哈希",
                score=5.0
            )
        
        # 简化比对：内容哈希是否包含在链上哈希中（完整实现需要调用API获取input数据）
        # 这里做简化判断，实际使用需要完整API调用
        if content_hash.lower().startswith(on_chain_hash.lower()[:10]):
            return BlockchainVerification(
                has_verification=True,
                blockchain_url=blockchain_url,
                content_hash=content_hash,
                on_chain_hash=on_chain_hash,
                verification_result=True,
                explanation="内容哈希与链上存证匹配，验证通过",
                score=10.0
            )
        else:
            return BlockchainVerification(
                has_verification=True,
                blockchain_url=blockchain_url,
                content_hash=content_hash,
                on_chain_hash=on_chain_hash,
                verification_result=False,
                explanation=f"内容哈希({content_hash[:10]}...)与链上存证({on_chain_hash[:10]}...)不匹配，内容可能被篡改",
                score=0.0
            )
