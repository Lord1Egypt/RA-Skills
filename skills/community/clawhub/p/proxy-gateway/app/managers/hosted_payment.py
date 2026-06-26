"""
主网支付管理器实现
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
    TransactionFailedError,
    InsufficientBalanceError,
)
from app.core.security import validate_user_id, validate_tx_hash
from app.managers.storage import StorageBackend, create_storage_backend
from app.managers import BasePaymentManager

logger = logging.getLogger(__name__)


class HostedPaymentManager(BasePaymentManager):
    """
    主网托管支付管理器
    
    用户流程:
    1. 用户查询充值地址
    2. 用户从自己的钱包转账 USDC 到平台地址
    3. 用户提交充值凭证
    4. 平台确认到账，更新用户余额
    5. 用户每次请求时，自动扣减余额
    """
    
    def __init__(self):
        super().__init__(cost_per_request=Decimal("0.001"))
        self.settings = get_settings()
        self.storage: StorageBackend = create_storage_backend()
    
    def _get_key(self, user_id: str, key_type: str) -> str:
        """生成存储键"""
        return f"pg:{user_id}:{key_type}"
    
    def get_deposit_address(self, user_id: str) -> Dict:
        """获取用户充值地址"""
        return {
            "address": self.settings.HOSTED_WALLET,
            "network": "Polygon",
            "token": "USDC",
            "memo": user_id,
            "instructions": [
                f"1. 转账 USDC 到地址: {self.settings.HOSTED_WALLET}",
                f"2. 必须备注 (Memo): {user_id}",
                "3. 网络: Polygon (Chain ID: 137)",
                "4. 确认后访问 /confirm-deposit 提交交易哈希"
            ]
        }
    
    async def confirm_deposit(self, user_id: str, tx_hash: str) -> Dict:
        """
        确认用户充值
        
        使用原子操作防止重放攻击
        """
        # 验证输入
        if not validate_user_id(user_id):
            raise InvalidUserIdError()
        
        if not validate_tx_hash(tx_hash):
            raise InvalidTxHashError()
        
        # 防重放检查 - 使用原子操作
        deposit_key = f"processed_deposit:{tx_hash}"
        
        if not self.storage.setnx(deposit_key, user_id, expire=86400*365):
            existing_user = self.storage.get(deposit_key)
            raise DepositAlreadyProcessedError(tx_hash)
        
        try:
            # 验证链上交易
            amount = await self._verify_onchain_deposit(tx_hash, user_id)
            
            # 更新余额
            current_balance = self.get_balance(user_id)
            new_balance = current_balance + amount
            
            self.storage.hset(
                self._get_key(user_id, "balance"),
                "available",
                float(new_balance)
            )
            
            # 记录充值
            self.storage.set(
                self._get_key(user_id, f"deposit:{tx_hash}"),
                {
                    "amount": float(amount),
                    "tx_hash": tx_hash,
                    "timestamp": int(time.time()),
                    "status": "confirmed"
                },
                expire=86400*365
            )
            
            return {
                "success": True,
                "amount": float(amount),
                "balance": float(new_balance),
                "message": f"充值成功！当前余额: {new_balance} USDC"
            }
            
        except Exception as e:
            # 发生异常，删除处理标记，允许重试
            self.storage.delete(deposit_key)
            logger.error(f"Deposit confirmation failed: {e}", exc_info=True)
            raise
    
    async def _verify_onchain_deposit(self, tx_hash: str, expected_user_id: str) -> Decimal:
        """
        验证链上存款
        
        Returns:
            Decimal: 存款金额
        
        Raises:
            TransactionFailedError: 交易失败或未找到
        """
        try:
            from web3 import Web3
            
            w3 = Web3(Web3.HTTPProvider(self.settings.RPC_URL))
            
            # 获取交易详情
            receipt = w3.eth.get_transaction_receipt(tx_hash)
            
            if not receipt:
                raise TransactionFailedError(tx_hash, "Transaction not found")
            
            if receipt['status'] != 1:
                raise TransactionFailedError(tx_hash, "Transaction failed")
            
            # 解析 USDC Transfer 事件
            transfer_topic = Web3.keccak(text="Transfer(address,address,uint256)").hex()
            
            amount = Decimal("0")
            for log in receipt['logs']:
                if log['topics'][0].hex() == transfer_topic:
                    # 检查是否是转到平台地址
                    to_address = '0x' + log['topics'][2].hex()[-40:]
                    if to_address.lower() == self.settings.HOSTED_WALLET.lower():
                        # 解析金额 (USDC 有 6 位小数)
                        amount = Decimal(int(log['data'], 16)) / Decimal(10**6)
                        break
            
            if amount <= 0:
                raise TransactionFailedError(tx_hash, "No USDC transfer found to hosted wallet")
            
            return amount
            
        except TransactionFailedError:
            raise
        except Exception as e:
            logger.error(f"On-chain verification failed: {e}", exc_info=True)
            raise TransactionFailedError(tx_hash, str(e))
    
    def get_balance(self, user_id: str) -> Decimal:
        """获取用户余额"""
        balance = self.storage.hget(
            self._get_key(user_id, "balance"),
            "available"
        )
        return Decimal(str(balance)) if balance else Decimal("0")
    
    async def deduct(self, user_id: str, amount: Optional[Decimal] = None) -> Tuple[bool, str, Decimal]:
        """
        扣减用户余额（原子操作）
        """
        amount = amount or self.cost_per_request
        
        if not validate_user_id(user_id):
            raise InvalidUserIdError()
        
        key = self._get_key(user_id, "balance")
        
        # 如果存储后端支持 Lua 脚本（Redis），使用原子操作
        if hasattr(self.storage, 'eval'):
            return await self._deduct_with_lua(key, user_id, amount)
        else:
            return await self._deduct_with_lock(key, user_id, amount)
    
    async def _deduct_with_lua(self, key: str, user_id: str, amount: Decimal) -> Tuple[bool, str, Decimal]:
        """使用 Redis Lua 脚本实现原子扣减"""
        # 输入校验 - 防止注入攻击
        if amount is None:
            amount = self.cost_per_request
        
        # 严格校验 amount 格式和范围
        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                raise ValueError("Amount must be positive")
            if amount > Decimal("1000"):  # 最大单次扣减限制
                raise ValueError("Amount exceeds maximum limit")
            # 确保最多6位小数（USDC精度）
            amount = amount.quantize(Decimal("0.000001"))
        except Exception as e:
            logger.error(f"Invalid amount: {amount}, error: {e}")
            raise ValueError(f"Invalid amount: {e}")
        
        # 校验 user_id 格式（只允许字母数字和下划线）
        if not user_id or not all(c.isalnum() or c == '_' for c in user_id):
            raise InvalidUserIdError()
        
        lua_script = """
            local balance_key = KEYS[1]
            local deduct_amount = tonumber(ARGV[1])
            local user_id = ARGV[2]
            local tx_id = ARGV[3]
            
            -- 参数校验
            if not deduct_amount or deduct_amount <= 0 then
                return {-1, "Invalid amount"}
            end
            if deduct_amount > 1000 then
                return {-1, "Amount exceeds limit"}
            end
            
            local balance = redis.call('hget', balance_key, 'available')
            if not balance then
                return {-1, "Insufficient balance: 0 USDC"}
            end
            
            balance = tonumber(balance)
            if balance < deduct_amount then
                return {-1, "Insufficient balance: " .. balance .. " USDC"}
            end
            
            local new_balance = balance - deduct_amount
            redis.call('hset', balance_key, 'available', new_balance)
            
            -- 记录交易 - 手动构造 JSON 字符串
            local timestamp = redis.call('time')[1]
            local tx_data = '{"type":"deduct","amount":' .. deduct_amount .. 
                            ',"balance_after":' .. new_balance .. 
                            ',"timestamp":' .. timestamp .. '}'
            redis.call('hset', balance_key .. ":transactions", tx_id, tx_data)
            
            return {new_balance, "Deducted " .. deduct_amount .. " USDC"}
        """
        
        tx_id = f"tx_{int(time.time())}_{hex(int(time.time() * 1000))[-8:]}"
        
        try:
            result = self.storage.eval(
                lua_script,
                1,
                key,
                str(float(amount)),
                user_id,
                tx_id
            )
            
            if result[0] == -1:
                current_balance = self.get_balance(user_id)
                raise InsufficientBalanceError(float(current_balance), float(amount))
            
            new_balance = Decimal(str(result[0]))
            return True, result[1], new_balance
            
        except InsufficientBalanceError:
            raise
        except Exception as e:
            logger.error(f"Lua deduct failed: {e}", exc_info=True)
            # 回退到锁方式
            return await self._deduct_with_lock(key, user_id, amount)
    
    async def _deduct_with_lock(self, key: str, user_id: str, amount: Decimal) -> Tuple[bool, str, Decimal]:
        """使用内存锁实现扣减（非Redis环境）"""
        import multiprocessing
        
        # 输入校验
        if amount is None:
            amount = self.cost_per_request
        
        try:
            amount = Decimal(str(amount))
            if amount <= 0:
                raise ValueError("Amount must be positive")
            if amount > Decimal("1000"):
                raise ValueError("Amount exceeds maximum limit")
            amount = amount.quantize(Decimal("0.000001"))
        except Exception as e:
            logger.error(f"Invalid amount: {amount}, error: {e}")
            raise ValueError(f"Invalid amount: {e}")
        
        # 检查多进程环境警告
        if multiprocessing.cpu_count() > 1:
            logger.warning(
                "Running in multi-process environment without Redis. "
                "Concurrent deduction protection may be limited."
            )
        
        # 简单锁实现（单进程有效）
        lock_key = f"lock:{user_id}"
        
        # 这里简化处理，实际生产环境应使用分布式锁
        current_balance = self.get_balance(user_id)
        
        if current_balance < amount:
            raise InsufficientBalanceError(float(current_balance), float(amount))
        
        # 扣减
        new_balance = current_balance - amount
        self.storage.hset(key, "available", float(new_balance))
        
        # 记录交易
        tx_id = f"tx_{int(time.time())}_{hex(int(time.time() * 1000))[-8:]}"
        self.storage.hset(
            f"{key}:transactions",
            tx_id,
            {
                "type": "deduct",
                "amount": float(amount),
                "balance_after": float(new_balance),
                "timestamp": int(time.time())
            }
        )
        
        return True, f"Deducted {amount} USDC", new_balance
    
    def get_transaction_history(self, user_id: str, limit: int = 10) -> list:
        """获取交易历史"""
        txs = self.storage.hgetall(
            self._get_key(user_id, "transactions")
        )
        
        # 排序并限制数量
        sorted_txs = sorted(
            txs.items(),
            key=lambda x: x[1].get("timestamp", 0),
            reverse=True
        )[:limit]
        
        return [{"id": k, **v} for k, v in sorted_txs]
