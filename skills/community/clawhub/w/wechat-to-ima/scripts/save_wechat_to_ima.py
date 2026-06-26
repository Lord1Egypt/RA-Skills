#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Tag

EXTRACTOR = Path(__file__).resolve().with_name('extract.js')
SKILL_DIR = EXTRACTOR.parent.parent
IMA_SKILL_DIR = SKILL_DIR.parent / 'ima-skill'
IMA_API_SCRIPT = IMA_SKILL_DIR / 'ima_api.cjs'
KB_SCRIPT_DIR = IMA_SKILL_DIR / 'knowledge-base' / 'scripts'
COS_UPLOAD_SCRIPT = KB_SCRIPT_DIR / 'cos-upload.cjs'
IMA_BASE = 'https://ima.qq.com/openapi/note/v1'


def load_local_env():
    env_path = SKILL_DIR / '.env'
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding='utf-8').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):].strip()
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


load_local_env()


def fail(msg, code=1):
    print(json.dumps({'ok': False, 'error': msg}, ensure_ascii=False))
    raise SystemExit(code)


def check_env():
    for key, filename in [
        ('IMA_OPENAPI_CLIENTID', 'client_id'),
        ('IMA_OPENAPI_APIKEY', 'api_key'),
    ]:
        if os.environ.get(key):
            continue
        path = Path.home() / '.config' / 'ima' / filename
        if path.exists():
            os.environ[key] = path.read_text(encoding='utf-8').strip()

    missing = [k for k in ['IMA_OPENAPI_CLIENTID', 'IMA_OPENAPI_APIKEY'] if not os.environ.get(k)]
    if missing:
        fail(f"missing env: {', '.join(missing)}", 2)
    if not EXTRACTOR.exists():
        fail(f'extractor not found in skill: {EXTRACTOR}', 3)


def run_extract(url: str):
    js = f"""
const fs = require('fs');
const {{ extract }} = require('{EXTRACTOR.as_posix()}');
(async () => {{
  const result = await extract({json.dumps(url)}, {{
    shouldReturnContent: true,
    shouldReturnRawMeta: false,
    shouldFollowTransferLink: true,
    shouldExtractMpLinks: true,
    shouldExtractTags: true,
    shouldExtractRepostMeta: true,
  }});
  process.stdout.write(JSON.stringify(result));
}})().catch(err => {{
  console.error(err);
  process.exit(1);
}});
"""
    res = subprocess.run(['node', '-e', js], capture_output=True, text=True)
    if res.returncode != 0:
        fail(res.stderr.strip() or 'extract failed', 4)
    try:
        obj = json.loads(res.stdout)
    except Exception as e:
        fail(f'invalid extractor output: {e}', 5)
    if not obj.get('done'):
        fail(obj.get('msg') or f"extract failed code={obj.get('code')}", 6)
    return obj['data']


def text_of(node):
    return ' '.join(node.stripped_strings).strip()


def normalize_text(text: str):
    text = text.replace('\xa0', ' ')
    text = re.sub(r'[ \t\r\f\v]+', ' ', text)
    text = re.sub(r' *\n *', '\n', text)
    return text.strip()


def inline_markdown(node):
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ''
    name = node.name.lower()
    if name == 'br':
        return '\n'
    if name == 'img':
        return ''
    if name == 'a':
        href = node.get('href')
        title = normalize_text(''.join(inline_markdown(c) for c in node.children))
        if href and title:
            return f'[{title}]({href})'
        return title
    return ''.join(inline_markdown(c) for c in node.children)


def code_text_of(node):
    # Preserve code/newline structure instead of collapsing whitespace.
    return node.get_text('\n', strip=False).strip('\n')


def is_code_block(node):
    if not isinstance(node, Tag):
        return False
    name = node.name.lower()
    classes = ' '.join(node.get('class') or []).lower()
    style = (node.get('style') or '').lower()
    return (
        name in ['pre', 'code']
        or 'code' in classes
        or 'code-snippet' in classes
        or 'monospace' in style
        or 'font-family: monospace' in style
    )


def append_code_block(lines, node):
    code = code_text_of(node)
    if code:
        lines += ['```', code, '```', '']
    return lines


