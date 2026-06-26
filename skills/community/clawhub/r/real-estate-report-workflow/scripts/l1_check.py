#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 6 L1 层检查脚本 - v1.0
检查范围：十四项写作原则中 L1 可自动检测的项目
- 标题结构完整性
- 三段式标签覆盖率
- 缺失数据标记 [*]
- 禁止 emoji/图形符号（精确版）
- 禁止反问句
- 数据来源星级标注

使用方法：python3 scripts/l1_check.py <报告文件路径>
"""

import sys
import os
import re
from pathlib import Path

# Unicode Emoji 精确区间（只匹配真正的 emoji，不含中文标点）
EMOJI_RANGES = [
    (0x1F300, 0x1F9FF),   # 杂项符号 + 表情符号
    (0x2600, 0x26FF),     # 杂项符号（A部分）
    (0x2700, 0x27BF),     # 装饰符号
    (0x231A, 0x231B),     # 手表/沙漏
    (0x23E9, 0x23F3),     # 交通标志（部分）
    (0x23F8, 0x23FA),     # 体育符号（部分）
    (0x24C2, 0x24C2),     # circled latin capital letter m
    (0x25AA, 0x25AB),     # 小方块
    (0x25B6, 0x25B6),     # 实心三角形
    (0x25C0, 0x25C0),     # 实心三角形（反）
    (0x25FB, 0x25FE),     # 中性方块
    (0x2614, 0x2615),     # 雨伞/热饮
    (0x2617, 0x2617),     # 向上箭头
    (0x2619, 0x2619),     # 回转箭头
    (0x261A, 0x261F),     # 手指示志
    (0x2620, 0x2623),     # skull/janger
    (0x2624, 0x2625),     # 宗教符号
    (0x2626, 0x2626),     # 正交
    (0x262A, 0x262F),     # 宗教符号
    (0x2638, 0x263A),     # 星座/笑脸
    (0x2640, 0x2653),     # 性别符号
    (0x265F, 0x2660),     # 棋子符号
    (0x2661, 0x2665),     # 心形/音符
    (0x2668, 0x2668),     # 热气
    (0x2669, 0x267F),     # 音符/骰子/wheelchair
    (0x2690, 0x269C),     # 旗帜/其他符号
    (0x26A0, 0x2B55),     # warning/禁止/大圆
    (0x2B50, 0x2B55),     # star/大圆
    (0x3030, 0x3030),     # 波浪号
    (0x303D, 0x303D),     # 分数
    (0x3297, 0x3299),     # 日月/私/禁
    (0xFE0F, 0xFE0F),     # emoji variation selector
]


def is_emoji(char):
    """判断单个字符是否为 emoji（精确版）"""
    code = ord(char)
    for start, end in EMOJI_RANGES:
        if start <= code <= end:
            return True
    return False


def find_emojis_in_text(text):
    """提取文本中所有 emoji，返回列表"""
    emojis = []
    for char in text:
        if is_emoji(char):
            emojis.append(char)
    return emojis


def count_emojis(text):
    """统计 emoji 数量（精确版）"""
    return sum(1 for char in text if is_emoji(char))


def check_emojis(content):
    """检查禁止 emoji/图形符号"""
    emoji_count = count_emojis(content)
    if emoji_count == 0:
        return True, [], 0

    emojis_found = find_emojis_in_text(content)
    # 去重展示
    unique_emojis = list(dict.fromkeys(emojis_found))
    return False, unique_emojis[:20], emoji_count  # 最多显示20种


def check_three_part_tags(content):
    """检查三段式标签完整性"""
    required_tags = ['【核心观点】', '【论据支撑】', '【结论摘要】']
    found = {}
    for tag in required_tags:
        count = content.count(tag)
        found[tag] = count

    # 检查每个标签至少出现一次
    missing = [tag for tag, cnt in found.items() if cnt == 0]

    if missing:
        return False, found, missing
    return True, found, []


def check_missing_data_markers(content):
    """检查缺失数据标记 [*]"""
    # 查找所有 [*] 标记
    pattern = re.compile(r'\[\*\]\s*[^\n]*')
    matches = pattern.findall(content)
    return len(matches)


def check_source_stars(content):
    """检查数据来源星级标注（文字形式 ⭐⭐⭐⭐★）"""
    # 匹配 ⭐★ 组合，至少2个
    star_pattern = re.compile(r'[⭐★]{2,}')
    matches = star_pattern.findall(content)
    return len(matches)


def check_rhetorical_questions(content):
    """检查反问句"""
    # 匹配包含"吗？"、"么？"、"？"结尾且含有"难道"、"怎么"、"是否"等反问特征
    patterns = [
        r'难道[^？\n]*[吗么]？',
        r'[是否]真的[^？\n]*[吗么]？',
        r'[不没]是[吗么]？',
        r'[怎怎]么[能会]够[^？\n]*[？]',
        r'难道不[^？\n]*吗？',
        r'[难莫难]道[^？\n]*[吗么]？',
    ]
    found = []
    for p in patterns:
        matches = re.findall(p, content)
        found.extend(matches)
    return found[:10]  # 最多返回10个


def check_heading_structure(content):
    """检查标题层级结构（Markdown 格式）"""
    # 提取 ## 一级标题和 ### 二级标题
    h1_matches = re.findall(r'^#{1}\s+(.+)$', content, re.MULTILINE)
    h2_matches = re.findall(r'^#{2}\s+(.+)$', content, re.MULTILINE)
    h3_matches = re.findall(r'^#{3}\s+(.+)$', content, re.MULTILINE)

    # 检查是否有标题但无内容的情况
    lines = content.split('\n')
    structure_issues = []

    # 检查连续的无内容标题
    for i in range(len(lines) - 1):
        line = lines[i].strip()
        next_line = lines[i+1].strip() if i+1 < len(lines) else ''
        if line.startswith('#') and line.startswith('##') is False and next_line.startswith('#'):
            structure_issues.append(f"标题后直接跟标题（第{i+1}行）")

    return {
        'h1': len(h1_matches),
        'h2': len(h2_matches),
        'h3': len(h3_matches),
        'h1_titles': h1_matches[:5],
        'h2_titles': h2_matches[:5],
        'h3_titles': h3_matches[:3],
        'issues': structure_issues
    }


def run_l1_check(file_path):
    """执行 L1 基础层检查"""
    if not os.path.exists(file_path):
        # 尝试读取 Markdown 文件
        md_path = file_path.replace('.docx', '.md')
        if os.path.exists(md_path):
            file_path = md_path
        else:
            print(f"❌ 文件不存在：{file_path} 或 {md_path}")
            sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    total_chars = len(content)
    total_words = len(content.replace(' ', '').replace('\n', ''))

    print("=" * 60)
    print(f"L1 基础层检查")
    print(f"文件：{os.path.basename(file_path)}")
    print(f"总字符：{total_chars:,}  总汉字+数字：{total_words:,}")
    print("=" * 60)

    results = {}
    passed = 0
    failed = 0
    warnings = 0

    # 1. Emoji 检查
    emoji_pass, emoji_examples, emoji_count = check_emojis(content)
    results['emoji'] = {'pass': emoji_pass, 'count': emoji_count, 'examples': emoji_examples}
    if emoji_pass:
        print(f"✅ 禁止项检查（emoji）：0 个")
        passed += 1
    else:
        print(f"❌ 禁止项检查（emoji）：发现 {emoji_count} 个，以下为例：")
        for e in emoji_examples:
            print(f"   → {e}")
        failed += 1

    # 2. 三段式标签
    tag_pass, tag_counts, tag_missing = check_three_part_tags(content)
    results['three_part_tags'] = {'pass': tag_pass, 'counts': tag_counts, 'missing': tag_missing}
    if tag_pass:
        print(f"✅ 三段式标签：核心观点 {tag_counts['【核心观点】']} 处，论据支撑 {tag_counts['【论据支撑】']} 处，结论摘要 {tag_counts['【结论摘要】']} 处")
        passed += 1
    else:
        print(f"❌ 三段式标签缺失：{tag_missing}")
        failed += 1

    # 3. 缺失数据标记
    missing_count = check_missing_data_markers(content)
    results['missing_data_markers'] = missing_count
    print(f"ℹ️  缺失数据标记 [*]：{missing_count} 处")

    # 4. 数据来源星级
    star_count = check_source_stars(content)
    results['source_stars'] = star_count
    if star_count > 0:
        print(f"✅ 数据来源星级标注：{star_count} 处")
        passed += 1
    else:
        print(f"⚠️  数据来源星级标注：0 处（请确认是否需要标注）")
        warnings += 1

    # 5. 反问句检查
    rq_found = check_rhetorical_questions(content)
    results['rhetorical_questions'] = rq_found
    if len(rq_found) == 0:
        print(f"✅ 禁止项检查（反问句）：0 处")
        passed += 1
    else:
        print(f"❌ 反问句检查：发现 {len(rq_found)} 处，以下为例：")
        for q in rq_found[:3]:
            print(f"   → {q[:60]}")
        failed += 1

    # 6. 标题结构
    heading_info = check_heading_structure(content)
    results['heading_structure'] = heading_info
    print(f"ℹ️  标题结构：H1={heading_info['h1']} 个，H2={heading_info['h2']} 个，H3={heading_info['h3']} 个")
    if heading_info['h1'] >= 4:
        print(f"✅ H1 标题数量：{heading_info['h1']} 个")
        passed += 1
    else:
        print(f"❌ H1 标题数量不足：{heading_info['h1']} 个（建议≥4）")
        failed += 1

    print("=" * 60)

    # 汇总
    print(f"\n📊 L1 汇总：{passed} 项通过，{warnings} 项警告，{failed} 项失败")
    if failed > 0:
        print(f"⚠️  L1 未通过，请修正后再继续")
        return False, results
    else:
        print(f"✅ L1 基础层检查通过，继续 L2")
        return True, results


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 scripts/l1_check.py <报告文件路径(.md 或 .docx)>")
        print("示例：python3 scripts/l1_check.py reports/GZ_Intl_Textile_REITs_Report.md")
        sys.exit(1)

    passed, results = run_l1_check(sys.argv[1])
    sys.exit(0 if passed else 1)
