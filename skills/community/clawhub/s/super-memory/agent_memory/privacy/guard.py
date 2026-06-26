"""Privacy Guard — 管家决定递出多少记忆

根据"谁在问 + 问什么 + 什么场景"决定递出多少记忆。
5级敏感度: public / normal / internal / confidential / private
3级访问: full / summary / deny
"""
from __future__ import annotations

import copy
import html
import logging
import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any

from .rules import AccessLevel, PrivacyRule, _sensitivity_to_visibility

logger = logging.getLogger(__name__)


class Sensitivity:
    """Memory sensitivity levels — kept as simple string constants."""
    PUBLIC = "public"              # Anyone can access
    NORMAL = "normal"              # Same-type agents can access
    INTERNAL = "internal"          # Work agents can access
    CONFIDENTIAL = "confidential"  # Requires explicit authorization, summary only
    PRIVATE = "private"            # Personal agents only


# Sensitivity hierarchy (higher = more restricted)
_SENSITIVITY_ORDER = {
    "public": 0,
    "normal": 1,
    "internal": 2,
    "confidential": 3,
    "private": 4,
}

# Agent scope hierarchy
_SCOPE_ORDER = {
    "personal": 0,
    "work": 1,
    "enterprise": 2,
    "external": 3,
}

_PII_PATTERNS = {
    'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
    'phone_cn': re.compile(r'1[3-9]\d{9}'),
    'id_card_cn': re.compile(r'[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx]'),
    'bank_card': re.compile(r'(?:62|4[0-9]|5[1-5])\d{14,17}'),
    'ip_address': re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b'),
    'passport': re.compile(r'[A-Z]{1,2}\d{6,9}'),
}

_REDACT_PLACEHOLDERS = {
    'email': '[EMAIL]',
    'phone_cn': '[PHONE]',
    'id_card_cn': '[ID_CARD]',
    'bank_card': '[BANK_CARD]',
    'ip_address': '[IP]',
    'passport': '[PASSPORT]',
}


@dataclass
class RequestContext:
    """Context of a memory access request."""
    agent_id: str = ""
    agent_type: str = "unknown"       # personal, work, external
    agent_scope: str = "personal"     # personal, work, enterprise, external
    task_type: str = ""               # search, report, decision, chat
    need_detail: bool = False         # Whether the task needs detailed info
    authorized_scopes: list[str] = field(default_factory=list)
    authorized_sensitivity_max: str = "normal"  # Max sensitivity this agent can access

    def can_access_scope(self, scope: str) -> bool:
        """Check if this context can access a given scope.

        Handles both memory_scope (V11) and tenant_id (existing).
        """
        if scope in self.authorized_scopes:
            return True
        # Default tenant is always accessible
        if scope in ("default", ""):
            return True
        # Personal scope: only personal agents
        if scope == "personal" and self.agent_scope != "personal":
            return False
        # Work scope: work and enterprise agents
        if scope == "work" and self.agent_scope not in ("work", "enterprise"):
            return False
        return True


# Default privacy rules (using rules.PrivacyRule — lower priority number = higher priority)
DEFAULT_RULES = [
    # External agents can only see public memories
    PrivacyRule(rule_id="external_public_only", name="External agents: public only",
                priority=10, agent_scopes=["external"],
                memory_visibilities=["public"], action=AccessLevel.FULL),
    # External agents denied non-public
    PrivacyRule(rule_id="external_deny_nonpublic", name="External agents: deny non-public",
                priority=11, agent_scopes=["external"],
                action=AccessLevel.DENY),
    # Work agents get summary for private
    PrivacyRule(rule_id="work_private_summary", name="Work agents: private → summary",
                priority=5, agent_scopes=["work"],
                memory_visibilities=["private"], action=AccessLevel.SUMMARY),
    # Work agents get summary for confidential sensitivity
    PrivacyRule(rule_id="work_confidential_summary", name="Work agents: confidential → summary",
                priority=6, agent_scopes=["work"],
                sensitivity_levels=["confidential"], action=AccessLevel.SUMMARY),
    # Personal agents can see everything
    PrivacyRule(rule_id="personal_full_access", name="Personal agents: full access",
                priority=1, agent_scopes=["personal"],
                action=AccessLevel.FULL),
]


