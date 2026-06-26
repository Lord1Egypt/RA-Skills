"""
测试网支付管理器实现
"""

import time
import logging
from typing import Dict, Tuple, Optional
from decimal import Decimal

from app.core.config import get_settings
from app.core.exceptions import (
    InvalidUserIdError,
    InvalidTxHashError,
    DepositAlreadyProcessedError,
)
from app.core.security import validate_user_id, validate_tx_hash
from app.managers.storage import StorageBackend, create_storage_backend
from app.managers import BasePaymentManager

logger = logging.getLogger(__name__)


class TestnetPaymentManager(BasePaymentManager):
    """
    测试网支付管理器
    
    特点:
    - 使用测试网 USDC（无真实价值）
    - 自动确认充值（无需真实转账）
    - 方便测试所有功能
    """
    
    # 测试网自动充值金额
    AUTO_DEPOSIT_AMOUNT = Decimal("10")
    
    def __init__(self):
        super().__init__(cost_per_request=Decimal("0.001"))
        self.settings = get_settings()
        self.storage: StorageBackend = create_storage_backend()
        self._auto_confirm = True  # 测试网自动确认
    
    def _get_key(self, user_id: str, key_type: str) -> str:
        """生成存储键"""
        return f"pg:testnet:{user_id}:{key_type}"
    
    def get_deposit_address(self, user_id: str) -> Dict:
        """获取测试网充值信息"""
        return {
            "address": self.settings.HOSTED_WALLET or "0xTestnetWallet",
            "network": "Polygon Mumbai (Testnet)",
            "token": "USDC (Test)",
            "memo": user_id,
            "warning": "⚠️ 这是测试网，USDC 没有真实价值",
            "faucet": {
                "matic": [
                    "https://faucet.polygon.technology/",
                    "https://mumbaifaucet.com/"
                ],
                "usdc": "可以通过 Uniswap 在测试网兑换"
            },
            "auto_confirm": True
        }
    
    async def confirm_deposit(self, user_id: str, tx_hash: str) -> Dict:
        """
        确认充值（测试网自动确认）
        """
        # 验证输入
        if not validate_user_id(user_id):
            raise InvalidUserIdError()
        
        if not validate_tx_hash(tx_hash):
            raise InvalidTxHashError()
        
        # 防重放检查
        deposit_key = f"deposit:{tx_hash}"
        
        if not self.storage.setnx(deposit_key, user_id, expire=86400*7):
            raise DepositAlreadyProcessedError(tx_hash)
        
        try:
            # 测试网：尝试验证交易，但失败时仍然处理（方便测试）
            if self._auto_confirm:
                try:
                    await self._verify_testnet_deposit(tx_hash)
                except Exception as e:
                    logger.warning(f"Testnet deposit verification skipped: {e}")
            
            # 自动给予测试 USDC
            current_balance = self.get_balance(user_id)
            new_balance = current_balance + self.AUTO_DEPOSIT_AMOUNT
            
            self.storage.hset(
                self._get_key(user_id, "balance"),
                "available",
                float(new_balance)
            )
            
            return {
                "success": True,
                "amount": float(self.AUTO_DEPOSIT_AMOUNT),
                "balance": float(new_balance),
                "network": "Polygon Mumbai (Testnet)",
                "message": "🧪 测试网自动充值成功！",
                "warning": "这是测试 USDC，仅用于测试"
            }
            
        except Exception as e:
            # 发生异常，删除标记允许重试
            self.storage.delete(deposit_key)
            logger.error(f"Testnet deposit failed: {e}", exc_info=True)
            raise
    
    async def _verify_testnet_deposit(self, tx_hash: str):
        """验证测试网交易（可选）"""
        try:
            from web3 import Web3
            
            w3 = Web3(Web3.HTTPProvider(self.settings.RPC_URL))
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            
            if not receipt or receipt['status'] != 1:
                raise Exception("Transaction failed or not found")
                
        except Exception as e:
            logger.warning(f"Testnet transaction verification failed: {e}")
            raise
    
    def get_balance(self, user_id: str) -> Decimal:
        """获取余额"""
        balance = self.storage.hget(
            self._get_key(user_id, "balance"),
            "available"
        )
        return Decimal(str(balance)) if balance else Decimal("0")
    
    async def deduct(self, user_id: str, amount: Optional[Decimal] = None) -> Tuple[bool, str, Decimal]:
        """
        扣减余额
        """
        amount = amount or self.cost_per_request
        
        if not validate_user_id(user_id):
            raise InvalidUserIdError()
        
        current_balance = self.get_balance(user_id)
        
        if current_balance < amount:
            return False, f"Insufficient test balance: {current_balance} USDC", current_balance
        
        new_balance = current_balance - amount
        
        self.storage.hset(
            self._get_key(user_id, "balance"),
            "available",
            float(new_balance)
        )
        
        # 记录交易
        tx_id = f"tx_{int(time.time())}_{hex(int(time.time() * 1000))[-8:]}"
        self.storage.hset(
            self._get_key(user_id, "transactions"),
            tx_id,
            {
                "type": "deduct",
                "amount": float(amount),
                "balance_after": float(new_balance),
                "timestamp": int(time.time())
            }
        )
        
        return True, f"Deducted {amount} test USDC", new_balance
    
    def get_transaction_history(self, user_id: str, limit: int = 10) -> list:
        """获取交易历史"""
        txs = self.storage.hgetall(
            self._get_key(user_id, "transactions")
        )
        
        sorted_txs = sorted(
            txs.items(),
            key=lambda x: x[1].get("timestamp", 0),
            reverse=True
        )[:limit]
        
        return [{"id": k, **v} for k, v in sorted_txs]
    
    def reset_test_balance(self, user_id: str, amount: Decimal = Decimal("100")) -> str:
        """
        重置测试余额（仅用于测试）
        """
        self.storage.hset(
            self._get_key(user_id, "balance"),
            "available",
            float(amount)
        )
        return f"Test balance reset to {amount} USDC"
