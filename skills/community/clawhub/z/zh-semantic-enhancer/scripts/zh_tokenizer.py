#!/usr/bin/env python3
"""
中文增强分词模块
Chinese Enhanced Tokenization Module
"""

import re
from typing import List, Tuple, Dict, Any

# 基础词典（简化版）
DOMAIN_DICTS = {
    "finance": ["股票", "基金", "期货", "外汇", "债券", "理财"],
    "medical": ["医院", "医生", "药品", "症状", "诊断", "治疗"],
    "legal": ["法律", "律师", "合同", "诉讼", "判决"],
    "tech": ["代码", "程序", "算法", "数据", "人工智能"]
}

# 词性标注简化映射
POS_MAP = {
    "n": "名词",
    "v": "动词",
    "a": "形容词",
    "d": "副词",
    "r": "代词",
    "m": "数词",
    "q": "量词",
    "p": "介词",
    "c": "连词",
    "u": "助词",
    "e": "叹词",
    "y": "语气词",
    "o": "拟声词",
    "x": "未知"
}


def enhanced_tokenize(text: str) -> Dict[str, Any]:
    """
    中文增强分词：支持新词发现 + 专业术语识别 + 实体标注
    """
    # 1. 基础分词
    tokens = _basic_tokenize(text)
    
    # 2. 检测领域
    domain = detect_domain(text)
    
    # 3. 命名实体识别（简化版）
    entities = _extract_entities(text)
    
    return {
        "tokens": tokens,
        "entities": entities,
        "domain": domain,
        "word_count": len(tokens)
    }


def _basic_tokenize(text: str) -> List[Tuple[str, str]]:
    """基础分词（简化版，不依赖jieba）"""
    tokens = []
    i = 0
    
    # 常见词库
    common_words = set()
    for words in DOMAIN_DICTS.values():
        common_words.update(words)
    common_words.update([
        "中文", "语义", "理解", "增强", "技能", "分析", "处理",
        "意思", "方便", "内卷", "躺平", "yyds", "画蛇添足",
        "首先", "然后", "最后", "因为", "所以", "但是"
    ])
    
    while i < len(text):
        matched = False
        # 尝试匹配最长词（4-2字）
        for length in [4, 3, 2]:
            if i + length <= len(text):
                word = text[i:i+length]
                if word in common_words:
                    tokens.append((word, _guess_pos(word)))
                    i += length
                    matched = True
                    break
        
        if not matched:
            char = text[i]
            # 判断字符类型
            if char.isdigit():
                tokens.append((char, "m"))  # 数词
            elif char in "，。！？；：""''（）【】":
                tokens.append((char, "w"))  # 标点
            else:
                tokens.append((char, "x"))  # 未知
            i += 1
    
    return tokens


def _guess_pos(word: str) -> str:
    """猜测词性（简化版）"""
    # 简单规则判断
    if word.endswith("性") or word.endswith("度"):
        return "n"  # 名词
    elif word.endswith("地"):
        return "d"  # 副词
    elif word.endswith("了") or word.endswith("着"):
        return "u"  # 助词
    else:
        return "n"  # 默认名词


def detect_domain(text: str) -> str:
    """检测文本领域"""
    domain_scores = {}
    
    for domain, words in DOMAIN_DICTS.items():
        score = sum(1 for word in words if word in text)
        if score > 0:
            domain_scores[domain] = score
    
    if domain_scores:
        return max(domain_scores, key=domain_scores.get)
    return "general"


def _extract_entities(text: str) -> List[Dict[str, Any]]:
    """提取命名实体（简化版）"""
    entities = []
    
    # 时间实体
    time_patterns = [
        r'(\d{4}年\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}月\d{1,2}日)',
        r'(\d{1,2}:\d{2})',
    ]
    for pattern in time_patterns:
        for match in re.finditer(pattern, text):
            entities.append({
                "text": match.group(1),
                "type": "TIME",
                "start": match.start(),
                "end": match.end()
            })
    
    # 数字/金额实体
    num_pattern = r'(\d+(?:\.\d+)?(?:万|亿|千|百)?(?:元|美元|￥|\$)?)'
    for match in re.finditer(num_pattern, text):
        entities.append({
            "text": match.group(1),
            "type": "NUMBER",
            "start": match.start(),
            "end": match.end()
        })
    
    return entities


if __name__ == "__main__":
    # 测试
    test_texts = [
        "中文语义理解增强技能",
        "我今天去了医院看病",
        "股票涨了10万元",
        "yyds永远的神"
    ]
    
    for text in test_texts:
        print(f"\n输入: {text}")
        result = enhanced_tokenize(text)
        print(f"分词: {result['tokens']}")
        print(f"领域: {result['domain']}")
        print(f"实体: {result['entities']}")
