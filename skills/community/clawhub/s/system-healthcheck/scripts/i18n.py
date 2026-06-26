#!/usr/bin/env python3
"""
国际化 (i18n) 支持模块

功能:
1. 自动检测系统语言
2. 加载对应语言文件
3. 提供翻译函数
4. 支持模板变量替换

使用示例:
    from i18n import get_i18n
    _ = get_i18n().t
    print(_("messages.disk_ok", usage=45))
"""

import os
import locale
from pathlib import Path
from typing import Dict, Any, Optional


class I18n:
    def __init__(self, locales_dir: Optional[Path] = None, default_locale: str = "en"):
        self.locales_dir = locales_dir
        self.default_locale = default_locale
        self.translations: Dict[str, Dict[str, Any]] = {}
        self.current_locale: str = default_locale
        
    def detect_locale(self) -> str:
        """自动检测系统语言"""
        # 1. 环境变量优先
        env_lang = os.getenv("OPENCLAW_LOCALE") or os.getenv("LANG") or os.getenv("LC_ALL")
        if env_lang:
            lang = env_lang.split(".")[0].replace("_", "-")
            if lang:
                return lang
        
        # 2. 系统 locale
        try:
            sys_lang = locale.getdefaultlocale()[0]
            if sys_lang:
                return sys_lang.replace("_", "-")
        except:
            pass
        
        # 3. 回退到默认
        return self.default_locale
    
    def load(self, locale_name: Optional[str] = None) -> "I18n":
        """加载指定语言文件
        
        Args:
            locale_name: 语言代码，如 zh-CN, en。None 则自动检测
        
        Returns:
            self (支持链式调用)
        """
        if locale_name is None:
            locale_name = self.detect_locale()
        
        self.current_locale = locale_name
        
        # 确定语言文件路径（优先使用传入的路径）
        if self.locales_dir is None:
            # 从当前脚本位置查找 locales 目录
            self.locales_dir = Path(__file__).parent.parent / "locales"
        
        locale_file = self.locales_dir / f"{locale_name}.yaml"
        
        # 如果指定语言不存在，回退到英语
        if not locale_file.exists():
            if locale_name != self.default_locale:
                locale_file = self.locales_dir / f"{self.default_locale}.yaml"
                if not locale_file.exists():
                    print(f"⚠️ No locale file found, using empty translations")
                    return self
        
        # 加载 YAML 文件
        self.translations = self._load_yaml(locale_file)
        return self
    
    def _load_yaml(self, file_path: Path) -> Dict:
        """加载 YAML 文件（支持 pyyaml 或简易解析）"""
        try:
            import yaml
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except ImportError:
            return self._simple_yaml_parse(file_path)
        except Exception as e:
            print(f"⚠️ Failed to load locale file: {e}")
            return {}
    
    def _simple_yaml_parse(self, file_path: Path) -> Dict:
        """简易 YAML 解析（无 pyyaml 依赖时的后备方案）"""
        result = {}
        current_section = None
        current_indent = 0
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip()
                if not line or line.startswith("#"):
                    continue
                
                # 计算缩进
                stripped = line.lstrip()
                indent = len(line) - len(stripped)
                
                if ":" not in stripped:
                    continue
                
                # 顶级键（无缩进）
                if indent == 0 and stripped.endswith(":"):
                    current_section = stripped[:-1]
                    result[current_section] = {}
                    current_indent = 0
                # 二级键（有缩进）
                elif current_section and indent > 0:
                    key, value = stripped.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')
                    result[current_section][key] = value
        
        return result
    
    def t(self, key: str, **kwargs) -> str:
        """翻译函数
        
        Args:
            key: 翻译键，如 "messages.disk_ok"
            **kwargs: 模板变量，如 usage=85, threshold=80
        
        Returns:
            翻译后的字符串
        """
        keys = key.split(".")
        value = self.translations
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                # 键不存在，返回原始键名
                return f"[{key}]"
        
        # 模板变量替换
        if isinstance(value, str) and kwargs:
            try:
                value = value.format(**kwargs)
            except KeyError as e:
                pass  # 静默忽略缺失的变量
        
        return value
    
    def get_locale_info(self) -> Dict[str, str]:
        """获取当前语言信息"""
        meta = self.translations.get("meta", {})
        return {
            "locale": self.current_locale,
            "language": meta.get("language", "Unknown"),
            "version": meta.get("version", "1.0")
        }


# 全局实例
_i18n_instance: Optional[I18n] = None


def get_i18n(locales_dir: Optional[Path] = None, locale_name: Optional[str] = None) -> I18n:
    """获取或创建 i18n 实例（单例模式）"""
    global _i18n_instance
    
    if _i18n_instance is None:
        _i18n_instance = I18n(locales_dir)
        _i18n_instance.load(locale_name)
    
    return _i18n_instance


def reload_i18n(locales_dir: Optional[Path] = None, locale_name: Optional[str] = None) -> I18n:
    """重新加载 i18n（用于切换语言）"""
    global _i18n_instance
    _i18n_instance = I18n(locales_dir)
    _i18n_instance.load(locale_name)
    return _i18n_instance


# 快捷函数
def t(key: str, **kwargs) -> str:
    """快捷翻译函数"""
    return get_i18n().t(key, **kwargs)


if __name__ == "__main__":
    # 测试
    i18n = get_i18n()
    print(f"Current locale: {i18n.get_locale_info()}")
    print(f"Test translation: {i18n.t('status.ok')}")
