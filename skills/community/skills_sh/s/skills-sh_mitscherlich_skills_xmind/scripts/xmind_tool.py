#!/usr/bin/env python3
"""
XMind Tool - 零依赖 XMind 文件解析、创建和更新工具。

支持 XMind 8（XML 格式）和 XMind Zen/2020+（JSON 格式）。
仅使用 Python 标准库，无需安装第三方依赖。

用法:
  python xmind_tool.py --session <id> parse   <file.xmind>                              解析为 Markdown
  python xmind_tool.py --session <id> create  <output.xmind> <input.md> [--format zen|legacy]  从 Markdown 创建
  python xmind_tool.py --session <id> update  <file.xmind> <modified.md>                更新已有文件
  python xmind_tool.py --session <id> memory  <file.xmind>                              查看会话记忆文件

--session <id> 为必填参数，用于隔离不同会话的记忆文件。
记忆文件存储路径: /tmp/skills-xmind-parsed/<session-id>/<filename>.md
"""

import io
import json
import os
import re
import sys
import tempfile
import time
import uuid
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


# ============================================================
# 数据模型
# ============================================================

class Topic:
    """思维导图节点"""

    def __init__(self, title="", topic_id=None):
        self.id = topic_id or uuid.uuid4().hex[:26]
        self.title = title
        self.children = []   # list[Topic]
        self.notes = ""      # 纯文本备注
        self.labels = []     # list[str]  标签
        self.link = ""       # 超链接 URL
        self.markers = []    # list[str]  标记/图标 ID


class Sheet:
    """工作表（一个 xmind 文件可含多个工作表）"""

    def __init__(self, title="Sheet 1", sheet_id=None):
        self.id = sheet_id or uuid.uuid4().hex[:26]
        self.title = title
        self.root_topic = None  # Topic


# ============================================================
# 格式检测
# ============================================================

def detect_format(xmind_path):
    """检测 xmind 文件格式：zen (JSON) 或 legacy (XML)。"""
    with zipfile.ZipFile(xmind_path, 'r') as zf:
        names = zf.namelist()
        if 'content.json' in names:
            return 'zen'
        elif 'content.xml' in names:
            return 'legacy'
        else:
            raise ValueError(
                f"无法识别的 XMind 格式：文件中既无 content.json 也无 content.xml\n"
                f"文件内容: {names}"
            )


# ============================================================
# Zen 格式解析 (XMind Zen / 2020+)
# ============================================================

def parse_zen(xmind_path):
    """解析 XMind Zen 格式（JSON）。"""
    with zipfile.ZipFile(xmind_path, 'r') as zf:
        raw = zf.read('content.json')
        content = json.loads(raw)

    sheets = []
    for sheet_data in content:
        sheet = Sheet(
            title=sheet_data.get('title', 'Sheet 1'),
            sheet_id=sheet_data.get('id'),
        )
        if 'rootTopic' in sheet_data:
            sheet.root_topic = _parse_zen_topic(sheet_data['rootTopic'])
        sheets.append(sheet)
    return sheets


def _parse_zen_topic(data):
    topic = Topic(
        title=data.get('title', ''),
        topic_id=data.get('id'),
    )

    # --- 备注 ---
    notes_data = data.get('notes', {})
    if isinstance(notes_data, dict):
        if 'plain' in notes_data:
            topic.notes = notes_data['plain'].get('content', '')
        elif 'ops' in notes_data:
            ops = notes_data['ops']
            if isinstance(ops, dict):
                ops = ops.get('ops', [])
            topic.notes = ''.join(
                op.get('insert', '') for op in ops if isinstance(op, dict)
            ).strip()

    # --- 标签 ---
    topic.labels = list(data.get('labels', []))

    # --- 超链接 ---
    topic.link = data.get('href', '')

    # --- 标记 ---
    topic.markers = [
        m.get('markerId', '')
        for m in data.get('markers', [])
        if isinstance(m, dict) and m.get('markerId')
    ]

    # --- 子节点 ---
    children_data = data.get('children', {})
    for child in children_data.get('attached', []):
        topic.children.append(_parse_zen_topic(child))

    return topic


