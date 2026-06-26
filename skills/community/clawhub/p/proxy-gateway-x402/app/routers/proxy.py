"""
代理路由 - x402 支付版本
按次付费，无需托管用户资金
"""
import json
from typing import Optional, Dict
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import get_settings
from app.core.security import validate_url
from app.middleware.x402_payment import (
    X402PaymentMiddleware,
    X402PaymentRequired,
    require_x402_payment
)
from app.managers.proxy_manager import ProxyManager

router = APIRouter()
proxy_manager = ProxyManager()
payment_middleware = X402PaymentMiddleware()


class FetchRequest(BaseModel):
    """URL 获取请求"""
    url: str
    method: str = "GET"
    headers: Optional[Dict[str, str]] = None
    body: Optional[str] = None
    region: str = "us"
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://api.github.com/users/github",
                "method": "GET",
                "region": "us"
            }
        }


@router.get("/regions")
async def list_regions():
    """
    列出可用代理区域
    
    无需支付，免费查询
    """
    return proxy_manager.get_regions()


@router.post("/fetch")
async def fetch_url(
    request: Request,
    fetch_request: FetchRequest
):
    """
    通过代理获取任意 URL 内容
    
    ## 付费说明
    
    本端点需要支付 **0.001 USDC** 每次调用
    
    ### 支付方式
    
    **方式一：自动支付（推荐）**
    ```bash
    export USER_EVM_PRIVATE_KEY="0xYourPrivateKey"
    # 使用 SDK 自动签名支付
    ```
    
    **方式二：手动支付**
    1. 首次调用会返回 `402 Payment Required`
    2. 按响应中的要求支付 USDC
    3. 将交易哈希放入 `X-Payment-Response` 请求头重试
    
    ### 请求头
    
    - `X-Payment-Response`: 支付凭证（JSON格式 {"tx_hash": "0x..."}）
    
    ## 示例
    
    ```bash
    curl -X POST https://proxy-gateway-x402.easky.cn/api/v1/fetch \\
      -H "Content-Type: application/json" \\
      -H 'X-Payment-Response: {"tx_hash": "0x..."}' \\
      -d '{"url": "https://api.github.com/users/github", "method": "GET"}'
    ```
    """
    settings = get_settings()
    
    # 验证 URL
    if not validate_url(fetch_request.url):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Invalid URL",
                "message": "URL必须以 http:// 或 https:// 开头"
            }
        )
    
    try:
        # x402 支付验证
        payment_info = await payment_middleware.verify_payment(request)
        
        # 支付验证通过，执行代理请求
        result = await proxy_manager.fetch_url(
            url=fetch_request.url,
            method=fetch_request.method,
            headers=fetch_request.headers,
            body=fetch_request.body,
            region=fetch_request.region
        )
        
        # 添加支付信息
        result["payment"] = {
            "verified": True,
            "tx_hash": payment_info.get("tx_hash"),
            "amount": str(settings.COST_PER_REQUEST),
            "token": "USDC",
            "network": settings.X402_CHAIN
        }
        
        return result
        
    except X402PaymentRequired as e:
        # 返回 402 Payment Required
        return JSONResponse(
            status_code=402,
            content={
                "success": False,
                "error": "Payment Required",
                "message": "此请求需要支付",
                **e.payment_details
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Request Failed",
                "message": str(e)
            }
        )


@router.get("/price")
async def get_price():
    """
    查询当前价格
    
    无需支付，免费查询
    """
    settings = get_settings()
    return {
        "price": str(settings.COST_PER_REQUEST),
        "token": "USDC",
        "network": settings.X402_CHAIN,
        "token_contract": payment_middleware.usdc_contract.address if hasattr(payment_middleware, 'usdc_contract') else None,
        "recipient": settings.DEVELOPER_WALLET
    }


@router.post("/auto-pay-demo")
async def auto_pay_demo(
    request: Request,
    fetch_request: FetchRequest
):
    """
    自动支付演示端点
    
    如果环境变量设置了 USER_EVM_PRIVATE_KEY，自动完成支付并执行请求
    """
    import os
    
    private_key = os.getenv("USER_EVM_PRIVATE_KEY")
    if not private_key:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "error": "Auto-Pay Not Configured",
                "message": "请设置 USER_EVM_PRIVATE_KEY 环境变量启用自动支付",
                "instructions": [
                    "export USER_EVM_PRIVATE_KEY=0xYourPrivateKey",
                    "注意：使用专用小额钱包，勿用主钱包"
                ]
            }
        )
    
    try:
        # 执行自动支付
        payment_result = await payment_middleware.auto_pay(private_key)
        
        # 构造支付凭证头
        payment_header = json.dumps({
            "tx_hash": payment_result["tx_hash"]
        })
        
        # 创建新的请求头用于验证
        class MockRequest:
            def __init__(self, headers):
                self.headers = headers
        
        mock_request = MockRequest({
            "X-Payment-Response": payment_header
        })
        
        # 验证支付
        payment_info = await payment_middleware.verify_payment(mock_request)
        
        # 执行代理请求
        result = await proxy_manager.fetch_url(
            url=fetch_request.url,
            method=fetch_request.method,
            headers=fetch_request.headers,
            body=fetch_request.body,
            region=fetch_request.region
        )
        
        result["payment"] = {
            "auto_paid": True,
            "tx_hash": payment_result["tx_hash"],
            "amount": payment_result["amount"],
            "token": payment_result["token"],
            "network": payment_result["network"]
        }
        
        return result
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": "Auto-Pay Failed",
                "message": str(e)
            }
        )
