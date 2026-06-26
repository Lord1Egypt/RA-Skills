"""
关键词过滤模块 - 支持 OR/AND 模式匹配 + word/regex 匹配类型
"""
import re
import logging
from config_loader import KeywordRules

logger = logging.getLogger(__name__)


class KeywordFilter:
    """消息关键词过滤器
    
    支持三种匹配类型：
    - substring: 子串匹配（默认），如「外挂」匹配「外挂辅助」
    - word: 词边界匹配，如「脚本」不匹配「Python脚本编写」
    - regex: 正则匹配，如「外挂|辅助|破解」
    """

    def __init__(self, keywords: list[str], rules: KeywordRules):
        """
        Args:
            keywords: 关键词列表
            rules: 匹配规则（match_mode: substring/word/regex, logic_mode: OR/AND, case_sensitive）
        """
        self.keywords = keywords
        self.rules = rules
        # 预编译正则（word 和 regex 模式用）
        self._compiled: list[re.Pattern] | None = None
        if rules.match_mode == "word":
            flags = 0 if rules.case_sensitive else re.IGNORECASE
            self._compiled = [re.compile(r'\b' + re.escape(kw) + r'\b', flags) for kw in keywords]
        elif rules.match_mode == "regex":
            flags = 0 if rules.case_sensitive else re.IGNORECASE
            self._compiled = [re.compile(kw, flags) for kw in keywords]

    def match(self, text: str | None) -> tuple[bool, list[str]]:
        """
        检查文本是否命中关键词

        Args:
            text: 消息文本

        Returns:
            (是否命中, 命中的关键词列表)
        """
        if not text or not self.keywords:
            return False, []

        search_text = text if self.rules.case_sensitive else text.lower()
        matched = []

        if self._compiled:
            # word 或 regex 模式
            for i, pattern in enumerate(self._compiled):
                if pattern.search(search_text):
                    matched.append(self.keywords[i])
        else:
            # substring 模式（默认，保持向后兼容）
            for kw in self.keywords:
                kw_search = kw if self.rules.case_sensitive else kw.lower()
                if kw_search in search_text:
                    matched.append(kw)

        if self.rules.logic_mode.upper() == "AND":
            hit = len(matched) == len(self.keywords)
        else:
            hit = len(matched) > 0

        return hit, matched

    @staticmethod
    def match_any(text: str | None, keywords: list[str], case_sensitive: bool = False) -> bool:
        """快速判断：任意关键词命中（不返回具体匹配列表）"""
        if not text or not keywords:
            return False
        search_text = text if case_sensitive else text.lower()
        for kw in keywords:
            kw_search = kw if case_sensitive else kw.lower()
            if kw_search in search_text:
                return True
        return False
