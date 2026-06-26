"""
建议生成器
"""
from typing import Optional
from pydantic import BaseModel
from src.models.habit import HabitReport


class Suggestion(BaseModel):
    """自动化建议"""
    id: str
    entity_id: str
    suggestion_type: str  # auto_off, auto_on, temperature
    trigger_time: str
    action: dict
    message: str
    confidence: float
    status: str = "pending"  # pending, accepted, rejected


class SuggestionEngine:
    """基于习惯生成自动化建议"""
    
    def __init__(self):
        self.suggestions = {}  # entity_id -> Suggestion
    
    def generate(self, habit: HabitReport) -> Optional[Suggestion]:
        """生成建议"""
        
        # 检查置信度
        if habit.confidence < 0.8:
            return None
        
        # 检查是否已有活跃建议
        if habit.entity_id in self.suggestions:
            existing = self.suggestions[habit.entity_id]
            if existing.status == "pending":
                return None
        
        # 根据习惯类型生成建议
        if habit.typical_off_time and "light" in habit.entity_id:
            # 关灯建议
            suggestion = Suggestion(
                id=f"sug_{habit.entity_id}_{habit.typical_off_time}",
                entity_id=habit.entity_id,
                suggestion_type="auto_off",
                trigger_time=habit.typical_off_time,
                action={
                    "service": "turn_off",
                    "entity": habit.entity_id
                },
                message=f"检测到您习惯在 {habit.typical_off_time} 关灯，是否自动执行？",
                confidence=habit.confidence
            )
            self.suggestions[habit.entity_id] = suggestion
            return suggestion
        
        if habit.typical_on_time and "climate" in habit.entity_id:
            # 温度建议
            suggestion = Suggestion(
                id=f"sug_{habit.entity_id}_{habit.typical_on_time}",
                entity_id=habit.entity_id,
                suggestion_type="auto_on",
                trigger_time=habit.typical_on_time,
                action={
                    "service": "turn_on",
                    "entity": habit.entity_id
                },
                message=f"检测到您习惯在 {habit.typical_on_time} 使用空调，是否自动开启？",
                confidence=habit.confidence
            )
            self.suggestions[habit.entity_id] = suggestion
            return suggestion
        
        return None
    
    def accept(self, entity_id: str) -> bool:
        """接受建议"""
        if entity_id in self.suggestions:
            self.suggestions[entity_id].status = "accepted"
            return True
        return False
    
    def reject(self, entity_id: str) -> bool:
        """拒绝建议"""
        if entity_id in self.suggestions:
            self.suggestions[entity_id].status = "rejected"
            return True
        return False
    
    def get_pending(self) -> list:
        """获取待确认的建议"""
        return [
            s for s in self.suggestions.values() 
            if s.status == "pending"
        ]
