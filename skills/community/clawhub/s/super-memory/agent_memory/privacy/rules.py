"""
privacy/rules.py — Privacy Rules Engine

Declarative rule system for memory access control.
Rules are evaluated in priority order; first match wins.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AccessLevel(Enum):
    FULL = "full"
    SUMMARY = "summary"
    DENY = "deny"


@dataclass
class PrivacyRule:
    """A single privacy rule.

    Rules are evaluated in priority order (lower number = higher priority).
    First matching rule wins. If no rule matches, the default_action applies.
    """
    rule_id: str                           # Unique identifier
    name: str                              # Human-readable name
    priority: int = 100                    # Lower = higher priority
    agent_types: list[str] = field(default_factory=list)  # Match agent_type (empty = any)
    agent_scopes: list[str] = field(default_factory=list)  # Match agent_scope (empty = any)
    memory_visibilities: list[str] = field(default_factory=list)  # Match visibility (empty = any)
    memory_scopes: list[str] = field(default_factory=list)  # Match memory_scope/tenant_id (empty = any)
    sensitivity_levels: list[str] = field(default_factory=list)  # Match sensitivity (empty = any)
    task_types: list[str] = field(default_factory=list)  # Match task context (empty = any)
    action: AccessLevel = AccessLevel.FULL  # What to do if matched
    enabled: bool = True

    def matches(self, ctx: Any, memory: dict) -> bool:
        """Check if this rule matches the given context and memory."""
        if not self.enabled:
            return False
        # Check agent_type
        if self.agent_types and getattr(ctx, 'agent_type', '') not in self.agent_types:
            return False
        # Check agent_scope
        if self.agent_scopes and getattr(ctx, 'agent_scope', '') not in self.agent_scopes:
            return False
        # Check memory visibility
        vis = memory.get("visibility", "")
        if not vis:
            vis = _sensitivity_to_visibility(memory.get("sensitivity", "normal"))
        if self.memory_visibilities and vis not in self.memory_visibilities:
            return False
        # Check memory scope
        scope = memory.get("memory_scope", "") or memory.get("tenant_id", "default")
        if self.memory_scopes and scope not in self.memory_scopes:
            return False
        # Check sensitivity
        sens = memory.get("sensitivity", "normal")
        if self.sensitivity_levels and sens not in self.sensitivity_levels:
            return False
        # Check task type
        if self.task_types:
            task = getattr(ctx, 'task_type', '')
            if task not in self.task_types:
                return False
        return True


def _sensitivity_to_visibility(sensitivity: str) -> str:
    """Map sensitivity to visibility."""
    mapping = {"public": "public", "normal": "team", "internal": "team",
               "confidential": "team", "private": "private"}
    return mapping.get(sensitivity, "team")


@dataclass
class PrivacyRuleSet:
    """A collection of privacy rules with evaluation logic."""
    rules: list[PrivacyRule] = field(default_factory=list)
    default_action: AccessLevel = AccessLevel.FULL

    def evaluate(self, ctx: Any, memory: dict) -> AccessLevel:
        """Evaluate all rules against the context and memory. First match wins."""
        # Sort by priority
        sorted_rules = sorted(self.rules, key=lambda r: r.priority)
        for rule in sorted_rules:
            if rule.matches(ctx, memory):
                logger.debug("PrivacyRule matched: %s (action=%s)", rule.rule_id, rule.action)
                return rule.action
        return self.default_action

    def add_rule(self, rule: PrivacyRule):
        """Add a rule to the set."""
        self.rules.append(rule)

    def remove_rule(self, rule_id: str) -> bool:
        """Remove a rule by ID."""
        before = len(self.rules)
        self.rules = [r for r in self.rules if r.rule_id != rule_id]
        return len(self.rules) < before

    def save(self, path: str):
        """Save rules to JSON file."""
        data = {
            "default_action": self.default_action.value,
            "rules": [
                {
                    "rule_id": r.rule_id,
                    "name": r.name,
                    "priority": r.priority,
                    "agent_types": r.agent_types,
                    "agent_scopes": r.agent_scopes,
                    "memory_visibilities": r.memory_visibilities,
                    "memory_scopes": r.memory_scopes,
                    "sensitivity_levels": r.sensitivity_levels,
                    "task_types": r.task_types,
                    "action": r.action.value,
                    "enabled": r.enabled,
                }
                for r in self.rules
            ]
        }
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> PrivacyRuleSet:
        """Load rules from JSON file."""
        if not os.path.exists(path):
            return cls()
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        rules = []
        for rd in data.get("rules", []):
            rd["action"] = AccessLevel(rd.get("action", "full"))
            rules.append(PrivacyRule(**rd))
        return cls(
            rules=rules,
            default_action=AccessLevel(data.get("default_action", "full")),
        )


def default_personal_ruleset() -> PrivacyRuleSet:
    """Create the default rule set for personal butler mode."""
    return PrivacyRuleSet(
        rules=[
            # R1: External agents can only see public
            PrivacyRule(
                rule_id="ext_public_only",
                name="External agents: public only",
                priority=10,
                agent_types=["external"],
                memory_visibilities=["public"],
                action=AccessLevel.FULL,
            ),
            # R2: External agents denied non-public
            PrivacyRule(
                rule_id="ext_deny_nonpublic",
                name="External agents: deny non-public",
                priority=11,
                agent_types=["external"],
                action=AccessLevel.DENY,
            ),
            # R3: Work agents get summary for private
            PrivacyRule(
                rule_id="work_private_summary",
                name="Work agents: private → summary",
                priority=20,
                agent_types=["work"],
                memory_visibilities=["private"],
                action=AccessLevel.SUMMARY,
            ),
            # R4: Work agents full access to team
            PrivacyRule(
                rule_id="work_team_full",
                name="Work agents: team → full",
                priority=21,
                agent_types=["work"],
                memory_visibilities=["team", "public"],
                action=AccessLevel.FULL,
            ),
            # R5: Personal agents full access to everything
            PrivacyRule(
                rule_id="personal_full",
                name="Personal agents: full access",
                priority=30,
                agent_types=["personal"],
                action=AccessLevel.FULL,
            ),
            # R6: Enterprise agents full access to team+public
            PrivacyRule(
                rule_id="enterprise_team_full",
                name="Enterprise agents: team+public → full",
                priority=40,
                agent_types=["enterprise"],
                memory_visibilities=["team", "public"],
                action=AccessLevel.FULL,
            ),
            # R7: Enterprise agents summary for private
            PrivacyRule(
                rule_id="enterprise_private_summary",
                name="Enterprise agents: private → summary",
                priority=41,
                agent_types=["enterprise"],
                memory_visibilities=["private"],
                action=AccessLevel.SUMMARY,
            ),
        ],
        default_action=AccessLevel.DENY,
    )


def default_enterprise_ruleset() -> PrivacyRuleSet:
    """Create the default rule set for enterprise butler mode."""
    return PrivacyRuleSet(
        rules=[
            # E1: Interns can only see public + team (summary for confidential)
            PrivacyRule(
                rule_id="intern_confidential_summary",
                name="Interns: confidential → summary",
                priority=10,
                agent_types=["intern"],
                sensitivity_levels=["confidential"],
                action=AccessLevel.SUMMARY,
            ),
            PrivacyRule(
                rule_id="intern_private_deny",
                name="Interns: private → deny",
                priority=11,
                agent_types=["intern"],
                sensitivity_levels=["private"],
                action=AccessLevel.DENY,
            ),
            # E2: Members full access to internal, summary for confidential
            PrivacyRule(
                rule_id="member_confidential_summary",
                name="Members: confidential → summary",
                priority=20,
                agent_types=["member"],
                sensitivity_levels=["confidential"],
                action=AccessLevel.SUMMARY,
            ),
            # E3: Managers full access to everything except private
            PrivacyRule(
                rule_id="manager_private_deny",
                name="Managers: private → deny",
                priority=30,
                agent_types=["manager"],
                sensitivity_levels=["private"],
                action=AccessLevel.DENY,
            ),
            # E4: Admins full access
            PrivacyRule(
                rule_id="admin_full",
                name="Admins: full access",
                priority=40,
                agent_types=["admin"],
                action=AccessLevel.FULL,
            ),
        ],
        default_action=AccessLevel.DENY,
    )
