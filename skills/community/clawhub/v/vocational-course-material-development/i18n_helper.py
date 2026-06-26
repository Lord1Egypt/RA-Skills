#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""i18n Helper for Vocational Course-Material Development Skill"""

import os
import json
from pathlib import Path


class I18NHelper:
    def __init__(self, i18n_file=None):
        if i18n_file is None:
            skill_dir = Path(__file__).parent
            i18n_file = skill_dir / "i18n.json"
        self.i18n_file = Path(i18n_file)
        self.translations = self._load_translations()
        self.current_lang = self._detect_language()

    def _load_translations(self):
        try:
            if self.i18n_file.exists():
                with open(self.i18n_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"Error loading i18n.json: {e}", file=__import__('sys').stderr)
            return {}

    def _detect_language(self):
        hermes_lang = os.environ.get('HERMES_LANG', '').lower()
        if hermes_lang in ['zh', 'en']:
            return hermes_lang
        lang_env = os.environ.get('LANG', '').lower()
        if 'zh' in lang_env or 'cn' in lang_env:
            return 'zh'
        elif 'en' in lang_env:
            return 'en'
        return 'zh'

    def get_str(self, key, lang=None, default=None):
        if lang is None:
            lang = self.current_lang
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        if lang != 'zh' and 'zh' in self.translations and key in self.translations['zh']:
            return self.translations['zh'][key]
        return default if default is not None else key

    def get_lang(self):
        return self.current_lang

    def set_lang(self, lang):
        if lang in ['zh', 'en']:
            self.current_lang = lang


_global_i18n_instance = None


def get_i18n(i18n_file=None):
    global _global_i18n_instance
    if _global_i18n_instance is None:
        _global_i18n_instance = I18NHelper(i18n_file)
    return _global_i18n_instance


def get_str(key, lang=None, default=None, i18n_file=None):
    helper = get_i18n(i18n_file)
    return helper.get_str(key, lang=lang, default=default)
