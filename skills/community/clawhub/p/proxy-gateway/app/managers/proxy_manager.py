"""
代理管理器
管理 Clash 代理池

⚠️ 安全提示:
本模块会检查本地 Clash 代理服务的端口状态（默认 127.0.0.1:7890/7893/9090）。
这是为了检测代理可用性，仅在服务启动和状态检查时执行。
如需禁用此行为，请修改配置或设置环境变量禁用健康检查。
"""

import socket
import random
import asyncio
import logging
from typing import Optional, Dict, List
from datetime import datetime, timedelta

import httpx
import yaml

logger = logging.getLogger(__name__)


class ProxyManager:
    """管理 Clash 代理池"""
    
    def __init__(self, config_path: str = "config/proxies.yaml"):
        self.config_path = config_path
        self.active_allocations: Dict[str, dict] = {}
        self.total_calls = 0
        
        # Clash 配置
        self.clash_http_port = 7890
        self.clash_mixed_port = 7893
        self.clash_api_port = 9090
        
        self._load_config()
    
    def _load_config(self):
        """加载代理配置"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
                clash_config = config.get('clash', {})
                self.clash_http_port = clash_config.get('http_port', 7890)
                self.clash_mixed_port = clash_config.get('mixed_port', 7893)
                self.clash_api_port = clash_config.get('api_port', 9090)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
    
    def _check_port_open(self, host: str, port: int) -> bool:
        """检查端口是否开放"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def _get_clash_current_proxy(self) -> Optional[str]:
        """获取 Clash 当前代理节点"""
        try:
            resp = httpx.get(
                f"http://127.0.0.1:{self.clash_api_port}/proxies/GLOBAL",
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
        clash_available = self._check_port_open('127.0.0.1', self.clash_http_port)
        current_proxy = self._get_clash_current_proxy() if clash_available else None
        
        regions = [
            {
                'region': 'us',
                'name': 'United States',
                'available': clash_available,
                'current_node': current_proxy,
                'price_multiplier': 1.0
            },
            {
                'region': 'eu',
                'name': 'Europe',
                'available': clash_available,
                'current_node': current_proxy,
                'price_multiplier': 1.0
            },
            {
                'region': 'sg',
                'name': 'Singapore',
                'available': clash_available,
                'current_node': current_proxy,
                'price_multiplier': 1.0
            },
            {
                'region': 'jp',
                'name': 'Japan',
                'available': clash_available,
                'current_node': current_proxy,
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
        # 检查 Clash 是否运行
        if not self._check_port_open('127.0.0.1', self.clash_http_port):
            logger.error("Clash proxy not available")
            return None
        
        # 获取当前节点
        current_node = self._get_clash_current_proxy()
        
        # 创建分配记录
        allocation_id = f"{user_id}_{datetime.utcnow().timestamp()}"
        
        proxy_info = {
            'allocation_id': allocation_id,
            'host': '127.0.0.1',
            'port': self.clash_mixed_port,
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
            'note': 'Clash automatically selects optimal node'
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
            'clash_http': {
                'host': '127.0.0.1',
                'port': self.clash_http_port,
                'available': self._check_port_open('127.0.0.1', self.clash_http_port)
            },
            'clash_mixed': {
                'host': '127.0.0.1',
                'port': self.clash_mixed_port,
                'available': self._check_port_open('127.0.0.1', self.clash_mixed_port)
            },
            'clash_api': {
                'host': '127.0.0.1',
                'port': self.clash_api_port,
                'available': self._check_port_open('127.0.0.1', self.clash_api_port)
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
        proxy_url = f"http://127.0.0.1:{self.clash_mixed_port}"
        
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
