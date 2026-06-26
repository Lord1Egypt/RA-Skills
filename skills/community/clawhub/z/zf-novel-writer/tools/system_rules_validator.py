#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
系统规则验证工具 v3.0
检查章节是否符合新系统定义（基于定位和核心能力）
不再验证返还倍率和每日限额（已废弃）
"""

import sys
import os
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class SystemLevelRules:
    """新系统规则（基于定位和核心能力）"""

    # 系统等级定义
    LEVEL_RULES = {
        1: {
            'level': '青铜',
            'position': '概率观察者',
            'chapter_range': (1, 500),
            'era': 1
        },
        2: {
            'level': '白银',
            'position': '概率干预者',
            'chapter_range': (501, 1000),
            'era': 2
        },
        3: {
            'level': '黄金',
            'position': '因果分析者',
            'chapter_range': (1001, 1500),
            'era': 3
        },
        4: {
            'level': '铂金',
            'position': '时间线观察者',
            'chapter_range': (1501, 2000),
            'era': 4
        },
        5: {
            'level': '钻石',
            'position': '规则干扰者',
            'chapter_range': (2001, 2500),
            'era': 5
        },
        6: {
            'level': '王者',
            'position': '因果操盘者',
            'chapter_range': (2501, 3000),
            'era': 6
        },
        7: {
            'level': '至尊',
            'position': '纪元操盘者',
            'chapter_range': (3001, 3500),
            'era': 7
        },
        8: {
            'level': '主宰',
            'position': '时间结构干预者',
            'chapter_range': (3501, 4000),
            'era': 8
        }
    }

    @classmethod
    def get_level_by_chapter(cls, chapter_num: int) -> Dict[str, Any]:
        """根据章节号获取等级信息"""
        for level_info in cls.LEVEL_RULES.values():
            start, end = level_info['chapter_range']
            if start <= chapter_num <= end:
                return level_info
        return None

    @classmethod
    def get_era_by_chapter(cls, chapter_num: int) -> int:
        """根据章节号获取纪元编号"""
        level_info = cls.get_level_by_chapter(chapter_num)
        return level_info['era'] if level_info else 1


def load_canon_bible(canon_file: Path) -> Dict[str, Any]:
    """加载 canon_bible.json"""
    if not canon_file.exists():
        return {}

    try:
        with open(canon_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 加载 {canon_file} 失败: {e}")
        return {}


def parse_chapter_file(file_path: Path) -> Tuple[Dict[str, Any], str]:
    """解析章节文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取章节号
        chapter_match = None
        for line in content.split('\n')[:10]:
            if 'chapter-' in line.lower() or '第' in line and '章' in line:
                m = re.search(r'[第](\d+)[章]|chapter[ -](\d+)', line, re.IGNORECASE)
                if m:
                    chapter_num = int(m.group(1) if m.group(1) else m.group(2))
                    chapter_match = chapter_num
                    break

        if not chapter_match:
            return None, "无法提取章节号"

        # 提取系统级别（如果章节中包含）
        level_match = re.search(r'系统(等级|级别)[：:]\s*([^\n章]+)', content)
        system_level = level_match.group(2).strip() if level_match else None

        return {
            'chapter_number': chapter_match,
            'system_level': system_level,
            'content': content
        }, None

    except Exception as e:
        return None, f"解析文件失败: {e}"


