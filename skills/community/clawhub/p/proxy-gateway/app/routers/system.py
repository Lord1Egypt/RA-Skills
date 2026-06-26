"""
系统路由 - 健康检查、根路径等
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.core.config import get_settings
from app.managers.proxy_manager import ProxyManager

router = APIRouter()
proxy_manager = ProxyManager()


@router.get("/")
async def root():
    """根路径 - 服务信息"""
    settings = get_settings()
    
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "mode": settings.NETWORK,
        "network": "Polygon Mumbai" if settings.is_testnet else "Polygon Mainnet",
        "chain_id": settings.CHAIN_ID,
        "pricing": {
            "per_request": settings.COST_PER_REQUEST,
            "currency": "USDC",
            "free_trial": f"{settings.FREE_TRIAL_LIMIT} calls" if settings.FREE_TRIAL_ENABLED else None
        },
        "endpoints": {
            "fetch": "POST /api/v1/fetch - Fetch any URL via API",
            "health": "GET /health - Health check",
            "regions": "GET /api/v1/regions - List available regions",
            "deposit": "GET /deposit-info?user_id=xxx - Get deposit address",
            "balance": "GET /balance?user_id=xxx - Check balance"
        }
    }


@router.get("/health")
async def health_check():
    """健康检查"""
    settings = get_settings()
    proxy_status = proxy_manager.get_status()
    
    # 检查 Clash 是否可用
    if not proxy_status['clash_http']['available']:
        raise HTTPException(
            status_code=503,
            detail="Clash proxy not available"
        )
    
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "network": settings.NETWORK,
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "clash_http": proxy_status['clash_http']['available'],
            "clash_mixed": proxy_status['clash_mixed']['available'],
            "clash_api": proxy_status['clash_api']['available']
        }
    }


@router.get("/network-info")
async def network_info():
    """网络信息"""
    settings = get_settings()
    
    return {
        "network": settings.NETWORK,
        "chain_id": settings.CHAIN_ID,
        "explorer": settings.EXPLORER_URL,
        "usdc_contract": settings.USDC_CONTRACT,
        "hosted_wallet": settings.HOSTED_WALLET,
        "is_testnet": settings.is_testnet
    }
