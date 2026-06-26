#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
x402 Payment Core Module
x402 支付核心模块 - 支持实时和异步支付
"""

import json
import time
import hashlib
from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from config import (
    RECEIVING_ADDRESS, 
    PRICING, 
    ASYNC_THRESHOLD,
    CONFIRMATION_BLOCKS,
    CONFIRMATION_TIMEOUT
)


@dataclass
class X402PaymentRequest:
    """x402 支付请求"""
    amount: float
    resource: str
    resource_id: str
    user_id: str
    expires: int
    nonce: str
    chain: str = "base"
    version: str = "x402-0.1"
    scheme: str = "exact"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "scheme": self.scheme,
            "amount": self.amount,
            "resource": self.resource,
            "resource_id": self.resource_id,
            "to": RECEIVING_ADDRESS,
            "chain": self.chain,
            "expires": self.expires,
            "nonce": self.nonce,
            "user_id": self.user_id,
        }
    
    def to_headers(self) -> Dict[str, str]:
        """转换为 HTTP 响应头"""
        return {
            "X-402-Version": self.version,
            "X-402-Scheme": self.scheme,
            "X-402-Amount": str(self.amount),
            "X-402-Address": RECEIVING_ADDRESS,
            "X-402-Resource": f"{self.resource}:{self.resource_id}",
            "X-402-Expires": str(self.expires),
            "X-402-Chain": self.chain,
            "X-402-Nonce": self.nonce,
        }


@dataclass
class X402PaymentProof:
    """x402 支付证明（用户提交）"""
    tx_hash: str
    nonce: str
    amount: float
    from_address: str
    timestamp: int
    signature: Optional[str] = None
    
    @classmethod
    def from_token(cls, token: str) -> "X402PaymentProof":
        """从 token 解析支付证明"""
        data = json.loads(token)
        return cls(
            tx_hash=data.get("tx_hash", ""),
            nonce=data.get("nonce", ""),
            amount=float(data.get("amount", 0)),
            from_address=data.get("from", ""),
            timestamp=data.get("timestamp", 0),
            signature=data.get("signature"),
        )


class X402PaymentRequired(Exception):
    """402 Payment Required Exception"""
    def __init__(self, payment_request: X402PaymentRequest):
        self.payment_request = payment_request
        self.amount = payment_request.amount
        super().__init__(f"Payment required: ${payment_request.amount} USDC")


class PaymentMode:
    """支付模式"""
    REALTIME = "realtime"   # 实时支付
    ASYNC = "async"         # 异步支付


class X402Processor:
    """x402 支付处理器"""
    
    def __init__(self):
        self.pending_payments: Dict[str, X402PaymentRequest] = {}
        self.confirmed_payments: Dict[str, Any] = {}
    
    def calculate_price(self, mode: str, count: int = 1) -> float:
        """
        计算价格
        mode: 'per_article' | 'per_account' | 'monthly'
        count: 数量
        """
        if mode == "per_article":
            return PRICING["per_article"] * count
        elif mode == "per_account":
            return PRICING["per_account"]
        elif mode == "monthly":
            return PRICING["monthly"]
        return 0.0
    
    def determine_payment_mode(self, amount: float) -> str:
        """根据金额确定支付模式"""
        if amount >= ASYNC_THRESHOLD:
            return PaymentMode.ASYNC
        return PaymentMode.REALTIME
    
    def create_payment_request(
        self, 
        user_id: str,
        resource: str,
        resource_id: str,
        amount: float
    ) -> X402PaymentRequest:
        """创建支付请求"""
        nonce = hashlib.sha256(
            f"{user_id}{resource}{resource_id}{time.time()}".encode()
        ).hexdigest()[:16]
        
        expires = int(time.time()) + CONFIRMATION_TIMEOUT
        
        request = X402PaymentRequest(
            amount=amount,
            resource=resource,
            resource_id=resource_id,
            user_id=user_id,
            expires=expires,
            nonce=nonce,
        )
        
        # 保存待支付请求
        self.pending_payments[nonce] = request
        
        return request
    
    def verify_payment(
        self, 
        payment_proof: X402PaymentProof,
        expected_request: X402PaymentRequest
    ) -> bool:
        """
        验证支付证明
        支持两种模式:
        1. 本地验证（模拟/开发环境）
        2. 链上验证（生产环境）
        """
        # 1. 基本验证
        if payment_proof.nonce != expected_request.nonce:
            print(f"❌ Nonce 不匹配")
            return False
        
        if payment_proof.amount < expected_request.amount:
            print(f"❌ 金额不足")
            return False
        
        if time.time() > expected_request.expires:
            print(f"❌ 支付请求已过期")
            return False
        
        if payment_proof.tx_hash in self.confirmed_payments:
            print(f"❌ 交易已使用（防重放）")
            return False
        
        # 2. 链上验证（如果启用）
        use_onchain = os.getenv("X402_ONCHAIN_VERIFY", "false").lower() == "true"
        
        if use_onchain:
            return self._verify_onchain(
                payment_proof, 
                expected_request
            )
        
        # 3. 本地验证（模拟）
        print(f"⚠️  使用本地验证（模拟）")
        print(f"   生产环境请设置 X402_ONCHAIN_VERIFY=true")
        return True
    
    def _verify_onchain(
        self, 
        payment_proof: X402PaymentProof,
        expected_request: X402PaymentRequest
    ) -> bool:
        """链上验证"""
        try:
            from blockchain_verifier import create_verifier
            from config import RECEIVING_ADDRESS
            
            # 创建验证器
            network = os.getenv("BASE_NETWORK", "mainnet")
            use_basescan = os.getenv("USE_BASESCAN", "false").lower() == "true"
            api_key = os.getenv("BASE_API_KEY")  # Alchemy/Infura/BaseScan API Key
            
            verifier = create_verifier(network, use_basescan, api_key)
            
            # 执行验证
            success, message, tx_info = verifier.verify_payment(
                tx_hash=payment_proof.tx_hash,
                expected_amount=expected_request.amount,
                expected_to=RECEIVING_ADDRESS,
                min_confirmations=3
            )
            
            if success:
                print(f"✅ 链上验证通过")
                print(f"   发送方: {tx_info.from_address}")
                print(f"   确认数: {tx_info.confirmations}")
                return True
            else:
                print(f"❌ 链上验证失败: {message}")
                return False
                
        except Exception as e:
            print(f"❌ 链上验证异常: {e}")
            return False
    
    def confirm_payment(self, payment_proof: X402PaymentProof) -> None:
        """确认支付完成"""
        self.confirmed_payments[payment_proof.tx_hash] = {
            "proof": payment_proof,
            "confirmed_at": time.time(),
        }
    
    def check_payment_status(self, nonce: str) -> Optional[Dict[str, Any]]:
        """检查支付状态"""
        if nonce in self.pending_payments:
            request = self.pending_payments[nonce]
            return {
                "status": "pending",
                "amount": request.amount,
                "expires": request.expires,
                "time_remaining": request.expires - time.time(),
            }
        
        for tx_hash, data in self.confirmed_payments.items():
            if data.get("proof", {}).nonce == nonce:
                return {
                    "status": "confirmed",
                    "tx_hash": tx_hash,
                    "confirmed_at": data["confirmed_at"],
                }
        
        return None


class PaymentResult:
    """支付结果"""
    def __init__(
        self, 
        success: bool,
        amount: float = 0,
        mode: str = "",
        tx_hash: str = "",
        message: str = "",
        order_id: str = ""
    ):
        self.success = success
        self.amount = amount
        self.mode = mode
        self.tx_hash = tx_hash
        self.message = message
        self.order_id = order_id
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "amount": self.amount,
            "mode": self.mode,
            "tx_hash": self.tx_hash,
            "message": self.message,
            "order_id": self.order_id,
        }


if __name__ == "__main__":
    # 测试
    processor = X402Processor()
    
    # 计算价格
    price = processor.calculate_price("per_article", 5)
    print(f"爬5篇文章价格: ${price} USDC")
    
    # 确定支付模式
    mode = processor.determine_payment_mode(price)
    print(f"支付模式: {mode}")
    
    # 创建支付请求
    request = processor.create_payment_request(
        user_id="0xUser123",
        resource="article",
        resource_id="batch_5",
        amount=price
    )
    print(f"\n支付请求:")
    print(json.dumps(request.to_dict(), indent=2))
