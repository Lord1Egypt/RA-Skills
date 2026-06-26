"""Sensitivity Analyzer — 自动分析记忆敏感度

基于关键词和模式匹配自动检测记忆中的敏感信息。
"""
from __future__ import annotations

import re
import logging
from dataclasses import dataclass

from .patterns import PIIPattern, get_patterns_by_category

logger = logging.getLogger(__name__)


@dataclass
class SensitivityResult:
    """Result of sensitivity analysis."""
    sensitivity: str = "normal"   # public/normal/internal/confidential/private
    confidence: float = 0.5
    detected_types: list[str] = None
    redacted_content: str = ""

    def __post_init__(self):
        if self.detected_types is None:
            self.detected_types = []


class SensitivityAnalyzer:
    """Auto-detect sensitivity level of memory content.

    Detection categories:
    - PII: Personal identifiable information (ID numbers, phone, email, address)
    - Financial: Salary, budget, pricing
    - Health: Medical conditions, medications
    - Credentials: Passwords, API keys, tokens
    - Emotional: Deep personal feelings, mental health
    """

    # Scope detection patterns (not PII, kept local)
    _SCOPE_PATTERNS = [
        (r'(?i)(项目|project|需求|requirement|迭代|sprint|部署|deploy)', 'work'),
        (r'(?i)(客户|client|合同|contract|报价|quote)', 'work'),
        (r'(?i)(家庭|family|孩子|child|父母|parent|朋友|friend)', 'personal'),
        (r'(?i)(爱好|hobby|游戏|game|电影|movie|旅行|travel)', 'personal'),
    ]

    # Category → sensitivity mapping
    _CATEGORY_SENSITIVITY = {
        "credential": "private",
        "pii": "confidential",
        "health": "confidential",
        "financial": "internal",
        "emotional": "private",
    }

    # Per-name overrides for sensitivity
    _NAME_SENSITIVITY = {
        "mental_health": "private",
    }

    def _patterns_for(self, category: str) -> list[PIIPattern]:
        """获取指定类别的模式列表。"""
        return get_patterns_by_category(category)

    def analyze(self, content: str) -> SensitivityResult:
        """Analyze content and determine sensitivity level.

        Returns SensitivityResult with:
        - sensitivity: the recommended level
        - confidence: how confident the analysis is
        - detected_types: list of detected sensitive info types
        - redacted_content: content with sensitive parts replaced
        """
        if not content:
            return SensitivityResult(sensitivity="normal", confidence=1.0)

        detected = []
        max_sensitivity = "normal"
        redacted = content

        # Check categories in priority order: credential → pii → health → financial → emotional
        for category in ("credential", "pii", "health", "financial", "emotional"):
            for p in self._patterns_for(category):
                if re.search(p.pattern, content):
                    detected.append(p.name)
                    # Determine sensitivity for this match
                    sensitivity = self._NAME_SENSITIVITY.get(
                        p.name, self._CATEGORY_SENSITIVITY.get(category, "normal")
                    )
                    if _sensitivity_level(max_sensitivity) < _sensitivity_level(sensitivity):
                        max_sensitivity = sensitivity
                    redacted = re.sub(p.pattern, f'[{p.name}_REDACTED]', redacted)

        confidence = min(0.5 + len(detected) * 0.15, 0.95) if detected else 0.3

        return SensitivityResult(
            sensitivity=max_sensitivity,
            confidence=confidence,
            detected_types=detected,
            redacted_content=redacted,
        )

    def detect_scope(self, content: str) -> str:
        """Detect the likely scope of memory content.

        Returns: 'personal', 'work', or 'mixed'
        """
        work_score = 0
        personal_score = 0

        for pattern, scope in self._SCOPE_PATTERNS:
            matches = len(re.findall(pattern, content))
            if scope == "work":
                work_score += matches
            elif scope == "personal":
                personal_score += matches

        if work_score > personal_score * 2:
            return "work"
        elif personal_score > work_score * 2:
            return "personal"
        elif work_score > 0 or personal_score > 0:
            return "mixed"
        return "personal"  # default


def _sensitivity_level(level: str) -> int:
    """Convert sensitivity string to numeric level."""
    return {"public": 0, "normal": 1, "internal": 2, "confidential": 3, "private": 4}.get(level, 1)