# ============================================================
# Legacy 格式解析 (XMind 8)
# ============================================================

_NS = {'c': 'urn:xmind:xmap:xmlns:content:2.0'}
_XLINK = '{http://www.w3.org/1999/xlink}href'


def parse_legacy(xmind_path):
    """解析 XMind 8 格式（XML）。"""
    with zipfile.ZipFile(xmind_path, 'r') as zf:
        raw = zf.read('content.xml')

    root = ET.fromstring(raw)
    sheets = []

    for sheet_elem in root.findall('c:sheet', _NS):
        title_elem = sheet_elem.find('c:title', _NS)
        sheet = Sheet(
            title=title_elem.text if title_elem is not None and title_elem.text else 'Sheet 1',
            sheet_id=sheet_elem.get('id'),
        )
        topic_elem = sheet_elem.find('c:topic', _NS)
        if topic_elem is not None:
            sheet.root_topic = _parse_legacy_topic(topic_elem)
        sheets.append(sheet)

    return sheets


def _parse_legacy_topic(elem):
    title_elem = elem.find('c:title', _NS)
    topic = Topic(
        title=title_elem.text if title_elem is not None and title_elem.text else '',
        topic_id=elem.get('id'),
    )

    # --- 备注 ---
    notes_elem = elem.find('c:notes', _NS)
    if notes_elem is not None:
        plain_elem = notes_elem.find('c:plain', _NS)
        if plain_elem is not None and plain_elem.text:
            topic.notes = plain_elem.text

    # --- 标签 ---
    labels_elem = elem.find('c:labels', _NS)
    if labels_elem is not None:
        for lbl in labels_elem.findall('c:label', _NS):
            if lbl.text:
                topic.labels.append(lbl.text)

    # --- 超链接 ---
    href = elem.get(_XLINK, '')
    if href:
        topic.link = href

    # --- 标记 ---
    mrefs = elem.find('c:marker-refs', _NS)
    if mrefs is not None:
        for mref in mrefs.findall('c:marker-ref', _NS):
            mid = mref.get('marker-id', '')
            if mid:
                topic.markers.append(mid)

    # --- 子节点 ---
    children_elem = elem.find('c:children', _NS)
    if children_elem is not None:
        for topics_elem in children_elem.findall('c:topics', _NS):
            if topics_elem.get('type') == 'attached':
                for child_elem in topics_elem.findall('c:topic', _NS):
                    topic.children.append(_parse_legacy_topic(child_elem))

    return topic


# ============================================================
# 数据模型 → Markdown
# ============================================================

def sheets_to_markdown(sheets):
    """将工作表列表转换为 Markdown 字符串。"""
    parts = []
    for i, sheet in enumerate(sheets):
        if i > 0:
            parts.append('\n---\n')

        parts.append(f'# Sheet: {sheet.title}\n')

        if sheet.root_topic:
            parts.append(f'\n## {sheet.root_topic.title}\n')

            # 中心主题的元数据
            meta = _format_meta_block(sheet.root_topic)
            if meta:
                parts.append(meta)

            parts.append('')  # 空行

            for child in sheet.root_topic.children:
                parts.append(_topic_to_md(child, depth=0))

    return '\n'.join(parts)


def _format_meta_block(topic):
    """为中心主题生成 blockquote 元数据。"""
    lines = []
    if topic.labels:
        lines.append(f'> Labels: {", ".join(topic.labels)}')
    if topic.link:
        lines.append(f'> Link: {topic.link}')
    if topic.markers:
        lines.append(f'> Markers: {", ".join(topic.markers)}')
    if topic.notes:
        for nl in topic.notes.splitlines():
            lines.append(f'> {nl}')
    return '\n'.join(lines)


