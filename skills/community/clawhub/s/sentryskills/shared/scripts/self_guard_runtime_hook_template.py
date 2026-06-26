#!/usr/bin/env python3
"""Runtime hook for TrinityGuard self-guard orchestration.

Primary output is JSONL event stream. Optional summary JSON can be written via --out.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any, Dict, List, Optional, Pattern

# Configure logging FIRST
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import TrinityGuard exceptions
from exceptions import (
    TrinityGuardError,
    InputValidationError,
    PolicyLoadError,
    DetectionError,
    safe_detect,
    handle_file_errors,
    ErrorRecovery,
    log_error_with_context,
)

# Import validation and resource management
try:
    from validation import validate_input, validate_policy, sanitize_input
    VALIDATION_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Validation modules not available: {e}")
    VALIDATION_AVAILABLE = False

# Import resource management (platform-specific)
try:
    from resource_management import (
        resource_context,
        check_disk_space,
        limit_text_length,
        limit_array_size,
    )
    RESOURCE_MANAGEMENT_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Resource management modules not available: {e}")
    RESOURCE_MANAGEMENT_AVAILABLE = False

# Import performance optimization module
try:
    from performance import (
        parallel_detect,
        parallel_detect_threadpool,
        should_early_exit,
        cached_detect,
        get_cache_stats,
        performance_monitor,
    )
    PERFORMANCE_AVAILABLE = True
    logger.info("Performance optimization module loaded")
except ImportError as e:
    logger.warning(f"Performance optimization module not available: {e}")
    PERFORMANCE_AVAILABLE = False

# Import predictive analysis module
try:
    from predictive_analysis import predict_risks
    PREDICTIVE_ANALYSIS_AVAILABLE = True
    logger.info("Predictive analysis module loaded")
except ImportError as e:
    logger.warning(f"Predictive analysis module not available: {e}")
    PREDICTIVE_ANALYSIS_AVAILABLE = False

# Create platform-specific fallbacks
if not RESOURCE_MANAGEMENT_AVAILABLE:
    # Fallback implementations for resource management
    import contextlib

    @contextlib.contextmanager
    def resource_context(**kwargs):
        """Fallback resource context (no-op)."""
        yield lambda: None

    def check_disk_space(*args, **kwargs):
        """Fallback disk space check (no-op)."""
        pass

    def limit_text_length(text, max_length=1000000):
        """Fallback text limiter."""
        if isinstance(text, str) and len(text) > max_length:
            suffix = "... [truncated]"
            truncated_max = max_length - len(suffix)
            return text[:max(0, truncated_max)] + suffix
        return text

    def limit_array_size(arr, max_size=10000):
        """Fallback array limiter."""
        if isinstance(arr, list) and len(arr) > max_size:
            return arr[:max_size]
        return arr

    logger.debug("Using fallback resource management (resource limits not available on this platform)")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Feature flags (controlled via environment, with defaults)
# These can be overridden in main() based on environment variables
early_exit_enabled: bool = True
contextual_matching_enabled: bool = True
pattern_cache_enabled: bool = True
parallel_detection_enabled: bool = True  # NEW: Parallel detection
detection_cache_enabled: bool = True      # NEW: Detection result cache

DEFAULT_POLICY: Dict[str, Any] = {
    "sensitive_event_types": ["read_secret", "read_credential", "read_private_pii", "read_key_material"],
    "sensitive_keywords": ["token", "password", "secret", "api_key", "credential", "private key", "id card", "phone number"],
    "explicit_disclosure_phrases": ["output token", "output password", "print token", "print password"],
    "implicit_disclosure_phrases": [
        "explain key fields and values",
        "repeat full configuration",
        "write out as-is",
        "show me the value",
        "include actual values",
    ],
    "explanation_leakage_phrases": ["explain purpose and give values", "list example values when explaining", "for explanation include exact values"],
    "high_risk_actions": ["execute_command", "write_file", "batch_modify", "network_call"],
    "retry_threshold_downgrade": 3,
    "single_source_types": ["tool_single_source"],
    "leak_patterns": [
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*[^\s,;]+",
        r"(?i)-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        r"\b\d{17}[0-9Xx]\b",
    ],
    "residual_leak_patterns": [
        r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*(?!\[REDACTED\])[^\s,;]+",
        r"(?i)-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
        r"\b\d{17}[0-9Xx]\b",
    ],
    "force_uncertainty_prefix": "Conclusion uncertain based on single tool source:",
    "block_on_highly_sensitive_leak": True,
    "redaction_replacements": {
        "credential": r"(?i)(api[_-]?key|token|password|secret)\s*[:=]\s*([^\s,;]+)",
        "id": r"\b\d{17}[0-9Xx]\b",
        "private_key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    },
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def append_jsonl(path: Path, record: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def merge_policy(default: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(default)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(merged.get(k), dict):
            inner = dict(merged[k])
            inner.update(v)
            merged[k] = inner
        else:
            merged[k] = v
    return merged


def compile_patterns(patterns: List[str]) -> List[Pattern[str]]:
    return [re.compile(p) for p in patterns]


# Pattern cache with policy hash tracking
_pattern_cache: Dict[str, List[Pattern[str]]] = {}
_policy_hash_cache: Dict[str, str] = {}

def get_cached_patterns(policy: Dict[str, Any], cache_key: str = "leak_patterns") -> List[Pattern[str]]:
    """Get compiled patterns from cache, recompiling only if policy changed."""
    if not pattern_cache_enabled:
        patterns_raw = [str(x) for x in policy.get(cache_key, [])]
        return compile_patterns(patterns_raw)

    patterns_raw = [str(x) for x in policy.get(cache_key, [])]
    policy_hash = hash_text("|".join(patterns_raw))

    if cache_key in _policy_hash_cache and _policy_hash_cache[cache_key] == policy_hash:
        return _pattern_cache.get(cache_key, [])

    # Cache miss - compile and store
    compiled = compile_patterns(patterns_raw)
    _pattern_cache[cache_key] = compiled
    _policy_hash_cache[cache_key] = policy_hash
    return compiled


def get_match_hits(text: str, phrases: List[str]) -> List[str]:
    """Find phrase matches with word-boundary awareness to reduce false positives."""
    if not contextual_matching_enabled:
        # Original behavior
        low_text = text.lower()
        hits: List[str] = []
        for phrase in phrases:
            if str(phrase).lower() in low_text:
                hits.append(str(phrase))
        return sorted(set(hits))

    # Enhanced behavior with word boundaries
    low_text = text.lower()
    hits: List[str] = []

    for phrase in phrases:
        phrase_low = str(phrase).lower()
        if phrase_low in low_text:
            # Check for word boundaries to avoid subword matches
            pattern = rf'\b{re.escape(phrase_low)}\b'
            if re.search(pattern, low_text):
                hits.append(str(phrase))

    return sorted(set(hits))


def is_credential_exfil_request(prompt_low: str) -> bool:
    """Detect credential exfiltration intent with negation awareness."""
    target_terms = [
        "api_key", "apikey", "access_token", "token",
        "password", "secret", "key", "credential"
    ]
    action_terms = [
        "find", "extract", "give me", "output", "list", "print", "return",
        "read", "extract", "show", "print", "list", "dump", "find", "give me"
    ]

    has_target = any(t in prompt_low for t in target_terms)
    has_action = any(a in prompt_low for a in action_terms)

    if not (has_target and has_action):
        return False

    if not contextual_matching_enabled:
        return True

    # Enhanced: check for negation
    negation_terms = [
        "don't", "not", "never", "without", "avoid", "prevent",
        "protect", "secure", "encrypt", "hide"
    ]

    has_negation = any(n in prompt_low for n in negation_terms)
    if has_negation:
        # Check proximity: negation within 50 chars before target
        for target in target_terms:
            if target in prompt_low:
                target_idx = prompt_low.find(target)
                for neg in negation_terms:
                    neg_idx = prompt_low.find(neg)
                    if 0 <= neg_idx < target_idx and (target_idx - neg_idx) < 50:
                        return False  # Negated exfil request

    return True


def detect_jwt_token(text: str) -> bool:
    """Detect JWT tokens in text."""
    jwt_pattern = r"eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+"
    matches = re.findall(jwt_pattern, text)

    for match in matches:
        # Basic JWT validation: 3 parts separated by dots
        parts = match.split('.')
        if len(parts) == 3:
            # Check reasonable length
            if all(len(p) > 10 for p in parts):
                return True
    return False


def detect_database_connection(text: str) -> bool:
    """Detect database connection strings."""
    db_patterns = [
        r"(?i)(mongodb(\+srv)?://|mysql://|postgresql?://|redis://)[^\s:@]+:[^\s@]+@",
        r"(?i)jdbc:\w+://[^\s:]+:[^\s@]+@",
        r"(?i)server=[^\s;]+;.*database=[^\s;]+;",
        r"(?i)host=[^\s;]+;.*password=[^\s;]+"
    ]

    for pattern in db_patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_email_addresses(text: str) -> bool:
    """Detect email addresses (for PII detection)."""
    # Only detect if multiple emails or email + sensitive keywords
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    emails = re.findall(email_pattern, text)

    # Multiple emails likely indicates PII
    if len(emails) >= 3:
        return True

    # Email + sensitive keywords
    sensitive_context = ["user", "customer", "client", "employee", "contact", "list"]
    if emails and any(ctx in text.lower() for ctx in sensitive_context):
        return True

    return False


def detect_ip_addresses(text: str) -> bool:
    """Detect IP addresses, excluding localhost."""
    ipv4_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ipv6_pattern = r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"

    # Find IPs
    ipv4_matches = re.findall(ipv4_pattern, text)
    ipv6_matches = re.findall(ipv6_pattern, text)

    all_ips = ipv4_matches + ipv6_matches

    # Filter out localhost/private ranges
    filtered_ips = []
    for ip in all_ips:
        ip_lower = ip.lower()
        # Skip localhost
        if ip in ["127.0.0.1", "::1", "localhost"]:
            continue
        # Skip common documentation examples
        if ip.startswith("192.0.2.") or ip.startswith("198.51.100.") or ip.startswith("203.0.113."):
            continue
        filtered_ips.append(ip)

    # Multiple non-localhost IPs
    if len(filtered_ips) >= 2:
        return True

    # IP + internal keywords
    internal_keywords = ["internal", "private", "server", "endpoint", "backend", "service"]
    if filtered_ips and any(kw in text.lower() for kw in internal_keywords):
        return True

    return False


def detect_credit_card(text: str) -> bool:
    """Detect potential credit card numbers."""
    cc_pattern = r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b"
    matches = re.findall(cc_pattern, text)

    for match in matches:
        # Remove spaces/dashes
        digits = re.sub(r"[\s-]", "", match)
        if len(digits) == 16:
            # Basic Luhn check could be added here
            # For now, just check for sensitive context
            sensitive_context = ["card", "credit", "payment", "visa", "mastercard", "amex"]
            if any(ctx in text.lower() for ctx in sensitive_context):
                return True

    return False


def detect_environment_variables(text: str) -> bool:
    """Detect environment variable references."""
    env_patterns = [
        r"%[A-Z_]+%",  # Windows style
        r"\$\{[A-Z_]+\}",  # Unix style
        r"\$[A-Z_]+"  # Simple Unix style
    ]

    for pattern in env_patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_attack_patterns(text: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect common attack patterns."""
    attack_detection = policy.get("attack_detection", {})
    if not attack_detection.get("enabled", False):
        return {"detected": False, "patterns": []}

    detected_patterns = []

    # SQL Injection
    sql_patterns = attack_detection.get("sql_injection_patterns", [])
    for pattern in sql_patterns:
        if re.search(pattern, text):
            detected_patterns.append("sql_injection")

    # Command Injection
    cmd_patterns = attack_detection.get("command_injection_patterns", [])
    for pattern in cmd_patterns:
        if re.search(pattern, text):
            detected_patterns.append("command_injection")

    # Path Traversal
    path_patterns = attack_detection.get("path_traversal_patterns", [])
    for pattern in path_patterns:
        if re.search(pattern, text):
            detected_patterns.append("path_traversal")

    return {
        "detected": len(detected_patterns) > 0,
        "patterns": detected_patterns
    }


def detect_environment_context(context: str) -> str:
    """Detect the current environment (production/staging/development)."""
    if not context:
        return "unknown"

    context_awareness = {
        "production": ["prod", "production", "live", "main"],
        "staging": ["staging", "stage", "uat"],
        "development": ["dev", "development", "local", "test"]
    }

    context_lower = context.lower()
    for env_type, keywords in context_awareness.items():
        if any(kw in context_lower for kw in keywords):
            return env_type

    return "unknown"


