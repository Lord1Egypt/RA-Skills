#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
铺垫数据结构升级工具
1. 清理重复铺垫
2. 添加类型、预期章节、优先级等字段
3. 生成健康度报告
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict

# 铺垫分类规则
SETUP_CLASSIFICATION = {
    # 短期铺垫（1-5章内兑现）
    "short": {
        "keywords": ["手术费", "拍卖", "资金链", "竞拍", "债务", "借款", "商铺", "拍卖会"],
        "max_chapters": 5
    },
    # 中期铺垫（5-20章内兑现）
    "medium": {
        "keywords": ["债务真相", "证据", "林晚晴", "沈烬", "河桐计划", "动机", "关系"],
        "max_chapters": 20
    },
    # 长期铺垫（20+章兑现）
    "long": {
        "keywords": ["陈父", "系统来源", "真正目标", "文明", "规则制定"],
        "max_chapters": None
    },
    # 周期铺垫（持续作用）
    "ongoing": {
        "keywords": ["赵家", "势力", "好感度", "声誉", "关系网"],
        "max_chapters": None
    }
}

# 手动分类的铺垫（优先级最高）
MANUAL_CLASSIFICATION = {
    "setup_ch1_001": {"type": "medium", "expected_range": [10, 30], "priority": "high"},
    "setup_ch1_002": {"type": "long", "expected_range": [50, 100], "priority": "medium"},
    "setup_ch1_003": {"type": "medium", "expected_range": [8, 15], "priority": "medium"},
    "setup_ch1_004": {"type": "medium", "expected_range": [5, 15], "priority": "medium"},
    "setup_ch1_005": {"type": "short", "expected_range": [1, 5], "priority": "high"},
    "setup_ch1_006": {"type": "short", "expected_range": [1, 3], "priority": "high"},
    "setup_ch1_007": {"type": "medium", "expected_range": [3, 10], "priority": "medium"},
    "setup_ch1_008": {"type": "short", "expected_range": [2, 5], "priority": "high"},
    "setup_ch1_009": {"type": "ongoing", "expected_range": None, "priority": "medium"},
    "setup_ch1_010": {"type": "short", "expected_range": [1, 3], "priority": "high"},
    
    "setup_ch2_001": {"type": "medium", "expected_range": [5, 15], "priority": "high"},
    "setup_ch2_002": {"type": "medium", "expected_range": [8, 20], "priority": "high"},
    "setup_ch2_003": {"type": "long", "expected_range": [50, 100], "priority": "medium"},
    "setup_ch2_004": {"type": "long", "expected_range": [100, 200], "priority": "medium"},
    "setup_ch2_005": {"type": "medium", "expected_range": [10, 30], "priority": "medium"},
    "setup_ch2_006": {"type": "long", "expected_range": [50, 100], "priority": "medium"},
    "setup_ch2_007": {"type": "long", "expected_range": [100, 200], "priority": "high"},
    "setup_ch2_008": {"type": "long", "expected_range": [50, 100], "priority": "high"},
    "setup_ch2_009": {"type": "medium", "expected_range": [5, 15], "priority": "high"},
    "setup_ch2_010": {"type": "medium", "expected_range": [10, 30], "priority": "medium"},
    "setup_ch2_011": {"type": "long", "expected_range": [50, 100], "priority": "high"},
    
    "setup_ch3_001": {"type": "short", "expected_range": [3, 10], "priority": "medium"},
    "setup_ch3_002": {"type": "medium", "expected_range": [10, 30], "priority": "medium"},
    "setup_ch3_003": {"type": "short", "expected_range": [1, 5], "priority": "high"}
}


def classify_setup(setup: Dict[str, Any]) -> Dict[str, Any]:
    """对铺垫进行分类"""
    setup_id = setup.get('id', '')
    setup_text = setup.get('setup', '')
    chapter = setup.get('chapter', 1)
    
    # 1. 优先使用手动分类
    if setup_id in MANUAL_CLASSIFICATION:
        manual = MANUAL_CLASSIFICATION[setup_id]
        return {
            **setup,
            "type": manual["type"],
            "expected_payoff_range": manual["expected_range"],
            "priority": manual["priority"],
            "status": "active",
            "related_characters": extract_characters(setup_text),
            "tags": extract_tags(setup_text)
        }
    
    # 2. 自动分类
    for setup_type, config in SETUP_CLASSIFICATION.items():
        for keyword in config["keywords"]:
            if keyword in setup_text:
                expected_range = None
                if config["max_chapters"]:
                    expected_range = [chapter, chapter + config["max_chapters"]]
                
                return {
                    **setup,
                    "type": setup_type,
                    "expected_payoff_range": expected_range,
                    "priority": "medium",
                    "status": "active",
                    "related_characters": extract_characters(setup_text),
                    "tags": extract_tags(setup_text)
                }
    
    # 3. 默认分类为中期
    return {
        **setup,
        "type": "medium",
        "expected_payoff_range": [chapter, chapter + 20],
        "priority": "medium",
        "status": "active",
        "related_characters": extract_characters(setup_text),
        "tags": extract_tags(setup_text)
    }


def extract_characters(text: str) -> List[str]:
    """提取相关角色"""
    characters = ["陈安", "林晚晴", "赵天赐", "沈烬", "李成", "陈父", "赵老爷子"]
    found = []
    for char in characters:
        if char in text:
            found.append(char)
    return found