def _topic_to_md(topic, depth=0):
    """递归地将节点转换为 Markdown 缩进列表项。"""
    indent = '  ' * depth
    lines = []

    # 节点标题 + 行内元数据
    inline = []
    if topic.labels:
        inline.append('{labels: ' + ', '.join(topic.labels) + '}')
    if topic.link:
        inline.append('{link: ' + topic.link + '}')
    if topic.markers:
        inline.append('{markers: ' + ', '.join(topic.markers) + '}')

    title_line = f'{indent}- {topic.title}'
    if inline:
        title_line += '  ' + '  '.join(inline)
    lines.append(title_line)

    # 备注 → blockquote
    if topic.notes:
        for nl in topic.notes.splitlines():
            lines.append(f'{indent}  > {nl}')

    # 递归子节点
    for child in topic.children:
        lines.append(_topic_to_md(child, depth + 1))

    return '\n'.join(lines)


# ============================================================
# Markdown → 数据模型
# ============================================================

def markdown_to_sheets(md_text):
    """将 Markdown 文本解析回工作表列表。"""
    # 按 '---' 分割多个工作表
    blocks = re.split(r'\n---\n', md_text)
    sheets = []
    for block in blocks:
        sheet = _parse_sheet_block(block.strip())
        if sheet:
            sheets.append(sheet)
    return sheets


def _parse_sheet_block(block):
    """解析单个工作表块。"""
    lines = block.split('\n')

    sheet_title = 'Sheet 1'
    root_title = ''
    root_meta = []
    body_lines = []

    phase = 'init'

    for line in lines:
        stripped = line.strip()

        if not stripped:
            if phase == 'body':
                body_lines.append(line)
            continue

        if phase == 'init' and stripped.startswith('# Sheet:'):
            sheet_title = stripped[len('# Sheet:'):].strip()
            phase = 'after_sheet'
            continue

        if phase in ('init', 'after_sheet') and stripped.startswith('## '):
            root_title = stripped[3:].strip()
            phase = 'root_meta'
            continue

        if phase == 'root_meta' and stripped.startswith('>'):
            root_meta.append(stripped)
            continue

        # 进入正文
        phase = 'body'
        body_lines.append(line)

    if not root_title and not body_lines:
        return None

    sheet = Sheet(title=sheet_title)
    sheet.root_topic = Topic(title=root_title)
    _apply_block_meta(sheet.root_topic, root_meta)

    if body_lines:
        sheet.root_topic.children = _parse_md_items(body_lines)

    return sheet


def _parse_md_items(lines):
    """将缩进列表行解析为 Topic 树。"""
    items = []
    idx = 0

    while idx < len(lines):
        line = lines[idx]
        m = re.match(r'^(\s*)- (.+)$', line)
        if not m:
            idx += 1
            continue

        cur_indent = len(m.group(1))
        topic = _parse_title_meta(m.group(2))

        idx += 1
        child_lines = []
        note_lines = []

        while idx < len(lines):
            nxt = lines[idx]
            stripped = nxt.strip()

            if not stripped:
                idx += 1
                continue

            # 是否是列表项？
            nm = re.match(r'^(\s*)- ', nxt)
            if nm:
                nxt_indent = len(nm.group(1))
                if nxt_indent > cur_indent:
                    child_lines.append(nxt)
                    idx += 1
                    continue
                else:
                    break

            # 是否是备注行（blockquote）？
            bm = re.match(r'^(\s*)> (.*)$', nxt)
            if bm:
                bm_indent = len(bm.group(1))
                # 当前节点的备注：缩进恰好为 cur_indent+2，且尚未出现子节点
                if not child_lines and bm_indent == cur_indent + 2:
                    note_lines.append(bm.group(2))
                    idx += 1
                    continue
                # 属于子节点的备注或内容
                elif bm_indent > cur_indent:
                    child_lines.append(nxt)
                    idx += 1
                    continue
                else:
                    break

            # 可能是子层级的续行
            if nxt.startswith(' ' * (cur_indent + 2)):
                child_lines.append(nxt)
                idx += 1
                continue

            break

        if note_lines:
            topic.notes = '\n'.join(note_lines)
        if child_lines:
            topic.children = _parse_md_items(child_lines)

        items.append(topic)

    return items


