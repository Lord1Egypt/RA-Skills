#!/usr/bin/env python3
"""
FMEA 风险优先数(RPN)计算器
基于2019版FMEA标准，支持S/O/D评分与风险等级评估
"""

import argparse
import json
import sys

# 风险等级阈值
RISK_LEVELS = {
    "低": (1, 20),
    "中": (21, 60),
    "高": (61, 100),
    "很高": (101, 200),
    "极高": (201, 1000)
}

# 严重度评价标准
SEVERITY_GUIDE = {
    (9, 10): "极高-危害安全/法规违反，必须立即处理",
    (7, 8): "高-系统功能丧失，可能影响安全",
    (5, 6): "中-性能下降，用户体验受影响",
    (3, 4): "低-轻微不便，可接受",
    (1, 2): "极低-几乎无影响"
}

# 发生度评价标准
OCCURRENCE_GUIDE = {
    (9, 10): "极高-几乎必然发生",
    (7, 8): "高-频繁发生",
    (5, 6): "中-偶尔发生",
    (3, 4): "低-很少发生",
    (1, 2): "极低-罕见，几乎不发生"
}

# 探测度评价标准
DETECTION_GUIDE = {
    (9, 10): "极低-几乎无法探测",
    (7, 8): "低-探测困难",
    (5, 6): "中-中等探测难度",
    (3, 4): "较高-容易探测",
    (1, 2): "高-几乎肯定能探测"
}


def get_risk_level(rpn):
    """根据RPN值确定风险等级"""
    for level, (low, high) in RISK_LEVELS.items():
        if low <= rpn <= high:
            return level
    return "极高"


def get_action_priority(severity, occurrence, detection):
    """根据评分给出优化优先级建议"""
    suggestions = []
    
    # 严重度最高优先
    if severity >= 8:
        suggestions.append("【紧急】严重度过高，考虑重新设计")
    elif severity >= 6:
        suggestions.append("【高优先级】评估是否可以降低失效后果")
    
    # 发生频率次之
    if occurrence >= 8:
        suggestions.append("【高优先级】优先降低发生频率")
    elif occurrence >= 6:
        suggestions.append("【中优先级】考虑预防措施减少失效发生")
    
    # 探测难度
    if detection >= 8:
        suggestions.append("【高优先级】改善探测手段，及早发现问题")
    elif detection >= 6:
        suggestions.append("【中优先级】评估现有探测方法的有效性")
    
    if not suggestions:
        suggestions.append("当前评分可接受，持续监控")
    
    return suggestions


def get_scoring_guide():
    """返回完整评分指南"""
    return {
        "severity": SEVERITY_GUIDE,
        "occurrence": OCCURRENCE_GUIDE,
        "detection": DETECTION_GUIDE
    }


def calculate_rpn(severity, occurrence, detection):
    """
    计算RPN并返回完整评估结果
    
    Args:
        severity: 严重度 (1-10)
        occurrence: 发生度 (1-10)
        detection: 探测度 (1-10)
    
    Returns:
        dict: 包含RPN、风险等级、评分说明等
    """
    # 验证输入范围
    for name, value in [("严重度", severity), ("发生度", occurrence), ("探测度", detection)]:
        if not 1 <= value <= 10:
            raise ValueError(f"{name}必须在1-10之间，当前值: {value}")
    
    rpn = severity * occurrence * detection
    risk_level = get_risk_level(rpn)
    priorities = get_action_priority(severity, occurrence, detection)
    
    # 查找评分对应的评价
    sev_desc = next((desc for (low, high), desc in SEVERITY_GUIDE.items() 
                    if low <= severity <= high), "")
    occ_desc = next((desc for (low, high), desc in OCCURRENCE_GUIDE.items() 
                    if low <= occurrence <= high), "")
    det_desc = next((desc for (low, high), desc in DETECTION_GUIDE.items() 
                    if low <= detection <= high), "")
    
    return {
        "rpn": rpn,
        "risk_level": risk_level,
        "severity": {
            "value": severity,
            "description": sev_desc
        },
        "occurrence": {
            "value": occurrence,
            "description": occ_desc
        },
        "detection": {
            "value": detection,
            "description": det_desc
        },
        "action_priorities": priorities,
        "recommendation": "立即采取行动" if risk_level in ["很高", "极高"] else
                          "需要改善" if risk_level == "高" else
                          "建议改善" if risk_level == "中" else
                          "可接受"
    }


def main():
    parser = argparse.ArgumentParser(description="FMEA RPN计算器")
    parser.add_argument("--action", choices=["calculate", "guide"], default="calculate",
                        help="操作类型: calculate(计算RPN) 或 guide(评分指南)")
    parser.add_argument("--severity", type=int, choices=range(1, 11), 
                        help="严重度S (1-10)")
    parser.add_argument("--occurrence", type=int, choices=range(1, 11),
                        help="发生度O (1-10)")
    parser.add_argument("--detection", type=int, choices=range(1, 11),
                        help="探测度D (1-10)")
    
    args = parser.parse_args()
    
    if args.action == "guide":
        result = get_scoring_guide()
    else:
        if args.severity is None or args.occurrence is None or args.detection is None:
            print(json.dumps({"error": "计算RPN需要提供 --severity, --occurrence, --detection 参数"}, 
                           ensure_ascii=False, indent=2))
            sys.exit(1)
        try:
            result = calculate_rpn(args.severity, args.occurrence, args.detection)
        except ValueError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False, indent=2))
            sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
