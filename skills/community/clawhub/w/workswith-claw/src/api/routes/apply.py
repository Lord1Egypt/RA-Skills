"""
采纳自动化 API - 生成 YAML 文件
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import yaml

router = APIRouter()

# 自动化存储目录
AUTOMATIONS_DIR = os.path.expanduser("~/.homeassistant/automations")


class ApplyRequest(BaseModel):
    """采纳请求"""
    insight_type: str
    params: Optional[dict] = None


# 自动化模板
AUTOMATION_TEMPLATES = {
    "wake": {
        "alias": "wc_weekend_wake",
        "description": "由 Workswith Claw 自动创建 - 周末自动开灯",
        "trigger": [
            {"platform": "time", "at": "09:00:00"}
        ],
        "condition": [
            {"condition": "time", "weekday": ["sat", "sun"]}
        ],
        "action": [
            {
                "service": "light.turn_on",
                "target": {"entity_id": "light.bedroom_ceiling"},
                "data": {"brightness": 30, "kelvin": 2700}
            }
        ]
    },
    "bath": {
        "alias": "wc_bath_preheat",
        "description": "由 Workswith Claw 自动创建 - 提前开启浴霸",
        "trigger": [
            {"platform": "time", "at": "22:50:00"}
        ],
        "condition": [],
        "action": [
            {
                "service": "climate.set_temperature",
                "target": {"entity_id": "climate.bathroom_heater"},
                "data": {"temperature": 45}
            }
        ]
    },
    "light": {
        "alias": "wc_night_off",
        "description": "由 Workswith Claw 自动创建 - 定时关灯",
        "trigger": [
            {"platform": "time", "at": "23:00:00"}
        ],
        "condition": [],
        "action": [
            {
                "service": "light.turn_off",
                "target": {"entity_id": "group.all_lights"}
            }
        ]
    }
}


def create_automation_file(insight_type: str, params: dict = None) -> dict:
    """创建自动化 YAML 文件"""
    if insight_type not in AUTOMATION_TEMPLATES:
        return {"success": False, "error": "未知的洞察类型"}
    
    # 获取模板
    template = AUTOMATION_TEMPLATES[insight_type].copy()
    
    # 应用自定义参数
    if params:
        if "time" in params:
            template["trigger"][0]["at"] = params["time"]
        if "temperature" in params:
            template["action"][0]["data"]["temperature"] = params["temperature"]
        if "brightness" in params:
            template["action"][0]["data"]["brightness"] = params["brightness"]
    
    # 确保目录存在
    os.makedirs(AUTOMATIONS_DIR, exist_ok=True)
    
    # 生成文件名
    filename = f"wc_{insight_type}.yaml"
    filepath = os.path.join(AUTOMATIONS_DIR, filename)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        yaml.dump([template], f, allow_unicode=True, default_flow_style=False)
    
    return {
        "success": True,
        "file": filepath,
        "automation": template
    }


@router.post("/apply")
async def apply_automation(request: ApplyRequest):
    """采纳洞察，创建自动化"""
    result = create_automation_file(request.insight_type, request.params)
    
    if result["success"]:
        return {
            "success": True,
            "message": f"自动化已生成: {result['file']}",
            "file": result["file"],
            "automation": result["automation"],
            "yaml": yaml.dump([result["automation"]], allow_unicode=True, default_flow_style=False)
        }
    else:
        return {
            "success": False,
            "message": result.get("error", "创建失败")
        }


@router.get("/templates")
async def get_templates():
    """获取所有自动化模板"""
    return {
        "templates": list(AUTOMATION_TEMPLATES.keys()),
        "details": AUTOMATION_TEMPLATES
    }


@router.get("/automations")
async def list_automations():
    """列出已创建的自动化"""
    if not os.path.exists(AUTOMATIONS_DIR):
        return {"automations": [], "dir": AUTOMATIONS_DIR}
    
    files = [f for f in os.listdir(AUTOMATIONS_DIR) if f.startswith("wc_")]
    return {"automations": files, "dir": AUTOMATIONS_DIR}


@router.get("/ha-status")
async def ha_status():
    """检查 HA 连接状态"""
    from dotenv import load_dotenv
    load_dotenv()
    
    ha_url = os.getenv("HA_URL", "http://192.168.31.27:8123")
    ha_token = os.getenv("HA_TOKEN", "")
    
    if not ha_token:
        return {"connected": False, "error": "未配置 Token"}
    
    import httpx
    headers = {"Authorization": f"Bearer {ha_token}"}
    
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(f"{ha_url}/api/", headers=headers)
            if response.status_code == 200:
                return {"connected": True, "message": "HA 连接正常"}
            else:
                return {"connected": False, "error": f"HTTP {response.status_code}"}
    except Exception as e:
        return {"connected": False, "error": str(e)}
