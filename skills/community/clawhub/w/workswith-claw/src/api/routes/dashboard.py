"""
可视化界面数据接口
"""
from fastapi import APIRouter, File, UploadFile
from typing import Optional

router = APIRouter()


@router.get("/status/dashboard")
async def get_dashboard_status():
    """获取仪表盘数据"""
    # 返回模拟数据
    return {
        "system": {
            "status": "ok",
            "uptime": "7天",
            "learning": True
        },
        "devices": {
            "total": 1100,
            "online": 1078,
            "offline": 22,
            "lights_on": 12,
            "temp_normal": "98%",
            "switches_on": 5
        },
        "habits": [
            {
                "entity": "light.bedroom",
                "name": "卧室灯",
                "confidence": 0.92,
                "pattern": "21:30 开 → 08:00 关",
                "progress": 92
            },
            {
                "entity": "climate.bathroom_heater",
                "name": "浴霸",
                "confidence": 0.40,
                "pattern": "分析中...",
                "progress": 40
            }
        ],
        "today": {
            "intents": 23,
            "automations": 8,
            "learns": 156
        },
        "privacy": {
            "storage": "本地",
            "learning_enabled": True,
            "days": 7
        }
    }


@router.get("/settings")
async def get_settings():
    """获取设置"""
    return {
        "auto_refresh": True,
        "refresh_interval": 30,
        "voice_broadcast": False,
        "push_time": "21:00",
        "auto_execute": True,
        "learning_enabled": True
    }


@router.put("/settings")
async def update_settings(settings: dict):
    """更新设置"""
    # 后续保存到配置
    return {"success": True}
