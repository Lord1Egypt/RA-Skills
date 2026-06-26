# -*- coding: utf-8 -*-
"""
翻译工具模块
将英文描述翻译为中文
"""
from typing import Dict
from utils.config import TRANSLATION_RULES


def translate_description(desc: str) -> str:
    """
    翻译技能描述
    
    Args:
        desc: 英文描述
        
    Returns:
        中文描述
    """
    if not desc:
        return desc
    
    result = desc
    
    # 优先匹配长规则
    for eng, chn in sorted(TRANSLATION_RULES.items(), key=lambda x: len(x[0]), reverse=True):
        if eng in result:
            result = result.replace(eng, chn)
            break
    
    return result


def extend_translation_rules(new_rules: Dict[str, str]):
    """
    扩展翻译规则
    
    Args:
        new_rules: 新的翻译规则 {英文: 中文}
    """
    TRANSLATION_RULES.update(new_rules)


def extract_untranslated(descriptions: list) -> list:
    """
    提取未翻译的短语
    
    Args:
        descriptions: 描述列表
        
    Returns:
        未翻译的英文短语列表
    """
    untranslated = set()
    
    for desc in descriptions:
        if not desc:
            continue
        
        # 简单检测：包含英文字母且未被翻译规则覆盖
        if any(c.isalpha() for c in desc):
            # 检查是否有未翻译的部分
            words = desc.split()
            for word in words:
                word = word.strip(',.()[]')
                if word and word.isalpha() and len(word) > 3:
                    # 检查是否在翻译规则中
                    found = False
                    for eng in TRANSLATION_RULES:
                        if word.lower() in eng.lower():
                            found = True
                            break
                    if not found:
                        untranslated.add(word)
    
    return sorted(list(untranslated))
