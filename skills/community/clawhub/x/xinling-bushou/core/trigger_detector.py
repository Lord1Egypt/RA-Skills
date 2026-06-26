"""
触发检测器
检测用户输入，判断是否需要触发心灵补手
"""
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from .config_manager import get_config_manager


class Scenario(Enum):
    """触发场景类型"""
    TASK_COMPLETED = "task_completed"
    SHARE_GOOD_NEWS = "share_good_news"
    DECISION_MADE = "decision_made"
    EMOTIONAL_LOW = "emotional_low"
    NEW_STAGE = "new_stage"
    GENERAL_PRAISE = "general_praise"
    EMOTIONAL_HIGH = "emotional_high"  # 用户情绪高涨（感谢等）
    SELF_NEGATIVE = "self_negative"  # 用户自我否定
    HIGH_RISK = "high_risk"  # 高风险词（轻生等）


# L1 关键词触发
L1_KEYWORDS = {
    Scenario.TASK_COMPLETED: ["完成", "搞定了", "解决了", "做完了", "成功了", "搞定了", "搞定", "完事", "收工", "搞定啦"],
    Scenario.SHARE_GOOD_NEWS: ["好消息", "太棒了", "升职了", "赚钱了", "中了", "中了彩票", "成功了", "赢", "突破", "进展"],
    Scenario.DECISION_MADE: ["决定了", "就这样", "开始干", "做了决定", "就这么办", "拍板", "决定了", "决定是", "我选"],
    Scenario.EMOTIONAL_LOW: ["累", "压力大", "不开心", "郁闷", "焦虑", "难受", "不爽", "心累", "疲惫", "烦恼"],
    Scenario.NEW_STAGE: ["新项目", "新开始", "重新", "出发", "新阶段", "新篇章", "新的开始", "开启", "起步"],
}

# L2 情绪模式 - 感谢类
THANK_KEYWORDS = ["谢谢", "感谢", "谢了", "多谢", "感恩", "谢谢你", "感谢您", "thx", "thanks"]

# L2 情绪模式 - 成就分享类
ACHIEVEMENT_KEYWORDS = ["我做出来了", "成功了", "完成了", "通过了", "拿到了", "获得了", "突破了"]

# L2 情绪模式 - 自我否定类
SELF_NEGATIVE_KEYWORDS = ["我不行", "我不会", "我不配", "我好差", "我废物", "我没用", "我做不好", "我好失败", "我不行的"]

# L2 情绪模式 - 情绪高涨类（触发高置信度）
EMOTIONAL_HIGH_KEYWORDS = ["太开心了", "太高兴了", "好兴奋", "好激动", "开心", "兴奋", "激动", "哇", "哇塞", "天哪"]

# 高风险词（轻生等）→ 切换关心模式，不触发谄媚
HIGH_RISK_KEYWORDS = ["不想活了", "活不下去了", "死了算了", "轻生", "自杀", "不想活了", "活着没意思", "人生没意义", "想死"]


@dataclass
class TriggerResult:
    """触发检测结果"""
    trigger: bool  # 是否触发
    scenario: str  # 触发场景类型
    confidence: float  # 置信度 0-1
    suggestion: str  # 建议的话术提示
    care_mode: bool = False  # 是否切换关心模式
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger": self.trigger,
            "scenario": self.scenario,
            "confidence": self.confidence,
            "suggestion": self.suggestion,
            "care_mode": self.care_mode
        }


