#!/usr/bin/env python3
"""
detect_language.py - 检测歌词主语言

支持检测的语言：
- Japanese (日语)
- Korean (韩语)
- Russian (俄语)
- Spanish (西语)
- French (法语)
- German (德语)
- Chinese (中文)
- English (英语，默认)

使用方法：
    python detect_language.py input.txt
    python detect_language.py -t "歌词文本"
"""

import sys
import argparse
from pathlib import Path
from collections import Counter


def detect_language_char(c: str) -> str:
    """检测单个字符所属语言"""
    cp = ord(c)

    # 日语
    if 0x3040 <= cp <= 0x309f:  # 平假名
        return 'Japanese'
    if 0x30a0 <= cp <= 0x30ff:  # 片假名
        return 'Japanese'

    # 韩语
    if 0xac00 <= cp <= 0xd7a3:  # 谚文
        return 'Korean'

    # 俄语（西里尔字母）
    if 0x0400 <= cp <= 0x04ff:
        return 'Russian'

    # 中文（CJK统一汉字）
    if 0x4e00 <= cp <= 0x9fff:
        return 'Chinese'
    if 0x3400 <= cp <= 0x4dbf:  # CJK扩展A
        return 'Chinese'

    # 西语/法语/德语特殊字符
    if c in 'áéíóúñü¿¡':
        return 'Spanish'
    if c in 'àâçéèêëïîôûœæ':
        return 'French'
    if c in 'äöüß':
        return 'German'

    # 英文字母
    if c.isascii() and c.isalpha():
        return 'English'

    return 'Other'


def detect_language(text: str) -> dict:
    """检测文本主语言，返回详细分析"""
    if not text.strip():
        return {'primary': 'Unknown', 'all': {}, 'ratios': {}}

    counts = Counter()
    for c in text:
        if c.isspace() or not c.isalpha():
            continue
        lang = detect_language_char(c)
        if lang != 'Other':
            counts[lang] += 1

    total = sum(counts.values())
    if total == 0:
        return {'primary': 'Unknown', 'all': {}, 'ratios': {}}

    primary = counts.most_common(1)[0][0]
    ratios = {lang: cnt / total for lang, cnt in counts.items()}

    return {
        'primary': primary,
        'all': dict(counts),
        'ratios': ratios,
        'total_chars': total,
        'is_mixed': len(counts) >= 2 and ratios[list(ratios.keys())[-1]] > 0.1
    }


def main():
    parser = argparse.ArgumentParser(description='检测歌词主语言')
    parser.add_argument('input', nargs='?', help='输入文件路径')
    parser.add_argument('-t', '--text', help='直接输入文本')
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.input:
        text = Path(args.input).read_text(encoding='utf-8')
    else:
        parser.error('需要提供输入文件或 -t 文本')

    result = detect_language(text)

    print(f'主语言: {result["primary"]}')
    print(f'总字符数: {result.get("total_chars", 0)}')
    print(f'是否混合语种: {"是" if result.get("is_mixed") else "否"}')
    print()
    print('语言分布:')
    for lang, ratio in sorted(result['ratios'].items(), key=lambda x: -x[1]):
        count = result['all'][lang]
        print(f'  {lang}: {count} 字符 ({ratio*100:.1f}%)')

    return result


if __name__ == '__main__':
    main()
