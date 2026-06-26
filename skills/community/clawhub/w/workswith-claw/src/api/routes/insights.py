"""
学习洞察路由 + 数据洞察
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os
import httpx
from datetime import datetime

router = APIRouter()

# 模拟数据
MOCK_HABITS = {
    "light.bedroom": {"typical_on_time": "21:30", "typical_off_time": "08:00", "confidence": 0.92},
    "light.living": {"typical_on_time": "19:00", "typical_off_time": "23:00", "confidence": 0.85}
}

# === 数据洞察 Dashboard (放在前面) ===
@router.get("/insights/dashboard")
async def get_insights_dashboard():
    """数据洞察首页"""
    HA_URL = os.getenv("HA_URL", "http://192.168.31.27:8123")
    HA_TOKEN = os.getenv("HA_TOKEN", "")
    
    states = []
    if HA_TOKEN:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get(
                    f"{HA_URL}/api/states",
                    headers={"Authorization": f"Bearer {HA_TOKEN}"}
                )
                if resp.status_code == 200:
                    states = resp.json()
        except:
            pass
    
    # 家中状态
    people_count = 0
    rooms = {"客厅": False, "卧室": False, "次卧": False, "厨房": False, "卫生间": False}
    
    for s in states:
        entity_id = s.get("entity_id", "")
        state = s.get("state")
        name = s.get("attributes", {}).get("friendly_name", "").lower()
        
        if entity_id.startswith("person.") and state == "home":
            people_count += 1
        if "客厅" in name and state == "on": rooms["客厅"] = True
        if "卧室" in name and state == "on": rooms["卧室"] = True
        if "次卧" in name or "扬仔" in name:
            if state == "on": rooms["次卧"] = True
        if "厨房" in name and state == "on": rooms["厨房"] = True
        if "卫生间" in name or "浴室" in name:
            if state == "on": rooms["卫生间"] = True
    
    insights = [
        {"type": "pattern", "title": "每天 19:30 左右开灯", "desc": "检测到规律，可以设置自动开灯", "suggestion": "设置每天 19:25 自动开灯"},
        {"type": "habit", "title": "周末用电量增加", "desc": "比工作日增加约 30%", "suggestion": "注意空调使用时长"},
        {"type": "env", "title": "客厅温度低于平均", "desc": "比全屋平均低 2°C", "suggestion": "可能有人开窗通风"}
    ]
    
    return {
        "home_status": {"people_count": people_count, "rooms": rooms, "text": f"{'有人' if people_count > 0 else '无人'}在家"},
        "activity_patterns": {"time_peak": "18:00 - 22:00", "quiet_time": "02:00 - 06:00"},
        "device_patterns": {"light_peak": "19:00 - 23:00", "tv_active": "20:00 - 22:00"},
        "insights": insights
    }

# === 原有的洞察接口 ===
class InsightReport(BaseModel):
    entity_id: str
    typical_on_time: Optional[str] = None
    typical_off_time: Optional[str] = None
    confidence: float
    suggestion: Optional[str] = None

class InsightsResponse(BaseModel):
    total_devices: int
    insights: List[InsightReport]
    summary: str

@router.get("/insights", response_model=InsightsResponse)
async def get_insights():
    insights = []
    for entity_id, habit_data in MOCK_HABITS.items():
        if habit_data.get("confidence", 0) > 0:
            suggestion = None
            if habit_data.get("confidence", 0) >= 0.8 and "light" in entity_id:
                suggestion = f"检测到您习惯 {habit_data.get('typical_off_time')} 关灯"
            insights.append(InsightReport(entity_id=entity_id, confidence=habit_data.get("confidence", 0), suggestion=suggestion))
    
    summary = f"我已经认识你的家了！观察到 {len(insights)} 个设备的使用习惯"
    return InsightsResponse(total_devices=len(MOCK_HABITS), insights=insights, summary=summary)

@router.get("/insights/{entity_id}")
async def get_entity_insight(entity_id: str):
    habit_data = MOCK_HABITS.get(entity_id)
    if not habit_data:
        return {"entity_id": entity_id, "error": "未找到"}
    return {"entity_id": entity_id, "confidence": habit_data.get("confidence", 0), "learned": habit_data.get("confidence", 0) > 0}
