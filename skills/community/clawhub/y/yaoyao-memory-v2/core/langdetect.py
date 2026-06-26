from typing import Dict, Tuple
"""多语言支持 - 语言检测"""
import re
from typing import Tuple, Optional

class LanguageDetector:
    # 语言特征
    PATTERNS = {
        'zh': r'[\u4e00-\u9fff]',  # 中文字符
        'en': r'[a-zA-Z]',  # 英文字符
        'ja': r'[\u3040-\u309f\u30a0-\u30ff]',  # 日文假名
        'ko': r'[\uac00-\ud7af]',  # 韩文字符
    }
    
    @classmethod
    def detect(cls, text: str) -> Tuple[str, float]:
        """检测语言"""
        if not text:
            return 'unknown', 0.0
        
        scores = {}
        total_chars = len(text)
        
        for lang, pattern in cls.PATTERNS.items():
            matches = len(re.findall(pattern, text))
            scores[lang] = matches / total_chars if total_chars > 0 else 0
        
        # 找出主要语言
        if scores:
            main_lang = max(scores, key=scores.get)
            confidence = scores[main_lang]
            return main_lang, confidence
        
        return 'unknown', 0.0
    
    @classmethod
    def is_chinese(cls, text: str) -> bool:
        """是否为中文"""
        lang, conf = cls.detect(text)
        return lang == 'zh' and conf > 0.5
    
    @classmethod
    def is_english(cls, text: str) -> bool:
        """是否为英文"""
        lang, conf = cls.detect(text)
        return lang == 'en' and conf > 0.5
    
    @classmethod
    def get_search_strategy(cls, text: str) -> Dict:
        """根据语言获取搜索策略"""
        lang, conf = cls.detect(text)
        
        if lang == 'zh':
            return {
                'language': 'zh',
                'tokenize': 'chinese',
                'use_fts': True,
                'vector_model': 'Qwen3-Embedding-8B',
            }
        elif lang == 'en':
            return {
                'language': 'en',
                'tokenize': 'english',
                'use_fts': True,
                'vector_model': 'Qwen3-Embedding-8B',  # 支持英文
            }
        else:
            return {
                'language': lang,
                'tokenize': 'default',
                'use_fts': True,
                'vector_model': 'Qwen3-Embedding-8B',
            }
