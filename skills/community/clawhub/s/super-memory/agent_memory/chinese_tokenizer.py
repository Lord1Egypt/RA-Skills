"""v8.5 — 中文分词增强
支持 jieba 分词 + 停用词过滤 + 同义词扩展 + 领域词典
降级方案: 正则分字 + bigram（不依赖 jieba）
"""
from __future__ import annotations

import logging
import re
import os

logger = logging.getLogger(__name__)

_STOP_WORDS = {
    "的", "了", "是", "在", "和", "有", "我", "你", "他", "她", "它", "们",
    "这", "那", "什么", "怎么", "如何", "就", "也", "都", "很", "要", "会",
    "能", "可以", "没", "不", "吗", "呢", "吧", "啊", "哦", "嗯",
    "一个", "这个", "那个", "一下", "一些", "所以", "因为", "如果", "但是",
    "说", "看", "把", "让", "给", "从", "到", "跟", "对", "被",
    "一个", "一种", "这种", "那种",
}

_SYNONYM_MAP: dict[str, list[str]] = {}


def _load_jieba():
    try:
        import jieba
        return jieba
    except ImportError:
        return None


def _load_synonyms():
    if _SYNONYM_MAP:
        return
    syn_path = os.path.join(os.path.dirname(__file__), "config", "synonyms.txt")
    if os.path.exists(syn_path):
        with open(syn_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",")
                if len(parts) >= 2:
                    _SYNONYM_MAP[parts[0].strip()] = [p.strip() for p in parts[1:]]


class ChineseTokenizer:

    def __init__(self, use_jieba: bool = True, enable_synonyms: bool = True):
        self._jieba = _load_jieba() if use_jieba else None
        self._use_jieba = use_jieba and self._jieba is not None
        self._enable_synonyms = enable_synonyms
        if enable_synonyms:
            _load_synonyms()

    def tokenize(self, text: str, remove_stop: bool = True) -> list[str]:
        if self._use_jieba:
            tokens = list(self._jieba.cut(text))
        else:
            tokens = self._regex_fallback(text)

        tokens = [t.strip().lower() for t in tokens if t.strip()]
        if remove_stop:
            tokens = [t for t in tokens if t not in _STOP_WORDS]
        return tokens

    def expand_synonyms(self, tokens: list[str]) -> list[str]:
        if not self._enable_synonyms:
            return tokens
        expanded = list(tokens)
        for t in tokens:
            if t in _SYNONYM_MAP:
                expanded.extend(_SYNONYM_MAP[t])
        return expanded

    def _regex_fallback(self, text: str) -> list[str]:
        result = []
        for chunk in re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z0-9]+', text):
            if re.match(r'[\u4e00-\u9fff]', chunk):
                if len(chunk) <= 2:
                    result.append(chunk)
                else:
                    for i in range(len(chunk) - 1):
                        result.append(chunk[i:i + 2])
                    if len(chunk) > 3:
                        result.append(chunk)
            else:
                result.append(chunk)
        return result

    @property
    def is_available(self) -> bool:
        return self._use_jieba

    def add_word(self, word: str, freq: int = None, tag: str = None):
        if self._jieba:
            self._jieba.add_word(word, freq, tag)

    def suggest(self, text: str) -> str:
        return " ".join(self.tokenize(text, remove_stop=True))