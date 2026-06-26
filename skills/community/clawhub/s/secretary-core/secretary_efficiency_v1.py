#!/usr/bin/env python3
"""
Secretary Skill v1.0 - 效率优先版
核心：高效意图理解 + 自学习习惯 + 精准响应
"""

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import deque

class IntentType(Enum):
    """意图类型"""
    SCHEDULE = "schedule"      # 日程安排
    REMINDER = "reminder"      # 提醒
    EMAIL = "email"           # 邮件
    MEETING = "meeting"       # 会议
    TASK = "task"             # 任务
    QUERY = "query"           # 查询
    ACTION = "action"         # 执行操作

@dataclass
class UserHabit:
    """用户习惯"""
    style: str = "concise"     # concise/detailed
    work_hours: Tuple = (9, 18)
    preferred_reminder: str = "message"  # message/call/email
    decision_style: str = "quick"  # quick/careful
    common_contacts: List[str] = field(default_factory=list)
    frequent_locations: List[str] = field(default_factory=list)

@dataclass
class ConversationContext:
    """对话上下文"""
    recent_turns: deque = field(default_factory=lambda: deque(maxlen=10))
    current_task: Optional[Dict] = None
    entities: Dict = field(default_factory=dict)  # 人名/地点/时间

@dataclass
class IntentResult:
    """意图识别结果"""
    intent_type: IntentType
    confidence: float
    entities: Dict
    action_required: bool
    suggested_actions: List[str] = field(default_factory=list)

