"""
场景模型
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class SceneTask(BaseModel):
    """场景任务"""
    entity: str
    service: str
    data: Dict[str, Any] = {}


class Scene(BaseModel):
    """场景"""
    id: str
    name: str
    keywords: List[str] = []
    tasks: List[SceneTask] = []
    decision_tree: Optional[Dict] = None  # 决策树配置


class SceneConfig(BaseModel):
    """场景配置"""
    scenes: Dict[str, Scene] = {}
