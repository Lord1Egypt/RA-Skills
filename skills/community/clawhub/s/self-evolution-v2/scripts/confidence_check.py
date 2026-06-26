#!/usr/bin/env python3
"""
置信度校准辅助工具
帮助在使用"不确定"之前做L1/L2/L3分类

使用方式:
python confidence_check.py "我可能需要查一下"
"""

import sys

LEVELS = {
    "L1": {
        "name": "需要查细节",
        "action": "立即查细节，不开口",
        "examples": [
            "不确定是今天还是明天",
            "大概价格是100左右",
            "可能是3个选项"
        ]
    },
    "L2": {
        "name": "需要查来源",
        "action": "立即查来源，不开口",
        "examples": [
            "我记得是这样的",
            "可能是百度的数据",
            "应该是去年的报告"
        ]
    },
    "L3": {
        "name": "完全不知道",
        "action": "直接说'我需要研究'，不猜测",
        "examples": [
            "这个概念我没听过",
            "这个领域我不熟悉",
            "我不知道用什么工具"
        ]
    }
}

def analyze(text):
    text_lower = text.lower()
    
    # 检测是否说了不确定的话
    uncertain_words = ["可能", "大概", "应该", "不确定", "也许", "估计"]
    has_uncertain = any(w in text_lower for w in uncertain_words)
    
    if not has_uncertain:
        print("✅ 没有检测到不确定表达")
        return
    
    print(f"⚠️ 检测到不确定表达: {text}")
    print("\n分类检查：")
    
    # 检测L1信号（细节不确定）
    l1_signals = ["今天", "明天", "价格", "数量", "时间", "日期", "期号"]
    l1_detected = [s for s in l1_signals if s in text_lower]
    
    # 检测L2信号（来源不确定）
    l2_signals = ["记得", "据说", "应该是", "可能是", "百度的", "网上的"]
    l2_detected = [s for s in l2_signals if s in text_lower]
    
    if l1_detected:
        print(f"  → L1（需要查细节）: 检测到 {l1_detected}")
        print(f"  → 行动: {LEVELS['L1']['action']}")
    elif l2_detected:
        print(f"  → L2（需要查来源）: 检测到 {l2_detected}")
        print(f"  → 行动: {LEVELS['L2']['action']}")
    else:
        print(f"  → L3（完全不知道）")
        print(f"  → 行动: {LEVELS['L3']['action']}")
    
    print("\n建议：先去查证，再回答。")
    print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze(" ".join(sys.argv[1:]))
    else:
        print("用法: python confidence_check.py \"你的不确定表达\"")
        print("\n各层级示例：")
        for level, info in LEVELS.items():
            print(f"\n{level} - {info['name']}")
            print(f"  行动: {info['action']}")
            print(f"  示例: {info['examples'][0]}")