class TriggerDetector:
    """触发检测器"""
    
    MAX_TRIGGERS_PER_SESSION = 8  # 每会话最多8次
    COOLDOWN_ROUNDS = 3  # 同一场景至少间隔3轮
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self._load_session_state()
    
    def _load_session_state(self) -> None:
        """加载会话状态"""
        config = self.config_manager.load_config()
        self.trigger_count = config.get("session_trigger_count", 0)
        self.last_trigger_round = config.get("last_trigger_round", {})
    
    def reset_session(self) -> None:
        """重置会话状态"""
        self.trigger_count = 0
        self.last_trigger_round = {}
        self.config_manager.update_config({
            "session_trigger_count": 0,
            "last_trigger_round": {}
        })
    
    def _check_high_risk(self, text: str) -> bool:
        """检查高风险词"""
        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in text:
                return True
        return False
    
    def _check_l1_keywords(self, text: str) -> List[Tuple[Scenario, float]]:
        """L1关键词检测"""
        results = []
        for scenario, keywords in L1_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text:
                    # 关键词越多，置信度越高
                    base_confidence = 0.5
                    keyword_count = sum(1 for k in keywords if k in text)
                    confidence = min(0.9, base_confidence + keyword_count * 0.1)
                    results.append((scenario, confidence))
                    break  # 只取第一个匹配的场景
        return results
    
    def _check_l2_emotion(self, text: str) -> Tuple[Optional[Scenario], float]:
        """L2情绪模式检测"""
        # 感谢
        for keyword in THANK_KEYWORDS:
            if keyword in text:
                return (Scenario.EMOTIONAL_HIGH, 0.85)
        
        # 成就
        for keyword in ACHIEVEMENT_KEYWORDS:
            if keyword in text:
                return (Scenario.EMOTIONAL_HIGH, 0.85)
        
        # 自我否定
        for keyword in SELF_NEGATIVE_KEYWORDS:
            if keyword in text:
                return (Scenario.SELF_NEGATIVE, 0.9)
        
        # 情绪高涨
        for keyword in EMOTIONAL_HIGH_KEYWORDS:
            if keyword in text:
                return (Scenario.EMOTIONAL_HIGH, 0.8)
        
        return (None, 0.0)
    
    def _check_frequency_limit(self) -> bool:
        """检查频率限制"""
        return self.trigger_count >= self.MAX_TRIGGERS_PER_SESSION
    
    def _check_cooldown(self, scenario: Scenario, current_round: int = 0) -> bool:
        """检查冷却时间"""
        last_round = self.last_trigger_round.get(scenario.value, -self.COOLDOWN_ROUNDS)
        return (current_round - last_round) < self.COOLDOWN_ROUNDS
    
    def _scenario_to_string(self, scenario: Scenario) -> str:
        """场景转字符串"""
        return scenario.value
    
    def _generate_suggestion(self, scenario: Scenario, config: Dict) -> str:
        """生成建议的话术提示"""
        persona = config.get("persona", "taijian")
        level = config.get("level", 5)
        
        # 根据场景和程度生成提示
        level_tier = "4-6"
        if level <= 3:
            level_tier = "1-3"
        elif level >= 7:
            level_tier = "7-9"
        
        suggestions = {
            Scenario.TASK_COMPLETED: f"赞扬任务完成",
            Scenario.SHARE_GOOD_NEWS: f"祝贺好消息",
            Scenario.DECISION_MADE: f"支持决定",
            Scenario.EMOTIONAL_LOW: f"关心安慰",
            Scenario.NEW_STAGE: f"鼓励新开始",
            Scenario.GENERAL_PRAISE: f"适度赞美",
            Scenario.EMOTIONAL_HIGH: f"热情回应",
            Scenario.SELF_NEGATIVE: f"关心鼓励",
            Scenario.HIGH_RISK: f"表达关心",
        }
        
        return suggestions.get(scenario, "谄媚话术")
    
    def detect(
        self, 
        text: str, 
        context: Optional[List[str]] = None,
        current_round: int = 0
    ) -> TriggerResult:
        """
        检测是否触发心灵补手
        
        Args:
            text: 用户消息文本
            context: 当前上下文（最近N轮对话）
            current_round: 当前轮次
            
        Returns:
            TriggerResult: 触发检测结果
        """
        config = self.config_manager.get_config()
        
        # 检查是否启用
        if not config.get("enabled", True):
            return TriggerResult(
                trigger=False,
                scenario="",
                confidence=0.0,
                suggestion="",
                care_mode=False
            )
        
        # 检查高风险词
        if self._check_high_risk(text):
            return TriggerResult(
                trigger=False,  # 不触发谄媚
                scenario=Scenario.HIGH_RISK.value,
                confidence=1.0,
                suggestion="表达关心和担忧",
                care_mode=True
            )
        
        # 检查频率限制
        if self._check_frequency_limit():
            return TriggerResult(
                trigger=False,
                scenario="",
                confidence=0.0,
                suggestion="频率已达上限",
                care_mode=False
            )
        
        # L1关键词检测
        l1_results = self._check_l1_keywords(text)
        
        # L2情绪检测
        l2_scenario, l2_confidence = self._check_l2_emotion(text)
        
        # 合并结果
        best_scenario = None
        best_confidence = 0.0
        
        for scenario, confidence in l1_results:
            if confidence > best_confidence:
                best_confidence = confidence
                best_scenario = scenario
        
        if l2_confidence > best_confidence:
            best_confidence = l2_confidence
            best_scenario = l2_scenario
        
        # 默认场景
        if best_scenario is None:
            best_scenario = Scenario.GENERAL_PRAISE
            best_confidence = 0.3
        
        # 检查冷却
        if self._check_cooldown(best_scenario, current_round):
            return TriggerResult(
                trigger=False,
                scenario=best_scenario.value,
                confidence=0.0,
                suggestion="冷却中",
                care_mode=False
            )
        
        # L3语义分析：当置信度 < 0.6 时，考虑上下文
        if best_confidence < 0.6 and context:
            # 简单的上下文分析
            context_text = " ".join(context[-3:])  # 最近3轮
            for scenario, keywords in L1_KEYWORDS.items():
                if any(k in context_text for k in keywords):
                    best_scenario = scenario
                    best_confidence = max(best_confidence, 0.5)
                    break
        
        # 判断是否触发
        should_trigger = best_confidence >= 0.4
        
        # 特殊场景判断
        care_mode = best_scenario == Scenario.SELF_NEGATIVE or best_scenario == Scenario.HIGH_RISK
        
        return TriggerResult(
            trigger=should_trigger,
            scenario=self._scenario_to_string(best_scenario),
            confidence=best_confidence,
            suggestion=self._generate_suggestion(best_scenario, config),
            care_mode=care_mode
        )
    
    def record_trigger(self, scenario: str, current_round: int = 0) -> None:
        """记录一次触发"""
        self.trigger_count = self.config_manager.increment_trigger_count()
        self.last_trigger_round[scenario] = current_round
        self.config_manager.update_last_trigger_round(scenario, current_round)


# 快捷函数
_detector: Optional[TriggerDetector] = None


def get_detector() -> TriggerDetector:
    """获取检测器单例"""
    global _detector
    if _detector is None:
        _detector = TriggerDetector()
    return _detector


def detect_trigger(
    text: str, 
    context: Optional[List[str]] = None,
    current_round: int = 0
) -> Dict[str, Any]:
    """快捷函数：检测触发"""
    result = get_detector().detect(text, context, current_round)
    return result.to_dict()