class EfficientSecretary:
    """高效秘书 v1.0"""
    
    # 意图关键词（精简高效）
    INTENT_PATTERNS = {
        IntentType.SCHEDULE: ["安排", "预定", "预约", "计划"],
        IntentType.REMINDER: ["提醒", "记得", "别忘"],
        IntentType.EMAIL: ["邮件", "email", "发给"],
        IntentType.MEETING: ["会议", "开会", "会议室"],
        IntentType.TASK: ["任务", "工作", "要做"],
        IntentType.QUERY: ["什么", "怎么", "哪里", "何时", "谁"],
        IntentType.ACTION: ["立即", "马上", "现在", "去"],
    }
    
    # 时间表达式
    TIME_PATTERNS = [
        (r"今天|今日", 0),
        (r"明天|明日", 1),
        (r"后天", 2),
        (r"上午|早上", "morning"),
        (r"下午", "afternoon"),
        (r"晚上", "evening"),
        (r"(\d+)[点時]", lambda m: int(m.group(1))),
    ]
    
    def __init__(self, verbose: bool = False):
        self.context = ConversationContext()
        self.user_habit = UserHabit()
        self.verbose = verbose
        self.habit_learning_buffer = []
        
    def understand_intent(self, text: str) -> IntentResult:
        """高效意图理解（核心）"""
        # 1. 关键词匹配
        scores = {t: 0.0 for t in IntentType}
        for intent_type, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in text.lower():
                    scores[intent_type] += 0.5
        
        # 2. 上下文增强
        if self.context.current_task:
            # 继承上文任务类型
            scores[self.context.current_task.get("type")] += 0.3
        
        # 3. 实体提取
        entities = self._extract_entities(text)
        
        # 4. 确定意图
        max_intent = max(scores, key=scores.get)
        confidence = min(1.0, scores[max_intent] + 0.5)
        
        # 5. 建议行动
        suggested = self._suggest_actions(max_intent, entities)
        
        return IntentResult(
            intent_type=max_intent,
            confidence=confidence,
            entities=entities,
            action_required=True,
            suggested_actions=suggested
        )
    
    def _extract_entities(self, text: str) -> Dict:
        """提取实体（人名/地点/时间）"""
        entities = {}
        
        # 时间
        for pattern, value in self.TIME_PATTERNS:
            match = re.search(pattern, text)
            if match:
                if isinstance(value, int):
                    entities["date"] = datetime.now() + timedelta(days=value)
                elif callable(value):
                    entities["time"] = value(match)
                else:
                    entities["time_of_day"] = value
        
        # 人名（简单实现）
        if re.search(r"[张王李赵刘陈] [总经理先生女士]", text):
            entities["person"] = re.search(r"([张王李赵刘陈] [总经理先生女士])", text).group(1)
        
        # 地点
        location_keywords = ["会议室", "办公室", "公司", "家"]
        for kw in location_keywords:
            if kw in text:
                entities["location"] = kw
        
        # 保存到上下文
        self.context.entities.update(entities)
        
        return entities
    
    def _suggest_actions(self, intent_type: IntentType, entities: Dict) -> List[str]:
        """建议行动"""
        suggestions = []
        
        if intent_type == IntentType.MEETING:
            suggestions.append("准备会议室")
            if "person" in entities:
                suggestions.append(f"通知 {entities['person']}")
            if "date" in entities:
                suggestions.append("设置提醒")
        
        elif intent_type == IntentType.EMAIL:
            suggestions.append("准备邮件模板")
            if "person" in entities:
                suggestions.append(f"查找 {entities['person']} 邮箱")
        
        elif intent_type == IntentType.REMINDER:
            suggestions.append("设置提醒时间")
            if "date" in entities:
                suggestions.append(f"确认 {entities['date']} 是否合适")
        
        return suggestions
    
    def respond(self, text: str) -> str:
        """精准响应（核心）"""
        # 1. 理解意图
        intent = self.understand_intent(text)
        
        # 2. 学习用户习惯
        self._learn_habit(text)
        
        # 3. 生成响应
        response = self._generate_efficient_response(text, intent)
        
        # 4. 更新上下文
        self._update_context(text, intent)
        
        if self.verbose:
            print(f"意图：{intent.intent_type.value} ({intent.confidence:.2f})")
            print(f"实体：{intent.entities}")
            print(f"建议：{intent.suggested_actions}")
        
        return response
    
    def _generate_efficient_response(self, text: str, intent: IntentResult) -> str:
        """生成高效响应"""
        # 根据用户习惯调整响应风格
        if self.user_habit.style == "concise":
            return self._concise_response(text, intent)
        else:
            return self._detailed_response(text, intent)
    
    def _concise_response(self, text: str, intent: IntentResult) -> str:
        """简洁响应"""
        if intent.intent_type == IntentType.MEETING:
            return f"好的，已安排会议📍。{self._format_entities(intent.entities)}"
        elif intent.intent_type == IntentType.REMINDER:
            return f"好的，已设置提醒⏰。{self._format_entities(intent.entities)}"
        elif intent.intent_type == IntentType.EMAIL:
            return f"好的，请说邮件内容📧。"
        else:
            return f"好的，已执行✅。"
    
    def _detailed_response(self, text: str, intent: IntentResult) -> str:
        """详细响应"""
        parts = [f"好的，已为您处理："]
        
        if intent.intent_type == IntentType.MEETING:
            parts.append(f"✅ 会议已安排")
            if "date" in intent.entities:
                parts.append(f"📅 时间：{intent.entities['date']}")
            if "person" in intent.entities:
                parts.append(f"👥 人员：{intent.entities['person']}")
            if "location" in intent.entities:
                parts.append(f"📍 地点：{intent.entities['location']}")
        
        if intent.suggested_actions:
            parts.append(f"\n建议：{', '.join(intent.suggested_actions)}")
        
        return '\n'.join(parts)
    
    def _format_entities(self, entities: Dict) -> str:
        """格式化实体信息"""
        parts = []
        if "date" in entities:
            parts.append(f"📅 {entities['date']}")
        if "person" in entities:
            parts.append(f"👥 {entities['person']}")
        if "location" in entities:
            parts.append(f"📍 {entities['location']}")
        return " ".join(parts) if parts else ""
    
    def _learn_habit(self, text: str):
        """学习用户习惯"""
        self.habit_learning_buffer.append(text)
        
        # 简洁度学习
        if len(text) < 20:
            self.user_habit.style = "concise"
        elif len(text) > 50:
            self.user_habit.style = "detailed"
        
        # 常用联系人学习
        if "person" in self.context.entities:
            person = self.context.entities["person"]
            if person not in self.user_habit.common_contacts:
                self.user_habit.common_contacts.append(person)
    
    def _update_context(self, text: str, intent: IntentResult):
        """更新上下文"""
        self.context.recent_turns.append({
            "text": text,
            "intent": intent.intent_type.value,
            "entities": intent.entities,
            "timestamp": datetime.now().isoformat()
        })
        
        # 更新当前任务
        if intent.action_required:
            self.context.current_task = {
                "type": intent.intent_type,
                "entities": intent.entities,
                "status": "pending"
            }
    
    def reset(self):
        """重置"""
        self.context = ConversationContext()

# 测试
def main():
    secretary = EfficientSecretary(verbose=True)
    
    test_cases = [
        "下午的会议",
        "帮我预定明天下午 2 点的会议室",
        "通知参会人员",
        "改到 3 点吧",
        "提醒我明天开会",
    ]
    
    print("=== 高效秘书测试 ===\n")
    for text in test_cases:
        print(f"用户：{text}")
        response = secretary.respond(text)
        print(f"秘书：{response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()