def extract_code_block(node):
    if not isinstance(node, Tag):
        return ''
    classes = set(node.get('class') or [])
    if 'code-snippet__fix' in classes or 'code-snippet__js' in classes:
        clone = BeautifulSoup(str(node), 'html.parser')
        for bad in clone.select('ul.code-snippet__line-index'):
            bad.decompose()
        inner = clone.find('pre', class_=lambda c: c and 'code-snippet__js' in c)
        if inner:
            return code_text_of(inner)
    if node.name and node.name.lower() == 'pre':
        nested_code_section = node.find('section', class_=lambda c: c and 'code-snippet__fix' in c)
        if nested_code_section:
            return ''
    return code_text_of(node)


def append_code_block(lines, node):
    code = extract_code_block(node)
    if code:
        lines += ['```', code, '```', '']
    return lines


def append_table(lines, table):
    rows = []
    for tr in table.find_all('tr'):
        cells = tr.find_all(['th', 'td'])
        if not cells:
            continue
        row = [normalize_text(text_of(cell)).replace('|', '\\|') for cell in cells]
        rows.append(row)
    if not rows:
        txt = normalize_text(text_of(table))
        if txt:
            lines += [txt, '']
        return
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    header = rows[0]
    sep = ['---'] * width
    lines.append('| ' + ' | '.join(header) + ' |')
    lines.append('| ' + ' | '.join(sep) + ' |')
    for row in rows[1:]:
        lines.append('| ' + ' | '.join(row) + ' |')
    lines.append('')


def walk_blocks(node, lines, seen, stats, inside_list=False):
    if isinstance(node, NavigableString):
        return
    if not isinstance(node, Tag):
        return

    name = node.name.lower()
    classes = set(node.get('class') or [])

    if name in {'script', 'style'}:
        return
    if name == 'img':
        src = node.get('data-src') or node.get('src')
        if src and src not in seen:
            seen.add(src)
            stats['body_img_count'] += 1
            lines += [f'![]({src})', '']
        return
    if name == 'hr':
        lines += ['---', '']
        return
    if 'code-snippet__fix' in classes or 'code-snippet__js' in classes:
        append_code_block(lines, node)
        return
    if name == 'pre':
        if node.find('section', class_=lambda c: c and 'code-snippet__fix' in c):
            for child in node.children:
                walk_blocks(child, lines, seen, stats, inside_list)
            return
        append_code_block(lines, node)
        return
    if name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
        title = normalize_text(text_of(node))
        if title:
            level = min(max(int(name[1]), 1), 6)
            lines += ['#' * level + ' ' + title, '']
        return
    if name in ['ul', 'ol']:
        idx = 1
        for li in node.find_all('li', recursive=False):
            prefix = f'{idx}. ' if name == 'ol' else '- '
            text = normalize_text(inline_markdown(li))
            if text:
                lines.append(prefix + text)
            child_imgs = li.find_all('img')
            for img in child_imgs:
                walk_blocks(img, lines, seen, stats, True)
            idx += 1
        if idx > 1:
            lines.append('')
        return
    if name == 'table':
        append_table(lines, table=node)
        return
    if name == 'blockquote':
        txt = normalize_text(inline_markdown(node))
        if txt:
            for part in txt.splitlines():
                lines.append('> ' + part)
            lines.append('')
        return

    is_container = name in ['section', 'div', 'article']
    is_para = name in ['p']

    if is_container:
        has_block_children = any(
            isinstance(c, Tag) and c.name and c.name.lower() in {
                'section', 'div', 'article', 'p', 'pre', 'ul', 'ol', 'table', 'img',
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'hr'
            }
            for c in node.children
        )
        if has_block_children:
            for child in node.children:
                walk_blocks(child, lines, seen, stats, inside_list)
            return

    if is_para or is_container or name == 'li':
        txt = normalize_text(inline_markdown(node))
        if txt:
            lines += [txt, '']
        for child in node.children:
            if isinstance(child, Tag) and child.name and child.name.lower() == 'img':
                walk_blocks(child, lines, seen, stats, inside_list)
        return

    for child in node.children:
        walk_blocks(child, lines, seen, stats, inside_list)


