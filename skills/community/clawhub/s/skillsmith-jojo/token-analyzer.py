#!/usr/bin/env python3
"""
Token 性能分析器
估算技能 Token 消耗，给出优化建议
"""

import sys
import argparse
import re
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description='Token 性能分析器')
    parser.add_argument('skill_path', help='技能目录路径')
    return parser.parse_args()

def estimate_tokens(text):
    """估算 Token 数量"""
    zh = len(re.findall(r'[\u4e00-\u9fff]', text))
    en = len(text) - zh
    return int(zh / 1.5 + en / 4)

def analyze_skill_md(skill_path):
    """分析 SKILL.md"""
    skill_md = Path(skill_path) / 'SKILL.md'
    if not skill_md.exists():
        return None

    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()

    fm = ''
    body = content
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm = content[3:end]
            body = content[end+3:]

    fm_tokens = estimate_tokens(fm)
    body_tokens = estimate_tokens(body)

    return {
        'size_bytes': len(content),
        'frontmatter_tokens': fm_tokens,
        'body_tokens': body_tokens,
        'total_tokens': fm_tokens + body_tokens
    }

def main():
    args = parse_args()
    result = analyze_skill_md(args.skill_path)

    if not result:
        print("❌ 未找到 SKILL.md")
        sys.exit(1)

    total = result['total_tokens']
    rating = 'A 优秀' if total <= 1500 else 'B 良好' if total <= 3000 else 'C 需优化' if total <= 5000 else 'D 严重'

    print(f"📊 Token 分析结果")
    print(f"  总计: {total} tokens")
    print(f"  评级: {rating}")

    if total > 1500:
        print(f"💡 建议: 将详细内容移至 references/ 目录")

    sys.exit(0)

if __name__ == '__main__':
    main()
