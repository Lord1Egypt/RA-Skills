"""Advanced Chinese tokenizer with jieba + custom dictionary support."""
from __future__ import annotations

import logging
import re
from typing import Optional

logger = logging.getLogger(__name__)

_HAS_JIEBA = False
try:
    import jieba
    import jieba.analyse
    _HAS_JIEBA = True
except ImportError:
    pass

_CHINESE_PATTERN = re.compile(r'[\u4e00-\u9fff]+')
_PUNCTUATION_PATTERN = re.compile(r'[，。！？、；：""''（）【】《》…—]')


class ChineseTokenizer:
    def __init__(self, user_dict: str = None, use_hmm: bool = True):
        self._use_hmm = use_hmm
        self._initialized = False
        self._user_dict = user_dict
        self._stop_words = self._load_stop_words()

    def _ensure_initialized(self):
        if self._initialized:
            return
        if _HAS_JIEBA:
            if self._user_dict:
                jieba.load_userdict(self._user_dict)
            jieba.initialize()
        self._initialized = True

    def _load_stop_words(self) -> set:
        default_stops = {
            "的", "了", "在", "是", "我", "有", "和", "就", "不", "人",
            "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去",
            "你", "会", "着", "没有", "看", "好", "自己", "这", "他", "她",
            "它", "们", "那", "些", "什么", "怎么", "如何", "为什么", "哪",
            "吗", "呢", "吧", "啊", "哦", "嗯", "呀", "哈", "嘛", "呗",
        }
        return default_stops

    def tokenize(self, text: str, use_stop_words: bool = True) -> list[str]:
        if not text:
            return []
        self._ensure_initialized()

        if _HAS_JIEBA:
            words = list(jieba.cut(text, HMM=self._use_hmm))
        else:
            words = self._simple_tokenize(text)

        if use_stop_words:
            words = [w for w in words if w.strip() and w not in self._stop_words]
        else:
            words = [w for w in words if w.strip()]

        return words

    def tokenize_for_search(self, text: str) -> str:
        tokens = self.tokenize(text, use_stop_words=True)
        return " ".join(tokens)

    def extract_keywords(self, text: str, top_k: int = 10) -> list[tuple[str, float]]:
        self._ensure_initialized()
        if _HAS_JIEBA:
            return jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        tokens = self.tokenize(text)
        from collections import Counter
        counts = Counter(tokens)
        total = sum(counts.values())
        return [(w, c / total) for w, c in counts.most_common(top_k)]

    def extract_entities(self, text: str) -> list[dict]:
        self._ensure_initialized()
        entities = []

        patterns = {
            "person": re.compile(r'[\u4e00-\u9fff]{2,4}(?:先生|女士|老师|教授|博士|经理|总监|总裁|部长|局长|主任|工程师|设计师|分析师)'),
            "organization": re.compile(r'[\u4e00-\u9fff]{2,8}(?:公司|集团|银行|大学|研究院|研究所|部门|委员会|基金会|协会|中心)'),
            "location": re.compile(r'[\u4e00-\u9fff]{1,4}(?:省|市|区|县|镇|村|路|街|道|巷|弄|号|楼|层|室)'),
            "product": re.compile(r'[\u4e00-\u9fff\w]{2,20}(?:系统|平台|引擎|框架|工具|软件|应用|服务|方案)'),
        }

        for entity_type, pattern in patterns.items():
            for match in pattern.finditer(text):
                entities.append({
                    "type": entity_type,
                    "text": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        return sorted(entities, key=lambda x: x["start"])

    def _simple_tokenize(self, text: str) -> list[str]:
        result = []
        current = []
        for ch in text:
            if '\u4e00' <= ch <= '\u9fff':
                if current:
                    result.append(''.join(current))
                    current = []
                result.append(ch)
            elif ch.isalnum():
                current.append(ch)
            else:
                if current:
                    result.append(''.join(current))
                    current = []
        if current:
            result.append(''.join(current))
        return result

    def is_chinese_text(self, text: str) -> bool:
        chinese_chars = sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')
        total_chars = len(text.replace(' ', ''))
        if total_chars == 0:
            return False
        return chinese_chars / total_chars > 0.3