def assess_action_risk(action: str, environment: str, sensitivity: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Assess the risk level of an action based on context."""
    context_awareness = policy.get("context_awareness", {})
    risk_multipliers = context_awareness.get("risk_multipliers", {})

    # Base risk levels
    base_risks = {
        "delete_database": "critical",
        "deploy_to_production": "critical",
        "modify_firewall": "critical",
        "change_dns": "critical",
        "execute_system_command": "critical",
        "drop_table": "critical",
        "truncate_database": "critical",
        "delete_file": "high",
        "delete_directory": "high",
        "database_query": "high",
        "execute_sql": "high",
        "send_email": "high",
        "external_api_call": "high",
        "write_file": "medium",
        "batch_modify": "medium",
        "network_call": "medium"
    }

    base_risk = base_risks.get(action, "medium")

    # Apply environment multiplier
    env_multiplier = 1.0
    if environment in risk_multipliers:
        env_multiplier = risk_multipliers[environment]

    # Apply sensitivity multiplier
    sensitivity_multiplier = 1.0
    if sensitivity == "highly_sensitive":
        sensitivity_multiplier = 2.0
    elif sensitivity == "sensitive":
        sensitivity_multiplier = 1.5

    # Calculate final risk score
    risk_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    base_score = risk_scores.get(base_risk, 2)
    adjusted_score = base_score * env_multiplier * sensitivity_multiplier

    # Convert back to risk level
    if adjusted_score >= 8:
        final_risk = "critical"
    elif adjusted_score >= 5:
        final_risk = "high"
    elif adjusted_score >= 3:
        final_risk = "medium"
    else:
        final_risk = "low"

    return {
        "risk_level": final_risk,
        "base_risk": base_risk,
        "environment": environment,
        "env_multiplier": env_multiplier,
        "sensitivity_multiplier": sensitivity_multiplier,
        "adjusted_score": adjusted_score
    }


# ============================================================================
# Phase 2: Advanced Attack Detection
# ============================================================================

def detect_ssrf(text: str, policy: Dict[str, Any]) -> bool:
    """Detect Server-Side Request Forgery (SSRF) attempts."""
    advanced_config = policy.get("advanced_attack_detection", {})
    if not advanced_config.get("enabled", False):
        return False

    ssrf_patterns = advanced_config.get("ssrf_patterns", [])

    # Check if any SSRF pattern matches
    for pattern in ssrf_patterns:
        if re.search(pattern, text):
            # Additional check: look for user-controlled URLs
            # URL parameters, fetch() with user input, etc.
            return True

    return False


def detect_xxe(text: str, policy: Dict[str, Any]) -> bool:
    """Detect XML External Entity (XXE) injection attempts."""
    advanced_config = policy.get("advanced_attack_detection", {})
    if not advanced_config.get("enabled", False):
        return False

    xxe_patterns = advanced_config.get("xxe_patterns", [])

    for pattern in xxe_patterns:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            # Check for ENTITY definitions
            if re.search(r"<!ENTITY", text, re.IGNORECASE):
                return True

    return False


def detect_template_injection(text: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect template injection attempts."""
    advanced_config = policy.get("advanced_attack_detection", {})
    if not advanced_config.get("enabled", False):
        return {"detected": False, "type": None}

    template_patterns = advanced_config.get("template_injection_patterns", [])

    detected_types = []
    for pattern in template_patterns:
        if re.search(pattern, text):
            # Determine template type
            if "{{" in text and "}}" in text:
                detected_types.append("jinja2")
            elif "${" in text and "}" in text:
                detected_types.append("spring_el")
            elif "<%" in text and "%>" in text:
                detected_types.append("jsp")
            elif "#{" in text and "}" in text:
                detected_types.append("ruby")

    return {
        "detected": len(detected_types) > 0,
        "types": detected_types
    }


def detect_ldap_injection(text: str, policy: Dict[str, Any]) -> bool:
    """Detect LDAP injection attempts."""
    advanced_config = policy.get("advanced_attack_detection", {})
    if not advanced_config.get("enabled", False):
        return False

    ldap_patterns = advanced_config.get("ldap_injection_patterns", [])

    for pattern in ldap_patterns:
        if re.search(pattern, text):
            # Additional context check
            ldap_keywords = ["ldap", "ad", "active directory", "directory"]
            if any(kw in text.lower() for kw in ldap_keywords):
                return True

    return False


def detect_xpath_injection(text: str, policy: Dict[str, Any]) -> bool:
    """Detect XPath injection attempts."""
    advanced_config = policy.get("advanced_attack_detection", {})
    if not advanced_config.get("enabled", False):
        return False

    xpath_patterns = advanced_config.get("xpath_injection_patterns", [])

    for pattern in xpath_patterns:
        if re.search(pattern, text):
            # Check for XPath keywords
            xpath_keywords = ["descendant", "ancestor", "following", "preceding"]
            if any(kw in text.lower() for kw in xpath_keywords):
                return True

    return False


# ============================================================================
# Extended Detection Rules (Phase 1: Pattern Matching)
# ============================================================================

def detect_llm_prompt_injection(text: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect LLM prompt injection and jailbreak attempts."""
    result = {
        "detected": False,
        "matches": [],
        "severity": "medium"
    }

    # Get patterns from detection rules
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("ai_model", {}).get("rules", [])
    injection_rule = next((r for r in rules if r["name"] == "llm_prompt_injection"), None)

    if not injection_rule or not injection_rule.get("enabled", False):
        return result

    text_lower = text.lower()
    patterns = injection_rule.get("patterns", [])

    for pattern in patterns:
        if pattern.lower() in text_lower:
            result["detected"] = True
            result["matches"].append(pattern)
            result["severity"] = injection_rule.get("severity", "medium")

    return result


def detect_llm_indirect_prompt_leak(text: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect attempts to extract system prompts."""
    result = {
        "detected": False,
        "matches": [],
        "severity": "medium"
    }

    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("ai_model", {}).get("rules", [])
    leak_rule = next((r for r in rules if r["name"] == "llm_indirect_prompt_leak"), None)

    if not leak_rule or not leak_rule.get("enabled", False):
        return result

    text_lower = text.lower()
    patterns = leak_rule.get("patterns", [])

    for pattern in patterns:
        if pattern.lower() in text_lower:
            result["detected"] = True
            result["matches"].append(pattern)
            result["severity"] = leak_rule.get("severity", "medium")

    return result


def detect_ssh_private_key(text: str, policy: Dict[str, Any]) -> bool:
    """Detect SSH private key exposure."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("data_leak", {}).get("rules", [])
    ssh_rule = next((r for r in rules if r["name"] == "ssh_private_key"), None)

    if not ssh_rule or not ssh_rule.get("enabled", False):
        return False

    patterns = ssh_rule.get("patterns", [])
    for pattern in patterns:
        if pattern in text:
            return True
    return False


def detect_aws_credentials(text: str, policy: Dict[str, Any]) -> bool:
    """Detect AWS credential exposure."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("data_leak", {}).get("rules", [])
    aws_rule = next((r for r in rules if r["name"] == "aws_credentials"), None)

    if not aws_rule or not aws_rule.get("enabled", False):
        return False

    patterns = aws_rule.get("patterns", [])
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_github_token(text: str, policy: Dict[str, Any]) -> bool:
    """Detect GitHub token exposure."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("data_leak", {}).get("rules", [])
    github_rule = next((r for r in rules if r["name"] == "github_token"), None)

    if not github_rule or not github_rule.get("enabled", False):
        return False

    patterns = github_rule.get("patterns", [])
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_slack_token(text: str, policy: Dict[str, Any]) -> bool:
    """Detect Slack token exposure."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("data_leak", {}).get("rules", [])
    slack_rule = next((r for r in rules if r["name"] == "slack_token"), None)

    if not slack_rule or not slack_rule.get("enabled", False):
        return False

    patterns = slack_rule.get("patterns", [])
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_ssti(text: str, policy: Dict[str, Any]) -> bool:
    """Detect Server-Side Template Injection."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("web_security", {}).get("rules", [])
    ssti_rule = next((r for r in rules if r["name"] == "ssti_detection"), None)

    if not ssti_rule or not ssti_rule.get("enabled", False):
        return False

    patterns = ssti_rule.get("patterns", [])
    for pattern in patterns:
        if pattern.lower() in text.lower():
            return True
    return False


def detect_log4j(text: str, policy: Dict[str, Any]) -> bool:
    """Detect Log4Shell and JNDI injection."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("web_security", {}).get("rules", [])
    log4j_rule = next((r for r in rules if r["name"] == "log4j_detection"), None)

    if not log4j_rule or not log4j_rule.get("enabled", False):
        return False

    patterns = log4j_rule.get("patterns", [])
    for pattern in patterns:
        if pattern.lower() in text.lower():
            return True
    return False


def detect_command_injection(text: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect command injection attempts."""
    result = {
        "detected": False,
        "matches": [],
        "severity": "high"
    }

    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("web_security", {}).get("rules", [])
    cmd_rule = next((r for r in rules if r["name"] == "command_injection_basic"), None)

    if not cmd_rule or not cmd_rule.get("enabled", False):
        return result

    patterns = cmd_rule.get("patterns", [])
    for pattern in patterns:
        if pattern.lower() in text.lower():
            result["detected"] = True
            result["matches"].append(pattern)
            result["severity"] = cmd_rule.get("severity", "high")

    return result


def detect_weak_crypto(text: str, policy: Dict[str, Any]) -> bool:
    """Detect weak cryptographic algorithms."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("code_security", {}).get("rules", [])
    crypto_rule = next((r for r in rules if r["name"] == "weak_crypto"), None)

    if not crypto_rule or not crypto_rule.get("enabled", False):
        return False

    patterns = crypto_rule.get("patterns", [])
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def detect_hardcoded_secrets(text: str, policy: Dict[str, Any]) -> bool:
    """Detect hardcoded secrets in code."""
    rules_dict = policy.get("detection_rules", {})
    rules = rules_dict.get("rule_categories", {}).get("code_security", {}).get("rules", [])
    secrets_rule = next((r for r in rules if r["name"] == "hardcoded_secrets"), None)

    if not secrets_rule or not secrets_rule.get("enabled", False):
        return False

    patterns = secrets_rule.get("patterns", [])
    for pattern in patterns:
        if re.search(pattern, text):
            return True
    return False


def load_detection_rules(rules_path: Optional[str] = None) -> Dict[str, Any]:
    """Load detection rules from JSON file."""
    if rules_path is None:
        # Default path relative to this script
        script_dir = Path(__file__).parent
        rules_path = script_dir / "detection_rules.json"

    rules_file = Path(rules_path)
    if not rules_file.exists():
        logger.warning(f"Detection rules file not found: {rules_path}")
        return {}

    try:
        with open(rules_file, 'r', encoding='utf-8') as f:
            rules = json.load(f)
        logger.info(f"Loaded detection rules from {rules_path}")
        return rules
    except Exception as e:
        logger.error(f"Failed to load detection rules: {e}")
        return {}


def run_extended_detection(text: str, policy: Dict[str, Any], phase: str) -> Dict[str, Any]:
    """Run all extended detection rules based on phase."""
    detections = {
        "total": 0,
        "by_category": {},
        "details": []
    }

    # Get detection rules from policy
    detection_rules = policy.get("detection_rules", {})

    if not detection_rules:
        # Try to load from file if not in policy
        detection_rules = load_detection_rules()
        if not detection_rules:
            return detections

    # AI Model Security
    rule_categories = detection_rules.get("rule_categories", {})
    if "ai_model" in rule_categories:
        category_results = []
        for rule in rule_categories["ai_model"]["rules"]:
            if phase not in rule.get("phase", []) or not rule.get("enabled", False):
                continue

            if rule["name"] == "llm_prompt_injection":
                result = detect_llm_prompt_injection(text, {"detection_rules": detection_rules})
            elif rule["name"] == "llm_indirect_prompt_leak":
                result = detect_llm_indirect_prompt_leak(text, {"detection_rules": detection_rules})
            else:
                continue

            if result.get("detected", False):
                category_results.append(result)
                detections["details"].append({
                    "category": "ai_model",
                    "rule": rule["name"],
                    "severity": result.get("severity", "medium"),
                    "matches": result.get("matches", [])
                })
                detections["total"] += 1

        if category_results:
            detections["by_category"]["ai_model"] = len(category_results)

    # Web Security
    if "web_security" in rule_categories:
        category_results = []
        for rule in rule_categories["web_security"]["rules"]:
            if phase not in rule.get("phase", []) or not rule.get("enabled", False):
                continue

            detected = False
            if rule["name"] == "ssti_detection":
                detected = detect_ssti(text, {"detection_rules": detection_rules})
            elif rule["name"] == "log4j_detection":
                detected = detect_log4j(text, {"detection_rules": detection_rules})
            elif rule["name"] == "command_injection_basic":
                result = detect_command_injection(text, {"detection_rules": detection_rules})
                detected = result.get("detected", False)

            if detected:
                category_results.append(rule["name"])
                detections["details"].append({
                    "category": "web_security",
                    "rule": rule["name"],
                    "severity": rule.get("severity", "medium")
                })
                detections["total"] += 1

        if category_results:
            detections["by_category"]["web_security"] = len(category_results)

    # Data Leak
    if "data_leak" in rule_categories:
        category_results = []
        for rule in rule_categories["data_leak"]["rules"]:
            if phase not in rule.get("phase", []) or not rule.get("enabled", False):
                continue

            detected = False
            if rule["name"] == "ssh_private_key":
                detected = detect_ssh_private_key(text, {"detection_rules": detection_rules})
            elif rule["name"] == "aws_credentials":
                detected = detect_aws_credentials(text, {"detection_rules": detection_rules})
            elif rule["name"] == "github_token":
                detected = detect_github_token(text, {"detection_rules": detection_rules})
            elif rule["name"] == "slack_token":
                detected = detect_slack_token(text, {"detection_rules": detection_rules})

            if detected:
                category_results.append(rule["name"])
                detections["details"].append({
                    "category": "data_leak",
                    "rule": rule["name"],
                    "severity": rule.get("severity", "high")
                })
                detections["total"] += 1

        if category_results:
            detections["by_category"]["data_leak"] = len(category_results)

    # Code Security
    if "code_security" in rule_categories:
        category_results = []
        for rule in rule_categories["code_security"]["rules"]:
            if phase not in rule.get("phase", []) or not rule.get("enabled", False):
                continue

            detected = False
            if rule["name"] == "weak_crypto":
                detected = detect_weak_crypto(text, {"detection_rules": detection_rules})
            elif rule["name"] == "hardcoded_secrets":
                detected = detect_hardcoded_secrets(text, {"detection_rules": detection_rules})

            if detected:
                category_results.append(rule["name"])
                detections["details"].append({
                    "category": "code_security",
                    "rule": rule["name"],
                    "severity": rule.get("severity", "medium")
                })
                detections["total"] += 1

        if category_results:
            detections["by_category"]["code_security"] = len(category_results)

    return detections


# ============================================================================
# Predictive Awareness System
# ============================================================================

def predict_execution_complexity(user_prompt: str, planned_actions: List[str]) -> Dict[str, Any]:
    """Predict execution complexity and potential resource issues."""
    predictions = {
        "complexity_level": "low",
        "risk_factors": [],
        "estimated_duration_seconds": 1.0,
        "resource_risks": {
            "cpu": "low",
            "memory": "low",
            "disk": "low",
            "network": "low"
        }
    }

    prompt_lower = user_prompt.lower()
    complexity_score = 0

    # Check for large-scale operations
    large_scale_patterns = [
        ("all files", 3),
        ("recursive", 2),
        ("entire directory", 3),
        ("every file", 3),
        ("bulk", 2),
        ("batch", 2),
        ("multiple files", 2),
        ("each and every", 3),
        ("whole project", 3),
        ("complete codebase", 3),
    ]

    for pattern, score in large_scale_patterns:
        if pattern in prompt_lower:
            complexity_score += score
            predictions["risk_factors"].append(f"large_scale:{pattern}")

    # Check for nested/recursive operations
    nested_patterns = [
        ("nested", 2),
        ("recursive", 2),
        ("deep", 1),
        ("tree", 1),
        ("hierarchy", 1),
        ("multiple layers", 2),
    ]

    for pattern, score in nested_patterns:
        if pattern in prompt_lower:
            complexity_score += score
            predictions["risk_factors"].append(f"nested:{pattern}")

    # Check for iteration/loop patterns
    iteration_patterns = [
        ("for each", 2),
        ("iterate", 2),
        ("loop through", 2),
        ("repeat", 2),
        ("multiple times", 2),
        ("again and again", 3),
    ]

    for pattern, score in iteration_patterns:
        if pattern in prompt_lower:
            complexity_score += score
            predictions["risk_factors"].append(f"iteration:{pattern}")

    # Check for heavy computation
    heavy_compute_patterns = [
        ("machine learning", 3),
        ("train model", 3),
        ("neural network", 2),
        ("deep learning", 2),
        ("data processing", 2),
        ("analyze all", 2),
        ("calculate", 1),
        ("compute", 1),
    ]

    for pattern, score in heavy_compute_patterns:
        if pattern in prompt_lower:
            complexity_score += score
            predictions["risk_factors"].append(f"heavy_compute:{pattern}")

    # Check planned actions
    high_complexity_actions = {
        "file_write": 1,
        "file_read": 1,
        "directory_scan": 3,
        "command_execute": 2,
        "network_request": 2,
        "database_query": 2,
    }

    for action in planned_actions:
        if action in high_complexity_actions:
            complexity_score += high_complexity_actions[action]
            predictions["risk_factors"].append(f"action:{action}")

    # Determine complexity level
    if complexity_score >= 10:
        predictions["complexity_level"] = "critical"
        predictions["estimated_duration_seconds"] = 60.0
    elif complexity_score >= 7:
        predictions["complexity_level"] = "high"
        predictions["estimated_duration_seconds"] = 30.0
    elif complexity_score >= 4:
        predictions["complexity_level"] = "medium"
        predictions["estimated_duration_seconds"] = 10.0
    else:
        predictions["complexity_level"] = "low"
        predictions["estimated_duration_seconds"] = 1.0

    # Predict resource risks
    if "large_scale" in str(predictions["risk_factors"]):
        predictions["resource_risks"]["disk"] = "medium"
        predictions["resource_risks"]["memory"] = "medium"

    if "heavy_compute" in str(predictions["risk_factors"]):
        predictions["resource_risks"]["cpu"] = "high"
        predictions["resource_risks"]["memory"] = "high"

    if any("network" in str(risk) or "request" in str(risk) for risk in predictions["risk_factors"]):
        predictions["resource_risks"]["network"] = "medium"

    return predictions


def predict_output_scale(user_prompt: str) -> Dict[str, Any]:
    """Predict the scale of output generation."""
    predictions = {
        "estimated_size": "small",
        "size_category": "bytes",
        "risk_factors": [],
        "concerns": []
    }

    prompt_lower = user_prompt.lower()
    size_score = 0

    # Check for requests for long content
    long_content_patterns = [
        ("detailed", 1),
        ("comprehensive", 2),
        ("exhaustive", 3),
        ("complete guide", 2),
        ("full documentation", 3),
        ("extensive", 2),
        ("in depth", 2),
        ("thorough", 2),
        ("step by step", 1),
        ("every detail", 3),
    ]

    for pattern, score in long_content_patterns:
        if pattern in prompt_lower:
            size_score += score
            predictions["risk_factors"].append(f"length:{pattern}")

    # Check for multiple outputs
    multiple_output_patterns = [
        ("multiple", 2),
        ("several", 2),
        ("various", 2),
        ("different versions", 3),
        ("all options", 3),
        ("list all", 2),
        ("each option", 2),
        ("generate 10", 3),
        ("create 5", 3),
    ]

    for pattern, score in multiple_output_patterns:
        if pattern in prompt_lower:
            size_score += score
            predictions["risk_factors"].append(f"multiplicity:{pattern}")

    # Check for code generation
    code_generation_patterns = [
        ("write code", 2),
        ("generate code", 2),
        ("create function", 2),
        ("implement", 2),
        ("write a script", 3),
        ("full program", 3),
        ("complete application", 3),
    ]

    for pattern, score in code_generation_patterns:
        if pattern in prompt_lower:
            size_score += score
            predictions["risk_factors"].append(f"code_generation:{pattern}")

    # Check for data generation
    data_generation_patterns = [
        ("generate data", 3),
        ("create dummy data", 2),
        ("produce sample", 2),
        ("make up", 1),
        ("invent", 1),
        ("fabricate", 1),
    ]

    for pattern, score in data_generation_patterns:
        if pattern in prompt_lower:
            size_score += score
            predictions["risk_factors"].append(f"data_generation:{pattern}")

    # Determine size category
    if size_score >= 10:
        predictions["estimated_size"] = "very_large"
        predictions["size_category"] = "MB"
        predictions["concerns"].append("May generate excessive output")
    elif size_score >= 7:
        predictions["estimated_size"] = "large"
        predictions["size_category"] = "KB"
        predictions["concerns"].append("May generate lengthy output")
    elif size_score >= 4:
        predictions["estimated_size"] = "medium"
        predictions["size_category"] = "KB"
    else:
        predictions["estimated_size"] = "small"
        predictions["size_category"] = "bytes"

    return predictions


def predict_security_boundaries(user_prompt: str, planned_actions: List[str]) -> Dict[str, Any]:
    """Predict if the request approaches security boundaries."""
    predictions = {
        "boundary_risk": "low",
        "risk_factors": [],
        "near_boundaries": [],
        "recommendations": []
    }

    prompt_lower = user_prompt.lower()

    # Check for system-level operations
    system_operations = [
        ("system configuration", "critical"),
        ("environment variables", "high"),
        ("system files", "high"),
        ("admin", "medium"),
        ("root", "high"),
        ("privilege", "high"),
        ("permission", "medium"),
    ]

    for pattern, severity in system_operations:
        if pattern in prompt_lower:
            predictions["risk_factors"].append(f"system_access:{pattern}:{severity}")
            predictions["near_boundaries"].append(pattern)

    # Check for network operations
    network_operations = [
        ("external api", "medium"),
        ("http request", "medium"),
        ("connect to", "medium"),
        ("download", "high"),
        ("upload", "high"),
        ("remote server", "high"),
    ]

    for pattern, severity in network_operations:
        if pattern in prompt_lower:
            predictions["risk_factors"].append(f"network:{pattern}:{severity}")
            predictions["near_boundaries"].append(pattern)

    # Check for file system operations near sensitive areas
    sensitive_paths = [
        ("etc/passwd", "critical"),
        ("etc/shadow", "critical"),
        ("home", "medium"),
        ("user data", "medium"),
        ("config", "medium"),
        ("secret", "high"),
        ("credential", "high"),
        ("key", "high"),
    ]

    for pattern, severity in sensitive_paths:
        if pattern in prompt_lower:
            predictions["risk_factors"].append(f"sensitive_path:{pattern}:{severity}")
            predictions["near_boundaries"].append(pattern)

    # Check planned actions
    sensitive_actions = {
        "file_delete": "high",
        "file_modify": "medium",
        "command_execute": "high",
        "network_request": "medium",
        "database_write": "high",
    }

    for action in planned_actions:
        if action in sensitive_actions:
            severity = sensitive_actions[action]
            predictions["risk_factors"].append(f"action:{action}:{severity}")
            predictions["near_boundaries"].append(action)

    # Determine overall boundary risk
    critical_count = sum(1 for r in predictions["risk_factors"] if ":critical" in r)
    high_count = sum(1 for r in predictions["risk_factors"] if ":high" in r)

    if critical_count > 0:
        predictions["boundary_risk"] = "critical"
        predictions["recommendations"].append("Block: touches critical security boundaries")
    elif high_count >= 2:
        predictions["boundary_risk"] = "high"
        predictions["recommendations"].append("Strong caution: multiple high-risk boundaries")
    elif high_count == 1:
        predictions["boundary_risk"] = "medium"
        predictions["recommendations"].append("Caution: approaches high-risk boundary")
    else:
        predictions["boundary_risk"] = "low"

    return predictions


def predict_contextual_risk(user_prompt: str, conversation_history: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Predict contextual risks from conversation patterns."""
    predictions = {
        "contextual_risk": "low",
        "risk_patterns": [],
        "concerns": [],
        "attack_indicators": []
    }

    prompt_lower = user_prompt.lower()

    # Check for probing patterns
    probing_patterns = [
        ("what can you do", "capability_discovery"),
        ("what are your limits", "boundary_testing"),
        ("what happens if", "boundary_testing"),
        ("can you", "capability_discovery"),
        ("are you allowed to", "boundary_testing"),
        ("what happens when i", "boundary_testing"),
    ]

    for pattern, indicator in probing_patterns:
        if pattern in prompt_lower:
            predictions["risk_patterns"].append(f"probing:{indicator}")
            predictions["attack_indicators"].append(indicator)

    # Check for information gathering
    info_gathering_patterns = [
        ("how does", "info_gathering"),
        ("tell me about", "info_gathering"),
        ("explain the system", "info_gathering"),
        ("what information do you have", "info_gathering"),
        ("show me your", "info_gathering"),
        ("list all", "info_gathering"),
    ]

    for pattern, indicator in info_gathering_patterns:
        if pattern in prompt_lower:
            predictions["risk_patterns"].append(f"info_gathering:{indicator}")
            predictions["attack_indicators"].append("information_disclosure")

    # Check for context building (potential multi-turn attack)
    context_building_patterns = [
        ("remember that", "context_building"),
        ("keep in mind", "context_building"),
        ("for later", "context_building"),
        ("next time", "context_building"),
        ("in the future", "context_building"),
    ]

    for pattern, indicator in context_building_patterns:
        if pattern in prompt_lower:
            predictions["risk_patterns"].append(f"context_building:{indicator}")
            predictions["attack_indicators"].append("multi_turn_preparation")

    # Check for persistence attempts
    persistence_patterns = [
        ("save", "persistence"),
        ("store", "persistence"),
        ("write to file", "persistence"),
        ("keep for later", "persistence"),
        ("remember between sessions", "persistence"),
    ]

    for pattern, indicator in persistence_patterns:
        if pattern in prompt_lower:
            predictions["risk_patterns"].append(f"persistence:{indicator}")
            predictions["attack_indicators"].append("state_manipulation")

    # Analyze conversation history if available
    if conversation_history:
        recent_topics = [turn.get("topics", []) for turn in conversation_history[-5:]]
        flat_topics = [topic for topics in recent_topics for topic in topics]

        # Check for topic drift or escalation
        if len(flat_topics) > 5:
            unique_topics = len(set(flat_topics))
            if unique_topics > len(flat_topics) * 0.7:
                predictions["risk_patterns"].append("topic_hopping:rapid_topic_changes")
                predictions["attack_indicators"].append("pattern_obsfuscation")

    # Determine overall contextual risk
    unique_indicators = len(set(predictions["attack_indicators"]))
    if unique_indicators >= 3:
        predictions["contextual_risk"] = "high"
        predictions["concerns"].append("Multiple attack indicators detected")
    elif unique_indicators >= 2:
        predictions["contextual_risk"] = "medium"
        predictions["concerns"].append("Multiple suspicious patterns")
    elif unique_indicators == 1:
        predictions["contextual_risk"] = "low"
        predictions["concerns"].append("Single suspicious pattern")
    else:
        predictions["contextual_risk"] = "low"

    return predictions


def run_predictive_analysis(
    user_prompt: str,
    planned_actions: List[str],
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    policy: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Run complete predictive analysis on the prompt."""
    policy = policy or {}

    # Get predictive configuration from policy
    predictive_config = policy.get("predictive_analysis", {})
    if not predictive_config.get("enabled", False):
        return {
            "enabled": False,
            "message": "Predictive analysis is disabled"
        }

    results = {
        "enabled": True,
        "overall_risk": "low",
        "predictions": {},
        "recommendations": [],
        "requires_human_review": False
    }

    # Run all predictive analyses
    results["predictions"]["complexity"] = predict_execution_complexity(user_prompt, planned_actions)
    results["predictions"]["output_scale"] = predict_output_scale(user_prompt)
    results["predictions"]["security_boundaries"] = predict_security_boundaries(user_prompt, planned_actions)
    results["predictions"]["contextual_risk"] = predict_contextual_risk(user_prompt, conversation_history)

    # Aggregate overall risk
    risk_scores = []

    # Complexity risk
    complexity_level = results["predictions"]["complexity"]["complexity_level"]
    if complexity_level == "critical":
        risk_scores.append(3)
    elif complexity_level == "high":
        risk_scores.append(2)
    elif complexity_level == "medium":
        risk_scores.append(1)

    # Boundary risk
    boundary_risk = results["predictions"]["security_boundaries"]["boundary_risk"]
    if boundary_risk == "critical":
        risk_scores.append(3)
    elif boundary_risk == "high":
        risk_scores.append(2)
    elif boundary_risk == "medium":
        risk_scores.append(1)

    # Contextual risk
    contextual_risk = results["predictions"]["contextual_risk"]["contextual_risk"]
    if contextual_risk == "high":
        risk_scores.append(2)
    elif contextual_risk == "medium":
        risk_scores.append(1)

    # Output scale risk
    output_size = results["predictions"]["output_scale"]["estimated_size"]
    if output_size in ["very_large", "large"]:
        risk_scores.append(1)

    # Determine overall risk
    total_risk_score = sum(risk_scores)
    if total_risk_score >= 6:
        results["overall_risk"] = "critical"
        results["requires_human_review"] = True
        results["recommendations"].append("CRITICAL: High probability of issues - human review required")
    elif total_risk_score >= 4:
        results["overall_risk"] = "high"
        results["requires_human_review"] = True
        results["recommendations"].append("HIGH: Significant risk detected - consider human review")
    elif total_risk_score >= 2:
        results["overall_risk"] = "medium"
        results["recommendations"].append("MEDIUM: Some risks detected - monitor execution")
    else:
        results["overall_risk"] = "low"

    # Add specific recommendations based on predictions
    complexity_risks = results["predictions"]["complexity"]["risk_factors"]
    if len(complexity_risks) >= 3:
        results["recommendations"].append("Set resource limits and timeout")

    boundary_recommendations = results["predictions"]["security_boundaries"]["recommendations"]
    results["recommendations"].extend(boundary_recommendations)

    output_concerns = results["predictions"]["output_scale"]["concerns"]
    if output_concerns:
        results["recommendations"].append("Monitor output size and truncate if necessary")

    contextual_concerns = results["predictions"]["contextual_risk"]["concerns"]
    results["recommendations"].extend(contextual_concerns)

    return results


# ============================================================================
# Phase 2: Behavioral Analysis
# ============================================================================

class ConversationTracker:
    """Track conversation history for multi-turn attack detection."""

    def __init__(self, max_history: int = 10):
        self.history = []
        self.max_history = max_history
        self.topic_history = []

    def add_turn(self, user_prompt: str, sensitive_topics: List[str]):
        """Add a conversation turn."""
        turn = {
            "prompt": user_prompt,
            "topics": sensitive_topics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        self.history.append(turn)
        self.topic_history.extend(sensitive_topics)

        # Keep only recent history
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        if len(self.topic_history) > self.max_history * 3:
            self.topic_history = self.topic_history[-self.max_history * 3:]

    def analyze_topic_progression(self) -> Dict[str, Any]:
        """Analyze if conversation is converging toward sensitive topics."""
        if len(self.history) < 2:
            return {"converging": False, "confidence": 0.0}

        # Calculate topic frequency in recent turns
        from collections import Counter
        recent_topics = self.topic_history[-10:]
        topic_counts = Counter(recent_topics)

        if not topic_counts:
            return {"converging": False, "confidence": 0.0}

        # Check if sensitive topics are increasing
        most_common = topic_counts.most_common(3)
        sensitive_count = sum(count for topic, count in most_common if topic in ["token", "password", "secret", "key"])

        # Calculate trend
        window_size = 5
        if len(self.topic_history) > window_size:
            old_window = self.topic_history[-(window_size * 2):-window_size]
            new_window = self.topic_history[-window_size:]

            old_sensitive = sum(1 for t in old_window if t in ["token", "password", "secret"])
            new_sensitive = sum(1 for t in new_window if t in ["token", "password", "secret"])

            if new_sensitive > old_sensitive:
                return {
                    "converging": True,
                    "confidence": min(0.9, 0.5 + (new_sensitive - old_sensitive) * 0.2),
                    "trend": "increasing"
                }

        return {
            "converging": sensitive_count >= 3,
            "confidence": min(1.0, sensitive_count * 0.2),
            "top_topics": most_common
        }


def detect_multi_turn_attack(user_prompt: str, tracker: ConversationTracker, policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect multi-turn conversation attacks."""
    behavioral_config = policy.get("behavioral_analysis", {})
    multi_turn_config = behavioral_config.get("multi_turn_attack", {})

    if not multi_turn_config.get("enabled", False):
        return {"detected": False}

    # Extract sensitive topics from current prompt
    sensitive_topics = multi_turn_config.get("sensitive_topics", [])
    current_topics = [topic for topic in sensitive_topics if topic.lower() in user_prompt.lower()]

    # Add to tracker
    tracker.add_turn(user_prompt, current_topics)

    # Analyze progression
    progression = tracker.analyze_topic_progression()

    return {
        "detected": progression["converging"],
        "confidence": progression["confidence"],
        "top_topics": progression.get("top_topics", [])[:3]
    }


def detect_rapid_file_access(events: List[Dict[str, Any]], policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect rapid file access patterns."""
    behavioral_config = policy.get("behavioral_analysis", {})
    rapid_config = behavioral_config.get("rapid_file_access", {})

    if not rapid_config.get("enabled", False):
        return {"detected": False}

    threshold = rapid_config.get("threshold", 10)
    time_window = rapid_config.get("time_window_seconds", 60)
    action_types = set(rapid_config.get("action_types", ["read_file", "write_file", "delete_file"]))

    # Filter file access events
    file_access_events = []
    for event in events:
        if event.get("type") in action_types:
            file_access_events.append(event)

    if len(file_access_events) < threshold:
        return {"detected": False, "event_count": len(file_access_events)}

    # Check time window
    if len(file_access_events) < 2:
        return {"detected": False, "event_count": len(file_access_events)}

    # Calculate time span
    try:
        first_time = datetime.fromisoformat(file_access_events[0].get("timestamp", ""))
        last_time = datetime.fromisoformat(file_access_events[-1].get("timestamp", ""))
        time_span = (last_time - first_time).total_seconds()
    except:
        return {"detected": False, "event_count": len(file_access_events)}

    # Check if threshold exceeded within time window
    if len(file_access_events) >= threshold and time_span <= time_window:
        return {
            "detected": True,
            "event_count": len(file_access_events),
            "time_span_seconds": time_span,
            "severity": "high" if len(file_access_events) >= threshold * 2 else "medium"
        }

    return {"detected": False, "event_count": len(file_access_events)}


def detect_bulk_operations(events: List[Dict[str, Any]], policy: Dict[str, Any]) -> Dict[str, Any]:
    """Detect bulk operations that may indicate data exfiltration."""
    behavioral_config = policy.get("behavioral_analysis", {})
    bulk_config = behavioral_config.get("bulk_operations", {})

    if not bulk_config.get("enabled", False):
        return {"detected": False}

    thresholds = bulk_config.get("thresholds", {})

    # Count operations by type
    operation_counts = {}
    for event in events:
        op_type = event.get("type", "")
        operation_counts[op_type] = operation_counts.get(op_type, 0) + 1

    # Check thresholds
    detected_ops = []
    for op_type, count in operation_counts.items():
        threshold = thresholds.get(op_type, float('inf'))
        if count >= threshold:
            detected_ops.append({"operation": op_type, "count": count, "threshold": threshold})

    if detected_ops:
        return {
            "detected": True,
            "operations": detected_ops,
            "severity": "high" if len(detected_ops) > 1 else "medium"
        }

    return {"detected": False, "operation_counts": operation_counts}


def analyze_semantic_intent(user_prompt: str, context: Dict[str, Any], policy: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze semantic intent of the user request."""
    semantic_config = policy.get("semantic_analysis", {})

    if not semantic_config.get("enabled", False):
        return {"intent": "neutral", "confidence": 0.5}

    prompt_lower = user_prompt.lower()

    # Check for malicious indicators
    malicious_indicators = semantic_config.get("malicious_indicators", [])
    has_malicious = any(ind in prompt_lower for ind in malicious_indicators)

    # Check for legitimate contexts
    legitimate_contexts = semantic_config.get("legitimate_contexts", [])
    has_legitimate = any(ctx in prompt_lower for ctx in legitimate_contexts)

    # Determine intent
    intent_keywords = semantic_config.get("intent_keywords", {})

    # Calculate intent scores
    explanation_score = sum(1 for kw in intent_keywords.get("explanation", []) if kw in prompt_lower)
    exploitation_score = sum(1 for kw in intent_keywords.get("exploitation", []) if kw in prompt_lower)
    verification_score = sum(1 for kw in intent_keywords.get("verification", []) if kw in prompt_lower)

    max_score = max(explanation_score, exploitation_score, verification_score)
    total_keywords = explanation_score + exploitation_score + verification_score

    # Determine intent
    if has_malicious and exploitation_score > 0:
        intent = "malicious"
        confidence = min(1.0, 0.7 + exploitation_score * 0.1)
    elif has_legitimate:
        intent = "legitimate"
        confidence = 0.8
    elif exploitation_score >= 2:
        intent = "suspicious"
        confidence = min(1.0, 0.6 + exploitation_score * 0.15)
    elif explanation_score > 0 and verification_score > 0:
        intent = "verification"
        confidence = 0.7
    elif total_keywords == 0:
        intent = "neutral"
        confidence = 0.3
    else:
        intent = "uncertain"
        confidence = 0.5

    return {
        "intent": intent,
        "confidence": confidence,
        "explanation_score": explanation_score,
        "exploitation_score": exploitation_score,
        "verification_score": verification_score,
        "has_malicious_indicator": has_malicious,
        "has_legitimate_context": has_legitimate
    }


def calculate_risk_score(
    attack_detected: bool,
    critical_action: bool,
    high_risk_action: bool,
    sensitive_data: bool,
    anomaly: bool,
    bulk_op: bool,
    rapid_access: bool,
    multi_turn: bool,
    policy: Dict[str, Any]
) -> Dict[str, Any]:
    """Calculate composite risk score."""
    risk_config = policy.get("risk_scoring", {})

    if not risk_config.get("enabled", False):
        return {"score": 0.0, "decision": "allow"}

    weights = risk_config.get("weights", {})
    thresholds = risk_config.get("thresholds", {})

    score = 0.0

    if attack_detected:
        score += weights.get("attack_pattern_hit", 10.0)
    if critical_action:
        score += weights.get("critical_action", 8.0)
    if high_risk_action:
        score += weights.get("high_risk_action", 5.0)
    if sensitive_data:
        score += weights.get("sensitive_data_detected", 3.0)
    if anomaly:
        score += weights.get("anomaly_detected", 4.0)
    if bulk_op:
        score += weights.get("bulk_operation", 3.0)
    if rapid_access:
        score += weights.get("rapid_access", 2.0)
    if multi_turn:
        score += weights.get("multi_turn_convergence", 6.0)

    # Determine decision
    block_threshold = thresholds.get("block", 15.0)
    downgrade_threshold = thresholds.get("downgrade", 8.0)

    if score >= block_threshold:
        decision = "block"
    elif score >= downgrade_threshold:
        decision = "downgrade"
    else:
        decision = "allow"

    return {
        "score": score,
        "decision": decision,
        "block_threshold": block_threshold,
        "downgrade_threshold": downgrade_threshold
    }


def is_refusal_response(text: str) -> bool:
    text_low = text.lower()
    refusal_markers = [
        "i can't help",
        "i cannot help",
        "can't assist",
        "cannot assist",
        "won't help",
        "cannot provide",
        "unable to help",
        "unable to assist"
    ]
    return any(m in text_low for m in refusal_markers)


def normalize_state(state: str) -> str:
    if state in {"normal", "sensitive", "highly_sensitive"}:
        return state
    return "normal"


def state_rank(state: str) -> int:
    return {"normal": 0, "sensitive": 1, "highly_sensitive": 2}[normalize_state(state)]


def max_state(a: str, b: str) -> str:
    return a if state_rank(a) >= state_rank(b) else b


def event_risk_level(decision: str) -> str:
    mapping = {
        "allow": "low",
        "continue": "low",
        "downgrade": "medium",
        "block": "high",
        "stop": "high",
        "error": "critical",
    }
    return mapping.get(decision, "low")


def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def excerpt(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def scan_for_leaks(text: str, patterns: List[str]) -> List[Dict[str, Any]]:
    """
    Scan text for all pattern matches that represent potential leaks.

    Args:
        text: The text to scan
        patterns: List of regex pattern strings

    Returns:
        List of leak dictionaries with pattern, start, end, match, and replacement
    """
    if not text or not patterns:
        return []

    leaks = []

    for pattern_str in patterns:
        try:
            pattern = re.compile(pattern_str)
            for match in pattern.finditer(text):
                leaks.append({
                    "pattern": pattern_str,
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": "[REDACTED]"
                })
        except re.error:
            # Invalid regex pattern, skip it
            continue

    return leaks


def apply_redaction(text: str, leaks: List[Dict[str, Any]]) -> str:
    """
    Apply redaction based on leak list.

    Processes leaks from end to start to avoid position offset issues.

    Args:
        text: Original text
        leaks: List of leak dictionaries (from scan_for_leaks)

    Returns:
        Redacted text
    """
    if not leaks:
        return text

    # Sort by position in reverse order (end to start) to avoid offset issues
    sorted_leaks = sorted(leaks, key=lambda x: x["end"], reverse=True)

    result = text
    for leak in sorted_leaks:
        start = leak["start"]
        end = leak["end"]
        replacement = leak.get("replacement", "[REDACTED]")

        # Apply replacement
        result = result[:start] + replacement + result[end:]

    return result


def redact_text(text: str, replacements: Dict[str, str]) -> Dict[str, Any]:
    """
    Redact sensitive text using specified replacement patterns.

    This function scans the text for all patterns in the replacements dictionary
    and applies redaction using [REDACTED_TYPE] format.

    Args:
        text: Original text
        replacements: Dictionary of {type: regex_pattern}

    Returns:
        {
            "text": Redacted text,
            "redaction_applied": bool,
            "summary": [{"type": leak_type, "count": count}, ...]
        }
    """
    if not text or not replacements:
        return {
            "text": text,
            "redaction_applied": False,
            "summary": []
        }

    # Scan for all leaks using the patterns
    all_leaks = []
    for leak_type, pattern_str in replacements.items():
        try:
            pattern = re.compile(pattern_str)
            for match in pattern.finditer(text):
                all_leaks.append({
                    "pattern": leak_type,
                    "start": match.start(),
                    "end": match.end(),
                    "match": match.group(0),
                    "replacement": f"[REDACTED_{leak_type.upper()}]"
                })
        except re.error:
            # Invalid regex pattern, skip it
            continue

    # Apply redaction if any leaks were found
    if all_leaks:
        redacted_text = apply_redaction(text, all_leaks)
        redaction_applied = True

        # Generate summary
        summary = {}
        for leak in all_leaks:
            leak_type = leak["pattern"]
            summary[leak_type] = summary.get(leak_type, 0) + 1

        summary_list = [{"type": k, "count": v} for k, v in summary.items()]
    else:
        redacted_text = text
        redaction_applied = False
        summary_list = []

    return {
        "text": redacted_text,
        "redaction_applied": redaction_applied,
        "summary": summary_list
    }


def build_retention_snapshot(policy: Dict[str, Any], final_action: str, user_prompt: str, safe_response: str) -> Dict[str, Any]:
    user_redacted = redact_text(user_prompt, policy.get("redaction_replacements", {}))["text"]
    resp_redacted = redact_text(safe_response, policy.get("redaction_replacements", {}))["text"]
    base = {
        "user_prompt_hash": hash_text(user_prompt),
        "safe_response_hash": hash_text(safe_response),
        "user_prompt_length": len(user_prompt),
        "safe_response_length": len(safe_response),
    }
    if final_action == "allow":
        base["retention_level"] = "summary_only"
        base["user_prompt_preview"] = excerpt(user_redacted, 120)
        base["safe_response_preview"] = excerpt(resp_redacted, 120)
    elif final_action == "downgrade":
        base["retention_level"] = "evidence_compact"
        base["user_prompt_preview"] = excerpt(user_redacted, 300)
        base["safe_response_preview"] = excerpt(resp_redacted, 300)
    else:
        base["retention_level"] = "evidence_full_redacted"
        base["user_prompt_preview"] = excerpt(user_redacted, 800)
        base["safe_response_preview"] = excerpt(resp_redacted, 800)
    return base


def build_unified_log(
    trace_id: str,
    session_id: str,
    turn_id: str,
    policy_profile: str,
    project_root: str,
    duration_ms: float,
    user_prompt: str,
    planned_actions: List[str],
    intent_tags: List[str],
    runtime_events: List[Dict[str, Any]],
    sources: List[Dict[str, Any]],
    candidate_response: str,
    preflight: Dict[str, Any],
    runtime: Dict[str, Any],
    output: Dict[str, Any],
    final_action: str,
    sensitivity_inference: Dict[str, Any],
    retention: Dict[str, Any],
) -> Dict[str, Any]:
    """Build a unified single-file log record for the entire query lifecycle."""

    # Extract decision codes and rules
    decision_reason_codes = sorted(
        set(preflight.get("decision_reason_codes", []))
        | set(runtime.get("decision_reason_codes", []))
        | set(output.get("decision_reason_codes", []))
    )
    matched_rules = sorted(
        set(preflight.get("matched_rules", []))
        | set(runtime.get("matched_rules", []))
        | set(output.get("matched_rules", []))
    )

    # Build residual risks
    residual_risks = []
    if output.get("leakage_detected"):
        residual_risks.append("privacy leakage risk")
    if any(a.get("source_type") in ["tool_single_source"] for a in runtime.get("trust_annotations", [])):
        residual_risks.append("single-source reliability risk")
    if runtime.get("alerts"):
        for alert in runtime["alerts"]:
            if alert.get("severity") in ["warning", "critical"]:
                residual_risks.append(f"runtime_{alert['severity']}_alert")

    # Build detected leaks for output guard
    detected_leaks = []
    if output.get("leakage_detected"):
        # This is a simplified version; in production you'd extract actual leak details
        detected_leaks.append({
            "type": "credential_or_sensitive",
            "count": len(output.get("redaction_summary", [])),
            "redacted": output.get("redaction_applied", False)
        })

    # Assemble unified log
    unified_log = {
        # ===== Meta =====
        "meta": {
            "version": "3.0",
            "ts": now_iso(),
            "session_id": session_id,
            "turn_id": turn_id,
            "trace_id": trace_id,
            "policy_profile": policy_profile,
            "project_root": project_root,
            "duration_ms": duration_ms,
        },

        # ===== Input =====
        "input": {
            "user_prompt": user_prompt,
            "planned_actions": planned_actions,
            "intent_tags": intent_tags,
            "runtime_events": runtime_events,
            "sources": sources,
            "candidate_response": candidate_response,
        },

        # ===== Preflight Stage =====
        "preflight": {
            "decision": preflight.get("preflight_decision", "unknown"),
            "sensitivity_state": preflight.get("sensitivity_state", "normal"),
            "previous_state": sensitivity_inference.get("previous_state", "normal"),
            "risk_summary": preflight.get("risk_summary", []),
            "allowed_actions": preflight.get("allowed_actions", []),
            "blocked_actions": preflight.get("blocked_actions", []),
            "verification_requirements": preflight.get("verification_requirements", []),
            "decision_reason_codes": preflight.get("decision_reason_codes", []),
            "matched_rules": preflight.get("matched_rules", []),
            "detected_attacks": preflight.get("detected_attacks", []),
            "detected_sensitive_content": preflight.get("detected_sensitive_content", []),
        },

        # ===== Runtime Stage =====
        "runtime": {
            "decision": runtime.get("runtime_decision", "unknown"),
            "events": runtime.get("runtime_events", []),
            "alerts": runtime.get("alerts", []),
            "suggested_actions": runtime.get("suggested_actions", []),
            "trust_annotations": runtime.get("trust_annotations", []),
            "decision_reason_codes": runtime.get("decision_reason_codes", []),
            "matched_rules": runtime.get("matched_rules", []),
            "behavior_analysis": {
                "rapid_file_access_detected": any("rapid" in str(a).lower() for a in runtime.get("decision_reason_codes", [])),
                "bulk_operations_detected": any("bulk" in str(a).lower() for a in runtime.get("decision_reason_codes", [])),
                "multi_turn_convergence": False,  # Would be populated if multi-turn tracking
            },
        },

        # ===== Output Guard Stage =====
        "output_guard": {
            "decision": output.get("output_decision", "unknown"),
            "leakage_detected": output.get("leakage_detected", False),
            "residual_leakage_detected": output.get("residual_leakage_detected", False),
            "redaction_applied": output.get("redaction_applied", False),
            "redaction_summary": output.get("redaction_summary", []),
            "confidence_level": output.get("confidence_level", "unknown"),
            "original_response": candidate_response,
            "safe_response": output.get("safe_response", ""),
            "decision_reason_codes": output.get("decision_reason_codes", []),
            "matched_rules": output.get("matched_rules", []),
            "detected_leaks": detected_leaks,
        },

        # ===== Final Decision =====
        "final": {
            "action": final_action,
            "reason_codes": decision_reason_codes,
            "matched_rules": matched_rules,
            "residual_risks": sorted(set(residual_risks)),
            "recommended_action": _get_recommended_action(final_action),
            "explanation": _build_explanation(preflight, runtime, output),
        },

        # ===== Audit Info =====
        "audit": {
            "checked_at": now_iso(),
            "policy_version": "3.0",
            "hooks_triggered": ["preflight", "runtime", "output_guard"],
            "early_exit": preflight.get("preflight_decision") == "block",
            "retention": retention,
        },
    }

    return unified_log


def _get_recommended_action(final_action: str) -> str:
    """Get recommended action based on final decision."""
    recommendations = {
        "allow": "Response can be delivered as-is",
        "downgrade": "Response should be delivered with uncertainty declarations",
        "block": "Response must be refused or redacted",
    }
    return recommendations.get(final_action, "Unknown action")


def _build_explanation(
    preflight: Dict[str, Any],
    runtime: Dict[str, Any],
    output: Dict[str, Any],
) -> str:
    """Build human-readable explanation of the decision."""
    explanations = []

    if preflight.get("risk_summary"):
        explanations.append(f"Preflight risks: {', '.join(preflight['risk_summary'][:2])}")

    if runtime.get("alerts"):
        alert_msgs = [a.get("message", "") for a in runtime["alerts"][:2]]
        explanations.append(f"Runtime alerts: {', '.join(alert_msgs)}")

    if output.get("leakage_detected"):
        explanations.append("Output guard detected sensitive leakage")

    return "; ".join(explanations) if explanations else "No significant risks detected"


def infer_sensitivity(prompt: str, events: List[Dict[str, Any]], previous_state: str, policy: Dict[str, Any]) -> Dict[str, Any]:
    state = normalize_state(previous_state)
    reasons: List[str] = []

    sensitive_keywords = [str(x).lower() for x in policy.get("sensitive_keywords", [])]
    sensitive_event_types = {str(x).lower() for x in policy.get("sensitive_event_types", [])}

    low_prompt = prompt.lower()
    if any(k in low_prompt for k in sensitive_keywords):
        state = max_state(state, "sensitive")
        reasons.append("prompt contains sensitive keyword")

    for e in events:
        event_type = str(e.get("type", "")).strip().lower()
        if event_type in sensitive_event_types:
            state = max_state(state, "highly_sensitive")
            reasons.append(f"runtime event {event_type} is highly sensitive")

    if not reasons:
        reasons.append("no new sensitivity signal")

    return {"sensitivity_state": state, "reasons": reasons}


def preflight_decision(
    user_prompt: str,
    planned_actions: List[str],
    intent_tags: List[str],
    sensitivity_state: str,
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    prompt_low = user_prompt.lower()
    high_risk_actions = {str(x) for x in policy.get("high_risk_actions", [])}
    explicit_phrases = [str(x).lower() for x in policy.get("explicit_disclosure_phrases", [])]
    implicit_phrases = [str(x).lower() for x in policy.get("implicit_disclosure_phrases", [])]
    explanation_phrases = [str(x).lower() for x in policy.get("explanation_leakage_phrases", [])]
    config_phrases = [str(x).lower() for x in policy.get("config_disclosure_phrases", [])]
    database_phrases = [str(x).lower() for x in policy.get("database_leak_phrases", [])]
    has_high_risk_action = any(a in high_risk_actions for a in planned_actions)

    # Early Exit Optimization: Check for high-risk patterns first
    if PERFORMANCE_AVAILABLE and early_exit_enabled:
        should_exit, exit_reason = should_early_exit(user_prompt, planned_actions, policy)
        if should_exit:
            # Return early block decision
            return {
                "preflight_decision": "block",
                "risk_summary": [exit_reason],
                "blocked_actions": ["all"],
                "verification_requirements": [],
                "decision_reason_codes": ["PF_EARLY_EXIT"],
                "matched_rules": ["early_exit_high_risk"],
                "sensitivity_state": sensitivity_state,
                "early_exit": True,
            }

    risk_summary: List[str] = []
    blocked_actions: List[str] = []
    verification_requirements: List[str] = []
    decision_reason_codes: List[str] = []
    matched_rules: List[str] = []
    decision = "allow"

    # Existing checks
    explicit_hits = get_match_hits(prompt_low, explicit_phrases)
    implicit_hits = get_match_hits(prompt_low, implicit_phrases)
    explanation_hits = get_match_hits(prompt_low, explanation_phrases)
    credential_exfil = is_credential_exfil_request(prompt_low)

    # New checks: config and database disclosure
    config_hits = get_match_hits(prompt_low, config_phrases)
    database_hits = get_match_hits(prompt_low, database_phrases)

    # New checks: sensitive content detection (PARALLEL)
    if PERFORMANCE_AVAILABLE and parallel_detection_enabled:
        # Use parallel detection for better performance
        parallel_results = parallel_detect_threadpool(
            user_prompt,
            policy,
            max_workers=4
        )
        jwt_detected = parallel_results.get("detect_jwt_token", False)
        db_connection_detected = parallel_results.get("detect_database_connection", False)
        email_detected = parallel_results.get("detect_email_addresses", False)
        ip_detected = parallel_results.get("detect_ip_addresses", False)
        cc_detected = parallel_results.get("detect_credit_card", False)
        env_var_detected = parallel_results.get("detect_environment_variables", False)
    else:
        # Fallback to serial detection
        jwt_detected = detect_jwt_token(user_prompt)
        db_connection_detected = detect_database_connection(user_prompt)
        email_detected = detect_email_addresses(user_prompt)
        ip_detected = detect_ip_addresses(user_prompt)
        cc_detected = detect_credit_card(user_prompt)
        env_var_detected = detect_environment_variables(user_prompt)

    # New checks: attack patterns
    attack_detection = detect_attack_patterns(user_prompt, policy)

    # Extended detection rules (Phase 1: Pattern Matching)
    extended_detection = run_extended_detection(user_prompt, policy, phase="preflight")
    if extended_detection.get("total", 0) > 0:
        # Process extended detection results
        for detail in extended_detection.get("details", []):
            category = detail.get("category", "unknown")
            rule = detail.get("rule", "unknown")
            severity = detail.get("severity", "medium")

            # Add to matched rules for tracking
            matched_rules.append(f"extended:{category}:{rule}")
            decision_reason_codes.append(f"PF_EXTENDED_{category.upper()}_{rule.upper()}")

            # Add to risk summary
            risk_summary.append(f"Extended detection: {rule} ({severity} severity)")

            # Determine action based on severity
            if severity == "critical":
                decision = "block"
                blocked_actions.append("all")
            elif severity == "high" and decision != "block":
                decision = "downgrade"
                blocked_actions.append(category)
            elif severity == "medium" and decision == "allow":
                verification_requirements.append(f"verify {rule} detection")

    if explicit_hits or credential_exfil:
        decision = "block"
        risk_summary.append("explicit sensitive disclosure request")
        blocked_actions.append("disclose_raw_secret")
        decision_reason_codes.append("PF_EXPLICIT_DISCLOSURE")
        matched_rules.extend(explicit_hits)
        if credential_exfil:
            risk_summary.append("credential exfiltration intent detected")
            decision_reason_codes.append("PF_CREDENTIAL_EXFIL_REQUEST")
            matched_rules.append("credential_exfil_intent")

    # Config disclosure - block or downgrade
    if config_hits:
        if any(h in ["show .env file", "display config", "show secrets"] for h in config_hits):
            decision = "block"
            risk_summary.append("explicit config disclosure request")
            decision_reason_codes.append("PF_CONFIG_DISCLOSURE")
            matched_rules.extend(config_hits)
        else:
            risk_summary.append("config disclosure risk")
            verification_requirements.append("enforce output check for config")
            decision_reason_codes.append("PF_CONFIG_DISCLOSURE_RISK")
            matched_rules.extend(config_hits)
            if decision != "block":
                decision = "downgrade"

    # Database disclosure
    if database_hits:
        risk_summary.append("database data disclosure risk")
        verification_requirements.append("enforce output guard for database")
        decision_reason_codes.append("PF_DATABASE_DISCLOSURE_RISK")
        matched_rules.extend(database_hits)
        if decision != "block":
            decision = "downgrade"

    # Attack pattern detection
    if attack_detection["detected"]:
        decision = "block"
        risk_summary.append(f"attack patterns detected: {', '.join(attack_detection['patterns'])}")
        decision_reason_codes.append(f"PF_ATTACK_{pattern.upper()}" for pattern in attack_detection["patterns"])
        matched_rules.extend(attack_detection["patterns"])

    # Phase 2: Advanced attack detection
    ssrf_detected = detect_ssrf(user_prompt, policy)
    if ssrf_detected:
        decision = "block"
        risk_summary.append("SSRF (Server-Side Request Forgery) detected")
        decision_reason_codes.append("PF_ATTACK_SSRF")
        matched_rules.append("ssrf")

    xxe_detected = detect_xxe(user_prompt, policy)
    if xxe_detected:
        decision = "block"
        risk_summary.append("XXE (XML External Entity) injection detected")
        decision_reason_codes.append("PF_ATTACK_XXE")
        matched_rules.append("xxe_injection")

    template_injection = detect_template_injection(user_prompt, policy)
    if template_injection["detected"]:
        decision = "block"
        risk_summary.append(f"template injection detected: {', '.join(template_injection['types'])}")
        decision_reason_codes.append("PF_ATTACK_TEMPLATE_INJECTION")
        matched_rules.append("template_injection")

    ldap_injection_detected = detect_ldap_injection(user_prompt, policy)
    if ldap_injection_detected:
        decision = "block"
        risk_summary.append("LDAP injection detected")
        decision_reason_codes.append("PF_ATTACK_LDAP_INJECTION")
        matched_rules.append("ldap_injection")

    xpath_injection_detected = detect_xpath_injection(user_prompt, policy)
    if xpath_injection_detected:
        decision = "block"
        risk_summary.append("XPath injection detected")
        decision_reason_codes.append("PF_ATTACK_XPATH_INJECTION")
        matched_rules.append("xpath_injection")

    # New sensitive content detection
    if jwt_detected:
        risk_summary.append("JWT token detected in prompt")
        decision_reason_codes.append("PF_JWT_DETECTED")
        matched_rules.append("jwt_token")
        if decision != "block":
            decision = "downgrade"

    if db_connection_detected:
        risk_summary.append("database connection string detected")
        decision_reason_codes.append("PF_DB_CONNECTION_DETECTED")
        matched_rules.append("database_connection")
        if decision != "block":
            decision = "downgrade"

    if email_detected:
        risk_summary.append("email addresses detected (potential PII)")
        decision_reason_codes.append("PF_EMAIL_DETECTED")
        matched_rules.append("email_addresses")
        if decision != "block":
            decision = "downgrade"

    if ip_detected:
        risk_summary.append("IP addresses detected")
        decision_reason_codes.append("PF_IP_DETECTED")
        matched_rules.append("ip_addresses")

    if cc_detected:
        decision = "block"
        risk_summary.append("credit card number detected")
        decision_reason_codes.append("PF_CREDIT_CARD_DETECTED")
        matched_rules.append("credit_card")

    if env_var_detected:
        risk_summary.append("environment variable references detected")
        decision_reason_codes.append("PF_ENV_VAR_DETECTED")
        matched_rules.append("environment_variables")
        if decision != "block":
            decision = "downgrade"

    # Existing logic: implicit and explanation
    if implicit_hits or explanation_hits or "summary_from_sensitive_context" in intent_tags:
        risk_summary.append("implicit disclosure risk in explanation/summarization")
        verification_requirements.append("enforce output leakage check")
        decision_reason_codes.append("PF_IMPLICIT_DISCLOSURE_RISK")
        matched_rules.extend(implicit_hits)
        matched_rules.extend(explanation_hits)
        if decision != "block":
            decision = "downgrade"

    # Enhanced high-risk action assessment with context awareness
    if has_high_risk_action:
        # Detect environment from prompt
        detected_env = detect_environment_context(user_prompt)

        # Assess each action
        critical_actions = {str(x) for x in policy.get("critical_actions", [])}
        for action in planned_actions:
            if action in high_risk_actions:
                risk_assessment = assess_action_risk(action, detected_env, sensitivity_state, policy)

                if risk_assessment["risk_level"] == "critical":
                    decision = "block"
                    blocked_actions.append(action)
                    risk_summary.append(f"critical action '{action}' in {detected_env} environment")
                    decision_reason_codes.append(f"PF_CRITICAL_ACTION_{action.upper()}")
                elif risk_assessment["risk_level"] == "high":
                    risk_summary.append(f"high-risk action '{action}' (risk: {risk_assessment['risk_level']})")
                    decision_reason_codes.append("PF_HIGH_RISK_ACTION")
                    if decision != "block":
                        decision = "downgrade"
                else:
                    risk_summary.append(f"action '{action}' planned")
                    if decision != "block":
                        decision = "downgrade"

        verification_requirements.append("require confirmation for high-risk actions")

    if sensitivity_state in {"sensitive", "highly_sensitive"}:
        verification_requirements.append("force output guard before final response")

    # Run predictive analysis (after all security checks pass)
    predictive_analysis = run_predictive_analysis(
        user_prompt,
        planned_actions,
        conversation_history=None,  # Could be enhanced with actual history
        policy=policy
    )

    # Incorporate predictive analysis results
    if predictive_analysis.get("enabled", False):
        overall_risk = predictive_analysis.get("overall_risk", "low")

        # Add predictive risk to decision codes
        if overall_risk in ["critical", "high"]:
            decision_reason_codes.append(f"PREDICTIVE_RISK_{overall_risk.upper()}")

        # Add predictive recommendations
        for rec in predictive_analysis.get("recommendations", []):
            verification_requirements.append(f"[PREDICTIVE] {rec}")

        # Update decision based on predictive risk
        if overall_risk == "critical" and decision != "block":
            decision = "downgrade"
            risk_summary.append("predictive analysis indicates high risk of issues")

    return {
        "risk_summary": risk_summary or ["no critical preflight risk"],
        "sensitivity_state": sensitivity_state,
        "allowed_actions": ["read_only", "summarize", "explain"],
        "blocked_actions": blocked_actions,
        "verification_requirements": sorted(set(verification_requirements)),
        "decision_reason_codes": sorted(set(decision_reason_codes)),
        "matched_rules": sorted(set(matched_rules)),
        "preflight_decision": decision,
        "predictive_analysis": predictive_analysis,
    }


def runtime_decision(runtime_events: List[Dict[str, Any]], sources: List[Dict[str, Any]], policy: Dict[str, Any]) -> Dict[str, Any]:
    alerts: List[Dict[str, str]] = []
    suggested_actions: List[str] = []
    trust_annotations: List[Dict[str, str]] = []
    decision_reason_codes: List[str] = []
    matched_rules: List[str] = []

    decision = "continue"
    retry_threshold = int(policy.get("retry_threshold_downgrade", 3))
    single_source_types = {str(x) for x in policy.get("single_source_types", ["tool_single_source"])}

    retry_count = sum(1 for e in runtime_events if str(e.get("type", "")).strip().lower() == "retry")
    if retry_count >= retry_threshold:
        alerts.append({"severity": "warning", "message": "repeated retries observed"})
        suggested_actions.append("pause and inspect root cause")
        decision = "downgrade"
        decision_reason_codes.append("RT_RETRY_THRESHOLD")
        matched_rules.append(f"retry_count>={retry_threshold}")

    for s in sources:
        source_type = str(s.get("source_type", "tool_single_source"))
        confidence = str(s.get("confidence", "low"))
        trust_annotations.append(
            {
                "source_id": str(s.get("source_id", "unknown")),
                "source_type": source_type,
                "confidence": confidence,
                "reason": str(s.get("reason", "runtime source annotation")),
            }
        )

    source_types = {t["source_type"] for t in trust_annotations}
    if source_types and source_types.issubset(single_source_types):
        alerts.append({"severity": "warning", "message": "single tool source only"})
        suggested_actions.append("collect independent corroboration source")
        if decision == "continue":
            decision = "downgrade"
        decision_reason_codes.append("RT_SINGLE_SOURCE_ONLY")
        matched_rules.extend(sorted(source_types))

    if any(a.get("severity") == "critical" for a in alerts):
        decision = "stop"
        decision_reason_codes.append("RT_CRITICAL_ALERT_STOP")

    # Phase 2: Behavioral analysis
    # Detect rapid file access
    rapid_access_result = detect_rapid_file_access(runtime_events, policy)
    if rapid_access_result["detected"]:
        alerts.append({
            "severity": rapid_access_result.get("severity", "warning"),
            "message": f"rapid file access detected: {rapid_access_result.get('event_count', 0)} files in {rapid_access_result.get('time_span_seconds', 0)}s"
        })
        decision_reason_codes.append("RT_RAPID_FILE_ACCESS")
        matched_rules.append("rapid_access_pattern")
        if decision == "continue":
            decision = "downgrade"

    # Detect bulk operations
    bulk_ops_result = detect_bulk_operations(runtime_events, policy)
    if bulk_ops_result["detected"]:
        alerts.append({
            "severity": bulk_ops_result.get("severity", "warning"),
            "message": f"bulk operations detected: {bulk_ops_result.get('operations', [])}"
        })
        decision_reason_codes.append("RT_BULK_OPERATIONS")
        matched_rules.append("bulk_operation_pattern")
        if decision == "continue":
            decision = "downgrade"

    return {
        "runtime_events": runtime_events,
        "alerts": alerts,
        "suggested_actions": sorted(set(suggested_actions)),
        "trust_annotations": trust_annotations,
        "decision_reason_codes": sorted(set(decision_reason_codes)),
        "matched_rules": sorted(set(matched_rules)),
        "runtime_decision": decision,
    }


def is_contextual_leak(text: str, match: re.Match) -> bool:
    """Check if pattern match represents actual leakage vs safe mention."""
    if not contextual_matching_enabled:
        return True  # Original behavior: all matches are leaks

    matched_text = match.group(0)
    context_start = max(0, match.start() - 50)
    context_end = min(len(text), match.end() + 50)
    context = text[context_start:context_end].lower()

    # Safe contexts
    safe_contexts = [
        "example", "sample", "placeholder", "dummy", "test", "fake",
        "xxx", "yyy", "your_api_key", "your_token", "your_password",
        "demo", "illustration", "pseudo"
    ]

    # Negation contexts
    negation_contexts = [
        "not", "without", "never", "avoid", "prevent", "don't", "no",
        "don't", "no", "none"
    ]

    # Check safe context
    for safe in safe_contexts:
        if safe in context:
            return False  # Safe example

    # Check negation
    for neg in negation_contexts:
        if neg in context[:20]:
            return False  # Negated

    # Check already redacted
    if "[redacted]" in matched_text.lower():
        return False

    return True  # Actual leakage


def detect_leakage(text: str, leak_patterns: List[Pattern[str]]) -> bool:
    """Detect leakage with context awareness."""
    for pattern in leak_patterns:
        for match in pattern.finditer(text):
            if is_contextual_leak(text, match):
                return True
    return False


def build_source_disclosure(
    trust_annotations: List[Dict[str, Any]],
    policy: Dict[str, Any],
) -> Dict[str, Any]:
    title = str(policy.get("single_source_disclosure_title", "Source Disclosure (Single-Source)")).strip() or "Source Disclosure (Single-Source)"
    missing_hint = str(policy.get("single_source_missing_hint", "source metadata missing")).strip() or "source metadata missing"

    source_items: List[Dict[str, str]] = []
    for ann in trust_annotations:
        source_items.append(
            {
                "source_id": str(ann.get("source_id", "unknown")),
                "source_type": str(ann.get("source_type", "unknown")),
                "confidence": str(ann.get("confidence", "unknown")),
                "reason": str(ann.get("reason", "")),
            }
        )

    if not source_items:
        return {
            "source_items": [],
            "source_disclosure": f"\n\n{title}\n- {missing_hint}",
        }

    lines: List[str] = [f"\n\n{title}"]
    for item in source_items:
        lines.append(
            "- source_id={source_id}, source_type={source_type}, confidence={confidence}, reason={reason}".format(
                source_id=item["source_id"],
                source_type=item["source_type"],
                confidence=item["confidence"],
                reason=item["reason"] if item["reason"] else "n/a",
            )
        )

    return {
        "source_items": source_items,
        "source_disclosure": "\n".join(lines),
    }


def output_guard(
    candidate_response: str,
    sensitivity_state: str,
    trust_annotations: List[Dict[str, Any]],
    policy: Dict[str, Any],
    leak_patterns: List[Pattern[str]],
) -> Dict[str, Any]:
    leakage = detect_leakage(candidate_response, leak_patterns)
    single_source_types = {str(x) for x in policy.get("single_source_types", ["tool_single_source"])}
    has_single_tool_only = bool(trust_annotations) and all(
        str(a.get("source_type", "")) in single_source_types for a in trust_annotations
    )

    decision = "allow"
    confidence = "high"
    safe_response = candidate_response
    redaction_applied = False
    residual_leakage_detected = False
    redaction_summary: List[Dict[str, Any]] = []
    source_items: List[Dict[str, str]] = []
    source_disclosure = ""
    decision_reason_codes: List[str] = []
    matched_rules: List[str] = []

    if leakage:
        redaction_result = redact_text(candidate_response, policy.get("redaction_replacements", {}))
        safe_response = str(redaction_result["text"])
        redaction_summary = list(redaction_result["summary"])
        redaction_applied = safe_response != candidate_response
        decision_reason_codes.append("OG_LEAK_PATTERN_HIT")
        matched_rules.append("leak_patterns")
        if bool(policy.get("block_on_highly_sensitive_leak", True)) and sensitivity_state == "highly_sensitive":
            decision = "block"
            decision_reason_codes.append("OG_HIGHLY_SENSITIVE_BLOCK")
        else:
            decision = "downgrade"
            decision_reason_codes.append("OG_REDACT_AND_DOWNGRADE")
        confidence = "low"

        residual_patterns = get_cached_patterns(policy, "residual_leak_patterns")
        residual_leakage_detected = detect_leakage(safe_response, residual_patterns or leak_patterns)
        if residual_leakage_detected:
            decision = "block"
            decision_reason_codes.append("OG_RESIDUAL_LEAK_BLOCK")

    if has_single_tool_only and decision == "allow" and not is_refusal_response(safe_response):
        decision = "downgrade"
        confidence = "low"
        decision_reason_codes.append("OG_SINGLE_SOURCE_DOWNGRADE")
        matched_rules.extend(sorted(single_source_types))
        prefix = str(policy.get("force_uncertainty_prefix", "Single-source evidence only; confidence is limited: "))
        disclosure = build_source_disclosure(trust_annotations, policy)
        source_items = disclosure["source_items"]
        source_disclosure = disclosure["source_disclosure"]
        safe_response = f"{prefix}{safe_response}{source_disclosure}"

    if sensitivity_state in {"sensitive", "highly_sensitive"} and decision == "allow":
        confidence = "medium"

    return {
        "leakage_detected": leakage,
        "residual_leakage_detected": residual_leakage_detected,
        "redaction_applied": redaction_applied,
        "redaction_summary": redaction_summary,
        "decision_reason_codes": sorted(set(decision_reason_codes)),
        "matched_rules": sorted(set(matched_rules)),
        "confidence_level": confidence,
        "safe_response": safe_response,
        "source_disclosure": source_disclosure,
        "source_items": source_items,
        "output_decision": decision,
    }


def decide_final_action(preflight: Dict[str, Any], runtime: Dict[str, Any], output: Dict[str, Any]) -> str:
    if preflight["preflight_decision"] == "block" or output["output_decision"] == "block":
        return "block"
    if runtime["runtime_decision"] == "stop":
        return "block"
    if (
        preflight["preflight_decision"] == "downgrade"
        or runtime["runtime_decision"] == "downgrade"
        or output["output_decision"] == "downgrade"
    ):
        return "downgrade"
    return "allow"


def emit_event(
    events_log: Optional[Path],
    trace_id: str,
    session_id: str,
    turn_id: str,
    policy_profile: str,
    event_type: str,
    decision: str,
    reason_codes: List[str],
    matched_rules: List[str],
    extra: Dict[str, Any],
) -> None:
    event = {
        "ts": now_iso(),
        "trace_id": trace_id,
        "session_id": session_id,
        "turn_id": turn_id,
        "policy_profile": policy_profile,
        "event_type": event_type,
        "risk_level": event_risk_level(decision),
        "decision": decision,
        "reason_codes": sorted(set(reason_codes)),
        "matched_rules": sorted(set(matched_rules)),
    }
    event.update(extra)
    if events_log is not None:
        append_jsonl(events_log, event)



def resolve_project_root(payload: Dict[str, Any], input_path: Path) -> Path:
    for key in ["project_path", "project_root", "workspace_root", "repo_root"]:
        val = payload.get(key)
        if isinstance(val, str) and val.strip():
            return Path(val).expanduser().resolve()
    return Path.cwd().resolve()


def resolve_path_in_project(path_str: str, project_root: Path) -> Path:
    p = Path(path_str)
    if p.is_absolute():
        return p.resolve()
    return (project_root / p).resolve()

def sanitize_turn_id(turn_id: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9._-]+", "_", turn_id.strip())
    cleaned = cleaned.strip("._-")
    return cleaned or "unknown-turn"


def make_turn_dir_name(turn_id: str) -> str:
    return f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{sanitize_turn_id(turn_id)}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Self-guard runtime hook template")
    parser.add_argument("input_json", help="Input JSON path")
    parser.add_argument("--out", default="", help="Optional summary JSON output path")
    parser.add_argument("--events-log", default="./sentry_skill_log/self_guard_events.jsonl", help="JSONL event log path (legacy mode)")
    parser.add_argument("--state-dir", default="./sentry_skill_log/.self_guard_state", help="Session state directory")
    parser.add_argument("--log-layout", choices=["legacy", "turn_dir", "unified"], default="unified", help="Log layout strategy (unified = single file per query)")
    parser.add_argument("--turns-dir", default="./sentry_skill_log/turns", help="Per-turn log root directory")
    parser.add_argument("--index-log", default="./sentry_skill_log/index.jsonl", help="Lightweight per-turn index JSONL")
    parser.add_argument("--unified-log-dir", default="./sentry_skill_log/trinityguard", help="Unified log directory (single file per query)")
    parser.add_argument("--policy", default=None, help="Optional runtime policy JSON path")
    parser.add_argument("--policy-profile", default="balanced", help="Policy profile tag for audit")
    parser.add_argument("--max-memory-mb", type=int, default=1024, help="Maximum memory usage in MB")
    parser.add_argument("--strict-validation", action="store_true", help="Enable strict input validation")
    args = parser.parse_args()

    # Resource-limited execution
    with resource_context(max_memory_mb=args.max_memory_mb):
        try:
            # Load input with error handling
            input_path = Path(args.input_json).resolve()
            hook_start = perf_counter()

            # Check disk space before starting
            check_disk_space(input_path.parent, min_space_mb=50)

            # Load and validate input
            try:
                payload = load_json(input_path)
            except Exception as e:
                logger.error(f"Failed to load input JSON: {e}")
                raise InputValidationError(
                    f"Failed to load input from {input_path}",
                    details={"error": str(e)},
                    original_error=e
                )

            # Validate input if validation is available
            if VALIDATION_AVAILABLE and args.strict_validation:
                validate_input(payload, strict=True)
                logger.debug("Input validation passed")

            # Sanitize input to prevent issues
            if VALIDATION_AVAILABLE:
                payload = sanitize_input(payload)
                logger.debug("Input sanitized")

            project_root = resolve_project_root(payload, input_path)
            events_log = resolve_path_in_project(args.events_log, project_root)
            state_dir = resolve_path_in_project(args.state_dir, project_root)
            out_path = resolve_path_in_project(args.out, project_root) if args.out else None
            turns_dir = resolve_path_in_project(args.turns_dir, project_root)
            index_log = resolve_path_in_project(args.index_log, project_root)
            unified_log_dir = resolve_path_in_project(args.unified_log_dir, project_root)

            # Extract and limit data sizes
            session_id = str(payload.get("session_id", "default-session"))[:1000]
            turn_id = str(payload.get("turn_id", payload.get("request_id", "unknown-turn")))[:1000]
            trace_id = f"{session_id}:{turn_id}:{uuid.uuid4().hex[:8]}"

            # Limit text lengths
            user_prompt = limit_text_length(
                str(payload.get("user_prompt", payload.get("user_request", "")))
            )
            candidate_response = limit_text_length(
                str(payload.get("candidate_response", "")))

            # Limit array sizes
            planned_actions = limit_array_size(
                [str(x) for x in payload.get("planned_actions", [])])
            runtime_events_list = limit_array_size(
                payload.get("runtime_events", []))
            sources_list = limit_array_size(
                payload.get("sources", []))
            intent_tags = limit_array_size(
                [str(x) for x in payload.get("intent_tags", [])])

        except TrinityGuardError as e:
            # Log TrinityGuard errors
            log_error_with_context(e, context={"input": str(args.input_json)})
            logger.error(f"TrinityGuard error: {e}")

            # Try to write error log
            try:
                error_log = {
                    "error": e.to_dict(),
                    "input": str(args.input_json),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
                error_log_path = Path("./sentry_skill_log/trinityguard/error.json")
                error_log_path.parent.mkdir(parents=True, exist_ok=True)
                save_json(error_log_path, error_log)
            except Exception:
                pass

            # Exit with error code
            import sys
            sys.exit(1)
    intent_tags = [str(x) for x in payload.get("intent_tags", [])]
    candidate_response = str(payload.get("candidate_response", ""))
    runtime_events_list = runtime_events if isinstance(runtime_events, list) else []
    sources_list = sources if isinstance(sources, list) else []

    events_sink: Optional[Path] = events_log if args.log_layout == "legacy" else None
    turn_dir = turns_dir / make_turn_dir_name(turn_id)
    turn_input_path = turn_dir / "input.json"
    turn_result_path = turn_dir / "result.json"
    unified_log_path = unified_log_dir / f"{make_turn_dir_name(turn_id)}_{session_id}.json"

    # Only write separate input.json in turn_dir mode
    # In unified mode, all info goes into single file later
    if args.log_layout == "turn_dir":
        save_json(
            turn_input_path,
            {
                "ts": now_iso(),
                "session_id": session_id,
                "turn_id": turn_id,
                "trace_id": trace_id,
                "project_root": str(project_root),
                "input_path": str(input_path),
                "payload": payload,
            },
        )

    emit_event(
        events_log=events_sink,
        trace_id=trace_id,
        session_id=session_id,
        turn_id=turn_id,
        policy_profile=str(args.policy_profile),
        event_type="hook_start",
        decision="allow",
        reason_codes=[],
        matched_rules=[],
        extra={
            "input_json": str(input_path),
            "project_root": str(project_root),
            "input_summary": {
                "user_prompt_length": len(user_prompt),
                "candidate_response_length": len(candidate_response),
                "planned_actions": planned_actions,
                "intent_tags": intent_tags,
                "runtime_event_count": len(runtime_events_list),
                "source_count": len(sources_list),
            },
        },
    )

    # Feature flags (controlled via environment)
    global early_exit_enabled, contextual_matching_enabled, pattern_cache_enabled
    global parallel_detection_enabled, detection_cache_enabled
    early_exit_enabled = os.environ.get("TRINITYGUARD_EARLY_EXIT", "true").lower() == "true"
    contextual_matching_enabled = os.environ.get("TRINITYGUARD_CONTEXTUAL_MATCHING", "true").lower() == "true"
    pattern_cache_enabled = os.environ.get("TRINITYGUARD_PATTERN_CACHE", "true").lower() == "true"
    parallel_detection_enabled = os.environ.get("TRINITYGUARD_PARALLEL_DETECTION", "true").lower() == "true"
    detection_cache_enabled = os.environ.get("TRINITYGUARD_DETECTION_CACHE", "true").lower() == "true"

    # Log performance optimization status
    if PERFORMANCE_AVAILABLE:
        logger.info(f"Performance optimizations enabled: parallel={parallel_detection_enabled}, early_exit={early_exit_enabled}, cache={detection_cache_enabled}")
    else:
        logger.warning("Performance optimization module not available")

    try:
        policy = dict(DEFAULT_POLICY)
        if args.policy:
            policy = merge_policy(policy, load_json(Path(args.policy).resolve()))

        # Load extended detection rules
        detection_rules = load_detection_rules()
        if detection_rules:
            policy["detection_rules"] = detection_rules
            logger.info(f"Extended detection rules loaded: {detection_rules.get('metadata', {}).get('total_rules', 0)} rules available")
        else:
            logger.warning("No extended detection rules loaded")

        leak_patterns = get_cached_patterns(policy, "leak_patterns")

        state_path = state_dir / f"{session_id}.json"
        prev_state = "normal"
        if state_path.exists():
            prev_state = normalize_state(str(load_json(state_path).get("sensitivity_state", "normal")))


        sens = infer_sensitivity(user_prompt, runtime_events_list, prev_state, policy)
        preflight = preflight_decision(user_prompt, planned_actions, intent_tags, sens["sensitivity_state"], policy)

        # Early exit optimization
        if early_exit_enabled and preflight["preflight_decision"] == "block":
            # Create minimal stub results for blocked case
            runtime = {
                "runtime_events": runtime_events_list,
                "alerts": [],
                "suggested_actions": [],
                "trust_annotations": [],
                "decision_reason_codes": ["PF_EARLY_EXIT_SKIP"],
                "matched_rules": [],
                "runtime_decision": "continue"
            }
            output = {
                "leakage_detected": False,
                "residual_leakage_detected": False,
                "redaction_applied": False,
                "redaction_summary": [],
                "decision_reason_codes": ["PF_EARLY_EXIT_SKIP"],
                "matched_rules": [],
                "confidence_level": "low",
                "safe_response": "[BLOCKED_BY_PREFLIGHT]",
                "source_disclosure": "",
                "source_items": [],
                "output_decision": "block"
            }
            # Empty predictive report for blocked case
            predictive_report = {
                "overall_risk_level": "none",
                "predicted_risks": [],
                "top_concerns": [],
                "recommended_actions": [],
                "confidence_summary": 0.0,
            }
        else:
            # Normal flow for non-blocked cases
            runtime = runtime_decision(runtime_events_list, sources_list, policy)

            # Run predictive analysis AFTER all detection rules pass
            # This predicts latent risks that may materialise during execution
            predictive_report_raw = {"overall_risk_level": "none", "predicted_risks": [], "top_concerns": [], "recommended_actions": [], "confidence_summary": 0.0}
            if PREDICTIVE_ANALYSIS_AVAILABLE and preflight["preflight_decision"] != "block":
                try:
                    # Load conversation history for grooming detection (if available)
                    conv_history = []
                    if state_path.exists():
                        prev_data = load_json(state_path)
                        if "conversation_history" in prev_data:
                            conv_history = prev_data["conversation_history"]

                    predictive_report_result = predict_risks(
                        user_prompt=user_prompt,
                        planned_actions=planned_actions,
                        conversation_history=conv_history,
                    )
                    predictive_report_raw = predictive_report_result.to_dict()
                    logger.info(f"Predictive analysis completed: risk_level={predictive_report_raw['overall_risk_level']}, risks_found={len(predictive_report_raw['predicted_risks'])}")
                except Exception as pa_exc:
                    logger.warning(f"Predictive analysis failed: {pa_exc}")

            output = output_guard(candidate_response, preflight["sensitivity_state"], runtime["trust_annotations"], policy, leak_patterns)

        final_action = decide_final_action(preflight, runtime, output)

        residual_risks: List[str] = []
        if output["leakage_detected"]:
            residual_risks.append("privacy leakage risk observed")
        if any(a["source_type"] in set(policy.get("single_source_types", [])) for a in runtime["trust_annotations"]):
            residual_risks.append("single-source reliability risk")

        decision_reason_codes = sorted(
            set(preflight.get("decision_reason_codes", []))
            | set(runtime.get("decision_reason_codes", []))
            | set(output.get("decision_reason_codes", []))
        )
        matched_rules = sorted(
            set(preflight.get("matched_rules", []))
            | set(runtime.get("matched_rules", []))
            | set(output.get("matched_rules", []))
        )

        retention = build_retention_snapshot(policy, final_action, user_prompt, output["safe_response"])

        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "preflight_result",
            preflight["preflight_decision"],
            preflight.get("decision_reason_codes", []),
            preflight.get("matched_rules", []),
            {
                "sensitivity_state": preflight["sensitivity_state"],
                "risk_summary": preflight["risk_summary"],
                "verification_requirements": preflight["verification_requirements"],
                "allowed_actions": preflight["allowed_actions"],
                "blocked_actions": preflight["blocked_actions"],
                "planned_actions": planned_actions,
            },
        )

        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "runtime_result",
            runtime["runtime_decision"],
            runtime.get("decision_reason_codes", []),
            runtime.get("matched_rules", []),
            {
                "runtime_event_count": len(runtime_events_list),
                "runtime_event_types": sorted(
                    set(str(e.get("type", "unknown")).strip().lower() for e in runtime_events_list)
                ),
                "source_types": sorted(set(str(s.get("source_type", "unknown")) for s in sources_list)),
                "alerts": runtime["alerts"],
                "suggested_actions": runtime["suggested_actions"],
                "trust_annotations": runtime["trust_annotations"],
            },
        )

        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "output_guard_result",
            output["output_decision"],
            output.get("decision_reason_codes", []),
            output.get("matched_rules", []),
            {
                "leakage_detected": output["leakage_detected"],
                "residual_leakage_detected": output["residual_leakage_detected"],
                "redaction_applied": output["redaction_applied"],
                "redaction_summary": output["redaction_summary"],
                "confidence_level": output["confidence_level"],
                "source_disclosure_present": bool(output.get("source_disclosure", "")),
                "source_count": len(output.get("source_items", [])),
                "safe_response_length": len(output["safe_response"]),
                "safe_response_preview": excerpt(output["safe_response"], 160),
            },
        )

        # Emit predictive analysis results (if available)
        if PREDICTIVE_ANALYSIS_AVAILABLE:
            predict_reason_codes = []
            if predictive_report_raw.get("overall_risk_level") in ("medium", "high"):
                predict_reason_codes.append(f"PREDICTIVE_RISK_{predictive_report_raw['overall_risk_level'].upper()}")
            emit_event(
                events_sink,
                trace_id,
                session_id,
                turn_id,
                str(args.policy_profile),
                "predictive_analysis_result",
                "review" if predictive_report_raw["overall_risk_level"] in ("medium", "high") else "continue",
                predict_reason_codes,
                [r["category"] for r in predictive_report_raw.get("predicted_risks", [])],
                predictive_report_raw,
            )

        duration_ms = int((perf_counter() - hook_start) * 1000)

        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "final_decision",
            final_action,
            decision_reason_codes,
            matched_rules,
            {
                "final_action": final_action,
                "residual_risks": sorted(set(residual_risks)),
                "audit_notes": sens["reasons"],
                "retention": retention,
                "decision_chain": {
                    "preflight_decision": preflight["preflight_decision"],
                    "runtime_decision": runtime["runtime_decision"],
                    "output_decision": output["output_decision"],
                },
                "predictive_analysis": predictive_report_raw if PREDICTIVE_ANALYSIS_AVAILABLE else {},
                "duration_ms": duration_ms,
                "optimization_metrics": {
                    "early_exit_triggered": early_exit_enabled and preflight["preflight_decision"] == "block",
                    "stages_skipped": ["runtime_decision", "output_guard"] if (early_exit_enabled and preflight["preflight_decision"] == "block") else [],
                },
            },
        )

        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "hook_end",
            final_action,
            decision_reason_codes,
            matched_rules,
            {"duration_ms": duration_ms},
        )

        save_json(state_path, {"session_id": session_id, "sensitivity_state": preflight["sensitivity_state"]})

        summary = {
            "session_id": session_id,
            "turn_id": turn_id,
            "trace_id": trace_id,
            "policy_profile": str(args.policy_profile),
            "final_action": final_action,
            "decision_reason_codes": decision_reason_codes,
            "matched_rules": matched_rules,
            "duration_ms": duration_ms,
            "decision_chain": {
                "preflight_decision": preflight["preflight_decision"],
                "runtime_decision": runtime["runtime_decision"],
                "output_decision": output["output_decision"],
            },
            "output_guard": {
                "output_decision": output["output_decision"],
                "redaction_summary": output["redaction_summary"],
                "safe_response": output["safe_response"],
                "source_disclosure": output.get("source_disclosure", ""),
                "source_items": output.get("source_items", []),
            },
        }

        # Add predictive analysis to summary if available
        if PREDICTIVE_ANALYSIS_AVAILABLE:
            summary["predictive_analysis"] = predictive_report_raw

        if args.log_layout == "unified":
            # Unified log: single file per query with all information
            unified_log = build_unified_log(
                trace_id=trace_id,
                session_id=session_id,
                turn_id=turn_id,
                policy_profile=str(args.policy_profile),
                project_root=str(project_root),
                duration_ms=duration_ms,
                user_prompt=user_prompt,
                planned_actions=planned_actions,
                intent_tags=intent_tags,
                runtime_events=runtime_events_list,
                sources=sources_list,
                candidate_response=candidate_response,
                preflight=preflight,
                runtime=runtime,
                output=output,
                final_action=final_action,
                sensitivity_inference=sens,
                retention=retention,
            )
            save_json(unified_log_path, unified_log)
            if out_path:
                save_json(out_path, summary)
                print(f"Saved summary: {out_path}")
            print(f"Unified log: {unified_log_path}")
            print(f"Session state: {state_path}")
        elif args.log_layout == "turn_dir":
            result_record = {
                "ts": now_iso(),
                "session_id": session_id,
                "turn_id": turn_id,
                "trace_id": trace_id,
                "policy_profile": str(args.policy_profile),
                "final_action": final_action,
                "duration_ms": duration_ms,
                "decision_chain": summary["decision_chain"],
                "decision_reason_codes": decision_reason_codes,
                "matched_rules": matched_rules,
                "residual_risks": sorted(set(residual_risks)),
                "sensitivity_state": preflight["sensitivity_state"],
                "safe_response_preview": excerpt(output["safe_response"], 200),
                "redaction_summary": output["redaction_summary"],
                "retention": retention,
                "input_path": str(turn_input_path),
                "turn_dir": str(turn_dir),
            }
            save_json(turn_result_path, result_record)
            append_jsonl(
                index_log,
                {
                    "ts": now_iso(),
                    "session_id": session_id,
                    "turn_id": turn_id,
                    "trace_id": trace_id,
                    "policy_profile": str(args.policy_profile),
                    "final_action": final_action,
                    "reason_codes": decision_reason_codes,
                    "matched_rules": matched_rules,
                    "duration_ms": duration_ms,
                    "turn_dir": str(turn_dir),
                    "input_path": str(turn_input_path),
                    "result_path": str(turn_result_path),
                },
            )
            if out_path:
                save_json(out_path, summary)
                print(f"Saved summary: {out_path}")
            print(f"Turn dir: {turn_dir}")
            print(f"Result path: {turn_result_path}")
            print(f"Index log path: {index_log}")
            print(f"Updated session state: {state_path}")
        else:
            if out_path:
                save_json(out_path, summary)
                print(f"Saved summary: {out_path}")
            print(f"Appended events: {events_log}")
            print("Turn dir: legacy-mode-disabled")
            print(f"Result path: {out_path if out_path else 'legacy-summary-disabled'}")
            print(f"Index log path: {index_log} (not written in legacy mode)")
            print(f"Updated session state: {state_path}")
    except Exception as exc:  # pragma: no cover - defensive logging
        emit_event(
            events_sink,
            trace_id,
            session_id,
            turn_id,
            str(args.policy_profile),
            "hook_error",
            "error",
            ["HOOK_RUNTIME_ERROR"],
            [],
            {
                "error": str(exc),
                "duration_ms": int((perf_counter() - hook_start) * 1000),
            },
        )
        raise


if __name__ == "__main__":
    main()
