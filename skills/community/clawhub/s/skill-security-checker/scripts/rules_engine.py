#!/usr/bin/env python3
"""
rules_engine.py - YAML Rule Pack Loader & Matcher.

Loads rule definitions from rules/*.yaml, compiles regex patterns,
and provides a unified match interface. New rules can be added by
dropping a YAML file — no code changes required.

Author: njskills@agent.qq.com
Version: 3.2.0
"""

import os
import re
import glob
from pathlib import Path

# ============================================================
# Minimal YAML Parser (no PyYAML dependency)
# ============================================================

def _parse_yaml_simple(text):
    """Parse flat YAML structure (key: value, list items with -)."""
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
# Rule Pack Loader
# ============================================================

class RulePack:
    """A single rule pack loaded from a YAML file."""

    def __init__(self, yaml_path):
        self.path = yaml_path
        self.name = ''
        self.display_name = ''
        self.severity = 'medium'
        self.description = ''
        self.patterns = []
        self.suggestion = ''
        self.source = 'static'
        self._compiled = []
        self._load()

    def _load(self):
        try:
            text = Path(self.path).read_text(encoding='utf-8')
            data = _parse_yaml_simple(text)
            self.name = data.get('name', '')
            self.display_name = data.get('display_name', self.name)
            self.severity = data.get('severity', 'medium')
            self.description = data.get('description', '')
            self.patterns = data.get('patterns', [])
            self.suggestion = data.get('suggestion', '')
            self.source = data.get('source', 'static')
            self._compiled = [re.compile(p, re.IGNORECASE) for p in self.patterns]
        except Exception:
            self._compiled = []

    def match(self, line):
        """Return list of (rule_name, pattern_str, match_obj) for all matches."""
        hits = []
        for i, compiled in enumerate(self._compiled):
            m = compiled.search(line)
            if m:
                hits.append((self.name, self.patterns[i], m))
        return hits


class RuleEngine:
    """Loads all rule packs from a directory and provides unified scanning."""

    def __init__(self, rules_dir=None):
        if rules_dir is None:
            rules_dir = Path(__file__).parent / "rules"
        self.rules_dir = Path(rules_dir)
        self.packs = []
        self._load_all()

    def _load_all(self):
        if not self.rules_dir.exists():
            return
        for yaml_file in sorted(self.rules_dir.glob("*.yaml")):
            try:
                pack = RulePack(yaml_file)
                if pack.patterns:
                    self.packs.append(pack)
            except Exception:
                continue

    def match_line(self, line):
        """Match a line against all rule packs. Returns list of (pack, pattern_str)."""
        all_hits = []
        for pack in self.packs:
            for hit in pack.match(line):
                all_hits.append((pack, hit[1]))
        return all_hits

    def get_all_rules(self):
        """Return list of (name, display_name, severity, pattern_count)."""
        return [(p.name, p.display_name, p.severity, len(p.patterns)) for p in self.packs]
