from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Optional

from ..llm_layer import SpiritLLMLayer

logger = logging.getLogger(__name__)


@dataclass
class ParsedCommand:
    intent: str = 'unknown'
    target: str = ''
    params: dict = field(default_factory=dict)
    confidence: float = 0.0
    method: str = 'rule'

    def to_dict(self) -> dict:
        return {
            'intent': self.intent,
            'target': self.target,
            'params': self.params,
            'confidence': self.confidence,
            'method': self.method,
        }


_INTENT_KEYWORDS = {
    'consolidate': [
        r'合并', r'整合', r'融合', r'去重', r'统一',
        r'consolidat', r'merge', r'dedup', r'integrat',
    ],
    'review': [
        r'回顾', r'查看', r'检查', r'审视', r'总结',
        r'review', r'check', r'inspect', r'summariz',
    ],
    'archive': [
        r'归档', r'存档', r'清理', r'删除', r'移除',
        r'archive', r'delete', r'remove', r'clean', r'purge',
    ],
    'find': [
        r'查找', r'搜索', r'寻找', r'找', r'查询',
        r'find', r'search', r'lookup', r'query', r'recall',
    ],
    'report': [
        r'报告', r'日报', r'周报', r'月报', r'统计',
        r'report', r'daily', r'weekly', r'monthly', r'stats',
    ],
    'correct': [
        r'修正', r'纠正', r'更正', r'修改', r'更新',
        r'correct', r'fix', r'update', r'amend', r'revis',
    ],
}

_TOPIC_PATTERN = re.compile(
    r'(?:关于|主题|topic|subject)[:\s]*["\']?([A-Za-z_.]+|[\u4e00-\u9fff.]+|["\'][^"\']+["\'])["\']?',
    re.IGNORECASE,
)

_TIME_PATTERNS = [
    (re.compile(r'今天|今日|today', re.IGNORECASE), 'today'),
    (re.compile(r'昨天|昨日|yesterday', re.IGNORECASE), 'yesterday'),
    (re.compile(r'本周|这周|this\s*week', re.IGNORECASE), 'this_week'),
    (re.compile(r'上周|last\s*week', re.IGNORECASE), 'last_week'),
    (re.compile(r'本月|这个月|this\s*month', re.IGNORECASE), 'this_month'),
    (re.compile(r'上月|last\s*month', re.IGNORECASE), 'last_month'),
]

_REPORT_TYPE_PATTERNS = [
    (re.compile(r'日报|daily', re.IGNORECASE), 'daily'),
    (re.compile(r'周报|weekly', re.IGNORECASE), 'weekly'),
    (re.compile(r'月报|monthly', re.IGNORECASE), 'monthly'),
]


class CommandParser:
    """Rule-first, LLM-fallback command parser.

    6 intent categories: consolidate, review, archive, find, report, correct
    - Keyword matching first
    - If no match, try LLM parsing
    - If LLM unavailable, return 'unknown' intent

    Security: Only whitelisted intents are allowed.
    """

    ALLOWED_INTENTS = frozenset({
        'consolidate', 'review', 'archive', 'find', 'report', 'correct', 'unknown',
    })

    def __init__(self, llm_layer: SpiritLLMLayer = None):
        self.llm_layer = llm_layer

    def parse(self, command_text: str) -> ParsedCommand:
        if not command_text or not command_text.strip():
            return ParsedCommand(intent='unknown', confidence=0.0, method='empty')

        rule_result = self._rule_parse(command_text)
        if rule_result.confidence >= 0.7:
            # Security: validate intent against whitelist
            if rule_result.intent not in self.ALLOWED_INTENTS:
                logger.warning("CommandParser: blocked non-whitelisted intent '%s'", rule_result.intent)
                return ParsedCommand(intent='unknown', confidence=0.0, method='blocked')
            return rule_result

        llm_result = self._llm_parse(command_text)
        if llm_result is not None and llm_result.confidence > rule_result.confidence:
            # Security: validate LLM-parsed intent against whitelist
            if llm_result.intent not in self.ALLOWED_INTENTS:
                logger.warning("CommandParser: blocked LLM non-whitelisted intent '%s'", llm_result.intent)
                return ParsedCommand(intent='unknown', confidence=0.0, method='blocked')
            return llm_result

        # Security: validate rule result intent
        if rule_result.intent not in self.ALLOWED_INTENTS:
            return ParsedCommand(intent='unknown', confidence=0.0, method='blocked')
        return rule_result

    def _rule_parse(self, text: str) -> ParsedCommand:
        text_lower = text.lower()

        best_intent = 'unknown'
        best_score = 0.0

        for intent, patterns in _INTENT_KEYWORDS.items():
            for pattern in patterns:
                match = re.search(pattern, text_lower)
                if match:
                    score = 0.7 + 0.05 * len(match.group())
                    if score > best_score:
                        best_score = score
                        best_intent = intent
                    break

        params = {}

        topic_match = _TOPIC_PATTERN.search(text)
        if topic_match:
            params['topic'] = topic_match.group(1)

        for pattern, time_val in _TIME_PATTERNS:
            if pattern.search(text):
                params['time_range'] = time_val
                break

        if best_intent == 'report':
            for pattern, report_type in _REPORT_TYPE_PATTERNS:
                if pattern.search(text):
                    params['report_type'] = report_type
                    break
            if 'report_type' not in params:
                params['report_type'] = 'daily'

        if best_intent == 'find':
            query_text = self._extract_query_text(text)
            if query_text:
                params['query'] = query_text

        if best_intent == 'archive':
            importance_match = re.search(r'(低|low|中|medium|高|high)', text_lower)
            if importance_match:
                imp_val = importance_match.group(1)
                imp_map = {'低': 'low', '中': 'medium', '高': 'high',
                           'low': 'low', 'medium': 'medium', 'high': 'high'}
                params['importance'] = imp_map.get(imp_val, 'low')

        target = params.get('topic', params.get('query', ''))

        return ParsedCommand(
            intent=best_intent,
            target=target,
            params=params,
            confidence=min(best_score, 1.0),
            method='rule',
        )

    def _llm_parse(self, text: str) -> Optional[ParsedCommand]:
        if self.llm_layer is None:
            return None

        result = self.llm_layer.parse_command_with_llm(text)
        if result is None:
            return None

        intent = result.get('intent', 'unknown')
        if intent not in _INTENT_KEYWORDS and intent != 'unknown':
            intent = 'unknown'

        return ParsedCommand(
            intent=intent,
            target=result.get('target', ''),
            params=result.get('params', {}),
            confidence=0.6,
            method='llm',
        )

    def _extract_query_text(self, text: str) -> str:
        query_patterns = [
            re.compile(r'(?:查找|搜索|找|查询|find|search|lookup|query)\s*[:：]?\s*["\']?(.+?)["\']?\s*$', re.IGNORECASE),
            re.compile(r'["\'](.+?)["\']'),
        ]

        for pattern in query_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1).strip()

        return ""
