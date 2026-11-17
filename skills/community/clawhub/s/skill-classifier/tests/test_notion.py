# -*- coding: utf-8 -*-
from exporter.notion import md_to_blocks


def test_blocks_conversion():
    md = '# 标题\n\n- 项目一\n\n```py\nprint(1)\n```\n正文段落'
    blocks = md_to_blocks(md)
    types = [b['type'] for b in blocks]
    assert types == ['heading_1', 'bulleted_list_item', 'code', 'paragraph']


def test_heading_levels():
    blocks = md_to_blocks('## 二级\n### 三级')
    assert [b['type'] for b in blocks] == ['heading_2', 'heading_3']


def test_table_line_becomes_paragraph():
    blocks = md_to_blocks('| a | b |')
    assert blocks[0]['type'] == 'paragraph'


def test_numbered_and_quote():
    blocks = md_to_blocks('1. 第一\n> 引用')
    assert [b['type'] for b in blocks] == ['numbered_list_item', 'quote']


def test_rich_text_truncated():
    blocks = md_to_blocks('x' * 3000)
    content = blocks[0]['paragraph']['rich_text'][0]['text']['content']
    assert len(content) <= 2000
