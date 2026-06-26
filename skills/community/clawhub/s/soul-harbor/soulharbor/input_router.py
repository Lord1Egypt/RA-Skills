"""
Input routing module
Handles language detection and sentiment scoring
"""

from typing import Tuple
from .models import Language
from .utils.sentiment_analyzer import SentimentAnalyzer


class InputRouter:
    """Input router"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self._current_lang = Language.ZH  # Global language variable
    
    def detect_language(self, text: str) -> Language:
        """
        Detect language of user input
        Simple implementation: Based on character range
        """
        # Count Chinese characters
        chinese_chars = sum(1 for char in text if '\u4e00' <= char <= '\u9fff')
        total_chars = len([c for c in text if c.isalnum() or '\u4e00' <= c <= '\u9fff'])
        
        if total_chars == 0:
            return self._current_lang  # Keep current language
        
        # If Chinese characters exceed 30%, classify as Chinese
        if chinese_chars / total_chars > 0.3:
            self._current_lang = Language.ZH
            return Language.ZH
        else:
            self._current_lang = Language.EN
            return Language.EN
    
    def analyze_sentiment(self, text: str, language: Language) -> float:
        """
        Analyze sentiment of user text
        Returns score from -1.0 to 1.0
        """
        lang_str = language.value
        return self.sentiment_analyzer.analyze(text, lang_str)
    
    def route(self, text: str) -> Tuple[Language, float]:
        """
        Route input: Detect language and analyze sentiment
        Returns (language, sentiment_score)
        """
        language = self.detect_language(text)
        sentiment_score = self.analyze_sentiment(text, language)
        return language, sentiment_score
    
    @property
    def current_language(self) -> Language:
        """Get current language preference"""
        return self._current_lang
    
    def set_language(self, language: Language) -> None:
        """Set language preference"""
        self._current_lang = language
