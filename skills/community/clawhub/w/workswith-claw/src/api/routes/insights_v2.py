"""
数据洞察 API - v2
"""
from dotenv import load_dotenv
load_dotenv()

from fastapi import APIRouter
import os
import httpx
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()

HA_URL = os.getenv("HA_URL", "http://192.168.31.27:8123")
HA_TOKEN = os.getenv("HA_TOKEN", "")


async def fetch_states():
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


@router.get("/insights/dashboard")
async def get_insights_dashboard():
    """数据洞察首页"""
    states = await fetch_states()
    
    # 1. 家中状态
    people_count = 0
    rooms = {"客厅": False, "卧室": False, "次卧": False, "厨房": False, "卫生间": False}
    
    for s in states:
        entity_id = s.get("entity_id", "")
        state = s.get("state")
        
        # 统计人
        if entity_id.startswith("person."):
            if state == "home":
                people_count += 1
        
        # 房间状态
        name = s.get("attributes", {}).get("friendly_name", "").lower()
        if "客厅" in name and state == "on":
            rooms["客厅"] = True
        if "卧室" in name and state == "on":
            rooms["卧室"] = True
        if "次卧" in name or "扬仔" in name:
            if state == "on":
                rooms["次卧"] = True
        if "厨房" in name and state == "on":
            rooms["厨房"] = True
        if "卫生间" in name or "浴室" in name:
            if state == "on":
                rooms["卫生间"] = True
    
    # 2. 设备统计
    device_stats = {"light": 0, "climate": 0, "switch": 0, "media": 0}
    for s in states:
        entity_id = s.get("entity_id", "")
        domain = entity_id.split(".")[0] if "." in entity_id else ""
        state = s.get("state")
        
        if domain == "light" and state == "on":
            device_stats["light"] += 1
        elif domain == "climate" and state not in ["off", "unavailable"]:
            device_stats["climate"] += 1
        elif domain == "switch" and state == "on":
            device_stats["switch"] += 1
        elif domain == "media_player" and state == "playing":
            device_stats["media"] += 1
    
    # 3. 模拟活动规律数据
    activity_patterns = {
        "time_peak": "18:00 - 22:00",
        "quiet_time": "02:00 - 06:00",
        "weekend_extend": "+2小时"
    }
    
    # 4. 设备使用规律
    device_patterns = {
        "light_peak": "19:00 - 23:00",
        "ac_active": "全天活跃",
        "tv_active": "20:00 - 22:00"
    }
    
    # 5. 智能洞察
    insights = [
        {
            "type": "pattern",
            "title": "每天 19:30 左右开灯",
            "desc": "检测到规律，可以设置自动开灯",
            "suggestion": "设置每天 19:25 自动开灯"
        },
        {
            "type": "habit",
            "title": "周末用电量增加",
            "desc": "比工作日增加约 30%",
            "suggestion": "注意空调使用时长"
        },
        {
            "type": "env",
            "title": "客厅温度低于平均",
            "desc": "比全屋平均低 2°C",
            "suggestion": "可能有人开窗通风"
        }
    ]
    
    return {
        "home_status": {
            "people_count": people_count,
            "rooms": rooms,
            "text": f"{'有人' if people_count > 0 else '无人'}在家"
        },
        "device_stats": device_stats,
        "activity_patterns": activity_patterns,
        "device_patterns": device_patterns,
        "insights": insights,
        "timestamp": datetime.now().isoformat()
    }


@router.get("/insights/activity")
async def get_activity_insights():
    """活动规律分析"""
    # 后续可接入真实数据分析
    return {
        "time_peak": "18:00 - 22:00",
        "quiet_time": "02:00 - 06:00",
        "avg_outside": "08:00",
        "avg_home": "19:30"
    }


@router.get("/insights/energy")
async def get_energy_insights():
    """能耗分析"""
    return {
        "today": "12.5 kWh",
        "yesterday": "11.8 kWh",
        "week_avg": "11.2 kWh",
        "trend": "+6%"
    }


@router.get("/insights/environment")
async def get_environment_insights():
    """环境分析"""
    return {
        "temperature": {"avg": 22, "living": 21, "bedroom": 23},
        "humidity": {"avg": 45},
        "pm25": {"avg": 15, "status": "优"}
    }