def _parse_title_meta(raw):
    """从标题行解析行内元数据 {labels:...} {link:...} {markers:...}。"""
    topic = Topic()
    remaining = raw

    for key, attr in [('labels', 'labels'), ('link', 'link'), ('markers', 'markers')]:
        pattern = r'\{' + key + r':\s*([^}]+)\}'
        match = re.search(pattern, remaining)
        if match:
            val = match.group(1).strip()
            if key in ('labels', 'markers'):
                setattr(topic, attr, [v.strip() for v in val.split(',') if v.strip()])
            else:
                setattr(topic, attr, val)
            remaining = remaining[:match.start()] + remaining[match.end():]

    topic.title = remaining.strip()
    return topic


def _apply_block_meta(topic, meta_lines):
    """从 blockquote 行中提取元数据并应用到节点。"""
    note_parts = []
    for line in meta_lines:
        text = re.sub(r'^>\s*', '', line)
        if text.startswith('Labels:'):
            topic.labels = [v.strip() for v in text[7:].split(',') if v.strip()]
        elif text.startswith('Link:'):
            topic.link = text[5:].strip()
        elif text.startswith('Markers:'):
            topic.markers = [v.strip() for v in text[8:].split(',') if v.strip()]
        else:
            note_parts.append(text)
    if note_parts:
        topic.notes = '\n'.join(note_parts)


# ============================================================
# 创建 XMind — Zen 格式
# ============================================================

def create_zen(sheets, output_path):
    """以 Zen 格式创建 .xmind 文件。"""
    content = []
    for sheet in sheets:
        sheet_data = {
            'id': sheet.id,
            'class': 'sheet',
            'title': sheet.title,
        }
        if sheet.root_topic:
            sheet_data['rootTopic'] = _topic_to_zen_dict(sheet.root_topic)
        content.append(sheet_data)

    metadata = {
        'creator': {
            'name': 'xmind-tool',
            'version': '1.0.0',
        }
    }

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('content.json', json.dumps(content, ensure_ascii=False, indent=2))
        zf.writestr('metadata.json', json.dumps(metadata, ensure_ascii=False, indent=2))

    return output_path


def _topic_to_zen_dict(topic):
    data = {
        'id': topic.id,
        'class': 'topic',
        'title': topic.title,
    }
    if topic.notes:
        data['notes'] = {'plain': {'content': topic.notes}}
    if topic.labels:
        data['labels'] = topic.labels
    if topic.link:
        data['href'] = topic.link
    if topic.markers:
        data['markers'] = [{'markerId': m} for m in topic.markers]
    if topic.children:
        data['children'] = {
            'attached': [_topic_to_zen_dict(c) for c in topic.children]
        }
    return data


# ============================================================
# 创建 XMind — Legacy 格式 (XMind 8)
# ============================================================

_CONTENT_NS = 'urn:xmind:xmap:xmlns:content:2.0'
_XLINK_NS = 'http://www.w3.org/1999/xlink'


def _ctag(local):
    """为 Legacy XML 元素添加内容命名空间前缀。"""
    return f'{{{_CONTENT_NS}}}{local}'


