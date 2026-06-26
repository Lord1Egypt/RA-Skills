#!/usr/bin/env python3
"""
Internationalization (i18n) Module
国际化模块

Supports: English (en), Chinese Simplified (zh_CN)
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

# Default language
DEFAULT_LANG = "en"

# Current language
_current_lang = DEFAULT_LANG

# Translations cache
_translations: Dict[str, Dict[str, Any]] = {}

def get_locale_dir() -> Path:
    """Get locales directory path"""
    return Path(__file__).parent / "locales"

def load_translations(lang: str) -> Dict[str, Any]:
    """Load translations for a language"""
    if lang in _translations:
        return _translations[lang]
    
    locale_file = get_locale_dir() / f"{lang}.json"
    
    if not locale_file.exists():
        # Fallback to default language
        if lang != DEFAULT_LANG:
            return load_translations(DEFAULT_LANG)
        return {}
    
    with open(locale_file, "r", encoding="utf-8") as f:
        _translations[lang] = json.load(f)
    
    return _translations[lang]

def set_language(lang: str) -> None:
    """
    Set current language
    
    Args:
        lang: Language code (e.g., "en", "zh_CN")
    """
    global _current_lang
    _current_lang = lang
    load_translations(lang)

def get_language() -> str:
    """Get current language"""
    return _current_lang

def t(key: str, default: str = None) -> str:
    """
    Translate a key
    
    Args:
        key: Translation key (dot notation, e.g., "support_resistance.title")
        default: Default value if key not found
    
    Returns:
        Translated string or key if not found
    """
    translations = load_translations(_current_lang)
    
    # Navigate nested keys
    keys = key.split(".")
    value = translations
    
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            # Key not found, return default or key
            return default if default else key
    
    return value

def _(key: str) -> str:
    """Alias for t() - shorter syntax"""
    return t(key)

def init_language() -> None:
    """Initialize language from environment or config"""
    # Check environment variable
    lang = os.environ.get("TRADING_ASSISTANT_LANG", DEFAULT_LANG)
    
    # Check config file
    config_file = Path(__file__).parent / "config.json"
    if config_file.exists():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                if "language" in config:
                    lang = config["language"]
        except:
            pass
    
    set_language(lang)

# Auto-initialize on import
init_language()

if __name__ == "__main__":
    # Test translations
    print("Testing translations...")
    print(f"Current language: {get_language()}")
    print()
    
    # Test English
    set_language("en")
    print("English:")
    print(f"  App Name: {t('app_name')}")
    print(f"  Support/Resistance: {t('support_resistance.title')}")
    print(f"  Current Price: {t('support_resistance.current_price')}")
    print()
    
    # Test Chinese
    set_language("zh_CN")
    print("中文:")
    print(f"  App Name: {t('app_name')}")
    print(f"  Support/Resistance: {t('support_resistance.title')}")
    print(f"  Current Price: {t('support_resistance.current_price')}")
