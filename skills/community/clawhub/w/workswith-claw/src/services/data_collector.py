"""
数据采集器
"""
import asyncio
from datetime import datetime, timedelta
from typing import List, Dict, Any
from src.services.ha_client import HAClient


class DataCollector:
    """从 HA 采集数据"""
    
    def __init__(self, ha_client: HAClient):
        self.ha_client = ha_client
        self.state_history: Dict[str, List[Dict]] = {}  # entity_id -> states
    
    async def collect_states(self, entity_ids: List[str] = None) -> Dict[str, Any]:
        """采集设备状态"""
        if entity_ids:
            return await self.ha_client.get_states(entity_ids)
        else:
            return await self.ha_client.get_all_states()
    
    async def record_interaction(
        self, 
        utterance: str, 
        intent: str, 
        result: str
    ) -> None:
        """记录用户交互"""
        # 后续存入数据库
        interaction = {
            "utterance": utterance,
            "intent": intent,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
        # TODO: 存入 SQLite
        print(f"[DataCollector] Recorded: {interaction}")
    
    async def get_history(
        self, 
        entity_id: str, 
        days: int = 30
    ) -> List[Dict]:
        """获取历史数据"""
        # 后续从数据库查询
        # 目前返回模拟数据
        return self.state_history.get(entity_id, [])
    
    async def analyze_device_usage(self, entity_id: str) -> Dict[str, Any]:
        """分析设备使用情况"""
        states = await self.get_history(entity_id, days=30)
        
        if not states:
            return {
                "entity_id": entity_id,
                "total_on": 0,
                "total_off": 0,
                "average_duration": 0
            }
        
        # 简单统计
        on_count = sum(1 for s in states if s.get("state") == "on")
        off_count = sum(1 for s in states if s.get("state") == "off")
        
        return {
            "entity_id": entity_id,
            "total_on": on_count,
            "total_off": off_count,
            "sample_count": len(states)
        }
