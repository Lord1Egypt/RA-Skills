"""vkey-bid-standardizer.markdown_parser

从 apply_md_to_docx.py 抽出的 Markdown 解析核心：
- classify_line: 识别行类型（heading / body / table / empty）
- parse_md_table: 解析 Markdown 表格块
- strip_md_format: 剥离行内格式
"""
import re
from typing import List, Tuple


def strip_md_format(text: str) -> str:
    """剥离 Markdown 行内格式标记（**bold** / *italic* / `code` / [text](url) / ---）。"""
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    text = re.sub(r'^---+$', '', text)
    return text.strip()


def classify_line(line: str) -> Tuple[str, str]:
    """识别单行 Markdown 类型。

    Returns:
        (type, content) 其中 type 是：
        - 'empty'
        - 'h1'..'h6'（Markdown 标题层级）
        - 'table_row'
        - 'body'（普通段落，已剥离格式）
    """
    line = line.strip()
    if not line:
        return 'empty', ''

    m = re.match(r'^(#{1,6})\s+(.+)', line)
    if m:
        return f'h{len(m.group(1))}', m.group(2).strip()

    if line.startswith('|') and line.endswith('|'):
        return 'table_row', line

    return 'body', strip_md_format(line)


def parse_md_table(lines: List[str], start_idx: int) -> Tuple[List[List[str]], int]:
    """从 start_idx 开始解析 Markdown 表格块。

    Returns:
        (rows, next_idx) — rows 是 [[cell, cell, ...], ...]，
        next_idx 是表格块结束后下一行的索引。
    """
    rows = []
    i = start_idx
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('|') and line.endswith('|'):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            if all(re.match(r'^[-:]+$', c) for c in cells):
                i += 1
                continue
            rows.append(cells)
            i += 1
        else:
            break
    return rows, i
