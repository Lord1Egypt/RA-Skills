#!/usr/bin/env python3
"""
validate_translation.py - 验证歌词翻译质量

按 song-translation-expert skill 的质量自检清单检查翻译。

使用方法：
    python validate_translation.py original.txt translated.txt
    python validate_translation.py original.txt translated.txt --verbose
"""

import re
import argparse
from pathlib import Path
from collections import Counter

SECTION_PATTERN = re.compile(r'^\[.+?\]\s*$')


def count_syllables_chinese(text: str) -> int:
    """估算中文字数（每字约一音节）"""
    return len([c for c in text if c.strip() and c not in '，。！？、；：""\'\'' and not c.isascii()])


def count_syllables_english(text: str) -> int:
    """估算英文音节数（基于元音组）"""
    words = re.findall(r'\b\w+\b', text.lower())
    syllables = 0
    for word in words:
        vowel_groups = re.findall(r'[aeiouy]+', word)
        syllables += max(1, len(vowel_groups))
    return syllables


def is_chinese(text: str) -> bool:
    """判断是否主要中文"""
    cn_count = len([c for c in text if 0x4e00 <= ord(c) <= 0x9fff])
    en_count = len([c for c in text if c.isascii() and c.isalpha()])
    return cn_count > en_count


def check_line_alignment(orig_lines, trans_lines):
    """检查行数对齐"""
    orig_real = [l for l in orig_lines if l.strip() and not SECTION_PATTERN.match(l.strip())]
    trans_real = [l for l in trans_lines if l.strip() and not SECTION_PATTERN.match(l.strip())]
    return {
        'orig_count': len(orig_real),
        'trans_count': len(trans_real),
        'aligned': len(orig_real) == len(trans_real),
        'difference': abs(len(orig_real) - len(trans_real))
    }


def check_section_markers(orig_lines, trans_lines):
    """检查段落标记保留"""
    orig_markers = [l.strip() for l in orig_lines if SECTION_PATTERN.match(l.strip())]
    trans_markers = [l.strip() for l in trans_lines if SECTION_PATTERN.match(l.strip())]
    return {
        'orig_markers': orig_markers,
        'trans_markers': trans_markers,
        'preserved': len(orig_markers) == len(trans_markers),
        'missing': [m for m in orig_markers if m not in trans_markers]
    }


def check_syllable_match(orig_lines, trans_lines, max_diff=2):
    """检查音节数匹配"""
    issues = []
    for i, (orig, trans) in enumerate(zip(orig_lines, trans_lines), 1):
        if not orig.strip() or not trans.strip():
            continue
        if SECTION_PATTERN.match(orig.strip()):
            continue

        orig_is_en = not is_chinese(orig)
        trans_is_cn = is_chinese(trans)

        if orig_is_en and trans_is_cn:
            orig_count = count_syllables_english(orig)
            trans_count = count_syllables_chinese(trans)
        elif not orig_is_en and trans_is_cn:
            orig_count = count_syllables_chinese(orig)
            trans_count = count_syllables_chinese(trans)
        else:
            continue

        diff = abs(orig_count - trans_count)
        if diff > max_diff:
            issues.append({
                'line': i,
                'orig': orig[:50],
                'trans': trans[:50],
                'orig_count': orig_count,
                'trans_count': trans_count,
                'diff': diff
            })
    return issues


def check_translation_style(trans_lines):
    """检查翻译腔"""
    translation_patterns = [
        (r'被.{1,5}所', '被动句"被...所"'),
        (r'^是的[，,]', '开头"是的,"'),
        (r'关于.{1,10}的问题', '"关于...的问题"'),
        (r'一个.{1,5}的(男|女)人', '"一个...的男/女人"'),
        (r'\.\.\.的(事实|时候|地方)', '"...的事实/时候/地方"'),
    ]

    issues = []
    for i, line in enumerate(trans_lines, 1):
        for pattern, desc in translation_patterns:
            if re.search(pattern, line):
                issues.append({'line': i, 'pattern': desc, 'text': line[:60]})
    return issues


def check_adlibs_consistency(orig_lines, trans_lines):
    """检查拟声词一致处理"""
    adlib_patterns = {
        'na_na': r'\bNa na na\b',
        'la_la': r'\bLa la la\b',
        'yeah': r'\bYeah,? yeah\b',
        'oh_oh': r'\bOh,? oh\b',
    }

    issues = []
    for name, pattern in adlib_patterns.items():
        orig_matches = sum(1 for l in orig_lines if re.search(pattern, l, re.IGNORECASE))
        trans_kept = sum(1 for l in trans_lines if re.search(pattern, l, re.IGNORECASE))
        trans_transliterated = sum(1 for l in trans_lines if re.search(
            r'那那|啦啦|耶耶|哦哦', l))

        if orig_matches > 0:
            total_trans = trans_kept + trans_transliterated
            if total_trans < orig_matches:
                issues.append({
                    'adlib': name,
                    'orig_count': orig_matches,
                    'trans_count': total_trans,
                    'note': f'原文 {orig_matches} 处，译文仅处理 {total_trans} 处'
                })

    return issues


