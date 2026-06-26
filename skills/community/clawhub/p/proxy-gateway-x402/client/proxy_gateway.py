"""
Proxy Gateway Client SDK

AI Agent 外网访问客户端
"""

import requests
import os
from typing import Optional, Dict, Any
from urllib.parse import urljoin

class ProxyGatewayClient:
    """
    Proxy Gateway 客户端
    
    使用示例:
        client = ProxyGatewayClient()
        
        # 免费试用模式
        client.setup()
        proxy = client.get_proxy(region="us")
        
        # 使用代理
        import requests
        response = requests.get(
            "https://api.github.com",
            proxies=client.get_requests_proxy()
        )
    """
    
    DEFAULT_GATEWAY_URL = "https://proxy.easky.cn"
    
    def __init__(
        self,
        client_id: Optional[str] = None,
        api_key: Optional[str] = None,
        gateway_url: Optional[str] = None
    ):
        """
        初始化 Proxy Gateway 客户端
        
        Args:
            client_id: 客户端ID（免费试用模式）
            api_key: API Key（付费模式）
            gateway_url: 网关地址，默认 https://proxy.easky.cn
        """
        self.client_id = client_id
        self.api_key = api_key
        self.gateway_url = gateway_url or self.DEFAULT_GATEWAY_URL
        self.proxy_config = None
        self.free_trial_used = 0
        self.free_trial_total = 10
        
    def setup(
        self,
        client_id: Optional[str] = None,
        api_key: Optional[str] = None,
        gateway_url: Optional[str] = None
    ) -> bool:
        """
        配置 Proxy Gateway
        
        Args:
            client_id: 客户端唯一标识（免费试用）
            api_key: API Key（付费模式）
            gateway_url: 自定义网关地址
            
        Returns:
            bool: 配置是否成功
            
        Example:
            # 免费试用模式
            client.setup(client_id="my_agent_001")
            
            # 付费模式
            client.setup(api_key="pg_auth_xxx...")
        """
        if client_id:
            self.client_id = client_id
        if api_key:
            self.api_key = api_key
        if gateway_url:
            self.gateway_url = gateway_url
            
        # 验证连接
        try:
            response = requests.get(
                urljoin(self.gateway_url, "/health"),
                timeout=5
            )
            if response.status_code == 200:
                print(f"✅ Proxy Gateway 已连接")
                print(f"   网关: {self.gateway_url}")
                if self.api_key:
                    print(f"   模式: 预授权额度")
                elif self.client_id:
                    print(f"   模式: 免费体验（10次）")
                    self._check_free_trial_status()
                return True
            else:
                print(f"⚠️  网关响应异常: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False
    
    def get_proxy(
        self,
        region: str = "us",
        duration: int = 300
    ) -> Optional[Dict[str, Any]]:
        """
        获取代理
        
        Args:
            region: 地区 (us/eu/sg/jp)
            duration: 代理有效期（秒）
            
        Returns:
            代理配置或 None
            
        Example:
            proxy = client.get_proxy(region="us")
            print(f"代理: {proxy['host']}:{proxy['port']}")
        """
        headers = {"Content-Type": "application/json"}
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        elif self.client_id:
            headers["X-Client-ID"] = self.client_id
        else:
            print("❌ 未配置 client_id 或 api_key")
            return None
        
        try:
            response = requests.post(
                urljoin(self.gateway_url, "/api/v1/proxy"),
                headers=headers,
                json={"region": region, "duration": duration},
                timeout=10
            )
            
            data = response.json()
            
            if data.get("success"):
                self.proxy_config = data.get("proxy")
                
                # 显示状态
                if data.get("mode") == "free_trial":
                    remaining = data.get("remaining_free_calls", 0)
                    print(f"🎁 免费体验: 还剩 {remaining} 次")
                    self.free_trial_used = self.free_trial_total - remaining
                elif data.get("mode") == "hosted_payment":
                    balance = data.get("balance", 0)
                    print(f"💰 剩余额度: {balance} USDC")
                
                return self.proxy_config
            else:
                error = data.get("error", "Unknown error")
                message = data.get("message", "")
                
                if error == "Free Trial Exhausted":
                    print(f"⚠️  免费体验已用完（10次）")
                    print(f"   请预授权额度以继续使用:")
                    print(f"   1. 访问: {self.gateway_url}/deposit-info")
                    print(f"   2. 充值 USDC 获得 API Key")
                elif error == "Authentication Required":
                    print(f"⚠️  {message}")
                else:
                    print(f"⚠️  {error}: {message}")
                
                return None
                
        except Exception as e:
            print(f"❌ 获取代理失败: {e}")
            return None
    
    def get_requests_proxy(self) -> Optional[Dict[str, str]]:
        """
        获取 requests 库可用的代理配置
        
        Returns:
            代理配置字典，可直接传递给 requests
            
        Example:
            proxy = client.get_requests_proxy()
            response = requests.get("https://github.com", proxies=proxy)
        """
        if not self.proxy_config:
            print("⚠️  未获取代理，请先调用 get_proxy()")
            return None
        
        host = self.proxy_config.get("host", "127.0.0.1")
        port = self.proxy_config.get("port", 7893)
        proxy_type = self.proxy_config.get("type", "http")
        
        proxy_url = f"{proxy_type}://{host}:{port}"
        
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def get_free_trial_status(self) -> Optional[Dict]:
        """
        查询免费试用状态
        
        Returns:
            {"total": 10, "used": 3, "remaining": 7}
        """
        if not self.client_id:
            print("❌ 未配置 client_id")
            return None
        
        # 尝试获取代理来检查状态
        proxy = self.get_proxy()
        if proxy:
            return {
                "total": self.free_trial_total,
                "used": self.free_trial_used,
                "remaining": self.free_trial_total - self.free_trial_used
            }
        return None
    
    def get_deposit_info(self, user_id: str) -> Optional[Dict]:
        """
        获取充值信息
        
        Args:
            user_id: 用户标识
            
        Returns:
            充值地址和说明
        """
        try:
            response = requests.get(
                urljoin(self.gateway_url, f"/deposit-info?user_id={user_id}"),
                timeout=5
            )
            return response.json()
        except Exception as e:
            print(f"❌ 获取充值信息失败: {e}")
            return None
    
    def get_balance(self, user_id: str) -> Optional[float]:
        """
        查询余额
        
        Args:
            user_id: 用户标识（通常与 api_key 相同）
            
        Returns:
            余额（USDC）
        """
        try:
            response = requests.get(
                urljoin(self.gateway_url, f"/balance?user_id={user_id}"),
                timeout=5
            )
            data = response.json()
            return data.get("balance")
        except Exception as e:
            print(f"❌ 查询余额失败: {e}")
            return None
    
    def test_connection(self) -> bool:
        """
        测试代理连接
        
        Returns:
            bool: 连接是否成功
        """
        proxy = self.get_requests_proxy()
        if not proxy:
            return False
        
        try:
            response = requests.get(
                "https://httpbin.org/ip",
                proxies=proxy,
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 代理连接成功")
                print(f"   出口IP: {data.get('origin', 'unknown')}")
                return True
        except Exception as e:
            print(f"❌ 代理连接失败: {e}")
        
        return False


# 便捷函数
def setup(
    client_id: Optional[str] = None,
    api_key: Optional[str] = None,
    gateway_url: Optional[str] = None
) -> ProxyGatewayClient:
    """
    快速配置 Proxy Gateway
    
    Example:
        # 免费试用
        client = proxy_gateway.setup(client_id="my_agent")
        
        # 付费模式
        client = proxy_gateway.setup(api_key="pg_auth_xxx...")
    """
    client = ProxyGatewayClient()
    client.setup(client_id=client_id, api_key=api_key, gateway_url=gateway_url)
    return client