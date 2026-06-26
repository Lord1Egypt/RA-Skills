"""
支付管理器抽象基类

定义统一的支付接口，主网和测试网分别实现
"""

from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from decimal import Decimal


class BasePaymentManager(ABC):
    """支付管理器抽象基类"""
    
    def __init__(self, cost_per_request: Decimal = Decimal("0.001")):
        self.cost_per_request = cost_per_request
    
    @abstractmethod
    def get_deposit_address(self, user_id: str) -> Dict:
        """
        获取用户充值地址
        
        Returns:
            {
                "address": str,
                "network": str,
                "token": str,
                "memo": str,
                "instructions": List[str]
            }
        """
        pass
    
    @abstractmethod
    async def confirm_deposit(self, user_id: str, tx_hash: str) -> Dict:
        """
        确认用户充值
        
        Returns:
            {
                "success": bool,
                "amount": float,
                "balance": float,
                "message": str
            }
        """
        pass
    
    @abstractmethod
    def get_balance(self, user_id: str) -> Decimal:
        """
        获取用户余额
        
        Returns:
            Decimal: 当前余额
        """
        pass
    
    @abstractmethod
    async def deduct(self, user_id: str, amount: Optional[Decimal] = None) -> Tuple[bool, str, Decimal]:
        """
        扣减用户余额（原子操作）
        
        Returns:
            (success: bool, message: str, remaining: Decimal)
        """
        pass
    
    async def charge_for_request(self, user_id: str) -> Dict:
        """
        为单次请求扣费
        
        Returns:
            {
                "success": bool,
                "message": str,
                "balance": float,
                "can_proceed": bool
            }
        """
        success, message, remaining = await self.deduct(user_id)
        
        return {
            "success": success,
            "message": message,
            "balance": float(remaining),
            "can_proceed": success
        }
    
    @abstractmethod
    def get_transaction_history(self, user_id: str, limit: int = 10) -> list:
        """
        获取交易历史
        
        Returns:
            List[Dict]: 交易记录列表
        """
        pass
    
    def _calculate_cost(self, num_requests: int = 1) -> Decimal:
        """
        计算请求费用
        """
        return self.cost_per_request * num_requests
