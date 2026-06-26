#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 6 L2 层检查脚本 - v1.0
检查范围：
- 数字一致性：同一数字在全文不同位置出现时是否一致
- 关键数据范围合理性：数值是否在常识范围内

使用方法：python3 scripts/l2_check.py <报告文件路径>
"""

import sys
import os
import re
from pathlib import Path


def extract_all_numbers(content):
    """从文本中提取所有数字及其上下文，返回列表"""
    # 匹配数字（支持整数、小数、负数、百分比、千分号）
    pattern = re.compile(
        r'(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?)\s*'  # 千分号格式：12,345.67
        r'|(-?\d+\.\d+%)\s*'                    # 百分比：3.5%
        r'|(-?\d+(?:\.\d+)?)\s*(?:元|万元|亿元|万|亿|㎡|平方米|公顷|公里|%|[^a-zA-Z\u4e00-\u9fff])',
        re.UNICODE
    )

    matches = []
    lines = content.split('\n')
    for line_no, line in enumerate(lines, 1):
        for m in pattern.finditer(line):
            num_str = m.group().strip()
            # 排除年份（通常是4位数字）
            if re.match(r'^[12]\d{3}$', num_str):
                continue
            # 排除行号、页码等
            if len(num_str) <= 3:
                continue
            # 上下文：取前后50字
            start = max(0, m.start() - 30)
            end = min(len(line), m.end() + 30)
            context = line[start:end]
            matches.append({
                'number': num_str,
                'line': line_no,
                'context': context
            })
    return matches


def group_numbers_by_value(matches):
    """将相同数值的数字归组"""
    groups = {}
    for m in matches:
        # 标准化数值（去掉逗号）
        key = m['number'].replace(',', '')
        if key not in groups:
            groups[key] = []
        groups[key].append(m)
    return groups


def check_number_consistency(groups):
    """检查同一数值在不同位置是否一致"""
    issues = []
    for value, occurrences in groups.items():
        if len(occurrences) < 2:
            continue
        # 检查是否有明显不同的上下文（可能不是同一个指标）
        contexts = [o['context'] for o in occurrences]
        # 如果上下文中有不同的关键词，说明可能不是同一个指标
        keywords = []
        for ctx in contexts:
            # 提取关键词（不含数字的词组）
            words = re.findall(r'[\u4e00-\u9fff]{2,}', ctx)
            keywords.append(set(words))
        # 检查是否所有上下文都有至少一个共同关键词
        if keywords:
            common = keywords[0]
            for kw_set in keywords[1:]:
                common = common.intersection(kw_set)
            if not common:
                # 上下文无交集，可能是不同指标，跳过
                continue
        # 如果相同数值出现超过3次且上下文相似，标记为需要核实
        if len(occurrences) > 3:
            issues.append({
                'value': value,
                'count': len(occurrences),
                'locations': [f"L{o['line']}" for o in occurrences],
                'type': 'repeated'
            })
    return issues


def check_value_reasonableness(content):
    """检查关键数值的范围合理性"""
    issues = []

    # 常见指标的合理范围（用于初筛）
    reasonability_rules = [
        # (指标关键词, 单位, 最小, 最大, 说明)
        (['租金', '单价', '价格'], '元/㎡/月', 1, 10000, '月租金单价'),
        (['价格', '单价', '均价'], '元/㎡', 100, 500000, '成交单价'),
        (['GDP'], '亿元', 1000, 500000, '城市 GDP'),
        (['常住人口', '人口'], '万人', 10, 4000, '城市常住人口'),
        (['出租率', '入住率'], '%', 30, 100, '出租率'),
        (['空置率'], '%', 0, 80, '空置率'),
        (['增长率', '增速'], '%', -20, 50, '增长率'),
    ]

    for keywords, unit, min_val, max_val, desc in reasonability_rules:
        # 检查是否涉及该指标
        has_indicator = any(kw in content for kw in keywords)
        if not has_indicator:
            continue

        # 提取该指标附近的数值
        for kw in keywords:
            # 找到关键词所在行
            lines = content.split('\n')
            for line_no, line in enumerate(lines, 1):
                if kw in line:
                    # 提取行中的数字
                    nums = re.findall(r'-?\d+(?:\.\d+)?', line)
                    for num_str in nums:
                        try:
                            num = float(num_str.replace(',', ''))
                            if unit == '%' and num > 1000:
                                continue  # 百分比通常不会超过100
                            if num > max_val or num < min_val:
                                issues.append({
                                    'line': line_no,
                                    'value': num_str,
                                    'expected_range': f'{min_val}-{max_val} {unit}',
                                    'description': desc,
                                    'context': line.strip()[:80]
                                })
                        except ValueError:
                            pass

    return issues


def check_cross_reference(content):
    """检查跨章节数据引用一致性（简版）"""
    # 提取 H1 标题
    h1_matches = re.findall(r'^#{1}\s+(.+)$', content, re.MULTILINE)

    issues = []

    # 检查第一章和最后一章对同一宏观数据的引用是否矛盾
    # 例如：广州 GDP 在开头说是 3.1 万亿，结尾说是 3.2 万亿
    critical_indicators = ['GDP', '常住人口', '地区生产总值', '成交额']

    for indicator in critical_indicators:
        if indicator not in content:
            continue

        # 找所有出现该指标的数值
        pattern = re.compile(
            rf'({indicator}.{{0,30}})(-?\d{{1,3}}(?:,\d{{3}})*(?:\.\d+)?)',
            re.UNICODE
        )
        matches = list(pattern.finditer(content))

        if len(matches) < 2:
            continue

        # 检查数值是否有明显差异（>10%）
        values = []
        for m in matches:
            try:
                val_str = m.group(2).replace(',', '')
                val = float(val_str)
                values.append((m.start(), val, m.group(0)[:60]))
            except ValueError:
                pass

        if len(values) < 2:
            continue

        # 比较首尾值
        first_val = values[0][1]
        last_val = values[-1][1]
        if first_val > 0 and last_val > 0:
            ratio = abs(last_val - first_val) / first_val
            if ratio > 0.1:  # 差异超过10%
                issues.append({
                    'indicator': indicator,
                    'first_value': values[0][2],
                    'last_value': values[-1][2],
                    'diff_percent': f'{ratio*100:.1f}%',
                    'type': 'cross_chapter'
                })

    return issues


def run_l2_check(file_path):
    """执行 L2 逻辑层检查"""
    if not os.path.exists(file_path):
        md_path = file_path.replace('.docx', '.md')
        if os.path.exists(md_path):
            file_path = md_path
        else:
            print(f"❌ 文件不存在：{file_path}")
            sys.exit(1)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print("=" * 60)
    print(f"L2 逻辑层检查")
    print(f"文件：{os.path.basename(file_path)}")
    print("=" * 60)

    passed = 0
    warnings = 0

    # 1. 数字一致性检查
    print("\n[1] 数字一致性检查...")
    matches = extract_all_numbers(content)
    groups = group_numbers_by_value(matches)
    consistency_issues = check_number_consistency(groups)
    print(f"  → 提取数字 {len(matches)} 个，归并 {len(groups)} 个不同数值")

    if consistency_issues:
        print(f"  ⚠️ 发现 {len(consistency_issues)} 处高频重复数字（建议核实是否一致）：")
        for issue in consistency_issues[:5]:
            print(f"    → {issue['value']} 出现 {issue['count']} 次：{', '.join(issue['locations'])}")
        warnings += len(consistency_issues)
    else:
        print(f"  ✅ 未发现明显数字不一致问题")
        passed += 1

    # 2. 数值合理性检查
    print("\n[2] 数值合理性检查...")
    reasonability_issues = check_value_reasonableness(content)

    if reasonability_issues:
        print(f"  ⚠️ 发现 {len(reasonability_issues)} 处超出合理范围的数值：")
        for issue in reasonability_issues[:5]:
            print(f"    → L{issue['line']}: {issue['value']} {issue['expected_range']}（{issue['description']}）")
            print(f"      上下文：{issue['context']}")
        warnings += len(reasonability_issues)
    else:
        print(f"  ✅ 主要数值均在合理范围内")
        passed += 1

    # 3. 跨章节引用检查
    print("\n[3] 跨章节宏观数据引用检查...")
    cross_ref_issues = check_cross_reference(content)

    if cross_ref_issues:
        print(f"  ⚠️ 发现 {len(cross_ref_issues)} 处宏观数据跨章差异（请核实口径是否一致）：")
        for issue in cross_ref_issues[:3]:
            print(f"    → {issue['indicator']}：首处={issue['first_value'][:40]}")
            print(f"      末处={issue['last_value'][:40]}（差异{issue['diff_percent']}）")
            print(f"      说明：差异可能因统计口径或年份不同，需确认是否合理")
        warnings += len(cross_ref_issues)
    else:
        print(f"  ✅ 跨章节宏观数据引用一致")
        passed += 1

    print("\n" + "=" * 60)
    print(f"📊 L2 汇总：{passed} 项通过，{warnings} 项警告")
    if warnings > 0:
        print(f"ℹ️  L2 警告不影响交付，建议人工核实后继续")
    else:
        print(f"✅ L2 逻辑层检查通过")
    print("=" * 60)

    return warnings == 0, {
        'consistency_issues': consistency_issues,
        'reasonability_issues': reasonability_issues,
        'cross_ref_issues': cross_ref_issues
    }


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python3 scripts/l2_check.py <报告文件路径>")
        sys.exit(1)

    passed, results = run_l2_check(sys.argv[1])
    sys.exit(0 if passed else 1)
