"""
路由模块
"""

from fastapi import APIRouter

from .system import router as system_router
from .payment import router as payment_router
from .proxy import router as proxy_router

# 主路由
api_router = APIRouter()

# 注册子路由
# 系统路由（健康检查、根路径）- 无前缀
api_router.include_router(system_router, tags=["System"])

# 支付路由 - 根路径（deposit-info, balance 等）
api_router.include_router(payment_router, tags=["Payment"])

# 代理路由 - /api/v1 前缀
api_router.include_router(proxy_router, prefix="/api/v1", tags=["Proxy"])
