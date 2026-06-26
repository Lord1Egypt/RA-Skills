"""
意图执行路由
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from src.models.intent import IntentRequest, IntentResult
from src.models.scene import SceneTask
from src.services.intent_parser import IntentParser
from src.services.scene_engine import SceneEngine
from src.services.task_orchestrator import TaskOrchestrator
from src.services.ha_client import HAClient, HAConfig

router = APIRouter()

# 全局实例（后续可通过依赖注入）
parser = IntentParser()
scene_engine = SceneEngine()

# HA 客户端初始化
ha_config = HAConfig(
    url="http://homeassistant.local:8123",
    token="your_token_here"
)
ha_client = HAClient(ha_config)
orchestrator = TaskOrchestrator(ha_client)


class IntentExecuteRequest(BaseModel):
    """意图执行请求"""
    utterance: str
    member_id: Optional[str] = None
    context: Dict[str, Any] = {}


class IntentExecuteResponse(BaseModel):
    """意图执行响应"""
    success: bool
    intent_type: str
    scene: Optional[str] = None
    message: str
    markdown: str = ""
    details: List[Dict] = []


@router.post("/intent/execute", response_model=IntentExecuteResponse)
async def execute_intent(request: IntentExecuteRequest):
    """执行用户意图"""
    
    # 1. 解析意图
    intent_request = IntentRequest(
        utterance=request.utterance,
        member_id=request.member_id,
        context=request.context
    )
    intent_result = parser.parse(intent_request)
    
    # 2. 如果是场景，执行场景任务
    if intent_result.intent_type == "scene" and intent_result.scene_id:
        scene = scene_engine.get_scene(intent_result.scene_id)
        if not scene:
            return IntentExecuteResponse(
                success=False,
                intent_type="error",
                message=f"场景 {intent_result.scene_id} 不存在"
            )
        
        # 3. 执行任务
        result = await orchestrator.execute_tasks(scene.tasks)
        
        return IntentExecuteResponse(
            success=len(result.failed) == 0,
            intent_type="scene",
            scene=intent_result.scene_id,
            message=intent_result.message,
            markdown=result.markdown,
            details=[{"entity": r.entity, "status": "ok" if r.success else "fail"} for r in result.succeeded + result.failed]
        )
    
    # 未知意图
    return IntentExecuteResponse(
        success=False,
        intent_type=intent_result.intent_type,
        message="抱歉，我没听懂"
    )


@router.get("/scenes")
async def list_scenes():
    """列出所有场景"""
    scenes = scene_engine.list_scenes()
    return {"scenes": scenes}
