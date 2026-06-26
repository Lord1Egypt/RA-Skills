import time
from typing import Dict, Any, List, Optional, Tuple


HESITATION_THRESHOLDS: Dict[str, Dict[str, float]] = {
    "en_US": {"short": 0.3, "medium": 0.8, "long": 2.0},
    "en_GB": {"short": 0.35, "medium": 0.9, "long": 2.2},
    "zh_CN": {"short": 0.5, "medium": 1.5, "long": 3.0},
    "zh_TW": {"short": 0.5, "medium": 1.5, "long": 3.0},
    "ja_JP": {"short": 0.4, "medium": 1.2, "long": 2.5},
    "ko_KR": {"short": 0.35, "medium": 1.0, "long": 2.5},
    "de_DE": {"short": 0.35, "medium": 0.9, "long": 2.0},
    "fr_FR": {"short": 0.35, "medium": 0.9, "long": 2.0},
    "es_ES": {"short": 0.3, "medium": 0.8, "long": 2.0},
    "pt_BR": {"short": 0.3, "medium": 0.8, "long": 2.0},
    "ru_RU": {"short": 0.35, "medium": 1.0, "long": 2.5},
    "ar_SA": {"short": 0.4, "medium": 1.2, "long": 3.0},
    "hi_IN": {"short": 0.35, "medium": 1.0, "long": 2.5},
}

DEFAULT_THRESHOLDS = HESITATION_THRESHOLDS["en_US"]


class CulturalPauseAdapter:
    """文化适配的停顿分析器

    问题场景：
    - 不同语言/文化下，"犹豫"的停顿阈值差异很大
    - 英文0.5秒可能算犹豫，中文可能需要1.5秒才算是犹豫

    解决方案：
    - 为不同文化/语言预设停顿阈值
    - 支持文化自动检测和手动指定
    - 提供文化特定的停顿类型判断
    """

    def __init__(self, culture: str = "en_US"):
        self._culture = culture
        self._thresholds = HESITATION_THRESHOLDS.get(culture, DEFAULT_THRESHOLDS)

    @property
    def culture(self) -> str:
        """当前文化"""
        return self._culture

    def set_culture(self, culture: str) -> bool:
        """设置文化

        Args:
            culture: 文化代码（如 zh_CN, en_US, ja_JP）

        Returns:
            是否设置成功
        """
        if culture in HESITATION_THRESHOLDS:
            self._culture = culture
            self._thresholds = HESITATION_THRESHOLDS[culture]
            return True
        return False

    def get_thresholds(self) -> Dict[str, float]:
        """获取当前文化的阈值

        Returns:
            阈值字典
        """
        return dict(self._thresholds)

    def classify_pause(self, duration: float) -> str:
        """分类停顿类型

        Args:
            duration: 停顿持续时间（秒）

        Returns:
            停顿类型: very_short, short, medium, long, very_long
        """
        if duration < self._thresholds["short"] * 0.5:
            return "very_short"
        elif duration < self._thresholds["short"]:
            return "short"
        elif duration < self._thresholds["medium"]:
            return "medium"
        elif duration < self._thresholds["long"]:
            return "long"
        else:
            return "very_long"

    def is_hesitation(self, duration: float) -> bool:
        """判断是否是犹豫

        Args:
            duration: 停顿持续时间（秒）

        Returns:
            是否是犹豫
        """
        return self.classify_pause(duration) in ["medium", "long", "very_long"]

    def is_interruption(self, duration: float) -> bool:
        """判断是否是打断

        Args:
            duration: 停顿持续时间（秒）

        Returns:
            是否是打断
        """
        return duration < self._thresholds["short"]

    def is_waiting(self, duration: float) -> bool:
        """判断是否是等待回应

        Args:
            duration: 停顿持续时间（秒）

        Returns:
            是否是等待回应
        """
        return duration >= self._thresholds["long"]

    def get_pause_description(self, duration: float) -> str:
        """获取停顿的文化适应描述

        Args:
            duration: 停顿持续时间（秒）

        Returns:
            停顿描述
        """
        pause_type = self.classify_pause(duration)

        descriptions = {
            "very_short": "极短停顿（快速接话）",
            "short": "短停顿（思考中）",
            "medium": "中等停顿（犹豫）",
            "long": "长停顿（等待回应）",
            "very_long": "很长停顿（明显等待）"
        }

        return descriptions.get(pause_type, "未知")

    @staticmethod
    def get_supported_cultures() -> List[str]:
        """获取支持的文化列表

        Returns:
            文化代码列表
        """
        return list(HESITATION_THRESHOLDS.keys())

    @staticmethod
    def detect_culture_from_text(text: str) -> str:
        """从文本中检测文化/语言

        Args:
            text: 输入文本

        Returns:
            可能的文化代码
        """
        chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
        japanese_chars = sum(1 for c in text if '\u3040' <= c <= '\u309f' or '\u30a0' <= c <= '\u30ff')
        korean_chars = sum(1 for c in text if '\uac00' <= c <= '\ud7af')
        arabic_chars = sum(1 for c in text if '\u0600' <= c <= '\u06ff')
        devanagari_chars = sum(1 for c in text if '\u0900' <= c <= '\u097f')

        total_chars = len(text.strip())
        if total_chars == 0:
            return "en_US"

        if chinese_chars / total_chars > 0.3:
            return "zh_CN"
        elif japanese_chars / total_chars > 0.3:
            return "ja_JP"
        elif korean_chars / total_chars > 0.3:
            return "ko_KR"
        elif arabic_chars / total_chars > 0.3:
            return "ar_SA"
        elif devanagari_chars / total_chars > 0.3:
            return "hi_IN"

        return "en_US"


