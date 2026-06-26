#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用于处理 IMA 笔记等无换行的纯文本，自动插入换行符

用法：
    python preprocess.py <input.txt> [output.md]
    python preprocess.py --stdin < input.txt > output.md
"""

import re
import sys
import io
from pathlib import Path

# Windows 编码设置
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


# 中文序号标题模式
TITLE_PATTERNS = [
    (r'([一二三四五六七八九十]+[、.])', '\n\\1'),  # 一、二、三、四、
    (r'([（\(][一二三四五六七八九十]+[）\)])', '\n\\1'),  # （一）、(一)
    (r'(\([1-9][\d]*\))', '\n\\1'),  # (1), (2)
]

# 标题关键词
TITLE_KEYWORDS = [
    '背景', '前言', '介绍', '概述', '总结', '结论',
    '方法', '步骤', '流程', '过程',
    '原因', '结果', '影响', '分析',
    '问题', '方案', '对策', '建议',
    '场景', '情况', '案例', '示例',
    '配置', '安装', '部署', '使用', '教程',
    '沟通话术', '价格异议', '注意事项', '说明', '提示',
    '优势', '特点', '功能', '特性',
]

# 转折词（分段标记）
TRANSITION_WORDS = [
    '但是', '然而', '不过', '可是', '只是',
    '因此', '所以', '于是', '从而', '故',
    '而且', '并且', '同时', '另外', '此外',
    '总之', '综上所述', '总而言之',
    '首先', '其次', '最后', '接着',
]

# 分隔线模式
SEPARATOR_PATTERNS = [
    r'^---+$',  # ---
    r'^=+$',     # ===
    r'^__+$',   # ___
]


def has_chinese_numbering(text: str) -> bool:
    """检查文本是否包含中文序号标题"""
    patterns = [
        r'^[一二三四五六七八九十]+[、.]',
        r'^[第一二三四五六七八九十]+[章节步段]',
        r'^[（\(][一二三四五六七八九十]+[）\)]',
        r'^\([1-9][\d]*\)',
    ]
    for p in patterns:
        if re.match(p, text.strip()):
            return True
    return False


def is_title_keyword_line(text: str) -> bool:
    """检查是否是标题关键词行（仅当关键词在行开头时）"""
    text = text.strip()
    # 只检查行开头是否是标题关键词
    for kw in TITLE_KEYWORDS:
        if text.startswith(kw + '：') or text.startswith(kw + ':'):
            return True
        if text == kw:
            return True
    return False


def split_sentences(text: str) -> list:
    """将长段落按句子分割"""
    # 句号、问号、感叹号后分段
    sentences = re.split(r'([。！？])', text)

    result = []
    current = []

    for i, part in enumerate(sentences):
        if not part:
            continue

        if i % 2 == 0:
            # 普通句子部分
            current.append(part)
        else:
            # 标点符号部分，合并到前一句
            current.append(part)
            result.append(''.join(current))
            current = []

    # 处理最后可能剩余的内容
    if current:
        result.append(''.join(current))

    return result


def preprocess_plain_text(text: str) -> str:
    """
    预处理纯文本，在适当位置插入换行符

    处理策略：
    1. 识别并标记标题行
    2. 在标题前插入换行
    3. 在转折词前插入换行
    4. 对超长段落进行分句
    """
    lines = text.split('\n')
    result_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            result_lines.append('')
            continue

        # 检查是否包含多个标题关键词（用于分段）
        has_title = False
        for kw in TITLE_KEYWORDS:
            if f'{kw}：' in line or f'{kw}:' in line:
                has_title = True
                break

        if has_title:
            # 按标题关键词分割
            pattern = '|'.join(rf'({kw}[：:])' for kw in TITLE_KEYWORDS)
            parts = re.split(pattern, line)
            for part in parts:
                if part:
                    part = part.strip()
                    if part:
                        result_lines.append(part)
        elif has_chinese_numbering(line):
            # 中文序号标题分割
            # 先匹配中文序号，然后在每个序号前插入换行
            new_line = line
            for pattern_str, replacement in TITLE_PATTERNS:
                new_line = re.sub(pattern_str, replacement, new_line)
            # 清理开头多余的换行，然后按换行分割
            new_line = new_line.lstrip('\n')
            parts = new_line.split('\n')
            for part in parts:
                part = part.strip()
                if part:
                    result_lines.append(part)
        elif any(tw in line for tw in TRANSITION_WORDS):
            # 包含转折词的段落，在转折词前分段
            new_line = line
            for tw in TRANSITION_WORDS:
                new_line = new_line.replace(tw, f'\n{tw}')
            new_line = new_line.lstrip('\n')
            parts = new_line.split('\n')
            for part in parts:
                part = part.strip()
                if part:
                    result_lines.append(part)
        elif len(line) > 200:
            # 超长段落按句号分句
            sentences = split_sentences(line)
            result_lines.extend(sentences)
        else:
            result_lines.append(line)

    # 再次处理，在标题前插入换行
    final_lines = []
    prev_was_empty = True

    for line in result_lines:
        line = line.strip()
        if not line:
            final_lines.append('')
            prev_was_empty = True
            continue

        # 恢复标题标记
        if '__TITLE_START__' in line:
            line = line.replace('__TITLE_START__', '')

        # 检查是否是标题
        is_title = has_chinese_numbering(line) or is_title_keyword_line(line)

        if is_title and not prev_was_empty:
            final_lines.append('')

        final_lines.append(line)
        prev_was_empty = False

    return '\n'.join(final_lines)


def main():
    input_text = ''
    output_path = None

    if len(sys.argv) > 1:
        if sys.argv[1] == '--stdin':
            input_text = sys.stdin.read()
        else:
            input_path = Path(sys.argv[1])
            if not input_path.exists():
                print(f"错误：文件不存在 - {input_path}", file=sys.stderr)
                sys.exit(1)
            input_text = input_path.read_text(encoding='utf-8')

            if len(sys.argv) > 2:
                output_path = Path(sys.argv[2])
    else:
        # 尝试从 stdin 读取
        if not sys.stdin.isatty():
            input_text = sys.stdin.read()
        else:
            print(__doc__)
            sys.exit(0)

    if not input_text:
        print("错误：没有输入内容", file=sys.stderr)
        sys.exit(1)

    result = preprocess_plain_text(input_text)

    if output_path:
        output_path.write_text(result, encoding='utf-8')
        print(f"已保存到：{output_path}")
    else:
        print(result)


if __name__ == '__main__':
    main()
