#!/usr/bin/env python3
"""
align_lyrics.py - 将原文与译文按行对齐

当原词与译文行数不匹配时，本脚本会：
1. 自动检测并删除空行差异
2. 检测段落标记 [Verse]/[Chorus] 并对齐
3. 输出对齐后的文件
4. 报告对齐情况

使用方法：
    python align_lyrics.py original.txt translated.txt
    python align_lyrics.py original.txt translated.txt --output aligned.md
"""

import re
import argparse
from pathlib import Path


SECTION_PATTERN = re.compile(r'^\[.+\]\s*$')


def is_section_marker(line: str) -> bool:
    """判断是否是段落标记"""
    return bool(SECTION_PATTERN.match(line.strip()))


def is_empty(line: str) -> bool:
    """判断是否是空行"""
    return not line.strip()


def filter_lines(lines, keep_sections=True, keep_empty=False):
    """过滤行"""
    result = []
    for line in lines:
        if is_section_marker(line):
            if keep_sections:
                result.append(line)
        elif is_empty(line):
            if keep_empty:
                result.append(line)
        else:
            result.append(line)
    return result


def align_lyrics(original: str, translation: str) -> dict:
    """对齐原文与译文"""
    orig_lines = original.split('\n')
    trans_lines = translation.split('\n')

    # 过滤空行但保留段落标记
    orig_filtered = filter_lines(orig_lines, keep_sections=True, keep_empty=False)
    trans_filtered = filter_lines(trans_lines, keep_sections=True, keep_empty=False)

    aligned = []
    orig_idx = 0
    trans_idx = 0
    issues = []

    while orig_idx < len(orig_filtered) or trans_idx < len(trans_filtered):
        orig_line = orig_filtered[orig_idx] if orig_idx < len(orig_filtered) else None
        trans_line = trans_filtered[trans_idx] if trans_idx < len(trans_filtered) else None

        # 双方都有
        if orig_line is not None and trans_line is not None:
            # 都是段落标记
            if is_section_marker(orig_line) and is_section_marker(trans_line):
                aligned.append((orig_line, trans_line))
                orig_idx += 1
                trans_idx += 1
            # 原文是段落标记，译文不是
            elif is_section_marker(orig_line) and not is_section_marker(trans_line):
                aligned.append((orig_line, ''))  # 译文段标记缺失
                orig_idx += 1
                issues.append(f'行 {orig_idx+1}: 原文有段落标记 "{orig_line}"，译文缺失')
            # 译文是段落标记，原文不是
            elif not is_section_marker(orig_line) and is_section_marker(trans_line):
                aligned.append(('', trans_line))
                trans_idx += 1
                issues.append(f'行 {orig_idx+1}: 译文有多余段落标记 "{trans_line}"')
            # 都是歌词行
            else:
                aligned.append((orig_line, trans_line))
                orig_idx += 1
                trans_idx += 1
        # 仅原文剩
        elif orig_line is not None:
            aligned.append((orig_line, ''))
            orig_idx += 1
            issues.append(f'行 {orig_idx+1}: 原文 "{orig_line[:30]}..." 无对应译文')
        # 仅译文剩
        elif trans_line is not None:
            aligned.append(('', trans_line))
            trans_idx += 1
            issues.append(f'行 {trans_idx+1}: 译文 "{trans_line[:30]}..." 无对应原文')

    return {
        'aligned': aligned,
        'issues': issues,
        'orig_total': len(orig_filtered),
        'trans_total': len(trans_filtered),
        'matched': sum(1 for o, t in aligned if o and t)
    }


def format_output(aligned_result: dict, format_type: str = 'markdown') -> str:
    """格式化输出"""
    output = []
    for orig, trans in aligned_result['aligned']:
        if format_type == 'markdown':
            if orig and trans:
                output.append(f'{orig}')
                output.append(f'{trans}')
                output.append('')  # 空行分隔
            elif orig:  # 仅原文
                output.append(f'{orig}')
                output.append('')
            elif trans:  # 仅译文
                output.append(f'{trans}')
                output.append('')
        elif format_type == 'table':
            output.append(f'| {orig} | {trans} |')
    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='对齐原文与译文')
    parser.add_argument('original', help='原文文件路径')
    parser.add_argument('translation', help='译文文件路径')
    parser.add_argument('--output', '-o', help='输出文件路径')
    parser.add_argument('--format', '-f', choices=['markdown', 'table'], default='markdown')
    args = parser.parse_args()

    orig_text = Path(args.original).read_text(encoding='utf-8')
    trans_text = Path(args.translation).read_text(encoding='utf-8')

    result = align_lyrics(orig_text, trans_text)

    print(f'原文行数: {result["orig_total"]}')
    print(f'译文行数: {result["trans_total"]}')
    print(f'成功对齐: {result["matched"]}')
    print(f'问题数: {len(result["issues"])}')

    if result['issues']:
        print('\n问题列表:')
        for issue in result['issues'][:10]:  # 只显示前10个
            print(f'  - {issue}')
        if len(result['issues']) > 10:
            print(f'  ...还有 {len(result["issues"])-10} 个问题')

    output_text = format_output(result, args.format)
    if args.output:
        Path(args.output).write_text(output_text, encoding='utf-8')
        print(f'\n已保存到: {args.output}')
    else:
        print('\n--- 对齐结果 ---')
        print(output_text)


if __name__ == '__main__':
    main()
