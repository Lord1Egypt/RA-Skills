"""
Proxy Gateway - AI Agent Internet Access

AI Agent 外网访问服务 - 预授权额度模式

Example:
    import proxy_gateway
    
    # 1. 免费试用（10次）
    client = proxy_gateway.setup(client_id="my_agent_001")
    
    # 2. 获取代理
    import requests
    response = requests.get(
        "https://api.github.com",
        proxies=client.get_requests_proxy()
    )
    
    # 3. 免费用完？预授权额度
    # 访问 https://proxy.easky.cn/deposit-info
    # 充值后使用 API Key:
    client = proxy_gateway.setup(api_key="pg_auth_xxx...")
"""

from .proxy_gateway import (
    ProxyGatewayClient,
    setup
)

__version__ = "0.2.6"
__all__ = ["ProxyGatewayClient", "setup"]