def check_notes(trans_text):
    """检查译注完整性"""
    note_patterns = [
        r'注\d+',
        r'注一|注二|注三|注四|注五',
        r'\[\d+\]',
    ]

    notes_found = []
    for pattern in note_patterns:
        notes_found.extend(re.findall(pattern, trans_text))

    return {
        'count': len(notes_found),
        'samples': notes_found[:5]
    }


def grade_translation(checks):
    """评分"""
    score = 100

    # 行数对齐 (30分)
    if not checks['alignment']['aligned']:
        score -= 30 * (checks['alignment']['difference'] / max(checks['alignment']['orig_count'], 1))

    # 段落标记 (15分)
    if not checks['section_markers']['preserved']:
        score -= 15

    # 音节匹配 (20分)
    syllable_issues = len(checks['syllable_issues'])
    if syllable_issues > 0:
        score -= min(20, syllable_issues * 2)

    # 翻译腔 (15分)
    style_issues = len(checks['translation_style'])
    if style_issues > 0:
        score -= min(15, style_issues * 3)

    # 拟声词一致性 (10分)
    if checks['adlibs_issues']:
        score -= min(10, len(checks['adlibs_issues']) * 5)

    # 译注 (10分)
    if checks['notes']['count'] == 0:
        score -= 5  # 注释缺失扣5分（非必须）

    return max(0, int(score))


def main():
    parser = argparse.ArgumentParser(description='验证歌词翻译质量')
    parser.add_argument('original', help='原文文件路径')
    parser.add_argument('translation', help='译文文件路径')
    parser.add_argument('--verbose', '-v', action='store_true', help='详细输出')
    args = parser.parse_args()

    orig_text = Path(args.original).read_text(encoding='utf-8')
    trans_text = Path(args.translation).read_text(encoding='utf-8')

    orig_lines = orig_text.split('\n')
    trans_lines = trans_text.split('\n')

    alignment = check_line_alignment(orig_lines, trans_lines)
    section_markers = check_section_markers(orig_lines, trans_lines)
    syllable_issues = check_syllable_match(orig_lines, trans_lines)
    style_issues = check_translation_style(trans_lines)
    adlibs_issues = check_adlibs_consistency(orig_lines, trans_lines)
    notes = check_notes(trans_text)

    checks = {
        'alignment': alignment,
        'section_markers': section_markers,
        'syllable_issues': syllable_issues,
        'translation_style': style_issues,
        'adlibs_issues': adlibs_issues,
        'notes': notes
    }

    score = grade_translation(checks)

    print('=' * 50)
    print(f'歌词翻译质量评分: {score}/100')
    print('=' * 50)

    print(f'\n1. 行数对齐: {"✓" if alignment["aligned"] else "✗"}')
    print(f'   原文 {alignment["orig_count"]} 行 / 译文 {alignment["trans_count"]} 行 / 差异 {alignment["difference"]}')

    print(f'\n2. 段落标记: {"✓" if section_markers["preserved"] else "✗"}')
    print(f'   原文 {len(section_markers["orig_markers"])} 个 / 译文 {len(section_markers["trans_markers"])} 个')
    if section_markers["missing"]:
        print(f'   缺失: {section_markers["missing"]}')

    print(f'\n3. 音节匹配: {len(syllable_issues)} 处问题')
    if args.verbose and syllable_issues:
        for issue in syllable_issues[:5]:
            print(f'   行 {issue["line"]}: {issue["orig_count"]}→{issue["trans_count"]} (差{issue["diff"]})')
            print(f'     原文: {issue["orig"]}')
            print(f'     译文: {issue["trans"]}')

    print(f'\n4. 翻译腔检查: {len(style_issues)} 处问题')
    if args.verbose and style_issues:
        for issue in style_issues[:5]:
            print(f'   行 {issue["line"]}: {issue["pattern"]}')
            print(f'     {issue["text"]}')

    print(f'\n5. 拟声词一致性: {len(adlibs_issues)} 处问题')
    if args.verbose and adlibs_issues:
        for issue in adlibs_issues:
            print(f'   {issue["adlib"]}: {issue["note"]}')

    print(f'\n6. 译注: {notes["count"]} 条')
    if notes["samples"]:
        print(f'   示例: {notes["samples"]}')

    # 总评
    print('\n' + '=' * 50)
    if score >= 90:
        print('✓ 优秀 - 翻译质量高')
    elif score >= 80:
        print('✓ 良好 - 建议小修')
    elif score >= 70:
        print('⚠ 合格 - 建议中等修改')
    else:
        print('✗ 不合格 - 建议重译')

    return score


if __name__ == '__main__':
    main()
