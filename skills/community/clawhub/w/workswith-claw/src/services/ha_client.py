"""
Home Assistant REST API 客户端 - 单例模式
"""
import os
import aiohttp
from typing import Optional
from pydantic import BaseModel, Field


class HAConfig(BaseModel):
    """HA 配置 - 从环境变量读取"""
    url: str = Field(default_factory=lambda: os.getenv("HA_URL", ""))
    token: str = Field(default_factory=lambda: os.getenv("HA_TOKEN", ""))
    
    def __init__(self, **data):
        if "url" not in data or not data["url"]:
            data["url"] = os.getenv("HA_URL", "http://homeassistant.local:8123")
        if "token" not in data or not data["token"]:
            data["token"] = os.getenv("HA_TOKEN", "")
        super().__init__(**data)
    
    def validate_config(self) -> bool:
        return bool(self.url and self.token)


class HAClient:
    """异步 HA REST API 客户端 - 单例模式"""
    
    _instance: Optional['HAClient'] = None
    _session: Optional[aiohttp.ClientSession] = None
    
    def __new__(cls, config: HAConfig = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: HAConfig = None):
        if self._initialized:
            return
            
        self.config = config or HAConfig()
        self.url = self.config.url.rstrip('/') if self.config.url else ""
        self.token = self.config.token
        self._initialized = True
    
    @classmethod
    def get_instance(cls, config: HAConfig = None) -> 'HAClient':
        """获取单例实例"""
        return cls(config)
    
    def update_config(self, url: str = None, token: str = None):
        """更新配置"""
        if url:
            self.url = url.rstrip('/')
        if token:
            self.token = token
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """获取或创建会话（复用连接）"""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {self.token}"},
                timeout=aiohttp.ClientTimeout(total=30),
                connector=aiohttp.TCPConnector(
                    limit=100,  # 连接池大小
                    limit_per_host=30
                )
            )
        return self._session
    
    async def close(self):
        """关闭会话"""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    async def call_service(self, domain: str, service: str, **data) -> dict:
        """调用 HA 服务"""
        if not self.token:
            raise Exception("HA Token 未配置")
            
        session = await self._get_session()
        url = f"{self.url}/api/services/{domain}/{service}"
        
        async with session.post(url, json=data) as resp:
            result = await resp.json()
            if resp.status >= 400:
                raise Exception(f"HA API Error: {result}")
            return result
    
    async def get_state(self, entity_id: str) -> dict:
        """获取实体状态"""
        if not self.token:
            raise Exception("HA Token 未配置")
            
        session = await self._get_session()
        url = f"{self.url}/api/states/{entity_id}"
        
        async with session.get(url) as resp:
            result = await resp.json()
            if resp.status >= 400:
                raise Exception(f"HA API Error: {result}")
            return result
    
    async def get_states(self, entity_ids: list[str]) -> list[dict]:
        """批量获取状态"""
        results = []
        for entity_id in entity_ids:
            try:
                state = await self.get_state(entity_id)
                results.append(state)
            except Exception:
                results.append({"entity_id": entity_id, "error": True})
        return results
    
    async def get_all_states(self) -> list[dict]:
        """获取所有实体状态"""
        if not self.token:
            raise Exception("HA Token 未配置")
            
        session = await self._get_session()
        url = f"{self.url}/api/states"
        
        async with session.get(url) as resp:
            result = await resp.json()
            if resp.status >= 400:
                raise Exception(f"HA API Error: {result}")
            return result
    
    async def fire_event(self, event_type: str, event_data: dict = None) -> dict:
        """触发 HA 事件"""
        if not self.token:
            raise Exception("HA Token 未配置")
            
        session = await self._get_session()
        url = f"{self.url}/api/events/{event_type}"
        
        async with session.post(url, json=event_data or {}) as resp:
            result = await resp.json()
            if resp.status >= 400:
                raise Exception(f"HA API Error: {result}")
            return result
