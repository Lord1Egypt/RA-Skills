"""
支付管理器工厂
"""

from app.core.config import get_settings
from app.managers.hosted_payment import HostedPaymentManager
from app.managers.testnet_payment import TestnetPaymentManager


def create_payment_manager():
    """
    根据配置创建支付管理器
    
    Returns:
        BasePaymentManager: 主网或测试网支付管理器
    """
    settings = get_settings()
    
    if settings.is_testnet:
        return TestnetPaymentManager()
    else:
        return HostedPaymentManager()


# 单例缓存
_payment_manager = None


def get_payment_manager():
    """获取支付管理器单例"""
    global _payment_manager
    if _payment_manager is None:
        _payment_manager = create_payment_manager()
    return _payment_manager
