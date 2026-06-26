#!/usr/bin/env python3
"""
多语言加载器
支持中英文切换
"""

import json
from pathlib import Path
from typing import Dict, Optional

class LocaleLoader:
    """多语言加载器"""
    
    def __init__(self, locales_dir: Optional[str] = None):
        if locales_dir:
            self.locales_dir = Path(locales_dir)
        else:
            self.locales_dir = Path(__file__).parent.parent / 'locales'
        self.locales: Dict[str, Dict] = {}
        self.current_lang = 'en'
    
    def load(self, lang: str = 'en') -> Dict:
        """加载指定语言包"""
        if lang in self.locales:
            return self.locales[lang]
        
        locale_file = self.locales_dir / f'{lang}.json'
        if not locale_file.exists():
            # 降级到英文
            locale_file = self.locales_dir / 'en.json'
        
        with open(locale_file, 'r', encoding='utf-8') as f:
            self.locales[lang] = json.load(f)
        
        self.current_lang = lang
        return self.locales[lang]
    
    def get(self, key: str, **kwargs) -> str:
        """获取翻译文本"""
        if self.current_lang not in self.locales:
            self.load(self.current_lang)
        
        text = self.locales[self.current_lang].get(key, key)
        if kwargs:
            text = text.format(**kwargs)
        return text
    
    def set_language(self, lang: str):
        """设置当前语言"""
        if lang not in self.locales:
            self.load(lang)
        self.current_lang = lang
    
    def detect_system_language(self) -> str:
        """检测系统语言"""
        import locale
        try:
            sys_locale = locale.getdefaultlocale()[0]
            if sys_locale and sys_locale.startswith('zh'):
                return 'zh'
        except:
            pass
        return 'en'
