#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
铺垫健康度检查工具 - Setup Health Check Tool
检查铺垫负载、过期铺垫、健康度统计
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Windows 控制台编码修复
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 路径
tools_dir = Path(__file__).parent
workspace_dir = tools_dir.parent.parent.parent
story_dir = workspace_dir / "story"
canon_file = story_dir / "meta" / "canon_bible.json"

# 健康度阈值
THRESHOLDS = {
    "short": 10,   # 短期铺垫最多10个
    "medium": 15,  # 中期铺垫最多15个
    "long": 5,     # 长期铺垫最多5个
    "ongoing": 3   # 周期铺垫最多3个
}


def load_canon():
    """加载 canon_bible.json"""
    with open(canon_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def check_setup_health(canon, current_chapter=5):
    """检查铺垫健康度"""
    continuity = canon.get('continuity', {})
    
    # pending_setups 是 dict 列表，需要先提取 id
    pending_setups_list = continuity.get('pending_setups', [])
    if pending_setups_list and isinstance(pending_setups_list[0], dict):
        pending_ids = {s.get('id') for s in pending_setups_list}
    else:
        pending_ids = set(pending_setups_list)
    
    all_setups = continuity.get('setups', [])
    
    # 获取待处理的铺垫（完整对象）
    pending = [s for s in all_setups if s.get('id') in pending_ids]
    
    # 按类型分组
    by_type = {
        "short": [],
        "medium": [],
        "long": [],
        "ongoing": []
    }
    
    for s in pending:
        setup_type = s.get('type', 'medium')  # 默认中期
        by_type[setup_type].append(s)
    
    # 检查过载
    warnings = []
    
    for setup_type, setups in by_type.items():
        threshold = THRESHOLDS.get(setup_type, 10)
        if len(setups) > threshold:
            warnings.append(f"⚠️ {setup_type}类铺垫过载：{len(setups)}个（建议≤{threshold}）")
    
    # 检查过期铺垫
    expired = []
    for s in pending:
        payoff_range = s.get('expected_payoff_range')
        if payoff_range:
            max_chapter = payoff_range[1]
            if current_chapter > max_chapter + 5:  # 超过预期5章
                expired.append({
                    "id": s['id'],
                    "setup": s['setup'],
                    "expected": f"第{payoff_range[0]}-{payoff_range[1]}章",
                    "overdue": current_chapter - max_chapter
                })
    
    if expired:
        warnings.append(f"⚠️ 发现{len(expired)}个过期铺垫")
    
    # 健康度统计
    health = {
        "short": len(by_type["short"]),
        "medium": len(by_type["medium"]),
        "long": len(by_type["long"]),
        "ongoing": len(by_type["ongoing"]),
        "total": len(pending),
        "expired": len(expired),
        "last_check_chapter": current_chapter
    }
    
    return {
        "health": health,
        "by_type": by_type,
        "warnings": warnings,
        "expired": expired
    }


def print_report(result):
    """打印报告"""
    print("="*60)
    print("         铺垫健康度检查报告")
    print("="*60)
    
    health = result['health']
    print(f"\n📊 铺垫统计：")
    print(f"  短期铺垫（short）：{health['short']}个")
    print(f"  中期铺垫（medium）：{health['medium']}个")
    print(f"  长期铺垫（long）：{health['long']}个")
    print(f"  周期铺垫（ongoing）：{health['ongoing']}个")
    print(f"  ─────────────────────")
    print(f"  总计：{health['total']}个")
    print(f"  过期：{health['expired']}个")
    
    if result['warnings']:
        print(f"\n⚠️ 警告：")
        for w in result['warnings']:
            print(f"  {w}")
    else:
        print(f"\n✅ 铺垫负载健康")
    
    if result['expired']:
        print(f"\n🔴 过期铺垫详情：")
        for e in result['expired']:
            print(f"  [{e['id']}] {e['setup'][:30]}...")
            print(f"      预期：{e['expected']}，已过期{e['overdue']}章")
    
    print("\n" + "="*60)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='铺垫健康度检查')
    parser.add_argument('--chapter', type=int, default=5, help='当前章节号')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    args = parser.parse_args()
    
    canon = load_canon()
    result = check_setup_health(canon, args.chapter)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
