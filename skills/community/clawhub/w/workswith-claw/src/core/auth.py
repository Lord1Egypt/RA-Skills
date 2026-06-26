"""
API 认证依赖
"""
import os
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyHeader

# 从环境变量读取 API Key
API_KEY = os.getenv("WORKSWITH_CLAW_API_KEY", "")

# 请求头
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """验证 API Key"""
    # 如果没配置 API Key，跳过验证
    if not API_KEY:
        return "dev"
    
    # 验证
    if not api_key:
        raise HTTPException(
            status_code=401,
            detail="请提供 API Key"
        )
    
    if api_key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="API Key 无效"
        )
    
    return api_key


def require_auth():
    """认证依赖"""
    return Depends(verify_api_key)
