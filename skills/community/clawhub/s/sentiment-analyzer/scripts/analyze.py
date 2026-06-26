#!/usr/bin/env python3
"""
情感分析器 - 客服场景文本情绪分析
基于本地规则引擎，无需外部 API
"""

import sys
import json
import re

# 负面情绪关键词
NEGATIVE_WORDS = [
    "垃圾", "废物", "没用", "差劲", "烂", "讨厌", "恶心", "滚", "白痴",
    "骗", "骗子", "欺诈", "坑", "坑人", "黑心", "无良",
    "退款", "退货", "投诉", "举报", "曝光", "差评",
    "失望", "绝望", "崩溃", "愤怒", "生气", "恼火",
    "太慢", "等太久", "效率低", "不专业", "敷衍",
    "不管", "不理", "推诿", "踢皮球", "搪塞",
    "虚假", "欺骗", "隐瞒", "欺骗", "货不对板",
    "质量问题", "坏了", "没用", "故障", "Bug",
    "要投诉", "要举报", "要曝光", "要差评", "要退款",
    "不满意", "不靠谱", "不行", "垃圾", "骗子",
    "怒", "烦", "急", "气", "躁",
    "简直", "太过分", "忍不了", "忍无可忍",
    "凭什么", "为什么", "怎么这样", "太过分了",
    "你们", "你们公司", "店家", "商家",
]

# 敏感词（需告警）
SENSITIVE_WORDS = [
    "傻逼", "智障", "脑残", "死全家", "畜生", "去死", "妈的",
    "fuck", "shit", "bitch", "asshole", "sucks",
    "骗子", "诈骗", "非法", "举报", "报警", "起诉",
]

# 焦虑情绪关键词
ANXIOUS_WORDS = [
    "急", "赶紧", "马上", "立刻", "什么时候", "多久",
    "怎么还没", "怎么还没到", "怎么还没来",
    "催", "催促", "超时", "过期", "失效",
    "担心", "怕", "慌张", "不安", "着急",
    "能解决吗", "能修好吗", "能退吗", "可以吗",
]

# 满意情绪关键词
SATISFIED_WORDS = [
    "谢谢", "感谢", "不错", "挺好", "满意", "喜欢",
    "靠谱", "专业", "负责", "高效", "棒", "厉害",
    "很好", "非常好", "超赞", "五星", "好评",
    "帮了大忙", "解决了", "很及时", "态度好",
    "比预期", "超出预期", "惊喜", "感动",
]

# 热情情绪关键词
ENTHUSIASTIC_WORDS = [
    "太棒了", "太厉害了", "太强了", "绝了", "无敌",
    "疯狂打call", "疯狂推荐", "必须点赞", "满分",
    "超级喜欢", "超级满意", "绝对好评", "强烈推荐",
    "真香", "绝了绝了", "牛", "太牛了",
]

# 强烈否定关键词
STRONG_NEGATION = [
    "绝不", "永远不会", "再也不", "绝不再",
    "垃圾", "骗子", "黑店",
]

# 告警关键词
ALERT_TRIGGERS = [
    "投诉", "举报", "曝光", "媒体", "12315",
    "警察", "法院", "起诉", "律师",
    "退款", "赔偿", "赔钱", "赔我",
]


def analyze(text: str) -> dict:
    """分析文本情绪"""
    text_lower = text.lower().strip()

    # 检测敏感词
    sensitive_found = [w for w in SENSITIVE_WORDS if w in text_lower]

    # 检测负面词
    negative_found = [w for w in NEGATIVE_WORDS if w in text_lower]

    # 检测焦虑词
    anxious_found = [w for w in ANXIOUS_WORDS if w in text_lower]

    # 检测满意词
    satisfied_found = [w for w in SATISFIED_WORDS if w in text_lower]

    # 检测热情词
    enthusiastic_found = [w for w in ENTHUSIASTIC_WORDS if w in text_lower]

    # 检测强烈否定
    negation_found = [w for w in STRONG_NEGATION if w in text_lower]

    # 检测告警触发词
    alert_triggers = [w for w in ALERT_TRIGGERS if w in text_lower]

    # 计算情绪得分
    score = 0.0
    score += len(satisfied_found) * 0.2
    score += len(enthusiastic_found) * 0.3
    score -= len(negative_found) * 0.25
    score -= len(anxious_found) * 0.15
    score -= len(sensitive_found) * 0.5
    score -= len(negation_found) * 0.4
    score = max(-1.0, min(1.0, score))

    # 判断情绪类别
    if sensitive_found or len(negative_found) >= 2:
        sentiment = "angry"
    elif negation_found:
        sentiment = "angry"
    elif anxious_found and not satisfied_found:
        sentiment = "anxious"
    elif enthusiastic_found:
        sentiment = "enthusiastic"
    elif satisfied_found:
        sentiment = "satisfied"
    else:
        sentiment = "neutral"

    # 告警判断
    alert = bool(sensitive_found) or bool(alert_triggers) or (sentiment == "angry" and score < -0.5)

    alert_reason = ""
    if sensitive_found:
        alert_reason = "检测到敏感词"
    elif alert_triggers:
        alert_reason = f"检测到告警触发词: {', '.join(alert_triggers[:3])}"
    elif sentiment == "angry" and score < -0.5:
        alert_reason = "情绪极负面，需要人工介入"

    # 回复语气
    reply_tone_map = {
        "angry": "apologetic",
        "anxious": "calm",
        "neutral": "neutral",
        "satisfied": "positive",
        "enthusiastic": "enthusiastic",
    }
    reply_tone = reply_tone_map[sentiment]

    return {
        "sentiment": sentiment,
        "score": round(score, 2),
        "keywords": negative_found + anxious_found + satisfied_found + enthusiastic_found,
        "sensitive_words": sensitive_found,
        "alert": alert,
        "alert_reason": alert_reason,
        "reply_tone": reply_tone,
        "input_length": len(text),
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "请传入要分析的文本"}, ensure_ascii=False))
        sys.exit(1)

    text = " ".join(sys.argv[1:])
    result = analyze(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()