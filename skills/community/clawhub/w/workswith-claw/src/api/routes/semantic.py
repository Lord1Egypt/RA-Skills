"""
设备语义化 API
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import httpx

router = APIRouter()

HA_URL = os.getenv("HA_URL", "http://192.168.31.27:8123")
HA_TOKEN = os.getenv("HA_TOKEN", "")

# 需要过滤的域名
EXCLUDE_DOMAINS = [
    'update', 'zone', 'person', 'device_tracker',
    'conversation', 'notify', 'tts', 'todo', 'event',
    'system_health', 'input_boolean', 'input_number',
    'input_text', 'input_select', 'scene', 'script'
]

# 需要过滤的前缀
EXCLUDE_PREFIXES = [
    'sensor.uptime', 'sensor.cpu_', 'sensor.memory_',
    'sensor.network_', 'sensor.process_', 'sensor.stats_',
    'sensor.stats_', 'sensor.time_', 'sensor.date_',
    'binary_sensor.updater'
]

# 空间关键词
SPACE_KEYWORDS = {
    '客厅': ['客厅', '客厅'],
    '卧室': ['卧室', '主卧', '次卧', '主卧'],
    '厨房': ['厨房'],
    '卫生间': ['卫生间', '浴室', '洗手间', '厕所'],
    '阳台': ['阳台'],
    '玄关': ['玄关', '门厅'],
    '扬仔房间': ['扬仔', '儿童房', '小孩房', 'timothy'],
    '书房': ['书房', '工作室'],
}


def get_filter_strategy(device_count: int) -> dict:
    """根据设备数量动态调整过滤策略"""
    if device_count <= 50:
        return {
            'exclude_domains': ['update', 'zone'],
            'exclude_prefixes': ['sensor.uptime']
        }
    elif device_count <= 200:
        return {
            'exclude_domains': ['update', 'zone', 'person', 'device_tracker'],
            'exclude_prefixes': ['sensor.uptime', 'sensor.cpu_', 'sensor.network_']
        }
    else:
        return {
            'exclude_domains': EXCLUDE_DOMAINS,
            'exclude_prefixes': EXCLUDE_PREFIXES
        }


def extract_space(friendly_name: str) -> Optional[str]:
    """从设备名提取空间标签"""
    name_lower = friendly_name.lower()
    for space, keywords in SPACE_KEYWORDS.items():
        for keyword in keywords:
            if keyword.lower() in name_lower:
                return f"#{space}"
    return None


def infer_features(domain: str, attributes: dict, friendly_name: str = "") -> List[str]:
    """根据设备属性推断功能标签"""
    features = []
    name_lower = friendly_name.lower()
    
    if domain == 'light':
        if attributes.get('rgb_color'):
            features.extend(['#氛围灯', '#观影', '#电竞'])
        if attributes.get('brightness'):
            features.append('#亮度可调')
        if '吸顶' in friendly_name or '顶灯' in friendly_name:
            features.append('#主照明')
            
    if domain == 'climate':
        features.append('#温控')
        if '浴霸' in friendly_name or '暖风机' in friendly_name:
            features.append('#洗浴预热')
        if '空调' in friendly_name:
            features.append('#空调')
            
    if domain == 'cover':
        features.append('#窗帘')
        if '窗帘' in friendly_name:
            features.append('#遮光')
            
    if domain == 'switch':
        features.append('#开关')
        if '插座' in friendly_name:
            features.append('#用电监测')
            
    if domain == 'media_player':
        features.append('#影音')
        if '电视' in friendly_name or 'tv' in name_lower or '投影' in friendly_name:
            features.append('#观影')
            
    if domain == 'fan':
        features.append('#风扇')
        
    return features


async def fetch_all_states() -> List[dict]:
    """获取所有实体"""
    if not HA_TOKEN:
        return []
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(
                f"{HA_URL}/api/states",
                headers={"Authorization": f"Bearer {HA_TOKEN}"}
            )
            if resp.status_code == 200:
                return resp.json()
    except:
        pass
    return []


@router.get("/devices/analyze")
async def analyze_devices():
    """分析设备，生成语义标签"""
    states = await fetch_all_states()
    
    if not states:
        return {
            "success": False,
            "error": "无法连接 HA 或无设备",
            "total": 0,
            "valid": 0,
            "devices": [],
            "spaces": {}
        }
    
    # 获取过滤策略
    strategy = get_filter_strategy(len(states))
    exclude_domains = strategy['exclude_domains']
    exclude_prefixes = strategy['exclude_prefixes']
    
    # 过滤设备
    valid_devices = []
    for s in states:
        entity_id = s.get("entity_id", "")
        domain = entity_id.split(".")[0] if "." in entity_id else ""
        
        # 排除域名
        if domain in exclude_domains:
            continue
        
        # 排除前缀
        if any(entity_id.startswith(p) for p in exclude_prefixes):
            continue
        
        # 排除非有意义的状态
        state = s.get("state", "")
        if state in ['unavailable', 'unknown', 'none']:
            continue
            
        valid_devices.append(s)
    
    # 语义化处理
    semantic_devices = []
    spaces = {}
    
    for s in valid_devices:
        entity_id = s.get("entity_id")
        friendly_name = s.get("attributes", {}).get("friendly_name", entity_id)
        domain = entity_id.split(".")[0]
        state = s.get("state")
        attrs = s.get("attributes", {})
        
        # 提取空间
        space = extract_space(friendly_name)
        
        # 推断功能
        features = infer_features(domain, attrs, friendly_name)
        
        device = {
            "entity_id": entity_id,
            "friendly_name": friendly_name,
            "domain": domain,
            "state": state,
            "space": space,
            "tags": features,
            "confidence": 0.9 if features else 0.5
        }
        
        semantic_devices.append(device)
        
        # 统计空间
        if space:
            if space not in spaces:
                spaces[space] = []
            spaces[space].append(device)
    
    return {
        "success": True,
        "total": len(states),
        "valid": len(valid_devices),
        "devices": semantic_devices,
        "spaces": spaces,
        "stats": {
            "过滤数量": len(states) - len(valid_devices),
            "有效设备": len(valid_devices),
            "已标空间": sum(1 for d in semantic_devices if d["space"]),
            "已标功能": sum(1 for d in semantic_devices if d["tags"])
        }
    }


@router.get("/devices/scan-status")
async def get_scan_status():
    """获取扫描状态"""
    # 后续可保存扫描历史
    return {
        "last_scan": None,
        "total_scans": 0
    }