def validate_system_rules(
    chapter_data: Dict[str, Any],
    canon_data: Dict[str, Any],
    story_dir: Path
) -> Tuple[List[str], List[str]]:
    """验证系统规则"""
    issues = []
    warnings = []
    chapter_number = chapter_data['chapter_number']
    system_level = chapter_data.get('system_level')

    # 1. 验证等级是否正确
    expected_level_info = SystemLevelRules.get_level_by_chapter(chapter_number)
    if not expected_level_info:
        issues.append(f"[ERROR] 章节{chapter_number}不在任何等级范围内")
        return issues, warnings

    expected_level = expected_level_info['level']
    expected_position = expected_level_info['position']

    if system_level and expected_level not in system_level:
        issues.append(f"[ERROR] 等级错误: 第{chapter_number}章应该是{expected_level}，但写的是{system_level}")

    # 2. 验证 canon_bible.json 中的定义
    eras = canon_data.get('eras', [])
    era_from_canon = None
    for era in eras:
        chapters = era.get('chapters', '')
        if '-' in chapters:
            start, end = map(int, chapters.split('-'))
            if start <= chapter_number <= end:
                era_from_canon = era
                break

    if era_from_canon:
        canon_level = era_from_canon.get('level')
        canon_position = era_from_canon.get('position')
        canon_core_ability = era_from_canon.get('core_ability')

        # 验证 canon 中的 level 是否与预期一致
        if canon_level != expected_level:
            issues.append(f"[ERROR] canon_bible.json 中的 level 不匹配: 期望 {expected_level}，实际 {canon_level}")

        # 验证 canon 中的 position 是否与预期一致
        if canon_position != expected_position:
            issues.append(f"[ERROR] canon_bible.json 中的 position 不匹配: 期望 {expected_position}，实际 {canon_position}")

        # 检查是否有旧字段（multiplier, daily_limit）
        if 'multiplier' in era_from_canon:
            warnings.append(f"[WARN] canon_bible.json 中存在旧字段 'multiplier'，建议删除")
        if 'daily_limit' in era_from_canon:
            warnings.append(f"[WARN] canon_bible.json 中存在旧字段 'daily_limit'，建议删除")

    # 3. 验证 LEVEL_*.md 文件是否存在
    level_mapping = {
        '青铜': 'BRONZE', '白银': 'SILVER', '黄金': 'GOLD',
        '铂金': 'PLATINUM', '钻石': 'DIAMOND', '王者': 'KING',
        '至尊': 'SUPREME', '主宰': 'LORD'
    }
    level_en = level_mapping.get(expected_level, 'BRONZE')
    level_file = story_dir / f"LEVEL_{level_en}.md"

    if not level_file.exists():
        issues.append(f"[ERROR] 等级定义文件不存在: {level_file}")
    else:
        # 验证 LEVEL_*.md 文件内容是否包含正确的定位
        try:
            with open(level_file, 'r', encoding='utf-8') as f:
                level_content = f.read()

            if expected_position not in level_content:
                warnings.append(f"[WARN] LEVEL_{level_en}.md 中未找到定位 '{expected_position}'")

            # 检查是否包含旧系统关键词
            old_keywords = ['返还倍率', '每日限额', '日限额']
            for keyword in old_keywords:
                if keyword in level_content:
                    warnings.append(f"[WARN] LEVEL_{level_en}.md 中包含旧系统关键词 '{keyword}'")

        except Exception as e:
            warnings.append(f"[WARN] 无法读取 {level_file}: {e}")

    return issues, warnings


def validate_and_report(
    file_path: Path,
    canon_file: Path,
    story_dir: Path
) -> bool:
    """验证并报告"""
    chapter_data, error = parse_chapter_file(file_path)

    if error:
        print(f"错误: {error}")
        return False

    # 加载 canon_bible.json
    canon_data = load_canon_bible(canon_file)

    issues, warnings = validate_system_rules(chapter_data, canon_data, story_dir)

    print(f"\n{'='*60}")
    print(f"系统规则验证 - 第{chapter_data['chapter_number']}章")
    print(f"{'='*60}")

    expected_level_info = SystemLevelRules.get_level_by_chapter(chapter_data['chapter_number'])
    if expected_level_info:
        print(f"系统等级: {expected_level_info['level']}")
        print(f"系统定位: {expected_level_info['position']}")

    if chapter_data.get('system_level'):
        print(f"章节中的等级: {chapter_data['system_level']}")

    if issues:
        print(f"\n发现 {len(issues)} 个错误:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
    else:
        print(f"\n✅ 规则验证通过")

    if warnings:
        print(f"\n发现 {len(warnings)} 个警告:")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")

    print(f"{'='*60}\n")

    return len(issues) == 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python system_rules_validator.py <章节文件>")
        print("示例: python system_rules_validator.py chapter-1_xxx.txt")
        sys.exit(1)

    # 路径设置
    tools_dir = Path(__file__).parent
    workspace_dir = tools_dir.parent.parent.parent
    story_dir = workspace_dir / "story"
    canon_file = story_dir / "meta" / "canon_bible.json"

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(f"文件不存在: {file_path}")
        sys.exit(1)

    success = validate_and_report(file_path, canon_file, story_dir)
    sys.exit(0 if success else 1)