def create_legacy(sheets, output_path):
    """以 Legacy (XMind 8) 格式创建 .xmind 文件。"""
    ET.register_namespace('', _CONTENT_NS)
    ET.register_namespace('xlink', _XLINK_NS)

    root = ET.Element(_ctag('xmap-content'))
    root.set('version', '2.0')

    for sheet in sheets:
        sheet_elem = ET.SubElement(root, _ctag('sheet'))
        sheet_elem.set('id', sheet.id)
        sheet_elem.set('timestamp', str(int(time.time() * 1000)))

        if sheet.root_topic:
            _topic_to_legacy_xml(sheet_elem, sheet.root_topic)

        title_elem = ET.SubElement(sheet_elem, _ctag('title'))
        title_elem.text = sheet.title

    tree = ET.ElementTree(root)

    manifest = (
        '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
        '<manifest xmlns="urn:xmind:xmap:xmlns:manifest:1.0">\n'
        '  <file-entry full-path="content.xml" media-type="text/xml"/>\n'
        '  <file-entry full-path="META-INF/" media-type=""/>\n'
        '  <file-entry full-path="META-INF/manifest.xml" media-type="text/xml"/>\n'
        '</manifest>'
    )

    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        buf = io.BytesIO()
        tree.write(buf, encoding='UTF-8', xml_declaration=True)
        zf.writestr('content.xml', buf.getvalue())
        zf.writestr('META-INF/manifest.xml', manifest)

    return output_path


def _topic_to_legacy_xml(parent, topic):
    elem = ET.SubElement(parent, _ctag('topic'))
    elem.set('id', topic.id)
    elem.set('timestamp', str(int(time.time() * 1000)))

    t = ET.SubElement(elem, _ctag('title'))
    t.text = topic.title

    if topic.notes:
        notes_e = ET.SubElement(elem, _ctag('notes'))
        plain_e = ET.SubElement(notes_e, _ctag('plain'))
        plain_e.text = topic.notes

    if topic.labels:
        labels_e = ET.SubElement(elem, _ctag('labels'))
        for lbl in topic.labels:
            le = ET.SubElement(labels_e, _ctag('label'))
            le.text = lbl

    if topic.link:
        elem.set(f'{{{_XLINK_NS}}}href', topic.link)

    if topic.markers:
        mrefs = ET.SubElement(elem, _ctag('marker-refs'))
        for mid in topic.markers:
            mr = ET.SubElement(mrefs, _ctag('marker-ref'))
            mr.set('marker-id', mid)

    if topic.children:
        children_e = ET.SubElement(elem, _ctag('children'))
        topics_e = ET.SubElement(children_e, _ctag('topics'))
        topics_e.set('type', 'attached')
        for child in topic.children:
            _topic_to_legacy_xml(topics_e, child)


# ============================================================
# 更新
# ============================================================

def update_xmind(xmind_path, md_path):
    """从修改后的 Markdown 更新已有 XMind 文件（保留原格式）。"""
    fmt = detect_format(xmind_path)

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    sheets = markdown_to_sheets(md_text)

    if fmt == 'zen':
        create_zen(sheets, xmind_path)
    else:
        create_legacy(sheets, xmind_path)

    return xmind_path


# ============================================================
# 会话记忆文件管理
# ============================================================

def get_memory_dir(session_id):
    """获取会话记忆目录: /tmp/skills-xmind-parsed/<session-id>/"""
    d = os.path.join(tempfile.gettempdir(), 'skills-xmind-parsed', session_id)
    os.makedirs(d, exist_ok=True)
    return d


def get_memory_path(session_id, xmind_path):
    """根据 session ID 和 xmind 文件路径生成对应的记忆文件路径。"""
    stem = Path(xmind_path).stem
    return os.path.join(get_memory_dir(session_id), f'{stem}.md')


# ============================================================
# CLI 入口
# ============================================================

def cmd_parse(session_id, args):
    if not args:
        print('错误：缺少 xmind 文件路径', file=sys.stderr)
        return 1

    xmind_path = args[0]
    if not os.path.exists(xmind_path):
        print(f'错误：文件不存在: {xmind_path}', file=sys.stderr)
        return 1

    fmt = detect_format(xmind_path)
    sheets = parse_zen(xmind_path) if fmt == 'zen' else parse_legacy(xmind_path)
    md = sheets_to_markdown(sheets)

    # 保存到会话记忆
    mem = get_memory_path(session_id, xmind_path)
    with open(mem, 'w', encoding='utf-8') as f:
        f.write(md)

    print(md)
    print(f'\n<!-- memory_file: {mem} -->')
    return 0


