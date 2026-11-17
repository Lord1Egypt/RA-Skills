# -*- coding: utf-8 -*-
"""
Notion 页面导出
环境变量：NOTION_TOKEN（integration token，必填）、NOTION_PAGE_ID（目标页面或块 ID，必填）
把 Markdown 行转换为 Notion blocks，按 ≤100 块分批追加到目标页
凭据只从环境变量读取，严禁写入任何文件
"""
import logging
import os
import re

from utils.webclient import http_json

logger = logging.getLogger(__name__)
API = 'https://api.notion.com/v1'
NOTION_VERSION = '2022-06-28'
MAX_BATCH = 100
RICH_TEXT_LIMIT = 2000


def _headers(token: str):
    return {'Authorization': f'Bearer {token}', 'Notion-Version': NOTION_VERSION}


def _rich(text: str):
    return [{'text': {'content': text[:RICH_TEXT_LIMIT]}}]


def _block(btype: str, text: str, **extra):
    block = {'object': 'block', 'type': btype, btype: {'rich_text': _rich(text)}}
    block[btype].update(extra)
    return block


def md_to_blocks(md_text: str) -> list:
    """极简 md→blocks：标题 1-3 级、无序/有序列表、引用、代码块、表格行按段落处理"""
    blocks = []
    in_code = False
    code_lines = []
    for raw in md_text.splitlines():
        line = raw.rstrip()
        if line.startswith('```'):
            if in_code:
                blocks.append(_block('code', '\n'.join(code_lines), language='plain text'))
                code_lines = []
            in_code = not in_code
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            continue
        stripped = line.strip()
        if stripped.startswith('|'):
            blocks.append(_block('paragraph', stripped))
            continue
        m = re.match(r'^(#{1,3})\s+(.*)$', stripped)
        if m:
            blocks.append(_block(f'heading_{len(m.group(1))}', m.group(2)))
            continue
        if stripped.startswith(('- ', '* ')):
            blocks.append(_block('bulleted_list_item', stripped[2:]))
            continue
        if re.match(r'^\d+\.\s+', stripped):
            blocks.append(_block('numbered_list_item', re.sub(r'^\d+\.\s+', '', stripped)))
            continue
        if stripped.startswith('> '):
            blocks.append(_block('quote', stripped[2:]))
            continue
        blocks.append(_block('paragraph', stripped))
    if in_code and code_lines:
        blocks.append(_block('code', '\n'.join(code_lines), language='plain text'))
    return blocks


def push_markdown(md_path: str, title: str = '') -> str:
    """把 md 追加写入 NOTION_PAGE_ID 指向的页面，返回页面链接"""
    token = os.environ.get('NOTION_TOKEN')
    page_id = os.environ.get('NOTION_PAGE_ID')
    if not token or not page_id:
        raise SystemExit("缺少环境变量 NOTION_TOKEN / NOTION_PAGE_ID，无法推送 Notion")

    with open(md_path, 'r', encoding='utf-8') as f:
        blocks = md_to_blocks(f.read())
    if not blocks:
        raise RuntimeError(f"{md_path} 无可写入内容")

    for i in range(0, len(blocks), MAX_BATCH):
        http_json('PATCH', f'{API}/blocks/{page_id}/children',
                  headers=_headers(token),
                  body={'children': blocks[i:i + MAX_BATCH]})
    logger.info(f"已写入 {len(blocks)} 个块到 Notion")
    return f'https://www.notion.so/{page_id.replace("-", "")}'
