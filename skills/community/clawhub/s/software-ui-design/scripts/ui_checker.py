#!/usr/bin/env python3
"""UI 规范检查器 - 验证设计稿是否符合规范"""
import argparse
import json
import re
from pathlib import Path


def parse_hex_color(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 6:
        return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))
    return None


def color_distance(c1, c2):
    return sum((a - b) ** 2 for a, b in zip(c1, c2))


def is_brand_color(hex_color, brand_colors, threshold=30):
    c = parse_hex_color(hex_color)
    if not c:
        return False
    for brand in brand_colors:
        bc = parse_hex_color(brand)
        if bc and color_distance(c, bc) < threshold ** 2:
            return True
    return False


def check_color规范(elements, brand_colors):
    issues = []
    for el in elements:
        color = el.get('color', '')
        if color and not is_brand_color(color, brand_colors):
            issues.append(f"  [!] {el['name']} 使用了非品牌色: {color} (路径: {el['path']})")
    return issues


def check_font规范(elements, size_rules=None):
    issues = []
    size_rules = size_rules or {'h1': 24, 'h2': 20, 'body': 14, 'caption': 12}
    for el in elements:
        fs = el.get('fontSize')
        if fs:
            name = el.get('name', '')
            expected = None
            for key, val in size_rules.items():
                if key.lower() in name.lower():
                    expected = val
            if expected and abs(fs - expected) > 1:
                issues.append(f"  [!] {name} 字号 {fs} 与规范 {expected} 不符")
    return issues


def check_spacing_8px(element_positions, threshold=8):
    issues = []
    positions = sorted(element_positions, key=lambda x: x['y'])
    for i in range(len(positions) - 1):
        gap = positions[i + 1]['y'] - positions[i]['y'] - positions[i]['height']
        if gap > 0 and gap % 8 != 0:
            issues.append(f"  [!] {positions[i]['name']} 与 {positions[i+1]['name']} 间距 {gap:.1f}px 不符合 8px 栅格")
    return issues


def load_elements_from_report(report_path):
    with open(report_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_check(report_path, brand_colors, output_path=None):
    data = load_elements_from_report(report_path)
    elements = data.get('elements', [])
    all_issues = []
    all_issues.extend(check_color规范(elements, brand_colors))
    all_issues.extend(check_font规范(elements))
    report = {
        'totalElements': len(elements),
        'issues': all_issues,
        'passed': len(all_issues) == 0
    }
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    if all_issues:
        print(f"发现 {len(all_issues)} 个规范问题:")
        for issue in all_issues:
            print(issue)
    else:
        print("[OK] 所有元素符合规范")
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UI 规范检查')
    parser.add_argument('--report', '-r', required=True, help='设计报告路径')
    parser.add_argument('--brand-colors', '-c', default='[]', help='品牌色 JSON')
    parser.add_argument('--output', '-o', default=None, help='输出报告路径')
    args = parser.parse_args()
    import json
    brand = json.loads(args.brand_colors)
    run_check(args.report, brand, args.output)
