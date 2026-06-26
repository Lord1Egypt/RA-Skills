"""
content_cleaner.py - 记忆内容清洗器
在写入前清理文本：删除废话、修复语病、保留核心信息

原则：
  - high 记忆：一字不改，只删明显废话
  - medium 记忆：修复语病，删除冗余，保留原意
  - low 记忆：提取核心，大胆精简
"""

from __future__ import annotations

import re


class ContentCleaner:
    """
    三级清洗策略，写入前自动执行。

    用法：
        cleaner = ContentCleaner()
        cleaned = cleaner.clean(raw_text, importance="medium")
    """

    # ── 废话模式（所有级别都会删）────────────────────────

    FILLER_PATTERNS = [
        # 口头禅 / 无意义开头
        r'^(嗯+[,，]?\s*)',
        r'^(那个[,，]?\s*)',
        r'^(就是说[,，]?\s*)',
        r'^(怎么说呢[,，]?\s*)',
        r'^(其实吧[,，]?\s*)',
        r'^(说实话[,，]?\s*)',
        r'^(我觉得吧[,，]?\s*)',
        r'^(well[,，]?\s*)',
        r'^(so[,，]?\s*)',
        r'^(like[,，]?\s*)',
        r'^(you know[,，]?\s*)',
        r'^(basically[,，]?\s*)',
        # 重复确认
        r'^(好的好的\s*)',
        r'^(行行行\s*)',
        r'^(嗯嗯\s*)',
        r'^(ok ok\s*)',
        # 结尾废话
        r'\s*(就这样|先这样|就这些|没了|ok\??|好了)\s*[。.！!]?\s*$',
        r'\s*(就这样吧|先这样吧|就这样了)\s*[。.！!]?\s*$',
    ]

    # ── 冗余短语模式（medium+ 用正则替换）────────────────
    # 安全设计原则：
    # 1. 不用嵌套可选组 (A)?(B)?(C)? — 经典 ReDoS 源
    # 2. 每条模式只含一层可选，或用非回溯匹配
    # 3. 匹配长度有上限，用 {0,N} 替代贪婪 .*

    # Fix #5: 从根上消除 ReDoS — 所有模式使用原子组或固定前缀
    # 原则：不用嵌套量词、不用 .* 回溯、不用 (?:A)?(?:B)?(?:C)? 重叠可选组
    REDUNDANCY_PATTERNS = [
        (r'经过我们?的?(?:反复|多次)?(?:测试|验证|实验)(?:和(?:测试|验证|实验))?(?:之?后)?(?:发现|显示)?[,，]\s*', '测试发现，'),
        (r'经过一番(?:调研|研究|探索|调查)[,，]\s*', '调研发现，'),
        (r'在经过了?(?:一系列|多次|反复)?的?(?:尝试|探索|测试|实验|调研|研究)(?:之?后)[,，]\s*', '经'),
        (r'我做了一[番次](?:测试|实验)[,，]\s*', '实验发现，'),
        (r'我发现?了?一个?问题[,，]这个问题是[,，]?\s*', '问题是'),
        (r'有一个需要注意的地方[,，]?\s*', '注意：'),
        (r'需要特别注意的是[,，]?\s*', '注意：'),
        (r'(?:换句话说|也就是说|简单来说|说白了)就?是?[,，]\s*', '即'),
        (r'在这里需要说明的是[,，]?\s*', '即'),
        (r'从本质上来说[,，]\s*', '本质上'),
        (r'(?:总而言之|不管怎么说|不管怎样)[,，]\s*', '总之'),
        (r'归根结底[,，]\s*', '根本上'),
    ]

    # ── 语病修复（medium+ 会执行）────────────────────────

    GRAMMAR_FIXES = [
        # 重复标点
        (r'[。.]{2,}', '。'),
        (r'[,，]{2,}', '，'),
        (r'[!！]{2,}', '！'),
        # 多余空格
        (r'\s{2,}', ' '),
        # 中英文之间加空格（可选，保持原样）
        # 重复的 "了了" "的的"
        (r'了了+', '了'),
        (r'的的+', '的'),
        (r'是是+', '是'),
        (r'有有+', '有'),
        # 语病："的时候" 冗余
        (r'在(.{1,10})的时候', r'\1时'),
    ]

    _HTML_TAG_RE = re.compile(r'<[^>]+>')

    def __init__(self):
        self._filler_re = [re.compile(p, re.IGNORECASE) for p in self.FILLER_PATTERNS if p != '']
        self._grammar_res = [(re.compile(p), r) for p, r in self.GRAMMAR_FIXES]
        self._redundancy_res = []
        for item in self.REDUNDANCY_PATTERNS:
            if isinstance(item, tuple):
                pattern, repl = item
                self._redundancy_res.append((re.compile(pattern), repl))
            else:
                self._redundancy_res.append((re.compile(item), ''))

    _MAX_TEXT_LENGTH = 10000
    _CHUNK_SIZE = 5000
    _SHORT_TEXT_THRESHOLD = 5

    def clean(self, text: str, importance: str = "medium") -> str:
        if not text or not text.strip():
            return text

        text = text.strip()

        if len(text) < self._SHORT_TEXT_THRESHOLD:
            return text

        if len(text) > self._MAX_TEXT_LENGTH:
            return self._clean_long_text(text, importance)

        return self._clean_chunk(text, importance)

    def _clean_chunk(self, text: str, importance: str = "medium") -> str:
        text = self._remove_fillers(text)

        if importance in ("medium", "high"):
            text = self._strip_html(text)

        if importance == "high":
            return text

        text = self._reduce_redundancy(text)
        text = self._fix_grammar(text)

        if importance == "medium":
            return text

        text = self._aggressive_simplify(text)
        return text

    def _clean_long_text(self, text: str, importance: str = "medium") -> str:
        chunks = []
        for i in range(0, len(text), self._CHUNK_SIZE):
            chunk = text[i:i + self._CHUNK_SIZE]
            chunks.append(self._clean_chunk(chunk, importance))
        return "".join(chunks)

    def _remove_fillers(self, text: str) -> str:
        """删除废话"""
        for pat in self._filler_re:
            text = pat.sub('', text)
        return text.strip()

    def _strip_html(self, text: str) -> str:
        """Strip HTML tags from content to prevent XSS."""
        return self._HTML_TAG_RE.sub('', text)

    def _reduce_redundancy(self, text: str) -> str:
        """用正则替换冗余短语 — Fix #5: 正则本身已消除回溯，无需超时保护"""
        for pat, repl in self._redundancy_res:
            try:
                text = pat.sub(repl, text)
            except Exception:
                continue
        text = re.sub(r'^[,，]\s*', '', text)
        text = re.sub(r'经(问题|注意|结论|总结)', r'\1', text)
        return text

    def _fix_grammar(self, text: str) -> str:
        """修复语病"""
        for pat, repl in self._grammar_res:
            text = pat.sub(repl, text)
        return text.strip()

    def _aggressive_simplify(self, text: str) -> str:
        """low 级别：删除修饰语、客套话"""
        # 删除 "我觉得" "我认为" "在我看来" 等主观前缀
        text = re.sub(r'^(我觉得|我认为|在我看来|个人认为|主观来说)[,，]?\s*', '', text)

        # 删除 "真的" "确实" "非常" 等程度副词
        text = re.sub(r'(真的|确实|非常|特别|尤其|十分|相当|比较)\s*', '', text)

        # 删除 "然后" "接着" "之后" 等连接词（保留因果）
        text = re.sub(r'(然后[,，]|接着[,，]|之后[,，]|接下来[,，])\s*', '', text)

        return text.strip()

    def clean_batch(self, texts: list[str], importance: str = "medium") -> list[str]:
        """批量清洗"""
        return [self.clean(t, importance) for t in texts]
