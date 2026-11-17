"""
global_exclude.py - Team-level global exclude configuration (.nosec.yml).

Parses .nosec.yml from skill root. Supports:
  - Category-level exclude: skip entire rule categories
  - File-level exclude: skip rules for specific files
  - Pattern-level exclude: skip rules matching regex patterns

Format:
  version: 1
  exclude:
    categories:
      - quality_check
      - dangerous_functions
    files:
      - "scripts/audit.py"
    patterns:
      - ".*test.*"

Author: njskills@agent.qq.com
Version: 3.1.0
"""

import os
import re
from pathlib import Path

# ============================================================
# Config Parser
# ============================================================

class GlobalExcludeConfig:
    """Parse and apply .nosec.yml global exclude configuration."""

    def __init__(self, skill_path=None):
        self.version = 1
        self.exclude_categories = set()
        self.exclude_files = set()
        self.exclude_patterns = []
        self._loaded = False

        if skill_path:
            self.load(skill_path)

    def load(self, skill_path):
        """Load .nosec.yml from skill root if present."""
        skill_path = Path(skill_path)
        config_path = skill_path / ".nosec.yml"
        if not config_path.exists():
            self._loaded = False
            return

        try:
            content = config_path.read_text(encoding='utf-8-sig')
        except Exception:
            self._loaded = False
            return

        # Minimal YAML-ish parser (avoid PyYAML dependency)
        in_exclude = False
        in_section = None
        for line in content.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            if stripped.startswith('version:'):
                try:
                    self.version = int(stripped.split(':', 1)[1].strip())
                except Exception:
                    self.version = 1
                continue
            if stripped == 'exclude:':
                in_exclude = True
                continue
            if not in_exclude:
                continue
            if stripped.startswith('categories:'):
                in_section = 'categories'
                continue
            if stripped.startswith('files:'):
                in_section = 'files'
                continue
            if stripped.startswith('patterns:'):
                in_section = 'patterns'
                continue
            if stripped.startswith('- '):
                val = stripped[2:].strip().strip('"').strip("'")
                if in_section == 'categories':
                    self.exclude_categories.add(val)
                elif in_section == 'files':
                    self.exclude_files.add(val)
                elif in_section == 'patterns':
                    self.exclude_patterns.append(val)
            elif not stripped.startswith('-'):
                in_section = None
        self._loaded = True

    def is_category_excluded(self, category):
        """Check if a rule category is globally excluded."""
        return category in self.exclude_categories

    def is_file_excluded(self, filepath):
        """Check if a file is globally excluded."""
        for pattern in self.exclude_files:
            if pattern in filepath:
                return True
        return False

    def is_pattern_excluded(self, text):
        """Check if text matches any excluded regex pattern."""
        for pat in self.exclude_patterns:
            try:
                if re.search(pat, text):
                    return True
            except re.error:
                continue
        return False

    def should_skip(self, category, filepath='', text=''):
        """Should we skip this result?"""
        if not self._loaded:
            return False
        if self.is_category_excluded(category):
            return True
        if filepath and self.is_file_excluded(filepath):
            return True
        if text and self.is_pattern_excluded(text):
            return True
        return False

    @property
    def loaded(self):
        return self._loaded