def extract_tags(text: str) -> List[str]:
    """提取标签"""
    tags = []
    tag_keywords = {
        "资金": ["资金", "钱", "债务", "拍卖"],
        "悬疑": ["秘密", "真相", "证据", "调查"],
        "人物": ["林晚晴", "沈烬", "赵天赐"],
        "系统": ["系统", "概率", "能力"]
    }
    
    for tag, keywords in tag_keywords.items():
        for keyword in keywords:
            if keyword in text:
                tags.append(tag)
                break
    
    return tags


def remove_duplicates(setups: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """移除重复的铺垫"""
    seen_ids = set()
    unique_setups = []
    
    for setup in setups:
        setup_id = setup.get('id', '')
        if setup_id not in seen_ids:
            seen_ids.add(setup_id)
            unique_setups.append(setup)
    
    return unique_setups


def calculate_health(setups: List[Dict[str, Any]], current_chapter: int = 5) -> Dict[str, Any]:
    """计算铺垫健康度"""
    by_type = defaultdict(int)
    expired = []
    
    for setup in setups:
        setup_type = setup.get('type', 'medium')
        by_type[setup_type] += 1
        
        # 检查是否过期
        expected = setup.get('expected_payoff_range')
        if expected and expected[1]:
            if current_chapter > expected[1] + 5:
                expired.append(setup['id'])
    
    return {
        "short": by_type['short'],
        "medium": by_type['medium'],
        "long": by_type['long'],
        "ongoing": by_type['ongoing'],
        "total": len(setups),
        "expired_count": len(expired),
        "expired_ids": expired,
        "last_check_chapter": current_chapter,
        "warnings": generate_warnings(by_type, len(expired))
    }


def generate_warnings(by_type: Dict[str, int], expired_count: int) -> List[str]:
    """生成警告信息"""
    warnings = []
    
    if by_type['short'] > 10:
        warnings.append(f"⚠️ 短期铺垫过多：{by_type['short']}个（建议≤10）")
    
    if by_type['medium'] > 15:
        warnings.append(f"⚠️ 中期铺垫过多：{by_type['medium']}个（建议≤15）")
    
    if by_type['long'] > 5:
        warnings.append(f"⚠️ 长期铺垫过多：{by_type['long']}个（建议≤5）")
    
    if expired_count > 0:
        warnings.append(f"⚠️ 发现{expired_count}个过期铺垫")
    
    return warnings


def main():
    """主函数"""
    canon_file = Path(r'C:\Users\huang\.openclaw\workspace\story\meta\canon_bible.json')
    
    # 读取数据
    with open(canon_file, 'r', encoding='utf-8') as f:
        canon = json.load(f)
    
    print("="*70)
    print("铺垫数据结构升级工具")
    print("="*70)
    
    # 1. 清理重复
    print("\n[1/4] 清理重复铺垫...")
    original_count = len(canon['continuity']['setups'])
    canon['continuity']['setups'] = remove_duplicates(canon['continuity']['setups'])
    new_count = len(canon['continuity']['setups'])
    print(f"  原始数量: {original_count}")
    print(f"  清理后: {new_count}")
    print(f"  删除重复: {original_count - new_count}")
    
    # 2. 分类和增强
    print("\n[2/4] 分类和增强铺垫...")
    classified_setups = []
    for setup in canon['continuity']['setups']:
        classified = classify_setup(setup)
        classified_setups.append(classified)
    
    canon['continuity']['setups'] = classified_setups
    
    # 统计分类结果
    by_type = defaultdict(int)
    for setup in classified_setups:
        by_type[setup['type']] += 1
    
    print(f"  短期铺垫: {by_type['short']}个")
    print(f"  中期铺垫: {by_type['medium']}个")
    print(f"  长期铺垫: {by_type['long']}个")
    print(f"  周期铺垫: {by_type['ongoing']}个")
    
    # 3. 更新 pending_setups（动态计算）
    print("\n[3/4] 更新 pending_setups...")
    payoff_ids = {p.get('original_setup', p.get('id')) for p in canon['continuity'].get('payoffs', [])}
    canon['continuity']['pending_setups'] = [
        s for s in canon['continuity']['setups']
        if s['id'] not in payoff_ids
    ]
    print(f"  未兑现铺垫: {len(canon['continuity']['pending_setups'])}个")
    
    # 4. 计算健康度
    print("\n[4/4] 计算铺垫健康度...")
    health = calculate_health(canon['continuity']['pending_setups'], current_chapter=5)
    canon['continuity']['setup_health'] = health
    
    print(f"  总数: {health['total']}")
    print(f"  过期铺垫: {health['expired_count']}个")
    if health['warnings']:
        print("  警告:")
        for warning in health['warnings']:
            print(f"    {warning}")
    
    # 保存
    with open(canon_file, 'w', encoding='utf-8') as f:
        json.dump(canon, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*70)
    print("✅ 升级完成！")
    print("="*70)
    
    # 输出报告
    print("\n📊 铺垫统计报告:")
    print(f"  总铺垫数: {len(canon['continuity']['setups'])}")
    print(f"  已兑现: {len(canon['continuity']['payoffs'])}")
    print(f"  未兑现: {len(canon['continuity']['pending_setups'])}")
    print(f"  健康度: {'良好' if not health['warnings'] else '需要注意'}")


if __name__ == "__main__":
    main()