def cmd_create(session_id, args):
    if len(args) < 2:
        print('用法: xmind_tool.py --session <id> create <output.xmind> <input.md> [--format zen|legacy]', file=sys.stderr)
        return 1

    output_path = args[0]
    md_path = args[1]

    fmt = 'zen'
    if '--format' in args:
        fi = args.index('--format')
        if fi + 1 < len(args):
            fmt = args[fi + 1]

    if not os.path.exists(md_path):
        print(f'错误：Markdown 文件不存在: {md_path}', file=sys.stderr)
        return 1

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    sheets = markdown_to_sheets(md_text)
    if not sheets:
        print('错误：未能从 Markdown 中解析出任何工作表', file=sys.stderr)
        return 1

    if fmt == 'legacy':
        create_legacy(sheets, output_path)
    else:
        create_zen(sheets, output_path)

    # 更新会话记忆
    mem = get_memory_path(session_id, output_path)
    with open(mem, 'w', encoding='utf-8') as f:
        f.write(md_text)

    print(f'已创建: {output_path}')
    print(f'格式: {fmt}')
    print(f'记忆文件: {mem}')
    return 0


def cmd_update(session_id, args):
    if len(args) < 2:
        print('用法: xmind_tool.py --session <id> update <file.xmind> <modified.md>', file=sys.stderr)
        return 1

    xmind_path = args[0]
    md_path = args[1]

    if not os.path.exists(xmind_path):
        print(f'错误：XMind 文件不存在: {xmind_path}', file=sys.stderr)
        return 1
    if not os.path.exists(md_path):
        print(f'错误：Markdown 文件不存在: {md_path}', file=sys.stderr)
        return 1

    update_xmind(xmind_path, md_path)

    # 更新会话记忆
    mem = get_memory_path(session_id, xmind_path)
    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()
    with open(mem, 'w', encoding='utf-8') as f:
        f.write(md_text)

    print(f'已更新: {xmind_path}')
    print(f'记忆文件: {mem}')
    return 0


def cmd_memory(session_id, args):
    if not args:
        print('错误：缺少 xmind 文件路径', file=sys.stderr)
        return 1

    xmind_path = args[0]
    mem = get_memory_path(session_id, xmind_path)

    if os.path.exists(mem):
        with open(mem, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print(f'未找到记忆文件: {mem}', file=sys.stderr)
        print(f'请先使用 parse 命令解析对应的 xmind 文件。', file=sys.stderr)
        return 1
    return 0


def print_usage():
    print(__doc__.strip())


def main():
    argv = sys.argv[1:]

    if not argv or argv[0] in ('-h', '--help', 'help'):
        print_usage()
        sys.exit(0 if argv else 1)

    # 解析 --session 参数
    session_id = None
    if '--session' in argv:
        si = argv.index('--session')
        if si + 1 < len(argv):
            session_id = argv[si + 1]
            argv = argv[:si] + argv[si + 2:]
        else:
            print('错误：--session 需要提供会话 ID', file=sys.stderr)
            sys.exit(1)

    if not session_id:
        print('错误：缺少必填参数 --session <id>', file=sys.stderr)
        print_usage()
        sys.exit(1)

    if not argv:
        print_usage()
        sys.exit(1)

    cmd = argv[0]
    rest = argv[1:]

    dispatch = {
        'parse': cmd_parse,
        'create': cmd_create,
        'update': cmd_update,
        'memory': cmd_memory,
    }

    fn = dispatch.get(cmd)
    if fn is None:
        print(f'未知命令: {cmd}', file=sys.stderr)
        print_usage()
        sys.exit(1)

    sys.exit(fn(session_id, rest))


if __name__ == '__main__':
    main()
