# -*- coding: utf-8 -*-
"""
描述汉化模块
基于内置词表将常见英文短语替换为中文（命中一条规则即停，未命中的保持原文）
"""
from typing import Dict
from utils.config import TRANSLATION_RULES


def translate_description(desc: str) -> str:
    """
    汉化技能描述

    Args:
        desc: 技能描述

    Returns:
        替换后的描述（未命中词表时保持原文）
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


def extract_untranslated(descriptions: list) -> list:
    """
    提取未命中词表的英文单词（用于扩充 TRANSLATION_RULES）

    Args:
        descriptions: 描述列表

    Returns:
        去重排序的英文单词列表
    """
    untranslated = set()
    for desc in descriptions:
        if not desc:
            continue
        for word in desc.split():
            w = word.strip(',.()[]{}:;!?·—-–"\'`')
            if not w or not w.isascii() or not w.isalpha() or len(w) <= 3:
                continue
            if any(w.lower() in eng.lower() for eng in TRANSLATION_RULES):
                continue
            untranslated.add(w.lower())
    return sorted(untranslated)
