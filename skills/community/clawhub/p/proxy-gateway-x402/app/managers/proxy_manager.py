"""
代理管理器 - HTTP 请求转发服务
管理上游代理配置和请求转发

本模块提供 HTTP API 请求转发功能，通过配置的代理服务器访问目标 URL。
"""

import random
import asyncio
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta

import httpx
import yaml

logger = logging.getLogger(__name__)


class ProxyManager:
    """HTTP 代理请求转发管理器"""
    
    def __init__(self, config_path: str = "config/proxies.yaml"):
        self.config_path = config_path
        self.active_allocations: Dict[str, dict] = {}
        self.total_calls = 0
        
        # 上游代理配置
        self.upstream_http_port = 7890
        self.upstream_mixed_port = 7893
        self.upstream_api_port = 9090
        
        self._load_config()
    
    def _load_config(self):
        """加载代理配置"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                clash_config = config.get('clash', {})
                self.upstream_http_port = clash_config.get('http_port', 7890)
                self.upstream_mixed_port = clash_config.get('mixed_port', 7893)
                self.upstream_api_port = clash_config.get('api_port', 9090)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
    
    async def _check_upstream_health(self, port: int) -> bool:
        """检查上游代理服务健康状态"""
        try:
            transport = httpx.AsyncHTTPTransport(proxy=f"http://localhost:{port}")
            async with httpx.AsyncClient(
                timeout=5.0,
                transport=transport
            ) as client:
                # 尝试通过代理访问一个可靠的测试地址
                response = await client.get("http://httpbin.org/ip")
                return response.status_code == 200
        except Exception:
            return False
    
    def _get_upstream_proxy(self) -> Optional[str]:
        """获取上游代理节点信息"""
        try:
            # 使用同步 httpx 获取当前代理信息
            resp = httpx.get(
                f"http://localhost:{self.upstream_api_port}/proxies/GLOBAL",
                timeout=2
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get('now', 'Unknown')
        except Exception:
            pass
        return None
    
    def get_regions(self) -> List[dict]:
        """获取可用区域列表"""
        # 简化区域信息，不实时检查上游状态
        current_proxy = self._get_upstream_proxy()
        
        regions = [
            {
                'region': 'us',
                'name': 'United States',
                'available': True,
                'current_node': current_proxy or 'Auto',
                'price_multiplier': 1.0
            },
            {
                'region': 'eu',
                'name': 'Europe',
                'available': True,
                'current_node': current_proxy or 'Auto',
                'price_multiplier': 1.0
            },
            {
                'region': 'sg',
                'name': 'Singapore',
                'available': True,
                'current_node': current_proxy or 'Auto',
                'price_multiplier': 1.0
            },
            {
                'region': 'jp',
                'name': 'Japan',
                'available': True,
                'current_node': current_proxy or 'Auto',
                'price_multiplier': 1.0
            }
        ]
        
        return regions
    
    async def allocate(self, user_id: str, region: str, duration: int) -> Optional[dict]:
        """
        分配代理
        
        Returns:
            {
                'host': str,
                'port': int,
                'type': str,
                'allocation_id': str,
                'actual_node': str
            }
        """
        # 获取当前节点
        current_node = self._get_upstream_proxy()
        
        # 创建分配记录
        allocation_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        
        proxy_info = {
            'allocation_id': allocation_id,
            'host': 'localhost',
            'port': self.upstream_mixed_port,
            'type': 'http',
            'region': region,
            'requested_region': region,
            'actual_node': current_node or 'Auto-selected',
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'expires_at': (datetime.utcnow() + timedelta(seconds=duration)).isoformat()
        }
        
        self.active_allocations[allocation_id] = proxy_info
        self.total_calls += 1
        
        # 安排清理
        asyncio.create_task(self._cleanup_allocation(allocation_id, duration))
        
        return {
            'host': proxy_info['host'],
            'port': proxy_info['port'],
            'type': proxy_info['type'],
            'allocation_id': allocation_id,
            'actual_node': proxy_info['actual_node'],
            'note': 'Auto-selects optimal node'
        }
    
    async def _cleanup_allocation(self, allocation_id: str, delay: int):
        """清理过期分配"""
        await asyncio.sleep(delay)
        self.active_allocations.pop(allocation_id, None)
    
    def release(self, allocation_id: str) -> bool:
        """手动释放代理"""
        if allocation_id in self.active_allocations:
            del self.active_allocations[allocation_id]
            return True
        return False
    
    def get_user_allocations(self, user_id: str) -> List[dict]:
        """获取用户的所有活跃分配"""
        return [
            alloc for alloc in self.active_allocations.values()
            if alloc['user_id'] == user_id
        ]
    
    def get_status(self) -> dict:
        """获取代理服务状态"""
        return {
            'upstream_http': {
                'host': 'localhost',
                'port': self.upstream_http_port
            },
            'upstream_mixed': {
                'host': 'localhost',
                'port': self.upstream_mixed_port
            },
            'upstream_api': {
                'host': 'localhost',
                'port': self.upstream_api_port
            },
            'active_allocations': len(self.active_allocations),
            'total_calls': self.total_calls
        }
    
    async def fetch_url(
        self,
        url: str,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        body: Optional[str] = None,
        region: str = "us"
    ) -> dict:
        """
        通过代理获取 URL 内容
        
        这是主要的代理功能 - 用户发送HTTP请求参数，
        服务器代为访问目标网站并返回内容。
        """
        proxy_url = f"http://localhost:{self.upstream_mixed_port}"
        
        transport = httpx.AsyncHTTPTransport(proxy=proxy_url)
        
        async with httpx.AsyncClient(
            timeout=30.0,
            follow_redirects=True,
            transport=transport
        ) as client:
            
            request_headers = headers or {}
            request_headers.setdefault("User-Agent", "ProxyGateway/0.3.0")
            
            response = await client.request(
                method=method.upper(),
                url=url,
                headers=request_headers,
                content=body
            )
            
            return {
                'success': True,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'content': response.text,
                'content_type': response.headers.get('content-type')
            }
