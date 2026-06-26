"""
Sentiment analysis tool
"""

from typing import Optional
import re


class SentimentAnalyzer:
    """Simple sentiment analyzer (can be replaced with more complex models)"""
    
    # Chinese negative words
    NEGATIVE_WORDS_ZH = {
        "难过", "伤心", "痛苦", "沮丧", "失望", "焦虑", "担心", "害怕",
        "累", "疲惫", "压力", "烦恼", "困扰", "生气", "愤怒", "郁闷"
    }
    
    # Chinese positive words
    POSITIVE_WORDS_ZH = {
        "开心", "高兴", "快乐", "兴奋", "满足", "幸福", "轻松", "愉快",
        "好", "棒", "赞", "不错", "很好", "太好了", "完美"
    }
    
    # English negative words
    NEGATIVE_WORDS_EN = {
        "sad", "upset", "angry", "worried", "anxious", "stressed", "tired",
        "exhausted", "frustrated", "disappointed", "depressed", "hurt"
    }
    
    # English positive words
    POSITIVE_WORDS_EN = {
        "happy", "glad", "excited", "great", "good", "wonderful", "amazing",
        "fantastic", "perfect", "nice", "pleased", "satisfied"
    }
    
    def analyze(self, text: str, language: str = "zh") -> float:
        """
        Analyze text sentiment, returns score from -1.0 to 1.0
        -1.0: Extremely negative
        0.0: Neutral
        1.0: Extremely positive
        """
        text_lower = text.lower()
        
        if language == "zh":
            negative_words = self.NEGATIVE_WORDS_ZH
            positive_words = self.POSITIVE_WORDS_ZH
        else:
            negative_words = self.NEGATIVE_WORDS_EN
            positive_words = self.POSITIVE_WORDS_EN
        
        # Count occurrences of negative and positive words
        negative_count = sum(1 for word in negative_words if word in text_lower)
        positive_count = sum(1 for word in positive_words if word in text_lower)
        
        # Calculate base score
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        # Normalize to -1.0 to 1.0
        score = (positive_count - negative_count) / max(total_words, 1)
        
        # Clamp to [-1.0, 1.0] range
        score = max(-1.0, min(1.0, score))
        
        # Enhance score if obvious emotion words present
        if negative_count > 0:
            score = min(score, -0.3)
        if positive_count > 0:
            score = max(score, 0.3)
        
        return score
