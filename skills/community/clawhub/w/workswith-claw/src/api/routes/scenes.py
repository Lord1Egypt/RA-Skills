"""
场景管理接口
"""
from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# 模拟场景数据（后续从配置文件读取）
SCENES = {
    "movie": {"name": "观影模式", "keywords": ["看电影", "电影", "影院"]},
    "cyberpunk": {"name": "赛博朋克", "keywords": ["赛博朋克", "电竞"]},
    "bath_prep": {"name": "洗澡准备", "keywords": ["洗澡", "浴霸"]},
    "home": {"name": "回家模式", "keywords": ["回来了", "回家"]},
    "away": {"name": "离家模式", "keywords": ["出门", "上班"]},
}


@router.get("/scenes")
async def list_scenes() -> Dict[str, List[Dict]]:
    """列出所有场景"""
    return {"scenes": SCENES}


@router.get("/scenes/{scene_id}")
async def get_scene(scene_id: str) -> Dict[str, Any]:
    """获取场景详情"""
    if scene_id not in SCENES:
        return {"error": "场景不存在"}
    return SCENES[scene_id]