class SocialTemporal:
    """社交时序理解 - 增强版

    负责理解对话中的停顿和节奏，实现自然的交互
    V2.1增强：
    - 文化适配的停顿分析
    - 多语言支持
    - 跨文化社交场景理解
    """

    def __init__(self, culture: str = "en_US"):
        self.conversation_history: List[Dict[str, Any]] = []
        self._pause_adapter = CulturalPauseAdapter(culture=culture)

    @property
    def culture(self) -> str:
        """当前文化"""
        return self._pause_adapter.culture

    def set_culture(self, culture: str) -> bool:
        """设置文化"""
        return self._pause_adapter.set_culture(culture)

    def record_utterance(
        self,
        speaker: str,
        content: str,
        timestamp: Optional[float] = None,
        detect_culture: bool = True
    ):
        """记录对话

        Args:
            speaker: 说话者
            content: 内容
            timestamp: 时间戳
            detect_culture: 是否自动检测文化
        """
        if timestamp is None:
            timestamp = time.time()

        if detect_culture and not self._pause_adapter:
            detected = CulturalPauseAdapter.detect_culture_from_text(content)
            self._pause_adapter.set_culture(detected)

        self.conversation_history.append({
            'speaker': speaker,
            'content': content,
            'timestamp': timestamp,
            'culture': self._pause_adapter.culture
        })

    def get_last_utterance(self) -> Optional[Dict[str, Any]]:
        """获取最后一次对话

        Returns:
            最后一次对话
        """
        if self.conversation_history:
            return self.conversation_history[-1]
        return None

    def get_pause_duration(self) -> float:
        """获取当前停顿时间

        Returns:
            停顿时间
        """
        last_utterance = self.get_last_utterance()
        if last_utterance:
            return time.time() - last_utterance['timestamp']
        return 0.0

    def get_pause_type(self, duration: Optional[float] = None) -> str:
        """获取停顿类型（文化适配）

        Args:
            duration: 停顿时间，如果为None则自动计算

        Returns:
            停顿类型
        """
        if duration is None:
            duration = self.get_pause_duration()
        return self._pause_adapter.classify_pause(duration)

    def get_pause_description(self, duration: Optional[float] = None) -> str:
        """获取停顿的文化适应描述

        Args:
            duration: 停顿时间，如果为None则自动计算

        Returns:
            停顿描述
        """
        if duration is None:
            duration = self.get_pause_duration()
        return self._pause_adapter.get_pause_description(duration)

    def is_hesitation(self, duration: Optional[float] = None) -> bool:
        """判断是否是犹豫（文化适配）

        Args:
            duration: 停顿时间，如果为None则自动计算

        Returns:
            是否是犹豫
        """
        if duration is None:
            duration = self.get_pause_duration()
        return self._pause_adapter.is_hesitation(duration)

    def should_respond(self) -> bool:
        """判断是否应该回应

        Returns:
            是否应该回应
        """
        pause_duration = self.get_pause_duration()
        return self._pause_adapter.is_hesitation(pause_duration)

    def is_interruption(self, timestamp: Optional[float] = None) -> bool:
        """判断是否是打断

        Args:
            timestamp: 时间戳，如果为None则使用当前时间

        Returns:
            是否是打断
        """
        if timestamp is None:
            timestamp = time.time()

        last_utterance = self.get_last_utterance()
        if last_utterance:
            pause_duration = timestamp - last_utterance['timestamp']
            return self._pause_adapter.is_interruption(pause_duration)
        return False

    def is_waiting(self, duration: Optional[float] = None) -> bool:
        """判断是否是等待回应

        Args:
            duration: 停顿时间，如果为None则自动计算

        Returns:
            是否是等待回应
        """
        if duration is None:
            duration = self.get_pause_duration()
        return self._pause_adapter.is_waiting(duration)

    def get_context_timeliness(self, context_timestamp: float) -> str:
        """获取上下文时效性

        Args:
            context_timestamp: 上下文时间戳

        Returns:
            时效性: very_recent, recent, within_day, old
        """
        current_time = time.time()
        time_diff = current_time - context_timestamp

        if time_diff < 60:
            return 'very_recent'
        elif time_diff < 3600:
            return 'recent'
        elif time_diff < 86400:
            return 'within_day'
        else:
            return 'old'

    def get_conversation_flow(self) -> List[Dict[str, Any]]:
        """获取对话流程（包含文化适配的停顿分析）

        Returns:
            对话流程
        """
        flow = []
        for i, utterance in enumerate(self.conversation_history):
            item = {
                'speaker': utterance['speaker'],
                'content': utterance['content'],
                'timestamp': utterance['timestamp'],
                'culture': utterance.get('culture', self._pause_adapter.culture)
            }

            if i > 0:
                previous = self.conversation_history[i-1]
                pause_duration = utterance['timestamp'] - previous['timestamp']
                item['pause_before'] = pause_duration
                item['pause_type'] = self.get_pause_type(pause_duration)
                item['pause_description'] = self.get_pause_description(pause_duration)
                item['is_hesitation'] = self._pause_adapter.is_hesitation(pause_duration)
                item['is_interruption'] = self._pause_adapter.is_interruption(pause_duration)

            flow.append(item)

        return flow

    def get_cross_cultural_insight(self) -> Dict[str, Any]:
        """获取跨文化洞察

        Returns:
            跨文化分析结果
        """
        cultures = set(u.get('culture', 'unknown') for u in self.conversation_history)

        return {
            'detected_cultures': list(cultures),
            'is_monocultural': len(cultures) <= 1,
            'current_culture': self._pause_adapter.culture,
            'thresholds': self._pause_adapter.get_thresholds(),
            'supported_cultures': CulturalPauseAdapter.get_supported_cultures()
        }