class PrivacyGuard:
    """Privacy Guard — 管家决定递出多少记忆.

    Core logic:
    1. Check sensitivity level vs agent scope
    2. Apply custom rules
    3. Apply minimum necessary principle
    4. Return filtered/summarized memories
    """

    @staticmethod
    def _normalize_text(text: str) -> str:
        """Normalize text before PII detection to prevent bypass."""
        # 1. Remove zero-width characters
        text = re.sub(r'[\u200b\u200c\u200d\ufeff\u00ad]', '', text)
        # 2. Remove RTL overrides
        text = re.sub(r'[\u202a\u202b\u202c\u202d\u202e]', '', text)
        # 3. Decode HTML entities
        text = html.unescape(text)
        # 4. Unicode NFC normalization (fullwidth -> ASCII)
        text = unicodedata.normalize('NFKC', text)
        # 5. Remove non-printable characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        return text

    def __init__(self, rules: list[PrivacyRule] | None = None):
        self._rules = rules or list(DEFAULT_RULES)
        self._rules.sort(key=lambda r: r.priority)

    def add_rule(self, rule: PrivacyRule):
        """Add a custom privacy rule."""
        self._rules.append(rule)
        self._rules.sort(key=lambda r: r.priority)

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by rule_id."""
        before = len(self._rules)
        self._rules = [r for r in self._rules if r.rule_id != rule_id]
        return len(self._rules) < before

    def check_access(self, memory: dict, ctx: RequestContext) -> AccessLevel:
        """Check the access level for a memory given a request context.

        Maps to existing visibility field (private/team/public) when available,
        falls back to sensitivity field for V11 compatibility.
        """
        # Prefer existing visibility field, map sensitivity to visibility if absent
        visibility = memory.get("visibility", "")
        if not visibility:
            visibility = _sensitivity_to_visibility(memory.get("sensitivity", "normal"))

        # Public visibility → always accessible
        if visibility == "public":
            return AccessLevel.FULL

        # Check scope access using tenant_id or memory_scope
        mem_scope = memory.get("memory_scope", "") or memory.get("tenant_id", "default")
        if not ctx.can_access_scope(mem_scope):
            return AccessLevel.DENY

        # Determine effective max visibility from agent context
        max_vis = ctx.authorized_sensitivity_max  # reused as max visibility
        vis_order = {"public": 0, "team": 1, "private": 2}
        mem_vis_level = vis_order.get(visibility, 1)
        max_vis_level = vis_order.get(max_vis, 1)

        if mem_vis_level <= max_vis_level:
            return AccessLevel.FULL

        # Sensitivity exceeds max — check for summary rule
        for rule in self._rules:
            if rule.matches(ctx, memory):
                if rule.action == AccessLevel.SUMMARY:
                    return AccessLevel.SUMMARY

        return AccessLevel.DENY

    def filter_memories(self, memories: list[dict],
                        ctx: RequestContext) -> list[dict]:
        """Filter a list of memories based on privacy rules.

        Returns a new list with only allowed memories, potentially summarized.
        """
        filtered = []
        for mem in memories:
            access = self.check_access(mem, ctx)
            if access == AccessLevel.DENY:
                continue
            elif access == AccessLevel.SUMMARY:
                filtered.append(self._summarize_memory(mem))
            else:
                filtered.append(mem)
        return filtered

    def _summarize_memory(self, memory: dict) -> dict:
        """Create a summary version of a memory (remove sensitive details)."""
        summary = copy.deepcopy(memory)
        content = summary.get("content", "")
        if len(content) > 100:
            summary["content"] = content[:100] + "..."
        summary.pop("person_id", None)
        summary.pop("compound_emotions", None)
        summary["access_level"] = "summary"
        return summary

    def redact(self, content: str, categories: list | None = None,
               replacement: str | None = None) -> str:
        """Detect and redact PII from content.

        Args:
            content: Text to redact
            categories: PII categories to detect (None = all)
            replacement: Custom replacement string (None = category-specific placeholder)

        Returns:
            Redacted content with PII replaced by placeholders
        """
        if not content:
            return content

        patterns = _PII_PATTERNS
        if categories:
            patterns = {k: v for k, v in patterns.items() if k in categories}

        normalized = self._normalize_text(content)
        result = normalized
        for category, pattern in patterns.items():
            repl = replacement or _REDACT_PLACEHOLDERS.get(category, '[REDACTED]')
            result = pattern.sub(repl, result)

        return result

    def detect_pii(self, content: str, categories: list | None = None) -> list[dict]:
        """Detect PII in content without redacting.

        Returns:
            List of dicts with keys: category, value, start, end
        """
        if not content:
            return []

        patterns = _PII_PATTERNS
        if categories:
            patterns = {k: v for k, v in patterns.items() if k in categories}

        normalized = self._normalize_text(content)
        findings = []
        for category, pattern in patterns.items():
            for match in pattern.finditer(normalized):
                findings.append({
                    'category': category,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                })

        return sorted(findings, key=lambda x: x['start'])

    def redact_memory(self, memory: dict, fields: list | None = None) -> dict:
        """Redact PII from a memory dict.

        Args:
            memory: Memory dict with 'content' and other fields
            fields: List of field names to redact (default: ['content'])

        Returns:
            Memory dict with PII redacted
        """
        if not memory:
            return memory

        fields = fields or ['content']
        result = dict(memory)

        for field in fields:
            if field in result and isinstance(result[field], str):
                result[field] = self.redact(result[field])

        return result
