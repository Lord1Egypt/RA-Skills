"""
意图解析模型
"""
from typing import Optional
from pydantic import BaseModel


class IntentResult(BaseModel):
    """意图解析结果"""
    intent_type: str  # scene, action, query
    scene_id: Optional[str] = None
    params: dict = {}
    confidence: float = 0.0
    message: str = ""


class IntentRequest(BaseModel):
    """意图执行请求"""
    utterance: str  # 用户输入
    member_id: Optional[str] = None  # 成员ID（可选）
    context: dict = {}  # 上下文
