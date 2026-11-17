#!/usr/bin/env python3
"""
community_rules.py - Third-party rule pack validator & loader.

Validates community YAML rule packs before loading:
- Schema validation (required fields, type checks)
- Source recording (where the rule came from)
- Optional signature verification (HMAC-SHA256)

Author: njskills@agent.qq.com
Version: 3.3.0
"""

import os
import re
import json
import hashlib
import hmac
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ============================================================
# Schema Definition
# ============================================================

RULE_SCHEMA = {
    'name': {'type': 'str', 'required': True, 'pattern': r'^[a-z][a-z0-9_]*$'},
    'display_name': {'type': 'str', 'required': True, 'max_len': 50},
    'severity': {'type': 'str', 'required': True, 'choices': ['critical', 'high', 'medium', 'low', 'info']},
    'description': {'type': 'str', 'required': True, 'max_len': 200},
    'patterns': {'type': 'list', 'required': True, 'min_items': 1, 'max_items': 100},
    'suggestion': {'type': 'str', 'required': False, 'max_len': 200},
    'source': {'type': 'str', 'required': False, 'choices': ['static', 'dynamic', 'community']},
}

# ============================================================
# Minimal YAML Parser (same as rules_engine.py)
# ============================================================

def _parse_yaml_simple(text: str) -> Dict:
    """Parse flat YAML structure."""
    result = {}
    current_key = None
    current_list = None
    for line in text.split('\n'):
        stripped = line.strip()
        if not stripped or stripped.startswith('#'):
            continue
        if stripped.startswith('- '):
            if current_list is not None:
                current_list.append(stripped[2:].strip().strip('"').strip("'"))
            continue
        if ':' in stripped:
            key, _, val = stripped.partition(':')
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            if val == '':
                result[key] = []
                current_key = key
                current_list = result[key]
            else:
                result[key] = val
                current_key = None
                current_list = None
    return result


# ============================================================
# Rule Pack Validator
# ============================================================

class RulePackValidator:
    """Validates community YAML rule packs."""

    def __init__(self, signature_key: Optional[str] = None):
        self.signature_key = signature_key
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate(self, yaml_path: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a rule pack YAML file.
        Returns: (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []

        path = Path(yaml_path)
        if not path.exists():
            self.errors.append(f"File not found: {yaml_path}")
            return False, self.errors, self.warnings

        try:
            text = path.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Cannot read file: {e}")
            return False, self.errors, self.warnings

        # Parse YAML
        data = _parse_yaml_simple(text)

        # Validate schema
        self._validate_schema(data)

        # Validate patterns (check regex validity)
        self._validate_patterns(data.get('patterns', []))

        # Check signature if key provided
        if self.signature_key:
            self._verify_signature(text)

        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_schema(self, data: Dict):
        """Validate data against schema."""
        for field, rules in RULE_SCHEMA.items():
            value = data.get(field)
            if rules['required'] and not value:
                self.errors.append(f"Missing required field: {field}")
                continue
            if not value:
                continue
            if rules['type'] == 'str' and not isinstance(value, str):
                self.errors.append(f"Field '{field}' must be a string")
            elif rules['type'] == 'list' and not isinstance(value, list):
                self.errors.append(f"Field '{field}' must be a list")
            if rules['type'] == 'str' and isinstance(value, str):
                if 'max_len' in rules and len(value) > rules['max_len']:
                    self.warnings.append(f"Field '{field}' exceeds max length ({len(value)} > {rules['max_len']})")
                if 'pattern' in rules and not re.match(rules['pattern'], value):
                    self.errors.append(f"Field '{field}' does not match pattern: {rules['pattern']}")
                if 'choices' in rules and value not in rules['choices']:
                    self.errors.append(f"Field '{field}' must be one of: {rules['choices']}")
            if rules['type'] == 'list' and isinstance(value, list):
                if 'min_items' in rules and len(value) < rules['min_items']:
                    self.errors.append(f"Field '{field}' must have at least {rules['min_items']} items")
                if 'max_items' in rules and len(value) > rules['max_items']:
                    self.errors.append(f"Field '{field}' must have at most {rules['max_items']} items")

    def _validate_patterns(self, patterns: List[str]):
        """Validate regex patterns."""
        for i, pat in enumerate(patterns):
            try:
                re.compile(pat)
            except re.error as e:
                self.errors.append(f"Invalid regex pattern #{i+1}: {pat} - {e}")

    def _verify_signature(self, text: str):
        """Verify HMAC-SHA256 signature."""
        # Look for signature in YAML comments
        sig_match = re.search(r'#\s*signature:\s*([a-f0-9]{64})', text)
        if not sig_match:
            self.warnings.append("No signature found (signature verification skipped)")
            return
        provided_sig = sig_match.group(1)
        # Compute HMAC of content without signature line
        content_without_sig = re.sub(r'#\s*signature:\s*[a-f0-9]{64}\n?', '', text)
        expected_sig = hmac.new(
            self.signature_key.encode() if self.signature_key else b'',
            content_without_sig.encode(),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(provided_sig, expected_sig):
            self.errors.append("Signature verification failed")


# ============================================================
# Community Rule Loader
# ============================================================

class CommunityRuleLoader:
    """Loads and validates community rule packs."""

    def __init__(self, rules_dir: str, signature_key: Optional[str] = None):
        self.rules_dir = Path(rules_dir)
        self.validator = RulePackValidator(signature_key)
        self.loaded_rules: List[Dict] = []
        self.failed_rules: List[Dict] = []

    def load_all(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Load all community rule packs from directory.
        Returns: (loaded_rules, failed_rules)
        """
        self.loaded_rules = []
        self.failed_rules = []
        if not self.rules_dir.exists():
            return self.loaded_rules, self.failed_rules
        for yaml_file in sorted(self.rules_dir.glob("*.yaml")):
            is_valid, errors, warnings = self.validator.validate(str(yaml_file))
            if is_valid:
                data = _parse_yaml_simple(yaml_file.read_text(encoding='utf-8'))
                data['_source'] = str(yaml_file)
                data['_loaded_at'] = time.time()
                self.loaded_rules.append(data)
            else:
                self.failed_rules.append({
                    'file': str(yaml_file),
                    'errors': errors,
                    'warnings': warnings,
                })
        return self.loaded_rules, self.failed_rules

    def get_stats(self) -> Dict:
        """Get loading statistics."""
        return {
            'loaded': len(self.loaded_rules),
            'failed': len(self.failed_rules),
            'total': len(self.loaded_rules) + len(self.failed_rules),
        }
