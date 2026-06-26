"""
HA 设备 API - 按区域和类型分组
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter
import os
import httpx

router = APIRouter()

HA_URL = os.getenv("HA_URL", "http://192.168.31.27:8123")
HA_TOKEN = os.getenv("HA_TOKEN", "")


def get_ha_headers():
    return {"Authorization": f"Bearer {HA_TOKEN}"}


async def fetch_all_states():
    """获取所有实体状态"""
    if not HA_TOKEN:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{HA_URL}/api/states", headers=get_ha_headers())
            if resp.status_code == 200:
                return resp.json()
    except:
        pass
    return []


@router.get("/devices")
async def get_devices():
    """获取设备列表（按类型分组）"""
    states = await fetch_all_states()
    
    if not states:
        return {"devices": [], "error": "未连接 HA", "groups": {}}
    
    # 按类型分组
    groups = {}
    for s in states:
        entity_id = s.get("entity_id", "")
        domain = entity_id.split(".")[0] if "." in entity_id else "unknown"
        state = s.get("state", "unknown")
        
        if domain not in groups:
            groups[domain] = {"count": 0, "online": 0, "devices": []}
        
        groups[domain]["count"] += 1
        if state != "unavailable":
            groups[domain]["online"] += 1
        
        groups[domain]["devices"].append({
            "entity_id": entity_id,
            "state": state,
            "attributes": s.get("attributes", {})
        })
    
    return {
        "devices": states,
        "total": len(states),
        "groups": groups
    }


@router.get("/areas")
async def get_areas():
    """获取区域传感器数据"""
    states = await fetch_all_states()
    
    # 关键传感器
    key_sensors = {
        "temperature": [],
        "humidity": [],
        "light": [],
        "motion": [],
        "door_window": [],
        "switch": [],
    }
    
    for s in states:
        entity_id = s.get("entity_id", "")
        state = s.get("state", "unknown")
        attrs = s.get("attributes", {})
        friendly_name = attrs.get("friendly_name", entity_id)
        
        # 温度
        if "temperature" in entity_id.lower() or "temp" in entity_id.lower():
            try:
                val = float(state)
                key_sensors["temperature"].append({
                    "entity": entity_id,
                    "name": friendly_name,
                    "value": val,
                    "unit": attrs.get("unit_of_measurement", "°C")
                })
            except:
                pass
        
        # 湿度
        if "humidity" in entity_id.lower() or "humid" in entity_id.lower():
            try:
                val = float(state)
                key_sensors["humidity"].append({
                    "entity": entity_id,
                    "name": friendly_name,
                    "value": val,
                    "unit": attrs.get("unit_of_measurement", "%")
                })
            except:
                pass
        
        # 光照
        if "illuminance" in entity_id.lower() or "light_level" in entity_id.lower():
            try:
                val = float(state)
                key_sensors["light"].append({
                    "entity": entity_id,
                    "name": friendly_name,
                    "value": val,
                    "unit": attrs.get("unit_of_measurement", "lux")
                })
            except:
                pass
        
        # 人体传感器
        if "motion" in entity_id.lower() or "presence" in entity_id.lower():
            key_sensors["motion"].append({
                "entity": entity_id,
                "name": friendly_name,
                "value": state
            })
        
        # 门窗传感器
        if "door" in entity_id.lower() or "window" in entity_id.lower() or "contact" in entity_id.lower():
            key_sensors["door_window"].append({
                "entity": entity_id,
                "name": friendly_name,
                "value": state
            })
        
        domain = entity_id.split(".")[0] if "." in entity_id else "unknown"
        
        # 开关
        if domain == "switch" or domain == "binary_sensor":
            key_sensors["switch"].append({
                "entity": entity_id,
                "name": friendly_name,
                "value": state
            })
    
    # 清理空列表
    return {k: v for k, v in key_sensors.items() if v}
