"""
建议确认路由
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.services.suggestion_engine import SuggestionEngine, Suggestion

router = APIRouter()

# 全局实例
engine = SuggestionEngine()


class SuggestionResponse(BaseModel):
    """建议响应"""
    id: str
    entity_id: str
    message: str
    confidence: float
    status: str


class SuggestionActionRequest(BaseModel):
    """建议操作请求"""
    entity_id: str
    action: str  # accept, reject


# 模拟建议数据
MOCK_SUGGESTIONS = {
    "light.bedroom": Suggestion(
        id="sug_light_bedroom_1",
        entity_id="light.bedroom",
        suggestion_type="auto_off",
        trigger_time="23:00",
        action={"service": "turn_off", "entity": "light.bedroom"},
        message="检测到您习惯 23:00 关灯，是否自动执行？",
        confidence=0.92,
        status="pending"
    ),
    "light.living": Suggestion(
        id="sug_light_living_1",
        entity_id="light.living",
        suggestion_type="auto_off",
        trigger_time="23:00",
        action={"service": "turn_off", "entity": "light.living"},
        message="检测到您习惯 23:00 关灯，是否自动执行？",
        confidence=0.85,
        status="pending"
    )
}


@router.get("/suggestions", response_model=List[SuggestionResponse])
async def get_suggestions():
    """获取所有建议"""
    return [
        SuggestionResponse(
            id=s.id,
            entity_id=s.entity_id,
            message=s.message,
            confidence=s.confidence,
            status=s.status
        )
        for s in MOCK_SUGGESTIONS.values()
        if s.status == "pending"
    ]


@router.post("/suggestions/{entity_id}/accept")
async def accept_suggestion(entity_id: str):
    """接受建议"""
    if entity_id not in MOCK_SUGGESTIONS:
        raise HTTPException(status_code=404, detail="建议不存在")
    
    suggestion = MOCK_SUGGESTIONS[entity_id]
    suggestion.status = "accepted"
    
    return {
        "success": True,
        "message": f"已接受建议：{suggestion.message}",
        "action": suggestion.action
    }


@router.post("/suggestions/{entity_id}/reject")
async def reject_suggestion(entity_id: str):
    """拒绝建议"""
    if entity_id not in MOCK_SUGGESTIONS:
        raise HTTPException(status_code=404, detail="建议不存在")
    
    suggestion = MOCK_SUGGESTIONS[entity_id]
    suggestion.status = "rejected"
    
    return {
        "success": True,
        "message": "已拒绝建议"
    }


@router.get("/suggestions/{entity_id}")
async def get_suggestion(entity_id: str):
    """获取单个建议"""
    if entity_id not in MOCK_SUGGESTIONS:
        raise HTTPException(status_code=404, detail="建议不存在")
    
    s = MOCK_SUGGESTIONS[entity_id]
    return {
        "id": s.id,
        "entity_id": s.entity_id,
        "message": s.message,
        "confidence": s.confidence,
        "status": s.status,
        "trigger_time": s.trigger_time
    }
