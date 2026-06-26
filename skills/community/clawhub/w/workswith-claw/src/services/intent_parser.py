"""
意图解析器
"""
from typing import Optional
from src.models.intent import IntentResult, IntentRequest


class IntentParser:
    """意图解析器 - 关键词匹配"""
    
    # 场景关键词映射
    SCENE_KEYWORDS = {
        # 氛围场景
        "movie": ["看电影", "电影", "影院", "投影", "观影"],
        "cyberpunk": ["赛博朋克", "电竞", "游戏"],
        "romantic": ["浪漫", "约会", "烛光"],
        
        # 准备场景
        "bath_prep": ["洗澡", "洗浴", "浴霸", "我要洗澡"],
        "cook": ["做饭", "炒菜", "厨房"],
        "sleep": ["睡觉", "熄灯", "晚安"],
        
        # 来离家场景
        "home": ["回来了", "回家", "开门", "我回来了"],
        "away": ["出门", "上班", "走了", "我出门了"],
        
        # 清洁场景
        "clean": ["打扫", "扫地", "清洁"],
    }
    
    # 动作关键词
    ACTION_KEYWORDS = {
        "turn_on": ["开", "打开", "启动"],
        "turn_off": ["关", "关闭", "关掉"],
        "set_temperature": ["调温度", "温度", "设置温度"],
        "set_brightness": ["调亮度", "亮度"],
    }
    
    def parse(self, request: IntentRequest) -> IntentResult:
        """解析用户输入"""
        utterance = request.utterance
        
        # 1. 场景匹配
        scene_result = self._match_scene(utterance)
        if scene_result:
            return scene_result
        
        # 2. 动作匹配
        action_result = self._match_action(utterance)
        if action_result:
            return action_result
        
        # 3. 无法识别
        return IntentResult(
            intent_type="unknown",
            confidence=0.0,
            message="抱歉，我没听懂"
        )
    
    def _match_scene(self, utterance: str) -> Optional[IntentResult]:
        """匹配场景"""
        for scene_id, keywords in self.SCENE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in utterance:
                    # 计算置信度
                    confidence = len(keyword) / len(utterance)
                    confidence = min(confidence, 1.0)
                    
                    return IntentResult(
                        intent_type="scene",
                        scene_id=scene_id,
                        confidence=confidence,
                        message=f"识别到场景: {scene_id}"
                    )
        return None
    
    def _match_action(self, utterance: str) -> Optional[IntentResult]:
        """匹配动作"""
        for action, keywords in self.ACTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in utterance:
                    # 提取实体（简化版）
                    params = self._extract_entity(utterance)
                    
                    return IntentResult(
                        intent_type="action",
                        scene_id=action,
                        params=params,
                        confidence=0.7,
                        message=f"识别到动作: {action}"
                    )
        return None
    
    def _extract_entity(self, utterance: str) -> dict:
        """提取实体（简化版）"""
        # 这里可以接入更复杂的 NER
        params = {}
        
        if "灯" in utterance:
            params["entity"] = "light"
        elif "空调" in utterance:
            params["entity"] = "climate"
        elif "浴霸" in utterance:
            params["entity"] = "climate.bathroom_heater"
            
        return params
