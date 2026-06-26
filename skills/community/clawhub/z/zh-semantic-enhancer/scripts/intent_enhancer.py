#!/usr/bin/env python3
"""
意图理解增强模块
Intent Enhancement Module
"""

from typing import Dict, Any, List


def enhance_intent(raw_intent: str, context: dict) -> Dict[str, Any]:
    """
    将原始意图 + 中文语义分析结果 → 结构化增强意图
    """
    # 1. 文本归一化
    normalized = normalize_chinese(raw_intent)
    
    # 2. 提取文化线索
    cultural_hints = extract_cultural_cues(raw_intent)
    
    # 3. 计算置信度
    confidence = calculate_confidence(raw_intent, context)
    
    # 4. 生成建议动作
    suggested_actions = generate_actions(raw_intent, context)
    
    return {
        "original": raw_intent,
        "normalized": normalized,
        "entities": context.get("entities", []),
        "expressions": context.get("expressions", []),
        "cultural_hints": cultural_hints,
        "confidence": confidence,
        "suggested_actions": suggested_actions
    }


def normalize_chinese(text: str) -> str:
    """
    中文文本归一化：繁简/口语/错别字归一
    """
    # 繁体转简体（简化映射）
    traditional_map = {
        "語": "语", "義": "义", "務": "务", "問": "问",
        "體": "体", "係": "系", "統": "统", "計": "计",
        "劃": "划", "處": "处", "學": "学", "習": "习"
    }
    
    result = text
    for trad, simp in traditional_map.items():
        result = result.replace(trad, simp)
    
    # 常见口语归一
    colloquial_map = {
        "啥": "什么",
        "咋": "怎么",
        "咋样": "怎么样",
        "行不": "可以吗",
        "成不": "可以吗",
        "好不": "好吗"
    }
    
    for collo, norm in colloquial_map.items():
        result = result.replace(collo, norm)
    
    return result


def extract_cultural_cues(text: str) -> List[str]:
    """
    提取文化线索
    """
    cues = []
    
    # 中式委婉表达
    euphemisms = {
        "考虑一下": "委婉拒绝",
        "研究研究": "拖延/不确定",
        "下次再说": "委婉拒绝",
        "随便": "需要对方决定",
        "都行": "随和/无偏好"
    }
    
    for phrase, meaning in euphemisms.items():
        if phrase in text:
            cues.append(f"{phrase} → {meaning}")
    
    # 敬语/礼貌用语
    polite_patterns = ["请", "谢谢", "麻烦", "不好意思", "打扰"]
    for pattern in polite_patterns:
        if pattern in text:
            cues.append(f"礼貌用语: {pattern}")
    
    return cues


def calculate_confidence(text: str, context: dict) -> float:
    """
    计算意图理解置信度
    """
    confidence = 0.8  # 基础置信度
    
    # 文本长度因子
    if len(text) < 5:
        confidence -= 0.1  # 太短可能信息不足
    elif len(text) > 50:
        confidence += 0.05  # 较长文本信息更丰富
    
    # 实体识别提升置信度
    if context.get("entities"):
        confidence += 0.05 * min(len(context["entities"]), 3)
    
    # 领域识别提升置信度
    if context.get("domain") != "general":
        confidence += 0.05
    
    # 特殊表达识别
    if context.get("expressions"):
        confidence += 0.03 * min(len(context["expressions"]), 2)
    
    return min(confidence, 1.0)


def generate_actions(text: str, context: dict) -> List[str]:
    """
    生成建议动作
    """
    actions = []
    
    # 根据领域生成建议
    domain = context.get("domain", "general")
    domain_actions = {
        "finance": ["查询相关数据", "分析市场趋势", "提供投资建议"],
        "medical": ["建议就医", "解释症状", "提供健康知识"],
        "legal": ["解释法律条款", "建议咨询律师", "提供案例参考"],
        "tech": ["提供技术方案", "解释技术概念", "推荐相关工具"]
    }
    
    if domain in domain_actions:
        actions.extend(domain_actions[domain][:2])
    
    # 根据意图类型生成建议
    if any(word in text for word in ["怎么", "如何", "怎样"]):
        actions.append("提供操作步骤说明")
    
    if any(word in text for word in ["为什么", "原因"]):
        actions.append("解释原因和背景")
    
    if any(word in text for word in ["推荐", "建议", "哪个"]):
        actions.append("提供对比和推荐")
    
    if not actions:
        actions.append("进一步询问以明确需求")
    
    return actions[:3]  # 最多返回3个建议


if __name__ == "__main__":
    # 测试
    test_cases = [
        {
            "text": "中文语义理解增强技能",
            "context": {"domain": "tech", "entities": []}
        },
        {
            "text": "我今天去了医院看病",
            "context": {"domain": "medical", "entities": [{"type": "TIME", "text": "今天"}]}
        }
    ]
    
    for case in test_cases:
        print(f"\n输入: {case['text']}")
        result = enhance_intent(case['text'], case['context'])
        print(f"归一化: {result['normalized']}")
        print(f"文化线索: {result['cultural_hints']}")
        print(f"置信度: {result['confidence']}")
        print(f"建议动作: {result['suggested_actions']}")
