"""
代理路由
"""

from typing import Optional, Dict
from fastapi import APIRouter, Header, HTTPException, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    FreeTrialExhaustedError,
    InsufficientBalanceError,
)
from app.core.security import validate_api_key, validate_user_id
from app.managers.factory import get_payment_manager
from app.managers.proxy_manager import ProxyManager

router = APIRouter()
payment_manager = get_payment_manager()
proxy_manager = ProxyManager()


class FetchRequest(BaseModel):
    """URL 获取请求"""
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    region: str = "us"


class ProxyRequest(BaseModel):
    """代理分配请求"""
    region: str = "us"
    duration: int = 300


@router.get("/regions")
async def list_regions():
    """
    列出可用区域
    """
    return proxy_manager.get_regions()


@router.post("/fetch")
async def fetch_url(request: Request, fetch_request: FetchRequest):
    """
    通过 API 获取任意 URL 的内容
    
    这是主要的代理功能 - 用户发送 HTTP 请求参数，
    服务器代为访问目标网站并返回内容。
    """
    settings = get_settings()
    api_key = request.headers.get("X-API-Key")
    client_id = request.headers.get("X-Client-ID")
    
    # 验证认证信息
    if not api_key and not client_id:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": "Authentication Required",
                "message": "请提供 X-Client-ID header (免费试用) 或 X-API-Key (付费模式)"
            }
        )
    
    # 确定用户ID
    user_id = api_key or f"free:{client_id}"
    
    # 验证 URL
    from app.core.security import validate_url
    if not validate_url(fetch_request.url):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Invalid URL",
                "message": "URL必须以 http:// 或 https:// 开头"
            }
        )
    
    # 处理免费试用
    if not api_key:
        # 验证 client_id 格式
        if not client_id or not validate_user_id(client_id):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Invalid Client ID",
                    "message": "Client ID 格式错误（只允许字母、数字、下划线、横线，最长64字符）"
                }
            )
        
        # 检查免费试用额度
        from cachetools import TTLCache
        
        # 使用模块级缓存存储免费试用状态
        if not hasattr(fetch_url, "_free_trial_cache"):
            fetch_url._free_trial_cache = TTLCache(maxsize=100000, ttl=86400)
        
        free_trial = fetch_url._free_trial_cache.get(client_id, {
            "remaining": settings.FREE_TRIAL_LIMIT,
            "total_used": 0
        })
        
        if free_trial["remaining"] <= 0:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "error": "Free Trial Exhausted",
                    "message": f"免费体验次数已用完（{settings.FREE_TRIAL_LIMIT}次）",
                    "instructions": [
                        "1. 访问 /deposit-info?user_id=your_id 获取充值地址",
                        "2. 充值 USDC 后使用 X-API-Key 访问"
                    ]
                }
            )
        
        # 扣减免费次数
        free_trial["remaining"] -= 1
        free_trial["total_used"] += 1
        fetch_url._free_trial_cache[client_id] = free_trial
        remaining_calls = free_trial["remaining"]
        mode = "free_trial"
    else:
        # 付费模式 - 验证 API Key
        if not validate_api_key(api_key):
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "error": "Invalid API Key",
                    "message": "API Key 格式错误"
                }
            )
        
        # 扣减余额
        try:
            result = await payment_manager.charge_for_request(user_id)
            if not result["can_proceed"]:
                return JSONResponse(
                    status_code=403,
                    content={
                        "success": False,
                        "error": "Insufficient Balance",
                        "message": "余额不足",
                        "balance": result["balance"],
                        "deposit_url": f"/deposit-info?user_id={user_id}"
                    }
                )
            remaining_calls = None
            mode = "paid"
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Payment Error",
                    "message": str(e)
                }
            )
    
    # 执行 HTTP 请求
    try:
        result = await proxy_manager.fetch_url(
            url=fetch_request.url,
            method=fetch_request.method,
            headers=fetch_request.headers,
            body=fetch_request.body,
            region=fetch_request.region
        )
        
        # 添加计费信息
        result["mode"] = mode
        result["remaining_calls"] = remaining_calls
        result["cost"] = f"{settings.COST_PER_REQUEST} USDC" if mode == "paid" else "free"
        
        return result
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Request Failed",
                "message": str(e)
            }
        )


@router.post("/proxy")
async def get_proxy(request: Request, proxy_request: ProxyRequest):
    """
    获取代理配置（已弃用）
    
    ⚠️ 此端点已弃用，请使用 /fetch
    """
    return JSONResponse(
        status_code=410,
        content={
            "success": False,
            "error": "Endpoint Deprecated",
            "message": "此端点已弃用，请使用新的 /api/v1/fetch 端点",
            "new_endpoint": "/api/v1/fetch"
        }
    )