def build_markdown(data: dict):
    html = data.get('msg_content') or ''
    soup = BeautifulSoup(html, 'html.parser')
    lines = [
        f"# {data.get('msg_title', '未命名文章')}",
        '',
        f"> **作者**: {data.get('msg_author') or '未知'}  ",
        f"> **公众号**: {data.get('account_name') or '未知'}  ",
        f"> **发布时间**: {data.get('msg_publish_time_str') or '未知'}  ",
        f"> **原文链接**: {data.get('msg_link') or ''}",
        '',
        '---',
        ''
    ]

    seen = set()

    stats = {'body_img_count': 0}
    for node in soup.children:
        walk_blocks(node, lines, seen, stats)

    cover = data.get('msg_cover')
    cover_used = False
    if stats['body_img_count'] == 0 and cover:
        cover_used = True
        lines = lines[:9] + [f'![]({cover})', ''] + lines[9:]

    cleaned = []
    blank = False
    for line in lines:
        if line == '':
            if not blank:
                cleaned.append(line)
            blank = True
        else:
            cleaned.append(line)
            blank = False
    md = '\n'.join(cleaned).strip() + '\n'
    return md, stats['body_img_count'], cover_used


def ima_post(endpoint: str, payload: dict):
    if IMA_API_SCRIPT.exists():
        opts = json.dumps({
            'clientId': os.environ['IMA_OPENAPI_CLIENTID'],
            'apiKey': os.environ['IMA_OPENAPI_APIKEY'],
        }, ensure_ascii=False)
        res = subprocess.run(
            ['node', str(IMA_API_SCRIPT), endpoint, json.dumps(payload, ensure_ascii=False), opts],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            err = (res.stderr or '').strip()
            try:
                err_obj = json.loads(err)
                fail(f"IMA {endpoint} failed: {err_obj.get('msg') or err}", 7)
            except Exception:
                fail(f"IMA {endpoint} failed: {err or 'unknown error'}", 7)
        try:
            obj = json.loads(res.stdout)
        except Exception as e:
            fail(f"invalid IMA response for {endpoint}: {e}", 7)
        if obj.get('code') != 0:
            fail(f"IMA {endpoint} failed: {obj.get('msg')}", 7)
        return obj

    req = urllib.request.Request(
        f'{IMA_BASE}/{endpoint}',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'ima-openapi-clientid': os.environ['IMA_OPENAPI_CLIENTID'],
            'ima-openapi-apikey': os.environ['IMA_OPENAPI_APIKEY'],
            'Content-Type': 'application/json',
        },
        method='POST'
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode('utf-8')
    obj = json.loads(raw)
    if obj.get('code') != 0:
        fail(f"IMA {endpoint} failed: {obj.get('msg')}", 7)
    return obj


def resolve_knowledge_base(target: str):
    target = (target or '').strip()
    if not target:
        return None
    # allow direct kb_id
    if len(target) > 20 and ('=' in target or '-' in target or '_' in target):
        return {'kb_id': target, 'kb_name': target}

    resp = ima_post('openapi/wiki/v1/search_knowledge_base', {
        'query': target,
        'cursor': '',
        'limit': 20,
    })
    info_list = resp.get('data', {}).get('info_list', [])
    exact = [x for x in info_list if x.get('kb_name') == target]
    if len(exact) == 1:
        return exact[0]
    if len(info_list) == 1:
        return info_list[0]
    if not info_list:
        fail(f'knowledge base not found: {target}', 8)
    names = ' / '.join(x.get('kb_name', '') for x in info_list[:5])
    fail(f'knowledge base ambiguous: {target}; candidates: {names}', 8)


def safe_filename(name: str, suffix: str = '.md'):
    raw = (name or 'wechat_article').strip()
    raw = re.sub(r'[\\/:*?"<>|\r\n]+', '_', raw)
    raw = re.sub(r'\s+', ' ', raw).strip().strip('.')
    if not raw:
        raw = 'wechat_article'
    if not raw.lower().endswith(suffix):
        raw += suffix
    return raw


def ensure_unique_kb_filename(kb_id: str, file_name: str, media_type: int = 7):
    resp = ima_post('openapi/wiki/v1/check_repeated_names', {
        'params': [{'name': file_name, 'media_type': media_type}],
        'knowledge_base_id': kb_id,
    })
    items = resp.get('data', {}).get('items') or []
    repeated = False
    if items:
        repeated = bool(items[0].get('is_repeated'))
    if not repeated:
        return file_name
    stem, ext = os.path.splitext(file_name)
    return f'{stem}_{time.strftime("%Y%m%d%H%M%S")}{ext}'


def upload_markdown_to_knowledge_base(md_path: Path, kb_info: dict, title: str):
    file_name = ensure_unique_kb_filename(kb_info['kb_id'], safe_filename(title))
    file_size = md_path.stat().st_size
    create = ima_post('openapi/wiki/v1/create_media', {
        'file_name': file_name,
        'file_size': file_size,
        'content_type': 'text/markdown',
        'knowledge_base_id': kb_info['kb_id'],
        'file_ext': 'md',
    })
    data = create.get('data', {})
    media_id = data.get('media_id')
    cred = data.get('cos_credential') or {}
    if not media_id or not cred:
        fail('create_media returned incomplete upload credentials', 7)

    if not COS_UPLOAD_SCRIPT.exists():
        fail(f'COS upload script not found: {COS_UPLOAD_SCRIPT}', 7)

    upload = subprocess.run([
        'node', str(COS_UPLOAD_SCRIPT),
        '--file', str(md_path),
        '--secret-id', str(cred['secret_id']),
        '--secret-key', str(cred['secret_key']),
        '--token', str(cred['token']),
        '--bucket', str(cred['bucket_name']),
        '--region', str(cred['region']),
        '--cos-key', str(cred['cos_key']),
        '--content-type', 'text/markdown',
        '--start-time', str(cred['start_time']),
        '--expired-time', str(cred['expired_time']),
        '--timeout', '300000',
    ], capture_output=True, text=True)
    if upload.returncode != 0:
        fail(f"COS upload failed: {(upload.stderr or upload.stdout or '').strip()}", 7)

    added = ima_post('openapi/wiki/v1/add_knowledge', {
        'media_type': 7,
        'media_id': media_id,
        'title': file_name,
        'knowledge_base_id': kb_info['kb_id'],
        'file_info': {
            'cos_key': cred['cos_key'],
            'file_size': file_size,
            'file_name': file_name,
        },
    })
    return {
        'knowledge_media_id': (added.get('data') or {}).get('media_id'),
        'knowledge_file_name': file_name,
        'media_id': media_id,
    }


def main():
    if len(sys.argv) not in (2, 3):
        fail('usage: save_wechat_to_ima.py <mp.weixin.qq.com url> [knowledge_base_name_or_id]', 9)
    url = sys.argv[1].strip()
    kb_target = sys.argv[2].strip() if len(sys.argv) == 3 else ''
    check_env()
    data = run_extract(url)
    md, body_img_count, cover_used = build_markdown(data)
    safe = data.get('msg_sn') or 'wechat_article'
    md_path = Path(tempfile.gettempdir()) / f'wechat_{safe}_inline.md'
    md_path.write_text(md, encoding='utf-8')

    kb_info = None
    kb_media_id = None
    kb_file_name = None
    note_id = None
    readback_ok = None
    if kb_target:
        kb_info = resolve_knowledge_base(kb_target)
        uploaded = upload_markdown_to_knowledge_base(md_path, kb_info, data.get('msg_title') or '未命名文章')
        kb_media_id = uploaded.get('knowledge_media_id')
        kb_file_name = uploaded.get('knowledge_file_name')
    else:
        imported = ima_post('openapi/note/v1/import_doc', {'content_format': 1, 'content': md})
        note_id = imported['data']['note_id']
        readback = ima_post('openapi/note/v1/get_doc_content', {'note_id': note_id, 'target_content_format': 0})
        content = readback.get('data', {}).get('content', '')
        readback_ok = bool(content.strip())

    print(json.dumps({
        'ok': True,
        'title': data.get('msg_title'),
        'account': data.get('account_name'),
        'author': data.get('msg_author'),
        'publish_time': data.get('msg_publish_time_str'),
        'body_img_count': body_img_count,
        'cover_used': cover_used,
        'markdown_path': str(md_path),
        'note_id': note_id,
        'readback_ok': readback_ok,
        'knowledge_base_name': kb_info.get('kb_name') if kb_info else None,
        'knowledge_base_id': kb_info.get('kb_id') if kb_info else None,
        'knowledge_media_id': kb_media_id,
        'knowledge_file_name': kb_file_name,
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
