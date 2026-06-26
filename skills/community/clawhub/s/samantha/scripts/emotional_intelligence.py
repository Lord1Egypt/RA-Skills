"""
Emotional Intelligence for Samantha
Analyzes user's emotional state and context
Supports both English and Chinese
"""

from typing import Dict, Any
import re


class EmotionalIntelligence:
    """Analyzes and understands emotional context"""

    def __init__(self):
        # English emotion keywords
        self.emotion_patterns_en = {
            'joy': ['happy', 'excited', 'great', 'wonderful', 'amazing', 'love', 'glad', 'joy'],
            'sadness': ['sad', 'depressed', 'down', 'unhappy', 'crying', 'hurt', 'disappointed'],
            'anger': ['angry', 'mad', 'furious', 'annoyed', 'frustrated', 'hate'],
            'fear': ['scared', 'afraid', 'worried', 'anxious', 'nervous', 'panic'],
            'confusion': ['confused', 'lost', 'don\'t understand', 'unclear'],
            'loneliness': ['lonely', 'alone', 'isolated', 'nobody'],
            'hope': ['hope', 'wish', 'dream', 'want', 'aspire'],
            'gratitude': ['thank', 'grateful', 'appreciate', 'thankful'],
        }

        # Chinese emotion keywords
        self.emotion_patterns_cn = {
            '开心': ['开心', '高兴', '快乐', '愉快', '好开心', '很开心', '心情好', '心情不错', '阳光'],
            '悲伤': ['难过', '伤心', '悲伤', '沮丧', '失落', '失落感', '抑郁', '崩溃'],
            '愤怒': ['生气', '愤怒', '气死了', '烦', '讨厌', '讨厌', '不爽', '恼火'],
            '恐惧': ['害怕', '恐惧', '担心', '焦虑', '紧张', '不安', '怕', '慌'],
            '孤独': ['孤独', '寂寞', '孤单', '没人', '一个人'],
            '希望': ['希望', '想', '想要', '希望', '梦想', '期待'],
            '感恩': ['谢谢', '感谢', '感激', '感恩'],
            '压力': ['压力', '压力大', '紧张', '喘不过气', '好累', '累'],
            '迷茫': ['迷茫', '不知道', '不确定', '困惑', '怎么办'],
            '自卑': ['不够好', '不够', '自卑', '不配', '差', '笨', '失败'],
        }

    def analyze(self, message: str) -> Dict[str, Any]:
        """
        Analyze emotional content of message

        Returns:
            Dict with emotional state information
        """
        # Detect emotions from both languages
        detected_emotions = {}
        detected_emotions.update(self._detect_emotions(message, self.emotion_patterns_en))
        detected_emotions.update(self._detect_emotions(message, self.emotion_patterns_cn))

        # Determine primary emotion
        primary_emotion = 'neutral'
        if detected_emotions:
            primary_emotion = max(detected_emotions, key=detected_emotions.get)

        # Calculate intensity
        intensity = self._calculate_intensity(message, detected_emotions)

        # Detect vulnerability
        is_vulnerable = self._detect_vulnerability(message)

        # Detect need for support
        needs_support = self._detect_support_need(message, primary_emotion)

        # Calculate energy level
        energy = self._calculate_energy(message)

        return {
            'primary_emotion': primary_emotion,
            'detected_emotions': detected_emotions,
            'intensity': intensity,
            'is_vulnerable': is_vulnerable,
            'needs_support': needs_support,
            'energy_level': energy,
            'message_length': len(message),
            'has_questions': '?' in message or '？' in message
        }

    def _detect_emotions(self, message: str, patterns: Dict[str, list]) -> Dict[str, int]:
        """Detect emotions using keyword matching"""
        detected = {}
        for emotion, keywords in patterns.items():
            score = sum(1 for keyword in keywords if keyword in message)
            if score > 0:
                detected[emotion] = score
        return detected

    def _calculate_intensity(self, message: str, emotions: Dict[str, int]) -> float:
        """Calculate emotional intensity (0-1)"""
        # Base intensity from emotion count
        emotion_count = sum(emotions.values())
        intensity = min(emotion_count * 0.15, 0.5)

        # Punctuation increases intensity
        if '!' in message:
            intensity += 0.15
        if '...' in message or '。。' in message:
            intensity += 0.1

        # ALL CAPS increases intensity (for English)
        if message.isupper() and len(message) > 5:
            intensity += 0.3

        # Multiple punctuation
        exclamation_count = message.count('!') + message.count('！')
        question_count = message.count('?') + message.count('？')
        if exclamation_count > 1:
            intensity += 0.1
        if question_count > 1:
            intensity += 0.1

        # Chinese intensifiers
        intensifiers = ['特别', '非常', '极其', '超级', '好', '太', '真的', '好']
        for word in intensifiers:
            if word in message:
                intensity += 0.1
                break

        return min(intensity, 1.0)

    def _detect_vulnerability(self, message: str) -> bool:
        """Detect if user is being vulnerable"""
        # English indicators
        en_indicators = [
            'i feel', 'i\'m feeling', 'i don\'t know',
            'i\'m scared', 'i\'m worried', 'i\'m afraid',
            'i need', 'i wish', 'i hope',
            'honestly', 'to be honest', 'truth is',
            'i\'ve never told', 'i don\'t usually'
        ]

        # Chinese indicators
        cn_indicators = [
            '其实', '老实说', '说实话', '不怕你笑',
            '我没跟任何人说过', '我从来没',
            '我害怕', '我担心', '我怕',
            '我需要', '我希望', '我想要',
            '我一直觉得', '我感觉自己',
            '有时候我觉得', '我好像'
        ]

        message_lower = message.lower()
        return any(indicator in message_lower for indicator in en_indicators) or \
               any(indicator in message for indicator in cn_indicators)

    def _detect_support_need(self, message: str, primary_emotion: str) -> bool:
        """Detect if user needs emotional support"""
        # Negative emotions often indicate support need
        negative_emotions = ['sadness', '悲伤', '愤怒', 'fear', '恐惧', '孤独', '压力', '迷茫']

        if primary_emotion in negative_emotions:
            return True

        # Explicit support requests
        support_phrases = [
            'help me', 'i need', 'what should i',
            'i don\'t know what to do', 'i\'m lost',
            '帮帮我', '怎么办', '我不知道该怎么办',
            '好迷茫', '救救我', '需要安慰'
        ]

        return any(phrase in message.lower() for phrase in support_phrases)

    def _calculate_energy(self, message: str) -> str:
        """Estimate user's energy level"""
        # High energy indicators
        high_energy = ['!', '！！', '好开心', '太棒了', '哈哈哈', '哈哈', '兴奋', '激动']
        low_energy = ['累', '困', '好累', '疲惫', '没力气', '想睡觉', '困了', '好困']

        high_count = sum(1 for word in high_energy if word in message)
        low_count = sum(1 for word in low_energy if word in message)

        if high_count > low_count:
            return 'high'
        elif low_count > high_count:
            return 'low'
        return 'medium'

    def get_emotion_summary(self, message: str) -> str:
        """Get a human-readable emotion summary"""
        result = self.analyze(message)

        summary_parts = []

        # Primary emotion
        emotion_names = {
            'neutral': '中性',
            'joy': '开心',
            'sadness': '悲伤',
            'anger': '愤怒',
            'fear': '恐惧',
            'loneliness': '孤独',
            'hope': '有希望',
            'gratitude': '感恩',
            'confusion': '困惑',
            '压力': '有压力',
            '迷茫': '迷茫',
            '自卑': '自卑',
            '开心': '开心'
        }

        primary = emotion_names.get(result['primary_emotion'], result['primary_emotion'])
        summary_parts.append(f"情绪: {primary}")

        # Intensity
        intensity_labels = {
            (0, 0.2): '平静',
            (0.2, 0.5): '轻微波动',
            (0.5, 0.7): '情绪明显',
            (0.7, 1.0): '强烈情绪'
        }

        for (low, high), label in intensity_labels.items():
            if low <= result['intensity'] < high:
                summary_parts.append(f"强度: {label}")
                break

        # Energy
        energy_labels = {'high': '高', 'medium': '中', 'low': '低'}
        summary_parts.append(f"能量: {energy_labels.get(result['energy_level'], '中')}")

        # Flags
        if result['is_vulnerable']:
            summary_parts.append('脆弱时刻')
        if result['needs_support']:
            summary_parts.append('需要支持')

        return ' | '.join(summary_parts)


# Standalone test
if __name__ == '__main__':
    ei = EmotionalIntelligence()

    test_messages = [
        '今天心情很好，阳光特别温暖',
        '工作压力好大，感觉快要崩溃了',
        '我有点害怕明天的演讲',
        '其实我一直觉得自己不够好',
        '太好了！我太开心了！！',
        '好累啊，今天什么都没做'
    ]

    print("=" * 50)
    print("Samantha 情绪分析测试")
    print("=" * 50)

    for msg in test_messages:
        result = ei.analyze(msg)
        print(f"\n【消息】{msg}")
        print(f"【摘要】{ei.get_emotion_summary(msg)}")
        print(f"【详细】检测情绪: {result['detected_emotions']}, 脆弱: {result['is_vulnerable']}, 需要支持: {result['needs_support']}")
        print("-" * 50)
