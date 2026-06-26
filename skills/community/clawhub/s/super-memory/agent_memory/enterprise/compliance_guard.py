"""
enterprise/compliance_guard.py — Compliance and PII detection.

Automatically scans memory content for PII, financial, and health data.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

from ..privacy.patterns import PIIPattern, get_all_patterns

logger = logging.getLogger(__name__)


@dataclass
class ComplianceResult:
    """Result of a compliance scan."""
    is_compliant: bool = True
    detected_types: list[str] = field(default_factory=list)
    risk_level: str = "low"  # low, medium, high, critical
    redacted_content: str = ""
    details: list[str] = field(default_factory=list)


class ComplianceGuard:
    """Scan and redact sensitive information for compliance.

    Detection categories:
    - PII: names, ID numbers, phone, email, address
    - Financial: salary, bank account, credit card
    - Health: medical conditions, medications
    - Credentials: passwords, API keys, tokens
    """

    # High-risk pattern names (determine critical risk level)
    _HIGH_RISK_NAMES = {"id_card", "bank_card", "credit_card", "password", "api_key", "auth_token"}

    # High-risk pattern names (determine high risk level)
    _ELEVATED_RISK_NAMES = {"salary", "medical", "mental_health", "deep_emotion", "therapy"}

    @property
    def _patterns(self) -> dict[str, re.Pattern]:
        """从统一模式注册表构建 {name: compiled_pattern} 映射。"""
        return {p.name: p.compiled for p in get_all_patterns()}

    def scan(self, content: str) -> ComplianceResult:
        """Scan content for compliance issues."""
        detected = []
        details = []
        redacted = content

        for ptype, pattern in self._patterns.items():
            matches = pattern.findall(content)
            if matches:
                detected.append(ptype)
                details.append(f"{ptype}: {len(matches)} occurrence(s)")
                # Redact
                redacted = pattern.sub(f"[REDACTED_{ptype.upper()}]", redacted)

        # Determine risk level
        if any(t in self._HIGH_RISK_NAMES for t in detected):
            risk = "critical"
        elif any(t in self._ELEVATED_RISK_NAMES for t in detected):
            risk = "high"
        elif detected:
            risk = "medium"
        else:
            risk = "low"

        return ComplianceResult(
            is_compliant=risk in ("low", "medium"),
            detected_types=detected,
            risk_level=risk,
            redacted_content=redacted,
            details=details,
        )

    def redact(self, content: str, types: list[str] | None = None) -> str:
        """Redact specified types of sensitive information."""
        result = content
        patterns = self._patterns
        target_types = types or list(patterns.keys())
        for ptype in target_types:
            if ptype in patterns:
                result = patterns[ptype].sub(f"[REDACTED_{ptype.upper()}]", result)
        return result
