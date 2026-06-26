#!/usr/bin/env python3
"""
Preset and Template management for Grasshopper definitions.
"""

import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List

logger = logging.getLogger("rhinoclaw.presets")

CONFIG_DIR = Path(__file__).parent / "config"


class PresetManager:
    """Manage GH definition templates and presets."""

    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or CONFIG_DIR
        self._templates = None
        self._presets = None

    @property
    def templates(self) -> dict:
        if self._templates is None:
            self._templates = self._load_yaml('templates.yaml').get('templates', {})
        return self._templates

    @property
    def presets(self) -> dict:
        if self._presets is None:
            self._presets = self._load_yaml('presets.yaml').get('presets', {})
        return self._presets

    def _load_yaml(self, filename: str) -> dict:
        path = self.config_dir / filename
        if not path.exists():
            logger.warning(f"Config file not found: {path}")
            return {}
        with open(path) as f:
            return yaml.safe_load(f) or {}

    def get_template(self, name: str) -> dict:
        """Get template by name, resolving inheritance chain."""
        if name not in self.templates:
            raise ValueError(f"Unknown template: '{name}'. Available: {', '.join(self.templates.keys())}")

        template = dict(self.templates[name])

        if 'inherits' in template:
            parent = self.get_template(template['inherits'])
            # Merge: parent first, child overrides
            merged_defaults = {**parent.get('defaults', {}), **template.get('defaults', {})}
            merged_validation = {**parent.get('validation', {}), **template.get('validation', {})}
            merged_aliases = {**parent.get('aliases', {}), **template.get('aliases', {})}

            template['defaults'] = merged_defaults
            template['validation'] = merged_validation
            template['aliases'] = merged_aliases
            # Inherit file path if not overridden
            if 'file' not in template:
                template['file'] = parent.get('file')
            # Inherit category if not overridden
            if 'category' not in template:
                template['category'] = parent.get('category')

        return template

    def get_preset(self, name: str) -> dict:
        """Get preset with resolved template."""
        if name not in self.presets:
            raise ValueError(f"Unknown preset: '{name}'. Available: {', '.join(self.presets.keys())}")

        preset = dict(self.presets[name])
        template = self.get_template(preset['template'])

        # Merge: template defaults + preset params (preset wins)
        params = {**template.get('defaults', {}), **preset.get('params', {})}

        return {
            'name': name,
            'description': preset.get('description', ''),
            'template_name': preset['template'],
            'file': template['file'],
            'params': params,
            'validation': template.get('validation', {}),
            'aliases': template.get('aliases', {}),
            'category': template.get('category', ''),
        }

    def list_presets(self, category: str = None) -> List[dict]:
        """List available presets, optionally filtered by category."""
        result = []
        for name, preset in self.presets.items():
            try:
                resolved = self.get_preset(name)
                if category and resolved.get('category') != category:
                    continue
                result.append({
                    'name': name,
                    'description': preset.get('description', ''),
                    'template': preset.get('template', ''),
                    'category': resolved.get('category', ''),
                })
            except ValueError as e:
                logger.warning(f"Skipping preset '{name}': {e}")
        return result

    def list_templates(self, category: str = None) -> List[dict]:
        """List available templates, optionally filtered by category."""
        result = []
        for name, tmpl in self.templates.items():
            if category and tmpl.get('category') != category:
                continue
            result.append({
                'name': name,
                'description': tmpl.get('description', ''),
                'category': tmpl.get('category', ''),
                'file': tmpl.get('file', ''),
            })
        return result

    def resolve_aliases(self, params: dict, aliases: dict) -> dict:
        """Apply alias mapping to parameter names."""
        return {aliases.get(k, k): v for k, v in params.items()}
