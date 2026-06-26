#!/usr/bin/env python3
"""
质量门控脚本
用于评估 Agent 输出质量，拦截低质量内容
"""

import re
from typing import Dict, Any


def evaluate_output(output_text: str, context: Dict[str, Any] = None) -> float:
    """
    评估输出质量
    
    Args:
        output_text: Agent 输出的文本
        context: 上下文信息（可选）
    
    Returns:
        float: 质量分数 (0-10)
    """
    if not output_text or len(output_text.strip()) < 10:
        return 0.0
    
    score = 10.0
    
    # 1. 准确性检查（基础规则）
    # 检查是否有明显的错误标记
    if "错误" in output_text or "失败" in output_text:
        if "成功" not in output_text:
            score -= 2.0
    
    # 2. 完整性检查
    # 检查是否有未完成的句子
    if output_text.endswith("...") or output_text.endswith("…"):
        score -= 1.0
    
    # 检查是否过短（可能不完整）
    if len(output_text.strip()) < 50:
        score -= 1.5
    
    # 3. 可读性检查
    # 检查是否有过多的特殊字符
    special_chars = len(re.findall(r'[^\w\s\u4e00-\u9fff]', output_text))
    if special_chars > len(output_text) * 0.3:
        score -= 1.0
    
    # 检查是否有重复内容
    lines = output_text.split('\n')
    unique_lines = set(lines)
    if len(lines) > 5 and len(unique_lines) < len(lines) * 0.7:
        score -= 1.5
    
    # 4. 安全性检查
    # 检查是否包含敏感信息泄露
    sensitive_patterns = [
        r'sk-[a-zA-Z0-9]{48}',  # API keys
        r'password\s*[:=]\s*\S+',  # 密码
        r'\d{15,19}',  # 信用卡号
    ]
    for pattern in sensitive_patterns:
        if re.search(pattern, output_text, re.IGNORECASE):
            score -= 3.0
            break
    
    # 5. 内容质量检查
    # 检查是否只是简单的确认或无意义回复
    meaningless_patterns = [
        r'^(好的|OK|知道了|收到|明白了)[\s\.\!！]*$',
        r'^NO_REPLY$',
    ]
    for pattern in meaningless_patterns:
        if re.match(pattern, output_text.strip(), re.IGNORECASE):
            score -= 2.0
            break
    
    # 确保分数在 0-10 范围内
    return max(0.0, min(10.0, score))


def should_block(score: float, threshold: float = 7.0) -> bool:
    """
    判断是否应该拦截输出
    
    Args:
        score: 质量分数
        threshold: 阈值（默认 7.0）
    
    Returns:
        bool: True 表示应该拦截
    """
    return score < threshold


def get_quality_label(score: float) -> str:
    """
    获取质量标签
    
    Args:
        score: 质量分数
    
    Returns:
        str: 质量标签
    """
    if score >= 9:
        return "优秀"
    elif score >= 8:
        return "良好"
    elif score >= 7:
        return "合格"
    elif score >= 5:
        return "待改进"
    else:
        return "不合格"


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("这是一个完整的、有意义的回复，包含了足够的信息和上下文。", None),
        ("错误", None),
        ("好的", None),
        ("sk-1234567890abcdefghijklmnopqrstuvwxyz1234567890", None),
        ("这是一个很长的回复，包含了很多有用的信息，并且格式清晰，逻辑连贯，没有明显的错误或问题。", None),
    ]
    
    for text, context in test_cases:
        score = evaluate_output(text, context)
        label = get_quality_label(score)
        blocked = should_block(score)
        print(f"文本: {text[:50]}...")
        print(f"分数: {score:.1f}/10 ({label})")
        print(f"拦截: {'是' if blocked else '否'}")
        print()
