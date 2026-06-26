# -*- coding: utf-8 -*-
"""
V4.6.14: 全链路统一禁句配置
所有禁句列表从此文件导入，避免散落导致不一致

分类：
- L1_ABSOLUTE: 绝对禁止词，任何阶段都禁止，无例外
- L2_CONTEXTUAL: 上下文判断词，有具体信号时可放过

修订历史：
- V4.6.14: 新建，统一全链路禁句配置
"""

import re
from typing import List


# ============================================================
# L1 绝对禁止词（无豁免）
# ============================================================
# 无论是否有上下文，这些词/短语出现即表示模糊表述
L1_ABSOLUTE: List[str] = [
    "正常加载",
    "验证成功",
    "符合业务规则",
    "符合预期",
    "功能正常",
    "数据正确",
    "操作成功",
    "展示完整",
    "流程正确",
    "结果正确",
    "处理正常",
    "结果符合",
]

# L1 正则模式（用于正则匹配，支持标点符号变化）
L1_PATTERNS: List[str] = [
    r'正常加载\s*[，。；]?',
    r'验证成功\s*[，。；]?',
    r'符合业务规则\s*[，。；]?',
    r'符合预期\s*[，。；]?',
    r'功能正常\s*[，。；]?',
    r'数据正确\s*[，。；]?',
    r'操作成功\s*[，。；]?',
    r'展示完整\s*[，。；]?',
    r'流程正确\s*[，。；]?',
    r'结果正确\s*[，。；]?',
    r'处理正常\s*[，。；]?',
    r'结果符合\s*[，。；]?',
]


# ============================================================
# L2 上下文判断词（有具体信号时可放过）
# ============================================================
# 这些词需要根据上下文判断是否模糊
# 如果周围有具体性信号（引号内文案/数字/UI元素），则放过
L2_CONTEXTUAL: List[str] = [
    "正常",
    "成功",
    "正确",
    "合法",
    "合理",
    "有效",
]


# ============================================================
# 具体性信号定义
# ============================================================
# 当文本中出现以下信号时，即使含有L2词也不视为模糊
CONTEXT_SIGNALS = {
    # 信号1: 引号包裹的具体UI文案
    "quoted_text": [
        r'「[^」]+」',      # 中文直角引号
        r'"[^"]+"',          # 英文双引号
        r'"[^"]+"',          # 中文双引号（书名号风格）
    ],
    
    # 信号2: 可量化数字词组
    "quantifiable": [
        r'\d+\s*条',         # 新增8条、显示3条、共10条
        r'\d+\s*次',         # 共5次、点击3次
        r'\d+\s*个',         # 共4个、新增2个
        r'\d+%',             # 50%、80%
        r'\d+\s*秒',         # 耗时3秒
        r'\d+\s*分钟',       # 耗时5分钟
        r'\d+\s*px',        # 100px
        r'共\s*\d+',         # 共10条、共200元
        r'变为\s*\d+',       # 变为8条
        r'增加\s*\d+',       # 增加3条
        r'减少\s*\d+',       # 减少2条
        r'第\s*\d+\s*页',    # 第1页/共5页
        r'\d{4}-\d{2}-\d{2}',  # 日期格式
    ],
    
    # 信号3: 强UI信号（单个即算）
    "strong_ui": [
        r'红色边框', r'绿色边框', r'蓝色边框',
        r'红色提示', r'绿色提示', r'橙色警告',
        r'红色图标', r'绿色图标',
        r'弹窗关闭', r'弹窗打开',
        r'输入框禁用', r'输入框启用',
        r'按钮置灰', r'按钮高亮',
        r'页面跳转',
        r'变为',             # 状态/值变化
        r'新增\d+条',
        r'URL变为',
    ],
    
    # 信号4: 弱UI信号（需要2个以上）
    "weak_ui": [
        "弹窗", "按钮", "输入框", "下拉框", "列表",
        "页面", "窗口", "对话框", "提示", "消息",
        "提交", "确认", "取消", "关闭", "保存",
    ],
}


def has_context_signal(text: str) -> bool:
    """
    检测文本中是否包含具体性信号。
    
    有以下任一信号即返回True（表示虽然含有L2词，但内容足够具体）：
    1. 「」引号包裹的具体文案
    2. 可量化数字词组
    3. 强UI信号
    4. 2个以上弱UI信号
    """
    # Signal 1: 引号包裹
    for pattern in CONTEXT_SIGNALS["quoted_text"]:
        if re.search(pattern, text):
            return True
    
    # Signal 2: 可量化数字
    for pattern in CONTEXT_SIGNALS["quantifiable"]:
        if re.search(pattern, text):
            return True
    
    # Signal 3: 强UI信号
    for pattern in CONTEXT_SIGNALS["strong_ui"]:
        if re.search(pattern, text):
            return True
    
    # Signal 4: 弱UI信号（需2个以上）
    weak_count = sum(1 for kw in CONTEXT_SIGNALS["weak_ui"] if kw in text)
    if weak_count >= 2:
        return True
    
    return False


def check_forbidden_words(text: str, level: str = "L1") -> dict:
    """
    检查文本是否包含禁句词。
    
    Args:
        text: 待检查的文本
        level: 检查级别 "L1"（只检查L1）/"L2"（检查L1+L2）/"ALL"（同L2）
    
    Returns:
        dict: {
            "has_banned": bool,      # 是否包含禁止词
            "banned_words": list,    # 包含的禁止词列表
            "forgiven": bool,        # 是否因上下文被放过
            "reason": str,           # 原因说明
        }
    """
    result = {
        "has_banned": False,
        "banned_words": [],
        "forgiven": False,
        "reason": "",
    }
    
    # 检查L1
    for word in L1_ABSOLUTE:
        if word in text:
            result["has_banned"] = True
            result["banned_words"].append(word)
    
    if level in ("L2", "ALL"):
        for word in L2_CONTEXTUAL:
            if word in text:
                result["has_banned"] = True
                result["banned_words"].append(word)
    
    if result["has_banned"]:
        # 检查是否有上下文信号放过
        if has_context_signal(text):
            result["forgiven"] = True
            result["reason"] = "含有禁止词但有具体上下文信号，已放过"
        else:
            result["reason"] = "含有禁止词且无具体上下文信号"
    
    return result


# ============================================================
# 各检查器配置
# ============================================================

# G2检查器使用的全部正则模式（从L1_PATTERNS导入）
G2_PATTERNS = L1_PATTERNS.copy()

# G4/G7检查器使用的关键词列表（用于其他检查）
G4_KEYWORDS = L1_ABSOLUTE.copy()

# P7检查器只检查L1（更严格）
P7_CHECK_WORDS = L1_ABSOLUTE.copy()
